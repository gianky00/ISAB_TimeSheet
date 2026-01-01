import pytest
from unittest.mock import MagicMock, patch
from src.bots.scarico_ts.bot import ScaricaTSBot
from src.bots.carico_ts.bot import CaricoTSBot
from src.bots.timbrature.bot import TimbratureBot

class TestSpecificBots:

    @pytest.fixture
    def mock_driver(self):
        with patch('src.bots.base.base_bot.webdriver.Chrome') as mock:
            yield mock

    @patch('src.bots.base.base_bot.BaseBot._init_driver')
    def test_scarico_ts_bot_init(self, mock_init):
        # Pass credentials in kwargs
        bot = ScaricaTSBot("01.01.2025", "Fornitore", False, username="u", password="p")
        assert bot.name == "Scarico TS"
        assert bot.username == "u"
        assert bot.data_da == "01.01.2025"

    @patch('src.bots.base.base_bot.BaseBot._init_driver')
    def test_carico_ts_bot_init(self, mock_init):
        bot = CaricoTSBot(username="u", password="p")
        # The property name returns "Carico TS" (title case) in the implementation
        assert bot.name == "Carico TS"
        assert bot.username == "u"

    @patch('src.bots.base.base_bot.BaseBot._init_driver')
    def test_timbrature_bot_init(self, mock_init):
        bot = TimbratureBot(username="u", password="p")
        assert bot.name == "Timbrature"

    @patch('src.bots.base.base_bot.BaseBot._init_driver')
    def test_scarico_ts_run(self, mock_init):
        # Init bot
        bot = ScaricaTSBot("01.01.2025", "Forn", False, username="u", password="p")
        bot.driver = MagicMock()
        bot._login = MagicMock(return_value=True)
        bot.wait = MagicMock()
        bot.log = MagicMock()
        
        # Test Data
        data = [{"numero_oda": "123", "posizione_oda": "1"}]
        
        # Patch internal methods called by run
        with patch.object(bot, '_navigate_to_timesheet', return_value=True) as mock_nav, \
             patch.object(bot, '_setup_filters', return_value=True) as mock_filter, \
             patch.object(bot, '_download_excel', return_value="path/to/file.xlsx") as mock_dl, \
             patch.object(bot, '_logout', return_value=True) as mock_logout, \
             patch.object(bot, '_attendi_scomparsa_overlay'), \
             patch('src.bots.scarico_ts.bot.time.sleep'): # Mock sleep
             
             # Mock driver execute_script (for JS inputs)
             bot.driver.execute_script = MagicMock()
             
             # Execute
             result = bot.run(data)
             
             assert result is True
             mock_nav.assert_called_once()
             mock_filter.assert_called_once()
             mock_dl.assert_called_once()
             mock_logout.assert_called_once()