"""Unit tests for ChildDescriptionDelegate."""

import pytest
from PySide6.QtCore import QPersistentModelIndex, QRect, Qt
from PySide6.QtGui import QImage, QPainter, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QStyleOptionViewItem, QTreeView

from src.gui.panels.storico_oda.oda_delegate import ChildDescriptionDelegate


@pytest.fixture
def real_tree(qtbot):
    tree = QTreeView()
    model = QStandardItemModel()
    tree.setModel(model)
    qtbot.addWidget(tree)
    return tree


@pytest.fixture
def delegate(real_tree):
    return ChildDescriptionDelegate(real_tree)


class TestChildDescriptionDelegate:
    """Test suite per ChildDescriptionDelegate."""

    def test_paint_parent_bg_error(self, delegate, real_tree):
        """Verifica la colorazione di sfondo per OdA cancellato."""
        model = real_tree.model()
        item = QStandardItem("ODA1")
        # Stato a indice 4
        raw_data = ["v", "v", "v", "v", "Cancellato"] + ["v"] * 30
        item.setData(raw_data, Qt.ItemDataRole.UserRole)
        model.appendRow(item)

        idx = model.index(0, 0)
        option = QStyleOptionViewItem()
        option.rect = QRect(0, 0, 100, 20)

        img = QImage(100, 20, QImage.Format.Format_ARGB32)
        painter = QPainter(img)
        try:
            delegate._paint_parent_bg(painter, option, idx)
        finally:
            painter.end()
        # Test di non-crash

    def test_paint_shimmer_trigger(self, delegate, real_tree):
        """Verifica che lo shimmer venga disegnato se lbl'animazione è attiva."""
        model = real_tree.model()
        item = QStandardItem("X")
        model.appendRow(item)
        idx = model.index(0, 0)

        real_tree._anim_index = QPersistentModelIndex(idx)
        real_tree._anim_progress = 0.5

        option = QStyleOptionViewItem()
        option.rect = QRect(0, 0, 100, 20)

        img = QImage(100, 20, QImage.Format.Format_ARGB32)
        painter = QPainter(img)
        try:
            delegate._paint_shimmer(painter, option, idx)
        finally:
            painter.end()
        # Test di non-crash

    def test_paint_child_row_merge(self, delegate, real_tree):
        """Verifica il merge delle colonne nelle righe figlie."""
        model = real_tree.model()
        parent = QStandardItem("Parent")
        child0 = QStandardItem("Long Description")
        child1 = QStandardItem("")
        parent.appendRow([child0, child1])
        model.appendRow(parent)

        idx_child1 = model.index(0, 1, model.index(0, 0))

        option = QStyleOptionViewItem()
        option.rect = QRect(100, 0, 100, 20)

        img = QImage(200, 20, QImage.Format.Format_ARGB32)
        painter = QPainter(img)
        try:
            res = delegate._paint_child_row(painter, option, idx_child1)
        finally:
            painter.end()

        assert res is True

    def test_paint_full_delegation(self, delegate, real_tree):
        """Verifica la chiamata al metodo paint completo."""
        model = real_tree.model()
        item = QStandardItem("P")
        item.setData(["v"] * 30, Qt.ItemDataRole.UserRole)
        model.appendRow(item)
        idx = model.index(0, 0)

        option = QStyleOptionViewItem()
        option.rect = QRect(0, 0, 100, 20)

        img = QImage(100, 20, QImage.Format.Format_ARGB32)
        painter = QPainter(img)
        try:
            delegate.paint(painter, option, idx)
        finally:
            painter.end()
