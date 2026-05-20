"""
Bot TS - Contabilita Queries
Gestisce tutte le query di lettura per i dati della Contabilità Strumentale.
Delegato al ContabilitaRepository per l'accesso ai dati.
"""

from pathlib import Path
from typing import Any

from src.core.database.repositories import ContabilitaRepository


class ContabilitaQueries:
    """Gestore per le query di lettura del database della Contabilità Strumentale."""

    _repo = ContabilitaRepository()

    # Indici Colonne Certificati (Allineati a get_certificati_campione_data)
    CERT_IDX_ID_STRUMENTO = 0
    CERT_IDX_CERTIFICATO = 1
    CERT_IDX_MODELLO = 2
    CERT_IDX_COSTRUTTORE = 3
    CERT_IDX_MATRICOLA = 4
    CERT_IDX_RANGE = 5
    CERT_IDX_ERRORE = 6
    CERT_IDX_EMISSIONE = 7
    CERT_IDX_SCADENZA = 8
    CERT_IDX_STATO = 9
    CERT_IDX_ANNOTAZIONI = 10
    CERT_IDX_UBICAZIONE = 11
    CERT_IDX_ID = 12

    @classmethod
    def get_available_years(cls, db_path: Path) -> list[int]:
        """Restituisce la lista degli anni presenti nel DB."""
        return cls._repo.get_available_years()

    @classmethod
    def get_data_by_year(cls, db_path: Path, year: int) -> list[tuple[Any, ...]]:
        """Restituisce i dati tabella Dati per un anno specifico."""
        # Restituiamo tuple per compatibilità con FastTableModel
        return cls._repo.get_data_by_year(year, as_objects=False)

    @classmethod
    def get_giornaliere_by_year(cls, db_path: Path, year: int) -> list[tuple[Any, ...]]:
        """Restituisce i dati Giornaliere per un anno specifico."""
        return cls._repo.get_giornaliere_by_year(year, as_objects=False)

    @classmethod
    def get_attivita_programmate_data(cls, db_path: Path) -> list[tuple[Any, ...]]:
        """Restituisce i dati Attività Programmate."""
        return cls._repo.get_attivita_programmate(as_objects=False)

    @classmethod
    def get_certificati_campione_data(cls, db_path: Path) -> list[tuple[Any, ...]]:
        """Restituisce i dati Certificati Campione."""
        return cls._repo.get_certificati_campione(as_objects=False)

    @classmethod
    def get_scarico_ore_data(cls, db_path: Path) -> list[tuple[Any, ...]]:
        """Restituisce tutti i dati della tabella scarico_ore."""
        return cls._repo.get_scarico_ore(as_objects=False)
