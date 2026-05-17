from selenium.webdriver.common.by import By

from src.bots.base.playwright_utils import get_playwright_selector


class TestPlaywrightUtils:
    def test_get_playwright_selector_basic(self):
        assert get_playwright_selector((By.ID, "myid")) == "#myid"
        assert get_playwright_selector((By.NAME, "myname")) == '[name="myname"]'
        assert get_playwright_selector((By.CLASS_NAME, "class1 class2")) == ".class1.class2"
        assert get_playwright_selector((By.CSS_SELECTOR, "div > span")) == "div > span"

    def test_get_playwright_selector_xpath(self):
        assert get_playwright_selector((By.XPATH, "//div")) == "xpath=//div"
        assert get_playwright_selector((By.ID, "//div")) == "xpath=//div"  # Auto-detection
        assert get_playwright_selector((By.NAME, "(//div)[1]")) == "xpath=(//div)[1]"

    def test_get_playwright_selector_already_prefixed(self):
        assert get_playwright_selector((By.ID, "xpath=//div")) == "xpath=//div"
        assert get_playwright_selector((By.NAME, "id=something")) == "id=something"
        assert get_playwright_selector((By.CLASS_NAME, "text=Login")) == "text=Login"
