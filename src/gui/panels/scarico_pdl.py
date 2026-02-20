"""
SyncroJob - Scarico PDL Panel
Pannello per il bot Scarico PDL (SafeWork).
"""

import traceback
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.widgets import EditableDataTable
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon
from src.utils.printing import get_installed_printers


class StatusListWidget(QListWidget):
    """Widget per visualizzare lo stato di elaborazione riga per riga della tabella PDL."""

    def __init__(self, parent=None):
        """Inizializza la lista degli stati."""
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet(
            """
            QListWidget {
                background: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 0px;
                margin: 0px;
                border: none;
            }
        """
        )
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def initialize_rows(self, count: int, row_height: int = 30):
        """
        Prepara n righe con stato 'Pending' (pallino grigio).

        Args:
            count: Numero di righe da inizializzare.
            row_height: Altezza di ogni riga in pixel.
        """
        self.clear()
        for _ in range(count):
            item = QListWidgetItem()
            # Altezza deve matchare la riga della tabella
            # Prima riga include offset per header tabella (circa 25px)
            effective_height = row_height
            item.setSizeHint(QSize(40, effective_height))

            icon_label = QLabel()
            icon_label.setFixedSize(24, 24)
            icon_label.setStyleSheet(
                "background-color: #E0E0E0; border-radius: 12px; border: 1px solid #BDBDBD;"
            )

            # Usiamo un widget container per centrare
            container = QWidget()
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 3, 0, 3)
            layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignCenter)

            self.addItem(item)
            self.setItemWidget(item, container)

    def update_status(self, index: int, success: bool):
        """
        Aggiorna l'icona della riga specificata (Verde se successo, Rosso se errore).

        Args:
            index: Indice della riga.
            success: Esito dell'operazione.
        """
        if index < 0 or index >= self.count():
            return

        item = self.item(index)
        widget = self.itemWidget(item)
        if not widget:
            return

        icon_label: QLabel = widget.findChild(QLabel)
        if not icon_label:
            return

        if success:
            # Spunta Verde
            icon_path = get_asset_path(Icons.CHECK)
            color = "#2E7D32"  # Green 800
            bg = "#C8E6C9"  # Green 100
            pixmap = get_colored_icon(icon_path, color).pixmap(16, 16)
            icon_label.setPixmap(pixmap)
            icon_label.setStyleSheet(
                f"background-color: {bg}; border-radius: 12px; border: 1px solid {color};"
            )
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            # Croce Rossa
            icon_path = get_asset_path(Icons.X_CIRCLE)
            color = "#C62828"  # Red 800
            bg = "#FFCDD2"  # Red 100
            pixmap = get_colored_icon(icon_path, color).pixmap(16, 16)
            icon_label.setPixmap(pixmap)
            icon_label.setStyleSheet(
                f"background-color: {bg}; border-radius: 12px; border: 1px solid {color};"
            )
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


class ScaricoPDLPanel(BaseBotPanel):
    """
    Pannello per lo scarico massivo delle PDL da SafeWork.
    Permette di inserire una lista di numeri PDL da processare, stamparli e unirli in PDF.
    """

    def __init__(self, parent=None):
        """
        Inizializza il pannello Scarico PDL.

        Args:
            parent: Widget genitore.
        """
        super().__init__(
            bot_id="scarico_pdl",
            bot_name="Scarico PDL",
            bot_description="Scarica e stampa i Permessi di Lavoro da SafeWork.",
            parent=parent,
        )
        self._setup_content()
        # Defer data loading
        QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self):
        """Restituisce la classe SafeWorkPDLBot associata."""
        from src.bots.safework.pdl.bot import SafeWorkPDLBot
        return SafeWorkPDLBot

    def _safe_load_data(self):
        """Carica i dati di configurazione in modo sicuro."""
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for ScaricoPDLPanel: {e}")
            traceback.print_exc()

    def _setup_content(self):
        """Configura l'interfaccia utente del pannello (Parametri, Tabella, Status)."""
        # --- 1. CARD PARAMETRI (Floating Card) ---
        self.params_container = QFrame()
        self.params_container.setObjectName("paramsContainer")
        self.params_container.setStyleSheet("""
            QFrame#paramsContainer {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-bottom: 3px solid #212121;
                border-radius: 12px;
            }
            QLabel {
                color: #424242;
                font-weight: bold;
                font-size: 13px;
                background: transparent;
            }
        """)
        
        # Applica Ombra (Shadow Effect)
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.params_container.setGraphicsEffect(shadow)

        params_layout = QVBoxLayout(self.params_container)
        params_layout.setContentsMargins(15, 15, 15, 15)
        params_layout.setSpacing(10)

        # Riga unica per tutte le opzioni
        options_layout = QHBoxLayout()
        options_layout.setSpacing(15)

        # 1. Stampa
        vbox_print = QVBoxLayout()
        vbox_print.addWidget(QLabel("Opzioni Stampa"))
        
        hbox_print = QHBoxLayout()
        self.print_check = QCheckBox("Stampa con:")
        self.print_check.stateChanged.connect(self._save_data)
        hbox_print.addWidget(self.print_check)

        self.printer_combo = QComboBox()
        self.printer_combo.setMinimumHeight(38)
        self.printer_combo.setMinimumWidth(180)
        self.printer_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.printer_combo.setStyleSheet(
            """
            QComboBox {
                border: 1px solid #cfd8dc;
                border-radius: 6px;
                padding: 5px 10px;
                background-color: #f8f9fa;
            }
            QComboBox:focus { border: 2px solid #212121; background-color: #ffffff; }
        """
        )
        # Popola stampanti
        printers = get_installed_printers()
        if printers:
            self.printer_combo.addItems(printers)
        else:
            self.printer_combo.addItem("Nessuna stampante trovata")
        self.printer_combo.currentTextChanged.connect(self._save_data)
        hbox_print.addWidget(self.printer_combo)
        vbox_print.addLayout(hbox_print)
        options_layout.addLayout(vbox_print)

        # 2. Merge
        vbox_merge = QVBoxLayout()
        vbox_merge.addWidget(QLabel("Unione PDF"))
        self.merge_all_check = QCheckBox("Unisci in unico file")
        self.merge_all_check.setToolTip(
            "Se attivo, alla fine scaricherà un unico file PDF contenente tutti i PDL."
        )
        self.merge_all_check.stateChanged.connect(self._save_data)
        vbox_merge.addWidget(self.merge_all_check)
        options_layout.addLayout(vbox_merge)

        # 3. Destinazione
        vbox_dest = QVBoxLayout()
        vbox_dest.addWidget(QLabel("Destinazione"))
        
        hbox_dest = QHBoxLayout()
        self.dest_path_edit = QLineEdit()
        self.dest_path_edit.setPlaceholderText("Download utente (default)")
        self.dest_path_edit.setReadOnly(True)
        self.dest_path_edit.setMinimumWidth(200)
        self.dest_path_edit.setMinimumHeight(38)
        self.dest_path_edit.setStyleSheet("border: 1px solid #cfd8dc; border-radius: 6px; padding: 5px; background-color: #f8f9fa;")
        hbox_dest.addWidget(self.dest_path_edit)

        browse_btn = QPushButton()
        browse_btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER), "#212121"))
        browse_btn.setIconSize(QSize(20, 20))
        browse_btn.setFixedSize(38, 38)
        browse_btn.clicked.connect(self._browse_dest_path)
        browse_btn.setStyleSheet("""
            QPushButton { background-color: #ffffff; border: 1px solid #cfd8dc; border-radius: 6px; }
            QPushButton:hover { background-color: #E0F7FA; border-color: #212121; }
        """)
        hbox_dest.addWidget(browse_btn)
        vbox_dest.addLayout(hbox_dest)
        options_layout.addLayout(vbox_dest)

        options_layout.addStretch()
        params_layout.addLayout(options_layout)

        # Aggiunta Card Parametri al layout principale
        params_wrapper = QWidget()
        wrapper_layout = QVBoxLayout(params_wrapper)
        wrapper_layout.setContentsMargins(10, 10, 10, 5) # Margine inferiore ridotto per avvicinare la tabella
        wrapper_layout.addWidget(self.params_container)
        self.content_layout.addWidget(params_wrapper)

        # --- 2. TOOLBAR TABELLA (Pulisci Tabella) ---
        table_toolbar = QHBoxLayout()
        table_toolbar.setContentsMargins(15, 0, 15, 5)
        table_toolbar.addStretch()
        self.clear_btn = ModernButton(
            "Pulisci Tabella",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),
        )
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)
        self.content_layout.addLayout(table_toolbar)

        # --- 3. AREA DI LAVORO (Tabella e Status) ---
        work_area = QHBoxLayout()
        work_area.setSpacing(10)
        work_area.setContentsMargins(0, 0, 0, 0)

        # Sinistra: Card Tabella (già implementata come card neon cyan via EditableDataTable)
        self.data_table = EditableDataTable([{"name": "NUMERO PDL", "type": "text"}])
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._save_data)
        self.data_table.data_changed.connect(self._reset_status_list)
        work_area.addWidget(self.data_table, stretch=8)

        # Destra: Contenitore Status con Header
        status_container = QVBoxLayout()
        status_container.setSpacing(0)
        status_container.setContentsMargins(0, 0, 0, 0)

        status_header = QLabel("Progresso")
        status_header.setStyleSheet("font-weight: bold; font-size: 12px; color: #424242; padding: 4px 0px;")
        status_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_container.addWidget(status_header)

        self.status_list = StatusListWidget()
        status_container.addWidget(self.status_list)

        work_area.addLayout(status_container, stretch=1)

        self.content_layout.addLayout(work_area)

    def _refresh_printers(self):
        """Aggiorna la lista delle stampanti di sistema disponibili."""
        current = self.printer_combo.currentText()
        self.printer_combo.clear()
        printers = get_installed_printers()
        if printers:
            self.printer_combo.addItems(printers)
            if current in printers:
                self.printer_combo.setCurrentText(current)
        else:
            self.printer_combo.addItem("Nessuna stampante trovata")

    def _browse_dest_path(self):
        """Apre un dialogo per selezionare la cartella di destinazione dei PDF."""
        path = QFileDialog.getExistingDirectory(self, "Seleziona cartella destinazione")
        if path:
            self.dest_path_edit.setText(path)
            self._save_data()

    def _load_saved_data(self):
        """Carica le ultime impostazioni e i dati PDL salvati."""
        config = config_manager.load_config()
        saved_data = config.get("last_pdl_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)

        self.print_check.setChecked(config.get("pdl_print_enabled", False))
        self.merge_all_check.setChecked(config.get("pdl_merge_all_session", False))
        saved_printer = config.get("pdl_printer_name", "")
        if saved_printer:
            index = self.printer_combo.findText(saved_printer)
            if index >= 0:
                self.printer_combo.setCurrentIndex(index)

        self.dest_path_edit.setText(config.get("path_scarico_pdl", ""))

    def _save_data(self):
        """Salva le impostazioni correnti nel file di configurazione."""
        data = self.data_table.get_data()
        config_manager.set_config_value("last_pdl_data", data)
        config_manager.set_config_value("pdl_print_enabled", self.print_check.isChecked())
        config_manager.set_config_value("pdl_merge_all_session", self.merge_all_check.isChecked())
        config_manager.set_config_value("pdl_printer_name", self.printer_combo.currentText())
        config_manager.set_config_value("path_scarico_pdl", self.dest_path_edit.text())

    def _reset_status_list(self):
        """Resetta la lista degli stati visivi quando la tabella viene modificata."""
        self.status_list.clear()

    def _clear_table(self):
        """Svuota la tabella dei PDL previa conferma."""
        if ConfirmationDialog.confirm(self, "Conferma", "Cancellare tutti i PDL?"):
            self.data_table.clear()
            self._save_data()

    def validate_ready(self) -> tuple[bool, str]:
        """
        Verifica la validità delle credenziali e la presenza di dati in tabella.

        Returns:
            tuple: (bool successo, str messaggio errore)
        """
        username, password = self.get_credentials()
        if not username or not password:
            return False, "Credenziali SafeWork mancanti."

        data = self.data_table.get_data()
        if not data:
            return False, "Nessun PDL inserito."

        return True, ""

    def get_credentials(self) -> tuple[str, str]:
        """Recupera le credenziali SafeWork configurate."""
        # Prende il default da safework_accounts
        accounts = config_manager.load_config().get("safework_accounts", [])
        if not accounts:
            return "", ""

        # Cerca il default
        default_acc = next((a for a in accounts if a.get("default")), accounts[0])
        return default_acc.get("username", ""), default_acc.get("password", "")

    #
    def _create_section(self, title: str, items: list[str], color: str, bg_color: str) -> QFrame:
        """Helper per creare sezioni visive (Placeholder fix for MyPy)."""
        frame = QFrame()
        return frame

    def _on_start(self, params_override: dict[str, Any] | None = None):
        """Avvia il bot Scarico PDL configurando worker e segnali."""
        super()._on_start(params_override)
        username, password = self.get_credentials()

        # Handle overrides for validation skipping if needed, or just row processing
        rows = self.data_table.get_data()

        if params_override and "single_item" in params_override:
            # Bypass table validation if single item provided
            item = params_override["single_item"]
            if item:
                rows = [item]
                self.log_widget.append(f"ℹ️ Esecuzione singola per PDL: {item.get('numero_pdl', 'N/D')}")
        else:
            if not self._validate_pdl_start(username, password):
                return

        bot_data = self._prepare_bot_data(rows)
        bot = self._create_pdl_bot(username, password)
        if not bot:
            return

        # Worker initialization
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None
        worker = BotWorker(bot, bot_data, telegram_service=tg_service)
        self.worker = worker
        self._setup_worker_connections(worker)
        worker.row_status_signal.connect(self._on_row_status)

        self.status_list.initialize_rows(len(bot_data))

        self._finalize_start_ui()
        worker.start()
        self.bot_started.emit()

    def _validate_pdl_start(self, username, password) -> bool:
        """Esegue validazioni pre-avvio specifiche per PDL."""
        if not username or not password:
            ToastManager.instance().show("Configura le credenziali SafeWork nelle Impostazioni.", "warning")
            self._update_status("#C62828", "Credenziali SafeWork mancanti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return False

        if not self.data_table.get_data():
            ToastManager.instance().show("Inserisci almeno un PDL.", "warning")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return False
        return True

    def _prepare_bot_data(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Prepara il dizionario dei dati per l'esecuzione del bot."""
        print_enabled = self.print_check.isChecked()
        printer_name = self.printer_combo.currentText()
        merge_and_send = getattr(self, "merge_and_send_from_telegram", False)
        merge_all = getattr(
            self,
            "merge_all_session_from_telegram",
            self.merge_all_check.isChecked(),
        )

        bot_data = []
        for row in rows:
            pdl_val = row.get("numero_pdl", "")
            if pdl_val:
                bot_data.append(
                    {
                        "pdl_number": pdl_val,
                        "print_enabled": print_enabled,
                        "printer_name": printer_name,
                        "merge_and_send": merge_and_send,
                        "merge_all_session": merge_all,
                    }
                )
        return bot_data

    def _create_pdl_bot(self, username, password):
        """Istanzia il bot scarico_pdl con i parametri correnti."""
        from src.bots import create_bot

        config = config_manager.load_config()
        path = self.dest_path_edit.text() or config_manager.get_download_path()
        bot = create_bot(
            "scarico_pdl",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=path,
        )
        if not bot:
            ToastManager.instance().show("Errore creazione bot.", "error")
        return bot

    def _finalize_start_ui(self):
        """Aggiorna lo stato dei pulsanti e del log all'avvio."""
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Avvio Scarico PDL SafeWork...")
        if self.print_check.isChecked():
            self.log_widget.append(f"Stampa attiva su: {self.printer_combo.currentText()}")
        if getattr(self, "merge_and_send_from_telegram", False):
            self.log_widget.append("Unione PDF per Telegram attiva")

    def _on_worker_finished(self, success: bool):
        """Gestisce il post-processing (Telegram, Refresh DB) dopo il worker."""
        merge_and_send = getattr(self, "merge_and_send_from_telegram", False)

        missing_list: list[str] = []
        files_to_send: list[str] = []

        if self.worker:
            if hasattr(self.worker.bot, "missing_pdls"):
                missing_list = getattr(self.worker.bot, "missing_pdls", [])
            if hasattr(self.worker.bot, "downloaded_files"):
                files_to_send = getattr(self.worker.bot, "downloaded_files", [])

        super()._on_worker_finished(success)

        # 1. Report Mancanti
        self._handle_missing_pdls(missing_list)

        # 2. Consegna Telegram
        if success and merge_and_send:
            self._send_pdl_to_telegram(files_to_send)

        # 3. Cleanup
        self._cleanup_telegram_flags()

        # 4. Auto-Refresh PDL Database
        if success:
            win = self.window()
            if win and hasattr(win, "pdl_db_panel"):
                # Ricarica i dati nel pannello PDL se inizializzato
                pdl_panel = getattr(win, "pdl_db_panel", None)
                if pdl_panel and hasattr(pdl_panel, "refresh_data"):
                    pdl_panel.refresh_data()
                    self._on_log("🔄 Aggiornamento Database PDL avviato.")

    def _handle_missing_pdls(self, missing_list: list[str]):
        """Segnala i PDL non trovati all'utente."""
        if missing_list:
            missing_str = ", ".join(missing_list)
            self._update_status("#2E7D32", f"Completato (Inesistenti: {missing_str})")

    def _on_row_status(self, index: int, success: bool):
        """Aggiorna lo stato visivo di una specifica riga PDL."""
        self.status_list.update_status(index, success)

    def _send_pdl_to_telegram(self, files: list[str]):
        """Invia i PDF scaricati al bot Telegram configurato."""
        if not files:
            return

        win = self.window()
        if win and hasattr(win, "telegram"):
            import os
            from typing import Any

            cast_win: Any = win
            self._on_log(f"Invio di {len(files)} PDF a Telegram...")
            for f in files:
                if Path(f).exists():
                    caption = f"**PDL Scaricato**\n`{os.path.basename(f)}`"
                    cast_win.telegram.send_document_sync(f, caption)
            self._on_log("PDF inviati con successo.")

    def _cleanup_telegram_flags(self):
        """Pulisce i flag temporanei per le notifiche Telegram."""
        for attr in ("merge_and_send_from_telegram", "merge_all_session_from_telegram"):
            if hasattr(self, attr):
                delattr(self, attr)
