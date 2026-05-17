from unittest.mock import MagicMock, patch

from src.core.importers.scarico_ore import ScaricoOreImporter


class TestScaricoOreImporter:
    @patch("src.core.importers.scarico_ore.Path")
    def test_import_scarico_ore_not_found(self, mock_path):
        """Testa import_scarico_ore con file non trovato."""
        mock_instance = mock_path.return_value
        mock_instance.exists.return_value = False

        success, msg, rows = ScaricoOreImporter.import_scarico_ore("/invalid/path")
        assert success is False
        assert "non trovato" in msg

    @patch("src.core.importers.scarico_ore.Pipeline")
    @patch("src.core.importers.scarico_ore.Path")
    def test_import_scarico_ore_success(self, mock_path, mock_pipeline_class):
        """Testa l'importazione con successo tramite pipeline."""
        mock_path.return_value.exists.return_value = True

        mock_pipeline = mock_pipeline_class.return_value
        mock_pipeline.run.return_value = {"success": True, "message": "Importato", "rows": [(1, "Test")]}

        success, msg, rows = ScaricoOreImporter.import_scarico_ore("/fake/path")
        assert success is True
        assert msg == "Importato"
        assert rows == [(1, "Test")]

    @patch("src.core.importers.scarico_ore.zipfile.ZipFile")
    @patch("src.core.importers.scarico_ore.Path")
    def test_scan_scarico_ore_rows_xml_parse(self, mock_path, mock_zip):
        """Testa la scansione rapida delle righe tramite parsing XML del file zip."""
        mock_path.return_value.exists.return_value = True

        # Mock dello zip e del contenuto XML
        mock_z = mock_zip.return_value.__enter__.return_value
        mock_z.namelist.return_value = ["xl/worksheets/sheet1.xml"]

        mock_f = MagicMock()
        # XML con dimensione 100 righe
        xml_content = b'<dimension ref="A1:L100"/>'
        mock_f.read.return_value = xml_content
        mock_z.open.return_value.__enter__.return_value = mock_f

        count = ScaricoOreImporter.scan_scarico_ore_rows("/fake/path.xlsx")
        assert count == 100

    @patch("src.core.importers.scarico_ore.zipfile.is_zipfile")
    @patch("src.core.importers.scarico_ore.Path")
    def test_scan_scarico_ore_rows_not_exists(self, mock_path, mock_is_zip):
        """Testa scan con file inesistente."""
        mock_path.return_value.exists.return_value = False
        assert ScaricoOreImporter.scan_scarico_ore_rows("/invalid") == 0

    @patch("src.core.processing.scarico_ore.steps.ProcessScaricoOreRowsStep")
    def test_process_all_scarico_rows_alias(self, mock_step_class):
        """Testa l'alias per il processamento righe."""
        mock_step = mock_step_class.return_value
        mock_ws = MagicMock()

        # Simula il comportamento dello step che popola context["rows"]
        def mock_execute(ctx):
            ctx["rows"] = [("row1",)]

        mock_step.execute.side_effect = mock_execute

        rows = ScaricoOreImporter._process_all_scarico_rows(mock_ws, None)
        assert rows == [("row1",)]
        assert mock_step.execute.called
