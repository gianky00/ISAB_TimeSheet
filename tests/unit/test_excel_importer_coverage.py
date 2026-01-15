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
    # 1. Preview DF (per _find_header_row)
    # Simula un foglio raw dove la prima riga contiene le intestazioni
    data_preview = {
        0: ["DATA PREV.", "MESE", "N° PREV.", "TOTALE PREV.", "ATTIVITA'", "ODC", "TCL"],
        1: ["01/01/2025", "Gennaio", "100", "1000", "Manutenzione", "123456", "TCL1"]
    }
    df_preview = pd.DataFrame(data_preview).T # Transpose per avere le intestazioni come prima riga di dati

    # 2. Actual DF (per _process_single_sheet)
    data_actual = {
        "DATA PREV.": ["01/01/2025"],
        "MESE": ["Gennaio"],
        "N° PREV.": ["100"],
        "TOTALE PREV.": ["1000"],
        "ATTIVITA'": ["Manutenzione"],
        "ODC": ["123456"],
        "TCL": ["TCL1"],
    }
    df_actual = pd.DataFrame(data_actual)
    
    mock_xls = MagicMock()
    mock_xls.sheet_names = ["Dati 2025", "Ignora"]
    
    # side_effect per pd.read_excel:
    # 1. Chiamata da _find_header_row -> df_preview
    # 2. Chiamata da _process_single_sheet -> df_actual
    
    with patch("src.core.excel_importer.ExcelImporter._get_excel_file", return_value=mock_xls), \
         patch("src.core.excel_importer.pd.read_excel", side_effect=[df_preview, df_actual]), \
         patch("pathlib.Path.exists", return_value=True), \
         patch("src.core.excel_importer.msoffcrypto", None): # Disable encryption check
         
        success, msg, rows, years = importer.import_contabilita_dati("fake.xlsx")
        
        # Debug info if fails
        if not success:
            print(f"DEBUG Failure Message: {msg}")

        assert success is True
        assert len(years) == 1
        assert years[0] == 2025
        assert len(rows) == 1
        
        # Verifica contenuto
        # Row format: (year, data_prev, mese, n_prev, totale_prev, attivita, tcl, odc, ...)
        # Colonne ordinate secondo COLUMNS_MAPPING: 
        # data_prev, mese, n_prev, totale_prev, attivita, tcl, odc, ...
        # Ricordiamo che la prima colonna aggiunta è 'year'
        
        # indice 0: year
        assert rows[0][0] == 2025
        
        # Indici successivi dipendono dall'ordine di COLUMNS_MAPPING values()
        # "DATA PREV." -> "data_prev"
        # "MESE" -> "mese"
        # "N° PREV." -> "n_prev"
        
        # Verifichiamo che i dati ci siano
        row_str = str(rows[0])
        assert "01/01/2025" in row_str
        assert "Manutenzione" in row_str
        assert "123456" in row_str

def test_import_contabilita_no_valid_sheets(importer):
    """Test file senza fogli validi."""
    mock_xls = MagicMock()
    mock_xls.sheet_names = ["Foglio1", "Foglio2"] # No year or keywords
    
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
    
    # Create past year folder (valid)
    past_year = root / "Giornaliere 2024"
    past_year.mkdir(parents=True)
    (past_year / "valid.xls").touch()
    (past_year / "~$lock.xls").touch() # Should be ignored
    
    tasks = importer._collect_giornaliere_tasks(root, {})
    
    # Should find at least 1 task
    assert len(tasks) >= 1
    found_files = [str(t[1].name) for t in tasks]
    assert "valid.xls" in found_files
    assert "~$lock.xls" not in found_files
