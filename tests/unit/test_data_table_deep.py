import pytest

from src.gui.widgets.data_table import DataTable


@pytest.fixture
def columns():
    return [
        {"name": "ID", "key": "id", "width": 50},
        {"name": "Nome", "key": "nome", "width": 150},
        {"name": "Stato", "key": "stato", "editable": False}
    ]

@pytest.fixture
def sample_data():
    return [
        {"id": "1", "nome": "Test 1", "stato": "completato"},
        {"id": "2", "nome": "Test 2", "stato": "errore"},
        {"id": "3", "nome": "Alpha", "stato": "in_corso"},
        {"id": "4", "nome": "Beta", "stato": "pending"}
    ]

def test_data_table_init(qtbot, columns):
    table = DataTable(columns)
    qtbot.addWidget(table)

    assert table._table.columnCount() == 3
    assert table._table.horizontalHeaderItem(0).text() == "ID"
    # Column width might be affected by stretch mode if not explicitly set
    # but ID has width: 50
    assert table._table.columnWidth(0) == 50
    assert table._table.columnWidth(1) == 150

def test_data_table_set_data(qtbot, columns, sample_data):
    table = DataTable(columns)
    qtbot.addWidget(table)

    table.setData(sample_data)

    assert table._table.rowCount() == 4
    assert table._table.item(0, 0).text() == "1"
    assert table._table.item(0, 1).text() == "Test 1"

    # Check status color (completato -> green)
    color = table._table.item(0, 2).background().color().name().upper()
    assert color == table.STATUS_COLORS["completato"]

def test_data_table_filter(qtbot, columns, sample_data):
    table = DataTable(columns)
    qtbot.addWidget(table)
    table.setData(sample_data)

    # Filter for "Alpha"
    table._search_input.setText("Alpha")

    # Visual rows are filtered
    assert table._table.isRowHidden(0) is True
    assert table._table.isRowHidden(1) is True
    assert table._table.isRowHidden(2) is False
    assert table._table.isRowHidden(3) is True

    # Clear filter
    table._search_input.clear()
    assert table._table.isRowHidden(0) is False

def test_data_table_selection(qtbot, columns, sample_data):
    table = DataTable(columns)
    qtbot.addWidget(table)
    table.setData(sample_data)

    # Select first row
    table._table.selectRow(0)

    selected = table.getSelectedRows()
    assert len(selected) == 1
    assert selected[0]["id"] == "1"
    assert selected[0]["nome"] == "Test 1"

def test_data_table_double_click(qtbot, columns, sample_data):
    table = DataTable(columns)
    qtbot.addWidget(table)
    table.setData(sample_data)

    clicked_data = []
    def on_double_click(idx, data):
        clicked_data.append(data)

    table.rowDoubleClicked.connect(on_double_click)

    # Simulate double click on row 1 (index 1)
    index = table._table.model().index(1, 0)
    table._on_double_click(index)

    assert len(clicked_data) == 1
    assert clicked_data[0]["id"] == "2"

def test_data_table_get_row_color_prefix(qtbot, columns):
    table = DataTable(columns)
    # Testing prefix match logic
    assert table._get_row_color("completato_con_successo") == table.STATUS_COLORS["completato"]
    assert table._get_row_color("unknown") is None

def test_data_table_refresh(qtbot, columns):
    table = DataTable(columns)
    # Simply calls refresh which does nothing in base class, just for coverage
    table.refresh()

def test_data_table_get_widget(qtbot, columns):
    table = DataTable(columns)
    assert table.get_table_widget() == table._table
