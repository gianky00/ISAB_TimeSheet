from src.core import constants

class TestConstantsCoverage:
    """Test suite per src/core/constants.py"""

    def test_urls(self):
        """Test URL constants."""
        assert constants.URLs.ISAB_PORTAL.startswith("https://")
        assert constants.URLs.UPDATE_URL.startswith("https://")

    def test_timeouts(self):
        """Test timeout values."""
        assert isinstance(constants.Timeouts.DEFAULT, int)
        assert constants.Timeouts.DEFAULT > 0
        assert constants.Timeouts.SHORT < constants.Timeouts.LONG
        assert constants.Timeouts.PAGE_LOAD > 0

    def test_bot_status_enum(self):
        """Test BotStatus enum values."""
        assert constants.BotStatus.IDLE.value == "idle"
        assert constants.BotStatus.ERROR.value == "error"
        assert constants.BotStatus.RUNNING in constants.BotStatus
        assert len(constants.BotStatus) >= 5

    def test_browser_config(self):
        """Test Browser configuration."""
        assert "1920" in constants.BrowserConfig.WINDOW_SIZE
        assert "Mozilla" in constants.BrowserConfig.USER_AGENT
        assert constants.BrowserConfig.CACHE_DIR_NAME == "chrome_profile"
