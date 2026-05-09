"""
Bot TS - Contabilita Search
Gestisce le funzionalita' di ricerca per i dati della Contabilit  Strumentale.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Any

from src.core.database import db_manager

logger = logging.getLogger(__name__)


class ContabilitaSearch:
    """Gestore per le funzionalita' di ricerca nel database della Contabilit  Strumentale."""

    @classmethod
    def search_oda(cls, db_path: Path, query: str) -> list[dict[str, Any]]:
        """
        Cerca OdA per codice, descrizione o ODC.
        Returns:
          List[Dict]: Lista di risultati [{'codice_oda': '...', 'descrizione': '...'}, ...]
        """
        if not db_path.exists():
            logger.debug("[DEBUG] DB Contabilit  non trovato")
            return []

        query = query.strip().lower()
        if len(query) < 2:  # noqa: PLR2004
            return []  # Minimo 2 caratteri

        results: list[dict[str, Any]] = []
        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()

                # Tentativo con FTS5 (molto piu' veloce)
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

                logger.debug(f"[DEBUG] Search '{query}' found {len(rows)} matches")

                results.extend(
                    {
                        "type": "ODA",
                        "codice_oda": row[0],
                        "descrizione": row[1] or "Nessuna descrizione",
                        "odc": row[2],
                    }
                    for row in rows
                )
        except Exception as e:
            logger.error(f"Search Error: {e}")  # noqa: TRY400

        return results

    @classmethod
    def search_extended(
        cls, db_path: Path, query: str, year: int | None = None, limit: int = 100
    ) -> dict[str, list[dict[str, Any]]]:
        """Ricerca estesa in tutti i moduli (Giornaliere, Scarico Ore, Certificati)."""
        if not db_path.exists() or len(query.strip()) < 2:  # noqa: PLR2004
            return {}

        query = query.strip().lower()
        out: dict[str, list[dict[str, Any]]] = {
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
            logger.error(f"Extended Search Error: {e}")  # noqa: TRY400

        return out

    @staticmethod
    def _fmt_date(val: Any) -> str:
        """Helper per formattazione date ISO in IT."""
        try:
            if not val:
                return ""
            parts = str(val).split()[0].split("-")
            # Verifica che sia un formato YYYY-MM-DD plausibile
            if len(parts) == 3 and len(parts[0]) == 4 and parts[0].isdigit():  # noqa: PLR2004
                return f"{parts[2]}/{parts[1]}/{parts[0]}"
            return str(val)
        except Exception:
            return str(val)

    @classmethod
    def _search_giornaliere(
        cls, cursor: sqlite3.Cursor, query: str, year: int | None, limit: int
    ) -> list[dict[str, Any]]:
        """Esegue la ricerca specifica nelle timbrature giornaliere."""
        like = f"%{query}%"
        params: list[Any] = [like, like]
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
            {"data": cls._fmt_date(r[0]), "personale": r[1], "descrizione": r[2]} for r in cursor.fetchall()
        ]

    @classmethod
    def _search_scarico_ore(
        cls, cursor: sqlite3.Cursor, query: str, year: int | None, limit: int
    ) -> list[dict[str, Any]]:
        """Esegue la ricerca specifica nello scarico ore (cantiere)."""
        like = f"%{query}%"
        params: list[Any] = [like, like, like]
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
    def _search_certificati(cls, cursor: sqlite3.Cursor, query: str, limit: int) -> list[dict[str, Any]]:
        """Esegue la ricerca specifica nei certificati campione."""
        like = f"%{query}%"
        sql = """SELECT modello, costruttore, matricola FROM certificati_campione
         WHERE lower(matricola) LIKE ? OR lower(modello) LIKE ? OR lower(costruttore) LIKE ? LIMIT ?"""
        cursor.execute(sql, [like, like, like, limit])
        return [{"modello": r[0], "costruttore": r[1], "matricola": r[2]} for r in cursor.fetchall()]
