"""Inizializzazione del pacchetto repositories."""

from src.application.services.database.repositories.contabilita_repository import ContabilitaRepository
from src.application.services.database.repositories.employee_repository import EmployeeRepository
from src.application.services.database.repositories.oda_repository import OdaRepository
from src.application.services.database.repositories.pdl_repository import PdlRepository

__all__ = ["ContabilitaRepository", "EmployeeRepository", "OdaRepository", "PdlRepository"]
