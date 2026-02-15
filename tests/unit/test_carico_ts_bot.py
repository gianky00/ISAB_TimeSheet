"""
Unit tests for CaricoTSBot and CaricoTSPage.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.carico_ts.bot import CaricoTSBot
from src.bots.portale_fornitori.carico_ts.pages.carico_ts_page import CaricoTSPage


class TestCaricoTSBot:
    @pytest.fixture
    def bot(self):
        return CaricoTSBot("user", "pass")

    def test_initialization(self, bot):
        """Testa l'inizializzazione e le proprietà base."""
        assert bot.name == "Carico TS"
        assert "timesheet" in bot.description.lower()
        assert len(bot.get_columns()) > 0
        assert bot.FORNITORE == "KK10608 - COEMI S.R.L."

    def test_validate_data_success(self, bot):
        """Verifica validazione con dati corretti."""
        data = [{"numero_oda": "123"}]
        valid, msg = bot.validate_data(data)
        assert valid
        assert msg == ""

    def test_validate_data_failure(self, bot):
        """Verifica fallimento validazione."""
        # Caso vuoto
        valid, msg = bot.validate_data([])
        assert not valid
        assert "Nessun dato" in msg

        # Caso OdA mancante
        valid, msg = bot.validate_data([{"altro": "123"}])
        assert not valid
        assert "Numero OdA mancante" in msg

    @patch("src.bots.portale_fornitori.carico_ts.bot.CaricoTSPage")
    def test_run_success(self, mock_page_cls, bot):
        """Verifica il flusso completo di esecuzione con successo."""
        mock_page = mock_page_cls.return_value
        mock_page.navigate.return_value = True
        mock_page.select_supplier.return_value = True
        mock_page.process_oda.return_value = True

        bot.driver = MagicMock()

        data = [{"numero_oda": "ODA123"}]
        result = bot.run(data)

        assert result is True
        mock_page.navigate.assert_called_once()
        mock_page.select_supplier.assert_called_with(bot.FORNITORE)
        mock_page.process_oda.assert_called_with("ODA123")

    @patch("src.bots.portale_fornitori.carico_ts.bot.CaricoTSPage")
    def test_run_navigation_fail(self, mock_page_cls, bot):
        """Verifica interruzione se navigazione fallisce."""
        mock_page = mock_page_cls.return_value
        mock_page.navigate.return_value = False

        bot.driver = MagicMock()
        result = bot.run([{"numero_oda": "123"}])

        assert result is False
        mock_page.select_supplier.assert_not_called()


class TestCaricoTSPage:
    @pytest.fixture
    def page(self):
        driver = MagicMock()
        # Mocking explicitly to avoid method vs mock attribute errors
        with patch("src.bots.portale_fornitori.carico_ts.pages.carico_ts_page.WebDriverWait"):
            return CaricoTSPage(driver)

    def test_navigate_success(self, page):
        """Verifica navigazione con successo."""
        page.wait = MagicMock()  # Replace method with mock
        page.wait.until.return_value = MagicMock()

        with patch.object(page, "_wait_overlay"):
            assert page.navigate() is True
            page.wait.until.assert_called()

    def test_navigate_exception(self, page):
        """Verifica gestione eccezione in navigazione."""
        page.wait = MagicMock()
        page.wait.until.side_effect = Exception("Click failed")
        assert page.navigate() is False

    @patch("src.bots.portale_fornitori.carico_ts.pages.carico_ts_page.ActionChains")
    def test_select_supplier_success(self, mock_ac, page):
        """Verifica selezione fornitore."""
        mock_arrow = MagicMock()
        mock_option = MagicMock()
        page.wait = MagicMock()

        page.wait.until.return_value = mock_arrow

        with patch(
            "src.bots.portale_fornitori.carico_ts.pages.carico_ts_page.WebDriverWait"
        ) as mock_wait_cls:
            mock_wait_cls.return_value.until.return_value = mock_option
            with patch.object(page, "_wait_overlay"):
                res = page.select_supplier("Fornitore X")
                assert res is True
                mock_ac.return_value.move_to_element.assert_called_with(mock_arrow)

    def test_process_oda_success(self, page):
        """Verifica inserimento OdA e click estrazione."""
        mock_input = MagicMock()
        mock_btn = MagicMock()
        page.wait = MagicMock()

        page.wait.until.side_effect = [mock_input, mock_btn]

        assert page.process_oda("ODA-TEST") is True
        mock_btn.click.assert_called_once()
