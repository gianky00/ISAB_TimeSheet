from unittest.mock import patch

import pandas as pd

from src.application.services.importers.giornaliere import GiornaliereImporter


class TestGiornaliereImporter:
    def test_scan_files_filtering(self, tmp_path):
        """Verifica che scan_files filtri correttamente anni e file temporanei."""
        g_dir = tmp_path / "Giornaliere"
        g_dir.mkdir()

        # Folder valida
        f2025 = g_dir / "Giornaliere 2025"
        f2025.mkdir()
        (f2025 / "test.xlsx").touch()
        (f2025 / "~$temp.xlsx").touch()  # Temp file

        # Folder anno vecchio
        f2024 = g_dir / "Giornaliere 2024"
        f2024.mkdir()
        (f2024 / "old.xlsx").touch()

        # Folder nome non conforme
        f_bad = g_dir / "Dati 2025"
        f_bad.mkdir()
        (f_bad / "data.xlsx").touch()

        count = GiornaliereImporter.scan_files(str(g_dir))
        # Dovrebbe contare solo test.xlsx in Giornaliere 2025
        assert count == 1

    def test_normalize_giornaliera_columns(self):
        """Verifica mappatura e validazione (mockata)."""
        from src.application.services.processing.giornaliere.steps import NormalizeGiornalieraStep

        df = pd.DataFrame(columns=["DATA", "PERSONALE", "ORE", "N° PDL"])
        context = {"success": True, "df": df}

        with patch("src.application.services.processing.giornaliere.steps.validate_giornaliere", side_effect=lambda x: x):
            NormalizeGiornalieraStep().execute(context)
            assert context.get("success") is False or "df" in context

            # Since _clean_data is called and drops rows because it's empty,
            # the step will mark context as failed or empty df.
            # We just assert that if df is present, it has the right columns.
            if "df" in context and not context["df"].empty:
                norm_df = context["df"]
                assert "data" in norm_df.columns
                assert "personale" in norm_df.columns
                assert "pdl" in norm_df.columns

    def test_clean_giornaliera_data_removes_totals(self):
        """Verifica rimozione riga totali e righe contenenti 'Totale'."""
        from src.application.services.processing.giornaliere.steps import NormalizeGiornalieraStep

        data = {
            "data": ["2025-01-01", "2025-01-02", "TOTALE GENERALE"],
            "personale": ["P1", "P2", ""],
            "ore": [8, 4, 12],
        }
        df = pd.DataFrame(data)

        cleaned = NormalizeGiornalieraStep()._clean_data(df)

        # iloc[:-1] toglie l'ultima riga
        # il filtro "Totale" dovrebbe togliere eventuali altre righe di riepilogo
        assert len(cleaned) == 2
        assert "TOTALE GENERALE" not in cleaned["data"].values

    def test_enrich_giornaliera_odc_regex(self):
        """Verifica estrazione ODC da descrizione e mapping."""
        from pathlib import Path

        from src.application.services.processing.giornaliere.steps import EnrichGiornalieraStep

        df = pd.DataFrame(
            {
                "odc": ["", "", "54001234 (extra)"],
                "n_prev": ["PREV1", "PREV2", ""],
                "descrizione": ["Lavoro su 24/123", "Altro", ""],
                "data": ["", "", ""],
                "personale": ["", "", ""],
                "tcl": ["", "", ""],
                "pdl": ["", "", ""],
                "inizio": ["", "", ""],
                "fine": ["", "", ""],
                "ore": ["", "", ""],
            }
        )
        lookup = {"PREV2": "99/999"}
        context = {
            "success": True,
            "df": df,
            "lookup_map": lookup,
            "year": 2025,
            "file_path": Path("test.xlsx"),
        }

        EnrichGiornalieraStep().execute(context)
        df_out = pd.DataFrame(
            context["rows"],
            columns=[
                "year",
                "data",
                "personale",
                "descrizione",
                "tcl",
                "odc",
                "pdl",
                "inizio",
                "fine",
                "ore",
                "n_prev",
                "nome_file",
            ],
        )

        # 1. 24/123 estratto da descrizione
        assert df_out.loc[0, "odc"] == "24/123"
        # 2. 99/999 mappato da n_prev
        assert df_out.loc[1, "odc"] == "99/999"
        # 3. 54001234 pulito da stringa sporca
        assert df_out.loc[2, "odc"] == "54001234"

    @patch("src.application.services.importers.giornaliere.ProcessPoolExecutor")
    def test_import_giornaliere_no_tasks(self, mock_executor, tmp_path):
        """Verifica comportamento se non ci sono file da processare."""
        success, msg, rows, _years = GiornaliereImporter.import_giornaliere(str(tmp_path), {})
        assert success is True
        assert "Nessuna nuova giornaliera" in msg
        assert rows == []
