# mypy: disable-error-code="no-any-unimported, unused-ignore"
"""
SyncroJob - Playwright Base Bot
Implementazione della classe base per i bot Playwright.
"""

import re
from abc import ABC
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.bots.base.base_bot import BaseBot
from src.bots.base.playwright_login_page import PlaywrightLoginPage
from src.core import config_manager
from src.core.constants import BotStatus, BrowserConfig, Timeouts
from src.core.logging import measure_time
from src.utils.helpers import cleanup_bot_processes


class PlaywrightBaseBot(BaseBot, ABC):
    """
    Classe base per i bot basati su Playwright.
    Centralizza la gestione del browser Chromium, la persistenza del profilo e i flag di sicurezza.
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
        Inizializza le proprietà fondamentali del bot Playwright.

        Args:
            username: Nome utente per il login.
            password: Password per il login.
            headless: Se True, avvia il browser in modalità nascosta.
            timeout: Tempo massimo di attesa per le operazioni (secondi).
            download_path: Percorso per il salvataggio dei file scaricati.
            company: Società da selezionare al login (ISAB o PSER).
        """
        super().__init__(username, password, headless, timeout, download_path, company=company)
        self.playwright: Any = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self.login_page: PlaywrightLoginPage | None = None

    @measure_time(threshold_ms=10000)
    def _init_driver(self) -> None:
        """Inizializza Playwright e il browser con logica di persistenza, stabilità e recovery."""
        from src.utils.browser_diagnostics import emergency_profile_reset  # noqa: PLC0415
        from src.utils.browser_profile_patcher import patch_browser_profile  # noqa: PLC0415

        self.status = BotStatus.INITIALIZING
        user_data_dir = config_manager.CONFIG_DIR / "data" / BrowserConfig.CACHE_DIR_NAME

        # Assicura esistenza directory dati
        user_data_dir.parent.mkdir(parents=True, exist_ok=True)

        cfg = config_manager.load_config()
        headless = self.headless or cfg.get("browser_headless", False)

        launch_options = {
            "headless": headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",  # Stabilità su Windows
                "--disable-software-rasterizer",
                "--disable-infobars",
                "--no-first-run",
                "--no-default-browser-check",
                "--no-pings",
                "--password-store=basic",
                "--use-mock-keychain",
                "--disable-component-update",
                "--disable-background-networking",
                "--disable-client-side-phishing-detection",
                "--disable-sync",
                # Disabilitazioni Mirate per il Gestore Password e Autocompletamento
                "--disable-features=PasswordLeakDetection,PasswordCheck,SafeBrowsingPasswordCheck,AutofillServerCommunication,AutofillAccountWalletStorage,OptimizationHints,OptimizationGuideFetching,OptimizationTargetPrediction,CredentialProviderExtension",
                "--disable-save-password-bubble",
                "--disable-single-click-autofill",
                "--disable-autofill",
                "--disable-password-generation",
                "--disable-password-manager-reauthentication",
                "--hide-crash-restore-bubble",
                "--disable-notifications",
            ],
        }

        # 1. Reset profilato preventivo per garantire tabula rasa (Standard per stabilità richiesto dall'utente)
        self.log("♻️ Esecuzione Reset Profilo Standard per avvio pulito...")
        with suppress(Exception):
            cleanup_bot_processes()
        emergency_profile_reset(user_data_dir)

        # 2. Patching preventivo del profilo per sopprimere popup sicurezza
        with suppress(Exception):
            if user_data_dir.exists():
                self.log("🛡️ Applicazione patch di sicurezza al profilo...")
                patch_browser_profile(user_data_dir)

        # 3. Tentativi di inizializzazione
        max_retries = 3

        for attempt in range(max_retries):
            try:
                self.log(f"🧹 Setup ambiente browser (Tentativo {attempt + 1}/{max_retries})...")

                if not self.playwright:
                    self.log("🌐 Inizializzazione Playwright Core...")
                    self.playwright = sync_playwright().start()

                self.log(f"[AVVIO] Lancio Chromium con profilo persistente: {user_data_dir.name}")
                self.context = self.playwright.chromium.launch_persistent_context(
                    user_data_dir=str(user_data_dir),
                    no_viewport=False,
                    viewport={"width": 1920, "height": 1080},
                    user_agent=BrowserConfig.USER_AGENT,
                    accept_downloads=True,
                    **launch_options,
                )
                break  # Successo

            except Exception as e:
                err_msg = str(e)
                self.log(f"[ATTENZIONE] Errore inizializzazione (T{attempt + 1}): {err_msg}", "WARNING")

                # Pulizia forzata dello stato interno ad ogni fallimento
                self._stop_playwright_internal()

                # Se è l'ultimo tentativo, rilanciamo l'errore definitivo
                if attempt == max_retries - 1:
                    self.log("[ERRORE] Impossibile inizializzare il browser dopo molteplici tentativi.", "ERROR")
                    raise

        if self.context is None:
            raise RuntimeError("BrowserInitFailed")

        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        # Playwright usa millisecondi per il timeout
        self.page.set_default_timeout(self.timeout * 1000)

        self.page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.login_page = PlaywrightLoginPage(self.page, self.log, self.ISAB_URL)

    def _stop_playwright_internal(self) -> None:
        """Ferma Playwright internamente senza loggare errori se già fermo."""
        if self.context:
            with suppress(Exception):
                self.context.close()
        if self.playwright:
            with suppress(Exception):
                self.playwright.stop()
        self.context = None
        self.playwright = None

    def _save_error_state(self, error_msg: str) -> None:
        """Cattura lo stato del browser in caso di errore (Screenshot + HTML)."""
        if not self.page:
            return
        with suppress(Exception):
            edir = config_manager.CONFIG_DIR / "logs" / "errors"
            edir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(UTC).astimezone().strftime("%Y%m%d_%H%M%S")
            sn = re.sub(r"[^\w\-]", "_", self.name.lower())

            self.page.screenshot(path=str(edir / f"error_{sn}_{ts}.png"))
            content = self.page.content()
            (edir / f"error_{sn}_{ts}.html").write_text(content, encoding="utf-8")
            self.log(f"📸 Stato errore salvato in: {edir.name}")

    def _login(self) -> bool:
        """Esegue il login delegandolo alla pagina di login specifica."""
        return self.login_page.login(self.username, self.password, self.company) if self.login_page else False

    def _get_selector(self, locator: tuple[str, str]) -> str:
        """Converte un locatore Selenium (By, value) in un selettore Playwright."""
        from .playwright_utils import get_playwright_selector  # noqa: PLC0415

        return get_playwright_selector(locator)

    def cleanup(self) -> None:
        """Rilascia tutte le risorse Playwright (contesto, browser, core)."""
        if self.context:
            with suppress(Exception):
                self.context.close()
        if self.playwright:
            with suppress(Exception):
                self.playwright.stop()

        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None
        self.login_page = None
