from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

from src.core.importers.attivita import AttivitaImporter


class TestAttivitaImporter:
    @patch("src.core.importers.attivita.pd.read_excel")
    def test_import_attivita_programmate_success(self, mock_read, fs):
        fs.create_file("attivita.xlsx")

        # Setup mock DF con le colonne attese
        df = pd.DataFrame(
            {
                "PS": ["1"],
                "AREA": ["A1"],
                "PdL": ["P100"],
                "IMP.": ["I1"],
                "DESCRIZIONE\nATTIVITÀ": ["Desc"],
                "LUN": ["X"],
                "STATO\nPdL": ["OK"],
                "STATO\nATTIVITÀ": ["Done"],
            }
        )
        mock_read.return_value = df

        success, _msg, rows = AttivitaImporter.import_attivita_programmate("attivita.xlsx")

        assert success is True
        assert len(rows) == 1
        cols = AttivitaImporter.ATTIVITA_PROGRAMMATE_COLS
        desc_idx = cols.index("descrizione")
        assert rows[0][desc_idx] == "Desc"

    def test_normalize_attivita_columns(self):
        df = pd.DataFrame(columns=["PS", "AREA", "DESCRIZIONE\nATTIVITÀ", "DATA\nCONTROLLO"])
        normalized = AttivitaImporter._normalize_attivita_columns(df)

        assert normalized is not None
        assert "ps" in normalized.columns
        assert "area" in normalized.columns
        assert "descrizione" in normalized.columns
        assert "data_controllo" in normalized.columns

    def test_normalize_attivita_columns_variations(self):
        # Test con variazioni À e apici
        # Nota: STATO\nPdL in mapping -> STATO PDL pulito
        df = pd.DataFrame(columns=[" DESCRIZIONE\nATTIVITA' ", "STATO\nPdL"])
        normalized = AttivitaImporter._normalize_attivita_columns(df)

        assert normalized is not None
        assert "descrizione" in normalized.columns
        assert "stato_pdl" in normalized.columns

    def test_prepare_attivita_rows_cleanup(self):
        # dropna(how="all") funziona solo su NaN
        df = pd.DataFrame(
            {
                "ps": ["1", np.nan, np.nan],
                "area": ["A1", np.nan, np.nan],
                "descrizione": ["D1", np.nan, np.nan],
            }
        )

        rows = AttivitaImporter._prepare_attivita_rows(df)
        assert len(rows) == 1
        assert rows[0][0] == "1"

    @patch("src.core.importers.attivita.pd.read_excel")
    def test_read_attivita_programmate_sheet_failure(self, mock_read, fs):
        fs.create_file("fail.xlsx")
        mock_read.side_effect = Exception("Open error")

        res = AttivitaImporter._read_attivita_programmate_sheet(Path("fail.xlsx"))
        assert res is None

    def test_import_attivita_programmate_not_found(self):
        success, msg, _rows = AttivitaImporter.import_attivita_programmate("missing.xlsx")
        assert success is False
        assert "non trovato" in msg
