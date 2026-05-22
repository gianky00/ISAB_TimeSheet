import sqlite3
from unittest.mock import patch

import pytest

from src.core.contabilita_manager import ContabilitaManager
from src.core.database.manager import db_manager
from src.core.sync_tracker import SyncTracker


class TestContabilitaIntegration:
    @pytest.fixture(autouse=True)
    def setup_integration_env(self, tmp_path, monkeypatch):
        """Inizializza un ambiente di test con DB temporaneo."""
        # 1. Configurazione Path nel sistema
        self.db_path = tmp_path / "test_contabilita.db"

        # Monkeypatch globale dei path per tutti i moduli
        monkeypatch.setattr("src.core.database.db_manager.DB_CONTABILITA", self.db_path)
        # Consolidiamo tutto su test_contabilita.db come fa il service
        monkeypatch.setattr("src.core.database.db_manager.DB_GIORNALIERE", self.db_path)
        monkeypatch.setattr("src.core.paths.DB_DIR", tmp_path)
        monkeypatch.setattr("src.core.sync_tracker.DB_DIR", tmp_path)

        # Reset tracker
        SyncTracker._loaded = False
        SyncTracker.STATE_FILE = tmp_path / "sync_state.json"

        # Inizializza schema (migrazioni v1-v7)
        db_manager.init_db()
        yield

    @patch("src.core.importers.ExcelImporter.import_contabilita_dati")
    def test_full_import_sync_flow(self, mock_import):
        """Testa il flusso completo: Import Excel -> Sincronizzazione DB -> Status Tracker."""
        # 1. Mock dati in ingresso da Excel (year as first column)
        mock_data = [
            (
                2024,
                "2024-01-01",
                "Gennaio",
                "PREV1",
                1000.0,
                "Att1",
                "T1",
                "ODC1",
                "APERT",
                "TIPO1",
                10.0,
                "100%",
                "Note1",
                "Path1",
                "File1",
            ),
            (
                2024,
                "2024-02-01",
                "Febbraio",
                "PREV2",
                2000.0,
                "Att2",
                "T2",
                "ODC2",
                "CHIUS",
                "TIPO2",
                20.0,
                "90%",
                "Note2",
                "Path2",
                "File2",
            ),
        ]
        mock_import.return_value = (True, "OK", mock_data, [2024])

        # 2. Esecuzione tramite Manager
        success, msg, added, _removed = ContabilitaManager.import_data_from_excel("fake_file.xlsx")

        # 3. Verifiche
        assert success is True, f"Import failed: {msg}"
        assert added == 2

        # Verifica persistenza fisica nel DB mockato
        with sqlite3.connect(self.db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM contabilita WHERE year = 2024").fetchone()[0]
            assert count == 2

    @patch("src.core.importers.ExcelImporter.import_giornaliere")
    def test_giornaliere_import_sync_flow(self, mock_import_g):
        """Testa il flusso di importazione delle giornaliere."""
        # Setup dati base nel DB Contabilita per il lookup ODC
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO contabilita (year, n_prev, odc) VALUES (?, ?, ?)", (2024, "PREV1", "ODC1")
            )
            conn.commit()

        # Mock Giornaliere da importare (simulando i dati già arricchiti da ExcelImporter)
        mock_g_data = [
            (
                2024,
                "2024-01-10",
                "Mario Rossi",
                "Lavoro",
                "TCL1",
                "ODC1",  # Arricchito da ExcelImporter tramite lookup_map
                "PDL1",
                "08:00",
                "17:00",
                8.0,
                "PREV1",
                "g1.xlsx",
            )
        ]
        mock_import_g.return_value = (True, "OK", mock_g_data, [2024])

        # Esecuzione
        # Mock folder exists
        with patch("src.core.importers.giornaliere.Path.exists", return_value=True):
            success, msg, added, _removed = ContabilitaManager.import_giornaliere("fake_giornaliere")

        assert success is True, f"Import failed: {msg}"
        assert added == 1

        # Verifica arricchimento ODC nel DB (stesso file)
        with sqlite3.connect(self.db_path) as conn:
            r = conn.execute("SELECT odc FROM giornaliere WHERE n_prev = 'PREV1'").fetchone()
            assert r[0] == "ODC1"
