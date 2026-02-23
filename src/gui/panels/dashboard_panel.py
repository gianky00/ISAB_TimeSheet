"""
SyncroJob - Dashboard Panel
Pannello di controllo principale (Home) dell'applicazione.
Organizza le azioni rapide, lo stato dell'Autopilot e il feed delle attività recenti.
"""

import os
from contextlib import suppress

from PyQt6.QtCore import (
    Qt,
    QTimer,
)
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.gui.widgets.activity_feed import ActivityFeed
from src.gui.widgets.autopilot import AutopilotWidget
from src.gui.widgets.quick_actions import QuickActions


class DashboardPanel(QWidget):
    """
    Pannello Home con layout raffinato ed elementi interattivi.
    Fornisce un riepilogo visivo dello stato del sistema e accesso rapido a tutte le funzioni.
    Include un timer per l'aggiornamento automatico dei dati in tempo reale.
    """

    def __init__(self, parent=None):
        """
        Inizializza il pannello dashboard e configura il contenitore principale.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.main_container: QFrame
        self.container_layout: QVBoxLayout
        self.scroll_area: QScrollArea
        self.content_widget: QWidget
        self.content_layout: QVBoxLayout
        self.quick_actions: QuickActions
        self.autopilot_widget: AutopilotWidget
        self.activity_feed: ActivityFeed

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

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

        self.main_layout.addWidget(self.main_container)

        self.chart = None

        self._setup_ui()

        # Refresh Timer (Live Dashboard)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_live_data)
        self.timer.start(30000)  # 30 seconds

    def refresh_data(self):
        """Esegue un aggiornamento forzato di tutti i widget della dashboard."""
        self.refresh_live_data()

    def refresh_live_data(self):
        """Aggiorna i dati dinamici dei widget (Feed, Azioni, Autopilot) senza ricostruire la UI."""
        if self.activity_feed:
            self.activity_feed.refresh_feed()

        if hasattr(self, "quick_actions"):
            self.quick_actions.refresh_actions()

        if hasattr(self, "autopilot_widget"):
            self.autopilot_widget.refresh_events()

    def _setup_ui(self):
        """Inizializza e posiziona i widget della dashboard nel layout dei contenuti."""
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

        self.content_layout.addStretch()

        # 2. Activity Feed (Bottom)
        subtitle = QLabel("Feed Attività")
        subtitle.setStyleSheet("font-size: 16px; font-weight: 700; color: #6c757d; margin-top: 20px;")
        self.content_layout.addWidget(subtitle)

        self.activity_feed = ActivityFeed()
        self.content_layout.addWidget(self.activity_feed)

        self.refresh_live_data()

    def _navigate_to(self, key):
        """Naviga verso un pannello specifico identificato da una chiave stringa."""
        main_window = self.window()
        if main_window is not None and hasattr(main_window, "navigate_to_panel"):
            main_window.navigate_to_panel(key)

    def _handle_quick_action(self, key):
        """Dispatch centralizzato per le azioni rapide cliccate nell'UI."""
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
        """Gestisce comandi globali come la sincronizzazione o l'apertura cartelle."""
        if key == "cmd_sync":
            self.refresh_data()
            return True
        if key == "cmd_open_folder":
            from src.core.config_manager import BASE_DIR

            output_dir = BASE_DIR / "output"
            output_dir.mkdir(exist_ok=True)
            if os.name == "nt":
                os.startfile(output_dir)  # noqa: S606
            else:
                import subprocess

                subprocess.run(["xdg-open", str(output_dir)])
            return True
        return False

    def _handle_automation_commands(self, key, main_window) -> bool:
        """Gestisce la navigazione verso i pannelli di automazione dei bot."""
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
        """Gestisce la navigazione verso le sezioni database e storici."""

        if key == "nav_storico_oda":
            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(10)
            return True

        if key.startswith("nav_sub_strumentale_"):
            return self._handle_strumentale_subtabs(key, main_window)

        if key in ("nav_page_2", "nav_lyra_ask"):
            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(2)
            return True

        if key.startswith("nav_sub_notifiche_"):
            return self._handle_notifications_subtabs(key, main_window)

        return False

    def _handle_strumentale_subtabs(self, key, main_window) -> bool:
        """Helper per la navigazione diretta verso i tab della contabilità strumentale."""
        with suppress(ValueError):
            tab_idx = int(key.split("_")[-1])

            if hasattr(main_window, "_navigate_to"):
                main_window._navigate_to(4)

                QTimer.singleShot(
                    100,
                    lambda: self._switch_tab_safe(main_window, "contabilita_panel", tab_idx),
                )
        return True

    def _handle_notifications_subtabs(self, key, main_window) -> bool:
        """Helper per la navigazione verso i tab delle notifiche."""
        with suppress(ValueError):
            tab_idx = int(key.split("_")[-1])

            if hasattr(main_window, "_handle_notifications_tab_change"):
                main_window._handle_notifications_tab_change(tab_idx)
        return True

    def _handle_settings_commands(self, key, main_window) -> bool:
        """Gestisce la navigazione verso specifiche sezioni delle impostazioni."""
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
                    lambda: self._switch_tab_safe(main_window, "settings_panel", tab_idx),
                )
            return True
        return False

    def _handle_navigation_fallback(self, key, main_window):
        """Gestisce percorsi di navigazione generici o legacy basati su prefissi chiave."""
        if key.startswith("nav_page_"):
            with suppress(ValueError):
                page_idx = int(key.split("_")[-1])
                if hasattr(main_window, "_navigate_to"):
                    main_window._navigate_to(page_idx)

        elif key.startswith("nav_sub_timbrature_"):
            # Timbrature Sub-Tabs
            with suppress(ValueError):
                tab_idx = int(key.split("_")[-1])
                if hasattr(main_window, "_navigate_to"):
                    main_window._navigate_to(3)
                    QTimer.singleShot(
                        100,
                        lambda: self._switch_tab_safe(main_window, "timbrature_db_panel", tab_idx),
                    )

        elif key.startswith("nav_sub_automazioni_"):
            # Automazioni Sub-tabs
            with suppress(ValueError):
                tab_idx = int(key.split("_")[-1])
                if hasattr(main_window, "_handle_automation_tab_change"):
                    main_window._handle_automation_tab_change(tab_idx)

    def _switch_tab_safe(self, main_window, panel_attr, tab_idx):
        """Helper per cambiare tab su un pannello bersaglio garantendo l'esistenza dell'attributo."""
        if hasattr(main_window, panel_attr):
            panel = getattr(main_window, panel_attr)
            if hasattr(panel, "tabs"):
                panel.tabs.setCurrentIndex(tab_idx)
            elif hasattr(panel, "main_tabs"):
                panel.main_tabs.setCurrentIndex(tab_idx)
