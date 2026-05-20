import pandas as pd

from src.core.processing.certificati.steps import (
    FormatCertificatiStep,
    NormalizeCertificatiStep,
    ReadCertificatiExcelStep,
)


class TestCertificatiSteps:
    def test_detect_header_logic(self):
        """Verifica il rilevamento della riga di intestazione tramite lo step dedicato."""
        step = ReadCertificatiExcelStep()
        data = [
            ["Titolo Inutile", "", "", "", ""],
            [
                "ID-COEMI",
                "Matricola",
                "Costruttore",
                "Certificato Taratura",
                "Modello / Tipo",
            ],  # Header reale
            ["1", "M1", "C1", "CERT1", "T1"],
        ]
        df = pd.DataFrame(data)
        header_idx = step._detect_header(df)
        assert header_idx == 1

    def test_build_rename_map_logic(self):
        """Verifica che le colonne siano mappate correttamente dallo step di normalizzazione."""
        step = NormalizeCertificatiStep()
        cols = ["ID-COEMI", "Matricola\nStrumento", "Certificato", "Scadenza Certificato"]

        rename_map = step._build_rename_map(cols)

        assert rename_map["ID-COEMI"] == "id_coemi"
        assert rename_map["Matricola\nStrumento"] == "matricola"
        assert rename_map["Scadenza Certificato"] == "scadenza"

    def test_formatting_logic(self):
        """Testa la formattazione di date e stati tramite lo step dedicato."""
        step = FormatCertificatiStep()
        data = {
            "emissione": ["2023-01-01"],
            "scadenza": ["2024-01-01"],
            "stato": ["10"],  # 10 giorni alla scadenza
            "errore_max": [0.005],  # 0.5%
        }
        df = pd.DataFrame(data)
        context = {"df": df}

        step.execute(context)
        formatted_df = context["df"]

        assert formatted_df.iloc[0]["scadenza"] == "01/01/2024"
        assert formatted_df.iloc[0]["stato"] == "Scade tra 10 giorni"
        assert formatted_df.iloc[0]["errore_max"] == "0,5%"

    def test_format_stato_negative_days(self):
        """Verifica la formattazione per certificati già scaduti."""
        step = FormatCertificatiStep()
        data = {"scadenza": [""], "emissione": [""], "stato": ["-5"], "errore_max": [""]}
        df = pd.DataFrame(data)
        context = {"df": df}

        step.execute(context)
        formatted_df = context["df"]

        assert formatted_df.iloc[0]["stato"] == "Scaduto da 5 giorni"
