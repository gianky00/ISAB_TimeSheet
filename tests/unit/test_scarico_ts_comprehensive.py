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
from src.core.constants import BotStatus


class TestScaricoTSComprehensive:
    @pytest.fixture
    def bot(self, mocker):  # noqa: ANN001
        """Inizializza bot con mock totali per isolamento."""
        with patch("src.bots.base.base_bot.BaseBot.__init__", return_value=None):
            bot = ScaricaTSBot()
            bot.driver = MagicMock()
            bot.wait = MagicMock()
            bot._log_callback = MagicMock()
            bot._logger = MagicMock()
            bot._trace_id = "test-trace"
            bot._stop_requested = False
            bot._status = BotStatus.IDLE
            bot._telegram_service = None
            bot.download_path = "C:/fake/downloads"
            bot.fornitore = ""  # Deve essere vuoto per testare la validazione
            return bot

    @pytest.fixture
    def page(self, bot):  # noqa: ANN001
        """Inizializza Page Object."""
        with patch("src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page.WebDriverWait") as mock_wait:
            page = ScaricoTSPage(bot.driver, bot.log)
            # Creiamo due mock distinti
            page.wait = MagicMock()
            page.long_wait = MagicMock()
            return page

    # ========================================================================
    # 1. BOT LOGIC & PROCESSOR INTEGRATION
    # ========================================================================

    def test_bot_validate_data(self, bot):  # noqa: ANN001
        """Verifica validazione input specifica per Scarico TS."""
        with patch("src.bots.base.base_bot.BaseBot.validate_data", return_value=(True, "")):
            # Fallimento: manca fornitore (data è dict, self.fornitore è vuoto)
            ok, msg = bot.validate_data({"rows": [{"numero_oda": "123"}]})
            assert ok is False
            assert "fornitore" in msg.lower()

            # Successo
            bot.fornitore = "COEMI"
            ok, _ = bot.validate_data({"rows": [{"numero_oda": "123"}]})
            assert ok is True

    def test_bot_validate_data_missing_fornitore_in_data(self, bot):  # noqa: ANN001
        """Verifica validazione quando il fornitore manca sia nel bot che nel dict."""
        with patch("src.bots.base.base_bot.BaseBot.validate_data", return_value=(True, "")):
            bot.fornitore = ""
            data = {"rows": [{"numero_oda": "123"}]}
            ok, msg = bot.validate_data(data)
            assert ok is False
            assert "fornitore" in msg.lower()

    def test_bot_process_oda_rows_success(self, bot, mocker):  # noqa: ANN001
        """Test loop di elaborazione OdA con successo."""
        mocker.patch.object(bot, "_search_oda", return_value=True)
        mocker.patch.object(bot, "_download_excel", return_value=Path("final.xlsx"))

        rows = [{"numero_oda": "ODA1", "posizione_oda": "10"}, {"numero_oda": "ODA2", "posizione_oda": "20"}]
        count, files = bot._process_oda_rows(rows, Path("C:/Dest"))

        assert count == 2  # noqa: PLR2004
        assert len(files) == 2  # noqa: PLR2004
        assert bot._search_oda.call_count == 2  # noqa: PLR2004

    def test_bot_process_oda_rows_empty_oda(self, bot, mocker):  # noqa: ANN001
        """Verifica che righe senza numero OdA vengano saltate."""
        rows = [{"note": "riga inutile"}]
        count, files = bot._process_oda_rows(rows, Path("."))
        assert count == 0
        assert len(files) == 0

    def test_bot_process_oda_rows_exception(self, bot, mocker):  # noqa: ANN001
        """Verifica che un errore su una OdA non blocchi il loop."""
        mocker.patch.object(bot, "_search_oda", side_effect=[Exception("Err"), True])
        mocker.patch.object(bot, "_download_excel", return_value=Path("ok.xlsx"))

        data = [{"numero_oda": "ERR"}, {"numero_oda": "OK"}]
        count, _ = bot._process_oda_rows(data, Path("."))
        assert count == 1
        assert bot._search_oda.call_count == 2  # noqa: PLR2004

    def test_bot_vba_processing_integration(self, bot, mocker):  # noqa: ANN001
        """Verifica chiamata al processore VBA."""
        mock_proc = mocker.patch("src.bots.portale_fornitori.scarico_ts.bot.TimesheetProcessor")
        mock_proc.process_and_move.return_value = (True, "OK")

        bot.elabora_ts = True
        bot._run_vba_processing(["file1.xlsx"], Path("C:/Dest"))

        mock_proc.process_and_move.assert_called_once()

    def test_bot_run_vba_processing_failure(self, bot, mocker):  # noqa: ANN001
        """Verifica gestione errore VBA."""
        mocker.patch(
            "src.bots.portale_fornitori.scarico_ts.bot.TimesheetProcessor.process_and_move",
            return_value=(False, "VBA Error"),
        )
        bot.elabora_ts = True
        # Non deve crashare
        bot._run_vba_processing(["f.xlsx"], Path("."))

    # ========================================================================
    # 2. PAGE OBJECT & NAVIGATION
    # ========================================================================

    def test_page_navigate_to_timesheet_exception(self, page):  # noqa: ANN001
        """Verifica cattura errore navigazione."""
        page.wait.until.side_effect = Exception("Nav Error")
        assert page.navigate_to_timesheet() is False

    def test_page_setup_filters(self, page, mocker):  # noqa: ANN001
        """Verifica setup filtri con interazione complessa (Combo Arrow + Date)."""
        page._wait_for_overlay = MagicMock()
        # Mock ActionChains
        mock_ac = mocker.patch("src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page.ActionChains")
        mock_ac_inst = mock_ac.return_value
        mock_ac_inst.move_to_element.return_value = mock_ac_inst
        mock_ac_inst.click.return_value = mock_ac_inst
        mock_ac_inst.perform.return_value = None

        mock_arrow = MagicMock(spec=WebElement)
        mock_option = MagicMock(spec=WebElement)
        mock_date = MagicMock(spec=WebElement)

        # Il codice chiama until 3 volte: arrow (wait), option (long_wait), date (wait)
        page.wait.until.side_effect = [mock_arrow, mock_date]
        page.long_wait.until.return_value = mock_option

        res = page.setup_filters("COEMI", "01.01.2025")

        assert res is True

    def test_page_setup_filters_exception(self, page):  # noqa: ANN001
        """Verifica cattura errore filtri."""
        page.wait.until.side_effect = Exception("Filter Error")
        assert page.setup_filters("V", "D") is False

    def test_page_search_and_download_exception(self, page):  # noqa: ANN001
        """Verifica cattura errore ricerca."""
        page.wait.until.side_effect = Exception("Search Error")
        assert page.search_and_download("ODA", "POS", Path(".")) is False

    # ========================================================================
    # 3. FILE SYSTEM & UNIQUE PATHS
    # ========================================================================

    def test_resolve_unique_path_logic(self, page):  # noqa: ANN001
        """Verifica generazione path unico ODA-POS.xlsx."""
        with patch("pathlib.Path.exists", return_value=False):
            dest_dir = Path("C:/Dest")
            current_file = Path("C:/Downloads/temp.xlsx")
            res = page._resolve_unique_path(dest_dir, "ODA1", "10", current_file)
            assert res.name == "ODA1-10.xlsx"

    def test_resolve_unique_path_fallback_locked(self, page):  # noqa: ANN001
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

    def test_bot_run_success_cycle(self, bot, mocker):  # noqa: ANN001
        """Test di esecuzione bot completo con una riga."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_navigate_to_timesheet", return_value=True)
        mocker.patch.object(bot, "_setup_filters", return_value=True)
        mocker.patch.object(bot, "_process_oda_rows", return_value=(1, [Path("test.xlsx")]))
        mocker.patch.object(bot, "_run_vba_processing")

        data = [{"numero_oda": "123"}]
        assert bot.run(data) is True
        bot._process_oda_rows.assert_called_once()

    def test_bot_run_filter_failure(self, bot, mocker):  # noqa: ANN001
        """Test fallimento setup iniziale filtri."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_navigate_to_timesheet", return_value=True)
        mocker.patch.object(bot, "_setup_filters", return_value=False)

        assert bot.run([{"numero_oda": "1"}]) is False

    def test_bot_search_oda_exception(self, bot, mocker):  # noqa: ANN001
        """Verifica hardening _search_oda con blocco try/except."""
        mocker.patch.object(bot, "_attendi_scomparsa_overlay")
        # Simulo errore nel driver durante l'inserimento campi
        bot.driver.execute_script.side_effect = Exception("Selenium Timeout")

        # Deve catturare l'errore e tornare False, non crashare
        res = bot._search_oda("123", "10")
        assert res is False

    def test_page_wait_for_download_timeout(self, page, mocker):  # noqa: ANN001
        """Verifica timeout download."""
        mocker.patch("time.time", side_effect=[0, 1000])  # Forza superamento timeout
        res = page._wait_for_download(Path("."), set())
        assert res is None

    def test_page_download_cleanup_integration(self, page, tmp_path, mocker):  # noqa: ANN001
        """Verifica cleanup Chromium residui (marker GUID) durante download."""
        download_dir = tmp_path / "downloads"
        download_dir.mkdir()

        # Mock ActionChains per evitare errori JS dispatch
        mocker.patch("src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page.ActionChains")

        mocker.patch.object(page, "_wait_for_download", return_value=download_dir / "test.xlsx")
        mocker.patch.object(page, "_resolve_unique_path", return_value=download_dir / "final.xlsx")
        # Mocking click per evitare chiamate driver reali
        mocker.patch.object(page, "_wait_for_overlay")
        mock_cleanup = mocker.patch("src.utils.helpers.cleanup_chrome_temp_files", return_value=["marker"])

        # Mock driver.find_element e wait.until per tutti i bottoni/campi
        mock_el = MagicMock(spec=WebElement)
        page.driver.find_element.return_value = mock_el
        page.wait.until.return_value = mock_el

        # Mock interdir del download_dir specifico (non globale)
        mocker.patch.object(Path, "iterdir", return_value=[])

        # Creiamo il file fisico perché rename() non fallisca
        test_file = download_dir / "test.xlsx"
        test_file.write_text("dummy")

        res = page.search_and_download("ODA", "POS", download_dir)

        assert res is True
        mock_cleanup.assert_called()
