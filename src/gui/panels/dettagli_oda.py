"""
SyncroJob - Dettagli OdA Panel
Pannello per il bot Dettagli OdA.
"""

import traceback
from pathlib import Path
from typing import Any, Dict, Optional

from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QMessageBox, QVBoxLayout

from src.core import config_manager
from src.core.constants import Icons
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.widgets import BotParametersWidget, EditableDataTable
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path


class DettagliOdAPanel(BaseBotPanel):
    """Pannello per il bot Dettagli OdA."""

    def __init__(self, parent=None):
        super().__init__(
            bot_id="dettagli_oda",
            bot_name="Dettagli OdA",
            bot_description="Scarica automaticamente i dettagli degli Ordini d'Acquisto.",
            parent=parent,
        )
        self._setup_content()
        # Defer data loading
        QTimer.singleShot(10, self._safe_load_data)

    def _safe_load_data(self):
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for DettagliOdAPanel: {e}")
            traceback.print_exc()

    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        params_group = QGroupBox("Parametri")
        params_layout = QVBoxLayout(params_group)
        params_layout.setSpacing(10)

        # Widget atomico per i parametri
        self.params_widget = BotParametersWidget(
            show_date_range=True, show_dest_path=True
        )
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        params_layout.addWidget(self.params_widget)

        params_layout.addSpacing(10)

        # Tabella
        table_toolbar = QHBoxLayout()
        table_toolbar.addStretch()
        self.clear_btn = ModernButton(
            "Pulisci Tabella",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),
        )
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)
        params_layout.addLayout(table_toolbar)

        # Carica lista contratti salvati
        config = config_manager.load_config()
        contracts = config.get("contracts", [])

        self.data_table = EditableDataTable(
            [
                {"name": "Numero OdA", "type": "text"},
                {
                    "name": "Numero Contratto",
                    "type": "combo",
                    "options": contracts,
                    "default": config.get("default_contract", ""),
                },
            ]
        )
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._save_data)
        params_layout.addWidget(self.data_table)

        self.content_layout.addWidget(params_group)

    def _open_settings(self):
        main_window = self.window()
        if hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def refresh_fornitori(self):
        """Ricarica i fornitori nel pannello Dettagli OdA."""
        self.params_widget.refresh_fornitori()

    def _load_saved_data(self):
        config = config_manager.load_config()
        self.refresh_fornitori()

        self.params_widget.set_fornitore(config.get("last_oda_fornitore", ""))
        self.params_widget.set_dates(
            config.get("last_oda_date_da", "01.01.2025"),
            config.get("last_oda_date_a", QDate.currentDate().toString("dd.MM.yyyy")),
        )
        self.params_widget.set_dest_path(config.get("path_dettagli_oda", ""))

        saved_data = config.get("last_oda_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)

    def _save_data(self):
        if not hasattr(self, "params_widget"):
            return

        data = self.data_table.get_data()
        date_da, date_a = self.params_widget.get_dates()

        config_manager.set_config_value("last_oda_data", data)
        config_manager.set_config_value(
            "last_oda_fornitore", self.params_widget.get_fornitore()
        )
        config_manager.set_config_value("last_oda_date_da", date_da)
        config_manager.set_config_value("last_oda_date_a", date_a)
        config_manager.set_config_value(
            "path_dettagli_oda", self.params_widget.get_dest_path()
        )

    def _clear_table(self):
        if (
            QMessageBox.question(self, "Conferma", "Svuotare la tabella?")
            == QMessageBox.StandardButton.Yes
        ):
            self.data_table.set_data([])
            self._save_data()

    def validate_ready(self) -> tuple[bool, str]:
        """Verifica se il pannello è pronto per l'avvio del bot."""
        username, password = self.get_credentials()
        if not username or not password:
            return False, "Credenziali ISAB mancanti."
        if not self.params_widget.get_fornitore():
            return False, "Fornitore mancante."

        return True, ""

    def _on_start(self, params_override: Optional[Dict[str, Any]] = None):
        super()._on_start(params_override)

        username, password = self.get_credentials()
        fornitore = self.params_widget.get_fornitore()
        data_da, data_a = self.params_widget.get_dates()
        download_path = self.params_widget.get_dest_path() or str(
            Path.home() / "Downloads"
        )

        rows = self.data_table.get_data()

        # Override logic
        if params_override:
            if "data_da" in params_override:
                data_da = params_override["data_da"]
            if "data_a" in params_override:
                data_a = params_override["data_a"]

            # Single Shot
            if "single_item" in params_override:
                item = params_override["single_item"]
                if item:
                    rows = [item]
                    self.log_widget.append(
                        f"ℹ️ Esecuzione singola per: {item.get('Numero OdA', 'N/D')}"
                    )

        self.log_widget.append(f"[DEBUG] Rows retrieved: {len(rows)}")

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
            data_a=data_a,
        )

        if not bot:
            ToastManager.instance().show("Errore creazione bot.", "error")
            return

        bot_data = {
            "rows": rows,
            "fornitore": fornitore,
            "data_da": data_da,
            "data_a": data_a,
        }

        # Get telegram service safely
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        self.worker = BotWorker(bot, bot_data, telegram_service=tg_service)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append(f"Avvio bot Dettagli OdA ({fornitore})")
        self.log_widget.append(f"  Periodo: {data_da} - {data_a}")
        self.worker.start()
        self.bot_started.emit()

    def _on_worker_finished(self, success: bool):
        """Override per aggiornare Storico OdA dopo il completamento."""
        super()._on_worker_finished(success)

        if success:
            win = self.window()
            if win and hasattr(win, "storico_oda_panel"):
                win.storico_oda_panel.refresh_data()
                self._on_log("🔄 Aggiornamento Storico OdA avviato.")
