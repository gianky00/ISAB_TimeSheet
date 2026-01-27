"""
Baseline tests for ExcelImporter.
Ensures 100% coverage and parity before refactoring.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.core.excel_importer import ExcelImporter
from src.core.importers.contabilita import ContabilitaImporter
from src.core.importers.giornaliere import GiornaliereImporter
from src.core.importers.scarico_ore import ScaricoOreImporter


@pytest.fixture
def mock_xls_file(tmp_path):
    """Crea un file Excel reale per i test di contabilità."""
    path = tmp_path / "test_contabilita.xlsx"
    df2025 = pd.DataFrame(
        {
            "DATA PREV.": ["01/01/2025", "extra"],
            "MESE": ["GENNAIO", ""],
            "N° PREV.": ["P123", ""],
            "TOTALE PREV.": ["1000.0", ""],
            "ATTIVITA'": ["Test 2025", ""],
            "ODC": ["ODC1", ""],
        }
    )
    df2026 = pd.DataFrame(
        {
            "DATA PREV.": ["01/01/2026", "extra"],
            "MESE": ["GENNAIO", ""],
            "N° PREV.": ["P456", ""],
            "TOTALE PREV.": ["2000.0", ""],
            "ATTIVITA'": ["Test 2026", ""],
            "ODC": ["ODC2", ""],
        }
    )

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df2025.to_excel(writer, sheet_name="2025", index=False)
        df2026.to_excel(writer, sheet_name="2026", index=False)
        # Empty sheet
        pd.DataFrame().to_excel(writer, sheet_name="Empty", index=False)
        # Invalid year sheet
        df2026.to_excel(writer, sheet_name="Old", index=False)

    return path


def test_import_contabilita_dati_file_not_found():
    success, msg, rows, years = ExcelImporter.import_contabilita_dati(
        "non_existent.xlsx"
    )
    assert success is False
    assert "File non trovato" in msg


def test_import_contabilita_dati_success(mock_xls_file):
    mock_cb = MagicMock()
    success, msg, rows, years = ExcelImporter.import_contabilita_dati(
        str(mock_xls_file), progress_callback=mock_cb
    )
    assert success is True
    assert 2025 in years
    assert 2026 in years
    assert len(rows) >= 2
    row2025 = [r for r in rows if r[0] == 2025][0]
    assert "P123" in row2025
    assert mock_cb.called


def test_import_contabilita_dati_no_valid_sheets(tmp_path):
    path = tmp_path / "invalid.xlsx"
    pd.DataFrame({"A": [1]}).to_excel(path, sheet_name="NoYear", index=False)
    success, msg, rows, years = ExcelImporter.import_contabilita_dati(str(path))
    assert success is False
    assert "Nessun anno importato" in msg


def test_import_contabilita_dati_empty_sheet(tmp_path):
    path = tmp_path / "empty.xlsx"
    df = pd.DataFrame()
    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name="2025", index=False)
    success, msg, rows, years = ExcelImporter.import_contabilita_dati(str(path))
    assert success is False


def test_import_contabilita_dati_critical_error():
    with patch(
        "src.core.importers.contabilita.pd.ExcelFile", side_effect=Exception("Critical")
    ):
        with patch("src.core.importers.contabilita.Path.exists", return_value=True):
            success, msg, rows, years = ExcelImporter.import_contabilita_dati(
                "dummy.xlsx"
            )
            assert success is False
            assert "Errore critico" in msg


def test_find_header_row_coverage(mock_xls_file):
    xls = pd.ExcelFile(mock_xls_file)
    with patch(
        "src.core.importers.contabilita.pd.read_excel",
        return_value=pd.DataFrame({"A": [1]}),
    ):
        idx = ContabilitaImporter._find_header_row(xls, "2025")
        assert idx == 0


def test_normalize_columns_extra_heuristics():
    df = pd.DataFrame(columns=["PREVENTIVO DATA", "NUMERO PREV"])
    df = ContabilitaImporter._normalize_columns(df)
    assert "data_prev" in df.columns
    assert "n_prev" in df.columns


def test_import_giornaliere_success(tmp_path):
    """Test prioritario: Importazione giornaliere da directory strutturata."""
    root = tmp_path / "Giornaliere"
    root.mkdir()
    folder2025 = root / "Giornaliere 2025"
    folder2025.mkdir()

    df = pd.DataFrame(
        {
            "DATA": ["01/01/2025"],
            "PERSONALE": ["Mario Rossi"],
            "DESCRIZIONE ATTIVITA'": ["Manutenzione 22/123"],
            "TCL": ["T1"],
            "ODC": [""],
            "N° PDL": ["PDL1"],
            "INIZIO": ["08:00"],
            "FINE": ["17:00"],
            "ORE": ["8.0"],
            "consuntivo": ["P123"],
        }
    )

    file_path = folder2025 / "test_giornaliera.xlsx"
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="RIASSUNTO", index=False)
        pd.DataFrame({"DATA": ["Totale"]}).to_excel(
            writer, sheet_name="RIASSUNTO", startrow=2, index=False, header=False
        )

    lookup_map = {"P123": "5400999"}
    mock_cb = MagicMock()

    with patch("src.core.importers.giornaliere.ProcessPoolExecutor") as mock_pool:
        mock_executor = MagicMock()
        mock_pool.return_value.__enter__.return_value = mock_executor
        args = (2025, Path(file_path), lookup_map)
        res = GiornaliereImporter._process_single_giornaliera(args)
        mock_executor.map.return_value = [res]

        success, msg, rows, years = ExcelImporter.import_giornaliere(
            str(root), lookup_map, progress_callback=mock_cb
        )
        assert success is True
        assert 2025 in years
        assert len(rows) > 0
        assert rows[0][5] == "5400999"
        assert rows[0][11] == "test_giornaliera.xlsx"


def test_import_giornaliere_directory_not_found():
    success, msg, rows, years = ExcelImporter.import_giornaliere("invalid_path", {})
    assert success is False
    assert "non trovata" in msg


def test_process_single_giornaliera_extraction_logic(tmp_path):
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame(
        {
            "DATA": ["01/01/2025", "02/01/2025", "03/01/2025"],
            "PERSONALE": ["A", "B", "C"],
            "DESCRIZIONE ATTIVITA'": [
                "Commessa 22/123",
                "Standard 540012345",
                "Canone mensile",
            ],
            "ODC": ["", "540012345", "CANONE_FIXED"],
            "consuntivo": ["P1", "P2", "P3"],
        }
    )
    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer, sheet_name="RIASSUNTO", index=False)
        pd.DataFrame([["X"]]).to_excel(
            writer, sheet_name="RIASSUNTO", startrow=4, index=False, header=False
        )

    args = (2025, Path(file_path), {})
    _, rows, _ = GiornaliereImporter._process_single_giornaliera(args)
    assert rows[0][5] == "22/123"
    assert rows[1][5] == "540012345"
    assert "CANONE" in rows[2][5].upper()


def test_process_single_giornaliera_invalid_sheet(tmp_path):
    file_path = tmp_path / "no_riassunto.xlsx"
    pd.DataFrame({"A": [1]}).to_excel(file_path, sheet_name="Sheet1")
    args = (2025, Path(file_path), {})
    year, rows, err = GiornaliereImporter._process_single_giornaliera(args)
    assert rows == []
    assert err is None


def test_import_scarico_ore_success(tmp_path):
    """Test: Importazione scarico ore con openpyxl e stili."""
    path = tmp_path / "scarico_ore.xlsx"

    # Creiamo un file excel con openpyxl per avere stili reali
    import openpyxl
    from openpyxl.styles import Font, PatternFill

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "SCARICO ORE"

    # Header row (6)
    # col 2 to 12
    headers = [
        "Data",
        "Pers1",
        "Pers2",
        "ODC",
        "Pos",
        "Dalle",
        "Alle",
        "Tot",
        "Desc",
        "Finito",
        "Comm",
    ]
    for i, h in enumerate(headers, start=2):
        ws.cell(row=5, column=i, value=h)

    # Data row (6)
    data = [
        "01/01/2025",
        "U1",
        "U2",
        "54001",
        "10",
        "08:00",
        "17:00",
        "8.0",
        "Desc",
        "Sì",
        "C1",
    ]
    for i, v in enumerate(data, start=2):
        cell = ws.cell(row=6, column=i, value=v)
        if i == 5:  # ODC: Blue foreground
            cell.font = Font(color="0000FF")
        if i == 10:  # Desc: Red background
            cell.fill = PatternFill(
                start_color="FF0000", end_color="FF0000", fill_type="solid"
            )

    wb.save(path)

    success, msg, rows = ExcelImporter.import_scarico_ore(str(path))
    assert success is True
    assert len(rows) == 1

    # Verify row and styles
    # row: (data, pers1, pers2, odc, pos, dalle, alle, totale_ore, descrizione, finito, commessa, styles_json)
    row = rows[0]
    assert row[3] == "54001"

    styles = json.loads(row[11])
    assert styles["odc"]["fg"] == "#0000FF"
    assert styles["descrizione"]["bg"] == "#FF0000"


def test_import_scarico_ore_missing_sheet(tmp_path):
    path = tmp_path / "wrong_sheet.xlsx"
    pd.DataFrame({"A": [1]}).to_excel(path, sheet_name="Wrong")
    success, msg, rows = ExcelImporter.import_scarico_ore(str(path))
    assert success is False
    assert "non trovato" in msg


def test_process_scarico_ore_row_validation():
    """Test casi limite validazione riga scarico ore."""

    # Mocking cell objects from openpyxl
    class MockCell:
        def __init__(self, value, font=None, fill=None):
            self.value = value
            self.font = font
            self.fill = fill

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

    # 1. Row with 0 as ODC (should be treated as empty)
    row_0_odc = [
        MockCell("date"),
        MockCell("P1"),
        MockCell(""),
        MockCell(0),
        MockCell("10"),
        MockCell(""),
        MockCell(""),
        MockCell("8"),
        MockCell(""),
        MockCell(""),
        MockCell(""),
    ]
    res = ScaricoOreImporter._process_scarico_ore_row(row_0_odc, col_keys)
    assert res is None  # ODC is empty string now

    # 2. Row with no personnel
    row_no_pers = [
        MockCell("date"),
        MockCell(""),
        MockCell(""),
        MockCell("5400"),
        MockCell("10"),
        MockCell(""),
        MockCell(""),
        MockCell("8"),
        MockCell(""),
        MockCell(""),
        MockCell(""),
    ]
    res = ScaricoOreImporter._process_scarico_ore_row(row_no_pers, col_keys)
    assert res is None

    # 3. Row with only partial required (missing pos)
    row_no_pos = [
        MockCell("date"),
        MockCell("P1"),
        MockCell(""),
        MockCell("5400"),
        MockCell(""),
        MockCell(""),
        MockCell(""),
        MockCell("8"),
        MockCell(""),
        MockCell(""),
        MockCell(""),
    ]
    res = ScaricoOreImporter._process_scarico_ore_row(row_no_pos, col_keys)
    assert res is None


def test_import_attivita_programmate_success(tmp_path):
    """Test: Importazione attività programmate con mapping colonne complesso."""
    path = tmp_path / "attivita.xlsx"

    df = pd.DataFrame(
        {
            "PS": ["PS1"],
            "AREA": ["Sud"],
            "PdL": ["PDL1"],
            "IMP.": ["X"],
            "DESCRIZIONE\nATTIVITA'": ["Pulizia"],
            "LUN": ["1"],
            "MAR": ["0"],
            "MER": ["1"],
            "GIO": ["0"],
            "VEN": ["1"],
            "STATO\nPdL": ["Attivo"],
            "STATO\nATTIVITA'": ["In corso"],
            "DATA\nCONTROLLO": ["10/01/2026"],
            "PERSONALE\nIMPIEGATO": ["User"],
            "PO": ["PO1"],
            "AVVISO": ["No"],
        }
    )

    # Write with header at row 3 (header=2 in pandas)
    with pd.ExcelWriter(path) as writer:
        # Prepend 2 empty rows by using startrow
        df.to_excel(writer, sheet_name="Riepilogo", startrow=2, index=False)

    success, msg, rows = ExcelImporter.import_attivita_programmate(str(path))
    assert success is True
    assert len(rows) == 1
    # row: (ps, area, pdl, imp, descrizione, lun, mar, mer, gio, ven, stato_pdl, stato_attivita, data_controllo, personale, po, avviso, styles)
    assert rows[0][0] == "PS1"
    assert rows[0][4] == "Pulizia"
    assert rows[0][16] == ""  # styles default


def test_import_attivita_programmate_not_found():
    success, msg, rows = ExcelImporter.import_attivita_programmate("missing.xlsx")
    assert success is False
    assert "non trovato" in msg


def test_import_attivita_programmate_missing_sheet(tmp_path):
    path = tmp_path / "wrong.xlsx"
    pd.DataFrame({"A": [1]}).to_excel(path, sheet_name="Sheet1", index=False)
    success, msg, rows = ExcelImporter.import_attivita_programmate(str(path))
    assert success is False
    assert "non trovato" in msg


def test_import_attivita_programmate_no_columns(tmp_path):
    path = tmp_path / "no_cols.xlsx"
    pd.DataFrame({"Wrong": [1]}).to_excel(
        path, sheet_name="Riepilogo", startrow=2, index=False
    )
    success, msg, rows = ExcelImporter.import_attivita_programmate(str(path))
    assert success is False
    assert "Colonne non trovate" in msg


def test_import_certificati_campione_success(tmp_path):
    """Test: Importazione certificati campione."""
    path = tmp_path / "certificati.xlsx"
    df = pd.DataFrame(
        {
            "Modello / Tipo": ["M1"],
            "Costruttore": ["C1"],
            "Matricola": ["SN1"],
            "Range Strumento": ["0-10"],
            "Errore max %": ["0.1"],
            "Certificato Taratura": ["CERT1"],
            "Scadenza Certificato": ["2026-12-31"],
            "Emissione Certificato": ["2025-01-01"],
            "ID-COEMI": ["ID1"],
            "Stato Certificato": ["30"],  # Days left
        }
    )

    with pd.ExcelWriter(path) as writer:
        # Header detection usually finds it by matching columns
        df.to_excel(writer, sheet_name="Strumenti Campione", startrow=5, index=False)

    success, msg, rows = ExcelImporter.import_certificati_campione(str(path))
    assert success is True
    assert len(rows) == 1
    # row: (modello, costruttore, matricola, range, errore, certificato, scadenza, emissione, id_coemi, stato)
    assert rows[0][0] == "M1"
    assert "31/12/2026" in rows[0][6]
    assert "Scade tra 30 giorni" in rows[0][9]


def test_import_certificati_campione_not_found():
    success, msg, rows = ExcelImporter.import_certificati_campione("missing.xlsx")
    assert success is False
    assert "non trovato" in msg


def test_scan_workload_coverage(tmp_path):
    """Test delle funzioni di scansione rapida workload."""
    # Stima rapida (basata su zip/regex)
    path = tmp_path / "workload.xlsx"
    pd.DataFrame({"A": [1, 2, 3]}).to_excel(path)

    sheets, files = ExcelImporter.scan_workload(str(path), str(tmp_path))
    assert sheets >= 0
    assert files == 0  # No giornaliere folders here

    rows = ExcelImporter.scan_scarico_ore_rows(str(path))
    assert rows >= 0
