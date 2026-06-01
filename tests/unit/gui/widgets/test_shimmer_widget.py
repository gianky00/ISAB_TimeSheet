"""Unit tests for Shimmer Widgets."""

from PySide6.QtCore import QPropertyAnimation

from src.gui.widgets.shimmer_widget import ShimmerItem, ShimmerSkeleton


class TestShimmerWidgets:
    """Test suite per Shimmer Widgets."""

    def test_shimmer_item(self, qtbot):
        item = ShimmerItem(height=30, width=150)
        qtbot.addWidget(item)

        assert item.height() == 30
        assert item.width() == 150
        assert item.anim.state() == QPropertyAnimation.State.Running
        assert item.anim.startValue() == 0.3
        assert item.anim.endValue() == 0.7

    def test_shimmer_skeleton(self, qtbot):
        skeleton = ShimmerSkeleton(rows=5)
        qtbot.addWidget(skeleton)

        # Ogni riga ha 2 ShimmerItem + spacing
        items = skeleton.findChildren(ShimmerItem)
        assert len(items) == 10
