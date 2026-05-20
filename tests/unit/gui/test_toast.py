from PySide6.QtWidgets import QWidget

from src.gui.toast import ToastOverlay


class TestToastOverlay:
    def test_show_toast_basic(self, qtbot):
        parent = QWidget()
        qtbot.addWidget(parent)
        parent.show()

        toast = ToastOverlay(parent)
        qtbot.addWidget(toast)

        toast.show_toast("Test Message", duration=100)
        assert toast.label.text() == "Test Message"
        assert toast.isVisible()
        # Wait for animation to at least start (opacity > 0)
        qtbot.wait_until(lambda: toast.opacity_effect.opacity() > 0, timeout=1000)

    def test_hide_toast_flow(self, qtbot):
        parent = QWidget()
        toast = ToastOverlay(parent)
        qtbot.addWidget(toast)

        toast.show_toast("Hide Me", duration=10)
        # Wait for timer and animation
        qtbot.wait_until(lambda: toast.opacity_effect.opacity() < 0.1, timeout=2000)
        # Eventually it calls hide()
        qtbot.wait_until(lambda: not toast.isVisible(), timeout=1000)
