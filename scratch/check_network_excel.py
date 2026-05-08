import pandas as pd

net_path = r"//192.168.11.251/Database_Tecnico_SMI/CERTIFICATI CAMPIONE/Registro calibrazioni/STRUMENTI CAMPIONE ISAB SUD AGGIORNATO.xlsm"
print(f"Checking Network Excel at: {net_path}")

try:
    xls = pd.ExcelFile(net_path)
    sheet_name = None
    for name in xls.sheet_names:
        if "strumenti campione" in name.lower() or "isab sud" in name.lower():
            sheet_name = name
            break
    if not sheet_name:
        sheet_name = xls.sheet_names[0]

    df = pd.read_excel(net_path, sheet_name=sheet_name, header=5)
    df.columns = df.columns.astype(str).str.strip()

    row = df[df["ID-COEMI"] == "CAT01563"]
    if row.empty:
        print("CAT01563 NOT FOUND in Network Excel")
    else:
        print("CAT01563 found in Network Excel:")
        print(row[["ID-COEMI", "Certificato Taratura", "Scadenza Certificato"]])

    print(f"Total rows in Network Excel: {len(df)}")

except Exception as e:
    print(f"Error: {e}")
