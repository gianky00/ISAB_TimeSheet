"""
SyncroJob - PDL Queries
Query SQL centralizzate per il database PDL.
"""

import logging
import sqlite3
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

            return sorted(clean_names)
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
            parts = d.split("/")
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
                    "stato": r[5],
                }
                for r in rows
            ]
        except Exception as e:
            logger.error(f"Errore recupero PDL in range: {e}")
            return []

    @classmethod
    def save_programming_results(cls, results: list[dict[str, Any]], start_date: str, end_date: str) -> bool:
        """Salva i risultati della programmazione settimanale nel DB per la settimana specificata."""
        # Nota: start_date ed end_date sono stringhe DD/MM/YYYY
        if not results:
            # Se lista vuota, potremmo voler cancellare i dati vecchi di quella settimana?
            # Per ora manteniamo logica esistente ma cancelliamo la settimana
            try:
                query_del = "DELETE FROM pdl_programmazione WHERE settimana_start = ? AND settimana_end = ?"
                db_manager.execute_query(db_manager.DB_PDL, query_del, (start_date, end_date))
                return True
            except Exception as e:
                logger.error(f"Errore pulizia programmazione vuota: {e}")
                return False

        try:
            # 1. Cancelliamo solo la settimana corrente
            query_del = "DELETE FROM pdl_programmazione WHERE settimana_start = ? AND settimana_end = ?"
            db_manager.execute_query(db_manager.DB_PDL, query_del, (start_date, end_date))

            query = """
                INSERT INTO pdl_programmazione (
                    richiedente, n_pdl, area, unita, descrizione,
                    lun_tcl, lun_tgo, mar_tcl, mar_tgo, mer_tcl, mer_tgo,
                    gio_tcl, gio_tgo, ven_tcl, ven_tgo, sab_tcl, sab_tgo, dom_tcl, dom_tgo,
                    settimana_start, settimana_end
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            data_to_insert = []
            for r in results:
                prog = r.get("programmazione", [])
                # Mapping giorni (assumiamo siano ordinati 1-7)
                row = [
                    r.get("richiedente"),
                    r.get("pdl"),
                    r.get("area"),
                    r.get("unita"),
                    r.get("descrizione"),
                ]
                # Aggiungiamo i 14 flag (TCL/TGO per 7 giorni)
                for day in prog:
                    row.extend([day["tcl"], day["tgo"]])

                # Riempimento se mancano giorni (safety)
                while len(row) < 19:
                    row.append(False)

                # Aggiungi date
                row.extend([start_date, end_date])

                data_to_insert.append(tuple(row))

            with db_manager.get_connection(db_manager.DB_PDL) as conn:
                conn.executemany(query, data_to_insert)
            return True
        except Exception as e:
            logger.error(f"Errore salvataggio programmazione: {e}")
            return False

    @classmethod
    def get_programming_results_by_week(cls, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """Recupera il controllo di programmazione per la settimana specifica."""
        query = (
            "SELECT * FROM pdl_programmazione WHERE settimana_start = ? AND settimana_end = ? ORDER BY id ASC"
        )
        try:
            # Recuperiamo nomi colonne per sicurezza visto l'evoluzione dello schema
            with db_manager.get_connection(db_manager.DB_PDL) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, (start_date, end_date))
                rows = cursor.fetchall()

            results = []
            for r in rows:
                row_dict = dict(r)
                results.append(
                    {
                        "richiedente": row_dict["richiedente"],
                        "pdl": row_dict["n_pdl"],
                        "area": row_dict["area"],
                        "unita": row_dict.get("unita", ""),  # Ora sicuro grazie a dict()
                        "descrizione": row_dict["descrizione"],
                        "ultimo_aggiornamento": row_dict["ultimo_aggiornamento"],
                        "programmazione": [
                            {"giorno": 1, "tcl": bool(row_dict["lun_tcl"]), "tgo": bool(row_dict["lun_tgo"])},
                            {"giorno": 2, "tcl": bool(row_dict["mar_tcl"]), "tgo": bool(row_dict["mar_tgo"])},
                            {"giorno": 3, "tcl": bool(row_dict["mer_tcl"]), "tgo": bool(row_dict["mer_tgo"])},
                            {"giorno": 4, "tcl": bool(row_dict["gio_tcl"]), "tgo": bool(row_dict["gio_tgo"])},
                            {"giorno": 5, "tcl": bool(row_dict["ven_tcl"]), "tgo": bool(row_dict["ven_tgo"])},
                            {"giorno": 6, "tcl": bool(row_dict["sab_tcl"]), "tgo": bool(row_dict["sab_tgo"])},
                            {"giorno": 7, "tcl": bool(row_dict["dom_tcl"]), "tgo": bool(row_dict["dom_tgo"])},
                        ],
                    }
                )
            return results
        except Exception as e:
            logger.error(f"Errore recupero programmazione: {e}")
            return []
