"""
Bot TS - Timbrature Storage
Handles database operations for Timbrature.
"""

import sqlite3
import pandas as pd
import json
from pathlib import Path
from typing import Optional, List, Dict, Callable
from src.core import config_manager
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
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_data ON timbrature(data)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_nome_cogn ON timbrature(nome, cognome)")
            conn.commit()

    def _ensure_db_exists(self):
        """Creates database and table if they don't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def search_employees(self, query: str) -> List[Dict]:
        """
        Cerca dipendenti per nome/cognome.
        Returns: Lista di dizionari con info dipendente.
        """
        query = query.strip().lower()
        if len(query) < 2: return []

        results = []
        try:
            with db_manager.get_connection(self.db_path, read_only=True) as conn:
                cursor = conn.cursor()
                # Cerca dipendenti unici
                sql = """
                    SELECT DISTINCT nome, cognome 
                    FROM timbrature 
                    WHERE lower(nome) LIKE ? OR lower(cognome) LIKE ?
                    LIMIT 20
                """
                like_query = f"%{query}%"
                cursor.execute(sql, (like_query, like_query))
                
                rows = cursor.fetchall()
                for row in rows:
                    results.append({
                        "nome": row[0],
                        "cognome": row[1]
                    })
        except Exception:
            pass
        return results

    def get_employees(self) -> List[Dict[str, str]]:
        """
        Recupera la lista unica dei dipendenti incrociando timbrature e mappature in config.json.
        """
        config = config_manager.load_config()
        mappings = config.get("employee_mappings", {})

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
                key = f"{nome}|{cognome}"
                
                emp_data = mappings.get(key, {"reparto": "", "cantiere": ""})

                employees.append({
                    "nome": nome,
                    "cognome": cognome,
                    "reparto": emp_data.get("reparto", ""),
                    "cantiere": emp_data.get("cantiere", "")
                })

            return employees

    def update_employee_details(self, nome: str, cognome: str, reparto: str = None, cantiere: str = None):
        """Salva l'assegnazione reparto/cantiere direttamente in config.json."""
        config = config_manager.load_config()
        mappings = config.get("employee_mappings", {})
        
        key = f"{nome}|{cognome}"
        current = mappings.get(key, {"reparto": "", "cantiere": ""})
        
        if reparto is not None: current["reparto"] = reparto
        if cantiere is not None: current["cantiere"] = cantiere
        
        mappings[key] = current
        config_manager.set_config_value("employee_mappings", mappings)

    def get_timbrature_with_reparto(self, limit: int = 500, filter_text: str = None, filter_reparto: str = None, filter_cantiere: str = None) -> List[tuple]:
        """
        Recupera le timbrature e le arricchisce con i dati da config.json.
        """
        config = config_manager.load_config()
        mappings = config.get("employee_mappings", {})

        with db_manager.get_connection(self.db_path) as conn:
            cursor = conn.cursor()

            # Query base (solo sulla tabella timbrature)
            query = "SELECT data, ingresso, uscita, nome, cognome, presenza_ts, sito_timbratura FROM timbrature"
            params = []
            conditions = []

            if filter_text:
                search_terms = filter_text.lower().split()
                columns_to_search = ["data", "nome", "cognome", "sito_timbratura"]
                for term in search_terms:
                    search_term = term
                    # (Logic date conversion DD/MM/YYYY omitted for brevity, same as before)
                    if '/' in term:
                        try:
                            parts = term.split('/')
                            if len(parts) == 3: d, m, y = parts; search_term = f"{y}-{m.zfill(2)}-{d.zfill(2)}"
                        except: pass
                    term_conditions = [f"{col} LIKE ?" for col in columns_to_search]
                    params.extend([f"%{search_term}%"] * len(columns_to_search))
                    conditions.append(f"({' OR '.join(term_conditions)})")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += f" ORDER BY id DESC LIMIT {limit * 2}" # Fetch more to allow Python filtering

            cursor.execute(query, params)
            raw_rows = cursor.fetchall()

            # Arricchimento e Filtro Python
            final_rows = []
            for row in raw_rows:
                # row indices: 0:data, 1:ingresso, 2:uscita, 3:nome, 4:cognome, 5:presenza_ts, 6:sito
                nome, cognome = row[3], row[4]
                key = f"{nome}|{cognome}"
                emp_data = mappings.get(key, {"reparto": "", "cantiere": ""})
                
                rep = emp_data.get("reparto", "")
                cant = emp_data.get("cantiere", "")

                # Applica Filtri Reparto/Cantiere
                if filter_reparto and filter_reparto != "Tutti" and rep != filter_reparto:
                    continue
                if filter_cantiere and filter_cantiere != "Tutti" and cant != filter_cantiere:
                    continue

                final_rows.append(row + (rep, cant))
                
                if len(final_rows) >= limit:
                    break

            return final_rows

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

    def get_lists(self) -> Dict[str, List[str]]:
        """Recupera le liste configurate (Reparti, Cantieri) da config.json con migrazione automatica."""
        config = config_manager.load_config()
        
        # Logica di migrazione se mancano i dati nel config ma esiste il vecchio file
        if "reparti" not in config or (not config.get("reparti") and not config.get("cantieri")):
            old_path = self.db_path.parent / "timbrature_lists.json"
            if old_path.exists():
                try:
                    import json
                    with open(old_path, 'r', encoding='utf-8') as f:
                        old_data = json.load(f)
                        if old_data:
                            self.save_lists(old_data)
                            return old_data
                except: pass

        return {
            "reparti": config.get("reparti", ["STRUMENTALE", "ELETTRICO", "CANTIERE", "ANALISI"]),
            "cantieri": config.get("cantieri", [])
        }

    def save_lists(self, data: Dict[str, List[str]]):
        """Salva le liste configurate in config.json."""
        config_manager.set_config_value("reparti", data.get("reparti", []))
        config_manager.set_config_value("cantieri", data.get("cantieri", []))
