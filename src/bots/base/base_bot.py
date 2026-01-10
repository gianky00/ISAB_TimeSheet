"""
Bot TS - Base Bot
Classe base astratta per tutti i bot di automazione con State Machine e Validazione.
"""

import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from src.bots.base.login_page import LoginPage
from src.bots.portale_fornitori.common.locators import CommonLocators
from src.core import config_manager
from src.core.constants import BotStatus, BrowserConfig, Timeouts, URLs


class BaseBot(ABC):
    """
    Abstract base class for all ISAB bots.
    """

    ISAB_URL = URLs.ISAB_PORTAL

    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = Timeouts.DEFAULT,
        download_path: str = "",
    ):
        self.username = username
        self.password = password
        self.headless = headless
        self.timeout = timeout
        self.download_path = download_path

        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.popup_wait: Optional[WebDriverWait] = None
        self.long_wait: Optional[WebDriverWait] = None

        self._status = BotStatus.IDLE
        self._stop_requested = False
        self._log_callback: Optional[Callable[[str], None]] = None
        self._input_callback: Optional[Callable[[str], str]] = None
        self.login_page: Optional[LoginPage] = None
        self._telegram_service: Any = None

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    def status(self) -> BotStatus:
        return self._status

    @status.setter
    def status(self, value: BotStatus):
        if self._status != value:
            self._status = value
            self.log(f"Stato: {value.name}")

    def validate_data(self, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        Esegue una validazione preventiva dei dati (Dry Run).
        Deve essere implementata dai bot derivati.
        """
        if not data:
            return False, "Nessun dato da elaborare."
        if not self.username or not self.password:
            return False, "Credenziali mancanti nelle impostazioni."
        return True, ""

    def log(self, message: str):
        """Log a message e inoltra al servizio Telegram."""
        print(f"[{self.name}] {message}")
        if self._log_callback:
            self._log_callback(message)
        if self._telegram_service:
            try:
                import re

                clean_msg = re.sub(
                    r"^[\\\[]\d{2}:\d{2}:\d{2}[\\\]]\s*", "", message.strip()
                )
                self._telegram_service.send_message_sync(
                    f"🔹 *{self.name}*\n{clean_msg}"
                )
            except Exception:
                pass

    def set_telegram_service(self, service: Any):
        self._telegram_service = service

    def set_log_callback(self, callback: Callable[[str], None]):
        self._log_callback = callback

    def set_input_callback(self, callback: Callable[[str], str]):
        self._input_callback = callback

    def request_stop(self):
        self._stop_requested = True
        self.log("⚠️ Interruzione richiesta...")

    def _check_stop(self):
        if self._stop_requested:
            raise InterruptedError("Bot interrotto dall'utente")

    def _init_driver(self):
        self.log("Inizializzazione browser...")
        self.status = BotStatus.INITIALIZING

        options = Options()
        options.add_argument("--disable-features=DownloadBubble,DownloadBubbleV2")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--no-restore-session-state")

        config = config_manager.load_config()
        # Headless logic: prioritize parameter, then config
        is_headless = self.headless or config.get("browser_headless", False)
        if is_headless:
            self.headless = True
            options.add_argument("--headless=new")
            options.add_argument(f"--window-size={BrowserConfig.WINDOW_SIZE}")

        profile_dir = config_manager.CONFIG_DIR / "data" / BrowserConfig.CACHE_DIR_NAME
        options.add_argument(f"user-data-dir={profile_dir}")

        prefs = {
            "profile.default_content_setting_values.automatic_downloads": 1,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)

    def _init_driver(self):
        self.log("Inizializzazione browser...")
        self.status = BotStatus.INITIALIZING

        options = Options()
        options.add_argument("--disable-features=DownloadBubble,DownloadBubbleV2")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--no-restore-session-state")

        config = config_manager.load_config()
        # Headless logic: prioritize parameter, then config
        is_headless = self.headless or config.get("browser_headless", False)
        if is_headless:
            self.headless = True
            options.add_argument("--headless=new")
            options.add_argument(f"--window-size={BrowserConfig.WINDOW_SIZE}")

        profile_dir = config_manager.CONFIG_DIR / "data" / BrowserConfig.CACHE_DIR_NAME
        options.add_argument(f"user-data-dir={profile_dir}")

        prefs = {
            "profile.default_content_setting_values.automatic_downloads": 1,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)

        driver_path = None
        service = None

        # 1. Tentativo con ChromeDriverManager (Network)
        try:
            self.log("Verifica aggiornamenti driver...")
            installed_path = ChromeDriverManager().install()
            # Fix per alcuni ambienti Windows dove il path non ha .exe
            if not installed_path.lower().endswith(".exe"):
                potential_exe = list(Path(installed_path).parent.rglob("chromedriver.exe"))
                if potential_exe:
                    installed_path = str(potential_exe[0])
            driver_path = installed_path
            self.log(f"Driver scaricato: {driver_path}")
        except Exception as e:
            self.log(f"⚠️ Impossibile scaricare driver automatico: {e}")
        
        # 2. Tentativo Fallback Locale (Cartella 'drivers' o 'bin')
        if not driver_path:
            local_driver = Path("drivers") / "chromedriver.exe"
            if local_driver.exists():
                driver_path = str(local_driver.absolute())
                self.log(f"Usando driver locale: {driver_path}")

        # 3. Tentativo creazione Service
        if driver_path:
            service = Service(driver_path)

        try:
            # Se service è None, Selenium cercherà nel PATH
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Anti-detection script
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                },
            )

            self.wait = WebDriverWait(self.driver, self.timeout)
            self.popup_wait = WebDriverWait(self.driver, Timeouts.SHORT)
            self.long_wait = WebDriverWait(self.driver, Timeouts.PAGE_LOAD)
            self.login_page = LoginPage(self.driver, self.wait, self.log, self.ISAB_URL)

        except Exception as e:
            msg = f"❌ ERRORE CRITICO DRIVER: {e}"
            self.log(msg)
            
            # User-friendly hint
            if "SessionNotCreatedException" in str(e) or "version" in str(e).lower():
                self.log("💡 SUGGERIMENTO: La tua versione di Chrome è troppo recente o obsoleta.")
                self.log("   1. Aggiorna Google Chrome all'ultima versione.")
                self.log("   2. Oppure scarica manualmente 'chromedriver.exe' compatibile e mettilo nella cartella 'drivers'.")
            
            raise

    def execute(self, data: List[Dict[str, Any]]) -> bool:
        """Workflow completo: Validazione -> Browser -> Esecuzione."""
        self._stop_requested = False
        self.log(f"Avvio {self.name}...")

        # 1. Validazione Preventiva
        self.status = BotStatus.IDLE
        valid, error_msg = self.validate_data(data)
        if not valid:
            self.log(f"❌ Validazione fallita: {error_msg}")
            self.status = BotStatus.ERROR
            return False

        try:
            # 2. Inizializzazione Browser
            if not self._safe_login_with_retry():
                self.status = BotStatus.ERROR
                return False

            # 3. Esecuzione
            self.status = BotStatus.RUNNING
            result = self.run(data)

            self.status = BotStatus.COMPLETED if result else BotStatus.ERROR
            return result

        except InterruptedError:
            self.log("Bot interrotto")
            self.status = BotStatus.STOPPED
            return False
        except Exception as e:
            self.log(f"✗ Errore fatale: {e}")
            self._save_error_state(str(e))
            self.status = BotStatus.ERROR
            return False
        finally:
            self.cleanup()

    def _save_error_state(self, error_msg: str):
        """Salva screenshot e sorgente HTML in caso di errore."""
        if not self.driver:
            return

        try:
            from datetime import datetime
            from src.core.config_manager import CONFIG_DIR
            
            error_dir = CONFIG_DIR / "logs" / "errors"
            error_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = self.name.replace(" ", "_").lower()
            
            # 1. Screenshot
            screenshot_path = error_dir / f"error_{safe_name}_{timestamp}.png"
            self.driver.save_screenshot(str(screenshot_path))
            
            # 2. HTML Source
            html_path = error_dir / f"error_{safe_name}_{timestamp}.html"
            html_path.write_text(self.driver.page_source, encoding="utf-8")
            
            self.log(f"📸 Stato errore salvato in: {error_dir.name}")
            
            # 3. Notifica Telegram con dettaglio (opzionale se il messaggio è troppo lungo)
            if self._telegram_service:
                # Invia solo il percorso dello screenshot per brevità
                pass

        except Exception as e:
            self.log(f"⚠️ Impossibile salvare lo stato di errore: {e}")

    def _login(self) -> bool:
        """Default login implementation using LoginPage."""
        if self.login_page:
            return self.login_page.login(self.username, self.password)
        return False

    def _attendi_scomparsa_overlay(self, timeout=None):
        """Proxy to LoginPage."""
        if self.login_page:
            if timeout:
                return self.login_page._attendi_scomparsa_overlay(timeout)
            return self.login_page._attendi_scomparsa_overlay()
        return True

    def _verify_login(self) -> bool:
        """Proxy to verify login."""
        if self.login_page:
            return self.login_page._verify_logged_in_via_ui()
        return False

    def _verify_logged_in_via_ui(self) -> bool:
        """Alias for _verify_login to satisfy tests/legacy."""
        return self._verify_login()

    def _logout(self) -> bool:
        """Logout da ISAB."""
        try:
            self.log("🚪 Eseguo il logout...")
            # 1. Clicca su impostazioni (ingranaggio)
            self.wait.until(EC.element_to_be_clickable(CommonLocators.SETTINGS_BUTTON)).click()
            time.sleep(0.5)
            # 2. Clicca su Esci
            self.wait.until(EC.element_to_be_clickable(CommonLocators.LOGOUT_OPTION)).click()
            self.log("✅ Logout effettuato.")
            return True
        except Exception as e:
            self.log(f"⚠️ Logout fallito: {e}")
            return False

    def navigate_to_menu(self, menu_path: List[str]) -> bool:
        """Navigate to a specific menu."""
        # Placeholder - implement if needed or used
        return True

    def _handle_unsaved_changes_popup(self):
        """Handle eventual 'unsaved changes' popup."""
        pass

    def _handle_session_popup(self):
        """Gestisce popup di sessione scaduta/esistente."""
        try:
            if self.popup_wait:
                btn = self.popup_wait.until(EC.element_to_be_clickable(CommonLocators.POPUP_SESSION_YES))
                btn.click()
                self.log("✅ Popup sessione gestito (SI).")
                return True
        except Exception:
            pass
        return False

    def _handle_ok_popup(self):
        """Gestisce popup OK generici."""
        try:
            if self.popup_wait:
                btn = self.popup_wait.until(EC.element_to_be_clickable(CommonLocators.POPUP_OK))
                btn.click()
                self.log("✅ Popup OK gestito.")
                return True
        except Exception:
            pass
        return False

    def _safe_login_with_retry(self, max_retries: int = 2) -> bool:
        for _attempt in range(1, max_retries + 1):
            self._check_stop()
            try:
                self._init_driver()
                if self._login():
                    return True
                self.cleanup()
                time.sleep(3)
            except Exception as e:
                self.log(f"⚠️ Errore tentativo {_attempt}: {e}")
                self.cleanup()
                time.sleep(3)
        return False

    def cleanup(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None

    @abstractmethod
    def run(self, data: List[Dict[str, Any]]) -> bool:
        pass
