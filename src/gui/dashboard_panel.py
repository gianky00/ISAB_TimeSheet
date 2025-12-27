"""
Bot TS - Dashboard Panel
Pannello "Mappa Applicazione" interattiva e modulare.
Updated to use ResponsiveContainer.
"""
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout,
    QScrollArea, QPushButton, QSizePolicy, QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QCursor, QIcon, QColor

from src.core.stats_manager import StatsManager
from src.gui.layouts.responsive import ResponsiveContainer

class DashboardPanel(QWidget):
    """Pannello Home con Mappa Modulare Interattiva Responsiva."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(30)

        # Scroll Area for responsive content if it overflows
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(30)

        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)

        self.refresh_data()

    def refresh_data(self):
        """Ricostruisce la UI per aggiornare statistiche e saluto."""
        self._clear_layout(self.content_layout)
        self._setup_ui()

    def _clear_layout(self, layout):
        """Rimuove ricorsivamente tutti gli elementi da un layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self._clear_layout(item.layout())

    def _setup_ui(self):
        # Dynamic Greeting
        hour = datetime.now().hour
        greeting = "Buongiorno" if 5 <= hour < 18 else "Buonasera"

        # Header
        header_layout = QVBoxLayout()
        title = QLabel(f"👋 {greeting}, benvenuto in Timesheet Manager")
        title.setStyleSheet("font-size: 32px; font-weight: 800; color: #343a40;")
        header_layout.addWidget(title)

        subtitle = QLabel("Seleziona il modulo operativo che desideri utilizzare.")
        subtitle.setStyleSheet("font-size: 18px; color: #6c757d;")
        header_layout.addWidget(subtitle)

        self.content_layout.addLayout(header_layout)

        # Retrieve Stats
        stats = StatsManager().get_all_stats()

        # Responsive Grid Container
        responsive_grid = ResponsiveContainer()

        # --- Bots ---
        # 1. Dettagli OdA
        s_oda = stats.get("dettagli_oda", {})
        responsive_grid.addWidget(self._create_module_card(
            "Dettagli OdA", "Scarica dettagli ordini.", "📋", "#6f42c1", "dettagli_oda",
            s_oda.get("runs", 0), s_oda.get("errors", 0)
        ))

        # 2. Scarico TS
        s_sts = stats.get("scarico_ts", {})
        responsive_grid.addWidget(self._create_module_card(
            "Scarico TS", "Scarica timesheet.", "📥", "#0d6efd", "scarico_ts",
            s_sts.get("runs", 0), s_sts.get("errors", 0)
        ))

        # 3. Timbrature
        s_tmb = stats.get("timbrature", {})
        responsive_grid.addWidget(self._create_module_card(
            "Timbrature", "Valida timbrature.", "⏱️", "#fd7e14", "timbrature",
            s_tmb.get("runs", 0), s_tmb.get("errors", 0)
        ))

        # 4. Carico TS
        s_cts = stats.get("carico_ts", {})
        responsive_grid.addWidget(self._create_module_card(
            "Carico TS", "Upload finale.", "📤", "#198754", "carico_ts",
            s_cts.get("runs", 0), s_cts.get("errors", 0)
        ))

        # --- Databases ---

        # 5. Timbrature DB
        responsive_grid.addWidget(self._create_module_card(
            "Timbrature Isab", "Database storico.", "🗃️", "#20c997", "db_timbrature",
            None, None
        ))

        # 6. Strumentale DB
        responsive_grid.addWidget(self._create_module_card(
            "Strumentale", "Contabilità & KPI.", "📊", "#ffc107", "db_strumentale",
            None, None
        ))

        # 7. DataEase DB
        responsive_grid.addWidget(self._create_module_card(
            "DataEase", "Scarico ore cantiere.", "🏗️", "#0dcaf0", "db_dataease",
            None, None
        ))

        self.content_layout.addWidget(responsive_grid)
        self.content_layout.addStretch()

    def _create_module_card(self, title, desc, icon, color, action_key, runs, errors):
        """Crea una card cliccabile ricca per un singolo modulo."""
        card = QFrame()
        # Responsive height fix?
        card.setMinimumSize(250, 200)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 20))
        card.setGraphicsEffect(shadow)

        # Stile Card
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 16px;
                border-left: 6px solid {color};
            }}
            QFrame:hover {{
                background-color: #f8f9fa;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)

        # Header Row: Title & Icon
        header_row = QHBoxLayout()

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 18px; font-weight: 800; color: #212529; border: none;")
        header_row.addWidget(title_lbl)

        header_row.addStretch()

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"font-size: 28px; color: {color}; border: none;")
        header_row.addWidget(icon_lbl)

        card_layout.addLayout(header_row)

        # Description
        desc_lbl = QLabel(desc)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("font-size: 13px; color: #6c757d; border: none; margin-bottom: 5px;")
        card_layout.addWidget(desc_lbl)

        card_layout.addStretch()

        # Stats Row
        if runs is not None:
            stats_row = QHBoxLayout()

            # Runs Badge
            runs_lbl = QLabel(f"🚀 {runs}")
            runs_lbl.setToolTip("Esecuzioni")
            runs_lbl.setStyleSheet("""
                background-color: #e9ecef;
                color: #495057;
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 11px;
                font-weight: bold;
                border: none;
            """)
            stats_row.addWidget(runs_lbl)

            if errors is not None and errors > 0:
                err_lbl = QLabel(f"⚠️ {errors}")
                err_lbl.setToolTip("Errori")
                err_lbl.setStyleSheet("""
                    background-color: #f8d7da;
                    color: #721c24;
                    border-radius: 10px;
                    padding: 2px 8px;
                    font-size: 11px;
                    font-weight: bold;
                    border: none;
                """)
                stats_row.addWidget(err_lbl)

            stats_row.addStretch()

            # Action Arrow
            arrow_lbl = QLabel("➜")
            arrow_lbl.setStyleSheet(f"font-size: 16px; color: {color}; font-weight: bold; border: none;")
            stats_row.addWidget(arrow_lbl)

            card_layout.addLayout(stats_row)
        else:
            # For Databases (No stats), just show arrow at bottom right
            stats_row = QHBoxLayout()
            stats_row.addStretch()
            arrow_lbl = QLabel("➜")
            arrow_lbl.setStyleSheet(f"font-size: 16px; color: {color}; font-weight: bold; border: none;")
            stats_row.addWidget(arrow_lbl)
            card_layout.addLayout(stats_row)

        # Full Card Click Button Overlay
        btn = QPushButton(card)
        btn.setStyleSheet("background: transparent; border: none;")
        btn.clicked.connect(lambda: self._navigate_to(action_key))

        # Ensure button resizes with card
        card.resizeEvent = lambda e: btn.resize(e.size())

        return card

    def _navigate_to(self, key):
        """Naviga alla tab specificata."""
        main_window = self.window()
        if hasattr(main_window, 'navigate_to_panel'):
            main_window.navigate_to_panel(key)
