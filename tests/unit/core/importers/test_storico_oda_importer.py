from unittest.mock import patch

import pandas as pd

from src.core.importers.storico_oda import StoricoOdaImporter


class TestStoricoOdaImporter:
    @patch("src.core.importers.storico_oda.pd.read_excel")
    def test_import_storico_oda_success(self, mock_read, fs):
        fs.create_file("oda.xlsx")
        # Setup mock DF
        df = pd.DataFrame(
            {"OdA": ["100"], "Data OdA": ["2023-01-01"], "Pos OdA": ["10"], "Valore Netto ODA": ["1.234,56"]}
        )
        mock_read.return_value = df

        success, _msg, data = StoricoOdaImporter.import_storico_oda("oda.xlsx")

        assert success is True
        assert len(data) == 1
        # Verifica mappatura e pulizia numeri
        # StoricoOdaImporter._clean_storico_oda_data viene chiamato internamente
        # L'ordine delle colonne è STORICO_ODA_COLS
        cols = StoricoOdaImporter.STORICO_ODA_COLS
        oda_idx = cols.index("oda")
        val_idx = cols.index("valore_netto_oda")

        assert data[0][oda_idx] == "100"
        assert data[0][val_idx] == 1234.56

    def test_map_storico_oda_columns(self):
        df = pd.DataFrame(columns=["ODA", "data oda", "Unknown"])
        mapping = StoricoOdaImporter._map_storico_oda_columns(df)

        assert mapping["ODA"] == "oda"
        assert mapping["data oda"] == "data_oda"
        assert "Unknown" not in mapping

    def test_clean_euro_num(self):
        assert StoricoOdaImporter._clean_euro_num("1.234,56") == 1234.56
        assert StoricoOdaImporter._clean_euro_num("1234,56") == 1234.56
        assert StoricoOdaImporter._clean_euro_num(100) == 100.0
        assert StoricoOdaImporter._clean_euro_num("") == 0.0

    def test_normalize_storico_oda_df(self):
        df = pd.DataFrame({"oda": ["1"], "extra": ["X"]})
        normalized = StoricoOdaImporter._normalize_storico_oda_df(df)

        assert len(normalized.columns) == len(StoricoOdaImporter.STORICO_ODA_COLS)
        assert "extra" not in normalized.columns
        assert "org_acq" in normalized.columns  # Una delle colonne mancanti riempite con ""

    def test_import_storico_oda_not_found(self):
        success, msg, _data = StoricoOdaImporter.import_storico_oda("missing.xlsx")
        assert success is False
        assert "File non trovato" in msg
