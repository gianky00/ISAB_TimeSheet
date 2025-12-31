import logging
import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Importa PyMuPDF per la gestione dei PDF
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

# --- CONFIGURAZIONE LOGGING ---
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(message)s",
    datefmt="%H:%M"
)
logger = logging.getLogger(__name__)

# --- CONFIGURAZIONE CREDENZIALI E PARAMETRI ---
URL = "https://safework.isab.com/"
USERNAME = "gallegretti95"
PASSWORD = "coemi.2024"
PDL_DA_CERCARE = "529453/C"
DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Downloads')

def attendi_scomparsa_overlay(driver, timeout_secondi=120):
    try:
        WebDriverWait(driver, timeout_secondi).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[@id='GISWaitOverlay']"))
        )
    except TimeoutException:
        logger.warning("⏳ Ancora in caricamento...")
    try:
        modale = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'modal') and contains(@style, 'display: block')]"))
        )
        modale.find_element(By.XPATH, ".//button[contains(text(), 'OK') or @data-dismiss='modal']").click()
    except: pass
    time.sleep(0.5)

def gestisci_alert_ricerca(driver, timeout=10):
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            btn_ok = driver.find_element(By.XPATH, "//button[contains(@class, 'btn dialog-btn btn-ok')]")
            if btn_ok.is_displayed():
                logger.info("⚠️ Alert rilevato, clicco OK")
                btn_ok.click()
                time.sleep(1)
                return True
        except: pass
        time.sleep(0.5)
    return False

def attendi_e_ritorna_nuovo_pdf(download_dir, tempo_riferimento, timeout=60):
    scadenza = time.time() + timeout
    while time.time() < scadenza:
        files = glob.glob(os.path.join(download_dir, "*.pdf"))
        nuovi_files = [f for f in files if os.path.getmtime(f) > tempo_riferimento]
        if nuovi_files:
            nuovi_files.sort(key=os.path.getmtime, reverse=True)
            ultimo_file = nuovi_files[0]
            if not glob.glob(os.path.join(download_dir, "*.crdownload")):
                logger.info(f"✅ Download completato: {os.path.basename(ultimo_file)}")
                return ultimo_file
        time.sleep(1)
    return None

def unisci_pdf(file1, file2, output_path):
    if not fitz:
        logger.error("❌ PyMuPDF non installato")
        return False
    logger.info("🔄 Unione PDF in corso...")
    try:
        result = fitz.open()
        with fitz.open(file1) as pdf1: result.insert_pdf(pdf1)
        with fitz.open(file2) as pdf2: result.insert_pdf(pdf2)
        result.save(output_path)
        result.close()
        logger.info(f"✅ Documento finale pronto: {os.path.basename(output_path)}")
        return True
    except Exception as e:
        logger.error(f"❌ Errore unione: {e}")
        return False

def esegui_procedura():
    logger.info("Avvio Bot")
    
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    })
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 60)

    try:
        logger.info("🌐 Accesso a Safework...")
        driver.get(URL)
        
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ms-choice']"))).click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ms-drop')]//span[normalize-space()='ISAB Sud']"))).click()
        except: pass

        logger.info("🔐 Login...")
        wait.until(EC.visibility_of_element_located((By.ID, "inpUtente"))).send_keys(USERNAME)
        wait.until(EC.visibility_of_element_located((By.ID, "inpPassword"))).send_keys(PASSWORD)
        wait.until(EC.element_to_be_clickable((By.ID, "btnLogin"))).click()
        
        logger.info("⏳ Caricamento sistema...")
        xpath_caricamento = "//span[contains(text(), 'Caricamento...')]"
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_caricamento)))
        WebDriverWait(driver, 420).until(EC.invisibility_of_element_located((By.XPATH, xpath_caricamento)))
        attendi_scomparsa_overlay(driver)

        logger.info(f"🔍 Ricerca PdL {PDL_DA_CERCARE}...")
        campo_ricerca = wait.until(EC.visibility_of_element_located((By.ID, "fldRicercaPdLVeloce")))
        campo_ricerca.clear()
        campo_ricerca.send_keys(PDL_DA_CERCARE)
        time.sleep(0.5)
        campo_ricerca.send_keys(Keys.ENTER)
        
        gestisci_alert_ricerca(driver)
        attendi_scomparsa_overlay(driver)
        logger.info("✅ PdL trovato")

        # --- PARTE PRIMA ---
        logger.info("📄 Scarico Parte Prima")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        ts_1 = time.time()
        wait.until(EC.element_to_be_clickable((By.ID, "topIcon-acticonAnteprimaStampaMenu"))).click()
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.ID, "appItaliano"))).click()
        
        pdf_1 = attendi_e_ritorna_nuovo_pdf(DOWNLOAD_DIR, ts_1)
        if not pdf_1: raise Exception("Timeout Parte 1")
        
        path_temp_1 = os.path.join(DOWNLOAD_DIR, "temp_p1.pdf")
        if os.path.exists(path_temp_1): os.remove(path_temp_1)
        os.rename(pdf_1, path_temp_1)

        # --- PARTE SECONDA ---
        try:
            if not driver.find_element(By.ID, "lblPAFoglio").is_displayed():
                try: driver.find_element(By.ID, "lblTitoloParteSeconda").click()
                except: driver.find_element(By.XPATH, "//span[contains(text(), 'PARTE SECONDA')]").click()
                time.sleep(1)
            wait.until(EC.visibility_of_element_located((By.ID, "lblPAFoglio")))
        except: pass

        logger.info("📄 Scarico Parte Seconda")
        attendi_scomparsa_overlay(driver)
        driver.execute_script("window.scrollTo(0, 0);")
        ts_2 = time.time()
        
        is_single = False
        try:
            txt = driver.find_element(By.ID, "lblPAFoglio").find_element(By.XPATH, "..").text
            is_single = "1/1" in txt
        except: pass

        wait.until(EC.element_to_be_clickable((By.ID, "btnPrintPS"))).click()
        
        if not is_single:
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.ID, "rbStampaTutte"))).click()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.ID, "btnAnteprima"))).click()
        
        pdf_2 = attendi_e_ritorna_nuovo_pdf(DOWNLOAD_DIR, ts_2, timeout=90)
        if not pdf_2: raise Exception("Timeout Parte 2")

        path_temp_2 = os.path.join(DOWNLOAD_DIR, "temp_p2.pdf")
        if os.path.exists(path_temp_2): os.remove(path_temp_2)
        os.rename(pdf_2, path_temp_2)

        # --- FINE ---
        nome_finale = PDL_DA_CERCARE.replace("/", "-") + ".pdf"
        percorso_finale = os.path.join(DOWNLOAD_DIR, nome_finale)
        if os.path.exists(percorso_finale): os.remove(percorso_finale)

        if unisci_pdf(path_temp_1, path_temp_2, percorso_finale):
            os.remove(path_temp_1)
            os.remove(path_temp_2)
            logger.info("✨ Bot terminato")
        
    except Exception as e:
        logger.error(f"❌ Errore: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    esegui_procedura()