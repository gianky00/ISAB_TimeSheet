# mypy: disable-error-code="no-untyped-call"
"""
SyncroJob - SafeWork PDL Download Bot
Bot modulare per lo scarico e la stampa dei PDL.
"""

import contextlib
import logging
import time
from contextlib import suppress
from pathlib import Path
from typing import Any, ClassVar

import fitz
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.base.base_bot import StepStatus
from src.bots.safework.base import SafeworkBaseBot
from src.utils.printing import print_pdf

logger = logging.getLogger(__name__)


class SafeWorkPDLBot(SafeworkBaseBot):
    """Bot per lo scarico e la stampa automatizzata dei PDL."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login SafeWork"),
        ("search", "Ricerca PdL"),
        ("download_p1", "Scarico Parte Prima"),
        ("download_p2", "Scarico Parte Seconda"),
        ("merge", "Unione e Stampa"),
        ("session", "Chiusura Sessione"),
    ]

    def __init__(  # noqa: PLR0913
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = 30,
        download_path: str = "",
        account_type: str = "Esecutore",
    ) -> None:
        """Inizializza il bot SafeWork PDL."""
        super().__init__(username, password, headless, timeout, download_path, account_type=account_type)
        self.downloaded_files: list[str] = []
        self.missing_pdls: list[str] = []

    @staticmethod
    def get_name() -> str:
        """Restituisce il nome visualizzato del bot."""
        return "Scarico PDL"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Definisce le colonne richieste per l'input dati del bot."""
        return [{"name": "numero_pdl", "label": "Numero PDL", "type": "text"}]

    @property
    def name(self) -> str:
        """Restituisce l'ID univoco del bot."""
        return "scarico_pdl"

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Validazione specifica per SafeWork PDL."""
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            return False, base_msg

        rows = data.get("rows", []) if isinstance(data, dict) else data
        if not rows:
            return False, "Nessun dato da elaborare."

        found_pdl = False
        for _i, item in enumerate(rows):
            if item.get("numero_pdl"):
                found_pdl = True
                break

        if not found_pdl:
            return False, "Nessun numero PDL trovato nei dati."

        return True, ""

    def run(self, data: list[dict[str, Any]]) -> bool:  # noqa: PLR0912, PLR0915
        """Ciclo principale di scarico PDL con gestione sessione."""
        self.update_step("login", StepStatus.COMPLETED)

        success_count = 0
        total = len(data)
        self.downloaded_files = []
        all_pdl_paths: list[str] = []

        self.log(f"🚀 Inizio elaborazione di {total} PDL...")

        for index, item in enumerate(data):
            pdl_raw = "N/A"
            try:
                self._check_stop()
                val = item.get("numero_pdl")
                pdl_raw = str(val) if val else "N/A"
                if not pdl_raw:
                    continue

                pdl_num = self._sanitizza_pdl_number(pdl_raw)
                self.log(f"📋 PDL {index + 1}/{total}: {pdl_num}")

                # Pipeline per singolo PDL
                self.update_step("search", StepStatus.RUNNING)
                if self._esegui_ricerca_pdl(pdl_num):
                    self.update_step("search", StepStatus.COMPLETED)

                    self.update_step("download_p1", StepStatus.RUNNING)
                    path_p1 = self._scarica_parte_prima(pdl_num)

                    path_p2 = None
                    if path_p1:
                        self.update_step("download_p1", StepStatus.COMPLETED)
                        self.update_step("download_p2", StepStatus.RUNNING)
                        path_p2 = self._scarica_parte_seconda(pdl_num)

                    if path_p1 and path_p2:
                        self.update_step("download_p2", StepStatus.COMPLETED)
                        self.update_step("merge", StepStatus.RUNNING)
                        if self._unisci_e_stampa(pdl_num, path_p1, path_p2, item, all_pdl_paths):
                            self.update_step("merge", StepStatus.COMPLETED)
                            success_count += 1
                        else:
                            self.update_step("merge", StepStatus.ERROR)
                    else:
                        if not path_p1:
                            self.update_step("download_p1", StepStatus.ERROR)
                        if not path_p2:
                            self.update_step("download_p2", StepStatus.ERROR)

                    self._safe_remove(path_p1)
                    self._safe_remove(path_p2)
                else:
                    self.update_step("search", StepStatus.ERROR)

                # Notifica progresso alla GUI (index, success, message)
                callback = getattr(self, "_progress_callback", None)
                if callback:
                    callback(index, True, "")
            except InterruptedError:
                raise
            except Exception as e:
                self.log(f"❌ Errore critico PDL {pdl_raw}: {e}")
                # Notifica errore alla GUI
                callback = getattr(self, "_progress_callback", None)
                if callback:
                    callback(index, False, str(e))

        # Unione finale di sessione se richiesto
        self.update_step("session", StepStatus.RUNNING)
        self._handle_session_merge(data, all_pdl_paths)
        self.update_step("session", StepStatus.COMPLETED)

        self.log(f"✨ Completato: {success_count}/{total} PDL.")
        return success_count == total

    def _sanitizza_pdl_number(self, pdl_raw: Any) -> str:
        """Formatta il numero PDL aggiungendo i suffissi /S o /C se necessario."""
        num = str(pdl_raw).strip().upper().replace(" ", "")
        if num.isdigit() and len(num) == 6:  # noqa: PLR2004
            suffix = "/S" if int(num) < 400000 else "/C"  # noqa: PLR2004
            return f"{num}{suffix}"
        return num

    def _esegui_ricerca_pdl(self, pdl_num: str) -> bool:
        """Esegue la ricerca del PDL e gestisce i vari popup di errore/estensione."""
        if not self.wait or not self.driver:
            return False

        try:
            from src.bots.safework.common.locators import SafeWorkLocators  # noqa: PLC0415

            # CRITICAL: Assicurarsi che l'overlay di caricamento sia sparito
            self._attendi_scomparsa_overlay(timeout_secondi=10)

            campo = self.wait.until(EC.element_to_be_clickable(SafeWorkLocators.RICERCA_VELOCE_PDL))
            self.log(f"⌨️ Inserimento numero PdL {pdl_num}...")
            campo.clear()
            campo.send_keys(pdl_num + Keys.ENTER)
        except Exception as e:
            self.log(f"❌ Campo ricerca veloce non trovato o non interagibile: {e}", "ERROR")
            return False

        if self._gestisci_ricerca_estesa():
            self.log(f"ℹ️ PdL {pdl_num} inesistente. Salto.")
            return False

        if self._gestisci_alert_ricerca():
            with contextlib.suppress(Exception):
                self._attendi_scomparsa_overlay(timeout_secondi=5)
        else:
            self._attendi_scomparsa_overlay()

        # Verifica finale caricamento (indipendente da alert)
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, "topIcon-acticonAnteprimaStampaMenu")))
            self._attendi_scomparsa_overlay(timeout_secondi=4)
            self.log(f"✅ PdL {pdl_num} caricato correttamente.")
            return True  # noqa: TRY300
        except Exception as e:
            self.log(f"❌ PDL {pdl_num} non caricato correttamente: {e}", "ERROR")
            return False

    def _scarica_parte_prima(self, pdl_num: str) -> str | None:
        """Scarica la parte prima del PDL con attese robuste e pulizia preventiva."""
        from src.bots.base.wait_helpers import poll_for_new_file  # noqa: PLC0415

        if not self.driver or not self.wait:
            return None

        # Gestione popup in differita (es. 'Si') che bloccano il menu stampa
        self._attendi_scomparsa_overlay(timeout_secondi=5)

        try:
            self.driver.execute_script("window.scrollTo(0, 0);")

            # Pulizia preventiva
            clean_name = pdl_num.replace("/", "") + ".pdf"
            target_path = Path(self.download_path) / clean_name
            self._safe_remove(str(target_path))

            ts = time.time()
            files_before = {str(f.resolve()) for f in Path(self.download_path).glob("*.pdf")}

            # Clicca su Anteprima Stampa usando click_robusto
            self.click_robusto((By.ID, "topIcon-acticonAnteprimaStampaMenu"), label="'Anteprima Stampa'")
            time.sleep(0.8)  # Breve pausa per animazione menu
            self.click_robusto((By.ID, "appItaliano"), label="'Lingua Italiano'")

            # Cerchiamo il file
            self.log(f"⏳ Polling per file PDF di {pdl_num}...")
            f = poll_for_new_file(self.download_path, files_before, pattern="*.pdf", timeout=60)
            if f:
                dest = Path(self.download_path) / f"temp_p1_{int(ts)}.pdf"
                Path(f).rename(dest)
                self._clean_pdf(str(dest))
                return str(dest)
            self.log("❌ Timeout: nessun PDF generato per la Parte Prima.", "ERROR")
        except Exception as e:
            self.log(f"❌ Errore scarico Parte Prima: {e}", "ERROR")
            logger.exception("Dettaglio crash Parte Prima:")
        return None

    def _scarica_parte_seconda(self, pdl_num: str) -> str | None:
        """Gestisce il download della Parte Seconda con pulizia preventiva."""
        from src.bots.base.wait_helpers import poll_for_new_file  # noqa: PLC0415

        if not self.driver or not self.wait:
            return None

        if not self._espandi_parte_seconda():
            self.log(f"❌ Impossibile espandere la sezione Parte Seconda per {pdl_num}.", "ERROR")
            return None

        self._attendi_scomparsa_overlay()

        try:
            self.driver.execute_script("window.scrollTo(0, 0);")

            # Pulizia preventiva
            self._safe_remove(str(Path(self.download_path) / "ReportPdLRinnovi.pdf"))

            ts = time.time()
            files_before = {str(f.resolve()) for f in Path(self.download_path).glob("*.pdf")}

            self.click_robusto((By.ID, "btnPrintPS"), label="'Stampa Parte Seconda'")
            self._gestisci_dialogo_stampa_tutte()

            self.log(f"⏳ Polling per file PDF Parte Seconda di {pdl_num}...")
            f = poll_for_new_file(self.download_path, files_before, pattern="*.pdf", timeout=90)
            if f:
                dest = Path(self.download_path) / f"temp_p2_{int(ts)}.pdf"
                Path(f).rename(dest)
                return str(dest)
            self.log("❌ Timeout: nessun PDF generato per la Parte Seconda.", "ERROR")
        except Exception as e:
            self.log(f"❌ Errore scarico Parte Seconda: {e}", "ERROR")
            logger.exception("Dettaglio crash Parte Seconda:")
        return None

    def _espandi_parte_seconda(self) -> bool:
        """Tenta di rendere visibile la sezione Parte Seconda con strategie multiple."""
        if not self.driver or not self.wait:
            return False

        self._attendi_scomparsa_overlay()

        try:
            # Verifica visibilità senza lanciare eccezioni se l'elemento non esiste ancora
            elementi = self.driver.find_elements(By.ID, "lblPAFoglio")
            if not elementi or not elementi[0].is_displayed():
                self.log("📂 Espansione sezione 'Parte Seconda'...")
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
            return True  # noqa: TRY300
        except Exception as e:
            self.log(f"⚠️ Errore apertura Parte Seconda: {e}")
            return False

    def _gestisci_ricerca_estesa(self) -> bool:
        """Gestisce il popup 'La ricerca veloce... estenderla?'."""
        if not self.driver:
            return False
        try:
            # Aumentato timeout a 10s per reattività SafeWork
            try:
                self.log("🔍 Controllo presenza popup 'Ricerca Estesa'...")
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'estenderla')]"))
                )
            except Exception:
                # Fallback idtxt
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "p[idtxt='1C51D77B']")
                    self.log("ℹ️ Popup 'Ricerca Estesa' rilevato via idtxt.")
                except Exception:
                    self.log("ℹ️ Nessun popup di ricerca estesa rilevato.")
                    return False

            # Click robusto su 'Si' (cerca span o button con classe btn-ok)
            clicked = False
            self.log("🖱️ Tentativo click su 'Si' per estensione ricerca...")
            for selector in (
                "span[idtxt='E421C594']",
                "//button[contains(@class, 'btn-ok') and contains(., 'Si')]",
                "//button[contains(., 'Si')]",
            ):
                try:
                    by = By.XPATH if selector.startswith("/") else By.CSS_SELECTOR
                    el = self.driver.find_element(by, selector)
                    el.click()
                    self.log(f"✅ Click su 'Si' riuscito (selector: {selector})")
                    clicked = True
                    break
                except Exception as e:
                    # Strategia di click multipla: ignoriamo l'errore e proviamo il selettore successivo
                    self.log(f"DEBUG: Fallito click su {selector}: {e}")
                    continue

            if clicked:
                self.log("✅ Ricerca PdL estesa agli altri siti.")
                self._attendi_scomparsa_overlay()
            else:
                self.log("⚠️ Popup ricerca estesa rilevato ma impossibile cliccare 'Si'.", "WARNING")

            # Verifica Risultati (se 0, PdL inesistente)
            with suppress(Exception):
                self.log("🔍 Verifica se PdL inesistente dopo estensione...")
                msg = self.driver.find_element(By.XPATH, "//div[contains(text(), 'nessun dato trovato')]")
                if msg.is_displayed():
                    self.log("ℹ️ PdL non trovato nemmeno con ricerca estesa.")
                    return True
            # Se siamo finiti direttamente nella pagina dettaglio, numPermessiTrovati non ci sarà
            with suppress(Exception):
                num_res_el = self.driver.find_elements(By.ID, "numPermessiTrovati")
                if num_res_el:
                    num_res = num_res_el[0].text.strip()
                    return bool(num_res == "0")

            return False  # Proseguiamo comunque, la verifica finale la fa _esegui_ricerca_pdl  # noqa: TRY300
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

    def _gestisci_dialogo_stampa_tutte(self) -> None:
        """Seleziona 'Stampa Tutte' nel popup se appare."""
        if not self.driver or not self.wait:
            return
        with contextlib.suppress(Exception):
            btn_tutte = self.wait.until(EC.element_to_be_clickable((By.ID, "rbStampaTutte")))
            btn_tutte.click()
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnAnteprima"))).click()

    def _clean_pdf(self, path: str) -> None:
        """Rimuove la pagina 2 (istruzioni) dal PDF della parte prima."""
        try:
            doc = fitz.open(path)
            if doc.page_count >= 2:  # noqa: PLR2004
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

                from src.utils.document_processor import DocumentProcessor  # noqa: PLC0415

                if DocumentProcessor.merge_pdfs(all_paths, str(path_merge)):
                    self.log(f"✅ PDF Unico Sessione creato: {path_merge.name}")
                    self.downloaded_files.append(str(path_merge))
            except Exception as e:
                logger.error("Errore unione sessione: %s", e)  # noqa: TRY400

    def _unisci_e_stampa(
        self, pdl_num: str, p1: str, p2: str, item: dict[str, Any], all_paths: list[str]
    ) -> bool:
        """Esegue il merge delle due parti e l'eventuale stampa."""
        from src.utils.document_processor import DocumentProcessor  # noqa: PLC0415

        nome = f"PDL_{pdl_num.replace('/', '-')}.pdf"
        out = Path(self.download_path) / nome
        if DocumentProcessor.merge_pdfs([p1, p2], str(out)):
            self.downloaded_files.append(str(out))
            all_paths.append(str(out))  # Aggiunto per il merge sessione
            if item.get("print_enabled") and item.get("printer_name"):
                print_pdf(str(out), item["printer_name"])
            return True
        return False

    def _safe_remove(self, path: str | None) -> None:
        """Rimuove un file dal filesystem in modo sicuro, ignorando errori se non esiste."""
        if path and Path(path).exists():
            with contextlib.suppress(Exception):
                Path(path).unlink()
