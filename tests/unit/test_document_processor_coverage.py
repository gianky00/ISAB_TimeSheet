import pytest
import base64
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.utils.document_processor import DocumentProcessor

class TestDocumentProcessorCoverage:
    @pytest.fixture
    def mock_fitz(self, mocker):
        """Mock della libreria PyMuPDF."""
        mock_lib = mocker.patch("src.utils.document_processor.fitz")
        return mock_lib

    def test_extract_text_success(self, mock_fitz):
        """Verifica estrazione testo da più pagine."""
        mock_doc = MagicMock()
        mock_page1 = MagicMock()
        mock_page1.get_text.return_value = "Pagina 1"
        mock_page2 = MagicMock()
        mock_page2.get_text.return_value = "Pagina 2"
        
        mock_doc.__iter__.return_value = [mock_page1, mock_page2]
        mock_fitz.open.return_value = mock_doc
        
        text = DocumentProcessor.extract_text(Path("test.pdf"))
        assert text == "Pagina 1Pagina 2"
        mock_doc.close.assert_called_once()

    def test_get_pages_as_images_limit(self, mock_fitz):
        """Verifica conversione in base64 con limite pagine."""
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 10 # 10 pagine
        
        mock_page = MagicMock()
        mock_pix = MagicMock()
        mock_pix.tobytes.return_value = b"fake_png_data"
        mock_page.get_pixmap.return_value = mock_pix
        
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz.open.return_value = mock_doc
        
        # Chiedi max 2 pagine
        images = DocumentProcessor.get_pages_as_images(Path("test.pdf"), max_pages=2)
        
        assert len(images) == 2
        assert images[0] == base64.b64encode(b"fake_png_data").decode("utf-8")

    def test_is_pdf_searchable_true(self, mock_fitz):
        """Verifica rilevamento PDF con testo."""
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "  Testo presente  "
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz.open.return_value = mock_doc
        
        assert DocumentProcessor.is_pdf_searchable(Path("test.pdf")) is True

    def test_is_pdf_searchable_false(self, mock_fitz):
        """Verifica rilevamento PDF immagine (senza testo)."""
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "   " # Solo spazi
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz.open.return_value = mock_doc
        
        assert DocumentProcessor.is_pdf_searchable(Path("test.pdf")) is False

    def test_merge_pdfs_logic(self, mock_fitz):
        """Verifica la sequenza di unione dei file."""
        mock_result_doc = MagicMock()
        mock_source_doc = MagicMock()
        
        # fitz.open() senza argomenti crea il doc di destinazione
        # fitz.open(path) apre il sorgente
        mock_fitz.open.side_effect = [mock_result_doc, mock_source_doc, mock_source_doc]
        
        paths = ["f1.pdf", "f2.pdf"]
        success = DocumentProcessor.merge_pdfs(paths, "out.pdf")
        
        assert success is True
        assert mock_result_doc.insert_pdf.call_count == 2
        mock_result_doc.save.assert_called_with("out.pdf")
        mock_result_doc.close.assert_called_once()

    def test_merge_pdfs_missing_fitz(self, mocker):
        """Verifica gestione errore se fitz non è installato."""
        with patch("src.utils.document_processor.fitz", None):
            success = DocumentProcessor.merge_pdfs(["f1.pdf"], "out.pdf")
            assert success is False