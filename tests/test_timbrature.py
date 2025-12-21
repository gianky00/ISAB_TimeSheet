"""
Tests for Timbrature module.
"""
import pytest
import sqlite3
import pandas as pd
from pathlib import Path
from src.bots.timbrature.storage import TimbratureStorage

@pytest.fixture
def temp_db(tmp_path):
    """Fixture per creare un DB temporaneo."""
    db_file = tmp_path / "test_timbrature.db"
    return db_file

@pytest.fixture
def storage(temp_db):
    """Fixture per creare uno storage con DB temporaneo."""
    storage = TimbratureStorage(temp_db)
    return storage

def test_db_creation(temp_db, storage):
    """Test che il database venga creato correttamente."""
    assert temp_db.exists()

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timbrature'")
    table = cursor.fetchone()
    conn.close()

    assert table is not None

def test_import_logic(temp_db, storage, tmp_path):
    """Test dell'importazione dati da Excel e prevenzione duplicati."""

    # 1. Crea un Excel di test
    excel_data = {
        "Data Timbratura": ["01.01.2025", "01.01.2025"],
        "Ora Ingresso": ["08:00", "09:00"],
        "Ora Uscita": ["17:00", "18:00"],
        "Nome Risorsa": ["Mario", "Luigi"],
        "Cognome Risorsa": ["Rossi", "Verdi"],
        "Presente Nei Timesheet": ["SI", "NO"],
        "Sito Timbratura": ["Sito A", "Sito B"],
        "Extra Column": ["Ignore", "Ignore"]
    }
    df = pd.DataFrame(excel_data)
    excel_file = tmp_path / "test_import.xlsx"
    df.to_excel(excel_file, index=False)

    # 2. Esegui import
    storage.import_excel(str(excel_file))

    # 3. Verifica DB
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timbrature ORDER BY nome")
    rows = cursor.fetchall()
    conn.close()

    # Dovremmo avere 2 righe
    # id, data, ingresso, uscita, nome, cognome, presenza_ts, sito_timbratura
    assert len(rows) == 2
    # Check index 4 (nome)
    # The order by nome means Luigi comes before Mario?
    # Luigi L, Mario M. Yes.
    assert rows[0][4] == "Luigi" # nome
    assert rows[1][4] == "Mario" # nome

    # 4. Test Duplicati: Importa lo stesso file
    storage.import_excel(str(excel_file))

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM timbrature")
    count = cursor.fetchone()[0]
    conn.close()

    # Il numero di righe non deve essere cambiato
    assert count == 2

def test_import_new_data(temp_db, storage, tmp_path):
    """Test che nuovi dati vengano aggiunti correttamente."""

    # Import iniziale
    data1 = {
        "Data Timbratura": ["01.01.2025"],
        "Ora Ingresso": ["08:00"],
        "Ora Uscita": ["17:00"],
        "Nome Risorsa": ["Mario"],
        "Cognome Risorsa": ["Rossi"],
        "Presente Nei Timesheet": ["SI"],
        "Sito Timbratura": ["Sito A"]
    }
    df1 = pd.DataFrame(data1)
    file1 = tmp_path / "test1.xlsx"
    df1.to_excel(file1, index=False)
    storage.import_excel(str(file1))

    # Import nuovi dati (uno duplicato, uno nuovo)
    data2 = {
        "Data Timbratura": ["01.01.2025", "02.01.2025"],
        "Ora Ingresso": ["08:00", "08:30"],
        "Ora Uscita": ["17:00", "17:30"],
        "Nome Risorsa": ["Mario", "Mario"],
        "Cognome Risorsa": ["Rossi", "Rossi"],
        "Presente Nei Timesheet": ["SI", "SI"],
        "Sito Timbratura": ["Sito A", "Sito A"]
    }
    df2 = pd.DataFrame(data2)
    file2 = tmp_path / "test2.xlsx"
    df2.to_excel(file2, index=False)
    storage.import_excel(str(file2))

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timbrature")
    rows = cursor.fetchall()
    conn.close()

    # Totale atteso: 2 righe (Mario 01.01 e Mario 02.01)
    assert len(rows) == 2
