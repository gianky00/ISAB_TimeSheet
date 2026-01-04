"""
Bot TS - Contabilita Search
Gestisce le funzionalità di ricerca per i dati della Contabilità Strumentale.
"""
import sqlite3
from typing import List, Dict
from pathlib import Path
import logging
from datetime import datetime

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
        if len(query) < 2: return [] # Minimo 2 caratteri

        results = []
        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                # Cerca in Contabilità (n_prev = codice_oda, attivita = descrizione)
                sql = """
                    SELECT DISTINCT n_prev, attivita, odc 
                    FROM contabilita 
                    WHERE (lower(n_prev) LIKE ? OR lower(attivita) LIKE ? OR lower(odc) LIKE ?)
                    AND n_prev IS NOT NULL AND n_prev != ''
                    LIMIT 20
                """
                like_query = f"%{query}%"
                cursor.execute(sql, (like_query, like_query, like_query))
                
                rows = cursor.fetchall()
                logging.debug(f"[DEBUG] Search '{query}' found {len(rows)} matches in Contabilita")
                
                for row in rows:
                    results.append({
                        "type": "ODA",
                        "codice_oda": row[0],
                        "descrizione": row[1] if row[1] else "Nessuna descrizione",
                        "odc": row[2]
                    })
        except Exception as e:
            logging.error(f"Search Error: {e}")
            
        return results

    @classmethod
    def search_extended(cls, db_path: Path, query: str) -> Dict[str, List[Dict]]:
        """
        Ricerca estesa in tutti i moduli (Giornaliere, Scarico Ore, Certificati).
        Returns: Dict con liste di risultati per categoria.
        """
        if not db_path.exists(): return {}
        query = query.strip().lower()
        if len(query) < 3: return {} # More strict for generic search

        out = {"GIORNALIERE": [], "CANTIERE": [], "CERTIFICATI": []}
        like_query = f"%{query}%"

        def _fmt_date(val):
            """Helper per formattare date ISO in IT."""
            try:
                if not val: return ""
                dt = datetime.strptime(str(val).split()[0], "%Y-%m-%d")
                return dt.strftime("%d/%m/%Y")
            except: return str(val)

        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                cursor = conn.cursor()
                
                # 1. Giornaliere (Cerca Personale o Descrizione)
                sql_g = """SELECT DISTINCT data, personale, descrizione FROM giornaliere 
                           WHERE lower(personale) LIKE ? OR lower(descrizione) LIKE ? LIMIT 20"""
                cursor.execute(sql_g, (like_query, like_query))
                for r in cursor.fetchall():
                    out["GIORNALIERE"].append({"data": _fmt_date(r[0]), "personale": r[1], "descrizione": r[2]})

                # 2. Scarico Ore (Cantiere - Cerca Persone, Descrizione o Commessa)
                sql_s = """SELECT DISTINCT data, pers1, descrizione, commessa FROM scarico_ore 
                           WHERE lower(pers1) LIKE ? OR lower(pers2) LIKE ? OR lower(descrizione) LIKE ? LIMIT 20"""
                cursor.execute(sql_s, (like_query, like_query, like_query))
                for r in cursor.fetchall():
                    out["CANTIERE"].append({"data": _fmt_date(r[0]), "personale": r[1], "descrizione": r[2], "commessa": r[3]})

                # 3. Certificati (Cerca Matricola, Costruttore, Modello)
                sql_c = """SELECT DISTINCT modello, costruttore, matricola FROM certificati_campione 
                           WHERE lower(matricola) LIKE ? OR lower(modello) LIKE ? OR lower(costruttore) LIKE ? LIMIT 20"""
                cursor.execute(sql_c, (like_query, like_query, like_query))
                for r in cursor.fetchall():
                    out["CERTIFICATI"].append({"modello": r[0], "costruttore": r[1], "matricola": r[2]})
                    
        except Exception as e:
            logging.error(f"Extended Search Error: {e}")
            
        return out
