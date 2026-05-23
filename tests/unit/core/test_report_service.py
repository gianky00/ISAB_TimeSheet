from unittest.mock import MagicMock, patch

from src.core.report_service import ReportService


class TestReportService:
    def test_norm_text(self):
        assert ReportService._norm_text("  mario  rossi  ") == "MARIO ROSSI"
        assert ReportService._norm_text(None) == "NONE"

    def test_build_access_maps(self):
        # r[0]: cognome, r[1]: nome, r[2]: cf, r[3]: data
        accessi = [
            ("Rossi", "Mario", "CF1", "2023-05-01"),
            ("Bianchi", "Luigi", "CF2", "2023-01-01"),
        ]

        l_cf, l_nm = ReportService._build_access_maps(accessi)

        assert "CF1" in l_cf
        assert ("ROSSI", "MARIO") in l_nm

    @patch("src.core.report_service.db_manager.execute_query")
    def test_collect_employee_status_lists(self, mock_query):
        # Mock dipendenti: id, cognome, nome, cf, badge, assunzione
        mock_query.side_effect = [
            [(1, "Rossi", "Mario", "CF1", "B1", "2020-01-01")],
            [("Rossi", "Mario", "CF1", "2023-04-23")],  # Un mese fa circa
        ]

        # Patching datetime.now(UTC) per avere delta fissi
        from datetime import UTC, datetime

        with patch("src.core.report_service.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2023, 5, 23, tzinfo=UTC)
            mock_dt.strptime = datetime.strptime

            w, _e = ReportService._collect_employee_status_lists()

            # 2023-05-23 minus 2023-04-23 = 30 giorni
            # 21 <= 30 <= 30 -> warning list
            assert len(w) == 1
            assert w[0]["cognome"] == "Rossi"

    @patch("src.core.report_service.win32_client")
    def test_dispatch_outlook_email(self, mock_win32):
        mock_outlook = MagicMock()
        mock_win32.Dispatch.return_value = mock_outlook
        mock_item = MagicMock()
        mock_outlook.CreateItem.return_value = mock_item

        w_list = [{"cognome": "R", "nome": "M", "giorni": 25, "data": "01/01"}]
        e_list = []

        ReportService._dispatch_outlook_email(w_list, e_list)

        assert mock_win32.Dispatch.called
        assert mock_item.Send.called
        assert "Report Accessi ISAB" in mock_item.HTMLBody

    @patch("src.core.report_service.ReportService._collect_employee_status_lists")
    @patch("src.core.report_service.ReportService._dispatch_outlook_email")
    @patch("src.core.report_service.ReportHistory.save_report")
    @patch("src.core.report_service.NotificationManager.instance")
    @patch("src.core.report_service.config_manager.set_config_value")
    @patch("src.core.report_service.os.name", "nt")
    def test_send_scheduled_report_email_success(
        self, mock_cfg, mock_notif, mock_save, mock_dispatch, mock_collect
    ):
        mock_collect.return_value = ([{"id": 1}], [])  # 1 warning

        ReportService.send_scheduled_report_email()

        assert mock_dispatch.called
        assert mock_save.called
        assert mock_notif.return_value.add_notification.called
