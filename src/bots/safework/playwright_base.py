# mypy: disable-error-code="no-untyped-call"
"""
SyncroJob - Playwright Safework Base Bot
Classe base specifica per SafeWork usando Playwright.
"""

from contextlib import suppress

from playwright.sync_api import TimeoutError

from src.bots.base.playwright_base_bot import PlaywrightBaseBot
from src.bots.safework.pages.playwright_login_page import PlaywrightSafeWorkLoginPage
from src.core.constants import URLs


class PlaywrightSafeworkBaseBot(PlaywrightBaseBot):
    """
    Classe base specifica per SafeWork (Playwright).
    Isola le logiche SafeWork da quelle del Portale Fornitori.
    """

    SAFEWORK_URL = URLs.SAFEWORK_URL
    ISAB_URL = SAFEWORK_URL

    def __init__(  # noqa: PLR0913
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = 30,
        download_path: str = "",
        account_type: str = "Esecutore",
    ) -> None:
        from src.bots.base.base_bot import BotConfig

        config = BotConfig(headless=headless, timeout=timeout, download_path=download_path)
        super().__init__(username, password, config)
        self.account_type = account_type
        self.safework_login_page: PlaywrightSafeWorkLoginPage | None = None

    def _init_driver(self) -> None:
        """Inizializza driver e page objects specifici."""
        super()._init_driver()
        if self.page:
            self.safework_login_page = PlaywrightSafeWorkLoginPage(self.page, self.log)

    def _login(self) -> bool:
        """Override del login per SafeWork usando Playwright."""
        if self.safework_login_page and self.page:
            self.page.goto(self.ISAB_URL)
            return self.safework_login_page.login(
                self.username, self.password, account_type=self.account_type
            )
        return False

    def click_robusto(self, selector: str, timeout_ms: int = 10000, label: str | None = None) -> None:
        """Tenta di cliccare un elemento gestendo overlay."""
        if not self.page:
            return

        if label:
            self.log(f"[CLICK] Click su {label}...")

        try:
            self._attendi_scomparsa_overlay()
            self.page.click(selector, timeout=timeout_ms)
        except Exception as e:
            self.log(f"❌ Errore click su {label or selector}: {e}")
            raise

    def _attendi_scomparsa_overlay(self, timeout_ms: int = 120000) -> bool:
        """Logica di attesa overlay specifica per SafeWork."""
        if not self.page:
            return False
        try:
            # GISWaitOverlay
            self.page.wait_for_selector("#GISWaitOverlay", state="hidden", timeout=timeout_ms)
        except TimeoutError:
            self.log("[ATTESA] Overlay ancora presente (proseguo...)")

        with suppress(Exception):
            # 1. Controllo specifico per Ricerca Estesa (Richiesto in Safework)
            self.log("[CERCA] Controllo presenza popup 'Ricerca Estesà...")
            popup_xpath = "//p[contains(text(), 'estenderla')]"

            # Usiamo wait_for_selector per attendere la comparsa reale (timeout breve)
            search_popup_visible = False
            with suppress(TimeoutError):
                self.page.wait_for_selector(f"xpath={popup_xpath}", state="visible", timeout=1500)
                search_popup_visible = True

            if search_popup_visible:
                self.log("[CLICK] Estensione ricerca...")
                for sel in (
                    "span[idtxt='E421C594']",
                    "//button[contains(., 'Si')]",
                    "xpath=//button[contains(@class, 'btn-ok')]",
                ):
                    with suppress(Exception):
                        xpath_full = sel if sel.startswith("/") else f"css={sel}"
                        if self.page.is_visible(xpath_full):
                            self.page.click(xpath_full, timeout=2000)
                            self.log("✅ Click su 'Sì riuscito (Ricerca Estesa)")
                            self.page.wait_for_timeout(1000)
                            return True
            else:
                self.log("ℹ️ Nessun popup di ricerca estesa rilevato.")

            # 2. Gestione Modali Generiche (es. Alert "Il PdL non  in programmazione")
            # Usiamo un ciclo di tentativi per gestire animazioni e caricamenti asincroni
            self.log("[ATTESA] Controllo Alert/Modali residue...")

            # Selettori pulsante robusti: classe btn-ok (standard), dialog-btn (Safework), o testo OK/Si/Yes
            btn_selectors = [
                "//button[contains(@class, 'btn-ok')]",
                "//button[contains(@class, 'dialog-btn')]",
                "//button[contains(., 'OK')]",
                "//span[contains(text(), 'OK')]",
                "//button[contains(., 'Si')]",
                "//a[contains(@class, 'btn-ok') or @data-dismiss='modal']",
            ]

            tentativi_max = 3
            for i in range(tentativi_max):  # Tentativi con mini-pause
                for b_sel in btn_selectors:
                    with suppress(Exception):
                        if self.page.is_visible(f"xpath={b_sel}", timeout=800):
                            self.page.click(f"xpath={b_sel}")
                            self.log(f"✅ Alert gestito cliccando su: {b_sel}")
                            self.page.wait_for_timeout(1000)
                            return True  # Chiudiamo al primo pulsante di conferma trovato

                if i < (tentativi_max - 1):
                    self.page.wait_for_timeout(500)

            self.log("ℹ️ Nessun Alert/Modale bloccante rilevata.")

        return True

    def _attendi_caricamento_sistema(self, timeout_ms: int = 420000) -> None:
        """Attesa specifica per SafeWork: 'Caricamento...'."""
        if not self.page:
            return
        xpath_caricamento = "xpath=//span[contains(text(), 'Caricamento...')]"
        try:
            with suppress(TimeoutError):
                self.page.wait_for_selector(xpath_caricamento, state="visible", timeout=3000)

            self.page.wait_for_selector(xpath_caricamento, state="hidden", timeout=timeout_ms)
        except TimeoutError:
            self.log("⚠️ Timeout attesa caricamento sistema.")

        self._attendi_scomparsa_overlay()
