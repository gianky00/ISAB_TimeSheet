import io
import sys

import PyPDF2

# Forza UTF-8 per l'output in Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

pdf_path = r"c:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\Certificati_Campione_20260423.pdf"


def debug_pdf() -> None:
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = reader.pages[0].extract_text()
            print("--- INIZIO TEXT PDF ---")
            print(text)
            print("--- FINE TEXT PDF ---")
    except Exception as e:
        print(f"Errore: {e}")


if __name__ == "__main__":
    debug_pdf()
