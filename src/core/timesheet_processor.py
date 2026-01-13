"""
SyncroJob - Timesheet Processing Logic (VBA Replacement)
Replica fedelmente la logica VBA "ProcessTimesheetFiles" per elaborazione, pulizia e rinomina.
"""

import time
from pathlib import Path

import openpyxl
from openpyxl.utils import column_index_from_string, get_column_letter

from src.utils.secure_logger import get_secure_logger

logger = get_secure_logger("TimesheetProcessor")


class TimesheetProcessor:
    """Classe per elaborare i file timesheet sostituendo la macro VBA."""

    @staticmethod
    def process_and_move(file_path: Path, dest_dir: Path) -> tuple[bool, str]:
        """
        Elabora il file Excel secondo la logica VBA e lo salva nella cartella di destinazione.

        Logica VBA replicata:
        1. Apre file e foglio 'Timesheet'.
        2. Legge ODC (A2).
        3. Conta POS univoci in colonna B (da B2 in giù).
        4. Genera nome file: {ODC}_TS.xlsx (se >1 POS) o {ODC}_{POS}_TS.xlsx.
        5. Rinomina Intestazioni (B1, C1, N1..W1).
        6. Pulisce Colonna B (numeri interi).
        7. Elimina colonne (AC, Z, X, L, I, H, G, F, E, D, A).
        8. Autofit colonne (stima).
        9. Salva in dest_dir gestendo conflitti.
        """
        if not file_path.exists():
            return False, f"File sorgente non trovato: {file_path}"

        if not dest_dir.exists():
            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                return False, f"Impossibile creare dest_dir: {e}"

        try:
            # --- 1. Apertura File ---
            # data_only=False per mantenere eventuali formule, anche se il VBA lavora sui valori.
            # L'importante è che openpyxl legga il file esistente.
            wb = openpyxl.load_workbook(file_path)

            if "Timesheet" not in wb.sheetnames:
                wb.close()
                return False, "Foglio 'Timesheet' non trovato."

            ws = wb["Timesheet"]

            # --- 2. Lettura ODC (A2) ---
            # VBA: valA2 = Trim(CStr(tsSheet.Range("A2").Value))
            val_a2 = str(ws["A2"].value).strip() if ws["A2"].value else ""
            if not val_a2:
                wb.close()
                return False, "Valore ODC (cella A2) mancante."

            # --- 3. Analisi POS (Colonna B) ---
            # Trova l'ultima riga
            last_row = ws.max_row
            pos_values = set()
            val_b2_cleaned = ""  # Per il nome file se POS unico

            # Raccogli valori per conteggio (saltando header riga 1)
            # VBA: Range("B2:B" & lastRow)
            for row in ws.iter_rows(min_row=2, max_row=last_row, min_col=2, max_col=2):
                cell = row[0]
                val = str(cell.value).strip() if cell.value is not None else ""
                if val:
                    pos_values.add(val)
                    # Logica pulizia specifica per B2 (usata nel nome file)
                    if cell.row == 2:
                        # VBA: If IsNumeric(rawValB2) ... CStr(CLng(rawValB2))
                        # Similiamo la conversione in intero per togliere zeri o decimali
                        if val.replace(".", "", 1).isdigit():
                            try:
                                val_b2_cleaned = str(int(float(val)))
                            except Exception:
                                val_b2_cleaned = val
                        else:
                            val_b2_cleaned = val

            # --- 4. Genera Nuovo Nome ---
            # VBA: If dict.Count > 1 Then ... Else ...
            if len(pos_values) > 1:
                new_base_name = f"{val_a2}_TS"
            else:
                # Se 0 POS (file vuoto?) usa comunque A2_TS o A2__TS
                # VBA usa valA2 & "_" & valB2 & "_TS"
                new_base_name = f"{val_a2}_{val_b2_cleaned}_TS"

            new_filename = f"{new_base_name}.xlsx"
            dest_path = dest_dir / new_filename

            # Gestione Conflitti Automatizzata
            if dest_path.exists():
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                new_filename = f"{new_base_name}_{timestamp}.xlsx"
                dest_path = dest_dir / new_filename

            # --- 5. Rinomina Intestazioni ---
            headers_map = {
                "B1": "POS",
                "C1": "Data",
                "N1": "Ing",
                "O1": "Usc",
                "P1": "Tot",
                "Q1": "Pre",
                "R1": "ORE_C",
                "S1": "ORE_M",
                "T1": "ORE_ST_NOT",
                "U1": "ORE_ST_DIU",
                "V1": "ORE_FEST_NOT",
                "W1": "ORE_FEST_DIU",
            }
            for cell_ref, val in headers_map.items():
                ws[cell_ref].value = val

            # --- 6. Pulizia Dati Colonna B ---
            # VBA: cell.Value = CLng(Trim(cell.Value)), NumberFormat = "0"
            for row in ws.iter_rows(min_row=2, max_row=last_row, min_col=2, max_col=2):
                cell = row[0]
                val = cell.value
                if val is not None:
                    s_val = str(val).strip()
                    # Check numerico lasco (es. "30.0" o "30")
                    if s_val.replace(".", "", 1).isdigit():
                        try:
                            num_val = int(float(s_val))
                            cell.value = num_val
                            cell.number_format = "0"
                        except Exception:
                            pass  # Lascia invariato se fallisce

            # --- 7. Elimina Colonne ---
            # VBA: AC, Z, X, L, I, H, G, F, E, D, A
            # Importante: eliminare in ordine decrescente di indice
            cols_to_delete_letters = [
                "AC",
                "Z",
                "X",
                "L",
                "I",
                "H",
                "G",
                "F",
                "E",
                "D",
                "A",
            ]
            cols_indices = [
                column_index_from_string(c) for c in cols_to_delete_letters
            ]
            cols_indices.sort(reverse=True)

            for col_idx in cols_indices:
                ws.delete_cols(col_idx)

            # --- 8. Autofit (Stima) ---
            for col in ws.columns:
                max_length = 0
                column = get_column_letter(col[0].column)
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2) * 1.2
                ws.column_dimensions[column].width = adjusted_width

            # --- 9. Salvataggio ---
            wb.save(dest_path)
            wb.close()

            # Pulizia sorgente
            try:
                if file_path.resolve() != dest_path.resolve():
                    file_path.unlink()
            except Exception:
                pass

            return True, f"Salvato in: {dest_path.name}"

        except Exception as e:
            logger.error(f"Errore elaborazione {file_path.name}: {e}")
            return False, str(e)