
import pytest

from src.core.contabilita.certificati_engine import CertificatiEngine


class TestCertificatiEngine:
    @pytest.fixture
    def engine(self):
        return CertificatiEngine()

    def test_parse_parent_label_standard(self, engine):
        label = "ID123  •  CostruttoreX  •  ModelloY  •  MatricolaZ  •  Attivo"
        res = engine.parse_parent_label(label)
        assert res["id_coemi"] == "ID123"
        assert res["costruttore"] == "CostruttoreX"
        assert res["modello"] == "ModelloY"
        assert res["matricola"] == "MatricolaZ"
        assert res["range"] == ""

    def test_parse_parent_label_with_range(self, engine):
        label = "ID456  •  CostruttoreA  •  Manometro Digitale  •  0-10 bar  •  Mat123  •  Attivo"
        res = engine.parse_parent_label(label)
        assert res["id_coemi"] == "ID456"
        assert res["costruttore"] == "CostruttoreA"
        assert res["modello"] == "Manometro Digitale"
        assert res["range"] == "0-10 bar"
        assert res["matricola"] == "Mat123"

    def test_parse_parent_label_with_exclusion_marker(self, engine):
        label = "ID789  •  C  •  M  •  MatricolaK  •  Attivo  [ESCLUSO]"
        res = engine.parse_parent_label(label)
        assert res["matricola"] == "MatricolaK"

        label_print = "ID789  •  C  •  M  •  MatricolaK  •  Attivo  [NON STAMPARE]"
        res_print = engine.parse_parent_label(label_print)
        assert res_print["matricola"] == "MatricolaK"

    def test_parse_parent_label_short(self, engine):
        # Caso con meno parti del previsto
        label = "Costruttore  •  Modello  •  Matricola  •  Stato"
        res = engine.parse_parent_label(label)
        assert res["costruttore"] == "Costruttore"
        assert res["modello"] == "Modello"
        assert res["matricola"] == "Matricola"

    def test_parse_parent_label_empty(self, engine):
        res = engine.parse_parent_label("")
        assert res["id_coemi"] == ""
        assert res["matricola"] == ""
        assert "range" in res
