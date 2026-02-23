import unittest
from unittest.mock import MagicMock, patch

from src.bots.portale_fornitori.carico_ts.bot import CaricoTSBot
from src.bots.portale_fornitori.carico_ts.pages.carico_ts_page import CaricoTSPage


class TestCaricoTSBotComprehensive(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        with patch("src.bots.base.base_bot.BaseBot.__init__", return_value=None):
            self.bot = CaricoTSBot()
            self.bot.driver = self.mock_driver
            self.bot._log_callback = MagicMock()
            self.bot._logger = MagicMock()
            self.bot._trace_id = "trace-123"
            self.bot._status = MagicMock()
            self.bot._status.name = "IDLE"
            self.bot._telegram_service = None

    def test_properties(self):
        self.assertEqual(self.bot.get_name(), "Carico TS")
        self.assertEqual(len(self.bot.get_columns()), 16)

    def test_validate_data(self):
        # Parent validation success
        with patch("src.bots.base.base_bot.BaseBot.validate_data", return_value=(True, "")):
            # Missing oda
            valid, msg = self.bot.validate_data({"rows": [{"nome": "M"}]})
            self.assertFalse(valid)
            self.assertIn("Numero OdA mancante", msg)

            # Valid
            valid, msg = self.bot.validate_data({"rows": [{"numero_oda": "123"}]})
            self.assertTrue(valid)

    @patch("src.bots.portale_fornitori.carico_ts.bot.CaricoTSPage")
    def test_run_success(self, mock_page_class):
        mock_page = mock_page_class.return_value
        mock_page.navigate.return_value = True
        mock_page.select_supplier.return_value = True
        mock_page.process_oda.return_value = True

        result = self.bot.run([{"numero_oda": "123"}])

        self.assertTrue(result)
        mock_page.navigate.assert_called_once()
        mock_page.process_oda.assert_called_with("123")


class TestCaricoTSPageComprehensive(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_log = MagicMock()
        with patch(
            "src.bots.portale_fornitori.carico_ts.pages.carico_ts_page.WebDriverWait"
        ) as mock_wait_class:
            self.mock_wait = MagicMock()
            mock_wait_class.return_value = self.mock_wait
            self.page = CaricoTSPage(self.mock_driver, self.mock_log)

    @patch("src.bots.portale_fornitori.carico_ts.pages.carico_ts_page.EC")
    def test_navigate_success(self, mock_ec):
        mock_btn = MagicMock()
        self.mock_wait.until.return_value = mock_btn

        # _wait_overlay internal call
        with patch(
            "src.bots.portale_fornitori.carico_ts.pages.carico_ts_page.WebDriverWait"
        ) as mock_wait_overlay:
            result = self.page.navigate()
            self.assertTrue(result)
            mock_btn.click.assert_called_once()

    @patch("src.bots.portale_fornitori.carico_ts.pages.carico_ts_page.ActionChains")
    @patch("src.bots.portale_fornitori.carico_ts.pages.carico_ts_page.EC")
    def test_select_supplier_flow(self, mock_ec, mock_action_class):
        mock_arrow = MagicMock()
        mock_opt = MagicMock()

        # 1. wait.until per arrow (navigate)
        # 2. wait.until per arrow (select_supplier)
        self.mock_wait.until.side_effect = [mock_arrow]

        # New WebDriverWait(driver, 5) for option
        with patch(
            "src.bots.portale_fornitori.carico_ts.pages.carico_ts_page.WebDriverWait"
        ) as mock_local_wait_class:
            mock_local_wait = MagicMock()
            mock_local_wait_class.return_value = mock_local_wait
            mock_local_wait.until.return_value = mock_opt

            result = self.page.select_supplier("VENDOR")

            self.assertTrue(result)
            mock_action_class.return_value.move_to_element.assert_called_with(mock_arrow)
            self.mock_driver.execute_script.assert_any_call("arguments[0].click();", mock_opt)

    @patch("src.bots.portale_fornitori.carico_ts.pages.carico_ts_page.EC")
    def test_process_oda_js_injection(self, mock_ec):
        mock_inp = MagicMock()
        mock_btn = MagicMock()
        self.mock_wait.until.side_effect = [mock_inp, mock_btn]

        result = self.page.process_oda("ODA123")

        self.assertTrue(result)
        # Verifica iniezione JS complessa per input
        calls = self.mock_driver.execute_script.call_args_list
        self.assertTrue(any("el.dispatchEvent" in c[0][0] for c in calls))
        self.assertTrue(any("ODA123" in str(c[0][2]) for c in calls if len(c[0]) > 2))
        mock_btn.click.assert_called_once()


if __name__ == "__main__":
    unittest.main()
