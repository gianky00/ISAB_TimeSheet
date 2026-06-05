from unittest.mock import MagicMock, patch

import pandas as pd

# Mock DataSynchronizer per tutti i test degli importer
import pytest

from src.application.services.excel_importer import ExcelImporter


@pytest.fixture(autouse=True)
def mock_data_synchronizer():
    with (
        patch(
            "src.application.services.data_synchronizer.DataSynchronizer.sync_certificati_campione",
            return_value=(1, 0),
        ),
        patch(
            "src.application.services.data_synchronizer.DataSynchronizer.sync_scarico_ore",
            return_value=(1, 0),
        ),
        patch(
            "src.application.services.data_synchronizer.DataSynchronizer.sync_giornaliere",
            return_value=(1, 0),
        ),
    ):
        yield


class TestExcelImporter:
    # --- Contabilita Dati ---
    @patch("src.application.services.importers.contabilita.validate_contabilita", side_effect=lambda x: x)
    @patch("src.application.services.importers.contabilita.ContabilitaImporter._get_excel_file")
    @patch("src.application.services.importers.base.BaseImporter._decrypt_if_encrypted")
    @patch("src.application.services.importers.contabilita.Path.exists", return_value=True)
    @patch("pandas.read_excel")
    def test_import_contabilita_dati_success(
        self,
        mock_read_excel,
        mock_exists,
        mock_decrypt,
        mock_get_excel,
        mock_validate,
    ):
        """Test importazione dati contabilità."""
        # Mock decryption
        mock_decrypt.return_value = (MagicMock(), False)

        # Mock ExcelFile
        mock_xls = MagicMock()
        mock_xls.sheet_names = ["Dati 2024"]
        mock_get_excel.return_value = mock_xls

        # Dataframe di test con tipi corretti
        df = pd.DataFrame(
            {
                "DATA PREV.": ["2024-01-01", "Totale"],
                "MESE": ["Gennaio", ""],
                "N° PREV.": ["P1", ""],
                "TOTALE PREV.": [1000.0, 0.0],
                "ATTIVITA'": ["A1", ""],
                "TCL": ["T1", ""],
                "ODC": ["O1", ""],
                "STATO ATTIVITA'": ["Aperta", ""],
                "TIPOLOGIA": ["Tip", ""],
                "ORE SP": [8.0, 0.0],
                "RESA": ["100", ""],
                "ANNOTAZIONI": ["Notes", ""],
                "INDIRIZZO CONSUNTIVO": ["Path", ""],
                "NOME FILE": ["File", ""],
            }
        )

        def mock_read_excel_side_effect(*args, **kwargs):
            if kwargs.get("header") is None:
                return pd.DataFrame([df.columns.tolist(), *df.values.tolist()])
            return df

        mock_read_excel.side_effect = mock_read_excel_side_effect

        success, _msg, rows, years = ExcelImporter.import_contabilita_dati("dummy.xlsx")

        assert success
        assert len(rows) > 0
        assert 2024 in years

    @patch("src.application.services.importers.contabilita.Path.exists", return_value=False)
    def test_import_contabilita_dati_file_not_found(self, mock_exists):
        success, msg, _rows, _years = ExcelImporter.import_contabilita_dati("missing.xlsx")
        assert not success
        assert "non trovato" in msg

    # --- Giornaliere ---
    def test_import_giornaliere(self, tmp_path):
        """Test prioritario: Importazione giornaliere da directory strutturata."""
        root = tmp_path / "Giornaliere"
        root.mkdir()
        folder2025 = root / "Giornaliere 2025"
        folder2025.mkdir()

        df = pd.DataFrame(
            {
                "DATA": ["01/01/2025"],
                "PERSONALE": ["Mario Rossi"],
                "DESCRIZIONE ATTIVITÀ": ["Manutenzione 22/123"],
                "TCL": ["T1"],
                "ODC": [""],
                "N  PDL": ["PDL1"],
                "INIZIO": ["08:00"],
                "FINE": ["17:00"],
                "ORE": ["8.0"],
                "consuntivo": ["P123"],
            }
        ).astype(str)

        file_path = folder2025 / "test_giornaliera.xlsx"
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="RIASSUNTO", index=False)

        lookup_map = {"P123": "5400999"}
        mock_cb = MagicMock()

        with (
            patch(
                "src.application.services.importers.giornaliere.GiornaliereImporter._process_single_giornaliera"
            ) as mock_proc,
            patch("src.gui.main_window.page_index.PageIndex") as mock_page_index,
            patch("src.application.services.importers.giornaliere.ProcessPoolExecutor") as mock_pool,
        ):
            mock_page_index.DASHBOARD = 0
            mock_proc.return_value = (
                2025,
                [
                    (
                        2025,
                        "01/01/2025",
                        "Mario Rossi",
                        "Manutenzione",
                        "T1",
                        "5400999",
                        "PDL1",
                        "08:00",
                        "17:00",
                        "8.0",
                        "P123",
                        "test_giornaliera.xlsx",
                    )
                ],
                None,
            )
            mock_executor = MagicMock()
            mock_pool.return_value.__enter__.return_value = mock_executor
            mock_executor.map.return_value = [mock_proc.return_value]

            success, _msg, rows, years = ExcelImporter.import_giornaliere(
                str(root), lookup_map, progress_callback=mock_cb
            )
            assert success is True
            assert 2025 in years
            assert len(rows) > 0
            assert rows[0][5] == "5400999"
            assert rows[0][11] == "test_giornaliera.xlsx"

    # --- Storico OdA ---
    @patch("pandas.read_excel")
    @patch("src.application.services.importers.storico_oda.Path.exists", return_value=True)
    def test_import_storico_oda(self, mock_exists, mock_read):
        # Mock columns matching STORICO_ODA_MAPPING
        data = {
            "Org. Acq.": ["OA1"],
            "data oda": ["2024-01-01"],
            "ODA": ["123"],
            "Prezzo Lordo": [100.0],
            # Add other required fields if strictly validated
            "Pos. OdA": ["1"],
            "Num. Riga": ["1"],
            "Divisione": ["D1"],
            "Destinatario": ["U1"],
            "Contratto": ["C1"],
            "Posizione Contratto": ["P1"],
            "Qta": [1],
            "Data Consegna": ["2024-02-01"],
            "Descrizione": ["Item"],
            "Valore Netto Pos.": [100],
            "Valore Residuo": [0],
            "Valore Netto OdA": [100],
            "Quantità": [1],
        }
        df = pd.DataFrame(data)
        mock_read.return_value = df

        success, _msg, rows = ExcelImporter.import_storico_oda("dummy.xlsx")
        assert success
        assert len(rows) == 1

    # --- Attivita Programmate ---
    @patch("pandas.read_excel")
    @patch("src.application.services.importers.attivita.Path.exists", return_value=True)
    def test_import_attivita_programmate(self, mock_exists, mock_read):
        # Mapping: PS, AREA, PdL, IMP., DESCRIZIONE ATTIVITA', ...
        data = {
            "PS": ["PS1"],
            "AREA": ["A1"],
            "PdL": ["PDL1"],
            "IMP.": ["IMP1"],
            "DESCRIZIONE\nATTIVITA'": ["Desc"],
            "DATA\nCONTROLLO": ["2024-01-01"],
        }
        df = pd.DataFrame(data)
        mock_read.return_value = df

        success, _msg, rows = ExcelImporter.import_attivita_programmate("dummy.xlsx")
        assert success
        assert len(rows) == 1
        # Check styles column is added (empty)
        assert rows[0][-1] == ""  # styles

    # --- Scarico Ore (OpenPyXL) ---
    @patch("src.application.services.processing.scarico_ore.steps.LoadScaricoOreStep._load_scarico_workbook")
    @patch("src.application.services.importers.scarico_ore.Path.exists", return_value=True)
    def test_import_scarico_ore_with_styles(self, mock_exists, mock_load_wb):
        # Mock Workbook and Worksheet
        wb = MagicMock()
        wb.sheetnames = ["SCARICO ORE"]
        ws = MagicMock()
        wb.__getitem__.return_value = ws
        mock_load_wb.return_value = wb

        # Mock rows (values_only=False) -> returns Cell objects
        # We need 6 rows header skip, so we simulate row 6 onwards
        # iter_rows returns generator of tuples of cells

        # Mock Cell
        def create_cell(value, color=None, bg=None):
            cell = MagicMock()
            cell.value = value
            cell.font = MagicMock()
            cell.fill = MagicMock()

            if color:
                cell.font.color.type = "rgb"
                cell.font.color.rgb = color
            else:
                cell.font.color = None

            if bg:
                cell.fill.patternType = "solid"
                cell.fill.start_color.type = "rgb"
                cell.fill.start_color.rgb = bg
            else:
                cell.fill.patternType = "none"
            return cell

        # Create one row of data (11 cols)
        # data, pers1, pers2, odc, pos, dalle, alle, tot, desc, fin, comm
        row_cells = (
            create_cell("2024-01-01"),  # data
            create_cell("P1", color="FFFF0000"),  # pers1 red
            create_cell("P2"),
            create_cell("ODC1"),
            create_cell("POS1"),
            create_cell("08:00"),
            create_cell("17:00"),
            create_cell(8),
            create_cell("Desc"),
            create_cell("NO"),
            create_cell("C1", bg="FF00FF00"),  # comm green bg
        )

        ws.iter_rows.return_value = [row_cells]
        ws.max_row = 7

        success, _msg, rows = ExcelImporter.import_scarico_ore("dummy.xlsx")

        assert success
        assert len(rows) == 1

        # Check styles JSON
        import json

        styles = json.loads(rows[0][-1])
        assert styles["pers1"]["fg"] == "#FF0000"
        assert styles["commessa"]["bg"] == "#00FF00"

    # --- Certificati Campione ---
    @patch("src.application.services.processing.certificati.steps.pd.read_excel")
    @patch("src.application.services.processing.certificati.steps.pd.ExcelFile")
    @patch("src.application.services.importers.certificati.Path.exists", return_value=True)
    def test_import_certificati_campione(self, mock_exists, mock_excel_file, mock_read):
        # Mock ExcelFile to return sheet names
        mock_excel = MagicMock()
        mock_excel.sheet_names = ["Strumenti Campione"]
        mock_excel_file.return_value = mock_excel

        # Mock read_excel (first for preview, second for data)
        # We can just return the same DF
        data = {
            "Modello / Tipo": ["M1"],
            "Costruttore": ["C1"],
            "Matricola": ["123"],
            "Scadenza Certificato": ["2024-12-31"],
            "Stato Certificato": [10],  # 10 days left
        }
        df = pd.DataFrame(data)
        mock_read.return_value = df

        success, _msg, rows = ExcelImporter.import_certificati_campione("dummy.xlsx")

        assert success
        assert len(rows) == 1
        assert "Scade tra 10 giorni" in rows[0]

    # --- Scan Methods ---
    @patch("src.application.services.importers.scarico_ore.zipfile.ZipFile")
    @patch("src.application.services.importers.scarico_ore.Path.exists", return_value=True)
    def test_scan_scarico_ore_rows(self, mock_exists, mock_zip):
        # Mock ZipFile context manager
        z = MagicMock()
        mock_zip.return_value.__enter__.return_value = z
        z.namelist.return_value = ["xl/worksheets/sheet1.xml"]

        # Mock file read content with dimension ref
        f = MagicMock()
        f.read.return_value = b'<dimension ref="A1:Z100"/>'
        z.open.return_value.__enter__.return_value = f

        rows = ExcelImporter.scan_scarico_ore_rows("dummy.xlsx")
        assert rows == 100

    @patch(
        "src.application.services.importers.contabilita.ContabilitaImporter.scan_sheets",
        return_value=["S1", "S2"],
    )
    @patch("src.application.services.importers.giornaliere.GiornaliereImporter.scan_files", return_value=3)
    def test_scan_workload(self, mock_scan_files, mock_scan_sheets):
        sheets, files = ExcelImporter.scan_workload("cont.xlsx", "root_giornaliere")
        # Returns (list, count) or (list, list)?
        # scan_sheets returns list. scan_files returns int.
        # But ExcelImporter.scan_workload says: return sheets, files
        # Let's check if I mocked scan_files correctly in previous attempt (I mocked return list)
        # GiornaliereImporter.scan_files returns int (count).
        # ContabilitaImporter.scan_sheets returns list.
        # So return value is (list, int).
        assert sheets == ["S1", "S2"]
        assert files == 3
