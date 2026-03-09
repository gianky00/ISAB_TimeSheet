"""
SyncroJob - Base Bot
Classe base astratta e orchestratore del ciclo di vita per tutti i bot di automazione Selenium.
Implementa una robusta State Machine per la gestione degli stati (IDLE, RUNNING, ERROR, etc.),
un sistema di tracciamento progressivo tramite 'Steps' per la timeline della GUI,
e logica enterprise di logging con trace_id e screenshot di errore automatici.
"""

import re
import sys
from abc import ABC, abstractmethod
from collections.abc import Callable
from contextlib import suppress
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, ClassVar

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

logger = get_logger(__name__)


class StepStatus(Enum):
    """Enumerazione degli stati possibili per un singolo step della timeline operativa."""

    PENDING = auto()
    """Step in attesa di esecuzione."""
    RUNNING = auto()
    """Step attualmente in fase di elaborazione."""
    COMPLETED = auto()
    """Step terminato con successo."""
    ERROR = auto()
    """Step fallito con errore."""


class BotSignals(QObject):
    """
    Segnali PyQt6 per la comunicazione asincrona tra il thread del bot e l'interfaccia utente.
    Permette l'aggiornamento real-time dei log, dello stato globale e della timeline.
    """

    step_changed = pyqtSignal(int, str, object)
    """Segnale emesso al cambio di stato di uno step (indice, nome, StepStatus)."""

    status_changed = pyqtSignal(object)
    """Segnale emesso al cambiamento dello stato globale della State Machine (BotStatus)."""

    log_emitted = pyqtSignal(str, str)
    """Segnale emesso per ogni nuovo messaggio di log (messaggio, livello)."""

    critical_error = pyqtSignal(str, str)
    """Segnale emesso per errori fatali che richiedono un'interazione UI bloccante (titolo, messaggio)."""


class BaseBot(ABC):
    """
    Architettura base per i bot ISAB/SafeWork.
    Fornisce metodi precostruiti per l'inizializzazione del driver Chrome, la gestione del login,
    il recupero dei driver tramite WebDriverManager e la pulizia delle risorse (cleanup).
    """

    ISAB_URL = URLs.ISAB_PORTAL
    """URL di default per l'accesso al portale fornitori ISAB."""

    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = Timeouts.DEFAULT,
        download_path: str = "",
    ) -> None:
        """
        Configura l'istanza del bot con le credenziali e le preferenze del browser.

        Args:
            username: Username per l'autenticazione.
            password: Password per l'autenticazione.
            headless: Se avviare Chrome senza interfaccia grafica.
            timeout: Secondi di attesa implicita per Selenium.
            download_path: Percorso assoluto per il salvataggio dei file scaricati.
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
        self._progress_callback: Callable[[int, bool, str], None] | None = None
        self.login_page: LoginPage | None = None
        self._telegram_service: Any = None
        self.signals = BotSignals()
        self._current_step_index = -1
        self._steps_state: list[StepStatus] = []
        self._trace_id = generate_trace_id()
        self._logger = get_logger(f"bot.{self.__class__.__name__}")
        self._force_download = False

    @property
    @abstractmethod
    def name(self) -> str:
        """Restituisce il nome visualizzato del bot."""

    STEPS: ClassVar[list[tuple[str, str]]] = []
    """Elenco statico degli step operativi (id, etichetta) definiti nella sottoclasse."""

    def _initialize_steps(self) -> None:
        """Resetta lo stato della timeline impostando tutti i passi definiti in PENDING."""
        self._steps_state = [StepStatus.PENDING for _ in self.STEPS]

    def update_step(self, step_id: str | int, status: StepStatus, message: str | None = None) -> None:
        """
        Aggiorna lo stato visivo di un passo nella timeline e invia i segnali alla GUI.

        Args:
            step_id: Identificativo stringa o indice numerico dello step.
            status: Nuovo stato (StepStatus).
            message: Eventuale messaggio di log contestuale opzionale.
        """
        if isinstance(step_id, str):
            try:
                index = [s[0] for s in self.STEPS].index(step_id)
            except ValueError:
                return
        else:
            index = step_id

        if not hasattr(self, "_steps_state") or not self._steps_state:
            self._initialize_steps()

        if 0 <= index < len(self._steps_state):
            self._steps_state[index] = status
            self._current_step_index = index
            step_name = self.STEPS[index][1]
            if hasattr(self, "signals"):
                self.signals.step_changed.emit(index, step_name, status)

            if message:
                self.log(f"[{step_name}] {message}", current_step=step_name, step_index=index)
            elif status == StepStatus.RUNNING:
                # Log più pulito per l'inizio dello step
                self.log(f"⏳ Avvio: {step_name}", current_step=step_name, step_index=index)
            elif status == StepStatus.ERROR:
                self.log(f"❌ ERRORE: {step_name}", "ERROR", current_step=step_name, step_index=index)

    @property
    @abstractmethod
    def description(self) -> str:
        """Restituisce la descrizione estesa delle operazioni svolte dal bot."""

    @staticmethod
    @abstractmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce lo schema delle colonne richieste per l'input dei dati nel pannello bot."""

    @property
    def status(self) -> BotStatus:
        """Restituisce lo stato corrente della State Machine del bot."""
        return self._status

    @status.setter
    def status(self, value: BotStatus) -> None:
        """Cambia lo stato del bot, emette il segnale PyQt e registra l'evento nel log."""
        if self._status != value:
            self._status = value
            self.signals.status_changed.emit(value)
            # Log dello stato solo se rilevante (es. ERROR o COMPLETED)
            if value in (BotStatus.ERROR, BotStatus.COMPLETED, BotStatus.STOPPED):
                self.log(f"🏁 Stato finale: {value.name}")

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """
        Esegue una validazione formale dei dati di input e della configurazione credenziali.

        Returns:
            tuple: (Successo, Messaggio descrittivo errore).
        """
        if not data:
            return False, "Nessun dato da elaborare."
        if not self.username or not self.password:
            return False, "Credenziali mancanti."
        return True, ""

    def log(
        self,
        message: str,
        level: str = "INFO",
        current_step: str | None = None,
        step_index: int | None = None,
    ) -> None:
        """
        Emette un messaggio di log strutturato verso la GUI, il file JSON e Telegram.

        Args:
            message: Testo del messaggio.
            level: Livello di severità (INFO, ERROR, etc.).
            current_step: Etichetta dello step operativo attuale.
            step_index: Indice dello step operativo attuale.
        """
        if hasattr(self, "signals"):
            self.signals.log_emitted.emit(message, level)
        if self._log_callback:
            self._log_callback(message)

        if (
            current_step is None
            and hasattr(self, "_current_step_index")
            and 0 <= self._current_step_index < len(self.STEPS)
        ):
            current_step = self.STEPS[self._current_step_index][1]

        # Robustness for mocked __init__ in tests
        logger_obj = getattr(self, "_logger", logger)
        trace_id = getattr(self, "_trace_id", "no-trace")
        status_name = (
            self._status.name if hasattr(self, "_status") and hasattr(self._status, "name") else "IDLE"
        )
        step_idx = step_index if step_index is not None else getattr(self, "_current_step_index", -1)

        getattr(logger_obj, level.lower(), logger_obj.info)(
            message,
            trace_id=trace_id,
            bot_type=self.name.lower().replace(" ", "_"),
            bot_status=status_name,
            current_step=current_step or "",
            step_index=step_idx,
        )

        if self._telegram_service:
            with suppress(Exception):
                clean = re.sub(r"^\[\d{2}:\d{2}:\d{2}\]\s*", "", message.strip())
                self._telegram_service.send_message_sync(f"🔹 *{self.name}*\n{clean}")

    def set_log_callback(self, callback: Callable[[str], None]) -> None:
        """Imposta una funzione esterna per ricevere i messaggi di log testuali."""
        self._log_callback = callback

    def set_telegram_service(self, service: Any) -> None:
        """Associa un servizio Telegram per l'inoltro dei messaggi di stato."""
        self._telegram_service = service

    def set_input_callback(self, callback: Callable[[str], str]) -> None:
        """Imposta una callback per richiedere dati all'utente durante l'esecuzione (es. CAPTCHA o OTP)."""
        self._input_callback = callback

    def set_progress_callback(self, callback: Callable[[int, bool, str], None]) -> None:
        """Imposta una callback per notificare il progresso di una riga specifica alla GUI."""
        self._progress_callback = callback

    def request_stop(self) -> None:
        """Invia una richiesta di interruzione gentile al loop operativo del bot."""
        self._stop_requested = True
        self.log("⚠️ Interruzione richiesta...")

    def _check_stop(self) -> None:
        """Verifica se è stata richiesta l'interruzione; in caso affermativo, blocca l'esecuzione."""
        if self._stop_requested:
            raise InterruptedError("Bot interrotto dall'utente")

    @measure_time(threshold_ms=10000)
    def _init_driver(self) -> None:
        """Inizializza il browser Chrome con opzioni anti-detection e configurazioni di download."""
        self.log("🌐 Inizializzazione browser...")
        self.status = BotStatus.INITIALIZING
        options = self._get_chrome_options()
        if d_path := self._get_chromedriver_path():
            try:
                service = Service(d_path)
                self._setup_driver_instance(service, options)
                self._configure_waits_and_pages()
            except Exception as e:
                self._handle_driver_error(e)
        else:
            raise RuntimeError("Chromedriver service non disponibile.")

    def _get_chrome_options(self) -> Options:
        """Configura le opzioni tecniche per Chrome (Sandboxing, Headless, Profile, Prefs)."""
        opt = Options()
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
            "--remote-debugging-port=0",
            "--disable-software-rasterizer",
        ]
        for a in args:
            opt.add_argument(a)

        opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        opt.add_experimental_option("useAutomationExtension", False)

        cfg = config_manager.load_config()
        if self.headless or cfg.get("browser_headless", False):
            self.headless = True
            opt.add_argument("--headless=new")
            opt.add_argument(f"--window-size={BrowserConfig.WINDOW_SIZE}")

        opt.add_argument(
            f"--user-data-dir={config_manager.CONFIG_DIR / 'data' / BrowserConfig.CACHE_DIR_NAME}"
        )

        prefs: dict[str, Any] = {
            "profile.default_content_setting_values.automatic_downloads": 1,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
        }
        if self.download_path:
            prefs["download.default_directory"] = str(Path(self.download_path).resolve())

        opt.add_experimental_option("prefs", prefs)
        return opt

    def _get_chromedriver_path(self) -> str | None:
        """Ricerca il path del driver Chrome tra cartelle persistenti, bundle e download automatico."""
        import shutil

        from src.utils.resource_manager import ResourceManager

        p_dir = ResourceManager.get_writable_drivers_dir()

        if not getattr(self, "_force_download", False):
            if (p_dir / "chromedriver.exe").exists():
                return str((p_dir / "chromedriver.exe").resolve())

            if (
                getattr(sys, "frozen", False)
                and (ext := Path(sys.executable).parent / "drivers" / "chromedriver.exe").exists()
            ):
                return str(ext.resolve())

            if (bndl := Path(ResourceManager.PROJECT_ROOT) / "drivers" / "chromedriver.exe").exists():
                return str(bndl.resolve())

        try:
            self.log("Aggiornamento driver in corso...")
            d_path = ChromeDriverManager().install()
            if not d_path.lower().endswith(".exe") and (
                pot := list(Path(d_path).parent.rglob("chromedriver.exe"))
            ):
                d_path = str(pot[0])
            if Path(d_path).exists():
                with suppress(Exception):
                    shutil.copy2(d_path, p_dir / "chromedriver.exe")
            return d_path
        except Exception as e:
            self.log(f"⚠️ Errore download driver: {e}")
        return None

    def _setup_driver_instance(self, service: Service, options: Options) -> None:
        """Crea l'istanza webdriver ed applica patch runtime per l'evasione dei controlli bot."""
        self.driver = webdriver.Chrome(service=service, options=options)

        # Forza SEMPRE il percorso di download per evitare fallback su cartelle temp
        # Se self.download_path è vuoto, usa la cartella Downloads dell'utente
        target_download = (
            Path(self.download_path).resolve() if self.download_path else Path.home() / "Downloads"
        )

        if not target_download.exists():
            with suppress(Exception):
                target_download.mkdir(parents=True, exist_ok=True)

        self.log(f"📁 Cartella download forzata: {target_download}")

        self.driver.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": str(target_download)},
        )

        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )

    def _configure_waits_and_pages(self) -> None:
        """Inizializza i Page Objects e i gestori di attesa esplicita."""
        if not self.driver:
            return
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.popup_wait = WebDriverWait(self.driver, Timeouts.SHORT)
        self.long_wait = WebDriverWait(self.driver, Timeouts.PAGE_LOAD)
        self.login_page = LoginPage(self.driver, self.wait, self.log, self.ISAB_URL)

    def _handle_driver_error(self, e: Exception) -> None:
        """Logga e gestisce errori fatali del browser (crash, mismatch di versione)."""
        msg = str(e).lower()
        if "chrome instance exited" in msg:
            self.log("❌ CRASH: Chrome si è chiuso all'avvio", "ERROR")
            self.log("💡 SUGGERIMENTO: Assicurati che Chrome sia aggiornato e non ci siano istanze appese.")
            self._force_driver_redownload()
        elif "version" in msg or "sessionnotcreated" in msg:
            self.log("❌ ERRORE CRITICO DRIVER: Versione incompatibile", "ERROR")
            self.log("💡 SUGGERIMENTO: Al prossimo avvio verrà scaricato un driver aggiornato.")
            self._force_driver_redownload()
        else:
            self.log(f"❌ ERRORE DRIVER: {e}", "ERROR")
        raise e

    def _force_driver_redownload(self) -> None:
        """Forza la rimozione del driver in cache per costringere il download al prossimo tentativo."""
        from src.utils.resource_manager import ResourceManager

        self._force_download = True
        with suppress(Exception):
            p_dir = ResourceManager.get_writable_drivers_dir()
            d_exe = p_dir / "chromedriver.exe"
            if d_exe.exists():
                d_exe.unlink()
                self.log("🗑️ Driver locale obsoleto rimosso dalla cache.")

    @measure_time(threshold_ms=5000)
    def execute(self, data: list[dict[str, Any]]) -> bool:
        """
        Orchestra il workflow principale del bot: Validazione -> Setup -> Run -> Cleanup.
        Garantisce il mantenimento del contesto di logging e la cattura di screenshot in caso di fallimento.
        """
        self._stop_requested = False

        # --- SICUREZZA: Verifica Licenza JIT (Just-In-Time) ---
        from src.core.license_updater import run_update
        from src.core.license_validator import verify_license

        try:
            # Tenta una sincronizzazione rapida cloud prima dell'avvio
            run_update()
        except Exception as le:
            if "REVOCATA" in str(le):
                self.log(f"❌ ACCESSO NEGATO: {le}", "ERROR")
                if hasattr(self, "signals"):
                    self.signals.critical_error.emit("Licenza Revocata", str(le))
                self.status = BotStatus.ERROR
                return False

        valid, msg = verify_license()
        if not valid:
            self.log(f"❌ AVVIO NEGATO: {msg}", "ERROR")
            self.status = BotStatus.ERROR
            return False
        # ----------------------------------------------------

        self._initialize_steps()
        with with_context(
            trace_id=self._trace_id,
            bot_type=self.name.lower().replace(" ", "_"),
            username=self.username[:3] + "***",
        ):
            # Log di configurazione iniziale pulito
            self.log(f"⚙️ Avvio {self.name} | Headless: {self.headless} | Timeout: {self.timeout}s")

            valid_res, valid_msg = self.validate_data(data)
            if not valid_res:
                self.log(f"❌ Validazione fallita: {valid_msg}", "ERROR")
                self.status = BotStatus.ERROR
                return False
            try:
                if self.STEPS:
                    self.update_step(0, StepStatus.RUNNING)
                if not self._safe_login_with_retry():
                    self.status = BotStatus.ERROR
                    if self.STEPS:
                        self.update_step(0, StepStatus.ERROR)
                    return False
                self.status = BotStatus.RUNNING
                result = self.run(data)
                self.status = BotStatus.COMPLETED if result else BotStatus.ERROR
                return result
            except InterruptedError:
                self.log("Bot interrotto", "WARNING")
                self.status = BotStatus.STOPPED
                return False
            except Exception as e:
                self.log(f"✗ Errore fatale: {e}", "ERROR")
                self._save_error_state(str(e))
                self.status = BotStatus.ERROR
                if 0 <= self._current_step_index < len(self.STEPS):
                    self.update_step(self._current_step_index, StepStatus.ERROR)
                return False
            finally:
                self.cleanup()

    def _save_error_state(self, error_msg: str) -> None:
        """Salva screenshot e HTML della pagina corrente per facilitare il debug post-mortem."""
        if not self.driver:
            return
        with suppress(Exception):
            edir = config_manager.CONFIG_DIR / "logs" / "errors"
            edir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            sn = self.name.replace(" ", "_").lower()
            self.driver.save_screenshot(str(edir / f"error_{sn}_{ts}.png"))
            (edir / f"error_{sn}_{ts}.html").write_text(self.driver.page_source, encoding="utf-8")
            self.log(f"📸 Stato errore salvato in: {edir.name}")

    def _login(self) -> bool:
        """Esegue il processo di login automatizzato sul portale target."""
        return self.login_page.login(self.username, self.password) if self.login_page else False

    def _attendi_scomparsa_overlay(self, timeout: int | None = None) -> bool:
        """Attende che gli overlay grafici (loading) del portale ISAB vengano rimossi dal DOM."""
        if self.login_page:
            if timeout is not None:
                return self.login_page._attendi_scomparsa_overlay(timeout)
            return self.login_page._attendi_scomparsa_overlay()
        return True

    def _handle_session_popup(self) -> bool:
        """Rileva e conferma il popup di 'Sessione Multipla' se presente."""
        with suppress(Exception):
            if self.popup_wait:
                self.popup_wait.until(EC.element_to_be_clickable(CommonLocators.POPUP_SESSION_YES)).click()
                self.log("✅ Popup sessione gestito (SI).")
                return True
        return False

    def _safe_login_with_retry(self, max_retries: int = 2) -> bool:
        """Tenta l'avvio del driver e il login con una logica di retry in caso di instabilità del browser."""
        for _ in range(max_retries):
            self._check_stop()
            try:
                self._init_driver()
                if self._login():
                    return True
                self.cleanup()
            except Exception as e:
                self.log(f"⚠️ Errore tentativo: {e}")
                self.cleanup()
        return False

    def cleanup(self) -> None:
        """Rilascia le risorse del driver, chiude il browser e rimuove file temporanei di Chrome."""
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
        """Punto di ingresso della logica bot specifica implementata nelle classi derivate."""
