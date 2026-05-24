"""Unit tests for Toast Notifications."""

from PySide6.QtCore import Qt

from src.gui.widgets.toast import Toast, ToastManager, ToastParams, toast_info, toast_success


class TestToast:
    """Test suite per il widget Toast."""

    def test_initialization(self, qtbot):
        params = ToastParams(message="Hello Toast", toast_type="success")
        toast = Toast(params)
        qtbot.addWidget(toast)

        assert "Hello Toast" in toast._msg_text
        assert toast._type == "success"
        assert toast.windowFlags() & Qt.WindowType.FramelessWindowHint

    def test_setup_animation(self, qtbot):
        params = ToastParams(message="Anim", pulse=True)
        toast = Toast(params)
        qtbot.addWidget(toast)

        assert hasattr(toast, "_fade_in")
        assert hasattr(toast, "_fade_out")
        assert hasattr(toast, "_pulse_anim")

    def test_show_at(self, qtbot):
        params = ToastParams(message="Pos")
        toast = Toast(params)
        qtbot.addWidget(toast)

        toast.show_at(100, 200)
        assert toast.pos().x() == 100
        assert toast.pos().y() == 200
        assert toast.isVisible()

    def test_mouse_hover_pause(self, qtbot):
        params = ToastParams(message="Hover", duration=1000)
        toast = Toast(params)
        qtbot.addWidget(toast)

        toast.show_at(0, 0)
        assert toast._hide_timer.isActive()

        # Simuliamo ingresso mouse
        from PySide6.QtCore import QPointF
        from PySide6.QtGui import QEnterEvent

        enter_event = QEnterEvent(QPointF(0, 0), QPointF(0, 0), QPointF(0, 0))
        toast.enterEvent(enter_event)

        assert not toast._hide_timer.isActive()

        # Simuliamo uscita mouse
        from PySide6.QtCore import QEvent

        leave_event = QEvent(QEvent.Type.Leave)
        toast.leaveEvent(leave_event)

        assert toast._hide_timer.isActive()


class TestToastManager:
    """Test suite per ToastManager."""

    def test_singleton(self):
        m1 = ToastManager.instance()
        m2 = ToastManager.instance()
        assert m1 is m2

    def test_show_toast(self, qtbot):
        mgr = ToastManager.instance()
        # Reset stato interno per il test
        ToastManager._active_toasts = []

        mgr.show("Manager Toast", toast_type=Toast.Type.SUCCESS)

        assert len(ToastManager._active_toasts) == 1
        assert ToastManager._active_toasts[0]._msg_text == "Manager Toast"

    def test_prevention_duplicates(self, qtbot):
        mgr = ToastManager.instance()
        ToastManager._active_toasts = []

        mgr.show("Duplicate")
        mgr.show("Duplicate")  # Dovrebbe essere ignorato

        assert len(ToastManager._active_toasts) == 1

    def test_limit_toasts(self, qtbot):
        mgr = ToastManager.instance()
        ToastManager._active_toasts = []

        mgr.show("1")
        mgr.show("2")
        mgr.show("3")
        mgr.show("4")  # Dovrebbe essere ignorato (limite 3)

        assert len(ToastManager._active_toasts) == 3

    def test_helper_functions(self, qtbot, mocker):
        mock_show = mocker.patch.object(ToastManager.instance(), "show")

        toast_info("Info message")
        assert mock_show.called
        assert mock_show.call_args[0][0] == "Info message"
        assert mock_show.call_args[0][1] == Toast.Type.INFO

        toast_success("Success!")
        assert mock_show.call_args[0][0] == "Success!"
        assert mock_show.call_args[0][1] == Toast.Type.SUCCESS
