"""
Selenium Wait Helper Utilities
===============================
Centralizza pattern di wait comuni per eliminare time.sleep() hardcoded.

Questo modulo fornisce:
1. Wait helpers per overlay, elementi stale, file download
2. Custom Expected Conditions per casi d'uso specifici
3. Polling utilities per operazioni asincrone (es. download)

Autore: Refactoring Sprint 2026-01
"""

import logging
import time
from collections.abc import Iterable
from contextlib import suppress
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


# ============================================================================
# WAIT HELPERS
# ============================================================================


def wait_for_overlay_to_disappear(
    driver: WebDriver,
    locator: tuple[str, str],
    timeout: int = 30,
) -> bool:
    """
    Attende che un overlay di caricamento scompaia.

    Args:
        driver: Istanza WebDriver.
        locator: Tupla (By.TYPE, "selector") dell'overlay.
        timeout: Timeout massimo in secondi.

    Returns:
        True se l'overlay è scomparso, False se timeout.
    """
    try:
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located(locator))
        return True
    except TimeoutException:
        logger.warning(f"Timeout waiting for overlay: {locator}")
        return False


def wait_for_element_clickable(
    driver: WebDriver,
    locator: tuple[str, str],
    timeout: int = 10,
) -> WebElement | None:
    """
    Attende che un elemento sia cliccabile.

    Args:
        driver: Istanza WebDriver.
        locator: Tupla (By.TYPE, "selector").
        timeout: Timeout massimo in secondi.

    Returns:
        WebElement se trovato e cliccabile, None se timeout.
    """
    try:
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
    except TimeoutException:
        logger.warning(f"Element not clickable within timeout: {locator}")
        return None


# ============================================================================
# FILE POLLING UTILITIES
# ============================================================================


def poll_for_file(
    directory: Path | str,
    pattern: str = "*",
    timeout: int = 60,
    poll_interval: float = 0.5,
    min_age: float | None = None,
    exclude_patterns: list[str] | None = None,
) -> str | None:
    """
    Attende che un file appaia in una directory usando polling.
    Approccio PERMISSIVO: ritorna il file più recente che soddisfa i criteri.

    Args:
        directory: Directory da monitorare.
        pattern: Glob pattern (es: "*.xlsx").
        timeout: Timeout massimo in secondi.
        poll_interval: Intervallo tra polling in secondi.
        min_age: Timestamp minimo del file (unix timestamp). Se None, accetta qualsiasi file.
        exclude_patterns: Pattern da escludere (es: [".crdownload", ".tmp"]).

    Returns:
        Path assoluto del file più recente, o None se timeout.
    """
    directory_path = Path(directory)
    if not directory_path.exists():
        logger.error(f"Directory does not exist: {directory_path}")
        return None

    exclude_patterns = exclude_patterns or []
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Check se ci sono download in corso (crdownload, tmp, part)
        in_progress = any(any(directory_path.glob(f"*{ext}")) for ext in (".crdownload", ".tmp", ".part"))

        if in_progress:
            time.sleep(poll_interval)
            continue

        # Trova tutti i file matching
        files = list(directory_path.glob(pattern))

        # DEBUG AGGRESSIVO (Richiesto da User per Troubleshooting)
        if time.time() - start_time < 5:  # Logga solo nei primi 5 secondi per non spammare
            all_files_in_dir = list(directory_path.glob("*"))
            logger.debug(
                f"[DEBUG-POLL] Scanning '{directory_path}'. Total files: {len(all_files_in_dir)}. Matching '{pattern}': {len(files)}"
            )
            if len(all_files_in_dir) < 20:
                logger.debug(f"[DEBUG-POLL] Files: {[f.name for f in all_files_in_dir]}")

        # Filtra per esclusioni
        files = [
            f
            for f in files
            if f.is_file() and not any(f.suffix == ext or ext in f.name for ext in exclude_patterns)
        ]

        # Filtra per età minima se specificata (con tolleranza per clock skew)
        if min_age is not None:
            # Tolleranza di 5 secondi
            cutoff = min_age - 5.0
            valid_files = []
            for f in files:
                stat = f.stat()
                # Usa il massimo tra mtime e ctime per gestire casi dove il browser
                # preserva il Last-Modified del server (mtime vecchio) ma il file è appena creato (ctime nuovo)
                effective_time = max(stat.st_mtime, stat.st_ctime)

                if effective_time >= cutoff:
                    valid_files.append(f)
                else:
                    logger.debug(
                        f"Ignorato file {f.name}: effective_time={effective_time} (mtime={stat.st_mtime}, ctime={stat.st_ctime}) < cutoff={cutoff}"
                    )
            files = valid_files

        if files:
            # Ritorna il più recente basandosi sull'effective_time
            latest = max(files, key=lambda f: max(f.stat().st_mtime, f.stat().st_ctime))
            logger.info(f"File trovato: {latest.name}")
            return str(latest.absolute())

        time.sleep(poll_interval)

    logger.warning(f"Timeout polling for file in {directory_path} with pattern {pattern} (min_age={min_age})")
    return None


def poll_for_new_file(
    directory: Path | str,
    files_before: Iterable[Path | str],
    pattern: str = "*.xlsx",
    timeout: int = 120,
    poll_interval: float = 1.0,
) -> str | None:
    """
    Attende che appaia un NUOVO file rispetto a uno snapshot precedente.
    Strategia ROBUSTA: immune a timestamp errati del server.

    Args:
        directory: Directory da monitorare.
        files_before: Set di Path o stringhe (snapshot pre-click).
        pattern: Pattern glob opzionale.
        timeout: Timeout in secondi.

    Returns:
        Path del nuovo file o None.
    """
    directory_path = Path(directory)
    # Crea dizionario {path: mtime} per lo snapshot
    # Questo permette di rilevare sia NUOVI file che FILE AGGIORNATI (overwrite)
    snapshot_map: dict[Path, float] = {}
    for f_path in files_before:
        with suppress(Exception):
            p = Path(f_path)
            if not p.is_absolute():
                p = directory_path / p
            p = p.resolve()
            if p.exists():
                snapshot_map[p] = p.stat().st_mtime

    start_time = time.time()
    logger.info(f"Monitoraggio files in {directory_path} (Snapshot: {len(snapshot_map)} files)...")

    while time.time() - start_time < timeout:
        # 1. Check download in corso
        if any(directory_path.glob("*.crdownload")) or any(directory_path.glob("*.tmp")):
            time.sleep(poll_interval)
            continue

        # 2. Get current files matching pattern
        current_files = list(directory_path.glob(pattern))

        # 3. Check for New or Modified files
        detected_file = None

        for f in current_files:
            with suppress(Exception):
                f_res = f.resolve()
                if not f_res.is_file():
                    continue

                # Caso 1: File Nuovo (non era nello snapshot)
                if f_res not in snapshot_map:
                    detected_file = f_res
                    logger.info(f"✅ FILE NUOVO RILEVATO: {f_res.name}")
                    break

                # Caso 2: File Aggiornato (era nello snapshot ma mtime è cambiato)
                # Tolleranza 1 secondo
                if f_res.stat().st_mtime > snapshot_map[f_res] + 1.0:
                    detected_file = f_res
                    logger.info(f"✅ FILE AGGIORNATO RILEVATO: {f_res.name}")
                    break

        if detected_file:
            return str(detected_file)

        # Log di debug periodico (ogni 5 secondi)
        if int(time.time() - start_time) % 5 == 0:
            logger.debug(f"[POLL] Scanning... Found {len(current_files)} matches.")

        time.sleep(poll_interval)

    logger.warning("Timeout attesa nuovo file / aggiornamento.")
    return None
