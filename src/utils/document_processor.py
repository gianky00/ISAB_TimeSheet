"""
SyncroJob - Document Processor
Gestisce l'estrazione di testo e immagini da file PDF per l'analisi AI.
"""

import base64
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import fitz  # type: ignore
except ImportError:
    fitz = None


class DocumentProcessor:
    """Classe per processare documenti PDF e prepararli per Lyra AI."""

    @staticmethod
    def extract_text(file_path: Path) -> str:
        """Estrae tutto il testo da un PDF."""
        try:
            with fitz.open(file_path) as doc:
                full_text = "".join(page.get_text() for page in doc)
            return full_text.strip()
        except Exception:
            logger.error("Errore estrazione testo PDF: %s", file_path, exc_info=True)
            return ""

    @staticmethod
    def get_pages_as_images(file_path: Path, max_pages: int = 5) -> list[str]:
        """Converte le pagine del PDF in immagini base64 per Gemini Vision."""
        images_base64 = []
        try:
            with fitz.open(file_path) as doc:
                # Limitiamo il numero di pagine per evitare payload troppo pesanti
                for i in range(min(len(doc), max_pages)):
                    page = doc[i]
                    # Zoom per migliore leggibilità (3.0x)
                    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
                    img_data = pix.tobytes("png")
                    b64_str = base64.b64encode(img_data).decode("utf-8")
                    images_base64.append(b64_str)
        except Exception:
            logger.error("Errore conversione PDF in immagini: %s", file_path, exc_info=True)

        return images_base64

    @staticmethod
    def is_pdf_searchable(file_path: Path) -> bool:
        """Verifica se il PDF contiene testo selezionabile o è solo un'immagine."""
        try:
            with fitz.open(file_path) as doc:
                return any(page.get_text().strip() for page in doc)
        except Exception:
            return False

    @staticmethod
    def merge_pdfs(file_paths: list[str], output_path: str) -> bool:
        """Unisce più file PDF in uno solo usando PyMuPDF (fitz)."""
        try:
            if not fitz:
                logger.error("Errore: PyMuPDF (fitz) non è installato.")
                return False

            with fitz.open() as result:
                for pdf_path in file_paths:
                    with fitz.open(pdf_path) as pdf_doc:
                        result.insert_pdf(pdf_doc)
                result.save(output_path)

            return True
        except Exception:
            logger.error("Errore durante l'unione dei PDF con fitz", exc_info=True)
            return False
