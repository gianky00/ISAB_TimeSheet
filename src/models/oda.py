from dataclasses import dataclass


@dataclass
class OdaRecord:
    """Modello per un record di Ordine di Acquisto (Storico OdA)."""
    org_acq: str
    data_oda: str
    oda: str
    pos_oda: str
    stato: str
    cat_contab: str
    descrizione: str
    qta: float
    uom: str
    data_consegna: str
    valore_netto_pos: float
    valore_residuo: float
    valore_netto_oda: float
    divisione: str
    destinatario: str
    nome_destinatario: str
    codice_fornitore: str
    descrizione_fornitore: str
    emittente_fattura: str
    desc_emittente_fattura: str
    contract_card: str
    contratto: str
    posizione_contratto: str
    gruppo_acquisti: str
    indicatore_rilascio: str
    stato_rilascio: str
    attivita: str
    num_riga: str
    quantita: float
    unita_mis: str
    prezzo_lordo: float
    testo_breve: str
    id: int | None = None
