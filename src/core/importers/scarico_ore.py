import io
import json
import re
import warnings
import zipfile
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

try:
    import msoffcrypto  # type: ignore
except ImportError:
    msoffcrypto = None

try:
    import openpyxl  # type: ignore

    HAS_OPENPYXL = True
except ImportError:
    openpyxl = None  # type: ignore
    HAS_OPENPYXL = False

from src.core.importers.base import BaseImporter


class ScaricoOreImporter(BaseImporter):
    """Importer per lo Scarico Ore Cantiere (con OpenPyXL per stili)."""

    SCARICO_ORE_COLS = [
        "data",
        "pers1",
        "pers2",
        "odc",
        "pos",
        "dalle",
        "alle",
        "totale_ore",
        "descrizione",
        "finito",
        "commessa",
        "styles",
    ]

    @classmethod
    def scan_scarico_ore_rows(cls, file_path: str) -> int:
        path = Path(file_path)
        if not path.exists():
            return 0

        def _scan_zip(zip_file_obj):
            try:
                cnt = 0
                with zipfile.ZipFile(zip_file_obj, "r") as z:
                    for name in z.namelist():
                        if name.startswith("xl/worksheets/sheet"):
                            with z.open(name) as f:
                                head = f.read(32768).decode("utf-8", errors="ignore")
                                match = re.search(r'<dimension ref="[A-Z]+[0-9]+:[A-Z]+(\d+)"', head)
                                if match:
                                    r = int(match.group(1))
                                    if r > cnt:
                                        cnt = r
                return cnt
            except Exception:
                return 0

        try:
            res = _scan_zip(path)
            if res > 0:
                return res
        except (zipfile.BadZipFile, Exception):
            pass

        if msoffcrypto:
            try:
                decrypted = io.BytesIO()
                with open(path, "rb") as f:
                    office_file = msoffcrypto.OfficeFile(f)
                    office_file.load_key(password="coemi")
                    office_file.decrypt(decrypted)
                decrypted.seek(0)
                return _scan_zip(decrypted)
            except Exception:
                return 0

        return 0

    @classmethod
    def import_scarico_ore(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        path = Path(file_path)
        if not path.exists():
            return False, f"File Scarico Ore non trovato: {file_path}", []

        if not HAS_OPENPYXL:
            return False, "Modulo 'openpyxl' mancante.", []

        try:
            wb_data = cls._load_scarico_workbook(path)
            if "SCARICO ORE" not in wb_data.sheetnames:
                return False, "Foglio 'SCARICO ORE' non trovato.", []

            ws_data = wb_data["SCARICO ORE"]
            rows = cls._process_all_scarico_rows(ws_data, progress_callback)

            return True, f"Importate {len(rows)} righe da Scarico Ore.", rows

        except Exception as e:
            return False, f"Errore importazione Scarico Ore: {e}", []

    @classmethod
    def _load_scarico_workbook(cls, path: Path) -> Any:
        wb_file = io.BytesIO()
        is_encrypted = False

        if msoffcrypto:
            try:
                with open(path, "rb") as f:
                    office_file = msoffcrypto.OfficeFile(f)
                    office_file.load_key(password="coemi")
                    office_file.decrypt(wb_file)
                    is_encrypted = True
            except Exception:
                pass

        if not is_encrypted:
            with open(path, "rb") as f:
                wb_file.write(f.read())

        wb_file.seek(0)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
            return openpyxl.load_workbook(
                wb_file,
                data_only=True,
                read_only=True,
                keep_vba=False,
                keep_links=False,
            )

    @classmethod
    def _process_all_scarico_rows(
        cls,
        ws,
        progress_callback: Optional[Callable],
    ) -> List[Tuple]:
        start_row = 6
        col_keys = [
            "data",
            "pers1",
            "pers2",
            "odc",
            "pos",
            "dalle",
            "alle",
            "totale_ore",
            "descrizione",
            "finito",
            "commessa",
        ]
        total_rows = ws.max_row

        rows_to_insert: List[Tuple] = []
        rows_to_insert_append = rows_to_insert.append

        progress_interval = 5000
        for row_idx, row in enumerate(
            ws.iter_rows(min_row=start_row, min_col=2, max_col=12, values_only=False),
            start=start_row,
        ):
            if progress_callback and row_idx % progress_interval == 0:
                progress_callback(row_idx, total_rows)

            db_row = cls._process_scarico_ore_row(row, col_keys)
            if db_row:
                rows_to_insert_append(db_row)

        return rows_to_insert

    @classmethod
    def _extract_row_values(cls, row) -> Optional[List[str]]:
        (
            c_data,
            c_p1,
            c_p2,
            c_odc,
            c_pos,
            c_dalle,
            c_alle,
            c_tot,
            c_desc,
            c_fin,
            c_comm,
        ) = row[0:11]

        v_odc = c_odc.value
        v_pos = c_pos.value

        if v_odc is None and v_pos is None:
            return None

        def _fmt(val):
            if val is None:
                return ""
            s = str(val).strip()
            return s.replace("\n", " ") if s else ""

        vals = []
        v_data = c_data.value
        s_data = ""
        if v_data:
            if hasattr(v_data, "strftime"):
                s_data = v_data.strftime("%Y-%m-%d")
            else:
                s = str(v_data).strip()
                if " " in s:
                    s = s.split(" ")[0]
                s_data = s
        vals.append(s_data)

        vals.append(_fmt(c_p1.value))
        vals.append(_fmt(c_p2.value))

        s_odc = _fmt(v_odc)
        if s_odc == "0" or s_odc == "0.0":
            s_odc = ""
        vals.append(s_odc)

        s_pos = _fmt(v_pos)
        if s_pos == "0" or s_pos == "0.0":
            s_pos = ""
        vals.append(s_pos)

        vals.append(_fmt(c_dalle.value))
        vals.append(_fmt(c_alle.value))
        vals.append(_fmt(c_tot.value))
        vals.append(_fmt(c_desc.value))
        vals.append(_fmt(c_fin.value))

        v_comm = c_comm.value
        s_comm = _fmt(v_comm)
        if s_comm == "0" or s_comm == "0.0":
            s_comm = ""
        vals.append(s_comm)

        return vals

    @classmethod
    def _process_scarico_ore_row(cls, row, col_keys) -> Optional[Tuple]:
        vals = cls._extract_row_values(row)
        if not vals:
            return None

        if not cls._validate_scarico_row(vals):
            return None

        styles_json = cls._extract_row_styles(row, col_keys, vals)

        return (
            vals[0],
            vals[1],
            vals[2],
            vals[3],
            vals[4],
            vals[5],
            vals[6],
            vals[7],
            vals[8],
            vals[9],
            vals[10],
            styles_json,
        )

    @staticmethod
    def _validate_scarico_row(vals) -> bool:
        if not vals[3] or not vals[4] or not vals[7]:
            return False
        if not vals[1] and not vals[2]:
            return False
        return True

    @staticmethod
    def _extract_row_styles(row, col_keys, vals) -> str:
        row_styles: Dict[str, Dict[str, str]] = {}
        for i, key in enumerate(col_keys):
            if vals[i] == "":
                continue

            cell = row[i]
            try:
                font = cell.font
                if font and font.color and font.color.type == "rgb":
                    rgb = str(font.color.rgb)
                    hex_code = f"#{rgb[2:]}" if len(rgb) > 6 else f"#{rgb}"
                    if hex_code != "#000000":
                        row_styles.setdefault(key, {})["fg"] = hex_code
            except (AttributeError, TypeError):
                pass

            try:
                fill = cell.fill
                if fill and fill.patternType == "solid":
                    start_color = fill.start_color
                    if start_color and start_color.type == "rgb":
                        rgb = str(start_color.rgb)
                        hex_code = f"#{rgb[2:]}" if len(rgb) > 6 else f"#{rgb}"
                        if hex_code != "#000000" and hex_code != "#FFFFFF":
                            row_styles.setdefault(key, {})["bg"] = hex_code
            except (AttributeError, TypeError):
                pass

        return json.dumps(row_styles) if row_styles else ""
