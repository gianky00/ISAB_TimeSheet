import base64
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import fitz
import pytest

from src.utils.document_processor import DocumentProcessor


@pytest.fixture
def sample_pdf(tmp_path):
    """Crea un PDF di prova con testo."""
    pdf_path = tmp_path / "test.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Testo di prova per DocumentProcessor")
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def image_pdf(tmp_path):
    """Crea un PDF che contiene un'immagine (non necessariamente testo ricercabile)."""
    # Nota: fitz può inserire immagini, ma qui ne creiamo uno vuoto per semplicità
    # e poi testeremo il fallimento di extract_text se vogliamo,
    # o useremo un PDF reale se necessario.
    pdf_path = tmp_path / "image.pdf"
    doc = fitz.open()
    doc.new_page()
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


class TestDocumentProcessorCoverage:
    def test_extract_text_success(self, sample_pdf):
        """Testa l'estrazione corretta del testo da un PDF."""
        text = DocumentProcessor.extract_text(sample_pdf)
        assert "Testo di prova" in text

    def test_extract_text_empty(self, image_pdf):
        """Testa l'estrazione da un PDF senza testo."""
        text = DocumentProcessor.extract_text(image_pdf)
        assert text == ""

    def test_extract_text_invalid_path(self):
        """Testa il comportamento con un path inesistente."""
        text = DocumentProcessor.extract_text(Path("non_existent.pdf"))
        assert text == ""

    def test_is_pdf_searchable_true(self, sample_pdf):
        """Testa se riconosce correttamente un PDF ricercabile."""
        assert DocumentProcessor.is_pdf_searchable(sample_pdf) is True

    def test_is_pdf_searchable_false(self, image_pdf):
        """Testa se riconosce un PDF non ricercabile (vuoto/solo immagini)."""
        assert DocumentProcessor.is_pdf_searchable(image_pdf) is False

    def test_get_pages_as_images_success(self, sample_pdf):
        """Testa la conversione delle pagine in base64."""
        images = DocumentProcessor.get_pages_as_images(sample_pdf)
        assert len(images) == 1
        # Verifica che sia una stringa base64 valida (almeno parzialmente)
        try:
            base64.b64decode(images[0])
            valid = True
        except Exception:
            valid = False
        assert valid is True

    def test_get_pages_as_images_limit(self, tmp_path):
        """Testa il limite delle pagine per la conversione in immagini."""
        pdf_path = tmp_path / "multi_page.pdf"
        doc = fitz.open()
        for i in range(10):
            doc.new_page()
        doc.save(str(pdf_path))
        doc.close()

        # Default max_pages è 5
        images = DocumentProcessor.get_pages_as_images(pdf_path)
        assert len(images) == 5

        # Custom max_pages
        images_custom = DocumentProcessor.get_pages_as_images(pdf_path, max_pages=2)
        assert len(images_custom) == 2

    def test_merge_pdfs_success(self, tmp_path):
        """Testa l'unione di più PDF."""
        p1 = tmp_path / "p1.pdf"
        p2 = tmp_path / "p2.pdf"
        out = tmp_path / "merged.pdf"

        # Crea due PDF
        doc1 = fitz.open()
        doc1.new_page().insert_text((50, 50), "Pagina 1")
        doc1.save(str(p1))
        doc1.close()

        doc2 = fitz.open()
        doc2.new_page().insert_text((50, 50), "Pagina 2")
        doc2.save(str(p2))
        doc2.close()

        success = DocumentProcessor.merge_pdfs([str(p1), str(p2)], str(out))
        assert success is True
        assert out.exists()

        # Verifica contenuto unito
        text = DocumentProcessor.extract_text(out)
        assert "Pagina 1" in text
        assert "Pagina 2" in text

    def test_merge_pdfs_error(self, tmp_path):
        """Testa l'unione con file non validi."""
        out = tmp_path / "fail.pdf"
        success = DocumentProcessor.merge_pdfs(["missing1.pdf", "missing2.pdf"], str(out))
        assert success is False

    def test_is_pdf_searchable_exception(self):
        """Testa l'eccezione in is_pdf_searchable."""
        # Passare None o qualcosa che non è un Path dovrebbe triggerare l'except
        assert DocumentProcessor.is_pdf_searchable(None) is False

    def test_merge_pdfs_no_fitz(self):
        """Testa merge_pdfs quando fitz non è installato."""
        with patch("src.utils.document_processor.fitz", None):
            # Forziamo l'uso del modulo patchato
            import src.utils.document_processor
            print(f"DEBUG: fitz in module is {src.utils.document_processor.fitz}")
            assert DocumentProcessor.merge_pdfs(["a.pdf"], "out.pdf") is False

    @patch("src.utils.document_processor.fitz")
    def test_get_pages_as_images_exception(self, mock_fitz):
        """Testa l'eccezione in get_pages_as_images."""
        mock_fitz.open.side_effect = Exception("Mocked error")
        res = DocumentProcessor.get_pages_as_images(Path("any.pdf"))
        assert res == []

    @patch("src.utils.document_processor.fitz")
    def test_merge_pdfs_exception(self, mock_fitz):
        """Testa l'eccezione in merge_pdfs."""
        mock_fitz.open.side_effect = Exception("Mocked error")
        assert DocumentProcessor.merge_pdfs(["a.pdf"], "out.pdf") is False

def test_fitz_import_error():
    """Testa il blocco ImportError per fitz ricaricando il modulo."""
    import sys
    import importlib
    import src.utils.document_processor
    
    # Salviamo il riferimento originale
    original_fitz = sys.modules.get('fitz')
    
    try:
        # Simuliamo la mancanza del modulo
        sys.modules['fitz'] = None
        importlib.reload(src.utils.document_processor)
        assert src.utils.document_processor.fitz is None
    finally:
        # Ripristiniamo
        if original_fitz:
            sys.modules['fitz'] = original_fitz
        else:
            del sys.modules['fitz']
        importlib.reload(src.utils.document_processor)
