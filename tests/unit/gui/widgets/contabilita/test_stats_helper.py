from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QTreeWidget, QWidget

from src.gui.widgets.contabilita.stats_helper import ContabilitaStatsHelper


def test_calculate_selection_stats_unsupported_widget(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    count, total = ContabilitaStatsHelper.calculate_selection_stats(widget)
    assert count == 0
    assert total == "0"


def test_calculate_selection_stats_treewidget(qtbot):
    tree = QTreeWidget()
    qtbot.addWidget(tree)
    # Creare mock finti non è compatibile con isinstance se non lo si fa bene,
    # ma qui usiamo tree reale
    from PySide6.QtWidgets import QTreeWidgetItem

    item1 = QTreeWidgetItem(["A"])
    item2 = QTreeWidgetItem(["B"])
    tree.addTopLevelItem(item1)
    tree.addTopLevelItem(item2)
    item1.setSelected(True)
    item2.setSelected(True)

    count, total = ContabilitaStatsHelper.calculate_selection_stats(tree)
    assert count == 2
    assert total == ""


def test_calculate_selection_stats_tablewidget_no_selection(qtbot):
    table = QTableWidget(2, 2)
    qtbot.addWidget(table)
    count, total = ContabilitaStatsHelper.calculate_selection_stats(table)
    assert count == 0
    assert total == "0"


def test_calculate_selection_stats_tablewidget_with_selection(qtbot):
    table = QTableWidget(3, 2)
    qtbot.addWidget(table)
    table.setHorizontalHeaderLabels(["DESC", "ORE"])

    table.setItem(0, 0, QTableWidgetItem("A"))
    table.setItem(0, 1, QTableWidgetItem("1,5"))

    table.setItem(1, 0, QTableWidgetItem("B"))
    table.setItem(1, 1, QTableWidgetItem("2,5"))

    # Riga totali (da escludere)
    table.setItem(2, 0, QTableWidgetItem("TOTALI"))
    table.setItem(2, 1, QTableWidgetItem("4,0"))

    # Seleziona tutte le celle
    table.selectAll()

    count, total = ContabilitaStatsHelper.calculate_selection_stats(table)
    assert count == 2  # Riga totali esclusa
    assert total == "4"  # 1.5 + 2.5 = 4.0 -> "4"


def test_calculate_selection_stats_tablewidget_hidden_rows(qtbot):
    table = QTableWidget(2, 2)
    qtbot.addWidget(table)
    table.setHorizontalHeaderLabels(["DESC", "ORE SP."])

    table.setItem(0, 0, QTableWidgetItem("A"))
    table.setItem(0, 1, QTableWidgetItem("1,5"))

    table.setItem(1, 0, QTableWidgetItem("B"))
    table.setItem(1, 1, QTableWidgetItem("1,25"))

    table.setRowHidden(1, True)
    table.selectAll()

    count, total = ContabilitaStatsHelper.calculate_selection_stats(table)
    assert count == 1  # Riga nascosta esclusa
    assert total == "1,50"


def test_format_hours():
    assert ContabilitaStatsHelper._format_hours(1.0) == "1"
    assert ContabilitaStatsHelper._format_hours(1.5) == "1,50"
    assert ContabilitaStatsHelper._format_hours(1234.56) == "1.234,56"


def test_find_ore_column_not_found(qtbot):
    table = QTableWidget(1, 2)
    qtbot.addWidget(table)
    table.setHorizontalHeaderLabels(["C1", "C2"])

    # Forziamo _update_table_selection con colonna non trovata
    table.setItem(0, 0, QTableWidgetItem("A"))
    table.setItem(0, 1, QTableWidgetItem("1"))
    table.selectAll()

    count, total = ContabilitaStatsHelper.calculate_selection_stats(table)
    assert count == 1
    assert total == "0"
