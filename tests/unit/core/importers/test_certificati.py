from unittest.mock import patch

from src.application.services.importers.certificati import CertificatiImporter


class TestCertificatiImporter:
    @patch("src.application.services.importers.certificati.Path")
    def test_import_certificati_campione_not_found(self, mock_path):
        """Testa import_certificati_campione con file non trovato."""
        mock_instance = mock_path.return_value
        mock_instance.exists.return_value = False

        success, msg, _rows = CertificatiImporter.import_certificati_campione("/invalid/path")
        assert success is False
        assert "File non trovato" in msg

    @patch("src.application.services.importers.certificati.Pipeline")
    @patch("src.application.services.importers.certificati.Path")
    def test_import_certificati_campione_success(self, mock_path, mock_pipeline_class):
        """Testa l'importazione con successo tramite pipeline."""
        mock_path.return_value.exists.return_value = True

        mock_pipeline = mock_pipeline_class.return_value
        mock_pipeline.run.return_value = {
            "success": True,
            "message": "Importato con successo",
            "rows": [(1, "Test")],
        }

        success, msg, rows = CertificatiImporter.import_certificati_campione("/fake/path")
        assert success is True
        assert msg == "Importato con successo"
        assert rows == [(1, "Test")]
        assert mock_pipeline.run.called

    @patch("src.application.services.importers.certificati.Pipeline")
    @patch("src.application.services.importers.certificati.Path")
    def test_import_certificati_campione_error(self, mock_path, mock_pipeline_class):
        """Testa la gestione errori durante l'importazione."""
        mock_path.return_value.exists.return_value = True

        mock_pipeline = mock_pipeline_class.return_value
        mock_pipeline.run.side_effect = Exception("Crash")

        success, msg, _rows = CertificatiImporter.import_certificati_campione("/fake/path")
        assert success is False
        assert "Errore importazione" in msg
        assert "Crash" in msg
