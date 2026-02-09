import time
from pathlib import Path
from typing import Any

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.safework.base import SafeworkBaseBot
from src.core.database import db_manager
from src.core.sync_tracker import SyncTracker


class SafeWorkPDLSearchBot(SafeworkBaseBot):
    """Bot per la ricerca massiva ed esportazione Excel dei PDL da SafeWork."""

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        self.sites = ["IGCC", "ISAB Nord", "ISAB Sud"]

    @staticmethod
    def get_name() -> str:
        return "Ricerca PDL"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return []

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
            self.log(f"i Selezione sito non necessaria o fallita (proseguo): {e}")

        try:
            self.log(f"🔐 Inserimento credenziali per utente: {self.username}")
            u_field = self.wait.until(EC.visibility_of_element_located((By.ID, "inpUtente")))
            u_field.clear()
            u_field.send_keys(self.username)

            p_field = self.wait.until(EC.visibility_of_element_located((By.ID, "inpPassword")))
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

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esegue la ricerca e l'esportazione dei PDL."""
        if not self.driver or not self.wait:
            self.log("❌ Driver non inizializzato correttamente.")
            return False

        params = data[0] if data else {}

        # 1. Navigazione e Setup
        if not self._naviga_a_ricerca():
            return False

        # 2. Filtri
        self._configura_filtri(params.get("exclude_closed", True))

        # 3. Elaborazione Siti
        site_selection = params.get("site_selection", "Seleziona tutto")
        self._processa_siti(site_selection)

        return True

    def _naviga_a_ricerca(self) -> bool:
        """Naviga verso la pagina di ricerca."""
        if not self.wait or not self.driver:
            return False
        try:
            self.log("🏠 Clic su Home Page...")
            btn_home = self.wait.until(EC.element_to_be_clickable((By.ID, "topIcon-actHomePage")))
            btn_home.click()
            # No sleep needed: _attendi_scomparsa_overlay() has internal wait
            self._attendi_scomparsa_overlay()

            self.log("🔍 Clic su Ricerca PdL (sideBar)...")
            btn_ricerca = self.wait.until(EC.element_to_be_clickable((By.ID, "sideBar-actRicercaPdL")))
            btn_ricerca.click()
            # No sleep needed: _attendi_scomparsa_overlay() has internal wait
            self._attendi_scomparsa_overlay()
            return True
        except Exception as e:
            self.log(f"❌ Errore navigazione ricerca: {e}")
            return False

    def _configura_filtri(self, exclude_closed: bool):
        """Imposta i filtri di ricerca."""
        if not self.wait or not self.driver:
            return
        try:
            checkbox = self.wait.until(EC.presence_of_element_located((By.ID, "fldEscludiChiusi")))
            if checkbox.is_selected() != exclude_closed:
                self.log(f"🖱️ Impostazione checkbox 'Escludi chiusi' a {exclude_closed}")
                self.driver.execute_script("arguments[0].click();", checkbox)
                # No sleep needed: checkbox state change is immediate
        except Exception as e:
            self.log(f"⚠️ Errore gestione checkbox: {e}")

    def _processa_siti(self, site_selection: str) -> None:
        """Cicla sui siti e importa i dati."""
        sites = self.sites if site_selection == "Seleziona tutto" else [site_selection]
        for site in sites:
            if self._select_site_and_search(site):
                excel_file = self._export_excel(site)
                if excel_file:
                    self._import_to_db(excel_file)
                    self._cleanup_temp_file(excel_file)
                else:
                    self.log(f"⚠️ Nessun file esportato per {site}")
            else:
                self.log(f"❌ Errore ricerca per sito {site}")

    def _cleanup_temp_file(self, file_path: str) -> None:
        """Rimuove file temporaneo."""
        try:
            p = Path(file_path)
            p.unlink()
            self.log(f"🗑️ File temporaneo rimosso: {p.name}")
        except Exception as e:
            self.log(f"⚠️ Impossibile rimuovere il file {file_path}: {e}")

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
            # Wait for dropdown options to appear
            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{site_name}']"))
            )
            option.click()
            # No sleep needed: next wait guarantees button availability
            self.log("🖱️ Clic su Cerca...")
            self.wait.until(EC.element_to_be_clickable((By.ID, "btnCerca"))).click()
            self._attendi_scomparsa_overlay(timeout_secondi=300)
            return True
        except Exception as e:
            self.log(f"❌ Errore selezione/ricerca: {e}")
            return False

    def _export_excel(self, site_name: str) -> str | None:
        """Esporta e attende download."""
        if not self.wait:
            return None
        try:
            self.log(f"📥 Esportazione Excel per {site_name}...")
            self.log(f"🔎 DEBUG: Attendo file in: '{self.download_path}'")
            # Use helper for efficient polling
            from src.bots.base.wait_helpers import poll_for_new_file

            # 1. Snapshot dei file PRE-CLICK (per rilevare il delta)
            download_dir = Path(self.download_path)
            files_before = {str(f.resolve()) for f in download_dir.glob("*") if f.is_file()}

            self.wait.until(EC.element_to_be_clickable((By.ID, "btnEsporta"))).click()

            # 2. Attesa NUOVO file (Delta)
            latest_file = poll_for_new_file(
                directory=self.download_path,
                files_before=files_before,
                pattern="Ricerca*.xlsx",
                timeout=600,
                poll_interval=1.0,
            )
            return latest_file
        except Exception as e:
            self.log(f"❌ Errore esportazione: {e}")
            return None

    def _import_to_db(self, file_path: str):
        """Importazione massiva in SQLite con calcolo diff e persistenza stato."""
        try:
            self.log("🗄️ Importazione in database...")
            start_time = time.time()

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

            # Garantisce che tutte le colonne del mapping esistano nel DataFrame
            for col in mapping.values():
                if col not in df.columns:
                    df[col] = ""

            # Sostituisce i valori NaN con stringhe vuote per evitare "nan" nel DB
            df.fillna("", inplace=True)

            # --- Calcolo Diff ---
            # 1. Ottieni ID esistenti (n_pdl)
            try:
                with db_manager.get_connection(db_manager.DB_PDL, read_only=True) as conn:
                    existing_pdls = {row[0] for row in conn.execute("SELECT n_pdl FROM pdl").fetchall()}
            except Exception:
                existing_pdls = set()

            # 2. Identifica nuovi ID
            current_pdls = set(df["n_pdl"].astype(str))
            new_pdls_count = len(current_pdls - existing_pdls)

            added_count = new_pdls_count
            removed_count = 0  # Non cancelliamo nulla in questa logica

            # Utilizza tutte le colonne definite nel mapping (che corrispondono al DB)
            columns = list(mapping.values())

            data_to_insert = [tuple(row) for row in df[columns].values]

            placeholders = ", ".join(["?"] * len(columns))
            col_names = ", ".join(columns)
            query = f"INSERT OR REPLACE INTO pdl ({col_names}) VALUES ({placeholders})"  # nosec B608

            with db_manager.get_connection(db_manager.DB_PDL) as conn:
                conn.executemany(query, data_to_insert)

            duration = time.time() - start_time
            SyncTracker.update_status("pdl", added_count, removed_count, duration)

            self.log(
                f"✅ Importazione completata: +{added_count} nuovi PDL su {len(data_to_insert)} righe processate."
            )
        except Exception as e:
            self.log(f"❌ Errore importazione: {e}")
