from PyQt6.QtCore import QObject

from src.core.notification_manager import NotificationManager
from src.gui.widgets.toast import ToastManager


class SignalConnector(QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

    def connect_global_signals(self):
        """Connects global application signals."""
        # Toast Manager
        NotificationManager.instance().request_toast.connect(
            lambda msg, t, d: ToastManager.instance().show(msg, t, d)
        )

        # Notification Badge on Sidebar
        # Accessing sidebar via tool_bar_component
        if (
            hasattr(self.main_window, "tool_bar_component")
            and self.main_window.tool_bar_component.sidebar
        ):
            sidebar = self.main_window.tool_bar_component.sidebar
            NotificationManager.instance().unread_count_changed.connect(
                sidebar.group_notifiche.header_btn.set_badge
            )
            sidebar.group_notifiche.header_btn.set_badge(
                NotificationManager.instance().get_unread_count()
            )

    def connect_sidebar_signals(self):
        """Connects sidebar navigation signals."""
        if (
            not hasattr(self.main_window, "tool_bar_component")
            or not self.main_window.tool_bar_component.sidebar
        ):
            return

        sidebar = self.main_window.tool_bar_component.sidebar

        sidebar.navigation_requested.connect(
            self.main_window.navigation_controller.navigate_to
        )
        sidebar.automation_tab_requested.connect(
            self.main_window._handle_automation_tab_change
        )
        sidebar.notifications_tab_requested.connect(
            self.main_window._handle_notifications_tab_change
        )
        sidebar.palette_requested.connect(self.main_window._open_command_palette)
