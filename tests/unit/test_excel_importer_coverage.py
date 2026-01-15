import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from src.core.excel_importer import ExcelImporter

@pytest.fixture
def importer():
    return ExcelImporter()

def test_import_contabilita_file_not_found(importer):
    """Test gestione file inesistente."""
    with patch("pathlib.Path.exists", return_value=False):
        success, msg, rows, years = importer.import_contabilita_dati("non_existent.xlsx")
        assert success is False
        assert "non trovato" in msg
        assert rows == []

def test_import_contabilita_valid_data(importer):
    """Test importazione dati validi (Contabilità)."""
    # Actual DF (restituito da _process_single_sheet -> read_excel)
    # IMPORTANTE: Aggiungiamo una riga extra perché _process_single_sheet fa df.iloc[:-1]
    data_actual = {
        "DATA PREV.": ["01/01/2025", "TOTALI"],
        "MESE": ["Gennaio", ""],
        "N° PREV.": ["100", ""],
        "TOTALE PREV.": ["1000", ""],
        "ATTIVITA'": ["Manutenzione", ""],
        "ODC": ["123456", ""],
        "TCL": ["TCL1", ""],
    }
    df_actual = pd.DataFrame(data_actual)

    mock_xls = MagicMock()
    mock_xls.sheet_names = ["Dati 2025", "Ignora"]

    with patch("src.core.excel_importer.ExcelImporter._get_excel_file", return_value=mock_xls), \
         patch("src.core.excel_importer.pd.read_excel", return_value=df_actual), \
         patch("src.core.excel_importer.ExcelImporter._find_header_row", return_value=0), \
         patch("pathlib.Path.exists", return_value=True), \
         patch("src.core.excel_importer.msoffcrypto", None): 

        success, msg, rows, years = importer.import_contabilita_dati("fake.xlsx")

        if not success:
            print(f"DEBUG Failure Message: {msg}")

        assert success is True
        assert len(years) == 1
        assert years[0] == 2025
        assert len(rows) == 1
        
        assert rows[0][0] == 2025
        row_str = str(rows[0])
        assert "01/01/2025" in row_str
        assert "Manutenzione" in row_str

def test_import_contabilita_no_valid_sheets(importer):
    """Test file senza fogli validi."""
    mock_xls = MagicMock()
    mock_xls.sheet_names = ["Foglio1", "Foglio2"] 
    
    with patch("src.core.excel_importer.ExcelImporter._get_excel_file", return_value=mock_xls), \
         patch("pathlib.Path.exists", return_value=True):
         
        success, msg, _, _ = importer.import_contabilita_dati("fake.xlsx")
        assert success is False
        assert "Nessun anno importato" in msg

def test_normalize_columns_logic(importer):
    """Test robustezza normalizzazione colonne."""
    df = pd.DataFrame(columns=[" DATA  PREV. ", "  MESE", "N°PREV"])
    norm_df = importer._normalize_columns(df)
    cols = norm_df.columns.tolist()
    assert "data_prev" in cols
    assert "mese" in cols
    assert "n_prev" in cols

def test_import_giornaliere_collection(importer, tmp_path):
    """Test logica raccolta file giornaliere."""
    root = tmp_path / "Giornaliere"
    
    past_year = root / "Giornaliere 2024"
    past_year.mkdir(parents=True)
    (past_year / "valid.xls").touch()
    (past_year / "~$lock.xls").touch() 
    
    # Passiamo un dizionario vuoto come lookup_map
    tasks = importer._collect_giornaliere_tasks(root, {})
    
    assert len(tasks) >= 1
    # Verifica il primo elemento della tupla (year, path, dict)
    found_files = [str(t[1].name) for t in tasks]
    assert "valid.xls" in found_files
    assert "~$lock.xls" not in found_files
