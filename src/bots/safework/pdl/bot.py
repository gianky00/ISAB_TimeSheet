"""
SyncroJob - SafeWork PDL Download Bot
Bot modulare per lo scarico e la stampa dei PDL.
"""

import contextlib
import logging
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

import fitz
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.base import SafeworkBaseBot
from src.utils.printing import print_pdf

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


class SafeWorkPDLBot(SafeworkBaseBot):
    """Bot per lo scarico e la stampa automatizzata dei PDL."""

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        self.downloaded_files: list[str] = []
        self.missing_pdls: list[str] = []
        self.progress_callback: Callable[[int, bool], None] | None = None

    @staticmethod
    def get_name() -> str:
        return "Scarico PDL"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return [{"name": "Numero PDL", "type": "text"}]

    @property
    def name(self) -> str:
        return "scarico_pdl"

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Validazione specifica per SafeWork PDL."""
        self.log("🔍 Avvio validazione dati...")
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            return False, base_msg

        rows = data.get("rows", []) if isinstance(data, dict) else data
        if not rows:
            return False, "Nessun dato da elaborare."

        found_pdl = False
        for _i, item in enumerate(rows):
            if item.get("pdl_number") or item.get("numero_pdl"):
                found_pdl = True
                break

        if not found_pdl:
            return False, "Nessun numero PDL trovato nei dati."

        return True, ""

    def set_progress_callback(self, callback):
        self.progress_callback = callback

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Ciclo principale di scarico PDL con gestione sessione."""
        success_count = 0
        total = len(data)
        self.downloaded_files = []
        all_pdl_paths: list[str] = []

        self.log(f"🚀 Inizio scarico di {total} PDL...")

        for index, item in enumerate(data):
            try:
                self._check_stop()
                pdl_raw = item.get("pdl_number") or item.get("numero_pdl")
                if not pdl_raw:
                    continue

                pdl_num = self._sanitizza_pdl_number(pdl_raw)
                self.log(f"--- PDL {index + 1}/{total}: {pdl_num} ---")

                # Pipeline per singolo PDL
                if self._esegui_ricerca_pdl(pdl_num):
                    path_p1 = self._scarica_parte_prima(pdl_num)
                    path_p2 = self._scarica_parte_seconda(pdl_num)

                    if (
                        path_p1
                        and path_p2
                        and self._unisci_e_stampa(pdl_num, path_p1, path_p2, item, all_pdl_paths)
                    ):
                        success_count += 1

                    self._safe_remove(path_p1)
                    self._safe_remove(path_p2)

                if self.progress_callback:
                    self.progress_callback(index, True)
            except InterruptedError:
                raise
            except Exception as e:
                self.log(f"❌ Errore critico PDL {pdl_raw}: {e}")

        # Unione finale di sessione se richiesto
        self._handle_session_merge(data, all_pdl_paths)

        self.log(f"✨ Completato: {success_count}/{total} PDL.")
        return success_count == total

    def _sanitizza_pdl_number(self, pdl_raw: Any) -> str:
        """Formatta il numero PDL aggiungendo i suffissi /S o /C se necessario."""
        num = str(pdl_raw).strip().upper().replace(" ", "")
        if num.isdigit() and len(num) == 6:
            suffix = "/S" if int(num) < 400000 else "/C"
            return f"{num}{suffix}"
        return num

    def _esegui_ricerca_pdl(self, pdl_num: str) -> bool:
        """Esegue la ricerca del PDL e gestisce i vari popup di errore/estensione."""
        if not self.wait or not self.driver:
            return False

        self.log(f"🔄 Ricerca PdL {pdl_num} in interfaccia...")
        try:
            campo = self.wait.until(EC.visibility_of_element_located((By.ID, "fldRicercaPdLVeloce")))
            campo.clear()
            campo.send_keys(pdl_num + Keys.ENTER)
        except Exception:
            return False

        if self._gestisci_ricerca_estesa():
            self.log(f"ℹ️ PdL {pdl_num} inesistente. Salto.")
            return False

        if self._gestisci_alert_ricerca():
            self.log(f"⚠️ Rilevato alert per {pdl_num}. Proseguo con attesa resiliente...")
            with contextlib.suppress(Exception):
                self._attendi_scomparsa_overlay(timeout_secondi=5)

            # Verifica se caricato nonostante l'alert
            try:
                self.wait.until(EC.presence_of_element_located((By.ID, "topIcon-acticonAnteprimaStampaMenu")))
            except Exception:
                self.log(f"❌ PDL {pdl_num} non caricato dopo alert. Salto.")
                return False
        else:
            self._attendi_scomparsa_overlay()

        return True

    def _scarica_parte_prima(self, pdl_num: str) -> str | None:
        """Scarica la parte prima del PDL con attese robuste e pulizia preventiva."""
        from src.bots.base.wait_helpers import poll_for_new_file

        if not self.driver or not self.wait:
            return None

        self.log(f"⬇️ Avvio scarico Parte Prima per PdL {pdl_num}...")
        self._attendi_scomparsa_overlay()
        self.driver.execute_script("window.scrollTo(0, 0);")

        # Pulizia preventiva: SafeWork scarica la parte 1 col nome del PDL (es. 566360C.pdf)
        clean_name = pdl_num.replace("/", "") + ".pdf"
        target_path = Path(self.download_path) / clean_name
        self._safe_remove(str(target_path))

        ts = time.time()
        files_before = {str(f.resolve()) for f in Path(self.download_path).glob("*.pdf")}

        try:
            # Clicca su Anteprima Stampa
            self.wait.until(EC.element_to_be_clickable((By.ID, "topIcon-acticonAnteprimaStampaMenu"))).click()
            time.sleep(0.5)
            self.wait.until(EC.element_to_be_clickable((By.ID, "appItaliano"))).click()

            # Cerchiamo il file
            f = poll_for_new_file(self.download_path, files_before, pattern="*.pdf", timeout=60)
            if f:
                dest = Path(self.download_path) / f"temp_p1_{int(ts)}.pdf"
                Path(f).rename(dest)
                self._clean_pdf(str(dest))
                return str(dest)
        except Exception:
            logger.debug("Impossibile scaricare la parte prima del PDL.")
        return None

    def _scarica_parte_seconda(self, pdl_num: str) -> str | None:
        """Gestisce il download della Parte Seconda con pulizia preventiva."""
        from src.bots.base.wait_helpers import poll_for_new_file

        if not self.driver or not self.wait:
            return None

        # Assicura che la "Parte Seconda" sia espansa/visibile
        if not self._espandi_parte_seconda():
            return None

        self.log(f"⬇️ Avvio scarico Parte Seconda per PdL {pdl_num}...")
        self._attendi_scomparsa_overlay()
        self.driver.execute_script("window.scrollTo(0, 0);")

        # Pulizia preventiva: SafeWork usa spesso questo nome fisso per la parte 2
        self._safe_remove(str(Path(self.download_path) / "ReportPdLRinnovi.pdf"))

        ts = time.time()
        files_before = {str(f.resolve()) for f in Path(self.download_path).glob("*.pdf")}

        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnPrintPS"))).click()
            self._gestisci_dialogo_stampa_tutte()
        except Exception:
            return None

        f = poll_for_new_file(self.download_path, files_before, pattern="*.pdf", timeout=90)
        if f:
            dest = Path(self.download_path) / f"temp_p2_{int(ts)}.pdf"
            Path(f).rename(dest)
            return str(dest)
        return None

    def _espandi_parte_seconda(self) -> bool:
        """Tenta di rendere visibile la sezione Parte Seconda con strategie multiple."""
        if not self.driver or not self.wait:
            return False
        try:
            if not self.driver.find_element(By.ID, "lblPAFoglio").is_displayed():
                self.log("📂 Tentativo espansione accordion 'Parte Seconda'...")
                clicked = False

                # Strategia 1: ID Label
                with contextlib.suppress(Exception):
                    self.driver.find_element(By.ID, "lblTitoloParteSeconda").click()
                    clicked = True

                # Strategia 2: Testo XPATH
                if not clicked:
                    with contextlib.suppress(Exception):
                        self.driver.find_element(
                            By.XPATH, "//span[contains(text(), 'PARTE SECONDA')]"
                        ).click()
                        clicked = True

                # Strategia 3: User Specific IDTXT
                if not clicked:
                    with contextlib.suppress(Exception):
                        self.driver.find_element(By.CSS_SELECTOR, "span[idtxt='2E20B56F']").click()
                        clicked = True

            # Attesa conferma visibilità
            self.wait.until(EC.visibility_of_element_located((By.ID, "lblPAFoglio")))
            return True
        except Exception as e:
            self.log(f"⚠️ Errore apertura Parte Seconda: {e}")
            return False

    def _gestisci_ricerca_estesa(self) -> bool:
        """Gestisce il popup 'La ricerca veloce... estenderla?'."""
        if not self.driver:
            return False
        try:
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "p[idtxt='1C51D77B']"))
                )
            except Exception:
                return False

            # Clicca su Si
            self.driver.find_element(By.CSS_SELECTOR, "span[idtxt='E421C594']").click()
            self._attendi_scomparsa_overlay()

            # Verifica Risultati (se 0, PdL inesistente)
            num_res = self.driver.find_element(By.ID, "numPermessiTrovati").text.strip()
            return num_res == "0"
        except Exception:
            return False

    def _gestisci_alert_ricerca(self) -> bool:
        """Chiude popup informativi che bloccano l'interfaccia."""
        if not self.driver:
            return False
        with contextlib.suppress(Exception):
            btn_ok = self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn dialog-btn btn-ok')]")
            if btn_ok.is_displayed():
                btn_ok.click()
                # Attendi chiusura effettiva modal
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located(
                        (By.XPATH, "//div[contains(@class, 'modal') and contains(@class, 'in')]")
                    )
                )
                return True
        return False

    def _gestisci_dialogo_stampa_tutte(self):
        """Seleziona 'Stampa Tutte' nel popup se appare."""
        if not self.driver or not self.wait:
            return
        with contextlib.suppress(Exception):
            btn_tutte = self.wait.until(EC.element_to_be_clickable((By.ID, "rbStampaTutte")))
            btn_tutte.click()
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnAnteprima"))).click()

    def _clean_pdf(self, path: str):
        """Rimuove la pagina 2 (istruzioni) dal PDF della parte prima."""
        try:
            doc = fitz.open(path)
            if doc.page_count >= 2:
                doc.delete_page(1)
                doc.save(path + ".tmp")
                doc.close()
                Path(path).unlink()
                Path(path + ".tmp").rename(path)
            else:
                doc.close()
        except Exception as e:
            logger.debug("Errore pulizia PDF: %s", e)

    def _handle_session_merge(self, data: list[dict[str, Any]], all_paths: list[str]) -> None:
        """Crea un unico PDF con tutti i PDL della sessione se configurato."""
        if any(i.get("merge_all_session") for i in data) and all_paths:
            try:
                self.log(f"🔗 Unione sessione ({len(all_paths)} PDL)...")
                ts = time.strftime("%d-%m-%Y_%H-%M")
                path_merge = Path(self.download_path) / f"PDL_SESSIONE_{ts}.pdf"

                from src.utils.document_processor import DocumentProcessor

                if DocumentProcessor.merge_pdfs(all_paths, str(path_merge)):
                    self.log(f"✅ PDF Unico Sessione creato: {path_merge.name}")
                    self.downloaded_files.append(str(path_merge))
            except Exception as e:
                logger.error("Errore unione sessione: %s", e)

    def _unisci_e_stampa(
        self, pdl_num: str, p1: str, p2: str, item: dict[str, Any], all_paths: list[str]
    ) -> bool:
        """Esegue il merge delle due parti e l'eventuale stampa."""
        from src.utils.document_processor import DocumentProcessor

        nome = f"PDL_{pdl_num.replace('/', '-')}.pdf"
        out = Path(self.download_path) / nome
        if DocumentProcessor.merge_pdfs([p1, p2], str(out)):
            self.downloaded_files.append(str(out))
            all_paths.append(str(out))  # Aggiunto per il merge sessione
            if item.get("print_enabled") and item.get("printer_name"):
                print_pdf(str(out), item["printer_name"])
            return True
        return False

    def _safe_remove(self, path: str | None):
        if path and Path(path).exists():
            with contextlib.suppress(Exception):
                Path(path).unlink()
