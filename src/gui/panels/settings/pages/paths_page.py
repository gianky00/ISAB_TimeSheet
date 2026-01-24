from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QCheckBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.panels.settings.shared import create_group_box, style_button, style_input
from src.utils.helpers import get_asset_path, get_colored_icon


class PathsPage(QWidget):
    """Pagina per la gestione dei percorsi file."""

    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # --- SEZIONE STRUMENTALE ---
        contabilita_group = create_group_box("Strumentale")
        cont_layout = QVBoxLayout(contabilita_group)

        # Bilancio
        cont_layout.addWidget(QLabel("File bilancio strumentale:"))
        self.contabilita_path_edit = self._create_path_row(cont_layout, self._browse_contabilita)

        self.auto_update_check = QCheckBox("Attiva aggiornamento automatico all'avvio (background)")
        self.auto_update_check.setStyleSheet("padding: 5px; font-size: 15px;")
        self.auto_update_check.stateChanged.connect(self.settings_changed.emit)
        cont_layout.addWidget(self.auto_update_check)

        # Giornaliere
        cont_layout.addWidget(QLabel("Cartella Giornaliere (Root):"))
        self.giornaliere_path_edit = self._create_path_row(cont_layout, self._browse_giornaliere, folder=True)

        # Attività
        cont_layout.addWidget(QLabel("File Attività Programmate (Riepilogo):"))
        self.attivita_path_edit = self._create_path_row(cont_layout, self._browse_attivita)

        # Certificati
        cont_layout.addWidget(QLabel("File Certificati Campione:"))
        self.certificati_path_edit = self._create_path_row(cont_layout, self._browse_certificati)

        layout.addWidget(contabilita_group)

        # --- SEZIONE DATAEASE ---
        dataease_group = create_group_box("DataEase & Consuntivi")
        de_layout = QVBoxLayout(dataease_group)

        de_layout.addWidget(QLabel("Database DataEase (Access/MDB):"))
        self.dataease_path_edit = self._create_path_row(de_layout, self._browse_dataease)

        de_layout.addWidget(QLabel("Cartella Export Consuntivi:"))
        self.consuntivi_path_edit = self._create_path_row(de_layout, self._browse_consuntivi, folder=True)

        layout.addWidget(dataease_group)
        layout.addStretch()

    def _create_path_row(self, parent_layout, browse_cb, folder=False):
        row = QHBoxLayout()
        edit = QLineEdit()
        edit.setReadOnly(True)
        edit.setMinimumHeight(40)
        edit.setPlaceholderText("Seleziona cartella..." if folder else "Seleziona file...")
        style_input(edit)
        edit.textChanged.connect(self.settings_changed.emit)
        row.addWidget(edit)

        btn = QPushButton("Sfoglia")
        btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER_OPEN), "#000000"))
        btn.setMinimumHeight(40)
        btn.setMinimumWidth(120)
        style_button(btn)
        btn.clicked.connect(browse_cb)
        row.addWidget(btn)

        parent_layout.addLayout(row)
        return edit

    # --- BROWSE HANDLERS ---

    def _browse_file(self, title, filter_str):
        path, _ = QFileDialog.getOpenFileName(self, title, str(Path.home()), filter_str)
        return path

    def _browse_folder(self, title):
        return QFileDialog.getExistingDirectory(self, title, str(Path.home()))

    def _browse_contabilita(self):
        p = self._browse_file("Seleziona File Contabilità", "Excel Files (*.xlsx *.xlsm)")
        if p: self.contabilita_path_edit.setText(p)

    def _browse_giornaliere(self):
        p = self._browse_folder("Seleziona Cartella Giornaliere")
        if p: self.giornaliere_path_edit.setText(p)

    def _browse_attivita(self):
        p = self._browse_file("Seleziona File Attività", "Excel Files (*.xlsx *.xlsm)")
        if p: self.attivita_path_edit.setText(p)

    def _browse_certificati(self):
        p = self._browse_file("Seleziona File Certificati", "Excel Files (*.xlsx *.xlsm)")
        if p: self.certificati_path_edit.setText(p)

    def _browse_dataease(self):
        p = self._browse_file("Seleziona DB DataEase", "Access DB (*.mdb *.accdb)")
        if p: self.dataease_path_edit.setText(p)

    def _browse_consuntivi(self):
        p = self._browse_folder("Seleziona Cartella Consuntivi")
        if p: self.consuntivi_path_edit.setText(p)

    # --- LOAD & SAVE ---

    def load_from_config(self, config: dict):
        self.contabilita_path_edit.setText(config.get("contabilita_file_path", ""))
        self.auto_update_check.setChecked(config.get("enable_auto_update_contabilita", False))
        self.giornaliere_path_edit.setText(config.get("giornaliere_path", ""))
        self.attivita_path_edit.setText(config.get("attivita_programmate_path", ""))
        self.certificati_path_edit.setText(config.get("certificati_campione_path", ""))
        self.dataease_path_edit.setText(config.get("dataease_db_path", ""))
        self.consuntivi_path_edit.setText(config.get("consuntivi_export_path", ""))

    def save_to_config(self, config_manager):
        config_manager.set_config_value("contabilita_file_path", self.contabilita_path_edit.text())
        config_manager.set_config_value("enable_auto_update_contabilita", self.auto_update_check.isChecked())
        config_manager.set_config_value("giornaliere_path", self.giornaliere_path_edit.text())
        config_manager.set_config_value("attivita_programmate_path", self.attivita_path_edit.text())
        config_manager.set_config_value("certificati_campione_path", self.certificati_path_edit.text())
        config_manager.set_config_value("dataease_db_path", self.dataease_path_edit.text())
        config_manager.set_config_value("consuntivi_export_path", self.consuntivi_path_edit.text())
