"""
Bot TS - Contabilita Search
Gestisce le funzionalità di ricerca per i dati della Contabilità Strumentale.
"""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from src.core.database import db_manager


class ContabilitaSearch:
    """Gestore per le funzionalità di ricerca nel database della Contabilità Strumentale."""

    @classmethod
    def search_oda(cls, db_path: Path, query: str) -> List[Dict]:
        """
        Cerca OdA per codice, descrizione o ODC.
        Returns:
            List[Dict]: Lista di risultati [{'codice_oda': '...', 'descrizione': '...'}, ...]
        """
        if not db_path.exists():
            logging.debug("[DEBUG] DB Contabilità non trovato")
            return []

        query = query.strip().lower()
        if len(query) < 2:
            return []  # Minimo 2 caratteri

        results = []
        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()

                # Tentativo con FTS5 (molto più veloce)
                sql_fts = """
                    SELECT n_prev, attivita, odc
                    FROM contabilita_fts
                    WHERE contabilita_fts MATCH ?
                    LIMIT 20
                """
                # Sanitizzazione semplice per FTS5
                fts_query = f'"{query}*"'

                try:
                    cursor.execute(sql_fts, (fts_query,))
                    rows = cursor.fetchall()
                except sqlite3.OperationalError:
                    rows = []  # Fallback al LIKE se FTS5 fallisce

                # Se FTS5 non trova nulla o fallisce, usiamo LIKE come fallback
                if not rows:
                    sql_like = """
                        SELECT DISTINCT n_prev, attivita, odc
                        FROM contabilita
                        WHERE (lower(n_prev) LIKE ? OR lower(attivita) LIKE ? OR lower(odc) LIKE ?)
                        AND n_prev IS NOT NULL AND n_prev != ''
                        LIMIT 20
                    """
                    like_query = f"%{query}%"
                    cursor.execute(sql_like, (like_query, like_query, like_query))
                    rows = cursor.fetchall()

                logging.debug(f"[DEBUG] Search '{query}' found {len(rows)} matches")

                for row in rows:
                    results.append(
                        {
                            "type": "ODA",
                            "codice_oda": row[0],
                            "descrizione": row[1] or "Nessuna descrizione",
                            "odc": row[2],
                        }
                    )
        except Exception as e:
            logging.error(f"Search Error: {e}")

        return results

    @classmethod
    def search_extended(
        cls, db_path: Path, query: str, year: int | None = None, limit: int = 100
    ) -> Dict[str, List[Dict]]:
        """Ricerca estesa in tutti i moduli (Giornaliere, Scarico Ore, Certificati)."""
        if not db_path.exists() or len(query.strip()) < 2:
            return {}

        query = query.strip().lower()
        out: Dict[str, List[Dict]] = {
            "GIORNALIERE": [],
            "CANTIERE": [],
            "CERTIFICATI": [],
        }

        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()

                # 1. Giornaliere
                out["GIORNALIERE"] = cls._search_giornaliere(cursor, query, year, limit)
                # 2. Scarico Ore (Cantiere)
                out["CANTIERE"] = cls._search_scarico_ore(cursor, query, year, limit)
                # 3. Certificati
                out["CERTIFICATI"] = cls._search_certificati(cursor, query, limit)

        except Exception as e:
            logging.error(f"Extended Search Error: {e}")

        return out

    @staticmethod
    def _fmt_date(val):
        """Helper per formattare date ISO in IT."""
        try:
            if not val:
                return ""
            dt = datetime.strptime(str(val).split()[0], "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except Exception:
            return str(val)

    @classmethod
    def _search_giornaliere(cls, cursor, query, year, limit) -> List[Dict]:
        """Esegue la ricerca specifica nelle timbrature giornaliere."""
        like = f"%{query}%"
        params = [like, like]
        where = ""
        if year:
            where = " AND data LIKE ?"
            params.append(f"{year}-%")

        sql = f"""SELECT data, personale, descrizione FROM giornaliere
                  WHERE (lower(personale) LIKE ? OR lower(descrizione) LIKE ?){where}
                  ORDER BY data DESC LIMIT ?"""  # nosec B608
        params.append(limit)
        cursor.execute(sql, params)
        return [
            {"data": cls._fmt_date(r[0]), "personale": r[1], "descrizione": r[2]}
            for r in cursor.fetchall()
        ]

    @classmethod
    def _search_scarico_ore(cls, cursor, query, year, limit) -> List[Dict]:
        """Esegue la ricerca specifica nello scarico ore (cantiere)."""
        like = f"%{query}%"
        params = [like, like, like]
        where = ""
        if year:
            where = " AND data LIKE ?"
            params.append(f"{year}-%")

        sql = f"""SELECT data, pers1, descrizione, commessa, totale_ore FROM scarico_ore
                  WHERE (lower(pers1) LIKE ? OR lower(pers2) LIKE ? OR lower(descrizione) LIKE ?){where}
                  ORDER BY data DESC LIMIT ?"""  # nosec B608
        params.append(limit)
        cursor.execute(sql, params)
        return [
            {
                "data": cls._fmt_date(r[0]),
                "personale": r[1],
                "descrizione": r[2],
                "commessa": r[3],
                "totale_ore": r[4],
            }
            for r in cursor.fetchall()
        ]

    @classmethod
    def _search_certificati(cls, cursor, query, limit) -> List[Dict]:
        """Esegue la ricerca specifica nei certificati campione."""
        like = f"%{query}%"
        sql = """SELECT modello, costruttore, matricola FROM certificati_campione
                 WHERE lower(matricola) LIKE ? OR lower(modello) LIKE ? OR lower(costruttore) LIKE ? LIMIT ?"""
        cursor.execute(sql, [like, like, like, limit])
        return [
            {"modello": r[0], "costruttore": r[1], "matricola": r[2]}
            for r in cursor.fetchall()
        ]
