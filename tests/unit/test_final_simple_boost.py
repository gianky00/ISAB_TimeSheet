
from src.core.contabilita_queries import ContabilitaQueries
from src.gui.widgets.sidebar_button import SidebarButton


class TestFinalSimpleBoost:
    def test_sidebar_button_badge(self, qapp):
        btn = SidebarButton("Test", icon="🏠")
        assert "🏠" in btn.text()

        btn.set_badge(5)
        assert "🔴 5" in btn.text()

        btn.set_badge(0)
        assert "🔴" not in btn.text()

    def test_contabilita_queries_exceptions(self, tmp_path):
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

    def test_modern_button_no_icon(self, qapp):
        from src.gui.widgets.modern_button import ModernButton
        btn = ModernButton("Text only")
        assert btn.text() == "Text only"
        # Check size logic
        btn._get_size_styles()
        btn._get_colors()
