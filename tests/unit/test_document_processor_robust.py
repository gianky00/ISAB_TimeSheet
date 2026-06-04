"""Tests for robust DocumentProcessor merge logic."""

from unittest.mock import MagicMock

import pytest

from src.infrastructure.utils.document_processor import DocumentProcessor


class TestDocumentProcessorRobust:
    @pytest.fixture
    def mock_fitz(self, mocker):
        mock = MagicMock()
        mocker.patch("src.infrastructure.utils.document_processor.fitz", mock)
        return mock

    @pytest.fixture
    def mock_path(self, mocker):
        # Patch the Path class within the module to avoid global pollution
        return mocker.patch("src.infrastructure.utils.document_processor.Path")

    def test_merge_pdfs_all_valid(self, mock_fitz, mock_path):
        """Test merge standard con file validi."""
        # Setup mock path behavior
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.stat.return_value.st_size = 100

        # Mock fitz.open context managers
        mock_doc = MagicMock()
        mock_doc.__enter__.return_value = mock_doc
        mock_doc.page_count = 1
        mock_doc.is_closed = False

        # Mock result doc
        mock_result = MagicMock()
        mock_result.__enter__.return_value = mock_result
        mock_result.__len__.return_value = 2  # Indica che ha pagine
        mock_result.is_closed = False

        # Secondo mock_fitz.open (senza argomenti) per il result
        mock_fitz.open.side_effect = [mock_result, mock_doc, mock_doc]

        success = DocumentProcessor.merge_pdfs(["f1.pdf", "f2.pdf"], "out.pdf")

        assert success is True
        mock_result.save.assert_called_with("out.pdf")
        assert mock_result.insert_pdf.call_count == 2

    def test_merge_pdfs_missing_file(self, mock_fitz, mock_path):
        """Verifica che i file mancanti vengano saltati."""
        # Primo file esiste, secondo no
        m1 = MagicMock()
        m1.exists.return_value = True
        m1.stat.return_value.st_size = 100

        m2 = MagicMock()
        m2.exists.return_value = False

        mock_path.side_effect = [m1, m2]

        mock_result = MagicMock()
        mock_result.__enter__.return_value = mock_result
        mock_result.__len__.return_value = 1
        mock_result.is_closed = False

        mock_doc = MagicMock()
        mock_doc.__enter__.return_value = mock_doc
        mock_doc.page_count = 1
        mock_doc.is_closed = False

        mock_fitz.open.side_effect = [mock_result, mock_doc]

        success = DocumentProcessor.merge_pdfs(["exists.pdf", "missing.pdf"], "out.pdf")

        assert success is True
        assert mock_result.insert_pdf.call_count == 1

    def test_merge_pdfs_empty_input(self, mock_fitz):
        """Verifica fallimento se non ci sono file validi."""
        success = DocumentProcessor.merge_pdfs([], "out.pdf")
        assert success is False

    def test_merge_pdfs_corrupt_file(self, mock_fitz, mock_path):
        """Verifica che un file corrotto non blocchi l'intero merge."""
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.stat.return_value.st_size = 100

        mock_result = MagicMock()
        mock_result.__enter__.return_value = mock_result
        mock_result.__len__.return_value = 1
        mock_result.is_closed = False

        mock_doc_ok = MagicMock()
        mock_doc_ok.__enter__.return_value = mock_doc_ok
        mock_doc_ok.page_count = 1
        mock_doc_ok.is_closed = False

        # Simula eccezione all'apertura del secondo file
        mock_fitz.open.side_effect = [mock_result, mock_doc_ok, Exception("Corrupt")]

        success = DocumentProcessor.merge_pdfs(["ok.pdf", "bad.pdf"], "out.pdf")

        assert success is True
        assert mock_result.insert_pdf.call_count == 1
        mock_result.save.assert_called()
