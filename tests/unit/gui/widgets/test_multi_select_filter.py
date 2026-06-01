"""Unit tests for MultiSelectFilter."""

from unittest.mock import MagicMock

from PySide6.QtCore import Qt

from src.gui.widgets.multi_select_filter import MultiSelectDialog, MultiSelectFilter


class TestMultiSelectDialog:
    """Test suite per MultiSelectDialog."""

    def test_initialization(self, qtbot):
        items = ["A", "B", "C"]
        selected = ["A"]
        dlg = MultiSelectDialog("Select Items", items, selected)
        qtbot.addWidget(dlg)

        assert dlg.list_widget.count() == 3
        assert dlg.list_widget.item(0).checkState() == Qt.CheckState.Checked
        assert dlg.list_widget.item(1).checkState() == Qt.CheckState.Unchecked

    def test_filtering(self, qtbot):
        items = ["Apple", "Banana", "Cherry"]
        dlg = MultiSelectDialog("Filter", items, [])
        qtbot.addWidget(dlg)

        dlg.search_input.setText("App")
        assert not dlg.list_widget.item(0).isHidden()
        assert dlg.list_widget.item(1).isHidden()

    def test_set_all_none(self, qtbot):
        items = ["A", "B"]
        dlg = MultiSelectDialog("Test", items, [])
        qtbot.addWidget(dlg)

        # All
        qtbot.mouseClick(dlg.btn_all, Qt.MouseButton.LeftButton)
        assert dlg.get_selected() == ["A", "B"]

        # None
        qtbot.mouseClick(dlg.btn_none, Qt.MouseButton.LeftButton)
        assert dlg.get_selected() == []


class TestMultiSelectFilter:
    """Test suite per MultiSelectFilter."""

    def test_initialization(self, qtbot):
        f = MultiSelectFilter("Area", "Select Area")
        qtbot.addWidget(f)
        assert f.btn_select.text() == "Select Area"

    def test_set_items_updates_button(self, qtbot):
        f = MultiSelectFilter("Area")
        qtbot.addWidget(f)
        f.set_items(["A", "B"])
        f.set_selected(["A"])
        assert "Area: 1" in f.btn_select.text()

    def test_open_dialog_accept(self, qtbot, mocker):
        f = MultiSelectFilter("Items")
        qtbot.addWidget(f)
        f.set_items(["1", "2", "3"])

        # Mock Dialog
        mock_dlg_cls = mocker.patch("src.gui.widgets.multi_select_filter.MultiSelectDialog")
        mock_dlg = MagicMock()
        mock_dlg_cls.return_value = mock_dlg
        mock_dlg.exec.return_value = True
        mock_dlg.get_selected.return_value = ["1", "2"]

        with qtbot.waitSignal(f.changed):
            f._open_dialog()

        assert f.selected == ["1", "2"]
        assert "Items: 2" in f.btn_select.text()
