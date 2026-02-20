"""
SyncroJob - Backup Tab
Interfaccia per la gestione della sicurezza dei dati tramite backup Cloud e locali.
Permette il rilevamento automatico di servizi come OneDrive/Google Drive e il ripristino di versioni precedenti.
"""

from datetime import UTC, datetime
from typing import Any

from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.backup_manager import BackupManager
from src.core.constants import Icons
from src.gui.panels.settings.shared import (
    create_group_box,
    style_button,
    style_mini_button,
)
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon, open_folder


class BackupTab(QWidget):
    """
    Tab dedicato alla configurazione del salvataggio dati.
    Gestisce la selezione del provider cloud, la schedulazione del backup automatico
    alla chiusura e fornisce strumenti per il ripristino atomico dei database.
    """

    def __init__(self, parent=None):
        """
        Inizializza il tab dei backup.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Configura l'interfaccia utente con sezioni per destinazione, opzioni e ripristino."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        info = QLabel("Salvataggio Dati in Cloud")
        info.setStyleSheet("font-size: 20px; font-weight: bold; color: #212529;")
        layout.addWidget(info)

        desc = QLabel(
            "Il sistema rileva automaticamente OneDrive, Google Drive, Dropbox o MEGA per salvare i tuoi dati al sicuro."
        )
        desc.setStyleSheet("color: #6c757d; font-size: 14px;")
        layout.addWidget(desc)

        # Detection Status & Selection
        clouds = BackupManager.detect_cloud_paths()
        status_group = QGroupBox("Destinazione Cloud")
        status_layout = QVBoxLayout(status_group)
        status_layout.addWidget(QLabel("Seleziona il servizio Cloud da utilizzare:"))

        self.cloud_combo = QComboBox()
        self.cloud_combo.setMinimumHeight(40)
        self.cloud_combo.setStyleSheet("QComboBox { border: 1px solid #ced4da; border-radius: 4px; padding: 5px; background-color: white; }")
        self.cloud_combo.addItem("Locale (Documenti)", "Local")
        if clouds:
            for name, path in clouds.items():
                self.cloud_combo.addItem(f"{name} ({path})", name)

        self.cloud_combo.currentIndexChanged.connect(self._save_cloud_preference)
        status_layout.addWidget(self.cloud_combo)
        layout.addWidget(status_group)

        # Settings & Actions
        sett_group = QGroupBox("Impostazioni")
        sett_layout = QHBoxLayout(sett_group)
        sett_layout.setSpacing(15)

        self.auto_backup_check = QCheckBox("Esegui backup automatico alla chiusura")
        self.auto_backup_check.stateChanged.connect(self._save_auto_backup)
        sett_layout.addWidget(self.auto_backup_check)

        sett_layout.addStretch()

        backup_btn = QPushButton("  Esegui Backup Ora")
        backup_btn.setIcon(get_colored_icon(get_asset_path(Icons.CLOUD_UPLOAD), "#000000"))
        backup_btn.clicked.connect(self._run_manual_backup)
        style_button(backup_btn)
        sett_layout.addWidget(backup_btn)

        open_folder_btn = QPushButton("  Apri Cartella Backup")
        open_folder_btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER), "#000000"))
        open_folder_btn.clicked.connect(self._open_backup_folder)
        style_button(open_folder_btn)
        sett_layout.addWidget(open_folder_btn)

        layout.addWidget(sett_group)

        # Restore Section
        restore_group = create_group_box("Ripristino Backup")
        restore_layout = QVBoxLayout(restore_group)
        restore_layout.addWidget(QLabel("Seleziona un backup da ripristinare:"))

        restore_controls = QHBoxLayout()
        self.restore_combo = QComboBox()
        self.restore_combo.setMinimumHeight(40)
        self.restore_combo.setStyleSheet("QComboBox { border: 1px solid #ced4da; border-radius: 4px; padding: 5px; background-color: white; }")
        restore_controls.addWidget(self.restore_combo)

        self.refresh_backups_btn = QPushButton()
        self.refresh_backups_btn.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), "#000000"))
        self.refresh_backups_btn.setToolTip("Aggiorna lista backup")
        self.refresh_backups_btn.clicked.connect(self._refresh_backups_list)
        style_mini_button(self.refresh_backups_btn, "#6c757d")
        restore_controls.addWidget(self.refresh_backups_btn)

        self.restore_btn = QPushButton("  Ripristina")
        self.restore_btn.setIcon(get_colored_icon(get_asset_path(Icons.UNDO), "#000000"))
        self.restore_btn.clicked.connect(self._restore_selected_backup)
        style_button(self.restore_btn)
        restore_controls.addWidget(self.restore_btn)

        restore_layout.addLayout(restore_controls)
        layout.addWidget(restore_group)
        layout.addStretch()

    def load_from_config(self, config: dict[str, Any]):
        """
        Carica le preferenze di backup dalla configurazione globale.

        Args:
            config: Dizionario delle impostazioni caricato.
        """
        saved_cloud = config.get("backup_cloud_provider")
        if saved_cloud:
            index = self.cloud_combo.findData(saved_cloud)
            if index >= 0:
                self.cloud_combo.setCurrentIndex(index)

        self.auto_backup_check.setChecked(config.get("auto_backup", True))
        self._refresh_backups_list()

    def _save_cloud_preference(self):
        """Salva il provider cloud selezionato nella configurazione."""
        provider = self.cloud_combo.currentData()
        if provider:
            config_manager.set_config_value("backup_cloud_provider", provider)

    def _save_auto_backup(self):
        """Salva lo stato dell'opzione di backup automatico."""
        config_manager.set_config_value("auto_backup", self.auto_backup_check.isChecked())

    def _run_manual_backup(self):
        """Avvia immediatamente la procedura di backup e aggiorna la lista cronologica."""
        success, msg = BackupManager.create_backup()
        if success:
            ToastManager.instance().show(f"Backup completato!\n{msg}", "success")
            self._refresh_backups_list()
        else:
            QMessageBox.warning(self, "Errore Backup", msg)

    def _open_backup_folder(self):
        """Apre la cartella contenente i file ZIP di backup nel file explorer di sistema."""
        path = BackupManager.get_backup_dir()
        open_folder(str(path))

    def _refresh_backups_list(self):
        """Scansiona la cartella backup e popola il menu a tendina con le versioni trovate."""
        self.restore_combo.clear()
        backups = BackupManager.list_backups()

        if not backups:
            self.restore_combo.addItem("Nessun backup trovato")
            self.restore_btn.setEnabled(False)
            return

        self.restore_btn.setEnabled(True)
        for backup_path in backups:
            try:
                name = backup_path.name
                ts_str = name.replace("BotTS_Backup_", "").replace(".zip", "")
                dt = datetime.strptime(ts_str, "%Y%m%d_%H%M%S").replace(tzinfo=UTC)
                display = f"{dt.strftime('%d/%m/%Y %H:%M:%S')} ({backup_path.stat().st_size // 1024} KB)"
                self.restore_combo.addItem(display, str(backup_path))
            except Exception:
                self.restore_combo.addItem(backup_path.name, str(backup_path))

    def _restore_selected_backup(self):
        """Ripristina i dati dal file selezionato previa conferma dell'utente."""
        path = self.restore_combo.currentData()
        if not path:
            return

        res = QMessageBox.question(self, "Conferma Ripristino", "ATTENZIONE: Il ripristino sovrascriverà i dati attuali.\nProcedere?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if res == QMessageBox.StandardButton.Yes:
            success, msg = BackupManager.restore_backup(path)
            if success:
                QMessageBox.information(self, "Ripristino Completato", "Dati ripristinati con successo. Riavvia l'app.")
            else:
                QMessageBox.critical(self, "Errore Ripristino", msg)
