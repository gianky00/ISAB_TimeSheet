from unittest.mock import MagicMock, patch

import pandas as pd

from src.core.importers.contabilita import ContabilitaImporter


class TestContabilitaImporter:
    @patch("src.core.importers.contabilita.Path")
    def test_import_contabilita_dati_not_found(self, mock_path):
        """Testa import_contabilita_dati con file non trovato."""
        mock_instance = mock_path.return_value
        mock_instance.exists.return_value = False

        success, msg, _rows, _years = ContabilitaImporter.import_contabilita_dati("/invalid/path")
        assert success is False
        assert "non trovato" in msg

    @patch("src.core.importers.contabilita.ContabilitaImporter._get_excel_file")
    @patch("src.core.importers.contabilita.ContabilitaImporter._decrypt_if_encrypted")
    @patch("src.core.importers.contabilita.Path")
    def test_import_contabilita_dati_no_valid_sheets(self, mock_path, mock_decrypt, mock_get_excel):
        """Testa import_contabilita_dati senza fogli validi."""
        mock_path.return_value.exists.return_value = True
        mock_decrypt.return_value = (MagicMock(), False)

        mock_xls = MagicMock()
        mock_xls.sheet_names = ["Sheet1", "OldData"]
        mock_get_excel.return_value = mock_xls

        success, msg, _rows, _years = ContabilitaImporter.import_contabilita_dati("/fake/path")
        assert success is False
        assert "Nessun anno importato" in msg

    def test_clean_numeric(self):
        """Testa la pulizia dei valori numerici."""
        assert ContabilitaImporter._clean_numeric("1.234,56") == 1234.56
        assert ContabilitaImporter._clean_numeric("1234,56") == 1234.56
        assert ContabilitaImporter._clean_numeric("1,234.56") == 1234.56
        assert ContabilitaImporter._clean_numeric("10.5") == 10.5
        assert ContabilitaImporter._clean_numeric("") == 0.0
        assert ContabilitaImporter._clean_numeric(None) == 0.0
        assert ContabilitaImporter._clean_numeric(100) == 100.0

    def test_clean_resa_value(self):
        """Testa la pulizia della colonna Resa."""
        assert ContabilitaImporter._clean_resa_value("100,00") == "100.0"
        assert ContabilitaImporter._clean_resa_value("95.5") == "95.5"
        assert ContabilitaImporter._clean_resa_value("TEST") == "TEST"
        assert ContabilitaImporter._clean_resa_value("") == ""
        assert ContabilitaImporter._clean_resa_value(None) == ""

    def test_identify_sheet_year(self):
        """Testa l'identificazione dell'anno dal nome del foglio."""
        from datetime import UTC, datetime

        current_year = datetime.now(UTC).year
        assert ContabilitaImporter._identify_sheet_year("2025") == 2025
        assert ContabilitaImporter._identify_sheet_year("Dati 2024") == 2024
        assert ContabilitaImporter._identify_sheet_year("Preventivi") == current_year
        assert ContabilitaImporter._identify_sheet_year("Unknown") is None

    @patch("src.core.importers.contabilita.ContabilitaImporter._get_pd")
    def test_find_header_row(self, mock_get_pd):
        """Testa la ricerca della riga di intestazione."""
        mock_pd = mock_get_pd.return_value
        # Crea un df dove la riga 2 (indice 1) ha le intestazioni
        data = [
            ["Noise", "Noise", "Noise"],
            ["DATA PREV.", "MESE", "N PREV."],
            ["2025-01-01", "Gennaio", "P1"],
        ]
        mock_pd.read_excel.return_value = pd.DataFrame(data)

        idx = ContabilitaImporter._find_header_row(MagicMock(), "Sheet1")
        assert idx == 1

    @patch("zipfile.is_zipfile")
    @patch("src.core.importers.contabilita.Path")
    def test_scan_sheets_not_zip(self, mock_path, mock_is_zip):
        """Testa scan_sheets con un file non zip (es. .xls vecchio)."""
        mock_path.return_value.exists.return_value = True
        mock_is_zip.return_value = False
        assert ContabilitaImporter.scan_sheets("test.xls") == 1

    def test_normalize_columns(self):
        """Testa la normalizzazione delle colonne."""
        df = pd.DataFrame(columns=["DATA PREV.", "N. PREV", "MESE", "UNKNOWN"])
        res = ContabilitaImporter._normalize_columns(df)
        assert "data_prev" in res.columns
        assert "n_prev" in res.columns
        assert "mese" in res.columns
        assert "UNKNOWN" in res.columns
