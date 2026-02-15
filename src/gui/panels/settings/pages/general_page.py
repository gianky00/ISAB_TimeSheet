from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.gui.panels.settings.shared import create_group_box, style_input


class GeneralPage(QWidget):
    """Pagina impostazioni generali e browser."""

    settings_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Generale Group
        self.general_group = create_group_box("Generale")
        gen_layout = QVBoxLayout(self.general_group)

        self.headless_check = QCheckBox("Nascondi browser dei bot")
        self.headless_check.setToolTip(
            "Se attivato, il browser verrà eseguito in background senza mostrare la finestra."
        )
        self.headless_check.setStyleSheet(
            "QCheckBox { padding: 5px; font-size: 15px; font-weight: bold; color: #d63384; }"
        )
        self.headless_check.stateChanged.connect(self.settings_changed.emit)
        gen_layout.addWidget(self.headless_check)
        layout.addWidget(self.general_group)

        # Browser Group
        self.browser_group = create_group_box("Impostazioni Browser")
        browser_layout = QVBoxLayout(self.browser_group)

        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Timeout (secondi):")
        timeout_label.setStyleSheet("font-size: 15px;")
        timeout_layout.addWidget(timeout_label)

        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(10, 120)
        self.timeout_spin.setValue(30)
        self.timeout_spin.setMinimumHeight(40)
        self.timeout_spin.setMinimumWidth(100)
        style_input(self.timeout_spin)
        self.timeout_spin.valueChanged.connect(self.settings_changed.emit)

        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        browser_layout.addLayout(timeout_layout)
        layout.addWidget(self.browser_group)

        layout.addStretch()

    def load_from_config(self, config: dict[str, Any]) -> None:
        """Carica i valori dalla configurazione."""
        self.headless_check.setChecked(bool(config.get("browser_headless", False)))
        self.timeout_spin.setValue(int(config.get("browser_timeout", 30)))

    def save_to_config(self, config_manager: Any) -> None:
        """Salva i valori nella configurazione."""
        config_manager.set_config_value("browser_headless", self.headless_check.isChecked())
        config_manager.set_config_value("browser_timeout", self.timeout_spin.value())
