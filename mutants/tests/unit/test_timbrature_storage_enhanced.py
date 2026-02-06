"""
Enhanced unit tests for TimbratureStorage.
"""

import sqlite3
from unittest.mock import patch

import pandas as pd
import pytest

from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage


class TestTimbratureStorage:
    @pytest.fixture
    def storage(self, tmp_path):
        db_path = tmp_path / "test_timbrature.db"
        return TimbratureStorage(db_path)

    def test_init_creates_tables(self, storage):
        # Table 'timbrature' should exist. 'dipendenti' info is in config.json.
        with sqlite3.connect(storage.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cursor.fetchall()]
            assert "timbrature" in tables

    def test_get_employees_from_timbrature(self, storage):
        # Need to insert timbratures first to get unique employees
        with sqlite3.connect(storage.db_path) as conn:
            conn.execute(
                "INSERT INTO timbrature (nome, cognome) VALUES ('MARIO', 'ROSSI')"
            )
            conn.commit()

        with patch("src.core.config_manager.load_config", return_value={}):
            employees = storage.get_employees()
            assert len(employees) == 1
            assert employees[0]["nome"] == "MARIO"

    def test_update_employee_details(self, storage):
        with (
            patch("src.core.config_manager.load_config", return_value={}),
            patch("src.core.config_manager.set_config_value") as mock_set,
        ):
            storage.update_employee_details(
                "MARIO", "ROSSI", reparto="STRUMENTALE", cantiere="ISAB SUD"
            )

            # Verify set_config_value called with correct mapping
            args, _ = mock_set.call_args
            assert args[0] == "employee_mappings"
            assert "MARIO|ROSSI" in args[1]
            assert args[1]["MARIO|ROSSI"]["reparto"] == "STRUMENTALE"

    def test_get_lists(self, storage):
        mock_conf = {"reparti": ["R1"], "cantieri": ["C1"]}
        with patch("src.core.config_manager.load_config", return_value=mock_conf):
            lists = storage.get_lists()
            assert "R1" in lists["reparti"]
            assert "C1" in lists["cantieri"]

    def test_import_excel_mock(self, storage):
        # Mock pandas read_excel
        mock_df = pd.DataFrame(
            {
                "Data Timbratura": ["01/01/2023"],
                "Ora Ingresso": ["08:00"],
                "Ora Uscita": ["17:00"],
                "Cognome Risorsa": ["ROSSI"],
                "Nome Risorsa": ["MARIO"],
                "Presente Nei Timesheet": ["S"],
                "Sito Timbratura": ["SUD"],
            }
        )

        with patch("pandas.read_excel", return_value=mock_df):
            success = storage.import_excel("dummy.xlsx", lambda x: None)
            assert success is True

        # Verify in DB
        rows = storage.get_timbrature_with_reparto()
        assert len(rows) == 1
        assert rows[0][3] == "MARIO"
        assert rows[0][4] == "ROSSI"
