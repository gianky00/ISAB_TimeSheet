import json
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.core.excel_importer import ExcelImporter
from src.core.importers.contabilita import ContabilitaImporter
from src.core.importers.giornaliere import GiornaliereImporter
from src.core.importers.scarico_ore import ScaricoOreImporter


class TestExcelImporterAdvanced:
    @pytest.fixture
    def mock_xls(self):
        """Mock per pd.ExcelFile."""
        mock = MagicMock(spec=pd.ExcelFile)
        mock.sheet_names = ["Dati 2026", "Foglio Inutile", "2025"]
        return mock

    # --- CONTABILITA DATI TESTS ---

    def test_import_contabilita_dati_mapping_resilience(self, mock_xls, mocker):  # noqa: ANN001
        """Test: Riconoscimento colonne con nomi leggermente diversi o sporchi."""
        # Patch diretta del metodo interno per evitare problemi con la logica complessa di read_excel/preview
        mock_data = [
            (
                2026,
                "2026-01-01",
                "Gennaio",
                "P123",
                1000.0,
                "Test",
                "T1",
                "ODC1",
                "IN CORSO",
                "TIP1",
                10.0,
                "100%",
                "Note",
                "Path",
                "file.pdf",
            )
        ]
        mocker.patch(
            "src.core.importers.contabilita.ContabilitaImporter._process_single_sheet",
            return_value=mock_data,
        )
        mocker.patch(
            "src.core.importers.contabilita.ContabilitaImporter._get_excel_file",
            return_value=mock_xls,
        )
        mocker.patch("src.core.importers.contabilita.Path.exists", return_value=True)
        mocker.patch(
            "src.core.importers.contabilita.ContabilitaImporter._decrypt_if_encrypted",
            return_value=("fake_path", False),
        )

        success, _msg, rows, years = ExcelImporter.import_contabilita_dati("fake.xlsx")

        assert success is True
        assert 2026 in years  # noqa: PLR2004
        # rows format: (year, data_prev, mese, n_prev, ...)
        assert rows[0][3] == "P123"

    # --- GIORNALIERE TESTS ---

    def test_process_single_giornaliera_cleaning(self):
        """Test: Pulizia dati giornaliere (rimozione Totale, strip, nan handling)."""
        df_giorn = pd.DataFrame(
            {
                "DATA": ["01/01/2026", "02/01/2026", "TOTALE", ""],
                "PERSONALE": ["Mario Rossi", "Luigi Bianchi", "Totale", ""],
                "DESCRIZIONE ATTIVITA'": ["D1", "D2", "DT", ""],
                "TCL": ["", "", "", ""],
                "ODC": ["ODC1", "NaN", "", ""],
                "N° PDL": ["", "", "", ""],
                "INIZIO": ["", "", "", ""],
                "FINE": ["", "", "", ""],
                "ORE": ["8", "4", "12", ""],
                "consuntivo": ["", "", "", ""],
            }
        )

        with patch("src.core.importers.giornaliere.pd.read_excel", return_value=df_giorn):
            _year, rows, err = GiornaliereImporter._process_single_giornaliera((2026, Path("test.xlsx"), {}))
            assert err is None
            assert len(rows) == 2  # noqa: PLR2004
            assert rows[0][2] == "Mario Rossi"

    def test_giornaliera_odc_lookup(self):
        """Test: Recupero ODC mancante tramite lookup_map (n_prev -> odc)."""
        df = pd.DataFrame(
            {
                "DATA": ["01/01/2026", "Footer"],
                "PERSONALE": ["User", "F"],
                "DESCRIZIONE ATTIVITA'": ["Descrizione", "F"],
                "TCL": ["", ""],
                "ODC": ["", ""],
                "N° PDL": ["", ""],
                "INIZIO": ["", ""],
                "FINE": ["", ""],
                "ORE": ["8", ""],
                "consuntivo": ["P999", ""],
            }
        )
        # L'ODC deve iniziare con 5400 per passare il filtro mask_standard nel sorgente
        lookup = {"P999": "54001234"}

        with patch("src.core.importers.giornaliere.pd.read_excel", return_value=df):
            _year, rows, _err = GiornaliereImporter._process_single_giornaliera(
                (2026, Path("f.xlsx"), lookup)
            )
            assert len(rows) > 0
            assert rows[0][10] == "P999"
            assert rows[0][5] == "54001234"

    # --- SCARICO ORE TESTS ---

    def test_process_scarico_ore_row_with_styles(self):
        """Test: Estrazione stili (colori) da una riga scarico ore."""
        mock_row = []
        # data, pers1, pers2, odc, pos, dalle, alle, totale_ore, descrizione, finito, commessa
        for i in range(11):
            cell = MagicMock()
            cell.value = f"val_{i}"

            # Setup font color
            cell.font.color.type = "rgb"
            cell.font.color.rgb = "FFFF0000"  # Rosso

            # Setup fill color
            cell.fill.patternType = "solid"
            cell.fill.start_color.type = "rgb"
            cell.fill.start_color.rgb = "FF00FF00"  # Verde

            mock_row.append(cell)

        col_keys = [
            "data",
            "pers1",
            "pers2",
            "odc",
            "pos",
            "dalle",
            "alle",
            "totale_ore",
            "descrizione",
            "finito",
            "commessa",
        ]

        res = ScaricoOreImporter._process_scarico_ore_row(mock_row, col_keys)

        assert res is not None
        styles_json = res[-1]
        styles = json.loads(styles_json)

        # Check first key 'data'
        assert styles["data"]["fg"] == "#FF0000"
        assert styles["data"]["bg"] == "#00FF00"

    # --- ATTIVITA PROGRAMMATE TESTS ---

    def test_import_attivita_programmate_not_found(self, tmp_path):  # noqa: ANN001
        """Test: Gestione file mancante per Attività Programmate."""
        success, msg, _rows = ExcelImporter.import_attivita_programmate(str(tmp_path / "missing.xlsx"))
        assert success is False
        assert "non trovato" in msg

    # --- UTILS ---

    def test_identify_sheet_year(self):
        """Test: Estrazione anno da nomi fogli."""
        assert ContabilitaImporter._identify_sheet_year("Dati 2026") == 2026  # noqa: PLR2004
        assert ContabilitaImporter._identify_sheet_year("2024_Riepilogo") == 2024  # noqa: PLR2004
        assert ContabilitaImporter._identify_sheet_year("Dati") == datetime.now().year
        assert ContabilitaImporter._identify_sheet_year("Foglio1") is None
