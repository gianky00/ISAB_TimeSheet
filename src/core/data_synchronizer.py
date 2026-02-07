"""
SyncroJob - Data Synchronizer
Gestisce la sincronizzazione dei dati importati con il database.
"""

from pathlib import Path

from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter


class DataSynchronizer:
    """Gestore per la sincronizzazione dei dati con il database ottimizzato tramite SQL."""

    @staticmethod
    def _validate_identifier(name: str):
        """Valida che un identificatore SQL (tabella o colonna) sia sicuro."""
        import re

        if not re.match(r"^[a-zA-Z0-9_]+$", name):
            raise ValueError(f"Identificatore SQL non sicuro: {name}")
        return name

    @classmethod
    def _create_temp_table(cls, cursor, table_name: str, columns: list[str]):
        """Crea una tabella temporanea validata."""
        safe_name = cls._validate_identifier(table_name)
        cursor.execute(f"DROP TABLE IF EXISTS temp_{safe_name}")  # nosec B608
        cols_def = ", ".join([f'"{cls._validate_identifier(c)}" TEXT' for c in columns])
        cursor.execute(f"CREATE TEMPORARY TABLE temp_{safe_name} ({cols_def})")  # nosec B608

    @classmethod
    def _get_diff_count(
        cls, cursor, table_name: str, columns: list[str], year: int | None = None
    ) -> tuple[int, int]:
        """Calcola record aggiunti e rimossi tramite EXCEPT SQL."""
        safe_table = cls._validate_identifier(table_name)
        safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])
        safe_cast_cols = ", ".join([f'CAST("{cls._validate_identifier(c)}" AS TEXT)' for c in columns])

        where_clause = "WHERE year = ?" if year is not None else ""
        params = (year,) if year is not None else ()

        # Aggiunti
        q_added = f"SELECT COUNT(*) FROM (SELECT {safe_cols} FROM temp_{safe_table} {where_clause} EXCEPT SELECT {safe_cast_cols} FROM {safe_table} {where_clause})"  # nosec B608
        cursor.execute(q_added, params + params)
        added = cursor.fetchone()[0]

        # Rimossi
        q_removed = f"SELECT COUNT(*) FROM (SELECT {safe_cast_cols} FROM {safe_table} {where_clause} EXCEPT SELECT {safe_cols} FROM temp_{safe_table} {where_clause})"  # nosec B608
        cursor.execute(q_removed, params + params)
        removed = cursor.fetchone()[0]

        return added, removed

    @classmethod
    def _replace_data(cls, cursor, table_name: str, columns: list[str], year: int | None = None):
        """Esegue la sostituzione atomica dei dati."""
        safe_table = cls._validate_identifier(table_name)
        safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])

        if year is not None:
            cursor.execute(f"DELETE FROM {safe_table} WHERE year = ?", (year,))  # nosec B608
            q_ins = f"INSERT INTO {safe_table} ({safe_cols}) SELECT {safe_cols} FROM temp_{safe_table} WHERE year = ?"  # nosec B608
            cursor.execute(q_ins, (year,))
        else:
            cursor.execute(f"DELETE FROM {safe_table}")  # nosec B608
            q_ins = f"INSERT INTO {safe_table} ({safe_cols}) SELECT {safe_cols} FROM temp_{safe_table}"  # nosec B608
            cursor.execute(q_ins)

    @classmethod
    def sync_contabilita_dati(
        cls, db_path: Path, imported_data: list[tuple], imported_years: list[int]
    ) -> tuple[int, int]:
        if not imported_data:
            return 0, 0

        target_columns = [
            "year",
            *[cls._validate_identifier(c) for c in ExcelImporter.COLUMNS_MAPPING.values()],
        ]
        total_added, total_removed = 0, 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            cls._create_temp_table(cursor, "contabilita", target_columns)

            placeholders = ", ".join(["?"] * len(target_columns))
            data = [tuple(str(x).strip() if x is not None else "" for x in r) for r in imported_data]
            cursor.executemany(
                f"INSERT INTO temp_contabilita VALUES ({placeholders})",  # nosec B608
                data,
            )

            for year in imported_years:
                added, removed = cls._get_diff_count(cursor, "contabilita", target_columns, year)
                total_added += added
                total_removed += removed
                cls._replace_data(cursor, "contabilita", target_columns, year)
            conn.commit()

        return total_added, total_removed

    @classmethod
    def sync_giornaliere(
        cls, db_path: Path, all_new_rows: list[tuple], years_to_clear: list[int]
    ) -> tuple[int, int]:
        if not all_new_rows and not years_to_clear:
            return 0, 0

        target_cols = [
            "year",
            "data",
            "personale",
            "descrizione",
            "tcl",
            "odc",
            "pdl",
            "inizio",
            "fine",
            "ore",
            "n_prev",
            "nome_file",
        ]
        total_added, total_removed = 0, 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            cls._create_temp_table(cursor, "giornaliere", target_cols)

            if all_new_rows:
                placeholders = ", ".join(["?"] * len(target_cols))
                data = [tuple(str(x).strip() if x is not None else "" for x in r) for r in all_new_rows]
                cursor.executemany(
                    f"INSERT INTO temp_giornaliere VALUES ({placeholders})",  # nosec B608
                    data,
                )

            for year in years_to_clear:
                added, removed = cls._get_diff_count(cursor, "giornaliere", target_cols, year)
                total_added += added
                total_removed += removed
                cls._replace_data(cursor, "giornaliere", target_cols, year)
            conn.commit()

        return total_added, total_removed

    @classmethod
    def sync_attivita_programmate(cls, db_path: Path, rows_to_insert: list[tuple]) -> tuple[int, int]:
        """
        Sincronizzazione per Attività Programmate.
        Usa DELETE ALL + INSERT per evitare duplicati (sostituzione completa).
        """
        db_cols = [*list(ExcelImporter.ATTIVITA_PROGRAMMATE_MAPPING.values()), "styles"]

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()

            # Count old rows before delete
            cursor.execute("SELECT COUNT(*) FROM attivita_programmate")
            old_count = cursor.fetchone()[0]

            # DELETE ALL existing data (prevents duplicates)
            cursor.execute("DELETE FROM attivita_programmate")

            if rows_to_insert:
                safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in db_cols])
                placeholders = ", ".join(["?"] * len(db_cols))

                # Clean values
                def clean_value(x):
                    if x is None:
                        return ""
                    if isinstance(x, (int, float)):
                        return x
                    return str(x).strip()

                data = [tuple(clean_value(x) for x in r) for r in rows_to_insert]

                cursor.executemany(
                    f"INSERT INTO attivita_programmate ({safe_cols}) VALUES ({placeholders})",  # nosec B608
                    data,
                )

            new_count = len(rows_to_insert) if rows_to_insert else 0
            conn.commit()

            added = max(0, new_count - old_count)
            removed = max(0, old_count - new_count)

            return added, removed

    @classmethod
    def sync_scarico_ore(cls, db_path: Path, rows_to_insert: list[tuple]) -> tuple[int, int]:
        """
        Sincronizzazione ULTRA-OTTIMIZZATA per Scarico Ore (130k+ righe).
        Usa aggressive PRAGMA + batch insert + DELETE ALL per massime prestazioni.
        """
        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()

            # Count old rows before delete
            cursor.execute("SELECT COUNT(*) FROM scarico_ore")
            old_count = cursor.fetchone()[0]

            # Fast replace: DELETE ALL (no need for diff on large tables)
            cursor.execute("DELETE FROM scarico_ore")

            if rows_to_insert:
                columns = ExcelImporter.SCARICO_ORE_COLS
                # Fix B608: Validate column names
                safe_columns = [cls._validate_identifier(c) for c in columns]
                placeholders = ", ".join(["?"] * len(columns))
                insert_query = f"INSERT INTO scarico_ore ({', '.join(safe_columns)}) VALUES ({placeholders})"  # nosec B608

                # Batch insert in larger chunks (10k rows) for better throughput
                batch_size = 10000

                # Pre-process ALL data at once (faster than batch-by-batch)
                all_data = [tuple(str(x).strip() if x is not None else "" for x in r) for r in rows_to_insert]

                # Insert in batches
                for i in range(0, len(all_data), batch_size):
                    batch = all_data[i : i + batch_size]
                    cursor.executemany(insert_query, batch)

            new_count = len(rows_to_insert)
            conn.commit()

            # Return approximate diff (not exact, but fast)
            added = max(0, new_count - old_count)
            removed = max(0, old_count - new_count)

            return added, removed

    @classmethod
    def sync_certificati_campione(cls, db_path: Path, rows_to_insert: list[tuple]) -> tuple[int, int]:
        return cls._sync_upsert_smart(
            db_path,
            "certificati_campione",
            ExcelImporter.CERTIFICATI_CAMPIONE_COLS,
            rows_to_insert,
        )

    @classmethod
    def sync_storico_oda(cls, db_path: Path, rows_to_insert: list[tuple]) -> tuple[int, int]:
        """Sincronizza i dati Storico OdA in modalità Upsert con calcolo diff intelligente."""
        return cls._sync_upsert_smart(
            db_path,
            "storico_oda",
            ExcelImporter.STORICO_ODA_COLS,
            rows_to_insert,
        )

    @classmethod
    def _sync_upsert_smart(
        cls, db_path: Path, table_name: str, columns: list[str], new_data: list[tuple]
    ) -> tuple[int, int]:
        """
        Esegue Upsert (Insert or Replace) calcolando esattamente le righe modificate o aggiunte.
        Usa una tabella temporanea e EXCEPT per confrontare i contenuti.
        """
        if not new_data:
            return 0, 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()

            # 1. Crea temp table e inserisci dati
            cls._create_temp_table(cursor, table_name, columns)

            safe_table = cls._validate_identifier(table_name)
            safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])
            safe_cast_cols = ", ".join([f'CAST("{cls._validate_identifier(c)}" AS TEXT)' for c in columns])
            placeholders = ", ".join(["?"] * len(columns))

            # Preserve numeric types, only strip strings (same as upsert)
            def clean_value(x):
                if x is None:
                    return ""
                if isinstance(x, (int, float)):
                    return x
                return str(x).strip()

            data = [tuple(clean_value(x) for x in r) for r in new_data]

            # Inserimento in temp (tutto come TEXT/affinity dinamica se non specificato in create_temp)
            # Nota: create_temp_table definisce le colonne come TEXT.
            # I valori inseriti verranno convertiti in TEXT da SQLite se necessario.
            cursor.executemany(
                f"INSERT INTO temp_{safe_table} VALUES ({placeholders})",  # nosec B608
                data,
            )

            # 2. Calcola Diff (Righe in Temp che sono diverse da Main)
            # EXCEPT restituisce le righe di Temp che non trovano corrispondenza in Main
            # (confronto colonna per colonna).
            # Main viene castata a TEXT per confrontarsi con Temp (che è TEXT).
            q_diff = f"""
                SELECT COUNT(*) FROM (
                    SELECT {safe_cols} FROM temp_{safe_table}
                    EXCEPT
                    SELECT {safe_cast_cols} FROM {safe_table}
                )
            """  # nosec B608

            cursor.execute(q_diff)
            added_or_updated = cursor.fetchone()[0]

            # 3. Upsert effettivo
            # Copiamo da Temp a Main
            # INSERT OR REPLACE into main SELECT * FROM temp
            q_upsert = (
                f"INSERT OR REPLACE INTO {safe_table} ({safe_cols}) SELECT {safe_cols} FROM temp_{safe_table}"  # nosec B608
            )

            cursor.execute(q_upsert)
            conn.commit()

            return added_or_updated, 0
