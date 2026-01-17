import sqlite3
import time
from pathlib import Path

from src.core.data_synchronizer import DataSynchronizer


def setup_test_db(db_path, num_rows=10000):
    if db_path.exists():
        db_path.unlink()

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contabilita (
                year INTEGER,
                data_prev TEXT,
                mese TEXT,
                n_prev TEXT,
                totale_prev REAL,
                attivita TEXT,
                tcl TEXT,
                odc TEXT,
                stato_attivita TEXT,
                tipologia TEXT,
                ore_sp REAL,
                resa REAL,
                annotazioni TEXT,
                indirizzo_consuntivo TEXT,
                nome_file TEXT
            )
        """
        )

        # Populate with some dummy data
        # target_columns = ["year"] + [data_prev, mese, n_prev, totale_prev, attivita, tcl, odc, stato_attivita, tipologia, ore_sp, resa, annotazioni, indirizzo_consuntivo, nome_file]
        data = [
            (
                2024,
                f"2024-01-{i % 28 + 1:02d}",
                "Gennaio",
                f"P-{i}",
                100.0,
                "Attività Test",
                "TCL",
                "ODC",
                "Aperto",
                "Tipo",
                8.0,
                12.5,
                "Nota",
                "C:\\test",
                "file.xlsx",
            )
            for i in range(num_rows)
        ]
        conn.executemany("INSERT INTO contabilita VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
        conn.commit()
    return data


def run_benchmark():
    db_path = Path("benchmark_sync.db")
    num_rows = 10000
    existing_data = setup_test_db(db_path, num_rows)

    # Create new data: 9000 same, 1000 different (added), 1000 from existing are "missing" (removed)
    # We take rows 1000 to 10000 (9000 rows)
    new_data = existing_data[1000:]
    # Add 1000 new rows
    for i in range(1000):
        new_data.append(
            (
                2024,
                "2024-12-01",
                "Dicembre",
                f"NEW-{i}",
                200.0,
                "Nuova",
                "TCL",
                "ODC",
                "Chiuso",
                "Tipo",
                4.0,
                50.0,
                "Nota",
                "C:\\test",
                "new.xlsx",
            )
        )

    print(f"Benchmarking with {num_rows} rows...")

    start_time = time.time()
    # In this scenario:
    # - 1000 rows were in existing but not in new_data -> removed
    # - 1000 rows are in new_data but were not in existing -> added
    # - 9000 rows are identical
    added, removed = DataSynchronizer.sync_contabilita_dati(db_path, new_data, [2024])
    end_time = time.time()

    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"Added: {added}, Removed: {removed}")

    if db_path.exists():
        db_path.unlink()


if __name__ == "__main__":
    run_benchmark()
