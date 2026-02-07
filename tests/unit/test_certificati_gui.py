from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from src.core.constants import Icons
from src.gui.widgets.contabilita.certificati_tab import (
    CertificatiCampioneTab,
    ScadenzeAnalysisDialog,
)


class TestCertificatiGUI:
    @pytest.fixture(autouse=True)
    def setup_qt(self, qtbot):
        self.qtbot = qtbot

    @pytest.fixture
    def cert_tab(self):
        with patch(
            "src.core.contabilita_manager.ContabilitaManager.get_certificati_campione_data"
        ) as mock_data:
            mock_data.return_value = []
            tab = CertificatiCampioneTab()
            self.qtbot.addWidget(tab)
            return tab

    def test_calculate_days_and_status(self, cert_tab):
        """Testa la logica di calcolo giorni e icone di stato."""
        today = datetime.now()

        # Scaduto
        past_date = (today - timedelta(days=5)).strftime("%d/%m/%Y")
        days, icon = cert_tab._calculate_days_and_status(past_date)
        assert days is not None and days < 0
        assert icon == Icons.STATUS_DOT_RED

        # Urgente (0-15 giorni)
        near_future = (today + timedelta(days=10)).strftime("%d/%m/%Y")
        days, icon = cert_tab._calculate_days_and_status(near_future)
        assert days is not None and 0 <= days <= 15
        assert icon == Icons.STATUS_DOT_ORANGE

        # Attenzione (16-30 giorni)
        attention_future = (today + timedelta(days=20)).strftime("%d/%m/%Y")
        days, icon = cert_tab._calculate_days_and_status(attention_future)
        assert days is not None and 16 <= days <= 30
        assert icon == Icons.STATUS_DOT_YELLOW

        # Attivo (>30 giorni)
        far_future = (today + timedelta(days=45)).strftime("%d/%m/%Y")
        days, icon = cert_tab._calculate_days_and_status(far_future)
        assert days is not None and days > 30
        assert icon == Icons.STATUS_DOT_GREEN

        # N/D
        days, icon = cert_tab._calculate_days_and_status("")
        assert days is None
        assert icon == Icons.STATUS_DOT_GRAY

    def test_format_days_text_short(self, cert_tab):
        """Testa la formattazione breve del testo giorni."""
        assert "Scaduto" in cert_tab._format_days_text_short(-10)
        assert "Scade tra 5gg" in cert_tab._format_days_text_short(5)
        assert "Attivo" in cert_tab._format_days_text_short(60)
        assert cert_tab._format_days_text_short(None) == "N/D"

    def test_exclusions_io(self, cert_tab, tmp_path):
        """Testa il caricamento e salvataggio delle esclusioni."""
        test_file = tmp_path / "exclusions.json"

        with patch.object(CertificatiCampioneTab, "EXCLUSIONS_FILE", test_file):
            # Salva
            cert_tab._exclusions = {"MAT-001", "MAT-002"}
            cert_tab._save_exclusions()
            assert test_file.exists()

            # Carica in una nuova istanza
            with patch(
                "src.core.contabilita_manager.ContabilitaManager.get_certificati_campione_data"
            ) as mock_data:
                mock_data.return_value = []
                new_tab = CertificatiCampioneTab()
                assert "MAT-001" in new_tab._exclusions
                assert "MAT-002" in new_tab._exclusions

    def test_exclude_include_methods(self, cert_tab, tmp_path):
        """Testa i metodi per escludere/includere matricole."""
        test_file = tmp_path / "exclusions_methods.json"
        with patch.object(CertificatiCampioneTab, "EXCLUSIONS_FILE", test_file):
            with patch.object(cert_tab, "_load_data") as mock_load:
                cert_tab._exclude_matricola("TEST-MAT")
                assert "TEST-MAT" in cert_tab._exclusions
                assert mock_load.called

                mock_load.reset_mock()
                cert_tab._include_matricola("TEST-MAT")
                assert "TEST-MAT" not in cert_tab._exclusions
                assert mock_load.called

    def test_analysis_dialog_init(self):
        """Verifica che il dialogo di analisi si inizializzi senza errori."""
        test_data = [
            {"matricola": "M1", "days": -5, "modello": "Mod1", "costruttore": "C1"},
            {"matricola": "M2", "days": 10, "modello": "Mod2", "costruttore": "C2"},
            {"matricola": "M3", "days": 40, "modello": "Mod3", "costruttore": "C3"},
        ]
        dialog = ScadenzeAnalysisDialog(test_data)
        self.qtbot.addWidget(dialog)

        assert dialog.windowTitle().startswith("Analisi Scadenze")
        # Verifica che i widget siano stati creati
        assert dialog.header is not None
        assert dialog.stats_frame is not None

    def test_load_data_grouping(self, cert_tab):
        """Testa il raggruppamento dei certificati per matricola."""
        # Mock data: 2 certificati per la stessa matricola
        mock_data = [
            # Modello, Costruttore, Matricola, Range, Errore, Certificato, Scadenza, Emissione, ID, Stato
            (
                "Mod A",
                "Costr A",
                "MAT-1",
                "0-10",
                "1%",
                "CERT-1",
                "10/02/2026",
                "10/02/2025",
                "ID1",
                "",
            ),
            (
                "Mod A",
                "Costr A",
                "MAT-1",
                "0-10",
                "1%",
                "CERT-2",
                "10/02/2025",
                "10/02/2024",
                "ID1",
                "",
            ),
        ]

        with patch(
            "src.core.contabilita_manager.ContabilitaManager.get_certificati_campione_data",
            return_value=mock_data,
        ):
            cert_tab._load_data()

            # Dovrebbe esserci 1 solo nodo top level (per matricola)
            assert cert_tab.tree.topLevelItemCount() == 1
            parent = cert_tab.tree.topLevelItem(0)
            assert "MAT-1" in parent.text(0)

            # Dovrebbe avere 2 figli
            assert parent.childCount() == 2

            # Il primo figlio dovrebbe essere il più recente (CERT-1)
            assert parent.child(0).text(cert_tab.IDX_CERTIFICATO) == "CERT-1"
            assert parent.child(1).text(cert_tab.IDX_CERTIFICATO) == "CERT-2"

    def test_screenshot_generation_logic(self, cert_tab):
        """Testa la logica di preparazione dello screenshot (senza esecuzione effettiva)."""
        test_data = [{"matricola": "M1", "days": 10, "modello": "Mod1", "costruttore": "C1"}]
        dialog = ScadenzeAnalysisDialog(test_data, cert_tab)
        self.qtbot.addWidget(dialog)

        # Mocking heavy Qt GUI operations that cause COM crashes on Windows
        with (
            patch("PyQt6.QtGui.QPainter"),
            patch("PyQt6.QtGui.QPixmap"),
            patch("PyQt6.QtWidgets.QMessageBox.information"),
            patch("PyQt6.QtWidgets.QMessageBox.critical"),
            patch("os.startfile"),
            patch("subprocess.Popen") as mock_popen,
        ):
            # Caso 1: Senza macro Excel
            with patch("src.core.config_manager.load_config", return_value={}):
                dialog._send_email()
                assert not mock_popen.called

            # Caso 2: Con macro Excel (simulata)
            with (
                patch(
                    "src.core.config_manager.load_config",
                    return_value={"certificati_campione_path": "test.xlsx"},
                ),
                patch("src.gui.widgets.contabilita.certificati_tab.Path.exists", return_value=True),
            ):
                dialog._send_email()
                assert mock_popen.called
                args, _kwargs = mock_popen.call_args
                assert "powershell" in args[0]
