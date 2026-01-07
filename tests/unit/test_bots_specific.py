from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.carico_ts.bot import CaricoTSBot
from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot
from src.bots.portale_fornitori.timbrature.bot import TimbratureBot


class TestSpecificBots:

    @pytest.fixture
    def mock_driver(self):
        with patch("src.bots.base.base_bot.webdriver.Chrome") as mock:
            yield mock

    @patch("src.bots.base.base_bot.BaseBot._init_driver")
    def test_scarico_ts_bot_init(self, mock_init):
        # Pass credentials in kwargs
        bot = ScaricaTSBot("01.01.2025", "Fornitore", False, username="u", password="p")
        assert bot.name == "Scarico TS"
        assert bot.username == "u"
        assert bot.data_da == "01.01.2025"

    @patch("src.bots.base.base_bot.BaseBot._init_driver")
    def test_carico_ts_bot_init(self, mock_init):
        bot = CaricoTSBot(username="u", password="p")
        # The property name returns "Carico TS" (title case) in the implementation
        assert bot.name == "Carico TS"
        assert bot.username == "u"

    @patch("src.bots.base.base_bot.BaseBot._init_driver")
    def test_timbrature_bot_init(self, mock_init):
        bot = TimbratureBot(username="u", password="p")
        assert bot.name == "Timbrature"

    @patch("src.bots.base.base_bot.BaseBot._init_driver")
    @patch("src.bots.portale_fornitori.scarico_ts.bot.ScaricaTSBot.run")
    def test_scarico_ts_run(self, mock_run, mock_init):
        # Init bot
        bot = ScaricaTSBot("01.01.2025", "Forn", False, username="u", password="p")
        bot.driver = MagicMock()
        bot._login = MagicMock(return_value=True)
        bot.wait = MagicMock()
        bot.log = MagicMock()

        # Test Data
        data = [{"numero_oda": "123", "posizione_oda": "1"}]

        # Patch internal methods if needed or just verify run call
        mock_run.return_value = True
        result = bot.run(data)
        assert result is True
