"""
SyncroJob - Dashboard Panel
Pannello di controllo principale (Home) dell'applicazione.
Refactored V9.6: Integrated Weather Widget and Bot Savings (ROI) Tracker.
"""

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

from src.gui.styles import COLORS
from src.gui.widgets import DashboardStatCard
from src.gui.widgets.activity_feed import ActivityFeed
from src.gui.widgets.autopilot import AutopilotWidget
from src.gui.widgets.dashboard.multi_window_status import MultiWindowStatusWidget
from src.gui.widgets.dashboard.roi_widget import BotSavingsWidget

# Nuovi Widget Dashboard
from src.gui.widgets.dashboard.weather_widget import WeatherWidget
from src.gui.widgets.quick_actions import QuickActions


class DashboardPanel(QWidget):
    """
    Dashboard Home evoluta.
    Sostituisce le card statiche con indicatori dinamici di valore (ROI) e contesto (Meteo).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Main Floating Container
        self.main_container = QFrame()
        self.main_container.setObjectName("mainDashboardContainer")
        self.main_container.setStyleSheet(
            f"""
            QFrame#mainDashboardContainer {{
                background-color: {COLORS["bg_white"]};
                border-radius: 20px;
                border: 1px solid {COLORS["border_light"]};
            }}
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

        self._setup_ui()

        # Refresh Timer (Live Dashboard)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_live_data)
        self.timer.start(30000)  # 30 seconds

    def refresh_data(self):
        """Esegue un aggiornamento forzato di tutti i widget della dashboard."""
        self.refresh_live_data()

    def refresh_live_data(self):
        """Aggiorna i dati dinamici dei widget senza ricostruire la UI."""
        self._update_quick_stats()
        with suppress(Exception):
            if hasattr(self, "activity_feed"):
                self.activity_feed.refresh_feed()

            if hasattr(self, "quick_actions"):
                self.quick_actions.refresh_actions()

            if hasattr(self, "autopilot_widget"):
                self.autopilot_widget.refresh_events()

            if hasattr(self, "roi_widget"):
                self.roi_widget.refresh_stats()

    def _setup_ui(self):
        """Inizializza e posiziona i widget della dashboard."""
        # -1. Multi Window Status Card
        self.multi_window_card = MultiWindowStatusWidget()
        self.content_layout.addWidget(self.multi_window_card)

        # 0. Context & Value Row (Meteo & ROI)
        context_row = QHBoxLayout()
        context_row.setSpacing(20)

        self.weather_widget = WeatherWidget()
        self.roi_widget = BotSavingsWidget()

        from src.core.constants import Icons

        self.card_pdl = DashboardStatCard("PDL In Database", "0", Icons.FILE_TEXT, COLORS["primary_blue"])

        context_row.addWidget(self.weather_widget, stretch=1)
        context_row.addWidget(self.roi_widget, stretch=1)
        context_row.addWidget(self.card_pdl, stretch=1)
        self.content_layout.addLayout(context_row)

        # 1. Quick Actions Row + Autopilot (Middle)
        actions_row = QHBoxLayout()
        actions_row.setSpacing(20)
        actions_row.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.quick_actions = QuickActions()
        self.quick_actions.action_clicked.connect(self._handle_quick_action)
        actions_row.addWidget(self.quick_actions, stretch=2)

        self.autopilot_widget = AutopilotWidget()
        actions_row.addWidget(self.autopilot_widget, stretch=1)

        self.content_layout.addLayout(actions_row)

        self.content_layout.addStretch()

        # 2. Activity Feed (Bottom)
        subtitle = QLabel("Feed Attività Recenti")
        subtitle.setStyleSheet(
            f"font-size: 16px; font-weight: 700; color: {COLORS['text_muted']}; margin-top: 20px;"
        )
        self.content_layout.addWidget(subtitle)

        self.activity_feed = ActivityFeed()
        self.content_layout.addWidget(self.activity_feed)

        self._update_quick_stats()

    def _update_quick_stats(self):
        """Recupera dati reali dal DB per la card PDL."""
        from src.core.database import db_manager
        from src.core.sync_tracker import SyncTracker

        with suppress(Exception):
            res = db_manager.execute_query(db_manager.DB_PDL, "SELECT COUNT(*) FROM pdl")
            total_pdl = res[0][0] if res else 0

            active_q = """
                SELECT COUNT(*) FROM pdl
                WHERE stato LIKE 'Aperto%'
                   OR stato LIKE 'Emesso%'
                   OR stato LIKE 'Richiesto%'
                   OR stato LIKE 'Accettato%'
            """
            res_active = db_manager.execute_query(db_manager.DB_PDL, active_q)
            active_pdl = res_active[0][0] if res_active else 0

            last_sync = SyncTracker.get_formatted_status("pdl")
            self.card_pdl.update_value(
                str(total_pdl),
                f"ATTIVE: {active_pdl} | CHIUSE: {total_pdl - active_pdl}",
                f"Ultima Sincronizzazione: {last_sync}",
            )

    def _handle_quick_action(self, key):
        main_window = self.window()
        if main_window is None or not hasattr(main_window, "navigation_controller"):
            return

        nav = main_window.navigation_controller

        # Mapping bot -> navigate_to_panel keys
        automation_map = {
            "nav_dettagli_oda": "dettagli_oda",
            "nav_scarico_ts": "scarico_ts",
            "nav_carico_ts": "carico_ts",
            "pf_timbrature": "timbrature",
            "pf_prenota_bp": "prenota_bp",
            "nav_scarico_pdl": "scarico_pdl",
            "nav_ricerca_pdl": "ricerca_pdl",
        }

        # Handle specific page navigation
        if key in automation_map:
            nav.navigate_to_panel(automation_map[key])
        elif key.startswith("nav_sub_strumentale_"):
            from contextlib import suppress
            with suppress(ValueError):
                sub_idx = int(key.split("_")[-1])
                nav.navigate_to(4, sub_index=sub_idx)
        elif key == "nav_page_2":
            nav.navigate_to(2)  # Lyra
        elif key == "nav_page_5":
            nav.navigate_to(5)  # DataEase
        elif key == "nav_page_6":
            nav.navigate_to(6)  # Anagrafiche PDL
        elif key == "nav_page_8":
            nav.navigate_to(8)  # Guida
        elif key == "nav_page_11":
            nav.navigate_to(11) # Dipendenti
        elif key == "nav_storico_oda":
            nav.navigate_to(10) # Storico OdA
        elif key == "nav_sub_notifiche_1":
            nav.navigate_to(9, sub_index=1) # Notifiche -> Audit
        elif key.startswith("settings_"):
            # Mappa le sotto-pagine dei settings (se configurate tramite sub_index)
            # Al momento mandiamo al pannello Impostazioni (7) principale
            nav.navigate_to(7)
