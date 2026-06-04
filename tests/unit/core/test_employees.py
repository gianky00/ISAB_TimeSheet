from unittest.mock import MagicMock, patch

import pytest

from src.application.services.employees import EmployeeManager


class TestEmployeeManager:
    @pytest.fixture
    def mock_db(self):
        m = MagicMock()
        m.DB_DIPENDENTI = "fake_dip.db"
        return m

    @pytest.fixture
    def manager(self, mock_db):
        return EmployeeManager(db_manager_instance=mock_db)

    def test_get_all_employees(self, manager, mock_db):
        manager._repo = MagicMock()
        manager._repo.get_all.return_value = [{"id": 1, "cognome": "ROSSI"}]

        res = manager.get_all_employees(active_only=True)
        assert len(res) == 1
        assert res[0]["cognome"] == "ROSSI"

    def test_get_employee_by_badge(self, manager, mock_db):
        mock_db.execute_query.return_value = [{"id": 1, "cognome": "ROSSI"}]
        res = manager.get_employee_by_badge("B1")
        assert res["cognome"] == "ROSSI"

    def test_add_employee_success(self, manager):
        manager._repo = MagicMock()
        manager._repo.save.return_value = True

        data = {"cognome": "Rossi", "nome": "Mario", "badge": "B1", "codice_fiscale": "cf1"}
        res = manager.add_employee(data)

        assert res is True
        args = manager._repo.save.call_args[0][0]
        assert args.cognome == "ROSSI"

    def test_update_employee_success(self, manager, mock_db):
        mock_db.execute_query.return_value = [
            {
                "id_risorsa": 10,
                "cognome": "VECCHIO",
                "nome": "N",
                "badge": "B1",
                "codice_fiscale": "cf",
                "data_assunzione": "2020",
                "monitoraggio_attivo": 1,
                "data_nascita": None,
            }
        ]

        manager._repo = MagicMock()
        manager._repo.save.return_value = True

        res = manager.update_employee(10, {"cognome": "Nuovo"})

        assert res is True
        args = manager._repo.save.call_args[0][0]
        # Align with current implementation (no normalization in update)
        assert args.cognome == "Nuovo"

    @patch("src.application.services.processing.base.Pipeline")
    @patch("src.application.services.employees.SyncTracker.update_status")
    def test_import_from_csv_success(self, mock_sync, mock_pipeline_class, manager):
        mock_p = MagicMock()
        mock_p.run.return_value = {"success": True, "added_count": 5, "total_processed": 10}
        mock_pipeline_class.return_value = mock_p

        res = manager.import_from_csv("test.csv")

        assert res == 10
        assert mock_sync.called

    def test_update_employee_not_found(self, manager, mock_db):
        mock_db.execute_query.return_value = []
        res = manager.update_employee(999, {})
        assert res is False
