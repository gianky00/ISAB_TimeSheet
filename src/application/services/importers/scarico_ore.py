"""Modulo Scarico Ore."""

import io
import re
import zipfile
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path
from typing import Any, ClassVar

try:
    import msoffcrypto
except ImportError:
    msoffcrypto = None

try:
    import openpyxl

    openpyxl_mod: Any = openpyxl
    HAS_OPENPYXL = True
except ImportError:
    openpyxl_mod = None
    HAS_OPENPYXL = False

from src.application.services.constants import Business
from src.application.services.importers.base import BaseImporter
from src.application.services.logging import get_logger
from src.application.services.processing.base import Pipeline
from src.application.services.processing.scarico_ore.steps import (
    LoadScaricoOreStep,
    ProcessScaricoOreRowsStep,
    SyncScaricoOreStep,
)

logger = get_logger(__name__)


class ScaricoOreImporter(BaseImporter):
    """Importer per lo Scarico Ore Cantiere (con OpenPyXL per stili)."""

    SCARICO_ORE_COLS: ClassVar[list[str]] = [
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
        """Esegue una scansione rapida del file Excel per stimare il numero di righe totali.

        Legge direttamente la struttura XML del file .xlsx per massima velocità.

        Args:
            file_path: Percorso del file Excel.

        Returns:
            int: Numero stimato di righe.
        """
        path = Path(file_path)
        if not path.exists():
            return 0

        def _scan_zip(zip_file_obj: Any) -> int:
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
                                    cnt = max(cnt, r)
                return cnt  # noqa: TRY300
            except Exception:
                return 0

        try:
            res = _scan_zip(path)
            if res > 0:
                return res
        except (zipfile.BadZipFile, Exception) as e:
            logger.debug(f"Scan excel rows error: {e}")

        if msoffcrypto:
            with suppress(Exception):
                decrypted = io.BytesIO()
                with path.open("rb") as f:
                    office_file = msoffcrypto.OfficeFile(f)
                    office_file.load_key(password=Business.DEFAULT_EXCEL_PASSWORD)  # nosec: B106
                    office_file.decrypt(decrypted)
                decrypted.seek(0)
                return _scan_zip(decrypted)

        return 0

    @classmethod
    def import_scarico_ore(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]]]:
        """Importa i dati dal file Excel dello Scarico Ore Cantiere tramite Pipeline.

        Args:
            file_path: Percorso del file da importare.
            progress_callback: Funzione opzionale per monitorare l'avanzamento.

        Returns:
            tuple: (successo, messaggio, lista di righe processate).
        """
        path = Path(file_path)
        if not path.exists():
            return False, f"File Scarico Ore non trovato: {file_path}", []

        if not HAS_OPENPYXL:
            return False, "Modulo 'openpyxl' mancante.", []

        try:
            pipeline = Pipeline()
            pipeline.add_step(LoadScaricoOreStep())
            pipeline.add_step(ProcessScaricoOreRowsStep())
            pipeline.add_step(SyncScaricoOreStep())

            context: dict[str, Any] = {
                "file_path": str(path),
                "progress_callback": progress_callback,
            }

            result = pipeline.run(context)

            if not result.get("success"):
                return False, result.get("message", "Errore pipeline."), []

            rows = result.get("rows", [])
            return True, result.get("message", f"Importate {len(rows)} righe."), rows

        except Exception as e:
            return False, f"Errore importazione Scarico Ore: {e}", []

    @classmethod
    def _process_all_scarico_rows(cls, ws: Any, progress_callback: Any) -> list[tuple[Any, ...]]:
        """Alias per retrocompatibilità con i test."""
        from typing import cast  # noqa: PLC0415

        from src.application.services.processing.scarico_ore.steps import (  # noqa: PLC0415
            ProcessScaricoOreRowsStep,
        )

        context = {"ws": ws, "progress_callback": progress_callback, "success": True}
        ProcessScaricoOreRowsStep().execute(context)
        return cast("list[tuple[Any, ...]]", context.get("rows", []))
