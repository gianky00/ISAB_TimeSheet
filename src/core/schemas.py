import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series


class DipendenteSchema(pa.DataFrameModel):
    """Schema di validazione per l'anagrafica dipendenti."""

    id_risorsa: Series[int] = pa.Field(coerce=True)
    Cognome: Series[str] = pa.Field(nullable=False)
    Nome: Series[str] = pa.Field(nullable=False)
    Data_nascita: Series[pd.Timestamp] = pa.Field(coerce=True)
    Badge: Series[str] = pa.Field(coerce=True)
    Data_assunzione: Series[pd.Timestamp] = pa.Field(coerce=True)

    class Config:
        strict = True
        coerce = True


class GiornaliereSchema(pa.DataFrameModel):
    """Schema di validazione per i file Giornaliera."""

    data: Series[pd.Timestamp] = pa.Field(coerce=True)
    personale: Series[str] = pa.Field(nullable=False)
    descrizione: Series[str] = pa.Field(nullable=True)
    tcl: Series[str] = pa.Field(coerce=True, nullable=True)
    odc: Series[str] = pa.Field(coerce=True, nullable=True)
    pdl: Series[str] = pa.Field(coerce=True, nullable=True)
    inizio: Series[str] = pa.Field(nullable=True)
    fine: Series[str] = pa.Field(nullable=True)
    ore: Series[float] = pa.Field(coerce=True)
    n_prev: Series[str] = pa.Field(coerce=True, nullable=True)

    class Config:
        coerce = True
        strict = False


class ContabilitaSchema(pa.DataFrameModel):
    """Schema di validazione per i file di Contabilità."""

    data_prev: Series[pd.Timestamp] = pa.Field(coerce=True, nullable=True)
    mese: Series[str] = pa.Field(nullable=True)
    n_prev: Series[str] = pa.Field(coerce=True, nullable=True)
    totale_prev: Series[float] = pa.Field(coerce=True, default=0.0)
    attivita: Series[str] = pa.Field(nullable=True)
    tcl: Series[str] = pa.Field(coerce=True, nullable=True)
    odc: Series[str] = pa.Field(coerce=True, nullable=True)
    stato_attivita: Series[str] = pa.Field(nullable=True)
    tipologia: Series[str] = pa.Field(nullable=True)
    ore_sp: Series[float] = pa.Field(coerce=True, default=0.0)
    resa: Series[float] = pa.Field(coerce=True, nullable=True)
    annotazioni: Series[str] = pa.Field(nullable=True)
    indirizzo_consuntivo: Series[str] = pa.Field(nullable=True)
    nome_file: Series[str] = pa.Field(nullable=True)

    class Config:
        coerce = True
        strict = False


def validate_dipendenti(df: pd.DataFrame) -> pd.DataFrame:
    """Valida un dataframe di dipendenti."""
    return DipendenteSchema.validate(df)


def validate_giornaliere(df: pd.DataFrame) -> pd.DataFrame:
    """Valida un dataframe di giornaliere."""
    return GiornaliereSchema.validate(df)


def validate_contabilita(df: pd.DataFrame) -> pd.DataFrame:
    """Valida un dataframe di contabilità."""
    return ContabilitaSchema.validate(df)
