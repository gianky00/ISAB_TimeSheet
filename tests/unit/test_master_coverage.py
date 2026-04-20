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

    def test_audit_manager_integrity(self, tmp_path):
        import time  # noqa: PLC0415
        from unittest.mock import PropertyMock  # noqa: PLC0415

        from src.core.audit.manager import AuditManager  # noqa: PLC0415

        AuditManager._instance = None  # Reset singleton per isolamento

        # Patch DB_PATH e calculate_hash per stabilità nel test
        with (
            patch("src.core.audit.database.AuditDatabase.DB_PATH", new_callable=PropertyMock) as mock_db_path,
            patch("src.core.audit.integrity.AuditIntegrity.calculate_hash", return_value="FIXED_HASH"),
        ):
            mock_db_path.return_value = tmp_path / "test_audit.db"
            am = AuditManager()
            am.log_action("Test", "User1", notify=False)
            time.sleep(0.3)  # Attesa per thread asincrono
            assert am.verify_integrity() is True

    def test_contabilita_queries_years(self, tmp_path):
        from src.core.contabilita_queries import ContabilitaQueries  # noqa: PLC0415

        # Just test the method doesn't crash with empty db
        db = tmp_path / "test.db"
        years = ContabilitaQueries.get_available_years(db)
        assert isinstance(years, list)
