"""
SyncroJob - Settings Main Panel
Pannello centralizzato per la configurazione dell'applicazione.
Organizza le impostazioni in tab tematici: Configurazione, Backup, Statistiche e Telegram.
Gestisce il salvataggio automatico e l'import/export della configurazione.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PyQt6.QtCore import QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from src.core import config_manager
from src.core.constants import Icons
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.panels.settings.shared import style_button
from src.gui.panels.settings.tabs.backup_tab import BackupTab
from src.gui.panels.settings.tabs.config_tab import ConfigTab
from src.gui.panels.settings.tabs.roi_tab import ROITab
from src.gui.panels.settings.tabs.telegram_tab import TelegramTab
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    PrimaryButton,
)
from src.gui.widgets.toast import ToastManager, toast_error
from src.utils.helpers import get_asset_path, get_colored_icon


class ConfigSaveWorker(QThread):
    """Worker thread per il salvataggio asincrono della configurazione."""

    finished = pyqtSignal(bool, str)

    def __init__(self, config: dict[str, Any]) -> None:
        """Inizializza il worker comunicando la configurazione da salvare."""
        super().__init__()
        self.config = config

    def run(self) -> None:
        try:
            config_manager.save_config(self.config)
            self.finished.emit(True, "")
        except Exception as e:
            self.finished.emit(False, str(e))


class SettingsPanel(QWidget):
    """
    Pannello principale delle impostazioni.
    Coordina i diversi tab di configurazione e fornisce funzionalità di sistema come reset e import/export.
    """

    settings_saved = pyqtSignal()
    """Segnale emesso dopo il salvataggio avvenuto con successo."""

    request_help_section = pyqtSignal(str)
    """Segnale per richiedere l'apertura di una sezione specifica della guida."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello impostazioni.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._is_loading = False
        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(500)  # 500ms debounce
        self._save_timer.timeout.connect(self._execute_async_save)
        self._save_worker: ConfigSaveWorker | None = None

        # UI Elements
        self.tabs: AnimatedTabWidget
        self.config_tab: ConfigTab
        self.roi_tab: ROITab
        self.backup_tab: BackupTab
        self.telegram_tab: TelegramTab
        self.btn_import: PrimaryButton
        self.btn_export: PrimaryButton
        self.btn_reset: PrimaryButton

        self._setup_ui()
        QTimer.singleShot(50, self.load_settings)

    def _setup_ui(self) -> None:
        """Configura il layout principale e inizializza i tab tematici."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.tabs = AnimatedTabWidget()

        # 1. Configurazione
        self.config_tab = ConfigTab()
        self.config_tab.settings_changed.connect(self.save_settings)
        self.tabs.addTab(
            self.config_tab,
            get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), COLORS["text_muted"]),
            "Configurazione",
        )

        # 2. Efficienza & ROI
        self.roi_tab = ROITab()
        self.roi_tab.settings_changed.connect(self.save_settings)
        self.tabs.addTab(
            self.roi_tab,
            get_colored_icon(get_asset_path(Icons.CLOCK), COLORS["text_muted"]),
            "Efficienza & ROI",
        )

        # 3. Backup e Manutenzione
        self.backup_tab = BackupTab()
        self.tabs.addTab(
            self.backup_tab,
            get_colored_icon(get_asset_path(Icons.DATABASE), COLORS["text_muted"]),
            "Backup & Log",
        )

        # 3. Telegram
        self.telegram_tab = TelegramTab()
        self.telegram_tab.settings_changed.connect(self.save_settings)
        self.tabs.addTab(
            self.telegram_tab,
            get_colored_icon(get_asset_path(Icons.SEND), COLORS["text_muted"]),
            "Telegram Bot",
        )

        main_layout.addWidget(self.tabs)

        # Barra Azioni Inferiore
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(10, 0, 10, 10)

        self.btn_import = PrimaryButton("Importa Config")
        self.btn_export = PrimaryButton("Esporta Config")
        self.btn_reset = PrimaryButton("Reset Fabbrica")

        style_button(self.btn_import)
        style_button(self.btn_export)
        style_button(self.btn_reset)

        # Sovrascrive il colore del reset essendo un'azione distruttiva
        self.btn_reset.setStyleSheet(
            self.btn_reset.styleSheet()
            + f"QPushButton {{ color: {COLORS['error_material']}; border-color: {COLORS['error_material']}; }}"
        )

        self.btn_import.clicked.connect(self._import_config)
        self.btn_export.clicked.connect(self._export_config)
        self.btn_reset.clicked.connect(self._reset_to_defaults)

        actions_layout.addWidget(self.btn_import)
        actions_layout.addWidget(self.btn_export)
        actions_layout.addStretch()
        actions_layout.addWidget(self.btn_reset)

        main_layout.addLayout(actions_layout)

    def load_settings(self) -> None:
        """Carica la configurazione attuale e aggiorna tutti i tab."""
        self._is_loading = True
        try:
            config = config_manager.load_config()
            self.config_tab.load_from_config(config)
            self.roi_tab.load_from_config(config)
            self.backup_tab.load_from_config(config)
            self.telegram_tab.load_from_config(config)
        finally:
            self._is_loading = False

    def save_settings(self) -> None:
        """Innesca il salvataggio con debouncing."""
        if self._is_loading:
            return
        self._save_timer.start()

    def _execute_async_save(self) -> None:
        """Raccoglie i dati e avvia il thread di salvataggio."""
        # Se c'è già un salvataggio in corso, lo ignoriamo per ora
        # Il debouncing gestisce la maggior parte dei casi.
        if self._save_worker and self._save_worker.isRunning():
            self._save_timer.start()  # Ritenta tra poco
            return

        config = config_manager.load_config()
        self.config_tab.save_to_config(config)
        self.roi_tab.save_to_config(config)
        self.telegram_tab.save_to_config(config)

        self._save_worker = ConfigSaveWorker(config)
        self._save_worker.finished.connect(self._on_save_finished)
        self._save_worker.start()

    def _on_save_finished(self, success: bool, error_msg: str) -> None:
        """Gestisce l'esito del salvataggio asincrono."""
        if success:
            self.settings_saved.emit()
        else:
            toast_error(f"Errore durante il salvataggio: {error_msg}")

    def has_unsaved_changes(self) -> bool:
        """Placeholder per la logica di rilevamento modifiche pendenti."""
        return False

    def prompt_save_if_needed(self) -> bool:
        """Sempre True per ora, dato che il salvataggio è automatico tramite segnali."""
        return True

    def _reset_to_defaults(self) -> None:
        """Ripristina la configurazione predefinita previa conferma."""
        from src.gui.dialogs.confirmation_dialog import ConfirmationDialog  # noqa: PLC0415

        if ConfirmationDialog.confirm(
            self,
            "Reset Totale",
            "Sei sicuro di voler ripristinare le impostazioni di fabbrica?\nTutti i dati verranno persi.",
        ):
            config_manager.reset_to_defaults()
            self.load_settings()
            ToastManager.instance().show("Sistema resettato!", "success")

    def _export_config(self) -> None:
        """Esporta il file di configurazione JSON in una posizione scelta dall'utente."""
        from PyQt6.QtWidgets import QFileDialog  # noqa: PLC0415

        path, _ = QFileDialog.getSaveFileName(
            self, "Esporta Configurazione", "config_backup.json", "JSON Files (*.json)"
        )
        if path:
            import shutil  # noqa: PLC0415

            try:
                shutil.copy(config_manager.CONFIG_FILE, path)
                ToastManager.instance().show("Configurazione esportata!", "success")
            except Exception as e:
                ToastManager.instance().show(f"Errore export: {e}", "error")

    def _import_config(self) -> None:
        """Importa un file di configurazione JSON esterno."""
        from PyQt6.QtWidgets import QFileDialog  # noqa: PLC0415

        path, _ = QFileDialog.getOpenFileName(self, "Importa Configurazione", "", "JSON Files (*.json)")
        if path:
            success, msg = config_manager.import_config_from_file(Path(path))
            if success:
                ToastManager.instance().show("Configurazione importata!", "success")
                self.load_settings()
            else:
                ToastManager.instance().show(f"Errore import: {msg}", "error")
