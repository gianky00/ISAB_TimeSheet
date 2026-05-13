from dataclasses import dataclass


@dataclass
class ContabilitaRecord:
    """Modello per un record di Contabilità Strumentale (Preventivi)."""
    data_prev: str | None
    mese: str | None
    n_prev: str | None
    totale_prev: float
    attivita: str | None
    tcl: str | None
    odc: str | None
    stato_attivita: str | None
    tipologia: str | None
    ore_sp: float
    resa: str | None
    annotazioni: str | None
    indirizzo_consuntivo: str | None
    nome_file: str | None
    year: int = 0
    id: int | None = None


@dataclass
class GiornalieraRecord:
    """Modello per un record di Giornaliera."""
    data: str
    personale: str
    tcl: str
    descrizione: str
    n_prev: str
    odc: str
    pdl: str
    inizio: str
    fine: str
    ore: float
    nome_file: str
    year: int = 0
    id: int | None = None


@dataclass
class AttivitaProgrammataRecord:
    """Modello per un'attività programmata."""
    n_prev: str
    odc: str
    descrizione: str
    data_inizio: str
    data_fine: str
    stato: str
    id: int | None = None


@dataclass
class CertificatoCampioneRecord:
    """Modello per un certificato campione."""
    id_strumento: str
    certificato: str
    modello: str
    costruttore: str
    matricola: str
    range: str
    errore: str
    emissione: str
    scadenza: str
    stato: str
    annotazioni: str | None = None
    ubicazione: str | None = None
    id: int | None = None
