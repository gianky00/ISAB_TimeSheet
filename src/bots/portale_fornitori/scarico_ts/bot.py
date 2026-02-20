"""
SyncroJob - Scarico TS Bot
Bot per il download automatico dei timesheet dal portale ISAB.
Sincronizzato con la logica stabile del branch main e arricchito con STEPS per Cyber-Stepper V5.
"""

import shutil
import time
from contextlib import suppress
from pathlib import Path
from typing import Any, ClassVar

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.bots.base import BaseBot, StepStatus
from src.core.timesheet_processor import TimesheetProcessor
from src.utils.helpers import sanitize_filename


class ScaricaTSBot(BaseBot):
    """
    Bot per lo scarico automatico dei timesheet dal portale ISAB.
    """

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Portale"),
        ("filters", "Impostazione Filtri"),
        ("download", "Download Timesheet"),
        ("process", "Elaborazione VBA"),
        ("cleanup", "Chiusura Sessione")
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
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"},
        ]

    @property
    def name(self) -> str:
        return "Scarico TS"

    @property
    def description(self) -> str:
        return "Scarica i timesheet dal portale ISAB"

    def __init__(
        self,
        data_da: str = "01.01.2025",
        fornitore: str = "",
        elabora_ts: bool = False,
        **kwargs,
    ):
        """
        Inizializza il bot.
        """
        super().__init__(**kwargs)
        self.data_da = data_da
        self.fornitore = fornitore
        self.elabora_ts = elabora_ts

    def _ask_user(self, prompt: str) -> str:
        """Richiede input all'utente."""
        if self._input_callback:
            return self._input_callback(prompt)
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
        """Esegue il download dei timesheet."""
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

            # Se almeno uno è stato scaricato, consideriamo lo step riuscito (o parziale)
            status_download = StepStatus.COMPLETED if success_count == len(rows) else StepStatus.ERROR
            if success_count > 0 and success_count < len(rows):
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

        self.log(f"🚀 Inizio scarico TS per {len(rows)} OdA (Fornitore: {self.fornitore})...")

        # Chrome downloads directly to download_path (if configured)
        # Forza la risoluzione del path per coerenza con BaseBot
        source_dir = Path(self.download_path).resolve() if self.download_path else Path.home() / "Downloads"
        dest_dir = source_dir

        # Aggiorna download_path per garantire che i metodi successivi usino lo stesso folder
        self.download_path = str(source_dir)

        return rows, dest_dir

    def _process_oda_rows(self, rows: list[dict[str, Any]], dest_dir: Path) -> tuple[int, list[str]]:
        """Cicla sugli OdA ed esegue la ricerca e il download."""
        success_count = 0
        downloaded_files = []
        source_dir = Path(self.download_path).resolve() if self.download_path else Path.home() / "Downloads"

        for row in rows:
            self._check_stop()
            numero_oda = str(row.get("numero_oda", "")).strip()
            posizione_oda = str(row.get("posizione_oda", "")).strip()

            if not numero_oda:
                continue

            try:
                if self._search_oda(numero_oda, posizione_oda):
                    final_path = self._download_excel(source_dir, dest_dir, numero_oda, posizione_oda)
                    if final_path:
                        success_count += 1
                        downloaded_files.append(str(final_path))
            except Exception as e:
                self.log(f"❌ Errore OdA {numero_oda}: {e}")

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
            # Numero OdA
            campo_num = self.wait.until(EC.presence_of_element_located((By.NAME, "NumeroOda")))
            self.driver.execute_script("arguments[0].value = arguments[1];", campo_num, numero_oda)
            self.driver.execute_script(js_dispatch, campo_num)

            # Posizione OdA
            campo_pos = self.wait.until(EC.presence_of_element_located((By.NAME, "PosizioneOda")))
            self.driver.execute_script(
                "arguments[0].value = ''; arguments[0].value = arguments[1];",
                campo_pos,
                posizione_oda,
            )
            self.driver.execute_script(js_dispatch, campo_pos)

            # Click Cerca
            xpath_cerca = "//a[contains(@class, 'x-btn')][.//span[normalize-space(text())='Cerca']]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerca))).click()

            self._attendi_scomparsa_overlay(90)
            return True
        except Exception as e:
            self.log(f"⚠️ Errore durante l'inserimento ricerca OdA {numero_oda}: {e}")
            return False

    def _run_vba_processing(self, file_list: list[str], dest_dir: Path):
        """Esegue il post-processing stile VBA (TimesheetProcessor)."""
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

    def _navigate_to_timesheet(self) -> bool:
        """Naviga a Report -> Timesheet."""
        if not self.wait:
            return False

        self._check_stop()

        try:
            # Click su "Report"
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Report']"))
            ).click()
            self._attendi_scomparsa_overlay()

            # Click su "Timesheet"
            timesheet_menu_xpath = "//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Timesheet']]"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, timesheet_menu_xpath))).click()

            # Attendi che il dropdown Fornitore sia visibile
            fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, fornitore_arrow_xpath)))
            self._attendi_scomparsa_overlay()

            return True

        except Exception as e:
            self.log(f"❌ Impossibile navigare al menu Timesheet: {e}")
            return False

    def _setup_filters(self) -> bool:
        """Imposta Fornitore e Data Da."""
        if not self.driver or not self.wait or not self.long_wait:
            return False

        self._check_stop()

        try:
            # Seleziona Fornitore
            fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            fornitore_arrow_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, fornitore_arrow_xpath))
            )
            ActionChains(self.driver).move_to_element(fornitore_arrow_element).click().perform()

            # Seleziona l'opzione fornitore
            fornitore_option_xpath = f"//li[normalize-space(text())='{self.fornitore}']"
            fornitore_option = self.long_wait.until(
                EC.presence_of_element_located((By.XPATH, fornitore_option_xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", fornitore_option)
            self.driver.execute_script("arguments[0].click();", fornitore_option)

            self._attendi_scomparsa_overlay()

            # Inserisci Data Da
            campo_data_da = self.wait.until(EC.visibility_of_element_located((By.NAME, "DataTimesheetDa")))
            campo_data_da.clear()
            campo_data_da.send_keys(self.data_da)

            return True

        except Exception as e:
            self.log(f"❌ Errore nell'impostazione dei filtri: {e}")
            return False

    def _download_excel(
        self, source_dir: Path, dest_dir: Path, numero_oda: str, posizione_oda: str
    ) -> Path | None:
        """Scarica il file Excel, lo rinomina e lo sposta."""
        if not self.wait or not self.driver:
            return None

        # Normalize path
        source_dir_path = Path(source_dir).resolve()
        self.log(f"[DEBUG] Cerco file in: {source_dir_path}")

        if not source_dir_path.exists():
            self.log(f"✗ Cartella non esiste: {source_dir_path}")
            return None

        # 1. Cattura file pre-esistenti
        files_before = {f for f in source_dir_path.iterdir() if f.is_file() and f.suffix.lower() == ".xlsx"}
        self.log(f"[DEBUG] File .xlsx prima del download: {len(files_before)}")

        # 2. Click pulsante Excel (Logica Main Branch con micro-attesa)
        time.sleep(1)
        if not self._click_excel_export_button():
            return None

        # 3. Attendi download
        downloaded_file = self._wait_for_new_file(source_dir_path, files_before)
        if not downloaded_file:
            # Debug: lista file attuali
            current_files = list(source_dir_path.iterdir()) if source_dir_path.exists() else []
            self.log(f"[DEBUG] File attuali nella cartella: {[f.name for f in current_files[:10]]}")
            self.log("⚠️ File non scaricato nel tempo stabilito.")
            return None

        # 4. Finalizzazione (Determina nome e Sposta)
        final_path = self._get_final_download_path(source_dir_path, dest_dir, numero_oda, posizione_oda)
        return self._move_to_destination(downloaded_file, final_path)

    def _click_excel_export_button(self) -> bool:
        """Individua e clicca il pulsante di esportazione Excel usando il selettore stabile del branch main."""
        if not self.wait:
            return False

        # XPath ESATTO dal branch main
        xpath = "//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]"
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            btn.click()
            return True
        except Exception as e:
            self.log(f"⚠️ Impossibile cliccare esportazione Excel: {e}")
            return False

    def _wait_for_new_file(self, source_dir: Path, files_before: set[Path], timeout: int = 35) -> Path | None:
        """Attende la comparsa di un nuovo file .xlsx (Logica Main Branch)."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            with suppress(Exception):
                # Se c'è un download in corso (.crdownload), continua l'attesa
                if any(f.suffix == ".crdownload" for f in source_dir.iterdir()):
                    time.sleep(1)
                    continue

                current_files = {
                    f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() == ".xlsx"
                }
                new_files = current_files - files_before
                if new_files:
                    # Restituisce il più recente tra i nuovi
                    return max(list(new_files), key=lambda f: f.stat().st_mtime)

            time.sleep(0.5)
        return None

    def _get_final_download_path(self, source_dir: Path, dest_dir: Path, oda: str, pos: str) -> Path:
        """Costruisce il percorso finale basato su ODA/POS."""
        safe_oda = sanitize_filename(oda)
        safe_pos = sanitize_filename(pos)

        base_name = (
            f"TS_{safe_oda}-{safe_pos}" if safe_pos and safe_pos != "unnamed_file" else f"TS_{safe_oda}"
        )
        filename = f"{base_name}.xlsx"

        # Se elabora_ts, il file resta in temp (Downloads) rinominato
        target_dir = source_dir if self.elabora_ts else dest_dir
        final_path = target_dir / filename

        if final_path.exists():
            with suppress(Exception):
                final_path.unlink()

            if final_path.exists():
                ts = time.strftime("%Y%m%d-%H%M%S")
                final_path = target_dir / f"{base_name}_{ts}.xlsx"

        return final_path

    def _move_to_destination(self, src: Path, dest: Path) -> Path | None:
        """Sposta il file scaricato con retry logic."""
        dest.parent.mkdir(parents=True, exist_ok=True)

        for attempt in range(3):
            try:
                shutil.move(str(src), str(dest))
                self.log(f"✅ Scaricato: {dest.name}")
                return dest
            except Exception as e:
                self.log(f"⚠️ Tentativo spostamento {attempt + 1}/3 fallito: {e}")
                time.sleep(1)
        self.log(f"❌ Impossibile spostare il file in: {dest}")
        return None
