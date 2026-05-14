"""
SyncroJob - PDL Queries
Query SQL centralizzate per il database PDL.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Any

from src.core import config_manager

logger = logging.getLogger(__name__)


from src.core.database.repositories import PdlRepository
from src.models import PdlProgrammazioneRecord


class PDLQueries:
    """Gestore per le query del database PDL."""

    _repo = PdlRepository()

    @classmethod
    def get_unique_requesters(cls) -> list[str]:
        """Restituisce la lista univoca normalizzata dei richiedenti presenti nel DB."""
        return cls._repo.get_unique_requesters()

    @classmethod
    def save_programming_results(cls, results: list[dict[str, Any]], start_date: str, end_date: str) -> bool:
        """Salva i risultati della programmazione settimanale delegando al repository."""
        records = []
        for r in results:
            prog = r.get("programmazione", [])
            # Convertiamo il dizionario complesso in un record piatto
            data = {
                "id": None,
                "richiedente": r.get("richiedente"),
                "n_pdl": r.get("pdl"),
                "area": r.get("area"),
                "unita": r.get("unita", ""),
                "descrizione": r.get("descrizione"),
                "settimana_start": start_date,
                "settimana_end": end_date,
            }
            # Mappatura giorni
            giorni = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]
            for i, day_name in enumerate(giorni):
                # Cerchiamo il giorno corrispondente o usiamo default False
                day_data = next((d for d in prog if d.get("giorno") == i + 1), {"tcl": False, "tgo": False})
                data[f"{day_name}_tcl"] = day_data.get("tcl", False)
                data[f"{day_name}_tgo"] = day_data.get("tgo", False)

            records.append(PdlProgrammazioneRecord(**data))

        return cls._repo.save_programming(records, start_date, end_date)

    @classmethod
    def get_programming_results_by_week(cls, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """Recupera la programmazione settimanale riconvertendo i record in dizionari legacy."""
        records = cls._repo.get_programming_by_week(start_date, end_date)
        results = []
        for r in records:
            results.append({
                "richiedente": r.richiedente,
                "pdl": r.n_pdl,
                "area": r.area,
                "unita": r.unita,
                "descrizione": r.descrizione,
                "ultimo_aggiornamento": r.ultimo_aggiornamento,
                "programmazione": [
                    {"giorno": 1, "tcl": r.lun_tcl, "tgo": r.lun_tgo},
                    {"giorno": 2, "tcl": r.mar_tcl, "tgo": r.mar_tgo},
                    {"giorno": 3, "tcl": r.mer_tcl, "tgo": r.mer_tgo},
                    {"giorno": 4, "tcl": r.gio_tcl, "tgo": r.gio_tgo},
                    {"giorno": 5, "tcl": r.ven_tcl, "tgo": r.ven_tgo},
                    {"giorno": 6, "tcl": r.sab_tcl, "tgo": r.sab_tgo},
                    {"giorno": 7, "tcl": r.dom_tcl, "tgo": r.dom_tgo},
                ],
            })
        return results

    @classmethod
    def get_pdl_interventions(cls, n_pdl: str) -> list[dict[str, Any]]:
        """
        dal database dei Report Attività.
        """

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
        'Relazionè as fonte,
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
        except Exception:
            logger.exception(f"Errore recuperòcronologiàinterventi per PDL {n_pdl}")
            return []
