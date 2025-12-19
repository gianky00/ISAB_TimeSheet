"""
Bot TS - Timbrature Bot
Bot per l'accesso alla sezione Timbrature del portale ISAB.
"""
import os
import time
import shutil
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.bots.base import BaseBot

class TimbratureBot(BaseBot):
    """
    Bot per l'accesso alle Timbrature.
    """

    @property
    def name(self) -> str:
        return "Timbrature"

    @property
    def description(self) -> str:
        return "Scarica e archivia le timbrature dal portale ISAB"

    @staticmethod
    def get_name() -> str:
        return "Timbrature"

    @staticmethod
    def get_description() -> str:
        return "Scarica e archivia le timbrature dal portale ISAB"

    def __init__(self, data_da: str = "", data_a: str = "", fornitore: str = "", **kwargs):
        super().__init__(**kwargs)
        self.data_da = data_da
        self.data_a = data_a
        self.fornitore = fornitore
        self.db_path = Path("data/timbrature_Isab.db")
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Crea il database e la tabella se non esistono."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timbrature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                ingresso TEXT,
                uscita TEXT,
                nome TEXT,
                cognome TEXT,
                presenza_ts TEXT,
                sito_timbratura TEXT,
                UNIQUE(data, ingresso, uscita, nome, cognome)
            )
        ''')
        conn.commit()
        conn.close()

    def run(self, data: Dict[str, Any]) -> bool:
        """
        Esegue la navigazione alle Timbrature e scarica i dati.
        """
        if isinstance(data, dict):
            self.data_da = data.get('data_da', self.data_da)
            self.data_a = data.get('data_a', self.data_a)
            self.fornitore = data.get('fornitore', self.fornitore)

        self.log(f"Avvio elaborazione Timbrature: Fornitore='{self.fornitore}', Periodo={self.data_da}-{self.data_a}")

        # 1. Navigazione Report -> Timbrature
        if not self._navigate_to_timbrature():
            self.log("❌ Navigazione non riuscita.")
            return False

        # 2. Imposta filtri e scarica Excel
        excel_path = self._process_filters_and_download()

        if excel_path:
            self.log("✅ File Excel scaricato. Elaborazione dati in corso...")
            try:
                self._import_to_db(excel_path)
                self.log("✅ Importazione nel database completata.")
            except Exception as e:
                self.log(f"❌ Errore durante l'importazione nel DB: {e}")
            finally:
                # 3. Elimina file Excel
                if os.path.exists(excel_path):
                    try:
                        os.remove(excel_path)
                        self.log("🗑️ File Excel eliminato.")
                    except Exception as e:
                        self.log(f"⚠️ Impossibile eliminare il file Excel: {e}")
        else:
            self.log("⚠️ Nessun file scaricato o nessun dato trovato.")

        self.log("Processo completato.")
        return True

    def _navigate_to_timbrature(self) -> bool:
        """Naviga a Report -> Timbrature."""
        self._check_stop()
        self.log("Navigazione verso pagina Timbrature...")

        try:
            # Clicca su Report
            report_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='Report']"))
            )
            report_element.click()
            time.sleep(1.5)

            # Sequenza tasti per selezionare la tab Timbrature
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.TAB).pause(0.3)
            actions.send_keys(Keys.TAB).pause(0.3)
            actions.send_keys(Keys.TAB).pause(0.3)
            actions.send_keys(Keys.ENTER).perform()

            time.sleep(1.0)

            # Attende caricamento (cerca elemento freccia fornitore o simile che conferma caricamento)
            self._attendi_scomparsa_overlay()
            return True

        except Exception as e:
            self.log(f"Errore navigazione: {e}")
            return False

    def _process_filters_and_download(self) -> str:
        """Imposta i filtri e scarica l'Excel."""
        self._check_stop()

        try:
            # 1. Seleziona Fornitore
            if self.fornitore:
                self.log(f"Seleziono fornitore: {self.fornitore}")
                try:
                    fornitore_arrow_xpath = "//div[starts-with(@id, 'generic_refresh_combo_box-') and contains(@id, '-trigger-picker') and contains(@class, 'x-form-arrow-trigger')]"

                    try:
                        fornitore_arrow_element = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, fornitore_arrow_xpath))
                        )
                    except TimeoutException:
                        self.log("ID specifico non trovato, provo selettore generico...")
                        # Fallback se l'ID specifico non funziona
                        fornitore_arrow_xpath = "//div[contains(@class, 'x-form-arrow-trigger')]"
                        fornitore_arrow_element = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, fornitore_arrow_xpath))
                        )

                    ActionChains(self.driver).move_to_element(fornitore_arrow_element).click().perform()
                    time.sleep(0.5)

                    fornitore_option_xpath = f"//li[contains(text(), '{self.fornitore}')]"
                    fornitore_option = self.long_wait.until(
                        EC.presence_of_element_located((By.XPATH, fornitore_option_xpath))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", fornitore_option)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", fornitore_option)
                    time.sleep(0.5)
                    self._attendi_scomparsa_overlay()
                    self.log("Fornitore selezionato.")
                except Exception as e:
                    self.log(f"⚠️ Errore selezione fornitore (tentativo mouse): {e}")

            self.log("Imposto filtri data e flag...")
            actions = ActionChains(self.driver)

            # 2. 1 tab per selezionare Data Da
            actions.send_keys(Keys.TAB).pause(0.3)
            if self.data_da:
                actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).pause(0.1)
                actions.send_keys(self.data_da).pause(0.3)

            # 3. 1 tab per selezione Data A
            actions.send_keys(Keys.TAB).pause(0.3)
            if self.data_a:
                actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).pause(0.1)
                actions.send_keys(self.data_a).pause(0.3)

            # 4. 5 tab e poi SPAZIO per selezionare flag "Verifica Presenza Timesheet"
            for _ in range(5):
                actions.send_keys(Keys.TAB).pause(0.2)

            actions.send_keys(Keys.SPACE).pause(0.3)

            # 5. 1 volta tab e invio per cliccare su cerca
            actions.send_keys(Keys.TAB).pause(0.3)
            actions.send_keys(Keys.ENTER)

            self.log("Eseguo sequenza tasti e click su Cerca...")
            actions.perform()

            # Attesa caricamento risultati
            self.log("Attendo caricamento risultati...")
            self._attendi_scomparsa_overlay()
            self.log("Caricamento terminato.")

            # Verifica righe tabella
            try:
                rows_xpath = "//tr[contains(@class, 'x-grid-row')]"
                rows = self.driver.find_elements(By.XPATH, rows_xpath)
                self.log(f"Righe tabella trovate: {len(rows)}")
            except Exception as e:
                self.log(f"Impossibile contare righe: {e}")

            # 6. Cliccare sul tasto Excel
            downloaded_file = ""
            try:
                self.log("Cerco pulsante Excel...")
                # Pausa extra per sicurezza
                time.sleep(1.0)

                # Tentativo 1: Cerca per testo (Fallback)
                try:
                    excel_xpath_text = "//*[contains(text(), 'Esporta in Excel')]"
                    excel_btn = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, excel_xpath_text))
                    )
                    self.log("Pulsante Excel trovato per testo.")
                except TimeoutException:
                    # Tentativo 2: Cerca per classe tool e icona (Primary per Timbrature)
                    self.log("Testo non trovato, cerco icona tool...")
                    # Cerchiamo un div con classe 'x-tool-tool-el' che sia visibile
                    # Potremmo raffinare cercando style='font-family: FontAwesome' se necessario
                    tool_xpath = "//div[contains(@class, 'x-tool-tool-el')]"
                    try:
                        # Trova tutti i tool visibili
                        tools = self.driver.find_elements(By.XPATH, tool_xpath)
                        excel_btn = None
                        for tool in tools:
                            if tool.is_displayed():
                                # Se c'è solo un tool o è il primo/unico rilevante
                                # Il screenshot mostrava ID tool-1105-toolEl
                                excel_btn = tool
                                break

                        if not excel_btn:
                            raise TimeoutException("Nessun tool visibile trovato")

                        self.log("Pulsante Excel (icona tool) trovato.")
                    except Exception:
                        self.log(f"⚠️ Timeout: Pulsante Excel non trovato.")
                        return ""

                # Scroll e click
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", excel_btn)
                time.sleep(0.5)

                self.log("Clicco su Excel...")
                try:
                    excel_btn.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", excel_btn)

                # Attesa download
                self.log("Attendo download...")
                time.sleep(3.0)
                downloaded_file = self._rename_latest_download("timbrature_temp")
                if downloaded_file:
                    self.log(f"File scaricato: {downloaded_file}")
                else:
                    self.log("File non trovato dopo il download.")

            except Exception as e:
                self.log(f"⚠️ Errore download Excel: {e}")

            return downloaded_file

        except Exception as e:
            self.log(f"❌ Errore impostazione filtri: {e}")
            return ""

    def _import_to_db(self, excel_path: str):
        """Legge Excel e importa in DB."""
        # Intestazioni da A1 a P1
        # Mappatura richiesta:
        # Data Timbratura -> Data
        # Ora Ingresso -> Ingresso
        # Ora Uscita -> Uscita
        # Nome Risorsa -> Nome
        # Cognome Risorsa -> Cognome
        # Presente Nei Timesheet -> Presenza TS
        # Sito Timbratura -> Sito Timbratura

        # Colonne da leggere
        cols_to_read = [
            "Data Timbratura",
            "Ora Ingresso",
            "Ora Uscita",
            "Nome Risorsa",
            "Cognome Risorsa",
            "Presente Nei Timesheet",
            "Sito Timbratura"
        ]

        try:
            # Leggi Excel
            # openpyxl engine is safer for .xlsx
            df = pd.read_excel(excel_path, engine='openpyxl')

            # Normalizza nomi colonne (strip spazi)
            df.columns = df.columns.str.strip()

            # Verifica presenza colonne
            missing_cols = [c for c in cols_to_read if c not in df.columns]
            if missing_cols:
                self.log(f"⚠️ Colonne mancanti nel file Excel: {missing_cols}")
                return

            # Filtra e rinomina
            df_filtered = df[cols_to_read].copy()
            df_filtered.rename(columns={
                "Data Timbratura": "data",
                "Ora Ingresso": "ingresso",
                "Ora Uscita": "uscita",
                "Nome Risorsa": "nome",
                "Cognome Risorsa": "cognome",
                "Presente Nei Timesheet": "presenza_ts",
                "Sito Timbratura": "sito_timbratura"
            }, inplace=True)

            # Inserisci in DB
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            added_count = 0
            skipped_count = 0

            for _, row in df_filtered.iterrows():
                try:
                    # Converti nan a stringa vuota o None
                    vals = row.fillna("").astype(str).to_dict()

                    cursor.execute('''
                        INSERT INTO timbrature (data, ingresso, uscita, nome, cognome, presenza_ts, sito_timbratura)
                        VALUES (:data, :ingresso, :uscita, :nome, :cognome, :presenza_ts, :sito_timbratura)
                    ''', vals)
                    added_count += 1
                except sqlite3.IntegrityError:
                    skipped_count += 1
                except Exception as e:
                    self.log(f"Errore riga: {e}")

            conn.commit()
            conn.close()

            self.log(f"Importazione: {added_count} nuovi record aggiunti, {skipped_count} duplicati ignorati.")

        except Exception as e:
            raise Exception(f"Errore lettura Excel: {e}")

    def execute(self, data: Any) -> bool:
        """Esegue login, run, logout e chiude il browser."""
        try:
            if not self._safe_login_with_retry():
                return False

            result = self.run(data)
            self._logout()
            return result
        except Exception as e:
            self.log(f"Errore critico: {e}")
            return False
        finally:
            self.cleanup()

    def _rename_latest_download(self, new_name_base: str) -> str:
        """Trova l'ultimo file scaricato e lo rinomina/sposta."""
        # Simile a DettagliOdA ma semplificato perché lo cancelleremo
        source_dir = Path.home() / "Downloads"
        # Usiamo una cartella temp interna per evitare conflitti con user files
        dest_dir = Path("temp_downloads")
        dest_dir.mkdir(exist_ok=True)

        timeout = 20
        start_time = time.time()
        latest_file = None

        while time.time() - start_time < timeout:
            files = list(source_dir.glob("*"))
            files = [f for f in files if not f.name.endswith('.crdownload') and not f.name.endswith('.tmp') and f.is_file()]

            if files:
                latest_file = max(files, key=lambda f: f.stat().st_mtime)
                if time.time() - latest_file.stat().st_mtime < 20:
                    break
            time.sleep(1)

        if not latest_file:
            return ""

        try:
            ext = latest_file.suffix
            new_path = dest_dir / f"{new_name_base}_{int(time.time())}{ext}"
            shutil.move(str(latest_file), str(new_path))
            return str(new_path)
        except Exception as e:
            self.log(f"Errore spostamento file: {e}")
            return ""

    def _attendi_scomparsa_overlay(self, *args, **kwargs):
        """Attende scomparsa overlay caricamento."""
        try:
            WebDriverWait(self.driver, 0.5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='x-mask']"))
            )
            WebDriverWait(self.driver, 30).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[class*='x-mask']"))
            )
        except:
            pass
