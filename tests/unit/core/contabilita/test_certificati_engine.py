from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.constants import Icons, StatoCertificatoLabel, UbicazioneStrumenti
from src.core.contabilita.certificati_engine import CertificatiEngine
from src.core.contabilita_queries import ContabilitaQueries


@pytest.fixture
def engine(fs) -> CertificatiEngine:
    db_dir = Path("data/db")
    fs.create_dir(db_dir)
    with patch("src.core.contabilita.certificati_engine.DB_DIR", db_dir):
        return CertificatiEngine()


@pytest.fixture
def mock_now():
    with patch("src.core.contabilita.certificati_engine.datetime") as mock_datetime:
        # Pass through strptime to the real datetime
        mock_datetime.strptime.side_effect = lambda *args, **kw: datetime.strptime(*args, **kw)
        # Mock now to return exactly midnight
        now = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
        mock_datetime.now.return_value = now
        yield now


def test_load_save_exclusions(engine: CertificatiEngine, fs) -> None:
    assert engine._exclusions == set()
    assert engine._print_exclusions == set()
    success = engine.save_exclusions({"123", "456"}, {"789"})
    assert success is True
    engine2 = CertificatiEngine()
    engine2.load_exclusions()
    assert engine2._exclusions == {"123", "456"}
    assert engine2._print_exclusions == {"789"}
    engine.exclusions_file.unlink()
    fs.create_file(engine.exclusions_file, contents="{invalid json}")
    engine2.load_exclusions()
    assert engine2._exclusions == set()
    assert engine2._print_exclusions == set()


def test_calculate_days_and_status(mock_now) -> None:
    days, icon = CertificatiEngine.calculate_days_and_status("")
    assert days is None
    assert icon == Icons.STATUS_DOT_GRAY
    days, icon = CertificatiEngine.calculate_days_and_status("GUASTO")
    assert days == CertificatiEngine.FAULTY_MARKER
    assert icon == Icons.STATUS_DOT_RED
    future_date = mock_now + timedelta(days=40)
    future_str = future_date.strftime("%d/%m/%Y")
    days, icon = CertificatiEngine.calculate_days_and_status(future_str)
    assert days == 40
    assert icon == Icons.STATUS_DOT_GREEN
    warning_date = mock_now + timedelta(days=10)
    warning_str = warning_date.strftime("%d/%m/%Y")
    days, icon = CertificatiEngine.calculate_days_and_status(warning_str)
    assert days == 10
    assert icon == Icons.STATUS_DOT_ORANGE
    past_date = mock_now - timedelta(days=5)
    past_str = past_date.strftime("%d/%m/%Y")
    days, icon = CertificatiEngine.calculate_days_and_status(past_str)
    assert days == -5
    assert icon == Icons.STATUS_DOT_RED


def test_format_days_text_short() -> None:
    assert StatoCertificatoLabel.GUASTO in CertificatiEngine.format_days_text_short(
        CertificatiEngine.FAULTY_MARKER
    )
    assert CertificatiEngine.format_days_text_short(None) == StatoCertificatoLabel.SENZA_SCADENZA
    assert StatoCertificatoLabel.SCADUTO in CertificatiEngine.format_days_text_short(-10)
    assert StatoCertificatoLabel.IN_SCADENZA in CertificatiEngine.format_days_text_short(10)
    assert StatoCertificatoLabel.IN_SCADENZA in CertificatiEngine.format_days_text_short(25)
    assert StatoCertificatoLabel.ATTIVO in CertificatiEngine.format_days_text_short(50)


def test_get_statistics(mock_now) -> None:
    active_date = (mock_now + timedelta(days=60)).strftime("%d/%m/%Y")
    warning_date = (mock_now + timedelta(days=10)).strftime("%d/%m/%Y")
    expired_date = (mock_now - timedelta(days=5)).strftime("%d/%m/%Y")

    def make_row(scadenza: str, ubicazione: str) -> list[str]:
        r = [""] * 15
        r[CertificatiEngine.IDX_SCADENZA] = scadenza
        r[CertificatiEngine.IDX_UBICAZIONE] = ubicazione
        return r

    data = [
        make_row(active_date, UbicazioneStrumenti.UFFICIO_STRU.value),
        make_row(warning_date, UbicazioneStrumenti.OFFICINA.value),
        make_row(expired_date, UbicazioneStrumenti.SEDE.value),
        make_row("GUASTO", "TECNICO PIPPO"),
        make_row("", UbicazioneStrumenti.ASSENTE.value),
        make_row(active_date, UbicazioneStrumenti.UFFICIO_CC.value),
    ]

    stats = CertificatiEngine.get_statistics(data)
    assert stats["totale"] == 6
    assert stats["attivi"] == 2
    assert stats["in_scadenza"] == 1
    assert stats["scaduti"] == 1
    assert stats["guasti"] == 1
    assert stats["senza_data"] == 1


def test_generate_outlook_draft(engine: CertificatiEngine) -> None:
    try:
        import win32com.client  # noqa: F401
    except ImportError:
        pytest.skip("win32com not available")

    with patch("win32com.client.Dispatch") as mock_dispatch:
        mock_outlook = MagicMock()
        mock_mail = MagicMock()
        mock_outlook.CreateItem.return_value = mock_mail
        mock_dispatch.return_value = mock_outlook

        certs = [
            {"id": "1", "modello": "A", "matricola": "M1", "scadenza": "01/01/2020", "giorni": -10},
            {"id": "2", "modello": "B", "matricola": "M2", "scadenza": "N/D", "giorni": None},
            {"id": "3", "modello": "C", "matricola": "M3", "scadenza": "01/01/2025", "giorni": 10},
        ]

        res = engine.generate_outlook_draft(certs)
        assert res is True
        mock_mail.Display.assert_called_once()
        html_body = mock_mail.HTMLBody
        assert "SCADUTO" in html_body
        assert "Scade tra 10 gg" in html_body
        assert "DATA NON DISPONIBILE" in html_body

        assert engine.generate_outlook_draft([]) is False

        mock_dispatch.side_effect = Exception("Outlook not installed")
        assert engine.generate_outlook_draft(certs) is False


def test_format_errore_max() -> None:
    assert CertificatiEngine.format_errore_max(None) == ""
    assert CertificatiEngine.format_errore_max("") == ""
    assert CertificatiEngine.format_errore_max(0.015) == "1,5%"
    assert CertificatiEngine.format_errore_max("0.02") == "2%"
    assert CertificatiEngine.format_errore_max("invalid") == "invalid"


@patch("src.core.contabilita.certificati_engine.get_config_value")
def test_find_certificate_path(mock_get_config, fs) -> None:
    cert_dir = Path("C:/certificati")
    fs.create_dir(cert_dir)
    fs.create_file(cert_dir / "12345.pdf")
    fs.create_file(cert_dir / "CERTIFICATO 67890.pdf")
    fs.create_file(cert_dir / "altro_555.pdf")

    mock_get_config.return_value = str(cert_dir)
    assert CertificatiEngine.find_certificate_path("12345") == str(cert_dir / "12345.pdf")
    assert CertificatiEngine.find_certificate_path("67890") == str(cert_dir / "CERTIFICATO 67890.pdf")
    assert CertificatiEngine.find_certificate_path("555") == str(cert_dir / "altro_555.pdf")
    assert CertificatiEngine.find_certificate_path("999") is None

    mock_get_config.return_value = ""
    assert CertificatiEngine.find_certificate_path("12345") is None


def test_parse_parent_label() -> None:
    res = CertificatiEngine.parse_parent_label("ID1  •  Cost1  •  Mod1  •  Mat1  •  Attivo [ESCLUSO]")
    assert res["id_coemi"] == "ID1"
    assert res["costruttore"] == "Cost1"
    assert res["modello"] == "Mod1"
    assert res["matricola"] == "Mat1"
    assert res["range"] == ""

    res = CertificatiEngine.parse_parent_label(
        "ID2  •  Cost2  •  ModDigital  •  0-10bar  •  Mat2  •  Scaduto"
    )
    assert res["id_coemi"] == "ID2"
    assert res["range"] == "0-10bar"
    assert res["matricola"] == "Mat2"

    res = CertificatiEngine.parse_parent_label("Cost3  •  Mod3  •  Mat3  •  Guasto")
    assert res["costruttore"] == "Cost3"
    assert res["modello"] == "Mod3"
    assert res["matricola"] == "Mat3"

    res = CertificatiEngine.parse_parent_label("")
    assert res["id_coemi"] == ""


def test_parse_filename(engine: CertificatiEngine) -> None:
    res = engine._parse_filename("Mat1_Cert1_Mod1.pdf")
    assert res["matricola"] == "Mat1"
    assert res["certificato"] == "Cert1"
    assert res["modello"] == "Mod1"
    assert res["range"] == ""

    res2 = engine._parse_filename("Mat2_Cert2_ModDigital_0-10.PDF")
    assert res2["matricola"] == "Mat2"
    assert res2["range"] == "0-10"


def test_group_data_by_id_coemi(engine: CertificatiEngine) -> None:
    idx_id = ContabilitaQueries.CERT_IDX_ID_STRUMENTO
    idx_mat = ContabilitaQueries.CERT_IDX_MATRICOLA
    max_idx = max(idx_id, idx_mat) + 1

    def make_row(id_val: str, mat_val: str) -> list[str]:
        r = [""] * max_idx
        r[idx_id] = id_val
        r[idx_mat] = mat_val
        return r

    data = [
        make_row("ID1", "M1"),
        make_row("ID1", "M1"),
        make_row("", "M2"),
        make_row("", ""),
    ]

    groups = engine.group_data_by_id_coemi(data)
    assert "ID1" in groups
    assert len(groups["ID1"]) == 2
    assert "M2" in groups
    assert "Sconosciuto" in groups


def test_prepare_groups_with_priority(mock_now, engine: CertificatiEngine) -> None:
    idx_scad = ContabilitaQueries.CERT_IDX_SCADENZA
    idx_id = ContabilitaQueries.CERT_IDX_ID_STRUMENTO
    max_idx = max(idx_scad, idx_id) + 1

    def make_row(scad: str, id_val: str) -> list[str]:
        r = [""] * max_idx
        r[idx_scad] = scad
        r[idx_id] = id_val
        return r

    future = (mock_now + timedelta(days=20)).strftime("%d/%m/%Y")

    groups = {
        "ID1": [make_row(future, "ID1")],
        "ID2": [make_row("GUASTO", "ID2")],
        "ID3": [make_row("", "ID3")],
    }

    res = engine.prepare_groups_with_priority(groups)
    assert len(res) == 3
    res_id1 = next(x for x in res if x["group_key"] == "ID1")
    assert res_id1["days"] == 20
    assert res_id1["priority"] == 20

    res_id2 = next(x for x in res if x["group_key"] == "ID2")
    assert res_id2["days"] == engine.FAULTY_MARKER

    res_id3 = next(x for x in res if x["group_key"] == "ID3")
    assert res_id3["days"] is None
    assert res_id3["priority"] == 9999
