"""
SyncroJob - Data Synchronizer
Gestisce la sincronizzazione dei dati importati con il database.
"""

import sqlite3
from typing import List, Tuple

import pandas as pd

from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter


class DataSynchronizer:
    """Gestore per la sincronizzazione dei dati con il database."""

    @classmethod
    def sync_contabilita_dati(
        cls, db_path: str, imported_data: List[Tuple], imported_years: List[int]
    ) -> Tuple[int, int]:
        """
        Sincronizza i dati della tabella 'contabilita' nel database.
        Rimuove i dati esistenti per gli anni importati e inserisce i nuovi.
        Restituisce il conteggio delle righe aggiunte e rimosse.
        """
        total_added = 0
        total_removed = 0

        target_columns = ["year"] + list(ExcelImporter.COLUMNS_MAPPING.values())

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()

            for year in imported_years:
                # Fetch existing rows for this year using pandas to ensure identical type/format handling
                existing_df = pd.read_sql(
                    f"SELECT {', '.join(target_columns)} FROM contabilita WHERE year = ?",
                    conn,
                    params=(year,),
                )

                # Apply EXACT SAME cleaning to existing data
                existing_df = existing_df.fillna("")
                cols_to_str_ex = [c for c in existing_df.columns if c != "year"]
                existing_df[cols_to_str_ex] = (
                    existing_df[cols_to_str_ex].astype(str).apply(lambda x: x.str.strip())
                )

                existing_rows = set(list(existing_df.itertuples(index=False, name=None)))

                # New rows from DF (assuming imported_data is already cleaned and formatted)
                new_rows_for_year = [row for row in imported_data if row[0] == year]  # row[0] is 'year'
                new_df_for_year = pd.DataFrame(new_rows_for_year, columns=target_columns)
                new_rows_set = set(list(new_df_for_year.itertuples(index=False, name=None)))

                added = len(new_rows_set - existing_rows)
                removed = len(existing_rows - new_rows_set)

                total_added += added
                total_removed += removed

                cursor.execute("DELETE FROM contabilita WHERE year = ?", (year,))
                placeholders = ", ".join(["?"] * len(target_columns))
                query = f"INSERT INTO contabilita ({', '.join(target_columns)}) VALUES ({placeholders})"
                cursor.executemany(
                    query, new_rows_for_year
                )  # Use already filtered and cleaned new_rows_for_year

            conn.commit()

        return total_added, total_removed

    @classmethod
    def sync_giornaliere(
        cls, db_path: str, all_new_rows: List[Tuple], years_to_clear: List[int]
    ) -> Tuple[int, int]:
        """
        Sincronizza i dati della tabella 'giornaliere' nel database.
        Rimuove i dati esistenti per gli anni specificati e inserisce i nuovi.
        Restituisce il conteggio delle righe aggiunte e rimosse.
        """
        total_added = 0
        total_removed = 0
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

        with db_manager.get_connection(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            existing_rows_set = set()
            if years_to_clear:
                placeholders = ",".join(["?"] * len(years_to_clear))
                query = f"SELECT {', '.join(target_cols)} FROM giornaliere WHERE year IN ({placeholders})"

                existing_df = pd.read_sql(query, conn, params=tuple(years_to_clear))

                existing_df = existing_df.fillna("")
                cols_str_ex = [c for c in existing_df.columns if c != "year"]
                existing_df[cols_str_ex] = existing_df[cols_str_ex].astype(str).apply(lambda x: x.str.strip())

                existing_rows_set = set(list(existing_df.itertuples(index=False, name=None)))

            if all_new_rows:
                new_df = pd.DataFrame(all_new_rows, columns=target_cols)
            else:
                new_df = pd.DataFrame(columns=target_cols)

            new_df = new_df.fillna("")
            cols_str_new = [c for c in new_df.columns if c != "year"]
            new_df[cols_str_new] = new_df[cols_str_new].astype(str).apply(lambda x: x.str.strip())

            new_rows_set = set(list(new_df.itertuples(index=False, name=None)))

            total_added = len(new_rows_set - existing_rows_set)
            total_removed = len(existing_rows_set - new_rows_set)

            for year in years_to_clear:
                cursor.execute("DELETE FROM giornaliere WHERE year = ?", (year,))

            final_rows_to_insert = list(new_df.itertuples(index=False, name=None))

            if final_rows_to_insert:
                placeholders = ", ".join(["?"] * len(target_cols))
                query = f"INSERT INTO giornaliere ({', '.join(target_cols)}) VALUES ({placeholders})"
                cursor.executemany(query, final_rows_to_insert)

            conn.commit()

        return total_added, total_removed

    @classmethod
    def sync_attivita_programmate(cls, db_path: str, rows_to_insert: List[Tuple]) -> Tuple[int, int]:
        """
        Sincronizza i dati della tabella 'attivita_programmate' nel database.
        Rimuove tutti i dati esistenti e inserisce i nuovi.
        Restituisce il conteggio delle righe aggiunte e rimosse.
        """
        total_added = 0
        total_removed = 0
        db_cols = list(ExcelImporter.ATTIVITA_PROGRAMMATE_MAPPING.values()) + ["styles"]

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()

            existing_df = pd.read_sql(f"SELECT {', '.join(db_cols)} FROM attivita_programmate", conn)
            existing_df = existing_df.fillna("")
            existing_df = existing_df.astype(str).apply(lambda x: x.str.strip())
            existing_rows_set = set(list(existing_df.itertuples(index=False, name=None)))

            new_rows_set = set(rows_to_insert)

            total_added = len(new_rows_set - existing_rows_set)
            total_removed = len(existing_rows_set - new_rows_set)

            cursor.execute("DELETE FROM attivita_programmate")

            if rows_to_insert:
                placeholders = ", ".join(["?"] * len(db_cols))
                query = f"INSERT INTO attivita_programmate ({', '.join(db_cols)}) VALUES ({placeholders})"
                cursor.executemany(query, rows_to_insert)

            conn.commit()

        return total_added, total_removed

    @classmethod
    def sync_scarico_ore(cls, db_path: str, rows_to_insert: List[Tuple]) -> Tuple[int, int]:
        """
        Sincronizza i dati della tabella 'scarico_ore' nel database.
        Rimuove tutti i dati esistenti e inserisce i nuovi.
        Restituisce il conteggio delle righe aggiunte e rimosse.
        """
        total_added = 0
        total_removed = 0
        db_cols = ExcelImporter.SCARICO_ORE_COLS

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()

            existing_df = pd.read_sql(f"SELECT {', '.join(db_cols)} FROM scarico_ore", conn)
            existing_df = existing_df.fillna("")
            existing_df = existing_df.astype(str).apply(lambda x: x.str.strip())
            existing_rows_set = set(list(existing_df.itertuples(index=False, name=None)))

            if rows_to_insert:
                new_df = pd.DataFrame(rows_to_insert, columns=db_cols)
                new_df = new_df.fillna("")
                new_df = new_df.astype(str).apply(lambda x: x.str.strip())
                new_rows_set = set(list(new_df.itertuples(index=False, name=None)))
            else:
                new_rows_set = set()

            total_added = len(new_rows_set - existing_rows_set)
            total_removed = len(existing_rows_set - new_rows_set)

            cursor.execute("DELETE FROM scarico_ore")

            if rows_to_insert:
                placeholders = ", ".join(["?"] * len(db_cols))
                query = f"INSERT INTO scarico_ore ({', '.join(db_cols)}) VALUES ({placeholders})"
                cursor.executemany(query, rows_to_insert)

            conn.commit()

        return total_added, total_removed

    @classmethod
    def sync_certificati_campione(cls, db_path: str, rows_to_insert: List[Tuple]) -> Tuple[int, int]:
        """
        Sincronizza i dati della tabella 'certificati_campione' nel database.
        Rimuove tutti i dati esistenti e inserisce i nuovi.
        Restituisce il conteggio delle righe aggiunte e rimosse.
        """
        total_added = 0
        total_removed = 0
        target_cols = ExcelImporter.CERTIFICATI_CAMPIONE_COLS

        with db_manager.get_connection(db_path) as conn:
            cursor = conn.cursor()

            existing_df = pd.read_sql(f"SELECT {', '.join(target_cols)} FROM certificati_campione", conn)
            existing_df = existing_df.fillna("")
            existing_df = existing_df.astype(str).apply(lambda x: x.str.strip())
            existing_rows_set = set(list(existing_df.itertuples(index=False, name=None)))

            new_rows_set = set(rows_to_insert)

            total_added = len(new_rows_set - existing_rows_set)
            total_removed = len(existing_rows_set - new_rows_set)

            cursor.execute("DELETE FROM certificati_campione")

            if rows_to_insert:
                placeholders = ", ".join(["?"] * len(target_cols))
                query = f"INSERT INTO certificati_campione ({', '.join(target_cols)}) VALUES ({placeholders})"
                cursor.executemany(query, rows_to_insert)

            conn.commit()

        return total_added, total_removed
