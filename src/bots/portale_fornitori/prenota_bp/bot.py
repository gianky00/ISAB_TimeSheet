"""
Bot per la prenotazione automatica dei Badge Provvisori (BP) sul Portale Fornitori ISAB.
"""

import traceback
from contextlib import suppress
from typing import Any

from src.bots.base.base_bot import BaseBot

from .pages.prenota_bp_page import PrenotaBPPage


class PrenotaBPBot(BaseBot):
    """Bot per la prenotazione massiva di Badge Provvisori (BP) sul Portale Fornitori."""

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Definisce le colonne richieste per l'input dei dati (Numero BP, Note)."""
        return [
            {"name": "Numero BP", "type": "text"},
            {"name": "Note di Ritiro", "type": "text"},
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
        data_da: str = "01.01.2024",
        data_a: str = "31.12.2025",
        fornitore: str = "KK10608 - COEMI S.R.L.",
        **kwargs,
    ):
        # Pulizia kwargs come in Scarico TS
        kwargs.pop("fornitore", None)
        kwargs.pop("data_a", None)
        kwargs.pop("data_da", None)

        # Passiamo i parametri richiesti a BaseBot
        super().__init__(username=username, password=password, **kwargs)
        self.data_da = data_da
        self.data_a = data_a
        self.fornitore = fornitore
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
        rows = self._init_run_data(data)
        if not rows:
            return True
        if not self.driver:
            return False

        self.log(f"Avvio elaborazione per {len(rows)} BP (Fornitore: {self.fornitore})")
        page = PrenotaBPPage(self.driver, self.log)

        try:
            page.navigate_to_gestione_bp()
            processed_count = 0
            for i, row in enumerate(rows):
                if self._stop_requested:
                    self.log("⚠️ Stop richiesto dall'utente.")
                    break
                if self._process_single_bp(page, i, row):
                    processed_count += 1

            self.log(f"✓ Elaborazione completata: {processed_count}/{len(rows)} BP prenotati.")
            return True
        except Exception as e:
            self.log(f"❗ Errore fatale durante l'esecuzione: {e}")
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
        num_bp = self._get_row_value(row, "Numero BP").strip()
        note = self._get_row_value(row, "Note di Ritiro").strip()

        if not num_bp:
            self.log(f"Riga {index + 1}: Numero BP mancante, salto.")
            return False

        try:
            page.filtra_buoni_prelievo(self.fornitore, num_bp, self.data_da, self.data_a)
            page.apri_dettagli_bp()
            page.gestisci_creazione_richiesta(note)
            with suppress(Exception):
                page.chiudi_dettagli_bp()

            self.results.append({"NUMERO BP": num_bp, "STATO": "OK"})
            return True
        except Exception as e:
            self.log(f"✗ Errore su BP {num_bp}: {e}")
            with suppress(Exception):
                page.chiudi_dettagli_bp()
            self.results.append({"NUMERO BP": num_bp, "STATO": "ERRORE", "MSG": str(e)})
            return False
