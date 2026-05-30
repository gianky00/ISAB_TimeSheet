from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from src.core.constants import Icons
from src.core.contabilita.certificati_engine import CertificatiEngine


class TestCertificatiEngine:
    @pytest.fixture
    def engine(self, tmp_path, mocker):
        mocker.patch("src.core.paths.DB_DIR", tmp_path)
        return CertificatiEngine()

    def test_load_save_exclusions(self, engine, tmp_path):
        exclusions = {"MAT1", "MAT2"}
        print_ex = {"MAT3"}

        assert engine.save_exclusions(exclusions, print_ex) is True

        # New instance to check persistence
        new_engine = CertificatiEngine()
        assert "MAT1" in new_engine._exclusions
        assert "MAT3" in new_engine._print_exclusions

    def test_calculate_days_and_status(self, engine, mocker):
        mock_now = datetime(2026, 5, 25, 0, 0, 0, tzinfo=UTC)
        mocker.patch("src.core.contabilita.certificati_engine.datetime", mocker.Mock(wraps=datetime))
        import src.core.contabilita.certificati_engine as ce_mod

        ce_mod.datetime.now.return_value = mock_now
        ce_mod.datetime.strptime = datetime.strptime

        # Case 1: Active. 25/06 - 25/05 = 31 days
        days, icon = ce_mod.CertificatiEngine.calculate_days_and_status("25/06/2026")
        assert days == 31
        assert icon == Icons.STATUS_DOT_GREEN

        # Case 2: Expiring (Yellow) - 30 days
        days, icon = ce_mod.CertificatiEngine.calculate_days_and_status("24/06/2026")
        assert days == 30
        assert icon == Icons.STATUS_DOT_YELLOW

        # Case 3: Warning (Orange) - 15 days
        days, icon = ce_mod.CertificatiEngine.calculate_days_and_status("09/06/2026")
        assert days == 15
        assert icon == Icons.STATUS_DOT_ORANGE

        # Case 4: Expired (Red)
        days, icon = ce_mod.CertificatiEngine.calculate_days_and_status("20/05/2026")
        assert days < 0
        assert icon == Icons.STATUS_DOT_RED

        # Case 5: Faulty
        days, icon = ce_mod.CertificatiEngine.calculate_days_and_status("GUASTO")
        assert days == ce_mod.CertificatiEngine.FAULTY_MARKER
        assert icon == Icons.STATUS_DOT_RED

        # Case 6: Empty
        days, icon = ce_mod.CertificatiEngine.calculate_days_and_status("")
        assert days is None
        assert icon == Icons.STATUS_DOT_GRAY

    def test_get_statistics(self, engine, mocker):
        # Data format: [IDX_ID_COEMI, IDX_CERTIFICATO, IDX_MODELLO, IDX_COSTRUTTORE, IDX_MATRICOLA, IDX_RANGE, ?, IDX_EMISSIONE, IDX_SCADENZA, ?, IDX_UBICAZIONE]
        data = [
            ["ID1", "C1", "M1", "B", "MAT1", "R", "", "20/05/2026", "25/06/2026", "", "OFFICINA"],
            ["ID2", "C2", "M2", "B", "MAT2", "R", "", "01/01/2026", "20/05/2026", "", "SEDE"],
            ["ID3", "C3", "M3", "B", "MAT3", "R", "", "", "GUASTO", "", "UFFICIO STRUMENTALE"],
            ["ID4", "C4", "M4", "B", "MAT4", "R", "", "", "", "", "UFFICIO CC"],
            ["ID5", "C5", "M5", "B", "MAT5", "R", "", "", "10/06/2026", "", "TECNICO"],
        ]

        # Mock calculate_days_and_status for consistency
        stats = CertificatiEngine.get_statistics(data)

        assert stats["totale"] == 5
        assert stats["ufficio_stru"] == 1
        assert stats["ufficio_cc"] == 1
        assert stats["officina"] == 1
        assert stats["sede"] == 1
        assert stats["tecnico"] == 1

    def test_analyze_bottlenecks(self, engine):
        stats = {"picco_imminente": {}}
        # 3 expirations on June 1st, 2 on June 3rd. Window 5 days.
        d1 = datetime(2026, 6, 1, tzinfo=UTC)
        d2 = datetime(2026, 6, 3, tzinfo=UTC)
        d3 = datetime(2026, 6, 10, tzinfo=UTC)

        expiration_map = {d1: 3, d2: 2, d3: 1}

        CertificatiEngine._analyze_bottlenecks(stats, expiration_map)

        assert stats["picco_imminente"]["count"] == 5
        assert stats["picco_imminente"]["inizio"] == "01/06"

    @patch("src.core.contabilita.certificati_engine.get_config_value")
    @patch("os.walk")
    def test_find_certificate_path(self, mock_walk, mock_config, tmp_path):
        mock_config.return_value = str(tmp_path)
        mock_walk.return_value = [
            (str(tmp_path), ["subdir"], ["123.pdf", "other.txt"]),
            (str(tmp_path / "subdir"), [], ["CERTIFICATO 456.PDF"]),
        ]

        assert CertificatiEngine.find_certificate_path("123") is not None
        assert "123.pdf" in CertificatiEngine.find_certificate_path("123")
        assert CertificatiEngine.find_certificate_path("456") is not None
        assert CertificatiEngine.find_certificate_path("999") is None

    def test_parse_filename(self, engine):
        res = engine._parse_filename("MAT123_CERT456_MOD789.pdf")
        assert res["matricola"] == "MAT123"
        assert res["certificato"] == "CERT456"
        assert res["modello"] == "MOD789"

        res_dig = engine._parse_filename("MAT1_CERT2_DigitalMod_10bar.pdf")
        assert res_dig["range"] == "10bar"

    def test_group_data_by_id_coemi(self, engine):
        data = [
            ["ID1", "C1", "M1", "B", "MAT1", "R", "", "", "25/06/2026", "", ""],
            [None, "C2", "M2", "B", "MAT2", "R", "", "", "25/06/2026", "", ""],  # Use MAT2 as key
            ["", "", "", "", "", "", "", "", "", "", ""],  # Sconosciuto
        ]
        groups = engine.group_data_by_id_coemi(data)
        assert "ID1" in groups
        assert "MAT2" in groups
        assert "Sconosciuto" in groups

    def test_prepare_groups_with_priority(self, engine):
        groups = {
            "G1": [
                ["ID1", "C1", "M1", "B", "MAT1", "R", "", "01/01/2026", "25/06/2026", "", ""],
                ["ID1", "C1", "M1", "B", "MAT1", "R", "", "01/02/2026", "25/07/2026", "", ""],  # Latest
            ]
        }
        processed = engine.prepare_groups_with_priority(groups)
        assert len(processed) == 1
        assert processed[0]["group_key"] == "G1"
        assert processed[0]["id_coemi"] == "ID1"
        # Check sort order (latest first)
        assert processed[0]["certificates"][0][7] == "01/02/2026"

    @patch("win32com.client.Dispatch")
    def test_generate_outlook_draft(self, mock_dispatch, engine):
        certs = [
            {"id": "ID1", "modello": "M1", "matricola": "MAT1", "scadenza": "25/06/2026", "giorni": 31},
            {"id": "ID2", "modello": "M2", "matricola": "MAT2", "scadenza": "20/05/2026", "giorni": -5},
        ]
        mock_outlook = MagicMock()
        mock_dispatch.return_value = mock_outlook
        mock_mail = MagicMock()
        mock_outlook.CreateItem.return_value = mock_mail

        assert engine.generate_outlook_draft(certs) is True
        assert mock_mail.Display.called
        # Check sorting in draft (ID2 should be first because days -5 < 31)
        assert "ID2" in mock_mail.HTMLBody

    def test_parse_parent_label_variants(self, engine):
        # Extended with range
        text = "ID1  •  COST  •  MOD  •  10BAR  •  MAT1  •  OK"
        res = engine.parse_parent_label(text)
        assert res["range"] == "10BAR"
        assert res["matricola"] == "MAT1"

        # Reduced
        text = "COST  •  MOD  •  MAT1  •  OK"
        res = engine.parse_parent_label(text)
        assert res["id_coemi"] == ""
        assert res["matricola"] == "MAT1"

    def test_get_col_safe(self, engine):
        row = ["A", None, "C"]
        assert engine.get_col_safe(row, 0) == "A"
        assert engine.get_col_safe(row, 1) == ""
        assert engine.get_col_safe(row, 5) == ""
