"""
Bot TS - Settings Panel
Pannello per la configurazione dell'applicazione.
Include gestione lista fornitori e tracking modifiche non salvate.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QLineEdit, QCheckBox, QSpinBox, QFileDialog,
    QMessageBox, QListWidget, QListWidgetItem, QInputDialog,
    QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal

from src.core import config_manager


class SettingsPanel(QWidget):
    """Pannello per le impostazioni dell'applicazione."""
    
    # Segnale emesso quando ci sono modifiche non salvate
    unsaved_changes = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._has_unsaved_changes = False
        self._setup_ui()
        self._load_settings()
        self._connect_change_signals()
    
    def _setup_ui(self):
        """Configura l'interfaccia."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header)
        
        title = QLabel("⚙️ Impostazioni")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title)
        
        desc = QLabel("Configurazione credenziali ISAB, browser e fornitori")
        desc.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 12px;")
        header_layout.addWidget(desc)
        
        main_layout.addWidget(header)
        
        # Scroll area per il contenuto
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        
        # --- Sezione Credenziali ISAB ---
        credentials_group = self._create_group_box("🔐 Credenziali ISAB")
        cred_layout = QVBoxLayout(credentials_group)
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setMinimumWidth(120)
        username_layout.addWidget(username_label)
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Inserisci username ISAB")
        self.username_edit.setMinimumHeight(35)
        self._style_input(self.username_edit)
        username_layout.addWidget(self.username_edit)
        cred_layout.addLayout(username_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setMinimumWidth(120)
        password_layout.addWidget(password_label)
        
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Inserisci password ISAB")
        self.password_edit.setMinimumHeight(35)
        self._style_input(self.password_edit)
        password_layout.addWidget(self.password_edit)
        
        self.show_password_btn = QPushButton("👁")
        self.show_password_btn.setFixedSize(35, 35)
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.clicked.connect(self._toggle_password_visibility)
        password_layout.addWidget(self.show_password_btn)
        cred_layout.addLayout(password_layout)
        
        scroll_layout.addWidget(credentials_group)
        
        # --- Sezione Fornitori ---
        fornitori_group = self._create_group_box("🏢 Gestione Fornitori")
        fornitori_layout = QVBoxLayout(fornitori_group)
        
        fornitori_hint = QLabel(
            "Gestisci l'elenco dei fornitori disponibili nel menu a tendina dello Scarico TS.\n"
            "Formato consigliato: CODICE - NOME (es: KK10608 - COEMI S.R.L.)"
        )
        fornitori_hint.setStyleSheet("color: #6c757d; font-size: 11px;")
        fornitori_hint.setWordWrap(True)
        fornitori_layout.addWidget(fornitori_hint)
        
        # Lista fornitori
        self.fornitori_list = QListWidget()
        self.fornitori_list.setMinimumHeight(150)
        self.fornitori_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
            }
            QListWidget::item:hover {
                background-color: #f8f9fa;
            }
        """)
        fornitori_layout.addWidget(self.fornitori_list)
        
        # Pulsanti gestione fornitori
        fornitori_btn_layout = QHBoxLayout()
        
        self.add_fornitore_btn = QPushButton("➕ Aggiungi")
        self.add_fornitore_btn.setMinimumHeight(32)
        self.add_fornitore_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.add_fornitore_btn.clicked.connect(self._add_fornitore)
        fornitori_btn_layout.addWidget(self.add_fornitore_btn)
        
        self.edit_fornitore_btn = QPushButton("✏️ Modifica")
        self.edit_fornitore_btn.setMinimumHeight(32)
        self.edit_fornitore_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        self.edit_fornitore_btn.clicked.connect(self._edit_fornitore)
        fornitori_btn_layout.addWidget(self.edit_fornitore_btn)
        
        self.remove_fornitore_btn = QPushButton("🗑️ Rimuovi")
        self.remove_fornitore_btn.setMinimumHeight(32)
        self.remove_fornitore_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.remove_fornitore_btn.clicked.connect(self._remove_fornitore)
        fornitori_btn_layout.addWidget(self.remove_fornitore_btn)
        
        fornitori_btn_layout.addStretch()
        fornitori_layout.addLayout(fornitori_btn_layout)
        
        scroll_layout.addWidget(fornitori_group)
        
        # --- Sezione Browser ---
        browser_group = self._create_group_box("🌐 Impostazioni Browser")
        browser_layout = QVBoxLayout(browser_group)
        
        # Headless
        self.headless_check = QCheckBox("Esegui in modalità headless (senza interfaccia grafica)")
        self.headless_check.setStyleSheet("padding: 5px;")
        browser_layout.addWidget(self.headless_check)
        
        # Timeout
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Timeout (secondi):")
        timeout_label.setMinimumWidth(120)
        timeout_layout.addWidget(timeout_label)
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(10, 120)
        self.timeout_spin.setValue(30)
        self.timeout_spin.setMinimumHeight(35)
        self.timeout_spin.setMinimumWidth(100)
        self._style_input(self.timeout_spin)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        browser_layout.addLayout(timeout_layout)
        
        scroll_layout.addWidget(browser_group)
        
        # --- Sezione Download ---
        download_group = self._create_group_box("📁 Cartella Download")
        download_layout = QVBoxLayout(download_group)
        
        path_layout = QHBoxLayout()
        
        self.download_path_edit = QLineEdit()
        self.download_path_edit.setPlaceholderText("Seleziona cartella per i file scaricati")
        self.download_path_edit.setReadOnly(True)
        self.download_path_edit.setMinimumHeight(35)
        self._style_input(self.download_path_edit)
        path_layout.addWidget(self.download_path_edit)
        
        self.browse_btn = QPushButton("📂 Sfoglia")
        self.browse_btn.setMinimumHeight(35)
        self.browse_btn.setMinimumWidth(100)
        self.browse_btn.clicked.connect(self._browse_download_path)
        self._style_button(self.browse_btn)
        path_layout.addWidget(self.browse_btn)
        
        download_layout.addLayout(path_layout)
        
        scroll_layout.addWidget(download_group)
        
        # Spacer
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # --- Pulsanti azione ---
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        # Indicatore modifiche non salvate
        self.unsaved_label = QLabel("⚠️ Modifiche non salvate")
        self.unsaved_label.setStyleSheet("""
            QLabel {
                color: #dc3545;
                font-weight: bold;
                padding: 5px 10px;
            }
        """)
        self.unsaved_label.setVisible(False)
        action_layout.addWidget(self.unsaved_label)
        
        self.reset_btn = QPushButton("↩️ Annulla modifiche")
        self.reset_btn.setMinimumWidth(140)
        self.reset_btn.setMinimumHeight(40)
        self.reset_btn.clicked.connect(self._reset_settings)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        action_layout.addWidget(self.reset_btn)
        
        self.save_btn = QPushButton("💾 Salva impostazioni")
        self.save_btn.setMinimumWidth(160)
        self.save_btn.setMinimumHeight(40)
        self.save_btn.clicked.connect(self._save_settings)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        action_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(action_layout)
    
    def _create_group_box(self, title: str) -> QGroupBox:
        """Crea un group box stilizzato."""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        return group
    
    def _style_input(self, widget):
        """Applica lo stile standard agli input."""
        widget.setStyleSheet("""
            QLineEdit, QSpinBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus, QSpinBox:focus {
                border-color: #0d6efd;
            }
            QLineEdit:read-only {
                background-color: #f8f9fa;
            }
        """)
    
    def _style_button(self, button):
        """Applica lo stile standard ai pulsanti."""
        button.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
    
    def _connect_change_signals(self):
        """Collega i segnali per tracciare le modifiche."""
        self.username_edit.textChanged.connect(self._on_change)
        self.password_edit.textChanged.connect(self._on_change)
        self.headless_check.stateChanged.connect(self._on_change)
        self.timeout_spin.valueChanged.connect(self._on_change)
        self.download_path_edit.textChanged.connect(self._on_change)
        # La lista fornitori è gestita separatamente nei metodi add/edit/remove
    
    def _on_change(self):
        """Chiamato quando un campo viene modificato."""
        self._set_unsaved_changes(True)
    
    def _set_unsaved_changes(self, has_changes: bool):
        """Imposta lo stato delle modifiche non salvate."""
        self._has_unsaved_changes = has_changes
        self.unsaved_label.setVisible(has_changes)
        self.unsaved_changes.emit(has_changes)
    
    def has_unsaved_changes(self) -> bool:
        """Restituisce True se ci sono modifiche non salvate."""
        return self._has_unsaved_changes
    
    def _toggle_password_visibility(self):
        """Mostra/nasconde la password."""
        if self.show_password_btn.isChecked():
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password_btn.setText("🔒")
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password_btn.setText("👁")
    
    def _browse_download_path(self):
        """Apre il dialogo per selezionare la cartella download."""
        current_path = self.download_path_edit.text()
        path = QFileDialog.getExistingDirectory(
            self,
            "Seleziona cartella download",
            current_path if current_path else ""
        )
        if path:
            self.download_path_edit.setText(path)
            self._set_unsaved_changes(True)
    
    def _add_fornitore(self):
        """Aggiunge un nuovo fornitore."""
        text, ok = QInputDialog.getText(
            self,
            "Aggiungi Fornitore",
            "Inserisci il codice e nome del fornitore:\n(es: KK10608 - COEMI S.R.L.)"
        )
        if ok and text.strip():
            # Verifica duplicati
            for i in range(self.fornitori_list.count()):
                if self.fornitori_list.item(i).text().lower() == text.strip().lower():
                    QMessageBox.warning(
                        self,
                        "Fornitore esistente",
                        "Questo fornitore è già presente nella lista."
                    )
                    return
            
            self.fornitori_list.addItem(text.strip())
            self._set_unsaved_changes(True)
    
    def _edit_fornitore(self):
        """Modifica il fornitore selezionato."""
        current_item = self.fornitori_list.currentItem()
        if not current_item:
            QMessageBox.information(
                self,
                "Nessuna selezione",
                "Seleziona un fornitore da modificare."
            )
            return
        
        text, ok = QInputDialog.getText(
            self,
            "Modifica Fornitore",
            "Modifica il codice e nome del fornitore:",
            text=current_item.text()
        )
        if ok and text.strip():
            current_item.setText(text.strip())
            self._set_unsaved_changes(True)
    
    def _remove_fornitore(self):
        """Rimuove il fornitore selezionato."""
        current_item = self.fornitori_list.currentItem()
        if not current_item:
            QMessageBox.information(
                self,
                "Nessuna selezione",
                "Seleziona un fornitore da rimuovere."
            )
            return
        
        reply = QMessageBox.question(
            self,
            "Conferma rimozione",
            f"Vuoi rimuovere il fornitore:\n{current_item.text()}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            row = self.fornitori_list.row(current_item)
            self.fornitori_list.takeItem(row)
            self._set_unsaved_changes(True)
    
    def _load_settings(self):
        """Carica le impostazioni salvate."""
        config = config_manager.load_config()
        
        self.username_edit.setText(config.get("isab_username", ""))
        self.password_edit.setText(config.get("isab_password", ""))
        self.headless_check.setChecked(config.get("browser_headless", False))
        self.timeout_spin.setValue(config.get("browser_timeout", 30))
        self.download_path_edit.setText(config.get("download_path", ""))
        
        # Carica fornitori
        self.fornitori_list.clear()
        fornitori = config.get("fornitori", [])
        for fornitore in fornitori:
            self.fornitori_list.addItem(fornitore)
        
        # Reset stato modifiche dopo il caricamento
        self._set_unsaved_changes(False)
    
    def _save_settings(self):
        """Salva le impostazioni."""
        # Raccogli fornitori dalla lista
        fornitori = []
        for i in range(self.fornitori_list.count()):
            fornitori.append(self.fornitori_list.item(i).text())
        
        # Salva tutte le impostazioni
        config_manager.set_config_value("isab_username", self.username_edit.text())
        config_manager.set_config_value("isab_password", self.password_edit.text())
        config_manager.set_config_value("browser_headless", self.headless_check.isChecked())
        config_manager.set_config_value("browser_timeout", self.timeout_spin.value())
        config_manager.set_config_value("download_path", self.download_path_edit.text())
        config_manager.set_config_value("fornitori", fornitori)
        
        self._set_unsaved_changes(False)
        
        QMessageBox.information(
            self,
            "Impostazioni salvate",
            "Le impostazioni sono state salvate con successo."
        )
    
    def _reset_settings(self):
        """Annulla le modifiche e ricarica le impostazioni salvate."""
        if self._has_unsaved_changes:
            reply = QMessageBox.question(
                self,
                "Annulla modifiche",
                "Vuoi annullare tutte le modifiche non salvate?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._load_settings()
        else:
            self._load_settings()
    
    def prompt_save_if_needed(self) -> bool:
        """
        Se ci sono modifiche non salvate, chiede all'utente se vuole salvarle.
        
        Returns:
            True se si può procedere (salvato o scartato), False se annullato
        """
        if not self._has_unsaved_changes:
            return True
        
        reply = QMessageBox.question(
            self,
            "Modifiche non salvate",
            "Ci sono modifiche non salvate nelle Impostazioni.\n\n"
            "Vuoi salvarle prima di continuare?",
            QMessageBox.StandardButton.Save | 
            QMessageBox.StandardButton.Discard | 
            QMessageBox.StandardButton.Cancel
        )
        
        if reply == QMessageBox.StandardButton.Save:
            self._save_settings()
            return True
        elif reply == QMessageBox.StandardButton.Discard:
            self._load_settings()  # Reset alle impostazioni salvate
            return True
        else:  # Cancel
            return False
