from typing import Dict, List, Optional

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
        coerce = True
        strict = False


def get_excel_column_letter(n: int) -> str:
    """Converte un indice di colonna (0-based) in lettera Excel (A, B, C...)."""
    string = ""
    n += 1
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def _group_ranges(numbers: List[int]) -> str:
    """Raggruppa numeri consecutivi in range (es. 1, 2, 3, 5 -> 1-3, 5)."""
    if not numbers:
        return ""
    numbers = sorted(set(numbers))
    ranges = []
    start = numbers[0]
    for i in range(1, len(numbers) + 1):
        if i == len(numbers) or numbers[i] != numbers[i - 1] + 1:
            end = numbers[i - 1]
            ranges.append(f"{start}-{end}" if start != end else f"{start}")
            if i < len(numbers):
                start = numbers[i]
    return ", ".join(ranges)


def format_schema_errors(
    e: pa.errors.SchemaErrors,
    filename: str = "",
    sheet: str = "",
    header_offset: int = 0,
    column_map: Optional[Dict[str, int]] = None,
) -> str:
    """Traduce gli errori in un formato compatto elencando tutte le celle in gioco."""
    lines = []
    if filename:
        lines.append(
            f"<b>📂 File:</b> {filename}" + (f" | 📄 Foglio: {sheet}" if sheet else "")
        )

    failure_cases = e.failure_cases
    if failure_cases is not None and not failure_cases.empty:
        for col, group in failure_cases.groupby("column"):
            col_letter = "?"
            if column_map and col in column_map:
                col_letter = get_excel_column_letter(column_map[col])

            # Calcola tutte le righe Excel coinvolte
            # Excel Row = Index in DF + Header Row Offset + 2
            excel_rows = [idx + header_offset + 2 for idx in group.index]

            # Raggruppa per range per non creare stringhe infinite
            row_ranges = _group_ranges(excel_rows)
            # Crea coordinate complete (es. K3-K7, K10)
            cell_coords = ", ".join(
                [f"{col_letter}{r}" for r in row_ranges.split(", ")]
            )

            lines.append(
                f"• <b>{col}</b>: {len(group)} err. nelle celle: <b>{cell_coords}</b>"
            )

    return "\n".join(lines) if lines else str(e)


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
