"""Modulo Timesheet."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TimesheetRecord:
    """Modello per una riga di Timesheet elaborata."""

    pos: str
    data: str
    ingresso: str
    uscita: str
    totale: str
    presenza: str
    ore_c: str
    ore_m: str
    ore_st_not: str
    ore_st_diu: str
    ore_fest_not: str
    ore_fest_diu: str
    odc: str | None = None
    tecnico: str | None = None


@dataclass(frozen=True, slots=True)
class TimesheetMetadata:
    """Metadati estratti da un file Timesheet."""

    odc: str
    pos_values: set[str]
    first_pos_cleaned: str
