from typing import Any

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import URLs
from src.core.secrets_manager import SecretsManager
from src.gui.panels.lyra.workers import ModelListWorker
from src.gui.panels.settings.shared import create_group_box, style_button, style_input
from src.gui.styles import COLORS


class GeneralPage(QWidget):
    """Pagina impostazioni generali e browser."""

    settings_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.model_worker: ModelListWorker | None = None
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
            f"QCheckBox {{ padding: 5px; font-size: 15px; font-weight: bold; color: {COLORS['magenta_pink']}; }}"
        )
        self.headless_check.stateChanged.connect(self.settings_changed.emit)
        gen_layout.addWidget(self.headless_check)
        layout.addWidget(self.general_group)

        # AI Group
        self.ai_group = create_group_box("Intelligenza Artificiale (Lyra AI)")
        ai_layout = QVBoxLayout(self.ai_group)

        # Provider
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("AI Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["gemini", "ollama"])
        self.provider_combo.setMinimumHeight(40)
        style_input(self.provider_combo)
        self.provider_combo.currentTextChanged.connect(self.settings_changed.emit)
        self.provider_combo.currentTextChanged.connect(self._on_provider_changed)
        provider_layout.addWidget(self.provider_combo)
        ai_layout.addLayout(provider_layout)

        # Ollama URL
        self.ollama_url_container = QWidget()
        ollama_url_layout = QHBoxLayout(self.ollama_url_container)
        ollama_url_layout.setContentsMargins(0, 0, 0, 0)
        ollama_url_layout.addWidget(QLabel("Ollama Server URL:"))
        self.ollama_url_edit = QLineEdit()
        self.ollama_url_edit.setPlaceholderText(URLs.OLLAMA_DEFAULT)
        self.ollama_url_edit.setMinimumHeight(40)
        style_input(self.ollama_url_edit)
        self.ollama_url_edit.textChanged.connect(self.settings_changed.emit)
        ollama_url_layout.addWidget(self.ollama_url_edit)
        ai_layout.addWidget(self.ollama_url_container)

        # Model Selection with Refresh
        model_container = QHBoxLayout()
        model_container.addWidget(QLabel("Modello AI:"))

        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)  # Permette inserimento manuale se fetch fallisce
        self.model_combo.setMinimumHeight(40)
        self.model_combo.setMinimumWidth(200)
        style_input(self.model_combo)
        self.model_combo.currentTextChanged.connect(self.settings_changed.emit)
        model_container.addWidget(self.model_combo, 1)

        self.btn_refresh_models = QPushButton("Aggiorna Lista")
        self.btn_refresh_models.setMinimumHeight(40)
        style_button(self.btn_refresh_models)
        self.btn_refresh_models.clicked.connect(self.refresh_models)
        model_container.addWidget(self.btn_refresh_models)

        ai_layout.addLayout(model_container)

        layout.addWidget(self.ai_group)

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

    def _on_provider_changed(self, provider: str) -> None:
        """Mostra/nasconde impostazioni specifiche e resetta i modelli."""
        self.ollama_url_container.setVisible(provider == "ollama")
        # Trigger automatico refresh quando cambia il provider
        QTimer.singleShot(500, self.refresh_models)

    def refresh_models(self):
        """Avvia il worker per recuperare i modelli in base al provider e config attuale."""
        if self.model_worker and self.model_worker.isRunning():
            return

        self.btn_refresh_models.setEnabled(False)
        self.btn_refresh_models.setText("Recupero...")

        provider = self.provider_combo.currentText()
        ollama_url = self.ollama_url_edit.text()
        api_key = SecretsManager.get_gemini_api_key()

        self.model_worker = ModelListWorker(api_key, provider=provider, ollama_url=ollama_url)
        self.model_worker.finished.connect(self._on_models_fetched)
        self.model_worker.start()

    def _on_models_fetched(self, models: list[str]):
        current_model = self.model_combo.currentText()
        self.model_combo.clear()
        if models:
            self.model_combo.addItems(sorted(models))
            if current_model in models:
                self.model_combo.setCurrentText(current_model)

        self.btn_refresh_models.setEnabled(True)
        self.btn_refresh_models.setText("Aggiorna Lista")

    def load_from_config(self, config: dict[str, Any]) -> None:
        """Carica i valori dalla configurazione."""
        self.headless_check.setChecked(bool(config.get("browser_headless", False)))
        self.timeout_spin.setValue(int(config.get("browser_timeout", 30)))

        # AI
        provider = config.get("ai_provider", "gemini")
        self.provider_combo.setCurrentText(provider)
        self.ollama_url_edit.setText(config.get("ollama_url", URLs.OLLAMA_DEFAULT))

        # Carichiamo il modello (se non c'è nella lista, il combo essendo editable lo mostrerà comunque)
        self.model_combo.setEditText(config.get("ai_model", ""))

        self._on_provider_changed(provider)

    def save_to_config(self, config_manager: Any) -> None:
        """Salva i valori nella configurazione."""
        config_manager.set_config_value("browser_headless", self.headless_check.isChecked())
        config_manager.set_config_value("browser_timeout", self.timeout_spin.value())

        # AI
        config_manager.set_config_value("ai_provider", self.provider_combo.currentText())
        config_manager.set_config_value("ai_model", self.model_combo.currentText())
        config_manager.set_config_value("ollama_url", self.ollama_url_edit.text())
