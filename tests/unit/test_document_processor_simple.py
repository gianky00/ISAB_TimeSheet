from pathlib import Path
from unittest.mock import MagicMock, patch

from src.utils.document_processor import DocumentProcessor


class TestDocumentProcessorSimple:
    def test_extract_text_exception_handling(self, tmp_path):
        # Path non esistente deve ritornare stringa vuota senza crash tramite exception block
        assert DocumentProcessor.extract_text(Path("missing.pdf")) == ""

    @patch("src.utils.document_processor.Path")
    @patch("src.utils.document_processor.fitz")
    def test_merge_pdfs_logic(self, mock_fitz, mock_path_cls, tmp_path):
        # Mock Path() per simulare file esistenti
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_stat = MagicMock()
        mock_stat.st_size = 1024
        mock_path_instance.stat.return_value = mock_stat
        mock_path_cls.return_value = mock_path_instance

        # Mock del documento risultante
        mock_result_doc = MagicMock()
        mock_result_doc.__enter__.return_value = mock_result_doc
        mock_result_doc.__exit__.return_value = None
        mock_result_doc.__len__ = lambda self: 2

        # Mock del documento sorgente
        mock_source_doc = MagicMock()
        mock_source_doc.__enter__.return_value = mock_source_doc
        mock_source_doc.__exit__.return_value = None
        mock_source_doc.is_closed = False
        mock_source_doc.page_count = 2

        mock_fitz.open.side_effect = [mock_result_doc, mock_source_doc, mock_source_doc]

        success = DocumentProcessor.merge_pdfs(["f1.pdf", "f2.pdf"], "out.pdf")
        assert success is True
        assert mock_fitz.open.called
