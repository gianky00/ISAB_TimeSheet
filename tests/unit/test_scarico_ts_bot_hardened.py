import pytest
import time
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot

class TestScaricoTSBotHardened:
    @pytest.fixture
    def bot(self):
        return ScaricaTSBot(username="u", password="p", fornitore="TestForn")

    def test_validate_data_missing_forn(self, bot):
        """Verifica che il bot rifiuti l'esecuzione senza fornitore."""
        bot.fornitore = ""
        valid, msg = bot.validate_data([{"numero_oda": "123"}])
        assert valid is False
        assert "Fornitore" in msg

    def test_download_excel_with_conflict_rename(self, bot, mocker, tmp_path):
        """Verifica la rinomina con timestamp se il file di destinazione esiste."""
        source_dir = tmp_path / "downloads"
        source_dir.mkdir()
        dest_dir = tmp_path / "dest"
        dest_dir.mkdir()
        
        # 1. Crea file pre-esistente in dest
        existing_file = dest_dir / "TS_123-10.xlsx"
        existing_file.write_text("old")
        
        # 2. Simula download di un nuovo file in source
        new_download = source_dir / "download.xlsx"
        new_download.write_text("new")
        
        # Mock per far trovare il file appena creato
        mocker.patch("pathlib.Path.iterdir", side_effect=[
            [], # files_before
            [new_download], # primo giro loop download
            [new_download]  # verifica exists
        ])
        mocker.patch("time.time", side_effect=[100, 101, 102, 103, 104, 105, 200])
        mocker.patch("time.sleep")
        m_shutil = mocker.patch("shutil.move")
        
        # Mock Selenium wait/click
        bot.wait = MagicMock()
        bot.driver = MagicMock()
        
        res = bot._download_excel(source_dir, dest_dir, "123", "10")
        
        # Poiché il file esisteva, deve aver generato un nome con timestamp
        # Il path finale passato a move deve contenere un underscore del timestamp
        args = m_shutil.call_args[0]
        dest_path_str = args[1]
        assert "_" in dest_path_str
        assert "TS_123-10" in dest_path_str

    def test_process_downloaded_files_vba_style_loop(self, bot, mocker, tmp_path):
        """Verifica il loop di richiesta suffisso in caso di conflitto stile VBA."""
        dest_dir = tmp_path / "dest"
        dest_dir.mkdir()
        
        # File esistente in dest
        (dest_dir / "test.xlsx").write_text("existing")
        
        # File sorgente
        src_file = tmp_path / "test.xlsx"
        src_file.write_text("new")
        
        # Simula input utente: prima invia "V2" (che esiste anche lui), poi "FINAL"
        (dest_dir / "test V2.xlsx").write_text("existing v2")
        
        m_ask = mocker.patch.object(bot, "_ask_user")
        m_ask.side_effect = ["V2", "FINAL"]
        m_shutil = mocker.patch("shutil.move")
        mocker.patch.object(bot, "_check_stop")
        
        bot._process_downloaded_files_vba_style([str(src_file)], dest_dir)
        
        # Deve aver chiamato ask due volte
        assert m_ask.call_count == 2
        # Il path finale deve essere "test FINAL.xlsx"
        args = m_shutil.call_args[0]
        assert "test FINAL.xlsx" in args[1]

    def test_setup_filters_js_injection(self, bot, mocker):
        """Verifica l'uso corretto di ActionChains e JS per i filtri."""
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot.long_wait = MagicMock()
        mocker.patch("time.sleep")
        
        # Mock elemento fornitore trovato
        mock_opt = MagicMock()
        bot.long_wait.until.return_value = mock_opt
        
        res = bot._setup_filters()
        
        assert res is True
        # Deve aver scrollato e cliccato via JS
        bot.driver.execute_script.assert_any_call("arguments[0].scrollIntoView({block: 'nearest'});", mock_opt)
        bot.driver.execute_script.assert_any_call("arguments[0].click();", mock_opt)