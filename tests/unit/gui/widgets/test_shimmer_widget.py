import pytest
from PySide6.QtCore import QAbstractAnimation
from PySide6.QtWidgets import QApplication

from src.gui.widgets.shimmer_widget import ShimmerItem, ShimmerSkeleton


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_shimmer_item_initialization(qapp):
    item = ShimmerItem(height=30, width=100)
    assert item.height() == 30
    assert item.width() == 100
    assert item.anim.state() == QAbstractAnimation.State.Running
    assert item.anim.loopCount() == -1


def test_shimmer_item_no_width(qapp):
    item = ShimmerItem(height=20)
    assert item.height() == 20
    # Width should be default layout width or something else, but not explicitly set fixed width
    assert item.anim.state() == QAbstractAnimation.State.Running


def test_shimmer_skeleton_initialization(qapp):
    skeleton = ShimmerSkeleton(rows=2)
    # 2 rows * (2 items + 1 spacing) + 1 stretch = 7 items in layout
    assert skeleton.layout().count() == 7

    # We can test with 0 rows
    skeleton_empty = ShimmerSkeleton(rows=0)
    assert skeleton_empty.layout().count() == 1  # 1 stretch
