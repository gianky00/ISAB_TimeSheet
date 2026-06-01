"""Baseline tests for ExcelTableWidget clipboard operations."""

import pytest
from PySide6.QtWidgets import QApplication, QComboBox, QTableWidgetItem

from src.gui.widgets.excel_table import ExcelTableWidget


@pytest.fixture
def table(qtbot):
    widget = ExcelTableWidget(10, 5)
    qtbot.addWidget(widget)
    # Fill some data
    for r in range(3):
        for c in range(3):
            widget.setItem(r, c, QTableWidgetItem(f"R{r}C{c}"))
    return widget


def test_copy_selection_logic(table, qtbot):
    """Test copying a range of cells to clipboard (including headers)."""
    clipboard = QApplication.clipboard()
    clipboard.clear()

    # Select range (0,0) to (1,1)
    table.setCurrentCell(0, 0)
    # Note: selectedIndexes() is used by Mixin
    table.item(0, 0).setSelected(True)
    table.item(0, 1).setSelected(True)
    table.item(1, 0).setSelected(True)
    table.item(1, 1).setSelected(True)

    table.copy_selection()

    text = clipboard.text()
    # Mixin includes headers by default: "Col 0\tCol 1\nR0C0\tR0C1\nR1C0\tR1C1"
    expected = "Col 0\tCol 1\nR0C0\tR0C1\nR1C0\tR1C1"
    assert text.strip() == expected


def test_paste_selection_logic(table, qtbot):
    """Test pasting TSV data from clipboard into table."""
    clipboard = QApplication.clipboard()
    data = "P1\tP2\nP3\tP4"
    clipboard.setText(data)

    # Paste starting at (2,2)
    table.setCurrentCell(2, 2)
    table.paste_selection()

    assert table.item(2, 2).text() == "P1"
    assert table.item(2, 3).text() == "P2"
    assert table.item(3, 2).text() == "P3"
    assert table.item(3, 3).text() == "P4"


def test_paste_into_combobox(table, qtbot):
    """Test that pasting into a cell with a ComboBox updates the index."""
    combo = QComboBox()
    combo.addItems(["", "Option1", "Option2"])
    table.setCellWidget(5, 0, combo)

    clipboard = QApplication.clipboard()
    clipboard.setText("Option2")

    table.setCurrentCell(5, 0)
    table.paste_selection()

    assert combo.currentText() == "Option2"
