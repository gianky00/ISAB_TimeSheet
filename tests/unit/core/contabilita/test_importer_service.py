import pytest

from src.application.services.contabilita.importer_service import ContabilitaImporterService


class TestContabilitaImporterService:
    @pytest.fixture
    def mock_importer(self, mocker):
        return mocker.patch("src.application.services.contabilita.importer_service.ExcelImporter")

    @pytest.fixture
    def mock_sync(self, mocker):
        return mocker.patch("src.application.services.contabilita.importer_service.DataSynchronizer")

    def test_scan_workload(self, mock_importer):
        mock_importer.scan_workload.return_value = (10, 20)
        res = ContabilitaImporterService.scan_workload("f1", "f2")
        assert res == (10, 20)

    def test_import_main_data_success(self, mocker):
        # We need to mock the Pipeline behavior
        mock_pipeline = mocker.patch("src.application.services.contabilita.importer_service.Pipeline")
        mock_pipeline.return_value.run.return_value = {
            "success": True,
            "message": "OK",
            "total_added": 5,
            "total_removed": 2,
        }

        success, _, added, removed = ContabilitaImporterService.import_main_data("path")
        assert success is True
        assert added == 5
        assert removed == 2

    def test_import_main_data_failure(self, mocker):
        mock_pipeline = mocker.patch("src.application.services.contabilita.importer_service.Pipeline")
        mock_pipeline.return_value.run.side_effect = Exception("Crash")

        success, msg, _, _ = ContabilitaImporterService.import_main_data("path")
        assert success is False
        assert "Errore critico" in msg

    def test_import_giornaliere_path_not_found(self, fs):
        success, msg, _, _ = ContabilitaImporterService.import_giornaliere("/non/existent")
        assert success is False
        assert "non trovata" in msg

    def test_import_giornaliere_success(self, mock_importer, mock_sync, mocker, fs):
        fs.create_dir("/data/giornaliere")
        mocker.patch.object(ContabilitaImporterService, "_prepare_odc_lookup_map", return_value={})

        mock_importer.import_giornaliere.return_value = (True, "OK", [{"id": 1}], [2026])
        mock_sync.sync_giornaliere.return_value = (1, 0)

        success, msg, added, _ = ContabilitaImporterService.import_giornaliere("/data/giornaliere")
        assert success is True
        assert added == 1
        assert "2026" in msg

    def test_import_attivita_programmate(self, mock_importer, mock_sync):
        mock_importer.import_attivita_programmate.return_value = (True, "OK", [])
        mock_sync.sync_attivita_programmate.return_value = (10, 5)

        success, _, added, _ = ContabilitaImporterService.import_attivita_programmate("p")
        assert success is True
        assert added == 10

    def test_import_scarico_ore(self, mock_importer, mock_sync):
        mock_importer.import_scarico_ore.return_value = (True, "OK", [])
        mock_sync.sync_scarico_ore.return_value = (20, 0)

        success, _, added, _ = ContabilitaImporterService.import_scarico_ore("p")
        assert success is True
        assert added == 20

    def test_import_certificati_campione(self, mock_sync, mocker):
        mock_imp = mocker.patch("src.application.services.importers.certificati.CertificatiImporter")
        mock_imp.import_certificati_campione.return_value = (True, "OK", [1, 2, 3])
        mock_sync.sync_certificati_campione.return_value = (3, 0)

        success, msg, added, _ = ContabilitaImporterService.import_certificati_campione("p")
        assert success is True
        assert added == 3
        assert "Importati 3" in msg
