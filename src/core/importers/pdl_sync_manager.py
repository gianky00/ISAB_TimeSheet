"""
SyncroJob - PDL Programming Sync Manager
Gestisce l'elaborazione dei file Excel di programmazione e il file Master aziendale.
"""

import os
import warnings
from typing import Any, ClassVar

import openpyxl

from src.core.logging import get_logger

try:
    import win32com.client

    xlCalculationManual = -4135  # noqa: N816
    xlCalculationAutomatic = -4105  # noqa: N816
    _win32com_found = True
except ImportError:
    _win32com_found = False

logger = get_logger(__name__)


class ProgrammingSyncManager:
    """Manager per la sincronizzazione dei dati di programmazione su Excel tramite Win32com."""

    FOGLI_PDL: ClassVar[list[str]] = ["A1", "A2", "A3", "CTE", "BLENDING", "TAS", "IGCC"]

    def __init__(self, master_path: str) -> None:
        self.master_path = master_path
        self.excel_app: Any = None
        self.wb_master: Any = None
        self._is_already_open = False
        self._original_calc_mode: Any = None

    def _get_excel_workbook(self) -> bool:
        """Tenta di agganciarsi a Excel o ne apre una nuova istanza."""
        if not _win32com_found:
            return False

        file_name = os.path.basename(self.master_path)
        try:
            self.excel_app = win32com.client.GetActiveObject("Excel.Application")  # type: ignore
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
            return True  # noqa: TRY300
        except Exception as e:
            logger.error(f"Errore apertura Master Excel: {e}")  # noqa: TRY400
            return False

    def run_sync_macros(self) -> None:
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

    def process_downloaded_report(self, downloaded_path: str) -> None:
        """Aggrega le modifiche dal report scaricato al file Master."""
        if (not self.wb_master or not self.excel_app) and not self._get_excel_workbook():
            return

        if not self.wb_master or not self.excel_app:
            logger.error("Master Excel o App non inizializzati.")
            return

        try:
            self._prepare_excel_state(True)

            # 1. Mappatura stato Master
            mappa_pdl = self._map_master_pdls()

            # 2. Analisi report scaricato
            nuovi_pdl, modif_x, modif_stato = self._analyze_downloaded_file(downloaded_path, mappa_pdl)

            # 3. Applicazione modifiche
            self._apply_modifications_to_master(mappa_pdl, modif_x, modif_stato)

            # 4. Inserimento nuovi PDL
            if nuovi_pdl:
                self._insert_new_pdls(nuovi_pdl)

            self.wb_master.Save()
            logger.info("✅ Sincronizzazione Master Excel completata.")

        except Exception as e:
            logger.error(f"❌ Errore durante l'elaborazione Excel: {e}", exc_info=True)
        finally:
            self._prepare_excel_state(False)

    def _prepare_excel_state(self, optimize: bool) -> None:
        """Imposta o ripristina lo stato di ottimizzazione di Excel."""
        if not self.excel_app:
            return

        if optimize:
            self._original_calc_mode = self.excel_app.Calculation
            self.excel_app.Calculation = xlCalculationManual
            self.excel_app.ScreenUpdating = False
            self.excel_app.EnableEvents = False
        else:
            self.excel_app.ScreenUpdating = True
            self.excel_app.EnableEvents = True
            if self._original_calc_mode is not None:
                self.excel_app.Calculation = self._original_calc_mode

    def _map_master_pdls(self) -> dict[str, dict[str, Any]]:
        """Crea una mappa dei PDL esistenti nel file Master."""
        mappa_pdl = {}
        for nome_foglio in self.FOGLI_PDL:
            sheet = self.wb_master.Sheets(nome_foglio)
            last_row = sheet.Cells(sheet.Rows.Count, 5).End(-4162).Row  # xlUp col E
            if last_row < 4:  # noqa: PLR2004
                continue

            data = sheet.Range(sheet.Cells(4, 1), sheet.Cells(last_row, 13)).Value
            if not data:
                continue

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
        return mappa_pdl

    def _analyze_downloaded_file(
        self, path: str, mappa_pdl: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        """Analizza il file scaricato e identifica differenze e nuovi record."""
        logger.info(f"Analisi report scaricato: {os.path.basename(path)}")
        nuovi_pdl: dict[str, Any] = {}
        modif_x: dict[str, dict[int, str]] = {}
        modif_stato: dict[str, Any] = {}
        mappa_giorni = {8: 3, 9: 5, 10: 7, 11: 9, 12: 11}

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            wb_in = openpyxl.load_workbook(path, read_only=True, data_only=True)
            ws_in = wb_in.active
            if ws_in is None:
                return {}, {}, {}

            for row in ws_in.iter_rows(min_row=2, values_only=True):
                if not row or not row[0]:
                    continue
                pdl_str = str(row[0]).strip()

                if pdl_str not in mappa_pdl:
                    nuovi_pdl[pdl_str] = [
                        row[0],
                        row[1],
                        row[14],
                        row[16],
                        row[18],
                        row[19],
                        row[20],
                        row[13],
                    ]
                else:
                    info = mappa_pdl[pdl_str]
                    # Check X giorni
                    for idx_excel, idx_report in mappa_giorni.items():
                        if str(row[idx_report] or "").strip().lower() == "si":
                            modif_x.setdefault(pdl_str, {})[idx_excel] = "X"
                    # Check Stato
                    is_richiesto = str(row[14] or "").strip() in ("Richiesto", "Richiesto (Ese ok)")
                    if is_richiesto and info["stato"] != "RICHIESTO":
                        modif_stato[pdl_str] = "RICHIESTO"
                    elif not is_richiesto and info["stato"] == "RICHIESTO":
                        modif_stato[pdl_str] = "EMESSO"
            wb_in.close()
        return nuovi_pdl, modif_x, modif_stato

    def _apply_modifications_to_master(
        self, mappa_pdl: dict[str, Any], modif_x: dict[str, Any], modif_stato: dict[str, Any]
    ) -> None:
        """Applica le X dei giorni e i cambi di stato sul file Master."""
        logger.info("Esecuzione macro 'reset_programmazionè...")
        self.excel_app.Run(f"'{self.wb_master.Name}'!reset_programmazione")

        # Applicazione X
        for pdl, giorni in modif_x.items():
            info = mappa_pdl[pdl]
            sh = self.wb_master.Sheets(info["foglio"])
            for col, val in giorni.items():
                sh.Cells(info["riga"], col).Value = val

        # Applicazione Stati
        for pdl, stato in modif_stato.items():
            info = mappa_pdl[pdl]
            self.wb_master.Sheets(info["foglio"]).Cells(info["riga"], 13).Value = stato

    def _insert_new_pdls(self, nuovi_pdl: dict[str, Any]) -> None:
        """Inserisce i nuovi PDL nel foglio dedicato."""
        sh_new = self.wb_master.Sheets("nuovi PdL rilevati")
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
        target = sh_new.Range(sh_new.Cells(riga_libera, 1), sh_new.Cells(riga_libera + len(rows_data) - 1, 8))
        target.Value = rows_data
        logger.info(f"Inseriti {len(rows_data)} nuovi PDL nel foglio dedicato.")

    def cleanup(self) -> None:
        """Chiude Excel se aperto dal manager."""
        if self.excel_app:
            if not self._is_already_open:
                if self.wb_master:
                    self.wb_master.Close(SaveChanges=True)
                self.excel_app.Quit()
            self.excel_app = None
