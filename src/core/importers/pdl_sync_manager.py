"""
SyncroJob - PDL Programming Sync Manager
Gestisce l'elaborazione dei file Excel di programmazione e il file Master aziendale.
"""

import logging
import os
import warnings
from typing import Any

import openpyxl

try:
    import win32com.client

    xlCalculationManual = -4135
    xlCalculationAutomatic = -4105
except ImportError:
    win32com = None  # type: ignore

logger = logging.getLogger(__name__)


class ProgrammingSyncManager:
    """Manager per la sincronizzazione dei dati di programmazione su Excel tramite Win32com."""

    FOGLI_PDL = ["A1", "A2", "A3", "CTE", "BLENDING", "TAS", "IGCC"]

    def __init__(self, master_path: str):
        self.master_path = master_path
        self.excel_app: Any = None
        self.wb_master: Any = None
        self._is_already_open = False
        self._original_calc_mode = None

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
        if not self.wb_master or not self.excel_app:
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
        """Aggrega le modifiche dal report scaricato al file Master."""
        if not self.wb_master or not self.excel_app:
            if not self._get_excel_workbook():
                return

        assert self.wb_master is not None
        assert self.excel_app is not None

        try:
            # 1. Preparazione Excel (Ottimizzazione)
            self._original_calc_mode = self.excel_app.Calculation
            self.excel_app.Calculation = xlCalculationManual
            self.excel_app.ScreenUpdating = False
            self.excel_app.EnableEvents = False

            # 2. Lettura Stato Master (Mappa PDL esistenti)
            mappa_pdl = {}
            for nome_foglio in self.FOGLI_PDL:
                sheet = self.wb_master.Sheets(nome_foglio)
                last_row = sheet.Cells(sheet.Rows.Count, 5).End(-4162).Row  # xlUp col E
                if last_row >= 4:
                    data = sheet.Range(sheet.Cells(4, 1), sheet.Cells(last_row, 13)).Value
                    if data:
                        if not isinstance(data, tuple):
                            data = ((data,),)
                        for i, row in enumerate(data):
                            pdl_val = row[4]  # Col E
                            if pdl_val:
                                mappa_pdl[str(pdl_val).strip()] = {
                                    "foglio": nome_foglio,
                                    "riga": i + 4,
                                    "stato": str(row[12] or "").strip().upper(),
                                }

            # 3. Elaborazione Report Scaricato (OpenPyXL per velocità)
            logger.info(f"Analisi report scaricato: {os.path.basename(downloaded_path)}")
            nuovi_pdl = {}
            modifiche_X = {}
            modifiche_stato = {}

            # Mapping colonne: H(8)->Lun, I(9)->Mar, J(10)->Mer, K(11)->Gio, L(12)->Ven
            mappa_giorni = {8: 3, 9: 5, 10: 7, 11: 9, 12: 11}

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                wb_in = openpyxl.load_workbook(downloaded_path, read_only=True, data_only=True)
                ws_in = wb_in.active
                assert ws_in is not None

                for row in ws_in.iter_rows(min_row=2, values_only=True):
                    if not row or not row[0]:
                        continue
                    pdl_str = str(row[0]).strip()

                    if pdl_str not in mappa_pdl:
                        # Nuovo PDL
                        nuovi_pdl[pdl_str] = [
                            row[0], row[1], row[14], row[16], row[18], row[19], row[20], row[13]
                        ]
                    else:
                        # PDL Esistente -> Controlla X
                        info = mappa_pdl[pdl_str]
                        for idx_excel, idx_report in mappa_giorni.items():
                            val_report = str(row[idx_report] or "").strip().lower()
                            if val_report == "si":
                                modifiche_X.setdefault(pdl_str, {})[idx_excel] = "X"

                        # Check Stato (Richiesto/Emesso)
                        col_O_val = str(row[14] or "").strip()
                        is_richiesto = col_O_val in ["Richiesto", "Richiesto (Ese ok)"]
                        if is_richiesto and info["stato"] != "RICHIESTO":
                            modifiche_stato[pdl_str] = "RICHIESTO"
                        elif not is_richiesto and info["stato"] == "RICHIESTO":
                            modifiche_stato[pdl_str] = "EMESSO"
                wb_in.close()

            # 4. Applicazione Reset e Modifiche sul Master
            logger.info("Esecuzione macro 'reset_programmazione'...")
            self.excel_app.Run(f"'{self.wb_master.Name}'!reset_programmazione")

            # Applicazione X
            for pdl, giorni in modifiche_X.items():
                info = mappa_pdl[pdl]
                sh = self.wb_master.Sheets(info["foglio"])
                for col, val in giorni.items():
                    sh.Cells(info["riga"], col).Value = val

            # Applicazione Stati
            for pdl, stato in modifiche_stato.items():
                info = mappa_pdl[pdl]
                self.wb_master.Sheets(info["foglio"]).Cells(info["riga"], 13).Value = stato

            # Scrittura Nuovi PDL
            if nuovi_pdl:
                sh_new = self.wb_master.Sheets("nuovi PdL rilevati")
                # Trova prima riga libera tra 3 e 23
                riga_libera = 24
                check_vals = sh_new.Range("A3:A23").Value
                if check_vals:
                    if not isinstance(check_vals, tuple):
                        check_vals = ((check_vals,),)
                    for i, r in enumerate(check_vals):
                        if not r[0]:
                            riga_libera = i + 3
                            break
                
                rows_data = list(nuovi_pdl.values())
                target = sh_new.Range(
                    sh_new.Cells(riga_libera, 1),
                    sh_new.Cells(riga_libera + len(rows_data) - 1, 8)
                )
                target.Value = rows_data
                logger.info(f"Inseriti {len(rows_data)} nuovi PDL nel foglio dedicato.")

            self.wb_master.Save()
            logger.info("✅ Sincronizzazione Master Excel completata.")

        except Exception as e:
            logger.error(f"❌ Errore durante l'elaborazione Excel: {e}", exc_info=True)
        finally:
            self._restore_settings()

    def _restore_settings(self):
        """Ripristina le impostazioni originali di Excel."""
        if self.excel_app:
            self.excel_app.ScreenUpdating = True
            self.excel_app.EnableEvents = True
            if self._original_calc_mode is not None:
                self.excel_app.Calculation = self._original_calc_mode

    def cleanup(self):
        """Chiude Excel se aperto dal manager."""
        if self.excel_app:
            if not self._is_already_open:
                if self.wb_master:
                    self.wb_master.Close(SaveChanges=True)
                self.excel_app.Quit()
            self.excel_app = None
