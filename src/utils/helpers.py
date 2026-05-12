"""
SyncroJob - Utility Helpers
Funzioni di utilit  generali per la gestione del filesystem, formattazione dati e cleanup processi.
Include una robusta logica di terminazione per processi Chrome/Chromedriver "zombie".
"""

import logging
import os
import re
import subprocess
import sys
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path

import psutil
from PySide6.QtGui import QColor, QIcon, QImage, QPainter, QPixmap

from src.core.constants import BrowserConfig
from src.core.paths import CONFIG_DIR
from src.utils.resource_manager import ResourceManager

# --- GLOBAL ICON CACHE ---
# Memorizza le QPixmap colorate per evitare re-rendering SVG costosi (15-30ms risparmiati per icona)
_ICON_CACHE: dict[str, QPixmap] = {}


def get_asset_path(relative_path: str) -> str:
    """
    Restituisce il percorso assoluto di un asset.
    Funziona sia in sviluppo che nell'app installata.
    Utilizza ResourceManager come fonte unica di verit .
    """
    return ResourceManager.get_asset_path(relative_path)


def get_app_icon_path() -> str | None:
    """Restituisce il percorso dell'icona dell'applicazione."""
    icon_path = get_asset_path("assets/app.ico")

    if Path(icon_path).exists():
        return icon_path
    return None


def setup_logging(name: str = "BotTS", log_file: str | None = None) -> logging.Logger:
    """
    Configura il sistema di logging.

    Args:
      name: Nome del logger
      log_file: Percorso opzionale per file di log

    Returns:
      Logger configurato
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (opzionale)
        if log_file:
            try:
                file_handler = logging.FileHandler(log_file, encoding="utf-8")
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                logger.warning(f"Impossibile creare file di log: {e}")

    return logger


def format_timestamp(dt: datetime | None = None) -> str:
    """
    Formatta un timestamp per la visualizzazione.

    Args:
      dt: Datetime da formattare (default: now)

    Returns:
      Stringa formattata
    """
    return (dt or datetime.now(UTC).astimezone()).strftime("%d/%m/%Y %H:%M:%S")


def get_months_list() -> list[str]:
    """Restituisce la lista dei mesi in italiano."""
    return [
        "Gennaio",
        "Febbraio",
        "Marzo",
        "Aprile",
        "Maggio",
        "Giugno",
        "Luglio",
        "Agosto",
        "Settembre",
        "Ottobre",
        "Novembre",
        "Dicembre",
    ]


def get_years_list(start_offset: int = -2, end_offset: int = 2) -> list[str]:
    """
    Restituisce una lista di anni intorno a quello corrente.

    Args:
      start_offset: Offset dall'anno corrente per l'inizio.
      end_offset: Offset dall'anno corrente per la fine.

    Returns:
      Lista di anni come stringhe.
    """
    current_year = datetime.now(UTC).astimezone().year
    return [str(year) for year in range(current_year + start_offset, current_year + end_offset + 1)]


def is_windows() -> bool:
    """Verifica se il sistema operativo corrente  Windows."""
    return sys.platform.startswith("win")


def safe_open(path: str | Path) -> bool:
    """
    Apre un file o una cartella nel programma predefinito in modo sicuro.
    Previene l'esecuzione di binari pericolosi tramite blacklist.

    Args:
      path: Percorso del file o della cartella.

    Returns:
      bool: True se aperto correttamente.
    """
    path_obj = Path(path).resolve()
    if not path_obj.exists():
        return False

    # Prevenzione esecuzione binari
    if path_obj.suffix.lower() in (".exe", ".bat", ".cmd", ".msi", ".ps1", ".vbs"):
        return False

    try:
        if is_windows():
            os.startfile(str(path_obj))  # noqa: S606
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path_obj)], check=False)
        else:
            subprocess.run(["xdg-open", str(path_obj)], check=False)
    except Exception:
        return False
    else:
        return True


def open_folder(path: str) -> bool:
    """Legacy wrapper for safe_open."""
    return safe_open(path)


def safe_str(value: object, default: str = "") -> str:
    """
    Esegue una conversione sicura a stringa gestendo i valori None.
    """
    return str(value) if value is not None else default


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Tronca una stringa se supera la lunghezza specificata.
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def sanitize_filename(filename: str) -> str:
    """
    Sanitizza una stringa per renderla sicura come nome file (previene Path Traversal).
    """
    if not filename:
        return "unnamed_file"

    filename = filename.replace("\0", "")
    # Whitelist: Alfanumerici, underscore, trattino, punto, parentesi, spazi.
    safe_filename = re.sub(r"[^a-zA-Z0-9_\-\.\(\)\[\] ]", "_", filename)
    safe_filename = re.sub(r"_+", "_", safe_filename)
    safe_filename = re.sub(r"\.+", ".", safe_filename).strip(" .")

    return safe_filename or "unnamed_file"


def cleanup_chrome_temp_files(directory: Path | str) -> list[str]:
    """
    Rimuove file da 0 KB nella directory (residui di download Selenium falliti).
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []

    removed = []
    try:
        for f in dir_path.iterdir():
            if f.is_file() and f.stat().st_size == 0:
                with suppress(Exception):
                    f.unlink()
                    removed.append(f.name)
    except Exception as e:
        logging.getLogger(__name__).warning(f"Error during temp cleanup: {e}")
    return removed


def cleanup_bot_processes() -> None:
    """
    Termina forzatamente le istanze 'zombiè di Chrome e Chromedriver legate all'applicazione.
    Rimuove i file di lock del profilo per prevenire errori di sessione (SessionNotCreated).
    Include anche processi Playwright/Node se rimasti appesi.
    """
    cleanup_logger = logging.getLogger("Cleanup")

    # 1. Terminazione Chromedriver e Binari Playwright
    _kill_zombie_drivers(cleanup_logger)

    # 2. Terminazione Chrome (Solo se utilizza il profilo dedicato di SyncroJob o se  orfano)
    _kill_automation_browsers(cleanup_logger)

    # 3. Rimozione file di lock nel profilo
    _remove_profile_locks(cleanup_logger)


def _kill_zombie_drivers(logger: logging.Logger) -> None:
    """Termina i driver e i processi di runtime appesi."""
    target_procs = ["chromedriver.exe", "msedge.exe", "playwright.exe", "node.exe"]
    for proc in psutil.process_iter(["name", "cmdline"]):
        with suppress(Exception):
            pname = proc.info["name"]
            if any(tp.lower() == pname.lower() for tp in target_procs):
                # Se  node o playwright, verifichiamo che sia della nostra app
                cmdline = " ".join(proc.info["cmdline"] or [])
                if pname.lower() in ("node.exe", "playwright.exe") and "playwright" not in cmdline.lower():
                    continue
                proc.kill()
                logger.info(f"Terminated zombie process: {pname}")


def _kill_automation_browsers(logger: logging.Logger) -> None:
    """Termina le istanze di Chrome legate all'automazione."""
    profile_dir = BrowserConfig.CACHE_DIR_NAME
    for proc in psutil.process_iter(["name", "cmdline"]):
        with suppress(Exception):
            if proc.info["name"] == "chrome.exe":
                cmdline = " ".join(proc.info["cmdline"] or [])
                # Terminiamo solo processi che puntano al nostro profilo o che hanno flag di automazione
                if profile_dir in cmdline or "remote-debugging-port" in cmdline:
                    proc.kill()
                    logger.info(f"Terminated automation chrome instance (PID: {proc.pid})")


def _remove_profile_locks(logger: logging.Logger) -> None:
    """Rimuove i file di lock dal profilo utente per evitare errori di sessione."""
    profile_path = CONFIG_DIR / "data" / BrowserConfig.CACHE_DIR_NAME
    lock_files = [
        "SingletonLock",
        "SingletonSocket",
        "SingletonCookie",
        "DevToolsActivePort",
        "Lock",
        "LOCK",
    ]

    if profile_path.exists():
        for lock_file in lock_files:
            f_path = profile_path / lock_file
            if f_path.exists():
                with suppress(Exception):
                    f_path.unlink()
                    logger.info(f"Removed stale lock file: {lock_file}")
            # Cerca anche in sottocartelle comuni (es. Local State)
            for sub in ("Default", "Network"):
                f_sub_path = profile_path / sub / lock_file
                if f_sub_path.exists():
                    with suppress(Exception):
                        f_sub_path.unlink()
                        logger.info(f"Removed stale lock file in {sub}: {lock_file}")


def get_colored_icon(icon_path: str, color: str = "#000000") -> QIcon:
    """
    Applica un colore personalizzato a un'icona SVG tramite QPainter.
    Implementa un sistema di caching per massimizzare le performance di rendering.
    """
    if not Path(icon_path).exists():
        return QIcon()

    # Genera chiave unica per la cache
    cache_key = f"{icon_path}_{color}"
    if cache_key in _ICON_CACHE:
        return QIcon(_ICON_CACHE[cache_key])

    # Se non in cache, renderizza l'immagine
    image = QImage(icon_path)
    if image.isNull():
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            return QIcon()
        image = pixmap.toImage()

    painter = QPainter(image)
    try:
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(image.rect(), QColor(color))
    finally:
        painter.end()

    # Salva in cache come Pixmap (piùveloce per Qt da visualizzare)
    pixmap = QPixmap.fromImage(image)
    _ICON_CACHE[cache_key] = pixmap

    return QIcon(pixmap)


def clear_icon_cache() -> None:
    """Svuota la cache delle icone per liberare memoria."""
    _ICON_CACHE.clear()
