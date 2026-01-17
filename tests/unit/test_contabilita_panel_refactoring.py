"""
Baseline tests for ContabilitaPanel selection totals.
"""

import pytest
from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)

from src.gui.contabilita_panel import ContabilitaPanel


@pytest.fixture
def panel(qtbot, mock_ui_dependencies, mocker):
    mocker.patch("src.gui.contabilita_panel.ContabilitaPanel.refresh_tabs")
    mocker.patch(
        "src.gui.widgets.contabilita.attivita_tab.AttivitaProgrammateTab",
        return_value=QWidget(),
    )
    mocker.patch(
        "src.gui.widgets.contabilita.certificati_tab.CertificatiCampioneTab",
        return_value=QWidget(),
    )
    mocker.patch(
        "src.gui.contabilita_kpi_panel.ContabilitaKPIPanel", return_value=QWidget()
    )
    mocker.patch("PyQt6.QtCore.QTimer.singleShot")
    p = ContabilitaPanel()
    qtbot.addWidget(p)
    return p


def test_update_selection_total_table(panel, qtbot):
    """Test calculation of totals in a QTableWidget."""
    table = QTableWidget(5, 3)
    table.setHorizontalHeaderLabels(["DATA", "ORE SP", "DESC"])

    # Fill data
    data = [
        ["01/01", "8,5", "A"],
        ["02/01", "7", "B"],
        ["TOTALI", "15,5", ""],  # Should be ignored
    ]
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            table.setItem(r, c, QTableWidgetItem(val))

    # Select first two rows
    table.item(0, 0).setSelected(True)
    table.item(1, 0).setSelected(True)

    panel._update_selection_total(table)

    assert "Righe: 2" in panel.selection_count_label.text()
    assert "15,5" in panel.selection_sum_label.text()


def test_update_selection_total_tree(panel, qtbot):
    """Test selection count in a QTreeWidget."""
    tree = QTreeWidget()
    item1 = QTreeWidgetItem(["A"])
    item2 = QTreeWidgetItem(["B"])
    tree.addTopLevelItem(item1)
    tree.addTopLevelItem(item2)

    item1.setSelected(True)

    panel._update_selection_total(tree)
    assert "Selezionati: 1" in panel.selection_count_label.text()
    assert panel.selection_sum_label.text() == ""
