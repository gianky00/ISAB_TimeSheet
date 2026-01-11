from pathlib import Path
from unittest.mock import MagicMock, patch

from src.utils.document_processor import DocumentProcessor


class TestDocumentProcessorSimple:
    def test_extract_text_exception_handling(self, tmp_path):
        # Path non esistente deve ritornare stringa vuota senza crash tramite exception block
        assert DocumentProcessor.extract_text(Path("missing.pdf")) == ""

    @patch("src.utils.document_processor.fitz")
    def test_merge_pdfs_logic(self, mock_fitz, tmp_path):
        mock_fitz.open.return_value = MagicMock()
        success = DocumentProcessor.merge_pdfs(["f1.pdf", "f2.pdf"], "out.pdf")
        assert success is True
        assert mock_fitz.open.called

    def test_get_pages_as_images_error(self):
        # Should return empty list on error
        res = DocumentProcessor.get_pages_as_images(Path("invalid.pdf"))
        assert res == []
