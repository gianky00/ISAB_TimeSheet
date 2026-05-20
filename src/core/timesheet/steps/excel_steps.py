import time
from contextlib import suppress
from typing import Any

import openpyxl
from openpyxl.utils import column_index_from_string

from src.core.processing.base import ProcessingStep


class LoadWorkbookStep(ProcessingStep):
    def execute(self, context: dict[str, Any]) -> None:
        file_path = context["file_path"]
        wb = openpyxl.load_workbook(file_path)
        if "Timesheet" not in wb.sheetnames:
            raise ValueError("Foglio 'Timesheet' non trovato.")
        context["wb"] = wb
        context["ws"] = wb["Timesheet"]


class TransformSheetStep(ProcessingStep):
    def execute(self, context: dict[str, Any]) -> None:
        ws = context["ws"]

        # Metadata extraction
        odc = str(ws["A2"].value).strip() if ws["A2"].value else ""
        if not odc:
            raise ValueError("Valore ODC mancante.")
        context["odc"] = odc

        # Logica di trasformazione (da vecchio processor)
        headers = {
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
        for cell_coord, val in headers.items():
            ws[cell_coord].value = val

        cols = ["AC", "Z", "X", "L", "I", "H", "G", "F", "E", "D", "A"]
        indices = sorted([column_index_from_string(c) for c in cols], reverse=True)
        for idx in indices:
            ws.delete_cols(idx)

            ws.delete_cols(idx)


class SaveWorkbookStep(ProcessingStep):
    def execute(self, context: dict[str, Any]) -> None:
        wb = context["wb"]
        dest_dir = context["dest_dir"]
        odc = context["odc"]

        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / f"{odc}_TS.xlsx"

        if dest_path.exists():
            dest_path = dest_dir / f"{odc}_TS_{time.strftime('%Y%m%d-%H%M%S')}.xlsx"

        wb.save(dest_path)
        context["dest_path"] = dest_path
        wb.close()


class CleanupStep(ProcessingStep):
    def execute(self, context: dict[str, Any]) -> None:
        src = context["file_path"]
        dest = context["dest_path"]
        with suppress(Exception):
            if src.resolve() != dest.resolve():
                src.unlink()
