"""SyncroJob - Telegram Bridge Data Processor.

Valida e inserisce dati (PDL, ODA, BP) provenienti da Telegram nelle tabelle UI.
"""

import logging
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QObject

from src.utils.validators import InputValidator

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow

logger = logging.getLogger(__name__)


class TelegramDataProcessor(QObject):
    """Gestisce la validazione e l'inserimento dei dati nelle tabelle della UI.

    Inizializza la classe.
    """

    def __init__(self, main_window: "MainWindow", telegram_service: Any) -> None:
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service

    def process_pdl_items(self, items: list[str]) -> None:
        """Valida e aggiunge PDL alla tabella."""
        panel = getattr(self.mw, "pdl_panel", None)
        if not panel:
            return

        valid_items, duplicates, errors = self._validate_and_filter_items(
            items, "numero_pdl", InputValidator.validate_pdl, panel
        )
        if valid_items:
            panel.add_rows_simple([{"numero_pdl": v} for v in valid_items])
            self.mw.navigation_controller.navigate_to_panel("scarico_pdl")
        self._send_data_feedback(len(valid_items), duplicates, errors)

    def process_oda_items(self, items: list[str]) -> None:
        """Valida e aggiunge ODA alla tabella."""
        panel = getattr(self.mw, "scarico_panel", None)
        if not panel:
            return

        valid_items, duplicates, errors = self._validate_and_filter_items(
            items, "numero_oda", InputValidator.validate_oda, panel
        )
        if valid_items:
            panel.add_rows_simple([{"numero_oda": v} for v in valid_items])
            self.mw.navigation_controller.navigate_to_panel("scarico_ts")
        self._send_data_feedback(len(valid_items), duplicates, errors)

    def process_bp_items(self, items: list[str]) -> None:
        """Valida e aggiunge BP alla tabella."""
        self.mw.navigation_controller.navigate_to_panel("prenota_bp")
        panel = self.mw.bot_controller._get_active_bot_panel()
        if not panel or getattr(panel, "bot_id", "") != "prenota_bp":
            return

        valid_items: list[dict[str, Any]] = []
        duplicates = 0

        for item in items:
            item = item.strip()  # noqa: PLW2901
            if not item:
                continue
            parts = item.split(" ", 1)
            bp_num = parts[0].strip()
            bp_note = parts[1].strip() if len(parts) > 1 else ""

            if any(v.get("NUMERO BP") == bp_num for v in valid_items):
                duplicates += 1
            else:
                valid_items.append({"NUMERO BP": bp_num, "NOTE DI RITIRO": bp_note})

        if valid_items:
            if hasattr(panel, "data_table"):
                panel.data_table.set_data(valid_items)
            if hasattr(panel, "_save_data"):
                panel._save_data()
            self.mw.show_toast(f"Telegram: Impostati {len(valid_items)} BP")

        self._send_data_feedback(len(valid_items), duplicates, [])

    def _validate_and_filter_items(
        self, items: list[str], field: str, validator_func: Any, panel: Any
    ) -> tuple[list[str], int, list[str]]:
        """Valida e filtra i dati in ingresso rispetto a quelli esistenti nel pannello."""
        valid_items, duplicates, errors = [], 0, []

        existing = []
        if hasattr(panel, "data_table"):
            existing = [str(row.get(field, "")) for row in panel.data_table.get_data()]

        for item in items:
            res = validator_func(item)
            if res.valid:
                val = res.sanitized_value
                if val in existing or val in valid_items:
                    duplicates += 1
                else:
                    valid_items.append(val)
            else:
                errors.append(f"❌ `{item}`: {res.error}")
        return valid_items, duplicates, errors

    def _send_data_feedback(self, count_valid: int, duplicates: int, errors: list[str]) -> None:
        """Invia il feedback dell'operazione al bot Telegram."""
        feedback = []
        if count_valid:
            feedback.append(f"✅ Aggiunti/Impostati {count_valid}")
        if duplicates:
            feedback.append(f"ℹ️ {duplicates} duplicati ignorati")
        if errors:
            feedback.append("⚠️ Errori:\n" + "\n".join(errors[:5]))

        msg = "\n".join(feedback) if feedback else "⚠️ Nessun dato valido."
        self.telegram.send_message_sync(msg)
