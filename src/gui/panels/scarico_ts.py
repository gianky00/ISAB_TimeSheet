"""
SyncroJob - Scarico TS Panel
Pannello per il bot Scarico TS.
"""

from __future__ import annotations

import traceback
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel
from src.gui.widgets import BotParametersWidget, EditableDataTable
from src.gui.widgets.core_widgets import (
    StandardCheckBox,
)
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.safework.status_list import StatusListWidget
from src.utils.helpers import get_asset_path

if TYPE_CHECKING:
    from src.bots.base.base_bot import BaseBot


class ScaricaTSPanel(BaseBotPanel):
    """Pannello per il bot Scarico TS."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello Scarico TS.

        Args:
            parent: Widget genitore.
        """
        super().__init__(
            bot_id="scarico_ts",
            bot_name="Scarico TS",
            bot_description="Tasto destro per aggiungere/rimuovere righe. Modifica i valori direttamente nelle celle.",
            parent=parent,
        )

        from src.gui.controllers.bot_execution_controller import BotExecutionController

        self.bot_controller = BotExecutionController("scarico_ts", self)
        self._setup_controller_connections()

        self.params_widget: BotParametersWidget
        self.elabora_ts_check: StandardCheckBox
        self.clear_btn: ModernButton
        self.data_table: EditableDataTable
        self.status_list: StatusListWidget

        self._setup_content()
        # Forza inizializzazione timeline immediata per Scarico TS
        from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot

        self.activity_timeline.set_steps(ScaricaTSBot.STEPS)

        self._data_loaded = False
        # Il caricamento dati viene differito a showEvent

    def _setup_controller_connections(self) -> None:
        """Connette i segnali del controller agli slot del pannello."""
        self.bot_controller.log_received.connect(self._on_log)
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
        Restituisce la classe ScaricaTSBot associata a questo pannello.
        """
        from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot

        return ScaricaTSBot

    def _safe_load_data(self) -> None:
        """Carica i dati dai file di configurazione in modo sicuro."""
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"[ERROR] Error loading data for ScaricaTSPanel: {e}")
            traceback.print_exc()

    def _setup_content(self) -> None:
        """Inizializza e posiziona i componenti UI specifici del pannello."""
        from src.gui.styles.ui_effects import UIEffectsManager
        from src.gui.styles.widget_styles import CARD_SHADOW_BLUR, CARD_SHADOW_COLOR

        params_container = QWidget()
        # Card style wrap
        params_container.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #dee2e6;")
        UIEffectsManager.apply_shadow(params_container, blur=CARD_SHADOW_BLUR, color=CARD_SHADOW_COLOR)
        UIEffectsManager.animate_fade(params_container, duration=400)

        self.params_layout = QVBoxLayout(params_container)
        self.params_layout.setContentsMargins(15, 15, 15, 15)
        self.params_layout.setSpacing(5)

        self._setup_params_section()
        self._setup_table_section()

        self.content_layout.addWidget(params_container)

    def _setup_params_section(self) -> None:
        """Configura la sezione dei parametri e la toolbar della tabella."""
        # Usiamo il widget atomico per i parametri comuni
        self.params_widget = BotParametersWidget(show_date_range=False, show_dest_path=True)
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        self.params_layout.addWidget(self.params_widget)

        # Parametri specifici: Flag Elabora TS
        self.elabora_ts_check = StandardCheckBox("Elabora TS")
        self.elabora_ts_check.stateChanged.connect(lambda _: self._save_data())
        self.params_widget.add_widget_to_row(self.elabora_ts_check)

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
        table_h = QHBoxLayout()
        table_h.setSpacing(10)

        # Tabella con tutte le colonne del database Scarico TS + ESITO
        bot_class = self.get_bot_class()
        cols = list(bot_class.get_columns())
        cols.append({"name": "esito", "label": "ESITO", "type": "text", "default": "", "readonly": True})

        self.data_table = EditableDataTable(cols)
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._update_status_list)
        self.data_table.data_changed.connect(self._save_data)

        # Status List (Pallini a sinistra)
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
        """Aggiorna il numero di righe nella lista degli stati."""
        count = self.data_table.table.rowCount()
        if force or self.status_list.count() != count:
            self.status_list.initialize_rows(count, self.data_table.table.rowHeight(0) or 30)

    def on_step_completed(self, step_idx: int, success: bool, message: str = "") -> None:
        """Aggiorna lo stato della riga quando il bot termina l'elaborazione."""
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
        """Apre il pannello impostazioni."""
        main_window: Any = self.window()
        if main_window and hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def refresh_fornitori(self) -> None:
        """Ricarica l'elenco dei fornitori."""
        if hasattr(self, "params_widget"):
            self.params_widget.refresh_fornitori()

    def _load_saved_data(self) -> None:
        """Carica i dati salvati."""
        self._is_loading = True
        try:
            from src.core.bots.services import ScaricoTSService

            service = ScaricoTSService()
            cfg = service.load_config()

            self.refresh_fornitori()
            self.params_widget.set_societa(cfg["societa"])
            self.params_widget.set_fornitore(cfg["fornitore"])
            self.params_widget.set_dest_path(cfg["dest_path"])
            self.elabora_ts_check.setChecked(cfg["elabora_ts"])

            if cfg["data"]:
                self.data_table.set_data(cfg["data"])

            self._update_status_list()
        finally:
            self._is_loading = False

    def _save_data(self) -> None:
        """Salva i dati correnti."""
        from PySide6.QtWidgets import QApplication

        if QApplication.closingDown():
            return
        if getattr(self, "_is_loading", False) or not hasattr(self, "params_widget"):
            return

        from src.core.bots.services import ScaricoTSService

        service = ScaricoTSService()

        params = {
            "societa": self.params_widget.get_societa(),
            "fornitore": self.params_widget.get_fornitore(),
            "dest_path": self.params_widget.get_dest_path(),
            "elabora_ts": self.elabora_ts_check.isChecked(),
        }

        service.save_config(params, self.data_table.get_data())

    def _clear_table(self) -> None:
        """Svuota la tabella."""
        if ConfirmationDialog.confirm(self, "Conferma", "Svuotare la tabella?"):
            self.data_table.clear()
            self._save_data()

    def validate_ready(self) -> tuple[bool, str]:
        """
        Verifica se tutti i campi necessari sono stati compilati correttamente.

        Returns:
            tuple: (bool successo, str messaggio errore)
        """
        if not self.data_table.get_data():
            return False, "Nessun dato OdA inserito in tabella."
        return True, ""

    def _on_start(self, params_override: dict[str, Any] | None = None) -> None:
        """
        Avvia l'esecuzione del bot Scarico TS gestendo il controller.

        Args:
            params_override: Parametri opzionali per sovrascrivere l'UI.
        """
        super()._on_start(params_override)

        if not params_override:
            self._save_data()

        from src.core.bots.services import ScaricoTSService

        service = ScaricoTSService()

        data_da, _ = self.params_widget.get_dates()
        params = {
            "societa": self.params_widget.get_societa(),
            "fornitore": self.params_widget.get_fornitore(),
            "dest_path": self.params_widget.get_dest_path(),
            "elabora_ts": self.elabora_ts_check.isChecked(),
            "data_da": data_da,
        }

        username, password = self.get_credentials()
        bot_params, bot_payload = service.prepare_payload(
            (username, password, ""), params, self.data_table.get_data(), params_override
        )
        main_win: Any = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        # Delega l'avvio al controller
        self.log_widget.clear()
        self.log_widget.append("Preparazione Bot Scarico TS...")

        # Passa direttamente bot_payload (dizionario strutturato con chiave 'rows')
        bot_data = bot_payload

        if self.bot_controller.start(bot_params, bot_data, tg_service):
            self.bot_started.emit()
        else:
            self.log_widget.append("❌ Errore: Il bot è già in esecuzione.")

    def _on_stop(self) -> None:
        """Gestisce la richiesta di stop."""
        self.bot_controller.stop()
        super()._on_stop()

    def _on_worker_finished(self, success: bool) -> None:
        """Chiamato al termine del bot."""
        super()._on_worker_finished(success)
        # Se successo, potremmo voler aggiornare altri componenti
