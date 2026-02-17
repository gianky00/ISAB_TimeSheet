"""
Scarico TS Bot - Comprehensive Test Suite (2026 Edition)
=======================================================
Test suite definitiva per ScaricaTSBot e ScaricoTSPage.
Copre il loop di scarico multi-OdA, la rinomina unica dei file e il cleanup.

Matches source code: 
- src/bots/portale_fornitori/scarico_ts/bot.py
- src/bots/portale_fornitori/scarico_ts/pages/scarico_ts_page.py
"""

import time
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest
from selenium.webdriver.common.by import By

from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot
from src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page import ScaricoTSPage
from src.core.constants import BotStatus


class TestScaricoTSComprehensive:
    @pytest.fixture
    def bot(self, mocker):
        """Fixture per il Bot con componenti mockati."""
        bot = ScaricaTSBot(username="u", password="p", download_path="/tmp/downloads", fornitore="TEST")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot.long_wait = MagicMock()
        mocker.patch.object(bot, "_login", return_value=True)
        return bot

    @pytest.fixture
    def page(self, bot):
        """Fixture per la Page Object Model."""
        p = ScaricoTSPage(bot.driver, bot.log)
        p.wait = MagicMock()
        p.long_wait = MagicMock()
        return p

    # ========================================================================
    # 1. BOT LOGIC & LOOP
    # ========================================================================

    def test_bot_validate_data(self, bot):
        """Verifica la validazione dati dei timesheet."""
        # Successo
        assert bot.validate_data([{"numero_oda": "123"}])[0] is True
        # Fallimento: no fornitore
        bot.fornitore = None
        assert bot.validate_data([{"numero_oda": "123"}])[0] is False

    def test_bot_validate_data_missing_fornitore_in_data(self, bot):
        """Verifica fallimento se manca il fornitore sia nel bot che nel dizionario dati."""
        bot.fornitore = None
        data = {"rows": [{"numero_oda": "123"}]}
        ok, msg = bot.validate_data(data)
        assert ok is False
        assert "Fornitore non specificato" in msg

    def test_bot_process_oda_rows_success(self, bot, mocker):
        """Verifica che il bot cicli correttamente sugli OdA e rinomini i file."""
        mocker.patch.object(bot, "_search_oda", return_value=True)
        mocker.patch.object(bot, "_download_excel", return_value=Path("final.xlsx"))
        
        rows = [{"numero_oda": "ODA1", "posizione_oda": "10"}, {"numero_oda": "ODA2", "posizione_oda": "20"}]
        count, files = bot._process_oda_rows(rows, Path("C:/Dest"))
        
        assert count == 2
        assert len(files) == 2
        assert bot._search_oda.call_count == 2

    def test_bot_process_oda_rows_empty_oda(self, bot, mocker):
        """Verifica che il bot salti righe con OdA vuoto."""
        count, files = bot._process_oda_rows([{"numero_oda": ""}], Path("."))
        assert count == 0
        assert len(files) == 0

    def test_bot_process_oda_rows_exception(self, bot, mocker):
        """Verifica che un'eccezione in un OdA non blocchi gli altri."""
        mocker.patch.object(bot, "_search_oda", side_effect=[Exception("Err"), True])
        mocker.patch.object(bot, "_download_excel", return_value=Path("ok.xlsx"))
        
        data = [{"numero_oda": "ERR"}, {"numero_oda": "OK"}]
        count, _ = bot._process_oda_rows(data, Path("."))
        assert count == 1

    def test_bot_vba_processing_integration(self, bot, mocker):
        """Verifica l'integrazione con TimesheetProcessor (VBA logic)."""
        mock_proc = mocker.patch("src.bots.portale_fornitori.scarico_ts.bot.TimesheetProcessor")
        mock_proc.process_and_move.return_value = (True, "OK")
        
        bot.elabora_ts = True
        bot._run_vba_processing(["file1.xlsx"], Path("C:/Dest"))
        
        mock_proc.process_and_move.assert_called_once()

    def test_bot_run_vba_processing_failure(self, bot, mocker):
        """Verifica log in caso di errore elaborazione VBA."""
        mock_proc = mocker.patch("src.bots.portale_fornitori.scarico_ts.bot.TimesheetProcessor")
        mock_proc.process_and_move.return_value = (False, "VBA Error")
        bot.elabora_ts = True
        # Non deve crashare
        bot._run_vba_processing(["file.xlsx"], Path("."))

    # ========================================================================
    # 2. PAGE INTERACTION
    # ========================================================================

    def test_page_navigate_to_timesheet_exception(self, page, mocker):
        """Verifica gestione eccezioni in navigazione."""
        page.wait.until.side_effect = Exception("Timeout")
        assert page.navigate_to_timesheet() is False

    def test_page_setup_filters(self, page, mocker):
        """Verifica l'impostazione dei filtri (Fornitore e Data) con verifica selettori."""
        from selenium.webdriver.remote.webelement import WebElement
        page._wait_for_overlay = MagicMock()
        mock_ec = mocker.patch("src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page.EC")
        
        mock_arrow = MagicMock(spec=WebElement)
        mock_option = MagicMock(spec=WebElement)
        mock_date = MagicMock(spec=WebElement)
        
        page.wait.until.side_effect = [mock_arrow, mock_date]
        page.long_wait.until.return_value = mock_option
        
        res = page.setup_filters("COEMI", "01.01.2025")
        
        assert res is True
        # 1. Verifica wait arrow
        args_ec_arrow = mock_ec.element_to_be_clickable.call_args_list[0][0][0]
        assert "trigger-picker" in str(args_ec_arrow)
        # 2. Verifica wait option
        args_ec_opt = mock_ec.presence_of_element_located.call_args_list[0][0][0]
        assert "COEMI" in args_ec_opt[1]
        # 3. Verifica wait data
        args_ec_date = mock_ec.visibility_of_element_located.call_args_list[0][0][0]
        assert "DataTimesheetDa" in str(args_ec_date)
        # 4. Verifica invio data
        mock_date.send_keys.assert_called_with("01.01.2025")

    def test_page_setup_filters_exception(self, page, mocker):
        """Verifica gestione eccezioni in filtri."""
        page.wait.until.side_effect = Exception("Driver error")
        assert page.setup_filters("F", "01.01") is False

    def test_page_search_and_download_exception(self, page, mocker):
        """Verifica gestione eccezioni in ricerca."""
        page.wait.until.side_effect = Exception("DOM Error")
        assert page.search_and_download("123", "10", Path(".")) is False

    # ========================================================================
    # 3. FILENAME & CONFLICT RESOLUTION
    # ========================================================================

    def test_resolve_unique_path_logic(self, page):
        """Verifica che la pagina generi nomi file univoci in caso di duplicati."""
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.side_effect = [True, False]
            res = page._resolve_unique_path(Path("C:/Downloads"), "ODA1", "10", Path("C:/Downloads/old.xlsx"))
            assert "ODA1-10" in res.name
            assert "_" in res.name

    def test_resolve_unique_path_fallback_locked(self, page, mocker):
        """Verifica il fallback con timestamp se il nome base esiste già."""
        # Simulo: il primo percorso esiste (conflitto), il secondo no (successo con timestamp)
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.side_effect = [True, False]
            
            # current_file deve essere diverso da new_path per innescare il loop
            current_file = Path("C:/Downloads/temp.xlsx")
            res = page._resolve_unique_path(Path("C:/Downloads"), "ODA1", "10", current_file)
            
            assert "ODA1-10" in res.name
            assert "_" in res.name # Ha usato il timestamp/counter
            assert mock_exists.call_count == 2

    # ========================================================================
    # 4. DOWNLOAD & CLEANUP (THE CRITICAL PART)
    # ========================================================================

    def test_bot_run_success_cycle(self, bot, mocker):
        """Verifica il ciclo run completo con successo."""
        mocker.patch.object(bot, "_navigate_to_timesheet", return_value=True)
        mocker.patch.object(bot, "_setup_filters", return_value=True)
        mocker.patch.object(bot, "_process_oda_rows", return_value=(1, [Path("test.xlsx")]))
        mocker.patch.object(bot, "_run_vba_processing")
        
        data = [{"numero_oda": "123"}]
        assert bot.run(data) is True

    def test_bot_run_filter_failure(self, bot, mocker):
        """Verifica fallimento run se i filtri falliscono."""
        mocker.patch.object(bot, "_navigate_to_timesheet", return_value=True)
        mocker.patch.object(bot, "_setup_filters", return_value=False)
        assert bot.run([]) is False

    def test_bot_search_oda_exception(self, bot, mocker):
        """Verifica gestione errori in _search_oda del bot."""
        # Mock per innescare eccezione durante la ricerca
        mocker.patch.object(bot, "wait")
        bot.wait.until.side_effect = Exception("Search error")
        assert bot._search_oda("123", "10") is False

    def test_page_wait_for_download_timeout(self, page, mocker):
        """Verifica ritorno None se il download va in timeout."""
        mocker.patch("time.time", side_effect=[0, 1000]) # Forza superamento timeout
        mocker.patch("src.core.constants.Timeouts.DOWNLOAD", 30)
        res = page._wait_for_download(Path("."), set())
        assert res is None

    def test_page_download_cleanup_integration(self, page, mocker, tmp_path):

        """Verifica che ScaricoTSPage pulisca i file 0 KB tramite helper."""
        download_dir = tmp_path / "downloads"
        download_dir.mkdir()
        
        mocker.patch.object(page, "_wait_for_download", return_value=download_dir / "test.xlsx")
        mocker.patch.object(page, "_resolve_unique_path", return_value=download_dir / "final.xlsx")
        mocker.patch("pathlib.Path.rename")
        mocker.patch("pathlib.Path.iterdir", return_value=[])

        mock_cleanup = mocker.patch("src.utils.helpers.cleanup_chrome_temp_files", return_value=["marker"])
        
        from selenium.webdriver.remote.webelement import WebElement
        page.wait.until.return_value = MagicMock(spec=WebElement)

        res = page._download_excel(download_dir, "ODA1", "10")
        assert res is True
        mock_cleanup.assert_called_once_with(download_dir)
