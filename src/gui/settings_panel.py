"""
SyncroJob - Settings Panel
Pannello per la configurazione dell'applicazione.
Include gestione lista fornitori, tracking modifiche non salvate e statistiche.
"""

from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.backup_manager import BackupManager
from src.core.secrets_manager import SecretsManager
from src.core.stats_manager import StatsManager
from src.gui.widgets.toast import ToastManager


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
        self.toggle_pass_btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: 1px solid black;
                border-radius: 4px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
            }
        """
        )
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


class ConfirmationDialog(QDialog):
    """Dialog di conferma personalizzato con lo stesso layout di AccountDialog."""

    def __init__(self, parent=None, title="Conferma", message="Sei sicuro?"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(350)
        self.setStyleSheet("font-size: 15px; background-color: white;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Messaggio
        self.msg_label = QLabel(message)
        self.msg_label.setWordWrap(True)
        self.msg_label.setStyleSheet("color: #212529; font-weight: 500;")
        layout.addWidget(self.msg_label)

        # Pulsanti
        btns = QHBoxLayout()
        btns.setSpacing(10)

        self.ok_btn = QPushButton("Elimina")
        self.ok_btn.setMinimumHeight(40)
        self.ok_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """
        )
        self.ok_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("Annulla")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f8f9fa;
                color: #212529;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """
        )
        self.cancel_btn.clicked.connect(self.reject)

        btns.addWidget(self.ok_btn)
        btns.addWidget(self.cancel_btn)

        layout.addLayout(btns)


class StatisticsWidget(QWidget):
    """Widget per visualizzare le statistiche di utilizzo."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Header
        info = QLabel("Statistiche di Utilizzo Globale")
        info.setStyleSheet("font-size: 20px; font-weight: bold; color: #212529;")
        layout.addWidget(info)

        # Summary Cards Container
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(15)
        layout.addLayout(self.cards_layout)

        # Table Title
        table_title = QLabel("Dettaglio Attività")
        table_title.setStyleSheet(
            "font-size: 16px; font-weight: bold; margin-top: 10px; color: #495057;"
        )
        layout.addWidget(table_title)

        # Table
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Bot", "Esecuzioni", "Errori", "Ultima Esecuzione"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setStyleSheet(
            """
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                selection-background-color: #0d6efd;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                color: #495057;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #0d6efd;
                color: white;
            }
        """
        )
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.table)

        # Refresh Button
        refresh_btn = QPushButton("🔄 Aggiorna Statistiche")
        refresh_btn.setFixedWidth(200)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid black;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """
        )
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.refresh()

    def _create_summary_card(self, title, value, color, icon=""):
        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: white;
                border: 1px solid #dee2e6;
                border-left: 5px solid {color};
                border-radius: 8px;
            }}
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)

        lbl_title = QLabel(f"{icon} {title}")
        lbl_title.setStyleSheet(
            "color: #6c757d; font-size: 13px; font-weight: bold; border: none;"
        )
        layout.addWidget(lbl_title)

        lbl_val = QLabel(str(value))
        lbl_val.setStyleSheet(
            f"color: {color}; font-size: 28px; font-weight: 800; border: none;"
        )
        layout.addWidget(lbl_val)

        return card

    def refresh(self):
        """Ricarica le statistiche."""
        stats = StatsManager().get_all_stats()

        # 1. Update Cards
        # Clear previous cards
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        total_runs = sum(d.get("runs", 0) for d in stats.values())
        total_errors = sum(d.get("errors", 0) for d in stats.values())
        if total_runs > 0:
            ((total_runs - total_errors) / total_runs) * 100

        self.cards_layout.addWidget(
            self._create_summary_card("Esecuzioni Totali", total_runs, "#0d6efd", "🚀")
        )
        self.cards_layout.addWidget(
            self._create_summary_card("Errori Totali", total_errors, "#dc3545", "⚠️")
        )

        # 2. Update Table
        self.table.setRowCount(0)

        bot_names = {
            "timbrature": "⏱️ Timbrature",
            "scarico_ts": "📥 Scarico TS",
            "carico_ts": "📤 Carico TS",
            "dettagli_oda": "📋 Dettagli OdA",
        }

        sorted_keys = sorted(stats.keys())

        for bot_id in sorted_keys:
            data = stats[bot_id]
            row = self.table.rowCount()
            self.table.insertRow(row)

            name = bot_names.get(bot_id, bot_id.capitalize())
            runs = data.get("runs", 0)
            errors = data.get("errors", 0)
            last_run = data.get("last_run", "")

            # Calc rate
            if runs > 0:
                ((runs - errors) / runs) * 100

            # Format date
            last_run_display = "Mai"
            if last_run:
                try:
                    from datetime import datetime

                    dt = datetime.fromisoformat(last_run)
                    last_run_display = dt.strftime("%d/%m/%Y %H:%M")
                except Exception:
                    last_run_display = last_run

            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(str(runs)))

            err_item = QTableWidgetItem(str(errors))
            if errors > 0:
                err_item.setForeground(Qt.GlobalColor.red)
                err_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            self.table.setItem(row, 2, err_item)

            self.table.setItem(row, 3, QTableWidgetItem(last_run_display))


class SettingsPanel(QWidget):
    """Pannello per le impostazioni dell'applicazione."""

    # Segnale emesso quando ci sono modifiche non salvate
    unsaved_changes = pyqtSignal(bool)
    # Segnale emesso quando le impostazioni vengono salvate
    settings_saved = pyqtSignal()
    # Segnale per richiedere l'apertura di una sezione della guida
    request_help_section = pyqtSignal(str)

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

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            """
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
            }
            QTabBar::tab {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 8px 20px;
                margin-right: 2px;
                color: #495057;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
                color: #0d6efd;
            }
        """
        )
        main_layout.addWidget(self.tabs)

        # --- TAB 1: Configurazione ---
        config_tab = QWidget()
        config_layout = QVBoxLayout(config_tab)

        # Scroll area per il contenuto config
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

        self.headless_check = QCheckBox("Esegui in modalità Headless (Nascosta)")
        self.headless_check.setToolTip(
            "Se attivato, il browser verrà eseguito in background senza mostrare la finestra."
        )
        self.headless_check.setStyleSheet(
            "QCheckBox { padding: 5px; font-size: 15px; font-weight: bold; color: #d63384; }"
        )
        general_layout.addWidget(self.headless_check)

        scroll_layout.addWidget(general_group)

        # --- CONTAINER ORIZZONTALE PER LISTE ---
        lists_container = QHBoxLayout()
        lists_container.setSpacing(15)

        # 1. Sezione Account
        account_group = self._create_group_box("🔐 Account ISAB")
        account_layout = QVBoxLayout(account_group)
        self.groups.append(account_group)

        self.account_list = QListWidget()
        self.account_list.setMaximumHeight(100)
        self.account_list.setStyleSheet(self._list_style())
        self.account_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.account_list.customContextMenuRequested.connect(
            lambda pos: self._show_account_context_menu(pos)
        )
        account_layout.addWidget(self.account_list)

        acc_btns = QHBoxLayout()
        add_acc_btn = QPushButton("➕")
        add_acc_btn.setToolTip("Aggiungi Account")
        add_acc_btn.clicked.connect(self._add_account)
        self._style_mini_button(add_acc_btn, "#28a745")
        acc_btns.addWidget(add_acc_btn)

        edit_acc_btn = QPushButton("✏️")
        edit_acc_btn.setToolTip("Modifica Account")
        edit_acc_btn.clicked.connect(self._edit_account)
        self._style_mini_button(edit_acc_btn, "#0d6efd")
        acc_btns.addWidget(edit_acc_btn)

        remove_acc_btn = QPushButton("🗑️")
        remove_acc_btn.setToolTip("Rimuovi Account")
        remove_acc_btn.clicked.connect(self._remove_account)
        self._style_mini_button(remove_acc_btn, "#dc3545")
        acc_btns.addWidget(remove_acc_btn)

        set_def_btn = QPushButton("⭐")
        set_def_btn.setToolTip("Imposta Default")
        set_def_btn.clicked.connect(self._set_default_account)
        self._style_mini_button(set_def_btn, "#ffc107", text_color="black")
        acc_btns.addWidget(set_def_btn)
        acc_btns.addStretch()
        account_layout.addLayout(acc_btns)

        lists_container.addWidget(account_group)

        # 1.5 Sezione Account SafeWork (Nuova)
        sw_account_group = self._create_group_box("🛡️ Account SafeWork")
        sw_account_layout = QVBoxLayout(sw_account_group)
        self.groups.append(sw_account_group)

        self.sw_account_list = QListWidget()
        self.sw_account_list.setMaximumHeight(100)
        self.sw_account_list.setStyleSheet(self._list_style())
        self.sw_account_list.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.sw_account_list.customContextMenuRequested.connect(
            lambda pos: self._show_sw_account_context_menu(pos)
        )
        sw_account_layout.addWidget(self.sw_account_list)

        sw_acc_btns = QHBoxLayout()
        add_sw_btn = QPushButton("➕")
        add_sw_btn.setToolTip("Aggiungi Account SafeWork")
        add_sw_btn.clicked.connect(self._add_sw_account)
        self._style_mini_button(add_sw_btn, "#28a745")
        sw_acc_btns.addWidget(add_sw_btn)

        edit_sw_btn = QPushButton("✏️")
        edit_sw_btn.setToolTip("Modifica Account")
        edit_sw_btn.clicked.connect(self._edit_sw_account)
        self._style_mini_button(edit_sw_btn, "#0d6efd")
        sw_acc_btns.addWidget(edit_sw_btn)

        rem_sw_btn = QPushButton("🗑️")
        rem_sw_btn.setToolTip("Rimuovi Account")
        rem_sw_btn.clicked.connect(self._remove_sw_account)
        self._style_mini_button(rem_sw_btn, "#dc3545")
        sw_acc_btns.addWidget(rem_sw_btn)

        def_sw_btn = QPushButton("⭐")
        def_sw_btn.setToolTip("Imposta Default")
        def_sw_btn.clicked.connect(self._set_default_sw_account)
        self._style_mini_button(def_sw_btn, "#ffc107", text_color="black")
        sw_acc_btns.addWidget(def_sw_btn)
        sw_acc_btns.addStretch()
        sw_account_layout.addLayout(sw_acc_btns)

        lists_container.addWidget(sw_account_group)

        # 2. Sezione Contratti
        contract_group = self._create_group_box("📋 Contratti")
        contract_layout = QVBoxLayout(contract_group)
        self.groups.append(contract_group)

        self.contract_list = QListWidget()
        self.contract_list.setMaximumHeight(130)
        self.contract_list.setStyleSheet(self._list_style())
        self.contract_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.contract_list.customContextMenuRequested.connect(
            lambda pos: self._show_generic_list_menu(
                pos,
                self.contract_list,
                self._add_contract,
                self._edit_contract,
                self._remove_contract,
            )
        )
        contract_layout.addWidget(self.contract_list)

        contract_btns = QHBoxLayout()
        add_contract_btn = QPushButton("➕")
        add_contract_btn.setToolTip("Aggiungi Contratto")
        add_contract_btn.clicked.connect(self._add_contract)
        self._style_mini_button(add_contract_btn, "#28a745")
        contract_btns.addWidget(add_contract_btn)

        edit_contract_btn = QPushButton("✏️")
        edit_contract_btn.setToolTip("Modifica Contratto")
        edit_contract_btn.clicked.connect(self._edit_contract)
        self._style_mini_button(edit_contract_btn, "#0d6efd")
        contract_btns.addWidget(edit_contract_btn)

        remove_contract_btn = QPushButton("🗑️")
        remove_contract_btn.setToolTip("Rimuovi Contratto")
        remove_contract_btn.clicked.connect(self._remove_contract)
        self._style_mini_button(remove_contract_btn, "#dc3545")
        contract_btns.addWidget(remove_contract_btn)
        contract_btns.addStretch()
        contract_layout.addLayout(contract_btns)

        lists_container.addWidget(contract_group)

        # 3. Sezione Fornitori
        fornitori_group = self._create_group_box("🏢 Fornitori")
        fornitori_layout = QVBoxLayout(fornitori_group)
        self.groups.append(fornitori_group)

        self.fornitori_list = QListWidget()
        self.fornitori_list.setMaximumHeight(100)
        self.fornitori_list.setStyleSheet(self._list_style())
        self.fornitori_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.fornitori_list.customContextMenuRequested.connect(
            lambda pos: self._show_generic_list_menu(
                pos,
                self.fornitori_list,
                self._add_fornitore,
                self._edit_fornitore,
                self._remove_fornitore,
            )
        )
        fornitori_layout.addWidget(self.fornitori_list)

        fornitori_btn_layout = QHBoxLayout()
        add_forn_btn = QPushButton("➕")
        add_forn_btn.setToolTip("Aggiungi Fornitore")
        add_forn_btn.clicked.connect(self._add_fornitore)
        self._style_mini_button(add_forn_btn, "#28a745")
        fornitori_btn_layout.addWidget(add_forn_btn)

        edit_forn_btn = QPushButton("✏️")
        edit_forn_btn.setToolTip("Modifica Fornitore")
        edit_forn_btn.clicked.connect(self._edit_fornitore)
        self._style_mini_button(edit_forn_btn, "#0d6efd")
        fornitori_btn_layout.addWidget(edit_forn_btn)

        rem_forn_btn = QPushButton("🗑️")
        rem_forn_btn.setToolTip("Rimuovi Fornitore")
        rem_forn_btn.clicked.connect(self._remove_fornitore)
        self._style_mini_button(rem_forn_btn, "#dc3545")
        fornitori_btn_layout.addWidget(rem_forn_btn)
        fornitori_btn_layout.addStretch()
        fornitori_layout.addLayout(fornitori_btn_layout)

        lists_container.addWidget(fornitori_group)

        scroll_layout.addLayout(lists_container)

        # --- CONTAINER ORIZZONTALE PER LISTE TIMBRATURE ---
        timbrature_lists_container = QHBoxLayout()
        timbrature_lists_container.setSpacing(15)

        # 4. Sezione Reparti
        reparti_group = self._create_group_box("🏢 Reparti (Timbrature)")
        reparti_layout = QVBoxLayout(reparti_group)
        self.groups.append(reparti_group)

        self.reparti_list = QListWidget()
        self.reparti_list.setMaximumHeight(100)
        self.reparti_list.setStyleSheet(self._list_style())
        self.reparti_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.reparti_list.customContextMenuRequested.connect(
            lambda pos: self._show_generic_list_menu(
                pos,
                self.reparti_list,
                self._add_reparto,
                self._edit_reparto,
                self._remove_reparto,
            )
        )
        reparti_layout.addWidget(self.reparti_list)

        reparti_btn_layout = QHBoxLayout()
        add_rep_btn = QPushButton("➕")
        add_rep_btn.setToolTip("Aggiungi Reparto")
        add_rep_btn.clicked.connect(self._add_reparto)
        self._style_mini_button(add_rep_btn, "#28a745")
        reparti_btn_layout.addWidget(add_rep_btn)

        edit_rep_btn = QPushButton("✏️")
        edit_rep_btn.setToolTip("Modifica Reparto")
        edit_rep_btn.clicked.connect(self._edit_reparto)
        self._style_mini_button(edit_rep_btn, "#0d6efd")
        reparti_btn_layout.addWidget(edit_rep_btn)

        rem_rep_btn = QPushButton("🗑️")
        rem_rep_btn.setToolTip("Rimuovi Reparto")
        rem_rep_btn.clicked.connect(self._remove_reparto)
        self._style_mini_button(rem_rep_btn, "#dc3545")
        reparti_btn_layout.addWidget(rem_rep_btn)
        reparti_btn_layout.addStretch()
        reparti_layout.addLayout(reparti_btn_layout)

        timbrature_lists_container.addWidget(reparti_group)

        # 5. Sezione Cantieri
        cantieri_group = self._create_group_box("🏗️ Cantieri (Timbrature)")
        cantieri_layout = QVBoxLayout(cantieri_group)
        self.groups.append(cantieri_group)

        self.cantieri_list = QListWidget()
        self.cantieri_list.setMaximumHeight(100)
        self.cantieri_list.setStyleSheet(self._list_style())
        self.cantieri_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.cantieri_list.customContextMenuRequested.connect(
            lambda pos: self._show_generic_list_menu(
                pos,
                self.cantieri_list,
                self._add_cantiere,
                self._edit_cantiere,
                self._remove_cantiere,
            )
        )
        cantieri_layout.addWidget(self.cantieri_list)

        cantieri_btn_layout = QHBoxLayout()
        add_cant_btn = QPushButton("➕")
        add_cant_btn.setToolTip("Aggiungi Cantiere")
        add_cant_btn.clicked.connect(self._add_cantiere)
        self._style_mini_button(add_cant_btn, "#28a745")
        cantieri_btn_layout.addWidget(add_cant_btn)

        edit_cant_btn = QPushButton("✏️")
        edit_cant_btn.setToolTip("Modifica Cantiere")
        edit_cant_btn.clicked.connect(self._edit_cantiere)
        self._style_mini_button(edit_cant_btn, "#0d6efd")
        cantieri_btn_layout.addWidget(edit_cant_btn)

        rem_cant_btn = QPushButton("🗑️")
        rem_cant_btn.setToolTip("Rimuovi Cantiere")
        rem_cant_btn.clicked.connect(self._remove_cantiere)
        self._style_mini_button(rem_cant_btn, "#dc3545")
        cantieri_btn_layout.addWidget(rem_cant_btn)
        cantieri_btn_layout.addStretch()
        cantieri_layout.addLayout(cantieri_btn_layout)

        timbrature_lists_container.addWidget(cantieri_group)

        scroll_layout.addLayout(timbrature_lists_container)

        # --- Sezione Strumentale ---
        contabilita_group = self._create_group_box("📊 Strumentale")
        contabilita_layout = QVBoxLayout(contabilita_group)
        self.groups.append(contabilita_group)

        # Path input
        path_label = QLabel("File bilancio strumentale:")
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
        self.auto_update_contabilita_check = QCheckBox(
            "Attiva aggiornamento automatico all'avvio (background)"
        )
        self.auto_update_contabilita_check.setStyleSheet(
            "padding: 5px; font-size: 15px; font-weight: normal;"
        )
        contabilita_layout.addWidget(self.auto_update_contabilita_check)

        # Giornaliere Path input
        giornaliere_label = QLabel("Cartella Giornaliere (Root):")
        giornaliere_label.setStyleSheet(
            "font-size: 14px; font-weight: normal; margin-top: 10px;"
        )
        contabilita_layout.addWidget(giornaliere_label)

        giornaliere_path_layout = QHBoxLayout()
        self.giornaliere_path_edit = QLineEdit()
        self.giornaliere_path_edit.setPlaceholderText(
            "Seleziona la cartella root delle Giornaliere..."
        )
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
        attivita_label.setStyleSheet(
            "font-size: 14px; font-weight: normal; margin-top: 10px;"
        )
        contabilita_layout.addWidget(attivita_label)

        attivita_path_layout = QHBoxLayout()
        self.attivita_path_edit = QLineEdit()
        self.attivita_path_edit.setPlaceholderText(
            "Seleziona file Attività Programmate..."
        )
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
        certificati_label.setStyleSheet(
            "font-size: 14px; font-weight: normal; margin-top: 10px;"
        )
        contabilita_layout.addWidget(certificati_label)

        certificati_path_layout = QHBoxLayout()
        self.certificati_path_edit = QLineEdit()
        self.certificati_path_edit.setPlaceholderText(
            "Seleziona file Certificati Campione..."
        )
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
        self.dataease_path_edit.setPlaceholderText(
            "Seleziona file Excel scarico ore..."
        )
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
        diag_layout = QHBoxLayout(diag_group)
        diag_layout.setSpacing(15)
        self.groups.append(diag_group)

        diag_label = QLabel("Gestione file di log e licenza:")
        diag_label.setStyleSheet("font-size: 14px;")
        diag_layout.addWidget(diag_label)

        diag_layout.addStretch()

        open_folder_btn = QPushButton("📂 Apri Cartella Dati")
        open_folder_btn.clicked.connect(self._open_data_folder)
        self._style_button(open_folder_btn)
        diag_layout.addWidget(open_folder_btn)

        scroll_layout.addWidget(diag_group)

        scroll_layout.addStretch()
        self.scroll.setWidget(self.scroll_content)
        config_layout.addWidget(self.scroll)

        # --- Pulsanti azione (Config Tab) - NASCOSTI (Salvataggio Automatico) ---
        self.action_container = QWidget()
        action_layout = QHBoxLayout(self.action_container)
        action_layout.addStretch()

        self.unsaved_label = QLabel("⚠️ Modifiche non salvate")
        self.unsaved_label.setStyleSheet(
            "color: #dc3545; font-weight: bold; padding: 5px 10px; font-size: 15px;"
        )
        self.unsaved_label.setVisible(False)
        action_layout.addWidget(self.unsaved_label)

        self.reset_btn = QPushButton("↩️ Annulla")
        self.reset_btn.setVisible(False) # Nascosto
        action_layout.addWidget(self.reset_btn)

        self.save_btn = QPushButton("💾 Salva impostazioni")
        self.save_btn.setVisible(False) # Nascosto
        action_layout.addWidget(self.save_btn)

        config_layout.addWidget(self.action_container)
        self.action_container.setVisible(False) # Nascondi l'intero container

        # Add Config Tab
        self.tabs.addTab(config_tab, "Configurazione")

        # --- TAB 2: Backup ---
        self.backup_tab = QWidget()
        self._setup_backup_tab(self.backup_tab)
        self.tabs.addTab(self.backup_tab, "☁️ Backup Cloud")

        # --- TAB 3: Statistiche ---
        self.stats_widget = StatisticsWidget()
        self.tabs.addTab(self.stats_widget, "Statistiche")

        # --- TAB 4: Telegram ---
        self.telegram_tab = QWidget()
        self._setup_telegram_tab(self.telegram_tab)
        self.tabs.addTab(self.telegram_tab, "✈️ Telegram")

        # Refresh stats when tab is clicked
        self.tabs.currentChanged.connect(self._on_tab_changed)

    def _setup_telegram_tab(self, parent_widget):
        layout = QVBoxLayout(parent_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_layout = QHBoxLayout()
        info = QLabel("Controllo Remoto Telegram")
        info.setStyleSheet("font-size: 20px; font-weight: bold; color: #212529;")
        header_layout.addWidget(info)

        header_layout.addStretch()

        help_btn = QPushButton("📖 Guida alla configurazione")
        help_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        help_btn.clicked.connect(
            lambda: self.request_help_section.emit("Configurazione Telegram")
        )
        help_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e7f1ff;
                color: #0d6efd;
                border: 1px solid #0d6efd;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #cfe2ff;
            }
        """
        )
        header_layout.addWidget(help_btn)
        layout.addLayout(header_layout)

        desc = QLabel(
            "Controlla SyncroJob dal tuo smartphone. Avvia bot, controlla lo stato e ricevi notifiche."
        )
        desc.setStyleSheet("color: #6c757d; font-size: 14px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Config Group
        group = self._create_group_box("Configurazione Bot")
        gl = QFormLayout(group)
        gl.setSpacing(15)

        self.tg_token_edit = QLineEdit()
        self.tg_token_edit.setPlaceholderText(
            "Inserisci il Token fornito da @BotFather"
        )
        self.tg_token_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.tg_token_edit.setMinimumHeight(40)
        self.tg_token_edit.textChanged.connect(self._on_change)
        self._style_input(self.tg_token_edit)
        gl.addRow("API Token:", self.tg_token_edit)

        self.tg_chat_id_edit = QLineEdit()
        self.tg_chat_id_edit.setPlaceholderText("In attesa del primo messaggio...")
        self.tg_chat_id_edit.setReadOnly(True)
        self.tg_chat_id_edit.setMinimumHeight(40)
        self._style_input(self.tg_chat_id_edit)

        tg_id_layout = QHBoxLayout()
        tg_id_layout.addWidget(self.tg_chat_id_edit)

        self.tg_reset_btn = QPushButton("Scollega")
        self.tg_reset_btn.setFixedWidth(80)
        self.tg_reset_btn.setMinimumHeight(40)
        self.tg_reset_btn.clicked.connect(self._reset_telegram_pairing)
        self.tg_reset_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                color: #dc3545;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fff5f5;
                border-color: #dc3545;
            }
        """
        )
        tg_id_layout.addWidget(self.tg_reset_btn)

        gl.addRow("Chat ID Autorizzato:", tg_id_layout)

        # Gemini API Key (Nuova)
        self.gemini_api_key_edit = QLineEdit()
        self.gemini_api_key_edit.setPlaceholderText(
            "Inserisci la Gemini API Key per l'AI Coach"
        )
        self.gemini_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.gemini_api_key_edit.setMinimumHeight(40)
        self.gemini_api_key_edit.textChanged.connect(self._on_change)
        self._style_input(self.gemini_api_key_edit)

        gemini_layout = QHBoxLayout()
        gemini_layout.addWidget(self.gemini_api_key_edit)

        self.gemini_toggle_btn = QPushButton("👁️")
        self.gemini_toggle_btn.setFixedSize(40, 40)
        self.gemini_toggle_btn.clicked.connect(self._toggle_gemini_visibility)
        self.gemini_toggle_btn.setStyleSheet(
            "background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px;"
        )
        gemini_layout.addWidget(self.gemini_toggle_btn)

        gl.addRow("Gemini API Key:", gemini_layout)

        layout.addWidget(group)
        layout.addStretch()

    def _reset_telegram_pairing(self):
        """Cancella l'associazione corrente del bot Telegram."""
        if not self.tg_chat_id_edit.text():
            return

        res = QMessageBox.warning(
            self,
            "Scollega Telegram",
            "Vuoi davvero scollegare il dispositivo corrente?\nAl prossimo avvio del bot dovrai inviare di nuovo /start per associarlo.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if res == QMessageBox.StandardButton.Yes:
            self.tg_chat_id_edit.clear()
            self._on_change()
            ToastManager.instance().show(
                "Dispositivo Telegram scollegato. Salva per applicare.", "warning"
            )

    def _toggle_gemini_visibility(self):
        """Alterna la visibilità della Gemini API Key."""
        if self.gemini_api_key_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.gemini_api_key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.gemini_toggle_btn.setText("🔒")
        else:
            self.gemini_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.gemini_toggle_btn.setText("👁️")

    def _setup_backup_tab(self, parent_widget):
        layout = QVBoxLayout(parent_widget)
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
        self.cloud_combo.setStyleSheet(
            """
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
                background-color: white;
            }
        """
        )

        # Populate
        # Always add Local option first
        self.cloud_combo.addItem("📂 Locale (Documenti)", "Local")

        # Add detected clouds
        if clouds:
            for name, path in clouds.items():
                self.cloud_combo.addItem(f"☁️ {name} ({path})", name)

        # Load selection
        config = config_manager.load_config()
        saved_cloud = config.get("backup_cloud_provider")
        if saved_cloud:
            index = self.cloud_combo.findData(saved_cloud)
            if index >= 0:
                self.cloud_combo.setCurrentIndex(index)

        # Save on change
        self.cloud_combo.currentIndexChanged.connect(self._save_cloud_preference)

        status_layout.addWidget(self.cloud_combo)
        layout.addWidget(status_group)

        # Settings & Actions combined
        sett_group = QGroupBox("Impostazioni")
        sett_layout = QHBoxLayout(sett_group)
        sett_layout.setSpacing(15)

        self.auto_backup_check = QCheckBox("Esegui backup automatico alla chiusura")
        config = config_manager.load_config()
        self.auto_backup_check.setChecked(config.get("auto_backup", True))
        self.auto_backup_check.stateChanged.connect(
            lambda: config_manager.set_config_value(
                "auto_backup", self.auto_backup_check.isChecked()
            )
        )
        sett_layout.addWidget(self.auto_backup_check)

        sett_layout.addStretch()  # Push buttons to the right

        backup_btn = QPushButton("☁️ Esegui Backup Ora")
        # Removed setMinimumHeight(45) to reduce bulk
        backup_btn.setStyleSheet(
            """
            QPushButton {
                background-color: white; color: black; border: 1px solid black; border-radius: 6px; font-weight: bold; font-size: 14px; padding: 8px 15px;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """
        )
        backup_btn.clicked.connect(self._run_manual_backup)
        sett_layout.addWidget(backup_btn)

        open_folder_btn = QPushButton("📂 Apri Cartella Backup")
        # Removed setMinimumHeight(45)
        open_folder_btn.setStyleSheet(
            """
            QPushButton {
                background-color: white; color: black; border: 1px solid black; border-radius: 6px; font-weight: bold; font-size: 14px; padding: 8px 15px;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """
        )
        open_folder_btn.clicked.connect(self._open_backup_folder)
        sett_layout.addWidget(open_folder_btn)

        layout.addWidget(sett_group)

        # Restore Section
        restore_group = self._create_group_box("Ripristino Backup")
        restore_layout = QVBoxLayout(restore_group)

        restore_label = QLabel("Seleziona un backup da ripristinare:")
        restore_layout.addWidget(restore_label)

        restore_controls = QHBoxLayout()

        self.restore_combo = QComboBox()
        self.restore_combo.setMinimumHeight(40)
        self.restore_combo.setStyleSheet(
            """
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
                background-color: white;
            }
        """
        )
        restore_controls.addWidget(self.restore_combo)

        self.refresh_backups_btn = QPushButton("🔄")
        self.refresh_backups_btn.setToolTip("Aggiorna lista backup")
        self.refresh_backups_btn.setFixedSize(32, 32)  # Standard size
        self.refresh_backups_btn.clicked.connect(self._refresh_backups_list)
        self._style_mini_button(self.refresh_backups_btn, "#6c757d")
        restore_controls.addWidget(self.refresh_backups_btn)

        self.restore_btn = QPushButton("↩️ Ripristina")
        self.restore_btn.clicked.connect(self._restore_selected_backup)
        self._style_button(self.restore_btn)  # Use standard button style
        restore_controls.addWidget(self.restore_btn)

        restore_layout.addLayout(restore_controls)
        layout.addWidget(restore_group)

        # Initial populate
        self._refresh_backups_list()

        layout.addStretch()

    def _save_cloud_preference(self):
        """Salva il provider cloud selezionato."""
        provider = self.cloud_combo.currentData()
        if provider:
            config_manager.set_config_value("backup_cloud_provider", provider)

    def _run_manual_backup(self):
        success, msg = BackupManager.create_backup()
        if success:
            from src.gui.widgets.toast import ToastManager

            ToastManager.instance().show(f"Backup completato!\n{msg}", "success")
            self._refresh_backups_list()
        else:
            QMessageBox.warning(self, "Errore Backup", msg)

    def _open_backup_folder(self):
        path = BackupManager.get_backup_dir()
        from src.utils.helpers import open_folder

        open_folder(str(path))

    def _refresh_backups_list(self):
        """Aggiorna la lista dei backup disponibili."""
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
                # Extract timestamp from filename: BotTS_Backup_YYYYMMDD_HHMMSS.zip
                ts_str = name.replace("BotTS_Backup_", "").replace(".zip", "")
                dt = datetime.strptime(ts_str, "%Y%m%d_%H%M%S")
                display = dt.strftime("%d/%m/%Y %H:%M:%S")

                size_kb = backup_path.stat().st_size // 1024
                display += f" ({size_kb} KB)"

                self.restore_combo.addItem(display, str(backup_path))
            except Exception:
                self.restore_combo.addItem(backup_path.name, str(backup_path))

    def _restore_selected_backup(self):
        """Esegue il ripristino del backup selezionato."""
        path = self.restore_combo.currentData()
        if not path:
            return

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Conferma Ripristino")
        msg_box.setText(
            "ATTENZIONE: Il ripristino sovrascriverà le impostazioni e i dati attuali.\n"
            "L'applicazione potrebbe richiedere un riavvio.\n\n"
            "Sei sicuro di voler procedere?"
        )
        msg_box.setIcon(QMessageBox.Icon.Question)

        # Add custom buttons for better control over text and styling
        btn_si = msg_box.addButton("Si", QMessageBox.ButtonRole.YesRole)
        btn_no = msg_box.addButton("No", QMessageBox.ButtonRole.NoRole)

        # Apply objectNames for specific styling from QSS
        btn_si.setObjectName("qt_msgbox_buttonbox_yes")
        btn_no.setObjectName("qt_msgbox_buttonbox_no")

        msg_box.setDefaultButton(btn_si)  # Set 'Si' as default

        msg_box.exec()

        if msg_box.clickedButton() == btn_si:
            success, msg = BackupManager.restore_backup(path)
            if success:
                QMessageBox.information(self, "Ripristino Completato", msg)
                self._load_settings()
            else:
                QMessageBox.critical(self, "Errore Ripristino", msg)

    def _on_tab_changed(self, index):
        if self.tabs.tabText(index) == "Statistiche":
            self.stats_widget.refresh()

    def _create_group_box(self, title: str) -> QGroupBox:
        group = QGroupBox(title)
        group.setStyleSheet(
            """
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
        """
        )
        return group

    def _list_style(self):
        return """
            QListWidget {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
            }
        """

    def _style_input(self, widget):
        widget.setStyleSheet(
            """
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
        """
        )

    def _style_button(self, button):
        button.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid black;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """
        )

    def _style_mini_button(self, button, color, text_color="black"):
        button.setFixedSize(32, 32)
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: white;
                color: black;
                border: 1px solid black;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
                padding: 0px;
                margin: 0px;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
                border-color: {color};
            }}
        """
        )

    def _connect_change_signals(self):
        # Generale
        self.headless_check.stateChanged.connect(self._save_settings)

        # Browser
        self.timeout_spin.valueChanged.connect(self._save_settings)

        # Strumentale (Save on editing finished to avoid spamming disk)
        self.contabilita_path_edit.textChanged.connect(self._save_settings)
        self.giornaliere_path_edit.textChanged.connect(self._save_settings)
        self.attivita_path_edit.textChanged.connect(self._save_settings)
        self.certificati_path_edit.textChanged.connect(self._save_settings)
        self.auto_update_contabilita_check.stateChanged.connect(self._save_settings)
        self.dataease_path_edit.textChanged.connect(self._save_settings)

        # Telegram
        self.tg_token_edit.editingFinished.connect(self._save_settings)
        self.gemini_api_key_edit.editingFinished.connect(self._save_settings)

    def _on_change(self):
        """Metodo mantenuto per compatibilità, ora chiama il salvataggio diretto."""
        self._save_settings()

    def _set_unsaved_changes(self, has_changes: bool):
        """Ora ridondante con il salvataggio automatico."""
        self._has_unsaved_changes = False
        self.unsaved_label.setVisible(False)
        self.unsaved_changes.emit(False)

    def has_unsaved_changes(self) -> bool:
        """Sempre False con salvataggio automatico."""
        return False

    def _open_data_folder(self):
        """Apre la cartella dei dati (logs, config, licenza)."""
        from PyQt6.QtCore import QUrl
        from PyQt6.QtGui import QDesktopServices

        folder = config_manager.CONFIG_DIR
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    def _browse_contabilita_path(self):
        current_path = self.contabilita_path_edit.text()
        directory = str(Path(current_path).parent) if current_path else str(Path.home())

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file Excel Contabilità",
            directory,
            "Excel Files (*.xlsx *.xlsm *.xls)",
        )
        if path:
            self.contabilita_path_edit.setText(path)
            self._save_settings()

    def _browse_giornaliere_path(self):
        current_path = self.giornaliere_path_edit.text()
        path = QFileDialog.getExistingDirectory(
            self,
            "Seleziona Cartella Root Giornaliere",
            current_path if current_path else str(Path.home()),
        )
        if path:
            self.giornaliere_path_edit.setText(path)
            self._save_settings()

    def _browse_attivita_path(self):
        current_path = self.attivita_path_edit.text()
        directory = str(Path(current_path).parent) if current_path else str(Path.home())

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file Attività Programmate",
            directory,
            "Excel Files (*.xlsx *.xlsm *.xls)",
        )
        if path:
            self.attivita_path_edit.setText(path)
            self._save_settings()

    def _browse_certificati_path(self):
        current_path = self.certificati_path_edit.text()
        directory = str(Path(current_path).parent) if current_path else str(Path.home())

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file Certificati Campione",
            directory,
            "Excel Files (*.xlsx *.xlsm *.xls)",
        )
        if path:
            self.certificati_path_edit.setText(path)
            self._save_settings()

    def _browse_dataease_path(self):
        current_path = self.dataease_path_edit.text()
        directory = str(Path(current_path).parent) if current_path else str(Path.home())

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file DataEase (Scarico Ore)",
            directory,
            "Excel Files (*.xlsx *.xlsm *.xls)",
        )
        if path:
            self.dataease_path_edit.setText(path)
            self._save_settings()

    # --- Gestione Account ---
    def _render_accounts(self, accounts):
        self.account_list.clear()
        for acc in accounts:
            label = acc["username"]
            if acc.get("default"):
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
                self._save_settings()

    def _edit_account(self):
        """Modifica l'account selezionato."""
        item = self.account_list.currentItem()
        if not item:
            QMessageBox.information(self, "Info", "Seleziona un account da modificare.")
            return

        acc_data = item.data(Qt.ItemDataRole.UserRole)
        dlg = AccountDialog(
            self, username=acc_data["username"], password=acc_data["password"]
        )

        if dlg.exec():
            new_u, new_p = dlg.get_data()
            if new_u:
                # Aggiorna dati
                acc_data["username"] = new_u
                acc_data["password"] = new_p
                # Renderizza di nuovo la lista per aggiornare la label
                self._render_accounts(self._get_current_accounts())
                self._save_settings()

    def _confirm_delete(self, item_name):
        """Mostra un dialog di conferma eliminazione stilizzato (layout coerente con AccountDialog)."""
        dlg = ConfirmationDialog(
            self,
            title="Conferma Eliminazione",
            message=f"Sei sicuro di voler rimuovere '{item_name}'?"
        )
        return dlg.exec() == QDialog.DialogCode.Accepted

    def _remove_account(self):
        row = self.account_list.currentRow()
        if row >= 0:
            item = self.account_list.item(row)
            acc = item.data(Qt.ItemDataRole.UserRole)
            if self._confirm_delete(acc.get("username", "Account")):
                self.account_list.takeItem(row)
                accounts = self._get_current_accounts()
                if accounts and not any(a["default"] for a in accounts):
                    accounts[0]["default"] = True
                    self._render_accounts(accounts)
                self._save_settings()

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

    def _show_generic_list_menu(
        self, position, list_widget, add_cb, edit_cb, remove_cb
    ):
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
                acc["default"] = i == row
            self._render_accounts(accounts)
            self._save_settings()

    def _get_current_accounts(self):
        accounts = []
        for i in range(self.account_list.count()):
            item = self.account_list.item(i)
            accounts.append(item.data(Qt.ItemDataRole.UserRole))
        return accounts

    # --- Gestione Account SafeWork ---
    def _render_sw_accounts(self, accounts):
        self.sw_account_list.clear()
        for acc in accounts:
            label = acc["username"]
            if acc.get("default"):
                label += " (⭐ Default)"
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, acc)
            self.sw_account_list.addItem(item)

    def _add_sw_account(self):
        dlg = AccountDialog(self)
        dlg.setWindowTitle("Account SafeWork")
        if dlg.exec():
            u, p = dlg.get_data()
            if u:
                is_default = self.sw_account_list.count() == 0
                acc = {"username": u, "password": p, "default": is_default}
                self._render_sw_accounts(self._get_current_sw_accounts() + [acc])
                self._save_settings()

    def _edit_sw_account(self):
        item = self.sw_account_list.currentItem()
        if not item:
            return
        acc_data = item.data(Qt.ItemDataRole.UserRole)
        dlg = AccountDialog(
            self, username=acc_data["username"], password=acc_data["password"]
        )
        dlg.setWindowTitle("Modifica SafeWork")
        if dlg.exec():
            u, p = dlg.get_data()
            if u:
                acc_data["username"] = u
                acc_data["password"] = p
                self._render_sw_accounts(self._get_current_sw_accounts())
                self._save_settings()

    def _remove_sw_account(self):
        row = self.sw_account_list.currentRow()
        if row >= 0:
            if (
                QMessageBox.question(self, "Conferma", "Rimuovere account SafeWork?")
                == QMessageBox.StandardButton.Yes
            ):
                self.sw_account_list.takeItem(row)
                accounts = self._get_current_sw_accounts()
                if accounts and not any(a["default"] for a in accounts):
                    accounts[0]["default"] = True
                    self._render_sw_accounts(accounts)
                self._save_settings()

    def _set_default_sw_account(self):
        row = self.sw_account_list.currentRow()
        if row >= 0:
            accounts = self._get_current_sw_accounts()
            for i, acc in enumerate(accounts):
                acc["default"] = i == row
            self._render_sw_accounts(accounts)
            self._save_settings()

    def _get_current_sw_accounts(self):
        accounts = []
        for i in range(self.sw_account_list.count()):
            item = self.sw_account_list.item(i)
            accounts.append(item.data(Qt.ItemDataRole.UserRole))
        return accounts

    def _show_sw_account_context_menu(self, position):
        menu = QMenu()
        item = self.sw_account_list.itemAt(position)
        add_action = QAction("➕ Aggiungi account", self)
        add_action.triggered.connect(self._add_sw_account)
        menu.addAction(add_action)
        if item:
            self.sw_account_list.setCurrentItem(item)
            menu.addSeparator()
            edit_action = QAction("✏️ Modifica", self)
            edit_action.triggered.connect(self._edit_sw_account)
            menu.addAction(edit_action)
            default_action = QAction("⭐ Imposta Default", self)
            default_action.triggered.connect(self._set_default_sw_account)
            menu.addAction(default_action)
            remove_action = QAction("🗑️ Rimuovi", self)
            remove_action.triggered.connect(self._remove_sw_account)
            menu.addAction(remove_action)
        menu.exec(self.sw_account_list.viewport().mapToGlobal(position))

    # --- Gestione Contratti ---
    def _add_contract(self):
        text, ok = QInputDialog.getText(
            self, "Aggiungi Contratto", "Inserisci il numero di contratto:"
        )
        if ok and text.strip():
            if not self.contract_list.findItems(
                text.strip(), Qt.MatchFlag.MatchExactly
            ):
                self.contract_list.addItem(text.strip())
                self._save_settings()

    def _edit_contract(self):
        item = self.contract_list.currentItem()
        if item:
            text, ok = QInputDialog.getText(
                self, "Modifica", "Valore:", text=item.text()
            )
            if ok and text.strip():
                item.setText(text.strip())
                self._save_settings()

    def _remove_contract(self):
        row = self.contract_list.currentRow()
        if row >= 0:
            if (
                QMessageBox.question(self, "Conferma", "Rimuovere contratto?")
                == QMessageBox.StandardButton.Yes
            ):
                self.contract_list.takeItem(row)
                self._save_settings()

    # --- Gestione Fornitori ---
    def _add_fornitore(self):
        text, ok = QInputDialog.getText(
            self, "Aggiungi Fornitore", "Inserisci il codice e nome:"
        )
        if ok and text.strip():
            for i in range(self.fornitori_list.count()):
                if self.fornitori_list.item(i).text().lower() == text.strip().lower():
                    QMessageBox.warning(self, "Esistente", "Fornitore già presente.")
                    return
            self.fornitori_list.addItem(text.strip())
            self._save_settings()

    def _edit_fornitore(self):
        item = self.fornitori_list.currentItem()
        if item:
            text, ok = QInputDialog.getText(
                self, "Modifica", "Valore:", text=item.text()
            )
            if ok and text.strip():
                item.setText(text.strip())
                self._save_settings()

    def _remove_fornitore(self):
        row = self.fornitori_list.currentRow()
        if row >= 0:
            if (
                QMessageBox.question(self, "Conferma", "Rimuovere?")
                == QMessageBox.StandardButton.Yes
            ):
                self.fornitori_list.takeItem(row)
                self._save_settings()

    # --- Gestione Reparti ---
    def _add_reparto(self):
        text, ok = QInputDialog.getText(self, "Aggiungi Reparto", "Nome:")
        if ok and text.strip():
            text = text.strip().upper()
            if not self.reparti_list.findItems(text, Qt.MatchFlag.MatchExactly):
                self.reparti_list.addItem(text)
                self._save_settings()

    def _edit_reparto(self):
        item = self.reparti_list.currentItem()
        if item:
            text, ok = QInputDialog.getText(
                self, "Modifica", "Valore:", text=item.text()
            )
            if ok and text.strip():
                item.setText(text.strip().upper())
                self._save_settings()

    def _remove_reparto(self):
        row = self.reparti_list.currentRow()
        if row >= 0:
            if (
                QMessageBox.question(self, "Conferma", "Rimuovere reparto?")
                == QMessageBox.StandardButton.Yes
            ):
                self.reparti_list.takeItem(row)
                self._save_settings()

    # --- Gestione Cantieri ---
    def _add_cantiere(self):
        text, ok = QInputDialog.getText(self, "Aggiungi Cantiere", "Nome:")
        if ok and text.strip():
            text = text.strip().upper()
            if not self.cantieri_list.findItems(text, Qt.MatchFlag.MatchExactly):
                self.cantieri_list.addItem(text)
                self._save_settings()

    def _edit_cantiere(self):
        item = self.cantieri_list.currentItem()
        if item:
            text, ok = QInputDialog.getText(
                self, "Modifica", "Valore:", text=item.text()
            )
            if ok and text.strip():
                item.setText(text.strip().upper())
                self._save_settings()

    def _remove_cantiere(self):
        row = self.cantieri_list.currentRow()
        if row >= 0:
            if (
                QMessageBox.question(self, "Conferma", "Rimuovere cantiere?")
                == QMessageBox.StandardButton.Yes
            ):
                self.cantieri_list.takeItem(row)
                self._save_settings()

    # --- Load & Save ---
    def _load_settings(self):
        config = config_manager.load_config()

        # Blocca segnali per evitare loop di salvataggio durante il caricamento
        self.blockSignals(True)
        for child in self.findChildren(QWidget):
            child.blockSignals(True)

        # Browser
        self.headless_check.setChecked(config.get("browser_headless", False))
        self.timeout_spin.setValue(config.get("browser_timeout", 30))

        # Contabilita
        self.contabilita_path_edit.setText(config.get("contabilita_file_path", ""))
        self.giornaliere_path_edit.setText(config.get("giornaliere_path", ""))
        self.attivita_path_edit.setText(config.get("attivita_programmate_path", ""))
        self.certificati_path_edit.setText(config.get("certificati_campione_path", ""))
        self.dataease_path_edit.setText(config.get("dataease_path", ""))  # New
        self.auto_update_contabilita_check.setChecked(
            config.get("enable_auto_update_contabilita", True)
        )

        # Telegram
        self.tg_token_edit.setText(config.get("telegram_token", ""))
        self.tg_chat_id_edit.setText(config.get("telegram_chat_id", ""))

        # Gemini API Key (da SecretsManager)
        self.gemini_api_key_edit.setText(SecretsManager.get_gemini_api_key())

        # Fornitori
        self.fornitori_list.clear()
        for f in config.get("fornitori", []):
            self.fornitori_list.addItem(f)

        # Contratti
        self.contract_list.clear()
        for c in config.get("contracts", []):
            self.contract_list.addItem(c)

        # Reparti
        self.reparti_list.clear()
        for r in config.get("reparti", []):
            self.reparti_list.addItem(r)

        # Cantieri
        self.cantieri_list.clear()
        for c in config.get("cantieri", []):
            self.cantieri_list.addItem(c)

        # Accounts
        self._render_accounts(config.get("accounts", []))
        self._render_sw_accounts(config.get("safework_accounts", []))

        # Sblocca
        for child in self.findChildren(QWidget):
            child.blockSignals(False)
        self.blockSignals(False)

        self._set_unsaved_changes(False)

    def _save_settings(self):
        # Impedisci salvataggi ricorsivi
        if self.signalsBlocked():
            return

        # Raccogli dati
        fornitori = [
            self.fornitori_list.item(i).text()
            for i in range(self.fornitori_list.count())
        ]
        contracts = [
            self.contract_list.item(i).text() for i in range(self.contract_list.count())
        ]
        reparti = [
            self.reparti_list.item(i).text() for i in range(self.reparti_list.count())
        ]
        cantieri = [
            self.cantieri_list.item(i).text() for i in range(self.cantieri_list.count())
        ]
        accounts = self._get_current_accounts()
        sw_accounts = self._get_current_sw_accounts()

        config_manager.set_config_value(
            "browser_headless", self.headless_check.isChecked()
        )
        config_manager.set_config_value("browser_timeout", self.timeout_spin.value())

        config_manager.set_config_value(
            "contabilita_file_path", self.contabilita_path_edit.text()
        )
        config_manager.set_config_value(
            "giornaliere_path", self.giornaliere_path_edit.text()
        )
        config_manager.set_config_value(
            "attivita_programmate_path", self.attivita_path_edit.text()
        )
        config_manager.set_config_value(
            "certificati_campione_path", self.certificati_path_edit.text()
        )
        config_manager.set_config_value(
            "dataease_path", self.dataease_path_edit.text()
        )  # New
        config_manager.set_config_value(
            "enable_auto_update_contabilita",
            self.auto_update_contabilita_check.isChecked(),
        )

        config_manager.set_config_value("telegram_token", self.tg_token_edit.text())
        config_manager.set_config_value("telegram_chat_id", self.tg_chat_id_edit.text())

        # Gemini API Key (Salva in SecretsManager)
        key_val = self.gemini_api_key_edit.text().strip()
        if key_val:
            SecretsManager.store_credential("api", "GEMINI_API_KEY", key_val)
        else:
            SecretsManager.delete_credential("api", "GEMINI_API_KEY")

        config_manager.set_config_value("fornitori", fornitori)
        config_manager.set_config_value("contracts", contracts)
        config_manager.set_config_value("reparti", reparti)
        config_manager.set_config_value("cantieri", cantieri)

        # Il primo della lista diventa default se esiste
        if contracts:
            config_manager.set_config_value("default_contract", contracts[0])

        config_manager.set_config_value("accounts", accounts)
        config_manager.set_config_value("safework_accounts", sw_accounts)

        # Emetti segnale per aggiornare il resto dell'app
        self.settings_saved.emit()

    def _reset_settings(self):
        if self._has_unsaved_changes:
            if (
                QMessageBox.question(self, "Conferma", "Annullare modifiche?")
                == QMessageBox.StandardButton.Yes
            ):
                self._load_settings()
        else:
            self._load_settings()

    def prompt_save_if_needed(self) -> bool:
        if not self._has_unsaved_changes:
            return True
        reply = QMessageBox.question(
            self,
            "Modifiche non salvate",
            "Salvare?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
        )
        if reply == QMessageBox.StandardButton.Save:
            self._save_settings()
            return True
        elif reply == QMessageBox.StandardButton.Discard:
            self._load_settings()
            return True

        return False
