# mypy: disable-error-code="no-any-unimported, unused-ignore"
"""
SyncroJob - Selenium Base Bot
Implementazione della classe base per i bot Selenium.
"""

import re
import shutil
from abc import ABC
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.base.base_bot import BaseBot
from src.bots.base.login_page import LoginPage
from src.core import config_manager
from src.core.constants import BotStatus, BrowserConfig, Timeouts
from src.core.logging import measure_time
from src.utils.helpers import cleanup_bot_processes


class SeleniumBaseBot(BaseBot, ABC):
    """
    Classe base per i bot basati su Selenium.
    Gestisce l'inizializzazione di ChromeDriver, le opzioni del browser e le attese.
    """

    def __init__(  # noqa: PLR0913
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = Timeouts.DEFAULT,
        download_path: str = "",
        company: str = "ISAB",
    ) -> None:
        """
        Inizializza le propriet  fondamentali del bot Selenium.

        Args:
          username: Nome utente per il login.
          password: Password per il login.
          headless: Se True, avvia il browser in modalita' nascosta.
          timeout: Tempo massimo di attesa per le operazioni (secondi).
          download_path: Percorso per il salvataggio dei file scaricati.
          company: Societa' da selezionare al login (ISAB o PSER).
        """
        super().__init__(username, password, headless, timeout, download_path, company=company)
        self.driver: webdriver.Chrome | None = None
        self.wait: WebDriverWait[webdriver.Chrome] | None = None
        self.popup_wait: WebDriverWait[webdriver.Chrome] | None = None
        self.long_wait: WebDriverWait[webdriver.Chrome] | None = None
        self.login_page: LoginPage | None = None
        self._force_download = False

    @measure_time(threshold_ms=10000)
    def _init_driver(self) -> None:
        """Inizializza il browser Chrome con gestione dei processi stale e caricamento driver."""
        self.log("   Cleanup processi stale...")
        with suppress(Exception):
            cleanup_bot_processes()

        self.log("   Inizializzazione browser (Selenium)...")
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
            raise RuntimeError("DriverUnavailable")

    def _get_chrome_options(self) -> Options:
        """Configura le opzioni di riga di comando per l'istanza Chrome."""
        opt = Options()

        # Flag aggressivi per sopprimere popup di sicurezza, password e aggiornamenti
        args = [
            # Disabilitazione feature di riga di comando (Password e SafeBrowsing)
            "--disable-features=PasswordLeakDetection,PasswordCheck,SafeBrowsingPasswordCheck,AutofillServerCommunication,AutofillAccountWalletStorage",
            "--disable-save-password-bubble",
            "--disable-password-manager-reauthentication",
            "--disable-password-generation",
            "--disable-single-click-autofill",
            "--disable-autofill",
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
            "--disable-component-update",
            "--no-first-run",
            "--no-default-browser-check",
        ]
        for a in args:
            opt.add_argument(a)

        opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        opt.add_experimental_option("useAutomationExtension", False)

        user_data_dir = config_manager.CONFIG_DIR / "data" / BrowserConfig.CACHE_DIR_NAME
        opt.add_argument(f"--user-data-dir={user_data_dir}")

        # Patching preventivo del profilo (file Preferences) per Selenium
        from src.utils.browser_profile_patcher import patch_browser_profile  # noqa: PLC0415

        with suppress(Exception):
            patch_browser_profile(user_data_dir)

        cfg = config_manager.load_config()
        if self.headless or cfg.get("browser_headless", False):
            self.headless = True
            opt.add_argument("--headless=new")
            opt.add_argument(f"--window-size={BrowserConfig.WINDOW_SIZE}")

        # Preferenze sperimentali forzate
        prefs: dict[str, Any] = {
            "profile.default_content_setting_values.automatic_downloads": 1,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "password_manager.enabled": False,
            "password_manager.leak_detection_check_enabled": False,
        }
        if self.download_path:
            prefs["download.default_directory"] = str(Path(self.download_path).resolve())

        opt.add_experimental_option("prefs", prefs)
        return opt

    def _get_chromedriver_path(self) -> str | None:
        """Recupera il percorso del driver locale o ne innesca il download automatico."""
        from src.utils.resource_manager import ResourceManager  # noqa: PLC0415

        if not getattr(self, "_force_download", False) and (
            d_path := ResourceManager.ensure_automation_driver()
        ):
            return d_path

        try:
            from webdriver_manager.chrome import ChromeDriverManager  # noqa: PLC0415

            self.log("Aggiornamento driver in corso...")
            d_path = ChromeDriverManager().install()
            if not d_path.lower().endswith(".exe") and (
                pot := list(Path(d_path).parent.rglob("chromedriver.exe"))
            ):
                d_path = str(pot[0])

            if Path(d_path).exists():
                p_dir = ResourceManager.get_writable_drivers_dir()
                with suppress(Exception):
                    shutil.copy2(d_path, p_dir / "chromedriver.exe")
                return d_path
        except Exception as e:
            self.log(f"⚠️ Errore download driver: {e}")
        return None

    def _setup_driver_instance(self, service: Service, options: Options) -> None:
        """Crea l'istanza del WebDriver e configura i comportamenti di download e script."""
        self.driver = webdriver.Chrome(service=service, options=options)
        target_download = (
            Path(self.download_path).resolve() if self.download_path else Path.home() / "Downloads"
        )
        if not target_download.exists():
            with suppress(Exception):
                target_download.mkdir(parents=True, exist_ok=True)

        self.log(f"   Cartella download forzata: {target_download}")
        self.driver.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": str(target_download)},
        )
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )

    def _configure_waits_and_pages(self) -> None:
        """Inizializza gli oggetti WebDriverWait e il Page Object Model di login."""
        if not self.driver:
            return
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.popup_wait = WebDriverWait(self.driver, Timeouts.SHORT)
        self.long_wait = WebDriverWait(self.driver, Timeouts.PAGE_LOAD)
        self.login_page = LoginPage(self.driver, self.wait, self.log, self.ISAB_URL)

    def _handle_driver_error(self, e: Exception) -> None:
        """Gestisce gli errori specifici del driver proponendo soluzioni come il download forzato."""
        msg = str(e).lower()
        if "chrome instance exited" in msg:
            self.log("❌ CRASH: Chrome si  chiuso all'avvio", "ERROR")
            self._force_driver_redownload()
        elif "version" in msg or "sessionnotcreated" in msg:
            self.log("❌ ERRORE CRITICO DRIVER: Versione incompatibile", "ERROR")
            self._force_driver_redownload()
        else:
            self.log(f"❌ ERRORE DRIVER: {e}", "ERROR")
        raise e

    def _force_driver_redownload(self) -> None:
        """Elimina il driver locale e imposta il flag per scaricarlo nuovamente al prossimo avvio."""
        from src.utils.resource_manager import ResourceManager  # noqa: PLC0415

        self._force_download = True
        with suppress(Exception):
            p_dir = ResourceManager.get_writable_drivers_dir()
            d_exe = p_dir / "chromedriver.exe"
            if d_exe.exists():
                d_exe.unlink()
                self.log("    Driver locale obsoleto rimosso dalla cache.")

    def _save_error_state(self, error_msg: str) -> None:
        """Cattura lo stato visuale e il sorgente pulito (senza script) in caso di errore."""
        if not self.driver:
            return
        with suppress(Exception):
            edir = config_manager.CONFIG_DIR / "logs" / "errors"
            edir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(UTC).astimezone().strftime("%Y%m%d_%H%M%S")
            sn = re.sub(r"[^\w\-]", "_", self.name.lower())
            self.driver.save_screenshot(str(edir / f"error_{sn}_{ts}.png"))

            raw_source = self.driver.page_source
            clean_source = re.sub(
                r"<script.*?>.*?</script>",
                "<!-- SCRIPT REMOVED FOR SECURITY -->",
                raw_source,
                flags=re.DOTALL | re.IGNORECASE,
            )
            (edir / f"error_{sn}_{ts}.html").write_text(clean_source, encoding="utf-8")
            self.log(f"   Stato errore salvato in: {edir.name}")

    def _login(self) -> bool:
        """Esegue il login al portale ISAB."""
        return self.login_page.login(self.username, self.password, self.company) if self.login_page else False

    def _attendi_scomparsa_overlay(self, timeout: int | None = None) -> bool:
        """Attende che gli overlay grafici (loading) del portale ISAB vengano rimossi dal DOM."""
        if self.login_page:
            if timeout is not None:
                return self.login_page._attendi_scomparsa_overlay(timeout)
            return self.login_page._attendi_scomparsa_overlay()
        return True

    def cleanup(self) -> None:
        """Rilascia le risorse del WebDriver e pulisce i file temporanei di Chrome."""
        if self.download_path:
            from src.utils.helpers import cleanup_chrome_temp_files  # noqa: PLC0415

            with suppress(Exception):
                cleanup_chrome_temp_files(self.download_path)
        if self.driver:
            with suppress(Exception):
                self.driver.quit()
            self.driver = None
