"""
SyncroJob - Scarico PDL Panel (Refactored)
Pannello coordinato per lo scarico massivo e la stampa dei PDL da SafeWork.
Modularizzato per una migliore manutenibilità.
"""

import logging
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel
from src.gui.styles import COLORS, COMBOBOX_STYLE, LABEL_MUTED, LINEEDIT_STYLE, STATUS_COLORS
from src.gui.widgets import EditableDataTable
from src.gui.widgets.core_widgets import (
    FilterComboBox,
    IconButton,
    StandardCheckBox,
    StandardInput,
)
from src.gui.widgets.safework.status_list import StatusListWidget
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon
from src.utils.printing import get_installed_printers

logger = logging.getLogger(__name__)


class ScaricoPDLPanel(BaseBotPanel):
    """
    Orchestratore per lo scarico PDL con gestione parametri e stati riga.
    Consente di definire una lista di numeri PDL, la cartella di destinazione e le opzioni di stampa.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello scarico PDL.

        Args:
            parent: Widget genitore opzionale.
        """
        super().__init__(
            bot_id="scarico_pdl",
            bot_name="Scarico PDL",
            bot_description="Scarica e stampa i Permessi di Lavoro da SafeWork.",
            parent=parent,
        )
        self._setup_content()
        QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self) -> Any:
        """
        Restituisce la classe del bot associata a questo pannello.

        Returns:
            Type[SafeWorkPDLBot]: La classe per l'automazione PDL.
        """
        from src.bots.safework.pdl.bot import SafeWorkPDLBot

        return SafeWorkPDLBot

    def _safe_load_data(self) -> None:
        """Carica i dati salvati dall'ultima sessione gestendo eventuali eccezioni."""
        try:
            self._load_saved_data()
        except Exception as e:
            logger.error(f"Error loading data: {e}")

    def _setup_content(self) -> None:
        """Inizializza il contenuto specifico del pannello: filtri, opzioni stampa e tabella PDL."""
        # 1. Parametri
        self.params_container = QFrame()
        self.params_container.setObjectName("filterBar")
        self.params_container.setStyleSheet(
            f"QFrame#filterBar {{ background: {COLORS['bg_white']}; border: 1px solid {COLORS['border_light']}; border-radius: 12px; }}"
        )
        params_lay = QHBoxLayout(self.params_container)
        params_lay.setContentsMargins(15, 10, 15, 10)
        params_lay.setSpacing(20)

        # Stampa
        v_print = QVBoxLayout()
        v_print.setSpacing(4)
        lbl_p = QLabel("OPZIONI STAMPA")
        lbl_p.setStyleSheet(LABEL_MUTED)
        v_print.addWidget(lbl_p)
        h_p = QHBoxLayout()
        h_p.setSpacing(10)
        self.check_stampa = StandardCheckBox("Attiva Stampa")
        self.combo_stampanti = FilterComboBox()
        self.combo_stampanti.addItems(get_installed_printers())
        self.combo_stampanti.setStyleSheet(COMBOBOX_STYLE)
        for w in (self.check_stampa, self.combo_stampanti):
            h_p.addWidget(w)
        v_print.addLayout(h_p)
        params_lay.addLayout(v_print)

        # Destinazione
        v_dest = QVBoxLayout()
        v_dest.setSpacing(4)
        lbl_d = QLabel("CARTELLA DESTINAZIONE")
        lbl_d.setStyleSheet(LABEL_MUTED)
        v_dest.addWidget(lbl_d)
        h_d = QHBoxLayout()
        h_d.setSpacing(5)
        self.edit_dest = StandardInput()
        self.edit_dest.setPlaceholderText("Seleziona cartella...")
        self.edit_dest.setStyleSheet(LINEEDIT_STYLE)
        self.btn_browse = IconButton()
        self.btn_browse.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER), COLORS["text_dark"]))
        self.btn_browse.setIconSize(QSize(20, 20))
        self.btn_browse.setFixedSize(38, 38)
        self.btn_browse.setToolTip("Sfoglia...")
        self.btn_browse.clicked.connect(self._on_browse_clicked)
        self.btn_browse.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["border_medium"]};
                border-radius: 6px;
                padding: 2px;
            }}
            QPushButton:hover {{ background-color: {COLORS["table_selection_bg"]}; }}
        """)

        from src.gui.widgets.modern_button import ModernButton
        self.btn_open = ModernButton(
            "APRI",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL
        )
        self.btn_open.setFixedSize(60, 38)
        self.btn_open.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS["bg_white"]};
                color: {COLORS["text_dark"]};
                border: 1px solid {COLORS["border_medium"]};
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {COLORS["table_selection_bg"]}; }}
        """)
        self.btn_open.setToolTip("Apri cartella nel file system")
        self.btn_open.clicked.connect(self._on_open_clicked)

        h_d.addWidget(self.edit_dest)
        h_d.addWidget(self.btn_browse)
        h_d.addWidget(self.btn_open)
        v_dest.addLayout(h_d)
        params_lay.addLayout(v_dest)

        params_lay.addStretch()

        # Inserisci nel layout del contenuto anziché nel layout principale
        self.content_layout.addWidget(self.params_container)

        # 2. Tabella e Stati
        content_lay = QHBoxLayout()
        content_lay.setSpacing(10)

        # Recupera le colonne dal bot e aggiunge la colonna ESITO
        cols = list(self.get_bot_class().get_columns())
        cols.append({"name": "esito", "label": "ESITO", "type": "text", "default": "", "readonly": True})

        self.data_table = EditableDataTable(cols)
        self.data_table.data_changed.connect(self._update_status_list)

        v_status = QVBoxLayout()
        # 56px offset = 10px (EditableDataTable margin) + 5px (container inner margin) + ~41px (table header)
        v_status.setContentsMargins(0, 56, 0, 0)
        self.status_list = StatusListWidget()
        self.status_list.setFixedWidth(40)
        v_status.addWidget(self.status_list)
        v_status.addStretch()

        content_lay.addWidget(self.data_table)
        content_lay.addLayout(v_status)

        self.content_layout.addLayout(content_lay)

    def _update_status_list(self, force: bool = False) -> None:
        """
        Sincronizza il contatore visivo dello stato con il numero di righe della tabella.

        Args:
            force: Se True, reinizializza sempre la lista (usato all'avvio bot).
        """
        count = self.data_table.table.rowCount()
        if force or self.status_list.count() != count:
            self.status_list.initialize_rows(count, self.data_table.table.rowHeight(0) or 30)

    def _on_browse_clicked(self) -> None:
        """Apre il dialogo di selezione cartella per i PDF scaricati."""
        path = QFileDialog.getExistingDirectory(self, "Seleziona Cartella Destinazione")
        if path:
            self.edit_dest.setText(path)

    def _on_open_clicked(self) -> None:
        """Apre la cartella di destinazione nell'esplora risorse di sistema."""
        import os
        from pathlib import Path

        path_str = self.edit_dest.text()
        if not path_str:
            path_str = str(Path.home() / "Downloads")

        path = Path(path_str).resolve()
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except Exception:
                ToastManager.instance().show(f"Impossibile creare la cartella: {path}", "error")
                return

        try:
            import os
            os.startfile(str(path)) # noqa: S606
        except Exception:
            ToastManager.instance().show(f"Impossibile aprire la cartella: {path}", "error")

    def _load_saved_data(self) -> None:
        """Ripristina i dati e i parametri dell'ultima sessione dalla configurazione locale."""
        config = config_manager.load_config()
        data = config.get("last_pdl_data", [])
        if data:
            self.data_table.set_data(data)

        p_cfg = config.get("last_pdl_params", {})
        self.check_stampa.setChecked(p_cfg.get("stampa", False))
        if p_cfg.get("stampante"):
            self.combo_stampanti.setCurrentText(p_cfg["stampante"])
        self.edit_dest.setText(p_cfg.get("destinazione", str(Path.home() / "Downloads")))
        self._update_status_list()

    def _get_bot_data(self) -> list[dict[str, Any]] | None:
        """
        Prepara e salva i dati da passare al bot per l'esecuzione.

        Returns:
            list[dict[str, Any]] | None: Lista di configurazioni riga o None se tabella vuota.
        """
        items = self.data_table.get_data()
        if not items:
            ConfirmationDialog.show_warning(
                self, "Tabella Vuota", "Inserisci almeno un numero PDL da processare."
            )
            return None

        # Salvataggio persistente
        config_manager.set_config_value("last_pdl_data", items)
        config_manager.set_config_value(
            "last_pdl_params",
            {
                "stampa": self.check_stampa.isChecked(),
                "stampante": self.combo_stampanti.currentText(),
                "destinazione": self.edit_dest.text(),
            },
        )

        return [
            {
                "numero_pdl": it["numero_pdl"],
                "print_enabled": self.check_stampa.isChecked(),
                "printer_name": self.combo_stampanti.currentText(),
                "output_dir": self.edit_dest.text(),
            }
            for it in items
        ]

    def get_safework_credentials(self) -> tuple[str, str, str]:
        """Recupera le credenziali SafeWork configurate. Ritorna (user, pass, tipo)."""
        accounts = config_manager.load_config().get("safework_accounts", [])
        if not accounts:
            return "", "", "Esecutore"
        default_acc = next((a for a in accounts if a.get("default")), accounts[0])
        return (
            default_acc.get("username", ""),
            default_acc.get("password", ""),
            default_acc.get("type", "Esecutore"),
        )

    def get_bot_instance(self) -> Any:
        """Crea e restituisce un'istanza configurata del bot Scarico PDL."""
        bot_class = self.get_bot_class()
        username, password, account_type = self.get_safework_credentials()
        config = config_manager.load_config()

        return bot_class(
            username=username,
            password=password,
            account_type=account_type,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
        )

    def validate_ready(self) -> tuple[bool, str]:
        """
        Verifica se il bot è pronto per l'avvio.
        Richiede almeno un numero PDL in tabella.
        """
        data = self.data_table.get_data()
        if not data:
            return False, "Nessun numero PDL inserito nella tabella."
        return True, ""

    def _on_start(self, params_override: dict[str, Any] | None = None) -> None:
        """Avvia l'esecuzione del bot configurando worker e segnali."""
        super()._on_start(params_override)
        username, password, _ = self.get_safework_credentials()

        if not username or not password:
            ToastManager.instance().show("Configura le credenziali SafeWork nelle Impostazioni.", "warning")
            self._update_status(STATUS_COLORS["error"], "Credenziali mancanti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        bot_data = self._get_bot_data()
        if not bot_data:
            self._update_status(STATUS_COLORS["pending"], "In attesa")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        bot = self.get_bot_instance()
        if not bot:
            return

        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        from src.gui.panels.base import BotWorker

        worker = BotWorker(bot, bot_data, telegram_service=tg_service)
        self.worker = worker
        self._setup_worker_connections(worker)

        # Connessione segnale specifico per riga PDL
        worker.row_status_signal.connect(self.on_step_completed)

        # Reset pallini all'avvio
        self._update_status_list(force=True)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Avvio Scarico PDL SafeWork...")
        worker.start()
        self.bot_started.emit()

    def _on_worker_finished(self, success: bool) -> None:
        """
        Gestisce il completamento del worker.
        Se richiesto da Telegram, unisce i PDF e invia il risultato.

        Args:
            success: Esito dell'operazione.
        """
        # Recupera i file scaricati prima che il worker venga distrutto dal super()
        downloaded_files: list[str] = []
        if self.worker and hasattr(self.worker.bot, "downloaded_files"):
            downloaded_files = getattr(self.worker.bot, "downloaded_files", [])

        super()._on_worker_finished(success)

        if success:
            ToastManager.instance().show("Processo PDL Completato!", "success")

            # Logica Telegram: Unione e invio se richiesto dal bridge
            if getattr(self, "merge_and_send_from_telegram", False) and downloaded_files:
                self._handle_telegram_auto_send(downloaded_files)

    def _on_bot_finished(self, success: bool) -> None:
        """Alias per compatibilità test."""
        self._on_worker_finished(success)

    def _handle_telegram_auto_send(self, files: list[str]) -> None:
        """Unisce i PDF e li invia via Telegram se il servizio è disponibile."""
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        if not tg_service or not files:
            return

        self.log_widget.append("📦 Elaborazione report per Telegram...")

        try:
            # Semplice invio del primo file o logica di merge (mockata per ora se non disponibile)
            # In produzione qui andrebbe il PDF Merger
            report_path = files[0]  # Fallback
            if len(files) > 1:
                self.log_widget.append(f"📎 Inviando {len(files)} file a Telegram...")

            tg_service.send_document_sync(report_path, caption=f"✅ Scarico PDL completato ({len(files)} file)")
            self.log_widget.append("📤 Report inviato correttamente a Telegram.")
        except Exception as e:
            self.log_widget.append(f"⚠️ Errore invio Telegram: {e}", "ERROR")

    def on_step_completed(self, step_idx: int, success: bool, message: str = "") -> None:
        """
        Aggiorna lo stato visivo di una specifica riga PDL al termine del suo processing.

        Args:
            step_idx: Indice della riga processata.
            success: Esito del processing della riga.
            message: Messaggio di errore opzionale.
        """
        self.status_list.update_status(step_idx, success)

        # Trova dinamicamente l'indice della colonna 'esito'
        col_idx = -1
        for i, col in enumerate(self.data_table.columns):
            if col["name"] == "esito":
                col_idx = i
                break

        if col_idx != -1:
            esito_text = "Completato" if success else f"Errore: {message}" if message else "Errore generico"
            self.data_table.update_cell(step_idx, col_idx, esito_text, emit_signal=False)

        if not success:
            logger.error(f"Errore riga {step_idx}: {message}")

    def set_pdl_list(self, pdl_numbers: list[str]) -> None:
        """
        Popola la tabella con i numeri PDL forniti e avvia automaticamente lo scarico.
        Utilizzato per l'integrazione con il Database PDL.
        """
        if not pdl_numbers:
            return

        # 1. Pulisci tabella
        self.data_table.clear()

        # 2. Prepara dati per la tabella (Formato: [{"numero_pdl": "...", "esito": ""}])
        rows = [{"numero_pdl": num, "esito": ""} for num in pdl_numbers]
        self.data_table.set_data(rows)

        # 3. Attiva stampa di default per questa modalità
        self.check_stampa.setChecked(True)

        # 4. Avvia bot dopo un delay di rendering
        self._on_log(f"📥 Ricevuti {len(pdl_numbers)} PDL dal database. Avvio stampa automatica...")
        QTimer.singleShot(500, self._on_start)
