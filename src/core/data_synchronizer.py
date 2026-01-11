"""
SyncroJob - Data Synchronizer
Gestisce la sincronizzazione dei dati importati con il database.
"""

import sqlite3
from pathlib import Path
from typing import List, Tuple

from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter


class DataSynchronizer:
    """Gestore per la sincronizzazione dei dati con il database ottimizzato tramite SQL."""

    @classmethod
    def sync_contabilita_dati(
        cls, db_path: Path, imported_data: List[Tuple], imported_years: List[int]
    ) -> Tuple[int, int]:
        """
        Sincronizza i dati della tabella 'contabilita' nel database.
        Usa tabelle temporanee per calcolare il diff in SQL per massima velocità.
        """
        if not imported_data:
            return 0, 0

        total_added = 0
        total_removed = 0
        target_columns = ["year"] + list(ExcelImporter.COLUMNS_MAPPING.values())

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            
            # 1. Crea tabella temporanea per l'import
            cursor.execute("DROP TABLE IF EXISTS temp_contabilita")
            cols_def = ", ".join([f'"{c}" TEXT' for c in target_columns])
            cursor.execute(f"CREATE TEMPORARY TABLE temp_contabilita ({cols_def})")
            
            # 2. Inserimento massivo dei nuovi dati (tutto come stringa per confronto coerente)
            placeholders = ", ".join(["?"] * len(target_columns))
            query_insert = f"INSERT INTO temp_contabilita VALUES ({placeholders})"
            
            # Normalizzazione dati: strip e stringa
            normalized_data = []
            for row in imported_data:
                normalized_data.append(tuple(str(x).strip() if x is not None else "" for x in row))
            
            cursor.executemany(query_insert, normalized_data)

            # 3. Calcolo diff per ogni anno
            for year in imported_years:
                year_str = str(year)
                
                # Righe aggiunte: presenti in temp_contabilita ma non in contabilita
                # Usiamo CAST o stringhe per garantire coerenza
                query_added = f"""
                    SELECT COUNT(*) FROM (
                        SELECT {', '.join([f'"{c}"' for c in target_columns])} FROM temp_contabilita WHERE year = ?
                        EXCEPT
                        SELECT {', '.join([f'CAST("{c}" AS TEXT)' for c in target_columns])} FROM contabilita WHERE year = ?
                    )
                """
                cursor.execute(query_added, (year_str, year))
                total_added += cursor.fetchone()[0]

                # Righe rimosse: presenti in contabilita ma non in temp_contabilita
                query_removed = f"""
                    SELECT COUNT(*) FROM (
                        SELECT {', '.join([f'CAST("{c}" AS TEXT)' for c in target_columns])} FROM contabilita WHERE year = ?
                        EXCEPT
                        SELECT {', '.join([f'"{c}"' for c in target_columns])} FROM temp_contabilita WHERE year = ?
                    )
                """
                cursor.execute(query_removed, (year, year_str))
                total_removed += cursor.fetchone()[0]

                # 4. Sostituzione atomica per l'anno
                cursor.execute("DELETE FROM contabilita WHERE year = ?", (year,))
                cursor.execute(f"""
                    INSERT INTO contabilita ({', '.join([f'"{c}"' for c in target_columns])})
                    SELECT {', '.join([f'"{c}"' for c in target_columns])} FROM temp_contabilita WHERE year = ?
                """, (year_str,))

            conn.commit()

        return total_added, total_removed

    @classmethod
    def sync_giornaliere(
        cls, db_path: Path, all_new_rows: List[Tuple], years_to_clear: List[int]
    ) -> Tuple[int, int]:
        """Sincronizzazione ottimizzata per giornaliere."""
        if not all_new_rows and not years_to_clear:
            return 0, 0

        target_cols = [
            "year", "data", "personale", "descrizione", "tcl", "odc",
            "pdl", "inizio", "fine", "ore", "n_prev", "nome_file"
        ]
        total_added = 0
        total_removed = 0

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("DROP TABLE IF EXISTS temp_giornaliere")
            cols_def = ", ".join([f'"{c}" TEXT' for c in target_cols])
            cursor.execute(f"CREATE TEMPORARY TABLE temp_giornaliere ({cols_def})")
            
            if all_new_rows:
                placeholders = ", ".join(["?"] * len(target_cols))
                normalized = [tuple(str(x).strip() if x is not None else "" for x in r) for r in all_new_rows]
                cursor.executemany(f"INSERT INTO temp_giornaliere VALUES ({placeholders})", normalized)

            for year in years_to_clear:
                year_str = str(year)
                
                # Added
                query_added = f"""
                    SELECT COUNT(*) FROM (
                        SELECT {', '.join([f'"{c}"' for c in target_cols])} FROM temp_giornaliere WHERE year = ?
                        EXCEPT
                        SELECT {', '.join([f'CAST("{c}" AS TEXT)' for c in target_cols])} FROM giornaliere WHERE year = ?
                    )
                """
                cursor.execute(query_added, (year_str, year))
                total_added += cursor.fetchone()[0]

                # Removed
                query_removed = f"""
                    SELECT COUNT(*) FROM (
                        SELECT {', '.join([f'CAST("{c}" AS TEXT)' for c in target_cols])} FROM giornaliere WHERE year = ?
                        EXCEPT
                        SELECT {', '.join([f'"{c}"' for c in target_cols])} FROM temp_giornaliere WHERE year = ?
                    )
                """
                cursor.execute(query_removed, (year, year_str))
                total_removed += cursor.fetchone()[0]

                cursor.execute("DELETE FROM giornaliere WHERE year = ?", (year,))
                cursor.execute(f"""
                    INSERT INTO giornaliere ({', '.join([f'"{c}"' for c in target_cols])})
                    SELECT {', '.join([f'"{c}"' for c in target_cols])} FROM temp_giornaliere WHERE year = ?
                """, (year_str,))

            conn.commit()

        return total_added, total_removed

    @classmethod
    def sync_attivita_programmate(
        cls, db_path: Path, rows_to_insert: List[Tuple]
    ) -> Tuple[int, int]:
        """Sincronizzazione ottimizzata per attività programmate."""
        db_cols = list(ExcelImporter.ATTIVITA_PROGRAMMATE_MAPPING.values()) + ["styles"]
        return cls._sync_generic(db_path, "attivita_programmate", db_cols, rows_to_insert)

    @classmethod
    def sync_scarico_ore(
        cls, db_path: Path, rows_to_insert: List[Tuple]
    ) -> Tuple[int, int]:
        """Sincronizzazione ottimizzata per scarico ore."""
        db_cols = ExcelImporter.SCARICO_ORE_COLS
        return cls._sync_generic(db_path, "scarico_ore", db_cols, rows_to_insert)

    @classmethod
    def sync_certificati_campione(
        cls, db_path: Path, rows_to_insert: List[Tuple]
    ) -> Tuple[int, int]:
        """Sincronizzazione ottimizzata per certificati campione."""
        target_cols = ExcelImporter.CERTIFICATI_CAMPIONE_COLS
        return cls._sync_generic(db_path, "certificati_campione", target_cols, rows_to_insert)

    @classmethod
    def _sync_generic(cls, db_path: Path, table_name: str, columns: List[str], new_data: List[Tuple]) -> Tuple[int, int]:
        """Metodo generico per sincronizzazione tabelle intere."""
        total_added = 0
        total_removed = 0
        
        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"DROP TABLE IF EXISTS temp_{table_name}")
            cols_def = ", ".join([f'"{c}" TEXT' for c in columns])
            cursor.execute(f"CREATE TEMPORARY TABLE temp_{table_name} ({cols_def})")
            
            if new_data:
                placeholders = ", ".join(["?"] * len(columns))
                normalized = [tuple(str(x).strip() if x is not None else "" for x in r) for r in new_data]
                cursor.executemany(f"INSERT INTO temp_{table_name} VALUES ({placeholders})", normalized)

            # Added
            cursor.execute(f"""
                SELECT COUNT(*) FROM (
                    SELECT {', '.join([f'"{c}"' for c in columns])} FROM temp_{table_name}
                    EXCEPT
                    SELECT {', '.join([f'CAST("{c}" AS TEXT)' for c in columns])} FROM {table_name}
                )
            """)
            total_added = cursor.fetchone()[0]

            # Removed
            cursor.execute(f"""
                SELECT COUNT(*) FROM (
                    SELECT {', '.join([f'CAST("{c}" AS TEXT)' for c in columns])} FROM {table_name}
                    EXCEPT
                    SELECT {', '.join([f'"{c}"' for c in columns])} FROM temp_{table_name}
                )
            """)
            total_removed = cursor.fetchone()[0]

            cursor.execute(f"DELETE FROM {table_name}")
            cursor.execute(f"""
                INSERT INTO {table_name} ({', '.join([f'"{c}"' for c in columns])})
                SELECT {', '.join([f'"{c}"' for c in columns])} FROM temp_{table_name}
            """)
            
            conn.commit()
            
        return total_added, total_removed