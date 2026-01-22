"""
SyncroJob - Bot Panels
Pannelli specifici per ogni bot.
"""

import threading
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PyQt6.QtCore import QDate, QSize, Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QStyledItemDelegate,
    QTableView,  # Moved from bottom
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage
from src.core import config_manager
from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.core.database import db_manager
from src.core.stats_manager import StatsManager
from src.gui.design.spacing import Spacing  # Added import
from src.gui.formatters import FastTableModel  # Moved from bottom

# Import UI Components
from src.gui.widgets import (
    BotParametersWidget,
    EditableDataTable,
    LogWidget,
    MissionReportCard,
)
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.status_card import StatusCard
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon
from src.utils.printing import get_installed_printers


class BotWorker(QThread):
    """
    Thread worker per eseguire i bot in background.
    Gestisce i segnali di log, stato, conclusione e richieste di input interattivo.
    """

    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)
    request_input_signal = pyqtSignal(str, dict, threading.Event)

    def __init__(self, bot, data, telegram_service=None):
        """
        Inizializza il worker del bot.

        Args:
            bot: L'istanza del bot da eseguire.
            data: I dati di input per il bot.
            telegram_service: Servizio opzionale per notifiche Telegram.
        """
        super().__init__()
        self.bot = bot
        self.data = data
        self._is_running = True
        self.telegram_service = telegram_service

    def run(self):
        """Avvia l'esecuzione del bot nel thread dedicato."""
        try:
            # Collega i callback
            self.bot.set_log_callback(self.log_signal.emit)

            # Setup input callback se supportato dal bot
            if hasattr(self.bot, "set_input_callback"):
                self.bot.set_input_callback(self._request_input_wrapper)

            result = self.bot.execute(self.data)
            self.finished_signal.emit(result)
        except Exception as e:
            error_trace = traceback.format_exc()
            self.log_signal.emit(f"[ERRORE CRITICO] {e}\n{error_trace}")
            self.finished_signal.emit(False)

    def _request_input_wrapper(self, prompt: str) -> str:
        """
        Wrapper thread-safe per richiedere input all'utente tramite la GUI.
        Blocca l'esecuzione del bot finché l'utente non risponde.

        Args:
            prompt: Messaggio da mostrare all'utente.
        Returns:
            str: Il valore inserito dall'utente.
        """
        result_container: Dict[str, str] = {}
        event = threading.Event()
        self.request_input_signal.emit(prompt, result_container, event)
        event.wait()
        return result_container.get("value", "")

    def stop(self):
        """Interrompe l'esecuzione del bot segnalando la richiesta di stop."""
        self._is_running = False
        if hasattr(self.bot, "request_stop"):
            self.bot.request_stop()


class BaseBotPanel(QWidget):
    """
    Classe base per i pannelli di controllo dei bot.
    Gestisce l'interfaccia comune: tabella dati, log, controlli di avvio/stop e report.
    """

    bot_started = pyqtSignal()
    bot_stopped = pyqtSignal()
    bot_finished = pyqtSignal(bool)
    bot_results_ready = pyqtSignal(
        str, list
    )  # bot_id, list of results (e.g. file paths)
    status_changed = pyqtSignal(str, str)  # status, message

    def __init__(self, bot_id: str, bot_name: str, bot_description: str, parent=None):
        """
        Inizializza il pannello base.

        Args:
            bot_id: Identificativo unico del bot.
            bot_name: Nome visualizzato del bot.
            bot_description: Descrizione delle funzionalità del bot.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.bot_description = bot_description

        self.worker = None
        self.start_time = None
        self._setup_ui()
        self._connect_signals()

    def _setup_base_ui(self):
        """Inizializza l'interfaccia utente di base comune a tutti i pannelli bot."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            Spacing.md, Spacing.md, Spacing.md, Spacing.md
        )
        self.main_layout.setSpacing(Spacing.md)

        # Status Card (Model only, not in layout)
        self.status_card = StatusCard("Stato Attività")

        # Content area (da sovrascrivere nelle sottoclassi)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(Spacing.md)
        self.main_layout.addWidget(self.content_widget)

        # Log
        self.log_widget = LogWidget()
        self.main_layout.addWidget(self.log_widget)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(Spacing.sm)
        btn_layout.addStretch()

        self.start_btn = ModernButton(
            "Avvia",
            variant=ModernButton.Variant.SUCCESS,
            size=ModernButton.Size.LARGE,
            icon=get_asset_path(Icons.PLAY),
        )
        self.start_btn.setMinimumWidth(120)
        self.start_btn.clicked.connect(self._on_start)
        btn_layout.addWidget(self.start_btn)

        self.stop_btn = ModernButton(
            "Stop",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.LARGE,
            icon=get_asset_path(Icons.STOP),
        )
        self.stop_btn.setMinimumWidth(100)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._on_stop)
        btn_layout.addWidget(self.stop_btn)

        self.main_layout.addLayout(btn_layout)

    def _setup_ui(self):
        """
        Inizializza l'interfaccia utente.
        Deve essere sovrascritto nelle sottoclassi se necessario.
        """
        self._setup_base_ui()

    def _update_status(self, color: str, message: str = ""):
        """Aggiorna la card di stato con colore e messaggio."""
        if not message:
            # Map standard colors to messages
            mapping = {
                "#0d6efd": "In esecuzione...",
                "#2E7D32": "Completato",
                "#ffc107": "In attesa",
                "#C62828": "Errore",
            }
            message = mapping.get(color, "In attesa")

        self.status_card.setStatus(message, color)
        self.status_changed.emit(color, message)

    def _connect_signals(self):
        """Connette i segnali comuni ai callback del pannello."""
        pass

    def get_bot_instance(self):
        """Restituisce un'istanza del bot. Da implementare nelle sottoclassi."""
        return None

    def get_current_status(self) -> Tuple[str, str]:
        """Restituisce lo stato attuale della card (id, messaggio)."""
        return self.status_card._status, self.status_card._status_label.text()

    def validate_ready(self) -> tuple[bool, str]:
        """
        Verifica se il bot è pronto per l'avvio (credenziali, dati, ecc.).
        Ritorna (Successo, Messaggio Errore).
        Da implementare nelle sottoclassi.
        """
        return True, ""

    def add_rows_simple(self, new_rows: list):
        """Aggiunge righe alla tabella dati esistente (se presente)."""
        if hasattr(self, "data_table"):
            current_data = self.data_table.get_data()
            current_data.extend(new_rows)
            self.data_table.set_data(current_data)
            if hasattr(self, "_save_data"):
                self._save_data()

    def clear_rows_simple(self):
        """Svuota la tabella dati."""
        if hasattr(self, "data_table"):
            self.data_table.set_data([])
            if hasattr(self, "_save_data"):
                self._save_data()

    def get_rows_count(self) -> int:
        """Ritorna il numero di righe nella tabella."""
        if hasattr(self, "data_table"):
            return len(self.data_table.get_data())
        return 0

    def _on_start(self):
        """Gestisce l'avvio del bot. Da implementare nelle sottoclassi."""
        self.start_time = datetime.now()
        self.log_widget.timeline.set_mood("running")
        self._update_status("#0d6efd")

        # Audit & Stats
        AuditManager.instance().log_action(
            action="Avvio Automazione",
            category="automazione",
            entity=self.bot_name,
            params={"bot_id": self.bot_id},
        )
        StatsManager().increment_usage(self.bot_id)

    def _on_stop(self):
        """Gestisce lo stop del bot."""
        if self.worker:
            self.worker.stop()
            self.log_widget.append("[AVVISO] Stop richiesto...")
            self._update_status("#ffc107", "Arresto richiesto...")

    def _on_worker_finished(self, success: bool):
        """Gestisce il completamento del worker."""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        duration = self._calculate_duration_str()
        self._log_mission_report(duration, success)

        # Update Status Card
        final_status = "#2E7D32" if success else "#C62828"
        self._update_status(final_status, "Completato" if success else "Errore")

        # Notify & Signals
        self._handle_worker_completion_signals(success)
        self._notify_completion(success)

        if self.worker:
            self.worker.wait()
            self.worker = None

    def _calculate_duration_str(self) -> str:
        """Helper per calcolare la durata dell'operazione."""
        if not self.start_time:
            return "N/D"
        delta = datetime.now() - self.start_time
        m, s = divmod(int(delta.total_seconds()), 60)
        return f"{m}m {s}s"

    def _log_mission_report(self, duration: str, success: bool):
        """Gestisce la UI del report e l'audit."""
        report = MissionReportCard(duration, success)
        self.log_widget.timeline.add_widget(report)

        dettagli = (
            "Esecuzione completata correttamente"
            if success
            else "Esecuzione fallita o interrotta"
        )

        AuditManager.instance().log_action(
            action="Completamento Automazione",
            category="automazione",
            entity=self.bot_name,
            params={"durata": duration, "dettagli": dettagli},
            status="success" if success else "error",
        )

    def _handle_worker_completion_signals(self, success: bool):
        """Invia segnali e gestisce risultati per Telegram."""
        if self.worker and hasattr(self.worker.bot, "downloaded_files"):
            if self.worker.bot.downloaded_files:
                self.bot_results_ready.emit(
                    self.bot_id, self.worker.bot.downloaded_files
                )
        self.bot_finished.emit(success)

    def _notify_completion(self, success: bool):
        """Gestisce le notifiche di sistema e background."""
        win = self.window()
        if win and hasattr(win, "show_background_notification"):
            msg = (
                "Operazione completata con successo."
                if success
                else "Si è verificato un errore durante l'esecuzione."
            )
            title = f"{self.bot_name} - {'Completato' if success else 'Errore'}"
            from typing import Any

            cast_win: Any = win
            cast_win.show_background_notification(title, msg, is_error=not success)
        else:
            QApplication.alert(self, 0)

    def _on_bot_finished(self, success: bool):
        """Alias per _on_worker_finished (compatibilità test)."""
        self._on_worker_finished(success)

    def _on_log(self, message: str):
        """Aggiunge un messaggio al log e lo inoltra a Telegram se importante."""
        self.log_widget.append(message)

        win = self.window()
        if win and hasattr(win, "telegram"):
            # Formattiamo il log per Telegram aggiungendo il nome del bot
            clean_msg = message.strip()
            # Rimuoviamo eventuali timestamp se presenti all'inizio (stile [HH:mm:ss])
            import re

            clean_msg = re.sub(r"^[\[]\d{2}:\d{2}:\d{2}[\]]\s*", "", clean_msg)

            tg_text = f"\U0001f539 *{self.bot_name}*\n{clean_msg}"
            from typing import Any

            cast_win: Any = win
            cast_win.telegram.send_message_sync(tg_text)

    def _on_status(self, status: str):
        """Aggiorna lo stato (messaggio custom)."""
        # Map string status to StatusCard if possible, or just update message
        # Often bots send generic strings like "Downloading..."
        # We keep the icon based on general state (RUNNING) but update text
        self.status_card._update_status_display(status)
        # We also need to emit the change for the global card
        # Using current status enum, but updating message
        self.status_changed.emit(self.status_card._status, status)

    def _ask_user_input(
        self, prompt: str, result_container: dict, event: threading.Event
    ):
        """Callback per input utente dal worker (thread-safe via signal)."""
        text, ok = QInputDialog.getText(self, "Richiesta Input", prompt)
        if ok:
            result_container["value"] = text
        else:
            result_container["value"] = ""
        event.set()

    def get_credentials(self) -> tuple:
        """Ottiene le credenziali dall'account di default."""
        account = config_manager.get_default_account()
        if account:
            return account.get("username", ""), account.get("password", "")
        return "", ""


class ScaricaTSPanel(BaseBotPanel):
    """Pannello per il bot Scarico TS."""

    def __init__(self, parent=None):
        super().__init__(
            bot_id="scarico_ts",
            bot_name="Scarico TS",
            bot_description="Tasto destro per aggiungere/rimuovere righe. Modifica i valori direttamente nelle celle.",
            parent=parent,
        )
        self._setup_content()
        # Defer data loading to speed up startup
        QTimer.singleShot(10, self._safe_load_data)

    def _safe_load_data(self):
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for ScaricaTSPanel: {e}")
            traceback.print_exc()

    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        params_group = QGroupBox("Parametri")
        params_layout = QVBoxLayout(params_group)
        params_layout.setSpacing(10)

        # Usiamo il widget atomico per i parametri comuni
        self.params_widget = BotParametersWidget(
            show_date_range=False, show_dest_path=True
        )
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        params_layout.addWidget(self.params_widget)

        # Parametri specifici: Flag Elabora TS
        self.elabora_ts_check = QCheckBox("Elabora TS")
        self.elabora_ts_check.stateChanged.connect(self._save_data)
        self.params_widget.add_widget_to_row(self.elabora_ts_check)

        params_layout.addSpacing(10)

        # Tabella
        table_toolbar = QHBoxLayout()
        table_toolbar.addStretch()
        self.clear_btn = ModernButton(
            "Pulisci Tabella",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),  # ModernButton handles coloring now
        )
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)
        params_layout.addLayout(table_toolbar)

        self.data_table = EditableDataTable([{"name": "Numero OdA", "type": "text"}])
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._save_data)
        params_layout.addWidget(self.data_table)

        self.content_layout.addWidget(params_group)

    def _open_settings(self):
        """Apre le impostazioni."""
        main_window = self.window()
        if hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def refresh_fornitori(self):
        """Ricarica i fornitori nel pannello Scarica TS."""
        self.params_widget.refresh_fornitori()

    def _load_saved_data(self):
        """Carica i dati salvati."""
        config = config_manager.load_config()
        self.refresh_fornitori()

        # Usa il widget per i parametri comuni
        self.params_widget.set_fornitore(config.get("last_ts_fornitore", ""))
        self.params_widget.set_dates(config.get("last_ts_date", "01.01.2025"))
        self.params_widget.set_dest_path(config.get("path_scarico_ts", ""))

        # Carica dati specifici
        saved_data = config.get("last_ts_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)

        self.elabora_ts_check.setChecked(config.get("elabora_ts", False))

    def _save_data(self):
        """Salva i dati correnti."""
        if not hasattr(self, "params_widget"):
            return

        date_da, _ = self.params_widget.get_dates()
        config_manager.set_config_value("last_ts_data", self.data_table.get_data())
        config_manager.set_config_value("last_ts_date", date_da)
        config_manager.set_config_value(
            "last_ts_fornitore", self.params_widget.get_fornitore()
        )
        config_manager.set_config_value(
            "path_scarico_ts", self.params_widget.get_dest_path()
        )
        config_manager.set_config_value("elabora_ts", self.elabora_ts_check.isChecked())

    def _clear_table(self):
        """Pulisce la tabella."""
        if (
            QMessageBox.question(self, "Conferma", "Svuotare la tabella?")
            == QMessageBox.StandardButton.Yes
        ):
            self.data_table.set_data([])
            self._save_data()

    def get_bot_instance(self):
        """Crea e restituisce un'istanza di ScaricaTSBot."""
        from src.bots import create_bot

        username, password = self.get_credentials()
        data_da, _ = self.params_widget.get_dates()
        config = config_manager.load_config()
        return create_bot(
            "scarico_ts",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=self.params_widget.get_dest_path(),
            data_da=data_da,
            fornitore=self.params_widget.get_fornitore(),
            elabora_ts=self.elabora_ts_check.isChecked(),
        )

    def validate_ready(self) -> tuple[bool, str]:
        """Verifica che il pannello Scarica TS sia pronto per l'esecuzione."""
        if not self.data_table.get_data():
            return False, "Nessun dato OdA inserito in tabella."
        return True, ""

    def _on_start(self):
        """Avvia il bot."""
        super()._on_start()

        username, password = self.get_credentials()
        data = self.data_table.get_data()
        fornitore = self.params_widget.get_fornitore()
        data_da, _ = self.params_widget.get_dates()

        self._save_data()

        bot = self.get_bot_instance()

        if not bot:
            self.log_widget.append("❌ Errore creazione bot (parametri mancanti?)")
            self._update_status("#C62828", "Errore avvio")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        bot_data = {
            "rows": data,
            "data_da": data_da,
            "fornitore": fornitore,
            "elabora_ts": self.elabora_ts_check.isChecked(),
        }

        # Get telegram service safely
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        self.worker = BotWorker(bot, bot_data, telegram_service=tg_service)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)
        self.worker.request_input_signal.connect(self._ask_user_input)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append(f"Avvio bot Scarico TS ({fornitore})")
        self.worker.start()
        self.bot_started.emit()


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

        self.data_table = EditableDataTable(
            [
                {"name": "Numero OdA", "type": "text"},
                {"name": "Numero Contratto", "type": "combo", "options": []},
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

    def _on_start(self):
        super()._on_start()

        username, password = self.get_credentials()
        fornitore = self.params_widget.get_fornitore()
        data_da, data_a = self.params_widget.get_dates()
        download_path = self.params_widget.get_dest_path() or str(
            Path.home() / "Downloads"
        )

        rows = self.data_table.get_data()
        self.log_widget.append(f"[DEBUG] Rows retrieved: {len(rows)}")

        if not all([username, password, fornitore]):
            ToastManager.instance().show("Verifica i parametri.", "warning")
            self._update_status("#C62828", "Parametri incompleti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

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


class PrenotaBPPanel(BaseBotPanel):
    """Pannello per il bot Prenota BP."""

    def __init__(self, parent=None):
        super().__init__(
            bot_id="prenota_bp",
            bot_name="Prenota BP",
            bot_description="Gestisce la prenotazione dei Badge Provvisori sul portale.",
            parent=parent,
        )
        self._setup_content()
        # Defer data loading
        QTimer.singleShot(10, self._safe_load_data)

    def _safe_load_data(self):
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for PrenotaBPPanel: {e}")

    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        params_group = QGroupBox("Parametri Prenotazione")
        params_layout = QVBoxLayout(params_group)
        params_layout.setSpacing(10)

        # Widget atomico per i parametri - Abilitato date range
        self.params_widget = BotParametersWidget(
            show_date_range=True, show_dest_path=False
        )
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        params_layout.addWidget(self.params_widget)

        params_layout.addSpacing(10)

        table_toolbar = QHBoxLayout()
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

        # Definiamo le nuove colonne: NUMERO BP e NOTE DI RITIRO
        columns = [
            {"name": "NUMERO BP", "type": "text"},
            {"name": "NOTE DI RITIRO", "type": "text"},
        ]
        self.data_table = EditableDataTable(columns)
        self.data_table.setMinimumHeight(200)
        self.data_table.data_changed.connect(self._save_data)
        params_layout.addWidget(self.data_table)

        self.content_layout.addWidget(params_group)

    def _open_settings(self):
        """Apre le impostazioni."""
        main_window = self.window()
        if hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def _load_saved_data(self):
        config = config_manager.load_config()
        saved_data = config.get("last_prenota_bp_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)

        # Usiamo set_dates (metodo corretto di BotParametersWidget)
        date_da = config.get("last_prenota_date_from", "01.01.2024")
        date_a = config.get("last_prenota_date_to", "31.12.2025")
        self.params_widget.set_dates(date_da, date_a)

    def _save_data(self):
        data = self.data_table.get_data()
        config_manager.set_config_value("last_prenota_bp_data", data)

        # Usiamo get_dates (metodo corretto di BotParametersWidget)
        date_da, date_a = self.params_widget.get_dates()
        config_manager.set_config_value("last_prenota_date_from", date_da)
        config_manager.set_config_value("last_prenota_date_to", date_a)

    def _clear_table(self):
        if (
            QMessageBox.question(
                self,
                "Conferma",
                "Cancellare tutti i dati dalla lista?",
                QMessageBox.StandardButton.Yes,
            )
            == QMessageBox.StandardButton.Yes
        ):
            self.data_table.set_data([])
            self._save_data()

    def _on_start(self):
        """Override: Prepara e avvia il worker specifico."""
        # Validazione form
        ready, msg = self.validate_ready()
        if not ready:
            QMessageBox.warning(self, "Attenzione", msg)
            return

        # Recupera dati e configura bot
        from src.bots.portale_fornitori.prenota_bp.bot import PrenotaBPBot

        username, password = self.get_credentials()
        config = config_manager.load_config()

        fornitore = self.params_widget.get_fornitore()
        date_da, date_a = self.params_widget.get_dates()

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
            "rows": self.data_table.get_data(),
            "fornitore": fornitore,
            "data_da": date_da,
            "data_a": date_a,
        }

        # Get telegram service safely
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        self.worker = BotWorker(bot, bot_data, telegram_service=tg_service)

        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)

        # UI Update
        self._update_status("#0d6efd", "Esecuzione...")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Avvio bot Prenota BP...")
        self.worker.start()
        self.bot_started.emit()


class CaricoTSPanel(BaseBotPanel):
    """
    Pannello per l'automazione del caricamento dei TimeSheet (Carico TS).
    Gestisce l'input dei dati e l'avvio del bot CaricoTSBot.
    """

    """Pannello per il bot Carico TS."""

    def __init__(self, parent=None):
        super().__init__(
            bot_id="carico_ts",
            bot_name="Carico TS",
            bot_description="Upload automatico dei Timesheet sul portale ISAB",
            parent=parent,
        )
        self._setup_content()
        # Defer data loading
        QTimer.singleShot(10, self._safe_load_data)

    def _safe_load_data(self):
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for CaricoTSPanel: {e}")
            traceback.print_exc()

    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        # Tabella dati
        group = QGroupBox("Parametri")
        group_layout = QVBoxLayout(group)

        # Toolbar per la tabella
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

        group_layout.addLayout(table_toolbar)

        # Tabella con tutte le colonne del database Carico TS
        self.data_table = EditableDataTable(
            [
                {"name": "Numero OdA", "type": "text"},
                {"name": "Posizione OdA", "type": "text"},
                {"name": "Codice Fiscale", "type": "text"},
                {"name": "Ingresso", "type": "text"},
                {"name": "Uscita", "type": "text"},
                {"name": "Tipo Prestazione", "type": "text"},
                {"name": "C", "type": "text"},
                {"name": "M", "type": "text"},
                {"name": "Str D", "type": "text"},
                {"name": "Str N", "type": "text"},
                {"name": "Str F D", "type": "text"},
                {"name": "Str F N", "type": "text"},
                {"name": "Sq", "type": "text"},
                {"name": "Nota D", "type": "text"},
                {"name": "Nota S", "type": "text"},
                {"name": "F S", "type": "text"},
                {"name": "G T", "type": "text"},
            ]
        )
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._save_data)
        group_layout.addWidget(self.data_table)

        self.content_layout.addWidget(group)

    def _load_saved_data(self):
        """Carica i dati salvati."""
        config = config_manager.load_config()
        saved_data = config.get("last_carico_ts_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)

    def _clear_table(self):
        """Pulisce la tabella."""
        if (
            QMessageBox.question(
                self, "Conferma", "Sei sicuro di voler cancellare tutte le righe?"
            )
            == QMessageBox.StandardButton.Yes
        ):
            self.data_table.set_data([])
            self._save_data()

    def validate_ready(self) -> tuple[bool, str]:
        """Verifica se il pannello Carico TS ha credenziali e dati validi."""
        username, password = self.get_credentials()
        if not username or not password:
            return False, "Credenziali ISAB mancanti."

        data = self.data_table.get_data()
        if not data:
            return False, "Nessuna riga di dati Timesheet inserita."

        return True, ""

    def _save_data(self):
        """Salva i dati correnti."""
        data = self.data_table.get_data()
        config_manager.set_config_value("last_carico_ts_data", data)

    def _on_start(self):
        """Avvia il bot Carico TS."""
        super()._on_start()
        username, password = self.get_credentials()

        if not username or not password:
            ToastManager.instance().show(
                "Configura le credenziali ISAB nelle Impostazioni.", "warning"
            )
            self._update_status("#C62828", "Credenziali mancanti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        data = self.data_table.get_data()
        if not data:
            ToastManager.instance().show(
                "Inserisci almeno una riga con i dati del Timesheet da caricare.",
                "warning",
            )
            self._update_status("#C62828", "Dati mancanti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        # Crea e avvia il worker
        from src.bots import create_bot

        config = config_manager.load_config()
        bot = create_bot(
            "carico_ts",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
        )

        if not bot:
            ToastManager.instance().show("Impossibile creare il bot.", "error")
            return

        # Get telegram service safely
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        self.worker = BotWorker(bot, {"rows": data}, telegram_service=tg_service)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        self.log_widget.clear()
        self.log_widget.append("Avvio bot Carico TS...")

        self.worker.start()
        self.bot_started.emit()


class ScaricoPDLPanel(BaseBotPanel):
    """
    Pannello per lo scarico massivo delle PDL da SafeWork.
    Permette di inserire una lista di numeri PDL da processare.
    """

    """Pannello per il bot Scarico PDL (SafeWork)."""

    def __init__(self, parent=None):
        super().__init__(
            bot_id="scarico_pdl",
            bot_name="Scarico PDL",
            bot_description="Scarica e stampa i Permessi di Lavoro da SafeWork.",
            parent=parent,
        )
        self._setup_content()
        # Defer data loading
        QTimer.singleShot(10, self._safe_load_data)

    def _safe_load_data(self):
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for ScaricoPDLPanel: {e}")
            traceback.print_exc()

    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        params_group = QGroupBox("Parametri")
        params_layout = QVBoxLayout(params_group)
        params_layout.setSpacing(10)

        # Riga unica per tutte le opzioni
        options_layout = QHBoxLayout()
        options_layout.setSpacing(15)

        # 1. Stampa
        self.print_check = QCheckBox("Al termine stampa con")
        self.print_check.stateChanged.connect(self._save_data)
        options_layout.addWidget(self.print_check)

        self.printer_combo = QComboBox()
        self.printer_combo.setMinimumHeight(35)
        self.printer_combo.setMinimumWidth(150)
        self.printer_combo.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self.printer_combo.setStyleSheet(
            """
            QComboBox {
                border: 1px solid black;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
                color: black;
            }
        """
        )
        # Popola stampanti
        printers = get_installed_printers()
        if printers:
            self.printer_combo.addItems(printers)
        else:
            self.printer_combo.addItem("Nessuna stampante trovata")
        self.printer_combo.currentTextChanged.connect(self._save_data)
        options_layout.addWidget(self.printer_combo)

        # 2. Merge
        self.merge_all_check = QCheckBox("e unisci tutti in un unico PDF")
        self.merge_all_check.setToolTip(
            "Se attivo, alla fine scaricherà un unico file PDF contenente tutti i PDL."
        )
        self.merge_all_check.stateChanged.connect(self._save_data)
        options_layout.addWidget(self.merge_all_check)

        # 3. Destinazione
        dest_label = QLabel("Destinazione:")
        options_layout.addWidget(dest_label)

        self.dest_path_edit = QLineEdit()
        self.dest_path_edit.setPlaceholderText("Download utente (default)")
        self.dest_path_edit.setReadOnly(True)
        self.dest_path_edit.setMinimumWidth(200)  # Ridotto per stare in riga

        # Dynamic Width logic simplified/removed as we are in HBox with stretch

        options_layout.addWidget(self.dest_path_edit)

        browse_btn = QPushButton()
        browse_btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER), "#000000"))
        browse_btn.setIconSize(QSize(20, 20))
        browse_btn.setFixedSize(35, 35)
        browse_btn.clicked.connect(self._browse_dest_path)
        browse_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f8f9fa;
                color: #212529;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding-bottom: 2px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #ced4da;
            }
        """
        )
        options_layout.addWidget(browse_btn)

        options_layout.addStretch()
        params_layout.addLayout(options_layout)

        # 3. Tabella Input
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

        self.data_table = EditableDataTable([{"name": "NUMERO PDL", "type": "text"}])
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._save_data)
        params_layout.addWidget(self.data_table)

        self.content_layout.addWidget(params_group)

    def _refresh_printers(self):
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
        path = QFileDialog.getExistingDirectory(self, "Seleziona cartella destinazione")
        if path:
            self.dest_path_edit.setText(path)
            self._save_data()

    def _load_saved_data(self):
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
        data = self.data_table.get_data()
        config_manager.set_config_value("last_pdl_data", data)
        config_manager.set_config_value(
            "pdl_print_enabled", self.print_check.isChecked()
        )
        config_manager.set_config_value(
            "pdl_merge_all_session", self.merge_all_check.isChecked()
        )
        config_manager.set_config_value(
            "pdl_printer_name", self.printer_combo.currentText()
        )
        config_manager.set_config_value("path_scarico_pdl", self.dest_path_edit.text())

    def _clear_table(self):
        if (
            QMessageBox.question(
                self,
                "Conferma",
                "Cancellare tutti i PDL?",
                QMessageBox.StandardButton.Yes,
            )
            == QMessageBox.StandardButton.Yes
        ):
            self.data_table.set_data([])
            self._save_data()

    def validate_ready(self) -> tuple[bool, str]:
        """Verifica se il pannello è pronto per l'avvio del bot."""
        username, password = self.get_credentials()
        if not username or not password:
            return False, "Credenziali SafeWork mancanti."

        data = self.data_table.get_data()
        if not data:
            return False, "Nessun PDL inserito."

        return True, ""

    def get_credentials(self) -> tuple:
        """Override: Recupera credenziali SafeWork."""
        # Prende il default da safework_accounts
        config = config_manager.load_config()
        accounts = config.get("safework_accounts", [])
        if not accounts:
            return "", ""

        # Cerca il default
        default_acc = next((a for a in accounts if a.get("default")), accounts[0])
        return default_acc.get("username", ""), default_acc.get("password", "")

    def _on_start(self):
        super()._on_start()
        username, password = self.get_credentials()

        if not self._validate_pdl_start(username, password):
            return

        bot_data = self._prepare_bot_data()
        bot = self._create_pdl_bot(username, password)
        if not bot:
            return

        # Worker initialization
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None
        self.worker = BotWorker(bot, bot_data, telegram_service=tg_service)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)

        self._finalize_start_ui()
        self.worker.start()
        self.bot_started.emit()

    def _validate_pdl_start(self, username, password) -> bool:
        """Verifica che i requisiti per l'avvio siano soddisfatti."""
        if not username or not password:
            ToastManager.instance().show(
                "Configura le credenziali SafeWork nelle Impostazioni.", "warning"
            )
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

    def _prepare_bot_data(self) -> List[dict]:
        """Prepara il payload per il bot."""
        print_enabled = self.print_check.isChecked()
        printer_name = self.printer_combo.currentText()
        merge_and_send = getattr(self, "merge_and_send_from_telegram", False)
        merge_all = getattr(
            self, "merge_all_session_from_telegram", self.merge_all_check.isChecked()
        )

        bot_data = []
        for row in self.data_table.get_data():
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
        """Crea l'istanza del bot scarico PDL."""
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
        """Aggiorna l'interfaccia all'avvio."""
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Avvio Scarico PDL SafeWork...")
        if self.print_check.isChecked():
            self.log_widget.append(
                f"Stampa attiva su: {self.printer_combo.currentText()}"
            )
        if getattr(self, "merge_and_send_from_telegram", False):
            self.log_widget.append("Unione PDF per Telegram attiva")

    def _on_worker_finished(self, success: bool):
        """Gestione custom per invio file unito e segnalazione PdL inesistenti."""
        merge_and_send = getattr(self, "merge_and_send_from_telegram", False)

        # Recupero dati prima di chiamare super (che pulisce il worker)
        missing_list: list[str] = (
            self.worker.bot.missing_pdls
            if self.worker and hasattr(self.worker.bot, "missing_pdls")
            else []
        )
        files_to_send: list[str] = (
            self.worker.bot.downloaded_files
            if self.worker and hasattr(self.worker.bot, "downloaded_files")
            else []
        )

        super()._on_worker_finished(success)

        # 1. Report Mancanti
        self._handle_missing_pdls(missing_list)

        # 2. Consegna Telegram
        if success and merge_and_send:
            self._send_pdl_to_telegram(files_to_send)

        # 3. Cleanup
        self._cleanup_telegram_flags()

    def _handle_missing_pdls(self, missing_list: list):
        """Segnala PdL non trovati sulla card di stato."""
        if missing_list:
            missing_str = ", ".join(missing_list)
            self._update_status("#2E7D32", f"Completato (Inesistenti: {missing_str})")

    def _send_pdl_to_telegram(self, files: list):
        """Invia i file PDF prodotti al bot Telegram."""
        if not files:
            return

        win = self.window()
        if win and hasattr(win, "telegram"):
            import os
            from typing import Any

            cast_win: Any = win
            self._on_log(f"Invio di {len(files)} PDF a Telegram...")
            for f in files:
                if os.path.exists(f):
                    caption = f"**PDL Scaricato**\n`{os.path.basename(f)}`"
                    cast_win.telegram.send_document_sync(f, caption)
            self._on_log("PDF inviati con successo.")

    def _cleanup_telegram_flags(self):
        """Pulisce i flag di stato temporanei."""
        for attr in ["merge_and_send_from_telegram", "merge_all_session_from_telegram"]:
            if hasattr(self, attr):
                delattr(self, attr)


class RicercaPDLPanel(BaseBotPanel):
    """
    Pannello per la ricerca ed esportazione massiva dei PDL da SafeWork.
    """

    data_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(
            bot_id="pdl_search",
            bot_name="Ricerca PDL",
            bot_description="Ricerca ed esporta i PDL da SafeWork nel database locale.",
            parent=parent,
        )
        self._setup_content()
        QTimer.singleShot(10, self._load_saved_data)

    def _setup_content(self):
        params_group = QGroupBox("Parametri di Ricerca")
        params_layout = QVBoxLayout(params_group)
        params_layout.setSpacing(15)

        # Riga unica per Flag e Sito
        top_row = QHBoxLayout()

        # 1. Flag Escludi Chiusi
        self.exclude_closed_check = QCheckBox(
            "Escludi permessi chiusi, scaduti o eliminati"
        )
        self.exclude_closed_check.setChecked(True)
        self.exclude_closed_check.stateChanged.connect(self._save_data)
        top_row.addWidget(self.exclude_closed_check)

        top_row.addSpacing(20)

        # 2. Selezione Sito
        top_row.addWidget(QLabel("Sito:"))
        self.site_combo = QComboBox()
        self.site_combo.addItems(["Seleziona tutto", "IGCC", "ISAB Nord", "ISAB Sud"])
        self.site_combo.setMinimumWidth(150)
        self.site_combo.currentTextChanged.connect(self._save_data)
        top_row.addWidget(self.site_combo)

        top_row.addStretch()
        params_layout.addLayout(top_row)

        self.content_layout.addWidget(params_group)
        self.content_layout.addStretch()

    def _load_saved_data(self):
        config = config_manager.load_config()
        self.exclude_closed_check.setChecked(
            config.get("pdl_search_exclude_closed", True)
        )
        saved_site = config.get("pdl_search_site", "Seleziona tutto")
        self.site_combo.setCurrentText(saved_site)

    def _save_data(self):
        config_manager.set_config_value(
            "pdl_search_exclude_closed", self.exclude_closed_check.isChecked()
        )
        config_manager.set_config_value(
            "pdl_search_site", self.site_combo.currentText()
        )

    def get_bot_instance(self):
        from src.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot

        username, password = self.get_credentials()
        config = config_manager.load_config()

        return SafeWorkPDLSearchBot(
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
        )

    def _on_start(self):
        """Avvia il bot Ricerca PDL."""
        super()._on_start()
        username, password = self.get_credentials()

        if not username or not password:
            ToastManager.instance().show(
                "Configura le credenziali SafeWork nelle Impostazioni.", "warning"
            )
            self._update_status("#C62828", "Credenziali mancanti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        bot = self.get_bot_instance()
        if not bot:
            return

        bot_data = {
            "exclude_closed": self.exclude_closed_check.isChecked(),
            "site_selection": self.site_combo.currentText(),
        }

        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        self.worker = BotWorker(bot, [bot_data], telegram_service=tg_service)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Avvio Ricerca PDL SafeWork...")
        self.worker.start()
        self.bot_started.emit()

    def get_credentials(self) -> tuple:
        """Override: Recupera credenziali SafeWork."""
        # Prende il default da safework_accounts
        config = config_manager.load_config()
        accounts = config.get("safework_accounts", [])
        if not accounts:
            return "", ""

        # Cerca il default
        default_acc = next((a for a in accounts if a.get("default")), accounts[0])
        return default_acc.get("username", ""), default_acc.get("password", "")

    def _on_worker_finished(self, success: bool):
        super()._on_worker_finished(success)
        if success:
            self.data_updated.emit()


class PDLDelegate(QStyledItemDelegate):
    """Delegate per gestire il wrap selettivo e l'allineamento nelle celle PDL."""

    def __init__(self, date_columns, parent=None):
        super().__init__(parent)
        self.date_columns = date_columns

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        # Abilita il wrap per tutte le colonne tranne quelle date
        if index.column() not in self.date_columns:
            option.features |= option.ViewItemFeature.HasDisplay
            option.displayAlignment = (
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )
            option.textElideMode = Qt.TextElideMode.ElideNone
        else:
            # Date: riga singola
            option.textElideMode = Qt.TextElideMode.ElideRight


class PDLDBPanel(QWidget):
    """Pannello per la visualizzazione del Database PDL SafeWork con architettura Master-Detail."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Nuove Colonne della Tabella (Vista Master)
        self.master_headers = [
            "Data Creazione",
            "Richiedente",
            "N° PDL",
            "Area",
            "Unità",
            "Stato",
            "Descrizione",
        ]

        # Mapping completo per il Dettaglio (Tutte le 21 colonne)
        self.full_headers = [
            "ID",
            "N° PDL",
            "Data Creazione",
            "Area",
            "Unità",
            "Ditta",
            "Descrizione",
            "Tipologia",
            "Stato",
            "Apparecchiatura",
            "Richiedente",
            "Data Richiesta",
            "Emittente",
            "Data Emissione",
            "Aprente",
            "Data Apertura",
            "Priorità",
            "Contratto",
            "Ordine",
            "Sito",
            "Importato il",
        ]

        self.model = FastTableModel([], self.master_headers)
        self._raw_full_data = []  # Buffer per i dati completi
        self._cache = {}  # Cache per le query

        # Stato Ordinamento
        self.current_sort_col = None
        self.current_sort_order = "DESC"

        # Timer per ricerca ritardata (Debounce)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._setup_ui()
        QTimer.singleShot(50, self.refresh_data)
        QTimer.singleShot(100, self._populate_groups)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Filtri (Top)
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca ovunque...")
        self.search_input.setMaximumWidth(250)  # Restringi barra ricerca
        self.search_input.textChanged.connect(lambda: self.search_timer.start(500))
        filter_layout.addWidget(self.search_input)

        filter_layout.addWidget(QLabel("Gruppo:"))
        self.group_filter = QComboBox()
        self.group_filter.addItem("Tutti")
        self.group_filter.currentTextChanged.connect(self.refresh_data)
        filter_layout.addWidget(self.group_filter)

        filter_layout.addWidget(QLabel("Sito:"))
        self.site_filter = QComboBox()
        self.site_filter.addItems(["Tutti i siti", "IGCC", "ISAB Nord", "ISAB Sud"])
        self.site_filter.currentTextChanged.connect(self.refresh_data)
        filter_layout.addWidget(self.site_filter)

        filter_layout.addStretch()

        refresh_btn = QPushButton("Aggiorna")
        refresh_btn.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), "#000000"))
        refresh_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(refresh_btn)
        main_layout.addLayout(filter_layout)

        # 2. Contenitore Splitter (Tabella | Dettaglio)
        from PyQt6.QtWidgets import QFormLayout, QScrollArea, QSplitter

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- TABELLA (MASTER) ---
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setItemDelegate(
            PDLDelegate([0], self.table)
        )  # Data Creazione è indice 0

        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        header = self.table.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self._on_header_clicked)

        self.splitter.addWidget(self.table)

        # --- PANNELLO DETTAGLIO (DETAIL) ---
        detail_container = QWidget()
        detail_layout = QVBoxLayout(detail_container)
        detail_layout.setContentsMargins(5, 0, 5, 0)

        detail_title = QLabel("Dettaglio Completo PDL")
        detail_title.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: #2196F3; margin-bottom: 5px;"
        )
        detail_layout.addWidget(detail_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout = QFormLayout(scroll_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.form_layout.setSpacing(10)

        self.detail_labels = {}
        for h in self.full_headers:
            val_label = QLabel("-")
            val_label.setWordWrap(True)
            val_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            self.detail_labels[h] = val_label
            self.form_layout.addRow(f"<b>{h}:</b>", val_label)

        scroll.setWidget(scroll_content)
        detail_layout.addWidget(scroll)

        self.splitter.addWidget(detail_container)
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)

        main_layout.addWidget(self.splitter)

    def _populate_groups(self):
        """Popola la dropdown dei gruppi estraendoli dal database."""
        try:
            query = "SELECT DISTINCT SUBSTR(n_pdl, INSTR(n_pdl, '/') + 1) as grp FROM pdl WHERE n_pdl LIKE '%/%' ORDER BY grp"
            rows = db_manager.execute_query(db_manager.DB_PDL, query)
            self.group_filter.blockSignals(True)
            self.group_filter.clear()
            self.group_filter.addItem("Tutti")
            for r in rows:
                if r[0]:
                    self.group_filter.addItem(str(r[0]))
            self.group_filter.blockSignals(False)
        except Exception as e:
            print(f"Errore popolamento gruppi: {e}")

    def _on_selection_changed(self, selected, _deselected):
        """Aggiorna il pannello dettaglio quando si seleziona una riga."""
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return

        row_idx = indexes[0].row()
        if row_idx < len(self._raw_full_data):
            data = self._raw_full_data[row_idx]
            for i, h in enumerate(self.full_headers):
                val = str(data[i])
                if val.lower() == "nan" or val == "None":
                    val = ""
                
                # Formattazione "Importato il"
                if h == "Importato il" and val:
                    try:
                        dt = datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
                        val = dt.strftime("%d/%m/%Y %H:%M:%S")
                    except:
                        pass
                
                self.detail_labels[h].setText(val)

    def _on_header_clicked(self, logical_index):
        """Gestisce il toggle dell'ordinamento."""
        if self.current_sort_col == logical_index:
            self.current_sort_order = "DESC" if self.current_sort_order == "ASC" else "ASC"
        else:
            self.current_sort_col = logical_index
            self.current_sort_order = "ASC"
        
        self.refresh_data(sort_col=logical_index)

    def refresh_data(self, sort_col=None):
        """Aggiorna i dati della tabella PDL con sistema di cache."""
        query, params = self._build_pdl_query(sort_col)
        cache_key = f"{query}_{params}"
        
        if cache_key in self._cache:
            full_rows = self._cache[cache_key]
        else:
            try:
                full_rows = db_manager.execute_query(db_manager.DB_PDL, query, tuple(params))
                self._cache[cache_key] = full_rows
            except Exception as e:
                print(f"Errore caricamento PDL: {e}")
                return

        self._raw_full_data = full_rows
        master_rows = self._process_pdl_rows(full_rows)
        self.model.update_data(master_rows)
        self._update_pdl_ui(len(master_rows))

    def _build_pdl_query(self, sort_col: Optional[int]) -> Tuple[str, List[Any]]:
        """Costruisce la query SQL per i PDL."""
        search_text = self.search_input.text().lower()
        site_filter = self.site_filter.currentText()
        group_filter = self.group_filter.currentText()

        query = "SELECT id, n_pdl, data_creazione, area, unita, ditta, descrizione_lavoro, tipologia, stato, apparecchiatura, richiedente, data_richiesta, emittente, data_emissione, aprente, data_apertura, priorita, contratto, ordine, sito, importato_il FROM pdl WHERE 1=1"
        params = []

        if site_filter != "Tutti i siti":
            query += " AND sito = ?"
            params.append(site_filter)
        
        if group_filter != "Tutti":
            query += " AND n_pdl LIKE ?"
            params.append(f"%/{group_filter}")

        if search_text:
            query += " AND (n_pdl LIKE ? OR area LIKE ? OR descrizione_lavoro LIKE ? OR ditta LIKE ? OR richiedente LIKE ? OR emittente LIKE ?)"
            p = f"%{search_text}%"
            params.extend([p, p, p, p, p, p])

        # Ordinamento
        order_map = {
            0: "data_creazione",
            1: "richiedente",
            2: "n_pdl",
            3: "area",
            4: "unita",
            5: "stato",
            6: "descrizione_lavoro",
        }
        
        order_clause = ""
        if sort_col is not None and sort_col in order_map:
            col_name = order_map[sort_col]
            # Ordinamento numerico speciale per N° PDL
            if col_name == "n_pdl":
                order_clause = f" ORDER BY CAST(n_pdl AS INTEGER) {self.current_sort_order}, n_pdl {self.current_sort_order}"
            else:
                order_clause = f" ORDER BY {col_name} {self.current_sort_order}"
        else:
            order_clause = " ORDER BY importato_il DESC"

        query += order_clause
        query += " LIMIT 2000"
        return query, params

    def _process_pdl_rows(self, full_rows: List[Tuple]) -> List[List[Any]]:
        """Pulisce e formatta le righe per la visualizzazione Master."""
        # Nuova mappatura Master: DATA CREAZIONE, RICHIEDENTE, N° PDL, AREA, UNITA, STATO, DESCRIZIONE
        # Indici full: 2, 10, 1, 3, 4, 8, 6
        master_rows = []
        for r in full_rows:
            row = [r[2], r[10], r[1], r[3], r[4], r[8], r[6]]
            master_rows.append(
                [("" if str(val).lower() in ["nan", "none"] else val) for val in row]
            )
        return master_rows

    def _update_pdl_ui(self, count: int):
        """Ottimizza il layout della tabella."""
        header = self.table.horizontalHeader()
        for i in range(len(self.master_headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        self.table.resizeColumnsToContents()
        # Limita larghezza colonne tranne descrizione
        for i in range(len(self.master_headers)):
            if i != 6 and header.sectionSize(i) > 200:
                header.resizeSection(i, 200)

        QTimer.singleShot(
            10, lambda: header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        )
        if count < 500:
            QTimer.singleShot(100, self.table.resizeRowsToContents)


class TimbratureBotPanel(BaseBotPanel):
    """Pannello per il bot Timbrature (Controlli e Log)."""

    data_updated = pyqtSignal()
    status_changed = pyqtSignal(str, str)  # status, message
    autopilot_changed = pyqtSignal()  # NEW: Segnale per aggiornamento UI real-time

    def __init__(self, parent=None):
        super().__init__(
            bot_id="timbrature",
            bot_name="Timbrature",
            bot_description="Scarica e gestisci le timbrature del personale",
            parent=parent,
        )
        self._is_loading = False  # Protezione caricamento
        self._setup_content()
        # Defer data loading
        QTimer.singleShot(10, self._safe_load_data)

    def _safe_load_data(self):
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for TimbratureBotPanel: {e}")
            traceback.print_exc()

    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        params_group = QGroupBox("Parametri")
        params_layout = QVBoxLayout(params_group)

        # Widget atomico
        self.params_widget = BotParametersWidget(
            show_date_range=True, show_dest_path=False
        )
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        params_layout.addWidget(self.params_widget)

        self.content_layout.addWidget(params_group)

        # Scheduler rimosso: ora la pianificazione si gestisce dall'Autopilot nella Dashboard

    def _open_settings(self):
        main_window = self.window()
        if hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def refresh_fornitori(self):
        """Ricarica i fornitori nel pannello timbrature."""
        if hasattr(self, "params_widget"):
            self.params_widget.refresh_fornitori()

    def _load_saved_data(self):
        self._is_loading = True  # Inizio blocco salvataggio
        try:
            self.refresh_fornitori()
            config = config_manager.load_config()

            self.params_widget.set_fornitore(
                config.get("last_timbrature_fornitore", "")
            )

            # Default dates: ALWAYS Yesterday
            yesterday = QDate.currentDate().addDays(-1)
            self.params_widget.set_dates(
                yesterday.toString("dd.MM.yyyy"), yesterday.toString("dd.MM.yyyy")
            )
        finally:
            self._is_loading = False  # Fine blocco salvataggio

    def _save_data(self):
        # Protezione: Se stiamo caricando, NON salvare (evita sovrascrittura con default)
        if getattr(self, "_is_loading", False):
            return

        if not hasattr(self, "params_widget"):
            return

        date_da, date_a = self.params_widget.get_dates()
        config_manager.set_config_value(
            "last_timbrature_fornitore", self.params_widget.get_fornitore()
        )
        config_manager.set_config_value("last_timbrature_date_da", date_da)
        config_manager.set_config_value("last_timbrature_date_a", date_a)

    def validate_ready(self) -> tuple[bool, str]:
        """Verifica se il pannello è pronto per l'avvio del bot."""
        username, password = self.get_credentials()
        if not username or not password:
            return False, "Credenziali ISAB mancanti."
        if not self.params_widget.get_fornitore():
            return False, "Nessun fornitore selezionato."
        return True, ""

    def _on_start(self):
        """Avvia il bot Timbrature."""
        super()._on_start()
        username, password = self.get_credentials()
        fornitore = self.params_widget.get_fornitore()

        if not all([username, password, fornitore]):
            ToastManager.instance().show("Verifica i parametri.", "warning")
            self._update_status("#C62828", "Parametri incompleti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        self._save_data()

        data_da, data_a = self.params_widget.get_dates()

        from src.bots import create_bot

        config = config_manager.load_config()
        bot = create_bot(
            "timbrature",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
            data_da=data_da,
            data_a=data_a,
            fornitore=fornitore,
        )

        if not bot:
            ToastManager.instance().show("Errore creazione bot.", "error")
            return

        bot_data = {"fornitore": fornitore, "data_da": data_da, "data_a": data_a}

        # Get telegram service safely
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        self.worker = BotWorker(bot, bot_data, telegram_service=tg_service)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished_custom)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append(f"Avvio bot Timbrature ({fornitore})")
        self.worker.start()
        self.bot_started.emit()

    def _on_worker_finished_custom(self, success: bool):
        super()._on_worker_finished(success)
        if success:
            self.data_updated.emit()


class TimbratureDBPanel(QWidget):
    """Pannello per la visualizzazione del Database Timbrature Isab ottimizzato."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_path = config_manager.CONFIG_DIR / "data" / "timbrature_Isab.db"
        self.storage = TimbratureStorage(self.db_path)

        # Load configurable lists
        self.lists = self.storage.get_lists()
        self.reparti = self.lists.get("reparti", [])
        self.cantieri = self.lists.get("cantieri", [])

        # Model initialization
        self.headers = [
            "Data",
            "Ingresso",
            "Uscita",
            "Nome",
            "Cognome",
            "Presenza TS",
            "Sito",
            "Reparto",
            "Cantiere",
        ]
        self.model = FastTableModel([], self.headers)

        self._setup_ui()
        # Pre-caricamento immediato e profondo
        QTimer.singleShot(50, self.refresh_data)

    def _setup_ui(self):
        """Configura l'interfaccia utente."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setProperty("class", "Level2Tabs")  # Clean Style

        # --- UNIFIED TOOLBAR (Corner Widget) ---
        self.toolbar_container = QWidget()
        toolbar_layout = QHBoxLayout(self.toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(lambda: self.refresh_data())

        # Reparto Filter
        self.reparto_filter = QComboBox()
        self.reparto_filter.addItem("Tutti i reparti", "Tutti")
        for rep in self.reparti:
            self.reparto_filter.addItem(rep, rep)
        self.reparto_filter.currentIndexChanged.connect(lambda: self.refresh_data())
        self.reparto_filter.setMinimumWidth(130)

        # Cantiere Filter
        self.cantiere_filter = QComboBox()
        self.cantiere_filter.addItem("Tutti i cantieri", "Tutti")
        for cant in self.cantieri:
            self.cantiere_filter.addItem(cant, cant)
        self.cantiere_filter.currentIndexChanged.connect(lambda: self.refresh_data())
        self.cantiere_filter.setMinimumWidth(130)

        # Import Button
        import_btn = QPushButton("Importa")  # Simplified
        import_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), "#FFFFFF"))
        import_btn.setFixedSize(90, 32)
        import_btn.clicked.connect(self._import_excel_manually)

        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.reparto_filter)
        toolbar_layout.addWidget(self.cantiere_filter)
        toolbar_layout.addWidget(import_btn)

        self.tabs.setCornerWidget(self.toolbar_container, Qt.Corner.TopRightCorner)

        # --- TAB 1: Database (Timbrature) ---
        self.tab_database = QWidget()
        self._setup_database_tab(self.tab_database)
        self.tabs.addTab(
            self.tab_database,
            get_colored_icon(get_asset_path(Icons.DATABASE), "#546E7A"),
            "Database",
        )

        # --- TAB 2: Impostazioni (Dipendenti) ---
        self.tab_settings = QWidget()
        self._setup_settings_tab(self.tab_settings)
        self.tabs.addTab(
            self.tab_settings,
            get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), "#546E7A"),
            "Impostazioni",
        )

        # Connect tab change
        self.tabs.currentChanged.connect(self._on_tab_changed)

        self.main_layout.addWidget(self.tabs)

    def _setup_database_tab(self, parent_widget):
        layout = QVBoxLayout(parent_widget)
        # Search layout removed (moved to corner widget)

        # Table (Model/View per massima reattività)
        self.db_table = QTableView()
        self.db_table.setModel(self.model)
        self.db_table.verticalHeader().setVisible(False)
        self.db_table.setAlternatingRowColors(True)
        self.db_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.db_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.db_table.setSortingEnabled(True)

        header = self.db_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)

        layout.addWidget(self.db_table)

    def refresh_data(self):
        """Carica i dati dal DB e aggiorna il modello virtuale."""
        text = self.search_input.text()
        reparto = self.reparto_filter.currentData()
        cantiere = self.cantiere_filter.currentData()

        # Rimuoviamo il limite di 500 per il precaricamento totale
        rows = self.storage.get_timbrature_with_reparto(
            limit=2000,
            filter_text=text,
            filter_reparto=reparto,
            filter_cantiere=cantiere,
        )

        # Formattazione dati in blocco
        formatted_rows = []
        for row in rows:
            f_row = list(row)
            try:
                date_str = str(f_row[0])
                if date_str:
                    date_part = date_str.split(" ")[0] if " " in date_str else date_str
                    dt = datetime.strptime(date_part, "%Y-%m-%d")
                    f_row[0] = dt.strftime("%d/%m/%Y")
            except Exception:
                pass
            formatted_rows.append(f_row)

        self.model.update_data(formatted_rows)
        # Ottimizza colonne dopo il caricamento
        QTimer.singleShot(0, lambda: self.db_table.resizeColumnsToContents())

    def _setup_settings_tab(self, parent_widget):
        layout = QVBoxLayout(parent_widget)

        # Header Controls
        header_layout = QHBoxLayout()

        info = QLabel("Gestione Dipendenti")
        info.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(info)

        header_layout.addStretch()

        # Open Settings Button
        open_settings_btn = ModernButton(
            "Gestisci Liste",
            variant=ModernButton.Variant.SECONDARY,
            size=ModernButton.Size.SMALL,
        )
        open_settings_btn.setToolTip("Gestisci reparti e cantieri nelle Impostazioni")
        open_settings_btn.clicked.connect(self._open_settings)
        header_layout.addWidget(open_settings_btn)

        layout.addLayout(header_layout)

        sub = QLabel(
            "Assegna Reparto e Cantiere ai dipendenti. Modifiche salvate automaticamente."
        )
        sub.setStyleSheet("color: #6c757d; margin-bottom: 5px;")
        layout.addWidget(sub)

        # Filters for Settings
        filter_layout = QHBoxLayout()
        self.filter_empty_cb = QCheckBox("Mostra solo dati mancanti (Vuoti)")

        # Load saved state
        config = config_manager.load_config()
        self.filter_empty_cb.setChecked(
            config.get("timbrature_filter_empty_only", False)
        )

        self.filter_empty_cb.stateChanged.connect(self._on_filter_empty_changed)
        filter_layout.addWidget(self.filter_empty_cb)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Table
        self.settings_table = QTableWidget()
        self.settings_table.verticalHeader().setVisible(False)
        self.settings_table.setColumnCount(4)
        self.settings_table.setHorizontalHeaderLabels(
            ["Nome", "Cognome", "Reparto", "Cantiere"]
        )

        header = self.settings_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.settings_table)

    def _on_filter_empty_changed(self, state):
        """Save preference and reload settings table."""
        config_manager.set_config_value(
            "timbrature_filter_empty_only", self.filter_empty_cb.isChecked()
        )
        self._load_settings_data()

    def _on_tab_changed(self, index):
        # Toggle toolbar visibility based on tab
        if index == 0:  # Database
            if hasattr(self, "toolbar_container"):
                self.toolbar_container.show()
            self.refresh_data()
        else:  # Settings
            if hasattr(self, "toolbar_container"):
                self.toolbar_container.hide()
            self._load_settings_data()

    def _open_settings(self):
        """Naviga verso il pannello impostazioni della finestra principale."""
        main_window = self.window()
        if hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def _manage_list(self, list_key, title):
        """Dialog generico per gestire liste di stringhe."""
        current_list = self.lists.get(list_key, [])

        d = QDialog(self)
        d.setWindowTitle(title)
        d.setMinimumWidth(300)
        layout = QVBoxLayout(d)

        list_widget = QListWidget()
        list_widget.addItems(current_list)
        layout.addWidget(list_widget)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Aggiungi")
        del_btn = QPushButton("Rimuovi")
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        layout.addLayout(btn_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(d.accept)
        layout.addWidget(button_box)

        def add_item():
            text, ok = QInputDialog.getText(d, "Aggiungi", "Nome:")
            if ok and text:
                text = text.upper()
                if text not in current_list:
                    current_list.append(text)
                    list_widget.addItem(text)
                    self.storage.save_lists(self.lists)
                    self._update_combo_boxes()

        def del_item():
            row = list_widget.currentRow()
            if row >= 0:
                item = list_widget.takeItem(row)
                val = item.text()
                if val in current_list:
                    current_list.remove(val)
                    self.storage.save_lists(self.lists)
                    self._update_combo_boxes()

        add_btn.clicked.connect(add_item)
        del_btn.clicked.connect(del_item)

        d.exec()

    def _update_combo_boxes(self):
        """Aggiorna i filtri e le combo nella tabella."""
        # Refresh local cache
        self.reparti = self.lists.get("reparti", [])
        self.cantieri = self.lists.get("cantieri", [])

        # Update Main Filters
        self.reparto_filter.blockSignals(True)
        self.reparto_filter.clear()
        self.reparto_filter.addItem("Tutti i reparti", "Tutti")
        for rep in self.reparti:
            self.reparto_filter.addItem(rep, rep)
        self.reparto_filter.blockSignals(False)

        self.cantiere_filter.blockSignals(True)
        self.cantiere_filter.clear()
        self.cantiere_filter.addItem("Tutti i cantieri", "Tutti")
        for cant in self.cantieri:
            self.cantiere_filter.addItem(cant, cant)
        self.cantiere_filter.blockSignals(False)

        # Refresh Settings Table Combos (Reload data)
        self._load_settings_data()

    def _load_settings_data(self):
        """Carica i dipendenti unici nella tabella impostazioni."""
        employees = self.storage.get_employees()
        show_empty_only = self.filter_empty_cb.isChecked()

        self.settings_table.blockSignals(True)
        self.settings_table.setRowCount(0)

        # Filter list first
        filtered_employees = []
        for emp in employees:
            if show_empty_only:
                # Se entrambi sono pieni, salta
                if emp["reparto"] and emp["cantiere"]:
                    continue
            filtered_employees.append(emp)

        for i, emp in enumerate(filtered_employees):
            self.settings_table.insertRow(i)

            # Nome
            item_nome = QTableWidgetItem(emp["nome"])
            item_nome.setFlags(item_nome.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.settings_table.setItem(i, 0, item_nome)

            # Cognome
            item_cognome = QTableWidgetItem(emp["cognome"])
            item_cognome.setFlags(item_cognome.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.settings_table.setItem(i, 1, item_cognome)

            combo_rep = QComboBox()
            combo_rep.addItems([""] + self.reparti)
            combo_rep.setCurrentText(emp["reparto"])
            combo_rep.setStyleSheet(
                "QComboBox { border: none; background: transparent; }"
            )

            combo_cant = QComboBox()
            combo_cant.addItems([""] + self.cantieri)
            combo_cant.setCurrentText(emp["cantiere"])
            combo_cant.setStyleSheet(
                "QComboBox { border: none; background: transparent; }"
            )

            # Connect signals with closures
            nome = emp["nome"]
            cognome = emp["cognome"]

            # Update Reparto
            combo_rep.currentTextChanged.connect(
                lambda text, n=nome, c=cognome: self.storage.update_employee_details(
                    n, c, reparto=text
                )
            )

            # Update Cantiere
            combo_cant.currentTextChanged.connect(
                lambda text, n=nome, c=cognome: self.storage.update_employee_details(
                    n, c, cantiere=text
                )
            )

            self.settings_table.setCellWidget(i, 2, combo_rep)
            self.settings_table.setCellWidget(i, 3, combo_cant)

        self.settings_table.blockSignals(False)

    def _import_excel_manually(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona File Excel Timbrature",
            str(Path.home() / "Downloads"),
            "Excel Files (*.xlsx *.xls)",
        )

        if not file_path:
            return

        try:

            def gui_log(msg):
                print(msg)

            success = self.storage.import_excel(file_path, gui_log)

            if success:
                AuditManager.instance().log_action(
                    "Importazione Manuale Timbrature",
                    category="database",
                    params={"file": Path(file_path).name},
                )
                self.refresh_data()
                ToastManager.instance().show(
                    "Dati importati correttamente nel database.", "success"
                )
                self._load_settings_data()
            else:
                ToastManager.instance().show("Impossibile importare il file.", "error")

        except Exception as e:
            ToastManager.instance().show(f"Errore durante l'importazione: {e}", "error")
