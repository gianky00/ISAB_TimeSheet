"""Inizializzazione del pacchetto models."""

from src.domain.contabilita import (
    AttivitaProgrammataRecord,
    CertificatoCampioneRecord,
    ContabilitaRecord,
    GiornalieraRecord,
)
from src.domain.employee import EmployeeRecord
from src.domain.oda import OdaRecord
from src.domain.pdl import PdlProgrammazioneRecord, PdlRecord
from src.domain.timesheet import TimesheetRecord

__all__ = [
    "AttivitaProgrammataRecord",
    "CertificatoCampioneRecord",
    "ContabilitaRecord",
    "EmployeeRecord",
    "GiornalieraRecord",
    "OdaRecord",
    "PdlProgrammazioneRecord",
    "PdlRecord",
    "TimesheetRecord",
]
