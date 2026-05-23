from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

from src.core.report_service import ReportService


class TestReportService:
    @patch("src.core.report_service.db_manager.execute_query")
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
            # NERI non ha accessi -> ignorato dal report (o gestito diversamente, attuale = ignorato se df is None)
        ]

        mock_query.side_effect = [dips, accs]

        w_list, e_list = ReportService._collect_employee_status_lists()

        assert len(w_list) == 1
        assert w_list[0]["cognome"] == "VERDI"
        assert w_list[0]["giorni"] == 25

        assert len(e_list) == 1
        assert e_list[0]["cognome"] == "BIANCHI"
        assert e_list[0]["giorni"] == 40

    @patch("src.core.report_service.os.name", "nt")
    @patch("src.core.report_service.win32_client")
    @patch("src.core.report_service.ReportService._collect_employee_status_lists")
    @patch("src.core.report_service.ReportHistory.save_report")
    @patch("src.core.report_service.config_manager.set_config_value")
    @patch("src.core.report_service.NotificationManager.instance")
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

    @patch("src.core.report_service.ReportService._collect_employee_status_lists")
    @patch("src.core.report_service.logger")
    def test_send_scheduled_report_empty(self, mock_logger, mock_collect):
        mock_collect.return_value = ([], [])
        ReportService.send_scheduled_report_email()
        assert mock_logger.info.called
        assert "Nessun dipendente" in mock_logger.info.call_args[0][0]

    @patch("src.core.report_service.os.name", "posix")
    @patch("src.core.report_service.ReportService._collect_employee_status_lists")
    @patch("src.core.report_service.logger")
    def test_send_scheduled_report_wrong_os(self, mock_logger, mock_collect):
        w_list = [{"cognome": "V", "nome": "L", "giorni": 25, "data": "01/01/2026"}]
        mock_collect.return_value = (w_list, [])

        ReportService.send_scheduled_report_email()
        assert mock_logger.warning.called
        assert "supportato solo su Windows" in mock_logger.warning.call_args[0][0]

    @patch("src.core.report_service.os.name", "nt")
    @patch("src.core.report_service.ReportService._collect_employee_status_lists")
    @patch("src.core.report_service.NotificationManager.instance")
    def test_send_scheduled_report_error(self, mock_notif, mock_collect):
        mock_collect.side_effect = Exception("DB Error")

        ReportService.send_scheduled_report_email()
        assert mock_notif.return_value.add_notification.called
        args = mock_notif.return_value.add_notification.call_args[1]
        assert args["level"] == "error"
