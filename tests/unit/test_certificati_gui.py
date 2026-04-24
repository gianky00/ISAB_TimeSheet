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
        """Testa la logica di calcolo giorni nell'Engine."""
        # Mock current date to fixed point
        with patch("src.core.contabilita.certificati_engine.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 1, 1, tzinfo=UTC)
            mock_dt.strptime = datetime.strptime

            # Scaduto
            days, icon = CertificatiEngine.calculate_days_and_status("01/12/2023")
            assert days is not None and days < 0
            assert icon == Icons.STATUS_DOT_RED

            # In Scadenza (10gg)
            days, icon = CertificatiEngine.calculate_days_and_status("11/01/2024")
            assert days is not None and 0 <= days <= 15
            assert icon == Icons.STATUS_DOT_ORANGE

            # Attivo
            days, icon = CertificatiEngine.calculate_days_and_status("01/03/2024")
            assert days is not None and days > 30
            assert icon == Icons.STATUS_DOT_GREEN

    def test_format_days_text_short(self):
        """Testa la formattazione breve del testo giorni nell'Engine.
        Queste stringhe sono fondamentali per il report PDF e la UI.
        """
        assert "[ROSSO] Scaduto" in CertificatiEngine.format_days_text_short(-10)
        assert "[ARANCIONE] In scadenza" in CertificatiEngine.format_days_text_short(5)
        assert "[OK] Attivo" in CertificatiEngine.format_days_text_short(60)
        assert CertificatiEngine.format_days_text_short(None) == "N/D (Senza Scadenza)"

    def test_exclusions_engine_io(self, tmp_path):
        """Testa il caricamento e salvataggio delle esclusioni nell'Engine."""
        test_file = tmp_path / "exclusions.json"

        with patch("src.core.contabilita.certificati_engine.CertificatiEngine.exclusions_file", test_file):
            engine = CertificatiEngine()
            # Salva
            engine.save_exclusions({"MAT-001", "MAT-002"})
            assert test_file.exists()

            # Ricarica
            engine2 = CertificatiEngine()
            exclusions = engine2.load_exclusions()
            assert "MAT-001" in exclusions
            assert "MAT-002" in exclusions

    def test_analysis_dialog_init(self):
        """Verifica che il dialogo di analisi si inizializzi senza errori."""
        test_data = [
            {"matricola": "M1", "days": -5, "modello": "Mod1", "costruttore": "C1"},
            {"matricola": "M2", "days": 10, "modello": "Mod2", "costruttore": "C2"},
        ]
        dialog = ScadenzeAnalysisDialog(test_data)
        self.qtbot.addWidget(dialog)

        assert "Analisi Scadenze" in dialog.windowTitle()
        assert dialog.header is not None

    def test_load_data_grouping(self, cert_tab):
        """Testa il raggruppamento dei certificati nel Tab UI."""
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
            cert_tab.refresh_data()

            # Dovrebbe esserci 1 solo nodo top level (per matricola)
            assert cert_tab.tree.topLevelItemCount() == 1
            parent = cert_tab.tree.topLevelItem(0)
            assert "MAT-1" in parent.text(0)

            # Dovrebbe avere 2 figli
            assert parent.childCount() == 2
