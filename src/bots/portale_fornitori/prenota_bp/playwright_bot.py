"""SyncroJob - Playwright Prenota BP Bot.

Versione Playwright del bot per la prenotazione automatica dei Badge Provvisori (BP).
"""

from __future__ import annotations

import traceback
from contextlib import suppress
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, ClassVar

from src.bots.base.base_bot import StepStatus
from src.bots.base.playwright_base_bot import PlaywrightBaseBot
from src.core.constants import Business

from .playwright_page import PlaywrightPrenotaBPPage

if TYPE_CHECKING:
    from src.bots.base.selenium_bot_config import SeleniumBotConfig


class PlaywrightPrenotaBPBot(PlaywrightBaseBot):
    """Bot per la prenotazione massiva di Badge Provvisori (BP) usando Playwright.

    Inizializza il bot con configurazione e parametri di filtraggio BP.
    """

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Gestione BP"),
        ("filter", "Filtraggio Buoni"),
        ("details", "Apertura Dettagli"),
        ("reserve", "Prenotazione BP"),
        ("cleanup", "Chiusura Sessione"),
    ]
    """Timeline operativa del bot."""

    @property
    def name(self) -> str:
        """Restituisce il nome visualizzato del bot."""
        return "Prenota BP (PW)"

    @property
    def description(self) -> str:
        """Restituisce la descrizione estesa."""
        return "Prenotazione Badge Provvisori sul portale ISAB (Playwright)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce lo schema delle colonne per i dati di input."""
        return [
            {"name": "numero_bp", "label": "Numero BP", "type": "text"},
            {"name": "note_ritiro", "label": "Note di Ritiro", "type": "text"},
        ]

    def __init__(
        self,
        config: SeleniumBotConfig,
        data_da: str | None = None,
        data_a: str | None = None,
        fornitore: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(config)
        current_year = datetime.now(UTC).astimezone().year

        self.data_da = data_da or f"01.01.{current_year}"
        self.data_a = data_a or f"31.12.{current_year}"
        self.fornitore = fornitore or Business.DEFAULT_SUPPLIER
        self.results: list[dict[str, Any]] = []

    def run(self, data: Any) -> bool:
        """Esecuzione principale del bot con Playwright."""
        self.update_step("login", StepStatus.COMPLETED)

        rows = self._init_run_data(data)
        if not rows:
            return True
        if not self.page:
            return False

        self.log(f"Avvio elaborazione (PW) per {len(rows)} BP (Fornitore: {self.fornitore})")
        self.update_step("nav", StepStatus.RUNNING)
        page_obj = PlaywrightPrenotaBPPage(self.page, self.log)

        try:
            page_obj.navigate_to_gestione_bp()
            self.update_step("nav", StepStatus.COMPLETED)

            processed_count = 0
            for i, row in enumerate(rows):
                self._check_stop()
                if self._process_single_bp(page_obj, i, row):
                    processed_count += 1

            self.log(f"  Elaborazione completata: {processed_count}/{len(rows)} BP prenotati.")
            self.update_step("cleanup", StepStatus.RUNNING)
            self.update_step("cleanup", StepStatus.COMPLETED)
        except Exception as e:
            self.log(f"  Errore fatale durante l'esecuzione: {e}")
            self.update_step("nav", StepStatus.ERROR)
            traceback.print_exc()
            return False
        else:
            return True
        finally:
            self.log("Fine sessione Prenota BP (PW).")

    def _init_run_data(self, data: Any) -> list[dict[str, Any]]:
        """Prepara i dati per l'esecuzione, supportando sia liste che dizionari di parametri."""
        if isinstance(data, dict):
            self.data_da = data.get("data_da") or self.data_da
            self.data_a = data.get("data_a") or self.data_a
            self.fornitore = data.get("fornitore") or self.fornitore
            return list(data.get("rows", []))
        return list(data)

    def _process_single_bp(self, page_obj: PlaywrightPrenotaBPPage, index: int, row: dict[str, Any]) -> bool:
        """Esegue il ciclo di filtraggio, apertura e prenotazione per un singolo BP."""
        num_bp = str(row.get("numero_bp", "")).strip()
        note = str(row.get("note_ritiro", "")).strip()

        if not num_bp:
            self.log(f"Riga {index + 1}: Numero BP mancante, salto.")
            return False

        try:
            self.update_step("filter", StepStatus.RUNNING)
            page_obj.filtra_buoni_prelievo(self.fornitore, num_bp, self.data_da, self.data_a)
            self.update_step("filter", StepStatus.COMPLETED)

            self.update_step("details", StepStatus.RUNNING)
            page_obj.apri_dettagli_bp()
            self.update_step("details", StepStatus.COMPLETED)

            self.update_step("reserve", StepStatus.RUNNING)
            page_obj.gestisci_creazione_richiesta(note)
            self.update_step("reserve", StepStatus.COMPLETED)

            with suppress(Exception):
                page_obj.chiudi_dettagli_bp()

            self.results.append({"NUMERO BP": num_bp, "STATO": "OK"})

            callback = getattr(self, "_progress_callback", None)
            if callback:
                callback(index, True, "")

        except Exception as e:
            self.log(f"  Errore su BP {num_bp}: {e}")
            self.update_step("reserve", StepStatus.ERROR)
            with suppress(Exception):
                page_obj.chiudi_dettagli_bp()
            self.results.append({"NUMERO BP": num_bp, "STATO": "ERRORE", "MSG": str(e)})

            callback = getattr(self, "_progress_callback", None)
            if callback:
                callback(index, False, str(e))

            return False
        else:
            return True
