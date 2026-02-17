"""
Dettagli OdA Bot - Comprehensive Test Suite (2026 Edition)
=========================================================
Copre navigazione, download, database import e cleanup residui.

Matches source code:
- src/bots/portale_fornitori/dettagli_oda/bot.py
- src/bots/portale_fornitori/dettagli_oda/pages/dettagli_oda_page.py
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot
from src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page import DettagliOdAPage


class TestDettagliOdaComprehensive:
    @pytest.fixture
    def bot(self, mocker):
        """Inizializzazione bot con mock totali."""
        with mocker.patch("src.bots.base.base_bot.BaseBot.__init__", return_value=None):
            bot = DettagliOdABot()
            bot.driver = MagicMock()
            bot.wait = MagicMock()
            bot._log_callback = MagicMock()
            bot._logger = MagicMock()
            bot._trace_id = "trace-oda"
            bot._stop_requested = False
            bot.download_path = "C:/fake/downloads"
            return bot

    @pytest.fixture
    def page(self, bot):
        """Inizializzazione Page Object."""
        with MagicMock() as mock_wait:
            p = DettagliOdAPage(bot.driver, bot.log)
            p.wait = mock_wait
            p.long_wait = mock_wait
            return p

    # ========================================================================
    # 1. BOT LOGIC & DATA FLOW
    # ========================================================================

    def test_bot_validate_data(self, bot, mocker):
        """Verifica validazione input."""
        mocker.patch("src.bots.base.base_bot.BaseBot.validate_data", return_value=(True, ""))
        # Successo
        ok, _ = bot.validate_data({"rows": [{"numero_oda": "123"}]})
        assert ok is True

    def test_bot_run_loop_success(self, bot, mocker):
        """Verifica il loop principale di esecuzione su più OdA."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_process_single_oda", return_value=True)
        data = [{"numero_oda": "ODA1"}, {"numero_oda": "ODA2"}]

        res = bot.run(data)

        assert res is True
        assert bot._process_single_oda.call_count == 2

    def test_bot_import_oda_to_db(self, bot, mocker):
        """Verifica l'integrazione con OdaManager."""
        mock_manager = mocker.patch("src.bots.portale_fornitori.dettagli_oda.bot.OdaManager")
        mock_manager.import_oda_from_excel.return_value = (True, "OK", 5, [])

        bot._import_oda_to_db(Path("test.xlsx"))

        mock_manager.import_oda_from_excel.assert_called_once_with("test.xlsx")

    # ========================================================================
    # 2. PAGE OBJECT - NAVIGATION & SUPPLIER
    # ========================================================================

    def test_page_navigation_retry_logic(self, page):
        """Verifica navigazione via script con gestione righe successive."""
        page._wait_for_overlay = MagicMock()
        page.expand_sidebar_if_collapsed = MagicMock()

        # Caso: riga 2+ (is_first_row=False)
        page.navigate_to_dettagli(is_first_row=False)

        # Deve aver chiamato execute_script per report_btn (2 volte) e oda_btn (1 volta)
        assert page.driver.execute_script.call_count == 3

    def test_page_setup_supplier(self, page, mocker):
        """Verifica selezione fornitore con selettore dinamico ExtJS."""
        mock_ec = mocker.patch("src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page.EC")
        page._wait_for_overlay = MagicMock()

        mock_arrow = MagicMock(spec=WebElement)
        page.wait.until.return_value = mock_arrow

        mock_option = MagicMock(spec=WebElement)
        page.long_wait.until.return_value = mock_option

        res = page.setup_supplier("COEMI")

        assert res is True
        # 1. Deve aver cercato l'arrow del combo box
        args_ec_arrow = mock_ec.element_to_be_clickable.call_args_list[0][0][0]
        assert "generic_refresh_combo_box-" in str(args_ec_arrow)
        # 2. Deve aver cercato l'opzione con il testo corretto
        args_ec_opt = mock_ec.presence_of_element_located.call_args_list[0][0][0]
        assert "COEMI" in str(args_ec_opt)

    def test_page_close_all_tabs(self, page):
        """Test chiusura tab multipli tramite loop is_displayed."""
        mock_btn = MagicMock(spec=WebElement)
        # Simula: visibile 2 volte, poi scompare
        mock_btn.is_displayed.side_effect = [True, True, False]
        page.driver.find_element.return_value = mock_btn

        page._close_all_tabs()

        assert page.driver.execute_script.call_count == 2

    # ========================================================================
    # 3. DOWNLOAD & CLEANUP
    # ========================================================================

    def test_page_download_cleanup_0kb(self, page, tmp_path, mocker):
        """Verifica cleanup aggressivo file 0KB post-download."""
        source_dir = tmp_path / "source"
        dest_dir = tmp_path / "dest"
        source_dir.mkdir()
        dest_dir.mkdir()

        # Patch per usare i percorsi reali della sandbox pytest
        mocker.patch("src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page.Path.resolve", return_value=source_dir)

        mocker.patch.object(page, "_click_export_button", return_value=True)
        mocker.patch.object(page, "_finalize_download", return_value=dest_dir / "final.xlsx")
        mocker.patch("time.sleep") # Salta attesa reale

        # Mock poll_for_new_file
        mocker.patch.object(page, "_wait_for_download", return_value=source_dir / "temp.xlsx")

        # Mock utility di pulizia
        mock_cleanup = mocker.patch("src.utils.helpers.cleanup_chrome_temp_files", return_value=["residuo_guid"])

        res = page._download(source_dir, dest_dir, "test.xlsx", (By.ID, "btn"))

        assert res is not None
        # Verifica che la pulizia sia stata chiamata DOPO il download
        mock_cleanup.assert_called_once_with(source_dir)

    def test_wait_for_download_with_crdownload(self, page, mocker):
        """Verifica che il bot attenda se trova file .crdownload."""
        source_dir = MagicMock(spec=Path)
        mocker.patch("time.time", side_effect=[0, 1, 2, 3, 4, 5])

        # Sequenza iterdir:
        # 1. Trova un .crdownload -> continua loop
        # 2. Trova il file finale .xlsx -> break
        mock_file = MagicMock(spec=Path)
        mock_file.suffix = ".xlsx"
        mock_file.stat.return_value.st_mtime = 100

        # Configuro iterdir per restituire prima crdownload, poi xlsx
        source_dir.iterdir.side_effect = [
            [MagicMock(suffix=".crdownload")],
            [mock_file],
            [mock_file] # Per il check dei new_files
        ]

        res = page._wait_for_download(source_dir, set())
        assert res == mock_file

    # ========================================================================
    # 4. EDGE CASES & EXCEPTIONS
    # ========================================================================

    def test_bot_run_no_oda_list_general(self, bot):
        """Verifica gestione lista vuota."""
        assert bot.run([]) is True

    def test_bot_process_single_oda_nav_failure(self, bot, mocker):
        """Verifica fallimento navigazione OdA."""
        bot.page = MagicMock()
        bot.page.navigate_to_dettagli.return_value = False
        assert bot._process_single_oda(bot.page, {"numero_oda": "1"}, True, Path("."), Path(".")) is False

    def test_bot_process_single_oda_supplier_failure(self, bot, mocker):
        """Verifica fallimento setup fornitore (solo prima riga)."""
        bot.page = MagicMock()
        bot.page.setup_supplier.return_value = False
        assert bot._process_single_oda(bot.page, {"numero_oda": "1"}, True, Path("."), Path(".")) is False

    def test_bot_import_oda_to_db_failure(self, bot, mocker):
        """Verifica cattura errore import DB."""
        mocker.patch("src.bots.portale_fornitori.dettagli_oda.bot.OdaManager.import_oda_from_excel", side_effect=Exception("DB Locked"))
        # Non deve crashare
        bot._import_oda_to_db(Path("f.xlsx"))

    def test_page_navigation_exception(self, page):
        """Cattura eccezione in navigazione."""
        page.driver.execute_script.side_effect = Exception("JS Error")
        assert page.navigate_to_dettagli() is False

    def test_page_setup_supplier_exception(self, page):
        """Cattura eccezione in setup fornitore."""
        page.wait.until.side_effect = Exception("Element not found")
        assert page.setup_supplier("V") is False

    def test_page_logout_full_flow(self, page, mocker):
        """Test logout con tentativi multipli e JS fallback."""
        mocker.patch.object(page, "_wait_for_overlay")
        mock_btn = MagicMock()
        page.wait.until.return_value = mock_btn
        assert page.logout() is True
        mock_btn.click.assert_called_once()

    def test_page_logout_exception(self, page):
        """Cattura eccezione logout."""
        page.wait.until.side_effect = Exception("Logout failed")
        assert page.logout() is False

    def test_page_process_oda_no_results(self, page, mocker):
        """Verifica gestione OdA inesistente (Trovati: 0)."""
        page._wait_for_overlay = MagicMock()
        page.wait.until.return_value.text = "Trovati : 0"
        mocker.patch.object(page, "_close_all_tabs")

        res = page.process_oda("", "", "01.01", "01.01", Path("."), Path("."))
        assert res is None

    def test_page_process_oda_exception(self, page, mocker):
        """Cattura eccezione in processo OdA."""
        page.wait.until.side_effect = Exception("Search crash")
        mocker.patch.object(page, "_close_all_tabs")
        assert page.process_oda("", "", "", "", Path("."), Path(".")) is None

    def test_page_download_failure(self, page, mocker):
        """Test download fallito (bottone non cliccabile)."""
        mocker.patch.object(page, "_click_export_button", return_value=False)
        res = page._download(Path("C:/"), Path("C:/"), "test.xlsx", (By.ID, "id"))
        assert res is None

    def test_page_download_exception(self, page, mocker):
        """Cattura eccezione download."""
        page.wait.until.side_effect = Exception("Download crash")
        res = page._download(Path("C:/"), Path("C:/"), "test.xlsx", (By.ID, "id"))
        assert res is None

    def test_page_click_export_button_strategies(self, page, mocker):
        """Verifica strategie click bottone export (Selenium poi JS)."""
        mock_btn = MagicMock()
        page.wait.until.return_value = mock_btn

        # Caso 1: click standard fallisce, prova JS
        mock_btn.click.side_effect = Exception("Intercepted")
        assert page._click_export_button((By.ID, "id")) is True
        page.driver.execute_script.assert_called()

    def test_page_close_all_tabs_exception(self, page):
        """Cattura errore chiusura tab."""
        page.driver.find_element.side_effect = Exception("DOM Error")
        # Non deve crashare
        page._close_all_tabs()

    def test_base_bot_final_cleanup(self, bot, mocker):
        """Verifica che BaseBot.cleanup chiami l'utility di pulizia file temp."""
        mock_cleanup_util = mocker.patch("src.utils.helpers.cleanup_chrome_temp_files")
        bot.download_path = "C:/Downloads"

        bot.cleanup()

        # Deve aver tentato di pulire la cartella
        mock_cleanup_util.assert_called_with("C:/Downloads")
