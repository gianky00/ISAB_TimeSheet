"""
SyncroJob - Dashboard Panel
Pannello di controllo principale (Home) dell'applicazione.
Refactored V9.7: Integrated PDL Stats Widget with Trends and Interactive Areas.
"""

from __future__ import annotations

from contextlib import suppress
from typing import Any

from PySide6.QtCore import (
    Qt,
    QTimer,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.gui.styles import COLORS
from src.gui.widgets.activity_feed import ActivityFeed
from src.gui.widgets.autopilot import AutopilotWidget
from src.gui.widgets.dashboard.multi_window_status import MultiWindowStatusWidget
from src.gui.widgets.dashboard.pdl_stats_widget import PDLStatsWidget
from src.gui.widgets.dashboard.roi_widget import BotSavingsWidget
from src.gui.widgets.dashboard.weather_widget import WeatherWidget
from src.gui.widgets.quick_actions import QuickActions


class DashboardPanel(QWidget):
    """
    Dashboard Home evoluta.
    Sostituisce le card statiche con indicatori dinamici di valore (ROI) e contesto (Meteo/PDL).
    """

    def __init__(self, parent: QWidget | None = None) -> None:
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

        # Widget attributes
        self.multi_window_card: MultiWindowStatusWidget
        self.weather_widget: WeatherWidget
        self.roi_widget: BotSavingsWidget
        self.card_pdl: PDLStatsWidget
        self.quick_actions: QuickActions
        self.autopilot_widget: AutopilotWidget
        self.activity_feed: ActivityFeed

        self._setup_ui()

        # Refresh Timer (Live Dashboard)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_live_data)
        self.timer.start(30000)  # 30 seconds

    def refresh_data(self) -> None:
        # """Esegue un aggiornamento forzato di tutti i widget della dashboard."""
        self.refresh_live_data()

    def refresh_live_data(self) -> None:
        """Aggiorna i dati dinamici dei widget senza ricostruire la UI."""
        with suppress(Exception):
            if hasattr(self, "activity_feed") and self.activity_feed:
                self.activity_feed.refresh_feed()

            if hasattr(self, "quick_actions") and self.quick_actions:
                self.quick_actions.refresh_actions()

            if hasattr(self, "autopilot_widget") and self.autopilot_widget:
                self.autopilot_widget.refresh_events()

            if hasattr(self, "roi_widget") and self.roi_widget:
                self.roi_widget.refresh_stats()

            if hasattr(self, "card_pdl") and self.card_pdl:
                self.card_pdl.refresh_stats()

    def _setup_ui(self) -> None:
        """Inizializza e posiziona i widget della dashboard."""
        # -1. Multi Window Status Card
        self.multi_window_card = MultiWindowStatusWidget()
        self.content_layout.addWidget(self.multi_window_card)

        # 0. Context & Value Row (Meteo, ROI & PDL)
        context_row = QHBoxLayout()
        context_row.setSpacing(20)

        self.weather_widget = WeatherWidget()
        self.roi_widget = BotSavingsWidget()
        self.card_pdl = PDLStatsWidget()

        # Connessione navigazione filtrata
        self.card_pdl.area_selected.connect(self._handle_pdl_area_click)

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
        self.autopilot_widget.bot_sync_requested.connect(self._handle_bot_sync_requested)
        actions_row.addWidget(self.autopilot_widget, stretch=1)

        self.content_layout.addLayout(actions_row)

        self.content_layout.addStretch()

        # 2. Activity Feed (Bottom)
        subtitle = QLabel("Feed AttivitàRecenti")
        subtitle.setStyleSheet(
            f"font-size: 16px; font-weight: 700; color: {COLORS['text_muted']}; margin-top: 20px;"
        )
        self.content_layout.addWidget(subtitle)

        self.activity_feed = ActivityFeed()
        self.content_layout.addWidget(self.activity_feed)

    def _handle_pdl_area_click(self, area_name: str) -> None:
        """Gestisce il click su un'area specifica dei PDL, navigando alla vista filtrata."""
        main_window: Any = self.window()
        if main_window is None or not hasattr(main_window, "navigation_controller"):
            return

        # Mapping inverso: Nome Visualizzato -> Nome Database
        db_area_name = {
            "Area 1": "Process Area 1",
            "Area 2": "Process Area 2",
            "Area 3": "Process Area 3",
            "Blending Sud": "Blending Sud",
            "Pontile Sud": "Pontile Sud",
            "UTILITIES (CTE/TAS)": "UTILITIES (CTE/TAS)",
        }.get(area_name, area_name)

        # Navigazione al database PDL con filtri pre-impostati
        main_window.navigation_controller.navigate_to_pdl(site="ISAB Sud", area=db_area_name)

    def _handle_bot_sync_requested(self, bot_id: str) -> None:
        """Avvia manualmente un bot dell'autopilot dal controller centrale."""
        mw: Any = self.window()
        if mw is None or not hasattr(mw, "service_controller"):
            return

        # Mapping bot_id -> (panel_attr, site, log_msg)
        bot_map = {
            "timbrature": (
                "timbrature_bot_panel",
                "portale_fornitori",
                "Avvio manuale Timbrature da Dashboard...",
            ),
            "scarico_oda_generale": (
                "dettagli_panel",
                "portale_fornitori",
                "Avvio manuale OdA da Dashboard...",
            ),
            "ricerca_pdl": ("pdl_search_panel", "safework", "Avvio manuale PDL da Dashboard..."),
        }

        if bot_id not in bot_map:
            return

        panel_attr, site, log_msg = bot_map[bot_id]
        if hasattr(mw, panel_attr):
            panel = getattr(mw, panel_attr)
            # Se  OdA Generale, applichiamo la preparazione (pulizia filtri)
            if bot_id == "scarico_oda_generale":
                mw.service_controller._prepare_scarico_oda_generale(panel)

            mw.service_controller._schedule_bot_with_parallelism(bot_id, panel, site, log_msg)

    def _handle_quick_action(self, key: str) -> None:  # noqa: C901
        """Gestisce il click su un'azione rapida della dashboard."""
        main_window: Any = self.window()
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
            with suppress(ValueError):
                sub_idx = int(key.split("_")[-1])
                nav.navigate_to(4, sub_index=sub_idx)
        elif key == "nav_page_5":
            nav.navigate_to(5)  # DataEase
        elif key == "nav_page_6":
            nav.navigate_to(6)  # Anagrafiche PDL
        elif key == "nav_page_8":
            nav.navigate_to(8)  # Guida
        elif key == "nav_page_11":
            nav.navigate_to(11)  # Dipendenti
        elif key == "nav_storico_oda":
            nav.navigate_to(10)  # Storico OdA
        elif key.startswith("nav_sub_notifiche_"):
            with suppress(ValueError):
                sub_idx = int(key.split("_")[-1])
                nav.navigate_to(9, sub_index=sub_idx)
        elif key.startswith("settings_"):
            nav.navigate_to(7)
