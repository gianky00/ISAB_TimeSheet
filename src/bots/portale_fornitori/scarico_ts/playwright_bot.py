# mypy: disable-error-code="no-untyped-call"
"""
SyncroJob - Playwright Scarico TS Bot
Versione Playwright del bot per il download dei timesheet dal portale ISAB.
"""

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, ClassVar

from playwright.sync_api import TimeoutError

from src.bots.base import StepStatus
from src.bots.base.playwright_base_bot import PlaywrightBaseBot
from src.core.constants import Timeouts
from src.core.timesheet_processor import TimesheetProcessor
from src.utils.helpers import sanitize_filename

from .locators import ScaricoTSLocators


class PlaywrightScaricaTSBot(PlaywrightBaseBot):
    """
    Bot per lo scarico automatico dei timesheet dal portale ISAB usando Playwright.
    """

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Portale"),
        ("filters", "Impostazione Filtri"),
        ("download", "Download Timesheet"),
        ("process", "Elaborazione VBA"),
        ("cleanup", "Chiusura Sessione"),
    ]

    @property
    def name(self) -> str:
        return "Scarico TS (PW)"

    @property
    def description(self) -> str:
        return "Scarica i timesheet dal portale ISAB (Playwright)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return [
            {"name": "numero_oda", "label": "Numero OdA", "type": "text"},
            {"name": "posizione_oda", "label": "Posizione OdA", "type": "text"},
        ]

    def __init__(
        self,
        data_da: str | None = None,
        fornitore: str = "",
        elabora_ts: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.data_da = data_da or f"01.01.{datetime.now(UTC).year}"
        self.fornitore = fornitore
        self.elabora_ts = elabora_ts

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            return False, base_msg

        if not self.fornitore:
            if isinstance(data, dict):
                if not data.get("fornitore"):
                    return False, "Fornitore non specificato."
            else:
                return False, "Fornitore non specificato."

        rows = data.get("rows", []) if isinstance(data, dict) else data
        if not rows:
            return False, "Nessun OdA da scaricare."

        return True, ""

    def run(self, data: list[dict[str, Any]] | dict[str, Any]) -> bool:
        """Esegue il download dei timesheet con Playwright."""
        self.update_step("login", StepStatus.COMPLETED)

        rows, dest_dir = self._prepare_run_environment(data)

        try:
            self.update_step("nav", StepStatus.RUNNING)
            if not self._navigate_to_timesheet():
                self.update_step("nav", StepStatus.ERROR)
                return False
            self.update_step("nav", StepStatus.COMPLETED)

            self.update_step("filters", StepStatus.RUNNING)
            if not self._setup_filters():
                self.update_step("filters", StepStatus.ERROR)
                return False
            self.update_step("filters", StepStatus.COMPLETED)

            self.update_step("download", StepStatus.RUNNING)
            success_count, downloaded_files = self._process_oda_rows(rows, dest_dir)

            self.log(f"✨ Download completati: {success_count}/{len(rows)}.")

            status_download = StepStatus.COMPLETED if success_count == len(rows) else StepStatus.ERROR
            if 0 < success_count < len(rows):
                self.log(f"⚠️ Scarico parziale: {success_count} su {len(rows)}")

            self.update_step("download", status_download)

            if self.elabora_ts and downloaded_files:
                self.update_step("process", StepStatus.RUNNING)
                self._run_vba_processing(downloaded_files, dest_dir)
                self.update_step("process", StepStatus.COMPLETED)

            self.update_step("cleanup", StepStatus.RUNNING)
            self.update_step("cleanup", StepStatus.COMPLETED)
            return success_count == len(rows)

        except Exception as e:
            self.log(f"❌ Errore imprevisto nel flusso run: {e}")
            return False

    def _prepare_run_environment(self, data: Any) -> tuple[list[dict[str, Any]], Path]:
        rows: list[dict[str, Any]]
        if isinstance(data, dict):
            rows = data.get("rows", [])
            self.data_da = data.get("data_da", self.data_da)
            forn = data.get("fornitore")
            if forn:
                self.fornitore = str(forn)
            self.elabora_ts = data.get("elabora_ts", self.elabora_ts)
        else:
            rows = list(data)

        self.log(f"🚀 Inizio scarico TS (PW) per {len(rows)} OdA (Fornitore: {self.fornitore})...")
        dest_dir = Path(self.download_path).resolve() if self.download_path else Path.home() / "Downloads"
        return rows, dest_dir

    def _process_oda_rows(self, rows: list[dict[str, Any]], dest_dir: Path) -> tuple[int, list[str]]:
        success_count = 0
        downloaded_files = []

        for i, row in enumerate(rows):
            self._check_stop()
            numero_oda = str(row.get("numero_oda", "")).strip()
            posizione_oda = str(row.get("posizione_oda", "")).strip()

            if not numero_oda:
                continue

            res = False
            msg = ""
            try:
                if self._search_oda(numero_oda, posizione_oda):
                    final_path = self._download_excel(dest_dir, numero_oda, posizione_oda)
                    if final_path:
                        success_count += 1
                        downloaded_files.append(str(final_path))
                        res = True
                    else:
                        msg = "File non scaricato"
                else:
                    msg = "OdA non trovato"
            except Exception as e:
                self.log(f"❌ Errore OdA {numero_oda}: {e}")
                msg = str(e)

            callback = getattr(self, "_progress_callback", None)
            if callback:
                callback(i, res, "" if res else msg)

        return success_count, downloaded_files

    def _wait_for_overlay(self) -> None:
        try:
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            self.page.wait_for_selector(f"xpath={xpath}", state="hidden", timeout=Timeouts.OVERLAY * 1000)
        except TimeoutError:
            self.log("⚠️ Timeout attesa overlay.")

    def _navigate_to_timesheet(self) -> bool:
        if not self.page:
            return False
        self._check_stop()
        try:
            self.page.click("xpath=//*[normalize-space(text())='Report']")
            self._wait_for_overlay()

            timesheet_menu_xpath = "xpath=//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Timesheet']]"
            self.page.click(timesheet_menu_xpath)

            fornitore_arrow_xpath = "xpath=//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            self.page.wait_for_selector(fornitore_arrow_xpath, state="visible")
            self._wait_for_overlay()
            return True
        except Exception as e:
            self.log(f"❌ Impossibile navigare al menu Timesheet: {e}")
            return False

    def _setup_filters(self) -> bool:
        """Imposta i filtri iniziali (Fornitore, Data)."""
        if not self.page:
            return False
        try:
            self.log(f"Impostazione filtri per fornitore: {self.fornitore}")
            arrow_sel = self._get_selector(ScaricoTSLocators.FORNITORE_ARROW)
            self.page.click(arrow_sel)

            fornitore_option_xpath = f"xpath=//li[normalize-space(text())='{self.fornitore}']"
            self.page.click(fornitore_option_xpath)
            self._wait_for_overlay()

            data_da_sel = self._get_selector(ScaricoTSLocators.DATE_FROM_FIELD)
            self.page.fill(data_da_sel, self.data_da)
            return True
        except Exception as e:
            self.log(f"❌ Errore nell'impostazione dei filtri: {e}")
            return False

    def _search_oda(self, numero_oda: str, posizione_oda: str) -> bool:
        """Esegue la ricerca per un specifico OdA."""
        if not self.page:
            return False
        try:
            num_oda_sel = self._get_selector(ScaricoTSLocators.ODA_NUMBER_FIELD)
            pos_oda_sel = self._get_selector(ScaricoTSLocators.ODA_POSITION_FIELD)

            self.page.fill(num_oda_sel, numero_oda)
            # Posizione OdA: prima pulisci poi scrivi
            self.page.locator(pos_oda_sel).fill("")
            self.page.locator(pos_oda_sel).fill(posizione_oda)

            xpath_cerca = "xpath=//a[contains(@class, 'x-btn')][.//span[normalize-space(text())='Cerca']]"
            self.page.click(xpath_cerca)
            self._wait_for_overlay()

            # Verifica se ci sono risultati
            xpath_empty = "//div[contains(@class, 'x-grid-empty')]"
            if self.page.locator(f"xpath={xpath_empty}").is_visible():
                self.log(f"⚠ Nessun TimeSheet trovato per OdA {numero_oda} / {posizione_oda}")
                return False
            return True
        except Exception as e:
            self.log(f"❌ Errore nella ricerca OdA: {e}")
            return False

    def _select_all_and_download(self, filename: str) -> bool:
        """Seleziona tutti i record e clicca Scarica."""
        if not self.page:
            return False
        try:
            # Seleziona tutto tramite la checkbox nell'header
            xpath_check_all = "//div[contains(@class, 'x-column-header-checkbox')]//span[contains(@class, 'x-column-header-text')]"
            self.page.click(f"xpath={xpath_check_all}")

            # Pulsante Scarica
            xpath_scarica = "//a[contains(@class, 'x-btn')][.//span[normalize-space(text())='Scarica']]"

            with self.page.expect_download() as download_info:
                self.page.click(f"xpath={xpath_scarica}")

            download = download_info.value
            download_path = os.path.join(self.download_dir, filename)
            download.save_as(download_path)

            self.log(f"✓ Download completato: {filename}")
            return True
        except Exception as e:
            self.log(f"❌ Errore durante il download: {e}")
            return False

    def _download_excel(self, dest_dir: Path, numero_oda: str, posizione_oda: str) -> Path | None:
        if not self.page:
            return None
        try:
            # XPath ESATTO dal branch main
            xpath_export = "xpath=//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]"

            with self.page.expect_download(timeout=Timeouts.DOWNLOAD * 1000) as download_info:
                self.page.click(xpath_export)

            download = download_info.value
            extension = Path(download.suggested_filename).suffix.lower() or ".xlsx"

            final_path = self._get_final_download_path(dest_dir, numero_oda, posizione_oda, extension)
            download.save_as(str(final_path))

            self.log(f"✅ Scaricato: {final_path.name}")
            return final_path
        except Exception as e:
            self.log(f"⚠️ Impossibile scaricare esportazione Excel: {e}")
            return None

    def _get_final_download_path(self, dest_dir: Path, oda: str, pos: str, extension: str) -> Path:
        safe_oda = sanitize_filename(oda)
        safe_pos = sanitize_filename(pos)
        base_name = (
            f"TS_{safe_oda}-{safe_pos}" if safe_pos and safe_pos != "unnamed_file" else f"TS_{safe_oda}"
        )

        # Se elabora_ts, usiamo una sottocartella temp per evitare conflitti
        target_dir = dest_dir
        if self.elabora_ts:
            target_dir = dest_dir / "temp_processing"
            target_dir.mkdir(parents=True, exist_ok=True)

        final_path = target_dir / f"{base_name}{extension}"
        if final_path.exists():
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_path = target_dir / f"{base_name}_{ts}{extension}"
        return final_path

    def _run_vba_processing(self, file_list: list[str], dest_dir: Path) -> None:
        self.log(f"⚙️ Avvio elaborazione TS (Logica VBA) su {len(file_list)} file...")
        processed = 0
        for f in file_list:
            ok, msg = TimesheetProcessor.process_and_move(Path(f), dest_dir)
            if ok:
                self.log(f"  ✅ {msg}")
                processed += 1
            else:
                self.log(f"  ❌ Errore elaborazione {Path(f).name}: {msg}")
        self.log(f"🏁 Elaborazione conclusa: {processed}/{len(file_list)} completati.")
