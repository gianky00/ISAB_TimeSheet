"""
SyncroJob - Dettagli OdA Panel
Pannello di controllo dedicato al bot per l'estrazione massiva dei dettagli degli Ordini d'Acquisto (OdA).
Permette di configurare un elenco di OdA e contratti, impostare range temporali e monitorare
il download automatico dei documenti dal portale fornitori.
"""

import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QDate, QTimer
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from src.core import config_manager
from src.core.constants import Icons
from src.gui.controllers.bot_worker import BotWorker
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel
from src.gui.styles import STATUS_COLORS
from src.gui.widgets import BotParametersWidget, EditableDataTable
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.safework.status_list import StatusListWidget
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path

if TYPE_CHECKING:
    from src.bots.base.base_bot import BaseBot


class DettagliOdAPanel(BaseBotPanel):
    """
    Pannello operativo per l'automazione dello scarico dettagli OdA.
    Eredita da BaseBotPanel per la gestione standardizzata del worker e del log.
    Include una tabella editabile per l'input dei numeri d'ordine e dei relativi contratti.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello configurando l'ID e la descrizione del bot.

        Args:
            parent: Widget genitore.
        """
        super().__init__(
            bot_id="dettagli_oda",
            bot_name="Dettagli OdA",
            bot_description="Scarica automaticamente i dettagli degli Ordini d'Acquisto.",
            parent=parent,
        )
        self.sync_module_id = "oda"
        self._setup_content()

        # Forza inizializzazione timeline immediata per Dettagli OdA (Previene blocchi su _on_start)
        from src.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot

        self.activity_timeline.set_steps(DettagliOdABot.STEPS)

        self._data_loaded = False
        # Il caricamento dati viene differito a showEvent

    def showEvent(self, event: Any) -> None:
        """Esegue il primo caricamento dati solo quando il pannello diventa visibile."""
        super().showEvent(event)
        if not self._data_loaded:
            self._data_loaded = True
            QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self) -> type["BaseBot"]:
        """Restituisce la classe bot specifica per lo scarico dei dettagli OdA."""
        from src.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot

        return DettagliOdABot

    def _safe_load_data(self) -> None:
        """Tenta il caricamento delle ultime impostazioni salvate gestendo errori di parsing."""
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"[ERROR] Error loading data for DettagliOdAPanel: {e}")
            traceback.print_exc()

    def _setup_content(self) -> None:
        """Costruisce il layout specifico con widget parametri e tabella dati editabile."""
        params_container = QWidget()
        self.params_layout = QVBoxLayout(params_container)
        self.params_layout.setContentsMargins(0, 0, 0, 0)
        self.params_layout.setSpacing(5)

        self._setup_params_section()
        self._setup_table_section()

        self.content_layout.addWidget(params_container)

    def _setup_params_section(self) -> None:
        """Configura la sezione dei parametri e la toolbar della tabella."""
        self.params_widget = BotParametersWidget(show_date_range=True, show_dest_path=True)
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        self.params_layout.addWidget(self.params_widget)

        # Tabella Toolbar
        table_toolbar = QHBoxLayout()
        table_toolbar.setContentsMargins(10, 0, 10, 0)
        table_toolbar.addStretch()
        self.clear_btn = ModernButton(
            "Pulisci Tabella",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),
        )
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)
        self.params_layout.addLayout(table_toolbar)

    def _setup_table_section(self) -> None:
        """Configura la tabella dati e la lista degli stati."""
        config = config_manager.load_config()
        table_h = QHBoxLayout()
        table_h.setSpacing(10)

        # Recupera le colonne dal bot
        cols = list(self.get_bot_class().get_columns())

        # Inietta le opzioni per la colonna contratto se presente
        for col in cols:
            if col["name"] == "numero_contratto":
                col["options"] = config.get("contracts", [])
                col["default"] = ""

        # Aggiunge la colonna ESITO
        cols.append({"name": "esito", "label": "ESITO", "type": "text", "default": "", "readonly": True})
        self.cols = cols

        self.data_table = EditableDataTable(self.cols)
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._update_status_list)
        self.data_table.data_changed.connect(self._save_data)

        v_status = QVBoxLayout()
        v_status.setContentsMargins(0, 56, 0, 0)
        self.status_list = StatusListWidget()
        self.status_list.setFixedWidth(40)
        v_status.addWidget(self.status_list)
        v_status.addStretch()

        table_h.addWidget(self.data_table)
        table_h.addLayout(v_status)
        self.params_layout.addLayout(table_h)

    def _update_status_list(self, force: bool = False) -> None:
        """
        Sincronizza il contatore visivo dello stato con il numero di righe della tabella.

        Args:
            force: Se True, reinizializza sempre la lista.
        """
        count = self.data_table.table.rowCount()
        if force or self.status_list.count() != count:
            self.status_list.initialize_rows(count, self.data_table.table.rowHeight(0) or 30)

    def on_step_completed(self, step_idx: int, success: bool, message: str = "") -> None:
        """
        Aggiorna lo stato visivo di una specifica riga al termine del suo processing.

        Args:
            step_idx: Indice della riga processata.
            success: Esito del processing della riga.
            message: Messaggio di errore opzionale.
        """
        self.status_list.update_status(step_idx, success)

        # Trova dinamicamente l'indice della colonna 'esitò
        col_idx = -1
        for i, col in enumerate(self.data_table.columns):
            if col["name"] == "esito":
                col_idx = i
                break

        if col_idx != -1:
            esito_text = "Completato" if success else f"Errore: {message}" if message else "Errore"
            self.data_table.update_cell(step_idx, col_idx, esito_text, emit_signal=False)

    def _open_settings(self) -> None:
        """Comunica alla finestra principale di mostrare la pagina delle impostazioni."""
        main_window = self.window()
        if main_window and hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def refresh_fornitori(self) -> None:
        """Aggiorna la lista dei fornitori selezionabili nel widget parametri."""
        self.params_widget.refresh_fornitori()

    def refresh_contracts(self) -> None:
        """Aggiorna dinamicamente i numeri di contratto selezionabili nella tabella."""
        contracts = config_manager.load_config().get("contracts", [])

        # Trova l'indice della colonna "numero_contratto"
        contract_col_idx = -1
        for i, col in enumerate(self.cols):
            if col["name"] == "numero_contratto":
                contract_col_idx = i
                break

        if contract_col_idx != -1:
            self.data_table.update_column_options(contract_col_idx, contracts)
            self._on_log("[SYNC] Elenco contratti aggiornato (Hot Reload).")

    def _load_saved_data(self) -> None:
        """Ripristina lo stato del pannello (date, fornitori, tabella) dall'ultimo salvataggio."""
        self._is_loading = True
        try:
            config = config_manager.load_config()
            self.refresh_fornitori()
            self.params_widget.set_societa(config.get("last_oda_societa", "ISAB"))
            self.params_widget.set_fornitore(config.get("last_oda_fornitore", ""))
            current_year = datetime.now(UTC).year
            self.params_widget.set_dates(
                config.get("last_oda_date_da", f"01.01.{current_year}"),
                config.get("last_oda_date_a", QDate.currentDate().toString("dd.MM.yyyy")),
            )
            self.params_widget.set_dest_path(config.get("path_dettagli_oda", ""))

            saved_data = config.get("last_oda_data", [])
            if saved_data:
                # Forza la colonna Numero Contratto a vuoto all'avvio per policy Enterprise
                for row_dict in saved_data:
                    # Supporta sia "Numero Contratto" che la chiave normalizzata "numero_contratto"
                    for k in list(row_dict.keys()):
                        if k.lower().replace(" ", "_") == "numero_contratto":
                            row_dict[k] = ""
                self.data_table.set_data(saved_data)
            else:
                # Se non ci sono dati salvati, svuota esplicitamente per evitare default indesiderati
                self.data_table.clear()

            self._update_status_list()
        finally:
            self._is_loading = False

    def _save_data(self) -> None:
        """Persiste i parametri attuali nella configurazione globale (Batch optimization)."""
        if getattr(self, "_is_loading", False) or not hasattr(self, "params_widget"):
            return
        date_da, date_a = self.params_widget.get_dates()

        updates = {
            "last_oda_data": self.data_table.get_data(),
            "last_oda_societa": self.params_widget.get_societa(),
            "last_oda_fornitore": self.params_widget.get_fornitore(),
            "last_oda_date_da": date_da,
            "last_oda_date_a": date_a,
            "path_dettagli_oda": self.params_widget.get_dest_path(),
        }

        config_manager.set_config_values(updates)

    def _clear_table(self) -> None:
        """Svuota l'elenco OdA previa conferma dell'utente."""
        if ConfirmationDialog.confirm(self, "Conferma", "Svuotare la tabella?"):
            self.data_table.clear()
            self._save_data()

    def validate_ready(self) -> tuple[bool, str]:
        """
        Valida i requisiti minimi per l'avvio del bot.

        Returns:
            tuple: (bool pronto, messaggio errore).
        """
        username, password = self.get_credentials()
        if not username or not password:
            return False, "Credenziali ISAB mancanti."
        if not self.params_widget.get_fornitore():
            return False, "Fornitore mancante."
        return True, ""

    def _on_start(self, params_override: dict[str, Any] | None = None) -> None:
        """Inizializza il bot e avvia il thread di esecuzione (Worker)."""
        super()._on_start(params_override)
        username, password = self.get_credentials()
        societa = self.params_widget.get_societa()
        fornitore = self.params_widget.get_fornitore()
        data_da, data_a = self.params_widget.get_dates()
        download_path = self.params_widget.get_dest_path() or str(Path.home() / "Downloads")
        rows = self.data_table.get_data()

        if params_override:
            data_da = params_override.get("data_da", data_da)
            data_a = params_override.get("data_a", data_a)
            if "rows" in params_override:
                rows = params_override["rows"]
            elif item := params_override.get("single_item"):
                rows = [item]
                self.log_widget.append(f"ℹ️ Esecuzione singola per: {item.get('Numero OdA', 'N/D')}")

        if not all([username, password, fornitore]):
            ToastManager.instance().show("Verifica i parametri.", "warning")
            self._update_status(STATUS_COLORS["error"], "Parametri incompleti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        if not params_override:
            self._save_data()

        from src.core.config_manager import load_config

        config = load_config()

        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        # Configura i parametri per il BotWorker (verranno passati a create_bot nel thread secondario)
        bot_params = {
            "username": username,
            "password": password,
            "headless": config.get("browser_headless", False),
            "timeout": config.get("browser_timeout", 30),
            "download_path": download_path,
            "fornitore": fornitore,
            "company": societa,
            "data_da": data_da,
            "data_a": data_a,
        }

        # Dati da elaborare (verranno passati a bot.execute() nel thread secondario)
        data = {
            "rows": rows,
            "fornitore": fornitore,
            "company": societa,
            "data_da": data_da,
            "data_a": data_a,
        }

        # Inizializza il worker (nessuna importazione pesante Selenium qui)
        self.worker = BotWorker(
            bot_id="dettagli_oda",
            bot_params=bot_params,
            data=data,
            telegram_service=tg_service,
        )

        self._setup_worker_connections(self.worker)

        # Reset pallini all'avvio (Asincrono per non bloccare il click)
        from PySide6.QtCore import QTimer

        QTimer.singleShot(0, lambda: self._update_status_list(force=True))

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append(f"Avvio bot Dettagli OdA ({fornitore})")
        self.log_widget.append(f"  Periodo: {data_da} - {data_a}")
        self.worker.start()
        self.bot_started.emit()

    def _on_worker_finished(self, success: bool) -> None:
        """Gestisce la pulizia post-esecuzione e tenta di aggiornare il pannello storico."""
        super()._on_worker_finished(success)
        if (
            success
            and (win := self.window())
            and (storico := getattr(win, "storico_oda_panel", None))
            and hasattr(storico, "refresh_data")
        ):
            storico.refresh_data()
            self._on_log("[SYNC] Aggiornamento Storico OdA avviato.")
