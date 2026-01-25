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
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
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
    locator: Tuple[By, str],
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
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located(locator)  # type: ignore[arg-type]
        )
        return True
    except TimeoutException:
        logger.warning(f"Timeout waiting for overlay: {locator}")
        return False


def wait_for_element_staleness(
    driver: WebDriver,
    element: WebElement,
    timeout: int = 10,
) -> bool:
    """
    Attende che un elemento diventi stale (rimosso dal DOM).

    Utile dopo click che causano refresh/navigazione.

    Args:
        driver: Istanza WebDriver.
        element: Elemento da monitorare.
        timeout: Timeout massimo in secondi.

    Returns:
        True se l'elemento è diventato stale.
    """
    try:
        WebDriverWait(driver, timeout).until(EC.staleness_of(element))
        return True
    except TimeoutException:
        logger.warning("Element did not become stale within timeout")
        return False


def wait_for_element_clickable(
    driver: WebDriver,
    locator: Tuple[By, str],
    timeout: int = 10,
) -> Optional[WebElement]:
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
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))  # type: ignore[arg-type]
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
    min_age: Optional[float] = None,
    exclude_patterns: Optional[List[str]] = None,
) -> Optional[str]:
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
    directory = Path(directory)
    if not directory.exists():
        logger.error(f"Directory does not exist: {directory}")
        return None

    exclude_patterns = exclude_patterns or []
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Check se ci sono download in corso (crdownload, tmp, part)
        in_progress = any(
            directory.glob(f"*{ext}") for ext in [".crdownload", ".tmp", ".part"]
        )

        if in_progress:
            time.sleep(poll_interval)
            continue

        # Trova tutti i file matching
        files = list(directory.glob(pattern))

        # Filtra per esclusioni
        files = [
            f
            for f in files
            if f.is_file()
            and not any(f.suffix == ext or ext in f.name for ext in exclude_patterns)
        ]

        # Filtra per età minima se specificata
        if min_age is not None:
            files = [f for f in files if f.stat().st_mtime > min_age]

        if files:
            # Ritorna il più recente
            latest = max(files, key=lambda f: f.stat().st_mtime)
            logger.debug(f"Found file: {latest.name}")
            return str(latest.absolute())

        time.sleep(poll_interval)

    logger.warning(f"Timeout polling for file in {directory} with pattern {pattern}")
    return None


def poll_for_download_complete(
    download_dir: Path | str,
    pattern: str,
    timeout: int = 120,
    poll_interval: float = 1.0,
) -> Optional[str]:
    """
    Attende che un download sia completato (no .crdownload/.tmp).

    Versione semplificata di poll_for_file specifica per Chrome downloads.

    Args:
        download_dir: Directory download di Chrome.
        pattern: Glob pattern del file finale (es: "Ricerca*.xlsx").
        timeout: Timeout massimo in secondi.
        poll_interval: Intervallo tra polling in secondi.

    Returns:
        Path assoluto del file scaricato, o None se timeout.
    """
    return poll_for_file(
        directory=download_dir,
        pattern=pattern,
        timeout=timeout,
        poll_interval=poll_interval,
        exclude_patterns=[".crdownload", ".tmp", ".part"],
    )


# ============================================================================
# CUSTOM EXPECTED CONDITIONS
# ============================================================================


class element_text_changes:
    """
    Expected Condition: attende che il testo di un elemento cambi.

    Utile per monitorare contatori, progress indicator, etc.

    Example:
        >>> wait = WebDriverWait(driver, 10)
        >>> wait.until(element_text_changes((By.ID, "counter"), "0"))
    """

    def __init__(self, locator: Tuple[By, str], initial_text: str):
        self.locator = locator
        self.initial_text = initial_text

    def __call__(self, driver: WebDriver) -> bool:
        try:
            element = driver.find_element(*self.locator)
            return element.text != self.initial_text
        except Exception:
            return False


class alert_appears_with_text:
    """
    Expected Condition: attende alert con testo specifico.

    Example:
        >>> wait = WebDriverWait(driver, 5)
        >>> wait.until(alert_appears_with_text("Operazione completata"))
    """

    def __init__(self, expected_text: str):
        self.expected_text = expected_text

    def __call__(self, driver: WebDriver) -> bool:
        try:
            alert = driver.switch_to.alert
            return self.expected_text in alert.text
        except Exception:
            return False


class element_count_is:
    """
    Expected Condition: attende un numero specifico di elementi.

    Utile per table rows, list items, etc.

    Example:
        >>> wait = WebDriverWait(driver, 10)
        >>> # Attende che ci siano almeno 10 righe nella tabella
        >>> wait.until(element_count_is((By.CSS_SELECTOR, "table tr"), min_count=10))
    """

    def __init__(
        self,
        locator: Tuple[By, str],
        exact_count: Optional[int] = None,
        min_count: Optional[int] = None,
        max_count: Optional[int] = None,
    ):
        self.locator = locator
        self.exact_count = exact_count
        self.min_count = min_count
        self.max_count = max_count

    def __call__(self, driver: WebDriver) -> bool:
        try:
            elements = driver.find_elements(*self.locator)
            count = len(elements)

            if self.exact_count is not None:
                return count == self.exact_count
            if self.min_count is not None and count < self.min_count:
                return False
            if self.max_count is not None and count > self.max_count:
                return False
            return True
        except Exception:
            return False


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def safe_click_with_retry(
    driver: WebDriver,
    locator: Tuple[By, str],
    timeout: int = 10,
    retries: int = 3,
    retry_delay: float = 0.5,
) -> bool:
    """
    Clicca su un elemento con retry automatico.

    Gestisce casi di ElementClickInterceptedException (overlay, animazioni).

    Args:
        driver: Istanza WebDriver.
        locator: Tupla (By.TYPE, "selector").
        timeout: Timeout per ogni tentativo.
        retries: Numero massimo di tentativi.
        retry_delay: Pausa tra i tentativi.

    Returns:
        True se il click ha avuto successo.
    """
    from selenium.common.exceptions import ElementClickInterceptedException

    for attempt in range(retries):
        try:
            element = wait_for_element_clickable(driver, locator, timeout)
            if element:
                element.click()
                return True
        except ElementClickInterceptedException:
            logger.warning(f"Click intercepted, retry {attempt + 1}/{retries}")
            time.sleep(retry_delay)
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return False

    logger.error(f"Failed to click {locator} after {retries} retries")
    return False


def execute_with_wait(
    action: Callable[[], None],
    driver: WebDriver,
    wait_locator: Optional[Tuple[By, str]] = None,
    wait_timeout: int = 10,
) -> bool:
    """
    Esegue un'azione e attende una condizione.

    Helper per pattern comune: click → wait overlay disappear.

    Args:
        action: Funzione da eseguire (es: lambda: button.click()).
        driver: Istanza WebDriver.
        wait_locator: Locator da attendere (invisibility).
        wait_timeout: Timeout per il wait.

    Returns:
        True se l'azione e il wait hanno successo.

    Example:
        >>> execute_with_wait(
        ...     action=lambda: driver.find_element(By.ID, "submit").click(),
        ...     driver=driver,
        ...     wait_locator=(By.CLASS_NAME, "loading-overlay")
        ... )
    """
    try:
        action()
        if wait_locator:
            return wait_for_overlay_to_disappear(driver, wait_locator, wait_timeout)
        return True
    except Exception as e:
        logger.error(f"Action failed: {e}")
        return False
