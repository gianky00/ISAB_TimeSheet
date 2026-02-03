import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.gui.panels.dipendenti.utils.report_generator import ReportGenerator


class TestReportGeneratorRobust(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()
        self.logger_patcher = patch(
            "src.gui.panels.dipendenti.utils.report_generator.logger", self.mock_logger
        )
        self.logger_patcher.start()

    def tearDown(self):
        self.logger_patcher.stop()

    @patch("src.gui.panels.dipendenti.utils.report_generator.db_manager")
    @patch(
        "src.gui.panels.dipendenti.utils.report_generator.ReportGenerator._send_report_email"
    )
    @patch(
        "src.gui.panels.dipendenti.utils.report_generator.ReportGenerator._create_report_excel"
    )
    @patch("src.gui.panels.dipendenti.utils.report_generator.build_timbrature_maps")
    def test_generate_email_report_success(
        self, mock_build_maps, mock_create_excel, mock_send_email, mock_db
    ):
        """Test the full generation flow."""
        # Setup mock data
        mock_db.execute_query.side_effect = [
            [(1, "Rossi", "Mario", "RSSMRA...", "123", "2020-01-01")],  # employees
            [("Rossi", "Mario", "RSSMRA...", "2024-01-01")],  # timbrature
        ]
        mock_build_maps.return_value = ({"rssmra...": 25}, {}, lambda x: x.lower())
        mock_create_excel.return_value = Path("/tmp/fake.xlsx")

        ReportGenerator.generate_email_report()

        mock_send_email.assert_called_once()
        # Check that warning_list is in the passed data (third argument)
        self.assertIn("warning_list", mock_send_email.call_args[0][2])

    @patch("win32com.client.Dispatch", create=True)
    @patch("pythoncom.CoInitialize", create=True)
    @patch("src.gui.panels.dipendenti.utils.report_generator.ReportHistory")
    @patch("src.gui.panels.dipendenti.utils.report_generator.ToastManager")
    def test_send_report_email_outlook_success(
        self, mock_toast, mock_history, mock_coinit, mock_dispatch
    ):
        """Test successful email sending via Outlook."""
        mock_outlook = MagicMock()
        mock_dispatch.return_value = mock_outlook
        mock_mail = MagicMock()
        mock_outlook.CreateItem.return_value = mock_mail

        data = {"warning_list": [], "expired_list": []}
        excel_path = Path("fake.xlsx")

        with patch("src.gui.panels.dipendenti.utils.report_generator.os.name", "nt"):
            ReportGenerator._send_report_email("<html></html>", excel_path, data)

        mock_coinit.assert_called_once()
        mock_dispatch.assert_called_with("Outlook.Application")
        mock_mail.Display.assert_called_once()
        mock_toast.instance().show.assert_called()

    @patch("PyQt6.QtGui.QDesktopServices.openUrl", create=True)
    @patch("PyQt6.QtCore.QUrl.fromLocalFile", create=True)
    @patch("src.gui.panels.dipendenti.utils.report_generator.Path.write_text")
    @patch("src.gui.panels.dipendenti.utils.report_generator.ReportHistory")
    @patch("src.gui.panels.dipendenti.utils.report_generator.ToastManager")
    def test_send_report_email_fallback(
        self, mock_toast, mock_history, mock_write, mock_from_local, mock_open_url
    ):
        """Test fallback when Outlook fails or is not available."""
        # Force Outlook failure by making Dispatch raise
        with patch(
            "win32com.client.Dispatch",
            side_effect=Exception("Outlook not found"),
            create=True,
        ):
            with patch(
                "src.gui.panels.dipendenti.utils.report_generator.os.name", "nt"
            ):
                data = {"warning_list": [], "expired_list": []}
                ReportGenerator._send_report_email("<html></html>", None, data)

        mock_write.assert_called_once()
        mock_open_url.assert_called_once()
        self.assertIn(
            "Outlook non disponibile", mock_toast.instance().show.call_args[0][0]
        )
