import sqlite3
from unittest.mock import patch

from src.core.audit_manager import AuditManager
from src.core.contabilita.stats_service import ContabilitaStats
from src.core.excel_importer import ExcelImporter


class TestCoreLogicRefined:
    def test_audit_manager_singleton_and_init(self, tmp_path):
        db_path = tmp_path / "audit.db"
        # Reset singleton
        AuditManager._instance = None
        # Patch the real DB_PATH in AuditDatabase
        with patch("src.core.audit.database.AuditDatabase.DB_PATH", db_path):
            am = AuditManager()
            # Verify DB was initialized
            with sqlite3.connect(db_path) as conn:
                res = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='audit_logs'"
                ).fetchone()
                assert res is not None

            am.log_action("Test Action")
            # Attendi il worker asincrono (necessario in V2)
            am._log_queue.join()
            assert len(am.get_logs()) == 1

    def test_contabilita_stats_calculation_real(self, tmp_path):
        db_path = tmp_path / "stats.db"
        with sqlite3.connect(db_path) as conn:
            # Create table with all required columns
            cols = ["id INTEGER PRIMARY KEY", "year INTEGER"]
            cols += [f"{v} TEXT" for v in ExcelImporter.COLUMNS_MAPPING.values()]
            conn.execute(f"CREATE TABLE contabilita ({', '.join(cols)})")

            g_cols = [
                "id INTEGER PRIMARY KEY",
                "year INTEGER",
                "data TEXT",
                "personale TEXT",
                "tcl TEXT",
                "descrizione TEXT",
                "n_prev TEXT",
                "odc TEXT",
                "pdl TEXT",
                "inizio TEXT",
                "fine TEXT",
                "ore TEXT",
                "nome_file TEXT",
            ]
            conn.execute(f"CREATE TABLE giornaliere ({', '.join(g_cols)})")

            # Insert data
            # index 2:n_prev, 3:totale_prev, 4:attivita, 7:stato_attivita, 9:ore_sp (val_ore)
            conn.execute(
                "INSERT INTO contabilita (year, n_prev, totale_prev, attivita, stato_attivita, ore_sp) VALUES (2024, 'PREV1', '1.000,00', 'Att1', 'COMPLETATO', '10,0')"
            )
            # index 4:n_prev (in giornaliere cols list), index 9:ore
            conn.execute("INSERT INTO giornaliere (year, n_prev, odc, ore) VALUES (2024, 'PREV1', '', '5,0')")

        stats = ContabilitaStats.get_year_stats(db_path, 2024)
        assert stats["total_prev"] == 1000.0
        assert stats["ore_dirette"] == 5.0
        assert stats["status_counts"]["COMPLETATO"] == 1
