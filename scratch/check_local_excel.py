import pandas as pd

local_path = r"C:\Users\Coemi\Desktop\CERTIFICATI CAMPIONE\Registro calibrazioni\STRUMENTI CAMPIONE ISAB SUD AGGIORNATO.xlsm"
print(f"Checking Local Excel at: {local_path}")

try:
    # Use pandas to read the Excel
    xls = pd.ExcelFile(local_path)
    # Find the sheet (using the same logic as the app)
    sheet_name = None
    for name in xls.sheet_names:
        if "strumenti campione" in name.lower() or "isab sud" in name.lower():
            sheet_name = name
            break
    if not sheet_name:
        sheet_name = xls.sheet_names[0]

    print(f"Reading sheet: {sheet_name}")

    # Read the first few rows to find the header (simplified)
    df_preview = pd.read_excel(local_path, sheet_name=sheet_name, header=None, nrows=20)
    header_idx = -1
    for i, row in df_preview.iterrows():
        if "ID-COEMI" in [str(v).strip() for v in row.values]:
            header_idx = i
            break

    if header_idx == -1:
        header_idx = 5

    print(f"Header at row: {header_idx}")

    df = pd.read_excel(local_path, sheet_name=sheet_name, header=header_idx)
    df.columns = df.columns.astype(str).str.strip()

    # Find CAT01563
    row = df[df["ID-COEMI"] == "CAT01563"]
    if row.empty:
        print("CAT01563 NOT FOUND in Local Excel")
    else:
        print("CAT01563 found in Local Excel:")
        print(row[["ID-COEMI", "Certificato Taratura", "Scadenza Certificato"]])

    print(f"Total rows in Local Excel: {len(df)}")

except Exception as e:
    print(f"Error: {e}")
