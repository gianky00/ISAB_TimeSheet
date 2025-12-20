"""
Bot TS - Base Bot
Classe base astratta per tutti i bot di automazione.
"""
import os
import time
import shutil
from abc import ABC, abstractmethod
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

from src.core.constants import URLs, Timeouts, BotStatus, BrowserConfig
from src.bots.common.locators import LoginLocators, CommonLocators

class BaseBot(ABC):
    """
    Abstract base class for all ISAB bots.
    
    Provides:
    - Selenium/Chrome management with anti-detection
    - Login to ISAB portal
    - Popup management
    - ExtJS menu navigation
    - Logging callback system
    - Stop mechanism
    """
    
    ISAB_URL = URLs.ISAB_PORTAL
    
    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = Timeouts.DEFAULT,
        download_path: str = ""
    ):
        """
        Initialize the bot.
        
        Args:
            username: ISAB Username
            password: ISAB Password
            headless: If True, run Chrome in headless mode
            timeout: Timeout in seconds for waits
            download_path: Path for downloads (empty = default)
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
        """Name of the bot."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the bot."""
        pass
    
    def set_log_callback(self, callback: Callable[[str], None]):
        """Set the logging callback."""
        self._log_callback = callback
    
    def log(self, message: str):
        """Log a message."""
        print(f"[{self.name}] {message}")
        if self._log_callback:
            self._log_callback(message)
    
    def request_stop(self):
        """Request bot interruption."""
        self._stop_requested = True
        self.log("⚠️ Interruzione richiesta...")
    
    def _check_stop(self):
        """Check if interruption was requested."""
        if self._stop_requested:
            raise InterruptedError("Bot interrotto dall'utente")
    
    def _init_driver(self):
        """Initialize Chrome driver with optimized configuration."""
        self.log("Inizializzazione browser...")
        self.status = BotStatus.INITIALIZING
        
        options = Options()
        
        # --- 1. UI & POPUP DISABLE ---
        options.add_argument("--disable-features=DownloadBubble,DownloadBubbleV2")
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_argument("--no-restore-session-state")
        options.add_argument("--disable-session-crashed-bubble")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        
        # --- 2. ANTI-DETECTION ---
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # --- 3. PERFORMANCE ---
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-proxy-server")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument(f"--window-size={BrowserConfig.WINDOW_SIZE}")

        # Eager load strategy for speed
        options.page_load_strategy = 'eager'

        # --- 4. CACHING & PERSISTENT PROFILE ---
        profile_dir = Path(f"data/{BrowserConfig.CACHE_DIR_NAME}").absolute()
        options.add_argument(f"user-data-dir={profile_dir}")
        self.log(f"Cache profilo attiva: {profile_dir}")

        # --- 5. USER PREFERENCES ---
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "users.users_allowed_to_save_passwords": False,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.automatic_downloads": 1,
            "plugins.always_open_pdf_externally": True,
            "safebrowsing.enabled": True, 
            "safebrowsing.disable_download_protection": True,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "browser.download.manager.showWhenStarting": False,
            "download.manager.showWhenStarting": False,
        }

        options.add_argument("--safebrowsing-disable-download-protection")
        options.add_argument("--safebrowsing-disable-extension-blacklist")
        options.add_experimental_option("prefs", prefs)
        
        # --- 6. DRIVER INSTALLATION (Robust handling for WinError 193) ---
        driver_path = None
        try:
            driver_path = ChromeDriverManager().install()
            self.log(f"Driver installato in: {driver_path}")

            # --- FIX FOR BAD WEBDRIVER PATH (THIRD_PARTY_NOTICES) ---
            # Recent webdriver-manager versions sometimes return the LICENSE file path
            # or the wrong file in the zip. We must ensure it's the executable.
            path_obj = Path(driver_path)
            if not driver_path.lower().endswith(".exe"):
                self.log(f"⚠️ Il path del driver non è un eseguibile: {driver_path}")
                # Look for chromedriver.exe in the same directory or parent
                potential_exe = list(path_obj.parent.rglob("chromedriver.exe"))
                if potential_exe:
                    driver_path = str(potential_exe[0])
                    self.log(f"✅ Trovato eseguibile corretto: {driver_path}")
                else:
                    self.log("❌ Impossibile trovare chromedriver.exe nella cartella.")

        except Exception as e:
            # WinError 193 means corrupted binary or arch mismatch
            if "WinError 193" in str(e) or "valid Win32" in str(e):
                self.log("⚠️ Rilevato driver corrotto (WinError 193). Tento pulizia forzata...")

                # Attempt to find the folder and delete it
                try:
                    wdm_root = Path.home() / ".wdm"
                    if wdm_root.exists():
                        self.log(f"Eliminazione cache driver: {wdm_root}")
                        shutil.rmtree(wdm_root, ignore_errors=True)
                        self.log("Cache eliminata. Riprovo download...")

                        # Retry install
                        time.sleep(2)
                        driver_path = ChromeDriverManager().install()

                        # Apply path fix again
                        path_obj = Path(driver_path)
                        if not driver_path.lower().endswith(".exe"):
                            potential_exe = list(path_obj.parent.rglob("chromedriver.exe"))
                            if potential_exe:
                                driver_path = str(potential_exe[0])

                        self.log(f"Driver reinstallato con successo: {driver_path}")
                except Exception as cleanup_error:
                    self.log(f"❌ Impossibile pulire/reinstallare driver: {cleanup_error}")
                    raise e
            else:
                self.log(f"❌ Errore installazione driver: {e}")
                raise e

        # Initialize Service
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver flag (JS side)
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
        )
        
        # Setup waits
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.popup_wait = WebDriverWait(self.driver, Timeouts.SHORT)
        self.long_wait = WebDriverWait(self.driver, Timeouts.PAGE_LOAD)
        
        self.log("✓ Browser inizializzato (Modalità Silenziosa)")
    
    def _attendi_scomparsa_overlay(self, timeout_secondi: int = Timeouts.OVERLAY) -> bool:
        """
        Waits for Ext JS loading overlays to disappear.
        """
        try:
            overlay_wait = WebDriverWait(self.driver, timeout_secondi)
            # Combine selectors for efficiency
            xpath_combined = f"{CommonLocators.LOADING_MASK[1]} | {CommonLocators.LOADING_TEXT[1]}"
            
            overlay_wait.until(EC.invisibility_of_element_located((By.XPATH, xpath_combined)))
            self.log(" -> Overlay di caricamento scomparso.")
            time.sleep(0.3)
            return True
        except TimeoutException:
            self.log(f"⚠ Timeout ({timeout_secondi}s) attesa overlay. Proseguo con cautela.")
            return False
    
    def _perform_login_form_action(self):
        """Fills login form and clicks Enter."""
        username_field = self.wait.until(
            EC.element_to_be_clickable(LoginLocators.USERNAME_FIELD)
        )
        username_field.clear()
        username_field.send_keys(self.username)

        password_field = self.wait.until(
            EC.element_to_be_clickable(LoginLocators.PASSWORD_FIELD)
        )
        password_field.clear()
        password_field.send_keys(self.password)

        try:
            # Standard click
            accedi_btn = self.wait.until(
                EC.element_to_be_clickable(LoginLocators.LOGIN_BUTTON)
            )
            accedi_btn.click()
        except (TimeoutException, ElementClickInterceptedException):
            self.log("⚠️ Click standard intercettato o timeout. Tento click JavaScript...")
            # Fallback: JavaScript click
            accedi_element = self.driver.find_element(*LoginLocators.LOGIN_BUTTON_FALLBACK)
            self.driver.execute_script("arguments[0].click();", accedi_element)

        self.log("Login effettuato. Attendo scomparsa overlay...")
        self._attendi_scomparsa_overlay(Timeouts.LONG)

    def _login(self) -> bool:
        """
        Performs login to ISAB portal.
        Returns False if Proxy Error is detected.
        """
        self._check_stop()
        self.log(f"Navigazione a: {self.ISAB_URL}")
        self.status = BotStatus.LOGGING_IN
        
        try:
            self.driver.get(self.ISAB_URL)
            
            # Check Proxy Error
            if "Proxy Error" in self.driver.title or "Proxy Error" in self.driver.page_source:
                self.log("⚠ Rilevato 'Proxy Error' durante l'accesso iniziale.")
                return False

            self.log("Tentativo di login...")
            self._attendi_scomparsa_overlay(timeout_secondi=10)

            # Check for existing session
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(LoginLocators.USERNAME_FIELD)
                )
                self._perform_login_form_action()

            except TimeoutException:
                self.log("Campo Username non trovato. Verifico se già loggato...")
                if self._verify_logged_in_via_ui():
                    self.log("✓ Rilevata sessione attiva (skip login).")
                    return True
                else:
                    self.log("⚠️ Username assente e sessione invalida/scaduta.")
                    self.log("🔄 Ricarico la pagina per forzare il form di login...")
                    self.driver.refresh()
                    self._attendi_scomparsa_overlay(10)

                    try:
                        self._perform_login_form_action()
                        return True
                    except Exception as e:
                        self.log(f"✗ Fallito recupero sessione: {e}")
                        return False
            
            self._check_stop()
            self._handle_session_popup()
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
        """Handles 'Active Session' popup."""
        try:
            si_button = self.popup_wait.until(EC.element_to_be_clickable(CommonLocators.POPUP_SESSION_YES))
            self.log("Pop-up 'Sessione attiva' trovato. Click su 'Si'...")
            si_button.click()
            self._attendi_scomparsa_overlay(10)
        except TimeoutException:
            pass
    
    def _handle_ok_popup(self):
        """Handles generic OK popup."""
        try:
            ok_button = self.popup_wait.until(
                EC.element_to_be_clickable(CommonLocators.POPUP_OK)
            )
            self.log("Pop-up 'OK' trovato. Click...")
            ok_button.click()
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(CommonLocators.POPUP_OK)
            )
            self.log("Popup gestito.")
        except TimeoutException:
            pass
    
    def _handle_new_session_popup(self):
        """Alias for backward compatibility."""
        self._handle_session_popup()
        self._handle_ok_popup()
    
    def _handle_unsaved_changes_popup(self):
        """Handles 'Unsaved Changes' popup."""
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(CommonLocators.POPUP_ATTENTION_HEADER)
            )
            
            self.log("Pop-up 'Attenzione - modifiche non salvate' trovato. Click su 'Si'...")
            
            si_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(CommonLocators.POPUP_YES_BUTTON)
            )
            
            try:
                si_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", si_button)
            
            self.log("Popup 'Attenzione' gestito - cliccato 'Si'.")
            time.sleep(0.5)
            return True
            
        except TimeoutException:
            pass
        except Exception as e:
            self.log(f"Errore gestione popup Attenzione: {e}")
        
        return False
    
    def _verify_login(self) -> bool:
        """Verifies if login was successful."""
        try:
            return "login" not in self.driver.current_url.lower()
        except Exception:
            return False

    def _verify_logged_in_via_ui(self) -> bool:
        """Checks for post-login UI elements."""
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CommonLocators.SETTINGS_BUTTON))
            return True
        except Exception:
            return False
    
    def _logout(self) -> bool:
        """Performs logout."""
        self.log("Tentativo di Logout...")
        try:
            settings_button = self.wait.until(
                EC.element_to_be_clickable(CommonLocators.SETTINGS_BUTTON)
            )
            settings_button.click()
            self.log("Pulsante Settings cliccato.")
            
            logout_option = self.wait.until(
                EC.element_to_be_clickable(CommonLocators.LOGOUT_OPTION)
            )
            logout_option.click()
            self.log("Opzione 'Esci' cliccata.")
            
            time.sleep(1)
            self._handle_unsaved_changes_popup()
            time.sleep(1)
            
            # Confirm Logout (Standard 'Si' button)
            try:
                yes_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(CommonLocators.POPUP_SESSION_YES)
                )
                self.log("Pulsante 'Si' per conferma logout trovato.")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", yes_button)
                self.log("Logout confermato.")
                time.sleep(3)
                
            except TimeoutException:
                self.log("Nessun ulteriore popup di conferma logout.")
            
            WebDriverWait(self.driver, 10).until(
                EC.url_contains(self.ISAB_URL.split("://")[1].split("/")[0])
            )
            self.log(f"✓ Logout completato. URL: {self.driver.current_url}")
            return True
            
        except TimeoutException:
            current_url = self.driver.current_url if self.driver else "N/A"
            self.log(f"⚠ Timeout durante il logout. URL attuale: {current_url}")
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(LoginLocators.USERNAME_FIELD)
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
        """Navigates through ExtJS menus."""
        self._check_stop()
        self.log(f"Navigazione: {' > '.join(menu_path)}")
        
        try:
            for menu_item in menu_path:
                self._check_stop()
                
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
        """Closes browser and releases resources."""
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
        """Main execution logic."""
        pass
    
    def _safe_login_with_retry(self, max_retries: int = 3) -> bool:
        """Initializes driver and login with retry mechanism."""
        for attempt in range(1, max_retries + 1):
            self._check_stop()
            try:
                self._init_driver()
                if self._login():
                    return True

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
        """Executes full bot workflow."""
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
        """Executes only login."""
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
