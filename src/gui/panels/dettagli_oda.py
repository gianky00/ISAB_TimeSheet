"""
SyncroJob - Dettagli OdA Panel
Pannello di controllo dedicato al bot per l'estrazione massiva dei dettagli degli Ordini d'Acquisto (OdA).
Permette di configurare un elenco di OdA e contratti, impostare range temporali e monitorare
il download automatico dei documenti dal portale fornitori.
"""

import traceback
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from src.core import config_manager
from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.widgets import BotParametersWidget, EditableDataTable
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path


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
        self._setup_content()
        QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self) -> type:
        """Restituisce la classe bot specifica per lo scarico dei dettagli OdA."""
        from src.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot
        return DettagliOdABot

    def _safe_load_data(self) -> None:
        """Tenta il caricamento delle ultime impostazioni salvate gestendo errori di parsing."""
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for DettagliOdAPanel: {e}")
            traceback.print_exc()

    def _setup_content(self) -> None:
        """Costruisce il layout specifico con widget parametri e tabella dati editabile."""
        # Sezione Parametri (Senza QGroupBox per favorire il design Floating Card)
        params_container = QWidget()
        params_layout = QVBoxLayout(params_container)
        params_layout.setContentsMargins(0, 0, 0, 0)
        params_layout.setSpacing(5)

        self.params_widget = BotParametersWidget(show_date_range=True, show_dest_path=True)
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
            icon=get_asset_path(Icons.TRASH)
        )
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)
        params_layout.addLayout(table_toolbar)

        config = config_manager.load_config()
        self.data_table = EditableDataTable([
            {"name": "Numero OdA", "type": "text"},
            {"name": "Numero Contratto", "type": "combo", "options": config.get("contracts", []), "default": config.get("default_contract", "")},
        ])
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._save_data)
        params_layout.addWidget(self.data_table)

        self.content_layout.addWidget(params_container)

    def _open_settings(self) -> None:
        """Comunica alla finestra principale di mostrare la pagina delle impostazioni."""
        main_window = self.window()
        if main_window and hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def refresh_fornitori(self) -> None:
        """Aggiorna la lista dei fornitori selezionabili nel widget parametri."""
        self.params_widget.refresh_fornitori()

    def _load_saved_data(self) -> None:
        """Ripristina lo stato del pannello (date, fornitori, tabella) dall'ultimo salvataggio."""
        config = config_manager.load_config()
        self.refresh_fornitori()
        self.params_widget.set_fornitore(config.get("last_oda_fornitore", ""))
        self.params_widget.set_dates(
            config.get("last_oda_date_da", "01.01.2025"),
            config.get("last_oda_date_a", QDate.currentDate().toString("dd.MM.yyyy"))
        )
        self.params_widget.set_dest_path(config.get("path_dettagli_oda", ""))
        if saved_data := config.get("last_oda_data", []):
            self.data_table.set_data(saved_data)

    def _save_data(self) -> None:
        """Persiste i parametri attuali nella configurazione globale."""
        if not hasattr(self, "params_widget"):
            return
        date_da, date_a = self.params_widget.get_dates()
        config_manager.set_config_value("last_oda_data", self.data_table.get_data())
        config_manager.set_config_value("last_oda_fornitore", self.params_widget.get_fornitore())
        config_manager.set_config_value("last_oda_date_da", date_da)
        config_manager.set_config_value("last_oda_date_a", date_a)
        config_manager.set_config_value("path_dettagli_oda", self.params_widget.get_dest_path())

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
        fornitore = self.params_widget.get_fornitore()
        data_da, data_a = self.params_widget.get_dates()
        download_path = self.params_widget.get_dest_path() or str(Path.home() / "Downloads")
        rows = self.data_table.get_data()

        if params_override:
            data_da, data_a = params_override.get("data_da", data_da), params_override.get("data_a", data_a)
            if item := params_override.get("single_item"):
                rows = [item]
                self.log_widget.append(f"ℹ️ Esecuzione singola per: {item.get('Numero OdA', 'N/D')}")

        if not all([username, password, fornitore]):
            ToastManager.instance().show("Verifica i parametri.", "warning")
            self._update_status("#C62828", "Parametri incompleti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        if not params_override:
            self._save_data()

        from src.bots import create_bot
        config = config_manager.load_config()
        bot = create_bot(
            "dettagli_oda",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=download_path,
            fornitore=fornitore,
            data_da=data_da,
            data_a=data_a
        )

        if not bot:
            ToastManager.instance().show("Errore creazione bot.", "error")
            return

        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None
        worker = BotWorker(
            bot,
            {"rows": rows, "fornitore": fornitore, "data_da": data_da, "data_a": data_a},
            telegram_service=tg_service
        )
        self.worker = worker
        self._setup_worker_connections(worker)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append(f"Avvio bot Dettagli OdA ({fornitore})")
        self.log_widget.append(f"  Periodo: {data_da} - {data_a}")
        worker.start()
        self.bot_started.emit()

    def _on_worker_finished(self, success: bool) -> None:
        """Gestisce la pulizia post-esecuzione e tenta di aggiornare il pannello storico."""
        super()._on_worker_finished(success)
        if success and (win := self.window()) and (storico := getattr(win, "storico_oda_panel", None)) and hasattr(storico, "refresh_data"):
            storico.refresh_data()
            self._on_log("🔄 Aggiornamento Storico OdA avviato.")
