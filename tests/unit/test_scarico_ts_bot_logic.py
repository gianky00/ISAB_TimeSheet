import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot


class TestScaricaTSBotLogic(unittest.TestCase):
    """Test unitari per la logica del bot Scarico TS (senza browser reale)."""

    def setUp(self):
        # Mock del driver e dei wait per evitare l'avvio del browser
        self.mock_driver = MagicMock()
        self.mock_wait = MagicMock()

        # Inizializza il bot con parametri di test
        self.bot = ScaricaTSBot(
            username="test_user",
            password="test_password",
            data_da="01/01/2026",
            fornitore="TEST FORNITORE",
            elabora_ts=False,
            headless=True,
        )
        # Inietta i mock
        self.bot.driver = self.mock_driver
        self.bot.wait = self.mock_wait
        self.bot.long_wait = self.mock_wait

    def test_validate_data_valid(self):
        """Verifica validazione con dati corretti."""
        data = [{"numero_oda": "123", "posizione_oda": "10"}]
        valid, msg = self.bot.validate_data(data)
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_validate_data_missing_fornitore(self):
        """Verifica errore se manca il fornitore."""
        self.bot.fornitore = ""
        data = [{"numero_oda": "123"}]
        valid, msg = self.bot.validate_data(data)
        self.assertFalse(valid)
        self.assertIn("Fornitore non specificato", msg)

    def test_prepare_run_environment_dict(self):
        """Verifica preparazione ambiente con input dizionario."""
        data = {
            "rows": [{"n": 1}],
            "data_da": "05/05/2026",
            "fornitore": "NEW FORN",
            "elabora_ts": True,
        }
        rows, _dest = self.bot._prepare_run_environment(data)

        self.assertEqual(len(rows), 1)
        self.assertEqual(self.bot.data_da, "05/05/2026")
        self.assertEqual(self.bot.fornitore, "NEW FORN")
        self.assertTrue(self.bot.elabora_ts)

    def test_get_final_download_path_logic(self):
        """Testa la costruzione del nome file e del percorso di destinazione."""
        source = Path("temp/downloads")
        dest = Path("data/ts")

        # Caso 1: Senza elaborazione (va in dest)
        self.bot.elabora_ts = False
        path = self.bot._get_final_download_path(source, dest, "12345", "10")
        self.assertEqual(path.name, "TS_12345-10.xlsx")
        self.assertEqual(path.parent, dest)

        # Caso 2: Con elaborazione (resta in source per processing)
        self.bot.elabora_ts = True
        path = self.bot._get_final_download_path(source, dest, "999", "")
        self.assertEqual(path.name, "TS_999.xlsx")
        self.assertEqual(path.parent, source)

    @patch("src.bots.portale_fornitori.scarico_ts.bot.ScaricaTSBot._search_oda")
    @patch("src.bots.portale_fornitori.scarico_ts.bot.ScaricaTSBot._download_excel")
    def test_process_oda_rows_iteration(self, mock_download, mock_search):
        """Verifica che il bot cicli correttamente sulle righe OdA."""
        rows = [
            {"numero_oda": "ODA1", "posizione_oda": "1"},
            {"numero_oda": "ODA2", "posizione_oda": "2"},
        ]
        dest = Path("temp")

        mock_search.return_value = True
        mock_download.return_value = Path("temp/file.xlsx")

        # Mock stop check per evitare loop infiniti o errori
        self.bot._check_stop = MagicMock()

        success, files = self.bot._process_oda_rows(rows, dest)

        self.assertEqual(success, 2)
        self.assertEqual(len(files), 2)
        self.assertEqual(mock_search.call_count, 2)

    def test_search_oda_js_injection(self):
        """Verifica che la ricerca OdA usi correttamente execute_script per i valori."""
        # Setup mock per trovare gli elementi
        mock_el = MagicMock()
        self.mock_wait.until.return_value = mock_el

        # Esegui (mockando attendi_scomparsa_overlay)
        with patch.object(self.bot, "_attendi_scomparsa_overlay"):
            self.bot._search_oda("12345", "10")

            # Dovrebbe aver chiamato execute_script per impostare i valori via JS
            # (pattern usato nel bot per bypassare limiti di input standard)
            self.assertTrue(self.mock_driver.execute_script.called)


if __name__ == "__main__":
    unittest.main()
