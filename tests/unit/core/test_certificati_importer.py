import pandas as pd

from src.core.importers.certificati import CertificatiImporter


class TestCertificatiImporter:
    def test_detect_certificati_header_logic(self):
        """Verifica il rilevamento della riga di intestazione."""
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

        header_idx = CertificatiImporter._detect_certificati_header(df)
        assert header_idx == 1

    def test_build_certificati_rename_map_partial_match(self):
        """Verifica che le colonne siano mappate anche con nomi parziali o sporchi."""
        cols = ["ID-COEMI", "Matricola\nStrumento", "Certificato", "Scadenza Certificato"]

        rename_map = CertificatiImporter._build_certificati_rename_map(cols)

        assert rename_map["ID-COEMI"] == "id_coemi"
        assert rename_map["Matricola\nStrumento"] == "matricola"
        assert rename_map["Scadenza Certificato"] == "scadenza"

    def test_apply_certificati_formatting_logic(self):
        """Testa la formattazione di date e stati di scadenza."""
        data = {
            "emissione": [pd.Timestamp("2023-01-01")],
            "scadenza": [pd.Timestamp("2024-01-01")],
            "stato": ["10"],  # 10 giorni alla scadenza
            "errore_max": [0.005],  # 0.5%
        }
        df = pd.DataFrame(data)

        formatted_df = CertificatiImporter._apply_certificati_formatting(df)

        assert formatted_df.iloc[0]["scadenza"] == "01/01/2024"
        assert formatted_df.iloc[0]["stato"] == "Scade tra 10 giorni"
        assert formatted_df.iloc[0]["errore_max"] == "0,5%"

    def test_format_stato_negative_days(self):
        """Verifica la formattazione per certificati già scaduti."""
        data = {"scadenza": [""], "emissione": [""], "stato": ["-5"]}
        df = pd.DataFrame(data)
        formatted = CertificatiImporter._apply_certificati_formatting(df)
        assert formatted.iloc[0]["stato"] == "Scaduto da 5 giorni"
