"""SyncroJob - Consuntivo DTO.

Oggetti di trasporto dati per il modulo Consuntivi.
Garantisce l'incapsulamento e la separazione CORE-GUI.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConsuntivoDataDTO:
    """struttura dati per la generazione di un nuovo consuntivo."""

    progressivo: str
    anno_short: str
    data: str
    tcl: str
    odc: str
    avviso: str
    ordine: str
    stato_attivita: str
    tipologia_preventivo: str
    tipologia_economia: str
    descrizione_lavoro: str
    descrizione_relazione: str

    def to_dict(self) -> dict[str, str]:
        """Converte il DTO in un dizionario per i worker legacy."""
        return {
            "progressivo": self.progressivo,
            "anno_short": self.anno_short,
            "data": self.data,
            "tcl": self.tcl,
            "odc": self.odc,
            "avviso": self.avviso,
            "ordine": self.ordine,
            "stato_attivita": self.stato_attivita,
            "tipologia_preventivo": self.tipologia_preventivo,
            "tipologia_economia": self.tipologia_economia,
            "descrizione_lavoro": self.descrizione_lavoro,
            "descrizione_relazione": self.descrizione_relazione,
        }
