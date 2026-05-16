"""
SyncroJob - Prenota BP Panel.

Gestisce l'interfaccia utente per il bot di prenotazione dei Badge Provvisori (BP)
sul portale fornitori ISAB. Consente di inserire una lista di BP, configurare
il fornitore e l'intervallo temporale, e avviare l'automazione.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel
from src.gui.styles import STATUS_COLORS
from src.gui.widgets import BotParametersWidget, EditableDataTable
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.safework.status_list import StatusListWidget
from src.utils.helpers import get_asset_path

if TYPE_CHECKING:
    from src.bots.base.base_bot import BaseBot


class PrenotaBPPanel(BaseBotPanel):
    """
    Pannello operativo per l'automazione della prenotazione BP.
    Eredita da BaseBotPanel per la gestione standard di log e stati.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello e carica i dati salvati.

        Args:
            parent: Widget genitore.
        """
        super().__init__(
            bot_id="prenota_bp",
            bot_name="Prenota BP",
            bot_description="Gestisce la prenotazione dei Badge Provvisori sul portale.",
            parent=parent,
        )

        from src.gui.controllers.bot_execution_controller import BotExecutionController

        self.bot_controller = BotExecutionController("prenota_bp", self)
        self._setup_controller_connections()

        self.params_widget: BotParametersWidget
        self.clear_btn: ModernButton
        self.data_table: EditableDataTable
        self.status_list: StatusListWidget

        self._setup_content()
        self._data_loaded = False
        # Il caricamento dati viene differito a showEvent

    def _setup_controller_connections(self) -> None:
        """Connette i segnali del controller agli slot del pannello."""
        self.bot_controller.log_received.connect(self.log_widget.append)
        self.bot_controller.execution_finished.connect(self._on_worker_finished)
        self.bot_controller.row_status_updated.connect(self.on_step_completed)
        self.bot_controller.step_changed.connect(self.activity_timeline.on_step_changed)
        self.bot_controller.critical_error.connect(lambda t, m: ConfirmationDialog.show_error(self, t, m))
        self.bot_controller.input_requested.connect(self._ask_user_input)

    def showEvent(self, event: Any) -> None:
        """Esegue il primo caricamento dati solo quando il pannello diventa visibile."""
        super().showEvent(event)
        if not self._data_loaded:
            self._data_loaded = True
            QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self) -> type[BaseBot]:
        """
        Restituisce la classe del bot associata al pannello.

        Returns:
            Type[PrenotaBPBot]: Classe del bot.
        """
        from src.bots.portale_fornitori.prenota_bp.bot import PrenotaBPBot

        return PrenotaBPBot

    def _safe_load_data(self) -> None:
        """Esegue il caricamento dei dati in modo sicuro gestendo eventuali eccezioni."""
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"[ERROR] Error loading data for PrenotaBPPanel: {e}")

    def _setup_content(self) -> None:
        """Configura il layout e i widget specifici per la prenotazione BP."""
        from src.gui.styles.ui_effects import UIEffectsManager
        from src.gui.styles.widget_styles import CARD_SHADOW_BLUR, CARD_SHADOW_COLOR, CARD_STYLE

        params_container = QWidget()
        params_container.setStyleSheet(CARD_STYLE)
        UIEffectsManager.apply_shadow(params_container, blur=CARD_SHADOW_BLUR, color=CARD_SHADOW_COLOR)
        UIEffectsManager.animate_fade(params_container, duration=400)

        params_layout = QVBoxLayout(params_container)
        params_layout.setContentsMargins(15, 15, 15, 15)
        params_layout.setSpacing(5)

        # Widget atomico per i parametri
        self.params_widget = BotParametersWidget(show_date_range=True, show_dest_path=False)
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        params_layout.addWidget(self.params_widget)

        # Tabella Toolbar
        table_toolbar = QHBoxLayout()
        table_toolbar.setContentsMargins(10, 0, 10, 0)
        table_toolbar.addStretch()
        self.clear_btn = ModernButton(
            "Pulisci Tabella",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),
            parent=self,
        )
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)
        params_layout.addLayout(table_toolbar)

        # 2. Tabella e Stati
        table_h = QHBoxLayout()
        table_h.setSpacing(10)

        # Recupera le colonne dal bot e aggiunge la colonna ESITO
        bot_class = self.get_bot_class()
        cols = list(bot_class.get_columns())
        cols.append({"name": "esito", "label": "ESITO", "type": "text", "default": "", "readonly": True})

        self.data_table = EditableDataTable(cols)
        self.data_table.setMinimumHeight(200)
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
        params_layout.addLayout(table_h)

        self.content_layout.addWidget(params_container)

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
        """Richiede alla MainWindow di visualizzare la pagina delle impostazioni."""
        main_window: Any = self.window()
        if main_window is not None and hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def _load_saved_data(self) -> None:
        """Carica l'ultima lista BP e i parametri temporali dalla configurazione."""
        self._is_loading = True
        try:
            from src.core.bots.services import PrenotaBPService

            service = PrenotaBPService()
            cfg = service.load_config()

            self.params_widget.set_societa(cfg["societa"])
            self.params_widget.set_fornitore(cfg["fornitore"])
            if cfg["data"]:
                self.data_table.set_data(cfg["data"])

            self.params_widget.set_dates(cfg["data_da"], cfg["data_a"])
            self._update_status_list()
        finally:
            self._is_loading = False

    def _save_data(self) -> None:
        """Salva i dati correnti della tabella e i parametri temporali in configurazione."""
        if getattr(self, "_is_loading", False) or not hasattr(self, "params_widget"):
            return

        date_da, date_a = self.params_widget.get_dates()
        params = {
            "societa": self.params_widget.get_societa(),
            "fornitore": self.params_widget.get_fornitore(),
            "data_da": date_da,
            "data_a": date_a,
        }

        from src.core.bots.services import PrenotaBPService

        service = PrenotaBPService()
        service.save_config(params, self.data_table.get_data())

    def _clear_table(self) -> None:
        """Svuota la tabella dei BP dopo conferma dell'utente."""
        if ConfirmationDialog.confirm(self, "Conferma", "Cancellare tutti i dati dalla lista?"):
            self.data_table.clear()
            self._save_data()

    def _on_start(self, params_override: dict[str, Any] | None = None) -> None:
        """
        Prepara l'ambiente e avvia il worker del bot tramite controller.

        Args:
            params_override: Eventuali parametri che sovrascrivono quelli della UI.
        """
        super()._on_start(params_override)

        # Validazione form
        ready, msg = self.validate_ready()
        if not ready:
            ConfirmationDialog.show_warning(self, "Attenzione", msg)
            self._update_status(STATUS_COLORS["error"], "Validazione fallita")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        # Recupera dati e configura bot
        username, password = self.get_credentials()

        date_da, date_a_opt = self.params_widget.get_dates()
        params = {
            "societa": self.params_widget.get_societa(),
            "fornitore": self.params_widget.get_fornitore(),
            "data_da": date_da,
            "data_a": date_a_opt or "",
        }

        if not params_override:
            self._save_data()

        from src.core.bots.services import PrenotaBPService

        service = PrenotaBPService()

        bot_params, bot_payload = service.prepare_payload(
            (username, password, ""), params, self.data_table.get_data(), params_override
        )

        main_win: Any = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        # Reset pallini all'avvio
        self._update_status_list(force=True)

        # UI Update
        self._update_status(STATUS_COLORS["running"], "Esecuzione...")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Preparazione Bot Prenota BP...")

        # BotWorker aspetta list[dict] nel parametro data
        # prepare_payload restituisce (params, data_dict)
        # Assicuriamoci che bot_data sia una lista
        bot_data = [bot_payload] if isinstance(bot_payload, dict) else bot_payload

        # Delega l'avvio al controller universale
        if self.bot_controller.start(bot_params, bot_data, tg_service):
            self.bot_started.emit()
        else:
            self.log_widget.append("❌ Errore: Il bot è già in esecuzione.")
            self._update_status(STATUS_COLORS["error"], "Errore avvio")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

    def _on_stop(self) -> None:
        """Gestisce la richiesta di stop tramite controller."""
        self.bot_controller.stop()
        super()._on_stop()
