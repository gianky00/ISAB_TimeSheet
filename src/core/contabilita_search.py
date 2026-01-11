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
                # Sanitizzazione semplice per FTS5 (evita errori se l'utente mette caratteri speciali)
                fts_query = f'"{query}*"' 
                
                try:
                    cursor.execute(sql_fts, (fts_query,))
                    rows = cursor.fetchall()
                except sqlite3.OperationalError:
                    rows = [] # Fallback al LIKE se FTS5 fallisce

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

                logging.debug(
                    f"[DEBUG] Search '{query}' found {len(rows)} matches"
                )

                for row in rows:
                    results.append(
                        {
                            "type": "ODA",
                            "codice_oda": row[0],
                            "descrizione": row[1] if row[1] else "Nessuna descrizione",
                            "odc": row[2],
                        }
                    )
        except Exception as e:
            logging.error(f"Search Error: {e}")

        return results

    @classmethod
    def search_extended(
        cls, db_path: Path, query: str, year: int = None, limit: int = 100
    ) -> Dict[str, List[Dict]]:
        """
        Ricerca estesa in tutti i moduli (Giornaliere, Scarico Ore, Certificati).
        Returns: Dict con liste di risultati per categoria.
        """
        if not db_path.exists():
            return {}
        query = query.strip().lower()
        if len(query) < 2:  # Relaxed limit
            return {}

        out: Dict[str, List[Dict]] = {
            "GIORNALIERE": [],
            "CANTIERE": [],
            "CERTIFICATI": [],
        }
        like_query = f"%{query}%"

        def _fmt_date(val):
            """Helper per formattare date ISO in IT."""
            try:
                if not val:
                    return ""
                dt = datetime.strptime(str(val).split()[0], "%Y-%m-%d")
                return dt.strftime("%d/%m/%Y")
            except Exception:
                return str(val)

        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()

                # Params list building
                g_params = [like_query, like_query]
                g_where_year = ""
                if year:
                    g_where_year = " AND data LIKE ?"
                    g_params.append(f"{year}-%")

                # 1. Giornaliere (Cerca Personale o Descrizione)
                sql_g = f"""SELECT DISTINCT data, personale, descrizione FROM giornaliere
                           WHERE (lower(personale) LIKE ? OR lower(descrizione) LIKE ?){g_where_year}
                           ORDER BY data DESC LIMIT ?"""
                g_params.append(limit)

                cursor.execute(sql_g, g_params)
                for r in cursor.fetchall():
                    out["GIORNALIERE"].append(
                        {
                            "data": _fmt_date(r[0]),
                            "personale": r[1],
                            "descrizione": r[2],
                        }
                    )

                # 2. Scarico Ore (Cantiere - Cerca Persone, Descrizione o Commessa)
                s_params = [like_query, like_query, like_query]
                s_where_year = ""
                if year:
                    s_where_year = " AND data LIKE ?"
                    s_params.append(f"{year}-%")

                sql_s = f"""SELECT DISTINCT data, pers1, descrizione, commessa, totale_ore FROM scarico_ore
                           WHERE (lower(pers1) LIKE ? OR lower(pers2) LIKE ? OR lower(descrizione) LIKE ?){s_where_year}
                           ORDER BY data DESC LIMIT ?"""
                s_params.append(limit)

                cursor.execute(sql_s, s_params)
                for r in cursor.fetchall():
                    out["CANTIERE"].append(
                        {
                            "data": _fmt_date(r[0]),
                            "personale": r[1],
                            "descrizione": r[2],
                            "commessa": r[3],
                            "totale_ore": r[4],
                        }
                    )

                # 3. Certificati (Cerca Matricola, Costruttore, Modello) - Year ignored for Certificati usually
                # But kept logic simple
                c_params = [like_query, like_query, like_query, limit]
                sql_c = """SELECT DISTINCT modello, costruttore, matricola FROM certificati_campione
                           WHERE lower(matricola) LIKE ? OR lower(modello) LIKE ? OR lower(costruttore) LIKE ? LIMIT ?"""
                cursor.execute(sql_c, c_params)
                for r in cursor.fetchall():
                    out["CERTIFICATI"].append(
                        {"modello": r[0], "costruttore": r[1], "matricola": r[2]}
                    )

        except Exception as e:
            logging.error(f"Extended Search Error: {e}")

        return out
