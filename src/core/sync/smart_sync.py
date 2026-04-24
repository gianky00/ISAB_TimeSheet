"""
SyncroJob - Smart Sync Engine
Gestisce sincronizzazioni intelligenti (UPSERT) con calcolo esatto del delta via EXCEPT.
"""

from contextlib import suppress
from pathlib import Path
from typing import Any

from src.core.database import db_manager
from src.core.sync.base import BaseSyncEngine


class SmartSyncEngine(BaseSyncEngine):
    """Motore di sync intelligente per tabelle con chiavi primarie (Certificati, ODA)."""

    @classmethod
    def sync_upsert_smart(  # noqa: PLR0913
        cls,
        db_path: Path,
        table_name: str,
        columns: list[str],
        new_data: list[tuple[Any, ...]],
        conflict_cols: list[str] | None = None,
        mirror: bool = False,
    ) -> tuple[int, int]:
        """Esegue Upsert calcolando esattamente le righe modificate o aggiunte."""
        if not new_data:
            return 0, 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            temp_table = cls._create_temp_table(cursor, table_name, columns)

            safe_table = cls._validate_identifier(table_name)
            safe_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in columns])
            safe_cast_cols = ", ".join([f'CAST("{cls._validate_identifier(c)}" AS TEXT)' for c in columns])
            placeholders = ", ".join(["?"] * len(columns))

            data = [tuple(cls._clean_value(x) for x in r) for r in new_data]
            cursor.executemany(f"INSERT INTO {temp_table} VALUES ({placeholders})", data)  # nosec B608

            # Calcola Diff (Righe in Temp diverse da Main)
            q_diff = f"""
                SELECT COUNT(*) FROM (
                    SELECT {safe_cols} FROM {temp_table}
                    EXCEPT
                    SELECT {safe_cast_cols} FROM {safe_table}
                )
            """  # nosec B608
            cursor.execute(q_diff)
            added_or_updated = cursor.fetchone()[0]

            # Upsert
            if conflict_cols:
                safe_conflict = ", ".join([f'"{cls._validate_identifier(c)}"' for c in conflict_cols])
                update_assignments = ", ".join(
                    [
                        f'"{cls._validate_identifier(c)}" = excluded."{cls._validate_identifier(c)}"'
                        for c in columns
                        if c not in conflict_cols
                    ]
                )

                # Se non ci sono colonne da aggiornare (tutte in conflict_cols), facciamo DO NOTHING
                if update_assignments:
                    q_upsert = f"""
                        INSERT INTO {safe_table} ({safe_cols})
                        SELECT {safe_cols} FROM {temp_table}
                        WHERE true
                        ON CONFLICT({safe_conflict}) DO UPDATE SET
                        {update_assignments}
                    """  # nosec B608
                else:
                    q_upsert = f"""
                        INSERT INTO {safe_table} ({safe_cols})
                        SELECT {safe_cols} FROM {temp_table}
                        WHERE true
                        ON CONFLICT({safe_conflict}) DO NOTHING
                    """  # nosec B608
            else:
                q_upsert = (
                    f"INSERT OR REPLACE INTO {safe_table} ({safe_cols}) SELECT {safe_cols} FROM {temp_table}"  # nosec B608
                )

            cursor.execute(q_upsert)

            # 3. Mirroring (Cancellazione righe rimosse dall'Excel)
            deleted_count = 0
            if mirror and conflict_cols:
                # Mirroring intelligente: cancelliamo solo se l'identità principale (es. Matricola)
                # non è più presente nel file Excel. Questo preserva lo storico per gli strumenti esistenti.
                main_id_col = conflict_cols[0]
                q_mirror = f"""
                    DELETE FROM {safe_table}
                    WHERE "{cls._validate_identifier(main_id_col)}" NOT IN (
                        SELECT "{cls._validate_identifier(main_id_col)}" FROM {temp_table}
                    )
                """  # nosec B608
                cursor.execute(q_mirror)
                deleted_count = cursor.rowcount

            conn.commit()

            return added_or_updated, deleted_count

    @classmethod
    def sync_full_replace_with_metadata(  # noqa: PLR0913
        cls,
        db_path: Path,
        table_name: str,
        columns: list[str],
        new_data: list[tuple[Any, ...]],
        key_cols: list[str],
        metadata_cols: list[str],
    ) -> tuple[int, int]:
        """
        Sostituisce completamente il contenuto della tabella con i nuovi dati,
        ma tenta di preservare i metadati (es. annotazioni) per le righe esistenti.
        """
        if not new_data:
            return 0, 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            safe_table = cls._validate_identifier(table_name)

            # 1. Salva i metadati attuali in un dizionario {(key1, key2): {meta1: val, ...}}
            # Usiamo i key_cols (es. matricola, certificato) come chiave di matching
            current_metadata = {}
            if key_cols and metadata_cols:
                all_cols = key_cols + metadata_cols
                safe_all_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in all_cols])
                with suppress(Exception):
                    cursor.execute(f"SELECT {safe_all_cols} FROM {safe_table}")
                    for row in cursor.fetchall():
                        keys = tuple(str(row[i]).strip() for i in range(len(key_cols)))
                        meta = {metadata_cols[i]: row[len(key_cols) + i] for i in range(len(metadata_cols))}
                        current_metadata[keys] = meta

            # 2. Svuota la tabella
            cursor.execute(f"DELETE FROM {safe_table}")

            # 3. Prepara i nuovi dati applicando i metadati salvati (se corrispondono)
            # Dobbiamo mappare le colonne di input alle colonne finali del DB
            final_rows = []
            for r in new_data:
                # Trasformiamo la riga in una lista per poterla modificare
                row_list = list(r)

                # Cerchiamo se abbiamo metadati salvati per questa riga
                # Assumiamo che l'ordine in r corrisponda a columns
                keys_val = []
                for k in key_cols:
                    if k in columns:
                        idx = columns.index(k)
                        keys_val.append(str(r[idx]).strip())

                match_key = tuple(keys_val)
                saved_meta = current_metadata.get(match_key)

                # Prepariamo la riga finale: [valori_excel] + [metadati_o_default]
                # Nota: qui dobbiamo stare attenti all'ordine previsto dalla tabella nel DB
                # Per semplicità, ricostruiamo la riga per l'INSERT
                meta_values = []
                for m in metadata_cols:
                    val = saved_meta.get(m) if saved_meta else ""
                    meta_values.append(val)

                final_rows.append(tuple(row_list) + tuple(meta_values))

            # 4. Inserimento massivo
            # Costruiamo la query basata su TUTTE le colonne (data + metadata)
            all_db_cols = columns + metadata_cols
            safe_db_cols = ", ".join([f'"{cls._validate_identifier(c)}"' for c in all_db_cols])
            placeholders = ", ".join(["?"] * len(all_db_cols))

            cursor.executemany(
                f"INSERT INTO {safe_table} ({safe_db_cols}) VALUES ({placeholders})",
                final_rows
            )

            conn.commit()
            return len(final_rows), 0
