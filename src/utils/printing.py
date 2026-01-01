import win32print
import os
import logging

logger = logging.getLogger(__name__)

def get_installed_printers():
    """Restituisce una lista di nomi delle stampanti installate."""
    try:
        printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        return printers
    except Exception as e:
        logger.error(f"Errore nel recupero stampanti: {e}")
        return []

def print_pdf(file_path, printer_name):
    """
    Stampa un PDF usando la stampante specificata.
    Usa ShellExecute per invocare il comando di stampa del sistema associato ai PDF,
    o win32print se necessario (ma per i PDF è complesso fare raw print).
    
    NOTA: Stampare PDF in modo silenzioso su una specifica stampante su Windows senza Adobe Reader 
    è complesso. Un approccio robusto è usare Ghostscript o simili, ma qui usiamo
    il metodo 'verb' di shell o tool esterni se disponibili.
    
    Per ora, dato che il requisito è 'win32', proviamo a cambiare la stampante di default temporaneamente
    o usare un comando specifico se Acrobat è installato.
    """
    if not os.path.exists(file_path):
        return False
        
    try:
        # Metodo 1: SetDefaultPrinter e ShellExecute "print"
        # Questo è il metodo più compatibile ma cambia la default printer dell'utente momentaneamente.
        
        current_default = win32print.GetDefaultPrinter()
        if printer_name and printer_name != current_default:
            win32print.SetDefaultPrinter(printer_name)
            
        try:
            os.startfile(file_path, "print")
            return True
        finally:
            # Ripristina
            if printer_name and printer_name != current_default:
                win32print.SetDefaultPrinter(current_default)
                
    except Exception as e:
        logger.error(f"Errore stampa: {e}")
        return False
