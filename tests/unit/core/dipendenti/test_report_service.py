from unittest.mock import patch

import pytest

from src.application.services.dipendenti.report_service import ReportService


class TestReportServiceDipendenti:
    @pytest.fixture
    def mock_db(self, mocker):
        return mocker.patch("src.application.services.dipendenti.report_service.db_manager")

    @pytest.fixture
    def mock_timbrature_maps(self, mocker):
        return mocker.patch("src.application.services.dipendenti.report_service.build_timbrature_maps")

    @pytest.fixture
    def mock_history(self, mocker):
        return mocker.patch("src.application.services.dipendenti.report_service.ReportHistory")

    def test_gather_report_data(self, mock_db, mock_timbrature_maps):
        # Setup data
        mock_db.execute_query.side_effect = [
            [(1, "ROSSI", "MARIO", "CF1", "B1", "2020-01-01")],  # Dipendenti
            [("ROSSI", "MARIO", "CF1", "2026-05-20")],  # Accessi
        ]

        # Mock timbrature maps logic
        last_by_cf = {"CF1": (5, "2026-05-24")}  # 5 days ago
        last_by_name = {}

        def normalize(x):
            return x.strip().upper()

        mock_timbrature_maps.return_value = (last_by_cf, last_by_name, normalize)

        data = ReportService.gather_report_data()

        assert data["total_monitored"] == 1
        # 5 days is below warning threshold (20)
        assert len(data["warning_list"]) == 0
        assert len(data["expired_list"]) == 0

    def test_gather_report_data_thresholds(self, mock_db, mock_timbrature_maps):
        # Setup data: one warning, one expired
        mock_db.execute_query.side_effect = [
            [
                (1, "ROSSI", "MARIO", "CF1", "B1", "2020-01-01"),
                (2, "VERDI", "LUIGI", "CF2", "B2", "2020-01-01"),
            ],
            [],  # Not used as we mock maps
        ]

        last_by_cf = {
            "CF1": (25, "2026-05-04"),  # Warning (20-30)
            "CF2": (40, "2026-04-19"),  # Expired (>30)
        }
        mock_timbrature_maps.return_value = (last_by_cf, {}, lambda x: x)

        data = ReportService.gather_report_data()

        assert len(data["warning_list"]) == 1
        assert data["warning_list"][0]["cognome"] == "ROSSI"
        assert len(data["expired_list"]) == 1
        assert data["expired_list"][0]["cognome"] == "VERDI"

    def test_build_report_html(self, mock_history):
        data = {
            "warning_list": [
                {"cognome": "R", "nome": "M", "badge": "B1", "giorni": 25, "data": "04/05/2026"}
            ],
            "expired_list": [
                {"cognome": "V", "nome": "L", "badge": "B2", "giorni": 70, "data": "19/04/2026"}
            ],
            "total_monitored": 10,
        }

        # Mock trend
        mock_history.calculate_trend.return_value = {
            "warning_diff": 1,
            "expired_diff": -1,
            "last_date": "28/05/2026",
        }

        html = ReportService.build_report_html(data)
        assert "ROSSI" not in html  # Should be cognome from data
        assert "Report Monitoraggio Accessi" in html
        assert "IMMEDIATA" in html  # because giorni > 60
        assert "+1 in scadenza" in html
        assert "-1 scaduti" in html

    def test_build_report_html_no_trend(self, mock_history):
        data = {"warning_list": [], "expired_list": [], "total_monitored": 5}
        mock_history.calculate_trend.return_value = None
        html = ReportService.build_report_html(data)
        assert "Trend" not in html

    def test_create_report_excel(self, fs):
        # Mock TEMP env var
        import os

        fs.create_dir("C:/temp")
        with patch.dict(os.environ, {"TEMP": "C:/temp"}):
            w_list = [{"cognome": "R", "nome": "M", "badge": "B1", "giorni": 25, "data": "04/05/2026"}]
            e_list = []

            # Mock pandas
            with patch("src.application.services.dipendenti.report_service.pd.DataFrame") as mock_df:
                path = ReportService.create_report_excel(w_list, e_list)
                assert path is not None
                assert "report Accessi ISAB" in str(path)
                mock_df.return_value.to_excel.assert_called()

    def test_create_report_excel_empty(self):
        assert ReportService.create_report_excel([], []) is None
