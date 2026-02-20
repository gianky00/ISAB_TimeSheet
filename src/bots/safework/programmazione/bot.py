"""
SyncroJob - SafeWork Programmazione Bot
Bot modulare per il monitoraggio della programmazione settimanale tramite Export Excel (Ricerca Massiva).
"""

import contextlib
import logging
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from src.bots.base.base_bot import StepStatus
from src.bots.base.wait_helpers import poll_for_new_file
from src.bots.safework.base import SafeworkBaseBot
from src.bots.safework.common.locators import SafeWorkLocators

logger = logging.getLogger(__name__)


class SafeWorkProgrammazioneBot(SafeworkBaseBot):
    """Bot per monitorare i flag TCL/TGO della settimana tramite Export Excel."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login SafeWork"),
        ("nav", "Navigazione Attività"),
        ("filter", "Configurazione Filtri"),
        ("search", "Ricerca ed Export"),
        ("parse", "Analisi Risultati")
    ]

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        self.results: list[dict[str, Any]] = []

    @staticmethod
    def get_name() -> str:
        return "Programmazione PDL"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return []

    @property
    def name(self) -> str:
        return "programmazione_pdl"

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esecuzione tramite export Excel massivo."""
        self.update_step("login", StepStatus.COMPLETED)

        params = data[0] if data else {}
        requesters = params.get("requesters", [])
        date_start = params.get("date_start")
        date_end = params.get("date_end")

        if not requesters or not date_start or not date_end:
            return False

        # 1. Navigazione
        self.update_step("nav", StepStatus.RUNNING)
        self.log("📋 Navigazione in 'Visualizza Attività'...")
        if not self.driver:
            self.log("❌ Driver non inizializzato.")
            self.update_step("nav", StepStatus.ERROR)
            return False

        self.click_robusto(SafeWorkLocators.HOME_BUTTON)
        self._attendi_scomparsa_overlay()

        self.click_robusto(SafeWorkLocators.VISUALIZZA_ATTIVITA_BUTTON)
        self._attendi_scomparsa_overlay()
        self.update_step("nav", StepStatus.COMPLETED)

        # 2. Setup Filtri Generali
        self.update_step("filter", StepStatus.RUNNING)
        if not self.attivita_page:
            self.log("❌ Pagina Attività non inizializzata.")
            self.update_step("filter", StepStatus.ERROR)
            return False

        self.attivita_page.pulisci_pdl()
        self.attivita_page.imposta_date(str(date_start), str(date_end))
        self.attivita_page.seleziona_ditta("CO.EMI SRL")
        self.update_step("filter", StepStatus.COMPLETED)

        # 3. Selezione Massiva Richiedenti
        self.log(f"👥 Selezione di {len(requesters)} richiedenti...")
        if not self.attivita_page.seleziona_richiedente(requesters):
            self.log("⚠️ Problemi nella selezione dei richiedenti.")
            # Proseguiamo comunque, magari ne ha selezionati alcuni

        # 4. Ricerca ed Export Unico
        self.update_step("search", StepStatus.RUNNING)
        self.log("🔍 Avvio ricerca massiva...")
        self.attivita_page.esegui_ricerca()
        self._attendi_scomparsa_overlay()

        excel_file = self._scarica_excel()
        if excel_file:
            self.update_step("search", StepStatus.COMPLETED)
            self.update_step("parse", StepStatus.RUNNING)
            self.results = []
            self._parse_excel_results(excel_file)
            self.update_step("parse", StepStatus.COMPLETED)
            self._cleanup_temp_file(excel_file)
        else:
            self.log("❌ Impossibile scaricare il file Excel dei risultati.")
            self.update_step("search", StepStatus.ERROR)
            return False

        self.log(f"✨ FINE: Trovati {len(self.results)} PDL con programmazione.")
        return True

    def _scarica_excel(self) -> str | None:
        """Esegue il download dell'Excel e attende il completamento."""
        files_before = {str(f.resolve()) for f in Path(self.download_path).glob("*") if f.is_file()}

        self.log("📥 Esportazione Excel massiva...")
        if self.attivita_page and self.attivita_page.esporta_excel():
            return poll_for_new_file(
                directory=self.download_path, files_before=files_before, pattern="*.xlsx", timeout=300
            )
        return None

    def _parse_excel_results(self, file_path: str):
        """Legge i dati dall'Excel scaricato per tutti i richiedenti."""
        try:
            self.log("📄 Analisi risultati Excel...")
            df = pd.read_excel(file_path, header=0)

            count_pdl = 0
            for _, row in df.iterrows():
                # Estrazione flag C-P (indici 2-15)
                prog_settimanale = []
                has_prog = False

                for i in range(7):
                    idx_tcl = 2 + (i * 2)
                    idx_tgo = 3 + (i * 2)

                    if idx_tgo >= len(row):
                        break

                    tcl = str(row.iloc[idx_tcl]).strip().lower() == "si"
                    tgo = str(row.iloc[idx_tgo]).strip().lower() == "si"

                    if tcl or tgo:
                        has_prog = True

                    prog_settimanale.append({"giorno": i + 1, "tcl": tcl, "tgo": tgo})

                if has_prog:
                    # Mapping Colonne Ricevuto:
                    # A (0) = N° PDL
                    # B (1) = Descrizione
                    # R (17) = Richiedente
                    # X (23) = Unità
                    # Y (24) = Area
                    pdl = str(row.iloc[0]).strip() if len(row) > 0 else "N/D"
                    desc = str(row.iloc[1]).strip() if len(row) > 1 else ""
                    richiedente = str(row.iloc[17]).strip() if len(row) > 17 else "N/D"
                    unita = str(row.iloc[23]).strip() if len(row) > 23 else ""
                    area = str(row.iloc[24]).strip() if len(row) > 24 else ""

                    self.results.append(
                        {
                            "pdl": pdl,
                            "unita": unita,
                            "area": area,
                            "descrizione": desc,
                            "richiedente": richiedente,
                            "programmazione": prog_settimanale,
                        }
                    )
                    count_pdl += 1

            self.log(f"✅ Trovati {count_pdl} record programmati nel file Excel.")

        except Exception as e:
            self.log(f"⚠️ Errore parsing Excel: {e}")

    def _cleanup_temp_file(self, file_path: str) -> None:
        with contextlib.suppress(Exception):
            Path(file_path).unlink()
            self.log("🗑️ File temporaneo rimosso.")
