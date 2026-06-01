from unittest.mock import MagicMock

import pytest

from src.gui.widgets.contabilita.helpers import SortableTreeWidgetItem


def test_numeric_comparison():
    item1 = SortableTreeWidgetItem(["100,50"])
    item2 = SortableTreeWidgetItem(["100,60"])

    # Simula treeWidget() e sortColumn()
    mock_tree = MagicMock()
    mock_tree.sortColumn.return_value = 0
    item1.treeWidget = MagicMock(return_value=mock_tree)
    item2.treeWidget = MagicMock(return_value=mock_tree)

    assert item1 < item2
    assert not (item2 < item1)


def test_date_comparison():
    item1 = SortableTreeWidgetItem(["01/01/2024"])
    item2 = SortableTreeWidgetItem(["02/01/2024"])

    mock_tree = MagicMock()
    mock_tree.sortColumn.return_value = 0
    item1.treeWidget = MagicMock(return_value=mock_tree)
    item2.treeWidget = MagicMock(return_value=mock_tree)

    assert item1 < item2
    assert not (item2 < item1)


def test_percentage_comparison():
    item1 = SortableTreeWidgetItem(["10%"])
    item2 = SortableTreeWidgetItem(["20%"])

    mock_tree = MagicMock()
    mock_tree.sortColumn.return_value = 0
    item1.treeWidget = MagicMock(return_value=mock_tree)
    item2.treeWidget = MagicMock(return_value=mock_tree)

    assert item1 < item2
    assert not (item2 < item1)


def test_string_comparison_fallback():
    item1 = SortableTreeWidgetItem(["Apple"])
    item2 = SortableTreeWidgetItem(["Banana"])

    mock_tree = MagicMock()
    mock_tree.sortColumn.return_value = 0
    item1.treeWidget = MagicMock(return_value=mock_tree)
    item2.treeWidget = MagicMock(return_value=mock_tree)

    assert item1 < item2
    assert not (item2 < item1)


def test_no_tree_widget_fallback():
    item1 = SortableTreeWidgetItem(["1"])
    item2 = SortableTreeWidgetItem(["2"])

    # Non patchiamo treeWidget, di default è None se non aggiunto a un QTreeWidget
    try:
        res = item1 < item2
    except Exception as e:
        pytest.fail(f"__lt__ crashed without tree widget: {e}")
