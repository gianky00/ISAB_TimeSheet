import sqlite3

from src.core.audit_manager import AuditManager
from src.core.contabilita.stats_service import ContabilitaStats


class TestCoreLogicRefined:
    def test_audit_manager_singleton_and_init(self, tmp_path, mocker):
        db_path = tmp_path / "logic_audit.db"
        mocker.patch("src.core.database.db_manager.DB_AUDIT", db_path)
        mocker.patch("src.core.audit.database.db_manager.DB_AUDIT", db_path)
        mocker.patch("src.core.audit.manager.AuditSignals.instance")

        AuditManager._instance = None
        am = AuditManager()

        with sqlite3.connect(db_path) as conn:
            res = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='audit_logs'"
            ).fetchone()
            assert res is not None

    def test_contabilita_stats_calculation_real(self, tmp_path, mocker):
        db_path = tmp_path / "logic_stats.db"

        # Mocking ContabilitaQueries to avoid index mismatch on incomplete DB
        mock_data = [
            # data_prev, mese, n_prev, totale_prev, attivita, tcl, odc, stato, tipo, ore_sp, resa, annotazioni
            ("01/01", "GEN", "P1", "1.000,00", "Att1", "T1", "O1", "COMPLETATO", "T", "10,0", "R", "N")
        ]
        mocker.patch(
            "src.core.contabilita.stats_service.ContabilitaQueries.get_data_by_year", return_value=mock_data
        )
        mocker.patch(
            "src.core.contabilita.stats_service.ContabilitaQueries.get_giornaliere_by_year", return_value=[]
        )

        stats = ContabilitaStats.get_year_stats(db_path, 2024)

        assert stats["total_prev"] == 1000.0
        assert stats["total_ore"] == 10.0
        assert stats["status_counts"]["COMPLETATO"] == 1
