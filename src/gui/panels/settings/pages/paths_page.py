from collections.abc import Callable
from pathlib import Path
from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.panels.settings.shared import create_group_box, style_button, style_input
from src.utils.helpers import get_asset_path, get_colored_icon


class PathsPage(QWidget):
    """Pagina per la gestione dei percorsi file."""

    settings_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
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

        # Database Report Attività
        cont_layout.addWidget(QLabel("Database Report Attività:"))
        self.activity_db_path_edit = self._create_path_row(cont_layout, self._browse_activity_db)

        # Certificati Excel
        cont_layout.addWidget(QLabel("File Certificati Campione (Excel):"))
        self.certificati_path_edit = self._create_path_row(cont_layout, self._browse_certificati)

        # Certificati PDF Root
        cont_layout.addWidget(QLabel("Cartella Certificati PDF (Root):"))
        self.certificati_root_edit = self._create_path_row(
            cont_layout, self._browse_certificati_root, folder=True
        )

        layout.addWidget(contabilita_group)

        # --- SEZIONE DATAEASE ---
        dataease_group = create_group_box("DataEase & Consuntivi")
        de_layout = QVBoxLayout(dataease_group)

        de_layout.addWidget(QLabel("Database DataEase (Access/MDB):"))
        self.dataease_path_edit = self._create_path_row(de_layout, self._browse_dataease)

        layout.addWidget(dataease_group)
        layout.addStretch()

    def _create_path_row(
        self, parent_layout: QLayout, browse_cb: Callable[[], None], folder: bool = False
    ) -> QLineEdit:
        row = QHBoxLayout()
        edit = QLineEdit()
        edit.setReadOnly(True)
        edit.setMinimumHeight(40)
        edit.setPlaceholderText("Seleziona cartella..." if folder else "Seleziona file...")
        style_input(edit)
        edit.textChanged.connect(self.settings_changed.emit)
        edit.textChanged.connect(lambda: self._validate_path(edit))
        row.addWidget(edit)

        btn = QPushButton("Sfoglia")
        btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER_OPEN), "#000000"))
        btn.setMinimumHeight(40)
        btn.setMinimumWidth(120)
        style_button(btn)
        btn.clicked.connect(browse_cb)
        row.addWidget(btn)

        if isinstance(parent_layout, (QVBoxLayout, QHBoxLayout)):
            parent_layout.addLayout(row)
        return edit

    def _validate_path(self, widget: QLineEdit) -> None:
        """Valida visivamente il percorso inserito."""
        path = widget.text().strip()
        if not path:
            style_input(widget)
            return

        p = Path(path)
        if p.exists():
            widget.setStyleSheet(
                """
                QLineEdit {
                    border: 2px solid #28a745;
                    border-radius: 4px;
                    padding: 10px;
                    font-size: 15px;
                    background-color: #e8f5e9;
                    color: #155724;
                }
                QLineEdit:focus { border-color: #28a745; }
            """
            )
        else:
            widget.setStyleSheet(
                """
                QLineEdit {
                    border: 2px solid #dc3545;
                    border-radius: 4px;
                    padding: 10px;
                    font-size: 15px;
                    background-color: #f8d7da;
                    color: #721c24;
                }
                QLineEdit:focus { border-color: #dc3545; }
            """
            )

    # --- BROWSE HANDLERS ---

    def _browse_file(self, title: str, filter_str: str) -> str:
        path, _ = QFileDialog.getOpenFileName(self, title, str(Path.home()), filter_str)
        return path

    def _browse_folder(self, title: str) -> str:
        return QFileDialog.getExistingDirectory(self, title, str(Path.home()))

    def _browse_contabilita(self) -> None:
        p = self._browse_file("Seleziona File Contabilità", "Excel Files (*.xlsx *.xlsm)")
        if p:
            self.contabilita_path_edit.setText(p)

    def _browse_giornaliere(self) -> None:
        p = self._browse_folder("Seleziona Cartella Giornaliere")
        if p:
            self.giornaliere_path_edit.setText(p)

    def _browse_attivita(self) -> None:
        p = self._browse_file("Seleziona File Attività", "Excel Files (*.xlsx *.xlsm)")
        if p:
            self.attivita_path_edit.setText(p)

    def _browse_activity_db(self) -> None:
        p = self._browse_file("Seleziona Database Report Attività", "SQLite DB (*.db *.sqlite)")
        if p:
            self.activity_db_path_edit.setText(p)

    def _browse_certificati(self) -> None:
        p = self._browse_file("Seleziona File Certificati", "Excel Files (*.xlsx *.xlsm)")
        if p:
            self.certificati_path_edit.setText(p)

    def _browse_certificati_root(self) -> None:
        p = self._browse_folder("Seleziona Cartella Certificati PDF")
        if p:
            self.certificati_root_edit.setText(p)

    def _browse_dataease(self) -> None:
        p = self._browse_file("Seleziona DB DataEase", "Access DB (*.mdb *.accdb)")
        if p:
            self.dataease_path_edit.setText(p)

    # --- LOAD & SAVE ---

    def load_from_config(self, config: dict[str, Any]) -> None:
        """Carica i percorsi dei file e delle cartelle dalla configurazione e li valida visivamente."""
        self.contabilita_path_edit.setText(str(config.get("contabilita_file_path", "")))
        self._validate_path(self.contabilita_path_edit)

        self.auto_update_check.setChecked(bool(config.get("enable_auto_update_contabilita", False)))

        self.giornaliere_path_edit.setText(str(config.get("giornaliere_path", "")))
        self._validate_path(self.giornaliere_path_edit)

        self.attivita_path_edit.setText(str(config.get("attivita_programmate_path", "")))
        self._validate_path(self.attivita_path_edit)

        self.activity_db_path_edit.setText(str(config.get("activity_db_path", "")))
        self._validate_path(self.activity_db_path_edit)

        self.certificati_path_edit.setText(str(config.get("certificati_campione_path", "")))
        self._validate_path(self.certificati_path_edit)

        self.certificati_root_edit.setText(str(config.get("certificati_root_path", "")))
        self._validate_path(self.certificati_root_edit)

        self.dataease_path_edit.setText(str(config.get("dataease_db_path", "")))
        self._validate_path(self.dataease_path_edit)

    def save_to_config(self, config_manager: Any) -> None:
        """Salva i percorsi attualmente impostati nella configurazione globale."""
        config_manager.set_config_value("contabilita_file_path", self.contabilita_path_edit.text())
        config_manager.set_config_value("enable_auto_update_contabilita", self.auto_update_check.isChecked())
        config_manager.set_config_value("giornaliere_path", self.giornaliere_path_edit.text())
        config_manager.set_config_value("attivita_programmate_path", self.attivita_path_edit.text())
        config_manager.set_config_value("activity_db_path", self.activity_db_path_edit.text())
        config_manager.set_config_value("certificati_campione_path", self.certificati_path_edit.text())
        config_manager.set_config_value("certificati_root_path", self.certificati_root_edit.text())
        config_manager.set_config_value("dataease_db_path", self.dataease_path_edit.text())
