"""
Bot TS - Timbrature Storage
Handles database operations for Timbrature.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Callable
from src.core.config_manager import CONFIG_DIR
from src.core.database import db_manager

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

    def _init_schema(self):
        """Initializes the database schema for timbrature."""
        with db_manager.get_connection(self.db_path) as conn:
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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dipendenti (
                    nome TEXT,
                    cognome TEXT,
                    reparto TEXT,
                    PRIMARY KEY (nome, cognome)
                )
            ''')
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_data ON timbrature(data)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_nome_cogn ON timbrature(nome, cognome)")
            conn.commit()

    def _ensure_db_exists(self):
        """Creates database and table if they don't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def get_employees(self) -> List[Dict[str, str]]:
        """
        Recupera la lista unica dei dipendenti (da timbrature e dipendenti).
        Restituisce una lista di dict: {'nome': ..., 'cognome': ..., 'reparto': ...}
        """
        with db_manager.get_connection(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Ottieni tutti i dipendenti unici dalle timbrature
            cursor.execute("SELECT DISTINCT nome, cognome FROM timbrature ORDER BY cognome, nome")
            rows = cursor.fetchall()

            employees = []
            for row in rows:
                nome = row['nome']
                cognome = row['cognome']

                # Cerca reparto salvato
                cursor.execute("SELECT reparto FROM dipendenti WHERE nome = ? AND cognome = ?", (nome, cognome))
                res = cursor.fetchone()
                reparto = res['reparto'] if res else ""

                employees.append({
                    "nome": nome,
                    "cognome": cognome,
                    "reparto": reparto
                })

            return employees

    def update_employee_reparto(self, nome: str, cognome: str, reparto: str):
        """Aggiorna il reparto di un dipendente."""
        with db_manager.get_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO dipendenti (nome, cognome, reparto)
                VALUES (?, ?, ?)
                ON CONFLICT(nome, cognome) DO UPDATE SET reparto = excluded.reparto
            ''', (nome, cognome, reparto))
            conn.commit()

    def get_timbrature_with_reparto(self, limit: int = 500, filter_text: str = None, filter_reparto: str = None) -> List[tuple]:
        """
        Recupera le timbrature con il reparto associato (JOIN).
        Restituisce lista di tuple (data, ingresso, uscita, nome, cognome, presenza_ts, sito_timbratura, reparto).
        """
        with db_manager.get_connection(self.db_path) as conn:
            cursor = conn.cursor()

            query = """
                SELECT
                    t.data, t.ingresso, t.uscita, t.nome, t.cognome,
                    t.presenza_ts, t.sito_timbratura, d.reparto
                FROM timbrature t
                LEFT JOIN dipendenti d ON t.nome = d.nome AND t.cognome = d.cognome
            """

            params = []
            conditions = []

            if filter_text:
                # Logica di ricerca testuale (multi-term)
                search_terms = filter_text.lower().split()
                columns_to_search = ["t.data", "t.nome", "t.cognome", "t.sito_timbratura"]

                for term in search_terms:
                    # Gestione Date (DD/MM/YYYY -> YYYY-MM-DD o partials)
                    search_term = term
                    if '/' in term:
                        try:
                            parts = term.split('/')
                            if len(parts) == 3: # DD/MM/YYYY
                                d, m, y = parts
                                if len(d) <= 2 and len(m) <= 2 and len(y) == 4:
                                     search_term = f"{y}-{m.zfill(2)}-{d.zfill(2)}"
                            elif len(parts) == 2: # MM/YYYY
                                p1, p2 = parts
                                if len(p2) == 4:
                                    search_term = f"{p2}-{p1.zfill(2)}"
                                elif len(p2) <= 2: # DD/MM -> -MM-DD
                                    search_term = f"-{p2.zfill(2)}-{p1.zfill(2)}"
                        except: pass

                    term_conditions = [f"{col} LIKE ?" for col in columns_to_search]
                    params.extend([f"%{search_term}%"] * len(columns_to_search))
                    conditions.append(f"({' OR '.join(term_conditions)})")

            if filter_reparto and filter_reparto != "Tutti":
                conditions.append("d.reparto = ?")
                params.append(filter_reparto)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += f" ORDER BY t.id DESC LIMIT {limit}"

            cursor.execute(query, params)
            return cursor.fetchall()

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

            with db_manager.get_connection(self.db_path) as conn:
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
