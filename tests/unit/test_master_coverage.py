from unittest.mock import patch

from src.gui.components.scarico_ore.filters.popup_date import DateFilterPopupWidget
from src.gui.components.scarico_ore.filters.popup_list import ListFilterPopupWidget


class TestMasterCoverage:
    def test_list_filter_popup_logic(self, qapp):
        values = ["Alfa", "Beta", "Gamma"]
        widget = ListFilterPopupWidget(values)

        # Test selection
        widget.select_all()
        assert len(widget.get_selected_values() or []) == 0  # None means all

        widget.select_none()
        assert len(widget.get_selected_values() or []) == 0

        # Filter list
        widget._filter_list("Al")
        assert not widget.list_view.isRowHidden(0)

    def test_date_filter_popup_logic(self, qapp):
        dates = ["01/01/2024", "05/02/2024", "10/01/2023"]
        widget = DateFilterPopupWidget(dates)

        # Check tree structure
        assert widget.model.rowCount() == 2  # 2024 and 2023

        selected = widget.get_selected_values()
        assert selected is None  # Initial state is all selected

    def test_audit_manager_integrity(self, tmp_path, mocker):
        from src.application.services.audit_manager import AuditManager

        # Isolamento totale del DB per evitare ID alti e collisioni
        db_path = tmp_path / "master_audit_test.db"
        mocker.patch("src.application.services.database.db_manager.DB_AUDIT", db_path)
        mocker.patch("src.application.services.audit.database.db_manager.DB_AUDIT", db_path)
        mocker.patch("src.application.services.audit.manager.AuditSignals.instance")

        AuditManager._instance = None  # Reset singleton
        am = AuditManager()

        # Patch hash per stabilità
        with patch("src.application.services.audit.integrity.AuditIntegrity.calculate_hash", return_value="FIXED_HASH"):
            am.log_action("Test", category="User1")
            am._log_queue.join()  # Attesa sincrona del worker

            assert am.verify_integrity() is True

    def test_contabilita_queries_years(self, tmp_path):
        from src.application.services.contabilita_queries import ContabilitaQueries

        # Just test the method doesn't crash with empty db
        db = tmp_path / "test_queries.db"
        years = ContabilitaQueries.get_available_years(db)
        assert isinstance(years, list)
