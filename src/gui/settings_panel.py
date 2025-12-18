"""
Bot TS - Settings Panel
Pannello per la configurazione dell'applicazione.
Include gestione lista fornitori e tracking modifiche non salvate.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QLineEdit, QCheckBox, QSpinBox, QFileDialog,
    QMessageBox, QListWidget, QListWidgetItem, QInputDialog,
    QFrame, QScrollArea, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal

from src.core import config_manager


class AccountDialog(QDialog):
    """Dialog per aggiungere/modificare un account."""
    def __init__(self, parent=None, username="", password=""):
        super().__init__(parent)
        self.setWindowTitle("Account ISAB")
        self.setFixedWidth(300)

        layout = QFormLayout(self)

        self.username_edit = QLineEdit(username)
        layout.addRow("Username:", self.username_edit)

        self.password_edit = QLineEdit(password)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Password:", self.password_edit)

        btns = QHBoxLayout()
        ok_btn = QPushButton("Salva")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Annulla")
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(ok_btn)
        btns.addWidget(cancel_btn)

        layout.addRow(btns)

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
        
        # --- Sezione Account ---
        account_group = self._create_group_box("🔐 Gestione Account ISAB")
        account_layout = QVBoxLayout(account_group)
        
        self.account_list = QListWidget()
        self.account_list.setMinimumHeight(100)
        self.account_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ced4da;
                border-radius: 4px;
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
        """)
        account_layout.addWidget(self.account_list)
        
        acc_btns = QHBoxLayout()
        
        add_acc_btn = QPushButton("➕ Aggiungi")
        add_acc_btn.clicked.connect(self._add_account)
        self._style_small_button(add_acc_btn, "#28a745")
        acc_btns.addWidget(add_acc_btn)
        
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

        # --- Sezione Dettagli OdA (Contratto Default) ---
        contract_group = self._create_group_box("📋 Default Dettagli OdA")
        contract_layout = QHBoxLayout(contract_group)
        
        contract_label = QLabel("Numero Contratto Standard:")
        contract_layout.addWidget(contract_label)
        
        self.default_contract_edit = QLineEdit()
        self.default_contract_edit.setPlaceholderText("Es: 4600002254")
        self._style_input(self.default_contract_edit)
        contract_layout.addWidget(self.default_contract_edit)

        scroll_layout.addWidget(contract_group)
        
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
        """)
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
        
        # --- Sezione Browser ---
        browser_group = self._create_group_box("🌐 Impostazioni Browser")
        browser_layout = QVBoxLayout(browser_group)
        
        self.headless_check = QCheckBox("Esegui in modalità headless (senza interfaccia grafica)")
        self.headless_check.setStyleSheet("padding: 5px;")
        browser_layout.addWidget(self.headless_check)
        
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Timeout (secondi):")
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
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # --- Pulsanti azione ---
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.unsaved_label = QLabel("⚠️ Modifiche non salvate")
        self.unsaved_label.setStyleSheet("color: #dc3545; font-weight: bold; padding: 5px 10px;")
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
    
    def _style_small_button(self, button, color, text_color="white"):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: {text_color};
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """)

    def _connect_change_signals(self):
        self.headless_check.stateChanged.connect(self._on_change)
        self.timeout_spin.valueChanged.connect(self._on_change)
        self.download_path_edit.textChanged.connect(self._on_change)
        self.default_contract_edit.textChanged.connect(self._on_change)
        # Liste gestite manualmente
    
    def _on_change(self):
        self._set_unsaved_changes(True)
    
    def _set_unsaved_changes(self, has_changes: bool):
        self._has_unsaved_changes = has_changes
        self.unsaved_label.setVisible(has_changes)
        self.unsaved_changes.emit(has_changes)
    
    def has_unsaved_changes(self) -> bool:
        return self._has_unsaved_changes
    
    def _browse_download_path(self):
        current_path = self.download_path_edit.text()
        path = QFileDialog.getExistingDirectory(self, "Seleziona cartella download", current_path if current_path else "")
        if path:
            self.download_path_edit.setText(path)
            self._set_unsaved_changes(True)
    
    # --- Gestione Account ---
    def _update_account_list(self):
        self.account_list.clear()
        config = config_manager.load_config()
        # Se ci sono modifiche pendenti, dovremmo usare la memoria locale?
        # Per semplicità, qui carichiamo da config, ma se abbiamo modificato ma non salvato?
        # In questo refactoring, le modifiche alla lista account sono immediate (in memoria config_manager)
        # o aspettiamo il salvataggio?
        # Il requisito dice: "Quando salvo le impostazioni, queste devono essere operative".
        # Quindi le liste (account e fornitori) dovrebbero essere "pendenti" fino al salva.
        # Tuttavia, Account Manager è complesso da fare "pendente".
        # Userò un approccio ibrido: leggo da config_manager ma modifico solo in memoria fino al save?
        # No, per semplicità userò una lista temporanea self._temp_accounts se volessi fare pure undo.
        # Ma per ora, faccio che le modifiche alla lista sono immediate nel widget, ma salvate su file solo al click di "Salva".
        pass

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
                # Aggiungi alla lista visuale
                is_default = self.account_list.count() == 0
                acc = {"username": u, "password": p, "default": is_default}
                self._render_accounts(self._get_current_accounts() + [acc])
                self._set_unsaved_changes(True)

    def _remove_account(self):
        row = self.account_list.currentRow()
        if row >= 0:
            self.account_list.takeItem(row)
            # Se rimosso default, eleggi il primo
            accounts = self._get_current_accounts()
            if accounts and not any(a['default'] for a in accounts):
                accounts[0]['default'] = True
                self._render_accounts(accounts)
            self._set_unsaved_changes(True)

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

    # --- Gestione Fornitori ---
    def _add_fornitore(self):
        text, ok = QInputDialog.getText(self, "Aggiungi Fornitore", "Inserisci il codice e nome:")
        if ok and text.strip():
             # Check duplicati
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
        self.download_path_edit.setText(config.get("download_path", ""))
        self.default_contract_edit.setText(config.get("default_contract_number", ""))
        
        # Fornitori
        self.fornitori_list.clear()
        for f in config.get("fornitori", []):
            self.fornitori_list.addItem(f)

        # Accounts
        self._render_accounts(config.get("accounts", []))
        
        self._set_unsaved_changes(False)
    
    def _save_settings(self):
        # Raccogli dati
        fornitori = [self.fornitori_list.item(i).text() for i in range(self.fornitori_list.count())]
        accounts = self._get_current_accounts()
        
        config_manager.set_config_value("browser_headless", self.headless_check.isChecked())
        config_manager.set_config_value("browser_timeout", self.timeout_spin.value())
        config_manager.set_config_value("download_path", self.download_path_edit.text())
        config_manager.set_config_value("default_contract_number", self.default_contract_edit.text())
        config_manager.set_config_value("fornitori", fornitori)
        config_manager.set_config_value("accounts", accounts)
        
        self._set_unsaved_changes(False)
        QMessageBox.information(self, "Salvataggio", "Impostazioni salvate.")
        
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
