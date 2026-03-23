from unittest.mock import patch

import pytest

from src.core.pdl.pdl_controller import PDLController
from src.core.pdl.pdl_dto import PdlRowDTO


@pytest.fixture
def mock_db_manager():
    with patch("src.core.pdl.pdl_controller.db_manager") as mock_db:
        # Mock della costante DB_PDL
        mock_db.DB_PDL = "pdl.db"
        yield mock_db


def test_pdl_controller_returns_dtos_with_mocked_db(mock_db_manager):  # noqa: ANN001
    """Verifica che il controller agisca come ponte convertendo i dati grezzi in DTO."""

    # 1. Arrange (Preparazione Mock)
    # Simuliamo 10.000 righe fittizie dal database per testare le performance di mapping
    mock_row = (
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

    mock_db_manager.execute_query.return_value = [mock_row] * 10000

    controller = PDLController()

    # 2. Act (Azione)
    results = controller.get_pdl_data(filters={})

    # 3. Assert (Verifiche)
    assert len(results) == 10000, "Deve restituire tutte le 10.000 righe"  # noqa: PLR2004
    assert isinstance(results[0], PdlRowDTO), "I risultati devono essere mappati come PdlRowDTO"
    assert results[0].n_pdl == "PDL001", "Il mapping del numero PDL deve essere corretto"
    assert results[0].area == "Area1", "Il mapping dell'area deve essere corretto"

    # Verifichiamo che il DB sia stato chiamato esattamente una volta
    mock_db_manager.execute_query.assert_called_once()

    # Verifichiamo il sistema di cache
    results_cached = controller.get_pdl_data(filters={})
    assert len(results_cached) == 10000  # noqa: PLR2004
    assert mock_db_manager.execute_query.call_count == 1, (
        "La seconda chiamata deve usare la cache interna, non il DB"
    )
