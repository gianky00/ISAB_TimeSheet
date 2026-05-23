from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.core.processing.giornaliere.steps import (
    EnrichGiornalieraStep,
    NormalizeGiornalieraStep,
    ReadGiornalieraStep,
    SyncGiornaliereStep,
)


class TestGiornaliereProcessingSteps:
    @patch("src.core.processing.giornaliere.steps.pd.read_excel")
    def test_read_giornaliera_step_success(self, mock_read, fs):
        fs.create_file("giorn.xlsx")
        mock_read.return_value = pd.DataFrame({"A": [1]})

        step = ReadGiornalieraStep()
        ctx = {"file_path": Path("giorn.xlsx")}
        step.execute(ctx)

        assert ctx["success"] is True
        assert "df" in ctx

    @patch("src.core.processing.giornaliere.steps.pd.read_excel", side_effect=ValueError("Fail"))
    def test_read_giornaliera_step_failure(self, mock_read, fs):
        fs.create_file("fail.xlsx")
        step = ReadGiornalieraStep()
        ctx = {"file_path": Path("fail.xlsx")}
        step.execute(ctx)

        assert ctx["success"] is False
        assert "Impossibile leggere" in ctx["message"]

    @patch("src.core.processing.giornaliere.steps.validate_giornaliere", side_effect=lambda df: df)
    def test_normalize_giornaliera_step(self, mock_val):
        df = pd.DataFrame(
            {
                "DATA": ["2023-01-01", "2023-01-02", "TOTALE"],
                "PERSONALE": ["P1", "P2", ""],
                "ORE": [8, 8, 16],
                "DESCRIZIONE ATTIVITÀ": ["D1", "D2", ""],
            }
        )

        step = NormalizeGiornalieraStep()
        ctx = {"df": df, "success": True}
        step.execute(ctx)

        normalized_df = ctx["df"]
        assert "data" in normalized_df.columns
        assert "personale" in normalized_df.columns
        assert len(normalized_df) == 2
        assert "TOTALE" not in normalized_df["data"].values

    def test_enrich_giornaliera_step(self):
        df = pd.DataFrame(
            {
                "data": ["2023-01-01"],
                "personale": ["P1"],
                "descrizione": ["Lavoro generico"],
                "tcl": [""],
                "odc": [""],
                "pdl": [""],
                "inizio": [""],
                "fine": [""],
                "ore": [8],
                "n_prev": ["PREV1"],
            }
        )

        step = EnrichGiornalieraStep()
        # Usiamo un ODC che passi i filtri successivi (es. formato 23/123 o 5400...)
        ctx = {
            "df": df,
            "success": True,
            "year": 2023,
            "file_path": Path("test.xlsx"),
            "lookup_map": {"PREV1": "23/123"},
        }
        step.execute(ctx)

        rows = ctx["rows"]
        assert len(rows) == 1
        assert rows[0][5] == "23/123"

    def test_enrich_giornaliera_pattern_matching(self):
        df = pd.DataFrame(
            {
                "data": ["2023-01-01"],
                "personale": ["P1"],
                "descrizione": ["Intervento su 24/456"],
                "tcl": [""],
                "odc": [""],
                "pdl": [""],
                "inizio": [""],
                "fine": [""],
                "ore": [8],
                "n_prev": [""],
            }
        )

        step = EnrichGiornalieraStep()
        ctx = {"df": df, "success": True, "year": 2024, "file_path": Path("test.xlsx")}
        step.execute(ctx)

        assert ctx["rows"][0][5] == "24/456"

    @patch("src.core.data_synchronizer.DataSynchronizer.sync_giornaliere")
    def test_sync_giornaliere_step(self, mock_sync):
        mock_sync.return_value = (10, 0)
        step = SyncGiornaliereStep()
        ctx = {"success": True, "rows": [("row",)], "year": 2023}

        step.execute(ctx)

        assert ctx["total_added"] == 10
        assert ctx["success"] is True
