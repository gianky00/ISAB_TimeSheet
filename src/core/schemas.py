"""Modulo Schemas."""

from dataclasses import dataclass
from typing import Any

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series


@dataclass
class ROIMetrics:
    """Modello dati per le metriche di ritorno sull'investimento."""

    total_minutes_saved: float
    net_minutes_saved: float
    total_operations: int
    success_rate: float
    reliability_score: int
    total_days: int
    trend_percentage: float
    top_task_name: str
    top_task_pct: float
    top_tasks: list[tuple[str, float]]


@dataclass
class PDLMetrics:
    """Modello dati per le metriche dei Permessi di Lavoro."""

    total_count: int
    active_count: int
    expired_count: int
    warning_count: int
    last_sync: str
    trend_percentage: float
    weekly_trend_percentage: float
    areas_stats: list[Any]


class DipendenteSchema(pa.DataFrameModel):
    """Schema di validazione per l'anagrafica dipendenti."""

    id_risorsa: Series[int] = pa.Field(coerce=True)
    Cognome: Series[str] = pa.Field(nullable=False)
    Nome: Series[str] = pa.Field(nullable=False)
    Data_nascita: Series[pd.Timestamp] = pa.Field(coerce=True)
    Badge: Series[str] = pa.Field(coerce=True)
    Data_assunzione: Series[pd.Timestamp] = pa.Field(coerce=True)

    class Config:
        """Configurazione per la validazione dello schema."""

        strict = False
        coerce = True


class GiornaliereSchema(pa.DataFrameModel):
    """Schema di validazione per i file Giornaliera."""

    data: Series[pd.Timestamp] = pa.Field(coerce=True, nullable=True)
    personale: Series[str] = pa.Field(nullable=True)
    descrizione: Series[str] = pa.Field(nullable=True)
    tcl: Series[str] = pa.Field(coerce=True, nullable=True)
    odc: Series[str] = pa.Field(coerce=True, nullable=True)
    pdl: Series[str] = pa.Field(coerce=True, nullable=True)
    inizio: Series[str] = pa.Field(nullable=True)
    fine: Series[str] = pa.Field(nullable=True)
    ore: Series[float] = pa.Field(coerce=True, nullable=True)
    n_prev: Series[str] = pa.Field(coerce=True, nullable=True)

    class Config:
        """Configurazione per la validazione dello schema."""

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
    resa: Series[str] = pa.Field(coerce=True, nullable=True)
    annotazioni: Series[str] = pa.Field(nullable=True)
    indirizzo_consuntivo: Series[str] = pa.Field(nullable=True)
    nome_file: Series[str] = pa.Field(nullable=True)

    class Config:
        """Configurazione per la validazione dello schema."""

        coerce = True
        strict = False


def validate_dipendenti(df: pd.DataFrame, headers_only: bool = False) -> pd.DataFrame:
    """Valida un dataframe di dipendenti."""
    if headers_only:
        return DipendenteSchema.validate(df.head(0), lazy=True)
    return DipendenteSchema.validate(df, lazy=True)


def validate_giornaliere(df: pd.DataFrame, headers_only: bool = False) -> pd.DataFrame:
    """Valida un dataframe di giornaliere."""
    if headers_only:
        return GiornaliereSchema.validate(df.head(0), lazy=True)
    return GiornaliereSchema.validate(df, lazy=True)


def validate_contabilita(df: pd.DataFrame, headers_only: bool = False) -> pd.DataFrame:
    """Valida un dataframe di contabilità."""
    if headers_only:
        return ContabilitaSchema.validate(df.head(0), lazy=True)
    return ContabilitaSchema.validate(df, lazy=True)
