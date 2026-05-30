from datetime import UTC, datetime

import pytest

from src.core.dipendenti.anagrafica_controller import AnagraficaController
from src.models.employee import EmployeeRecord


class TestAnagraficaController:
    @pytest.fixture
    def controller(self):
        return AnagraficaController()

    def test_get_employees(self, controller, mocker):
        mock_records = [
            EmployeeRecord(
                id_risorsa=1,
                cognome="A",
                nome="B",
                data_nascita="",
                badge="1",
                data_assunzione="",
                codice_fiscale="CF1",
                monitoraggio_attivo=1,
            )
        ]
        mocker.patch.object(controller.repository, "get_filtered", return_value=mock_records)

        res = controller.get_employees("test")
        assert len(res) == 1
        assert res[0].cognome == "A"

    def test_process_rows(self, controller, mocker):
        # Setup mocks
        records = [
            EmployeeRecord(
                id_risorsa=1,
                cognome="ROSSI",
                nome="MARIO",
                data_nascita="",
                badge="B1",
                data_assunzione="",
                codice_fiscale="CF1",
                monitoraggio_attivo=1,
            )
        ]

        last_by_cf = {"CF1": (5, "25/05/2026")}
        last_by_name = {}
        mocker.patch.object(
            controller, "_get_timbrature_maps", return_value=(last_by_cf, last_by_name, lambda x: x)
        )

        dtos, counts = controller.process_rows(records)

        assert len(dtos) == 1
        assert dtos[0].cognome == "ROSSI"
        assert counts["ok"] == 1
        assert counts["warning"] == 0

    def test_process_rows_filtering(self, controller, mocker):
        records = [
            EmployeeRecord(
                id_risorsa=1,
                cognome="A",
                nome="B",
                data_nascita="",
                badge="1",
                data_assunzione="",
                codice_fiscale="CF1",
                monitoraggio_attivo=1,
            ),
            EmployeeRecord(
                id_risorsa=2,
                cognome="C",
                nome="D",
                data_nascita="",
                badge="2",
                data_assunzione="",
                codice_fiscale="CF2",
                monitoraggio_attivo=1,
            ),
        ]
        # CF1: 5 days (OK), CF2: 40 days (EXPIRED)
        last_by_cf = {"CF1": (5, "X"), "CF2": (40, "Y")}
        mocker.patch.object(controller, "_get_timbrature_maps", return_value=(last_by_cf, {}, lambda x: x))

        # Filter for expired
        dtos, _ = controller.process_rows(records, current_filter="expired")
        assert len(dtos) == 1
        assert dtos[0].id_risorsa == "2"

    def test_get_last_isab_access_success(self, controller, mocker):
        mocker.patch("src.core.database.db_manager.execute_query", return_value=[("2026-05-20 10:00:00",)])

        # Fixed "now" for test
        mock_now = datetime(2026, 5, 25, 12, 0, tzinfo=UTC)
        mocker.patch("src.core.dipendenti.anagrafica_controller.datetime", mocker.Mock(wraps=datetime))
        import src.core.dipendenti.anagrafica_controller as ac

        ac.datetime.now.return_value = mock_now
        ac.datetime.strptime = datetime.strptime

        text, delta, color = controller.get_last_isab_access("Rossi", "Mario")

        assert "20/05/2026" in text
        assert delta == 5
        assert color == "#198754"  # success_dark

    def test_get_last_isab_access_never(self, controller, mocker):
        mocker.patch("src.core.database.db_manager.execute_query", return_value=[])
        text, delta, _ = controller.get_last_isab_access("X", "Y")
        assert "Mai effettuato" in text
        assert delta == -1

    def test_toggle_monitoring(self, controller, mocker):
        mock_toggle = mocker.patch.object(controller.repository, "toggle_monitoring", return_value=True)
        assert controller.toggle_monitoring("1", True) is True
        mock_toggle.assert_called_once_with("1", True)

    def test_should_skip_row_logic(self, controller):
        # excluded filter
        assert controller._should_skip_row(is_monitored=True, diff_days=5, current_filter="excluded") is True
        assert (
            controller._should_skip_row(is_monitored=False, diff_days=None, current_filter="excluded")
            is False
        )

        # status filters
        # OK filter: skip if > 20 days
        assert controller._should_skip_row(True, 25, "ok") is True
        assert controller._should_skip_row(True, 5, "ok") is False

        # Warning filter: skip if <= 20 or > 30
        assert controller._should_skip_row(True, 5, "warning") is True
        assert controller._should_skip_row(True, 25, "warning") is False
        assert controller._should_skip_row(True, 40, "warning") is True
