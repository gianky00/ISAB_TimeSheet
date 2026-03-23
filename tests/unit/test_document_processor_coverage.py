from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.utils.document_processor import DocumentProcessor


class TestDocumentProcessorCoverage:
    @pytest.fixture
    def mock_fitz(self, mocker):  # noqa: ANN001
        """Mock della libreria PyMuPDF."""
        return mocker.patch("src.utils.document_processor.fitz")

    def test_extract_text_success(self, mock_fitz):  # noqa: ANN001
        """Verifica estrazione testo da più pagine."""
        mock_doc = MagicMock()
        mock_doc.__enter__.return_value = mock_doc
        mock_doc.__exit__.return_value = None
        mock_page1 = MagicMock()
        mock_page1.get_text.return_value = "Pagina 1"
        mock_page2 = MagicMock()
        mock_page2.get_text.return_value = "Pagina 2"

        mock_doc.__iter__.return_value = [mock_page1, mock_page2]
        mock_fitz.open.return_value = mock_doc

        text = DocumentProcessor.extract_text(Path("test.pdf"))
        assert text == "Pagina 1Pagina 2"

    def test_is_pdf_searchable_true(self, mock_fitz):  # noqa: ANN001
        """Verifica rilevamento PDF con testo."""
        mock_doc = MagicMock()
        mock_doc.__enter__.return_value = mock_doc
        mock_doc.__exit__.return_value = None
        mock_page = MagicMock()
        mock_page.get_text.return_value = "  Testo presente  "
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz.open.return_value = mock_doc

        assert DocumentProcessor.is_pdf_searchable(Path("test.pdf")) is True

    def test_is_pdf_searchable_false(self, mock_fitz):  # noqa: ANN001
        """Verifica rilevamento PDF immagine (senza testo)."""
        mock_doc = MagicMock()
        mock_doc.__enter__.return_value = mock_doc
        mock_doc.__exit__.return_value = None
        mock_page = MagicMock()
        mock_page.get_text.return_value = "   "  # Solo spazi
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz.open.return_value = mock_doc

        assert DocumentProcessor.is_pdf_searchable(Path("test.pdf")) is False

    def test_merge_pdfs_logic(self, mock_fitz, mocker):  # noqa: ANN001
        """Verifica la sequenza di unione dei file."""
        # Mock Path.exists() e Path.stat() per simulare file esistenti
        mock_path = mocker.patch("src.utils.document_processor.Path", wraps=Path)
        mock_instance = MagicMock()
        mock_instance.exists.return_value = True
        mock_stat = MagicMock()
        mock_stat.st_size = 1024
        mock_instance.stat.return_value = mock_stat
        mock_path.return_value = mock_instance

        mock_result_doc = MagicMock()
        mock_result_doc.__enter__.return_value = mock_result_doc
        mock_result_doc.__exit__.return_value = None
        mock_result_doc.__len__ = lambda self: 2

        mock_source_doc = MagicMock()
        mock_source_doc.__enter__.return_value = mock_source_doc
        mock_source_doc.__exit__.return_value = None
        mock_source_doc.is_closed = False
        mock_source_doc.page_count = 2

        # fitz.open() senza argomenti crea il doc di destinazione
        # fitz.open(path) apre il sorgente
        mock_fitz.open.side_effect = [mock_result_doc, mock_source_doc, mock_source_doc]

        paths = ["f1.pdf", "f2.pdf"]
        success = DocumentProcessor.merge_pdfs(paths, "out.pdf")

        assert success is True
        assert mock_result_doc.insert_pdf.call_count == 2  # noqa: PLR2004
        mock_result_doc.save.assert_called_with("out.pdf")

    def test_merge_pdfs_missing_fitz(self, mocker):  # noqa: ANN001
        """Verifica gestione errore se fitz non è installato."""
        with patch("src.utils.document_processor.fitz", None):
            success = DocumentProcessor.merge_pdfs(["f1.pdf"], "out.pdf")
            assert success is False
