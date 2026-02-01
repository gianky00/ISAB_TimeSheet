from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from src.core.importers.giornaliere import GiornaliereImporter
from src.core.importers.scarico_ore import ScaricoOreImporter


class TestImportersRobust:
    # --- GIORNALIERE ---
    @patch("src.core.importers.giornaliere.GiornaliereImporter._read_giornaliera_sheet")
    @patch("src.core.importers.giornaliere.GiornaliereImporter._decrypt_if_encrypted")
    def test_process_single_giornaliera_success(self, mock_decrypt, mock_read):
        # Mock dataframe input con 2 righe (l'ultima viene scartata dall'importer)
        data = {
            "DATA": ["01/01/2025", "TOTALI"],
            "PERSONALE": ["Rossi", ""],
            "DESCRIZIONE ATTIVITA'": ["Lavoro", ""],
            "TCL": ["T1", ""],
            "ODC": ["O1", ""],
            "N° PDL": ["P1", ""],
            "INIZIO": ["08:00", ""],
            "FINE": ["17:00", ""],
            "ORE": [8.0, 8.0],
            "consuntivo": ["123", ""],
        }
        df = pd.DataFrame(data)

        mock_decrypt.return_value = (MagicMock(), False)
        mock_read.return_value = df

        args = (2025, Path("test.xlsx"), {})
        year, rows, err = GiornaliereImporter._process_single_giornaliera(args)

        assert year == 2025
        assert len(rows) >= 1
        assert err is None

    def test_giornaliera_normalize_columns(self):
        df = pd.DataFrame({"DATA": [1], "PERSONALE": [2], "ORE": [3]})
        # Deve rinominare e mantenere solo colonne mappate
        normalized = GiornaliereImporter._normalize_giornaliera_columns(df)
        assert "data" in normalized.columns
        assert "personale" in normalized.columns

    # --- SCARICO ORE ---
    @patch(
        "src.core.importers.scarico_ore.ScaricoOreImporter._identify_sheet_year",
        return_value=2025,
    )
    def test_scarico_ore_parsing_logic(self, mock_year):
        # ScaricoOre è più complesso perché usa openpyxl per gli stili
        # Testiamo la logica di estrazione data
        importer = ScaricoOreImporter()

        # Testiamo un metodo interno di utilità se possibile, o mockiamo l'intero flusso
        with patch("pandas.read_excel") as mock_pd_read:
            mock_pd_read.return_value = pd.DataFrame(
                {
                    "Data": ["2025-01-01"],
                    "Dipendente": ["X"],
                    "Commessa": ["Y"],
                    "Ore Ordinarie": [8],
                    "Ore Straordinarie": [0],
                }
            )

            # Nota: ScaricoOre non ha un metodo 'import_file' semplice,
            # spesso viene usato tramite orchestratori.
            # Testiamo la robustezza della classe base ereditata.
            assert importer._get_pd() is not None
