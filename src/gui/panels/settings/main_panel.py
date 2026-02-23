"""
SyncroJob - Settings Main Panel
Pannello centralizzato per la configurazione dell'applicazione.
Organizza le impostazioni in tab tematici: Configurazione, Backup, Statistiche e Telegram.
Gestisce il salvataggio automatico con debounce e l'import/export delle preferenze.
"""

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
    """
    Pannello principale delle impostazioni.
    Coordina i diversi moduli di configurazione e garantisce la persistenza dei dati.
    Supporta il monitoraggio dei cambiamenti non salvati e l'integrazione con la guida contestuale.
    """

    unsaved_changes = pyqtSignal(bool)
    """Segnale emesso quando lo stato delle modifiche cambia (True se ci sono modifiche pendenti)."""

    settings_saved = pyqtSignal()
    """Segnale emesso a conferma del completamento del salvataggio su disco."""

    request_help_section = pyqtSignal(str)
    """Segnale emesso per richiedere l'apertura di una specifica sezione della guida."""

    def __init__(self, parent=None):
        """
        Inizializza il pannello impostazioni e configura il timer di autosave.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._has_unsaved_changes = False

        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.setInterval(800)
        self.save_timer.timeout.connect(self._save_settings)

        self._setup_ui()
        self.load_settings()
        self._has_unsaved_changes = False

    def _setup_ui(self):
        """Costruisce l'interfaccia a schede e i pulsanti di manutenzione (Export/Import)."""
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
            self.backup_tab, get_colored_icon(get_asset_path(Icons.CLOUD), "#546E7A"), "Backup Cloud"
        )

        # 3. Statistiche
        self.stats_widget = StatisticsWidget()
        self.tabs.addTab(
            self.stats_widget, get_colored_icon(get_asset_path(Icons.ROCKET), "#546E7A"), "Statistiche"
        )

        # 4. Telegram
        self.telegram_tab = TelegramTab()
        self.telegram_tab.settings_changed.connect(self._on_settings_changed)
        self.telegram_tab.request_help.connect(self.request_help_section.emit)
        self.tabs.addTab(
            self.telegram_tab, get_colored_icon(get_asset_path(Icons.SEND), "#546E7A"), "Telegram"
        )

        self.tabs.currentChanged.connect(self._on_tab_changed)
        main_layout.addWidget(self.tabs)

        # Footer
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
        """Aggiorna i widget dinamici (es. statistiche) al cambio di tab."""
        if self.tabs.tabText(index) == "Statistiche":
            self.stats_widget.refresh()

    def _on_settings_changed(self):
        """Reagisce alla modifica di un valore attivando il timer per il salvataggio differito."""
        self._has_unsaved_changes = True
        self.unsaved_changes.emit(True)
        self.save_timer.start()

    def _save_settings(self):
        """Persiste tutte le impostazioni correnti nel file di configurazione globale."""
        try:
            self.config_tab.save_to_config(config_manager)
            self.telegram_tab.save_to_config(config_manager)
            self.backup_tab._save_auto_backup()

            self._has_unsaved_changes = False
            self.unsaved_changes.emit(False)
            self.settings_saved.emit()
        except Exception as e:
            print(f"Errore salvataggio impostazioni: {e}")

    def load_settings(self):
        """Carica lo stato corrente dei widget leggendo la configurazione da disco."""
        config = config_manager.load_config()
        self.config_tab.load_from_config(config)
        self.backup_tab.load_from_config(config)
        self.telegram_tab.load_from_config(config)

    def has_unsaved_changes(self) -> bool:
        """Restituisce True se ci sono modifiche non ancora persistite."""
        return self._has_unsaved_changes

    def prompt_save_if_needed(self) -> bool:
        """Esegue un salvataggio forzato se ci sono modifiche pendenti."""
        if self._has_unsaved_changes:
            self._save_settings()
        return True

    def _export_settings(self):
        """Apre un dialogo per esportare l'intera configurazione JSON in un file esterno."""
        from PyQt6.QtWidgets import QFileDialog

        path, _ = QFileDialog.getSaveFileName(
            self, "Esporta Configurazione", "SyncroJob_Config.json", "JSON Files (*.json)"
        )
        if path:
            success, msg = config_manager.export_configuration(path)
            if success:
                ToastManager.instance().show("Configurazione esportata!", "success")
            else:
                ToastManager.instance().show(f"Errore export: {msg}", "error")

    def _import_settings(self):
        """Importa una configurazione JSON da file, sovrascrivendo quella attuale previa conferma."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        path, _ = QFileDialog.getOpenFileName(self, "Importa Configurazione", "", "JSON Files (*.json)")
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
