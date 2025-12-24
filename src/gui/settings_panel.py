"""
Bot TS - Settings Panel
Pannello per la configurazione dell'applicazione.
Include gestione lista fornitori e tracking modifiche non salvate.
"""
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QLineEdit, QCheckBox, QSpinBox, QFileDialog,
    QMessageBox, QListWidget, QListWidgetItem, QInputDialog,
    QFrame, QScrollArea, QDialog, QFormLayout, QMenu
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal

from src.core import config_manager


class AccountDialog(QDialog):
    """Dialog per aggiungere/modificare un account."""
    def __init__(self, parent=None, username="", password=""):
        super().__init__(parent)
        self.setWindowTitle("Account ISAB")
        self.setFixedWidth(350)
        self.setStyleSheet("font-size: 15px;")

        layout = QFormLayout(self)

        self.username_edit = QLineEdit(username)
        self.username_edit.setMinimumHeight(35)
        layout.addRow("Username:", self.username_edit)

        self.password_edit = QLineEdit(password)
        self.password_edit.setMinimumHeight(35)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        # Password layout with toggle
        pass_layout = QHBoxLayout()
        pass_layout.setContentsMargins(0, 0, 0, 0)
        pass_layout.setSpacing(5)

        pass_layout.addWidget(self.password_edit)

        self.toggle_pass_btn = QPushButton("👁️")
        self.toggle_pass_btn.setToolTip("Mostra/Nascondi password")
        self.toggle_pass_btn.setFixedSize(35, 35)
        self.toggle_pass_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_pass_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #adb5bd;
            }
        """)
        self.toggle_pass_btn.clicked.connect(self._toggle_password_visibility)
        pass_layout.addWidget(self.toggle_pass_btn)

        layout.addRow("Password:", pass_layout)

        btns = QHBoxLayout()
        ok_btn = QPushButton("Salva")
        ok_btn.setMinimumHeight(35)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Annulla")
        cancel_btn.setMinimumHeight(35)
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(ok_btn)
        btns.addWidget(cancel_btn)

        layout.addRow(btns)

    def _toggle_password_visibility(self):
        if self.password_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pass_btn.setText("🔒")
            self.toggle_pass_btn.setToolTip("Nascondi password")
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pass_btn.setText("👁️")
            self.toggle_pass_btn.setToolTip("Mostra password")

    def get_data(self):
        return self.username_edit.text(), self.password_edit.text()


class SettingsPanel(QWidget):
    """Pannello per le impostazioni dell'applicazione."""
    
    # Segnale emesso quando ci sono modifiche non salvate
    unsaved_changes = pyqtSignal(bool)
    # Segnale emesso quando le impostazioni vengono salvate
    settings_saved = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._has_unsaved_changes = False

        # Keep references to prevent GC
        self.scroll = None
        self.scroll_content = None
        self.groups = []  # Store group boxes to prevent premature GC

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
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title)
        
        desc = QLabel("Configurazione credenziali ISAB, browser e fornitori")
        desc.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 16px;")
        header_layout.addWidget(desc)
        
        main_layout.addWidget(header)
        
        # Scroll area per il contenuto
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        self.scroll_content = QWidget()
        scroll_layout = QVBoxLayout(self.scroll_content)
        scroll_layout.setSpacing(20)
        
        # --- Sezione Generale (Top Level) ---
        general_group = self._create_group_box("⚙️ Generale")
        general_layout = QVBoxLayout(general_group)
        self.groups.append(general_group)

        # HEADLESS MODE CHECKBOX - Explicitly ensure visibility and styling
        self.headless_check = QCheckBox("Esegui in modalità Headless (Nascosta)")
        self.headless_check.setToolTip("Se attivato, il browser verrà eseguito in background senza mostrare la finestra.")
        self.headless_check.setStyleSheet("QCheckBox { padding: 5px; font-size: 15px; font-weight: bold; color: #d63384; }") # Pink/Bold to highlight
        general_layout.addWidget(self.headless_check)

        scroll_layout.addWidget(general_group)

        # --- Sezione Account ---
        account_group = self._create_group_box("🔐 Gestione Account ISAB")
        account_layout = QVBoxLayout(account_group)
        self.groups.append(account_group)
        
        self.account_list = QListWidget()
        self.account_list.setMinimumHeight(120)
        self.account_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                font-size: 15px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
            }
        """)
        self.account_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.account_list.customContextMenuRequested.connect(lambda pos: self._show_account_context_menu(pos))
        account_layout.addWidget(self.account_list)
        
        acc_btns = QHBoxLayout()
        
        add_acc_btn = QPushButton("➕ Aggiungi")
        add_acc_btn.clicked.connect(self._add_account)
        self._style_small_button(add_acc_btn, "#28a745")
        acc_btns.addWidget(add_acc_btn)
        
        edit_acc_btn = QPushButton("✏️ Modifica")
        edit_acc_btn.clicked.connect(self._edit_account)
        self._style_small_button(edit_acc_btn, "#0d6efd")
        acc_btns.addWidget(edit_acc_btn)

        remove_acc_btn = QPushButton("🗑️ Rimuovi")
        remove_acc_btn.clicked.connect(self._remove_account)
        self._style_small_button(remove_acc_btn, "#dc3545")
        acc_btns.addWidget(remove_acc_btn)

        set_def_btn = QPushButton("⭐ Imposta Default")
        set_def_btn.clicked.connect(self._set_default_account)
        self._style_small_button(set_def_btn, "#ffc107", text_color="black")
        acc_btns.addWidget(set_def_btn)

        acc_btns.addStretch()
        account_layout.addLayout(acc_btns)

        scroll_layout.addWidget(account_group)
        
        # --- Sezione Contratti ---
        contract_group = self._create_group_box("📋 Numeri Contratto")
        contract_layout = QVBoxLayout(contract_group)
        self.groups.append(contract_group)
        
        contract_hint = QLabel("Gestisci l'elenco dei contratti disponibili nel menu a tendina di Dettagli OdA.")
        contract_hint.setStyleSheet("color: #6c757d; font-size: 14px;")
        contract_hint.setWordWrap(True)
        contract_layout.addWidget(contract_hint)

        self.contract_list = QListWidget()
        self.contract_list.setMinimumHeight(120)
        self.contract_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                font-size: 15px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
            }
        """)
        self.contract_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.contract_list.customContextMenuRequested.connect(lambda pos: self._show_generic_list_menu(pos, self.contract_list, self._add_contract, self._edit_contract, self._remove_contract))
        contract_layout.addWidget(self.contract_list)

        contract_btns = QHBoxLayout()

        add_contract_btn = QPushButton("➕ Aggiungi")
        add_contract_btn.clicked.connect(self._add_contract)
        self._style_small_button(add_contract_btn, "#28a745")
        contract_btns.addWidget(add_contract_btn)

        edit_contract_btn = QPushButton("✏️ Modifica")
        edit_contract_btn.clicked.connect(self._edit_contract)
        self._style_small_button(edit_contract_btn, "#0d6efd")
        contract_btns.addWidget(edit_contract_btn)

        remove_contract_btn = QPushButton("🗑️ Rimuovi")
        remove_contract_btn.clicked.connect(self._remove_contract)
        self._style_small_button(remove_contract_btn, "#dc3545")
        contract_btns.addWidget(remove_contract_btn)

        contract_btns.addStretch()
        contract_layout.addLayout(contract_btns)

        scroll_layout.addWidget(contract_group)
        
        # --- Sezione Fornitori ---
        fornitori_group = self._create_group_box("🏢 Gestione Fornitori")
        fornitori_layout = QVBoxLayout(fornitori_group)
        self.groups.append(fornitori_group)
        
        fornitori_hint = QLabel(
            "Gestisci l'elenco dei fornitori disponibili nel menu a tendina dello Scarico TS.\n"
            "Formato consigliato: CODICE - NOME (es: KK10608 - COEMI S.R.L.)"
        )
        fornitori_hint.setStyleSheet("color: #6c757d; font-size: 14px;")
        fornitori_hint.setWordWrap(True)
        fornitori_layout.addWidget(fornitori_hint)
        
        self.fornitori_list = QListWidget()
        self.fornitori_list.setMinimumHeight(150)
        self.fornitori_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
                padding: 5px;
                font-size: 15px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
            }
        """)
        self.fornitori_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.fornitori_list.customContextMenuRequested.connect(lambda pos: self._show_generic_list_menu(pos, self.fornitori_list, self._add_fornitore, self._edit_fornitore, self._remove_fornitore))
        fornitori_layout.addWidget(self.fornitori_list)
        
        fornitori_btn_layout = QHBoxLayout()
        
        add_forn_btn = QPushButton("➕ Aggiungi")
        add_forn_btn.clicked.connect(self._add_fornitore)
        self._style_small_button(add_forn_btn, "#28a745")
        fornitori_btn_layout.addWidget(add_forn_btn)
        
        edit_forn_btn = QPushButton("✏️ Modifica")
        edit_forn_btn.clicked.connect(self._edit_fornitore)
        self._style_small_button(edit_forn_btn, "#0d6efd")
        fornitori_btn_layout.addWidget(edit_forn_btn)
        
        rem_forn_btn = QPushButton("🗑️ Rimuovi")
        rem_forn_btn.clicked.connect(self._remove_fornitore)
        self._style_small_button(rem_forn_btn, "#dc3545")
        fornitori_btn_layout.addWidget(rem_forn_btn)
        
        fornitori_btn_layout.addStretch()
        fornitori_layout.addLayout(fornitori_btn_layout)
        
        scroll_layout.addWidget(fornitori_group)

        # --- Sezione Strumentale ---
        contabilita_group = self._create_group_box("📊 Strumentale")
        contabilita_layout = QVBoxLayout(contabilita_group)
        self.groups.append(contabilita_group)

        # Path input
        path_label = QLabel("File Excel di origine:")
        path_label.setStyleSheet("font-size: 14px; font-weight: normal;")
        contabilita_layout.addWidget(path_label)

        contabilita_path_layout = QHBoxLayout()
        self.contabilita_path_edit = QLineEdit()
        self.contabilita_path_edit.setPlaceholderText("Seleziona il file Excel...")
        self.contabilita_path_edit.setReadOnly(True)
        self.contabilita_path_edit.setMinimumHeight(40)
        self._style_input(self.contabilita_path_edit)
        contabilita_path_layout.addWidget(self.contabilita_path_edit)

        self.browse_contabilita_btn = QPushButton("📂 Sfoglia")
        self.browse_contabilita_btn.setMinimumHeight(40)
        self.browse_contabilita_btn.setMinimumWidth(120)
        self.browse_contabilita_btn.clicked.connect(self._browse_contabilita_path)
        self._style_button(self.browse_contabilita_btn)
        contabilita_path_layout.addWidget(self.browse_contabilita_btn)
        contabilita_layout.addLayout(contabilita_path_layout)

        # Auto-update checkbox
        self.auto_update_contabilita_check = QCheckBox("Attiva aggiornamento automatico all'avvio (background)")
        self.auto_update_contabilita_check.setStyleSheet("padding: 5px; font-size: 15px; font-weight: normal;")
        contabilita_layout.addWidget(self.auto_update_contabilita_check)

        # Giornaliere Path input
        giornaliere_label = QLabel("Cartella Giornaliere (Root):")
        giornaliere_label.setStyleSheet("font-size: 14px; font-weight: normal; margin-top: 10px;")
        contabilita_layout.addWidget(giornaliere_label)

        giornaliere_path_layout = QHBoxLayout()
        self.giornaliere_path_edit = QLineEdit()
        self.giornaliere_path_edit.setPlaceholderText("Seleziona la cartella root delle Giornaliere...")
        self.giornaliere_path_edit.setReadOnly(True)
        self.giornaliere_path_edit.setMinimumHeight(40)
        self._style_input(self.giornaliere_path_edit)
        giornaliere_path_layout.addWidget(self.giornaliere_path_edit)

        self.browse_giornaliere_btn = QPushButton("📂 Sfoglia")
        self.browse_giornaliere_btn.setMinimumHeight(40)
        self.browse_giornaliere_btn.setMinimumWidth(120)
        self.browse_giornaliere_btn.clicked.connect(self._browse_giornaliere_path)
        self._style_button(self.browse_giornaliere_btn)
        giornaliere_path_layout.addWidget(self.browse_giornaliere_btn)
        contabilita_layout.addLayout(giornaliere_path_layout)

        # Attività Programmate Input
        attivita_label = QLabel("File Attività Programmate (Riepilogo):")
        attivita_label.setStyleSheet("font-size: 14px; font-weight: normal; margin-top: 10px;")
        contabilita_layout.addWidget(attivita_label)

        attivita_path_layout = QHBoxLayout()
        self.attivita_path_edit = QLineEdit()
        self.attivita_path_edit.setPlaceholderText("Seleziona file Attività Programmate...")
        self.attivita_path_edit.setReadOnly(True)
        self.attivita_path_edit.setMinimumHeight(40)
        self._style_input(self.attivita_path_edit)
        attivita_path_layout.addWidget(self.attivita_path_edit)

        self.browse_attivita_btn = QPushButton("📂 Sfoglia")
        self.browse_attivita_btn.setMinimumHeight(40)
        self.browse_attivita_btn.setMinimumWidth(120)
        self.browse_attivita_btn.clicked.connect(self._browse_attivita_path)
        self._style_button(self.browse_attivita_btn)
        attivita_path_layout.addWidget(self.browse_attivita_btn)
        contabilita_layout.addLayout(attivita_path_layout)

        # Certificati Campione Input
        certificati_label = QLabel("File Certificati Campione:")
        certificati_label.setStyleSheet("font-size: 14px; font-weight: normal; margin-top: 10px;")
        contabilita_layout.addWidget(certificati_label)

        certificati_path_layout = QHBoxLayout()
        self.certificati_path_edit = QLineEdit()
        self.certificati_path_edit.setPlaceholderText("Seleziona file Certificati Campione...")
        self.certificati_path_edit.setReadOnly(True)
        self.certificati_path_edit.setMinimumHeight(40)
        self._style_input(self.certificati_path_edit)
        certificati_path_layout.addWidget(self.certificati_path_edit)

        self.browse_certificati_btn = QPushButton("📂 Sfoglia")
        self.browse_certificati_btn.setMinimumHeight(40)
        self.browse_certificati_btn.setMinimumWidth(120)
        self.browse_certificati_btn.clicked.connect(self._browse_certificati_path)
        self._style_button(self.browse_certificati_btn)
        certificati_path_layout.addWidget(self.browse_certificati_btn)
        contabilita_layout.addLayout(certificati_path_layout)

        scroll_layout.addWidget(contabilita_group)

        # --- Sezione Scarico Ore Cantiere (DataEase) ---
        dataease_group = self._create_group_box("🏗️ Scarico Ore Cantiere (DataEase)")
        dataease_layout = QVBoxLayout(dataease_group)
        self.groups.append(dataease_group)

        dataease_label = QLabel("File Scarico Ore Cantiere (DataEase):")
        dataease_label.setStyleSheet("font-size: 14px; font-weight: normal;")
        dataease_layout.addWidget(dataease_label)

        dataease_path_layout = QHBoxLayout()
        self.dataease_path_edit = QLineEdit()
        self.dataease_path_edit.setPlaceholderText("Seleziona file Excel scarico ore...")
        self.dataease_path_edit.setReadOnly(True)
        self.dataease_path_edit.setMinimumHeight(40)
        self._style_input(self.dataease_path_edit)
        dataease_path_layout.addWidget(self.dataease_path_edit)

        self.browse_dataease_btn = QPushButton("📂 Sfoglia")
        self.browse_dataease_btn.setMinimumHeight(40)
        self.browse_dataease_btn.setMinimumWidth(120)
        self.browse_dataease_btn.clicked.connect(self._browse_dataease_path)
        self._style_button(self.browse_dataease_btn)
        dataease_path_layout.addWidget(self.browse_dataease_btn)
        dataease_layout.addLayout(dataease_path_layout)

        scroll_layout.addWidget(dataease_group)
        
        # --- Sezione Browser ---
        browser_group = self._create_group_box("🌐 Impostazioni Browser")
        browser_layout = QVBoxLayout(browser_group)
        self.groups.append(browser_group)
        
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Timeout (secondi):")
        timeout_label.setStyleSheet("font-size: 15px;")
        timeout_layout.addWidget(timeout_label)
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(10, 120)
        self.timeout_spin.setValue(30)
        self.timeout_spin.setMinimumHeight(40)
        self.timeout_spin.setMinimumWidth(100)
        self._style_input(self.timeout_spin)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        browser_layout.addLayout(timeout_layout)
        
        # --- Sezione Diagnostica ---
        diag_group = self._create_group_box("🛠️ Diagnostica & Licenza")
        diag_layout = QVBoxLayout(diag_group)
        self.groups.append(diag_group)

        open_folder_btn = QPushButton("📂 Apri cartella Logs e Licenza")
        open_folder_btn.setMinimumHeight(45)
        open_folder_btn.clicked.connect(self._open_data_folder)
        self._style_button(open_folder_btn)
        diag_layout.addWidget(open_folder_btn)

        scroll_layout.addWidget(diag_group)
        
        scroll_layout.addStretch()
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)
        
        # --- Pulsanti azione ---
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.unsaved_label = QLabel("⚠️ Modifiche non salvate")
        self.unsaved_label.setStyleSheet("color: #dc3545; font-weight: bold; padding: 5px 10px; font-size: 15px;")
        self.unsaved_label.setVisible(False)
        action_layout.addWidget(self.unsaved_label)
        
        self.reset_btn = QPushButton("↩️ Annulla modifiche")
        self.reset_btn.setMinimumWidth(160)
        self.reset_btn.setMinimumHeight(45)
        self.reset_btn.clicked.connect(self._reset_settings)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        action_layout.addWidget(self.reset_btn)
        
        self.save_btn = QPushButton("💾 Salva impostazioni")
        self.save_btn.setMinimumWidth(180)
        self.save_btn.setMinimumHeight(45)
        self.save_btn.clicked.connect(self._save_settings)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        action_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(action_layout)
    
    def _create_group_box(self, title: str) -> QGroupBox:
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 15px;
                padding-top: 15px;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        return group
    
    def _style_input(self, widget):
        widget.setStyleSheet("""
            QLineEdit, QSpinBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 10px;
                font-size: 15px;
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
        button.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 18px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
    
    def _style_small_button(self, button, color, text_color="white"):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: {text_color};
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """)

    def _connect_change_signals(self):
        self.headless_check.stateChanged.connect(self._on_change)
        self.timeout_spin.valueChanged.connect(self._on_change)
        self.contabilita_path_edit.textChanged.connect(self._on_change)
        self.giornaliere_path_edit.textChanged.connect(self._on_change)
        self.attivita_path_edit.textChanged.connect(self._on_change)
        self.certificati_path_edit.textChanged.connect(self._on_change)
        self.auto_update_contabilita_check.stateChanged.connect(self._on_change)
        self.dataease_path_edit.textChanged.connect(self._on_change)
        # Liste gestite manualmente
    
    def _on_change(self):
        self._set_unsaved_changes(True)
    
    def _set_unsaved_changes(self, has_changes: bool):
        self._has_unsaved_changes = has_changes
        self.unsaved_label.setVisible(has_changes)
        self.unsaved_changes.emit(has_changes)
    
    def has_unsaved_changes(self) -> bool:
        """Restituisce True se ci sono modifiche non salvate."""
        return self._has_unsaved_changes

    def _open_data_folder(self):
        """Apre la cartella dei dati (logs, config, licenza)."""
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl
        folder = config_manager.CONFIG_DIR
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    def _browse_contabilita_path(self):
        current_path = self.contabilita_path_edit.text()
        directory = str(Path(current_path).parent) if current_path else str(Path.home())

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file Excel Contabilità",
            directory,
            "Excel Files (*.xlsx *.xlsm *.xls)"
        )
        if path:
            self.contabilita_path_edit.setText(path)
            self._set_unsaved_changes(True)

    def _browse_giornaliere_path(self):
        current_path = self.giornaliere_path_edit.text()
        path = QFileDialog.getExistingDirectory(
            self,
            "Seleziona Cartella Root Giornaliere",
            current_path if current_path else str(Path.home())
        )
        if path:
            self.giornaliere_path_edit.setText(path)
            self._set_unsaved_changes(True)

    def _browse_attivita_path(self):
        current_path = self.attivita_path_edit.text()
        directory = str(Path(current_path).parent) if current_path else str(Path.home())

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file Attività Programmate",
            directory,
            "Excel Files (*.xlsx *.xlsm *.xls)"
        )
        if path:
            self.attivita_path_edit.setText(path)
            self._set_unsaved_changes(True)

    def _browse_certificati_path(self):
        current_path = self.certificati_path_edit.text()
        directory = str(Path(current_path).parent) if current_path else str(Path.home())

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file Certificati Campione",
            directory,
            "Excel Files (*.xlsx *.xlsm *.xls)"
        )
        if path:
            self.certificati_path_edit.setText(path)
            self._set_unsaved_changes(True)

    def _browse_dataease_path(self):
        current_path = self.dataease_path_edit.text()
        directory = str(Path(current_path).parent) if current_path else str(Path.home())

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file DataEase (Scarico Ore)",
            directory,
            "Excel Files (*.xlsx *.xlsm *.xls)"
        )
        if path:
            self.dataease_path_edit.setText(path)
            self._set_unsaved_changes(True)
    
    # --- Gestione Account ---
    def _render_accounts(self, accounts):
        self.account_list.clear()
        for acc in accounts:
            label = acc['username']
            if acc.get('default'):
                label += " (⭐ Default)"
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, acc)
            self.account_list.addItem(item)

    def _add_account(self):
        dlg = AccountDialog(self)
        if dlg.exec():
            u, p = dlg.get_data()
            if u:
                is_default = self.account_list.count() == 0
                acc = {"username": u, "password": p, "default": is_default}
                self._render_accounts(self._get_current_accounts() + [acc])
                self._set_unsaved_changes(True)

    def _edit_account(self):
        """Modifica l'account selezionato."""
        item = self.account_list.currentItem()
        if not item:
            QMessageBox.information(self, "Info", "Seleziona un account da modificare.")
            return

        acc_data = item.data(Qt.ItemDataRole.UserRole)
        dlg = AccountDialog(self, username=acc_data["username"], password=acc_data["password"])

        if dlg.exec():
            new_u, new_p = dlg.get_data()
            if new_u:
                # Aggiorna dati
                acc_data["username"] = new_u
                acc_data["password"] = new_p
                # Renderizza di nuovo la lista per aggiornare la label
                self._render_accounts(self._get_current_accounts())
                self._set_unsaved_changes(True)

    def _remove_account(self):
        row = self.account_list.currentRow()
        if row >= 0:
            if QMessageBox.question(self, "Conferma", "Rimuovere account?") == QMessageBox.StandardButton.Yes:
                self.account_list.takeItem(row)
                accounts = self._get_current_accounts()
                if accounts and not any(a['default'] for a in accounts):
                    accounts[0]['default'] = True
                    self._render_accounts(accounts)
                self._set_unsaved_changes(True)

    def _show_account_context_menu(self, position):
        """Mostra menu contestuale per lista account."""
        menu = QMenu()
        item = self.account_list.itemAt(position)
        
        # Action Aggiungi sempre visibile
        add_action = QAction("➕ Aggiungi account", self)
        add_action.triggered.connect(self._add_account)
        menu.addAction(add_action)
        
        if item:
            self.account_list.setCurrentItem(item)
            menu.addSeparator()
            
            edit_action = QAction("✏️ Modifica", self)
            edit_action.triggered.connect(self._edit_account)
            menu.addAction(edit_action)
            
            default_action = QAction("⭐ Imposta come Default", self)
            default_action.triggered.connect(self._set_default_account)
            menu.addAction(default_action)
            
            remove_action = QAction("🗑️ Rimuovi", self)
            remove_action.triggered.connect(self._remove_account)
            menu.addAction(remove_action)
            
        menu.exec(self.account_list.viewport().mapToGlobal(position))

    def _show_generic_list_menu(self, position, list_widget, add_cb, edit_cb, remove_cb):
        """Menu generico per liste semplici (contratti, fornitori)."""
        menu = QMenu()
        item = list_widget.itemAt(position)
        
        add_action = QAction("➕ Aggiungi", self)
        add_action.triggered.connect(add_cb)
        menu.addAction(add_action)
        
        if item:
            list_widget.setCurrentItem(item)
            menu.addSeparator()
            
            edit_action = QAction("✏️ Modifica", self)
            edit_action.triggered.connect(edit_cb)
            menu.addAction(edit_action)
            
            remove_action = QAction("🗑️ Rimuovi", self)
            remove_action.triggered.connect(remove_cb)
            menu.addAction(remove_action)
            
        menu.exec(list_widget.viewport().mapToGlobal(position))

    def _set_default_account(self):
        row = self.account_list.currentRow()
        if row >= 0:
            accounts = self._get_current_accounts()
            for i, acc in enumerate(accounts):
                acc['default'] = (i == row)
            self._render_accounts(accounts)
            self._set_unsaved_changes(True)

    def _get_current_accounts(self):
        accounts = []
        for i in range(self.account_list.count()):
            item = self.account_list.item(i)
            accounts.append(item.data(Qt.ItemDataRole.UserRole))
        return accounts

    # --- Gestione Contratti ---
    def _add_contract(self):
        text, ok = QInputDialog.getText(self, "Aggiungi Contratto", "Inserisci il numero di contratto:")
        if ok and text.strip():
            if not self.contract_list.findItems(text.strip(), Qt.MatchFlag.MatchExactly):
                self.contract_list.addItem(text.strip())
                self._set_unsaved_changes(True)

    def _edit_contract(self):
        item = self.contract_list.currentItem()
        if item:
            text, ok = QInputDialog.getText(self, "Modifica", "Valore:", text=item.text())
            if ok and text.strip():
                item.setText(text.strip())
                self._set_unsaved_changes(True)

    def _remove_contract(self):
        row = self.contract_list.currentRow()
        if row >= 0:
            if QMessageBox.question(self, "Conferma", "Rimuovere contratto?") == QMessageBox.StandardButton.Yes:
                self.contract_list.takeItem(row)
                self._set_unsaved_changes(True)

    # --- Gestione Fornitori ---
    def _add_fornitore(self):
        text, ok = QInputDialog.getText(self, "Aggiungi Fornitore", "Inserisci il codice e nome:")
        if ok and text.strip():
            for i in range(self.fornitori_list.count()):
                if self.fornitori_list.item(i).text().lower() == text.strip().lower():
                    QMessageBox.warning(self, "Esistente", "Fornitore già presente.")
                    return
            self.fornitori_list.addItem(text.strip())
            self._set_unsaved_changes(True)

    def _edit_fornitore(self):
        item = self.fornitori_list.currentItem()
        if item:
            text, ok = QInputDialog.getText(self, "Modifica", "Valore:", text=item.text())
            if ok and text.strip():
                item.setText(text.strip())
                self._set_unsaved_changes(True)

    def _remove_fornitore(self):
        row = self.fornitori_list.currentRow()
        if row >= 0:
            if QMessageBox.question(self, "Conferma", "Rimuovere?") == QMessageBox.StandardButton.Yes:
                self.fornitori_list.takeItem(row)
                self._set_unsaved_changes(True)

    # --- Load & Save ---
    def _load_settings(self):
        config = config_manager.load_config()
        
        # Browser
        self.headless_check.setChecked(config.get("browser_headless", False))
        self.timeout_spin.setValue(config.get("browser_timeout", 30))
        
        # Contabilita
        self.contabilita_path_edit.setText(config.get("contabilita_file_path", ""))
        self.giornaliere_path_edit.setText(config.get("giornaliere_path", ""))
        self.attivita_path_edit.setText(config.get("attivita_programmate_path", ""))
        self.certificati_path_edit.setText(config.get("certificati_campione_path", ""))
        self.dataease_path_edit.setText(config.get("dataease_path", "")) # New
        self.auto_update_contabilita_check.setChecked(config.get("enable_auto_update_contabilita", True))

        # Fornitori
        self.fornitori_list.clear()
        for f in config.get("fornitori", []):
            self.fornitori_list.addItem(f)

        # Contratti
        self.contract_list.clear()
        for c in config.get("contracts", []):
            self.contract_list.addItem(c)

        # Accounts
        self._render_accounts(config.get("accounts", []))
        
        self._set_unsaved_changes(False)
    
    def _save_settings(self):
        # Raccogli dati
        fornitori = [self.fornitori_list.item(i).text() for i in range(self.fornitori_list.count())]
        contracts = [self.contract_list.item(i).text() for i in range(self.contract_list.count())]
        accounts = self._get_current_accounts()
        
        config_manager.set_config_value("browser_headless", self.headless_check.isChecked())
        config_manager.set_config_value("browser_timeout", self.timeout_spin.value())

        config_manager.set_config_value("contabilita_file_path", self.contabilita_path_edit.text())
        config_manager.set_config_value("giornaliere_path", self.giornaliere_path_edit.text())
        config_manager.set_config_value("attivita_programmate_path", self.attivita_path_edit.text())
        config_manager.set_config_value("certificati_campione_path", self.certificati_path_edit.text())
        config_manager.set_config_value("dataease_path", self.dataease_path_edit.text()) # New
        config_manager.set_config_value("enable_auto_update_contabilita", self.auto_update_contabilita_check.isChecked())

        config_manager.set_config_value("fornitori", fornitori)
        config_manager.set_config_value("contracts", contracts)
        # Il primo della lista diventa default se esiste
        if contracts:
            config_manager.set_config_value("default_contract", contracts[0])

        config_manager.set_config_value("accounts", accounts)
        
        self._set_unsaved_changes(False)
        # QMessageBox.information(self, "Salvataggio", "Impostazioni salvate.") # Suppresso, usa Toast
        
        # Emetti segnale
        self.settings_saved.emit()
    
    def _reset_settings(self):
        if self._has_unsaved_changes:
            if QMessageBox.question(self, "Conferma", "Annullare modifiche?") == QMessageBox.StandardButton.Yes:
                self._load_settings()
        else:
            self._load_settings()

    def prompt_save_if_needed(self) -> bool:
        if not self._has_unsaved_changes: return True
        reply = QMessageBox.question(self, "Modifiche non salvate", "Salvare?",
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
        if reply == QMessageBox.StandardButton.Save:
            self._save_settings()
            return True
        elif reply == QMessageBox.StandardButton.Discard:
            self._load_settings()
            return True
        return False
