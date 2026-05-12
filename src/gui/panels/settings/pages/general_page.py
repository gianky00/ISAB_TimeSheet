from typing import Any

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.gui.panels.settings.shared import create_group_box, style_input
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    StandardCheckBox,
    StandardSpinBox,
)


class GeneralPage(QWidget):
    """Pagina impostazioni generali e browser."""

    settings_changed = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Generale Group
        self.general_group = create_group_box("Generale")
        gen_layout = QVBoxLayout(self.general_group)

        # Motore di Automazione
        engine_layout = QHBoxLayout()
        engine_label = QLabel("Motore Automazione:")
        engine_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        engine_layout.addWidget(engine_label)

        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Selenium", "Playwright"])
        self.engine_combo.setMinimumHeight(40)
        self.engine_combo.setMinimumWidth(150)
        style_input(self.engine_combo)
        self.engine_combo.currentIndexChanged.connect(lambda: self.settings_changed.emit())
        engine_layout.addWidget(self.engine_combo)
        engine_layout.addStretch()
        gen_layout.addLayout(engine_layout)

        self.headless_check = StandardCheckBox("Nascondi browser dei bot")
        self.headless_check.setToolTip(
            "Se attivato, il browser verr  eseguito in background senza mostrare la finestra."
        )
        self.headless_check.setStyleSheet(
            f"QCheckBox {{ padding: 5px; font-size: 15px; font-weight: bold; color: {COLORS['magenta_pink']}; }}"
        )
        self.headless_check.stateChanged.connect(lambda: self.settings_changed.emit())
        gen_layout.addWidget(self.headless_check)
        layout.addWidget(self.general_group)

        # Browser Group
        self.browser_group = create_group_box("Impostazioni Browser")
        browser_layout = QVBoxLayout(self.browser_group)

        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Timeout (secondi):")
        timeout_label.setStyleSheet("font-size: 15px;")
        timeout_layout.addWidget(timeout_label)

        self.timeout_spin = StandardSpinBox()
        self.timeout_spin.setRange(10, 600)
        self.timeout_spin.setValue(300)
        self.timeout_spin.setMinimumHeight(40)
        self.timeout_spin.setMinimumWidth(100)
        style_input(self.timeout_spin)
        self.timeout_spin.valueChanged.connect(lambda: self.settings_changed.emit())

        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        browser_layout.addLayout(timeout_layout)
        layout.addWidget(self.browser_group)

        layout.addStretch()

    def load_from_config(self, config: dict[str, Any]) -> None:
        """Carica i valori dalla configurazione."""
        engine = config.get("automation_engine", "selenium").lower()
        index = 1 if engine == "playwright" else 0
        self.engine_combo.setCurrentIndex(index)

        self.headless_check.setChecked(bool(config.get("browser_headless", False)))
        self.timeout_spin.setValue(int(config.get("browser_timeout", 300)))

    def save_to_config(self, config: dict[str, Any]) -> None:
        """Salva i valori nel dizionario di configurazione."""
        config["automation_engine"] = self.engine_combo.currentText().lower()
        config["browser_headless"] = self.headless_check.isChecked()
        config["browser_timeout"] = self.timeout_spin.value()
