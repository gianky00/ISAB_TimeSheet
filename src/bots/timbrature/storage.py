"""
Bot TS - Timbrature Storage
Handles database operations for Timbrature.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Callable
from src.core.config_manager import CONFIG_DIR

class TimbratureStorage:
    """Manages SQLite database for Timbrature."""

    DB_PATH = CONFIG_DIR / "data" / "timbrature_Isab.db"

    COLUMNS_MAP = {
        "Data Timbratura": "data",
        "Ora Ingresso": "ingresso",
        "Ora Uscita": "uscita",
        "Nome Risorsa": "nome",
        "Cognome Risorsa": "cognome",
        "Presente Nei Timesheet": "presenza_ts",
        "Sito Timbratura": "sito_timbratura"
    }

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Creates database and table if they don't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timbrature (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT,
                    ingresso TEXT,
                    uscita TEXT,
                    nome TEXT,
                    cognome TEXT,
                    presenza_ts TEXT,
                    sito_timbratura TEXT,
                    UNIQUE(data, ingresso, uscita, nome, cognome)
                )
            ''')
            conn.commit()

    def import_excel(self, excel_path: str, log_callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Imports an Excel file into the database.

        Args:
            excel_path: Path to the Excel file.
            log_callback: Optional callback for logging messages.

        Returns:
            True if import was successful.
        """
        def log(msg):
            if log_callback:
                log_callback(msg)
            else:
                print(msg)

        try:
            df = pd.read_excel(excel_path, engine='openpyxl')

            # Normalize column names
            df.columns = df.columns.str.strip()

            # Validate columns
            missing_cols = [c for c in self.COLUMNS_MAP.keys() if c not in df.columns]
            if missing_cols:
                log(f"⚠️ Colonne mancanti nel file Excel: {missing_cols}")
                return False

            # Filter and rename
            df_filtered = df[list(self.COLUMNS_MAP.keys())].copy()
            df_filtered.rename(columns=self.COLUMNS_MAP, inplace=True)

            added_count = 0
            skipped_count = 0

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                for _, row in df_filtered.iterrows():
                    try:
                        # Normalize date
                        if 'data' in row and pd.notna(row['data']):
                            if isinstance(row['data'], (pd.Timestamp, pd.DatetimeIndex)):
                                row['data'] = row['data'].strftime('%Y-%m-%d')
                            else:
                                try:
                                    ts = pd.to_datetime(row['data'])
                                    row['data'] = ts.strftime('%Y-%m-%d')
                                except:
                                    pass # Keep original if parse fails

                        vals = row.fillna("").astype(str).to_dict()

                        cursor.execute('''
                            INSERT INTO timbrature (data, ingresso, uscita, nome, cognome, presenza_ts, sito_timbratura)
                            VALUES (:data, :ingresso, :uscita, :nome, :cognome, :presenza_ts, :sito_timbratura)
                        ''', vals)
                        added_count += 1
                    except sqlite3.IntegrityError:
                        skipped_count += 1
                    except Exception as e:
                        log(f"Errore riga: {e}")

                conn.commit()

            log(f"Importazione: {added_count} nuovi record aggiunti, {skipped_count} duplicati ignorati.")
            return True

        except Exception as e:
            log(f"Errore lettura Excel: {e}")
            raise e
