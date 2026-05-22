"""SyncroJob - Preventivi Generator Manager.

Gestisce la generazione di preventivi Excel a partire da un file Master con macro.
Implementa una tecnica avanzata di "Sanitizzazione XML" per eliminare i bug
dei Nomi Definiti (Print_Area) prima di lanciare l'automazione Win32COM.
"""

import os
import re
import shutil
import tempfile
import zipfile
from contextlib import suppress
from pathlib import Path
from typing import Any

from PySide6.QtCore import QThread, Signal

from src.core.logging import get_logger

try:
    import pythoncom
    import win32com.client

    _win32com_found = True
except ImportError:
    _win32com_found = False

logger = get_logger(__name__)


class GeneratoreWorker(QThread):
    """Esegue la generazione del file Excel in background."""

    finished_signal = Signal(bool, str)

    def __init__(self, master_path: str, data: dict[str, Any], dest_path: str) -> None:
        """Inizializza il worker per la generazione del preventivo.

        Args:
          master_path: Percorso del file Excel master template.
          data: Dizionario contenente i dati da inserire nel preventivo.
          dest_path: Percorso di destinazione per il file generato.
        """
        super().__init__()
        self.master_path = master_path
        self.data = data
        self.dest_path = dest_path

    def run(self) -> None:
        """Esegue la logica di generazione nel thread dedicato."""
        try:
            manager = PreventiviGeneratorManager(self.master_path)
            success, result = manager.generate_preventivo(self.data, self.dest_path)
            self.finished_signal.emit(success, result)
        except Exception as e:
            logger.exception("Errore critico thread generatore")
            self.finished_signal.emit(False, f"Errore critico thread: {e}")


class MacroWorker(QThread):
    """Esegue una o più Macro VBA sul file generato in un thread separato."""

    finished_signal = Signal(bool, str)
    macro_started = Signal(str)  # Emesso quando inizia una macro
    macro_progress = Signal(str, bool)  # Emesso quando finisce una singola macro (nome, successo)

    def __init__(self, file_path: str, macros: list[str]) -> None:
        """Inizializza il worker per l'esecuzione delle macro.

        Args:
          file_path: Percorso del file Excel su cui eseguire le macro.
          macros: Lista dei nomi delle macro da lanciare.
        """
        super().__init__()
        self.file_path = file_path
        self.macros = macros

    def run(self) -> None:
        """Esegue le macro VBA sequenzialmente tramite Win32COM."""
        try:
            pythoncom.CoInitialize()

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
                    logger.exception(f"Errore durante macro {macro}", exc=me)
                    self.macro_progress.emit(macro, False)
                    # Fermiamo il loop se una macro critica fallisce
                    self.finished_signal.emit(False, f"Errore nell'esecuzione della macro '{macro}':\n{me}")
                    wb.Close(False)
                    return

            wb.Save()
            self.finished_signal.emit(True, "Operazioni macro completate.")
        except Exception as e:
            logger.exception("Errore thread macro")
            self.finished_signal.emit(False, f"Errore macro: {e}")
        finally:
            pythoncom.CoUninitialize()


class PreventiviGeneratorManager:
    """Manager avanzato per la generazione di preventivi basati su template Excel Master."""

    def __init__(self, master_path: str = "") -> None:
        """Inizializza il manager dei preventivi.

        Args:
          master_path: Percorso assoluto del file Master XLSM.
        """
        self.master_path = master_path
        self.excel_app: Any = None
        self.wb: Any = None

    def get_next_progressive(self, directory: str) -> str:
        """Scansiona una cartella per determinare il prossimo numero progressivo disponibile.

        Args:
          directory: Cartella contenente i preventivi esistenti.

        Returns:
          str: Il prossimo progressivo formattato a 3 cifre (es. '005').
        """
        if not Path(directory).exists():
            return "001"

        max_num = 0
        pattern = re.compile(r"(\d{3})[-/]\d{2}")

        try:
            for f in os.listdir(directory):
                match = pattern.search(f)
                if match:
                    num = int(match.group(1))
                    max_num = max(max_num, num)
        except Exception as e:
            logger.warning(f"Errore calcolo progressivo: {e}")
            return "001"
        else:
            return f"{max_num + 1:03d}"

    def read_existing_data(self, file_path: str) -> dict[str, Any]:
        """Legge i dati da un file Excel esistente per popolare la UI."""
        if not _win32com_found or not Path(file_path).exists():
            return {}

        data: dict[str, Any] = {}
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
                    val = sheet.Range(f"A{11 + i}").Value
                    if val:
                        desc.append(str(val))
                data["descrizione_lavoro"] = "\n".join(desc)
                data["descrizione_relazione"] = str(sheet.Range("A32").Value or "")

                # Progressivo da rif.VBA
                with suppress(Exception):
                    vba_sheet = wb.Sheets("rif.VBA")
                    prog_val = str(vba_sheet.Range("A4").Value)
                    if "/" in prog_val:
                        data["progressivo"] = prog_val.split("/")[0]
                        data["anno_full"] = "20" + prog_val.split("/")[1]

            finally:
                wb.Close(False)
                app.Quit()
                pythoncom.CoUninitialize()
        except Exception:
            logger.exception("Errore lettura dati esistenti")
        return data

    def _sanitize_excel_file(self, filepath: str) -> None:
        """Rimuove i riferimenti corrotti a Print_Area all'interno dell'XML di Excel.

        Risolve il bug 'Impossibile trovare il filè durante l'esecuzione di macro.
        """
        temp_dir = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(filepath, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            wb_xml_path = Path(temp_dir) / "xl" / "workbook.xml"
            if wb_xml_path.exists():
                xml = wb_xml_path.read_text(encoding="utf-8")

                xml = re.sub(
                    r'<definedName[^>]*name="[^"]*Print_Area"[^>]*>.*?</definedName>',
                    "",
                    xml,
                    flags=re.IGNORECASE | re.DOTALL,
                )
                xml = re.sub(r'<definedName[^>]*name="[^"]*Print_Area"[^>]*/>', "", xml, flags=re.IGNORECASE)

                wb_xml_path.write_text(xml, encoding="utf-8")

            temp_zip = filepath + ".tmp"
            with zipfile.ZipFile(temp_zip, "w", zipfile.ZIP_DEFLATED) as zip_out:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_out.write(file_path, arcname)

            shutil.move(temp_zip, filepath)
        except Exception:
            logger.exception("Errore sanitizzazione")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def generate_preventivo(self, data: dict[str, Any], output_dir: str) -> tuple[bool, str]:
        """Genera un nuovo preventivo popolando il template e sanitizzando l'output.

        Args:
          data: Dati inseriti dall'utente nella UI.
          output_dir: Cartella dove salvare il preventivo.

        Returns:
          tuple: (successo, percorso del file generato o messaggio di errore).
        """
        if not _win32com_found:
            return False, "pywin32 mancante."
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
        except Exception as e:
            return False, str(e)
        else:
            return success, str(dest_file) if success else msg

    def _fill_excel_data(self, file_path: str, data: dict[str, Any]) -> tuple[bool, str]:
        """Inietta i dati nelle celle specifiche del foglio 'inserimento datì."""
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
                sheet.Range(f"A{11 + i}").Value = line
            sheet.Range("A32").Value = data.get("descrizione_relazione", "")

            with suppress(Exception):
                vba_ref = self.wb.Sheets("rif.VBA")
                vba_ref.Range("A4").Value = f"{data.get('progressivo', '000')}/{data.get('anno_short', '26')}"
                vba_ref.Range("A6").Value = data.get("data", "")

            self.wb.Save()
        except Exception as e:
            return False, str(e)
        else:
            return True, "OK"
        finally:
            if self.wb:
                self.wb.Close(False)
            if self.excel_app:
                self.excel_app.Quit()
            pythoncom.CoUninitialize()
