"""
SyncroJob - Playwright Scarico TS Bot
Versione Playwright del bot per il download dei timesheet dal portale ISAB.
"""

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
    Gestisce la navigazione, il filtraggio per OdA e l'esportazione Excel massiva.
    """

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Portale"),
        ("filters", "Impostazione Filtri"),
        ("download", "Download Timesheet"),
        ("process", "Elaborazione VBA"),
        ("cleanup", "Chiusura Sessione"),
    ]
    """Timeline operativa del bot."""

    @property
    def name(self) -> str:
        """Restituisce il nome visualizzato del bot."""
        return "Scarico TS (PW)"

    @property
    def description(self) -> str:
        """Restituisce la descrizione estesa."""
        return "Scarica i timesheet dal portale ISAB (Playwright)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce lo schema delle colonne per l'input dati."""
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
        """Inizializza le propriet  del bot Playwright."""
        super().__init__(**kwargs)
        self.data_da = data_da or f"01.01.{datetime.now(UTC).year}"
        self.fornitore = fornitore
        self.elabora_ts = elabora_ts

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Valida la presenza del fornitore e degli OdA da scaricare."""
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

            self.log(f"ℹ️ Download completati: {success_count}/{len(rows)}.")

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
        except Exception as e:
            self.log(f"❌ Errore imprevisto nel flusso run: {e}")
            return False
        else:
            return success_count == len(rows)

    def _prepare_run_environment(self, data: Any) -> tuple[list[dict[str, Any]], Path]:
        """Inizializza i parametri di esecuzione e la cartella di destinazione."""
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

        self.log(f"[AVVIO] Inizio scarico TS (PW) per {len(rows)} OdA (Fornitore: {self.fornitore})...")
        dest_dir = Path(self.download_path).resolve() if self.download_path else Path.home() / "Downloads"
        return rows, dest_dir

    def _process_oda_rows(self, rows: list[dict[str, Any]], dest_dir: Path) -> tuple[int, list[str]]:
        """Esegue l'iterazione sulle righe degli OdA per la ricerca e il download."""
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
        """Attende che gli overlay grafici vengano rimossi dal DOM."""
        if not self.page:
            return
        try:
            xpath = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            self.page.wait_for_selector(f"xpath={xpath}", state="hidden", timeout=Timeouts.OVERLAY * 1000)
        except TimeoutError:
            self.log("⚠️ Timeout attesa overlay.")

    def _navigate_to_timesheet(self) -> bool:
        """Naviga verso il menu Report -> Timesheet."""
        if not self.page:
            return False
        self._check_stop()
        try:
            el_report = self.page.wait_for_selector(
                "xpath=//*[normalize-space(text())='Report']", state="attached"
            )
            if el_report:
                el_report.evaluate("el => el.click()")

            self._wait_for_overlay()

            timesheet_menu_xpath = "xpath=//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Timesheet']]"
            el_ts = self.page.wait_for_selector(timesheet_menu_xpath, state="attached")
            if el_ts:
                el_ts.evaluate("el => el.click()")

            fornitore_arrow_xpath = "xpath=//input[@name='CodiceFornitore' or @name='Fornitore']/ancestor::div[contains(@class, 'x-form-trigger-wrap') or contains(@class, 'x-form-item-body')]//div[contains(@class, 'x-form-arrow-trigger')]"
            self.page.wait_for_selector(fornitore_arrow_xpath, state="visible")
            self._wait_for_overlay()
        except Exception as e:
            self.log(f"❌ Impossibile navigare al menu Timesheet: {e}")
            return False
        else:
            return True

    def _setup_filters(self) -> bool:
        """Imposta i filtri iniziali (Fornitore, Data)."""
        if not self.page:
            return False
        try:
            self.log(f"Impostazione filtri per fornitore: {self.fornitore}")
            input_sel = self._get_selector(ScaricoTSLocators.SUPPLIER_INPUT)
            arrow_sel = self._get_selector(ScaricoTSLocators.SUPPLIER_DROPDOWN_ARROW)

            if not self._select_combobox_item(input_sel, arrow_sel, self.fornitore):
                self.log("   Avviso: Selezione fornitore fallita, tento inserimento manuale forzato.")
                self.page.fill(input_sel, self.fornitore)
                self.page.press(input_sel, "Enter")

            self._wait_overlay()

            data_da_sel = self._get_selector(ScaricoTSLocators.DATE_FROM_FIELD)

            # Inserimento via JS per robustezza (allineamento con Selenium)
            self.page.locator(data_da_sel).evaluate(
                "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', {bubbles: true})); el.dispatchEvent(new Event('change', {bubbles: true})); }",
                self.data_da,
            )
        except Exception as e:
            self.log(f"❌ Errore nell'impostazione dei filtri: {e}")
            return False
        else:
            return True

    def _search_oda(self, numero_oda: str, posizione_oda: str) -> bool:
        """Esegue la ricerca per un specifico OdA."""
        if not self.page:
            return False
        try:
            num_oda_sel = self._get_selector(ScaricoTSLocators.ODA_NUMBER_FIELD)
            pos_oda_sel = self._get_selector(ScaricoTSLocators.ODA_POSITION_FIELD)

            # Inserimento via JS per robustezza (come Selenium) per bypassare controlli di visibilità restrittivi
            js_script = "(el, val) => { el.value = val; el.dispatchEvent(new Event('input', {bubbles: true})); el.dispatchEvent(new Event('change', {bubbles: true})); }"

            self.page.locator(num_oda_sel).evaluate(js_script, numero_oda)
            self.page.locator(pos_oda_sel).evaluate(js_script, posizione_oda)

            xpath_cerca = "xpath=//a[contains(@class, 'x-btn')][.//span[normalize-space(text())='Cerca']]"
            # Utilizza state="visible" e click nativo per simulare fedelmente l'interazione umana (allineato a Selenium)
            el_cerca = self.page.wait_for_selector(xpath_cerca, state="visible", timeout=5000)
            if el_cerca:
                el_cerca.click()

            # --- ATTESA ROBUSTA DEL CARICAMENTO ASINCRONO ---
            # 1. Attesa di cortesia per far partire la richiesta e far apparire l'overlay
            self.page.wait_for_timeout(500)

            # 2. Attesa della scomparsa dell'overlay
            self._wait_for_overlay()

            # 3. Attesa dinamica del rendering della griglia (vuota o con risultati)
            xpath_rows_or_empty = (
                "xpath=//div[contains(@class, 'x-grid-empty')] | "
                "//table[contains(@class, 'x-grid-item')] | "
                "//tr[contains(@class, 'x-grid-row')]"
            )
            try:
                self.page.wait_for_selector(xpath_rows_or_empty, state="attached", timeout=5000)
            except Exception:
                self.log("⚠️ Timeout attesa caricamento griglia risultati, procedo comunque.")

            # Ulteriore attesa per stabilità del repaint grafico ExtJS
            self.page.wait_for_timeout(500)
            # -------------------------------------------------

            # Verifica se ci sono risultati
            xpath_empty = "//div[contains(@class, 'x-grid-empty')]"
            if self.page.locator(f"xpath={xpath_empty}").is_visible():
                self.log(f"  Nessun TimeSheet trovato per OdA {numero_oda} / {posizione_oda}")
                return False
        except Exception as e:
            self.log(f"❌ Errore nella ricerca OdA: {e}")
            return False
        else:
            return True

    def _select_all_and_download(self, filename: str) -> bool:
        """Seleziona tutti i record nella griglia e clicca Scarica."""
        if not self.page:
            return False
        try:
            # Seleziona tutto tramite la checkbox nell'header
            xpath_check_all = "//div[contains(@class, 'x-column-header-checkbox')]//span[contains(@class, 'x-column-header-text')]"
            el_check = self.page.wait_for_selector(f"xpath={xpath_check_all}", state="attached")
            if el_check:
                el_check.evaluate("el => el.click()")

            # Pulsante Scarica
            xpath_scarica = "//a[contains(@class, 'x-btn')][.//span[normalize-space(text())='Scarica']]"

            with self.page.expect_download() as download_info:
                el_download = self.page.wait_for_selector(f"xpath={xpath_scarica}", state="attached")
                if el_download:
                    el_download.evaluate("el => el.click()")

            download = download_info.value
            base_dir = (
                Path(self.download_path).resolve()
                if self.download_path
                else (Path.home() / "Downloads").resolve()
            )
            base_dir.mkdir(parents=True, exist_ok=True)
            download_path = base_dir / filename
            download.save_as(str(download_path))

            self.log(f"  Download completato: {filename}")
        except Exception as e:
            self.log(f"❌ Errore durante il download: {e}")
            return False
        else:
            return True

    def _download_excel(self, dest_dir: Path, numero_oda: str, posizione_oda: str) -> Path | None:
        """Esegue l'export Excel specifico per un OdA tramite il pulsante tecnico."""
        if not self.page:
            return None
        try:
            # Attesa di cortesia per far stabilizzare l'interfaccia dopo il caricamento dei dati
            self.page.wait_for_timeout(500)

            # XPath ESATTO dal branch main
            xpath_export = "xpath=//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]"

            with self.page.expect_download(timeout=Timeouts.DOWNLOAD * 1000) as download_info:
                el_export = self.page.wait_for_selector(xpath_export, state="attached")
                if el_export:
                    el_export.evaluate("el => el.click()")

            download = download_info.value
            extension = Path(download.suggested_filename).suffix.lower() or ".xlsx"

            final_path = self._get_final_download_path(dest_dir, numero_oda, posizione_oda, extension)
            download.save_as(str(final_path))

            self.log(f"✅ Scaricato: {final_path.name}")
        except Exception as e:
            self.log(f"⚠️ Impossibile scaricare esportazione Excel: {e}")
            return None
        else:
            return final_path

    def _get_final_download_path(self, dest_dir: Path, oda: str, pos: str, extension: str) -> Path:
        """Calcola il percorso finale di salvataggio del file, gestendo eventuali duplicati."""
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
            ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            final_path = target_dir / f"{base_name}_{ts}{extension}"
        return final_path

    def _run_vba_processing(self, file_list: list[str], dest_dir: Path) -> None:
        """Avvia la logica di processamento VBA (TimesheetProcessor) sui file scaricati."""
        self.log(f"    Avvio elaborazione TS (Logica VBA) su {len(file_list)} file...")
        processed = 0
        for f in file_list:
            ok, msg = TimesheetProcessor.process_and_move(Path(f), dest_dir)
            if ok:
                self.log(f" ✅ {msg}")
                processed += 1
            elif msg.startswith("EMPTY:"):
                clean_msg = msg.replace("EMPTY:", "").strip()
                self.log(f" ⚠️ {clean_msg}")
                # Emette il segnale per far apparire il popup grafico nella GUI
                self.signals.critical_error.emit("Avviso Timesheet Vuoto", clean_msg)
            else:
                self.log(f" ❌ Errore elaborazione {Path(f).name}: {msg}")
        self.log(f"   Elaborazione conclusa: {processed}/{len(file_list)} completati.")
