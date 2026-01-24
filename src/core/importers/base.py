import io
import re
import warnings
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Tuple, Optional

# Lazy import placeholder
_pd = None

# Tentativo di importare msoffcrypto
try:
    import msoffcrypto  # type: ignore
except ImportError:
    msoffcrypto = None

# Tentativo di importare openpyxl
try:
    import openpyxl  # type: ignore
    HAS_OPENPYXL = True
except ImportError:
    openpyxl = None  # type: ignore
    HAS_OPENPYXL = False


class BaseImporter:
    """Classe base per tutti gli importer Excel."""

    @staticmethod
    def _get_pd():
        """Lazy load di pandas"""
        global _pd
        if _pd is None:
            import pandas as _pd
        return _pd

    @staticmethod
    def _decrypt_if_encrypted(file_path: Path) -> Tuple[Any, bool]:
        """Tenta di decifrare un file Excel se protetto da password."""
        if msoffcrypto:
            try:
                from src.core import config_manager

                config = config_manager.load_config()
                # Recupera password da config, default "coemi"
                pwd = config.get("excel_decryption_password", "coemi")

                with Path(file_path).open("rb") as f:
                    office_file = msoffcrypto.OfficeFile(f)
                    office_file.load_key(password=pwd)
                    temp_decrypted = io.BytesIO()
                    office_file.decrypt(temp_decrypted)
                    temp_decrypted.seek(0)
                    return temp_decrypted, True
            except Exception:
                # Non cifrato o errore msoffcrypto, procediamo col file originale
                pass
        return file_path, False

    @classmethod
    def _get_excel_file(cls, file_obj) -> Any:
        """Tenta di aprire il file Excel con motore ottimizzato (calamine > default > openpyxl)."""
        pd = cls._get_pd()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # 1. Tentativo con Calamine (Rust-based, ultra veloce)
            try:
                return pd.ExcelFile(file_obj, engine="calamine")
            except (ImportError, ValueError, Exception):
                pass

            # 2. Tentativo Standard (Pandas auto-detect)
            try:
                return pd.ExcelFile(file_obj)
            except Exception:
                pass

            # 3. Fallback esplicito OpenPyXL
            return pd.ExcelFile(file_obj, engine="openpyxl")

    @classmethod
    def _identify_sheet_year(cls, sheet_name: str) -> Optional[int]:
        """Estrae l'anno dal nome del foglio o usa l'anno corrente per nomi specifici."""
        match = re.search(r"(\d{4})", sheet_name)
        if match:
            year = int(match.group(1))
            return year if 2000 <= year <= 2100 else None

        if sheet_name.lower() in ("dati", "preventivi", "riepilogo"):
            return datetime.now().year
        return None
