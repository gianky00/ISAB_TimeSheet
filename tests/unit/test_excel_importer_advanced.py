import io
import json
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.core.excel_importer import ExcelImporter

class TestExcelImporterAdvanced:
    def test_identify_sheet_year_edge_cases(self):
        """Verifica l'identificazione dell'anno in casi limite."""
        assert ExcelImporter._identify_sheet_year("2024") == 2024
        assert ExcelImporter._identify_sheet_year("Dati") == datetime.now().year
        assert ExcelImporter._identify_sheet_year("Foglio 1") is None
        assert ExcelImporter._identify_sheet_year("2024_Riepilogo") == 2024
        # Fuori range
        assert ExcelImporter._identify_sheet_year("1999") is None
        assert ExcelImporter._identify_sheet_year("2101") is None

    def test_normalize_columns_heuristics(self):
        """Verifica le euristiche di rinomina colonne."""
        df = pd.DataFrame(columns=["DATA PREV", "NUM PREV", "ALTRO"])
        df_norm = ExcelImporter._normalize_columns(df)
        assert "data_prev" in df_norm.columns
        assert "n_prev" in df_norm.columns
        assert "ALTRO" in df_norm.columns

    def test_decrypt_if_encrypted_failure(self, tmp_path):
        """Verifica che la decrittazione fallita restituisca il file originale."""
        file_path = tmp_path / "test.xlsx"
        file_path.write_text("dummy")
        
        # Simula msoffcrypto presente ma file non valido
        with patch("msoffcrypto.OfficeFile") as mock_office:
            mock_office.side_effect = Exception("Not an office file")
            result, encrypted = ExcelImporter._decrypt_if_encrypted(file_path)
            assert result == file_path
            assert encrypted is False

    def test_process_scarico_ore_row_colors(self):
        """Verifica l'estrazione dei colori RGB dalla riga Excel."""
        mock_cell = MagicMock()
        mock_cell.value = "Test"
        mock_cell.font.color.type = "rgb"
        mock_cell.font.color.rgb = "FFFF0000" # Rosso
        mock_cell.fill.patternType = "solid"
        mock_cell.fill.start_color.type = "rgb"
        mock_cell.fill.start_color.rgb = "FF00FF00" # Verde
        
        # Mock row con dati minimi per passare i check
        row = [MagicMock() for _ in range(11)]
        for c in row: c.value = "X"; c.font = None; c.fill = None
        
        # Colonna 3 (ODC) e 4 (POS) e 7 (TOTALE ORE) sono obbligatorie
        row[0].value = "2024-01-01"
        row[1].value = "P1" # Pers1
        row[3].value = "5400123" # ODC
        row[4].value = "10" # POS
        row[7].value = "8.0" # TOTALE ORE
        
        # Metti la cella colorata in ODC
        row[3] = mock_cell
        
        col_keys = [
            "data", "pers1", "pers2", "odc", "pos", 
            "dalle", "alle", "totale_ore", "descrizione", 
            "finito", "commessa"
        ]
        
        db_row = ExcelImporter._process_scarico_ore_row(row, col_keys)
        assert db_row is not None
        styles_json = db_row[-1]
        styles = json.loads(styles_json)
        
        assert "odc" in styles
        assert styles["odc"]["fg"] == "#FF0000"
        assert styles["odc"]["bg"] == "#00FF00"

    def test_scan_scarico_ore_rows_zip_logic(self, tmp_path):
        """Verifica la scansione rapida delle righe tramite metadati XML zip."""
        excel_zip = tmp_path / "test.xlsx"
        import zipfile
        
        with zipfile.ZipFile(excel_zip, 'w') as z:
            # XML minimale che contiene la dimensione del foglio
            sheet_content = '<worksheet><dimension ref="A1:K150000"/></worksheet>'
            z.writestr('xl/worksheets/sheet1.xml', sheet_content)
            
        rows = ExcelImporter.scan_scarico_ore_rows(str(excel_zip))
        assert rows == 150000

    def test_process_single_giornaliera_odc_extraction(self, tmp_path):
        """Verifica l'estrazione di ODC/Commessa dalle descrizioni nelle giornaliere."""
        file_path = tmp_path / "Giornaliera.xlsx"
        
        # Mock pandas read_excel
        # Il metodo scarta l'ultima riga con iloc[:-1], quindi ne aggiungiamo una dummy
        mock_df = pd.DataFrame({
            "DATA": ["2024-01-01", "TOTALE"],
            "PERSONALE": ["Rossi", ""],
            "DESCRIZIONE ATTIVITA'": ["Lavoro su commessa 24/123", ""],
            "ODC": ["", ""],
            "N° PDL": ["123", ""],
            "INIZIO": ["08:00", ""],
            "FINE": ["17:00", ""],
            "ORE": ["9.0", ""],
            "consuntivo": ["PREV1", ""]
        })
        
        with patch("pandas.read_excel", return_value=mock_df):
            year, rows, err = ExcelImporter._process_single_giornaliera((2024, file_path, {}))
            
            assert err is None
            assert len(rows) == 1
            # ODC (indice 5 nella tupla finale) dovrebbe contenere 24/123
            # Tupla: (year, data, personale, descrizione, tcl, odc, pdl, inizio, fine, ore, n_prev, nome_file)
            assert rows[0][5] == "24/123"

    def test_process_certificati_df_stato_formatting(self):
        """Verifica la formattazione dello stato (giorni alla scadenza) nei certificati."""
        df = pd.DataFrame({
            "Certificato": ["CERT1"],
            "Stato Certificato": ["10.2"], # Scade tra 10 giorni
            "Scadenza Certificato": ["2024-12-31"]
        })
        # Mock mapping columns
        with patch.dict(ExcelImporter.CERTIFICATI_CAMPIONE_MAPPING, {"Certificato": "certificato", "Stato Certificato": "stato", "Scadenza Certificato": "scadenza"}):
            res_bool, msg, rows = ExcelImporter._process_certificati_df(df, "Sheet", 0)
            
            # CERTIFICATI_CAMPIONE_MAPPING order: modello, costruttore, matricola, range, errore, certificato, scadenza, emissione, id_coemi, stato
            # Stato è l'indice 9
            assert "Scade tra 10 giorni" in rows[0][9]

    def test_import_contabilita_dati_no_valid_sheets(self, tmp_path, mocker):
        """Verifica errore se non ci sono fogli con anni validi."""
        file_path = tmp_path / "empty.xlsx"
        file_path.write_text("dummy")
        
        mock_xls = mocker.MagicMock()
        mock_xls.sheet_names = ["Foglio1", "Note"]
        
        mocker.patch("pandas.ExcelFile", return_value=mock_xls)
        mocker.patch.object(ExcelImporter, "_decrypt_if_encrypted", return_value=(file_path, False))
        
        res, msg, rows, years = ExcelImporter.import_contabilita_dati(str(file_path))
        assert res is False
        assert "Nessun anno importato" in msg