import unittest
from unittest.mock import MagicMock, patch

from src.bots.portale_fornitori.prenota_bp.bot import PrenotaBPBot


class TestPrenotaBPBotLogic(unittest.TestCase):
    """Test unitari per la logica del bot Prenota BP."""

    def setUp(self):
        self.bot = PrenotaBPBot(
            username="test_user",
            password="test_password",
            fornitore="TEST COEMI",
            headless=True,
        )
        # Mock driver e log
        self.bot.driver = MagicMock()
        self.bot.log = MagicMock()

    def test_get_row_value_robustness(self):
        """Verifica che il recupero dei valori dalle righe sia case-insensitive e ignori spazi/_."""
        row = {"Numero_BP": "BP001", "  Note di ritiro  ": "Ritirare domani"}

        val1 = self.bot._get_row_value(row, "numero bp")
        val2 = self.bot._get_row_value(row, "NOTE DI RITIRO")
        val3 = self.bot._get_row_value(row, "NON_ESISTE")

        self.assertEqual(val1, "BP001")
        self.assertEqual(val2, "Ritirare domani")
        self.assertEqual(val3, "")

    def test_init_run_data(self):
        """Verifica l'inizializzazione dei dati da dizionario o lista."""
        data_dict = {
            "rows": [{"n": 1}],
            "data_da": "01/01/2026",
            "fornitore": "NEW FORN",
        }
        rows = self.bot._init_run_data(data_dict)
        self.assertEqual(len(rows), 1)
        self.assertEqual(self.bot.data_da, "01/01/2026")
        self.assertEqual(self.bot.fornitore, "NEW FORN")

        data_list = [{"n": 2}]
        rows2 = self.bot._init_run_data(data_list)
        self.assertEqual(rows2, data_list)

    @patch("src.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_process_single_bp_success(self, mock_page_cls):
        """Verifica il flusso di successo per un singolo BP."""
        mock_page = mock_page_cls.return_value
        row = {"Numero BP": "BP123", "Note": "Test Note"}

        result = self.bot._process_single_bp(mock_page, 0, row)

        self.assertTrue(result)
        self.assertEqual(len(self.bot.results), 1)
        self.assertEqual(self.bot.results[0]["STATO"], "OK")
        self.assertTrue(mock_page.filtra_buoni_prelievo.called)
        self.assertTrue(mock_page.gestisci_creazione_richiesta.called)

    @patch("src.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_process_single_bp_failure(self, mock_page_cls):
        """Verifica la gestione degli errori durante l'elaborazione di un BP."""
        mock_page = mock_page_cls.return_value
        mock_page.apri_dettagli_bp.side_effect = Exception("Element not found")
        row = {"Numero BP": "BP_FAIL"}

        result = self.bot._process_single_bp(mock_page, 0, row)

        self.assertFalse(result)
        self.assertEqual(self.bot.results[0]["STATO"], "ERRORE")
        self.assertIn("Element not found", self.bot.results[0]["MSG"])

    @patch("src.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_run_stop_requested(self, mock_page_cls):
        """Verifica che il bot si fermi se richiesto dall'utente."""
        rows = [{"Numero BP": "BP1"}, {"Numero BP": "BP2"}]

        self.bot._stop_requested = True
        success = self.bot.run(rows)

        # Non dovrebbe aver processato nulla
        self.assertEqual(len(self.bot.results), 0)
        self.assertTrue(success)  # Ritorna comunque True per segnalare fine normale


if __name__ == "__main__":
    unittest.main()
