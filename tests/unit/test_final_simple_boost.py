from src.core.contabilita_queries import ContabilitaQueries
from src.gui.widgets.sidebar_button import SidebarButton


class TestFinalSimpleBoost:
    def test_sidebar_button_badge(self, qapp):  # noqa: ANN001
        # SidebarButton expects an icon_path, not unicode char.
        # But we just test logic here, passing empty or dummy path.
        btn = SidebarButton("Test", icon_path="dummy.svg")

        # Check text format (spaces + text)
        assert "Test" in btn.text()

        # Check badge logic: append " (N)"
        btn.set_badge(5)
        # Implementation: f"   {self.label_text} ({count})"  # noqa: ERA001
        assert "(5)" in btn.text()

        btn.set_badge(0)
        assert "(0)" not in btn.text()
        assert "Test" in btn.text()

    def test_contabilita_queries_exceptions(self, tmp_path):  # noqa: ANN001
        # Create a file that is NOT a database to trigger exception
        db_path = tmp_path / "fake.db"
        db_path.write_text("not a db")

        # All these should return [] instead of crashing
        assert ContabilitaQueries.get_available_years(db_path) == []
        assert ContabilitaQueries.get_data_by_year(db_path, 2024) == []
        assert ContabilitaQueries.get_giornaliere_by_year(db_path, 2024) == []
        assert ContabilitaQueries.get_attivita_programmate_data(db_path) == []
        assert ContabilitaQueries.get_certificati_campione_data(db_path) == []
        assert ContabilitaQueries.get_scarico_ore_data(db_path) == []

    def test_modern_button_no_icon(self, qapp):  # noqa: ANN001
        from src.gui.widgets.modern_button import ModernButton  # noqa: PLC0415

        btn = ModernButton("Text only")
        assert btn.text() == "Text only"
        # Check size logic
        btn._get_size_styles()
        btn._get_colors()
