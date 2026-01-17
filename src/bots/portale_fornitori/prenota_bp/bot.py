"""
Bot per la prenotazione automatica dei Badge Provvisori (BP) sul Portale Fornitori ISAB.
"""

import traceback
from typing import Any, Dict, List

from src.bots.base.base_bot import BaseBot

from .pages.prenota_bp_page import PrenotaBPPage


class PrenotaBPBot(BaseBot):
    """Bot per la prenotazione massiva di Badge Provvisori (BP) sul Portale Fornitori."""

    @staticmethod
    def get_columns() -> list:
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
        self.results: List[Dict[str, Any]] = []

    def _get_row_value(self, row: dict, target_key: str) -> str:
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
        # Gestione dati come in Scarico TS (se passati come dict con 'rows')
        if isinstance(data, dict):
            rows = data.get("rows", [])
            self.data_da = data.get("data_da") or self.data_da
            self.data_a = data.get("data_a") or self.data_a
            self.fornitore = data.get("fornitore") or self.fornitore
        else:
            rows = data

        if not rows:
            self.log("Nessun dato da processare.")
            return True

        if not self.driver:
            return False
        assert self.driver

        self.log(f"Avvio elaborazione per {len(rows)} BP (Fornitore: {self.fornitore})")
        page = PrenotaBPPage(self.driver, self.log)

        try:
            # 1. Navigazione (Il login è già stato gestito da BaseBot.execute)
            page.navigate_to_gestione_bp()

            # 2. Ciclo Elaborazione

            processed_count = 0
            for i, row in enumerate(rows):
                if self._stop_requested:
                    self.log("⚠️ Stop richiesto dall'utente.")
                    break

                num_bp = self._get_row_value(row, "Numero BP").strip()
                note = self._get_row_value(row, "Note di Ritiro").strip()

                if not num_bp:
                    self.log(
                        f"Riga {i + 1}: Numero BP mancante o colonna errata, salto."
                    )
                    continue

                try:
                    # Filtraggio specifico per il BP corrente (Selezione Fornitore robusta)
                    page.filtra_buoni_prelievo(
                        fornitore=self.fornitore,
                        numero_bp=num_bp,
                        data_da=self.data_da,
                        data_a=self.data_a,
                    )

                    # Verifica e Creazione Richiesta da Dettagli
                    try:
                        page.apri_dettagli_bp()

                        # La nuova logica gestisce selezione e click su "Crea Richiesta"
                        page.gestisci_creazione_richiesta(note)

                        # Tentativo di chiusura dettagli se rimasti aperti (clean up)
                        try:
                            page.chiudi_dettagli_bp()
                        except Exception:
                            pass

                        self.results.append({"NUMERO BP": num_bp, "STATO": "OK"})
                        processed_count += 1

                    except Exception as e:
                        self.log(
                            f"⚠️ Errore durante processamento dettagli per {num_bp}: {e}"
                        )
                        try:
                            page.chiudi_dettagli_bp()
                        except Exception:
                            pass
                        self.results.append(
                            {
                                "NUMERO BP": num_bp,
                                "STATO": "ERROR_PROC",
                                "MSG": f"Err: {e}",
                            }
                        )
                        continue

                    # page.prenota_nuovo_bp(num_bp, note) # RIMOSSO: Sostituito da flow Dettagli
                except Exception as e:
                    self.log(f"✗ Errore su BP {num_bp}: {str(e)}")
                    self.results.append(
                        {"NUMERO BP": num_bp, "STATO": "ERRORE", "MSG": str(e)}
                    )

            self.log(
                f"✓ Elaborazione completata: {processed_count}/{len(rows)} BP prenotati."
            )
            return True

        except Exception as e:
            self.log(f"❗ Errore fatale durante l'esecuzione: {str(e)}")
            traceback.print_exc()
            return False
        finally:
            self.log("Fine sessione Prenota BP.")
