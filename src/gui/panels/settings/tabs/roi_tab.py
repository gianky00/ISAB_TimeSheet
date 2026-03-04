"""
SyncroJob - ROI Settings Tab
Pannello per la configurazione dei pesi ROI (minuti manuali stimati).
Consente all'utente di definire quanto tempo risparmia ogni singola operazione bot.
"""

from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QSpinBox,
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

        # Dictionary per conservare i widget di input (min e sec per ogni task)
        self.task_inputs: dict[str, dict[str, QSpinBox]] = {}

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
            # Layout orizzontale per ospitare minuti e secondi
            input_layout = QHBoxLayout()
            input_layout.setSpacing(10)

            # Campo Minuti
            spin_min = QSpinBox()
            spin_min.setRange(0, 120)
            spin_min.setFixedWidth(60)
            spin_min.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
            spin_min.setAlignment(Qt.AlignmentFlag.AlignCenter)
            spin_min.setStyleSheet(self._get_input_style())
            spin_min.valueChanged.connect(lambda _: self.settings_changed.emit())

            # Campo Secondi
            spin_sec = QSpinBox()
            spin_sec.setRange(0, 59)
            spin_sec.setFixedWidth(60)
            spin_sec.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
            spin_sec.setAlignment(Qt.AlignmentFlag.AlignCenter)
            spin_sec.setStyleSheet(self._get_input_style())
            spin_sec.valueChanged.connect(lambda _: self.settings_changed.emit())

            # Label separatrici
            lbl_min = QLabel("min")
            lbl_min.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 700;")
            lbl_sec = QLabel("sec")
            lbl_sec.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 700;")

            input_layout.addWidget(spin_min)
            input_layout.addWidget(lbl_min)
            input_layout.addWidget(spin_sec)
            input_layout.addWidget(lbl_sec)
            input_layout.addStretch()

            label = QLabel(f"Tempo per {task}:")
            label.setStyleSheet(f"font-weight: 600; color: {COLORS['text_dark']};")

            self.form_layout.addRow(label, input_layout)
            self.task_inputs[task] = {"min": spin_min, "sec": spin_sec}

        self.layout.addWidget(self.form_container)
        self.layout.addStretch()

    def _get_input_style(self) -> str:
        """Ritorna lo stile CSS per i campi di input numerici senza pulsanti."""
        return f"""
            QSpinBox {{
                padding: 5px;
                border: 1px solid {COLORS['border_light']};
                border-radius: 6px;
                background: {COLORS['bg_white']};
                color: {COLORS['text_dark']};
                font-weight: 800;
                font-size: 12px;
            }}
            QSpinBox:focus {{
                border: 1.5px solid {COLORS['primary_blue']};
                background: #FFFFFF;
            }}
        """

    def load_from_config(self, config: dict[str, Any]) -> None:
        weights = config.get("roi_weights", {})
        for task, inputs in self.task_inputs.items():
            val = float(weights.get(task, 5.0))  # Default in minuti decimali
            
            minutes = int(val)
            seconds = int(round((val - minutes) * 60))
            
            # Gestione arrotondamento (es. 5.999 -> 6.0)
            if seconds >= 60:
                minutes += 1
                seconds = 0

            inputs["min"].blockSignals(True)
            inputs["sec"].blockSignals(True)
            inputs["min"].setValue(minutes)
            inputs["sec"].setValue(seconds)
            inputs["min"].blockSignals(False)
            inputs["sec"].blockSignals(False)

    def save_to_config(self, config: dict[str, Any]) -> None:
        weights = {}
        for task, inputs in self.task_inputs.items():
            mins = inputs["min"].value()
            secs = inputs["sec"].value()
            # Converte tutto in minuti decimali per ROIEngine
            weights[task] = mins + (secs / 60.0)
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

        # Header bar
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
            "Definisci minuti e secondi che un operatore impiegherebbe per ogni task.",
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
        self.weights_page.save_to_config(config)
