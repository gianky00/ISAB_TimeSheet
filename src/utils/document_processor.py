"""
SyncroJob - Document Processor
Gestisce l'estrazione di testo e immagini da file PDF per l'analisi AI.
"""

import base64
from pathlib import Path
from typing import List

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
            doc = fitz.open(file_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            doc.close()
            return full_text.strip()
        except Exception as e:
            print(f"Errore estrazione testo PDF: {e}")
            return ""

    @staticmethod
    def get_pages_as_images(file_path: Path, max_pages: int = 5) -> List[str]:
        """Converte le pagine del PDF in immagini base64 per Gemini Vision."""
        images_base64 = []
        try:
            doc = fitz.open(file_path)
            # Limitiamo il numero di pagine per evitare payload troppo pesanti
            for i in range(min(len(doc), max_pages)):
                page = doc[i]
                # Zoom per migliore leggibilità (3.0x)
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
                img_data = pix.tobytes("png")
                b64_str = base64.b64encode(img_data).decode("utf-8")
                images_base64.append(b64_str)
            doc.close()
        except Exception as e:
            print(f"Errore conversione PDF in immagini: {e}")

        return images_base64

    @staticmethod
    def is_pdf_searchable(file_path: Path) -> bool:
        """Verifica se il PDF contiene testo selezionabile o è solo un'immagine."""
        try:
            doc = fitz.open(file_path)
            has_text = False
            for page in doc:
                if page.get_text().strip():
                    has_text = True
                    break
            doc.close()
            return has_text
        except:
            return False
