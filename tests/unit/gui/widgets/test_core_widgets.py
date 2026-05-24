"""Unit tests for Core Widgets."""

from src.gui.widgets.core_widgets import (
    FilterComboBox,
    PrimaryButton,
    SearchInput,
    SortableTableWidgetItem,
    StandardCheckBox,
    StandardGroupBox,
    StandardInput,
    StandardProgressBar,
    StandardTable,
    StandardTextEdit,
)


def test_buttons(qtbot):
    pb = PrimaryButton("Test")
    qtbot.addWidget(pb)
    assert pb.text() == "Test"
    assert "background-color" in pb.styleSheet()


def test_inputs(qtbot):
    si = SearchInput("Placeholder")
    qtbot.addWidget(si)
    assert si.placeholderText() == "Placeholder"
    assert si.isClearButtonEnabled()

    sti = StandardInput("Initial")
    qtbot.addWidget(sti)
    assert sti.text() == "Initial"


def test_text_edit(qtbot):
    te = StandardTextEdit()
    qtbot.addWidget(te)
    te.setPlainText("Some text")
    assert te.toPlainText() == "Some text"


def test_combobox(qtbot):
    cb = FilterComboBox()
    qtbot.addWidget(cb)
    cb.addItems(["A", "B"])
    assert cb.count() == 2


def test_checkbox(qtbot):
    chk = StandardCheckBox("Check")
    qtbot.addWidget(chk)
    assert chk.text() == "Check"


def test_table(qtbot):
    table = StandardTable(2, 2)
    qtbot.addWidget(table)
    assert table.alternatingRowColors() is True
    assert table.selectionBehavior() == StandardTable.SelectionBehavior.SelectRows


def test_progressbar(qtbot):
    pb = StandardProgressBar()
    qtbot.addWidget(pb)
    pb.setValue(50)
    assert pb.value() == 50


def test_groupbox(qtbot):
    gb = StandardGroupBox("Group")
    qtbot.addWidget(gb)
    assert gb.title() == "Group"


class TestSortableTableWidgetItem:
    """Test suite per SortableTableWidgetItem."""

    def test_sorting_numbers(self):
        item1 = SortableTableWidgetItem("10,50")
        item2 = SortableTableWidgetItem("5,20")
        # 10.5 > 5.2, quindi item2 < item1
        assert item2 < item1

        item3 = SortableTableWidgetItem("1.000,50")
        item4 = SortableTableWidgetItem("900,00")
        assert item4 < item3

    def test_sorting_dates(self):
        item1 = SortableTableWidgetItem("24/05/2026")
        item2 = SortableTableWidgetItem("20/05/2026")
        assert item2 < item1

        item3 = SortableTableWidgetItem("2026-05-24")
        assert not (item1 < item3)  # Identiche

    def test_sorting_strings(self):
        item1 = SortableTableWidgetItem("Banana")
        item2 = SortableTableWidgetItem("Apple")
        assert item2 < item1

    def test_sorting_empty(self):
        item_val = SortableTableWidgetItem("Value")
        item_empty = SortableTableWidgetItem("")
        # Vuoto viene prima (minore)
        assert item_empty < item_val
