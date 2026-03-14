"""
Bot per la prenotazione automatica dei Badge Provvisori (BP) sul Portale Fornitori ISAB.
"""

import traceback
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any, ClassVar

from src.bots.base.base_bot import BaseBot, StepStatus

from .pages.prenota_bp_page import PrenotaBPPage


class PrenotaBPBot(BaseBot):
    """Bot per la prenotazione massiva di Badge Provvisori (BP) sul Portale Fornitori."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Gestione BP"),
        ("filter", "Filtraggio Buoni"),
        ("details", "Apertura Dettagli"),
        ("reserve", "Prenotazione BP"),
        ("cleanup", "Chiusura Sessione"),
    ]

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Definisce le colonne richieste per l'input dei dati (Numero BP, Note)."""
        return [
            {"name": "numero_bp", "label": "Numero BP", "type": "text"},
            {"name": "note_ritiro", "label": "Note di Ritiro", "type": "text"},
        ]

    @property
    def name(self) -> str:
        return "Prenota BP"

    @property
    def description(self) -> str:
        return "Prenotazione Badge Provvisori sul portale ISAB"

    def __init__(
        self,
        username: str = "",
        password: str = "",
        data_da: str | None = None,
        data_a: str | None = None,
        fornitore: str | None = None,
        **kwargs,
    ):
        # Pulizia kwargs come in Scarico TS
        kwargs.pop("fornitore", None)
        kwargs.pop("data_a", None)
        kwargs.pop("data_da", None)

        # Passiamo i parametri richiesti a BaseBot
        super().__init__(username=username, password=password, **kwargs)
        current_year = datetime.now(UTC).astimezone().year
        from src.core.constants import Business

        self.data_da = data_da or f"01.01.{current_year}"
        self.data_a = data_a or f"31.12.{current_year}"
        self.fornitore = fornitore or Business.DEFAULT_SUPPLIER
        self.results: list[dict[str, Any]] = []

    def _get_row_value(self, row: dict[str, Any], target_key: str) -> str:
        """Estrae un valore dalla riga in modo robusto (ignora case, spazi e underscore)."""

        def normalize(s):
            return str(s).upper().replace(" ", "").replace("_", "")

        target_norm = normalize(target_key)
        for k, v in row.items():
            if normalize(k) == target_norm:
                return str(v) if v is not None else ""
        return ""

    def run(self, data: Any):
        """Esecuzione principale del bot."""
        self.update_step("login", StepStatus.COMPLETED)

        rows = self._init_run_data(data)
        if not rows:
            return True
        if not self.driver:
            return False

        self.log(f"Avvio elaborazione per {len(rows)} BP (Fornitore: {self.fornitore})")
        self.update_step("nav", StepStatus.RUNNING)
        page = PrenotaBPPage(self.driver, self.log)

        try:
            page.navigate_to_gestione_bp()
            self.update_step("nav", StepStatus.COMPLETED)
            processed_count = 0
            for i, row in enumerate(rows):
                if self._stop_requested:
                    self.log("⚠️ Stop richiesto dall'utente.")
                    break
                if self._process_single_bp(page, i, row):
                    processed_count += 1

            self.log(f"✓ Elaborazione completata: {processed_count}/{len(rows)} BP prenotati.")
            self.update_step("cleanup", StepStatus.RUNNING)
            self.update_step("cleanup", StepStatus.COMPLETED)
            return True
        except Exception as e:
            self.log(f"❗ Errore fatale durante l'esecuzione: {e}")
            self.update_step("nav", StepStatus.ERROR)
            traceback.print_exc()
            return False
        finally:
            self.log("Fine sessione Prenota BP.")

    def _init_run_data(self, data: Any) -> list[dict[str, Any]]:
        """Inizializza i parametri della sessione."""
        if isinstance(data, dict):
            self.data_da = data.get("data_da") or self.data_da
            self.data_a = data.get("data_a") or self.data_a
            self.fornitore = data.get("fornitore") or self.fornitore
            result: list[dict[str, Any]] = data.get("rows", [])
            return result
        return list(data)

    def _process_single_bp(self, page: PrenotaBPPage, index: int, row: dict[str, Any]) -> bool:
        """Elabora un singolo buono prelievo."""
        num_bp = str(row.get("numero_bp", "")).strip()
        note = str(row.get("note_ritiro", "")).strip()

        if not num_bp:
            self.log(f"Riga {index + 1}: Numero BP mancante, salto.")
            return False

        try:
            self.update_step("filter", StepStatus.RUNNING)
            page.filtra_buoni_prelievo(self.fornitore, num_bp, self.data_da, self.data_a)
            self.update_step("filter", StepStatus.COMPLETED)

            self.update_step("details", StepStatus.RUNNING)
            page.apri_dettagli_bp()
            self.update_step("details", StepStatus.COMPLETED)

            self.update_step("reserve", StepStatus.RUNNING)
            page.gestisci_creazione_richiesta(note)
            self.update_step("reserve", StepStatus.COMPLETED)

            with suppress(Exception):
                page.chiudi_dettagli_bp()

            self.results.append({"NUMERO BP": num_bp, "STATO": "OK"})

            # Notifica progresso alla GUI (index, success, message)
            callback = getattr(self, "_progress_callback", None)
            if callback:
                callback(index, True, "")

            return True
        except Exception as e:
            self.log(f"✗ Errore su BP {num_bp}: {e}")
            self.update_step("reserve", StepStatus.ERROR)
            with suppress(Exception):
                page.chiudi_dettagli_bp()
            self.results.append({"NUMERO BP": num_bp, "STATO": "ERRORE", "MSG": str(e)})

            # Notifica progresso alla GUI (index, success, message)
            callback = getattr(self, "_progress_callback", None)
            if callback:
                callback(index, False, str(e))

            return False
