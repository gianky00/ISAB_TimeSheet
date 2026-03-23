import json
from unittest.mock import MagicMock, patch

import openpyxl
import pandas as pd
import pytest
from openpyxl.styles import Font

from src.core.importers.giornaliere import GiornaliereImporter
from src.core.importers.scarico_ore import ScaricoOreImporter


class TestImportersRobust:
    # --- Giornaliere Tests (Pandas based) ---

    @pytest.fixture
    def mock_giornaliera_df(self):
        """DataFrame simulato per Giornaliere."""
        data = {
            "DATA": ["2024-01-01", "2024-01-02", "Totale"],
            "PERSONALE": ["Rossi", "Bianchi", ""],
            "DESCRIZIONE ATTIVITA'": ["Lavoro", "Ferie", ""],
            "TCL": ["T1", "T2", ""],
            "ODC": [
                "540012345",
                "",
                "",
            ],  # ODC valido (formato 5400...) per evitare cancellazione
            "N° PDL": ["123", "456", ""],
            "INIZIO": ["08:00", "09:00", ""],
            "FINE": ["17:00", "18:00", ""],
            "ORE": [8, 8, 16],
            "consuntivo": ["5400123", "5400456", ""],  # n_prev
        }
        return pd.DataFrame(data)

    def test_process_single_giornaliera_success(self, mock_giornaliera_df, tmp_path):
        """Test processamento completo singola giornaliera."""
        path = tmp_path / "Giornaliera_2024.xlsx"
        path.touch()

        args = (2024, path, {"5400456": "540099999"})  # Mapping verso ODC valido

        # Mock pandas read_excel
        with patch(
            "src.core.importers.giornaliere.GiornaliereImporter._read_giornaliera_sheet",
            return_value=mock_giornaliera_df,
        ):
            year, rows, err = GiornaliereImporter._process_single_giornaliera(args)

            assert year == 2024
            assert err is None
            assert len(rows) == 2

            # Verifica mapping ODC
            # Riga 1: 540012345 (presente e valido)
            assert rows[0][5] == "540012345"
            # Riga 2: ODC vuoto, ma n_prev="5400456" -> Mapped to "540099999"
            assert rows[1][5] == "540099999"

    def test_giornaliera_normalize_columns(self):
        """Test normalizzazione nomi colonne."""
        df = pd.DataFrame({"  Data  ": [], "Personale": [], "Unknown": []})
        norm_df = GiornaliereImporter._normalize_giornaliera_columns(df)

        assert "data" in norm_df.columns  # Lowercase e strip
        assert "personale" in norm_df.columns
        assert "Unknown" in norm_df.columns

    def test_giornaliera_clean_data(self, mock_giornaliera_df):
        """Test pulizia dati (rimozione totali)."""
        # Necessaria normalizzazione prima della pulizia (che si aspetta colonne minuscole)
        norm_df = GiornaliereImporter._normalize_giornaliera_columns(mock_giornaliera_df)
        clean_df = GiornaliereImporter._clean_giornaliera_data(norm_df)

        assert len(clean_df) == 2
        assert "Totale" not in clean_df["data"].values

    # --- Scarico Ore Tests (OpenPyXL based) ---

    @pytest.fixture
    def mock_scarico_wb(self):
        """Crea un workbook Excel reale in memoria."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "SCARICO ORE"

        # Header (righe 1-5 ignorate)
        for i in range(1, 6):
            ws.cell(row=i, column=1, value="Header")

        # Riga 6: Dati validi
        # Col 2-12: Data, P1, P2, ODC, POS, Dalle, Alle, Tot, Desc, Fin, Comm
        row_valid = [
            None,
            "2024-01-01",
            "P1",
            "P2",
            "ODC1",
            "10",
            "8",
            "17",
            "8",
            "Desc",
            "S",
            "C",
        ]
        for col, val in enumerate(row_valid, start=1):
            if val:
                c = ws.cell(row=6, column=col, value=val)
                # Aggiungi stile
                if col == 5:  # ODC
                    c.font = Font(color="FF0000")  # Red

        # Riga 7: Dati invalidi (manca ODC e POS)
        row_invalid = [
            None,
            "2024-01-02",
            "P1",
            "",
            "",
            "",
            "8",
            "17",
            "8",
            "Desc",
            "S",
            "C",
        ]
        for col, val in enumerate(row_invalid, start=1):
            if val:
                ws.cell(row=7, column=col, value=val)

        return wb

    def test_scarico_ore_parsing_logic(self, mock_scarico_wb):
        """Test logica parsing Scarico Ore con workbook reale."""
        ws = mock_scarico_wb["SCARICO ORE"]

        rows = ScaricoOreImporter._process_all_scarico_rows(ws, None)

        assert len(rows) == 1  # Solo riga 6 valida
        valid_row = rows[0]

        # Verifica dati
        assert valid_row[0] == "2024-01-01"  # Data
        assert valid_row[3] == "ODC1"  # ODC

        # Verifica stili JSON
        styles = json.loads(valid_row[11])
        assert "odc" in styles
        assert styles["odc"]["fg"] == "#FF0000"

    def test_scarico_ore_import_file_not_found(self):
        """Test file non trovato."""
        success, msg, _ = ScaricoOreImporter.import_scarico_ore("non_existent.xlsx")
        assert success is False
        assert "non trovato" in msg

    @patch("src.core.importers.scarico_ore.msoffcrypto")
    def test_scan_encrypted_file(self, mock_crypto, tmp_path):
        """Test scansione file cifrato."""
        from src.core.constants import Business

        path = tmp_path / "protected.xlsx"
        path.touch()

        # Simuliamo decifratura
        mock_file = MagicMock()
        mock_crypto.OfficeFile.return_value = mock_file

        # Se msoffcrypto c'è, deve tentare di aprire
        ScaricoOreImporter.scan_scarico_ore_rows(str(path))
        mock_file.load_key.assert_called_with(password=Business.DEFAULT_EXCEL_PASSWORD)
        mock_file.decrypt.assert_called()
