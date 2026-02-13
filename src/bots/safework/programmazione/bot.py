"""
SyncroJob - SafeWork Programmazione Bot
Bot per il monitoraggio della programmazione settimanale dei richiedenti su SafeWork.
"""

import logging
import time
import traceback
from datetime import datetime, timedelta
from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from src.bots.safework.base import SafeworkBaseBot

logger = logging.getLogger(__name__)


class SafeWorkProgrammazioneBot(SafeworkBaseBot):
    """Bot per monitorare i flag TCL/TGO della settimana per richiedenti specifici."""

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        self.results: list[dict[str, Any]] = []

    @staticmethod
    def get_name() -> str:
        return "Programmazione PDL"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return []

    @property
    def name(self) -> str:
        return "programmazione_pdl"

    def _login(self) -> bool:
        """Login SafeWork con selezione sito obbligatoria."""
        if not self.driver or not self.wait:
            return False

        self.log("🌐 Navigazione verso SafeWork...")
        try:
            self.driver.get(self.SAFEWORK_URL)
        except Exception as e:
            self.log(f"❌ Errore apertura URL: {e}")
            return False

        try:
            self.log("⏳ Selezione sito 'ISAB Sud'...")
            btn_sito = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='ms-choice']"))
            )
            btn_sito.click()

            opzione_isab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'ms-drop')]//span[normalize-space()='ISAB Sud']",
                    )
                )
            )
            opzione_isab.click()
            self.log("✅ Sito selezionato.")
        except Exception as e:
            self.log(f"i Selezione sito saltata o già impostata: {e}")

        try:
            self.log(f"🔐 Inserimento credenziali per: {self.username}")
            u_field = self.wait.until(EC.visibility_of_element_located((By.ID, "inpUtente")))
            u_field.clear()
            u_field.send_keys(self.username)
            
            p_field = self.wait.until(EC.visibility_of_element_located((By.ID, "inpPassword")))
            p_field.clear()
            p_field.send_keys(self.password)
            
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnLogin"))).click()
            
            if "fcaldarella" in self.username.lower():
                self.log("⏳ Account TCL (fcaldarella) rilevato: attendo solo overlay...")
                self._attendi_scomparsa_overlay(timeout_secondi=60)
            else:
                self.log("⏳ Account standard rilevato: attendo caricamento sistema...")
                self._attendi_caricamento_sistema()
                
            self.log("✅ Login completato con successo.")
            return True
        except Exception as e:
            self.log(f"❌ Errore durante il login: {e}")
            return False

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esecuzione principale del controllo programmazione."""
        try:
            if not self.driver or not self.wait:
                self.log("❌ Driver non pronto.")
                return False

            params = data[0] if data else {}
            requesters = params.get("requesters", [])
            date_start = params.get("date_start")
            date_end = params.get("date_end")

            if not requesters:
                self.log("⚠️ Nessun richiedente in input.")
                return False

            self.log(f"🚀 Avvio Analisi per: {', '.join(requesters)}")
            self.log(f"📅 Periodo: {date_start} - {date_end}")

            # 1. Navigazione
            if not self._naviga_a_visualizza_attivita():
                return False

            # 2. Setup Filtri Statici (Date e Ditta)
            self._setup_filtri_base(date_start, date_end)

            # 3. Ciclo Richiedenti
            self.results = []
            for req in requesters:
                self._check_stop()
                self.log(f"👤 Elaborazione: {req}...")
                
                if self._applica_filtro_richiedente(req):
                    self.log(f"🔍 Ricerca in corso per {req}...")
                    self._esegui_ricerca()
                    self._scrap_risultati(req)
                else:
                    self.log(f"⚠️ Salto {req} (impossibile selezionare)")

            self.log(f"✨ FINE: Trovati {len(self.results)} PDL con programmazione.")
            return True

        except Exception as e:
            self.log(f"❌ ERRORE CRITICO BOT: {e}")
            logger.error(traceback.format_exc())
            return False

    def _naviga_a_visualizza_attivita(self) -> bool:
        """Naviga verso la pagina corretta gestendo gli overlay."""
        try:
            self.log("🏠 Ritorno alla Home...")
            btn_home = self.wait.until(EC.element_to_be_clickable((By.ID, "topIcon-actHomePage")))
            self.driver.execute_script("arguments[0].click();", btn_home)
            self._attendi_scomparsa_overlay()

            self.log("📋 Navigazione in 'Visualizza Attività'...")
            btn_vis = self.wait.until(EC.element_to_be_clickable((By.ID, "sideBar-actVisualizzaAttivita")))
            self.driver.execute_script("arguments[0].click();", btn_vis)
            self._attendi_scomparsa_overlay()
            return True
        except Exception as e:
            self.log(f"❌ Fallita navigazione attività: {e}")
            return False

    def _setup_filtri_base(self, start: str, end: str):
        """Imposta date, ditta e pulisce campi PDL."""
        try:
            # Pulisci campo PDL (fondamentale per ricerca generale)
            self.log("🧹 Pulizia filtri precedenti...")
            pdl_field = self.driver.find_element(By.ID, "fldNumPermesso")
            pdl_field.clear()
            pdl_field.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)

            # Imposta Date
            self.log(f"📅 Impostazione date: {start} - {end}")
            for field_id, val in [("programmazioneDal", start), ("programmazioneAl", end)]:
                el = self.driver.find_element(By.ID, field_id)
                self.driver.execute_script("arguments[0].value = '';", el)
                self.driver.execute_script("arguments[0].value = arguments[1];", el, val)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", el)

            # Filtro Ditta CO.EMI
            self.log("🏢 Filtro Ditta: CO.EMI SRL")
            btn_ditta = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='fldIdDitta']/following-sibling::div/button")))
            btn_ditta.click()
            time.sleep(0.5)
            opt = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ms-drop')]//span[normalize-space()='CO.EMI SRL']")))
            opt.click()
            btn_ditta.click() # Chiudi
            
        except Exception as e:
            self.log(f"⚠️ Errore durante setup filtri: {e}")

    def _applica_filtro_richiedente(self, nome: str) -> bool:
        """Seleziona il richiedente gestendo la multiselezione di SafeWork."""
        try:
            # 1. Apri Dropdown
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='fldIdRichiedente']/following-sibling::div/button")))
            btn.click()
            time.sleep(0.5)

            # 2. Ricerca nome
            dropdown = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'ms-drop') and contains(@style,'display: block')]")))
            search = dropdown.find_element(By.XPATH, ".//input[@type='text']")
            search.clear()
            search.send_keys(nome)
            time.sleep(1)

            # 3. Clicca l'opzione
            opzioni = dropdown.find_elements(By.XPATH, f".//label//span[contains(normalize-space(), '{nome}')]")
            if not opzioni:
                nome_short = nome.split()[0]
                opzioni = dropdown.find_elements(By.XPATH, f".//label//span[contains(normalize-space(), '{nome_short}')]")

            if opzioni:
                self.driver.execute_script("arguments[0].click();", opzioni[0])
                time.sleep(0.5)
                btn.click() # Chiudi
                return True
            
            self.log(f"❌ Richiedente '{nome}' non trovato nel sistema.")
            btn.click()
            return False
        except Exception as e:
            self.log(f"⚠️ Errore selezione richiedente: {e}")
            return False

    def _esegui_ricerca(self):
        """Clicca Cerca e attende caricamento."""
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.ID, "btnAvviaRicerca")))
            btn.click()
            self._attendi_scomparsa_overlay(timeout_secondi=60)
            time.sleep(1) # Buffer stabilità tabella
        except Exception as e:
            self.log(f"⚠️ Errore clic ricerca: {e}")

    def _scrap_risultati(self, req_input: str):
        """Estrae i dati dalla tabella con mapping indici corretto."""
        try:
            # Verifica se ci sono risultati
            try:
                msg_vuoto = self.driver.find_elements(By.XPATH, "//td[contains(text(), 'Nessun dato')]")
                if msg_vuoto and msg_vuoto[0].is_displayed():
                    self.log(f"ℹ️ Nessun PDL programmato per {req_input}")
                    return
            except: pass

            table = self.wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'table')]")))
            rows = table.find_elements(By.XPATH, ".//tbody/tr")
            
            if not rows:
                return

            self.log(f"📊 Analisi di {len(rows)} righe per {req_input}...")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                # La tabella SafeWork ha indici diversi da quelli ipotizzati:
                # Indice 0: Sito (Icona)
                # Indice 1: N° PDL <-- Questo era il bug (PDL è 1, non 2)
                # Indice 2: Area <-- Questo era il bug (Area è 2, non 1)
                # Indice 3: Descrizione
                # ...
                # Indice 18: Richiedente
                if len(cells) < 19: continue

                pdl = cells[1].text.strip()
                area = cells[2].text.strip()
                desc = cells[3].text.strip()
                richiedente_sito = cells[18].text.strip()
                
                # Se richiedente è "Si", significa che l'indice 18 è sbagliato per questa vista.
                # Nello script originale Richiedente era 18. Controlliamo se è slittato.
                if richiedente_sito.lower() in ("si", "no"):
                    # Fallback: cerchiamo la colonna con il nome del richiedente
                    # Spesso in SafeWork il richiedente è nell'ultima colonna utile
                    self.log("🔎 Rilevato slittamento colonne richiedente, cerco indice corretto...")
                    for idx, c in enumerate(cells):
                        t = c.text.strip()
                        if any(n in t for n in req_input.split()):
                            richiedente_sito = t
                            break

                self.log(f"📝 Analisi PDL {pdl}...")

                prog_settimanale = []
                found_at_least_one = False
                for i in range(7):
                    idx_tcl = 4 + (i * 2)
                    idx_tgo = 5 + (i * 2)
                    
                    has_tcl = self._check_flag(cells[idx_tcl], "_TCL")
                    has_tgo = self._check_flag(cells[idx_tgo], "_TGO")
                    
                    if has_tcl or has_tgo:
                        found_at_least_one = True
                    
                    prog_settimanale.append({
                        "giorno": i + 1,
                        "tcl": has_tcl,
                        "tgo": has_tgo
                    })

                if found_at_least_one:
                    self.results.append({
                        "pdl": pdl,
                        "area": area,
                        "descrizione": desc,
                        "richiedente": richiedente_sito,
                        "programmazione": prog_settimanale
                    })
                    self.log(f"✅ PDL {pdl} aggiunto.")

        except Exception as e:
            self.log(f"⚠️ Errore scraping risultati: {e}")

    def _check_flag(self, cell, pattern: str) -> bool:
        """Verifica se il flag è attivo (presenza di attributo 'title')."""
        try:
            inp = cell.find_element(By.XPATH, f".//input[contains(@id, '{pattern}')]")
            title = inp.get_attribute("title")
            return bool(title and title.strip())
        except:
            return False
