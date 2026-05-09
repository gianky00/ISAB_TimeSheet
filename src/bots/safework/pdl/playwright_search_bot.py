# mypy: disable-error-code="no-any-unimported, unused-ignore"
"""
SyncroJob - Playwright SafeWork PDL Search Bot
Versione Playwright del bot per la ricerca massiva ed esportazione Excel dei PDL.
"""

import time
from contextlib import suppress
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from src.bots.base.base_bot import StepStatus
from src.bots.safework.common.locators import SafeWorkLocators
from src.bots.safework.pages.playwright_ricerca_pdl_page import PlaywrightRicercaPDLPage
from src.bots.safework.playwright_base import PlaywrightSafeworkBaseBot
from src.core.database import db_manager
from src.core.sync_tracker import SyncTracker


class PlaywrightSafeWorkPDLSearchBot(PlaywrightSafeworkBaseBot):
    """
    Bot per la ricerca massiva ed esportazione Excel dei PDL usando Playwright.
    """

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login SafeWork"),
        ("nav", "Navigazione Ricerca"),
        ("filter", "Configurazione Filtri"),
        ("search", "Ricerca e Export"),
        ("db", "Importazione Database"),
    ]

    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = 30,
        download_path: str = "",
        account_type: str = "Esecutore",
    ) -> None:
        super().__init__(username, password, headless, timeout, download_path, account_type=account_type)
        self.sites = ["IGCC", "ISAB Nord", "ISAB Sud"]
        self.ricerca_pdl_page: PlaywrightRicercaPDLPage | None = None

    @property
    def name(self) -> str:
        return "Ricerca PDL (PW)"

    @property
    def description(self) -> str:
        return "Ricerca massiva e aggiornamento database PDL (Playwright)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Nessun input tabellare richiesto per la ricerca massiva PDL."""
        return []

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esegue la pipeline di ricerca con Playwright."""
        self.update_step("login", StepStatus.COMPLETED)

        if not self.page:
            return False

        self.ricerca_pdl_page = PlaywrightRicercaPDLPage(self.page, self.log)
        params = data[0] if data else {}

        # 1. Navigazione
        self.update_step("nav", StepStatus.RUNNING)
        if not self._naviga_a_ricerca():
            self.update_step("nav", StepStatus.ERROR)
            return False
        self.update_step("nav", StepStatus.COMPLETED)

        # 2. Filtri
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
                excel_file = self._esegui_export(site)
                if excel_file:
                    self.update_step("db", StepStatus.RUNNING)
                    self._import_to_db(excel_file)
                    self.update_step("db", StepStatus.COMPLETED)
                    self._cleanup_temp_file(excel_file)

        self.update_step("search", StepStatus.COMPLETED)
        return True

    def _naviga_a_ricerca(self) -> bool:
        if not self.page:
            return False
        try:
            self.log("   Clic su Home Page...")
            self.page.click(self._get_selector(SafeWorkLocators.HOME_BUTTON))
            self._attendi_scomparsa_overlay()

            self.log("[CERCA] Clic su Ricerca PdL...")
            self.page.click(self._get_selector(SafeWorkLocators.RICERCA_PDL_BUTTON))
            self._attendi_scomparsa_overlay()
        except Exception:
            return False
        else:
            return True

    def _get_selector(self, locator: tuple[str, str]) -> str:
        _by, value = locator
        if value.startswith(("//", "(")):
            return f"xpath={value}"
        if _by == "id":
            return f"id={value}"
        return value

    def _esegui_export(self, site_name: str) -> str | None:
        self.log(f"   Esportazione Excel per {site_name}...")
        if not self.ricerca_pdl_page or not self.page:
            return None

        try:
            with self.page.expect_download(timeout=600000) as download_info:
                if self.ricerca_pdl_page.esporta_excel():
                    download = download_info.value
                    dest = Path(self.download_path) / download.suggested_filename
                    download.save_as(str(dest))
                    return str(dest)
        except Exception as e:
            self.log(f"❌ Errore export: {e}")
        return None

    def _cleanup_temp_file(self, file_path: str) -> None:
        with suppress(Exception):
            Path(file_path).unlink()
            self.log(f"    File temporaneo rimosso: {Path(file_path).name}")

    def _import_to_db(self, file_path: str) -> None:
        try:
            self.log("    Importazione in database...")
            start_time = time.time()
            df = pd.read_excel(file_path)

            mapping_ita = {
                "N  PDL": "n_pdl",
                "DATA CREAZIONE": "data_creazione",
                "AREA": "area",
                "Unità": "unita",
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
                "Priorità": "priorita",
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
