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
from selenium.webdriver.remote.webelement import WebElement

from src.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot
from src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page import DettagliOdAPage
from src.core.constants import BotStatus


class TestDettagliOdaComprehensive:
    @pytest.fixture
    def bot(self, mocker):
        """Inizializzazione bot con mock totali."""
        mocker.patch("src.bots.base.base_bot.BaseBot.__init__", return_value=None)
        bot = DettagliOdABot()
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot._log_callback = MagicMock()
        bot._logger = MagicMock()
        bot._trace_id = "trace-oda"
        bot._stop_requested = False
        bot._status = BotStatus.IDLE
        bot._telegram_service = None
        bot.username = "test"
        bot.password = "test"
        bot.download_path = "C:/fake/downloads"
        bot.data_da = "01.01.2024"
        bot.data_a = "31.12.2025"
        bot.fornitore = "KK10608 - COEMI S.R.L."
        return bot

    @pytest.fixture
    def page(self, bot):
        """Inizializzazione Page Object."""
        p = DettagliOdAPage(bot.driver, bot.log)
        p.wait = MagicMock()
        p.long_wait = MagicMock()
        return p

    # ========================================================================
    # 1. BOT LOGIC & DATA FLOW
    # ========================================================================

    def test_bot_validate_data(self, bot):
        """Verifica validazione input."""
        ok, _ = bot.validate_data([])
        assert ok is True

    def test_bot_run_loop_success(self, bot, mocker):
        """Verifica il loop principale di esecuzione su più OdA."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_process_single_oda", return_value=True)
        mocker.patch("src.bots.portale_fornitori.dettagli_oda.bot.OdaManager.init_db")
        data = [{"numero_oda": "ODA1"}, {"numero_oda": "ODA2"}]

        res = bot.run(data)

        assert res is True
        assert bot._process_single_oda.call_count == 2

    def test_bot_import_oda_to_db(self, bot, mocker):
        """Verifica l'integrazione con OdaManager."""
        mock_manager = mocker.patch("src.bots.portale_fornitori.dettagli_oda.bot.OdaManager")
        mock_manager.import_oda_from_excel.return_value = (True, "OK", 5, [])

        bot._import_oda_to_db(Path("test.xlsx"))

        mock_manager.import_oda_from_excel.assert_called_once()

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
        mock_option = MagicMock(spec=WebElement)

        page.wait.until.side_effect = [mock_arrow, mock_option]

        res = page.setup_supplier("COEMI")

        assert res is True
        mock_ec.presence_of_element_located.assert_called()

    # ========================================================================
    # 3. PAGE OBJECT - DOWNLOAD & CLEANUP
    # ========================================================================

    def test_page_close_all_tabs(self, page):
        """Verifica chiusura tab multiple via script (metodo privato _close_all_tabs)."""
        mock_btn = MagicMock()
        mock_btn.is_displayed.side_effect = [True, False]
        page.driver.find_element.return_value = mock_btn

        page._close_all_tabs()

        assert page.driver.execute_script.call_count == 1

    def test_page_process_oda_no_results(self, page, mocker):
        """Test process_oda quando non ci sono risultati nella grid."""
        page._wait_for_overlay = MagicMock()
        mocker.patch.object(page, "_close_all_tabs")

        # Simula grid vuota
        mock_label = MagicMock()
        mock_label.text = "Risultati: 0"
        page.wait.until.return_value = mock_label

        res = page.process_oda("ODA", "CON", "01.01", "02.01", Path("."), Path("."))
        assert res is None
        page._close_all_tabs.assert_called()

    def test_wait_for_download_with_crdownload(self, page, tmp_path, mocker):
        """Verifica polling download che ignora file .crdownload."""
        temp_file = tmp_path / "data.xlsx.crdownload"
        temp_file.write_text("partial data")

        mocker.patch("pathlib.Path.iterdir", return_value=[temp_file])
        mocker.patch("time.time", side_effect=[0, 1000])

        res = page._wait_for_download(tmp_path, set())
        assert res is None

    # ========================================================================
    # 4. ERROR HANDLING & ROBUSTNESS
    # ========================================================================

    def test_bot_run_no_oda_list_general(self, bot, mocker):
        """Verifica gestione lista vuota che innesca ricerca generale."""
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_process_single_oda", return_value=True)
        mocker.patch("src.bots.portale_fornitori.dettagli_oda.bot.OdaManager.init_db")

        assert bot.run([]) is True
        bot._process_single_oda.assert_called_once()

    def test_bot_process_single_oda_nav_failure(self, bot, mocker):
        """Test fallimento navigazione durante processamento singolo OdA."""
        mock_page = MagicMock()
        mock_page.navigate_to_dettagli.return_value = False

        res = bot._process_single_oda(
            mock_page, {"numero_oda": "123"}, index=1, source_dir=Path("."), dest_dir=Path(".")
        )
        assert res is False

    def test_bot_import_oda_to_db_failure(self, bot, mocker):
        """Verifica gestione errori durante importazione DB."""
        mock_manager = mocker.patch("src.bots.portale_fornitori.dettagli_oda.bot.OdaManager")
        mock_manager.import_oda_from_excel.side_effect = Exception("DB Locked")

        bot._import_oda_to_db(Path("test.xlsx"))
        mock_manager.import_oda_from_excel.assert_called_once()

    def test_page_navigation_exception(self, page):
        """Verifica che navigate_to_dettagli gestisca eccezioni driver."""
        page.driver.execute_script.side_effect = Exception("JS Error")
        res = page.navigate_to_dettagli(is_first_row=True)
        assert res is False

    def test_page_logout_full_flow(self, page, mocker):
        """Test logout con tentativi multipli e JS fallback."""
        mock_btn = MagicMock()
        page.wait.until.return_value = mock_btn
        assert page.logout() is True
        assert page.driver.execute_script.call_count >= 1

    def test_page_logout_exception(self, page):
        """Test logout con errore fatale driver."""
        page.wait.until.side_effect = Exception("Fatal")
        assert page.logout() is False

    def test_page_click_export_button_direct(self, page, mocker):
        """Test click diretto su export button."""
        mock_btn = MagicMock()
        page.wait.until.return_value = mock_btn

        res = page._click_export_button(("id", "btn"))
        assert res is True
        mock_btn.click.assert_called_once()

    def test_base_bot_final_cleanup(self, bot):
        """Verifica che il cleanup finale del bot chiami quit()."""
        saved_driver = bot.driver
        bot.cleanup()
        saved_driver.quit.assert_called_once()
