from datetime import UTC, datetime
from unittest.mock import patch

import pytest

from src.core.constants import Icons
from src.core.contabilita.certificati_engine import CertificatiEngine
from src.gui.dialogs.certificati_analysis_dialog import ScadenzeAnalysisDialog
from src.gui.widgets.contabilita.certificati_tab import (
    CertificatiCampioneTab,
)


class TestCertificatiGUI:
    @pytest.fixture(autouse=True)
    def setup_qt(self, qtbot):
        self.qtbot = qtbot

    @pytest.fixture(autouse=True)
    def mock_sync_worker(self, mocker):
        """Forza il worker certificati ad essere sincrono."""

        def mock_start(instance):
            instance.run()

        mocker.patch("src.gui.workers.certificati_worker.CertificatiWorker.start", mock_start)

    @pytest.fixture
    def cert_tab(self):
        with patch(
            "src.core.contabilita_manager.ContabilitaManager.get_certificati_campione_data"
        ) as mock_data:
            mock_data.return_value = []
            tab = CertificatiCampioneTab()
            self.qtbot.addWidget(tab)
            return tab

    def test_calculate_days_and_status_logic(self):
        with patch("src.core.contabilita.certificati_engine.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 1, 1, tzinfo=UTC)
            mock_dt.strptime = datetime.strptime

            days, icon = CertificatiEngine.calculate_days_and_status("01/12/2023")
            assert days is not None and days < 0
            assert icon == Icons.STATUS_DOT_RED

    def test_format_days_text_short(self):
        assert "Scaduto" in CertificatiEngine.format_days_text_short(-10)
        assert "Attivo" in CertificatiEngine.format_days_text_short(60)

    def test_exclusions_engine_io(self, tmp_path):
        test_file = tmp_path / "exclusions.json"
        with patch("src.core.contabilita.certificati_engine.CertificatiEngine.exclusions_file", test_file):
            engine = CertificatiEngine()
            engine.save_exclusions({"MAT-001"})
            assert test_file.exists()

    def test_analysis_dialog_init(self):
        test_data = [
            {"matricola": "M1", "days": -5, "modello": "Mod1", "costruttore": "C1"},
        ]
        dialog = ScadenzeAnalysisDialog(test_data)
        self.qtbot.addWidget(dialog)
        assert "Analisi Scadenze" in dialog.windowTitle()

    def test_load_data_grouping(self, cert_tab):
        """Testa il raggruppamento dei certificati nel Tab UI."""
        mock_groups = [
            {
                "id_coemi": "ID1",
                "costruttore": "Costr A",
                "modello": "Mod A",
                "matricola": "MAT-1",
                "range_strumento": "0-10",
                "days": 50,
                "priority": 50,  # Required by worker for sorting
                "icon": Icons.STATUS_DOT_GREEN,
                "certificates": [
                    (
                        "ID1",
                        "CERT-1",
                        "Mod A",
                        "Costr A",
                        "MAT-1",
                        "0-10",
                        "1%",
                        "10/02/2025",
                        "10/02/2026",
                        "Attivo",
                        "SUD",
                        "Note",
                    )
                ],
            }
        ]

        with patch.object(CertificatiEngine, "prepare_groups_with_priority", return_value=mock_groups):
            cert_tab.refresh_data()
            assert cert_tab.tree.topLevelItemCount() == 1
            assert "MAT-1" in cert_tab.tree.topLevelItem(0).text(0)
