import logging
import os
import time
from contextlib import suppress
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import fitz  # type: ignore # PyMuPDF
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.base import SafeworkBaseBot
from src.utils.printing import print_pdf

logger = logging.getLogger(__name__)


class SafeWorkPDLBot(SafeworkBaseBot):
    """Bot per lo scarico e la stampa automatizzata dei Permessi di Lavoro (PDL) da SafeWork."""

    @staticmethod
    def get_name() -> str:
        """Restituisce il nome del bot."""
        return "Scarico PDL"

    @staticmethod
    def get_description() -> str:
        """Restituisce una descrizione delle funzionalità del bot."""
        return "Scarica e stampa PDL da SafeWork"

    @staticmethod
    def get_columns() -> list:
        """Definisce le colonne richieste per l'input dei dati (Numero PDL)."""
        return [{"name": "Numero PDL", "type": "text"}]

    @property
    def name(self) -> str:
        """Restituisce il nome dell'istanza del bot."""
        return "scarico_pdl"

    @property
    def description(self) -> str:
        """Restituisce la descrizione dell'istanza del bot."""
        return "Scarica e stampa PDL da SafeWork"

    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = 30,
        download_path: str = "",
    ):
        """Inizializza il bot PDL."""
        super().__init__(username, password, headless, timeout, download_path)
        self.merged_pdf_path: Optional[Path] = None
        self.downloaded_files: List[str] = []
        self.missing_pdls: List[str] = []

    def log_error(self, context: str, exception: Exception):
        """Logga un errore dettagliato con stack trace."""
        logger.error(f"❌ ERRORE CRITICO in {context}: {exception}", exc_info=True)

    def validate_data(self, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Validazione specifica per SafeWork PDL."""
        self.log("🔍 Avvio validazione dati...")
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            self.log(f"❌ Validazione base fallita: {base_msg}")
            return False, base_msg

        if not data:
            self.log("❌ Lista dati vuota.")
            return False, "Nessun dato da elaborare."

        # Verifica che almeno una riga abbia un PDL
        found_pdl = False
        for i, item in enumerate(data):
            pdl = item.get("pdl_number") or item.get("numero_pdl")
            if pdl:
                found_pdl = True
                self.log(f"✅ Riga {i + 1}: Trovato PDL {pdl}")
            else:
                self.log(f"⚠️ Riga {i + 1}: PDL mancante")

        if not found_pdl:
            self.log("❌ Nessun numero PDL trovato nei dati forniti.")
            return False, "Nessun numero PDL trovato nei dati forniti."

        self.log("✅ Validazione completata con successo.")
        return True, ""

    def _login(self) -> bool:
        """Login SafeWork ricalcato dall'originale."""
        if not self.driver or not self.wait:
            self.log("❌ Driver o Wait non inizializzati.")
            return False

        self.log("🌐 Navigazione verso l'URL SafeWork...")
        try:
            self.driver.get(self.SAFEWORK_URL)
            self.log(f"📍 URL caricato. Titolo pagina: {self.driver.title}")
        except Exception as e:
            self.log_error("Apertura URL", e)
            return False

        try:
            self.log("⏳ Cerco pulsante selezione sito (ms-choice)...")
            btn_sito = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='ms-choice']"))
            )
            btn_sito.click()
            self.log("🖱️ Menu siti aperto. Cerco 'ISAB Sud'...")

            opzione_isab = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'ms-drop')]//span[normalize-space()='ISAB Sud']",
                    )
                )
            )
            opzione_isab.click()
            self.log("✅ Sito ISAB Sud selezionato.")
        except Exception as e:
            self.log(f"ℹ️ Selezione sito non necessaria o fallita (proseguo): {e}")

        try:
            self.log(f"🔐 Inserimento credenziali per utente: {self.username}")
            u_field = self.wait.until(
                EC.visibility_of_element_located((By.ID, "inpUtente"))
            )
            u_field.clear()
            u_field.send_keys(self.username)
            self.log("⌨️ Username inserito.")

            p_field = self.wait.until(
                EC.visibility_of_element_located((By.ID, "inpPassword"))
            )
            p_field.clear()
            p_field.send_keys(self.password)
            self.log("⌨️ Password inserita.")

            self.log("🖱️ Clic su pulsante Login...")
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnLogin"))).click()
        except Exception as e:
            self.log_error("Inserimento credenziali login", e)
            return False

        self.log("⏳ Attendo il caricamento del sistema (overlay/caricamento)...")
        try:
            self._attendi_caricamento_sistema()
            self.log("✅ Login a Safework completato. Dashboard pronta.")
        except Exception as e:
            self.log_error("Attesa post-login", e)
            return False

        return True

    def _safe_remove(self, path: str | Path):
        """Rimuove un file ignorando errori se in uso."""
        with suppress(Exception):
            p = Path(path)
            if p.exists():
                p.unlink()
                self.log(f"🗑️ Rimosso file temporaneo: {p.name}")

    def run(self, data: List[Dict[str, Any]]) -> bool:
        """Esegue il ciclo principale di scarico PDL."""
        success_count = 0
        total = len(data)
        self.downloaded_files = []
        all_downloaded_pdl_paths: List[str] = []
        self.missing_pdls = []
        self.merged_pdf_path = None

        self.log(f"🚀 Inizio elaborazione di {total} righe di dati.")

        for index, item in enumerate(data):
            try:
                self._check_stop()
                res = self._process_single_pdl_row(
                    index, total, item, all_downloaded_pdl_paths
                )
                if res:
                    success_count += 1
            except InterruptedError:
                self.log("🛑 Stop richiesto dall'utente durante il loop.")
                raise
            except Exception as e:
                self.log_error(f"Processo PDL riga {index + 1}", e)

        # Merge finale di sessione
        self._handle_session_merge(data, all_downloaded_pdl_paths)

        self.log(f"✨ FINE ESECUZIONE: {success_count}/{total} PDL completati.")
        return success_count == total

    def _process_single_pdl_row(self, index, total, item, all_paths) -> bool:
        """Gestisce l'intera pipeline per un singolo PDL."""
        pdl_raw = item.get("pdl_number") or item.get("numero_pdl")
        if not pdl_raw:
            self.log(f"⚠️ PDL non valido o mancante nella riga {index + 1}. Salto.")
            return False

        self.log(f"--- Elaborazione Riga {index + 1}/{total} ---")
        pdl_num = self._sanitizza_pdl_number(pdl_raw)

        # 1. Ricerca
        if not self._esegui_ricerca_pdl(pdl_num):
            return True  # Contato come gestito (mancante)

        # 2. Scarico Parte Prima
        path_p1 = self._scarica_parte_prima(pdl_num)
        if not path_p1:
            return False

        # 3. Scarico Parte Seconda
        path_p2 = self._scarica_parte_seconda(pdl_num)
        if not path_p2:
            self._safe_remove(path_p1)
            return False

        # 4. Unione, Stampa e Tracking
        success = self._unisci_e_stampa_pdl(pdl_num, path_p1, path_p2, item, all_paths)

        # Pulizia temporanei
        self._safe_remove(path_p1)
        self._safe_remove(path_p2)
        return success

    def _sanitizza_pdl_number(self, pdl_raw: Any) -> str:
        """Formatta il numero PDL aggiungendo i suffissi /S o /C se necessario."""
        pdl_num = str(pdl_raw).strip().upper().replace(" ", "")
        if pdl_num.isdigit() and len(pdl_num) == 6:
            num = int(pdl_num)
            suffix = "/S" if num < 400000 else "/C"
            pdl_num = f"{pdl_num}{suffix}"
            self.log(f"ℹ️ PDL auto-completato: {pdl_raw} -> {pdl_num}")
        else:
            self.log(f"ℹ️ PDL già formattato o non standard: {pdl_num}")
        return pdl_num

    def _esegui_ricerca_pdl(self, pdl_num: str) -> bool:
        """Esegue la ricerca del PDL e gestisce i vari popup di errore/estensione."""
        if not self.wait or not self.driver:
            return False
        assert self.wait and self.driver
        self.log(f"🔄 Ricerca PdL {pdl_num} in interfaccia...")
        try:
            campo = self.wait.until(
                EC.visibility_of_element_located((By.ID, "fldRicercaPdLVeloce"))
            )
            campo.clear()
            campo.send_keys(pdl_num)
            # No sleep needed: send_keys is synchronous
            campo.send_keys(Keys.ENTER)
        except Exception as e:
            self.log_error(f"Interazione campo ricerca PDL {pdl_num}", e)
            return False

        if self._gestisci_ricerca_estesa():
            self.log(f"ℹ️ PdL {pdl_num} inesistente. Salto.")
            self.missing_pdls.append(pdl_num)
            return False

        if self._gestisci_alert_ricerca():
            self.log(f"⚠️ Rilevato alert per {pdl_num}. Attesa resiliente...")
            try:
                self._attendi_scomparsa_overlay(timeout_secondi=5)
            except Exception:
                pass
            # Verifica che il PDL sia stato caricato controllando presenza pulsante stampa
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(
                        (By.ID, "topIcon-acticonAnteprimaStampaMenu")
                    )
                )
            except Exception:
                self.log(f"❌ PDL {pdl_num} non caricato dopo alert. Salto.")
                self.missing_pdls.append(pdl_num)
                return False
        else:
            self._attendi_scomparsa_overlay()

        return True

    def _scarica_parte_prima(self, pdl_num: str) -> Optional[str]:
        """Gestisce il download e la pulizia (rimozione pag 2) della Parte Prima."""
        if not self.driver or not self.wait:
            return None
        assert self.driver and self.wait
        self.log(f"⬇️ Avvio scarico Parte Prima per PdL {pdl_num}...")
        self.driver.execute_script("window.scrollTo(0, 0);")
        # No sleep needed: scroll is synchronous
        ts = time.time()

        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "topIcon-acticonAnteprimaStampaMenu")
                )
            ).click()
            # No sleep needed: wait esplicito su appItaliano
            self.wait.until(EC.element_to_be_clickable((By.ID, "appItaliano"))).click()
        except Exception as e:
            self.log_error(f"Click stampa Parte 1 PDL {pdl_num}", e)
            return None

        pdf_path = self._attendi_e_ritorna_nuovo_pdf(ts)
        if not pdf_path:
            return None

        # Rinomina e Pulizia Pagine
        temp_path = os.path.join(self.download_path, f"temp_p1_{int(ts)}.pdf")
        try:
            os.rename(pdf_path, temp_path)
            self._clean_p1_pdf(temp_path)
            return temp_path
        except Exception as e:
            self.log(f"⚠️ Errore post-download Parte 1: {e}")
            return pdf_path

    def _clean_p1_pdf(self, path: str):
        """Rimuove la seconda pagina dal PDF se presente."""
        try:
            doc = fitz.open(path)
            if doc.page_count >= 2:
                doc.delete_page(1)
                tmp = path + "_clean.pdf"
                doc.save(tmp)
                doc.close()
                self._safe_remove(path)
                os.rename(tmp, path)
            else:
                doc.close()
        except Exception as e:
            self.log(f"⚠️ Errore pulizia PDF: {e}")

    def _scarica_parte_seconda(self, pdl_num: str) -> Optional[str]:
        """Gestisce il download della Parte Seconda."""
        if not self.driver or not self.wait:
            return None
        assert self.driver and self.wait
        self.log(f"⬇️ Avvio scarico Parte Seconda per PdL {pdl_num}...")
        self.driver.execute_script("window.scrollTo(0, 0);")
        ts = time.time()

        # Assicura che la "Parte Seconda" sia espansa/visibile
        self._espandi_parte_seconda()

        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnPrintPS"))).click()
            # No sleep needed: _gestisci_dialogo_stampa_tutte() checks visibility
            # Gestione eventuale dialogo "Stampa Tutte"
            self._gestisci_dialogo_stampa_tutte()
        except Exception as e:
            self.log_error(f"Click stampa Parte 2 PDL {pdl_num}", e)
            return None

        pdf_path = self._attendi_e_ritorna_nuovo_pdf(ts, timeout=90)
        if not pdf_path:
            return None

        temp_path = os.path.join(self.download_path, f"temp_p2_{int(ts)}.pdf")
        try:
            os.rename(pdf_path, temp_path)
            return temp_path
        except Exception:
            return pdf_path

    def _espandi_parte_seconda(self) -> bool:
        """Tenta di rendere visibile la sezione Parte Seconda."""
        if not self.driver or not self.wait:
            return False
        assert self.driver and self.wait
        try:
            # Se la sezione non è visibile, prova ad aprirla
            if not self.driver.find_element(By.ID, "lblPAFoglio").is_displayed():
                self.log("📂 Tentativo espansione accordion 'Parte Seconda'...")
                clicked = False

                # Strategia 1: ID Label
                try:
                    self.driver.find_element(By.ID, "lblTitoloParteSeconda").click()
                    clicked = True
                except Exception:
                    pass

                # Strategia 2: Testo XPATH
                if not clicked:
                    try:
                        self.driver.find_element(
                            By.XPATH, "//span[contains(text(), 'PARTE SECONDA')]"
                        ).click()
                        clicked = True
                    except Exception:
                        pass

                # Strategia 3: User Specific IDTXT (2E20B56F)
                if not clicked:
                    try:
                        self.driver.find_element(
                            By.CSS_SELECTOR, "span[idtxt='2E20B56F']"
                        ).click()
                        self.log("✓ Aperto tramite idtxt='2E20B56F'")
                        clicked = True
                    except Exception:
                        pass

                # No sleep needed: next wait guarantees visibility

            # Attesa conferma visibilità
            self.wait.until(EC.visibility_of_element_located((By.ID, "lblPAFoglio")))
            return True
        except Exception as e:
            self.log(f"⚠️ Errore apertura Parte Seconda: {e}")
            return False

    def _gestisci_dialogo_stampa_tutte(self):
        """Seleziona 'Stampa Tutte' nel popup se appare."""
        if not self.driver or not self.wait:
            return
        assert self.driver and self.wait
        try:
            # Attende che il radio button "Tutte" sia cliccabile
            btn_tutte = self.wait.until(
                EC.element_to_be_clickable((By.ID, "rbStampaTutte"))
            )
            btn_tutte.click()
            self.log("✓ Selezionato radio button 'Tutte'")

            # Attende che il pulsante "Anteprima" sia cliccabile
            btn_anteprima = self.wait.until(
                EC.element_to_be_clickable((By.ID, "btnAnteprima"))
            )
            btn_anteprima.click()
            self.log("✓ Cliccato su 'Anteprima'")
        except Exception:
            # Il dialogo non appare quando c'è solo 1 rinnovo
            self.log("ℹ️ PDL con 1 rinnovo, dialogo non necessario")
            pass

    def _unisci_e_stampa_pdl(self, pdl_num, p1, p2, item, all_paths) -> bool:
        """Esegue il merge dei PDF e l'eventuale stampa fisica."""
        nome_finale = f"PDL_{pdl_num.replace('/', '-')}.pdf"
        percorso_finale = os.path.join(self.download_path, nome_finale)
        self._safe_remove(percorso_finale)

        from src.utils.document_processor import DocumentProcessor

        if DocumentProcessor.merge_pdfs([p1, p2], percorso_finale):
            self.log(f"✅ PdL {pdl_num} unito con successo.")
            self.downloaded_files.append(percorso_finale)
            all_paths.append(percorso_finale)

            # Stampa
            if item.get("print_enabled") and item.get("printer_name"):
                try:
                    print_pdf(percorso_finale, item["printer_name"])
                    self.log("✅ Comando stampa inviato.")
                except Exception as e:
                    self.log(f"⚠️ Errore stampa: {e}")
            return True

        self.log(f"❌ Fallimento unione PDF per PdL {pdl_num}.")
        return False

    def _handle_session_merge(self, data, all_paths):
        """Crea un unico PDF con tutti i PDL se richiesto."""
        if any(i.get("merge_all_session") for i in data) and all_paths:
            try:
                self.log(f"🔗 Unione sessione ({len(all_paths)} PDL)...")
                ts = time.strftime("%d-%m-%Y_%H-%M")
                path_merge = os.path.join(self.download_path, f"PDL_SESSIONE_{ts}.pdf")

                from src.utils.document_processor import DocumentProcessor

                if DocumentProcessor.merge_pdfs(all_paths, path_merge):
                    self.log(
                        f"✅ PDF Unico Sessione creato: {os.path.basename(path_merge)}"
                    )
                    self.downloaded_files.append(path_merge)
            except Exception as e:
                self.log_error("Unione totale sessione", e)

    def _gestisci_ricerca_estesa(self) -> bool:
        """
        Gestisce il popup 'La ricerca veloce... estenderla?'.
        Ritorna True se, dopo l'estensione, non si trovano risultati (0 Permessi).
        """
        if not self.driver:
            return False
        assert self.driver  # Type narrowing

        try:
            # Cerca il testo specifico indicato dall'utente: <p idtxt="1C51D77B">
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "p[idtxt='1C51D77B']")
                    )
                )
                self.log("ℹ️ Rilevato popup 'Ricerca estesa'.")
            except Exception:
                return False  # Popup non apparso, procedi normale

            # Clicca su Si: <span idtxt="E421C594">
            try:
                btn_si = self.driver.find_element(
                    By.CSS_SELECTOR, "span[idtxt='E421C594']"
                )
                btn_si.click()
                self.log("🖱️ Cliccato 'Si' per estendere la ricerca.")
            except Exception as e:
                self.log(f"⚠️ Popup trovato ma impossibile cliccare Si: {e}")
                return False

            # Attendi ricaricamento pagina/overlay
            self._attendi_scomparsa_overlay()

            # Verifica Risultati: <span id="numPermessiTrovati">0</span>
            try:
                num_res = self.driver.find_element(By.ID, "numPermessiTrovati")
                valore = num_res.text.strip()
                self.log(f"ℹ️ Risultati trovati dopo estensione: {valore}")
                if valore == "0":
                    return True  # Stop, PdL inesistente
            except Exception:
                self.log("⚠️ Impossibile leggere il numero di risultati.")

        except Exception as e:
            self.log_error("Gestione Ricerca Estesa", e)

        return False

    def _gestisci_alert_ricerca(self, timeout=10):
        if not self.driver:
            return False
        assert self.driver
        self.log("🔍 Controllo eventuali alert di errore ricerca...")
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                # Cerca il testo dell'alert per il log
                try:
                    alert_content = self.driver.find_element(
                        By.XPATH, "//div[contains(@class, 'modal-content')]"
                    )
                    if alert_content.is_displayed():
                        testo = alert_content.text.replace("\n", " ").strip()
                        self.log(f"🚩 ALERT RILEVATO: '{testo}'")
                except Exception:
                    pass

                btn_ok = self.driver.find_element(
                    By.XPATH, "//button[contains(@class, 'btn dialog-btn btn-ok')]"
                )
                if btn_ok.is_displayed():
                    self.log("🖱️ Clic su OK per chiudere alert.")
                    btn_ok.click()

                    # CRITICAL FIX: Attendi che il modal scompaia completamente
                    # per evitare ElementClickInterceptedException
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.invisibility_of_element_located(
                                (
                                    By.XPATH,
                                    "//div[contains(@class, 'modal') and contains(@class, 'in')]",
                                )
                            )
                        )
                        self.log("✓ Modal dialog chiuso completamente")
                    except Exception:
                        # Fallback: sleep breve se wait fallisce
                        time.sleep(0.5)

                    return True
            except Exception:
                pass
            # Polling interval handled by while loop condition
        return False

    def _attendi_e_ritorna_nuovo_pdf(self, tempo_riferimento, timeout=60):
        """Attende e restituisce il nuovo PDF scaricato con polling inline (da main)."""
        scadenza = time.time() + timeout
        # Margine di 2 secondi per arrotondamenti filesystem
        tempo_riferimento_adjusted = tempo_riferimento - 2
        self.log(
            f"⏳ Polling cartella download (Ref Time: {int(tempo_riferimento)})..."
        )
        download_path = Path(self.download_path)
        while time.time() < scadenza:
            files = list(download_path.glob("*.pdf"))
            # Escludi file temporanei (temp_p1_*, temp_p2_*) per evitare conflitti
            files = [f for f in files if not f.name.startswith("temp_p")]
            nuovi_files = [
                f for f in files if f.stat().st_mtime > tempo_riferimento_adjusted
            ]
            if nuovi_files:
                nuovi_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
                ultimo_file = nuovi_files[0]
                # Verifica che non ci siano download in corso (.crdownload)
                if not list(download_path.glob("*.crdownload")):
                    self.log(f"📄 Trovato nuovo file: {ultimo_file.name}")
                    return str(ultimo_file)
            time.sleep(1)
        self.log("❌ Nessun nuovo PDF trovato entro il timeout.")
        return None
