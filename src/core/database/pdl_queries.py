"""
SyncroJob - PDL Queries
Query SQL centralizzate per il database PDL.
"""

import logging
from typing import Any

from src.core.database import db_manager

logger = logging.getLogger(__name__)


class PDLQueries:
    """Gestore per le query del database PDL."""

    @classmethod
    def get_unique_requesters(cls) -> list[str]:
        """Restituisce la lista univoca normalizzata dei richiedenti presenti nel DB."""
        # Recuperiamo i nomi grezzi
        query = "SELECT DISTINCT richiedente FROM pdl WHERE richiedente IS NOT NULL AND richiedente != ''"
        try:
            rows = db_manager.execute_query(db_manager.DB_PDL, query)
            # Normalizzazione Python: collassa spazi multipli interni, trim e title case
            clean_names = set()
            for r in rows:
                if r[0]:
                    # split() senza argomenti collassa qualsiasi whitespace (\s+)
                    normalized = " ".join(str(r[0]).split()).title()
                    clean_names.add(normalized)
            
            return sorted(list(clean_names))
        except Exception as e:
            logger.error(f"Errore recupero richiedenti: {e}")
            return []

    @classmethod
    def get_pdl_created_in_range(cls, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """
        Restituisce i PDL creati in un intervallo di date.
        Date in formato DD/MM/YYYY.
        """
        # SQLite non ha un tipo DATE, usiamo manipolazione stringhe se il formato è DD/MM/YYYY HH:MM:SS
        # Oppure convertiamo in formato comparabile YYYYMMDD
        query = """
            SELECT n_pdl, data_creazione, richiedente, area, descrizione_lavoro, stato 
            FROM pdl 
            WHERE substr(data_creazione, 7, 4) || substr(data_creazione, 4, 2) || substr(data_creazione, 1, 2) 
            BETWEEN ? AND ?
        """
        # Converti DD/MM/YYYY -> YYYYMMDD
        def to_iso(d):
            parts = d.split('/')
            return f"{parts[2]}{parts[1]}{parts[0]}"

        params = (to_iso(start_date), to_iso(end_date))
        
        try:
            rows = db_manager.execute_query(db_manager.DB_PDL, query, params)
            return [
                {
                    "n_pdl": r[0],
                    "data_creazione": r[1],
                    "richiedente": r[2],
                    "area": r[3],
                    "descrizione": r[4],
                    "stato": r[5]
                }
                for r in rows
            ]
        except Exception as e:
            logger.error(f"Errore recupero PDL in range: {e}")
            return []

    @classmethod
    def save_programming_results(cls, results: list[dict[str, Any]]) -> bool:
        """Salva i risultati della programmazione settimanale nel DB."""
        if not results:
            return True
            
        try:
            # Svuotiamo la tabella precedente prima di salvare i nuovi risultati
            # (Per mantenere solo l'ultimo controllo fresco)
            db_manager.execute_query(db_manager.DB_PDL, "DELETE FROM pdl_programmazione")
            
            query = """
                INSERT INTO pdl_programmazione (
                    richiedente, n_pdl, area, descrizione,
                    lun_tcl, lun_tgo, mar_tcl, mar_tgo, mer_tcl, mer_tgo,
                    gio_tcl, gio_tgo, ven_tcl, ven_tgo, sab_tcl, sab_tgo, dom_tcl, dom_tgo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            data_to_insert = []
            for r in results:
                prog = r.get("programmazione", [])
                # Mapping giorni (assumiamo siano ordinati 1-7)
                row = [
                    r.get("richiedente"), r.get("pdl"), r.get("area"), r.get("descrizione")
                ]
                # Aggiungiamo i 14 flag (TCL/TGO per 7 giorni)
                for day in prog:
                    row.extend([day["tcl"], day["tgo"]])
                
                # Riempimento se mancano giorni (safety)
                while len(row) < 18:
                    row.append(False)
                    
                data_to_insert.append(tuple(row))
            
            with db_manager.get_connection(db_manager.DB_PDL) as conn:
                conn.executemany(query, data_to_insert)
            return True
        except Exception as e:
            logger.error(f"Errore salvataggio programmazione: {e}")
            return False

    @classmethod
    def get_last_programming_results(cls) -> list[dict[str, Any]]:
        """Recupera l'ultimo controllo di programmazione salvato."""
        query = "SELECT * FROM pdl_programmazione ORDER BY id ASC"
        try:
            rows = db_manager.execute_query(db_manager.DB_PDL, query)
            results = []
            for r in rows:
                results.append({
                    "richiedente": r[1],
                    "pdl": r[2],
                    "area": r[3],
                    "descrizione": r[4],
                    "programmazione": [
                        {"giorno": 1, "tcl": bool(r[5]), "tgo": bool(r[6])},
                        {"giorno": 2, "tcl": bool(r[7]), "tgo": bool(r[8])},
                        {"giorno": 3, "tcl": bool(r[9]), "tgo": bool(r[10])},
                        {"giorno": 4, "tcl": bool(r[11]), "tgo": bool(r[12])},
                        {"giorno": 5, "tcl": bool(r[13]), "tgo": bool(r[14])},
                        {"giorno": 6, "tcl": bool(r[15]), "tgo": bool(r[16])},
                        {"giorno": 7, "tcl": bool(r[17]), "tgo": bool(r[18])},
                    ]
                })
            return results
        except Exception as e:
            logger.error(f"Errore recupero programmazione: {e}")
            return []
