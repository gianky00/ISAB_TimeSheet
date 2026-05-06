# mypy: disable-error-code="no-any-unimported, unused-ignore"
"""
SyncroJob - Playwright Base Bot
Implementazione della classe base per i bot Playwright.
"""

import re
import sys
from abc import ABC
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.bots.base.base_bot import BaseBot
from src.bots.base.playwright_login_page import PlaywrightLoginPage
from src.bots.portale_fornitori.common.locators import CommonLocators
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
    def _init_driver(self) -> None:  # noqa: PLR0915
        """Inizializza Playwright e il browser con logica di persistenza, stabilità e recovery."""
        import os  # noqa: PLC0415

        from src.utils.browser_profile_patcher import patch_browser_profile  # noqa: PLC0415

        self.status = BotStatus.INITIALIZING

        # --- CONFIGURAZIONE BINARI BUNDLED ---
        # Determina la cartella base (src se in dev, root se bundle)
        if getattr(sys, "frozen", False):
            # Percorso dell'eseguibile (PyInstaller/Nuitka)
            bundle_dir = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(sys.executable).parent
            drivers_pw_path = bundle_dir / "drivers" / "ms-playwright"

            if drivers_pw_path.exists():
                self.log(f"[BUNDLE] Utilizzo binari Playwright inclusi nel pacchetto: {drivers_pw_path}")
                os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(drivers_pw_path)

                # Debug log per verificare i contenuti della cartella driver (utile per diagnosticare shell headless mancanti)
                with suppress(Exception):
                    contents = [p.name for p in drivers_pw_path.iterdir() if p.is_dir()]
                    self.log(f"[BUNDLE] Contenuto driver rilevato: {', '.join(contents)}")
            else:
                self.log(
                    "[WARNING] Binari Playwright bundled non trovati, uso percorso di sistema.", "WARNING"
                )
        # -------------------------------------

        user_data_dir = config_manager.CONFIG_DIR / "data" / BrowserConfig.CACHE_DIR_NAME

        # Assicura esistenza directory dati
        user_data_dir.parent.mkdir(parents=True, exist_ok=True)

        cfg = config_manager.load_config()
        headless = self.headless or cfg.get("browser_headless", False)

        downloads_dir = (
            Path(self.download_path).resolve()
            if self.download_path
            else (Path.home() / "Downloads").resolve()
        )
        downloads_dir.mkdir(parents=True, exist_ok=True)

        launch_options = {
            "headless": headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
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

        # 1. Cleanup processi e file di lock (senza resettare l'intero profilo)
        self.log("[AVVIO] Ottimizzazione ambiente browser...")
        with suppress(Exception):
            cleanup_bot_processes()
            # Rimuove solo i file di lock che impediscono l'avvio, preservando le Preferences patchate
            for lock in ("SingletonLock", "Lock", "DevToolsActivePort"):
                lock_path = user_data_dir / lock
                if lock_path.exists():
                    lock_path.unlink(missing_ok=True)

        # 2. Patching preventivo del profilo per sopprimere popup sicurezza
        # Ora è efficace perché non rinominiamo la cartella subito dopo
        with suppress(Exception):
            self.log("[AVVIO] Applicazione patch di sicurezza al profilo...")
            patch_browser_profile(user_data_dir, download_dir=downloads_dir)


        # 3. Tentativi di inizializzazione
        max_retries = 3

        for attempt in range(max_retries):
            try:
                self.log(f"[AVVIO] Setup ambiente browser (Tentativo {attempt + 1}/{max_retries})...")

                if not self.playwright:
                    self.log("[AVVIO] Inizializzazione Playwright Core...")
                    self.playwright = sync_playwright().start()

                self.log(f"[AVVIO] Lancio Chromium con profilo persistente: {user_data_dir.name}")
                self.context = self.playwright.chromium.launch_persistent_context(
                    user_data_dir=str(user_data_dir),
                    no_viewport=False,
                    viewport={"width": 1920, "height": 1080},
                    user_agent=BrowserConfig.USER_AGENT,
                    accept_downloads=True,
                    downloads_path=str(downloads_dir),
                    **launch_options,
                )

                break  # Successo


            except Exception as e:
                err_msg = str(e)
                self.log(f"[ATTENZIONE] Errore inizializzazione (T{attempt + 1}): {err_msg}", "WARNING")

                # Pulizia forzata dello stato interno ad ogni fallimento
                self._stop_playwright_internal()

                # Recovery automatico: alcuni profili persistenti corrotti causano
                # "Browser.getWindowForTarget: Browser window not found" all'avvio.
                if "Browser.getWindowForTarget" in err_msg:
                    with suppress(Exception):
                        from src.utils.browser_diagnostics import emergency_profile_reset  # noqa: PLC0415

                        self.log("[RECOVERY] Profilo browser instabile, reset automatico in corso...", "WARNING")
                        if emergency_profile_reset(user_data_dir):
                            patch_browser_profile(user_data_dir, download_dir=downloads_dir)
                            self.log("[RECOVERY] Nuovo profilo creato e patchato. Riprovo avvio browser...")

                # Se è l'ultimo tentativo, rilanciamo l'errore definitivo
                if attempt == max_retries - 1:
                    self.log(
                        "[ERRORE] Impossibile inizializzare il browser dopo molteplici tentativi.", "ERROR"
                    )
                    raise

        if self.context is None:
            raise RuntimeError("BrowserInitFailed")

        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        # Playwright usa millisecondi per il timeout
        self.page.set_default_timeout(self.timeout * 1000)

        # Init script per sopprimere webdriver detection e avvisi password
        self.page.add_init_script("""
            // 1. Evasione base
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});

            // 2. Neutralizzazione Credential Management API (blocca popup nativi)
            if (navigator.credentials) {
                navigator.credentials.get = () => new Promise(() => {});
                navigator.credentials.store = () => new Promise(() => {});
            }

            // 3. Monitoraggio e rimozione forzata di banner/popup "Cambia Password"
            const observer = new MutationObserver((mutations) => {
                const keywords = ['password', 'compromessa', 'sicurezza', 'cambia'];
                document.querySelectorAll('div, section, aside').forEach(el => {
                    if (el.innerText && keywords.some(k => el.innerText.toLowerCase().includes(k))) {
                        // Se sembra un banner di sistema iniettato, lo nascondiamo
                        if (el.style.position === 'fixed' || el.style.zIndex > 1000) {
                            el.remove();
                        }
                    }
                });
            });
            observer.observe(document.documentElement, { childList: true, subtree: true });
        """)
        self.login_page = PlaywrightLoginPage(self.page, self.log, self.ISAB_URL)

    def cleanup(self) -> None:
        """Rilascia le risorse di Playwright e chiude il browser."""
        self.log("🧹 Cleanup risorse Playwright...")
        self._stop_playwright_internal()

    def _stop_playwright_internal(self) -> None:
        """Ferma Playwright internamente senza loggare errori se già fermo."""
        if self.context:
            with suppress(Exception):
                # Chiude tutte le pagine prima del contesto
                for page in self.context.pages:
                    with suppress(Exception):
                        page.close()
                self.context.close()
        if self.playwright:
            with suppress(Exception):
                self.playwright.stop()

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
        from .playwright_utils import get_playwright_selector  # noqa: PLC0415

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
        """
        Seleziona un elemento in modo ultra-robusto emulando Selenium.
        Gestisce i duplicati nelle tab prendendo sempre il primo elemento visibile.
        """
        if not self.page:
            return False

        try:
            self.log(f"  [COMBO] Selezione: '{item_text}'")

            # 1. Trigger freccia (usiamo .first per i duplicati ExtJS)
            with suppress(Exception):
                # Puntiamo al primo elemento visibile se ce ne sono multipli (come Selenium)
                arrow = self.page.locator(arrow_selector).first
                arrow.evaluate("el => el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}))")
                arrow.evaluate("el => el.dispatchEvent(new MouseEvent('click', {bubbles: true}))")

            # 2. Ricerca opzione nella lista (le liste ExtJS sono a fine body)
            option_xpath = f"xpath=//li[normalize-space(text())='{item_text}']"

            try:
                # Attesa breve per la comparsa dell'opzione (.first gestisce ambiguità)
                option = self.page.locator(option_xpath).first
                option.wait_for(state="attached", timeout=2000)
            except Exception:
                # 3. Fallback: Digitazione nell'input (sempre il primo visibile)
                self.log("  [COMBO] Opzione non trovata, digito nell'input...")
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
            self.log(f"  [COMBO] Errore: {str(e)[:50]}...")
            return False
        else:
            return True

    def _debug_dump_page(self, suffix: str = "debug") -> str:
        """
        Esegue una scansione profonda della pagina corrente e salva un report tecnico.
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
