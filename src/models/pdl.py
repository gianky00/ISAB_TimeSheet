from dataclasses import dataclass


@dataclass
class PdlRecord:
    """Modello per un record di Permesso di Lavoro (PDL)."""

    id: int | None
    n_pdl: str
    data_creazione: str
    area: str
    unita: str
    ditta: str
    descrizione_lavoro: str
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


@dataclass
class PdlProgrammazioneRecord:
    """Modello per un record di programmazione PDL settimanale."""

    id: int | None
    richiedente: str
    n_pdl: str
    area: str
    unita: str
    descrizione: str
    lun_tcl: bool
    lun_tgo: bool
    mar_tcl: bool
    mar_tgo: bool
    mer_tcl: bool
    mer_tgo: bool
    gio_tcl: bool
    gio_tgo: bool
    ven_tcl: bool
    ven_tgo: bool
    sab_tcl: bool
    sab_tgo: bool
    dom_tcl: bool
    dom_tgo: bool
    settimana_start: str
    settimana_end: str
    ultimo_aggiornamento: str | None = None
