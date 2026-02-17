
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path
from itertools import count
import shutil
import tempfile
import os

from src.bots.portale_fornitori.timbrature.bot import TimbratureBot
from src.bots.portale_fornitori.timbrature.pages.timbrature_page import TimbraturePage
from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage

class TestTimbratureBotComprehensive(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        with patch("src.bots.base.base_bot.BaseBot.__init__", return_value=None):
            with patch("src.bots.portale_fornitori.timbrature.bot.TimbratureStorage") as mock_storage_class:
                self.bot = TimbratureBot(data_da="01/01/2026", data_a="31/01/2026", fornitore="VENDOR")
                self.bot.driver = self.mock_driver
                self.bot._log_callback = MagicMock()
                self.bot._logger = MagicMock()
                self.bot._trace_id = "test-trace"
                self.bot._status = MagicMock()
                self.bot._status.name = "RUNNING"
                self.bot._telegram_service = None
                self.bot._stop_requested = False
                self.bot.download_path = "C:/fake/downloads"
                self.mock_storage = self.bot.storage = mock_storage_class.return_value

    def test_init_and_properties(self):
        self.assertEqual(self.bot.name, "Timbrature")

    @patch("src.bots.portale_fornitori.timbrature.bot.TimbraturePage")
    def test_run_success(self, mock_page_class):
        mock_page = mock_page_class.return_value
        mock_page.navigate_to_timbrature.return_value = True
        mock_page.set_filters.return_value = True
        mock_page.download_excel.return_value = "fake_path.xlsx"
        
        with patch("src.bots.portale_fornitori.timbrature.bot.Path.exists", return_value=True):
            with patch("src.bots.portale_fornitori.timbrature.bot.Path.unlink"):
                result = self.bot.run([{"data_da": "01/01/2026", "fornitore": "V"}])
                self.assertTrue(result)

class TestTimbraturePageComprehensive(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_log = MagicMock()
        self.test_dir = Path(tempfile.mkdtemp())
        self.download_dir = self.test_dir / "downloads"
        self.download_dir.mkdir()
        
        # Patching WebDriverWait
        with patch("src.bots.portale_fornitori.timbrature.pages.timbrature_page.WebDriverWait") as mock_wait_class:
            self.mock_wait = MagicMock()
            self.mock_long_wait = MagicMock()
            mock_wait_class.side_effect = [self.mock_wait, self.mock_long_wait]
            self.page = TimbraturePage(self.mock_driver, self.mock_log, str(self.download_dir))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("src.bots.portale_fornitori.timbrature.pages.timbrature_page.time.sleep")
    @patch("src.bots.portale_fornitori.timbrature.pages.timbrature_page.time.time")
    def test_rename_latest_download_success(self, mock_time, mock_sleep):
        """Test download con filesystem reale per evitare problemi di mocking Path."""
        # 1. Crea un file finto nella cartella download
        fake_file = self.download_dir / "report.xlsx"
        fake_file.write_text("dummy content")
        
        # 2. Mock tempo: start=1000, current=1001
        # Il bot fa time.time() all'inizio, poi nel loop.
        mock_time.side_effect = count(start=1000)
        
        # 3. Patch CONFIG_DIR per puntare alla nostra cartella temporanea
        # Il bot fa: from src.core.config_manager import CONFIG_DIR; dest_dir = CONFIG_DIR / "temp"
        with patch("src.bots.portale_fornitori.timbrature.pages.timbrature_page.Timeouts.DOWNLOAD", 5):
            with patch("src.core.config_manager.CONFIG_DIR", self.test_dir):
                result = self.page._rename_latest_download("test_timb")
                
                # Verifica
                self.assertTrue(result)
                self.assertIn("test_timb_", result)
                self.assertTrue(Path(result).exists())
                self.assertFalse(fake_file.exists()) # Deve essere stato rimosso/mosso

class TestTimbratureStorageComprehensive(unittest.TestCase):
    def setUp(self):
        self.temp_db = Path("test_timbrature_storage.db")
        with patch("src.core.database.db_manager.get_connection"):
            self.storage = TimbratureStorage(self.temp_db)

    @patch("pandas.read_excel")
    @patch("src.core.database.db_manager.get_connection")
    @patch("src.core.sync_tracker.SyncTracker.update_status")
    def test_import_excel_data_flow(self, mock_sync, mock_get_conn, mock_read_excel):
        import pandas as pd
        mock_read_excel.return_value = pd.DataFrame({
            "Id Dipendente": ["1"],
            "Data Timbratura": ["2026-01-01"],
            "Ora Ingresso": ["08:00"],
            "Ora Uscita": ["17:00"],
            "Nome Risorsa": ["M"],
            "Cognome Risorsa": ["R"],
            "Fornitore": ["V"],
            "Codice Fiscale": ["CF"]
        })
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        result = self.storage.import_excel("path.xlsx")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
