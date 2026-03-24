import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Any, cast

import fitz
import win32con
import win32print

try:
    import win32ui
except ImportError:
    win32ui = None  # type: ignore

from PIL import Image, ImageWin

logger = logging.getLogger(__name__)


def get_installed_printers() -> list[str]:
    """Restituisce una lista di nomi delle stampanti installate."""
    try:
        return [str(printer[2]) for printer in win32print.EnumPrinters(2)]
    except Exception:
        logger.exception("Errore nel recupero stampanti")
        return []


def _run_powershell(command: str) -> subprocess.CompletedProcess[str] | None:
    """Esegue un comando PowerShell e restituisce l'output."""
    try:
        creation_flags = 0x08000000  # CREATE_NO_WINDOW
        return subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            creationflags=creation_flags,
            check=False,
        )
    except Exception:
        logger.exception("Errore esecuzione PowerShell")
        return None


def _set_printer_duplex_powershell(printer_name: str, mode: str = "OneSided") -> bool:
    """
    Tenta di forzare la modalità via PowerShell.
    Non è critico se fallisce, poiché la strategia 'Split Jobs' garantirà comunque fogli separati.
    """
    try:
        cmd_set = f"Set-PrintConfiguration -PrinterName '{printer_name}' -DuplexingMode {mode}"
        _run_powershell(cmd_set)
    except Exception as e:
        logger.warning(f"Warning configurazione PS: {e}")
        return False
    else:
        return True


def print_pdf(file_path: str, printer_name: str) -> bool:
    """
    Stampa un PDF usando la stampante specificata.
    STRATEGIA 'NUCLEAR' PER SIMPLEX:
    Invia ogni pagina del PDF come un lavoro di stampa (Job) separato.
    Questo impedisce fisicamente alla stampante di fare fronte-retro tra le pagine,
    poiece le considera documenti distinti.
    """
    if not Path(file_path).exists():
        return False

    try:
        current_default = win32print.GetDefaultPrinter()
        target_printer = printer_name or current_default

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
                hdc = cast("Any", win32ui).CreateDC()
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
                    img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
                    if mode == "RGBA":
                        img = img.convert("RGB")

                    # Stampa Fit-to-Page
                    dib = ImageWin.Dib(img)
                    dib.draw(hdc.GetHandleOutput(), (0, 0, horz_res, vert_res))

                except Exception:
                    logger.exception(f"Errore rendering pagina {page_num + 1}")
                    hdc.AbortDoc()
                    raise

                # 4. Chiudi Pagina e Documento -> FORZA ESPULSIONE FOGLIO
                hdc.EndPage()
                hdc.EndDoc()
                hdc.DeleteDC()

                # Piccola pausa per dare ordine allo spooler
                time.sleep(0.5)

            doc.close()
            logger.info("Ciclo di stampa completato.")
        except Exception:
            logger.exception("Errore durante la stampa split")
            raise
        else:
            return True

    except Exception:
        logger.exception("Errore critico stampa")
        # Fallback disperato
        try:
            os.startfile(file_path, "print")  # noqa: S606
        except Exception:
            return False
        else:
            return True
