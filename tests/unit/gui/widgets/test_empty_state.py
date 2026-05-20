import pytest
from PySide6.QtWidgets import QApplication

from src.core.constants import Icons
from src.gui.widgets.empty_state import EmptyStateWidget


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_empty_state_widget_initialization(qapp):
    widget = EmptyStateWidget()
    assert widget.title_lbl.text() == "Nessun dato trovato"
    assert widget.msg_lbl.text() == "Prova a cambiare i filtri o ad aggiornare il database."
    assert "background: transparent" in widget.styleSheet()


def test_empty_state_widget_custom_text(qapp):
    widget = EmptyStateWidget(title="Custom Title", message="Custom Message", icon_key=Icons.ALERT)
    assert widget.title_lbl.text() == "Custom Title"
    assert widget.msg_lbl.text() == "Custom Message"
