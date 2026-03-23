from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.core.importers.giornaliere import GiornaliereImporter


class TestExcelImporterComprehensive:
    def test_import_giornaliere_parsing(self, tmp_path):
        file1 = tmp_path / "file1.xlsx"
        file1.touch()

        cols = [
            "DATA",
            "PERSONALE",
            "DESCRIZIONE ATTIVITA'",
            "TCL",
            "ODC",
            "N° PDL",
            "INIZIO",
            "FINE",
            "ORE",
            "consuntivo",
        ]
        # Add 3 rows: Data, extra, and Total (which is dropped)
        data = [
            [
                "01/01/2024",
                "Mario Rossi",
                "Desc",
                "T1",
                "O1",
                "P1",
                "08:00",
                "17:00",
                8,
                "100/24",
            ],
            [
                "02/01/2024",
                "Luigi Verdi",
                "Desc",
                "T1",
                "O1",
                "P1",
                "08:00",
                "17:00",
                8,
                "100/24",
            ],
            ["Totale", "", "", "", "", "", "", "", 16, ""],
        ]
        df = pd.DataFrame(data, columns=cols)

        with patch("src.core.importers.giornaliere.pd.read_excel", return_value=df):
            # Using dict() to avoid tool interpolation issues with {}
            _year, rows, err = GiornaliereImporter._process_single_giornaliera((2024, Path(file1), {}))

            assert err is None
            # Code does iloc[:-1], so "Totale" row is dropped. 2 rows remain.
            assert len(rows) == 2
            assert rows[0][2] == "Mario Rossi"
            assert rows[1][2] == "Luigi Verdi"
