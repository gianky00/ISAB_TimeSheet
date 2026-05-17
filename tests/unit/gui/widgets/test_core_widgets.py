from src.gui.widgets.core_widgets import (
    FilterComboBox,
    IconButton,
    PrimaryButton,
    SearchInput,
    SortableTableWidgetItem,
    StandardCheckBox,
    StandardGroupBox,
    StandardInput,
    StandardListWidget,
    StandardProgressBar,
    StandardSpinBox,
    StandardTable,
    StandardTextEdit,
    StandardTreeWidget,
)


class TestCoreWidgets:
    def test_buttons(self, qtbot):
        p = PrimaryButton("P")
        qtbot.addWidget(p)
        assert p.text() == "P"

        i = IconButton()
        qtbot.addWidget(i)
        assert i.styleSheet() != ""

    def test_inputs(self, qtbot):
        s = SearchInput("Search")
        qtbot.addWidget(s)
        assert s.placeholderText() == "Search"
        assert s.isClearButtonEnabled()

        std = StandardInput("Value")
        qtbot.addWidget(std)
        assert std.text() == "Value"

        txt = StandardTextEdit()
        qtbot.addWidget(txt)
        txt.setText("Hello")
        assert txt.toPlainText() == "Hello"

    def test_selectors(self, qtbot):
        combo = FilterComboBox()
        qtbot.addWidget(combo)
        combo.addItems(["A", "B"])
        assert combo.count() == 2

        cb = StandardCheckBox("Check")
        qtbot.addWidget(cb)
        assert cb.text() == "Check"

        sb = StandardSpinBox()
        qtbot.addWidget(sb)
        sb.setValue(10)
        assert sb.value() == 10

    def test_containers(self, qtbot):
        table = StandardTable(2, 2)
        qtbot.addWidget(table)
        assert table.rowCount() == 2

        lst = StandardListWidget()
        qtbot.addWidget(lst)
        lst.addItem("Item")
        assert lst.count() == 1

        tree = StandardTreeWidget()
        qtbot.addWidget(tree)
        assert tree.columnCount() == 1

        group = StandardGroupBox("Group")
        qtbot.addWidget(group)
        assert group.title() == "Group"

        prog = StandardProgressBar()
        qtbot.addWidget(prog)
        prog.setValue(50)
        assert prog.value() == 50


class TestSortableTableWidgetItem:
    def test_sort_numbers(self):
        it1 = SortableTableWidgetItem("10,50")
        it2 = SortableTableWidgetItem("2.000,00")
        it3 = SortableTableWidgetItem("15")

        assert it1 < it2
        assert it1 < it3
        assert not (it2 < it1)

    def test_sort_dates(self):
        it1 = SortableTableWidgetItem("15/10/2023")
        it2 = SortableTableWidgetItem("20/10/2023")
        it3 = SortableTableWidgetItem("01/01/2024")

        assert it1 < it2
        assert it2 < it3
        assert not (it3 < it1)

    def test_sort_strings_fallback(self):
        it1 = SortableTableWidgetItem("Apple")
        it2 = SortableTableWidgetItem("Banana")
        assert it1 < it2

    def test_sort_empty(self):
        it1 = SortableTableWidgetItem("")
        it2 = SortableTableWidgetItem("Anything")
        assert it1 < it2
        assert not (it2 < it1)

        it3 = SortableTableWidgetItem(None)
        assert it3 < it2
