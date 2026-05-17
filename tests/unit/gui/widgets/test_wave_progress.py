import pytest
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QApplication

from src.gui.widgets.wave_progress import WaveProgressBar


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_wave_progress_initialization(qapp):
    bar = WaveProgressBar()
    assert bar.minimum() == 0
    assert bar.maximum() == 100
    assert bar.value() == 0
    assert not bar.isTextVisible()
    assert bar.timer.isActive()


def test_wave_progress_update_wave(qapp):
    bar = WaveProgressBar()
    initial_phase = bar._phase
    initial_phase2 = bar._phase2

    bar._update_wave()

    assert bar._phase > initial_phase
    assert bar._phase2 > initial_phase2


def test_wave_progress_update_wave_stop(qapp):
    bar = WaveProgressBar()
    bar.setValue(100)
    bar._update_wave()

    assert not bar.timer.isActive()


def test_wave_progress_paint_event_small(qapp):
    bar = WaveProgressBar()
    bar.setFixedHeight(10)  # Small enough to bypass text drawing
    event = QPaintEvent(bar.rect())
    bar.paintEvent(event)


def test_wave_progress_paint_event_large(qapp):
    bar = WaveProgressBar()
    bar.setFixedHeight(40)  # Large enough to draw text
    bar.setValue(50)
    event = QPaintEvent(bar.rect())
    bar.paintEvent(event)


def test_wave_progress_paint_event_high_value(qapp):
    bar = WaveProgressBar()
    bar.setFixedHeight(40)
    bar.setValue(90)  # Above WAVE_THRESHOLD_LIGHT
    event = QPaintEvent(bar.rect())
    bar.paintEvent(event)
