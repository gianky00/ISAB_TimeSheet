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
from collections.abc import Callable, Iterable
from contextlib import suppress
from pathlib import Path
from typing import Any

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
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
        return True  # noqa: TRY300
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


def wait_for_element_staleness(driver: WebDriver, element: WebElement, timeout: int = 10) -> bool:
    """Attende che un elemento diventi stale (non più presente nel DOM)."""
    try:
        WebDriverWait(driver, timeout).until(EC.staleness_of(element))
        return True  # noqa: TRY300
    except TimeoutException:
        return False


# ============================================================================
# CUSTOM CONDITIONS
# ============================================================================


def element_text_changes(locator: tuple[str, str], old_text: str) -> Callable[[WebDriver], bool]:
    """Condition: il testo dell'elemento è diverso da quello fornito."""

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
    from selenium.common.exceptions import ElementClickInterceptedException  # noqa: PLC0415

    for i in range(retries):
        try:
            element = wait_for_element_clickable(driver, locator, timeout)
            if element:
                element.click()
                return True
        except ElementClickInterceptedException:
            logger.warning(f"Click intercettato su {locator}. Tentativo {i + 1}/{retries}...")
            time.sleep(retry_delay)
        except Exception as e:
            logger.error(f"Errore durante click su {locator}: {e}")  # noqa: TRY400
            break
    return False


def execute_with_wait(
    action: Callable[[], Any],
    driver: WebDriver,
    overlay_locator: tuple[str, str] | None = None,
    timeout: int = 30,
    wait_locator: tuple[str, str] | None = None,
) -> Any:  # noqa: ANN401
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


def poll_for_file(  # noqa: PLR0913
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
        if time.time() - start_time < 5:  # Logga solo nei primi 5 secondi per non spammare  # noqa: PLR2004
            all_files_in_dir = list(directory_path.glob("*"))
            logger.debug(
                f"[DEBUG-POLL] Scanning '{directory_path}'. Total files: {len(all_files_in_dir)}. Matching '{pattern}': {len(files)}"
            )
            if len(all_files_in_dir) < 20:  # noqa: PLR2004
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


# Alias per retrocompatibilità
poll_for_download_complete = poll_for_file
