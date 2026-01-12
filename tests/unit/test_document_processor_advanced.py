
import base64
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.utils.document_processor import DocumentProcessor


class TestDocumentProcessorAdvanced:

    @pytest.fixture
    def mock_fitz(self, mocker):
        """Mock globale per fitz (PyMuPDF)."""
        return mocker.patch("src.utils.document_processor.fitz")

    def test_extract_text_success(self, mock_fitz):
        """Test: Estrazione testo corretta da più pagine."""
        mock_doc = MagicMock()
        # Mocking iterate pages
        mock_page1 = MagicMock()
        mock_page1.get_text.return_value = "Testo Pagina 1"
        mock_page2 = MagicMock()
        mock_page2.get_text.return_value = "Testo Pagina 2"

        mock_doc.__iter__.return_value = [mock_page1, mock_page2]
        mock_fitz.open.return_value = mock_doc

        text = DocumentProcessor.extract_text(Path("fake.pdf"))

        assert "Pagina 1" in text
        assert "Pagina 2" in text
        mock_doc.close.assert_called_once()

    def test_get_pages_as_images_limit(self, mock_fitz):
        """Test: Conversione in base64 con limite pagine."""
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 10 # PDF da 10 pagine

        mock_page = MagicMock()
        mock_pix = MagicMock()
        mock_pix.tobytes.return_value = b"FAKE_PNG_DATA"
        mock_page.get_pixmap.return_value = mock_pix

        mock_doc.__getitem__.return_value = mock_page
        mock_fitz.open.return_value = mock_doc

        # Chiamiamo con max_pages=3
        images = DocumentProcessor.get_pages_as_images(Path("long.pdf"), max_pages=3)

        assert len(images) == 3
        # Verifica codifica base64
        expected = base64.b64encode(b"FAKE_PNG_DATA").decode("utf-8")
        assert images[0] == expected

    def test_is_pdf_searchable_true(self, mock_fitz):
        """Test: PDF riconosciuto come ricercabile se ha testo."""
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "   Somme Text   "
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz.open.return_value = mock_doc

        assert DocumentProcessor.is_pdf_searchable(Path("text.pdf")) is True

    def test_is_pdf_searchable_false(self, mock_fitz):
        """Test: PDF riconosciuto come NON ricercabile se vuoto o solo immagine."""
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = " \n "
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz.open.return_value = mock_doc

        assert DocumentProcessor.is_pdf_searchable(Path("scanned.pdf")) is False

    def test_merge_pdfs_logic(self, mock_fitz):
        """Test: Logica di unione PDF."""
        mock_out_doc = MagicMock()
        mock_fitz.open.side_effect = [
            mock_out_doc, # Primo call per output
            MagicMock(),   # Call per file 1
            MagicMock()    # Call per file 2
        ]

        success = DocumentProcessor.merge_pdfs(["f1.pdf", "f2.pdf"], "merged.pdf")

        assert success is True
        assert mock_out_doc.insert_pdf.call_count == 2
        mock_out_doc.save.assert_called_with("merged.pdf")
        mock_out_doc.close.assert_called_once()

    def test_extract_text_exception_handling(self, mock_fitz):
        """Test: Gestione graziosa degli errori di apertura file."""
        mock_fitz.open.side_effect = Exception("Corrupted File")

        text = DocumentProcessor.extract_text(Path("corrupt.pdf"))
        assert text == "" # Non deve crashare
