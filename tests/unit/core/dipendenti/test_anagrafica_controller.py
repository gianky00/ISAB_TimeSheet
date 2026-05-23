from unittest.mock import patch

import pytest

from src.core.constants import REPORT_COLORS as COLORS, THRESHOLD_DAYS
from src.core.dipendenti.anagrafica_controller import AnagraficaController
from src.models.employee import EmployeeRecord


class TestAnagraficaController:
    @pytest.fixture
    def controller(self):
        with patch("src.core.dipendenti.anagrafica_controller.EmployeeRepository") as mock_repo:
            ctrl = AnagraficaController()
            ctrl.repository = mock_repo.return_value
            yield ctrl

    def test_get_employees_filtering(self, controller):
        mock_records = [
            EmployeeRecord(id_risorsa=1, cognome="Rossi", nome="Mario"),
            EmployeeRecord(id_risorsa=2, cognome="Verdi", nome="Luigi"),
        ]
        controller.repository.get_filtered.return_value = mock_records

        results = controller.get_employees("Rossi")

        assert len(results) == 2
        controller.repository.get_filtered.assert_called_with(search_text="Rossi", as_objects=True)

    @patch("src.core.dipendenti.anagrafica_controller.db_manager.execute_query")
    def test_process_rows_logic(self, mock_query, controller):
        mock_query.return_value = []

        records = [
            EmployeeRecord(
                id_risorsa=1,
                cognome="ROSSI",
                nome="MARIO",
                monitoraggio_attivo=1,
                badge="B1",
                codice_fiscale="RSSMRA",
            ),
            EmployeeRecord(id_risorsa=2, cognome="VERDI", nome="LUIGI", monitoraggio_attivo=0, badge="B2"),
        ]

        with patch("src.core.dipendenti.anagrafica_controller.compute_employee_status") as mock_status:
            # Rossi: 5 giorni (OK)
            mock_status.side_effect = [(5, False, "2023-05-18"), (None, False, None)]

            dtos, counts = controller.process_rows(records)

            assert counts["ok"] == 1
            assert counts["excluded"] == 1
            assert len(dtos) == 2

    @patch("src.core.dipendenti.anagrafica_controller.db_manager.execute_query")
    def test_get_last_isab_access_colors(self, mock_query, controller):
        from datetime import UTC, datetime, timedelta

        # Caso: OK (5 giorni fa)
        ok_date = (datetime.now(UTC) - timedelta(days=5)).strftime("%Y-%m-%d")
        mock_query.return_value = [[ok_date]]
        _, _, color_ok = controller.get_last_isab_access("Rossi", "Mario")
        assert color_ok == COLORS["success_dark"]

        # Caso: Warning (25 giorni fa, soglia warning=20)
        warn_date = (datetime.now(UTC) - timedelta(days=25)).strftime("%Y-%m-%d")
        mock_query.side_effect = [[[warn_date]]]
        _, _, color_warn = controller.get_last_isab_access("Rossi", "Mario")
        assert color_warn == COLORS["warning_orange"]

        # Caso: Scaduta (40 giorni fa, soglia expired=30)
        expired_date = (datetime.now(UTC) - timedelta(days=40)).strftime("%Y-%m-%d")
        mock_query.side_effect = [[[expired_date]]]
        _, _, color_err = controller.get_last_isab_access("Rossi", "Mario")
        assert color_err == COLORS["error_red"]

    def test_toggle_monitoring_success(self, controller):
        controller.repository.toggle_monitoring.return_value = True
        assert controller.toggle_monitoring("1", True) is True

    def test_should_skip_row_filters(self, controller):
        # Utilizziamo i valori reali delle soglie per il test
        w = THRESHOLD_DAYS["warning"]
        e = THRESHOLD_DAYS["expired"]

        # Filter "ok": skip if > warning
        assert controller._should_skip_row(is_monitored=True, diff_days=w - 1, current_filter="ok") is False
        assert controller._should_skip_row(is_monitored=True, diff_days=w + 1, current_filter="ok") is True

        # Filter "warning": skip if <= warning or > expired
        assert (
            controller._should_skip_row(is_monitored=True, diff_days=w + 1, current_filter="warning") is False
        )
        assert (
            controller._should_skip_row(is_monitored=True, diff_days=w - 1, current_filter="warning") is True
        )
