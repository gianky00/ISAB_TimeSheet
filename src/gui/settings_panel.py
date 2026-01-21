"""
SyncroJob - Settings Panel
Pannello per la configurazione dell'applicazione.
Include gestione lista fornitori, tracking modifiche non salvate e statistiche.
"""

from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
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
    QTabWidget,
    QToolBox,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.backup_manager import BackupManager
from src.core.constants import Icons
from src.core.secrets_manager import SecretsManager
from src.gui.dialogs.account_dialog import AccountDialog
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.widgets.statistics_widget import StatisticsWidget
from src.gui.widgets.toast import ToastManager
from src.gui.workers.connection_worker import ConnectionTestWorker
from src.utils.helpers import get_asset_path, get_colored_icon


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

        # Timer per Debounce Salvataggio
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.setInterval(800)  # 800ms di attesa
        self.save_timer.timeout.connect(self._save_settings)

        self._setup_ui()
        self.load_settings()
        self._connect_change_signals()

    def _setup_ui(self):
        """Configura l'interfaccia."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setProperty("class", "Level2Tabs")  # Clean Standard Style
        main_layout.addWidget(self.tabs)

        # --- TAB 1: Configurazione ---
        config_tab = QWidget()
        config_layout = QVBoxLayout(config_tab)
        config_layout.setContentsMargins(0, 10, 0, 0)  # Top Spacing

        # Toolbox (Accordion)
        self.toolbox = QToolBox()
        self.toolbox.setStyleSheet(
            """
            QToolBox::tab {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                color: #495057;
                font-weight: bold;
                padding: 5px 15px;
                min-height: 45px;
            }
            QToolBox::tab:selected {
                background: #e7f1ff;
                color: #0d6efd;
                border-color: #0d6efd;
            }
        """
        )

        # --- PAGE 1: Generale & Browser ---
        page_general = QWidget()
        vbox_general = QVBoxLayout(page_general)
        vbox_general.setSpacing(20)

        # Generale Group
        general_group = self._create_group_box("Generale")
        general_layout = QVBoxLayout(general_group)
        self.groups.append(general_group)

        self.headless_check = QCheckBox("Nascondi browser dei bot")
        self.headless_check.setToolTip(
            "Se attivato, il browser verrà eseguito in background senza mostrare la finestra."
        )
        self.headless_check.setStyleSheet(
            "QCheckBox { padding: 5px; font-size: 15px; font-weight: bold; color: #d63384; }"
        )
        general_layout.addWidget(self.headless_check)
        vbox_general.addWidget(general_group)

        # Browser Group
        browser_group = self._create_group_box("Impostazioni Browser")
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
        vbox_general.addWidget(browser_group)

        vbox_general.addStretch()
        self.toolbox.addItem(page_general, "Generale Browser")

        # --- PAGE 2: Liste Dati ---
        # Usiamo una scroll area interna per le liste perché occupano spazio
        page_lists = QWidget()
        vbox_lists = QVBoxLayout(page_lists)
        scroll_lists = QScrollArea()
        scroll_lists.setWidgetResizable(True)
        scroll_lists.setFrameShape(QFrame.Shape.NoFrame)
        lists_content = QWidget()
        vbox_lists_content = QVBoxLayout(lists_content)
        vbox_lists_content.setSpacing(20)

        # CONTAINER ORIZZONTALE 1 (Account)
        lists_container = QHBoxLayout()
        lists_container.setSpacing(15)

        # 1. Sezione Account
        account_group = self._create_group_box("Account ISAB")
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
        add_acc_btn = QPushButton()
        add_acc_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), "#000000"))
        add_acc_btn.setToolTip("Aggiungi Account")
        add_acc_btn.clicked.connect(self._add_account)
        self._style_mini_button(add_acc_btn, "#28a745")
        acc_btns.addWidget(add_acc_btn)

        edit_acc_btn = QPushButton()
        edit_acc_btn.setIcon(get_colored_icon(get_asset_path(Icons.EDIT), "#000000"))
        edit_acc_btn.setToolTip("Modifica Account")
        edit_acc_btn.clicked.connect(self._edit_account)
        self._style_mini_button(edit_acc_btn, "#0d6efd")
        acc_btns.addWidget(edit_acc_btn)

        remove_acc_btn = QPushButton()
        remove_acc_btn.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), "#000000"))
        remove_acc_btn.setToolTip("Rimuovi Account")
        remove_acc_btn.clicked.connect(self._remove_account)
        self._style_mini_button(remove_acc_btn, "#dc3545")
        acc_btns.addWidget(remove_acc_btn)

        set_def_btn = QPushButton()
        set_def_btn.setIcon(get_colored_icon(get_asset_path(Icons.STAR), "#000000"))
        set_def_btn.setToolTip("Imposta Default")
        set_def_btn.clicked.connect(self._set_default_account)
        self._style_mini_button(set_def_btn, "#ffc107", text_color="black")
        acc_btns.addWidget(set_def_btn)
        acc_btns.addStretch()
        account_layout.addLayout(acc_btns)

        lists_container.addWidget(account_group)

        # 1.5 Sezione Account SafeWork (Nuova)
        sw_account_group = self._create_group_box("Account SafeWork")
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
        add_sw_btn = QPushButton()
        add_sw_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), "#000000"))
        add_sw_btn.setToolTip("Aggiungi Account SafeWork")
        add_sw_btn.clicked.connect(self._add_sw_account)
        self._style_mini_button(add_sw_btn, "#28a745")
        sw_acc_btns.addWidget(add_sw_btn)

        edit_sw_btn = QPushButton()
        edit_sw_btn.setIcon(get_colored_icon(get_asset_path(Icons.EDIT), "#000000"))
        edit_sw_btn.setToolTip("Modifica Account")
        edit_sw_btn.clicked.connect(self._edit_sw_account)
        self._style_mini_button(edit_sw_btn, "#0d6efd")
        sw_acc_btns.addWidget(edit_sw_btn)

        rem_sw_btn = QPushButton()
        rem_sw_btn.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), "#000000"))
        rem_sw_btn.setToolTip("Rimuovi Account")
        rem_sw_btn.clicked.connect(self._remove_sw_account)
        self._style_mini_button(rem_sw_btn, "#dc3545")
        sw_acc_btns.addWidget(rem_sw_btn)

        def_sw_btn = QPushButton()
        def_sw_btn.setIcon(get_colored_icon(get_asset_path(Icons.STAR), "#000000"))
        def_sw_btn.setToolTip("Imposta Default")
        def_sw_btn.clicked.connect(self._set_default_sw_account)
        self._style_mini_button(def_sw_btn, "#ffc107", text_color="black")
        sw_acc_btns.addWidget(def_sw_btn)
        sw_acc_btns.addStretch()
        sw_account_layout.addLayout(sw_acc_btns)

        lists_container.addWidget(sw_account_group)
        vbox_lists_content.addLayout(lists_container)

        # CONTAINER ORIZZONTALE 2 (Contratti e Fornitori)
        lists_container_2 = QHBoxLayout()
        lists_container_2.setSpacing(15)

        # 2. Sezione Contratti
        contract_group = self._create_group_box("Contratti")
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
        add_contract_btn = QPushButton()
        add_contract_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.PLUS), "#000000")
        )
        add_contract_btn.setToolTip("Aggiungi Contratto")
        add_contract_btn.clicked.connect(self._add_contract)
        self._style_mini_button(add_contract_btn, "#28a745")
        contract_btns.addWidget(add_contract_btn)

        edit_contract_btn = QPushButton()
        edit_contract_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.EDIT), "#000000")
        )
        edit_contract_btn.setToolTip("Modifica Contratto")
        edit_contract_btn.clicked.connect(self._edit_contract)
        self._style_mini_button(edit_contract_btn, "#0d6efd")
        contract_btns.addWidget(edit_contract_btn)

        remove_contract_btn = QPushButton()
        remove_contract_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.TRASH), "#000000")
        )
        remove_contract_btn.setToolTip("Rimuovi Contratto")
        remove_contract_btn.clicked.connect(self._remove_contract)
        self._style_mini_button(remove_contract_btn, "#dc3545")
        contract_btns.addWidget(remove_contract_btn)
        contract_btns.addStretch()
        contract_layout.addLayout(contract_btns)

        lists_container_2.addWidget(contract_group)

        # 3. Sezione Fornitori
        fornitori_group = self._create_group_box("Fornitori")
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
        add_forn_btn = QPushButton()
        add_forn_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), "#000000"))
        add_forn_btn.setToolTip("Aggiungi Fornitore")
        add_forn_btn.clicked.connect(self._add_fornitore)
        self._style_mini_button(add_forn_btn, "#28a745")
        fornitori_btn_layout.addWidget(add_forn_btn)

        edit_forn_btn = QPushButton()
        edit_forn_btn.setIcon(get_colored_icon(get_asset_path(Icons.EDIT), "#000000"))
        edit_forn_btn.setToolTip("Modifica Fornitore")
        edit_forn_btn.clicked.connect(self._edit_fornitore)
        self._style_mini_button(edit_forn_btn, "#0d6efd")
        fornitori_btn_layout.addWidget(edit_forn_btn)

        rem_forn_btn = QPushButton()
        rem_forn_btn.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), "#000000"))
        rem_forn_btn.setToolTip("Rimuovi Fornitore")
        rem_forn_btn.clicked.connect(self._remove_fornitore)
        self._style_mini_button(rem_forn_btn, "#dc3545")
        fornitori_btn_layout.addWidget(rem_forn_btn)
        fornitori_btn_layout.addStretch()
        fornitori_layout.addLayout(fornitori_btn_layout)

        lists_container_2.addWidget(fornitori_group)
        vbox_lists_content.addLayout(lists_container_2)

        # CONTAINER ORIZZONTALE 3 (Reparti e Cantieri)
        timbrature_lists_container = QHBoxLayout()
        timbrature_lists_container.setSpacing(15)

        # 4. Sezione Reparti
        reparti_group = self._create_group_box("Reparti (Timbrature)")
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
        add_rep_btn = QPushButton()
        add_rep_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), "#000000"))
        add_rep_btn.setToolTip("Aggiungi Reparto")
        add_rep_btn.clicked.connect(self._add_reparto)
        self._style_mini_button(add_rep_btn, "#28a745")
        reparti_btn_layout.addWidget(add_rep_btn)

        edit_rep_btn = QPushButton()
        edit_rep_btn.setIcon(get_colored_icon(get_asset_path(Icons.EDIT), "#000000"))
        edit_rep_btn.setToolTip("Modifica Reparto")
        edit_rep_btn.clicked.connect(self._edit_reparto)
        self._style_mini_button(edit_rep_btn, "#0d6efd")
        reparti_btn_layout.addWidget(edit_rep_btn)

        rem_rep_btn = QPushButton()
        rem_rep_btn.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), "#000000"))
        rem_rep_btn.setToolTip("Rimuovi Reparto")
        rem_rep_btn.clicked.connect(self._remove_reparto)
        self._style_mini_button(rem_rep_btn, "#dc3545")
        reparti_btn_layout.addWidget(rem_rep_btn)
        reparti_btn_layout.addStretch()
        reparti_layout.addLayout(reparti_btn_layout)

        timbrature_lists_container.addWidget(reparti_group)

        # 5. Sezione Cantieri
        cantieri_group = self._create_group_box("Cantieri (Timbrature)")
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
        add_cant_btn = QPushButton()
        add_cant_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), "#000000"))
        add_cant_btn.setToolTip("Aggiungi Cantiere")
        add_cant_btn.clicked.connect(self._add_cantiere)
        self._style_mini_button(add_cant_btn, "#28a745")
        cantieri_btn_layout.addWidget(add_cant_btn)

        edit_cant_btn = QPushButton()
        edit_cant_btn.setIcon(get_colored_icon(get_asset_path(Icons.EDIT), "#000000"))
        edit_cant_btn.setToolTip("Modifica Cantiere")
        edit_cant_btn.clicked.connect(self._edit_cantiere)
        self._style_mini_button(edit_cant_btn, "#0d6efd")
        cantieri_btn_layout.addWidget(edit_cant_btn)

        rem_cant_btn = QPushButton()
        rem_cant_btn.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), "#000000"))
        rem_cant_btn.setToolTip("Rimuovi Cantiere")
        rem_cant_btn.clicked.connect(self._remove_cantiere)
        self._style_mini_button(rem_cant_btn, "#dc3545")
        cantieri_btn_layout.addWidget(rem_cant_btn)
        cantieri_btn_layout.addStretch()
        cantieri_layout.addLayout(cantieri_btn_layout)

        timbrature_lists_container.addWidget(cantieri_group)
        vbox_lists_content.addLayout(timbrature_lists_container)

        vbox_lists_content.addStretch()
        scroll_lists.setWidget(lists_content)
        vbox_lists.addWidget(scroll_lists)
        self.toolbox.addItem(page_lists, "Gestione Liste Dati")

        # --- PAGE 3: Percorsi File ---
        page_paths = QWidget()
        vbox_paths = QVBoxLayout(page_paths)

        # --- Sezione Strumentale ---
        contabilita_group = self._create_group_box("Strumentale")
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

        self.browse_contabilita_btn = QPushButton("Sfoglia")
        self.browse_contabilita_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.FOLDER_OPEN), "#000000")
        )
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

        self.browse_giornaliere_btn = QPushButton("Sfoglia")
        self.browse_giornaliere_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.FOLDER_OPEN), "#000000")
        )
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

        self.browse_attivita_btn = QPushButton("Sfoglia")
        self.browse_attivita_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.FOLDER_OPEN), "#000000")
        )
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

        self.browse_certificati_btn = QPushButton("Sfoglia")
        self.browse_certificati_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.FOLDER_OPEN), "#000000")
        )
        self.browse_certificati_btn.setMinimumHeight(40)
        self.browse_certificati_btn.setMinimumWidth(120)
        self.browse_certificati_btn.clicked.connect(self._browse_certificati_path)
        self._style_button(self.browse_certificati_btn)
        certificati_path_layout.addWidget(self.browse_certificati_btn)
        contabilita_layout.addLayout(certificati_path_layout)

        vbox_paths.addWidget(contabilita_group)

        # --- Sezione Scarico Ore Cantiere (DataEase) ---
        dataease_group = self._create_group_box("Scarico Ore Cantiere (DataEase)")
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

        self.browse_dataease_btn = QPushButton("Sfoglia")
        self.browse_dataease_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.FOLDER_OPEN), "#000000")
        )
        self.browse_dataease_btn.setMinimumHeight(40)
        self.browse_dataease_btn.setMinimumWidth(120)
        self.browse_dataease_btn.clicked.connect(self._browse_dataease_path)
        self._style_button(self.browse_dataease_btn)
        dataease_path_layout.addWidget(self.browse_dataease_btn)
        dataease_layout.addLayout(dataease_path_layout)

        vbox_paths.addWidget(dataease_group)
        vbox_paths.addStretch()
        self.toolbox.addItem(page_paths, "Percorsi File Integrazioni")

        # --- PAGE 4: Diagnostica ---
        page_diag = QWidget()
        vbox_diag = QVBoxLayout(page_diag)

        # --- Sezione Diagnostica ---
        diag_group = self._create_group_box("Diagnostica & Licenza")
        diag_layout = QHBoxLayout(diag_group)
        diag_layout.setSpacing(15)
        self.groups.append(diag_group)

        diag_label = QLabel("Gestione file di log e licenza:")
        diag_label.setStyleSheet("font-size: 14px;")
        diag_layout.addWidget(diag_label)

        diag_layout.addStretch()

        open_folder_btn = QPushButton("  Apri Cartella Dati")
        open_folder_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.FOLDER), "#000000")
        )
        open_folder_btn.clicked.connect(self._open_data_folder)
        self._style_button(open_folder_btn)
        diag_layout.addWidget(open_folder_btn)

        vbox_diag.addWidget(diag_group)
        vbox_diag.addStretch()
        self.toolbox.addItem(page_diag, "Diagnostica")

        self.toolbox.setCurrentIndex(-1)  # Inizia con tutto collassato

        config_layout.addWidget(self.toolbox)

        # --- Pulsanti azione (Config Tab) - NASCOSTI (Salvataggio Automatico) ---
        self.action_container = QWidget()
        action_layout = QHBoxLayout(self.action_container)
        action_layout.addStretch()

        self.unsaved_label = QLabel("Modifiche non salvate")
        self.unsaved_label.setStyleSheet(
            "color: #dc3545; font-weight: bold; padding: 5px 10px; font-size: 15px;"
        )
        self.unsaved_label.setVisible(False)
        action_layout.addWidget(self.unsaved_label)

        self.reset_btn = QPushButton("Annulla")
        self.reset_btn.setIcon(get_colored_icon(get_asset_path(Icons.UNDO), "#000000"))
        self.reset_btn.setVisible(False)  # Nascosto
        action_layout.addWidget(self.reset_btn)

        self.save_btn = QPushButton("Salva impostazioni")
        self.save_btn.setIcon(get_colored_icon(get_asset_path(Icons.SAVE), "#000000"))
        self.save_btn.setVisible(False)  # Nascosto
        action_layout.addWidget(self.save_btn)

        config_layout.addWidget(self.action_container)
        self.action_container.setVisible(False)  # Nascondi l'intero container

        # Add Config Tab
        self.tabs.addTab(
            config_tab,
            get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), "#546E7A"),
            "Configurazione",
        )

        # --- TAB 2: Backup ---
        self.backup_tab = QWidget()
        self._setup_backup_tab(self.backup_tab)
        self.tabs.addTab(
            self.backup_tab,
            get_colored_icon(get_asset_path(Icons.CLOUD), "#546E7A"),
            "Backup Cloud",
        )

        # --- TAB 3: Statistiche ---
        self.stats_widget = StatisticsWidget()
        self.tabs.addTab(
            self.stats_widget,
            get_colored_icon(get_asset_path(Icons.ROCKET), "#546E7A"),
            "Statistiche",
        )

        # --- TAB 4: Telegram ---
        self.telegram_tab = QWidget()
        self._setup_telegram_tab(self.telegram_tab)
        self.tabs.addTab(
            self.telegram_tab,
            get_colored_icon(get_asset_path(Icons.SEND), "#546E7A"),
            "Telegram",
        )

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

        help_btn = QPushButton("Guida alla configurazione")
        help_btn.setIcon(get_colored_icon(get_asset_path(Icons.HELP), "#000000"))
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

        # Telegram Token Row with Test Button
        self.tg_token_edit = QLineEdit()
        self.tg_token_edit.setPlaceholderText(
            "Inserisci il Token fornito da @BotFather"
        )
        self.tg_token_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.tg_token_edit.setMinimumHeight(40)
        self.tg_token_edit.textChanged.connect(self._on_change)
        self._style_input(self.tg_token_edit)

        tg_token_layout = QHBoxLayout()
        tg_token_layout.addWidget(self.tg_token_edit)

        self.test_tg_btn = QPushButton("Test")
        self.test_tg_btn.setToolTip("Verifica connessione Telegram")
        self.test_tg_btn.setFixedSize(60, 40)
        self.test_tg_btn.clicked.connect(self._test_telegram_connection)
        self._style_button(self.test_tg_btn)
        tg_token_layout.addWidget(self.test_tg_btn)

        gl.addRow("API Token:", tg_token_layout)

        self.tg_chat_id_edit = QLineEdit()
        self.tg_chat_id_edit.setPlaceholderText("In attesa del primo messaggio...")
        self.tg_chat_id_edit.setReadOnly(True)
        self.tg_chat_id_edit.setMinimumHeight(40)
        self._style_input(self.tg_chat_id_edit)

        tg_id_layout = QHBoxLayout()
        tg_id_layout.addWidget(self.tg_chat_id_edit)

        self.tg_reset_btn = QPushButton(" Scollega Dispositivo")
        self.tg_reset_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.TRASH), "#dc3545")
        )
        self.tg_reset_btn.setFixedWidth(180)
        self.tg_reset_btn.setMinimumHeight(40)
        self.tg_reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tg_reset_btn.clicked.connect(self._reset_telegram_pairing)
        self.tg_reset_btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: 2px solid #dc3545;
                border-radius: 6px;
                color: #dc3545;
                font-weight: bold;
                font-size: 13px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #dc3545;
                color: white;
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

        self.gemini_toggle_btn = QPushButton()
        self.gemini_toggle_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.EYE), "#000000")
        )
        self.gemini_toggle_btn.setIconSize(QSize(20, 20))
        self.gemini_toggle_btn.setFixedSize(40, 40)
        self.gemini_toggle_btn.clicked.connect(self._toggle_gemini_visibility)
        self.gemini_toggle_btn.setStyleSheet(
            "background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px;"
        )
        gemini_layout.addWidget(self.gemini_toggle_btn)

        self.test_gemini_btn = QPushButton("Test")
        self.test_gemini_btn.setToolTip("Verifica connessione Gemini")
        self.test_gemini_btn.setFixedSize(60, 40)
        self.test_gemini_btn.clicked.connect(self._test_gemini_connection)
        self._style_button(self.test_gemini_btn)
        gemini_layout.addWidget(self.test_gemini_btn)

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
            self.gemini_toggle_btn.setIcon(
                get_colored_icon(get_asset_path(Icons.LOCK), "#000000")
            )
        else:
            self.gemini_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.gemini_toggle_btn.setIcon(
                get_colored_icon(get_asset_path(Icons.EYE), "#000000")
            )

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
        self.cloud_combo.addItem("Locale (Documenti)", "Local")

        # Add detected clouds
        if clouds:
            for name, path in clouds.items():
                self.cloud_combo.addItem(f"{name} ({path})", name)

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

        backup_btn = QPushButton("  Esegui Backup Ora")
        backup_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.CLOUD_UPLOAD), "#000000")
        )
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

        open_folder_btn = QPushButton("  Apri Cartella Backup")
        open_folder_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.FOLDER), "#000000")
        )
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

        self.refresh_backups_btn = QPushButton()
        self.refresh_backups_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.REFRESH), "#000000")
        )
        self.refresh_backups_btn.setToolTip("Aggiorna lista backup")
        self.refresh_backups_btn.setFixedSize(32, 32)  # Standard size
        self.refresh_backups_btn.clicked.connect(self._refresh_backups_list)
        self._style_mini_button(self.refresh_backups_btn, "#6c757d")
        restore_controls.addWidget(self.refresh_backups_btn)

        self.restore_btn = QPushButton("  Ripristina")
        self.restore_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.UNDO), "#000000")
        )
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
        button.setIconSize(QSize(18, 18))
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

            # Strumentale (Save on debounce to avoid lag)

            self.contabilita_path_edit.textChanged.connect(self._debounce_save)

            self.contabilita_path_edit.textChanged.connect(
                lambda: self._validate_path(self.contabilita_path_edit)
            )

            self.giornaliere_path_edit.textChanged.connect(self._debounce_save)

            self.giornaliere_path_edit.textChanged.connect(
                lambda: self._validate_path(self.giornaliere_path_edit)
            )

            self.attivita_path_edit.textChanged.connect(self._debounce_save)

            self.attivita_path_edit.textChanged.connect(
                lambda: self._validate_path(self.attivita_path_edit)
            )

            self.certificati_path_edit.textChanged.connect(self._debounce_save)

            self.certificati_path_edit.textChanged.connect(
                lambda: self._validate_path(self.certificati_path_edit)
            )

            self.dataease_path_edit.textChanged.connect(self._debounce_save)

            self.dataease_path_edit.textChanged.connect(
                lambda: self._validate_path(self.dataease_path_edit)
            )

            self.auto_update_contabilita_check.stateChanged.connect(self._save_settings)

            # Telegram - Debounce here too

            self.tg_token_edit.textChanged.connect(self._debounce_save)

            self.gemini_api_key_edit.textChanged.connect(self._debounce_save)

    def _on_change(self):
        """Metodo mantenuto per compatibilità, ora chiama il salvataggio diretto."""
        self._save_settings()

    def _set_unsaved_changes(self, _: bool):
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
                label += " (Default)"
            item = QListWidgetItem(label)
            if acc.get("default"):
                item.setIcon(get_colored_icon(get_asset_path(Icons.STAR), "#000000"))
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
            message=f"Sei sicuro di voler rimuovere '{item_name}'?",
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
        add_action = QAction(
            get_colored_icon(get_asset_path(Icons.PLUS), "#000000"),
            "Aggiungi account",
            self,
        )
        add_action.triggered.connect(self._add_account)
        menu.addAction(add_action)

        if item:
            self.account_list.setCurrentItem(item)
            menu.addSeparator()

            edit_action = QAction(
                get_colored_icon(get_asset_path(Icons.EDIT), "#000000"),
                "Modifica",
                self,
            )
            edit_action.triggered.connect(self._edit_account)
            menu.addAction(edit_action)

            default_action = QAction(
                get_colored_icon(get_asset_path(Icons.STAR), "#000000"),
                "Imposta come Default",
                self,
            )
            default_action.triggered.connect(self._set_default_account)
            menu.addAction(default_action)

            remove_action = QAction(
                get_colored_icon(get_asset_path(Icons.TRASH), "#000000"),
                "Rimuovi",
                self,
            )
            remove_action.triggered.connect(self._remove_account)
            menu.addAction(remove_action)

        menu.exec(self.account_list.viewport().mapToGlobal(position))

    def _show_generic_list_menu(
        self, position, list_widget, add_cb, edit_cb, remove_cb
    ):
        """Menu generico per liste semplici (contratti, fornitori)."""
        menu = QMenu()
        item = list_widget.itemAt(position)

        add_action = QAction(
            get_colored_icon(get_asset_path(Icons.PLUS), "#000000"), "Aggiungi", self
        )
        add_action.triggered.connect(add_cb)
        menu.addAction(add_action)

        if item:
            list_widget.setCurrentItem(item)
            menu.addSeparator()

            edit_action = QAction(
                get_colored_icon(get_asset_path(Icons.EDIT), "#000000"),
                "Modifica",
                self,
            )
            edit_action.triggered.connect(edit_cb)
            menu.addAction(edit_action)

            remove_action = QAction(
                get_colored_icon(get_asset_path(Icons.TRASH), "#000000"),
                "Rimuovi",
                self,
            )
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
                label += " (Default)"
            item = QListWidgetItem(label)
            if acc.get("default"):
                item.setIcon(get_colored_icon(get_asset_path(Icons.STAR), "#000000"))
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
        add_action = QAction(
            get_colored_icon(get_asset_path(Icons.PLUS), "#000000"),
            "Aggiungi account",
            self,
        )
        add_action.triggered.connect(self._add_sw_account)
        menu.addAction(add_action)
        if item:
            self.sw_account_list.setCurrentItem(item)
            menu.addSeparator()
            edit_action = QAction(
                get_colored_icon(get_asset_path(Icons.EDIT), "#000000"),
                "Modifica",
                self,
            )
            edit_action.triggered.connect(self._edit_sw_account)
            menu.addAction(edit_action)
            default_action = QAction(
                get_colored_icon(get_asset_path(Icons.STAR), "#000000"),
                "Imposta Default",
                self,
            )
            default_action.triggered.connect(self._set_default_sw_account)
            menu.addAction(default_action)
            remove_action = QAction(
                get_colored_icon(get_asset_path(Icons.TRASH), "#000000"),
                "Rimuovi",
                self,
            )
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

    def _validate_path(self, line_edit):
        """Cambia il bordo in base all'esistenza del file/cartella."""
        path_str = line_edit.text().strip()
        if not path_str:
            self._style_input(line_edit)
            return

        path = Path(path_str)
        if path.exists():
            line_edit.setStyleSheet(
                """
                QLineEdit {
                    border: 2px solid #28a745;
                    border-radius: 4px;
                    padding: 10px;
                    font-size: 15px;
                    background-color: #f0fff4;
                }
                """
            )
        else:
            line_edit.setStyleSheet(
                """
                QLineEdit {
                    border: 2px solid #dc3545;
                    border-radius: 4px;
                    padding: 10px;
                    font-size: 15px;
                    background-color: #fff5f5;
                }
                """
            )

    def _debounce_save(self):
        """Avvia il timer per il salvataggio ritardato."""
        self.save_timer.start()

    def _show_styled_message(self, title, message, icon_type="info"):
        """Mostra un QMessageBox con lo stile dell'applicazione."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        if icon_type == "success":
            msg_box.setIcon(QMessageBox.Icon.Information)
        elif icon_type == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)

        # Stile coerente con ConfirmationDialog
        msg_box.setStyleSheet(
            """
            QMessageBox {
                background-color: white;
                font-size: 15px;
            }
            QLabel {
                color: #212529;
                font-weight: 500;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                padding: 8px 20px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """
        )
        msg_box.exec()

    def _validate_all_paths(self):
        """Esegue la validazione su tutti i campi percorso noti."""
        widgets = [
            self.contabilita_path_edit,
            self.giornaliere_path_edit,
            self.attivita_path_edit,
            self.certificati_path_edit,
            self.dataease_path_edit,
        ]
        for w in widgets:
            self._validate_path(w)

    def showEvent(self, event):
        """Override dell'evento di visualizzazione per aggiornare le validazioni."""
        super().showEvent(event)
        self._validate_all_paths()

    def _handle_test_result(self, success, title, message):
        """Gestisce il risultato del worker di test connessione."""
        self.test_tg_btn.setEnabled(True)
        self.test_gemini_btn.setEnabled(True)

        icon = "success" if success else "error"
        self._show_styled_message(title, message, icon)

    def _test_telegram_connection(self):
        token = self.tg_token_edit.text().strip()
        if not token:
            QMessageBox.warning(self, "Errore", "Inserisci un token Telegram.")
            return

        self.test_tg_btn.setEnabled(False)
        self.worker = ConnectionTestWorker("telegram", token)
        self.worker.result_ready.connect(self._handle_test_result)
        self.worker.start()

    def _test_gemini_connection(self):
        key = self.gemini_api_key_edit.text().strip()
        if not key:
            QMessageBox.warning(self, "Errore", "Inserisci una API Key Gemini.")
            return

        self.test_gemini_btn.setEnabled(False)
        self.worker = ConnectionTestWorker("gemini", key)
        self.worker.result_ready.connect(self._handle_test_result)
        self.worker.start()

    # --- Load & Save ---
    def load_settings(self):
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
        self._validate_path(self.contabilita_path_edit)

        self.giornaliere_path_edit.setText(config.get("giornaliere_path", ""))
        self._validate_path(self.giornaliere_path_edit)

        self.attivita_path_edit.setText(config.get("attivita_programmate_path", ""))
        self._validate_path(self.attivita_path_edit)

        self.certificati_path_edit.setText(config.get("certificati_campione_path", ""))
        self._validate_path(self.certificati_path_edit)

        self.dataease_path_edit.setText(config.get("dataease_path", ""))
        self._validate_path(self.dataease_path_edit)
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

    def _connect_change_signals(self):
        # Generale
        self.headless_check.stateChanged.connect(self._save_settings)

        # Browser
        self.timeout_spin.valueChanged.connect(self._save_settings)

        # Strumentale (Save on debounce to avoid lag)
        self.contabilita_path_edit.textChanged.connect(self._debounce_save)
        self.contabilita_path_edit.textChanged.connect(
            lambda: self._validate_path(self.contabilita_path_edit)
        )

        self.giornaliere_path_edit.textChanged.connect(self._debounce_save)
        self.giornaliere_path_edit.textChanged.connect(
            lambda: self._validate_path(self.giornaliere_path_edit)
        )

        self.attivita_path_edit.textChanged.connect(self._debounce_save)
        self.attivita_path_edit.textChanged.connect(
            lambda: self._validate_path(self.attivita_path_edit)
        )

        self.certificati_path_edit.textChanged.connect(self._debounce_save)
        self.certificati_path_edit.textChanged.connect(
            lambda: self._validate_path(self.certificati_path_edit)
        )

        self.dataease_path_edit.textChanged.connect(self._debounce_save)
        self.dataease_path_edit.textChanged.connect(
            lambda: self._validate_path(self.dataease_path_edit)
        )

        self.auto_update_contabilita_check.stateChanged.connect(self._save_settings)

        # Telegram - Debounce here too
        self.tg_token_edit.textChanged.connect(self._debounce_save)
        self.gemini_api_key_edit.textChanged.connect(self._debounce_save)

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
            self.load_settings()
            return True

        return False
