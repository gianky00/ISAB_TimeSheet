"""
Bot TS - Base Bot
Classe base astratta per tutti i bot di automazione con State Machine e Validazione.
"""

import logging
from abc import ABC, abstractmethod
from contextlib import suppress
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

logger = logging.getLogger(__name__)


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
        """
        Inizializza il bot base con credenziali e configurazioni driver.

        Args:
            username: Nome utente portale ISAB.
            password: Password portale ISAB.
            headless: Se True, avvia il browser senza interfaccia grafica.
            timeout: Tempo di attesa default per Selenium.
            download_path: Percorso dove scaricare i file.
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

        self._status = BotStatus.IDLE
        self._stop_requested = False
        self._log_callback: Optional[Callable[[str], None]] = None
        self._input_callback: Optional[Callable[[str], str]] = None
        self.login_page: Optional[LoginPage] = None
        self._telegram_service: Any = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Restituisce il nome identificativo del bot."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Restituisce una descrizione testuale delle funzionalità del bot."""
        pass

    @property
    def status(self) -> BotStatus:
        """Restituisce lo stato attuale della State Machine del bot."""
        return self._status

    @status.setter
    def status(self, value: BotStatus):
        """Aggiorna lo stato del bot e logga il cambiamento."""
        if self._status != value:
            self._status = value
            self.log(f"Stato: {value.name}")

    def validate_data(self, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        Esegue una validazione preventiva dei dati (Dry Run).
        Deve essere implementata dai bot derivati.

        Args:
            data: Lista di dizionari contenenti i dati da processare.
        Returns:
            tuple: (Successo, Messaggio di errore)
        """
        if not data:
            return False, "Nessun dato da elaborare."
        if not self.username or not self.password:
            return False, "Credenziali mancanti nelle impostazioni."
        return True, ""

    def log(self, message: str):
        """
        Logga un messaggio in console, nel widget log e via Telegram se configurato.

        Args:
            message: Testo del messaggio da loggare.
        """
        # print(f"[{self.name}] {message}")
        if self._log_callback:
            self._log_callback(message)

        # Log to file via logging framework
        logger.info(f"[{self.name}] {message}")
        if self._telegram_service:
            try:
                import re

                clean_msg = re.sub(
                    r"^[\\\\[]\\d{2}:\\d{2}:\\d{2}[\\\\]]\\s*", "", message.strip()
                )
                self._telegram_service.send_message_sync(
                    f"🔹 *{self.name}*\n{clean_msg}"
                )
            except Exception:
                pass

    def set_log_callback(self, callback: Callable[[str], None]):
        """Imposta la callback per inoltrare i log all'interfaccia utente."""
        self._log_callback = callback

    def set_telegram_service(self, service: Any):
        """Imposta il servizio Telegram per l'invio di notifiche."""
        self._telegram_service = service

    def set_input_callback(self, callback: Callable[[str], str]):
        """Imposta la callback per richiedere input interattivo all'utente."""
        self._input_callback = callback

    def request_stop(self):
        """Segnala al bot di interrompere l'esecuzione alla prima occasione sicura."""
        self._stop_requested = True
        self.log("⚠️ Interruzione richiesta...")

    def _check_stop(self):
        """Verifica se è stata richiesta l'interruzione e solleva InterruptedError."""
        if self._stop_requested:
            raise InterruptedError("Bot interrotto dall'utente")

    def _init_driver(self):
        """Inizializzazione del driver Chrome con opzioni e configurazioni specifiche."""
        self.log("Inizializzazione browser...")
        self.status = BotStatus.INITIALIZING

        options = self._get_chrome_options()
        driver_path = self._get_chromedriver_path()
        service = Service(driver_path) if driver_path else None

        try:
            # Type narrowing for mypy
            if not service:
                raise RuntimeError("Chromedriver service non disponibile")
            self._setup_driver_instance(service, options)
            self._configure_waits_and_pages()
        except Exception as e:
            self._handle_driver_error(e)

    def _get_chrome_options(self) -> Options:
        """Configura e restituisce le opzioni di Chrome per massimizzare stabilità e performance."""
        options = Options()
        # Argomenti standard
        args = [
            "--disable-features=DownloadBubble,DownloadBubbleV2",
            "--disable-notifications",
            "--disable-infobars",
            "--disable-popup-blocking",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--start-maximized",
            "--no-restore-session-state",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--remote-debugging-port=9222",
            "--disable-software-rasterizer",
        ]
        for arg in args:
            options.add_argument(arg)

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Gestione Headless
        config = config_manager.load_config()
        if self.headless or config.get("browser_headless", False):
            self.headless = True
            options.add_argument("--headless=new")
            options.add_argument(f"--window-size={BrowserConfig.WINDOW_SIZE}")

        # Directory Profilo e Preferenze
        profile_dir = config_manager.CONFIG_DIR / "data" / BrowserConfig.CACHE_DIR_NAME
        options.add_argument(f"user-data-dir={profile_dir}")

        prefs: Dict[str, Any] = {
            "profile.default_content_setting_values.automatic_downloads": 1,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
        }

        if self.download_path:
            import os

            prefs["download.default_directory"] = os.path.abspath(self.download_path)

        options.add_experimental_option("prefs", prefs)
        return options

    def _get_chromedriver_path(self) -> Optional[str]:
        """Tenta di ottenere il path di chromedriver scaricandolo automaticamente o via fallback locale."""
        # 1. Automatico
        try:
            self.log("Verifica aggiornamenti driver...")
            path = ChromeDriverManager().install()
            if not path.lower().endswith(".exe"):
                potential = list(Path(path).parent.rglob("chromedriver.exe"))
                if potential:
                    path = str(potential[0])
            return path
        except Exception as e:
            self.log(f"⚠️ Impossibile scaricare driver automatico: {e}")

        # 2. Locale Fallback
        local_driver = Path("drivers") / "chromedriver.exe"
        if local_driver.exists():
            path = str(local_driver.absolute())
            self.log(f"Usando driver locale: {path}")
            return path
        return None

    def _setup_driver_instance(self, service: Service, options: Options):
        """Crea l'istanza di webdriver.Chrome applicando tecniche anti-detection."""
        self.driver = webdriver.Chrome(service=service, options=options)
        # Anti-detection
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            },
        )

    def _configure_waits_and_pages(self):
        """Inizializza gli oggetti WebDriverWait per diverse durate e la LoginPage."""
        if not self.driver:
            return
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.popup_wait = WebDriverWait(self.driver, Timeouts.SHORT)
        self.long_wait = WebDriverWait(self.driver, Timeouts.PAGE_LOAD)
        self.login_page = LoginPage(self.driver, self.wait, self.log, self.ISAB_URL)

    def _handle_driver_error(self, e: Exception):
        """Gestisce gli errori critici di avvio del driver Chrome."""
        msg = f"❌ ERRORE CRITICO DRIVER: {e}"
        self.log(msg)
        err_str = str(e).lower()
        if "chrome instance exited" in err_str:
            self.log(
                "💡 SUGGERIMENTO: Chrome è crashato all'avvio (Sandbox/Version Mismatch)."
            )
            self.log("   - Assicurati che Chrome sia aggiornato.")
        elif "sessionnotcreatedexception" in err_str or "version" in err_str:
            self.log(
                "💡 SUGGERIMENTO: La tua versione di Chrome è troppo recente o obsoleta."
            )
            self.log("   1. Aggiorna Google Chrome all'ultima versione.")
            self.log("   2. Oppure scarica manualmente 'chromedriver.exe' compatibile.")
        raise e

    def execute(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue il workflow completo del bot: Validazione -> Accesso -> Esecuzione -> Cleanup.

        Args:
            data: Lista di dati da elaborare.
        Returns:
            bool: True se l'intera esecuzione ha avuto successo.
        """
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
        """Salva uno screenshot e il sorgente HTML corrente per il debug post-mortem."""
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

        except Exception as e:
            self.log(f"⚠️ Impossibile salvare lo stato di errore: {e}")

    def _login(self) -> bool:
        """Esegue il login al portale ISAB usando la LoginPage."""
        if self.login_page:
            return self.login_page.login(self.username, self.password)
        return False

    def _attendi_scomparsa_overlay(self, timeout=None):
        """Attende che gli overlay di caricamento del portale ISAB scompaiano."""
        if self.login_page:
            if timeout:
                return self.login_page._attendi_scomparsa_overlay(timeout)
            return self.login_page._attendi_scomparsa_overlay()
        return True

    def _verify_login(self) -> bool:
        """Verifica se l'utente è attualmente loggato analizzando l'UI."""
        if self.login_page:
            return self.login_page._verify_logged_in_via_ui()
        return False

    def _verify_logged_in_via_ui(self) -> bool:
        """Alias per _verify_login compatibile con i test legacy."""
        return self._verify_login()

    def _handle_session_popup(self):
        """Gestisce il popup di sessione multipla cliccando su 'SI'."""
        with suppress(Exception):
            if self.popup_wait:
                btn = self.popup_wait.until(
                    EC.element_to_be_clickable(CommonLocators.POPUP_SESSION_YES)
                )
                btn.click()
                self.log("✅ Popup sessione gestito (SI).")
                return True
        return False

    def _safe_login_with_retry(self, max_retries: int = 2) -> bool:
        """
        Tenta il login con un numero limitato di riprova in caso di errori driver.

        Args:
            max_retries: Numero massimo di tentativi.
        Returns:
            bool: True se il login ha avuto successo.
        """
        for _attempt in range(1, max_retries + 1):
            self._check_stop()
            try:
                self._init_driver()
                if self._login():
                    return True
                self.cleanup()
                # No sleep needed: _init_driver() has internal waits
            except Exception as e:
                self.log(f"⚠️ Errore tentativo {_attempt}: {e}")
                self.cleanup()
                # No sleep needed: cleanup() is synchronous
        return False

    def cleanup(self):
        """Chiude il browser e pulisce le risorse del driver."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None

    @abstractmethod
    def run(self, data: List[Dict[str, Any]]) -> bool:
        """
        Logica principale dell'automazione da implementare nelle sottoclassi.

        Args:
            data: Dati validati da processare.
        Returns:
            bool: True se l'esecuzione è completata correttamente.
        """
        pass
