import io
import re
import warnings
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Lazy import placeholder
_pd = None

# Tentativo di importare msoffcrypto
try:
    import msoffcrypto
except ImportError:
    msoffcrypto = None

# Tentativo di importare openpyxl
try:
    import openpyxl

    openpyxl_mod: Any = openpyxl
    HAS_OPENPYXL = True
except ImportError:
    openpyxl_mod = None
    HAS_OPENPYXL = False


class BaseImporter:
    """Classe base per tutti gli importer Excel."""

    @staticmethod
    def _get_pd() -> Any:
        """Lazy load di pandas"""
        global _pd  # noqa: PLW0603
        if _pd is None:
            import pandas as _pd  # noqa: PLC0415
        return _pd

    @staticmethod
    def _decrypt_if_encrypted(file_path: Path) -> tuple[Any, bool]:
        """Tenta di decifrare un file Excel se protetto da password."""
        if msoffcrypto:
            with suppress(Exception):
                from src.core import config_manager  # noqa: PLC0415
                from src.core.constants import Business  # noqa: PLC0415

                config = config_manager.load_config()
                # Recupera password da config, default centralizzato
                pwd = config.get("excel_decryption_password", Business.DEFAULT_EXCEL_PASSWORD)

                with Path(file_path).open("rb") as f:
                    office_file = msoffcrypto.OfficeFile(f)
                    office_file.load_key(password=pwd)
                    temp_decrypted = io.BytesIO()
                    office_file.decrypt(temp_decrypted)
                    temp_decrypted.seek(0)
                    return temp_decrypted, True
        return file_path, False

    @classmethod
    def _get_excel_file(cls, file_obj: Any) -> Any:
        """Tenta di aprire il file Excel con motore ottimizzato (calamine > default > openpyxl)."""
        pd = cls._get_pd()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # 1. Tentativo con Calamine (Rust-based, ultra veloce)
            with suppress(ImportError, ValueError, Exception):
                return pd.ExcelFile(file_obj, engine="calamine")

            # 2. Tentativo Standard (Pandas auto-detect)
            with suppress(Exception):
                return pd.ExcelFile(file_obj)

            # 3. Fallback esplicito OpenPyXL
            return pd.ExcelFile(file_obj, engine="openpyxl")

    @classmethod
    def _identify_sheet_year(cls, sheet_name: str) -> int | None:
        """Estrae l'anno dal nome del foglio o usa l'anno corrente per nomi specifici."""
        match = re.search(r"(\d{4})", sheet_name)
        if match:
            year = int(match.group(1))
            return year if 2000 <= year <= 2100 else None  # noqa: PLR2004

        if sheet_name.lower() in ("dati", "preventivi", "riepilogo"):
            return datetime.now(UTC).year
        return None
