from selenium.webdriver.common.by import By

from src.bots.portale_fornitori.common.locators import CommonLocators, LoginLocators
from src.bots.portale_fornitori.scarico_ts.locators import ScaricoTSLocators


class TestBotLocators:
    def _check_locators(self, locator_class):
        """Helper to check all attributes of a locator class."""
        for attr_name in dir(locator_class):
            if attr_name.startswith("__") or callable(
                getattr(locator_class, attr_name)
            ):
                continue

            locator = getattr(locator_class, attr_name)
            assert isinstance(locator, tuple), f"{attr_name} should be a tuple"
            assert len(locator) == 2, f"{attr_name} should have 2 elements"
            assert locator[0] in [
                By.ID,
                By.XPATH,
                By.LINK_TEXT,
                By.PARTIAL_LINK_TEXT,
                By.NAME,
                By.TAG_NAME,
                By.CLASS_NAME,
                By.CSS_SELECTOR,
            ], f"{attr_name} invalid By type"
            assert isinstance(
                locator[1], str
            ), f"{attr_name} selector should be a string"

    def test_login_locators_structure(self):
        self._check_locators(LoginLocators)

    def test_common_locators_structure(self):
        self._check_locators(CommonLocators)

    def test_scarico_ts_locators_structure(self):
        self._check_locators(ScaricoTSLocators)
