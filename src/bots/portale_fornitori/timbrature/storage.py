"""
SyncroJob - Timbrature Storage
Handles database operations for Timbrature.
"""

import sqlite3
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path
from typing import Any, ClassVar, cast

import pandas as pd

from src.core import config_manager
from src.core.config_manager import CONFIG_DIR
from src.core.database import db_manager
from src.core.sync_tracker import SyncTracker


class TimbratureStorage:
    """Manages SQLite database for Timbrature."""

    DB_PATH: ClassVar[Path] = CONFIG_DIR / "data" / "timbrature_Isab.db"

    COLUMNS_MAP: ClassVar[dict[str, str]] = {
        "Id Dipendente": "id_dipendente",
        "Data Timbratura": "data",
        "Ora Ingresso": "ingresso",
        "Ora Uscita": "uscita",
        "Fornitore": "fornitore",
        "Codice Fornitore RILPRES": "codice_rilpres",
        "Numero Badge": "numero_badge",
        "Nome Risorsa": "nome",
        "Cognome Risorsa": "cognome",
        "Codice Fiscale": "codice_fiscale",
        "Codice Qualifica": "codice_qualifica",
        "Specializzazione": "specializzazione",
        "Società Ospitante": "societa_ospitante",
        "Data Ins": "data_ins",
        "Presente Nei Timesheet": "presenza_ts",
        "Sito Timbratura": "sito_timbratura",
    }

    def __init__(self, db_path: Path = DB_PATH):
        """Inizializza il database delle timbrature configurando il percorso e lo schema."""
        self.db_path = Path(db_path)
        self._ensure_db_exists()

    def _init_schema(self):
        """Initializes the database schema for timbrature with all real columns."""
        with db_manager.get_connection(self.db_path) as conn:
            cursor = conn.cursor()

            # 1. Crea tabella se non esiste con schema completo
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS timbrature (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_dipendente TEXT,
                    data TEXT,
                    ingresso TEXT,
                    uscita TEXT,
                    fornitore TEXT,
                    codice_rilpres TEXT,
                    numero_badge TEXT,
                    nome TEXT,
                    cognome TEXT,
                    codice_fiscale TEXT,
                    codice_qualifica TEXT,
                    specializzazione TEXT,
                    societa_ospitante TEXT,
                    data_ins TEXT,
                    presenza_ts TEXT,
                    sito_timbratura TEXT,
                    UNIQUE(data, ingresso, uscita, nome, cognome)
                )
            """
            )

            # 2. Migrazione manuale: aggiungi colonne se la tabella esiste già ma è incompleta
            cursor.execute("PRAGMA table_info(timbrature)")
            existing_cols = [row[1] for row in cursor.fetchall()]

            expected_cols = {
                "id_dipendente": "TEXT",
                "fornitore": "TEXT",
                "codice_rilpres": "TEXT",
                "numero_badge": "TEXT",
                "codice_fiscale": "TEXT",
                "codice_qualifica": "TEXT",
                "specializzazione": "TEXT",
                "societa_ospitante": "TEXT",
                "data_ins": "TEXT",
                "ore_effettive": "TEXT",  # Presente in alcune migrazioni v3
            }

            for col, col_type in expected_cols.items():
                if col not in existing_cols:
                    with suppress(sqlite3.OperationalError):
                        cursor.execute(f"ALTER TABLE timbrature ADD COLUMN {col} {col_type}")  # nosec B608

            # 3. Indici
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_data ON timbrature(data)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_nome_cogn ON timbrature(nome, cognome)")

            if "codice_fiscale" in [
                row[1] for row in cursor.execute("PRAGMA table_info(timbrature)").fetchall()
            ]:
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_timb_cf ON timbrature(codice_fiscale)")

            conn.commit()

    def _ensure_db_exists(self):
        """Creates database and table if they don't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def search_employees(self, query: str) -> list[dict[str, str]]:
        """
        Cerca dipendenti per nome/cognome.
        Returns: Lista di dizionari con info dipendente.
        """
        query = query.strip().lower()
        if len(query) < 2:
            return []

        results: list[dict[str, str]] = []
        with suppress(Exception), db_manager.get_connection(self.db_path, read_only=True) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Cerca dipendenti unici
            sql = """
                    SELECT DISTINCT nome, cognome, codice_fiscale
                    FROM timbrature
                    WHERE lower(nome) LIKE ? OR lower(cognome) LIKE ? OR lower(codice_fiscale) LIKE ?
                    LIMIT 20
                """
            like_query = f"%{query}%"
            cursor.execute(sql, (like_query, like_query, like_query))

            rows = cursor.fetchall()
            results.extend(
                {
                    "nome": str(row["nome"]),
                    "cognome": str(row["cognome"]),
                    "codice_fiscale": str(row["codice_fiscale"]),
                }
                for row in rows
            )
        return results

    def get_employees(self) -> list[dict[str, str]]:
        """
        Recupera la lista unica dei dipendenti incrociando timbrature e mappature in config.json.
        """
        mappings = config_manager.load_config().get("employee_mappings", {})

        with db_manager.get_connection(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Ottieni tutti i dipendenti unici dalle timbrature
            rows = cursor.execute(
                "SELECT DISTINCT nome, cognome, codice_fiscale FROM timbrature ORDER BY cognome, nome"
            ).fetchall()

            employees = []
            for row in rows:
                nome, cognome = row["nome"], row["cognome"]
                cf = row["codice_fiscale"]
                key = f"{nome}|{cognome}"

                emp_data = mappings.get(key, {"reparto": "", "cantiere": ""})

                employees.append(
                    {
                        "nome": nome,
                        "cognome": cognome,
                        "codice_fiscale": cf or "",
                        "reparto": emp_data.get("reparto", ""),
                        "cantiere": emp_data.get("cantiere", ""),
                    }
                )

            return employees

    def update_employee_details(
        self,
        nome: str,
        cognome: str,
        reparto: str | None = None,
        cantiere: str | None = None,
    ):
        """
        Aggiorna le informazioni di reparto e cantiere per un dipendente specifico.
        I dati vengono salvati nel file di configurazione globale.

        Args:
            nome: Nome del dipendente.
            cognome: Cognome del dipendente.
            reparto: Nome del reparto opzionale.
            cantiere: Nome del cantiere opzionale.
        """
        mappings = config_manager.load_config().get("employee_mappings", {})

        key = f"{nome}|{cognome}"
        current = mappings.get(key, {"reparto": "", "cantiere": ""})

        if reparto is not None:
            current["reparto"] = reparto
        if cantiere is not None:
            current["cantiere"] = cantiere

        mappings[key] = current
        config_manager.set_config_value("employee_mappings", mappings)

    def get_timbrature_with_reparto(
        self,
        limit: int = 500,
        filter_text: str | None = None,
        filter_reparto: str | None = None,
        filter_cantiere: str | None = None,
    ) -> list[tuple[Any, ...]]:
        """Recupera le timbrature e le arricchisce con i dati da config.json."""
        mappings: dict[str, dict[str, str]] = config_manager.load_config().get("employee_mappings", {})

        with db_manager.get_connection(self.db_path) as conn:
            cursor = conn.cursor()
            sql, params = self._build_timb_query(filter_text, limit)
            raw_rows = cursor.execute(sql, params).fetchall()

            return self._enrich_and_filter_timb(raw_rows, mappings, filter_reparto, filter_cantiere, limit)

    def _build_timb_query(self, filter_text: str | None, limit: int) -> tuple[str, list[Any]]:
        query = """
            SELECT data, ingresso, uscita, nome, cognome, presenza_ts, sito_timbratura,
                   codice_fiscale, id_dipendente, fornitore, codice_rilpres, numero_badge,
                   codice_qualifica, specializzazione, societa_ospitante, data_ins
            FROM timbrature
        """
        params: list[str] = []
        if not filter_text:
            return query + f" ORDER BY id DESC LIMIT {limit * 2}", params

        search_terms = filter_text.lower().split()
        conditions = []
        for term in search_terms:
            search_term = self._normalize_search_date(term)
            term_conditions = [
                f"{col} LIKE ?"
                for col in (
                    "data",
                    "nome",
                    "cognome",
                    "sito_timbratura",
                    "codice_fiscale",
                )
            ]
            params.extend([f"%{search_term}%"] * 5)
            conditions.append(f"({' OR '.join(term_conditions)})")

        query += " WHERE " + " AND ".join(conditions)
        return query + f" ORDER BY id DESC LIMIT {limit * 2}", params

    def _normalize_search_date(self, term: str) -> str:
        """
        Tenta di convertire una data input (DD/MM/YYYY, DD-MM-YYYY, ecc)
        nel formato DB (YYYY-MM-DD).
        """
        term = term.strip()

        # Mapping preliminare separatori
        clean_term = term
        for sep in ("/", ".", " "):
            clean_term = clean_term.replace(sep, "-")

        if "-" in clean_term:
            with suppress(Exception):
                parts = clean_term.split("-")

                # Caso DD-MM (es. 05/12 -> cerca 12 Dicembre)
                if len(parts) == 2:
                    d, m = parts
                    # Ignoriamo se contengono testo
                    if d.isdigit() and m.isdigit():
                        return f"-{m.zfill(2)}-{d.zfill(2)}"

                # Caso DD-MM-YYYY
                if len(parts) == 3:
                    d, m, y = parts

                    # Se l'anno è incompleto (es. 202), non normalizzare ancora
                    # Ritorna il termine originale parziale per permettere like testuale se serve,
                    # ma probabilmente fallirà il match su YYYY-MM-DD.
                    # Ma meglio che fallire convertendo in "202-12-05".
                    if len(y) not in (2, 4):
                        return term

                    # Gestione anno 2 cifre
                    if len(y) == 2:
                        y = "20" + y

                    # Ricostruisci YYYY-MM-DD
                    return f"{y}-{m.zfill(2)}-{d.zfill(2)}"

        return term

    def _enrich_and_filter_timb(
        self,
        rows: list[tuple[Any, ...]],
        mappings: dict[str, dict[str, str]],
        f_rep: str | None,
        f_cant: str | None,
        limit: int,
    ) -> list[tuple[Any, ...]]:
        final: list[tuple[Any, ...]] = []
        for r in rows:
            # Indices: 0:data, 1:ingresso, 2:uscita, 3:nome, 4:cognome, ...
            nome, cognome = r[3], r[4]
            emp = mappings.get(f"{nome}|{cognome}", {"reparto": "", "cantiere": ""})
            rep, cant = emp.get("reparto", ""), emp.get("cantiere", "")

            if f_rep and f_rep != "Tutti" and rep != f_rep:
                continue
            if f_cant and f_cant != "Tutti" and cant != f_cant:
                continue

            final.append((*r, rep, cant))
            if len(final) >= limit:
                break
        return final

    def import_excel(self, excel_path: str, log_callback: Callable[[str], None] | None = None) -> bool:
        """Imports an Excel file into the database."""

        def log(m):
            """Internal logging helper."""
            log_callback(m) if log_callback else print(m)

        with suppress(Exception):
            df = pd.read_excel(excel_path, engine="openpyxl")
            df.columns = df.columns.str.strip()

            missing = [c for c in self.COLUMNS_MAP if c not in df.columns]
            if missing:
                log(f"⚠️ Colonne mancanti: {missing}")
                # return False - Non bloccare se mancano CF o Ore Effettive (vecchi file)

            # Filtriamo solo le colonne presenti
            cols_to_use = [c for c in self.COLUMNS_MAP if c in df.columns]
            df_filtered = df[cols_to_use].copy()
            df_filtered.rename(columns=self.COLUMNS_MAP, inplace=True)

            # Aggiungi colonne mancanti con valori vuoti
            for db_col in self.COLUMNS_MAP.values():
                if db_col not in df_filtered.columns:
                    df_filtered[db_col] = ""

            stats = {"added": 0, "skipped": 0}
            with db_manager.get_connection(self.db_path) as conn:
                cursor = conn.cursor()
                for _, row in df_filtered.iterrows():
                    self._process_excel_row(cursor, row, stats, log)
                conn.commit()

            log(f"Importazione: {stats['added']} nuovi, {stats['skipped']} duplicati.")

            # Aggiorna lo stato di sincronizzazione
            SyncTracker.update_status(
                module="timbrature",
                added=stats["added"],
                removed=0,
                duration=0.0,  # La durata viene gestita meglio dal bot se necessario, qui mettiamo 0 per ora
            )

            return True
        return False

    def _process_excel_row(self, cursor, row, stats, log):
        try:
            # Data Normalization
            data_val = row.get("data")
            if pd.notna(data_val):
                if hasattr(data_val, "date") and callable(getattr(data_val, "date", None)):
                    # Explicitly strip time
                    with suppress(Exception):
                        date_func = data_val.date
                        row["data"] = date_func().isoformat()
                else:
                    with suppress(Exception):
                        # Attempt to parse and standardise with Italian format preference
                        dt = pd.to_datetime(data_val, dayfirst=True)
                        row["data"] = dt.date().isoformat()

            vals = row.fillna("").astype(str).to_dict()
            cursor.execute(
                """
                INSERT INTO timbrature (
                    id_dipendente, data, ingresso, uscita, fornitore,
                    codice_rilpres, numero_badge, nome, cognome, codice_fiscale,
                    codice_qualifica, specializzazione, societa_ospitante,
                    data_ins, presenza_ts, sito_timbratura
                )
                VALUES (
                    :id_dipendente, :data, :ingresso, :uscita, :fornitore,
                    :codice_rilpres, :numero_badge, :nome, :cognome, :codice_fiscale,
                    :codice_qualifica, :specializzazione, :societa_ospitante,
                    :data_ins, :presenza_ts, :sito_timbratura
                )
            """,
                vals,
            )
            stats["added"] += 1
        except sqlite3.IntegrityError:
            stats["skipped"] += 1
        except Exception as e:
            log(f"Errore riga: {e}")

    def get_lists(self) -> dict[str, list[str]]:
        """Recupera le liste configurate (Reparti, Cantieri) da config.json con migrazione automatica."""
        config = config_manager.load_config()

        # Logica di migrazione se mancano i dati nel config ma esiste il vecchio file
        if "reparti" not in config or (not config.get("reparti") and not config.get("cantieri")):
            old_path = self.db_path.parent / "timbrature_lists.json"
            if old_path.exists():
                with suppress(Exception):
                    import json

                    old_data = json.loads(old_path.read_text(encoding="utf-8"))
                    if isinstance(old_data, dict):
                        # Migrazione sicura
                        self.save_lists(old_data)
                        return cast("dict[str, list[str]]", old_data)

        return {
            "reparti": config.get("reparti", ["STRUMENTALE", "ELETTRICO", "CANTIERE", "ANALISI"]),
            "cantieri": config.get("cantieri", []),
        }

    def save_lists(self, data: dict[str, list[str]]):
        """Salva le liste configurate in config.json."""
        config_manager.set_config_value("reparti", data.get("reparti", []))
        config_manager.set_config_value("cantieri", data.get("cantieri", []))
