"""
SyncroJob - Preventivi Generator Manager
Gestisce la generazione di preventivi Excel a partire da un file Master con macro.
Implementa una tecnica avanzata di "Sanitizzazione XML" per eliminare i bug 
dei Nomi Definiti (Print_Area) prima di lanciare l'automazione Win32COM.
"""

import os
import shutil
import re
import zipfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from src.core.logging import get_logger

try:
    import win32com.client
    _win32com_found = True
except ImportError:
    _win32com_found = False

logger = get_logger(__name__)


class PreventiviGeneratorManager:
    """Manager avanzato per la generazione di preventivi basati su template Excel Master."""

    def __init__(self, master_path: str):
        self.master_path = master_path
        self.excel_app: Any = None
        self.wb_copy: Any = None

    def get_next_progressive(self, directory: str) -> str:
        if not os.path.exists(directory):
            return "001"

        max_num = 0
        pattern = re.compile(r"(\d{3})[-/]\d{2}")
        
        try:
            for f in os.listdir(directory):
                match = pattern.search(f)
                if match:
                    num = int(match.group(1))
                    if num > max_num:
                        max_num = num
            
            return f"{max_num + 1:03d}"
        except Exception as e:
            logger.warning(f"Errore calcolo progressivo: {e}")
            return "001"

    def _sanitize_excel_file(self, filepath: str):
        """
        TECNICA CHIRURGICA: Decomprime il file XLSM, rimuove i nomi definiti corrotti 
        (Print_Area) direttamente dall'XML per evitare i blocchi di Excel, e ricomprime.
        Questo preserva il 100% delle macro e dei pulsanti ActiveX.
        """
        temp_dir = tempfile.mkdtemp()
        try:
            # Estrae l'intero archivio xlsm
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                
            wb_xml_path = os.path.join(temp_dir, 'xl', 'workbook.xml')
            if os.path.exists(wb_xml_path):
                with open(wb_xml_path, 'r', encoding='utf-8') as f:
                    xml = f.read()
                
                # Rimuove chirurgicamente ogni traccia di "Print_Area" che causa il popup
                xml = re.sub(r'<definedName[^>]*name="[^"]*Print_Area"[^>]*>.*?</definedName>', '', xml, flags=re.IGNORECASE|re.DOTALL)
                xml = re.sub(r'<definedName[^>]*name="[^"]*Print_Area"[^>]*/>', '', xml, flags=re.IGNORECASE)
                
                with open(wb_xml_path, 'w', encoding='utf-8') as f:
                    f.write(xml)
                    
            # Ricomprime il file
            temp_zip = filepath + ".tmp"
            with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_out.write(file_path, arcname)
                        
            # Sostituisce il file originale con quello pulito
            shutil.move(temp_zip, filepath)
            logger.info("Sanitizzazione XML completata con successo: Print_Area rimosso.")
        except Exception as e:
            logger.error(f"Errore durante la sanitizzazione zip: {e}")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def generate_preventivo(self, data: dict[str, Any], output_dir: str) -> tuple[bool, str]:
        if not _win32com_found:
            return False, "Libreria pywin32 non trovata."

        if not self.master_path or not Path(self.master_path).exists():
            return False, f"File Master non trovato: {self.master_path}"

        try:
            out_path = Path(output_dir)
            out_path.mkdir(parents=True, exist_ok=True)

            prog = data.get("progressivo", "000")
            year_short = data.get("anno_short", datetime.now().strftime("%y"))
            filename = f"{prog}-{year_short}.xlsm"
            dest_file = out_path / filename

            # 1. Copia fisica (3.7MB conservati)
            shutil.copy2(self.master_path, dest_file)

            # 2. SANITIZZAZIONE XML - Rimuove Print_Area prima che Excel lo veda
            self._sanitize_excel_file(str(dest_file))

            # 3. Compilazione tramite Win32COM
            success, msg = self._fill_excel_data(str(dest_file), data)
            if not success:
                return False, msg

            return True, str(dest_file)

        except Exception as e:
            logger.error(f"Errore generazione: {e}", exc_info=True)
            return False, str(e)

    def _fill_excel_data(self, file_path: str, data: dict[str, Any]) -> tuple[bool, str]:
        try:
            self.excel_app = win32com.client.Dispatch("Excel.Application")
            
            # Modalità invisibile ora è sicura perché il file è stato curato
            self.excel_app.Visible = False
            self.excel_app.DisplayAlerts = False
            self.excel_app.AskToUpdateLinks = False

            # Apre il file senza scatenare ricalcoli e aggiornamenti
            self.wb_copy = self.excel_app.Workbooks.Open(file_path, UpdateLinks=0)
            
            try:
                sheet = self.wb_copy.Sheets("inserimento dati")
            except Exception:
                return False, "Foglio 'inserimento dati' non trovato nel file Master."

            # --- MAPPATURA ---
            sheet.Range("A5").Value = data.get("data", "")
            sheet.Range("A7").Value = data.get("tcl", "")
            sheet.Range("B5").Value = data.get("odc", "")
            sheet.Range("C7").Value = data.get("avviso", "")
            sheet.Range("C5").Value = data.get("ordine", "")
            
            sheet.Range("D11").Value = data.get("stato_attivita", "")
            sheet.Range("D13").Value = data.get("tipologia_preventivo", "")
            sheet.Range("E13").Value = data.get("tipologia_economia", "")

            desc_lavoro = data.get("descrizione_lavoro", "")
            lines = desc_lavoro.split("\n")[:11]
            for i, line in enumerate(lines):
                sheet.Range(f"A{11 + i}").Value = line

            sheet.Range("A32").Value = data.get("descrizione_relazione", "")

            # Progressivo
            try:
                vba_ref = self.wb_copy.Sheets("rif.VBA")
                vba_ref.Range("A4").Value = f"{data.get('progressivo', '000')}/{data.get('anno_short', '26')}"
            except Exception:
                pass

            self.wb_copy.Save()
            return True, "OK"

        except Exception as e:
            logger.error(f"Errore scrittura Excel COM: {e}")
            return False, f"Errore automazione Excel: {e}"
        finally:
            self._cleanup()

    def _cleanup(self):
        try:
            if self.wb_copy:
                self.wb_copy.Close(SaveChanges=False)
        except Exception:
            pass
            
        try:
            if self.excel_app:
                self.excel_app.DisplayAlerts = True
                self.excel_app.Quit()
        except Exception:
            pass
            
        self.wb_copy = None
        self.excel_app = None
