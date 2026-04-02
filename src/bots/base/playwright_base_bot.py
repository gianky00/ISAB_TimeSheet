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
    """

    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = Timeouts.DEFAULT,
        download_path: str = "",
    ) -> None:
        super().__init__(username, password, headless, timeout, download_path)
        self.playwright: Any = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self.login_page: PlaywrightLoginPage | None = None

    @measure_time(threshold_ms=10000)
    def _init_driver(self) -> None:
        """Inizializza Playwright e il browser con logica di persistenza, stabilità e recovery."""
        from src.utils.browser_diagnostics import (  # noqa: PLC0415
            emergency_profile_reset,
            run_browser_diagnostic,
        )

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
            ],
        }

        # Tentativi di inizializzazione (Aumentati a 3 per includere la recovery)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.log(f"🧹 Setup ambiente browser (Tentativo {attempt + 1}/{max_retries})...")

                # Pulizia preventiva ad ogni tentativo
                with suppress(Exception):
                    cleanup_bot_processes()

                if not self.playwright:
                    self.log("🌐 Inizializzazione Playwright Core...")
                    self.playwright = sync_playwright().start()

                self.log(f"🚀 Lancio Chromium con profilo persistente: {user_data_dir.name}")
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
                self.log(f"⚠️ Errore inizializzazione (T{attempt + 1}): {err_msg}", "WARNING")

                # Pulizia forzata dello stato interno ad ogni fallimento
                self._stop_playwright_internal()

                # Se siamo al secondo fallimento, eseguiamo diagnostica e tentiamo il reset del profilo
                if attempt == 1:
                    self.log("🔍 Esecuzione diagnostica browser per isolare il problema...")
                    diag = run_browser_diagnostic(user_data_dir)

                    # Se Playwright barebone funziona, ma il lancio persistente fallisce, resettiamo il profilo
                    if diag["checks"]["playwright_launch"]["status"] == "PASS":
                        self.log(
                            "♻️ Binari Playwright OK, ma profilo instabile. Eseguo Emergency Reset...",
                            "WARNING",
                        )
                        if emergency_profile_reset(user_data_dir):
                            self.log("✅ Profilo resettato. Ultimo tentativo con sessione pulita.")
                            continue

                # Se è l'ultimo tentativo, rilanciamo l'errore definitivo
                if attempt == max_retries - 1:
                    self.log("❌ Impossibile inizializzare il browser dopo molteplici tentativi.", "ERROR")
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
        return self.login_page.login(self.username, self.password) if self.login_page else False

    def _get_selector(self, locator: tuple[str, str]) -> str:
        """Converte un locatore Selenium (By, value) in un selettore Playwright."""
        from .playwright_utils import get_playwright_selector  # noqa: PLC0415

        return get_playwright_selector(locator)

    def cleanup(self) -> None:
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
