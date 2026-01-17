import glob
import os
import time
from typing import Any, Dict, List, Optional

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.base import SafeworkBaseBot
from src.core.database import db_manager


class SafeWorkPDLSearchBot(SafeworkBaseBot):
    """Bot per la ricerca massiva ed esportazione Excel dei PDL da SafeWork."""

    def __init__(
        self, username, password, headless=False, timeout=30, download_path=""
    ):
        super().__init__(username, password, headless, timeout, download_path)
        self.sites = ["IGCC", "ISAB Nord", "ISAB Sud"]

    @staticmethod
    def get_name() -> str:
        return "Ricerca PDL"

    @property
    def name(self) -> str:
        return "Ricerca PDL"

    def _login(self) -> bool:
        """Login SafeWork ricalcato esattamente dal bot funzionante."""
        if not self.driver or not self.wait:
            self.log("❌ Driver o Wait non inizializzati.")
            return False

        self.log("🌐 Navigazione verso l'URL SafeWork...")
        try:
            self.driver.get(self.SAFEWORK_URL)
            self.log(f"📍 URL caricato. Titolo pagina: {self.driver.title}")
        except Exception as e:
            self.log(f"❌ Errore apertura URL: {e}")
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
            self.log("✅ Sito ISAB Sud selezionato per login.")
        except Exception as e:
            self.log(f"ℹ️ Selezione sito non necessaria o fallita (proseguo): {e}")

        try:
            self.log(f"🔐 Inserimento credenziali per utente: {self.username}")
            u_field = self.wait.until(
                EC.visibility_of_element_located((By.ID, "inpUtente"))
            )
            u_field.clear()
            u_field.send_keys(self.username)

            p_field = self.wait.until(
                EC.visibility_of_element_located((By.ID, "inpPassword"))
            )
            p_field.clear()
            p_field.send_keys(self.password)

            self.log("🖱️ Clic su pulsante Login...")
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnLogin"))).click()
        except Exception as e:
            self.log(f"❌ Errore inserimento credenziali: {e}")
            return False

        self.log("⏳ Attendo il caricamento del sistema (overlay/caricamento)...")
        try:
            # Metodo ereditato da SafeworkBaseBot che gestisce la comparsa/scomparsa del caricamento
            self._attendi_caricamento_sistema()
            self.log("✅ Caricamento sistema completato.")
        except Exception as e:
            self.log(f"❌ Errore durante l'attesa post-login: {e}")
            return False

        return True

    def run(self, data: List[Dict[str, Any]]) -> bool:
        """Esegue la ricerca e l'esportazione dei PDL."""
        # NOTA: _login() viene chiamato automaticamente da BaseBot prima di run()
        if not self.driver or not self.wait:
            self.log("❌ Driver non inizializzato correttamente.")
            return False

        params = data[0] if data else {}
        exclude_closed = params.get("exclude_closed", True)
        site_selection = params.get("site_selection", "Seleziona tutto")

        # 1. Clic su Home Page
        try:
            self.log("🏠 Clic su Home Page...")
            # Attendi che il tasto home sia cliccabile
            btn_home = self.wait.until(
                EC.element_to_be_clickable((By.ID, "topIcon-actHomePage"))
            )
            btn_home.click()
            self.log("⏳ Attesa caricamento Home Page...")
            time.sleep(3)  # Attesa generica post-click Home
            self._attendi_scomparsa_overlay()
        except Exception as e:
            self.log(f"⚠️ Errore clic Home Page: {e}")

        # 2. Clic su Ricerca PdL
        try:
            self.log("🔍 Clic su Ricerca PdL (sideBar)...")
            # Attendi che il tasto ricerca sia cliccabile
            btn_ricerca = self.wait.until(
                EC.element_to_be_clickable((By.ID, "sideBar-actRicercaPdL"))
            )
            btn_ricerca.click()
            self.log("⏳ Attesa caricamento pagina Ricerca...")
            time.sleep(3)  # Attesa generica post-click Ricerca
            self._attendi_scomparsa_overlay()
        except Exception as e:
            self.log(f"❌ Errore apertura Ricerca PdL: {e}")
            return False

        # 3. Gestione Flag "Escludi chiusi"
        try:
            checkbox = self.wait.until(
                EC.presence_of_element_located((By.ID, "fldEscludiChiusi"))
            )
            is_checked = checkbox.is_selected()
            if is_checked != exclude_closed:
                self.log(f"🖱️ Impostazione checkbox 'Escludi chiusi' a {exclude_closed}")
                self.driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(1)
        except Exception as e:
            self.log(f"⚠️ Errore gestione checkbox: {e}")

        # 4. Iterazione Siti
        sites_to_process = (
            self.sites if site_selection == "Seleziona tutto" else [site_selection]
        )

        for site in sites_to_process:
            if not self._select_site_and_search(site):
                self.log(f"❌ Errore ricerca per sito {site}")
                continue

            excel_file = self._export_excel(site)
            if excel_file:
                self._import_to_db(excel_file)
                # Eliminazione file dopo importazione
                try:
                    os.remove(excel_file)
                    self.log(
                        f"🗑️ File temporaneo rimosso: {os.path.basename(excel_file)}"
                    )
                except Exception as e:
                    self.log(f"⚠️ Impossibile rimuovere il file {excel_file}: {e}")
            else:
                self.log(f"⚠️ Nessun file esportato per {site}")

        return True

    def _select_site_and_search(self, site_name: str) -> bool:
        """Seleziona il sito dal menu e clicca Cerca."""
        if not self.wait:
            return False
        try:
            self.log(f"🏢 Selezione sito: {site_name}")
            site_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//span[contains(text(), 'ISAB Sud') or contains(text(), 'ISAB Nord') or contains(text(), 'IGCC') or contains(text(), 'Sito')]",
                    )
                )
            )
            site_dropdown.click()
            time.sleep(1)

            option = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//li//span[text()='{site_name}']")
                )
            )
            option.click()
            time.sleep(1)

            self.log("🖱️ Clic su Cerca...")
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnCerca"))).click()
            self._attendi_scomparsa_overlay(timeout_secondi=300)
            return True
        except Exception as e:
            self.log(f"❌ Errore selezione/ricerca: {e}")
            return False

    def _export_excel(self, site_name: str) -> Optional[str]:
        """Esporta e attende download."""
        if not self.wait:
            return None
        try:
            self.log(f"📥 Esportazione Excel per {site_name}...")
            ts_start = time.time()
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnEsporta"))).click()

            timeout = 600
            end_time = time.time() + timeout
            while time.time() < end_time:
                files = glob.glob(os.path.join(self.download_path, "Ricerca*.xlsx"))
                new_files = [f for f in files if os.path.getmtime(f) > ts_start]
                if new_files:
                    if not any(
                        f.endswith(".crdownload")
                        for f in glob.glob(os.path.join(self.download_path, "*"))
                    ):
                        latest_file = max(new_files, key=os.path.getmtime)
                        return latest_file
                time.sleep(2)
            return None
        except Exception as e:
            self.log(f"❌ Errore esportazione: {e}")
            return None

    def _import_to_db(self, file_path: str):
        """Importazione massiva in SQLite."""
        try:
            self.log("🗄️ Importazione in database...")
            df = pd.read_excel(file_path)
            mapping = {
                "N° PDL": "n_pdl",
                "DATA CREAZIONE": "data_creazione",
                "AREA": "area",
                "UNITÀ": "unita",
                "DITTA": "ditta",
                "DESCRIZIONE DEL LAVORO": "descrizione_lavoro",
                "TIPOLOGIA": "tipologia",
                "STATO": "stato",
                "APPARECCHIATURA": "apparecchiatura",
                "RICHIEDENTE": "richiedente",
                "DATA RICHIESTA": "data_richiesta",
                "EMITTENTE": "emittente",
                "DATA EMISSIONE": "data_emissione",
                "APRENTE": "aprente",
                "DATA APERTURA": "data_apertura",
                "PRIORITÀ": "priorita",
                "CONTRATTO": "contratto",
                "ORDINE": "ordine",
                "SITO": "sito",
            }
            df.rename(columns=mapping, inplace=True)
            for col in mapping.values():
                if col not in df.columns:
                    df[col] = ""

            data_to_insert = [
                tuple(str(val) for val in row)
                for row in df[list(mapping.values())].values
            ]

            query = f"INSERT INTO pdl ({', '.join(mapping.values())}) VALUES ({', '.join(['?'] * len(mapping))})"

            with db_manager.get_connection(db_manager.DB_PDL) as conn:
                conn.executemany(query, data_to_insert)

            self.log(f"✅ {len(data_to_insert)} righe importate.")
        except Exception as e:
            self.log(f"❌ Errore importazione: {e}")
