"""
SyncroJob - Base Sync Engine
Fornisce helper SQL protetti e metodi base per la sincronizzazione dati.
"""

import re
from typing import Any


class BaseSyncEngine:
    """Classe base con utility per operazioni SQL sicure e gestione tabelle temporanee."""

    @staticmethod
    def _validate_identifier(name: str) -> str:
        """Valida che un identificatore SQL sia sicuro."""
        if not re.match(r"^[a-zA-Z0-9_]+$", name):
            raise ValueError(f"Identificatore SQL non sicuro: {name}")  # noqa: TRY003
        return name

    @classmethod
    def _create_temp_table(cls, cursor: Any, table_name: str, columns: list[str]) -> str:
        """Crea una tabella temporanea e restituisce il suo nome sicuro."""
        safe_name = cls._validate_identifier(table_name)
        temp_name = f"temp_{safe_name}"
        cursor.execute(f"DROP TABLE IF EXISTS {temp_name}")  # nosec B608
        cols_def = ", ".join([f'"{cls._validate_identifier(c)}" TEXT' for c in columns])
        cursor.execute(f"CREATE TEMPORARY TABLE {temp_name} ({cols_def})")  # nosec B608
        return temp_name

    @staticmethod
    def _clean_value(x: Any) -> Any:
        """Pulisce il valore per l'inserimento nel DB."""
        if x is None:
            return ""
        if isinstance(x, (int, float)):
            return x
        return str(x).strip()
