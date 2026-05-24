"""Unit tests for EditableDataTable."""

import pytest
from PySide6.QtCore import Qt

from src.gui.widgets.data_table import EditableDataTable


@pytest.fixture
def columns():
    """Definizione colonne di test."""
    return [
        {"name": "id", "label": "ID", "readonly": True, "default": "NEW"},
        {"name": "name", "label": "Nome", "readonly": False, "default": ""},
        {"name": "status", "label": "Stato", "readonly": True, "default": "Pendente"},
    ]


class TestEditableDataTable:
    """Test suite per EditableDataTable."""

    def test_initialization(self, qtbot, columns):
        """Verifica lbl'inizializzazione della tabella."""
        widget = EditableDataTable(columns)
        qtbot.addWidget(widget)

        assert widget.table.columnCount() == 3
        assert widget.table.horizontalHeaderItem(0).text() == "ID"
        assert widget.table.horizontalHeaderItem(1).text() == "Nome"

    def test_add_row(self, qtbot, columns):
        """Verifica lbl'aggiunta di righe."""
        widget = EditableDataTable(columns)
        qtbot.addWidget(widget)

        with qtbot.waitSignal(widget.data_changed):
            widget.add_row({"name": "Test User"})

        assert widget.table.rowCount() == 1
        assert widget.table.item(0, 0).text() == "NEW"
        assert widget.table.item(0, 1).text() == "Test User"
        assert widget.table.item(0, 2).text() == "Pendente"

        # Verifica readonly
        assert not (widget.table.item(0, 0).flags() & Qt.ItemFlag.ItemIsEditable)
        assert widget.table.item(0, 1).flags() & Qt.ItemFlag.ItemIsEditable

    def test_remove_row(self, qtbot, columns):
        """Verifica la rimozione di righe."""
        widget = EditableDataTable(columns)
        qtbot.addWidget(widget)
        widget.add_row()

        assert widget.table.rowCount() == 1

        with qtbot.waitSignal(widget.data_changed):
            widget.remove_row(0)

        assert widget.table.rowCount() == 0

    def test_get_set_data(self, qtbot, columns):
        """Verifica il recupero e lbl'impostazione massiva dei dati."""
        widget = EditableDataTable(columns)
        qtbot.addWidget(widget)

        test_data = [
            {"id": "1", "name": "User 1", "status": "OK"},
            {"id": "2", "name": "User 2", "status": "ERR"},
        ]

        widget.set_data(test_data)

        assert widget.table.rowCount() == 2

        exported_data = widget.get_data()
        assert len(exported_data) == 2
        assert exported_data[0]["name"] == "User 1"
        assert exported_data[1]["status"] == "ERR"

    def test_clear_status_columns(self, qtbot, columns):
        """Verifica la pulizia selettiva delle colonne readonly."""
        widget = EditableDataTable(columns)
        qtbot.addWidget(widget)
        widget.add_row({"id": "X", "name": "Keep Me", "status": "Delete Me"})

        widget.clear_status_columns()

        # 'id' e 'status' sono readonly, dovrebbero essere vuoti
        assert widget.table.item(0, 0).text() == ""
        assert widget.table.item(0, 2).text() == ""
        # 'name' NON è readonly, dovrebbe essere rimasto
        assert widget.table.item(0, 1).text() == "Keep Me"

    def test_item_changed_signal(self, qtbot, columns):
        """Verifica lbl'emissione del segnale alla modifica di una cella."""
        widget = EditableDataTable(columns)
        qtbot.addWidget(widget)
        widget.add_row({"name": "Initial"})

        with qtbot.waitSignal(widget.data_changed):
            widget.table.item(0, 1).setText("Modified")

    def test_hover_state(self, qtbot, columns):
        """Verifica lo stato di hover."""
        from PySide6.QtCore import QPointF
        from PySide6.QtGui import QEnterEvent

        widget = EditableDataTable(columns)
        qtbot.addWidget(widget)

        assert not widget._is_hovered

        # Simuliamo enter event
        enter_event = QEnterEvent(QPointF(0, 0), QPointF(0, 0), QPointF(0, 0))
        widget.enterEvent(enter_event)
        assert widget._is_hovered

        # Simuliamo leave event
        from PySide6.QtCore import QEvent

        leave_event = QEvent(QEvent.Type.Leave)
        widget.leaveEvent(leave_event)
        assert not widget._is_hovered
