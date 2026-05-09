"""
SyncroJob - Document Processor
Gestisce l'estrazione di testo e la manipolazione di file PDF.
"""

import logging
from pathlib import Path
from typing import Any

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
            logger.exception("Errore estrazione testo PDF: %s", file_path)
            return ""

    @staticmethod
    def is_pdf_searchable(file_path: Path) -> bool:
        """Verifica se il PDF contiene testo selezionabile o  solo un'immagine."""
        if not fitz:
            return False
        try:
            with fitz.open(file_path) as doc:
                return any(page.get_text().strip() for page in doc)
        except Exception:
            return False

    @staticmethod
    def merge_pdfs(file_paths: list[str], output_path: str) -> bool:
        """Unisce piu' file PDF in uno solo in modo robusto."""
        try:
            if not fitz:
                logger.error("Errore: PyMuPDF (fitz) non  installato.")
                return False

            valid_paths = DocumentProcessor._collect_valid_paths(file_paths)
            if not valid_paths:
                logger.error("Nessun file valido fornito per l'unione.")
                return False

            with fitz.open() as result:
                for pdf_path in valid_paths:
                    DocumentProcessor._append_to_pdf_result(result, pdf_path)

                if len(result) > 0:
                    result.save(output_path)
                    return True

                logger.error("Risultato del merge vuoto per %s", output_path)
                return False

        except Exception:
            logger.exception("Errore critico durante l'unione dei PDF in %s", output_path)
            return False

    @staticmethod
    def _collect_valid_paths(file_paths: list[str]) -> list[str]:
        """Filtra i percorsi file validi e non vuoti."""
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
        return valid_paths

    @staticmethod
    def _append_to_pdf_result(result: Any, pdf_path: str) -> None:
        """Helper per inserire un PDF nel documento finale gestendo gli errori."""
        try:
            with fitz.open(pdf_path) as pdf_doc:
                # Verifica minima che sia un PDF valido apribile
                if pdf_doc.is_closed or pdf_doc.page_count == 0:
                    logger.warning("File PDF non valido o senza pagine: %s", pdf_path)
                    return
                result.insert_pdf(pdf_doc)
        except Exception:
            logger.exception("Impossibile inserire il PDF %s nel merge", pdf_path)
