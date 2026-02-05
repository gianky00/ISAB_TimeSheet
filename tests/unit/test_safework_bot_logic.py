import unittest
from unittest.mock import MagicMock, patch

from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkPDLBotLogic(unittest.TestCase):
    """Test unitari per la logica del bot SafeWork PDL."""

    def setUp(self):
        self.bot = SafeWorkPDLBot(
            username="safe_user",
            password="safe_password",
            headless=True,
            download_path="temp/test_pdl",
        )
        self.bot.driver = MagicMock()
        self.bot.wait = MagicMock()
        self.bot.log = MagicMock()

    def test_validate_data_pdl_variants(self):
        """Verifica validazione con diversi nomi chiave per il PDL."""
        data1 = [{"numero_pdl": "123456"}]
        data2 = [{"pdl_number": "654321"}]
        data3 = [{"note": "manca pdl"}]

        v1, _ = self.bot.validate_data(data1)
        v2, _ = self.bot.validate_data(data2)
        v3, _ = self.bot.validate_data(data3)

        self.assertTrue(v1)
        self.assertTrue(v2)
        self.assertFalse(v3)

    def test_sanitizza_pdl_number(self):
        """Testa l'autocompletamento dei suffissi /S e /C."""
        # < 400000 -> /S
        self.assertEqual(self.bot._sanitizza_pdl_number("399999"), "399999/S")
        # >= 400000 -> /C
        self.assertEqual(self.bot._sanitizza_pdl_number("400000"), "400000/C")
        # Già formattato -> invariato
        self.assertEqual(self.bot._sanitizza_pdl_number("123456/S"), "123456/S")
        # Non standard -> invariato (strip/upper)
        self.assertEqual(self.bot._sanitizza_pdl_number(" abc 123 "), "ABC123")

    @patch("src.bots.safework.pdl.bot.WebDriverWait")
    def test_login_flow(self, mock_wait_cls):
        """Verifica i passaggi principali del login."""
        # Mock per l'istanza creata con WebDriverWait(self.driver, 10)
        mock_wait_local = mock_wait_cls.return_value
        mock_el = MagicMock()
        mock_wait_local.until.return_value = mock_el

        # Mock per self.bot.wait (già MagicMock da setUp)
        self.bot.wait.until.return_value = mock_el

        # Mock metodo interno
        self.bot._attendi_caricamento_sistema = MagicMock()

        success = self.bot._login()

        self.assertTrue(success)
        self.assertTrue(self.bot.driver.get.called)
        # Dovrebbe aver inserito username e password (2 chiamate a send_keys)
        self.assertGreaterEqual(mock_el.send_keys.call_count, 2)

    def test_safe_remove_resilience(self):
        """Verifica che _safe_remove non esploda se il file non esiste o è bloccato."""
        # Caso file inesistente
        self.bot._safe_remove("non_esiste.pdf")  # Non deve alzare eccezione

        # Caso errore durante unlink
        with patch("pathlib.Path.exists", return_value=True), patch(
            "pathlib.Path.unlink", side_effect=Exception("Locked")
        ):
            self.bot._safe_remove("locked.pdf")  # Deve gestire l'errore internamente

    @patch("src.utils.document_processor.DocumentProcessor.merge_pdfs")
    def test_unisci_e_stampa_pdl_logic(self, mock_merge):
        """Verifica la logica di unione PDF e tracking file scaricati."""
        mock_merge.return_value = True
        item = {"print_enabled": False}
        all_paths = []

        success = self.bot._unisci_e_stampa_pdl(
            "123456/S", "p1.pdf", "p2.pdf", item, all_paths
        )

        self.assertTrue(success)
        self.assertEqual(len(self.bot.downloaded_files), 1)
        self.assertIn("PDL_123456-S.pdf", self.bot.downloaded_files[0])
        self.assertEqual(len(all_paths), 1)

    @patch("src.utils.document_processor.DocumentProcessor.merge_pdfs")
    def test_handle_session_merge(self, mock_merge):
        """Verifica la creazione del PDF unico di sessione."""
        mock_merge.return_value = True
        data = [{"merge_all_session": True}]
        all_paths = ["pdl1.pdf", "pdl2.pdf"]

        self.bot._handle_session_merge(data, all_paths)

        self.assertTrue(mock_merge.called)
        # Dovrebbe aver aggiunto il file di sessione alla lista finale
        self.assertEqual(len(self.bot.downloaded_files), 1)
        self.assertIn("PDL_SESSIONE_", self.bot.downloaded_files[0])


if __name__ == "__main__":
    unittest.main()
