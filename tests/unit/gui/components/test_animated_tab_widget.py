"""Unit tests for AnimatedTabWidget."""

from PySide6.QtWidgets import QWidget

from src.gui.components.animated_tab_widget import AnimatedTabWidget


class TestAnimatedTabWidget:
    """Test suite per AnimatedTabWidget."""

    def test_initialization(self, qtbot):
        widget = AnimatedTabWidget()
        qtbot.addWidget(widget)
        assert widget.count() == 0

    def test_add_remove_tab(self, qtbot):
        widget = AnimatedTabWidget()
        qtbot.addWidget(widget)

        t1 = QWidget()
        index = widget.addTab(t1, "Tab 1")
        assert index == 0
        assert widget.count() == 1
        assert widget.tabText(0) == "Tab 1"

        widget.removeTab(0)
        assert widget.count() == 0

    def test_navigation(self, qtbot):
        widget = AnimatedTabWidget()
        qtbot.addWidget(widget)

        widget.addTab(QWidget(), "T1")
        widget.addTab(QWidget(), "T2")

        with qtbot.waitSignal(widget.currentChanged):
            widget.setCurrentIndex(1)

        assert widget.currentIndex() == 1

    def test_clear(self, qtbot):
        widget = AnimatedTabWidget()
        qtbot.addWidget(widget)
        widget.addTab(QWidget(), "T1")
        widget.clear()
        assert widget.count() == 0

    def test_tab_position(self, qtbot):
        from PySide6.QtWidgets import QTabWidget

        widget = AnimatedTabWidget()
        qtbot.addWidget(widget)

        widget.setTabPosition(QTabWidget.TabPosition.South)
        assert widget._tab_position == QTabWidget.TabPosition.South
