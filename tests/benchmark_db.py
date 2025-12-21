
import sqlite3
import time
import os

DB_PATH = "benchmark_contabilita_db.db"

def create_large_db(rows=200000):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE contabilita (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            data_prev TEXT
        )
    """)
    
    years = [2020, 2021, 2022, 2023, 2024]
    data = []
    print(f"Generating {rows} rows...")
    for i in range(rows):
        year = years[i % 5]
        data.append((year, '2024-01-01'))
    
    cursor.executemany("INSERT INTO contabilita (year, data_prev) VALUES (?, ?)", data)
    conn.commit()
    conn.close()

def benchmark_delete_no_index():
    print("Benchmarking DELETE (No Index)...")
    create_large_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    start = time.time()
    cursor.execute("DELETE FROM contabilita WHERE year = 2020")
    conn.commit()
    end = time.time()
    print(f"DELETE time (no index): {end - start:.4f}s")
    conn.close()

def benchmark_delete_with_index():
    print("Benchmarking DELETE (With Index)...")
    create_large_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("CREATE INDEX idx_year ON contabilita(year)")
    conn.commit()
    
    start = time.time()
    cursor.execute("DELETE FROM contabilita WHERE year = 2020")
    conn.commit()
    end = time.time()
    print(f"DELETE time (WITH index): {end - start:.4f}s")
    conn.close()

if __name__ == "__main__":
    benchmark_delete_no_index()
    benchmark_delete_with_index()
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
