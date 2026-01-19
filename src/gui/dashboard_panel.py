import os
import subprocess
from datetime import datetime

from PyQt6.QtCore import (  # type: ignore
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

from src.core.config_manager import BASE_DIR
from src.gui.widgets.activity_feed import ActivityFeed
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

    def _setup_ui(self):
        # 1. Header Section (Greeting Only, Clean)
        header_row = QHBoxLayout()

        greeting_col = QVBoxLayout()
        hour = datetime.now().hour
        greeting = "Buongiorno" if 5 <= hour < 18 else "Buonasera"
        title = QLabel(f"{greeting}! Dashboard Operativa")
        title.setStyleSheet("font-size: 28px; font-weight: 800; color: #343a40;")

        subtitle = QLabel("Overview Attività")
        subtitle.setStyleSheet("font-size: 16px; color: #6c757d;")

        greeting_col.addWidget(title)
        greeting_col.addWidget(subtitle)
        header_row.addLayout(greeting_col)
        header_row.addStretch()

        self.content_layout.addLayout(header_row)

        # 2. Activity Feed (Horizontal, Compact)
        self.activity_feed = ActivityFeed()
        self.content_layout.addWidget(self.activity_feed)

        # 3. Quick Actions Row (NO MODULES AFTER THIS)
        self.quick_actions = QuickActions()
        self.quick_actions.action_clicked.connect(self._handle_quick_action)
        self.content_layout.addWidget(self.quick_actions)

        self.content_layout.addStretch()

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

        # ============================================================
        # COMANDI GENERALI
        # ============================================================
        if key == "cmd_sync":
            self.refresh_data()
            if hasattr(main_window, "service_controller"):
                pass

        elif key == "cmd_open_folder":
            output_dir = BASE_DIR / "output"
            output_dir.mkdir(exist_ok=True)
            if os.name == "nt":
                os.startfile(output_dir)
            else:
                subprocess.run(["xdg-open", str(output_dir)])

        # ============================================================
        # AUTOMAZIONI > PORTALE FORNITORI
        # ============================================================
        elif key == "nav_dettagli_oda":
            # Automazioni (1) > Portale Fornitori (tab 0) > Dettagli OdA
            if hasattr(main_window, "_handle_automation_tab_change"):
                main_window._handle_automation_tab_change(0)

        elif key == "nav_scarico_ts":
            # Automazioni (1) > Portale Fornitori (tab 0) > Scarico TS
            if hasattr(main_window, "_handle_automation_tab_change"):
                main_window._handle_automation_tab_change(0)

        elif key == "nav_carico_ts":
            # Automazioni (1) > Portale Fornitori (tab 0) > Carico TS
            if hasattr(main_window, "_handle_automation_tab_change"):
                main_window._handle_automation_tab_change(0)

        elif key == "pf_timbrature":
            # Automazioni (1) > Portale Fornitori (tab 0) > Timbrature
            if hasattr(main_window, "_handle_automation_tab_change"):
                main_window._handle_automation_tab_change(0)

        elif key == "pf_prenota_bp":
            # Automazioni (1) > Portale Fornitori (tab 0) > Prenota BP
            if hasattr(main_window, "_handle_automation_tab_change"):
                main_window._handle_automation_tab_change(0)

        # ============================================================
        # DATABASE > STRUMENTALE
        # ============================================================
        elif key.startswith("nav_sub_strumentale_"):
            # Strumentale Sub-Tabs
            try:
                tab_idx = int(key.split("_")[-1])
                if hasattr(main_window, "_navigate_to"):
                    main_window._navigate_to(4)  # Strumentale Page
                    QTimer.singleShot(
                        100,
                        lambda: self._switch_tab_safe(
                            main_window, "contabilita_panel", tab_idx
                        ),
                    )
            except ValueError:
                pass

        # ============================================================
        # LYRA AI
        # ============================================================
        elif key == "nav_page_2" or key == "nav_lyra_ask":
            # Lyra AI (2)
            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(2)

        # ============================================================
        # NOTIFICHE
        # ============================================================
        elif key.startswith("nav_sub_notifiche_"):
            # Notifiche Sub-tabs (0: Messaggi, 1: Audit)
            try:
                tab_idx = int(key.split("_")[-1])
                if hasattr(main_window, "_handle_notifications_tab_change"):
                    main_window._handle_notifications_tab_change(tab_idx)
            except ValueError:
                pass

        # ============================================================
        # IMPOSTAZIONI
        # ============================================================
        elif key == "settings_configurazione":
            # Impostazioni (7) > Configurazione (tab 0)
            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(7)
                QTimer.singleShot(
                    100,
                    lambda: self._switch_tab_safe(main_window, "settings_panel", 0),
                )

        elif key == "settings_backup_cloud":
            # Impostazioni (7) > Backup Cloud (tab 1)
            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(7)
                QTimer.singleShot(
                    100,
                    lambda: self._switch_tab_safe(main_window, "settings_panel", 1),
                )

        elif key == "settings_statistiche":
            # Impostazioni (7) > Statistiche (tab 2)
            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(7)
                QTimer.singleShot(
                    100,
                    lambda: self._switch_tab_safe(main_window, "settings_panel", 2),
                )

        elif key == "settings_telegram":
            # Impostazioni (7) > Telegram (tab 3)
            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(7)
                QTimer.singleShot(
                    100,
                    lambda: self._switch_tab_safe(main_window, "settings_panel", 3),
                )

        # ============================================================
        # NAVIGAZIONE GENERICA (FALLBACK)
        # ============================================================
        elif key.startswith("nav_page_"):
            # Simple Page Navigation per tutte le altre pagine
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
