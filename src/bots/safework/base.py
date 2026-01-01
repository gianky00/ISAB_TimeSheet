from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.bots.base.base_bot import BaseBot
from src.core.constants import Timeouts

class SafeworkBaseBot(BaseBot):
    """
    Classe base per i bot del portale SafeWork (safework.isab.com).
    Sovrascrive la logica di login e gestione attese specifica per questo portale.
    """
    
    SAFEWORK_URL = "https://safework.isab.com/"

    def _login(self) -> bool:
        """Login specifico per SafeWork."""
        self._check_stop()
        self.log(f"Navigazione a: {self.SAFEWORK_URL}")
        self.status = "LOGGING_IN"

        try:
            self.driver.get(self.SAFEWORK_URL)
            
            # Gestione selettore società (ISAB Sud) se presente
            try:
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ms-choice']"))).click()
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ms-drop')]//span[normalize-space()='ISAB Sud']"))).click()
            except: 
                pass

            self.log("Inserimento credenziali SafeWork...")
            
            # Verifica presenza campi login
            try:
                user_field = self.wait.until(EC.visibility_of_element_located((By.ID, "inpUtente")))
                pass_field = self.wait.until(EC.visibility_of_element_located((By.ID, "inpPassword")))
                login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "btnLogin")))
                
                user_field.clear()
                user_field.send_keys(self.username)
                pass_field.clear()
                pass_field.send_keys(self.password)
                
                login_btn.click()
            except TimeoutException:
                # Se non trovo i campi, potrei essere già loggato?
                if "Default.aspx" in self.driver.current_url:
                    self.log("✓ Sessione già attiva rilevata.")
                    return True
                raise

            self.log("Attesa caricamento sistema...")
            
            # Attesa specifica SafeWork
            xpath_caricamento = "//span[contains(text(), 'Caricamento...')]"
            try:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_caricamento)))
                WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((By.XPATH, xpath_caricamento)))
            except: 
                pass # A volte è troppo veloce
            
            self._attendi_scomparsa_overlay()

            self.log("✓ Login SafeWork completato.")
            return True

        except Exception as e:
            self.log(f"✗ Errore login SafeWork: {e}")
            return False

    def _attendi_scomparsa_overlay(self, timeout_secondi: int = 120) -> bool:
        """Attende la scomparsa dell'overlay (#GISWaitOverlay) e del testo 'Caricamento...'."""
        xpath_caricamento = "//span[contains(text(), 'Caricamento...')]"
        xpath_overlay = "//div[@id='GISWaitOverlay']"
        
        try:
            # 1. Piccola attesa per dare tempo agli elementi di apparire
            time.sleep(0.5)
            
            # 2. Attendi scomparsa overlay ID
            WebDriverWait(self.driver, timeout_secondi).until(
                EC.invisibility_of_element_located((By.ID, "GISWaitOverlay"))
            )
            
            # 3. Attendi scomparsa testo "Caricamento..."
            WebDriverWait(self.driver, timeout_secondi).until(
                EC.invisibility_of_element_located((By.XPATH, xpath_caricamento))
            )
            
            return True
        except TimeoutException:
            self.log("⏳ Caricamento ancora in corso o overlay persistente (Timeout)")
            return False
        finally:
            # Gestione modali imprevisti (es. errori o avvisi)
            try:
                # Cerca pulsanti OK in div che sembrano modali
                modale_btn = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'OK') or @data-dismiss='modal']")
                for btn in modale_btn:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(0.5)
            except: 
                pass

    @property
    def name(self) -> str:
        return "SafeWorkBot"

    @property
    def description(self) -> str:
        return "Bot Base SafeWork"
    
    @property
    def ISAB_URL(self) -> str:
        return self.SAFEWORK_URL
