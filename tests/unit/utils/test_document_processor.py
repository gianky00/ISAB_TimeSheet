from pathlib import Path
from unittest.mock import MagicMock, patch

from src.utils.document_processor import DocumentProcessor


class TestDocumentProcessor:
    @patch("src.utils.document_processor.fitz")
    def test_extract_text_success(self, mock_fitz):
        # Setup mock doc
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Hello PDF"
        mock_doc.__enter__.return_value = [mock_page]
        mock_fitz.open.return_value = mock_doc

        text = DocumentProcessor.extract_text(Path("test.pdf"))
        assert text == "Hello PDF"

    @patch("src.utils.document_processor.fitz")
    def test_is_pdf_searchable(self, mock_fitz):
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "  "  # Solo spazi
        mock_doc.__enter__.return_value = [mock_page]
        mock_fitz.open.return_value = mock_doc

        assert DocumentProcessor.is_pdf_searchable(Path("test.pdf")) is False

        mock_page.get_text.return_value = "Some text"
        assert DocumentProcessor.is_pdf_searchable(Path("test.pdf")) is True

    @patch("src.utils.document_processor.fitz")
    def test_merge_pdfs_success(self, mock_fitz, fs):
        fs.create_file("p1.pdf", contents=b"content1")
        fs.create_file("p2.pdf", contents=b"content2")

        # Mock result document
        mock_result = MagicMock()
        mock_result.__len__.return_value = 2
        mock_result.is_closed = False

        # Mock individual pages
        mock_p1 = MagicMock()
        mock_p1.page_count = 1
        mock_p1.is_closed = False

        mock_p2 = MagicMock()
        mock_p2.page_count = 1
        mock_p2.is_closed = False

        # Configurazione side_effect per gestire le varie chiamate a fitz.open()
        # 1. open() -> result doc
        # 2. open("p1.pdf") -> p1 doc
        # 3. open("p2.pdf") -> p2 doc
        # Usiamo un context manager mockato

        def mock_open_side_effect(path=None):
            m = MagicMock()
            if path is None:
                m.__enter__.return_value = mock_result
            elif "p1" in str(path):
                m.__enter__.return_value = mock_p1
            elif "p2" in str(path):
                m.__enter__.return_value = mock_p2
            return m

        mock_fitz.open.side_effect = mock_open_side_effect

        success = DocumentProcessor.merge_pdfs(["p1.pdf", "p2.pdf"], "out.pdf")
        assert success is True
        assert mock_result.save.called

    def test_collect_valid_paths(self, fs):
        fs.create_file("valid.pdf", contents=b"abc")
        fs.create_file("empty.pdf", contents=b"")
        # missing.pdf non esiste

        paths = ["valid.pdf", "empty.pdf", "missing.pdf"]
        valid = DocumentProcessor._collect_valid_paths(paths)

        assert len(valid) == 1
        assert valid[0] == "valid.pdf"

    def test_append_to_pdf_result_invalid(self):
        mock_result = MagicMock()
        with patch("src.utils.document_processor.fitz.open") as mock_open:
            mock_pdf = MagicMock()
            mock_pdf.page_count = 0  # Invalido
            mock_open.return_value.__enter__.return_value = mock_pdf

            DocumentProcessor._append_to_pdf_result(mock_result, "invalid.pdf")
            assert mock_result.insert_pdf.called is False
