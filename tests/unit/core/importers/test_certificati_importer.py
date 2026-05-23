from unittest.mock import patch

from src.core.importers.certificati import CertificatiImporter


class TestCertificatiImporter:
    @patch("src.core.importers.certificati.Pipeline")
    def test_import_certificati_campione_success(self, mock_pipeline_class, fs):
        fs.create_file("certs.xlsx")

        mock_pipeline = mock_pipeline_class.return_value
        mock_pipeline.run.return_value = {"success": True, "message": "Import OK", "rows": [("ID1", "C1")]}

        success, msg, rows = CertificatiImporter.import_certificati_campione("certs.xlsx")

        assert success is True
        assert msg == "Import OK"
        assert len(rows) == 1
        assert rows[0] == ("ID1", "C1")

    @patch("src.core.importers.certificati.Pipeline")
    def test_import_certificati_campione_failure(self, mock_pipeline_class, fs):
        fs.create_file("certs.xlsx")

        mock_pipeline = mock_pipeline_class.return_value
        mock_pipeline.run.return_value = {"success": False, "message": "Read fail", "rows": []}

        success, msg, _rows = CertificatiImporter.import_certificati_campione("certs.xlsx")
        assert success is False
        assert msg == "Read fail"

    def test_import_certificati_campione_not_found(self):
        success, msg, _rows = CertificatiImporter.import_certificati_campione("missing.xlsx")
        assert success is False
        assert "non trovato" in msg

    @patch("src.core.importers.certificati.Pipeline.run", side_effect=Exception("Crash"))
    def test_import_certificati_campione_exception(self, mock_run, fs):
        fs.create_file("certs.xlsx")
        success, msg, _rows = CertificatiImporter.import_certificati_campione("certs.xlsx")
        assert success is False
        assert "Errore" in msg
