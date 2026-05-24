"""Unit tests for WaveProgressBar."""

from src.gui.widgets.wave_progress import WaveProgressBar


class TestWaveProgressBar:
    """Test suite per WaveProgressBar."""

    def test_initialization(self, qtbot):
        widget = WaveProgressBar()
        qtbot.addWidget(widget)

        assert widget.value() == 0
        assert widget.maximum() == 100
        assert widget.timer.isActive()

    def test_wave_update(self, qtbot):
        widget = WaveProgressBar()
        qtbot.addWidget(widget)

        initial_phase = widget._phase
        # Attendiamo il timer dell'animazione
        qtbot.wait(32)  # ~2 frames

        assert widget._phase > initial_phase

    def test_timer_stops_at_max(self, qtbot):
        widget = WaveProgressBar()
        qtbot.addWidget(widget)

        widget.setValue(100)
        widget._update_wave()

        assert not widget.timer.isActive()

    def test_paint_event_no_crash(self, qtbot):
        widget = WaveProgressBar()
        qtbot.addWidget(widget)
        widget.setValue(50)
        widget.update()
        # Test di rendering 2D senza crash
