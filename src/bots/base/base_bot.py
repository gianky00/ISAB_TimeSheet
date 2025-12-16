"""
Bot TS - Base Bot
Classe base astratta per tutti i bot di automazione.
"""
import os
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Callable, List, Dict, Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    ISAB_URL = "https://portal.isab.com"
    
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
        """Inizializza il driver Chrome con anti-detection."""
        self.log("Inizializzazione browser...")
        self.status = BotStatus.INITIALIZING
        
        options = Options()
        
        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Performance
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        
        # Headless mode
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        
        # Download configuration
        if self.download_path and os.path.isdir(self.download_path):
            prefs = {
                "download.default_directory": self.download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option("prefs", prefs)
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver flag
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
        )
        
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.log("✓ Browser inizializzato")
    
    def _login(self) -> bool:
        """
        Esegue il login al portale ISAB.
        
        Returns:
            True se il login ha successo, False altrimenti
        """
        self._check_stop()
        self.log("Accesso al portale ISAB...")
        self.status = BotStatus.LOGGING_IN
        
        try:
            self.driver.get(self.ISAB_URL)
            time.sleep(2)
            
            # Wait for login form
            self._check_stop()
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            password_field = self.driver.find_element(By.ID, "password")
            
            # Clear and fill fields
            username_field.clear()
            username_field.send_keys(self.username)
            
            password_field.clear()
            password_field.send_keys(self.password)
            
            # Submit
            password_field.send_keys(Keys.RETURN)
            self.log("Credenziali inviate...")
            
            time.sleep(3)
            self._check_stop()
            
            # Handle "new session" popup if present
            self._handle_new_session_popup()
            
            # Verify login success
            time.sleep(2)
            if self._verify_login():
                self.log("✓ Login effettuato con successo")
                return True
            else:
                self.log("✗ Login fallito - verifica credenziali")
                return False
                
        except TimeoutException:
            self.log("✗ Timeout durante il login")
            return False
        except Exception as e:
            self.log(f"✗ Errore login: {e}")
            return False
    
    def _handle_new_session_popup(self):
        """Gestisce il popup 'altro utente connesso'."""
        try:
            # Look for OK button in popup
            ok_buttons = self.driver.find_elements(
                By.XPATH, 
                "//button[contains(text(), 'OK') or contains(text(), 'Sì') or contains(text(), 'Si')]"
            )
            
            for btn in ok_buttons:
                if btn.is_displayed():
                    btn.click()
                    self.log("✓ Popup sessione gestito")
                    time.sleep(1)
                    return
            
            # Try ExtJS button style
            ext_buttons = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".x-btn-text, .x-btn-inner"
            )
            
            for btn in ext_buttons:
                if btn.text.upper() in ["OK", "SÌ", "SI", "YES"]:
                    btn.click()
                    self.log("✓ Popup sessione gestito (ExtJS)")
                    time.sleep(1)
                    return
                    
        except Exception:
            pass  # No popup present
    
    def _verify_login(self) -> bool:
        """Verifica se il login è avvenuto con successo."""
        try:
            # Check for common post-login elements
            # This might need adjustment based on ISAB portal structure
            return "login" not in self.driver.current_url.lower()
        except Exception:
            return False
    
    def navigate_to_menu(self, menu_path: List[str]) -> bool:
        """
        Naviga attraverso i menu ExtJS.
        
        Args:
            menu_path: Lista di elementi menu da cliccare in sequenza
            
        Returns:
            True se la navigazione ha successo
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
                    f"//*[contains(@class, 'x-menu-item')][contains(text(), '{menu_item}')]"
                ]
                
                clicked = False
                for selector in selectors:
                    try:
                        element = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        element.click()
                        clicked = True
                        time.sleep(1)
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
        
        Args:
            data: Dati da processare (es. lista di commesse)
            
        Returns:
            True se l'esecuzione ha successo
        """
        pass
    
    def execute(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue il workflow completo del bot.
        
        Args:
            data: Dati da processare
            
        Returns:
            True se l'esecuzione ha successo
        """
        self._stop_requested = False
        
        try:
            self._init_driver()
            
            if not self._login():
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
        Utile per bot che lasciano il browser aperto.
        
        Returns:
            True se il login ha successo
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
        # Note: No cleanup here - browser stays open
