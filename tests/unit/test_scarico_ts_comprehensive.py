"""
Scarico Timesheet Bot - Comprehensive Test Suite (2026 Edition)
============================================================
Copre il loop di scarico multi-OdA, la rinomina unica dei file e il cleanup.

Matches source code:
- src/bots/portale_fornitori/scarico_ts/bot.py
- src/bots/portale_fornitori/scarico_ts/pages/scarico_ts_page.py
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from selenium.webdriver.remote.webelement import WebElement

from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot
from src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page import ScaricoTSPage


class TestScaricoTSComprehensive:
    @pytest.fixture
    def bot(self, mocker):
        """Inizializza bot con mock totali per isolamento."""
        with patch("src.bots.base.base_bot.BaseBot.__init__", return_value=None):
            bot = ScaricaTSBot()
            bot.driver = MagicMock()
            bot.wait = MagicMock()
            bot._log_callback = MagicMock()
            bot._logger = MagicMock()
            bot._trace_id = "test-trace"
            bot._stop_requested = False
            bot.download_path = "C:/fake/downloads"
            return bot

    @pytest.fixture
    def page(self, bot):
        """Inizializza Page Object."""
        with patch("src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page.WebDriverWait") as mock_wait:
            page = ScaricoTSPage(bot.driver, bot.log)
            page.wait = mock_wait.return_value
            page.long_wait = mock_wait.return_value
            return page

    # ========================================================================
    # 1. BOT LOGIC & PROCESSOR INTEGRATION
    # ========================================================================

    def test_bot_validate_data(self, bot):
        """Verifica validazione input specifica per Scarico TS."""
        with patch("src.bots.base.base_bot.BaseBot.validate_data", return_value=(True, "")):
            # Fallimento: manca fornitore
            ok, msg = bot.validate_data({"rows": []})
            assert ok is False
            assert "fornitore" in msg.lower()

            # Successo
            ok, _ = bot.validate_data({"fornitore": "COEMI", "rows": [{"numero_oda": "123"}]})
            assert ok is True

    def test_bot_validate_data_missing_fornitore_in_data(self, bot):
        """Verifica validazione quando il fornitore manca anche nel parametro 'fornitore'."""
        with patch("src.bots.base.base_bot.BaseBot.validate_data", return_value=(True, "")):
            data = {"rows": [{"numero_oda": "123"}]}
            ok, msg = bot.validate_data(data)
            assert ok is False
            assert "fornitore" in msg.lower()

    def test_bot_process_oda_rows_success(self, bot, mocker):
        """Test loop di elaborazione OdA con successo."""
        mocker.patch.object(bot, "_search_oda", return_value=True)
        mocker.patch.object(bot, "_download_excel", return_value=Path("final.xlsx"))

        rows = [{"numero_oda": "ODA1", "posizione_oda": "10"}, {"numero_oda": "ODA2", "posizione_oda": "20"}]
        count, files = bot._process_oda_rows(rows, Path("C:/Dest"))

        assert count == 2
        assert len(files) == 2
        assert bot._search_oda.call_count == 2

    def test_bot_process_oda_rows_empty_oda(self, bot, mocker):
        """Verifica che righe senza numero OdA vengano saltate."""
        rows = [{"note": "riga inutile"}]
        count, files = bot._process_oda_rows(rows, Path("."))
        assert count == 0
        assert len(files) == 0

    def test_bot_process_oda_rows_exception(self, bot, mocker):
        """Verifica che un errore su una OdA non blocchi il loop."""
        mocker.patch.object(bot, "_search_oda", side_effect=[Exception("Err"), True])
        mocker.patch.object(bot, "_download_excel", return_value=Path("ok.xlsx"))

        data = [{"numero_oda": "ERR"}, {"numero_oda": "OK"}]
        count, _ = bot._process_oda_rows(data, Path("."))
        assert count == 1
        assert bot._search_oda.call_count == 2

    def test_bot_vba_processing_integration(self, bot, mocker):
        """Verifica chiamata al processore VBA."""
        mock_proc = mocker.patch("src.bots.portale_fornitori.scarico_ts.bot.TimesheetProcessor")
        mock_proc.process_and_move.return_value = (True, "OK")

        bot.elabora_ts = True
        bot._run_vba_processing(["file1.xlsx"], Path("C:/Dest"))

        mock_proc.process_and_move.assert_called_once()

    def test_bot_run_vba_processing_failure(self, bot, mocker):
        """Verifica gestione errore VBA."""
        mocker.patch("src.bots.portale_fornitori.scarico_ts.bot.TimesheetProcessor.process_and_move", return_value=(False, "VBA Error"))
        bot.elabora_ts = True
        # Non deve crashare
        bot._run_vba_processing(["f.xlsx"], Path("."))

    # ========================================================================
    # 2. PAGE OBJECT & NAVIGATION
    # ========================================================================

    def test_page_navigate_to_timesheet_exception(self, page):
        """Verifica cattura errore navigazione."""
        page.wait.until.side_effect = Exception("Nav Error")
        assert page.navigate_to_timesheet() is False

    def test_page_setup_filters(self, page, mocker):
        """Verifica setup filtri con interazione complessa (Combo Arrow + Date)."""
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
        args_arrow = mock_ec.element_to_be_clickable.call_args_list[0][0][0]
        assert "generic_refresh_combo_box-" in str(args_arrow)
        # 2. Verifica wait data
        args_date = mock_ec.visibility_of_element_located.call_args_list[0][0][0]
        assert "DataTimesheetDa" in str(args_date)

    def test_page_setup_filters_exception(self, page):
        """Verifica cattura errore filtri."""
        page.wait.until.side_effect = Exception("Filter Error")
        assert page.setup_filters("V", "D") is False

    def test_page_search_and_download_exception(self, page):
        """Verifica cattura errore ricerca."""
        page.wait.until.side_effect = Exception("Search Error")
        assert page.search_and_download("ODA", "POS") is None

    # ========================================================================
    # 3. FILE SYSTEM & UNIQUE PATHS
    # ========================================================================

    def test_resolve_unique_path_logic(self, page):
        """Verifica generazione path unico ODA-POS.xlsx."""
        with patch("pathlib.Path.exists", return_value=False):
            dest_dir = Path("C:/Dest")
            current_file = Path("C:/Downloads/temp.xlsx")
            res = page._resolve_unique_path(dest_dir, "ODA1", "10", current_file)
            assert res.name == "ODA1-10.xlsx"

    def test_resolve_unique_path_fallback_locked(self, page):
        """Verifica fallback con timestamp se il file base esiste (es. ricaricamento)."""
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.side_effect = [True, False]

            # current_file deve essere diverso da new_path per innescare il loop
            current_file = Path("C:/Downloads/temp.xlsx")
            res = page._resolve_unique_path(Path("C:/Downloads"), "ODA1", "10", current_file)

            assert "ODA1-10" in res.name
            assert "_" in res.name  # Ha usato il timestamp/counter

    # ========================================================================
    # 4. FULL RUN & LIFECYCLE
    # ========================================================================

    def test_bot_run_success_cycle(self, bot, mocker):
        """Test di esecuzione bot completo con una riga."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_process_oda_rows", return_value=(1, [Path("test.xlsx")]))
        mocker.patch.object(bot, "_run_vba_processing")

        data = [{"numero_oda": "123"}]
        assert bot.run(data) is True
        bot._process_oda_rows.assert_called_once()

    def test_bot_run_filter_failure(self, bot, mocker):
        """Test fallimento setup iniziale filtri."""
        mocker.patch.object(bot, "_login", return_value=True)
        mock_page = mocker.patch("src.bots.portale_fornitori.scarico_ts.bot.ScaricoTSPage").return_value
        mock_page.navigate_to_timesheet.return_value = True
        mock_page.setup_filters.return_value = False

        assert bot.run([{"numero_oda": "1"}]) is False

    def test_bot_search_oda_exception(self, bot, mocker):
        """Verifica hardening _search_oda con blocco try/except."""
        bot.page = MagicMock()
        bot.page.search_and_download.side_effect = Exception("Selenium Timeout")
        # Deve catturare l'errore e tornare False, non crashare
        res = bot._search_oda("123", "10")
        assert res is False

    def test_page_wait_for_download_timeout(self, page, mocker):
        """Verifica timeout download."""
        mocker.patch("time.time", side_effect=[0, 1000]) # Forza superamento timeout
        res = page._wait_for_download(Path("."), set())
        assert res is None

    def test_page_download_cleanup_integration(self, page, tmp_path, mocker):
        """Verifica cleanup Chromium residui (marker GUID) durante download."""
        download_dir = tmp_path / "downloads"
        download_dir.mkdir()

        mocker.patch.object(page, "_wait_for_download", return_value=download_dir / "test.xlsx")
        mocker.patch.object(page, "_resolve_unique_path", return_value=download_dir / "final.xlsx")
        # Mocking click per evitare chiamate driver reali
        mocker.patch.object(page, "_wait_for_overlay")
        mock_cleanup = mocker.patch("src.utils.helpers.cleanup_chrome_temp_files", return_value=["marker"])

        from selenium.webdriver.remote.webelement import WebElement
        page.wait.until.return_value = MagicMock(spec=WebElement)

        res = page.download_oda("ODA", "POS", download_dir, download_dir)

        assert res is not None
        mock_cleanup.assert_called()
