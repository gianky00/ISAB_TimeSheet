import base64
import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from src.core.lyra_sentinel import LyraSentinel
from src.utils.document_processor import DocumentProcessor


class TestAISentinelHardened:
    @pytest.fixture
    def sentinel(self, qapp, mocker):
        """Fixture for LyraSentinel with mocked signals."""
        # We don't mock __init__ anymore to avoid breaking internal Qt state
        s = LyraSentinel()
        # Mock the signal emission
        mocker.patch.object(s, "anomalies_found")
        return s

    def test_sentinel_anomaly_detection_sqlite(self, sentinel, mocker, tmp_path):
        """Verifica il rilevamento anomalie timbrature tramite query SQL."""
        # Point CONFIG_DIR to our tmp path
        mocker.patch("src.core.lyra_sentinel.CONFIG_DIR", tmp_path)
        (tmp_path / "data").mkdir()
        db_path = tmp_path / "data" / "timbrature_Isab.db"

        # Crea DB reale temporaneo per testare la query specifica
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE timbrature (data TEXT, uscita TEXT)")
        # Anomalia: uscita mancante ieri
        conn.execute("INSERT INTO timbrature VALUES (date('now', '-1 day'), '')")
        # Non anomalia: oggi (in corso)
        conn.execute("INSERT INTO timbrature VALUES (date('now'), '')")
        # Non anomalia: uscita presente
        conn.execute("INSERT INTO timbrature VALUES (date('now', '-2 days'), '17:00')")
        conn.commit()
        conn.close()

        # Mock Contabilita per evitare altre anomalie
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_available_years",
            return_value=[],
        )

        # Run logic synchronously for testing
        sentinel.run()

        # Deve aver trovato 1 anomalia (quella di ieri)
        sentinel.anomalies_found.emit.assert_called_with(1)

    def test_document_processor_image_conversion(self, mocker, tmp_path):
        """Verifica la conversione delle pagine PDF in immagini Base64."""
        dummy_pdf = tmp_path / "test.pdf"
        dummy_pdf.write_text("fake pdf content")

        # Mock PyMuPDF (fitz)
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_pix = MagicMock()
        mock_pix.tobytes.return_value = b"fake_png_data"
        mock_page.get_pixmap.return_value = mock_pix

        # Setup mock doc
        mock_doc.__len__.return_value = 1
        mock_doc.__getitem__.return_value = mock_page
        mock_doc.__enter__.return_value = mock_doc
        mock_doc.__exit__.return_value = None

        with patch("src.utils.document_processor.fitz.open", return_value=mock_doc) as mock_open:
            images = DocumentProcessor.get_pages_as_images(dummy_pdf)

            assert len(images) == 1
            # Verifica che sia base64 valido
            decoded = base64.b64decode(images[0])
            assert decoded == b"fake_png_data"
            # Verifica zoom
            mock_page.get_pixmap.assert_called()
            args = mock_page.get_pixmap.call_args[1]
            assert "matrix" in args
            mock_open.assert_called_once_with(dummy_pdf)

    def test_document_processor_searchable_check(self, mocker, tmp_path):
        """Verifica se il processore distingue correttamente PDF testo da PDF immagine."""
        dummy_pdf = tmp_path / "test.pdf"
        dummy_pdf.write_text("fake")

        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_doc.__iter__.return_value = [mock_page]
        mock_doc.__enter__.return_value = mock_doc
        mock_doc.__exit__.return_value = None

        with patch("src.utils.document_processor.fitz.open", return_value=mock_doc):
            # Caso 1: Ha testo
            mock_page.get_text.return_value = "Contenuto testuale"
            assert DocumentProcessor.is_pdf_searchable(dummy_pdf) is True

            # Caso 2: Vuoto (solo immagine)
            mock_page.get_text.return_value = "  "
            assert DocumentProcessor.is_pdf_searchable(dummy_pdf) is False

    def test_document_processor_merge_logic(self, mocker, tmp_path):
        """Verifica l'unione fisica dei PDF."""
        out_pdf = str(tmp_path / "merged.pdf")

        mock_res = MagicMock()
        mock_res.__enter__.return_value = mock_res
        mock_res.__exit__.return_value = None

        mock_doc1 = MagicMock()
        mock_doc1.__enter__.return_value = mock_doc1
        mock_doc1.__exit__.return_value = None

        mock_doc2 = MagicMock()
        mock_doc2.__enter__.return_value = mock_doc2
        mock_doc2.__exit__.return_value = None

        with patch(
            "src.utils.document_processor.fitz.open",
            side_effect=[mock_res, mock_doc1, mock_doc2],
        ):
            success = DocumentProcessor.merge_pdfs(["p1.pdf", "p2.pdf"], out_pdf)

            assert success is True
            assert mock_res.insert_pdf.called
            assert mock_res.save.called
