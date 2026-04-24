import sqlite3
import warnings

import pandas as pd

db_path = r'C:\Users\Coemi\AppData\Local\SyncroJob\data\contabilita.db'
excel_path = r'c:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\File certificati campione (Excel).xlsx'

def check_counts() -> None:
    # 1. Conteggio DB
    try:
        conn = sqlite3.connect(db_path)
        db_count = conn.execute("SELECT COUNT(*) FROM certificati_campione").fetchone()[0]
        conn.close()
        print(f"Righe nel DATABASE: {db_count}")
    except Exception as e:
        print(f"Errore lettura DB: {e}")
        return

    # 2. Conteggio Excel
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Leggiamo il file cercando il foglio corretto come fa il programma
            xls = pd.ExcelFile(excel_path)
            sheet_name = None
            for name in xls.sheet_names:
                if "strumenti campione" in name.lower() or "isab sud" in name.lower():
                    sheet_name = name
                    break
            if not sheet_name:
                sheet_name = xls.sheet_names[0]

            # Leggiamo dall'intestazione corretta (riga 5 o 6 solitamente)
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
            # Contiamo le righe totali dopo una certa riga per evitare l'intestazione
            # Se l'utente dice 165, probabilmente conta tutte le righe dati
            print(f"Righe TOTALI nel foglio '{sheet_name}': {len(df)}")

            # Proviamo a simulare il caricamento del programma (header detection)
            # Cerchiamo la riga che contiene 'Matricola'
            header_idx = 0
            for i, row in df.iterrows():
                if 'Matricola' in [str(x).strip() for x in row.values]:
                    header_idx = i
                    break

            df_data = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_idx)
            df_data = df_data.dropna(how='all') # Rimuoviamo righe completamente vuote
            print(f"Righe DATI rilevate (dopo header riga {header_idx}): {len(df_data)}")

    except Exception as e:
        print(f"Errore lettura Excel: {e}")

if __name__ == "__main__":
    check_counts()
