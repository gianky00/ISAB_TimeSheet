from unittest.mock import MagicMock, patch

import pytest

from src.core.database.repositories.pdl_repository import PdlRepository
from src.core.pdl.pdl_controller import PDLController
from src.models import PdlRecord


class TestPdlArchitecture:
    @pytest.fixture
    def mock_db_manager(self):
        mock = MagicMock()
        mock.DB_PDL = "mock_pdl_db"
        return mock

    def test_repository_get_filtered(self, mock_db_manager):
        repo = PdlRepository(db_manager_instance=mock_db_manager)

        mock_row = {
            "id": 1, "n_pdl": "PDL1", "data_creazione": "13/05/2026",
            "area": "AREA1", "unita": "UNIT1", "ditta": "DITTA1",
            "descrizione_lavoro": "DESC", "tipologia": "TIP1", "stato": "APERTO",
            "apparecchiatura": "APP1", "richiedente": "RICH1", "data_richiesta": "12/05/2026",
            "emittente": "EMI1", "data_emissione": "12/05/2026", "aprente": "APR1",
            "data_apertura": "12/05/2026", "priorita": "ALTA", "contratto": "CON1",
            "ordine": "ORD1", "sito": "SITO1", "importato_il": "2026-05-13"
        }

        mock_db_manager.execute_query.return_value = [mock_row]

        records = repo.get_filtered(filters={}, as_objects=True)
        assert len(records) == 1
        assert isinstance(records[0], PdlRecord)
        assert records[0].n_pdl == "PDL1"

    def test_controller_data_loading(self, mock_db_manager):
        with patch("src.core.database.repositories.pdl_repository.PdlRepository.get_filtered") as mock_get:
            record = PdlRecord(
                id=1, n_pdl="PDL1", data_creazione="13/05/2026",
                area="AREA1", unita="UNIT1", ditta="DITTA1",
                descrizione_lavoro="DESC", tipologia="TIP1", stato="APERTO",
                apparecchiatura="APP1", richiedente="RICH1", data_richiesta="12/05/2026",
                emittente="EMI1", data_emissione="12/05/2026", aprente="APR1",
                data_apertura="12/05/2026", priorita="ALTA", contratto="CON1",
                ordine="ORD1", sito="SITO1", importato_il="2026-05-13"
            )
            mock_get.return_value = [record]

            controller = PDLController()
            dtos = controller.get_pdl_data(filters={})

            assert len(dtos) == 1
            assert dtos[0].n_pdl == "PDL1"
            assert dtos[0].descrizione == "DESC"
