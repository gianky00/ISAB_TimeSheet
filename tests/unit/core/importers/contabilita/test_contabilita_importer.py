from unittest.mock import patch

from src.core.importers.contabilita import ContabilitaImporter


def test_scan_sheets_valid_excel():
    # Mock per simulare un file excel con fogli validi
    with patch("pathlib.Path.exists", return_value=True), \
         patch("zipfile.is_zipfile", return_value=True), \
         patch("zipfile.ZipFile") as mock_zip:

        mock_zip.return_value.__enter__.return_value.namelist.return_value = ["xl/workbook.xml"]
        mock_zip.return_value.__enter__.return_value.read.return_value = b'name="2026" name="2025"'

        count = ContabilitaImporter.scan_sheets("fake.xlsx")
        assert count == 2

def test_scan_sheets_missing_file():
    count = ContabilitaImporter.scan_sheets("nonexistent.xlsx")
    assert count == 0

def test_import_contabilita_dati_missing_file():
    success, msg, _data, _years = ContabilitaImporter.import_contabilita_dati("missing.xlsx")
    assert success is False
    assert "non trovato" in msg
