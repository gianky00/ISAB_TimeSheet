from unittest.mock import MagicMock, patch

from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot


class TestScaricoTSBotDeep:
    def test_bot_workflow_simulation(self):
        bot = ScaricaTSBot(username="u", password="p", data_da="01.01.2024", fornitore="F1")

        # Mock Selenium dependencies and internal wait
        with patch.object(bot, "_init_driver"), \
             patch.object(bot, "_safe_login_with_retry", return_value=True), \
             patch.object(bot, "cleanup"):

            bot.wait = MagicMock()
            bot.driver = MagicMock()

            # Mock internal navigation methods
            with patch.object(bot, "_navigate_to_timesheet", return_value=True), \
                 patch.object(bot, "_setup_filters", return_value=True), \
                 patch.object(bot, "_download_excel", return_value=True):

                # Run the simulation
                res = bot.run([{"numero_oda": "123"}])
                assert res is True

    def test_validate_data_failure(self):
        bot = ScaricaTSBot(username="u", password="p", fornitore="")
        # Provide data to trigger fornitore check
        valid, msg = bot.validate_data([{"oda": "123"}])
        assert valid is False
        assert "fornitore" in msg.lower()
