"""
Bot TS - Settings Panel
Pannello per le impostazioni dell'applicazione.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QLineEdit, QCheckBox, QFrame, QGridLayout,
    QFileDialog, QMessageBox, QSpinBox, QApplication
)
from PyQt6.QtCore import pyqtSignal

from src.core import config_manager, license_validator, version


class SettingsPanel(QWidget):
    """Pannello impostazioni dell'applicazione."""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._load_settings()
    
    def _setup_ui(self):
        """Configura l'interfaccia."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
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
        
        desc = QLabel("Configura le impostazioni dell'applicazione")
        desc.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 12px;")
        header_layout.addWidget(desc)
        
        layout.addWidget(header)
        
        # Credenziali ISAB
        credentials_group = QGroupBox("🔐 Credenziali ISAB")
        credentials_group.setStyleSheet(self._get_group_style())
        cred_layout = QGridLayout(credentials_group)
        cred_layout.setSpacing(10)
        
        cred_layout.addWidget(QLabel("Username:"), 0, 0)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Inserisci username ISAB")
        self.username_input.setMinimumHeight(36)
        cred_layout.addWidget(self.username_input, 0, 1)
        
        cred_layout.addWidget(QLabel("Password:"), 1, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Inserisci password ISAB")
        self.password_input.setMinimumHeight(36)
        cred_layout.addWidget(self.password_input, 1, 1)
        
        self.show_password_cb = QCheckBox("Mostra password")
        self.show_password_cb.toggled.connect(self._toggle_password_visibility)
        cred_layout.addWidget(self.show_password_cb, 2, 1)
        
        layout.addWidget(credentials_group)
        
        # Download Path
        download_group = QGroupBox("📁 Percorso Download")
        download_group.setStyleSheet(self._get_group_style())
        download_layout = QVBoxLayout(download_group)
        
        download_desc = QLabel(
            "Seleziona la cartella dove verranno salvati i file scaricati dai bot. "
            "Se lasciato vuoto, verrà usata la cartella Download predefinita."
        )
        download_desc.setStyleSheet("color: #6c757d; font-size: 11px;")
        download_desc.setWordWrap(True)
        download_layout.addWidget(download_desc)
        
        path_layout = QHBoxLayout()
        
        self.download_path_input = QLineEdit()
        self.download_path_input.setPlaceholderText("Cartella Download predefinita")
        self.download_path_input.setReadOnly(True)
        self.download_path_input.setMinimumHeight(36)
        path_layout.addWidget(self.download_path_input)
        
        browse_btn = QPushButton("📂 Sfoglia")
        browse_btn.setMinimumWidth(100)
        browse_btn.clicked.connect(self._browse_download_path)
        path_layout.addWidget(browse_btn)
        
        clear_path_btn = QPushButton("✕")
        clear_path_btn.setFixedWidth(40)
        clear_path_btn.setToolTip("Ripristina percorso predefinito")
        clear_path_btn.clicked.connect(self._clear_download_path)
        path_layout.addWidget(clear_path_btn)
        
        download_layout.addLayout(path_layout)
        
        # Mostra percorso corrente
        self.current_path_label = QLabel()
        self.current_path_label.setStyleSheet("color: #28a745; font-size: 11px;")
        download_layout.addWidget(self.current_path_label)
        
        layout.addWidget(download_group)
        
        # Opzioni Browser
        browser_group = QGroupBox("🌐 Opzioni Browser")
        browser_group.setStyleSheet(self._get_group_style())
        browser_layout = QVBoxLayout(browser_group)
        
        self.headless_cb = QCheckBox("Esegui in modalità headless (senza finestra browser)")
        self.headless_cb.setToolTip(
            "Se attivo, il browser funziona in background senza mostrare la finestra. "
            "Utile per esecuzioni automatiche, ma non permette di vedere cosa sta facendo il bot."
        )
        browser_layout.addWidget(self.headless_cb)
        
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Timeout operazioni (secondi):"))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(10, 120)
        self.timeout_spin.setValue(30)
        self.timeout_spin.setFixedWidth(80)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        browser_layout.addLayout(timeout_layout)
        
        layout.addWidget(browser_group)
        
        # Informazioni Licenza
        license_group = QGroupBox("📜 Licenza")
        license_group.setStyleSheet(self._get_group_style())
        license_layout = QGridLayout(license_group)
        
        # Hardware ID
        license_layout.addWidget(QLabel("Hardware ID:"), 0, 0)
        hw_id = license_validator.get_hardware_id()
        hw_id_display = hw_id[:30] + "..." if len(hw_id) > 30 else hw_id
        self.hw_id_label = QLabel(hw_id_display)
        self.hw_id_label.setStyleSheet("color: #495057; font-family: monospace;")
        license_layout.addWidget(self.hw_id_label, 0, 1)
        
        copy_hwid_btn = QPushButton("📋 Copia")
        copy_hwid_btn.setFixedWidth(80)
        copy_hwid_btn.clicked.connect(self._copy_hardware_id)
        license_layout.addWidget(copy_hwid_btn, 0, 2)
        
        # Stato licenza
        license_layout.addWidget(QLabel("Stato:"), 1, 0)
        is_valid, message = license_validator.verify_license()
        self.license_status_label = QLabel(message)
        if is_valid:
            self.license_status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        else:
            self.license_status_label.setStyleSheet("color: #dc3545; font-weight: bold;")
        license_layout.addWidget(self.license_status_label, 1, 1, 1, 2)
        
        # Scadenza
        license_layout.addWidget(QLabel("Scadenza:"), 2, 0)
        expiry = license_validator.get_license_expiry()
        self.license_expiry_label = QLabel(expiry)
        self.license_expiry_label.setStyleSheet("color: #495057;")
        license_layout.addWidget(self.license_expiry_label, 2, 1, 1, 2)
        
        layout.addWidget(license_group)
        
        # Info Applicazione
        app_group = QGroupBox("ℹ️ Informazioni")
        app_group.setStyleSheet(self._get_group_style())
        app_layout = QGridLayout(app_group)
        
        app_layout.addWidget(QLabel("Applicazione:"), 0, 0)
        app_layout.addWidget(QLabel(version.__app_name__), 0, 1)
        
        app_layout.addWidget(QLabel("Versione:"), 1, 0)
        app_layout.addWidget(QLabel(version.__version__), 1, 1)
        
        app_layout.addWidget(QLabel("Percorso dati:"), 2, 0)
        data_path = config_manager.get_data_path()
        data_path_label = QLabel(data_path)
        data_path_label.setStyleSheet("color: #6c757d; font-size: 10px;")
        data_path_label.setWordWrap(True)
        app_layout.addWidget(data_path_label, 2, 1)
        
        layout.addWidget(app_group)
        
        # Spacer
        layout.addStretch()
        
        # Pulsanti
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.save_btn = QPushButton("💾 Salva Impostazioni")
        self.save_btn.setMinimumWidth(150)
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        self.save_btn.clicked.connect(self._save_settings)
        btn_layout.addWidget(self.save_btn)
        
        reset_btn = QPushButton("🔄 Ripristina")
        reset_btn.setMinimumWidth(100)
        reset_btn.setMinimumHeight(40)
        reset_btn.setStyleSheet("""
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
        reset_btn.clicked.connect(self._load_settings)
        btn_layout.addWidget(reset_btn)
        
        layout.addLayout(btn_layout)
        
        # Stile input
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 13px;
                background-color: #ffffff;
                color: #333333;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #0d6efd;
                border-width: 2px;
            }
            QLineEdit:read-only {
                background-color: #f8f9fa;
            }
            QCheckBox {
                spacing: 8px;
                font-size: 12px;
            }
            QSpinBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px;
                background-color: #ffffff;
                min-height: 20px;
            }
            QLabel {
                color: #333333;
            }
        """)
    
    def _get_group_style(self) -> str:
        """Restituisce lo stile per i GroupBox."""
        return """
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 10px;
                padding: 15px;
                padding-top: 25px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """
    
    def _toggle_password_visibility(self, checked: bool):
        """Mostra/nasconde la password."""
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def _browse_download_path(self):
        """Apre il dialog per selezionare la cartella download."""
        current = self.download_path_input.text() or config_manager.get_download_path()
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Seleziona cartella download",
            current,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder:
            self.download_path_input.setText(folder)
            self._update_current_path_label()
    
    def _clear_download_path(self):
        """Ripristina il percorso download predefinito."""
        self.download_path_input.clear()
        self._update_current_path_label()
    
    def _update_current_path_label(self):
        """Aggiorna l'etichetta del percorso corrente."""
        custom_path = self.download_path_input.text()
        if custom_path:
            self.current_path_label.setText(f"📁 Percorso personalizzato: {custom_path}")
        else:
            default_path = config_manager.get_download_path()
            self.current_path_label.setText(f"📁 Percorso predefinito: {default_path}")
    
    def _copy_hardware_id(self):
        """Copia l'Hardware ID negli appunti."""
        hw_id = license_validator.get_hardware_id()
        QApplication.clipboard().setText(hw_id)
        QMessageBox.information(self, "Copiato", "Hardware ID copiato negli appunti!")
    
    def _load_settings(self):
        """Carica le impostazioni salvate."""
        config = config_manager.load_config()
        
        self.username_input.setText(config.get("isab_username", ""))
        self.password_input.setText(config.get("isab_password", ""))
        self.download_path_input.setText(config.get("download_path", ""))
        self.headless_cb.setChecked(config.get("browser_headless", False))
        self.timeout_spin.setValue(config.get("browser_timeout", 30))
        
        self._update_current_path_label()
    
    def _save_settings(self):
        """Salva le impostazioni."""
        config = config_manager.load_config()
        
        config["isab_username"] = self.username_input.text().strip()
        config["isab_password"] = self.password_input.text()
        config["download_path"] = self.download_path_input.text().strip()
        config["browser_headless"] = self.headless_cb.isChecked()
        config["browser_timeout"] = self.timeout_spin.value()
        
        if config_manager.save_config(config):
            QMessageBox.information(self, "Salvato", "Impostazioni salvate con successo!")
            self.settings_changed.emit()
        else:
            QMessageBox.critical(self, "Errore", "Impossibile salvare le impostazioni.")
