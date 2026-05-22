"""SyncroJob - Playwright SafeWork Programmazione Bot.

Versione Playwright del bot per il monitoraggio della programmazione settimanale.
"""

from __future__ import annotations

from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Final

import pandas as pd

from src.bots.base.base_bot import StepStatus
from src.bots.safework.common.locators import SafeWorkLocators
from src.bots.safework.pages.playwright_visualizza_attivita_page import PlaywrightVisualizzaAttivitaPage
from src.bots.safework.playwright_base import PlaywrightSafeworkBaseBot

if TYPE_CHECKING:
    from src.bots.base.selenium_bot_config import SeleniumBotConfig

# Costanti per parsing Excel
IDX_RICHIEDENTE: Final[int] = 17
IDX_UNITA: Final[int] = 23
IDX_AREA: Final[int] = 24


class PlaywrightSafeWorkProgrammazioneBot(PlaywrightSafeworkBaseBot):
    """Bot per monitorare i flag TCL/TGO della settimana usando Playwright."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login SafeWork"),
        ("nav", "Navigazione Attività"),
        ("filter", "Configurazione Filtri"),
        ("search", "Ricerca ed Export"),
        ("parse", "Analisi Risultati"),
    ]

    def __init__(
        self,
        config: SeleniumBotConfig,
        account_type: str = "Esecutore",
    ) -> None:
        super().__init__(config, account_type=account_type)
        self.results: list[dict[str, Any]] = []
        self.attivita_page: PlaywrightVisualizzaAttivitaPage | None = None

    @property
    def name(self) -> str:
        return "Programmazione PDL (PW)"

    @property
    def description(self) -> str:
        return "Monitoraggio programmazione settimanale SafeWork (Playwright)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Nessuna tabella input: i filtri arrivano dai parametri del pannello."""
        return []

    def run(self, data: list[dict[str, Any]] | dict[str, Any]) -> bool:
        """Esegue il monitoraggio settimanale e aggiorna i risultati aggregati."""
        self.update_step("login", StepStatus.COMPLETED)

        params = data[0] if isinstance(data, list) and data else data if isinstance(data, dict) else {}
        requesters = params.get("requesters", [])
        date_start = params.get("date_start")
        date_end = params.get("date_end")

        if not requesters or not date_start or not date_end:
            return False

        if not self.page:
            return False

        self.attivita_page = PlaywrightVisualizzaAttivitaPage(self.page, self.log)

        # 1. Navigazione
        self.update_step("nav", StepStatus.RUNNING)
        self.log("   Navigazione in 'Visualizza Attività'...")

        self.page.click(self._get_selector(SafeWorkLocators.HOME_BUTTON))
        self._attendi_scomparsa_overlay()

        self.page.click(self._get_selector(SafeWorkLocators.VISUALIZZA_ATTIVITA_BUTTON))
        self._attendi_scomparsa_overlay()
        self.update_step("nav", StepStatus.COMPLETED)

        # 2. Filtri
        self.update_step("filter", StepStatus.RUNNING)
        self.attivita_page.pulisci_pdl()
        self.attivita_page.imposta_date(str(date_start), str(date_end))
        self.attivita_page.seleziona_ditta("CO.EMI SRL")

        self.log(f"   Selezione di {len(requesters)} richiedenti...")
        self.attivita_page.seleziona_richiedente(requesters)
        self.update_step("filter", StepStatus.COMPLETED)

        # 3. Ricerca ed Export
        self.update_step("search", StepStatus.RUNNING)
        self.log("[CERCA] Avvio ricerca massiva...")
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

        return True

    def _get_selector(self, locator: tuple[str, str]) -> str:
        _by, value = locator
        if value.startswith(("//", "(")):
            return f"xpath={value}"
        if _by == "id":
            return f"id={value}"
        return value

    def _scarica_excel(self) -> str | None:
        if not self.attivita_page or not self.page:
            return None
        self.log("   Esportazione Excel massiva...")
        try:
            with self.page.expect_download(timeout=300000) as download_info:
                if self.attivita_page.esporta_excel():
                    download = download_info.value
                    dest = Path(self.download_path) / download.suggested_filename
                    download.save_as(str(dest))
                    return str(dest)
        except Exception as e:
            self.log(f"❌ Errore download Excel: {e}")
        return None

    def _parse_excel_results(self, file_path: str) -> None:
        try:
            self.log("   Analisi risultati Excel...")
            df = pd.read_excel(file_path, header=0)
            count_pdl = 0
            for _, row in df.iterrows():
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
                    pdl = str(row.iloc[0]).strip() if len(row) > 0 else "N/D"
                    desc = str(row.iloc[1]).strip() if len(row) > 1 else ""
                    richiedente = (
                        str(row.iloc[IDX_RICHIEDENTE]).strip() if len(row) > IDX_RICHIEDENTE else "N/D"
                    )
                    unita = str(row.iloc[IDX_UNITA]).strip() if len(row) > IDX_UNITA else ""
                    area = str(row.iloc[IDX_AREA]).strip() if len(row) > IDX_AREA else ""

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
            self.log(f"✅ Trovati {count_pdl} record programmati.")
        except Exception as e:
            self.log(f"⚠️ Errore parsing Excel: {e}")

    def _cleanup_temp_file(self, file_path: str) -> None:
        with suppress(Exception):
            Path(file_path).unlink()
            self.log("    File temporaneo rimosso.")
