import os

from PyQt6.QtCore import (  # type: ignore
    Qt,
    QTimer,
)
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.gui.widgets.activity_feed import ActivityFeed
from src.gui.widgets.autopilot_widget import AutopilotWidget
from src.gui.widgets.quick_actions import QuickActions


class DashboardPanel(QWidget):
    """Pannello Home con Layout Raffinato."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(0)

        # Main Floating Container
        self.main_container = QFrame()
        self.main_container.setObjectName("mainDashboardContainer")
        self.main_container.setStyleSheet(
            """
            QFrame#mainDashboardContainer {
                background-color: #ffffff;
                border-radius: 20px;
                border: 1px solid #dee2e6;
            }
        """
        )

        container_shadow = QGraphicsDropShadowEffect()
        container_shadow.setBlurRadius(30)
        container_shadow.setXOffset(0)
        container_shadow.setYOffset(10)
        container_shadow.setColor(QColor(0, 0, 0, 20))
        self.main_container.setGraphicsEffect(container_shadow)

        self.container_layout = QVBoxLayout(self.main_container)
        self.container_layout.setContentsMargins(25, 25, 25, 25)
        self.container_layout.setSpacing(20)

        # Scroll Area inside container
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(25)

        self.scroll_area.setWidget(self.content_widget)
        self.container_layout.addWidget(self.scroll_area)

        self.layout.addWidget(self.main_container)

        # SubWidgets references
        self.activity_feed = None
        self.chart = None

        self._setup_ui()

        # Refresh Timer (Live Dashboard)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_live_data)
        self.timer.start(30000)  # 30 seconds

    def refresh_data(self):
        """Metodo chiamato esternamente per force-refresh."""
        self.refresh_live_data()

    def refresh_live_data(self):
        """Aggiorna i dati senza ricostruire l'intera UI se possibile."""
        if self.activity_feed:
            self.activity_feed.refresh_feed()

        if hasattr(self, "quick_actions"):
            self.quick_actions.refresh_actions()

        if hasattr(self, "autopilot_widget"):
            self.autopilot_widget.refresh_events()

    def _setup_ui(self):
        # 1. Quick Actions Row + Autopilot (Top)
        actions_row = QHBoxLayout()
        actions_row.setSpacing(20)
        actions_row.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Quick Actions (Left)
        self.quick_actions = QuickActions()
        self.quick_actions.action_clicked.connect(self._handle_quick_action)
        actions_row.addWidget(self.quick_actions, stretch=2)

        # Autopilot Widget (Right)
        self.autopilot_widget = AutopilotWidget()
        actions_row.addWidget(self.autopilot_widget, stretch=1)

        self.content_layout.addLayout(actions_row)

        # Space to push the activity feed to the bottom
        self.content_layout.addStretch()

        # 2. Activity Feed (Bottom)
        subtitle = QLabel("Feed Attività")
        subtitle.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #6c757d; margin-top: 20px;"
        )
        self.content_layout.addWidget(subtitle)

        self.activity_feed = ActivityFeed()
        self.content_layout.addWidget(self.activity_feed)

        # Initial data load
        self.refresh_live_data()

    def _navigate_to(self, key):
        """Naviga alla tab specificata."""
        main_window = self.window()
        if hasattr(main_window, "navigate_to_panel"):
            main_window.navigate_to_panel(key)

    def _handle_quick_action(self, key):
        """Gestisce i click delle azioni rapide con navigazione completa."""
        main_window = self.window()

        if self._handle_general_commands(key, main_window):
            return
        if self._handle_automation_commands(key, main_window):
            return
        if self._handle_database_commands(key, main_window):
            return
        if self._handle_settings_commands(key, main_window):
            return
        self._handle_navigation_fallback(key, main_window)

    def _handle_general_commands(self, key, main_window) -> bool:
        """Gestisce comandi generali (sync, cartelle)."""
        if key == "cmd_sync":
            self.refresh_data()
            return True
        elif key == "cmd_open_folder":
            from src.core.config_manager import BASE_DIR

            output_dir = BASE_DIR / "output"
            output_dir.mkdir(exist_ok=True)
            if os.name == "nt":
                os.startfile(output_dir)
            else:
                import subprocess

                subprocess.run(["xdg-open", str(output_dir)])
            return True
        return False

    def _handle_automation_commands(self, key, main_window) -> bool:
        """Gestisce navigazione verso automazioni specifiche."""
        # Mappa chiavi quick actions -> panel keys per navigation_controller
        automation_map = {
            "nav_dettagli_oda": "dettagli_oda",
            "nav_scarico_ts": "scarico_ts",
            "nav_carico_ts": "carico_ts",
            "pf_timbrature": "timbrature",
            "pf_prenota_bp": "prenota_bp",
            "nav_scarico_pdl": "scarico_pdl",
            "nav_ricerca_pdl": "ricerca_pdl",
        }

        if key in automation_map:
            panel_key = automation_map[key]
            if hasattr(main_window, "navigation_controller"):
                main_window.navigation_controller.navigate_to_panel(panel_key)
            return True
        return False

    def _handle_database_commands(self, key, main_window) -> bool:
        """Gestisce navigazione verso database e notifiche."""

        if key == "nav_storico_oda":
            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(10)

            return True

        if key.startswith("nav_sub_strumentale_"):
            return self._handle_strumentale_subtabs(key, main_window)

        if key == "nav_page_2" or key == "nav_lyra_ask":
            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(2)

            return True

        if key.startswith("nav_sub_notifiche_"):
            return self._handle_notifications_subtabs(key, main_window)

        return False

    def _handle_strumentale_subtabs(self, key, main_window) -> bool:
        """Helper per tab strumentale."""

        try:
            tab_idx = int(key.split("_")[-1])

            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(4)

                QTimer.singleShot(
                    100,
                    lambda: self._switch_tab_safe(
                        main_window, "contabilita_panel", tab_idx
                    ),
                )

        except ValueError:
            pass

        return True

    def _handle_notifications_subtabs(self, key, main_window) -> bool:
        """Helper per tab notifiche."""

        try:
            tab_idx = int(key.split("_")[-1])

            if hasattr(main_window, "_handle_notifications_tab_change"):
                main_window._handle_notifications_tab_change(tab_idx)

        except ValueError:
            pass

        return True

    def _handle_settings_commands(self, key, main_window) -> bool:
        """Gestisce navigazione verso impostazioni."""
        settings_map = {
            "settings_configurazione": 0,
            "settings_backup_cloud": 1,
            "settings_statistiche": 2,
            "settings_telegram": 3,
        }
        if key in settings_map:
            tab_idx = settings_map[key]
            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(7)
                QTimer.singleShot(
                    100,
                    lambda: self._switch_tab_safe(
                        main_window, "settings_panel", tab_idx
                    ),
                )
            return True
        return False

    def _handle_navigation_fallback(self, key, main_window):
        """Gestisce navigazione generica di fallback."""
        if key.startswith("nav_page_"):
            try:
                page_idx = int(key.split("_")[-1])
                if hasattr(main_window, "_navigate_to"):
                    main_window._navigate_to(page_idx)
            except ValueError:
                pass

        elif key.startswith("nav_sub_timbrature_"):
            # Timbrature Sub-Tabs
            try:
                tab_idx = int(key.split("_")[-1])
                if hasattr(main_window, "_navigate_to"):
                    main_window._navigate_to(3)  # Timbrature Page
                    QTimer.singleShot(
                        100,
                        lambda: self._switch_tab_safe(
                            main_window, "timbrature_db_panel", tab_idx
                        ),
                    )
            except ValueError:
                pass

        elif key.startswith("nav_sub_automazioni_"):
            # Automazioni Sub-tabs (legacy)
            try:
                tab_idx = int(key.split("_")[-1])
                if hasattr(main_window, "_handle_automation_tab_change"):
                    main_window._handle_automation_tab_change(tab_idx)
            except ValueError:
                pass

    def _switch_tab_safe(self, main_window, panel_attr, tab_idx):
        """Helper to switch tabs on a target panel if it exists."""
        if hasattr(main_window, panel_attr):
            panel = getattr(main_window, panel_attr)
            # Try common tab names
            if hasattr(panel, "tabs"):
                panel.tabs.setCurrentIndex(tab_idx)
            elif hasattr(panel, "main_tabs"):
                panel.main_tabs.setCurrentIndex(tab_idx)

    # Note: nav_scarico_pdl, nav_carico_ts will fall through to nav_ prefix handler
    # and try to navigate to 'scarico_pdl', 'carico_ts'.
    # MainWindow must have these registered in panels.py/main_window.py logic.
