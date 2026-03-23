import unittest
from unittest.mock import MagicMock, patch

from selenium.webdriver.common.by import By

from src.bots.safework.programmazione_sync.bot import SafeWorkProgrammazioneSyncBot


class TestSafeWorkProgrammazioneSyncComprehensive(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        with patch("src.bots.safework.base.SafeworkBaseBot.__init__", return_value=None):
            self.bot = SafeWorkProgrammazioneSyncBot("user", "pass")
            self.bot.driver = self.mock_driver
            self.bot._log_callback = MagicMock()
            self.bot._logger = MagicMock()
            self.bot._trace_id = "test-trace"
            self.bot._status = MagicMock()
            self.bot._status.name = "RUNNING"
            self.bot._telegram_service = None
            self.bot.download_path = "C:/fake/downloads"
            self.bot.attivita_page = MagicMock()

    def test_properties(self):
        self.assertEqual(self.bot.get_name(), "Sincronizzazione Programmazione")
        self.assertEqual(self.bot.name, "programmazione_sync")

    @patch("src.bots.safework.programmazione_sync.bot.poll_for_new_file")
    @patch.object(SafeWorkProgrammazioneSyncBot, "_attendi_scomparsa_overlay")
    def test_run_success_flow(self, mock_overlay, mock_poll):  # noqa: ANN001
        """Test del flusso di sincronizzazione (download excel)."""
        data = [{"date_start": "01/01/2026", "date_end": "07/01/2026", "requesters": ["R1"]}]
        mock_poll.return_value = "C:/fake/downloads/Programmazione_2026.xlsx"
        self.bot.attivita_page.esporta_excel.return_value = True

        # Mock find_element per navigazione ID
        mock_home = MagicMock()
        mock_visualizza = MagicMock()
        self.mock_driver.find_element.side_effect = [mock_home, mock_visualizza]

        result = self.bot.run(data)

        self.assertTrue(result)
        self.assertEqual(self.bot.downloaded_file, "C:/fake/downloads/Programmazione_2026.xlsx")

        # Verifica navigazione
        self.mock_driver.find_element.assert_any_call(By.ID, "topIcon-actHomePage")
        self.mock_driver.find_element.assert_any_call(By.ID, "sideBar-actVisualizzaAttivita")

        # Verifica filtri
        self.bot.attivita_page.imposta_date.assert_called_with("01/01/2026", "07/01/2026")
        self.bot.attivita_page.seleziona_richiedente.assert_called_with("R1")
        self.bot.attivita_page.esegui_ricerca.assert_called_once()

    def test_run_missing_dates(self):
        """Verifica che il bot ritorni False se mancano le date."""
        result = self.bot.run([{"requesters": ["R1"]}])
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
