"""SyncroJob - PDL Service.

Gestione della logica di business e delle query per i Permessi di Lavoro (PDL).
Delegato al PdlRepository per l'accesso ai dati.
"""

import logging
from pathlib import Path
from typing import Any

from src.application.services import config_manager
from src.application.services.database.repositories import PdlRepository
from src.domain import PdlProgrammazioneRecord

logger = logging.getLogger(__name__)


class PDLService:
    """Servizio per la gestione dei dati e delle operazioni sui PDL.

    Inizializza il servizio con un repository iniettato o predefinito.
    """

    def __init__(self, repo: PdlRepository | None = None) -> None:
        self._repo = repo or PdlRepository()

    @staticmethod
    def _get_default_repo() -> PdlRepository:
        """Restituisce l'istanza predefinita del repository."""
        return PdlRepository()

    @classmethod
    def get_unique_requesters(cls) -> list[str]:
        """Restituisce la lista univoca normalizzata dei richiedenti presenti nel DB."""
        return cls._get_default_repo().get_unique_requesters()

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

        return cls._get_default_repo().save_programming(records, start_date, end_date)

    @classmethod
    def get_programming_results_by_week(cls, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """Recupera la programmazione settimanale riconvertendo i record in dizionari legacy."""
        records = cls._get_default_repo().get_programming_by_week(start_date, end_date)
        return [
            {
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
            }
            for r in records
        ]

    @classmethod
    def get_pdl_interventions(cls, n_pdl: str) -> list[dict[str, Any]]:
        """Recupera la cronologia interventi delegando al repository."""
        config = config_manager.load_config()
        # Path di default storico
        default_path = str(config_manager.BASE_DIR.parent / "report-attivita-app" / "report_attivita.db")
        ext_db_path = config.get("activity_db_path", default_path)

        if not ext_db_path or not Path(ext_db_path).exists():
            if ext_db_path != default_path and Path(default_path).exists():
                logger.warning(f"DB configurato non trovato ({ext_db_path}). Tento default: {default_path}")
                ext_db_path = default_path

            if not Path(ext_db_path).exists():
                logger.warning(f"Database esterno non trovato: {ext_db_path}")
                return []

        return cls._get_default_repo().get_interventions(n_pdl, ext_db_path)
