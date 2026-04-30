import re
import sqlite3

import PyPDF2

pdf_path = r"c:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\Certificati_Campione_20260423.pdf"
db_path = r"C:\Users\Coemi\AppData\Local\SyncroJob\data\contabilita.db"


def extract_text_from_pdf(path: str) -> str:
    """Estrae tutto il testo da un file PDF."""
    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n---PAGE---\n"
            return full_text
    except Exception as e:
        print(f"Errore lettura PDF: {e}")
        return ""


def parse_blocks_from_text(text: str) -> list[list[str]]:
    """Divide il testo in blocchi logici basati sulla colonna Utilizzato (SI/NO)."""
    lines = text.split("\n")
    records = []
    current_block = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line or "Pagina" in line or "Generato il" in line or "Lista Strumenti" in line:
            continue

        current_block.append(line)

        # Se la riga è "SI" o "NO", abbiamo finito un blocco (colonna Utilizzato)
        if line in ("SI", "NO"):
            records.append(current_block)
            current_block = []

    return records


def extract_data_from_blocks(records: list[list[str]]) -> dict[str, dict[str, str]]:
    """Estrae i dati (ubicazione, annotazioni) da ogni blocco di testo."""
    extracted_data = {}
    keywords_ubic = ["UFFICIO", "OFFICINA", "CANTIERE", "LABORATORIO", "CAMPO", "TECNICO", "MAGAZZINO"]
    min_block_size_for_annotation = 2

    for block in records:
        id_coemi = None
        # Cerchiamo ID-COEMI (CAT...) nei primi 3 elementi
        for item in block[:3]:
            if item.startswith("CAT") or re.match(r"^[A-Z]{2,}\d+$", item):
                id_coemi = item
                break

        if not id_coemi and block:
            id_coemi = block[0]

        ubicazione = "ASSENTE"
        annotazioni = ""
        found_ubic = False

        # Scansioniamo il blocco dal fondo (escludendo l'ultimo SI/NO)
        for i in range(len(block) - 2, 0, -1):
            val = block[i].upper()
            if any(k in val for k in keywords_ubic):
                ubicazione = block[i]
                found_ubic = True
                if i < len(block) - 2:
                    annotazioni = " ".join(block[i + 1 : len(block) - 1])
                break

        if not found_ubic and len(block) >= min_block_size_for_annotation:
            annotazioni = block[-2]

        if id_coemi:
            extracted_data[id_coemi] = {"ubicazione": ubicazione, "annotazioni": annotazioni}

    return extracted_data


def update_database(data: dict[str, dict[str, str]]) -> None:
    """Aggiorna il database con i dati estratti."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        updated_count = 0
        for key, info in data.items():
            # Cerchiamo per ID-COEMI
            cursor.execute(
                """
                UPDATE certificati_campione
                SET ubicazione = ?, annotazioni = ?
                WHERE id_coemi = ? AND (ubicazione = 'ASSENTE' OR ubicazione = '' OR ubicazione IS NULL)
            """,
                (info["ubicazione"], info["annotazioni"], key),
            )

            if cursor.rowcount > 0:
                updated_count += cursor.rowcount
            else:
                # Fallback: prova per Matricola
                cursor.execute(
                    """
                    UPDATE certificati_campione
                    SET ubicazione = ?, annotazioni = ?
                    WHERE matricola = ? AND (ubicazione = 'ASSENTE' OR ubicazione = '' OR ubicazione IS NULL)
                """,
                    (info["ubicazione"], info["annotazioni"], key),
                )
                updated_count += cursor.rowcount

        conn.commit()
        conn.close()
        print(f"Ripristino completato! Aggiornati {updated_count} record nel database.")

    except Exception as e:
        print(f"Errore database: {e}")


def run_restoration() -> None:
    print(f"Inizio ripristino da: {pdf_path}")

    full_text = extract_text_from_pdf(pdf_path)
    if not full_text:
        return

    records = parse_blocks_from_text(full_text)
    print(f"Trovati {len(records)} blocchi di dati nel PDF.")

    extracted_data = extract_data_from_blocks(records)
    print(f"Dati mappati per {len(extracted_data)} strumenti.")

    update_database(extracted_data)


if __name__ == "__main__":
    run_restoration()
