from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.bots.base.base_bot import BaseBot


class SafeworkBaseBot(BaseBot):
    """
    Classe base specifica per SafeWork.
    Isola le logiche SafeWork da quelle del Portale Fornitori.
    """

    SAFEWORK_URL = "https://safework.isab.com/"
    ISAB_URL = SAFEWORK_URL

    def _attendi_scomparsa_overlay(self, timeout_secondi: int = 120) -> bool:
        """Logica di attesa fedele allo script originale."""
        if not self.driver:
            return False
        try:
            # Attende la scomparsa dell'overlay grigio
            WebDriverWait(self.driver, timeout_secondi).until(
                EC.invisibility_of_element_located((By.ID, "GISWaitOverlay"))
            )
        except TimeoutException:
            self.log("⏳ Overlay ancora presente (proseguo...)")

        # Gestione modale OK/Annulla se appare
        try:
            modale = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'modal') and contains(@style, 'display: block')]",
                    )
                )
            )
            modale.find_element(
                By.XPATH, ".//button[contains(text(), 'OK') or @data-dismiss='modal']"
            ).click()
            self.log("ℹ️ Modale gestita (OK/Annulla).")
        except Exception:
            pass

        # No sleep needed: invisibility check is sufficient
        return True

    def _attendi_caricamento_sistema(self):
        """Implementa l'attesa specifica: compare e poi scompare."""
        if not self.driver:
            return
        xpath_caricamento = "//span[contains(text(), 'Caricamento...')]"
        try:
            self.log("⏳ Attesa comparsa caricamento...")
            WebDriverWait(self.driver, 120).until(
                EC.visibility_of_element_located((By.XPATH, xpath_caricamento))
            )
            self.log("⏳ Sistema in caricamento, attesa completamento...")
            WebDriverWait(self.driver, 420).until(
                EC.invisibility_of_element_located((By.XPATH, xpath_caricamento))
            )
            self.log("✅ Caricamento sistema completato.")
        except TimeoutException:
            self.log("⚠️ Timeout attesa caricamento (proseguo...)")

        self._attendi_scomparsa_overlay()

    @property
    def name(self) -> str:
        return "SafeWorkBot"

    @property
    def description(self) -> str:
        return "Bot Base SafeWork"
