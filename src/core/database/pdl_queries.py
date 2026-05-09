"""
SyncroJob - PDL Queries
Query SQL centralizzate per il database PDL.
"""

import logging
import sqlite3
from pathlib import Path
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
            logger.error(f"Errore recupero richiedenti: {e}")  # noqa: TRY400
            return []

    @classmethod
    def save_programming_results(cls, results: list[dict[str, Any]], start_date: str, end_date: str) -> bool:
        """Salva i risultati della programmazione settimanale nel DB per la settimana specificata."""
        # Nota: start_date ed end_date sono stringhe DD/MM/YYYY
        if not results:
            try:
                query_del = "DELETE FROM pdl_programmazione WHERE settimana_start = ? AND settimana_end = ?"
                db_manager.execute_query(db_manager.DB_PDL, query_del, (start_date, end_date))
                return True  # noqa: TRY300
            except Exception as e:
                logger.error(f"Errore pulizia programmazione vuota: {e}")  # noqa: TRY400
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
                while len(row) < 19:  # noqa: PLR2004
                    row.append(False)

                # Aggiungi date
                row.extend([start_date, end_date])

                data_to_insert.append(tuple(row))

            with db_manager.get_connection(db_manager.DB_PDL) as conn:
                conn.executemany(query, data_to_insert)
            return True  # noqa: TRY300
        except Exception as e:
            logger.error(f"Errore salvataggio programmazione: {e}")  # noqa: TRY400
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
            return results  # noqa: TRY300
        except Exception as e:
            logger.error(f"Errore recupero programmazione: {e}")  # noqa: TRY400
            return []

    @classmethod
    def get_pdl_interventions(cls, n_pdl: str) -> list[dict[str, Any]]:
        """
        Recupera la cronologia degli interventi per un determinato PDL
        dal database dei Report Attivita'.
        """
        from src.core import config_manager  # noqa: PLC0415

        config = config_manager.load_config()
        # Path di default storico (Cerca in folder parallela se non configurato)
        # Nota: Idealmente l'utente lo configura nelle impostazioni.
        default_path = str(config_manager.BASE_DIR.parent / "report-attivita-app" / "report_attivita.db")
        ext_db_path = config.get("activity_db_path", default_path)

        if not ext_db_path or not Path(ext_db_path).exists():
            if ext_db_path != default_path and Path(default_path).exists():
                logger.warning(f"DB configurato non trovato ({ext_db_path}). Tento default: {default_path}")
                ext_db_path = default_path

            if not Path(ext_db_path).exists():
                logger.warning(f"Database esterno non trovato: {ext_db_path}")
                return []

        query = """
      SELECT
        'Report (Validato)' as fonte,
        data_riferimento_attivita as data,
        nome_tecnico as tecnico,
        '' as team,
        '' as ore_lavoro,
        testo_report as descrizione
      FROM report_interventi
      WHERE pdl = ?

      UNION ALL

      SELECT
        'Report (In Attesa)' as fonte,
        data_riferimento_attivita as data,
        nome_tecnico as tecnico,
        '' as team,
        '' as ore_lavoro,
        testo_report as descrizione
      FROM report_da_validare
      WHERE pdl = ?

      UNION ALL

      SELECT
        'Relazione' as fonte,
        data_intervento as data,
        nome_compilatore || ' ' || cognome_compilatore as tecnico,
        '' as team,
        '' as ore_lavoro,
        corpo_relazione as descrizione
      FROM relazioni
      WHERE pdl = ?

      ORDER BY data DESC
    """

        try:
            with sqlite3.connect(f"file:{ext_db_path}?mode=ro", uri=True) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, (n_pdl, n_pdl, n_pdl))
                rows = cursor.fetchall()

            return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Errore recupero cronologia interventi per PDL {n_pdl}: {e}")  # noqa: TRY400
            return []
