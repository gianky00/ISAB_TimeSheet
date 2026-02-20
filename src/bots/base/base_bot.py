"""
Bot TS - Base Bot
Classe base astratta per tutti i bot di automazione con State Machine e Validazione.
"""

import re
import sys
from abc import ABC, abstractmethod
from collections.abc import Callable
from contextlib import suppress
from enum import Enum, auto
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal
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
from src.core.logging import generate_trace_id, get_logger, measure_time, with_context


class StepStatus(Enum):
    """Stati possibili per uno step della timeline."""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    ERROR = auto()


class BotSignals(QObject):
    """Segnali PyQt6 per la comunicazione bot -> GUI."""
    step_changed = pyqtSignal(int, str, object)  # index, name, status (StepStatus)
    status_changed = pyqtSignal(object)         # BotStatus
    log_emitted = pyqtSignal(str, str)          # message, level


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
    ) -> None:
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

        self.driver: webdriver.Chrome | None = None
        self.wait: WebDriverWait[webdriver.Chrome] | None = None
        self.popup_wait: WebDriverWait[webdriver.Chrome] | None = None
        self.long_wait: WebDriverWait[webdriver.Chrome] | None = None

        self._status = BotStatus.IDLE
        self._stop_requested = False
        self._log_callback: Callable[[str], None] | None = None
        self._input_callback: Callable[[str], str] | None = None
        self.login_page: LoginPage | None = None
        self._telegram_service: Any = None

        # Nuova gestione Step
        self.signals = BotSignals()
        self._current_step_index = -1
        self._steps_state: list[StepStatus] = []

        # Enterprise logging
        self._trace_id = generate_trace_id()
        self._logger = get_logger(f"bot.{self.__class__.__name__}")

    @property
    @abstractmethod
    def name(self) -> str:
        """Restituisce il nome identificativo del bot."""

    # Lista degli step per la timeline (da sovrascrivere nelle sottoclassi)
    STEPS: list[tuple[str, str]] = []

    def _initialize_steps(self) -> None:
        """Inizializza lo stato degli step a PENDING."""
        self._steps_state = [StepStatus.PENDING for _ in self.STEPS]

    def update_step(self, step_id: str | int, status: StepStatus, message: str | None = None) -> None:
        """
        Aggiorna lo stato di uno step nella timeline.
        """
        if isinstance(step_id, str):
            try:
                index = [s[0] for s in self.STEPS].index(step_id)
            except ValueError:
                self._logger.warning(f"Step ID '{step_id}' non trovato in {self.name}. Steps disponibili: {[s[0] for s in self.STEPS]}")
                return
        else:
            index = step_id

        if not self._steps_state:
            self._initialize_steps()

        if 0 <= index < len(self._steps_state):
            self._steps_state[index] = status
            
            # Aggiorna sempre l'indice corrente per i log contestuali
            self._current_step_index = index
            
            step_name = self.STEPS[index][1]
            
            # Emit signal for GUI
            self.signals.step_changed.emit(index, step_name, status)
            
            # Log automatically with explicit step context
            if message:
                self.log(f"[{step_name}] {message}", current_step=step_name, step_index=index)
            elif status == StepStatus.RUNNING:
                self.log(f"Inizio operazione: {step_name}", current_step=step_name, step_index=index)
            elif status == StepStatus.COMPLETED:
                self.log(f"Completato: {step_name}", current_step=step_name, step_index=index)
            elif status == StepStatus.ERROR:
                self.log(f"❌ ERRORE in {step_name}", "ERROR", current_step=step_name, step_index=index)
        else:
            self._logger.error(f"Indice step {index} fuori range (Max: {len(self._steps_state)-1})")

    @property
    @abstractmethod
    def description(self) -> str:
        """Restituisce una descrizione testuale delle funzionalità del bot."""

    @staticmethod
    @abstractmethod
    def get_columns() -> list[dict[str, Any]]:
        """Definisce le colonne richieste per l'input dei dati."""

    @property
    def status(self) -> BotStatus:
        """Restituisce lo stato attuale della State Machine del bot."""
        return self._status

    @status.setter
    def status(self, value: BotStatus) -> None:
        """Aggiorna lo stato del bot e logga il cambiamento."""
        if self._status != value:
            self._status = value
            self.signals.status_changed.emit(value)
            self.log(f"Stato: {value.name}")

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """
        Esegue una validazione preventiva dei dati (Dry Run).
        Deve essere implementata dai bot derivati.

        Args:
            data: Lista di dizionari o dizionario contenente i dati da processare.
        Returns:
            tuple: (Successo, Messaggio di errore)
        """
        if not data:
            return False, "Nessun dato da elaborare."
        if not self.username or not self.password:
            return False, "Credenziali mancanti nelle impostazioni."
        return True, ""

    def log(self, message: str, level: str = "INFO", current_step: str | None = None, step_index: int | None = None) -> None:
        """
        Logga un messaggio in console, nel widget log e via Telegram se configurato.

        Args:
            message: Testo del messaggio da loggare.
            level: Livello log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            current_step: Nome dello step corrente (opzionale).
            step_index: Indice dello step corrente (opzionale).
        """
        # Send to UI signal
        self.signals.log_emitted.emit(message, level)

        # Send to UI callback
        if self._log_callback:
            self._log_callback(message)

        # Contextual info for logging
        if current_step is None and 0 <= self._current_step_index < len(self.STEPS):
            current_step = self.STEPS[self._current_step_index][1]
        
        if step_index is None:
            step_index = self._current_step_index

        # Structured logging with bot context
        log_method = getattr(self._logger, level.lower(), self._logger.info)
        log_method(
            message,
            trace_id=self._trace_id,
            bot_type=self.name.lower().replace(" ", "_"),
            bot_status=self._status.name,
            current_step=current_step or "",
            step_index=step_index
        )

        # Telegram notification
        if self._telegram_service:
            with suppress(Exception):
                clean_msg = re.sub(r"^\[\d{2}:\d{2}:\d{2}\]\s*", "", message.strip())
                self._telegram_service.send_message_sync(f"🔹 *{self.name}*\n{clean_msg}")

    def set_log_callback(self, callback: Callable[[str], None]) -> None:
        """Imposta la callback per inoltrare i log all'interfaccia utente."""
        self._log_callback = callback

    def set_telegram_service(self, service: Any) -> None:
        """Imposta il servizio Telegram per l'invio di notifiche."""
        self._telegram_service = service

    def set_input_callback(self, callback: Callable[[str], str]) -> None:
        """Imposta la callback per richiedere input interattivo all'utente."""
        self._input_callback = callback

    def request_stop(self) -> None:
        """Segnala al bot di interrompere l'esecuzione alla prima occasione sicura."""
        self._stop_requested = True
        self.log("⚠️ Interruzione richiesta...")

    def _check_stop(self) -> None:
        """Verifica se è stata richiesta l'interruzione e solleva InterruptedError."""
        if self._stop_requested:
            raise InterruptedError("Bot interrotto dall'utente")

    @measure_time(threshold_ms=10000)
    def _init_driver(self) -> None:
        """Inizializzazione del driver Chrome con opzioni e configurazioni specifiche."""
        self.log("Inizializzazione browser...")
        self.status = BotStatus.INITIALIZING
        self._logger.debug("Starting Chrome driver initialization", headless=self.headless)

        options = self._get_chrome_options()
        driver_path = self._get_chromedriver_path()
        service = Service(driver_path) if driver_path else None

        try:
            # Type narrowing for mypy
            if not service:
                raise RuntimeError("Chromedriver service non disponibile")
            self._setup_driver_instance(service, options)
            self._configure_waits_and_pages()
            self._logger.info("Chrome driver initialized successfully")
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
            "--disable-software-rasterizer",
            "--log-level=3",
            "--silent",
        ]
        for arg in args:
            options.add_argument(arg)

        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
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

        prefs: dict[str, Any] = {
            "profile.default_content_setting_values.automatic_downloads": 1,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
        }

        if self.download_path:
            prefs["download.default_directory"] = str(Path(self.download_path).resolve())

        options.add_experimental_option("prefs", prefs)
        return options

    def _get_chromedriver_path(self) -> str | None:
        """Tenta di ottenere il path di chromedriver con logica di persistenza e auto-healing."""
        import shutil

        from src.utils.resource_manager import ResourceManager

        # 1. Driver Persistente (Aggiornato dall'app stessa in precedenza)
        persistent_dir = ResourceManager.get_writable_drivers_dir()
        persistent_driver = persistent_dir / "chromedriver.exe"
        if persistent_driver.exists():
            path = str(persistent_driver.resolve())
            self._logger.debug(f"Usando driver persistente (auto-aggiornato): {path}")
            return path

        # 2. Driver Esterno (Priorità massima per l'assistenza tecnica o lo sviluppatore)
        if getattr(sys, "frozen", False):
            exe_dir = Path(sys.executable).parent
            external_driver = exe_dir / "drivers" / "chromedriver.exe"
            if external_driver.exists():
                path = str(external_driver.resolve())
                self.log(f"Usando driver esterno (override): {path}")
                return path

        # 3. Locale Bundled o Dev Root (PROJECT_ROOT/drivers/chromedriver.exe)
        bundled_driver = Path(ResourceManager.PROJECT_ROOT) / "drivers" / "chromedriver.exe"
        if bundled_driver.exists():
            path = str(bundled_driver.resolve())
            self._logger.debug(f"Usando driver locale/integrato: {path}")
            return path

        # 4. Automatico (Online) + Salvataggio Persistente
        try:
            self.log("Verifica aggiornamenti driver...")
            downloaded_path = ChromeDriverManager().install()

            # Estrai l'eseguibile se necessario (webdriver-manager a volte scarica folder)
            if not downloaded_path.lower().endswith(".exe"):
                potential = list(Path(downloaded_path).parent.rglob("chromedriver.exe"))
                if potential:
                    downloaded_path = str(potential[0])

            # PERSISTENZA: Copia il driver scaricato nella cartella persistente per il futuro
            if Path(downloaded_path).exists():
                dest_path = persistent_dir / "chromedriver.exe"
                try:
                    shutil.copy2(downloaded_path, dest_path)
                    self._logger.info(f"Driver scaricato e salvato permanentemente in: {dest_path}")
                    return str(dest_path.resolve())
                except Exception as copy_err:
                    self._logger.warning(f"Impossibile salvare il driver in modo persistente: {copy_err}")

            return downloaded_path
        except Exception as e:
            self.log(f"⚠️ Impossibile scaricare driver automatico: {e}")

        return None

    def _setup_driver_instance(self, service: Service, options: Options) -> None:
        """Crea l'istanza di webdriver.Chrome applicando tecniche anti-detection e forzando il download path."""
        self.driver = webdriver.Chrome(service=service, options=options)

        # Forza il percorso di download tramite CDP (più robusto delle prefs)
        if self.download_path:
            path_str = str(Path(self.download_path).resolve())
            self.log(f"Cartella monitorata: {path_str}")
            self.driver.execute_cdp_cmd(
                "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": path_str}
            )

        # Anti-detection
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )

    def _configure_waits_and_pages(self) -> None:
        """Inizializza gli oggetti WebDriverWait per diverse durate e la LoginPage."""
        if not self.driver:
            return
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.popup_wait = WebDriverWait(self.driver, Timeouts.SHORT)
        self.long_wait = WebDriverWait(self.driver, Timeouts.PAGE_LOAD)
        self.login_page = LoginPage(self.driver, self.wait, self.log, self.ISAB_URL)

    def _handle_driver_error(self, e: Exception) -> None:
        """Gestisce gli errori critici di avvio del driver Chrome."""
        err_str = str(e).lower()
        error_type = "unknown"

        if "chrome instance exited" in err_str:
            error_type = "chrome_crashed"
            self._logger.error(
                "Chrome driver initialization failed - browser crashed",
                exc=e,
                error_type=error_type,
                suggestion="Ensure Chrome is updated",
            )
            self.log("❌ ERRORE CRITICO DRIVER: Chrome è crashato all'avvio", "ERROR")
            self.log("💡 SUGGERIMENTO: Assicurati che Chrome sia aggiornato.")
        elif "sessionnotcreatedexception" in err_str or "version" in err_str:
            error_type = "version_mismatch"
            self._logger.error(
                "Chrome driver initialization failed - version mismatch",
                exc=e,
                error_type=error_type,
                suggestion="Update Chrome or download compatible chromedriver",
            )
            self.log("❌ ERRORE CRITICO DRIVER: Versione incompatibile", "ERROR")
            self.log("💡 SUGGERIMENTO: Aggiorna Chrome o scarica chromedriver compatibile.")
        else:
            self._logger.exception("Chrome driver initialization failed", exc=e, error_type=error_type)
            self.log(f"❌ ERRORE CRITICO DRIVER: {e}", "ERROR")

        raise e

    @measure_time(threshold_ms=5000)
    def execute(self, data: list[dict[str, Any]]) -> bool:
        """
        Esegue il workflow completo del bot: Validazione -> Accesso -> Esecuzione -> Cleanup.
        """
        self._stop_requested = False
        
        # Inizializza lo stato degli step ORA che la sottoclasse è pronta
        self._initialize_steps()

        # Set up logging context for this bot execution
        bot_type = self.name.lower().replace(" ", "_")
        with with_context(
            trace_id=self._trace_id,
            bot_type=bot_type,
            username=self.username[:3] + "***",  # Masked for privacy
        ):
            self._logger.info(
                "Bot execution started",
                data_count=len(data) if isinstance(data, list) else 1,
            )

            # 1. Validazione Preventiva
            self.status = BotStatus.IDLE
            valid, error_msg = self.validate_data(data)
            if not valid:
                self._logger.error("Validation failed", error=error_msg)
                self.log(f"❌ Validazione fallita: {error_msg}", "ERROR")
                self.status = BotStatus.ERROR
                return False

            try:
                # 2. Inizializzazione Browser & Login
                # Attiviamo il primo step (tipicamente login) subito
                if self.STEPS:
                    self.update_step(self.STEPS[0][0], StepStatus.RUNNING)
                    # Forziamo l'indice per il logger iniziale
                    self._current_step_index = 0

                if not self._safe_login_with_retry():
                    self.status = BotStatus.ERROR
                    if self.STEPS:
                        self.update_step(self.STEPS[0][0], StepStatus.ERROR)
                    return False

                # 3. Esecuzione
                self.status = BotStatus.RUNNING
                result = self.run(data)

                self.status = BotStatus.COMPLETED if result else BotStatus.ERROR
                self._logger.info("Bot execution completed", success=result)
                self._current_step_index = -1  # Reset step context
                return result

            except InterruptedError:
                self._logger.warning("Bot execution interrupted by user")
                self.log("Bot interrotto", "WARNING")
                self.status = BotStatus.STOPPED
                return False
            except Exception as e:
                self._logger.exception("Fatal bot error", exc=e)
                self.log(f"✗ Errore fatale: {e}", "ERROR")
                self._save_error_state(str(e))
                self.status = BotStatus.ERROR
                
                # Aggiorna timeline se c'è uno step attivo
                if 0 <= self._current_step_index < len(self.steps):
                    self.update_step(self._current_step_index, StepStatus.ERROR)
                
                return False
            finally:
                self.cleanup()

    def _save_error_state(self, error_msg: str) -> None:
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

            self._logger.info(
                "Error state saved for debugging",
                screenshot=str(screenshot_path),
                html_source=str(html_path),
                error_message=error_msg,
            )
            self.log(f"📸 Stato errore salvato in: {error_dir.name}")

        except Exception as e:
            self._logger.warning("Failed to save error state", exc=e)
            self.log(f"⚠️ Impossibile salvare lo stato di errore: {e}", "WARNING")

    @measure_time(threshold_ms=15000)
    def _login(self) -> bool:
        """Esegue il login al portale ISAB usando la LoginPage."""
        self._logger.debug("Starting login process")
        if self.login_page:
            result = self.login_page.login(self.username, self.password)
            if result:
                self._logger.info("Login successful")
            else:
                self._logger.error("Login failed")
            return result
        self._logger.error("Login page not initialized")
        return False

    def _attendi_scomparsa_overlay(self, timeout: int | None = None) -> bool:
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

    def _handle_session_popup(self) -> bool:
        """Gestisce il popup di sessione multipla cliccando su 'SI'."""
        with suppress(Exception):
            if self.popup_wait:
                btn = self.popup_wait.until(EC.element_to_be_clickable(CommonLocators.POPUP_SESSION_YES))
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

    def cleanup(self) -> None:
        """Chiude il browser e pulisce le risorse del driver."""
        # Pulizia residui download GUID
        if self.download_path:
            from src.utils.helpers import cleanup_chrome_temp_files

            with suppress(Exception):
                cleanup_chrome_temp_files(self.download_path)

        if self.driver:
            with suppress(Exception):
                self.driver.quit()
            self.driver = None

    @abstractmethod
    def run(self, data: list[dict[str, Any]]) -> bool:
        """
        Logica principale dell'automazione da implementare nelle sottoclassi.

        Args:
            data: Dati validati da processare.
        Returns:
            bool: True se l'esecuzione è completata correttamente.
        """
