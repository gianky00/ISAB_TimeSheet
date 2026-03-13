"""
SyncroJob - Document Processor
Gestisce l'estrazione di testo e la manipolazione di file PDF.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import fitz
except ImportError:
    fitz = None


class DocumentProcessor:
    """Classe per processare documenti PDF."""

    @staticmethod
    def extract_text(file_path: Path) -> str:
        """Estrae tutto il testo da un PDF."""
        if not fitz:
            return ""
        try:
            with fitz.open(file_path) as doc:
                full_text = "".join(page.get_text() for page in doc)
            return full_text.strip()
        except Exception:
            logger.error("Errore estrazione testo PDF: %s", file_path, exc_info=True)
            return ""

    @staticmethod
    def is_pdf_searchable(file_path: Path) -> bool:
        """Verifica se il PDF contiene testo selezionabile o è solo un'immagine."""
        if not fitz:
            return False
        try:
            with fitz.open(file_path) as doc:
                return any(page.get_text().strip() for page in doc)
        except Exception:
            return False

    @staticmethod
    def merge_pdfs(file_paths: list[str], output_path: str) -> bool:
        """Unisce più file PDF in uno solo in modo robusto."""
        try:
            if not fitz:
                logger.error("Errore: PyMuPDF (fitz) non è installato.")
                return False

            valid_paths = []
            for p in file_paths:
                path = Path(p)
                if not path.exists():
                    logger.warning("File non trovato per il merge: %s", p)
                    continue
                if path.stat().st_size == 0:
                    logger.warning("File vuoto ignorato nel merge: %s", p)
                    continue
                valid_paths.append(p)

            if not valid_paths:
                logger.error("Nessun file valido fornito per l'unione.")
                return False

            with fitz.open() as result:
                for pdf_path in valid_paths:
                    try:
                        with fitz.open(pdf_path) as pdf_doc:
                            # Verifica minima che sia un PDF valido apribile
                            if pdf_doc.is_closed or pdf_doc.page_count == 0:
                                logger.warning("File PDF non valido o senza pagine: %s", pdf_path)
                                continue
                            result.insert_pdf(pdf_doc)
                    except Exception as e:
                        logger.error("Impossibile inserire il PDF %s nel merge: %s", pdf_path, e)
                        continue

                if len(result) > 0:
                    result.save(output_path)
                    return True

                logger.error("Risultato del merge vuoto per %s", output_path)
                return False

        except Exception:
            logger.error("Errore critico durante l'unione dei PDF in %s", output_path, exc_info=True)
            return False
