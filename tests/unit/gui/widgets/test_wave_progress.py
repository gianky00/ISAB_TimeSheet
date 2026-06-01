from src.gui.widgets.wave_progress import WaveProgressBar


def test_wave_progress_init(qtbot):
    bar = WaveProgressBar()
    qtbot.addWidget(bar)

    assert bar.minimum() == 0
    assert bar.maximum() == 100
    assert bar.value() == 0
    assert bar.timer.isActive()


def test_wave_progress_animation(qtbot):
    bar = WaveProgressBar()
    qtbot.addWidget(bar)

    initial_phase = bar._phase
    # Wait for a few frames
    qtbot.wait(50)

    assert bar._phase > initial_phase
    assert bar.timer.isActive()


def test_wave_progress_completion(qtbot):
    bar = WaveProgressBar()
    qtbot.addWidget(bar)

    bar.setValue(100)
    # The timer should stop when reaching maximum
    # (Checking the logic in _update_wave)
    bar._update_wave()

    assert not bar.timer.isActive()


def test_wave_progress_paint(qtbot):
    bar = WaveProgressBar()
    qtbot.addWidget(bar)
    bar.resize(200, 34)

    # Force a paint event to ensure no crashes in the math/painter logic
    bar.update()
    qtbot.wait(20)
