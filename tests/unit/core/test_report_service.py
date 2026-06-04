from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

from src.application.services.report_service import ReportService


class TestReportService:
    @patch("src.application.services.report_service.db_manager.execute_query")
    def test_collect_employee_status_lists(self, mock_query):
        # Dipendenti: id, cognome, nome, CF, badge, data_ass
        dips = [
            (1, "ROSSI", "MARIO", "CF1", "B1", "2020-01-01"),
            (2, "VERDI", "LUIGI", "CF2", "B2", "2020-01-01"),
            (3, "BIANCHI", "PAOLO", "CF3", "B3", "2020-01-01"),
            (4, "NERI", "GINO", "CF4", "B4", "2020-01-01"),
        ]

        # Accessi: cognome, nome, CF, data
        today = datetime.now(UTC)
        date_ok = (today - timedelta(days=5)).strftime("%Y-%m-%d")
        date_warn = (today - timedelta(days=25)).strftime("%Y-%m-%d")
        date_exp = (today - timedelta(days=40)).strftime("%Y-%m-%d")

        accs = [
            ("ROSSI", "MARIO", "CF1", date_ok),
            ("VERDI", "LUIGI", "CF2", date_warn),
            ("BIANCHI", "PAOLO", "CF3", date_exp),
        ]

        mock_query.side_effect = [dips, accs]

        w_list, e_list = ReportService._collect_employee_status_lists()

        assert len(w_list) == 1
        assert w_list[0]["cognome"] == "VERDI"
        assert w_list[0]["giorni"] == 25

        assert len(e_list) == 1
        assert e_list[0]["cognome"] == "BIANCHI"
        assert e_list[0]["giorni"] == 40

    @patch("src.application.services.report_service.os.name", "nt")
    @patch("src.application.services.report_service.win32_client")
    @patch("src.application.services.report_service.ReportService._collect_employee_status_lists")
    @patch("src.application.services.report_service.ReportHistory.save_report")
    @patch("src.application.services.report_service.config_manager.set_config_value")
    @patch("src.application.services.report_service.NotificationManager.instance")
    def test_send_scheduled_report_email_success(
        self, mock_notif, mock_set, mock_save, mock_collect, mock_win32
    ):
        w_list = [{"cognome": "V", "nome": "L", "giorni": 25, "data": "01/01/2026"}]
        e_list = [{"cognome": "B", "nome": "P", "giorni": 40, "data": "01/01/2026"}]
        mock_collect.return_value = (w_list, e_list)

        mock_outlook = MagicMock()
        mock_win32.Dispatch.return_value = mock_outlook
        mock_mail = MagicMock()
        mock_outlook.CreateItem.return_value = mock_mail

        ReportService.send_scheduled_report_email()

        assert mock_mail.Send.called
        assert mock_save.called
        assert mock_set.called
        assert mock_notif.return_value.add_notification.called
        assert mock_mail.To == "supporto@syncrojob.it"

    def test_norm_text(self):
        assert ReportService._norm_text("  Rossi   Mario  ") == "ROSSI MARIO"
        assert ReportService._norm_text(None) == "NONE"
        assert ReportService._norm_text(123) == "123"

    def test_build_access_maps_formats(self):
        today = datetime.now(UTC)
        d1 = (today - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        d2 = (today - timedelta(days=20)).strftime("%d/%m/%Y")

        accessi = [
            ("Rossi", "Mario", "CF1", d1),
            ("Verdi", "Luigi", None, d2),
            ("Neri", "Gino", "CF4", ""),  # Data vuota
        ]

        l_cf, l_nm = ReportService._build_access_maps(accessi)

        assert l_cf["CF1"] == 10
        assert l_nm[("VERDI", "LUIGI")] == 20
        assert "CF4" not in l_cf

    @patch("src.application.services.report_service.win32_client", None)
    @patch("src.application.services.report_service.logger")
    def test_dispatch_outlook_no_client(self, mock_logger):
        ReportService._dispatch_outlook_email([], [])
        assert mock_logger.error.called
        assert "non disponibile" in mock_logger.error.call_args[0][0]

    @patch("src.application.services.report_service.ReportService._collect_employee_status_lists")
    @patch("src.application.services.report_service.logger")
    def test_send_scheduled_report_empty(self, mock_logger, mock_collect):
        mock_collect.return_value = ([], [])
        ReportService.send_scheduled_report_email()
        assert mock_logger.info.called

    @patch("src.application.services.report_service.os.name", "posix")
    @patch("src.application.services.report_service.ReportService._collect_employee_status_lists")
    @patch("src.application.services.report_service.logger")
    def test_send_scheduled_report_wrong_os(self, mock_logger, mock_collect):
        mock_collect.return_value = ([{"x": 1}], [])
        ReportService.send_scheduled_report_email()
        assert mock_logger.warning.called
