import warnings

import pandas as pd

excel_path = r'C:\Users\Coemi\Desktop\CERTIFICATI CAMPIONE\Registro calibrazioni\STRUMENTI CAMPIONE ISAB SUD AGGIORNATO.xlsm'

def debug_row_36() -> None:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            xls = pd.ExcelFile(excel_path)
            sheet_name = next(n for n in xls.sheet_names if "isab sud" in n.lower() or "strumenti" in n.lower())

            # Leggiamo tutto il foglio senza header per non perdere nulla
            df_raw = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)

            # Excel riga 36 è indice 35
            if len(df_raw) > 35:
                row_36 = df_raw.iloc[35]
                print("--- CONTENUTO EXCEL RIGA 36 (Indice 35) ---")
                print(row_36.values)
                print("-------------------------------------------")

            # Cerchiamo CAT01647 in tutto il foglio
            print("\nRicerca di 'CAT01647' nel foglio...")
            found = False
            for i, row in df_raw.iterrows():
                if 'CAT01647' in [str(x).strip() for x in row.values]:
                    print(f"TROVATO alla riga Excel {i+1} (Indice {i})")
                    print(f"Contenuto riga: {row.values}")
                    found = True

            if not found:
                print("CAT01647 NON TROVATO nel foglio tramite ricerca testuale.")

            # Proviamo a simulare l'importer con header=5
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=5)
            # Excel riga 36 (se header=5 è riga 6) dovrebbe essere df.iloc[36 - 7] = 29
            if len(df) > 29:
                target_row = df.iloc[29]
                print("\nRiga caricata da Pandas in posizione corrispondente alla 36 di Excel:")
                print(target_row.to_dict())

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    debug_row_36()
