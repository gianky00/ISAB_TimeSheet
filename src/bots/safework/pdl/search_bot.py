"""
SyncroJob - SafeWork PDL Search Bot
Bot modulare per la ricerca massiva ed esportazione Excel dei PDL.
"""

import logging
import time
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from src.bots.base.base_bot import StepStatus
from src.bots.safework.base import SafeworkBaseBot
from src.bots.safework.common.locators import SafeWorkLocators
from src.core.database import db_manager
from src.core.sync_tracker import SyncTracker

logger = logging.getLogger(__name__)


class SafeWorkPDLSearchBot(SafeworkBaseBot):
    """Bot per la ricerca massiva ed esportazione Excel dei PDL da SafeWork."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login SafeWork"),
        ("nav", "Navigazione Ricerca"),
        ("filter", "Configurazione Filtri"),
        ("search", "Ricerca e Export"),
        ("db", "Importazione Database")
    ]

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        self.sites = ["IGCC", "ISAB Nord", "ISAB Sud"]

    @staticmethod
    def get_name() -> str:
        return "Ricerca PDL"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return []

    @property
    def name(self) -> str:
        return "ricerca_pdl"

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esegue la ricerca e l'esportazione dei PDL delegando alle Page Objects."""
        self.update_step("login", StepStatus.COMPLETED)

        if not self.driver or not self.wait:
            return False

        params = data[0] if data else {}

        # 1. Navigazione a Ricerca
        self.update_step("nav", StepStatus.RUNNING)
        if not self._naviga_a_ricerca():
            self.update_step("nav", StepStatus.ERROR)
            return False
        self.update_step("nav", StepStatus.COMPLETED)

        # 2. Configurazione Filtri
        if not self.ricerca_pdl_page:
            self.log("❌ Pagina Ricerca PDL non inizializzata.")
            return False

        self.update_step("filter", StepStatus.RUNNING)
        self.ricerca_pdl_page.configura_filtro_chiusi(params.get("exclude_closed", True))
        self.update_step("filter", StepStatus.COMPLETED)

        # 3. Elaborazione per ogni Sito
        self.update_step("search", StepStatus.RUNNING)
        site_selection = params.get("site_selection", "Seleziona tutto")
        sites = self.sites if site_selection == "Seleziona tutto" else [site_selection]

        for site in sites:
            self._check_stop()
            if self.ricerca_pdl_page.seleziona_sito_e_cerca(site):
                self._attendi_scomparsa_overlay(timeout_secondi=300)
                excel_file = self._esegui_export(site)
                if excel_file:
                    self.update_step("db", StepStatus.RUNNING)
                    self._import_to_db(excel_file)
                    self.update_step("db", StepStatus.COMPLETED)
                    self._cleanup_temp_file(excel_file)

        self.update_step("search", StepStatus.COMPLETED)
        return True

    def _naviga_a_ricerca(self) -> bool:
        if not self.wait:
            self.log("❌ Wait non inizializzato.")
            return False

        try:
            self.log("🏠 Clic su Home Page...")
            self.wait.until(lambda d: d.find_element(*SafeWorkLocators.HOME_BUTTON)).click()
            self._attendi_scomparsa_overlay()

            self.log("🔍 Clic su Ricerca PdL...")
            self.wait.until(lambda d: d.find_element(*SafeWorkLocators.RICERCA_PDL_BUTTON)).click()
            self._attendi_scomparsa_overlay()
            return True
        except Exception:
            return False

    def _esegui_export(self, site_name: str) -> str | None:
        from src.bots.base.wait_helpers import poll_for_new_file

        files_before = {str(f.resolve()) for f in Path(self.download_path).glob("*") if f.is_file()}

        self.log(f"📥 Esportazione Excel per {site_name}...")

        if not self.ricerca_pdl_page:
            self.log("❌ Pagina Ricerca PDL non inizializzata per export.")
            return None

        if self.ricerca_pdl_page.esporta_excel():
            return poll_for_new_file(
                directory=self.download_path, files_before=files_before, pattern="Ricerca*.xlsx", timeout=600
            )
        return None

    def _cleanup_temp_file(self, file_path: str) -> None:
        try:
            Path(file_path).unlink()
            self.log(f"🗑️ File temporaneo rimosso: {Path(file_path).name}")
        except Exception:
            logger.debug(f"Impossibile rimuovere il file temporaneo: {file_path}")

    def _import_to_db(self, file_path: str):
        """Importazione massiva in SQLite con mapping normalizzato."""
        try:
            self.log("🗄️ Importazione in database...")
            start_time = time.time()
            df = pd.read_excel(file_path)

            # Nota: Ho usato nomi inglesi per le colonne per coerenza interna se necessario,
            # ma dovrei verificare src/core/database/migrations/pdl.py
            # Per ora manteniamo il mapping originale visto in precedenza
            mapping_ita = {
                "N° PDL": "n_pdl",
                "DATA CREAZIONE": "data_creazione",
                "AREA": "area",
                "UNITÀ": "unita",
                "DITTA": "ditta",
                "DESCRIZIONE DEL LAVORO": "descrizione_lavoro",
                "TIPOLOGIA": "tipologia",
                "STATO": "stato",
                "APPARECCHIATURA": "apparecchiatura",
                "RICHIEDENTE": "richiedente",
                "DATA RICHIESTA": "data_richiesta",
                "EMITTENTE": "emittente",
                "DATA EMISSIONE": "data_emissione",
                "APRENTE": "aprente",
                "DATA APERTURA": "data_apertura",
                "PRIORITÀ": "priorita",
                "CONTRATTO": "contratto",
                "ORDINE": "ordine",
                "SITO": "sito",
            }
            df.rename(columns=mapping_ita, inplace=True)
            for col in mapping_ita.values():
                if col not in df.columns:
                    df[col] = ""
            df.fillna("", inplace=True)

            columns = list(mapping_ita.values())
            data_to_insert = [tuple(row) for row in df[columns].values]
            placeholders = ", ".join(["?"] * len(columns))
            query = f"INSERT OR REPLACE INTO pdl ({', '.join(columns)}) VALUES ({placeholders})"

            with db_manager.get_connection(db_manager.DB_PDL) as conn:
                conn.executemany(query, data_to_insert)

            SyncTracker.update_status("pdl", len(data_to_insert), 0, time.time() - start_time)
            self.log(f"✅ Importazione completata: {len(data_to_insert)} record processati.")
        except Exception as e:
            self.log(f"❌ Errore importazione: {e}")
