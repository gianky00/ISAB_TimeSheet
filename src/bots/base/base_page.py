"""
Bot TS - Base Page Object
Base class for all Page Objects with common utility methods.
"""
import time
from abc import ABC
from typing import Optional, Tuple, Callable

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from src.core.constants import Timeouts

class BasePage(ABC):
    """
    Abstract Base Class for Page Objects.
    Provides common methods for finding elements, clicking, and waiting.
    """

    # Standard timeouts mapping
    DEFAULT_TIMEOUT = Timeouts.DEFAULT
    OVERLAY_TIMEOUT = Timeouts.OVERLAY
    PAGE_LOAD_TIMEOUT = Timeouts.PAGE_LOAD

    def __init__(self, driver: WebDriver, log_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize the page.

        Args:
            driver: Selenium WebDriver instance
            log_callback: Optional function to log messages
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)
        self.long_wait = WebDriverWait(driver, self.PAGE_LOAD_TIMEOUT)
        self._log = log_callback or print

    def log(self, msg: str):
        """Log a message using the callback."""
        self._log(msg)

    def find(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        Find an element with explicit wait.

        Args:
            locator: Tuple of (By.*, "selector")
            timeout: Optional custom timeout

        Returns:
            WebElement
        """
        wait = WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT)
        return wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        Find an element that is clickable.

        Args:
            locator: Tuple of (By.*, "selector")
            timeout: Optional custom timeout

        Returns:
            WebElement
        """
        wait = WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT)
        return wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: Tuple[str, str], retry: int = 3):
        """
        Click an element with retry logic for StaleElementReferenceException.

        Args:
            locator: Tuple of (By.*, "selector")
            retry: Number of retries
        """
        for attempt in range(retry):
            try:
                element = self.find_clickable(locator)
                element.click()
                return
            except StaleElementReferenceException:
                if attempt == retry - 1:
                    raise
                time.sleep(0.5)

    def type_text(self, locator: Tuple[str, str], text: str, clear: bool = True):
        """
        Type text into an input field.

        Args:
            locator: Tuple of (By.*, "selector")
            text: Text to type
            clear: Whether to clear the field first
        """
        element = self.find(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def wait_for_overlay(self, timeout: int = None):
        """
        Wait for loading overlay to disappear.
        Defaults to Timeouts.OVERLAY if not specified.
        """
        timeout = timeout or self.OVERLAY_TIMEOUT
        # Common ExtJS mask locators used in the app
        xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(("xpath", xpath))
            )
            # Brief pause to ensure UI settles
            time.sleep(0.3)
        except TimeoutException:
            self.log("⚠️ Timeout waiting for overlay to disappear (or no overlay found).")

    def retry_on_failure(self, func: Callable, max_attempts: int = 3, delay: float = 1.0):
        """
        Retry a function if it raises an exception.

        Args:
            func: Function to execute
            max_attempts: Maximum number of attempts
            delay: Delay between attempts in seconds
        """
        last_error = None
        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                last_error = e
                if attempt < max_attempts - 1:
                    time.sleep(delay)
        raise last_error
