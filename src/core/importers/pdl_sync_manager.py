"""
SyncroJob - PDL Programming Sync Manager
Gestisce l'elaborazione dei file Excel di programmazione e il file Master aziendale.
"""

import logging
import os
from typing import Any

try:
    import win32com.client

    xlCalculationManual = -4135
    xlCalculationAutomatic = -4105
except ImportError:
    win32com = None  # type: ignore

logger = logging.getLogger(__name__)


class ProgrammingSyncManager:
    """Manager per la sincronizzazione dei dati di programmazione su Excel tramite Win32com."""

    def __init__(self, master_path: str):
        self.master_path = master_path
        self.excel_app: Any = None
        self.wb_master: Any = None
        self._is_already_open = False

    def _get_excel_workbook(self) -> bool:
        """Tenta di agganciarsi a Excel o ne apre una nuova istanza."""
        if not win32com:
            return False

        file_name = os.path.basename(self.master_path)
        try:
            self.excel_app = win32com.client.GetActiveObject("Excel.Application")
            for wb in self.excel_app.Workbooks:
                if wb.Name.lower() == file_name.lower():
                    self.wb_master = wb
                    self._is_already_open = True
                    return True
        except Exception:
            logger.debug("Nessuna istanza Excel attiva trovata.")

        try:
            self.excel_app = win32com.client.DispatchEx("Excel.Application")
            self.excel_app.Visible = False
            self.excel_app.DisplayAlerts = False
            self.wb_master = self.excel_app.Workbooks.Open(self.master_path, UpdateLinks=0)
            return True
        except Exception as e:
            logger.error(f"Errore apertura Master Excel: {e}")
            return False

    def run_sync_macros(self):
        """Esegue le macro di pulizia e formattazione nel file master."""
        if not self.wb_master:
            return

        name = self.wb_master.Name
        macros: list[str] = ["PulisciNomiDefiniti", "RimuoviTuttiIFiltri", "OrdinaEFormattaTabellaCorrente"]

        for m in macros:
            try:
                self.excel_app.Run(f"'{name}'!{m}")
                logger.info(f"✅ Macro '{m}' eseguita.")
            except Exception as e:
                logger.warning(f"⚠️ Impossibile eseguire macro '{m}': {e}")

    def process_downloaded_report(self, downloaded_path: str):
        """Implementa la logica di aggregazione dal report scaricato al master."""
        # Nota: Qui andrebbe la logica complessa di iterazione righe
        # Per ora lasciamo lo scheletro pronto per essere popolato con la logica di 'aggrega_e_applica_modifiche'

    def cleanup(self):
        """Chiude Excel se aperto dal manager."""
        if self.excel_app:
            if not self._is_already_open:
                if self.wb_master:
                    self.wb_master.Close(SaveChanges=True)
                self.excel_app.Quit()
            self.excel_app = None
