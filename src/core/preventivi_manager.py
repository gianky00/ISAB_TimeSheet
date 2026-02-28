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
from typing import Any, Optional, List, Dict

from PyQt6.QtCore import QThread, pyqtSignal

from src.core.logging import get_logger

try:
    import win32com.client
    import pythoncom
    _win32com_found = True
except ImportError:
    _win32com_found = False

logger = get_logger(__name__)


class GeneratoreWorker(QThread):
    """Esegue la generazione del file Excel in background."""
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, master_path: str, data: dict, dest_path: str):
        super().__init__()
        self.master_path = master_path
        self.data = data
        self.dest_path = dest_path

    def run(self):
        try:
            manager = PreventiviGeneratorManager(self.master_path)
            success, result = manager.generate_preventivo(self.data, self.dest_path)
            self.finished_signal.emit(success, result)
        except Exception as e:
            logger.error(f"Errore critico thread generatore: {e}")
            self.finished_signal.emit(False, f"Errore critico thread: {e}")


class MacroWorker(QThread):
    """Esegue una o più Macro VBA sul file generato in un thread separato."""
    finished_signal = pyqtSignal(bool, str)
    macro_started = pyqtSignal(str)     # Emesso quando inizia una macro
    macro_progress = pyqtSignal(str, bool) # Emesso quando finisce una singola macro (nome, successo)

    def __init__(self, file_path: str, macros: List[str]):
        super().__init__()
        self.file_path = file_path
        self.macros = macros

    def run(self):
        try:
            pythoncom.CoInitialize()
            import win32com.client
            
            excel_app = win32com.client.Dispatch("Excel.Application")
            excel_app.Visible = True 
            excel_app.DisplayAlerts = False
            
            wb = excel_app.Workbooks.Open(self.file_path, UpdateLinks=0)
            
            for macro in self.macros:
                self.macro_started.emit(macro)
                logger.info(f"Esecuzione macro: {macro}")
                try:
                    excel_app.Run(f"'{wb.Name}'!{macro}")
                    self.macro_progress.emit(macro, True)
                except Exception as me:
                    logger.error(f"Errore durante macro {macro}: {me}")
                    self.macro_progress.emit(macro, False)
                    # Fermiamo il loop se una macro critica fallisce
                    self.finished_signal.emit(False, f"Errore nell'esecuzione della macro '{macro}':\n{me}")
                    wb.Close(False)
                    return
            
            wb.Save()
            self.finished_signal.emit(True, "Operazioni macro completate.")
        except Exception as e:
            logger.error(f"Errore thread macro: {e}")
            self.finished_signal.emit(False, f"Errore macro: {e}")
        finally:
            pythoncom.CoUninitialize()


class PreventiviGeneratorManager:
    """Manager avanzato per la generazione di preventivi basati su template Excel Master."""

    def __init__(self, master_path: str = ""):
        self.master_path = master_path
        self.excel_app: Any = None
        self.wb: Any = None

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

    def read_existing_data(self, file_path: str) -> Dict[str, Any]:
        """Legge i dati da un file Excel esistente per popolare la UI."""
        if not _win32com_found or not os.path.exists(file_path):
            return {}

        data = {}
        try:
            pythoncom.CoInitialize()
            app = win32com.client.Dispatch("Excel.Application")
            app.Visible = False
            wb = app.Workbooks.Open(file_path, ReadOnly=True, UpdateLinks=0)
            
            try:
                sheet = wb.Sheets("inserimento dati")
                data["data"] = str(sheet.Range("A5").Value)
                data["tcl"] = str(sheet.Range("A7").Value)
                data["odc"] = str(sheet.Range("B5").Value or "")
                data["avviso"] = str(sheet.Range("C7").Value or "")
                data["ordine"] = str(sheet.Range("C5").Value or "")
                data["stato_attivita"] = str(sheet.Range("D11").Value)
                data["tipologia_preventivo"] = str(sheet.Range("D13").Value)
                data["tipologia_economia"] = str(sheet.Range("E13").Value)
                
                # Descrizione lavoro (prime 11 righe)
                desc = []
                for i in range(11):
                    val = sheet.Range(f"A{11+i}").Value
                    if val: desc.append(str(val))
                data["descrizione_lavoro"] = "\n".join(desc)
                data["descrizione_relazione"] = str(sheet.Range("A32").Value or "")
                
                # Progressivo da rif.VBA
                try:
                    vba_sheet = wb.Sheets("rif.VBA")
                    prog_val = str(vba_sheet.Range("A4").Value)
                    if "/" in prog_val:
                        data["progressivo"] = prog_val.split("/")[0]
                        data["anno_full"] = "20" + prog_val.split("/")[1]
                except:
                    pass
                    
            finally:
                wb.Close(False)
                app.Quit()
                pythoncom.CoUninitialize()
        except Exception as e:
            logger.error(f"Errore lettura dati esistenti: {e}")
        return data

    def _sanitize_excel_file(self, filepath: str):
        temp_dir = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                
            wb_xml_path = os.path.join(temp_dir, 'xl', 'workbook.xml')
            if os.path.exists(wb_xml_path):
                with open(wb_xml_path, 'r', encoding='utf-8') as f:
                    xml = f.read()
                
                xml = re.sub(r'<definedName[^>]*name="[^"]*Print_Area"[^>]*>.*?</definedName>', '', xml, flags=re.IGNORECASE|re.DOTALL)
                xml = re.sub(r'<definedName[^>]*name="[^"]*Print_Area"[^>]*/>', '', xml, flags=re.IGNORECASE)
                
                with open(wb_xml_path, 'w', encoding='utf-8') as f:
                    f.write(xml)
                    
            temp_zip = filepath + ".tmp"
            with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_out.write(file_path, arcname)
                        
            shutil.move(temp_zip, filepath)
        except Exception as e:
            logger.error(f"Errore sanitizzazione: {e}")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def generate_preventivo(self, data: dict[str, Any], output_dir: str) -> tuple[bool, str]:
        if not _win32com_found: return False, "pywin32 mancante."
        try:
            out_path = Path(output_dir)
            out_path.mkdir(parents=True, exist_ok=True)
            prog = data.get("progressivo", "000")
            year_short = data.get("anno_short", "26")
            filename = f"{prog}-{year_short}.xlsm"
            dest_file = out_path / filename

            shutil.copy2(self.master_path, dest_file)
            self._sanitize_excel_file(str(dest_file))
            
            success, msg = self._fill_excel_data(str(dest_file), data)
            return success, str(dest_file) if success else msg
        except Exception as e:
            return False, str(e)

    def _fill_excel_data(self, file_path: str, data: dict[str, Any]) -> tuple[bool, str]:
        try:
            pythoncom.CoInitialize()
            self.excel_app = win32com.client.Dispatch("Excel.Application")
            self.excel_app.Visible = False
            self.excel_app.DisplayAlerts = False
            self.wb = self.excel_app.Workbooks.Open(file_path, UpdateLinks=0)
            
            sheet = self.wb.Sheets("inserimento dati")
            sheet.Range("A5").Value = data.get("data", "")
            sheet.Range("A7").Value = data.get("tcl", "")
            sheet.Range("B5").Value = data.get("odc", "")
            sheet.Range("C7").Value = data.get("avviso", "")
            sheet.Range("C5").Value = data.get("ordine", "")
            sheet.Range("D11").Value = data.get("stato_attivita", "")
            sheet.Range("D13").Value = data.get("tipologia_preventivo", "")
            sheet.Range("E13").Value = data.get("tipologia_economia", "")

            lines = data.get("descrizione_lavoro", "").split("\n")[:11]
            for i, line in enumerate(lines):
                sheet.Range(f"A{11+i}").Value = line
            sheet.Range("A32").Value = data.get("descrizione_relazione", "")

            try:
                vba_ref = self.wb.Sheets("rif.VBA")
                vba_ref.Range("A4").Value = f"{data.get('progressivo', '000')}/{data.get('anno_short', '26')}"
                vba_ref.Range("A6").Value = data.get("data", "")
            except: pass

            self.wb.Save()
            return True, "OK"
        except Exception as e:
            return False, str(e)
        finally:
            if self.wb: self.wb.Close(False)
            if self.excel_app: self.excel_app.Quit()
            pythoncom.CoUninitialize()
