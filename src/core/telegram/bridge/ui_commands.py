"""
SyncroJob - Telegram Bridge UI Commands
Gestisce l'attivazione dei bot e la navigazione UI richiesta da Telegram.
"""

import logging
from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QDate, QObject

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow

logger = logging.getLogger(__name__)


class TelegramUICommands(QObject):
    """Esegue comandi di navigazione e avvio bot desktop."""

    def __init__(self, main_window: "MainWindow", telegram_service: Any) -> None:  # noqa: ANN401
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service

    def run_pdl_bot(self, params: dict[str, Any]) -> None:
        """Avvia il bot Scarico PDL con i parametri specificati."""
        self.mw.navigation_controller.navigate_to_panel("scarico_pdl")
        panel = getattr(self.mw, "pdl_panel", None)
        if not panel:
            return

        print_enabled = params.get("print", False)
        panel.print_check.setChecked(print_enabled)
        panel.merge_and_send_from_telegram = params.get("merge_and_send", False)
        panel.merge_all_session_from_telegram = params.get("merge_all", False)

        if hasattr(panel, "validate_ready"):
            ready, msg = panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Scarico PDL.\nMotivo: {msg}")
                return

        if hasattr(panel, "start_btn"):
            panel.start_btn.click()
            self.telegram.send_message_sync(f"✅ Avvio Scarico PDL (Stampa={print_enabled})")

    def list_pdl(self) -> None:
        """Invia a Telegram la lista dei PDL attualmente in tabella."""
        panel = getattr(self.mw, "pdl_panel", None)
        if not panel:
            return
        data = panel.data_table.get_data()
        items = [str(row.get(next(iter(row)))) for row in data if row][:20]
        text = "📋 **Lista PDL Corrente:**\n" + "\n".join([f"• `{i}`" for i in items])
        self.telegram.send_message_sync(text)

    def clear_pdl(self) -> None:
        """Svuota la tabella PDL."""
        panel = getattr(self.mw, "pdl_panel", None)
        if panel:
            panel.clear_rows_simple()
            self.telegram.send_message_sync("🗑️ Tabella PDL svuotata.")

    def run_ts_bot(self) -> None:
        """Avvia il bot Scarico TS."""
        self.mw.navigation_controller.navigate_to_panel("scarico_ts")
        panel = getattr(self.mw, "scarico_panel", None)
        if not panel:
            return
        ready, msg = panel.validate_ready()
        if not ready:
            self.telegram.send_message_sync(f"⚠️ Impossibile avviare Scarico TS.\nMotivo: {msg}")
            return
        panel.start_btn.click()
        self.telegram.send_message_sync("✅ Avvio Scarico Timesheet.")

    def run_carico_bot(self) -> None:
        """Avvia il bot Carico TS."""
        self.mw.navigation_controller.navigate_to_panel("carico_ts")
        panel = getattr(self.mw, "carico_panel", None)
        if not panel:
            return
        ready, msg = panel.validate_ready()
        if not ready:
            self.telegram.send_message_sync(f"⚠️ Impossibile avviare Carico TS.\nMotivo: {msg}")
            return
        panel.start_btn.click()
        self.telegram.send_message_sync("✅ Avvio Carico Timesheet.")

    def run_prenota_bp_bot(self) -> None:
        """Avvia il bot Prenotazione BP."""
        self.mw.navigation_controller.navigate_to_panel("prenota_bp")
        panel = self.mw.bot_controller._get_active_bot_panel()

        if not panel or getattr(panel, "bot_id", "") != "prenota_bp":
            self.telegram.send_message_sync("⚠️ Errore interno: Pannello Prenota BP non trovato.")
            return

        if hasattr(panel, "validate_ready"):
            ready, msg = panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Prenota BP.\nMotivo: {msg}")
                return

        if hasattr(panel, "start_btn"):
            panel.start_btn.click()
            self.telegram.send_message_sync("✅ Avvio Prenotazione BP.")

    def run_timbrature_bot(self, params: dict[str, Any]) -> None:
        """Avvia il bot Timbrature."""
        period = params.get("period", "today")
        self.mw.navigation_controller.navigate_to_panel("timbrature")
        panel = getattr(self.mw, "timbrature_bot_panel", None)
        if not panel:
            return

        today = QDate.currentDate()
        if period == "yesterday":
            target = today.addDays(-1)
            panel.date_da_edit.setDate(target)
            panel.date_a_edit.setDate(target)
        elif period == "today":
            panel.date_da_edit.setDate(today)
            panel.date_a_edit.setDate(today)

        if hasattr(panel, "validate_ready"):
            ready, msg = panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Timbrature.\nMotivo: {msg}")
                return

        if hasattr(panel, "start_btn"):
            panel.start_btn.click()
            period_str = "oggi" if period == "today" else "ieri"
            self.telegram.send_message_sync(f"✅ Avvio Scarico Timbrature ({period_str}).")

    def stop_all_bots(self) -> None:
        """Invia il segnale di stop al bot correntemente attivo."""
        panel = self.mw.bot_controller._get_active_bot_panel()
        if panel and hasattr(panel, "stop_btn") and panel.stop_btn.isEnabled():
            panel.stop_btn.click()
            self.telegram.send_message_sync("🛑 Stop inviato.")
        else:
            self.telegram.send_message_sync("ℹ️ Nessun processo attivo.")
