"""SyncroJob - Playwright Base Bot.

Implementazione della classe base per i bot Playwright.
"""

from __future__ import annotations

import os
import re
import sys
from abc import ABC
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from src.bots.base.base_bot import BaseBot
from src.bots.base.playwright_login_page import PlaywrightLoginPage
from src.bots.portale_fornitori.common.locators import CommonLocators
from src.core import config_manager
from src.core.constants import BotStatus, BrowserConfig, Timeouts
from src.core.exceptions import BrowserInitError
from src.core.logging import measure_time
from src.utils.browser_diagnostics import emergency_profile_reset
from src.utils.browser_profile_patcher import patch_browser_profile
from src.utils.helpers import cleanup_bot_processes

from .playwright_utils import get_playwright_selector

if TYPE_CHECKING:
    from src.bots.base.selenium_bot_config import SeleniumBotConfig


class PlaywrightBaseBot(BaseBot, ABC):
    """Classe base per i bot basati su Playwright.

    Centralizza la gestione del browser Chromium, la persistenza del profilo e i flag di sicurezza.

    Inizializza le proprietà fondamentali del bot Playwright.

    Args:
      config: Istanza di SeleniumBotConfig con le impostazioni del bot.
      **kwargs: Altri parametri di configurazione extra.
    """

    def __init__(
        self,
        config: SeleniumBotConfig,
        **kwargs: Any,
    ) -> None:
        super().__init__(config.username, config.password, config)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self.login_page: PlaywrightLoginPage | None = None

    @measure_time(threshold_ms=10000)
    def _init_driver(self) -> None:
        """Inizializza Playwright e il browser con logica di persistenza, stabilità e recovery."""
        self.status = BotStatus.INITIALIZING

        # 1. Configurazione ambiente e binari
        self._setup_playwright_env()

        # 2. Preparazione percorsi e opzioni
        user_data_dir = config_manager.CONFIG_DIR / "data" / BrowserConfig.CACHE_DIR_NAME
        user_data_dir.parent.mkdir(parents=True, exist_ok=True)

        downloads_dir = (
            Path(self.download_path).resolve()
            if self.download_path
            else (Path.home() / "Downloads").resolve()
        )
        downloads_dir.mkdir(parents=True, exist_ok=True)

        cfg = config_manager.load_config()
        headless = self.headless or cfg.get("browser_headless", False)
        launch_options = self._get_browser_launch_options(headless)

        # 3. Ottimizzazione e Patching profilo
        self._apply_pre_launch_patches(user_data_dir, downloads_dir)

        # 4. Tentativi di lancio
        self._launch_browser_with_retry(user_data_dir, downloads_dir, launch_options)

        self._setup_page_context()

        if self.context is None or self.page is None:
            raise BrowserInitError()

        self.login_page = PlaywrightLoginPage(self.page, self.log, self.ISAB_URL)

    def _setup_playwright_env(self) -> None:
        """Configura le variabili d'ambiente per i binari bundled di Playwright."""
        if not getattr(sys, "frozen", False):
            return

        bundle_dir = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(sys.executable).parent
        drivers_pw_path = bundle_dir / "drivers" / "ms-playwright"

        if drivers_pw_path.exists():
            self.log(f"[BUNDLE] Utilizzo binari Playwright inclusi: {drivers_pw_path}")
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(drivers_pw_path)
            with suppress(Exception):
                contents = [p.name for p in drivers_pw_path.iterdir() if p.is_dir()]
                self.log(f"[BUNDLE] Driver rilevati: {', '.join(contents)}")
        else:
            self.log("[WARNING] Binari Playwright bundled non trovati.", "WARNING")

    def _get_browser_launch_options(self, headless: bool) -> dict[str, Any]:
        """Restituisce le opzioni di lancio per Chromium ottimizzate per l'evasione."""
        return {
            "headless": headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
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
                "--disable-features=LeakDetection,PasswordLeakDetection,PasswordCheck,SafeBrowsingPasswordCheck,AutofillServerCommunication,AutofillAccountWalletStorage,OptimizationHints,OptimizationGuideFetching,OptimizationTargetPrediction,CredentialProviderExtension,BackgroundPasswordCheck,InsecureDownloadWarnings,PasswordManager,PasswordGeneration,SafeBrowsing,DownloadBubble,DownloadBubbleV2",
                "--force-fieldtrials=PasswordLeakDetection/Disabled",
                "--no-manage-passwords",
                "--disable-save-password-bubble",
                "--disable-single-click-autofill",
                "--disable-autofill",
                "--disable-password-generation",
                "--disable-password-manager-reauthentication",
                "--hide-crash-restore-bubble",
                "--disable-notifications",
                "--disable-search-engine-choice-screen",
            ],
        }

    def _apply_pre_launch_patches(self, user_data_dir: Path, downloads_dir: Path) -> None:
        """Esegue il cleanup e il patching del profilo prima del lancio."""
        self.log("[AVVIO] Ottimizzazione ambiente browser...")
        with suppress(Exception):
            cleanup_bot_processes()
            for lock in ("SingletonLock", "Lock", "DevToolsActivePort"):
                (user_data_dir / lock).unlink(missing_ok=True)

        with suppress(Exception):
            self.log("[AVVIO] Applicazione patch di sicurezza al profilo...")
            patch_browser_profile(user_data_dir, download_dir=downloads_dir)

    def _launch_browser_with_retry(
        self, user_data_dir: Path, downloads_dir: Path, launch_options: dict[str, Any]
    ) -> None:
        """Tenta il lancio del browser con logica di recovery automatica."""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                self.log(f"[AVVIO] Lancio Chromium (Tentativo {attempt + 1}/{max_retries})...")

                if not self.playwright:
                    self.playwright = sync_playwright().start()

                self.context = self.playwright.chromium.launch_persistent_context(
                    user_data_dir=str(user_data_dir),
                    no_viewport=False,
                    viewport={"width": 1920, "height": 1080},
                    user_agent=BrowserConfig.USER_AGENT,
                    accept_downloads=True,
                    downloads_path=str(downloads_dir),
                    **launch_options,
                )
            except Exception as e:
                err_msg = str(e)
                self.log(f"⚠️ Errore inizializzazione (T{attempt + 1}): {err_msg}", "WARNING")
                self._stop_playwright_internal()

                # Se fallisce il lancio, forziamo il reset del profilo per ripristinare database SQL/lock corrotti
                if attempt < max_retries - 1:
                    with suppress(Exception):
                        self.log(
                            "[RECOVERY] Rilevato fallimento avvio. Forzatura reset profilo per recupero da corruzioni...",
                            "WARNING",
                        )
                        if emergency_profile_reset(user_data_dir):
                            patch_browser_profile(user_data_dir, download_dir=downloads_dir)

                if attempt == max_retries - 1:
                    self.log("❌ Fallimento definitivo inizializzazione browser.", "ERROR")
                    raise
            else:
                return

    def _setup_page_context(self) -> None:
        """Configura la pagina e inietta gli script di evasione."""
        if not self.context:
            return

        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self.page.set_default_timeout(self.timeout * 1000)

        self.page.add_init_script("""
      Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
      if (navigator.credentials) {
        navigator.credentials.get = () => new Promise(() => {});
        navigator.credentials.store = () => new Promise(() => {});
      }
      const observer = new MutationObserver((mutations) => {
        const keywords = ['password', 'compromessa', 'sicurezza', 'cambia'];
        document.querySelectorAll('div, section, aside').forEach(el => {
          if (el.innerText && keywords.some(k => el.innerText.toLowerCase().includes(k))) {
            if (el.style.position === 'fixed' || el.style.zIndex > 1000) { el.remove(); }
          }
        });
      });
      observer.observe(document.documentElement, { childList: true, subtree: true });
    """)

        self.login_page = PlaywrightLoginPage(self.page, self.log, self.ISAB_URL)

    def cleanup(self) -> None:
        """Rilascia le risorse di Playwright e chiude il browser."""
        self.log("   Cleanup risorse Playwright...")
        self._stop_playwright_internal()

    def _stop_playwright_internal(self) -> None:
        """Ferma Playwright internamente senza loggare errori se già fermo."""
        if self.context:
            with suppress(Exception):
                self.context.close()
        if self.playwright:
            with suppress(Exception):
                self.playwright.stop()

        # Pulisce i processi orfani di Chrome/Node per rilasciare istantaneamente i lock sul filesystem
        with suppress(Exception):
            cleanup_bot_processes()

        self.page = None
        self.context = None
        self.playwright = None
        self.status = BotStatus.IDLE

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
            self.log(f"[DIAGNOSTICA] Stato errore salvato in: {edir.name}")

    def _login(self) -> bool:
        """Esegue il login delegandolo alla pagina di login specifica."""
        return self.login_page.login(self.username, self.password, self.company) if self.login_page else False

    def _get_selector(self, locator: tuple[str, str]) -> str:
        """Converte un locatore Selenium (By, value) in un selettore Playwright."""
        return get_playwright_selector(locator)

    def _wait_overlay(self, timeout_ms: int = Timeouts.OVERLAY * 1000) -> None:
        """Attende la scomparsa delle maschere di caricamento del portale."""
        if not self.page:
            return
        with suppress(Exception):
            xpath_combined = f"{CommonLocators.LOADING_MASK[1]} | {CommonLocators.LOADING_TEXT[1]}"
            self.page.wait_for_selector(f"xpath={xpath_combined}", state="hidden", timeout=timeout_ms)

    def _select_combobox_item(
        self, input_selector: str, arrow_selector: str, item_text: str, timeout_ms: int = 15000
    ) -> bool:
        """Seleziona un elemento in modo ultra-robusto emulando Selenium.

        Gestisce i duplicati nelle tab prendendo sempre il primo elemento visibile.
        """
        if not self.page:
            return False

        try:
            self.log(f" [COMBO] Selezione: '{item_text}'")

            # 1. Trigger freccia (usiamo .first per i duplicati ExtJS)
            with suppress(Exception):
                # Puntiamo al primo elemento visibile se ce ne sono multipli (come Selenium)
                arrow = self.page.locator(arrow_selector).first
                arrow.evaluate("el => el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}))")
                arrow.evaluate("el => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")

            # 2. Ricerca opzione nella lista (le liste ExtJS sono a fine body)
            option_xpath = f"xpath=//li[normalize-space(text())='{item_text}']"

            try:
                # Attesa breve per la comparsa dell'opzione (.first gestisce ambiguit )
                option = self.page.locator(option_xpath).first
                option.wait_for(state="attached", timeout=2000)
            except Exception:
                # 3. Fallback: Digitazione nell'input (sempre il primo visibile)
                self.log(" [COMBO] Opzione non trovata, digito nell'input...")
                inp = self.page.locator(input_selector).first

                inp.evaluate(
                    "el => { el.value = ''; el.dispatchEvent(new Event('input', {bubbles: true})); el.focus(); }"
                )
                inp.type(item_text, delay=20)
                self.page.wait_for_timeout(500)
                option = self.page.locator(option_xpath).first

            # 4. Click finale forzato via JS
            option.wait_for(state="attached", timeout=5000)
            option.evaluate("el => { el.scrollIntoView({block: 'nearest'}); el.click(); }")

            self._wait_overlay(timeout_ms=2000)
        except Exception as e:
            self.log(f" [COMBO] Errore: {str(e)[:50]}...")
            return False
        else:
            return True

    def _debug_dump_page(self, suffix: str = "debug") -> str:
        """Esegue una scansione profonda della pagina corrente e salva un report tecnico.

        Utilissimo per mappare campi dinamici di ExtJS.
        """
        if not self.page:
            return ""

        try:
            self.log(f"[DEBUG] Avvio scansione diagnostica pagina ({suffix})...")
            report_dir = config_manager.CONFIG_DIR / "logs" / "debug_dumps"
            report_dir.mkdir(parents=True, exist_ok=True)

            ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            filename = f"dump_{suffix}_{ts}.txt"
            filepath = report_dir / filename

            # Script JS per estrarre informazioni rilevanti da ExtJS e dal DOM
            scan_script = """
      () => {
        let info = "--- SYNCROJOB PAGE DUMP ---\\n";
        info += "URL: " + window.location.href + "\\n\\n";

        // 1. Cerca input e loro attributi
        info += "[INPUT FIELDS]\\n";
        document.querySelectorAll('input, textarea, select').forEach(el => {
          info += `- ID: ${el.id} | NAME: ${el.name} | TYPE: ${el.type} | VALUE: ${el.value} | VISIBLE: ${el.offsetParent !== null}\\n`;
        });

        // 2. Cerca trigger di combobox (le freccette)
        info += "\\n[COMBOBOX TRIGGERS]\\n";
        document.querySelectorAll('.x-form-trigger').forEach(el => {
          let parent = el.closest('.x-field') || {id: 'unknown'};
          info += `- ID: ${el.id} | CLASS: ${el.className} | FIELD_ID: ${parent.id}\\n`;
        });

        // 3. Cerca elementi della lista (gli li che compaiono nei dropdown)
        info += "\\n[VISIBLE LIST ITEMS]\\n";
        document.querySelectorAll('li.x-boundlist-item').forEach(el => {
          info += `- TEXT: ${el.innerText.trim()} | ID: ${el.id} | VISIBLE: ${el.offsetParent !== null}\\n`;
        });

        // 4. Struttura dei bottoni
        info += "\\n[BUTTONS]\\n";
        document.querySelectorAll('.x-btn').forEach(el => {
          info += `- TEXT: ${el.innerText.trim()} | ID: ${el.id} | ROLE: ${el.getAttribute('role')}\\n`;
        });

        return info;
      }
      """

            content = str(self.page.evaluate(scan_script))
            filepath.write_text(content, encoding="utf-8")
            self.log(f"[DEBUG] Scansione completata. Report salvato in: {filepath.name}")
        except Exception as e:
            self.log(f"[DEBUG] Errore durante il dump diagnostico: {e}")
            return ""
        else:
            return content
