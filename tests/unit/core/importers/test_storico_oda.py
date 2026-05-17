from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.core.importers.storico_oda import StoricoOdaImporter


class TestStoricoOdaImporter:
    @patch("src.core.importers.storico_oda.Path")
    def test_import_storico_oda_not_found(self, mock_path):
        """Testa import_storico_oda con file inesistente."""
        mock_path.return_value.exists.return_value = False
        success, msg, data = StoricoOdaImporter.import_storico_oda("/invalid/path")
        assert success is False
        assert "File non trovato" in msg

    @patch("src.core.importers.storico_oda.StoricoOdaImporter._read_storico_oda_excel")
    @patch("src.core.importers.storico_oda.Path")
    def test_import_storico_oda_empty_sheet(self, mock_path, mock_read):
        """Testa import_storico_oda con foglio vuoto."""
        mock_path.return_value.exists.return_value = True
        mock_read.return_value = pd.DataFrame()
        success, msg, data = StoricoOdaImporter.import_storico_oda("/fake/path")
        assert success is False
        assert "Foglio vuoto" in msg

    def test_map_storico_oda_columns(self):
        """Testa la mappatura delle colonne excel -> db."""
        df = pd.DataFrame(columns=["OdA", "Data OdA", "ALTRO"])
        rename_map = StoricoOdaImporter._map_storico_oda_columns(df)
        assert rename_map["OdA"] == "oda"
        assert rename_map["Data OdA"] == "data_oda"
        assert "ALTRO" not in rename_map

    def test_clean_euro_num(self):
        """Testa il parsing dei numeri in formato europeo."""
        assert StoricoOdaImporter._clean_euro_num("1.234,56") == 1234.56
        assert StoricoOdaImporter._clean_euro_num("1234,56") == 1234.56
        assert StoricoOdaImporter._clean_euro_num("1.234,00") == 1234.0
        assert StoricoOdaImporter._clean_euro_num(100.5) == 100.5
        assert StoricoOdaImporter._clean_euro_num(None) == 0.0
        assert StoricoOdaImporter._clean_euro_num("") == 0.0
        assert StoricoOdaImporter._clean_euro_num("ABC") == 0.0

    @patch("src.core.importers.storico_oda.StoricoOdaImporter._get_pd")
    def test_read_storico_oda_excel_success(self, mock_get_pd):
        """Testa la lettura excel con successo su foglio specifico."""
        mock_pd = mock_get_pd.return_value
        mock_pd.read_excel.return_value = pd.DataFrame({"A": [1]})

        res = StoricoOdaImporter._read_storico_oda_excel(Path("test.xlsx"))
        assert not res.empty
        assert mock_pd.read_excel.called
        assert mock_pd.read_excel.call_args[1]["sheet_name"] == "Formato PF"

    @patch("src.core.importers.storico_oda.StoricoOdaImporter._get_pd")
    def test_read_storico_oda_excel_fallback(self, mock_get_pd):
        """Testa il fallback sul primo foglio (indice 0)."""
        mock_pd = mock_get_pd.return_value
        mock_pd.read_excel.side_effect = [ValueError("Sheet not found"), pd.DataFrame({"A": [1]})]

        res = StoricoOdaImporter._read_storico_oda_excel(Path("test.xlsx"))
        assert not res.empty
        assert mock_pd.read_excel.call_count == 2
        assert mock_pd.read_excel.call_args_list[1][1]["sheet_name"] == 0

    def test_normalize_storico_oda_df(self):
        """Testa la normalizzazione (reindex) del dataframe."""
        df = pd.DataFrame({"oda": ["123"], "extra": ["X"]})
        res = StoricoOdaImporter._normalize_storico_oda_df(df)
        assert "oda" in res.columns
        assert "data_oda" in res.columns  # Added by reindex
        assert "extra" not in res.columns  # Removed by reindex
        assert len(res.columns) == len(StoricoOdaImporter.STORICO_ODA_COLS)
