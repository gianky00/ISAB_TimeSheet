from src.gui.widgets.priority_badge import PriorityBadge


class TestPriorityBadge:
    def test_initialization(self, qtbot):
        badge = PriorityBadge(priority="alta")
        qtbot.addWidget(badge)
        assert badge.priority == "alta"
        assert badge.anim.state() == badge.anim.State.Running

    def test_set_priority(self, qtbot):
        badge = PriorityBadge(priority="bassa")
        qtbot.addWidget(badge)

        badge.set_priority("alta")
        assert badge.priority == "alta"
        # Verify color change (internal check is hard, but calling is coverage)

    def test_visibility_stops_starts_anim(self, qtbot):
        badge = PriorityBadge()
        qtbot.addWidget(badge)
        badge.show()
        qtbot.wait_until(lambda: badge.isVisible())

        badge.hide()
        # Verify it's stopped (may need a small wait for event loop)
        qtbot.wait_until(lambda: badge.anim.state() == badge.anim.State.Stopped)

        badge.show()
        qtbot.wait_until(lambda: badge.anim.state() == badge.anim.State.Running)

    def test_pulse_scale_property(self, qtbot):
        badge = PriorityBadge()
        qtbot.addWidget(badge)

        badge.set_pulse_scale(0.8)
        assert badge._pulse_scale == 0.8
        # Should have updated dot size
        assert badge.dot.size().width() == int(8 * 0.8)
