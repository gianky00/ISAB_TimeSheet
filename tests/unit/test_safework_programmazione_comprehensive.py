import unittest
from unittest.mock import MagicMock, patch

from selenium.webdriver.common.by import By

from src.bots.safework.pages.visualizza_attivita_page import VisualizzaAttivitaPage
from src.bots.safework.programmazione.bot import SafeWorkProgrammazioneBot


class TestSafeWorkProgrammazioneComprehensive(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        with patch("src.bots.safework.base.SafeworkBaseBot.__init__", return_value=None):
            self.bot = SafeWorkProgrammazioneBot("user", "pass")
            self.bot.signals = MagicMock()  # Inizializza manualmente signals

            # Inizializza mock per step_manager (necessario dopo refactoring SRP)
            self.bot.step_manager = MagicMock()
            self.bot.step_manager.update_step.return_value = (0, "test-step")
            self.bot.step_manager.current_step_name = "test-step"
            self.bot.step_manager.current_index = 0

            self.bot.driver = self.mock_driver
            self.bot._log_callback = None
            self.bot._input_callback = None
            self.bot._progress_callback = None
            self.bot._logger = MagicMock()
            self.bot._trace_id = "test-trace"
            self.bot._status = MagicMock()
            self.bot._status.name = "RUNNING"
            self.bot._telegram_service = None
            self.bot.download_path = "C:/fake/downloads"
            self.bot.attivita_page = MagicMock()

    def test_properties(self):
        self.assertEqual(self.bot.get_name(), "Programmazione PDL")
        self.assertEqual(self.bot.name, "programmazione_pdl")

    @patch("src.bots.safework.programmazione.bot.pd.read_excel")
    @patch("src.bots.safework.programmazione.bot.poll_for_new_file")
    @patch.object(SafeWorkProgrammazioneBot, "click_robusto")
    @patch.object(SafeWorkProgrammazioneBot, "_attendi_scomparsa_overlay")
    def test_run_success_flow(self, mock_overlay, mock_click, mock_poll, mock_read_excel):
        data = [{"requesters": ["RICH1"], "date_start": "01/01/2026", "date_end": "07/01/2026"}]
        mock_poll.return_value = "fake_report.xlsx"

        # DataFrame columns: A(0):PDL, B(1):Desc, C(2):TCL1, D(3):TGO1... R(17):Req, X(23):Unit, Y(24):Area
        cols = list(range(25))  # Fix C416
        row_data = (
            ["PDL001", "TEST DESC", "Si", "No", "No", "Si"]
            + ["No"] * 11
            + ["RICH1"]
            + [""] * 5
            + ["U1", "A1"]
        )
        # Mocking pandas row access (iloc used in bot)
        mock_df = MagicMock()
        mock_row = MagicMock()
        mock_row.iloc = row_data
        mock_row.__len__.return_value = 25
        mock_df.iterrows.return_value = [(0, mock_row)]
        mock_read_excel.return_value = mock_df

        with patch("src.bots.safework.programmazione.bot.Path.unlink"):
            result = self.bot.run(data)

            self.assertTrue(result)
            self.assertEqual(len(self.bot.results), 1)
            res = self.bot.results[0]
            self.assertEqual(res["pdl"], "PDL001")


class TestVisualizzaAttivitaPageComprehensive(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_wait = MagicMock()
        self.mock_log = MagicMock()
        self.page = VisualizzaAttivitaPage(self.mock_driver, self.mock_wait, self.mock_log)

    def test_imposta_date_js(self):
        self.page.imposta_date("01/01/2026", "02/01/2026")
        calls = self.mock_driver.execute_script.call_args_list
        self.assertTrue(any("programmazioneDal').value = '01/01/2026'" in c[0][0] for c in calls))

    def test_seleziona_da_dropdown_multiple(self):
        mock_btn = MagicMock()
        mock_dropdown = MagicMock()
        mock_input = MagicMock()
        mock_opt = MagicMock()

        self.mock_wait.until.side_effect = [mock_btn, mock_dropdown]
        mock_dropdown.find_element.side_effect = [mock_input, mock_opt, mock_opt]

        result = self.page.seleziona_richiedente(["REQ1", "REQ2"])

        self.assertTrue(result)
        mock_input.send_keys.assert_any_call("REQ1")
        self.mock_driver.find_element.assert_called_with(By.TAG_NAME, "body")

    def test_esporta_excel_success(self):
        mock_btn = MagicMock()
        self.mock_wait.until.return_value = mock_btn
        result = self.page.esporta_excel()
        self.assertTrue(result)
        mock_btn.click.assert_called_once()


if __name__ == "__main__":
    unittest.main()
