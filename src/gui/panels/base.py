"""
SyncroJob - Base Panel Components
Classi base e worker per i pannelli dei bot.
"""

import threading
import traceback
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QInputDialog,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.core.stats_manager import StatsManager
from src.gui.design.spacing import Spacing
from src.gui.widgets import MissionReportCard, TimelineWidget
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.status_card import StatusCard
from src.utils.helpers import get_asset_path


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
    bot_results_ready = pyqtSignal(str, list)  # bot_id, list of results (e.g. file paths)
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

        self.worker: Optional[BotWorker] = None
        self.start_time: Optional[datetime] = None
        self._setup_ui()
        self._connect_signals()

    def _setup_base_ui(self):
        """Inizializza l'interfaccia utente di base comune a tutti i pannelli bot."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(Spacing.md, Spacing.md, Spacing.md, Spacing.md)
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
        self.log_widget = TimelineWidget()
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

    def run_externally(self, params: Optional[Dict[str, Any]] = None):
        """
        Avvia il bot programmaticamente con parametri opzionali che sovrascrivono quelli UI.

        Args:
            params: Dizionario di parametri da sovrascrivere (es. {'data_da': '01.01.2025'}).
        """
        self._on_start(params_override=params)

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

    def _on_start(self, params_override: Optional[Dict[str, Any]] = None):
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

        dettagli = "Esecuzione completata correttamente" if success else "Esecuzione fallita o interrotta"

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
                self.bot_results_ready.emit(self.bot_id, self.worker.bot.downloaded_files)
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

            clean_msg = re.sub(r"^[\\[\\]\d{2}:\d{2}:\d{2}[\\]]s*", "", clean_msg)

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

    def _ask_user_input(self, prompt: str, result_container: dict, event: threading.Event):
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
