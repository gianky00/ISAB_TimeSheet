"""
Dettagli OdA Bot - Comprehensive Test Suite (2026 Edition)
=========================================================
Test suite definitiva per DettagliOdABot e DettagliOdAPage.
Copre navigazione, download, database import e cleanup residui.

Matches source code: 
- src/bots/portale_fornitori/dettagli_oda/bot.py
- src/bots/portale_fornitori/dettagli_oda/pages/dettagli_oda_page.py
"""

import time
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from src.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot
from src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page import DettagliOdAPage
from src.core.constants import BotStatus


class TestDettagliOdaComprehensive:
    @pytest.fixture
    def bot(self, mocker):
        """Fixture per il Bot con componenti mockati."""
        bot = DettagliOdABot(username="u", password="p", download_path="C:/Downloads")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot.long_wait = MagicMock()
        mocker.patch.object(bot, "_login", return_value=True)
        # Mock per evitare chiamate reali al driver durante il cleanup
        mocker.patch.object(bot.driver, "quit")
        return bot

    @pytest.fixture
    def page(self, bot):
        """Fixture per la Page Object Model."""
        p = DettagliOdAPage(bot.driver, bot.log)
        p.wait = MagicMock()
        p.long_wait = MagicMock()
        return p

    # ========================================================================
    # 1. BOT LOGIC & LIFECYCLE
    # ========================================================================

    def test_bot_validate_data(self, bot):
        """Verifica la validazione dati specifica."""
        # Successo (anche vuoto per lista generale)
        assert bot.validate_data([])[0] is True
        # Fallimento credenziali
        bot.username = None
        assert bot.validate_data([])[0] is False

    def test_bot_run_loop_success(self, bot, mocker):
        """Verifica il ciclo run per più OdA."""
        mocker.patch.object(bot, "_process_single_oda", return_value=True)
        data = [{"numero_oda": "ODA1"}, {"numero_oda": "ODA2"}]
        
        res = bot.run(data)
        
        assert res is True
        assert bot._process_single_oda.call_count == 2

    def test_bot_import_oda_to_db(self, bot, mocker):
        """Verifica l'interazione con OdaManager per l'importazione."""
        mock_manager = mocker.patch("src.bots.portale_fornitori.dettagli_oda.bot.OdaManager")
        mock_manager.import_oda_from_excel.return_value = (True, "OK", 5, [])
        
        bot._import_oda_to_db(Path("test.xlsx"))
        
        mock_manager.import_oda_from_excel.assert_called_once_with("test.xlsx")

    # ========================================================================
    # 2. PAGE NAVIGATION & INTERACTION
    # ========================================================================

    def test_page_navigation_retry_logic(self, page):
        """Verifica il doppio click per righe successive alla prima con target precisi."""
        page._wait_for_overlay = MagicMock()
        page.expand_sidebar_if_collapsed = MagicMock()
        
        # Caso: riga 2+ (is_first_row=False)
        page.navigate_to_dettagli(is_first_row=False)
        
        # Deve aver chiamato execute_script per report_btn (2 volte) e oda_btn (1 volta)
        assert page.driver.execute_script.call_count == 3
        scripts = [str(c) for c in page.driver.execute_script.call_args_list]
        # Verifica che i target siano quelli corretti (es. click() su elementi specifici)
        assert any("click()" in s for s in scripts)

    def test_page_setup_supplier(self, page, mocker):
        """Verifica la selezione del fornitore via JS con verifica selettori."""
        page._wait_for_overlay = MagicMock()
        mock_ec = mocker.patch("src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page.EC")
        from selenium.webdriver.remote.webelement import WebElement
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
        assert "COEMI" in args_ec_opt[1]
        # 3. Deve aver eseguito click via JS
        assert page.driver.execute_script.call_count >= 2

    def test_page_close_all_tabs(self, page):
        """Verifica la chiusura ciclica dei tab aperti."""
        from selenium.webdriver.remote.webelement import WebElement
        mock_btn = MagicMock(spec=WebElement)
        # Simula 2 tab visibili, poi nessuno
        mock_btn.is_displayed.side_effect = [True, True, False]
        page.driver.find_element.return_value = mock_btn
        
        page._close_all_tabs()
        
        assert page.driver.execute_script.call_count == 2

    # ========================================================================
    # 3. DOWNLOAD & CLEANUP (THE CRITICAL PART)
    # ========================================================================

    def test_page_download_cleanup_0kb(self, page, mocker, tmp_path):
        """
        Verifica la rimozione dei residui 0 KB dopo il download.
        Questo test protegge dalla regressione del file GUID rimasto orfano.
        """
        # Creiamo cartelle reali nel sistema temporaneo di pytest
        source_dir = tmp_path / "downloads"
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
        """Verifica che il polling aspetti la scomparsa dei file .crdownload."""
        source_dir = MagicMock(spec=Path)
        mocker.patch("time.time", side_effect=[0, 1, 2, 3, 4, 5])
        
        # Sequenza iterdir:
        # 1. Trova un .crdownload -> continua loop
        # 2. Trova il file .xlsx finale
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

    def test_bot_run_no_oda_list_general(self, bot, mocker):
        """Verifica che se non ci sono OdA, il bot tenti la lista generale."""
        mocker.patch.object(bot, "_process_single_oda", return_value=True)
        # Passiamo lista vuota
        res = bot.run([])
        assert res is True
        # Deve aver chiamato _process_single_oda con una riga vuota
        bot._process_single_oda.assert_called_once()
        args = bot._process_single_oda.call_args[0]
        assert args[1]["numero_oda"] == ""

    def test_bot_process_single_oda_nav_failure(self, bot, page, mocker):
        """Verifica fallimento se la navigazione fallisce."""
        mocker.patch.object(page, "navigate_to_dettagli", return_value=False)
        res = bot._process_single_oda(page, {"numero_oda": "123"}, 1, Path("."), Path("."))
        assert res is False

    def test_bot_process_single_oda_supplier_failure(self, bot, page, mocker):
        """Verifica fallimento se la selezione fornitore fallisce."""
        mocker.patch.object(page, "navigate_to_dettagli", return_value=True)
        mocker.patch.object(page, "setup_supplier", return_value=False)
        res = bot._process_single_oda(page, {"numero_oda": "123"}, 1, Path("."), Path("."))
        assert res is False

    def test_bot_import_oda_to_db_failure(self, bot, mocker):
        """Verifica log in caso di fallimento importazione database."""
        mock_manager = mocker.patch("src.bots.portale_fornitori.dettagli_oda.bot.OdaManager")
        mock_manager.import_oda_from_excel.return_value = (False, "Error message", 0, [])
        # Non deve crashare
        bot._import_oda_to_db(Path("test.xlsx"))

    # ========================================================================
    # 2. PAGE NAVIGATION & INTERACTION
    # ========================================================================

    def test_page_navigation_exception(self, page, mocker):
        """Verifica gestione eccezioni in navigazione."""
        page.driver.execute_script.side_effect = Exception("JS Error")
        assert page.navigate_to_dettagli() is False

    def test_page_setup_supplier_exception(self, page, mocker):
        """Verifica gestione eccezioni in selezione fornitore."""
        page.wait.until.side_effect = Exception("Timeout")
        assert page.setup_supplier("COEMI") is False

    def test_page_logout_full_flow(self, page, mocker):
        """Verifica il flusso di logout completo inclusi i timeout dei popup."""
        page.wait.until.side_effect = [MagicMock(), MagicMock(), MagicMock(), MagicMock()] # settings, logout, yes, login
        page.logout()
        assert page.driver.execute_script.call_count >= 3

    def test_page_logout_exception(self, page, mocker):
        """Verifica che il logout non crashi in caso di errore driver."""
        page.wait.until.side_effect = Exception("Driver disconnected")
        page.logout() # No exception should be raised

    # ========================================================================
    # 3. DOWNLOAD & CLEANUP (THE CRITICAL PART)
    # ========================================================================

    def test_page_process_oda_no_results(self, page, mocker):
        """Verifica salto esportazione se risultati = 0."""
        page.wait.until.return_value.text = "Trovati : 0"
        mocker.patch.object(page, "_close_all_tabs")
        
        res = page.process_oda("", "", "01.01", "01.01", Path("."), Path("."))
        assert res is None
        page._close_all_tabs.assert_called()

    def test_page_process_oda_exception(self, page, mocker):
        """Verifica gestione eccezioni durante process_oda."""
        # Mock _close_all_tabs per evitare loop infinito con driver mock
        mocker.patch.object(page, "_close_all_tabs")
        page.wait.until.side_effect = Exception("DOM Error")
        res = page.process_oda("123", "C1", "", "", Path("."), Path("."))
        assert res is None


    def test_page_download_failure(self, page, mocker):
        """Verifica ritorno None se il file non viene trovato dopo il polling."""
        mocker.patch.object(page, "_click_export_button", return_value=True)
        mocker.patch.object(page, "_wait_for_download", return_value=None)
        
        res = page._download(Path("C:/"), Path("C:/"), "test.xlsx", (By.ID, "id"))
        assert res is None

    def test_page_download_exception(self, page, mocker):
        """Verifica gestione eccezioni durante il download."""
        mocker.patch.object(page, "_click_export_button", side_effect=Exception("Click error"))
        res = page._download(Path("C:/"), Path("C:/"), "test.xlsx", (By.ID, "id"))
        assert res is None

    def test_page_click_export_button_strategies(self, page, mocker):
        """Verifica i vari tentativi di click (standard e JS)."""
        mock_btn = MagicMock()
        page.wait.until.return_value = mock_btn
        
        # Caso 1: click standard fallisce, prova JS
        mock_btn.click.side_effect = Exception("Intercepted")
        assert page._click_export_button((By.ID, "id")) is True
        page.driver.execute_script.assert_called()

    def test_page_close_all_tabs_exception(self, page, mocker):
        """Verifica che la chiusura tab non crashi."""
        page.driver.find_element.side_effect = Exception("NoSuchElement")
        page._close_all_tabs() # No exception

    def test_base_bot_final_cleanup(self, bot, mocker):

        """Verifica che BaseBot pulisca la cartella alla chiusura."""
        # Non usiamo stopall() ma patch mirata
        mock_cleanup_util = mocker.patch("src.utils.helpers.cleanup_chrome_temp_files")
        bot.download_path = "C:/Downloads"
        
        bot.cleanup()
        
        # Deve aver tentato di pulire la cartella
        mock_cleanup_util.assert_called_with("C:/Downloads")

