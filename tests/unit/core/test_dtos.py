from dataclasses import FrozenInstanceError

import pytest

from src.core.dipendenti.employee_dto import EmployeeDTO
from src.core.pdl.pdl_dto import PdlRowDTO


def test_pdl_dto_immutability_and_slots():
    """Verifica l'efficienza della memoria (__slots__) e l'immutabilità (frozen=True) del DTO."""
    row = (
        1,
        "PDL001",
        "2023-01-01",
        "Area1",
        "Unita1",
        "Ditta",
        "Desc",
        "Tipo",
        "Aperto",
        "App",
        "Rich",
        "DataR",
        "Emitt",
        "DataE",
        "Apr",
        "DataA",
        "Alta",
        "Contr",
        "Ord",
        "Sito",
        "Importato",
    )

    dto = PdlRowDTO.from_db_row(row)

    # 1. Verifica assenza di dizionario interno (Data Bloat Protection)
    assert not hasattr(dto, "__dict__"), (
        "Il DTO non deve avere __dict__ se slots=True è configurato correttamente"
    )

    # 2. Verifica immutabilità (Data Leakage Protection)
    with pytest.raises(FrozenInstanceError):
        dto.n_pdl = "PDL_HACKED"  # type: ignore


def test_employee_dto_immutability_and_slots():
    dto = EmployeeDTO("R001", "Rossi", "Mario")
    assert not hasattr(dto, "__dict__")
    with pytest.raises(FrozenInstanceError):
        dto.cognome = "Bianchi"  # type: ignore
