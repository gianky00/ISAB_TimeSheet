from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

from src.core.importers.attivita import AttivitaImporter


class TestAttivitaImporter:
    @patch("src.core.importers.attivita.Path")
    def test_import_attivita_programmate_not_found(self, mock_path):
        """Testa import_attivita_programmate con file non trovato."""
        mock_instance = mock_path.return_value
        mock_instance.exists.return_value = False

        success, msg, _rows = AttivitaImporter.import_attivita_programmate("/invalid/path")
        assert success is False
        assert "non trovato" in msg

    @patch("src.core.importers.attivita.AttivitaImporter._read_attivita_programmate_sheet")
    @patch("src.core.importers.attivita.Path")
    def test_import_attivita_programmate_sheet_not_found(self, mock_path, mock_read):
        """Testa import_attivita_programmate quando il foglio non esiste."""
        mock_path.return_value.exists.return_value = True
        mock_read.return_value = None

        success, msg, _rows = AttivitaImporter.import_attivita_programmate("/fake/path")
        assert success is False
        assert "Riepilog" in msg

    def test_normalize_attivita_columns(self):
        """Testa la normalizzazione delle colonne."""
        df = pd.DataFrame(columns=["PS", "AREA ", "DESCRIZIONE\nATTIVITÀ", "OTHER"])
        res = AttivitaImporter._normalize_attivita_columns(df)

        assert "ps" in res.columns
        assert "area" in res.columns
        assert "descrizione" in res.columns
        assert "OTHER" in res.columns  # Not in mapping, remains same

    def test_normalize_attivita_columns_fail(self):
        """Testa il fallimento della normalizzazione se nessuna colonna coincide."""
        df = pd.DataFrame(columns=["INVALID", "COLS"])
        res = AttivitaImporter._normalize_attivita_columns(df)
        assert res is None

    def test_prepare_attivita_rows(self):
        """Testa la preparazione delle righe per il database."""
        df = pd.DataFrame(
            {
                "ps": ["PS1", "PS2", np.nan],
                "area": ["A1", "A2", np.nan],
                "descrizione": ["D1", "D2", np.nan],
                "extra": ["E1", "E2", "E3"],
            }
        )

        rows = AttivitaImporter._prepare_attivita_rows(df)

        # Dovrebbe aver rimosso la terza riga (tutte NaN le check_cols)
        assert len(rows) == 2
        # Dovrebbe aver aggiunto tutte le colonne mancanti del mapping e 'styles'
        assert len(rows[0]) == len(AttivitaImporter.ATTIVITA_PROGRAMMATE_MAPPING) + 1
        assert rows[0][0] == "PS1"
        assert rows[0][-1] == ""  # styles

    @patch("src.core.importers.attivita.AttivitaImporter._get_pd")
    def test_read_attivita_programmate_sheet_success(self, mock_get_pd):
        """Testa la lettura del foglio excel con successo."""
        mock_pd = mock_get_pd.return_value
        mock_df = pd.DataFrame({"Test": [1]})
        mock_pd.read_excel.return_value = mock_df

        res = AttivitaImporter._read_attivita_programmate_sheet(Path("test.xlsx"))
        assert isinstance(res, pd.DataFrame)
        assert mock_pd.read_excel.called

    @patch("src.core.importers.attivita.AttivitaImporter._get_pd")
    def test_read_attivita_programmate_sheet_fallback(self, mock_get_pd):
        """Testa il fallback sul motore openpyxl se il primo tentativo fallisce."""
        mock_pd = mock_get_pd.return_value
        # Primo tentativo lancia ValueError (es: sheet missing o engine issue)
        mock_pd.read_excel.side_effect = [ValueError("Error"), pd.DataFrame({"A": [1]})]

        res = AttivitaImporter._read_attivita_programmate_sheet(Path("test.xlsx"))
        assert isinstance(res, pd.DataFrame)
        assert mock_pd.read_excel.call_count == 2
        assert mock_pd.read_excel.call_args_list[1].kwargs.get("engine") == "openpyxl"
