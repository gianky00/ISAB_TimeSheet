import warnings
from pathlib import Path

import pandas as pd

# Percorso reale dal config
excel_path = r"C:\Users\Coemi\Desktop\CERTIFICATI CAMPIONE\Registro calibrazioni\STRUMENTI CAMPIONE ISAB SUD AGGIORNATO.xlsm"

MAPPING = {
    "ID-COEMI": "id_coemi",
    "Certificato Taratura": "certificato",
    "Modello / Tipo": "modello",
    "Costruttore": "costruttore",
    "Matricola": "matricola",
    "Range Strumento": "range_strumento",
    "Errore max %": "errore_max",
    "Emissione Certificato": "emissione",
    "Scadenza Certificato": "scadenza",
    "Stato Certificato": "stato",
}


def debug_import() -> None:
    try:
        if not Path(excel_path).exists():
            print(f"ERRORE: File non trovato a {excel_path}")
            return

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            xls = pd.ExcelFile(excel_path)
            # Cerchiamo il foglio
            sheet_name = [n for n in xls.sheet_names if "isab sud" in n.lower() or "strumenti" in n.lower()]
            sheet_name = xls.sheet_names[0] if not sheet_name else sheet_name[0]

            # Leggiamo con header=5 (Excel riga 6) -> Dati da riga 7
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=5)

            print(f"Foglio utilizzato: {sheet_name}")

            # Cerchiamo l'ID-COEMI nelle colonne
            id_col = None
            for c in df.columns:
                if "ID-COEMI" in str(c).upper():
                    id_col = c
                    break

            if id_col:
                print(f"Colonna ID-COEMI individuata: '{id_col}'")
            else:
                print(f"ATTENZIONE: Colonna ID-COEMI NON individuata tra: {list(df.columns)}")

            # Conteggio grezzo
            print(f"Righe lette da Pandas (da riga 7 in poi): {len(df)}")

            # Pulizia come nel programma
            df_cleaned = df.dropna(how="all")
            print(f"Righe dopo rimozione righe COMPLETAMENTE vuote: {len(df_cleaned)}")

            # Se ne abbiamo meno di 165, stampiamo le ultime righe per vedere dove si ferma
            if len(df_cleaned) < 165:  # noqa: PLR2004
                print("\nUltime 5 righe caricate:")
                print(df_cleaned.tail())

                # Forse ci sono righe con ID-COEMI ma senza altre info?
                if id_col:
                    valid_ids = df[df[id_col].notna() & (df[id_col].astype(str).str.strip() != "")]
                    print(f"Righe con ID-COEMI non vuoto: {len(valid_ids)}")

    except Exception as e:
        print(f"Errore durante l'analisi: {e}")


if __name__ == "__main__":
    debug_import()
