from src.core.constants import Icons
from src.gui.widgets.empty_state import EmptyStateWidget
from src.gui.widgets.shimmer_widget import ShimmerItem, ShimmerSkeleton


class TestVisualFeedbackWidgets:
    def test_shimmer_skeleton(self, qtbot):
        shimmer = ShimmerSkeleton(rows=2)
        qtbot.addWidget(shimmer)

        # Verify it has enough items (2 rows * 2 items each = 4 items)
        # Plus spacing and stretch?
        items = shimmer.findChildren(ShimmerItem)
        assert len(items) == 4

        # Verify animation is running on one item
        assert items[0].anim.state() == items[0].anim.State.Running

    def test_empty_state_widget(self, qtbot):
        empty = EmptyStateWidget(title="Zero", message="Empty", icon_key=Icons.DATABASE)
        qtbot.addWidget(empty)

        assert empty.title_lbl.text() == "Zero"
        assert empty.msg_lbl.text() == "Empty"
        assert empty.icon_lbl.pixmap() is not None
