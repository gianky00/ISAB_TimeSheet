"""Unit tests for EmptyStateWidget."""

from src.gui.widgets.empty_state import EmptyStateWidget


class TestEmptyStateWidget:
    """Test suite per EmptyStateWidget."""

    def test_initialization(self, qtbot):
        widget = EmptyStateWidget(title="Custom Title", message="Custom Message")
        qtbot.addWidget(widget)

        assert widget.title_lbl.text() == "Custom Title"
        assert widget.msg_lbl.text() == "Custom Message"
        assert widget.icon_lbl.pixmap() is not None

    def test_default_values(self, qtbot):
        widget = EmptyStateWidget()
        qtbot.addWidget(widget)

        assert "Nessun dato" in widget.title_lbl.text()
        assert "filtri" in widget.msg_lbl.text()
