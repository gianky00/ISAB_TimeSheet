from unittest.mock import MagicMock, patch

from PySide6.QtCore import QAbstractAnimation, QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect, QVBoxLayout, QWidget

from src.utils.animation_helpers import (
    cleanup_animation_safely,
    cleanup_effect_safely,
    clear_layout_safely,
    create_animation_timer,
    create_fade_animation,
    create_opacity_effect,
    create_position_animation,
    create_pulse_animation,
    delayed_call,
    staggered_fade_in,
)


class TestAnimationHelpers:
    def test_create_opacity_effect(self, qtbot):
        w = QWidget()
        effect = create_opacity_effect(w)
        assert isinstance(effect, QGraphicsOpacityEffect)
        assert w.graphicsEffect() is effect

    def test_create_fade_animation(self, qtbot):
        w = QWidget()
        effect = create_opacity_effect(w)
        anim = create_fade_animation(effect, start=0.0, end=1.0, duration=100)

        assert isinstance(anim, QPropertyAnimation)
        assert anim.duration() == 100
        assert anim.startValue() == 0.0
        assert anim.endValue() == 1.0

    def test_create_pulse_animation(self, qtbot):
        w = QWidget()
        effect = create_opacity_effect(w)
        anim = create_pulse_animation(effect, min_opacity=0.2, max_opacity=0.8, loop=True)

        assert anim.loopCount() == -1
        assert anim.startValue() == 0.2
        assert anim.endValue() == 0.8

    def test_create_position_animation(self, qtbot):
        w = QWidget()
        anim = create_position_animation(w, (0, 0), (100, 100))
        assert anim.startValue().x() == 0
        assert anim.endValue().y() == 100

    def test_cleanup_animation_safely(self, qtbot):
        cleanup_animation_safely(None)

        w = QWidget()
        anim = QPropertyAnimation(w, b"pos")
        anim.start()

        with patch.object(anim, "deleteLater") as mock_del:
            cleanup_animation_safely(anim)
            assert anim.state() == QAbstractAnimation.State.Stopped
            assert mock_del.called

    def test_cleanup_effect_safely(self, qtbot):
        w = QWidget()
        effect = QGraphicsOpacityEffect()
        w.setGraphicsEffect(effect)

        with patch.object(effect, "deleteLater") as mock_del:
            cleanup_effect_safely(w, effect)
            assert w.graphicsEffect() is None
            assert mock_del.called

    def test_clear_layout_safely(self, qtbot):
        w = QWidget()
        layout = QVBoxLayout(w)
        child1 = QWidget()
        child1.cleanup = MagicMock()
        layout.addWidget(child1)

        clear_layout_safely(layout, process_events=False)
        assert layout.count() == 0
        assert child1.cleanup.called

    def test_create_animation_timer(self, qtbot):
        w = QWidget()
        callback = MagicMock()
        # Test con interval
        timer = create_animation_timer(w, callback, interval=75, single_shot=False)
        assert timer.interval() == 75
        assert timer.isSingleShot() is False

        # Test single shot
        timer2 = create_animation_timer(w, callback, single_shot=True)
        assert timer2.isSingleShot() is True

    @patch("PySide6.QtCore.QTimer.singleShot")
    def test_delayed_call(self, mock_shot):
        def cb():
            return None

        delayed_call(cb, delay=200)
        mock_shot.assert_called_with(200, cb)

    def test_staggered_fade_in(self, qtbot):
        widgets = [QWidget(), QWidget()]
        anims = staggered_fade_in(widgets, delay_between=10)
        assert len(anims) == 2
        assert widgets[0].graphicsEffect() is not None
