import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.utils.document_processor import DocumentProcessor

class TestUtilsDeep:
    def test_document_processor_text_extraction(self, tmp_path):
        pdf_path = tmp_path / "test.pdf"
        pdf_path.touch()
        
        # We need to mock fitz.open and its return object
        mock_doc = MagicMock()
        mock_page = MagicMock()
        # Mocking iteration
        mock_doc.__iter__.return_value = [mock_page]
        mock_page.get_text.return_value = "Contenuto PDF"
        
        with patch("src.utils.document_processor.fitz.open", return_value=mock_doc):
            text = DocumentProcessor.extract_text(pdf_path)
            assert text == "Contenuto PDF"
            mock_doc.close.assert_called_once()

    def test_is_pdf_searchable(self, tmp_path):
        pdf_path = tmp_path / "searchable.pdf"
        pdf_path.touch()
        
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_doc.__iter__.return_value = [mock_page]
        mock_page.get_text.return_value = "  found text  "
        
        with patch("src.utils.document_processor.fitz.open", return_value=mock_doc):
            assert DocumentProcessor.is_pdf_searchable(pdf_path) is True