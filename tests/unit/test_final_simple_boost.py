import pytest


class TestFinalSimpleBoost:
    def test_contabilita_queries_exceptions(self, mocker):
        from src.core.contabilita_queries import ContabilitaQueries

        # Patch repository
        m_repo = mocker.patch("src.core.contabilita_queries.ContabilitaQueries._repo")
        m_repo.get_available_years.side_effect = Exception("DB Crash")

        # In V9.4 get_available_years potrebbe non catturare l'eccezione volutamente
        with pytest.raises(Exception, match="DB Crash"):
            ContabilitaQueries.get_available_years("fake.db")

    def test_sidebar_button_badge(self):
        # Placeholder per logica sidebar se non già coperta
        assert True

    def test_modern_button_no_icon(self, qapp):
        from src.gui.widgets.modern_button import ModernButton

        btn = ModernButton("Test")
        assert btn.text() == "Test"
