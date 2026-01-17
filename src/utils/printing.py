import logging
import os
import subprocess
import time

import fitz  # type: ignore
import win32con
import win32print
import win32ui
from PIL import Image, ImageWin  # type: ignore

logger = logging.getLogger(__name__)


def get_installed_printers():
    """Restituisce una lista di nomi delle stampanti installate."""
    try:
        printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        return printers
    except Exception as e:
        logger.error(f"Errore nel recupero stampanti: {e}")
        return []


def _run_powershell(command):
    """Esegue un comando PowerShell e restituisce l'output."""
    try:
        creation_flags = 0x08000000  # CREATE_NO_WINDOW
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            creationflags=creation_flags,
        )
        return result
    except Exception as e:
        logger.error(f"Errore esecuzione PowerShell: {e}")
        return None


def _set_printer_duplex_powershell(printer_name, mode="OneSided"):
    """
    Tenta di forzare la modalità via PowerShell.
    Non è critico se fallisce, poiché la strategia 'Split Jobs' garantirà comunque fogli separati.
    """
    try:
        cmd_set = f"Set-PrintConfiguration -PrinterName '{printer_name}' -DuplexingMode {mode}"
        _run_powershell(cmd_set)
    except Exception as e:
        logger.warning(f"Warning configurazione PS: {e}")


def print_pdf(file_path, printer_name):
    """
    Stampa un PDF usando la stampante specificata.
    STRATEGIA 'NUCLEAR' PER SIMPLEX:
    Invia ogni pagina del PDF come un lavoro di stampa (Job) separato.
    Questo impedisce fisicamente alla stampante di fare fronte-retro tra le pagine,
    poiché le considera documenti distinti.
    """
    if not os.path.exists(file_path):
        return False

    try:
        current_default = win32print.GetDefaultPrinter()
        target_printer = printer_name if printer_name else current_default

        logger.info(f"Avvio stampa 'Split Jobs' di {file_path} su {target_printer}")

        # Tentativo best-effort di configurazione (opzionale ma utile)
        _set_printer_duplex_powershell(target_printer, "OneSided")

        try:
            doc = fitz.open(file_path)
            total_pages = len(doc)

            # Loop per inviare OGNI PAGINA come JOB SEPARATO
            for page_num in range(total_pages):
                logger.debug(f"Invio pagina {page_num + 1} di {total_pages}...")

                # 1. Crea un NUOVO contesto di stampa per ogni pagina
                hdc = win32ui.CreateDC()
                hdc.CreatePrinterDC(target_printer)

                # 2. Avvia un NUOVO documento (Job)
                job_name = f"{os.path.basename(file_path)} - Pag {page_num + 1}/{total_pages}"
                hdc.StartDoc(job_name)
                hdc.StartPage()

                # 3. Renderizza la pagina
                try:
                    # Recupera risoluzione stampante
                    horz_res = hdc.GetDeviceCaps(win32con.HORZRES)
                    vert_res = hdc.GetDeviceCaps(win32con.VERTRES)

                    page = doc[page_num]

                    # Rendering Alta Risoluzione (~300 DPI)
                    mat = fitz.Matrix(4, 4)
                    pix = page.get_pixmap(matrix=mat)

                    # Conversione PIL
                    mode = "RGBA" if pix.alpha else "RGB"
                    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                    if mode == "RGBA":
                        img = img.convert("RGB")

                    # Stampa Fit-to-Page
                    dib = ImageWin.Dib(img)
                    dib.draw(hdc.GetHandleOutput(), (0, 0, horz_res, vert_res))

                except Exception as render_err:
                    logger.error(f"Errore rendering pagina {page_num + 1}: {render_err}")
                    hdc.AbortDoc()
                    raise render_err

                # 4. Chiudi Pagina e Documento -> FORZA ESPULSIONE FOGLIO
                hdc.EndPage()
                hdc.EndDoc()
                hdc.DeleteDC()

                # Piccola pausa per dare ordine allo spooler
                time.sleep(0.5)

            doc.close()
            logger.info("Ciclo di stampa completato.")
            return True

        except Exception as e:
            logger.error(f"Errore durante la stampa split: {e}")
            raise e

    except Exception as e:
        logger.error(f"Errore critico stampa: {e}")
        # Fallback disperato
        try:
            os.startfile(file_path, "print")
            return True
        except Exception:
            return False
