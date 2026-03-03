"""
SyncroJob - ROI Settings Tab
Pannello per la configurazione dei pesi ROI (minuti manuali stimati).
Consente all'utente di definire quanto tempo risparmia ogni singola operazione bot.
"""

from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.panels.settings.tabs.config_tab import SettingCard
from src.gui.styles import COLORS


class ROIWeightsPage(QWidget):
    """Pagina di dettaglio per l'editing dei pesi ROI."""

    settings_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 10, 0, 10)
        self.layout.setSpacing(15)

        # Container per il form
        self.form_container = QFrame()
        self.form_container.setStyleSheet("background: transparent; border: none;")
        self.form_layout = QFormLayout(self.form_container)
        self.form_layout.setSpacing(12)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.spinners: dict[str, QDoubleSpinBox] = {}

        # Definizione dei task standard (quelli usati in ROIEngine)
        self.tasks = [
            "Scarico TS",
            "Carico TS",
            "Dettagli ODA",
            "Prenota BP",
            "Scarico PDL",
            "Ricerca PDL",
            "Sincronizzazione",
            "Export Excel"
        ]

        for task in self.tasks:
            spinner = QDoubleSpinBox()
            spinner.setRange(0.1, 120.0)
            spinner.setSuffix(" min")
            spinner.setSingleStep(0.5)
            spinner.setDecimals(1)
            spinner.setFixedWidth(100)
            spinner.setStyleSheet(f"""
                QDoubleSpinBox {{
                    padding: 5px;
                    border: 1px solid {COLORS['border_light']};
                    border-radius: 6px;
                    background: {COLORS['bg_white']};
                    font-weight: 700;
                }}
            """)
            spinner.valueChanged.connect(lambda _: self.settings_changed.emit())

            label = QLabel(f"Tempo per {task}:")
            label.setStyleSheet(f"font-weight: 600; color: {COLORS['text_dark']};")

            self.form_layout.addRow(label, spinner)
            self.spinners[task] = spinner

        self.layout.addWidget(self.form_container)
        self.layout.addStretch()

    def load_from_config(self, config: dict[str, Any]) -> None:
        weights = config.get("roi_weights", {})
        for task, spinner in self.spinners.items():
            val = weights.get(task, 5.0)  # Default fallbacks
            spinner.blockSignals(True)
            spinner.setValue(float(val))
            spinner.blockSignals(False)

    def save_to_config(self, config: dict[str, Any]) -> None:
        weights = {}
        for task, spinner in self.spinners.items():
            weights[task] = spinner.value()
        config["roi_weights"] = weights


class ROITab(QWidget):
    """Tab per la gestione dell'Efficienza (ROI)."""

    settings_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header bar (placeholder for search if needed)
        self.header_bar = QFrame()
        self.header_bar.setFixedHeight(50)
        self.header_bar.setStyleSheet(
            f"background: {COLORS['bg_light']}; border-bottom: 1px solid {COLORS['border_light']};"
        )
        header_layout = QHBoxLayout(self.header_bar)
        header_layout.setContentsMargins(20, 0, 20, 0)

        title_lbl = QLabel("CONFIGURAZIONE ROI & EFFICIENZA")
        title_lbl.setStyleSheet(f"color: {COLORS['text_dark']}; font-weight: 800; font-size: 13px; letter-spacing: 1px;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()

        layout.addWidget(self.header_bar)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.cards_layout = QVBoxLayout(scroll_content)
        self.cards_layout.setContentsMargins(30, 30, 30, 30)
        self.cards_layout.setSpacing(30)

        # Card: Pesi Manuali
        self.weights_page = ROIWeightsPage()
        self.weights_page.settings_changed.connect(self.settings_changed.emit)

        card_weights = SettingCard(
            "Stima Tempi Manuali",
            "Definisci i minuti che un operatore impiegherebbe per ogni task.",
            Icons.CLOCK,
            self.weights_page
        )
        self.cards_layout.addWidget(card_weights)

        self.cards_layout.addStretch()
        self.scroll.setWidget(scroll_content)
        layout.addWidget(self.scroll)

    def load_from_config(self, config: dict[str, Any]) -> None:
        self.weights_page.load_from_config(config)

    def save_to_config(self, config: dict[str, Any]) -> None:
        """Note: In this project architecture, saving is often handled by the main panel."""
        self.weights_page.save_to_config(config)
