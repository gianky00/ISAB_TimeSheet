r"""
Debug script per diagnosticare problemi di importazione Giornaliere.
Esegui con: .venv\Scripts\python.exe scripts\debug_giornaliere.py
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from pathlib import Path

import pandas as pd

from src.core import config_manager


def debug_giornaliere():
    print("=" * 70)
    print("DEBUG IMPORTAZIONE GIORNALIERE")
    print("=" * 70)

    # 1. Leggi configurazione
    config = config_manager.load_config()
    giornaliere_path = config.get("giornaliere_path", "")

    print(f"\n[1] Path configurato: {giornaliere_path}")

    if not giornaliere_path or not Path(giornaliere_path).exists():
        print("    ERRORE: Path non trovato!")
        return

    root = Path(giornaliere_path)
    print("    OK: Directory esiste")

    # 2. Scansiona cartelle
    print(f"\n[2] Scansione cartelle in: {root}")
    print("-" * 50)

    folders_found = []
    for item in root.iterdir():
        if item.is_dir():
            match = re.match(r"Giornaliere\s+(\d{4})", item.name, re.IGNORECASE)
            if match:
                year = int(match.group(1))
                folders_found.append((year, item))
                print(f"    [OK] {item.name} -> Anno {year}")
            else:
                print(f"    [SKIP] {item.name} (non matcha pattern 'Giornaliere YYYY')")

    if not folders_found:
        print("    ERRORE: Nessuna cartella Giornaliere trovata!")
        return

    # 3. Per ogni cartella, analizza i file
    print("\n[3] Analisi file Excel per ogni anno")
    print("=" * 70)

    for year, folder in sorted(folders_found):
        print(f"\n>>> ANNO {year}: {folder.name}")
        print("-" * 50)

        excel_files = list(folder.glob("*.xls*"))
        excel_files = [f for f in excel_files if not f.name.startswith("~$")]

        print(f"    File Excel trovati: {len(excel_files)}")

        if not excel_files:
            print("    ATTENZIONE: Nessun file Excel nella cartella!")
            continue

        for file_path in excel_files[:3]:  # Analizza max 3 file per anno
            print(f"\n    FILE: {file_path.name}")

            try:
                # Prova a leggere i fogli disponibili
                xl = pd.ExcelFile(file_path)
                sheets = xl.sheet_names
                print(f"        Fogli disponibili: {sheets}")

                if "RIASSUNTO" not in sheets:
                    print("        ERRORE: Foglio 'RIASSUNTO' non trovato!")
                    continue

                # Leggi il foglio RIASSUNTO
                df = pd.read_excel(file_path, sheet_name="RIASSUNTO")
                print(f"        Righe lette: {len(df)}")
                print(f"        Colonne trovate: {list(df.columns)}")

                # Verifica se prima riga sembra un header valido
                first_cols = [str(c).upper().strip() for c in df.columns]
                expected_headers = ["DATA", "PERSONALE", "ORE", "TCL"]
                headers_found = sum(1 for h in expected_headers if any(h in c for c in first_cols))
                print(f"        Header validi trovati: {headers_found}/4 ({expected_headers})")

                if headers_found < 2:
                    print("        ATTENZIONE: Header probabilmente in riga diversa!")
                    print("        Prime 3 righe del file:")
                    df_raw = pd.read_excel(file_path, sheet_name="RIASSUNTO", header=None, nrows=5)
                    for i, row in df_raw.head(3).iterrows():
                        print(f"            Riga {i}: {list(row.values)[:6]}...")

                # Verifica colonne critiche
                expected_cols = ["DATA", "PERSONALE", "ORE", "consuntivo"]
                missing = []
                found = []
                for col in expected_cols:
                    col_found = False
                    for actual_col in df.columns:
                        if str(actual_col).upper().strip() == col.upper():
                            col_found = True
                            found.append(f"{col} -> {actual_col}")
                            break
                    if not col_found:
                        missing.append(col)

                if found:
                    print(f"        Colonne mappate: {found}")
                if missing:
                    print(f"        COLONNE MANCANTI: {missing}")

                # Mostra prime righe della colonna n_prev se esiste
                for col in df.columns:
                    col_upper = str(col).upper().strip()
                    if "PREV" in col_upper or "CONSUNTIVO" in col_upper:
                        print(f"        Colonna '{col}' - primi 5 valori: {df[col].head().tolist()}")

            except Exception as e:
                print(f"        ERRORE lettura: {e}")

        if len(excel_files) > 3:
            print(f"\n    ... e altri {len(excel_files) - 3} file")

    print("\n" + "=" * 70)
    print("DEBUG COMPLETATO")
    print("=" * 70)


def debug_import_simulation():
    """Simula l'importazione per capire dove si perdono i dati."""
    print("\n" + "=" * 70)
    print("DEBUG SIMULAZIONE IMPORTAZIONE")
    print("=" * 70)

    from pathlib import Path

    from src.core import config_manager
    from src.core.importers.giornaliere import GiornaliereImporter

    config = config_manager.load_config()
    giornaliere_path = config.get("giornaliere_path", "")

    if not giornaliere_path:
        print("Path non configurato!")
        return

    root = Path(giornaliere_path)
    print(f"\n[1] MIN_IMPORT_YEAR: {GiornaliereImporter.MIN_IMPORT_YEAR}")

    # Simula raccolta task
    print("\n[2] Raccolta task...")
    tasks = GiornaliereImporter._collect_giornaliere_tasks(root, {})
    print(f"    Task raccolti: {len(tasks)}")

    # Raggruppa per anno
    by_year: dict[int, list[str]] = {}
    for year, path, _ in tasks:
        by_year.setdefault(year, []).append(path.name)

    for year in sorted(by_year.keys()):
        print(f"    Anno {year}: {len(by_year[year])} file")

    # Prova a processare un file 2025
    print("\n[3] Test processamento file 2025...")
    tasks_2025 = [(y, p, lm) for y, p, lm in tasks if y == 2025]

    if not tasks_2025:
        print("    Nessun file 2025 trovato!")
        return

    test_task = tasks_2025[0]
    print(f"    File test: {test_task[1].name}")

    try:
        year, rows, err = GiornaliereImporter._process_single_giornaliera(test_task)
        print(f"    Anno: {year}")
        print(f"    Righe estratte: {len(rows) if rows else 0}")
        print(f"    Errore: {err}")

        if rows and len(rows) > 0:
            print("\n    Prima riga (sample):")
            print(f"    {rows[0][:5]}...")  # Prime 5 colonne
    except Exception as e:
        print(f"    ERRORE: {e}")
        import traceback

        traceback.print_exc()

    # Controlla database attuale
    print("\n[4] Stato database attuale...")
    from src.core.contabilita_manager import ContabilitaManager

    for year in [2025, 2026]:
        data = ContabilitaManager.get_giornaliere_by_year(year)
        print(f"    Anno {year}: {len(data)} righe nel DB")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    debug_giornaliere()
    print("\n\nVuoi eseguire la simulazione di import? (s/n)")
    choice = input().strip().lower()
    if choice == "s":
        debug_import_simulation()
