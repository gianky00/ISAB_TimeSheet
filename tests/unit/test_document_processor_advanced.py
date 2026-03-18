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
        mock_doc.__enter__.return_value = mock_doc
        mock_doc.__exit__.return_value = None
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

    def test_is_pdf_searchable_true(self, mock_fitz):
        """Test: PDF riconosciuto come ricercabile se ha testo."""
        mock_doc = MagicMock()
        mock_doc.__enter__.return_value = mock_doc
        mock_doc.__exit__.return_value = None
        mock_page = MagicMock()
        mock_page.get_text.return_value = "   Somme Text   "
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz.open.return_value = mock_doc

        assert DocumentProcessor.is_pdf_searchable(Path("text.pdf")) is True

    def test_is_pdf_searchable_false(self, mock_fitz):
        """Test: PDF riconosciuto come NON ricercabile se vuoto o solo immagine."""
        mock_doc = MagicMock()
        mock_doc.__enter__.return_value = mock_doc
        mock_doc.__exit__.return_value = None
        mock_page = MagicMock()
        mock_page.get_text.return_value = " \n "
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz.open.return_value = mock_doc

        assert DocumentProcessor.is_pdf_searchable(Path("scanned.pdf")) is False

    def test_merge_pdfs_logic(self, mock_fitz, mocker):
        """Test: Logica di unione PDF."""
        # Mock Path.exists() e Path.stat() per simulare file esistenti
        mock_path = mocker.patch("src.utils.document_processor.Path", wraps=Path)
        mock_instance = MagicMock()
        mock_instance.exists.return_value = True
        mock_stat = MagicMock()
        mock_stat.st_size = 1024
        mock_instance.stat.return_value = mock_stat
        mock_path.return_value = mock_instance

        mock_out_doc = MagicMock()
        mock_out_doc.__enter__.return_value = mock_out_doc
        mock_out_doc.__exit__.return_value = None
        mock_out_doc.__len__ = lambda self: 2  # Simula pagine nel risultato

        mock_in_doc1 = MagicMock()
        mock_in_doc1.__enter__.return_value = mock_in_doc1
        mock_in_doc1.__exit__.return_value = None
        mock_in_doc1.is_closed = False
        mock_in_doc1.page_count = 2

        mock_in_doc2 = MagicMock()
        mock_in_doc2.__enter__.return_value = mock_in_doc2
        mock_in_doc2.__exit__.return_value = None
        mock_in_doc2.is_closed = False
        mock_in_doc2.page_count = 2

        mock_fitz.open.side_effect = [
            mock_out_doc,  # Primo call per output
            mock_in_doc1,  # Call per file 1
            mock_in_doc2,  # Call per file 2
        ]

        success = DocumentProcessor.merge_pdfs(["f1.pdf", "f2.pdf"], "merged.pdf")

        assert success is True
        assert mock_out_doc.insert_pdf.call_count == 2
        mock_out_doc.save.assert_called_with("merged.pdf")

    def test_extract_text_exception_handling(self, mock_fitz):
        """Test: Gestione graziosa degli errori di apertura file."""
        mock_fitz.open.side_effect = Exception("Corrupted File")

        text = DocumentProcessor.extract_text(Path("corrupt.pdf"))
        assert text == ""  # Non deve crashare
