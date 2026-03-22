from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.core.importers.contabilita import ContabilitaImporter


class TestContabilitaImporter:
    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame(
            {
                "DATA PREV.": ["2024-01-01", "2024-02-01"],
                "MESE": ["Gennaio", "Febbraio"],
                "N° PREV.": ["123", "124"],
                "TOTALE PREV.": ["1500.50", "2000"],
                "ATTIVITA'": ["A1", "A2"],
                "ODC": ["O1", "O2"],
            }
        )

    def test_normalize_columns_mapping(self, sample_df):
        """Verifica che le colonne vengano mappate correttamente ai nomi DB."""
        # Aggiungiamo una colonna con nome leggermente diverso
        sample_df["DATA PREVENTIVO"] = sample_df["DATA PREV."]
        del sample_df["DATA PREV."]

        importer = ContabilitaImporter()
        normalized_df = importer._normalize_columns(sample_df)

        assert "data_prev" in normalized_df.columns
        assert "n_prev" in normalized_df.columns
        assert "totale_prev" in normalized_df.columns

    def test_find_header_row_success(self, sample_df, tmp_path):
        """Verifica il rilevamento automatico della riga di intestazione."""
        # Creiamo un file excel dove l'header è alla riga 5 (indice 4)
        file_path = tmp_path / "test_header.xlsx"
        # Dummy rows
        dummy = pd.DataFrame([[""] * 6] * 4)
        full_df = pd.concat([dummy, sample_df.columns.to_frame().T, sample_df], ignore_index=True)

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            full_df.to_excel(writer, sheet_name="2024", index=False, header=False)

        # Dobbiamo mockare l'oggetto xls di pandas (ExcelFile)
        xls = pd.ExcelFile(file_path)
        header_idx = ContabilitaImporter._find_header_row(xls, "2024")

        assert header_idx == 4

    def test_process_single_sheet_numeric_conversion(self):
        """Verifica che totale_prev e ore_sp siano convertiti correttamente in float."""
        # Creiamo un DF con TUTTE le colonne previste dal mapping
        # Aggiungiamo 2 righe: la prima è dati veri, la seconda verrà scartata da iloc[:-1]
        data = {
            "DATA PREV.": ["2024-01-01", "TOTALI"],
            "MESE": ["GEN", ""],
            "N° PREV.": ["1", ""],
            "TOTALE PREV.": ["1.234,56", "1234.56"],
            "ATTIVITA'": ["TEST", ""],
            "TCL": ["X", ""],
            "ODC": ["O1", ""],
            "STATO ATTIVITA'": ["OK", ""],
            "TIPOLOGIA": ["T1", ""],
            "ORE SP": ["10.5", "10.5"],
            "RESA": ["0.85", ""],
            "ANNOTAZIONI": ["", ""],
            "INDIRIZZO CONSUNTIVO": ["", ""],
            "NOME FILE": ["test.pdf", ""],
        }
        df = pd.DataFrame(data)

        # Mock per _find_header_row e read_excel
        with (
            patch.object(ContabilitaImporter, "_find_header_row", return_value=0),
            patch("pandas.read_excel", return_value=df),
            patch("src.core.importers.contabilita.validate_contabilita", side_effect=lambda x: x),
        ):  # Bypass pandera per ora
            res = ContabilitaImporter._process_single_sheet(MagicMock(), "2024", 2024)

            assert len(res) == 1
            row = res[0]
            # Struttura attesa (indice):
            # 0: year (2024)
            # 1: data_prev (data_prev)
            # 2: mese (mese)
            # 3: n_prev (n_prev)
            # 4: totale_prev (totale_prev) -> 1234.56
            # 5: attivita
            # 6: tcl
            # 7: odc
            # 8: stato_attivita
            # 9: tipologia
            # 10: ore_sp -> 10.5

            assert row[0] == 2024
            assert row[4] == 1234.56  # Verifichiamo conversione IT
            assert row[10] == 10.5  # ORE SP (indice 10)

    def test_import_contabilita_dati_no_valid_sheets(self, tmp_path):
        """Verifica errore se non ci sono fogli con anni nel nome."""
        file_path = tmp_path / "empty.xlsx"
        pd.DataFrame().to_excel(file_path, sheet_name="Foglio1")

        success, msg, _rows, _years = ContabilitaImporter.import_contabilita_dati(str(file_path))
        assert success is False
        assert "Nessun anno" in msg

    def test_scan_sheets_fast(self, tmp_path):
        """Verifica il conteggio veloce dei fogli tramite XML."""
        file_path = tmp_path / "fast_scan.xlsx"
        # Creiamo un file con 2 fogli "annuali" e 1 no
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            pd.DataFrame().to_excel(writer, sheet_name="2023")
            pd.DataFrame().to_excel(writer, sheet_name="2024")
            pd.DataFrame().to_excel(writer, sheet_name="Note")

        count = ContabilitaImporter.scan_sheets(str(file_path))
        assert count == 2
