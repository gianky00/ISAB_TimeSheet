"""
SyncroJob - PDL DTO
Oggetti di trasporto dati per il modulo PDL.
Garantisce l'incapsulamento e previene la data leakage verso la GUI.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class PdlRowDTO:
    """Rappresenta una riga completa del database PDL."""

    id: int
    n_pdl: str
    data_creazione: str
    area: str
    unita: str
    ditta: str
    descrizione: str
    tipologia: str
    stato: str
    apparecchiatura: str
    richiedente: str
    data_richiesta: str
    emittente: str
    data_emissione: str
    aprente: str
    data_apertura: str
    priorita: str
    contratto: str
    ordine: str
    sito: str
    importato_il: str

    # Metadati extra per la GUI (opzionali)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_db_row(cls, r: tuple[Any, ...]) -> "PdlRowDTO":
        """Factory method per creare un DTO da una riga grezza del DB."""
        return cls(
            id=int(r[0]),
            n_pdl=str(r[1]),
            data_creazione=str(r[2]),
            area=str(r[3]),
            unita=str(r[4]),
            ditta=str(r[5]),
            descrizione=str(r[6]),
            tipologia=str(r[7]),
            stato=str(r[8]),
            apparecchiatura=str(r[9]),
            richiedente=str(r[10]),
            data_richiesta=str(r[11]),
            emittente=str(r[12]),
            data_emissione=str(r[13]),
            aprente=str(r[14]),
            data_apertura=str(r[15]),
            priorita=str(r[16]),
            contratto=str(r[17]),
            ordine=str(r[18]),
            sito=str(r[19]),
            importato_il=str(r[20]),
        )

    def to_master_list(self) -> list[str]:
        """Restituisce i campiu'formattati per la tabella master della GUI."""
        raw = [
            self.data_creazione,
            self.richiedente,
            self.n_pdl,
            self.area,
            self.unita,
            self.stato,
            self.descrizione,
        ]
        return [("" if val.lower() in ("nan", "none") else val) for val in raw]

    def to_full_list(self) -> list[str | int]:
        """Restituisce tutti i campiu'come lista (per compatibilit  legacy se necessaria)."""
        return [
            self.id,
            self.n_pdl,
            self.data_creazione,
            self.area,
            self.unita,
            self.ditta,
            self.descrizione,
            self.tipologia,
            self.stato,
            self.apparecchiatura,
            self.richiedente,
            self.data_richiesta,
            self.emittente,
            self.data_emissione,
            self.aprente,
            self.data_apertura,
            self.priorita,
            self.contratto,
            self.ordine,
            self.sito,
            self.importato_il,
        ]
