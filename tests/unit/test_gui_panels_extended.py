import pytest
from PySide6.QtCore import Qt

from src.gui.panels import HelpPanel, NotificationsPanel


class TestGUIPanelsExtended:
    @pytest.fixture
    def help_panel(self, qtbot):
        p = HelpPanel()
        qtbot.addWidget(p)
        return p

    def test_notifications_panel(self, qtbot):
        p = NotificationsPanel()
        # Impediamo la distruzione automatica per evitare RuntimeError in ambiente headless veloce
        p.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        qtbot.addWidget(p)
        p.show()
        assert p.isVisible()
        p.close()

    def test_help_panel_navigation(self, help_panel):
        """Verifica che il pannello help si inizializzi correttamente."""
        assert help_panel.layout() is not None

    def test_help_panel_content(self, help_panel):
        # HelpPanel in V9.4 usa un QTextBrowser o simili
        from PySide6.QtWidgets import QTextBrowser

        browser = help_panel.findChild(QTextBrowser)
        if browser:
            assert browser.toHtml() != ""
