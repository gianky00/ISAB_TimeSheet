from datetime import datetime

from PyQt6.QtCore import (  # type: ignore
    QEasingCurve,
    QPropertyAnimation,
    QSize,
    Qt,
    pyqtProperty,
)
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.stats_manager import StatsManager
from src.gui.layouts.responsive import ResponsiveContainer
from src.utils.helpers import get_asset_path, get_colored_icon


class HoverCard(QFrame):
    """Card con effetto hover lift e ombra dinamica."""

    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.setMinimumSize(250, 200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Shadow Setup
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(self.shadow)

        # Pulsante overlay per il click (creato dal parent o internamente)
        self.click_btn = None

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: #ffffff;
                border-radius: 15px;
                border: 1px solid #e9ecef;
                border-left: 5px solid {color};
            }}
            QFrame:hover {{
                background-color: #f8f9fa;
                border: 1px solid {color}44;
                border-left: 6px solid {color};
            }}
        """
        )

        # Animation for Y Offset (Lift effect)
        self._y_offset = 4
        self.anim = QPropertyAnimation(self, b"yOffset")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    @pyqtProperty(int)  # type: ignore
    def yOffset(self):
        return self._y_offset

    @yOffset.setter  # type: ignore
    def yOffset(self, value):
        self._y_offset = value
        self.shadow.setYOffset(value)
        self.shadow.setBlurRadius(15 + (4 - value) * 2)

    def set_click_callback(self, callback):
        """Configura il pulsante trasparente sopra la card."""
        if not self.click_btn:
            self.click_btn = QPushButton(self)
            self.click_btn.setStyleSheet("background: transparent; border: none;")
            self.click_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.click_btn.show()
        self.click_btn.clicked.connect(callback)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.click_btn:
            self.click_btn.resize(event.size())

    def enterEvent(self, event):
        self.anim.setStartValue(self._y_offset)
        self.anim.setEndValue(8)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.setStartValue(self._y_offset)
        self.anim.setEndValue(4)
        self.anim.start()
        super().leaveEvent(event)


class DashboardPanel(QWidget):
    """Pannello Home con Mappa Modulare Interattiva Responsiva."""

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
        self.container_layout.setContentsMargins(30, 30, 30, 30)
        self.container_layout.setSpacing(20)

        # Scroll Area inside container
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(30)

        self.scroll_area.setWidget(self.content_widget)
        self.container_layout.addWidget(self.scroll_area)

        self.layout.addWidget(self.main_container)

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
        title = QLabel(f"{greeting}, benvenuto in Timesheet Manager")
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
        responsive_grid.addWidget(
            self._create_module_card(
                "Dettagli OdA",
                "Scarica dettagli ordini.",
                Icons.LIST,
                "#6f42c1",
                "dettagli_oda",
                s_oda.get("runs", 0),
                s_oda.get("errors", 0),
            )
        )

        # 2. Scarico TS
        s_sts = stats.get("scarico_ts", {})
        responsive_grid.addWidget(
            self._create_module_card(
                "Scarico TS",
                "Scarica timesheet.",
                Icons.DOWNLOAD,
                "#0d6efd",
                "scarico_ts",
                s_sts.get("runs", 0),
                s_sts.get("errors", 0),
            )
        )

        # 3. Timbrature
        s_tmb = stats.get("timbrature", {})
        responsive_grid.addWidget(
            self._create_module_card(
                "Timbrature",
                "Valida timbrature.",
                Icons.CLOCK,
                "#fd7e14",
                "timbrature",
                s_tmb.get("runs", 0),
                s_tmb.get("errors", 0),
            )
        )

        # 4. Carico TS
        s_cts = stats.get("carico_ts", {})
        responsive_grid.addWidget(
            self._create_module_card(
                "Carico TS",
                "Upload finale.",
                Icons.UPLOAD,
                "#198754",
                "carico_ts",
                s_cts.get("runs", 0),
                s_cts.get("errors", 0),
            )
        )

        # --- Databases ---

        # 5. Timbrature DB
        responsive_grid.addWidget(
            self._create_module_card(
                "Timbrature Isab",
                "Database storico.",
                Icons.DATABASE,
                "#20c997",
                "db_timbrature",
                None,
                None,
            )
        )

        # 6. Strumentale DB
        responsive_grid.addWidget(
            self._create_module_card(
                "Strumentale",
                "Contabilità & KPI.",
                Icons.DATABASE,  # Or chart?
                "#ffc107",
                "db_strumentale",
                None,
                None,
            )
        )

        # 7. DataEase DB
        responsive_grid.addWidget(
            self._create_module_card(
                "DataEase",
                "Scarico ore cantiere.",
                Icons.CPU,
                "#0dcaf0",
                "db_dataease",
                None,
                None,
            )
        )

        self.content_layout.addWidget(responsive_grid)
        self.content_layout.addStretch()

    def _create_module_card(
        self, title, desc, icon_path, color, action_key, runs, errors
    ):
        """Crea una card cliccabile ricca per un singolo modulo."""
        card = HoverCard(color)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)

        # Header Row: Title & Icon
        header_row = QHBoxLayout()

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(
            "font-size: 18px; font-weight: 800; color: #212529; border: none; background: transparent;"
        )
        header_row.addWidget(title_lbl)

        header_row.addStretch()

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(32, 32)
        icon_lbl.setScaledContents(True)
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        # Apply black color filter
        pixmap = get_colored_icon(get_asset_path(icon_path), "#000000").pixmap(
            QSize(32, 32)
        )
        icon_lbl.setPixmap(pixmap)
        header_row.addWidget(icon_lbl)

        card_layout.addLayout(header_row)

        # Description
        desc_lbl = QLabel(desc)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet(
            "font-size: 13px; color: #6c757d; border: none; background: transparent; margin-bottom: 5px;"
        )
        card_layout.addWidget(desc_lbl)

        card_layout.addStretch()

        # Stats Row
        if runs is not None:
            stats_row = QHBoxLayout()

            # Runs Badge - Circled and subtle
            runs_lbl = QLabel(str(runs))
            runs_lbl.setToolTip(f"Esecuzioni: {runs}")
            runs_lbl.setFixedSize(24, 24)
            runs_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            runs_lbl.setStyleSheet(
                """
                background-color: #e9ecef;
                color: #495057;
                border-radius: 12px;
                font-size: 10px;
                font-weight: bold;
                border: none;
            """
            )
            stats_row.addWidget(runs_lbl)

            if errors is not None and errors > 0:
                err_lbl = QLabel(str(errors))
                err_lbl.setToolTip(f"Errori: {errors}")
                err_lbl.setFixedSize(24, 24)
                err_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                err_lbl.setStyleSheet(
                    """
                    background-color: #f8d7da;
                    color: #721c24;
                    border-radius: 12px;
                    font-size: 10px;
                    font-weight: bold;
                    border: none;
                """
                )
                stats_row.addWidget(err_lbl)

            stats_row.addStretch()

            # Action Arrow
            arrow_lbl = QLabel()
            arrow_lbl.setPixmap(
                get_colored_icon(get_asset_path(Icons.PLAY), color).pixmap(16, 16)
            )
            arrow_lbl.setStyleSheet("border: none; background: transparent;")
            stats_row.addWidget(arrow_lbl)

            card_layout.addLayout(stats_row)
        else:
            # For Databases (No stats), just show arrow at bottom right
            stats_row = QHBoxLayout()
            stats_row.addStretch()
            arrow_lbl = QLabel()
            arrow_lbl.setPixmap(
                get_colored_icon(get_asset_path(Icons.PLAY), color).pixmap(16, 16)
            )
            arrow_lbl.setStyleSheet("border: none; background: transparent;")
            stats_row.addWidget(arrow_lbl)
            card_layout.addLayout(stats_row)

        # Full Card Click Button Overlay
        card.set_click_callback(lambda: self._navigate_to(action_key))

        return card

    def _navigate_to(self, key):
        """Naviga alla tab specificata."""
        main_window = self.window()
        if hasattr(main_window, "navigate_to_panel"):
            main_window.navigate_to_panel(key)
