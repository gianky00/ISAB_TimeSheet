from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.base_bot import BaseBot
from src.core.constants import BotStatus


class DummyBot(BaseBot):
    @property
    def name(self): return "Dummy"
    @property
    def description(self): return "Desc"
    def run(self, data): return True

class TestBaseBotOrchestration:
    @pytest.fixture
    def bot(self):
        return DummyBot(username="user", password="pw")

    @patch("src.bots.base.base_bot.webdriver.Chrome")
    @patch("src.bots.base.base_bot.ChromeDriverManager")
    def test_init_driver_options(self, mock_dm, mock_chrome, bot):
        mock_dm.return_value.install.return_value = "chromedriver.exe"
        bot._init_driver()
        assert mock_chrome.called
        assert bot.driver is not None

    def test_execute_full_flow(self, bot):
        with patch.object(bot, "_safe_login_with_retry", return_value=True), \
             patch.object(bot, "run", return_value=True), \
             patch.object(bot, "cleanup"):

            result = bot.execute([{"data": "test"}])
            assert result is True
            assert bot.status == BotStatus.COMPLETED

    def test_save_error_state(self, bot, tmp_path):
        bot.driver = MagicMock()
        bot.driver.page_source = "<html>Error</html>"

        # Patching datetime where it's used
        with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
            # We don't patch datetime to avoid AttributeError if it's imported as class
            # We just let it run and check if files are created in tmp_path
            bot._save_error_state("Something went wrong")

            error_dir = tmp_path / "logs" / "errors"
            assert error_dir.exists()
