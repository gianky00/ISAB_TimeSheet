"""Unit tests for ScadenzeAnalysisDialog."""

import os
from unittest.mock import MagicMock

import pytest

from src.gui.dialogs.certificati_analysis_dialog import (
    ScadenzeAnalysisDialog,
)


@pytest.fixture
def certificates_data():
    """Dati di test per i certificati."""
    return [
        {
            "id_strumento": "ID1",
            "costruttore": "Coemi",
            "modello": "Manometro",
            "matricola": "M1",
            "ubicazione": "ISAB SUD",
            "days": -5,
            "range": "0-10 bar",
        },  # Scaduto
        {
            "id_strumento": "ID2",
            "costruttore": "Wika",
            "modello": "Manometro Digitale",
            "matricola": "M2",
            "ubicazione": "LAB",
            "days": 10,
            "range": "0-100 bar",
        },  # Urgente
        {
            "id_strumento": "ID3",
            "costruttore": "Fluke",
            "modello": "Multimetro",
            "matricola": "M3",
            "ubicazione": "ISAB SUD",
            "days": 25,
            "range": None,
        },  # Attenzione
        {
            "id_strumento": "ID4",
            "costruttore": "Druck",
            "modello": "Calibratore",
            "matricola": "M4",
            "ubicazione": "OFFICINA",
            "days": 60,
            "range": None,
        },  # Attivo
        {
            "id_strumento": "ID5",
            "costruttore": "Unknown",
            "modello": "Test",
            "matricola": "M5",
            "ubicazione": "ASSENTE",
            "days": 0,
            "range": None,
        },  # Escluso (Assente)
        {
            "id_strumento": "ID6",
            "costruttore": "N/D",
            "modello": "N/D",
            "matricola": "M6",
            "ubicazione": "ISAB SUD",
            "days": None,
            "range": None,
        },  # Data non disponibile
    ]


class TestScadenzeAnalysisDialog:
    """Test suite per ScadenzeAnalysisDialog."""

    def test_initialization_filtering(self, qtbot, certificates_data):
        """Verifica che gli strumenti ASSENTI vengano filtrati subito."""
        dialog = ScadenzeAnalysisDialog(certificates_data)
        qtbot.addWidget(dialog)

        # ID5 dovrebbe essere sparito
        assert len(dialog.certificates_data) == 5
        assert not any(c["id_strumento"] == "ID5" for c in dialog.certificates_data)

    def test_metrics_calculation(self, qtbot, certificates_data):
        """Verifica il conteggio corretto nelle varie categorie."""
        dialog = ScadenzeAnalysisDialog(certificates_data)
        qtbot.addWidget(dialog)

        stats = dialog._calculate_metrics()
        assert stats["total"] == 5
        assert stats["scaduti"] == 1  # ID1 (-5)
        assert stats["urgenti"] == 1  # ID2 (10)
        assert stats["attenzione"] == 1  # ID3 (25)
        assert stats["attivi"] == 1  # ID4 (60)
        # ID6 ha days=None, non rientra in queste categorie basate su numeri

    def test_sections_creation(self, qtbot, certificates_data):
        """Verifica che vengano create le sezioni nel layout."""
        dialog = ScadenzeAnalysisDialog(certificates_data)
        qtbot.addWidget(dialog)

        # Le sezioni sono QFrame aggiunte al layout di content_widget
        sections = dialog.content_widget.findChildren(pytest.importorskip("PySide6.QtWidgets").QFrame)
        # Cerchiamo i titoli delle sezioni nelle label
        labels = dialog.content_widget.findChildren(pytest.importorskip("PySide6.QtWidgets").QLabel)

        assert any("SCADUTI (1)" in lbl.text() for lbl in labels)
        assert any("IN SCADENZA (0-15 giorni) (1)" in lbl.text() for lbl in labels)
        assert any("DATA NON DISPONIBILE (1)" in lbl.text() for lbl in labels)

    def test_capture_widgets_as_images(self, qtbot, certificates_data):
        """Verifica la cattura degli screenshot delle sezioni critiche."""
        dialog = ScadenzeAnalysisDialog(certificates_data)
        qtbot.addWidget(dialog)
        dialog.show()

        image_paths = dialog._capture_widgets_as_images()

        # Dovrebbe aver catturato Scaduti, In Scadenza e Data Non Disponibile
        assert len(image_paths) >= 1

        # Cleanup
        dialog._cleanup_temp_images(image_paths)
        for p in image_paths:
            assert not os.path.exists(p)

    def test_send_email_trigger(self, qtbot, certificates_data, mocker):
        """Verifica lbl'avvio del worker email."""
        dialog = ScadenzeAnalysisDialog(certificates_data)
        qtbot.addWidget(dialog)
        dialog.show()

        # Mocking OutlookEmailWorker e cattura immagini
        mocker.patch.object(dialog, "_capture_widgets_as_images", return_value=["/tmp/img.png"])
        mock_worker_cls = mocker.patch("src.gui.dialogs.certificati_analysis_dialog.OutlookEmailWorker")
        mock_worker = MagicMock()
        mock_worker_cls.return_value = mock_worker

        # Mocking PDF generation
        mocker.patch.object(dialog, "_generate_audit_pdf", return_value="/tmp/test.pdf")

        dialog._send_email()

        assert mock_worker_cls.called
        assert mock_worker.start.called

    def test_email_subject_builder(self, qtbot, certificates_data):
        """Verifica la costruzione dell'oggetto email."""
        dialog = ScadenzeAnalysisDialog(certificates_data)
        qtbot.addWidget(dialog)

        subject = dialog._build_email_subject(scaduti=3, nd=2)
        assert "[URGENTE]" in subject
        assert "3 Scaduti" in subject
        assert "2 N/D" in subject

        subject_normal = dialog._build_email_subject(scaduti=0, nd=1)
        assert "[URGENTE]" not in subject_normal
        assert "1 N/D" in subject_normal

    def test_generate_audit_pdf_no_engine(self, qtbot, certificates_data):
        """Verifica che senza engine ritorni None."""
        dialog = ScadenzeAnalysisDialog(certificates_data, engine=None)
        qtbot.addWidget(dialog)
        assert dialog._generate_audit_pdf() is None
