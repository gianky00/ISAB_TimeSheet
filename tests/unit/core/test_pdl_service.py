from unittest.mock import patch

import pytest

from src.core.pdl.pdl_service import PDLService


class TestPDLService:
    @pytest.fixture
    def mock_repo(self, mocker):
        # Mock the repository class in the service module
        mock_class = mocker.patch("src.core.pdl.pdl_service.PdlRepository")
        mock_instance = mock_class.return_value
        return mock_instance

    def test_get_unique_requesters_normalization(self, mock_repo):
        """Verifica la normalizzazione dei nomi dei richiedenti."""
        mock_repo.get_unique_requesters.return_value = ["Mario Rossi", "Luigi Verdi", "Isab S.R.L."]

        results = PDLService.get_unique_requesters()

        assert "Mario Rossi" in results
        assert "Luigi Verdi" in results
        assert "Isab S.R.L." in results
        assert len(results) == 3

    def test_save_programming_results_success(self, mock_repo):
        """Verifica l'inserimento corretto dei dati di programmazione."""
        results = [
            {
                "richiedente": "R1",
                "pdl": "P1",
                "area": "A1",
                "unita": "U1",
                "descrizione": "D1",
                "programmazione": [{"giorno": 1, "tcl": True, "tgo": False}] * 7,
            }
        ]

        mock_repo.save_programming.return_value = True
        success = PDLService.save_programming_results(results, "01/01", "07/01")

        assert success is True
        assert mock_repo.save_programming.called
        args = mock_repo.save_programming.call_args
        records = args[0][0]
        assert len(records) == 1
        assert records[0].richiedente == "R1"

    def test_get_programming_results_by_week(self, mock_repo):
        """Verifica il recupero dei dati settimanali mappati in dizionari."""
        from src.models import PdlProgrammazioneRecord

        mock_record = PdlProgrammazioneRecord(
            id=1,
            richiedente="R1",
            n_pdl="P1",
            area="A1",
            unita="U1",
            descrizione="D1",
            settimana_start="start",
            settimana_end="end",
            lun_tcl=True,
            lun_tgo=False,
            mar_tcl=True,
            mar_tgo=True,
            mer_tcl=False,
            mer_tgo=False,
            gio_tcl=False,
            gio_tgo=False,
            ven_tcl=False,
            ven_tgo=False,
            sab_tcl=False,
            sab_tgo=False,
            dom_tcl=False,
            dom_tgo=False,
            ultimo_aggiornamento="2024",
        )
        mock_repo.get_programming_by_week.return_value = [mock_record]

        results = PDLService.get_programming_results_by_week("start", "end")

        assert len(results) == 1
        assert results[0]["richiedente"] == "R1"
        assert results[0]["programmazione"][0]["tcl"] is True
        assert results[0]["programmazione"][1]["tgo"] is True

    def test_get_pdl_interventions_success(self, tmp_path, mock_repo):
        """Verifica il recupero interventi delegato al repo."""
        db_file = tmp_path / "ext.db"
        db_file.touch()

        mock_repo.get_interventions.return_value = [{"fonte": "Report (Validato)", "tecnico": "T1"}]

        with patch("src.core.config_manager.load_config") as mock_cfg:
            mock_cfg.return_value = {"activity_db_path": str(db_file)}
            res = PDLService.get_pdl_interventions("P1")

            assert len(res) == 1
            assert res[0]["fonte"] == "Report (Validato)"
            assert res[0]["tecnico"] == "T1"
            assert mock_repo.get_interventions.called
