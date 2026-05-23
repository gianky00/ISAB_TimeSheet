from unittest.mock import patch

from src.core.excel_importer import ExcelImporter


class TestExcelImporterFacade:
    @patch("src.core.importers.contabilita.ContabilitaImporter.import_contabilita_dati")
    def test_import_contabilita_dati(self, mock_import):
        mock_import.return_value = (True, "OK", [], [])
        res = ExcelImporter.import_contabilita_dati("test.xlsx")
        assert res[0] is True
        assert mock_import.called

    @patch("src.core.importers.giornaliere.GiornaliereImporter.import_giornaliere")
    def test_import_giornaliere(self, mock_import):
        mock_import.return_value = (True, "OK", [], [])
        res = ExcelImporter.import_giornaliere("/root", {})
        assert res[0] is True
        assert mock_import.called

    @patch("src.core.importers.attivita.AttivitaImporter.import_attivita_programmate")
    def test_import_attivita_programmate(self, mock_import):
        mock_import.return_value = (True, "OK", [])
        res = ExcelImporter.import_attivita_programmate("test.xlsx")
        assert res[0] is True
        assert mock_import.called

    @patch("src.core.importers.scarico_ore.ScaricoOreImporter.import_scarico_ore")
    def test_import_scarico_ore(self, mock_import):
        mock_import.return_value = (True, "OK", [])
        res = ExcelImporter.import_scarico_ore("test.xlsx")
        assert res[0] is True
        assert mock_import.called

    @patch("src.core.importers.certificati.CertificatiImporter.import_certificati_campione")
    def test_import_certificati_campione(self, mock_import):
        mock_import.return_value = (True, "OK", [])
        res = ExcelImporter.import_certificati_campione("test.xlsx")
        assert res[0] is True
        assert mock_import.called

    @patch("src.core.importers.storico_oda.StoricoOdaImporter.import_storico_oda")
    def test_import_storico_oda(self, mock_import):
        mock_import.return_value = (True, "OK", [])
        res = ExcelImporter.import_storico_oda("test.xlsx")
        assert res[0] is True
        assert mock_import.called

    @patch("src.core.importers.contabilita.ContabilitaImporter.scan_sheets", return_value=5)
    @patch("src.core.importers.giornaliere.GiornaliereImporter.scan_files", return_value=10)
    def test_scan_workload(self, mock_files, mock_sheets):
        res = ExcelImporter.scan_workload("f1", "f2")
        assert res == (5, 10)
