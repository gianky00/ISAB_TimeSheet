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
        super().__init__(username, password, headless, timeout, download_path)
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
            self.log(f"[ERRORE] Errore click su {label or selector}: {e}")
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
            modale_xpath = "//div[contains(@class, 'modal') and contains(@style, 'display: block')]"
            if self.page.is_visible(f"xpath={modale_xpath}", timeout=3000):
                btn_xpath = ".//*[self::button or self::span or self::a][contains(text(), 'OK') or contains(text(), 'Si') or contains(text(), 'Yes') or @data-dismiss='modal']"
                self.page.click(f"xpath={modale_xpath}{btn_xpath}")
                self.log("[INFO] Modale gestita (OK/Annulla/Si/Yes).")

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
            self.log("[ATTENZIONE] Timeout attesa caricamento sistema.")

        self._attendi_scomparsa_overlay()
