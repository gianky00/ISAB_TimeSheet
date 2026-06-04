from unittest.mock import patch

import pandas as pd

from src.application.services.processing.certificati.steps import (
    FormatCertificatiStep,
    NormalizeCertificatiStep,
    ReadCertificatiExcelStep,
    SyncCertificatiStep,
)


class TestCertificatiSteps:
    @patch("src.application.services.processing.certificati.steps.pd.ExcelFile")
    @patch("src.application.services.processing.certificati.steps.pd.read_excel")
    def test_read_certificati_excel_step(self, mock_read, mock_xls, fs):
        fs.create_file("cert.xlsx")
        mock_xls.return_value.sheet_names = ["Strumenti Campione"]

        # Mock preview e df finale
        mock_read.side_effect = [
            pd.DataFrame([["ID-COEMI", "CERTIFICATO", "SCADENZA"]]),  # Preview
            pd.DataFrame({"ID-COEMI": ["1"], "CERTIFICATO": ["C1"], "SCADENZA": ["2025"]}),  # Data
        ]

        step = ReadCertificatiExcelStep()
        context = {"file_path": "cert.xlsx"}
        step.execute(context)

        assert context["sheet_name"] == "Strumenti Campione"
        assert context["df"].iloc[0]["ID-COEMI"] == "1"

    def test_normalize_certificati_step(self):
        # Setup df con colonne da mappare
        df = pd.DataFrame(
            {
                "ID STRUMENTO": ["COE1", ""],
                "N. CERT.": ["CERT1", "CERT2"],
                "MATRICOLA": ["MAT1", ""],
                "ERR %": ["0,5", "1"],
                "ALTRO": ["X", "Y"],
            }
        )

        step = NormalizeCertificatiStep()
        context = {"df": df}
        step.execute(context)

        normalized_df = context["df"]
        assert "id_coemi" in normalized_df.columns
        assert "certificato" in normalized_df.columns
        assert normalized_df.iloc[0]["id_coemi"] == "COE1"
        # Verifica FFILL su id_coemi e matricola
        assert normalized_df.iloc[1]["id_coemi"] == "COE1"
        assert normalized_df.iloc[1]["matricola"] == "MAT1"

    def test_format_certificati_step(self):
        df = pd.DataFrame(
            {
                "id_coemi": ["C1"],
                "scadenza": ["2023-12-31"],
                "emissione": ["2023-01-01"],
                "stato": ["10"],
                "errore_max": ["0.005"],
            }
        )

        step = FormatCertificatiStep()
        context = {"df": df}
        step.execute(context)

        assert context["success"] is True
        formatted_df = context["df"]
        assert formatted_df.iloc[0]["scadenza"] == "31/12/2023"
        assert formatted_df.iloc[0]["stato"] == "Scade tra 10 giorni"
        assert formatted_df.iloc[0]["errore_max"] == "0,5%"

    @patch("src.application.services.data_synchronizer.DataSynchronizer.sync_certificati_campione")
    def test_sync_certificati_step(self, mock_sync):
        mock_sync.return_value = (5, 2)
        step = SyncCertificatiStep()
        context = {
            "success": True,
            "rows": [("C1", "CERT1", "M1", "COST1", "MAT1", "R1", "E1", "EM1", "SC1", "ST1")],
        }

        step.execute(context)

        assert context["total_added"] == 5
        assert context["total_removed"] == 2
