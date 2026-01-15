"""
SyncroJob - Scarico TS Bot
Bot per il download automatico dei timesheet dal portale ISAB.
Basato sullo script standalone funzionante.
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.bots.base import BaseBot
from src.core.timesheet_processor import TimesheetProcessor
from src.utils.helpers import sanitize_filename


class ScaricaTSBot(BaseBot):
    """
    Bot per lo scarico automatico dei timesheet.

    Funzionalità:
    - Login al portale ISAB
    - Navigazione a Report -> Timesheet
    - Selezione fornitore (da configurazione)
    - Impostazione data iniziale
    - Ricerca per Numero OdA / Posizione OdA
    - Download del file Excel
    - Rinomina file scaricato
    - Logout e chiusura browser
    """

    @staticmethod
    def get_name() -> str:
        return "Scarico TS"

    @staticmethod
    def get_description() -> str:
        return "Scarica i timesheet dal portale ISAB"

    @staticmethod
    def get_columns() -> list:
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

    def validate_data(self, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Validazione specifica per Scarico TS."""
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            return False, base_msg

        if not self.fornitore:
            # Prova a prenderlo dai dati
            if isinstance(data, dict) and not data.get("fornitore"):
                return False, "Fornitore non specificato."
            elif isinstance(data, list):
                return False, "Fornitore non specificato."

        rows = data if isinstance(data, list) else data.get("rows", [])
        if not rows:
            return False, "Nessun OdA da scaricare."

        return True, ""

    def run(self, data: List[Dict[str, Any]]) -> bool:
        """Esegue il download dei timesheet."""
        rows, dest_dir = self._prepare_run_environment(data)

        try:
            if not self._navigate_to_timesheet() or not self._setup_filters():
                return False

            success_count, downloaded_files = self._process_oda_rows(rows, dest_dir)

            self.log(f"✨ Download completati: {success_count}/{len(rows)}.")

            if self.elabora_ts and downloaded_files:
                self._run_vba_processing(downloaded_files, dest_dir)

            return success_count == len(rows)

        except Exception as e:
            self.log(f"❌ Errore imprevisto: {e}")
            return False

    def _prepare_run_environment(self, data: Any) -> Tuple[List[Dict], Path]:
        """Estrae i dati e prepara la directory di destinazione."""
        if isinstance(data, dict):
            rows = data.get("rows", [])
            self.data_da = data.get("data_da", self.data_da)
            forn = data.get("fornitore")
            if forn:
                self.fornitore = str(forn)
            self.elabora_ts = data.get("elabora_ts", self.elabora_ts)
        else:
            rows = data

        self.log(f"🚀 Inizio scarico TS per {len(rows)} OdA (Fornitore: {self.fornitore})...")

        source_dir = Path.home() / "Downloads"
        dest_dir = Path(self.download_path) if self.download_path else source_dir
        return rows, dest_dir

    def _process_oda_rows(self, rows: List[Dict], dest_dir: Path) -> Tuple[int, List[str]]:
        """Cicla sugli OdA ed esegue la ricerca e il download."""
        success_count = 0
        downloaded_files = []
        source_dir = Path.home() / "Downloads"

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
        assert self.wait and self.driver

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
        self.driver.execute_script("arguments[0].value = ''; arguments[0].value = arguments[1];", campo_pos, posizione_oda)
        self.driver.execute_script(js_dispatch, campo_pos)

        # Click Cerca
        xpath_cerca = "//a[contains(@class, 'x-btn')][.//span[normalize-space(text())='Cerca']]"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cerca))).click()

        self._attendi_scomparsa_overlay(90)
        return True

    def _run_vba_processing(self, file_list: List[str], dest_dir: Path):
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
        assert self.wait
        self._check_stop()

        try:
            # Click su "Report"
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[normalize-space(text())='Report']")
                )
            ).click()
            self._attendi_scomparsa_overlay()

            # Click su "Timesheet"
            timesheet_menu_xpath = "//span[contains(@id, 'generic_menu_button-') and contains(@id, '-btnEl')][.//span[text()='Timesheet']]"
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, timesheet_menu_xpath))
            ).click()

            # Attendi che il dropdown Fornitore sia visibile
            fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, fornitore_arrow_xpath))
            )
            self._attendi_scomparsa_overlay()

            return True

        except Exception as e:
            self.log(f"❌ Impossibile navigare al menu Timesheet: {e}")
            return False

    def _setup_filters(self) -> bool:
        """Imposta Fornitore e Data Da."""
        if not self.driver or not self.wait or not self.long_wait:
            return False
        assert self.driver and self.wait and self.long_wait
        self._check_stop()

        try:
            # Seleziona Fornitore
            fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"
            fornitore_arrow_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, fornitore_arrow_xpath))
            )
            ActionChains(self.driver).move_to_element(
                fornitore_arrow_element
            ).click().perform()

            # Seleziona l'opzione fornitore
            fornitore_option_xpath = f"//li[normalize-space(text())='{self.fornitore}']"
            fornitore_option = self.long_wait.until(
                EC.presence_of_element_located((By.XPATH, fornitore_option_xpath))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'nearest'});", fornitore_option
            )
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", fornitore_option)

            self._attendi_scomparsa_overlay()

            # Inserisci Data Da
            campo_data_da = self.wait.until(
                EC.visibility_of_element_located((By.NAME, "DataTimesheetDa"))
            )
            campo_data_da.clear()
            campo_data_da.send_keys(self.data_da)

            return True

        except Exception as e:
            self.log(f"❌ Errore nell'impostazione dei filtri: {e}")
            return False

    def _download_excel(
        self, source_dir: Path, dest_dir: Path, numero_oda: str, posizione_oda: str
    ) -> Optional[Path]:
        """Scarica il file Excel, lo rinomina e lo sposta."""
        if not self.wait or not self.driver:
            return None
        assert self.wait and self.driver

        try:
            files_before = {f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() == ".xlsx"}

            # 1. Clicca tasto Excel
            if not self._click_excel_export_button():
                return None

            # 2. Attendi download
            downloaded_file = self._wait_for_new_file(source_dir, files_before)
            if not downloaded_file or not downloaded_file.exists():
                self.log("⚠️ File non trovato dopo il download.")
                return None

            # 3. Determina nome e destinazione
            final_path = self._get_final_download_path(source_dir, dest_dir, numero_oda, posizione_oda)

            # 4. Sposta/Rinomina
            return self._move_to_destination(downloaded_file, final_path)

        except Exception as e:
            self.log(f"❌ Problema durante il download: {e}")
            return None

    def _click_excel_export_button(self) -> bool:
        """Individua e clicca il pulsante di esportazione Excel."""
        if not self.wait:
            return False
        assert self.wait
        xpath = "//div[contains(@class, 'x-tool') and @role='button'][.//div[@data-ref='toolEl' and contains(@class, 'x-tool-tool-el') and contains(@style, 'FontAwesome')]]"
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            return True
        except Exception as e:
            self.log(f"⚠️ Impossibile cliccare esportazione Excel: {e}")
            return False

    def _wait_for_new_file(self, source_dir: Path, files_before: set, timeout: int = 25) -> Optional[Path]:
        """Attende la comparsa di un nuovo file .xlsx nella directory sorgente."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Se c'è un download in corso, attendi
                if any(f.suffix == ".crdownload" for f in source_dir.iterdir()):
                    time.sleep(0.5)
                    continue

                current_files = {f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() == ".xlsx"}
                new_files = current_files - files_before
                if new_files:
                    return max(list(new_files), key=lambda f: f.stat().st_mtime)
            except Exception:
                pass
            time.sleep(0.5)
        return None

    def _get_final_download_path(self, source_dir: Path, dest_dir: Path, oda: str, pos: str) -> Path:
        """Costruisce il percorso finale basato su ODA/POS e impostazione elabora_ts."""
        safe_oda = sanitize_filename(oda)
        safe_pos = sanitize_filename(pos)

        base_name = f"TS_{safe_oda}-{safe_pos}" if safe_pos and safe_pos != "unnamed_file" else f"TS_{safe_oda}"
        filename = f"{base_name}.xlsx"

        # Se elabora_ts, il file resta in temp (Downloads) rinominato
        target_dir = source_dir if self.elabora_ts else dest_dir
        final_path = target_dir / filename

        if final_path.exists():
            try:
                final_path.unlink()
            except Exception:
                # Fallback con timestamp se file bloccato
                ts = time.strftime("%Y%m%d-%H%M%S")
                final_path = target_dir / f"{base_name}_{ts}.xlsx"

        return final_path

    def _move_to_destination(self, src: Path, dest: Path) -> Optional[Path]:
        """Sposta il file scaricato nella posizione finale con retry logic."""
        import shutil

        # Assicura directory esistente
        dest.parent.mkdir(parents=True, exist_ok=True)

        for attempt in range(3):
            try:
                shutil.move(str(src), str(dest))
                self.log(f"✅ Scaricato: {dest.name}")
                return dest
            except Exception as e:
                self.log(f"⚠️ Tentativo spostamento {attempt+1}/3 fallito: {e}")
                time.sleep(2)

        self.log(f"❌ Impossibile spostare il file in: {dest}")
        return None

    def _process_downloaded_files_vba_style(self, files: List[str], dest_dir: Path):
        """
        Implementa la logica VBA: sposta file e chiede all'utente in caso di conflitto.
        """
        import shutil

        if not dest_dir.exists():
            self.log(f"  Creazione cartella destinazione: {dest_dir}")
            dest_dir.mkdir(parents=True, exist_ok=True)

        for file_path_str in files:
            self._check_stop()
            src_file = Path(file_path_str)
            if not src_file.exists():
                continue

            # Nome file base (es TS_12345.xlsx)
            filename = src_file.name
            dest_file = dest_dir / filename

            base_name = src_file.stem
            extension = src_file.suffix

            # Loop finché c'è conflitto
            while dest_file.exists():
                self.log(f"⚠ Conflitto: '{filename}' esiste già.")

                prompt = (
                    f"ATTENZIONE: Il file '{filename}' esiste già.\n\n"
                    f"Per rinominare e spostare, inserisci un testo da aggiungere al nome originale ('{base_name}').\n\n"
                    "Per SALTARE questo file, premi Annulla o lascia il campo vuoto."
                )

                # Chiedi all'utente (tramite callback GUI)
                suffix = self._ask_user(prompt)

                if not suffix or not suffix.strip():
                    self.log(f"⏭️ File '{filename}' saltato dall'utente.")
                    break  # Break loop, dest_file esiste ancora, quindi if sotto fallirà

                # Nuovo tentativo
                new_filename = f"{base_name} {suffix}{extension}"
                dest_file = dest_dir / new_filename
                filename = new_filename

            # Se non esiste (conflitto risolto o non c'era), sposta
            if not dest_file.exists():
                try:
                    shutil.move(str(src_file), str(dest_file))
                    self.log(f"✓ Spostato: {src_file.name} -> {dest_file.name}")
                except Exception as e:
                    self.log(f"✗ Errore spostamento {src_file.name}: {e}")
            else:
                # Caso saltato: cancelliamo il temp?
                # Sì, per pulizia.
                try:
                    src_file.unlink()
                    self.log("  (Temp eliminato)")
                except Exception:
                    pass
