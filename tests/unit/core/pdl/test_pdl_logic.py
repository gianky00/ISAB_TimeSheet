from unittest.mock import MagicMock, patch

import pytest

from src.application.services.pdl.pdl_controller import PDLController
from src.application.services.pdl.pdl_dto import PdlRowDTO
from src.application.services.pdl.pdl_service import PDLService


class TestPDLLogic:
    @pytest.fixture
    def mock_repo(self):
        with patch("src.application.services.pdl.pdl_controller.PdlRepository") as mock:
            yield mock.return_value

    @pytest.fixture
    def controller(self, mock_repo):
        return PDLController()

    def test_controller_get_pdl_data_caching(self, controller, mock_repo):
        mock_record = MagicMock()
        mock_record.id = 1
        mock_record.n_pdl = "12345"
        mock_record.descrizione_lavoro = "Test"
        mock_repo.get_filtered.return_value = [mock_record]

        filters = {"area": "ISAB"}

        # Prima chiamata: accede al repo
        data1 = controller.get_pdl_data(filters)
        assert len(data1) == 1
        assert data1[0].n_pdl == "12345"
        assert mock_repo.get_filtered.call_count == 1

        # Seconda chiamata: usa la cache
        data2 = controller.get_pdl_data(filters)
        assert data1 == data2
        assert mock_repo.get_filtered.call_count == 1

        # Svuota cache
        controller.clear_cache()
        controller.get_pdl_data(filters)
        assert mock_repo.get_filtered.call_count == 2

    def test_controller_process_master_rows(self):
        dto = PdlRowDTO(
            id=1,
            n_pdl="123",
            data_creazione="2023-01-01",
            area="A",
            unita="U",
            ditta="D",
            descrizione="Desc",
            tipologia="T",
            stato="S",
            apparecchiatura="App",
            richiedente="Rich",
            data_richiesta="2023-01-01",
            emittente="E",
            data_emissione="2023-01-01",
            aprente="Ap",
            data_apertura="2023-01-01",
            priorita="P",
            contratto="C",
            ordine="O",
            sito="Sito",
            importato_il="2023-01-01",
        )

        master = PDLController.process_master_rows([dto])
        assert len(master[0]) == 7
        assert master[0][2] == "123"  # n_pdl è alla terza posizione nel master_list

    @patch("src.application.services.pdl.pdl_service.PdlRepository")
    def test_service_save_programming(self, mock_repo_class):
        mock_repo = mock_repo_class.return_value
        service = PDLService(repo=mock_repo)

        results = [
            {
                "pdl": "12345",
                "richiedente": "R1",
                "area": "A1",
                "programmazione": [
                    {"giorno": 1, "tcl": True, "tgo": False}  # lunedi
                ],
            }
        ]

        service.save_programming_results(results, "2023-05-22", "2023-05-28")

        assert mock_repo.save_programming.called
        records = mock_repo.save_programming.call_args[0][0]
        assert len(records) == 1
        assert records[0].n_pdl == "12345"
        assert records[0].lun_tcl is True
        assert records[0].mar_tcl is False

    @patch("src.application.services.pdl.pdl_service.PdlRepository")
    @patch("src.application.services.pdl.pdl_service.config_manager.load_config")
    @patch("src.application.services.pdl.pdl_service.Path.exists")
    def test_service_get_interventions_missing_db(self, mock_exists, mock_config, mock_repo_class):
        mock_exists.return_value = False
        mock_config.return_value = {"activity_db_path": "/non/existent.db"}

        service = PDLService()
        interventions = service.get_pdl_interventions("123")

        assert interventions == []
        # Non deve nemmeno chiamare il repo se il DB non esiste
        assert not mock_repo_class.return_value.get_interventions.called
