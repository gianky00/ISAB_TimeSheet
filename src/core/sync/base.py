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

    @classmethod
    def _sync_partitioned_table(  # noqa: PLR0913
        cls,
        cursor: Any,
        table_name: str,
        columns: list[str],
        partition_col: str,
        partition_values: list[Any],
        new_data: list[tuple[Any, ...]],
    ) -> tuple[int, int]:
        """
        Esegue la sincronizzazione di una tabella partizionata.

        Args:
            cursor: Cursore del database.
            table_name: Nome della tabella reale.
            columns: Elenco delle colonne.
            partition_col: Colonna usata per il partizionamento (es. 'year').
            partition_values: Valori delle partizioni da aggiornare.
            new_data: Nuovi dati da inserire nella tabella temporanea.

        Returns:
            Tuple (aggiunti, rimossi).
        """
        safe_table = cls._validate_identifier(table_name)
        temp_table = cls._create_temp_table(cursor, safe_table, columns)

        if new_data:
            placeholders = ", ".join(["?"] * len(columns))
            # Pulisce i dati prima dell'inserimento
            cleaned_data = [tuple(cls._clean_value(x) for x in r) for r in new_data]
            cursor.executemany(f"INSERT INTO {temp_table} VALUES ({placeholders})", cleaned_data)

        total_added, total_removed = 0, 0
        safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])
        safe_cast_cols = ", ".join([f'CAST("{cls._validate_identifier(c)}" AS TEXT)' for c in columns])
        safe_part_col = cls._validate_identifier(partition_col)

        for val in partition_values:
            # 1. Calcolo Diff (Aggiunti)
            q_added = (
                f"SELECT COUNT(*) FROM ("
                f"SELECT {safe_cast_cols} FROM {temp_table} WHERE {safe_part_col} = ? "
                f"EXCEPT SELECT {safe_cast_cols} FROM {safe_table} WHERE {safe_part_col} = ?)"
            )
            cursor.execute(q_added, (val, val))
            total_added += cursor.fetchone()[0]

            # 2. Calcolo Diff (Rimossi)
            q_removed = (
                f"SELECT COUNT(*) FROM ("
                f"SELECT {safe_cast_cols} FROM {safe_table} WHERE {safe_part_col} = ? "
                f"EXCEPT SELECT {safe_cast_cols} FROM {temp_table} WHERE {safe_part_col} = ?)"
            )
            cursor.execute(q_removed, (val, val))
            total_removed += cursor.fetchone()[0]

            # 3. Sostituzione Atomica
            cursor.execute(f"DELETE FROM {safe_table} WHERE {safe_part_col} = ?", (val,))
            q_ins = f"INSERT INTO {safe_table} ({safe_cols}) SELECT {safe_cols} FROM {temp_table} WHERE {safe_part_col} = ?"
            cursor.execute(q_ins, (val,))

        return total_added, total_removed
