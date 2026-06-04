"""SyncroJob - Scarico TS Bot.

Bot per il download automatico dei timesheet dal portale ISAB.
Sincronizzato con la logica stabile del branch main e arricchito con STEPS per Cyber-Stepper V5.
"""

import shutil
import time
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, ClassVar

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812

from src.application.services.constants import Timeouts
from src.application.services.timesheet_processor import TimesheetProcessor
from src.infrastructure.bots.base import StepStatus
from src.infrastructure.bots.base.selenium_base_bot import SeleniumBaseBot
from src.infrastructure.bots.base.selenium_bot_config import SeleniumBotConfig
from src.infrastructure.bots.base.wait_helpers import PollConfig, poll_for_new_file
from src.infrastructure.utils.helpers import sanitize_filename


class ScaricaTSBot(SeleniumBaseBot):
    """Bot per lo scarico automatico dei timesheet dal portale ISAB.

    Inizializza il bot Scarico TS.
    """

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Portale"),
        ("filters", "Impostazione Filtri"),
        ("download", "Download Timesheet"),
        ("process", "Elaborazione VBA"),
        ("cleanup", "Chiusura Sessione"),
    ]

    @staticmethod
    def get_name() -> str:
        """Restituisce il nome visualizzato del bot."""
        return "Scarico TS"

    @staticmethod
    def get_description() -> str:
        """Restituisce una descrizione delle funzionalità del bot."""
        return "Scarica i timesheet dal portale ISAB"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce la configurazione delle colonne per l'input dati."""
        return [
            {"name": "numero_oda", "label": "Numero OdA", "type": "text"},
            {"name": "posizione_oda", "label": "Posizione OdA", "type": "text"},
        ]

    @property
    def name(self) -> str:
        """Restituisce l'ID del bot."""
        return "scarico_ts"

    @property
    def description(self) -> str:
        """Restituisce la descrizione del bot."""
        return "Scarica i timesheet dal portale ISAB"

    def __init__(  # noqa: PLR0913
        self,
        username: str | None = None,
        password: str | None = None,
        config: SeleniumBotConfig | None = None,
        data_da: str | None = None,
        fornitore: str = "",
        elabora_ts: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(username, password, config)
        self.data_da = data_da or f"01.01.{datetime.now(UTC).year}"
        self.fornitore = fornitore
        self.elabora_ts = elabora_ts

    def _ask_user(self, prompt: str) -> str:
        """Richiede input all'utente."""
        if self._input_callback:
            return str(self._input_callback(prompt))
        return ""

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Validazione specifica per Scarico TS."""
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
        """Esegue il download dei timesheet orchestrando i vari step."""
        self.update_step("login", StepStatus.COMPLETED)
        rows, dest_dir = self._prepare_run_environment(data)

        try:
            if not self._setup_timesheet_view():
                return False

            self.update_step("download", StepStatus.RUNNING)
            success_count, downloaded_files = self._process_oda_rows(rows, dest_dir)

            # Valutazione esito scarico
            self._log_download_summary(success_count, len(rows))
            status_download = StepStatus.COMPLETED if success_count == len(rows) else StepStatus.ERROR
            self.update_step("download", status_download)

            if self.elabora_ts and downloaded_files:
                self._handle_vba_processing(downloaded_files, dest_dir)

            self.update_step("cleanup", StepStatus.COMPLETED)
            return success_count == len(rows)

        except Exception as e:
            self.log(f"❌ Errore imprevisto nel flusso run: {e}")
            return False

    def _setup_timesheet_view(self) -> bool:
        """Naviga e imposta i filtri iniziali."""
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
        return True

    def _log_download_summary(self, success: int, total: int) -> None:
        """Emette log di riepilogo per il download."""
        self.log(f"ℹ️ Download completati: {success}/{total}.")
        if 0 < success < total:
            self.log(f"⚠️ Scarico parziale: {success} su {total}")

    def _handle_vba_processing(self, files: list[str], dest_dir: Path) -> None:
        """Coordina l'elaborazione VBA post-download."""
        self.update_step("process", StepStatus.RUNNING)
        self._run_vba_processing(files, dest_dir)
        self.update_step("process", StepStatus.COMPLETED)

    def _prepare_run_environment(self, data: Any) -> tuple[list[dict[str, Any]], Path]:
        """Estrae i dati e prepara la directory di destinazione."""
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

        self.log(f"[AVVIO] Inizio scarico TS per {len(rows)} OdA (Fornitore: {self.fornitore})...")

        # Chrome downloads direttamente a download_path
        source_dir = Path(self.download_path).resolve() if self.download_path else Path.home() / "Downloads"
        dest_dir = source_dir
        self.download_path = str(source_dir)

        return rows, dest_dir

    def _process_oda_rows(self, rows: list[dict[str, Any]], dest_dir: Path) -> tuple[int, list[str]]:
        """Cicla sugli OdA ed esegue la ricerca e il download."""
        success_count = 0
        downloaded_files = []
        source_dir = Path(self.download_path).resolve()

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
                    final_path = self._download_excel(source_dir, dest_dir, numero_oda, posizione_oda)
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

            if callback := getattr(self, "_progress_callback", None):
                callback(i, res, "" if res else msg)

        return success_count, downloaded_files

    def _search_oda(self, numero_oda: str, posizione_oda: str) -> bool:
        """Inserisce i parametri di ricerca e clicca Cerca."""
        if not self.wait or not self.driver:
            return False

        try:
            js_dispatch = """
        var el = arguments[0];
        var ev_in = new Event('input', {bubbles:true}); el.dispatchEvent(ev_in);
        var ev_ch = new Event('change', {bubbles:true}); el.dispatchEvent(ev_ch);
      """
            campo_num = self.wait.until(EC.presence_of_element_located((By.NAME, "NumeroOda")))
            self.driver.execute_script("arguments[0].value = arguments[1];", campo_num, numero_oda)
            self.driver.execute_script(js_dispatch, campo_num)

            campo_pos = self.wait.until(EC.presence_of_element_located((By.NAME, "PosizioneOda")))
            self.driver.execute_script(
                "arguments[0].value = ''; arguments[0].value = arguments[1];", campo_pos, posizione_oda
            )
            self.driver.execute_script(js_dispatch, campo_pos)

            xpath_cerca = "//a[contains(@class, 'x-btn')][.//span[normalize-space(text())='Cerca']]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerca))).click()

            self._attendi_scomparsa_overlay(Timeouts.OVERLAY)
        except Exception as e:
            self.log(f"⚠️ Errore ricerca OdA {numero_oda}: {e}")
            return False
        else:
            return True

    def _run_vba_processing(self, file_list: list[str], dest_dir: Path) -> None:
        """Esegue il post-processing stile VBA (TimesheetProcessor)."""
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

    def _navigate_to_timesheet(self) -> bool:
        """Naviga a Report -> Timesheet."""
        if not self.wait:
            return False
        self._check_stop()

        try:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Report']"))
            ).click()
            self._attendi_scomparsa_overlay()

            timesheet_menu_xpath = "//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Timesheet']]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, timesheet_menu_xpath))).click()

            fornitore_arrow_xpath = "//input[@name='CodiceFornitore' or @name='Fornitore']/ancestor::div[contains(@class, 'x-form-trigger-wrap') or contains(@class, 'x-form-item-body')]//div[contains(@class, 'x-form-arrow-trigger')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, fornitore_arrow_xpath)))
            self._attendi_scomparsa_overlay()
        except Exception as e:
            self.log(f"❌ Errore navigazione Timesheet: {e}")
            return False
        else:
            return True

    def _setup_filters(self) -> bool:
        """Imposta Fornitore e Data Da."""
        if not self.driver or not self.wait or not self.long_wait:
            return False
        self._check_stop()

        try:
            arrow_xpath = "//input[@name='CodiceFornitore' or @name='Fornitore']/ancestor::div[contains(@class, 'x-form-trigger-wrap') or contains(@class, 'x-form-item-body')]//div[contains(@class, 'x-form-arrow-trigger')]"
            arrow = self.wait.until(EC.element_to_be_clickable((By.XPATH, arrow_xpath)))
            ActionChains(self.driver).move_to_element(arrow).click().perform()

            option_xpath = f"//li[normalize-space(text())='{self.fornitore}']"
            option = self.long_wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option)
            self.driver.execute_script("arguments[0].click();", option)
            self._attendi_scomparsa_overlay()

            campo_data_da = self.wait.until(EC.visibility_of_element_located((By.NAME, "DataTimesheetDa")))
            campo_data_da.clear()
            campo_data_da.send_keys(self.data_da)
        except Exception as e:
            self.log(f"❌ Errore impostazione filtri: {e}")
            return False
        else:
            return True

    def _download_excel(
        self, source_dir: Path, dest_dir: Path, numero_oda: str, posizione_oda: str
    ) -> Path | None:
        """Scarica il file Excel, lo rinomina e lo sposta."""
        if not self.wait or not self.driver:
            return None

        source_dir_path = Path(source_dir).resolve()
        if not source_dir_path.exists():
            self.log(f"  Cartella non esiste: {source_dir_path}")
            return None

        # Snapshot file esistenti
        allowed_ext = {".xlsx", ".xls"}
        files_before = {
            f for f in source_dir_path.iterdir() if f.is_file() and f.suffix.lower() in allowed_ext
        }

        # Trigger
        time.sleep(Timeouts.UI_DELAY)
        if not self._click_excel_export_button():
            return None

        # Polling

        res_path = poll_for_new_file(
            PollConfig(
                directory=source_dir_path,
                pattern=["*.xlsx", "*.xls"],
                timeout=Timeouts.DOWNLOAD,
            ),
            files_before=files_before,
        )

        if not res_path:
            self.log(f"⚠️ Timeout download ({Timeouts.DOWNLOAD}s).")
            return None

        downloaded_file = Path(res_path)
        final_path = self._get_final_download_path(
            source_dir_path, dest_dir, numero_oda, posizione_oda, downloaded_file.suffix.lower()
        )
        return self._move_to_destination(downloaded_file, final_path)

    def _click_excel_export_button(self) -> bool:
        """Clicca il pulsante di esportazione Excel."""
        if not self.wait or not self.driver:
            return False
        xpath = "//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]"
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(0.5)
            btn.click()
        except Exception as e:
            self.log(f"⚠️ Errore click export: {e}")
            return False
        else:
            return True

    def _get_final_download_path(
        self, source_dir: Path, dest_dir: Path, oda: str, pos: str, extension: str = ".xlsx"
    ) -> Path:
        """Costruisce il percorso finale basato su ODA/POS."""
        safe_oda, safe_pos = sanitize_filename(oda), sanitize_filename(pos)
        base_name = (
            f"TS_{safe_oda}-{safe_pos}" if safe_pos and safe_pos != "unnamed_file" else f"TS_{safe_oda}"
        )
        filename = f"{base_name}{extension}"

        target_dir = source_dir if self.elabora_ts else dest_dir
        final_path = target_dir / filename

        if final_path.exists():
            with suppress(Exception):
                final_path.unlink()
            if final_path.exists():
                ts = time.strftime("%Y%m%d-%H%M%S")
                final_path = target_dir / f"{base_name}_{ts}{extension}"
        return final_path

    def _move_to_destination(self, src: Path, dest: Path) -> Path | None:
        """Sposta il file scaricato con retry logic."""
        dest.parent.mkdir(parents=True, exist_ok=True)
        max_move_attempts = 3
        for attempt in range(max_move_attempts):
            try:
                shutil.move(str(src), str(dest))
                self.log(f"✅ Scaricato: {dest.name}")
            except Exception as e:
                self.log(f"⚠️ Tentativo {attempt + 1}/{max_move_attempts} fallito: {e}")
                time.sleep(Timeouts.UI_DELAY * 2)  # 1s
            else:
                return dest

        self.log(f"❌ Impossibile spostare il file in: {dest}")
        return None
