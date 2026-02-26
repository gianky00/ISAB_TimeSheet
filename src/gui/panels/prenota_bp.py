"""
SyncroJob - Prenota BP Panel.

Gestisce l'interfaccia utente per il bot di prenotazione dei Badge Provvisori (BP)
sul portale fornitori ISAB. Consente di inserire una lista di BP, configurare
il fornitore e l'intervallo temporale, e avviare l'automazione.
"""

from typing import Any

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from src.core import config_manager
from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.styles import STATUS_COLORS
from src.gui.widgets import BotParametersWidget, EditableDataTable
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path


class PrenotaBPPanel(BaseBotPanel):
    """
    Pannello operativo per l'automazione della prenotazione BP.
    Eredita da BaseBotPanel per la gestione standard di log e stati.
    """

    def __init__(self, parent=None):
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
        self._setup_content()
        # Caricamento dati differito per non rallentare l'avvio GUI
        QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self):
        """
        Restituisce la classe del bot associata al pannello.

        Returns:
            Type[PrenotaBPBot]: Classe del bot.
        """
        from src.bots.portale_fornitori.prenota_bp.bot import PrenotaBPBot

        return PrenotaBPBot

    def _safe_load_data(self):
        """Esegue il caricamento dei dati in modo sicuro gestendo eventuali eccezioni."""
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for PrenotaBPPanel: {e}")

    def _setup_content(self):
        """Configura il layout e i widget specifici per la prenotazione BP."""
        # Sezione Parametri
        params_container = QWidget()
        params_layout = QVBoxLayout(params_container)
        params_layout.setContentsMargins(0, 0, 0, 0)
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

        # Definiamo le colonne
        columns = [
            {"name": "NUMERO BP", "type": "text"},
            {"name": "NOTE DI RITIRO", "type": "text"},
        ]
        self.data_table = EditableDataTable(columns)
        self.data_table.setMinimumHeight(200)
        self.data_table.data_changed.connect(self._save_data)
        params_layout.addWidget(self.data_table)

        self.content_layout.addWidget(params_container)

    def _open_settings(self):
        """Richiede alla MainWindow di visualizzare la pagina delle impostazioni."""
        main_window = self.window()
        if main_window is not None and hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def _load_saved_data(self):
        """Carica l'ultima lista BP e i parametri temporali dalla configurazione."""
        config = config_manager.load_config()
        saved_data = config.get("last_prenota_bp_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)

        current_year = datetime.now().year
        date_da = config.get("last_prenota_date_from", f"01.01.{current_year}")
        date_a = config.get("last_prenota_date_to", f"31.12.{current_year}")
        self.params_widget.set_dates(date_da, date_a)

    def _save_data(self):
        """Salva i dati correnti della tabella e i parametri temporali in configurazione."""
        data = self.data_table.get_data()
        config_manager.set_config_value("last_prenota_bp_data", data)

        date_da, date_a = self.params_widget.get_dates()
        config_manager.set_config_value("last_prenota_date_from", date_da)
        config_manager.set_config_value("last_prenota_date_to", date_a)

    def _clear_table(self):
        """Svuota la tabella dei BP dopo conferma dell'utente."""
        if ConfirmationDialog.confirm(self, "Conferma", "Cancellare tutti i dati dalla lista?"):
            self.data_table.clear()
            self._save_data()

    def _on_start(self, params_override: dict[str, Any] | None = None):
        """
        Prepara l'ambiente e avvia il worker del bot.

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
        from src.bots.portale_fornitori.prenota_bp.bot import PrenotaBPBot

        username, password = self.get_credentials()
        config = config_manager.load_config()

        fornitore = self.params_widget.get_fornitore()
        date_da, date_a = self.params_widget.get_dates()

        # Gestione Overrides
        rows = self.data_table.get_data()
        if params_override:
            if "fornitore" in params_override:
                fornitore = params_override["fornitore"]
            if "data_da" in params_override:
                date_da = params_override["data_da"]
            if "data_a" in params_override:
                date_a = params_override["data_a"]

            if "single_item" in params_override:
                item = params_override["single_item"]
                if item:
                    rows = [item]
                    self.log_widget.append(f"ℹ️ Esecuzione singola per BP: {item.get('numero_bp', 'N/D')}")

        date_da, date_a_opt = self.params_widget.get_dates()
        date_a = date_a_opt or ""

        bot = PrenotaBPBot(
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            fornitore=fornitore,
            data_da=date_da,
            data_a=date_a,
        )

        bot_data = {
            "rows": rows,
            "fornitore": fornitore,
            "data_da": date_da,
            "data_a": date_a,
        }

        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        worker = BotWorker(bot, bot_data, telegram_service=tg_service)
        self.worker = worker
        self._setup_worker_connections(worker)

        # UI Update
        self._update_status(STATUS_COLORS["running"], "Esecuzione...")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Avvio bot Prenota BP...")
        worker.start()
        self.bot_started.emit()
