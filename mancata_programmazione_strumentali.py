# --- Importazioni Necessarie ---
import logging
import os
import time
from datetime import datetime

import openpyxl
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

try:
    import win32com.client

    xlCellTypeVisible = 12
except ImportError:
    logging.error("Libreria 'pywin32' non trovata. Per favore, installala con: pip install pywin32")
    win32com = None

# --- CONFIGURAZIONE LOGGING E COSTANTI ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# --- INFORMAZIONI DA CONFIGURARE ---
URL = "https://safework.isab.com/"
EXCEL_FILE_PATH = r"\\192.168.11.251\Database_Tecnico_SMI\cartella strumentale condivisa\ALLEGRETTI\ATTIVITA_PROGRAMMATE.xlsm"
EXCEL_SHEET_CREDENTIALS = "Inserimento dati"
EXCEL_CELL_USERNAME = "P7"
EXCEL_CELL_PASSWORD = "Q7"
FOGLIO_RIEPILOGO = "Riepilogo"
MACRO_DA_ESEGUIRE = "FiltraProgrGiornalieraRiepilogoDinamico"
COL_AREA = 4  # Col D
COL_PDL = 5  # Col E
COL_IMPIANTO = 6  # Col F
COL_DESCRIZIONE = 7  # Col G
COL_STATO = 13  # Col M
RIGA_INIZIO_DATI = 4
ID_PANNELLO_FILTRI = "pnlDataAttivita"

INDICI_COLONNE_FISSI = {"TCL": 4, "TGO_CTM": 5, "Richiedente": 7}

CC_DESTINATARI = "francesco.millo@coemi.it; ciro.scaravelli@coemi.it"

# --- FUNZIONI HELPER (Excel) ---


def get_excel_workbook_win32(file_path):
    """Ottiene un'istanza di Excel senza chiudere i processi esistenti."""
    if not win32com:
        raise ImportError("Modulo pywin32 non disponibile.")

    file_path = os.path.abspath(file_path)
    file_name = os.path.basename(file_path)

    # Tenta di agganciarsi a un'istanza esistente
    try:
        excel_app = win32com.client.GetActiveObject("Excel.Application")
        for wb in excel_app.Workbooks:
            if wb.FullName.lower() == file_path.lower() or wb.Name.lower() == file_name.lower():
                logger.info(f"File '{file_name}' già aperto. Lo script utilizzerà l'istanza esistente.")
                return excel_app, wb, True
    except Exception:
        pass

    logger.info("Apertura di una nuova istanza Excel in background.")
    excel_app = win32com.client.DispatchEx("Excel.Application")
    excel_app.Visible = False
    excel_app.DisplayAlerts = False
    excel_app.AskToUpdateLinks = False

    max_retries = 3
    for attempt in range(max_retries):
        try:
            workbook = excel_app.Workbooks.Open(file_path, ReadOnly=True, CorruptLoad=1)
            return excel_app, workbook, False
        except Exception as e:
            logger.warning(f"Tentativo {attempt + 1}/{max_retries} apertura fallito: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                excel_app.Quit()
                raise e


def esegui_macro_e_leggi_dati_visibili(file_path, nome_foglio, nome_macro):
    """Esegue la macro e legge i dati in modalità bulk ibrida."""
    logger.info("\n--- Fase 1 & 2: Esecuzione Macro e Lettura Excel ---")
    excel_app, wb, era_gia_aperto = None, None, False
    dati_pdl = []

    try:
        excel_app, wb, era_gia_aperto = get_excel_workbook_win32(file_path)

        logger.info(f"Esecuzione macro: '{nome_macro}'...")
        try:
            excel_app.Run(f"'{wb.Name}'!{nome_macro}")
        except Exception as em:
            logger.error(f"Errore macro: {em}")

        sheet = wb.Sheets(nome_foglio)
        last_row = sheet.UsedRange.Rows.Count + sheet.UsedRange.Row - 1
        if last_row < RIGA_INIZIO_DATI:
            return []

        # Bulk Read Matrice
        raw_range = sheet.Range(sheet.Cells(1, 1), sheet.Cells(last_row, 13))
        matrix = raw_range.Value

        # Identifica visibili
        data_range = sheet.Range(sheet.Cells(RIGA_INIZIO_DATI, 1), sheet.Cells(last_row, 1))
        try:
            visible_cells = data_range.SpecialCells(xlCellTypeVisible)
        except:
            return []

        righe_ignorate = 0
        for area in visible_cells.Areas:
            for r in range(area.Row, area.Row + area.Rows.Count):
                riga_dati = matrix[r - 1]
                pdl_val = riga_dati[COL_PDL - 1]
                if not pdl_val:
                    continue

                stato = str(riga_dati[COL_STATO - 1] or "").strip()
                if stato.upper() == "DA CHIUDERE":
                    righe_ignorate += 1
                    continue

                dati_pdl.append(
                    {
                        "Area": str(riga_dati[COL_AREA - 1] or "").strip(),
                        "PdL": str(pdl_val).strip(),
                        "Impianto": str(riga_dati[COL_IMPIANTO - 1] or "").strip(),
                        "Descrizione": str(riga_dati[COL_DESCRIZIONE - 1] or "").strip(),
                        "Stato PdL": stato,
                    }
                )

        logger.info(f"Trovati {len(dati_pdl)} PdL visibili. (Ignorati {righe_ignorate} 'DA CHIUDERE')")
        return dati_pdl

    finally:
        if wb and not era_gia_aperto:
            wb.Close(SaveChanges=False)
            logger.info("Workbook chiuso.")
        if excel_app and not era_gia_aperto:
            if excel_app.Workbooks.Count == 0:
                excel_app.Quit()
                logger.info("Istanza Excel chiusa.")
        elif era_gia_aperto:
            logger.info("Lo script si è sganciato lasciando Excel aperto come trovato.")


# --- FUNZIONI HELPER (SafeWork) ---


def leggi_valore_cella_excel(file_path, sheet_name, cell_address):
    try:
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        val = workbook[sheet_name][cell_address].value
        workbook.close()
        return str(val).strip() if val else ""
    except Exception as e:
        logger.error(f"Errore lettura credenziali: {e}")
        return None


def pulisci_e_inserisci_testo(driver, wait, by, value, testo, nome_log):
    try:
        attendi_scomparsa_overlay(driver)
        el = wait.until(EC.presence_of_element_located((by, value)))
        # Usa JavaScript per impostare il valore direttamente
        driver.execute_script("arguments[0].value = '';", el)
        driver.execute_script("arguments[0].value = arguments[1];", el, testo)
        # Trigger evento change per attivare eventuali listener
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", el)
        logger.info(f"Inserito '{testo}' in '{nome_log}'.")
    except Exception as e:
        logger.error(f"Errore input '{nome_log}': {e}")
        raise


def attendi_scomparsa_overlay(driver, timeout=120):
    """Attende che l'overlay di caricamento scompaia completamente."""

    def overlay_non_presente(drv):
        try:
            overlay = drv.find_element(By.ID, "GISWaitOverlay")
            # Se esiste, verifica che non sia visibile (display:none o opacity:0)
            return not overlay.is_displayed()
        except NoSuchElementException:
            return True

    try:
        WebDriverWait(driver, timeout).until(overlay_non_presente)
    except TimeoutException:
        logger.warning("Timeout attesa scomparsa overlay")


def clicca_elemento_sicuro(driver, wait, by, value, nome_log):
    """Clicca un elemento attendendo che l'overlay scompaia e usando JS come fallback."""
    attendi_scomparsa_overlay(driver)
    el = wait.until(EC.element_to_be_clickable((by, value)))
    try:
        el.click()
    except Exception:
        driver.execute_script("arguments[0].click();", el)
    logger.info(f"Click su '{nome_log}' eseguito.")


def esegui_login_e_naviga(driver, wait_medio, wait_lungo, user, pwd):
    driver.get(URL)
    wait_medio.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ms-choice']"))).click()
    wait_medio.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'ms-drop')]//span[normalize-space()='ISAB Sud']")
        )
    ).click()
    pulisci_e_inserisci_testo(driver, wait_medio, By.ID, "inpUtente", user, "Username")
    pulisci_e_inserisci_testo(driver, wait_medio, By.ID, "inpPassword", pwd, "Password")
    wait_medio.until(EC.element_to_be_clickable((By.ID, "btnLogin"))).click()

    logger.info("Login effettuato. Attesa caricamento...")
    xpath_caricamento = "//span[@style='margin-left: 10px;' and text()='Caricamento...']"
    # Attende comparsa del messaggio di caricamento
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_caricamento)))
    logger.info("Caricamento in corso...")
    # Attende scomparsa del messaggio di caricamento
    wait_lungo.until(EC.invisibility_of_element_located((By.XPATH, xpath_caricamento)))
    logger.info("Caricamento completato.")

    clicca_elemento_sicuro(driver, wait_lungo, By.ID, "topIcon-actHomePage", "Home Page")
    clicca_elemento_sicuro(driver, wait_lungo, By.ID, "sideBar-actVisualizzaAttivita", "Visualizza Attività")


def esegui_navigazione_con_tab(driver, n_tabs, azione):
    try:
        driver.find_element(By.ID, ID_PANNELLO_FILTRI).click()
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB * n_tabs).send_keys(Keys.ENTER).perform()
        logger.info(f"Azione '{azione}' eseguita (Fast).")
    except Exception as e:
        logger.error(f"Errore TAB '{azione}': {e}")
        raise


def analizza_risultati_sito(driver, indici):
    try:
        riga = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//table[contains(@class, 'table')]/tbody/tr[1]"))
        )
        celle = riga.find_elements(By.TAG_NAME, "td")
        if not celle:
            return False, False, "Nessun risultato"

        richiedente = celle[indici["Richiedente"]].text.strip()

        tcl = False
        try:
            title = (
                celle[indici["TCL"]]
                .find_element(By.XPATH, ".//input[contains(@id, '_TCL')]")
                .get_attribute("title")
            )
            if title and title.strip():
                tcl = True
        except:
            pass

        tgo = False
        try:
            title = (
                celle[indici["TGO_CTM"]]
                .find_element(By.XPATH, ".//input[contains(@id, '_TGO')]")
                .get_attribute("title")
            )
            if title and title.strip():
                tgo = True
        except:
            pass

        return tcl, tgo, richiedente
    except:
        return False, False, "Nessun risultato"


# --- MAIN LOOP ---


def main_loop():
    logger.info("====== INIZIO SCRIPT CONTROLLO FLAG TGO/CTM (FAST & DISCRETE MODE) ======")
    data_di_oggi = datetime.now().strftime("%d/%m/%Y")

    try:
        dati_da_verificare = esegui_macro_e_leggi_dati_visibili(
            EXCEL_FILE_PATH, FOGLIO_RIEPILOGO, MACRO_DA_ESEGUIRE
        )
        if not dati_da_verificare:
            logger.info("Nessun dato da verificare trovato. Fine.")
            return
    except Exception as e:
        logger.critical(f"Errore preparazione Excel: {e}")
        return

    driver = None
    dati_email = []

    try:
        # --- MODIFICA AGGRESSIVA ---
        opt = Options()
        opt.add_argument("--start-maximized")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--ignore-certificate-errors")

        # Disabilita specificamente il rilevamento delle password compromesse
        opt.add_argument("--disable-features=PasswordLeakDetection")
        opt.add_argument("--disable-save-password-bubble")

        # Preferenze per spegnere completamente il gestore password e Safe Browsing
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,  # Questo è il colpevole
            "safebrowsing.enabled": False,  # Disabilita il controllo generale di sicurezza
            "safebrowsing.disable_download_protection": True,
            "profile.default_content_setting_values.notifications": 2,
        }
        opt.add_experimental_option("prefs", prefs)

        # Nasconde la barra "Chrome è controllato da un software..."
        opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        opt.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=opt)

        wait_rapido = WebDriverWait(driver, 40)
        wait_medio = WebDriverWait(driver, 90)
        wait_lungo = WebDriverWait(driver, 300)

        user = leggi_valore_cella_excel(EXCEL_FILE_PATH, EXCEL_SHEET_CREDENTIALS, EXCEL_CELL_USERNAME)
        pwd = leggi_valore_cella_excel(EXCEL_FILE_PATH, EXCEL_SHEET_CREDENTIALS, EXCEL_CELL_PASSWORD)

        esegui_login_e_naviga(driver, wait_medio, wait_lungo, user, pwd)

        pulisci_e_inserisci_testo(driver, wait_rapido, By.ID, "programmazioneDal", data_di_oggi, "Data Dal")
        pulisci_e_inserisci_testo(driver, wait_rapido, By.ID, "programmazioneAl", data_di_oggi, "Data Al")

        logger.info("Impostazione filtro Sito...")
        try:
            attendi_scomparsa_overlay(driver)
            btn = wait_rapido.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//select[@id='fldIdSito']/following-sibling::div/button")
                )
            )
            btn.click()
            chk = wait_rapido.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//label//span[normalize-space()='[Seleziona tutti]']")
                )
            )
            driver.execute_script("arguments[0].click();", chk)
            btn.click()
        except:
            pass

        for i, dati in enumerate(dati_da_verificare):
            pdl = dati["PdL"]
            logger.info(f"Verifica {i + 1}/{len(dati_da_verificare)}: {pdl}")
            try:
                pulisci_e_inserisci_testo(driver, wait_rapido, By.ID, "fldNumPermesso", pdl, f"PdL {pdl}")
                esegui_navigazione_con_tab(driver, 25, "Cerca")
                attendi_scomparsa_overlay(driver)

                tcl, tgo, rich = analizza_risultati_sito(driver, INDICI_COLONNE_FISSI)

                if rich == "Nessun risultato":
                    continue

                if not tcl or not tgo:
                    causa = (
                        "Flag TCL e TGO mancanti"
                        if not tcl and not tgo
                        else ("Flag TCL mancante" if not tcl else "Flag TGO mancante")
                    )
                    dati["Richiedente"] = rich
                    dati["Causa"] = causa
                    dati_email.append(dati)
                    logger.warning(f"  -> ANOMALIA rilevata: {causa}")
            except Exception as e:
                logger.error(f"Errore loop PdL {pdl}: {e}")

    except Exception as e:
        logger.critical(f"Errore script: {e}")
    finally:
        if driver:
            driver.quit()

    if not dati_email:
        logger.info("Nessuna anomalia rilevata.")
        return

    # --- EMAIL ---
    richiedenti_unici = set(r["Richiedente"] for r in dati_email)
    dati_ordinati = sorted(dati_email, key=lambda x: x["Richiedente"])

    lista_to = []
    for r in richiedenti_unici:
        p = r.split()
        if len(p) >= 2:
            lista_to.append(f"{p[1][0].lower()}{p[0].lower()}@isab.com")

    oggetto = f"Mancata programmazione attività manutenzione del {data_di_oggi}"
    saluto = (
        f"Gentilissimo {list(richiedenti_unici)[0].split()[1]},"
        if len(richiedenti_unici) == 1
        else "Gentilissimi,"
    )
    poss = "tua" if len(richiedenti_unici) == 1 else "vostra"

    tbl = "<table border='1' style='border-collapse:collapse; font-family: Calibri; font-size: 11pt;'>\n"
    tbl += "<tr style='background:#f2f2f2;'><th>Richiedente</th><th>Area</th><th>PdL</th><th>Impianto</th><th>Descrizione</th><th>Stato</th><th>Causa</th></tr>\n"
    for r in dati_ordinati:
        tbl += f"<tr><td>{r['Richiedente']}</td><td>{r['Area']}</td><td>{r['PdL']}</td><td>{r['Impianto']}</td><td>{r['Descrizione']}</td><td>{r['Stato PdL']}</td><td style='color:red;'>{r['Causa']}</td></tr>\n"
    tbl += "</table>"

    corpo = f"<p style='font-family: Calibri;'>{saluto}</p><p>per {poss} conoscenza trasmetto mancata programmazione attività:</p><br>{tbl}<br>"

    try:
        out = win32com.client.Dispatch("Outlook.Application")
        mail = out.CreateItem(0)
        mail.Subject = oggetto
        mail.To = "; ".join(lista_to)
        mail.CC = CC_DESTINATARI
        mail.Display()
        mail.HTMLBody = corpo + mail.HTMLBody
        logger.info("Bozza Outlook generata.")
    except Exception as e:
        logger.error(f"Errore Outlook: {e}")


if __name__ == "__main__":
    if win32com:
        main_loop()
    time.sleep(5)
