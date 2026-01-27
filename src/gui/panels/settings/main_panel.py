from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QWidget

from src.core import config_manager
from src.core.constants import Icons
from src.gui.panels.settings.shared import style_button
from src.gui.panels.settings.tabs.backup_tab import BackupTab
from src.gui.panels.settings.tabs.config_tab import ConfigTab
from src.gui.panels.settings.tabs.telegram_tab import TelegramTab
from src.gui.widgets.statistics_widget import StatisticsWidget
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon


class SettingsPanel(QWidget):
    """Pannello per le impostazioni dell'applicazione (Refactored)."""

    unsaved_changes = pyqtSignal(bool)
    settings_saved = pyqtSignal()
    request_help_section = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._has_unsaved_changes = False

        # Timer per Debounce Salvataggio
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.setInterval(800)
        self.save_timer.timeout.connect(self._save_settings)

        self._setup_ui()
        self.load_settings()
        self._has_unsaved_changes = False


    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.tabs = QTabWidget()
        self.tabs.setProperty("class", "Level2Tabs")

        # 1. Configurazione
        self.config_tab = ConfigTab()
        self.config_tab.settings_changed.connect(self._on_settings_changed)
        self.tabs.addTab(
            self.config_tab,
            get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), "#546E7A"),
            "Configurazione",
        )

        # 2. Backup
        self.backup_tab = BackupTab()
        self.tabs.addTab(
            self.backup_tab,
            get_colored_icon(get_asset_path(Icons.CLOUD), "#546E7A"),
            "Backup Cloud",
        )

        # 3. Statistiche
        self.stats_widget = StatisticsWidget()
        self.tabs.addTab(
            self.stats_widget,
            get_colored_icon(get_asset_path(Icons.ROCKET), "#546E7A"),
            "Statistiche",
        )

        # 4. Telegram
        self.telegram_tab = TelegramTab()
        self.telegram_tab.settings_changed.connect(self._on_settings_changed)
        self.telegram_tab.request_help.connect(self.request_help_section.emit)
        self.tabs.addTab(
            self.telegram_tab,
            get_colored_icon(get_asset_path(Icons.SEND), "#546E7A"),
            "Telegram",
        )

        self.tabs.currentChanged.connect(self._on_tab_changed)
        main_layout.addWidget(self.tabs)

        # Footer Actions (Import/Export)
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 10, 0, 0)

        export_btn = QPushButton("Esporta backup")
        export_btn.setIcon(get_colored_icon(get_asset_path(Icons.DOWNLOAD), "#000000"))
        export_btn.clicked.connect(self._export_settings)
        style_button(export_btn)
        footer_layout.addWidget(export_btn)

        import_btn = QPushButton("Importa backup")
        import_btn.setIcon(get_colored_icon(get_asset_path(Icons.UPLOAD), "#000000"))
        import_btn.clicked.connect(self._import_settings)
        style_button(import_btn)
        footer_layout.addWidget(import_btn)

        footer_layout.addStretch()
        main_layout.addLayout(footer_layout)

    def _on_tab_changed(self, index):
        if self.tabs.tabText(index) == "Statistiche":
            self.stats_widget.refresh()

    def _on_settings_changed(self):
        """Chiamato quando una qualsiasi impostazione cambia."""
        self._has_unsaved_changes = True
        self.unsaved_changes.emit(True)
        self.save_timer.start()  # Reset timer debounce

    def _save_settings(self):
        """Salva le impostazioni su disco."""
        try:
            self.config_tab.save_to_config(config_manager)
            self.telegram_tab.save_to_config(config_manager)
            self.backup_tab._save_auto_backup()  # Backup tab manages its own logic mostly, but check consistency

            # Persist changes
            # config_manager handles persistence internally usually via set_config_value calls immediately?
            # Or does it need a save() call?
            # In the original code, set_config_value writes to file. So we are good.

            self._has_unsaved_changes = False
            self.unsaved_changes.emit(False)
            self.settings_saved.emit()

            # Optional: Show unobtrusive toast?
            # ToastManager.instance().show("Salvataggio automatico...", "info", 1000)

        except Exception as e:
            print(f"Errore salvataggio impostazioni: {e}")

    def load_settings(self):
        config = config_manager.load_config()
        self.config_tab.load_from_config(config)
        self.backup_tab.load_from_config(config)
        self.telegram_tab.load_from_config(config)

    def has_unsaved_changes(self):
        return self._has_unsaved_changes

    def prompt_save_if_needed(self):
        """Se ci sono modifiche non salvate, chiede all'utente (usato alla chiusura)."""
        # Con autosave, questo serve meno, ma per sicurezza.
        if self._has_unsaved_changes:
            self._save_settings()
        return True

    def _export_settings(self):
        from PyQt6.QtWidgets import QFileDialog

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Esporta Configurazione",
            "SyncroJob_Config.json",
            "JSON Files (*.json)",
        )
        if path:
            success, msg = config_manager.export_configuration(path)
            if success:
                ToastManager.instance().show("Configurazione esportata!", "success")
            else:
                ToastManager.instance().show(f"Errore export: {msg}", "error")

    def _import_settings(self):
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        path, _ = QFileDialog.getOpenFileName(
            self, "Importa Configurazione", "", "JSON Files (*.json)"
        )
        if path:
            res = QMessageBox.warning(
                self,
                "Conferma",
                "L'importazione sovrascriverà le impostazioni attuali.\nContinuare?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if res == QMessageBox.StandardButton.Yes:
                success, msg = config_manager.import_configuration(path)
                if success:
                    ToastManager.instance().show("Configurazione importata!", "success")
                    self.load_settings()
                else:
                    ToastManager.instance().show(f"Errore import: {msg}", "error")
