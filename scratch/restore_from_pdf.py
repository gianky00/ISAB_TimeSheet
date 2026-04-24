import re
import sqlite3

import PyPDF2

pdf_path = r'c:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\Certificati_Campione_20260423.pdf'
db_path = r'C:\Users\Coemi\AppData\Local\SyncroJob\data\contabilita.db'

def run_restoration() -> None:
    print(f"Inizio ripristino da: {pdf_path}")

    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n---PAGE---\n"
    except Exception as e:
        print(f"Errore lettura PDF: {e}")
        return

    # Dividiamo il testo in righe e cerchiamo di identificare i record
    # Un record finisce con "SI" o "NO" (colonna Utilizzato)
    lines = full_text.split('\n')

    records = []
    current_block = []

    for line in lines:
        line = line.strip()
        if not line or "Pagina" in line or "Generato il" in line or "Lista Strumenti" in line:
            continue

        current_block.append(line)

        # Se la riga è "SI" o "NO", abbiamo finito un blocco (colonna Utilizzato)
        if line in ("SI", "NO"):
            records.append(current_block)
            current_block = []

    print(f"Trovati {len(records)} blocchi di dati nel PDF.")

    # Mappa dei dati estratti: {id_coemi: {ubicazione: str, annotazioni: str}}
    # Useremo anche la matricola come fallback se l'ID-COEMI manca
    extracted_data = {}

    for block in records:
        # Tentativo di estrazione euristica
        # In base al debug:
        # [0] ID-COEMI (se presente) o Certificato
        # [1] Certificato o parte del Modello
        # ...
        # [-2] Ubicazione (se presente)
        # [-1] Utilizzato (SI/NO)

        # Cerchiamo ID-COEMI (CAT...)
        id_coemi = None
        for item in block[:3]:
            if item.startswith("CAT") or re.match(r'^[A-Z]{2,}\d+$', item):
                id_coemi = item
                break

        # Se non troviamo CAT, proviamo a vedere se il primo elemento è un codice
        if not id_coemi and len(block) > 0:
             # Se è tipo 082-20, è un certificato, ma potrebbe essere l'unico ID
             id_coemi = block[0]

        # Ubicazione e Annotazioni
        # Sappiamo che l'ultima riga è SI/NO.
        # Quella prima potrebbe essere l'Annotazione o l'Ubicazione.

        ubicazione = "ASSENTE"
        annotazioni = ""

        # Parole chiave note per ubicazione
        keywords_ubic = ["UFFICIO", "OFFICINA", "CANTIERE", "LABORATORIO", "CAMPO", "TECNICO", "MAGAZZINO"]

        # Scansioniamo il blocco dal fondo (escludendo l'ultimo SI/NO)
        found_ubic = False
        for i in range(len(block)-2, 0, -1):
            val = block[i].upper()
            if any(k in val for k in keywords_ubic):
                ubicazione = block[i]
                found_ubic = True
                # Tutto quello che c'è tra l'ubicazione e il SI/NO (se c'è altro) sono annotazioni?
                # O quello prima dell'ubicazione?
                if i < len(block) - 2:
                    annotazioni = " ".join(block[i+1 : len(block)-1])
                break

        if not found_ubic:
            # Se non abbiamo trovato l'ubicazione, forse l'annotazione è l'ultima riga prima di SI/NO
            if len(block) >= 2:
                annotazioni = block[-2]

        if id_coemi:
            extracted_data[id_coemi] = {
                "ubicazione": ubicazione,
                "annotazioni": annotazioni
            }

    print(f"Dati mappati per {len(extracted_data)} strumenti.")

    # Aggiornamento Database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        updated_count = 0
        for key, info in extracted_data.items():
            # Cerchiamo per ID-COEMI
            cursor.execute("""
                UPDATE certificati_campione
                SET ubicazione = ?, annotazioni = ?
                WHERE id_coemi = ? AND (ubicazione = 'ASSENTE' OR ubicazione = '' OR ubicazione IS NULL)
            """, (info['ubicazione'], info['annotazioni'], key))

            if cursor.rowcount > 0:
                updated_count += cursor.rowcount
            else:
                # Fallback: prova per Matricola se key sembra una matricola
                cursor.execute("""
                    UPDATE certificati_campione
                    SET ubicazione = ?, annotazioni = ?
                    WHERE matricola = ? AND (ubicazione = 'ASSENTE' OR ubicazione = '' OR ubicazione IS NULL)
                """, (info['ubicazione'], info['annotazioni'], key))
                updated_count += cursor.rowcount

        conn.commit()
        conn.close()
        print(f"Ripristino completato! Aggiornati {updated_count} record nel database.")

    except Exception as e:
        print(f"Errore database: {e}")

if __name__ == "__main__":
    run_restoration()
