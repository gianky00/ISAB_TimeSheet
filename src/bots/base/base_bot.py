"""
Bot TS - Base Bot
Classe base astratta per tutti i bot di automazione.
"""
import os
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Callable, List, Dict, Any
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager


class BotStatus(Enum):
    """Stati possibili del bot."""
    IDLE = "idle"
    INITIALIZING = "initializing"
    LOGGING_IN = "logging_in"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    STOPPED = "stopped"


class BaseBot(ABC):
    """
    Classe base astratta per tutti i bot ISAB.
    
    Fornisce:
    - Gestione Selenium/Chrome con anti-detection
    - Login al portale ISAB
    - Gestione popup "altro utente connesso"
    - Navigazione menu ExtJS
    - Sistema di callback per logging
    - Meccanismo di stop
    """
    
    # URL del portale ISAB
    ISAB_URL = "https://portalefornitori.isab.com/Ui/"
    
    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = 30,
        download_path: str = ""
    ):
        """
        Inizializza il bot.
        
        Args:
            username: Username ISAB
            password: Password ISAB
            headless: Se True, esegue Chrome in modalità headless
            timeout: Timeout in secondi per le attese
            download_path: Percorso per i download (vuoto = default)
        """
        self.username = username
        self.password = password
        self.headless = headless
        self.timeout = timeout
        self.download_path = download_path
        
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.popup_wait: Optional[WebDriverWait] = None
        self.long_wait: Optional[WebDriverWait] = None
        self.status = BotStatus.IDLE
        self._stop_requested = False
        self._log_callback: Optional[Callable[[str], None]] = None
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nome del bot."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Descrizione del bot."""
        pass
    
    def set_log_callback(self, callback: Callable[[str], None]):
        """Imposta la callback per il logging."""
        self._log_callback = callback
    
    def log(self, message: str):
        """Logga un messaggio."""
        print(f"[{self.name}] {message}")
        if self._log_callback:
            self._log_callback(message)
    
    def request_stop(self):
        """Richiede l'interruzione del bot."""
        self._stop_requested = True
        self.log("⚠️ Interruzione richiesta...")
    
    def _check_stop(self):
        """Controlla se è stata richiesta l'interruzione."""
        if self._stop_requested:
            raise InterruptedError("Bot interrotto dall'utente")
    
    def _init_driver(self):
        """Inizializza il driver Chrome con configurazione ottimizzata e SENZA POPUP."""
        self.log("Inizializzazione browser...")
        self.status = BotStatus.INITIALIZING
        
        options = Options()
        
        # --- 1. ARGOMENTI PER DISABILITARE UI E POPUP (Chrome Switches) ---
        # Disabilita la bolla dei download (Download Bubble)
        options.add_argument("--disable-features=DownloadBubble,DownloadBubbleV2")
        
        # Disabilita la schermata di scelta motore di ricerca (EU compliance screen)
        options.add_argument("--disable-search-engine-choice-screen")
        
        # Disabilita popup di "Ripristina sessione" in caso di chiusura forzata
        options.add_argument("--no-restore-session-state")
        options.add_argument("--disable-session-crashed-bubble")
        
        # Disabilita notifiche e infobar di automazione
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking") # Blocca i popup nativi del browser
        
        # Anti-detection base
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Performance
        # options.add_argument("--disable-gpu") # Removed to allow hardware acceleration
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Network optimizations (No Proxy)
        options.add_argument("--no-proxy-server")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        
        # Headless mode
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        # Load strategy EAGER (DOMContentLoaded instead of Load complete)
        # This speeds up automation significantly as we don't wait for all images/css
        options.page_load_strategy = 'eager'

        # --- CACHING & PERSISTENT PROFILE ---
        # Usa un profilo persistente nella cartella data/chrome_profile del progetto.
        # Questo permette di mantenere la cache (immagini, JS, CSS) e velocizzare i caricamenti successivi.
        profile_dir = Path("data/chrome_profile").absolute()
        options.add_argument(f"user-data-dir={profile_dir}")
        self.log(f"Cache profilo attiva: {profile_dir}")

        # --- 2. PREFERENZE PROFILO UTENTE (Prefs) ---
        prefs = {
            # Blocca gestore password e credenziali
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "users.users_allowed_to_save_passwords": False,
            
            # Blocca notifiche e popup generici
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.automatic_downloads": 1,
            
            # Evita che il browser chieda cosa fare con i PDF (li scarica direttamente)
            "plugins.always_open_pdf_externally": True,
            
            # Disabilita avvisi di sicurezza fastidiosi sui download
            "safebrowsing.enabled": True, 
            "safebrowsing.disable_download_protection": True,
        }

        # --- 3. CONFIGURAZIONE DOWNLOAD PATH ---
        # Nota: Non impostiamo più 'download.default_directory' per usare quella di default del sistema/browser.
        # I file verranno poi spostati nella cartella di destinazione configurata (self.download_path).

        # Aggiorna le preferenze base
        prefs.update({
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            # Impostazioni extra per evitare la barra/bolla dei download
            "browser.download.manager.showWhenStarting": False,
            "download.manager.showWhenStarting": False,
        })

        # Argomenti extra di sicurezza per permettere download automatici
        options.add_argument("--safebrowsing-disable-download-protection")
        options.add_argument("--safebrowsing-disable-extension-blacklist")

        # Applica tutte le preferenze
        options.add_experimental_option("prefs", prefs)
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver flag (JS side)
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
        )
        
        # Setup waits con timeout diversi
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.popup_wait = WebDriverWait(self.driver, 7)
        self.long_wait = WebDriverWait(self.driver, 15)
        
        self.log("✓ Browser inizializzato (Modalità Silenziosa)")
    
    def _attendi_scomparsa_overlay(self, timeout_secondi: int = 45) -> bool:
        """
        Attende in modo robusto che gli overlay di caricamento tipici dei siti Ext JS scompaiano.
        """
        try:
            overlay_wait = WebDriverWait(self.driver, timeout_secondi)
            # XPath per maschere di caricamento comuni in Ext JS
            xpath_mask = "//div[contains(@class, 'x-mask-msg') or contains(@class, 'x-mask')][not(contains(@style,'display: none'))]"
            # XPath per il testo di caricamento
            xpath_text = "//div[text()='Caricamento...']"
            
            # Attende che gli elementi diventino invisibili
            overlay_wait.until(EC.invisibility_of_element_located((By.XPATH, f"{xpath_mask} | {xpath_text}")))
            self.log(" -> Overlay di caricamento scomparso.")
            time.sleep(0.3)  # Piccola pausa per stabilizzare l'interfaccia
            return True
        except TimeoutException:
            self.log(f"⚠ Timeout ({timeout_secondi}s) attesa overlay. Proseguo con cautela.")
            return False
    
    def _perform_login_form_action(self):
        """Esegue le azioni di compilazione form e click su Accedi."""
        username_field = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "Username"))
        )
        username_field.clear()
        username_field.send_keys(self.username)

        password_field = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "Password"))
        )
        password_field.clear()
        password_field.send_keys(self.password)

        # Clicca sul pulsante Accedi (ExtJS button)
        accedi_xpath = "//span[text()='Accedi' and contains(@class, 'x-btn-inner')]"
        try:
            # Tenta click standard
            accedi_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, accedi_xpath))
            )
            accedi_btn.click()
        except (TimeoutException, ElementClickInterceptedException):
            self.log("⚠️ Click standard intercettato o timeout. Tento click JavaScript...")
            # Fallback: JavaScript click forzato
            accedi_element = self.driver.find_element(By.XPATH, accedi_xpath)
            self.driver.execute_script("arguments[0].click();", accedi_element)

        self.log("Login effettuato. Attendo scomparsa overlay...")
        self._attendi_scomparsa_overlay(60)

    def _login(self) -> bool:
        """
        Esegue il login al portale ISAB con i selettori corretti per ExtJS.
        Ritorna False se viene rilevato "Proxy Error".
        """
        self._check_stop()
        self.log(f"Navigazione a: {self.ISAB_URL}")
        self.status = BotStatus.LOGGING_IN
        
        try:
            self.driver.get(self.ISAB_URL)
            
            # Check Proxy Error immediato
            page_title = self.driver.title
            page_source = self.driver.page_source
            if "Proxy Error" in page_title or "Proxy Error" in page_source:
                self.log("⚠ Rilevato 'Proxy Error' durante l'accesso iniziale.")
                return False

            # Attendi il form di login - usa NAME invece di ID (specifico ISAB)
            self.log("Tentativo di login...")
            
            # Attende che eventuali overlay iniziali spariscano prima di interagire
            self._attendi_scomparsa_overlay(timeout_secondi=10)

            # --- Check sessione esistente (Profilo Persistente) ---
            # Se siamo già loggati, il campo Username non c'è.
            try:
                # Tenta un'attesa breve per vedere se appare il login
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "Username"))
                )
                # Se trovato, procedi con il login normale
                self._perform_login_form_action()

            except TimeoutException:
                # Se TimeoutException avviene nel blocco 'try' principale (attesa Username),
                # potrebbe essere perché siamo già loggati. Verifichiamo.
                self.log("Campo Username non trovato. Verifico se già loggato...")
                if self._verify_logged_in_via_ui():
                    self.log("✓ Rilevata sessione attiva (skip login).")
                    return True
                else:
                    self.log("⚠️ Username assente e sessione invalida/scaduta.")
                    self.log("🔄 Ricarico la pagina per forzare il form di login...")
                    self.driver.refresh()
                    self._attendi_scomparsa_overlay(10)

                    # Riprova a cercare username DOPO il refresh
                    try:
                        self._perform_login_form_action()
                        return True
                    except Exception as e:
                        self.log(f"✗ Fallito recupero sessione: {e}")
                        return False
            
            self._check_stop()
            
            # Gestisci popup "Sessione attiva" - clicca su "Si"
            self._handle_session_popup()
            
            # Gestisci popup generico "OK"
            self._handle_ok_popup()
            
            self.log("✓ Login completato con successo")
            return True
                
        except TimeoutException:
            self.log("✗ Timeout durante il login")
            return False
        except Exception as e:
            self.log(f"✗ Errore login: {e}")
            return False
    
    def _handle_session_popup(self):
        """Gestisce il popup 'Esiste già una sessione attiva'."""
        try:
            si_button_xpath = "//span[text()='Si' and contains(@class, 'x-btn-inner')]/ancestor::a[contains(@class, 'x-btn')]"
            si_button = self.popup_wait.until(EC.element_to_be_clickable((By.XPATH, si_button_xpath)))
            self.log("Pop-up 'Sessione attiva' trovato. Click su 'Si'...")
            si_button.click()
            self._attendi_scomparsa_overlay(10)
        except TimeoutException:
            pass  # Nessun popup sessione - normale
    
    def _handle_ok_popup(self):
        """Gestisce popup generico con pulsante OK."""
        try:
            ok_button = self.popup_wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='OK' and contains(@class, 'x-btn-inner')]"))
            )
            self.log("Pop-up 'OK' trovato. Click...")
            ok_button.click()
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.XPATH, "//span[text()='OK' and contains(@class, 'x-btn-inner')]"))
            )
            self.log("Popup gestito.")
        except TimeoutException:
            pass  # Nessun popup OK - normale
    
    def _handle_new_session_popup(self):
        """Alias per retrocompatibilità."""
        self._handle_session_popup()
        self._handle_ok_popup()
    
    def _handle_unsaved_changes_popup(self):
        """
        Gestisce il popup 'Attenzione - Le modifiche non salvate andranno perse'.
        Questo popup può apparire dopo aver cliccato su 'Esci'.
        """
        try:
            # Cerca popup con titolo "Attenzione" e messaggio su modifiche non salvate
            # Prima verifica se c'è una finestra con titolo "Attenzione"
            attenzione_xpath = "//span[contains(@class, 'x-window-header-text') and contains(text(), 'Attenzione')]"
            
            # Attendi brevemente per vedere se appare il popup
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, attenzione_xpath))
            )
            
            self.log("Pop-up 'Attenzione - modifiche non salvate' trovato. Click su 'Si'...")
            
            # Trova il pulsante "Si" nel popup
            si_button_xpath = "//div[contains(@class, 'x-window')]//span[normalize-space(text())='Si' and contains(@class, 'x-btn-inner')]"
            si_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, si_button_xpath))
            )
            
            # Click sul pulsante Si
            try:
                si_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", si_button)
            
            self.log("Popup 'Attenzione' gestito - cliccato 'Si'.")
            time.sleep(0.5)
            return True
            
        except TimeoutException:
            pass  # Nessun popup "Attenzione" - normale
        except Exception as e:
            self.log(f"Errore gestione popup Attenzione: {e}")
        
        return False
    
    def _verify_login(self) -> bool:
        """Verifica se il login è avvenuto con successo."""
        try:
            return "login" not in self.driver.current_url.lower()
        except Exception:
            return False

    def _verify_logged_in_via_ui(self) -> bool:
        """Controlla se ci sono elementi della UI post-login (es. bottone Settings)."""
        try:
            # Cerca il bottone settings o logout
            settings_xpath = "//span[contains(@id, 'user-info-settings-btnEl') or contains(@class, 'x-btn-icon-el-default-toolbar-small-settings')]"
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, settings_xpath)))
            return True
        except Exception:
            return False
    
    def _logout(self) -> bool:
        """
        Esegue il logout dal portale ISAB.
        Gestisce anche il popup 'Attenzione - modifiche non salvate'.
        """
        self.log("Tentativo di Logout...")
        try:
            # Click su pulsante Settings (ingranaggio)
            settings_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[@id='user-info-settings-btnEl' and contains(@class, 'x-btn-button')]"))
            )
            settings_button.click()
            self.log("Pulsante Settings cliccato.")
            
            # Click su "Esci"
            logout_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'x-menu-item-link')][.//span[normalize-space(text())='Esci']]"))
            )
            logout_option.click()
            self.log("Opzione 'Esci' cliccata.")
            
            time.sleep(1)
            
            # Gestisci popup "Attenzione - modifiche non salvate" se presente
            self._handle_unsaved_changes_popup()
            
            time.sleep(1)
            
            # Conferma logout cliccando su "Si" (popup di conferma logout standard)
            yes_button_xpath = "//a[contains(@class, 'x-btn') and @role='button'][.//span[normalize-space(text())='Si']]"
            try:
                yes_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, yes_button_xpath))
                )
                self.log("Pulsante 'Si' per conferma logout trovato.")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", yes_button)
                self.log("Logout confermato.")
                
                # Attesa per permettere al logout di completarsi
                time.sleep(3)
                
            except TimeoutException:
                # Potrebbe essere già stato gestito dal popup precedente
                self.log("Nessun ulteriore popup di conferma logout.")
            
            # Verifica ritorno alla pagina di login
            WebDriverWait(self.driver, 10).until(
                EC.url_contains(self.ISAB_URL.split("://")[1].split("/")[0])
            )
            self.log(f"✓ Logout completato. URL: {self.driver.current_url}")
            return True
            
        except TimeoutException:
            current_url = self.driver.current_url if self.driver else "N/A"
            self.log(f"⚠ Timeout durante il logout. URL attuale: {current_url}")
            # Verifica comunque se siamo sulla pagina di login
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "Username"))
                )
                self.log("Campo Username trovato. Logout probabilmente riuscito.")
                return True
            except TimeoutException:
                self.log("⚠ Logout incerto.")
                return False
        except Exception as e:
            self.log(f"✗ Errore durante il logout: {e}")
            return False
    
    def navigate_to_menu(self, menu_path: List[str]) -> bool:
        """
        Naviga attraverso i menu ExtJS.
        """
        self._check_stop()
        self.log(f"Navigazione: {' > '.join(menu_path)}")
        
        try:
            for menu_item in menu_path:
                self._check_stop()
                
                # Try multiple selectors for ExtJS menus
                selectors = [
                    f"//span[contains(text(), '{menu_item}')]",
                    f"//div[contains(text(), '{menu_item}')]",
                    f"//a[contains(text(), '{menu_item}')]",
                    f"//*[contains(@class, 'x-menu-item')][contains(text(), '{menu_item}')]",
                    f"//*[normalize-space(text())='{menu_item}']"
                ]
                
                clicked = False
                for selector in selectors:
                    try:
                        element = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        element.click()
                        clicked = True
                        self._attendi_scomparsa_overlay()
                        break
                    except (TimeoutException, ElementClickInterceptedException):
                        continue
                
                if not clicked:
                    self.log(f"✗ Impossibile cliccare su '{menu_item}'")
                    return False
            
            self.log("✓ Navigazione completata")
            return True
            
        except Exception as e:
            self.log(f"✗ Errore navigazione: {e}")
            return False
    
    def cleanup(self):
        """Chiude il browser e rilascia le risorse."""
        if self.driver:
            try:
                self.driver.quit()
                self.log("Browser chiuso")
            except Exception:
                pass
            self.driver = None
            self.wait = None
    
    @abstractmethod
    def run(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue la logica specifica del bot.
        """
        pass
    
    def _safe_login_with_retry(self, max_retries: int = 3) -> bool:
        """
        Inizializza driver e login con retry in caso di Proxy Error.
        """
        for attempt in range(1, max_retries + 1):
            self._check_stop()
            try:
                self._init_driver()
                if self._login():
                    return True

                # Se login fallisce (es. Proxy Error), chiudi e riprova
                self.log(f"Tentativo {attempt}/{max_retries} fallito. Riprovo tra 5 secondi...")
                self.cleanup()
                time.sleep(5)
            except Exception as e:
                self.log(f"Errore inizializzazione (Tentativo {attempt}): {e}")
                self.cleanup()
                time.sleep(5)

        self.log("✗ Tutti i tentativi di login sono falliti.")
        return False

    def execute(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue il workflow completo del bot.
        """
        self._stop_requested = False
        
        try:
            if not self._safe_login_with_retry():
                self.status = BotStatus.ERROR
                return False
            
            self.status = BotStatus.RUNNING
            result = self.run(data)
            
            self.status = BotStatus.COMPLETED if result else BotStatus.ERROR
            return result
            
        except InterruptedError:
            self.log("Bot interrotto")
            self.status = BotStatus.STOPPED
            return False
        except Exception as e:
            self.log(f"✗ Errore esecuzione: {e}")
            self.status = BotStatus.ERROR
            return False
        finally:
            self.cleanup()
    
    def execute_login_only(self) -> bool:
        """
        Esegue solo il login senza cleanup.
        """
        self._stop_requested = False
        
        try:
            self._init_driver()
            
            if not self._login():
                self.status = BotStatus.ERROR
                return False
            
            self.status = BotStatus.COMPLETED
            return True
            
        except InterruptedError:
            self.log("Bot interrotto")
            self.status = BotStatus.STOPPED
            self.cleanup()
            return False
        except Exception as e:
            self.log(f"✗ Errore esecuzione: {e}")
            self.status = BotStatus.ERROR
            self.cleanup()
            return False
