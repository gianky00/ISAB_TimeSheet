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

import time
from collections.abc import Callable, Iterable
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from src.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PollConfig:
    """Configurazione per il polling di file."""

    directory: Path | str
    pattern: str | list[str] = "*.xlsx"
    timeout: int = 120
    poll_interval: float = 1.0


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
      True se l'overlay  scomparso, False se timeout.
    """
    try:
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located(locator))
    except TimeoutException:
        logger.warning(f"Timeout waiting for overlay: {locator}")
        return False
    else:
        return True


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


def wait_for_element_staleness(driver: WebDriver, element: WebElement, timeout: int = 10) -> bool:
    """Attende che un elemento diventi stale (non più presente nel DOM)."""
    try:
        WebDriverWait(driver, timeout).until(EC.staleness_of(element))
    except TimeoutException:
        return False
    else:
        return True


# ============================================================================
# CUSTOM CONDITIONS
# ============================================================================


def element_text_changes(locator: tuple[str, str], old_text: str) -> Callable[[WebDriver], bool]:
    """Condition: il testo dell'elemento  diverso da quello fornito."""

    def _predicate(driver: WebDriver) -> bool:
        try:
            element = driver.find_element(*locator)
            return element.text.strip() != old_text.strip()
        except Exception:
            return True  # Se sparisce, consideriamo il testo cambiato

    return _predicate


def element_count_is(
    locator: tuple[str, str],
    exact_count: int | None = None,
    min_count: int | None = None,
    max_count: int | None = None,
) -> Callable[[WebDriver], bool]:
    """Condition: verifica il numero di elementi trovati."""

    def _predicate(driver: WebDriver) -> bool:
        elements = driver.find_elements(*locator)
        count = len(elements)
        if exact_count is not None:
            return count == exact_count
        if min_count is not None:
            if max_count is not None:
                return min_count <= count <= max_count
            return count >= min_count
        if max_count is not None:
            return count <= max_count
        return True

    return _predicate


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def safe_click_with_retry(
    driver: WebDriver,
    locator: tuple[str, str],
    retries: int = 3,
    retry_delay: float = 1.0,
    timeout: int = 10,
) -> bool:
    """
    Tenta il click su un elemento gestendo overlay e intercettazioni temporanee.
    """

    for i in range(retries):
        try:
            element = wait_for_element_clickable(driver, locator, timeout)
            if element:
                element.click()
                return True
        except ElementClickInterceptedException:
            logger.warning(f"Click intercettato su {locator}. Tentativo {i + 1}/{retries}...")
            time.sleep(retry_delay)
        except Exception:
            logger.exception("Errore durante click", locator=locator)
            break
    return False


def execute_with_wait(
    action: Callable[[], Any],
    driver: WebDriver,
    overlay_locator: tuple[str, str] | None = None,
    timeout: int = 30,
    wait_locator: tuple[str, str] | None = None,
) -> Any:
    """
    Esegue un'azione e attende la scomparsa di un overlay.
    Supporta sia overlay_locator che wait_locator (alias).
    """
    locator = wait_locator or overlay_locator
    result = action()
    if locator:
        wait_for_overlay_to_disappear(driver, locator, timeout)
    return result


# ============================================================================
# FILE POLLING UTILITIES
# ============================================================================


from src.bots.base.file_polling_params import FilePollingParams  # noqa: E402

# ... (rest of imports)


def poll_for_file(params: FilePollingParams) -> str | None:
    """
    Attende che un file appaia in una directory usando polling.
    Approccio PERMISSIVO: ritorna il file più recente che soddisfa i criteri.

    Args:
      params: Oggetto FilePollingParams con i parametri di polling.

    Returns:
      Path assoluto del file più recente, o None se timeout.
    """
    directory_path = Path(params.directory)
    if not directory_path.exists():
        logger.error(f"Directory does not exist: {directory_path}")
        return None

    exclude_patterns = params.exclude_patterns or []
    start_time = time.time()

    while time.time() - start_time < params.timeout:
        if _is_any_download_in_progress(directory_path):
            time.sleep(params.poll_interval)
            continue

        files = list(directory_path.glob(params.pattern))
        _log_debug_poll_info(directory_path, params.pattern, files, start_time)

        valid_files = _filter_valid_files(files, exclude_patterns, params.min_age)

        if valid_files:
            # Ritorna il più recente basandosi sull'effective_time
            latest = max(valid_files, key=lambda f: max(f.stat().st_mtime, f.stat().st_ctime))
            logger.info(f"File trovato: {latest.name}")
            return str(latest.absolute())

        time.sleep(params.poll_interval)

    logger.warning(
        f"Timeout polling for file in {directory_path} with pattern {params.pattern} "
        f"(min_age={params.min_age})"
    )
    return None


def _is_any_download_in_progress(directory: Path) -> bool:
    """Check se ci sono download in corso basandosi sulle estensioni comuni."""
    temp_exts = (".crdownload", ".tmp", ".part")
    return any(any(directory.glob(f"*{ext}")) for ext in temp_exts)


def _log_debug_poll_info(directory: Path, pattern: str, matches: list[Path], start_time: float) -> None:
    """Logga informazioni di debug nei primi secondi di polling."""
    debug_threshold_sec = 5
    max_files_to_log = 20

    if time.time() - start_time < debug_threshold_sec:
        all_files = list(directory.glob("*"))
        logger.debug(
            f"[DEBUG-POLL] Scanning '{directory}'. Total files: {len(all_files)}. Matching '{pattern}': {len(matches)}"
        )
        if len(all_files) < max_files_to_log:
            logger.debug(f"[DEBUG-POLL] Files: {[f.name for f in all_files]}")


def _filter_valid_files(files: list[Path], excludes: list[str], min_age: float | None) -> list[Path]:
    """Filtra i file basandosi su esclusioni e età minima."""
    # 1. Filtra per esclusioni e se è un file reale
    filtered = [
        f for f in files if f.is_file() and not any(f.suffix == ext or ext in f.name for ext in excludes)
    ]

    if min_age is None:
        return filtered

    # 2. Filtra per età minima con tolleranza (5 secondi) per clock skew
    clock_skew_tolerance_sec = 5.0
    cutoff = min_age - clock_skew_tolerance_sec
    valid = []
    for f in filtered:
        stat = f.stat()
        # Usa il massimo tra mtime e ctime per gestire casi dove il browser
        # preserva il Last-Modified del server (mtime vecchio) ma il file è appena creato (ctime nuovo)
        effective_time = max(stat.st_mtime, stat.st_ctime)
        if effective_time >= cutoff:
            valid.append(f)
        else:
            logger.debug(
                f"Ignorato file {f.name}: effective_time={effective_time} (mtime={stat.st_mtime}, ctime={stat.st_ctime}) < cutoff={cutoff}"
            )
    return valid


def poll_for_new_file(config: PollConfig, files_before: Iterable[Path | str]) -> str | None:
    """
    Attende che appaia un NUOVO file rispetto a uno snapshot precedente.
    Supporta pattern multipli e ignora file temporanei pre-esistenti.
    """
    directory_path = Path(config.directory)
    snapshot_map = _create_snapshot_map(directory_path, files_before)
    patterns = [config.pattern] if isinstance(config.pattern, str) else config.pattern

    start_time = time.time()
    logger.info(
        f"Monitoraggio files in {directory_path} (Snapshot: {len(snapshot_map)} files, Patterns: {patterns})..."
    )

    temp_snapshot = _get_temp_files_snapshot(directory_path)

    while time.time() - start_time < config.timeout:
        try:
            if _is_download_in_progress(directory_path, temp_snapshot, start_time):
                time.sleep(config.poll_interval)
                continue

            detected_file = _detect_new_or_modified_file(directory_path, patterns, snapshot_map)
            if detected_file:
                return str(detected_file)

            _log_polling_status(directory_path, patterns, start_time)

        except Exception as e:
            logger.debug(f"Errore durante scansione: {e}")

        time.sleep(config.poll_interval)

    logger.warning(
        f"Timeout attesa nuovo file in {directory_path} (Pattern: {patterns}, Timeout: {config.timeout}s)."
    )
    return None


def _create_snapshot_map(directory: Path, files: Iterable[Path | str]) -> dict[Path, float]:
    """Crea una mappa {Path: mtime} per i file esistenti."""
    snapshot_map: dict[Path, float] = {}
    for f_path in files:
        with suppress(Exception):
            p = Path(f_path)
            if not p.is_absolute():
                p = directory / p
            p = p.resolve()
            if p.exists():
                snapshot_map[p] = p.stat().st_mtime
    return snapshot_map


def _get_temp_files_snapshot(directory: Path) -> set[str]:
    """Ritorna i nomi dei file temporanei correntemente presenti."""
    temp_exts = (".crdownload", ".tmp", ".part")
    return {
        f.name.lower() for f in directory.iterdir() if any(f.name.lower().endswith(ext) for ext in temp_exts)
    }


def _is_download_in_progress(directory: Path, initial_temp_snapshot: set[str], start_time: float) -> bool:
    """Verifica se ci sono nuovi file temporanei che indicano un download in corso."""
    log_interval_sec = 5
    current_temps = _get_temp_files_snapshot(directory)
    new_temps = current_temps - initial_temp_snapshot
    if new_temps:
        if int(time.time() - start_time) % log_interval_sec == 0:
            logger.debug(f"[POLL] Download in corso: {list(new_temps)}")
        return True
    return False


def _detect_new_or_modified_file(
    directory: Path, patterns: list[str], snapshot_map: dict[Path, float]
) -> Path | None:
    """Cerca un file nuovo o modificato rispetto allo snapshot."""
    mtime_tolerance_sec = 1.0
    for p_str in patterns:
        for f in directory.glob(p_str):
            with suppress(Exception):
                f_res = f.resolve()
                if not f_res.is_file():
                    continue

                # Caso 1: File Nuovo (non era nello snapshot)
                if f_res not in snapshot_map:
                    logger.info(f"✅ FILE NUOVO RILEVATO: {f_res.name}")
                    return f_res

                # Caso 2: File Aggiornato (mtime cambiato > 1s)
                if f_res.stat().st_mtime > snapshot_map[f_res] + mtime_tolerance_sec:
                    logger.info(f"✅ FILE AGGIORNATO RILEVATO: {f_res.name}")
                    return f_res
    return None


def _log_polling_status(directory: Path, patterns: list[str], start_time: float) -> None:
    """Logga periodicamente lo stato della scansione."""
    log_status_interval_sec = 10
    if int(time.time() - start_time) % log_status_interval_sec == 0:
        # Conteggio approssimativo per il log
        count = sum(len(list(directory.glob(p))) for p in patterns)
        logger.debug(f"[POLL] Scanning {directory}... Matches: {count}")


# Alias per retrocompatibilit
poll_for_download_complete = poll_for_file
