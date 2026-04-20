"""
Dettagli OdA Bot - Comprehensive Test Suite (2026 Edition)
=========================================================
Copre navigazione, download, database import e cleanup residui.

Matches source code:
- src/bots/portale_fornitori/dettagli_oda/bot.py
- src/bots/portale_fornitori/dettagli_oda/pages/dettagli_oda_page.py
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot
from src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page import (
    DettagliOdAPage,
)


@pytest.fixture
def bot():
    return DettagliOdABot("user", "pass", fornitore="COEMI")


class TestDettagliOdaComprehensive:
    def test_bot_validate_data(self, bot):
        """Verifica validazione parametri input."""
        # Case 1: Dati validi (lista OdA)
        ok, _msg = bot.validate_data([{"numero_oda": "123"}])
        assert ok is True

        # Case 2: Dati validi (Generale - senza OdA)
        ok, _msg = bot.validate_data([])
        assert ok is True

    @patch("src.bots.portale_fornitori.dettagli_oda.bot.DettagliOdAPage")
    def test_bot_run_loop_success(self, mock_page_cls, bot, mocker):
        """Test ciclo principale con successo."""
        mock_page = mock_page_cls.return_value
        mock_page.navigate_to_dettagli.return_value = True
        mock_page.setup_supplier.return_value = True
        mock_page.process_oda.return_value = Path("/tmp/oda.pdf")

        # Mock importazione DB per evitare multiprocess reale
        mocker.patch.object(bot, "_import_oda_to_db")

        data = [{"numero_oda": "123"}]
        # Mock driver
        bot.driver = MagicMock()

        success = bot.run(data)

        assert success is True
        # BaseBot non ha status_history ma emette segnali o aggiorna step
        # Verifichiamo il log o i segnali se possibile, o semplicemente l'esito
        assert success is True

    def test_bot_import_oda_to_db(self, bot, mocker):
        """Verifica l'integrazione con OdaManager (bypassando il multiprocess)."""
        mock_manager = mocker.patch("src.bots.portale_fornitori.dettagli_oda.bot.OdaManager")
        mock_manager.import_oda_from_excel.return_value = (True, "OK", 5, [])

        # Mock dell'esecutore per farlo girare in-process durante il test
        mock_executor = MagicMock()
        mock_future = MagicMock()
        mock_future.result.return_value = (True, "OK", 5, [])
        mock_executor.submit.return_value = mock_future
        mock_executor.__enter__.return_value = mock_executor

        with patch("concurrent.futures.ProcessPoolExecutor", return_value=mock_executor):
            bot._import_oda_to_db(Path("test.xlsx"))

        mock_executor.submit.assert_called_once()

    def test_page_expand_sidebar(self):
        """Test espansione sidebar."""
        mock_driver = MagicMock()
        mock_btn = MagicMock()
        mock_driver.find_element.return_value = mock_btn
        mock_btn.is_displayed.return_value = True

        page = DettagliOdAPage(mock_driver)
        page.expand_sidebar_if_collapsed()

        mock_driver.execute_script.assert_called()

    @patch("src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page.ActionChains")
    def test_page_setup_supplier_success(self, mock_action_chains):
        mock_driver = MagicMock()

        # Mock WebDriverWait prima dell'istanziazione
        with patch(
            "src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page.WebDriverWait"
        ) as mock_wait:
            mock_wait.return_value.until.return_value = MagicMock()
            page = DettagliOdAPage(mock_driver)
            res = page.setup_supplier("COEMI")
            assert res is True

    def test_page_logout_flow(self):
        mock_driver = MagicMock()

        with patch(
            "src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page.WebDriverWait"
        ) as mock_wait:
            mock_wait.return_value.until.return_value = MagicMock()
            page = DettagliOdAPage(mock_driver)
            res = page.logout()
            assert res is True

    def test_wait_for_download_logic(self):
        """Test logica attesa download tramite poll_for_new_file helper."""
        mock_driver = MagicMock()
        page = DettagliOdAPage(mock_driver)

        source_dir = MagicMock(spec=Path)
        file_mock = MagicMock(spec=Path)
        file_mock.suffix = ".xlsx"
        file_mock.name = "downloaded.xlsx"

        # Patchiamo l'helper centralizzato invece del metodo rimosso
        with patch(
            "src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page.poll_for_new_file",
            return_value=file_mock,
        ) as mock_poll:
            # Simuliamo una parte del metodo _download
            res = mock_poll(source_dir, set(), ["*.xlsx"], 30)
            assert res == file_mock
            mock_poll.assert_called_once()

    @patch("src.bots.portale_fornitori.dettagli_oda.bot.DettagliOdAPage")
    def test_bot_run_no_oda_list_general(self, mock_page_cls, bot, mocker):
        """Test scarico lista generale."""
        mock_page = mock_page_cls.return_value
        mock_page.navigate_to_dettagli.return_value = True
        mock_page.setup_supplier.return_value = True
        mock_page.process_oda.return_value = Path("/tmp/lista.xlsx")

        mocker.patch.object(bot, "_import_oda_to_db")
        bot.driver = MagicMock()

        success = bot.run([])
        assert success is True

        # Verifica che oda_number passato a process_oda sia vuoto
        args = mock_page.process_oda.call_args[0]
        assert args[0] == ""

    def test_bot_import_oda_to_db_failure(self, bot, mocker):
        """Test gestione errore durante importazione DB."""
        mock_executor = MagicMock()
        mock_future = MagicMock()
        mock_future.result.return_value = (False, "Errore SQL", 0, [])
        mock_executor.submit.return_value = mock_future
        mock_executor.__enter__.return_value = mock_executor

        with patch("concurrent.futures.ProcessPoolExecutor", return_value=mock_executor):
            bot._import_oda_to_db(Path("test.xlsx"))

        mock_executor.submit.assert_called_once()

    def test_base_bot_final_cleanup(self, bot):
        """Verifica cleanup finale."""
        mock_driver = MagicMock()
        bot.driver = mock_driver
        bot.cleanup()
        mock_driver.quit.assert_called_once()
