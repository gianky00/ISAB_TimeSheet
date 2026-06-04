from unittest.mock import MagicMock, patch

from src.infrastructure.utils.document_processor import DocumentProcessor


class TestUtilsDeep:
    def test_document_processor_text_extraction(self, tmp_path):
        pdf_path = tmp_path / "test.pdf"
        pdf_path.touch()

        # We need to mock fitz.open and its return object
        mock_doc = MagicMock()
        mock_doc.__enter__.return_value = mock_doc
        mock_page = MagicMock()
        # Mocking iteration
        mock_doc.__iter__.return_value = [mock_page]
        mock_page.get_text.return_value = "Contenuto PDF"

        with patch("src.infrastructure.utils.document_processor.fitz.open", return_value=mock_doc):
            text = DocumentProcessor.extract_text(pdf_path)
            assert text == "Contenuto PDF"
            # In use as context manager, __exit__ is called instead of close() directly
            # but PyMuPDF's close() is often called by __exit__ or manually.
            # DocumentProcessor uses the 'with' statement.

    def test_is_pdf_searchable(self, tmp_path):
        pdf_path = tmp_path / "searchable.pdf"
        pdf_path.touch()

        mock_doc = MagicMock()
        mock_doc.__enter__.return_value = mock_doc
        mock_page = MagicMock()
        mock_doc.__iter__.return_value = [mock_page]
        mock_page.get_text.return_value = "  found text  "

        with patch("src.infrastructure.utils.document_processor.fitz.open", return_value=mock_doc):
            assert DocumentProcessor.is_pdf_searchable(pdf_path) is True

    def test_document_processor_no_fitz(self, tmp_path):
        """Test: Ritorna stringa vuota se fitz non è installato."""
        with patch("src.infrastructure.utils.document_processor.fitz", None):
            text = DocumentProcessor.extract_text(tmp_path / "any.pdf")
            assert text == ""
