import sys

import pytest
from PySide6.QtWidgets import QApplication, QLabel, QWidget

from src.gui.components.animated_stack import SlidingStackedWidget


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication(sys.argv)
    return app


def test_initialization(qapp):
    stack = SlidingStackedWidget()
    assert stack.currentIndex() == -1
    assert stack.count() == 0


def test_add_widgets(qapp):
    stack = SlidingStackedWidget()
    w1 = QLabel("Widget 1")
    w2 = QLabel("Widget 2")
    stack.addWidget(w1)
    stack.addWidget(w2)

    assert stack.count() == 2
    assert stack.widget(0) == w1
    assert stack.widget(1) == w2


def test_slide_to_index(qapp, qtbot):
    stack = SlidingStackedWidget()
    w1 = QWidget()
    w2 = QWidget()
    stack.addWidget(w1)
    stack.addWidget(w2)

    qtbot.addWidget(stack)
    stack.resize(400, 300)
    stack.show()

    # Test valid slide
    stack.slide_to_index(1)
    assert stack._is_animating is True

    # Aspettiamo il completamento dell'animazione
    def check_finished():
        assert stack._is_animating is False
        assert stack.currentIndex() == 1

    qtbot.waitUntil(check_finished, timeout=1000)


def test_invalid_slide(qapp):
    stack = SlidingStackedWidget()
    w1 = QWidget()
    stack.addWidget(w1)

    # Test invalid index
    stack.slide_to_index(5)
    assert stack.currentIndex() == 0

    # Test same index
    stack.slide_to_index(0)
    assert stack.currentIndex() == 0
