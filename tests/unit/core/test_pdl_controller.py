from unittest.mock import patch

import pytest

from src.core.pdl.pdl_controller import PDLController
from src.core.pdl.pdl_dto import PdlRowDTO
from src.models.pdl import PdlRecord


@pytest.fixture
def mock_pdl_repository():
    with patch("src.core.pdl.pdl_controller.PdlRepository") as mock_repo_class:
        mock_repo = mock_repo_class.return_value
        yield mock_repo


def test_pdl_controller_returns_dtos_with_mocked_db(mock_pdl_repository):
    """Verifica che il controller agisca come ponte convertendo i dati grezzi in DTO."""
    # 1. Arrange (Preparazione Mock)
    # Simuliamo 10.000 righe fittizie dal database per testare le performance di mapping
    mock_record = PdlRecord(
        id=1,
        n_pdl="PDL001",
        data_creazione="2023-01-01",
        area="Area1",
        unita="Unita1",
        ditta="Ditta",
        descrizione_lavoro="Desc",
        tipologia="Tipo",
        stato="Aperto",
        apparecchiatura="App",
        richiedente="Rich",
        data_richiesta="DataR",
        emittente="Emitt",
        data_emissione="DataE",
        aprente="Apr",
        data_apertura="DataA",
        priorita="Alta",
        contratto="Contr",
        ordine="Ord",
        sito="Sito",
        importato_il="Importato",
    )

    mock_pdl_repository.get_filtered.return_value = [mock_record] * 10000

    controller = PDLController()

    # 2. Act (Azione)
    results = controller.get_pdl_data(filters={})

    # 3. Assert (Verifiche)
    assert len(results) == 10000, "Deve restituire tutte le 10.000 righe"
    assert isinstance(results[0], PdlRowDTO), "I risultati devono essere mappati come PdlRowDTO"
    assert results[0].n_pdl == "PDL001", "Il mapping del numero PDL deve essere corretto"
    assert results[0].area == "Area1", "Il mapping dell'area deve essere corretto"

    # Verifichiamo che la repository sia stata chiamata
    mock_pdl_repository.get_filtered.assert_called_once()

    # Verifichiamo il sistema di cache
    results_cached = controller.get_pdl_data(filters={})
    assert len(results_cached) == 10000
    assert mock_pdl_repository.get_filtered.call_count == 1, (
        "La seconda chiamata deve usare la cache interna, non la repository"
    )
