"""
Unit Tests for Universal Search Features
Tests extended search capabilities across ContabilitaManager and TimbratureStorage.
"""

import sqlite3
from unittest.mock import patch

import pytest

from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage
from src.core.contabilita_manager import ContabilitaManager


@pytest.fixture
def mock_db(tmp_path):
    """Creates a temporary database with sample data for testing search."""
    db_path = tmp_path / "test_contabilita.db"
    ContabilitaManager.DB_PATH = db_path

    with sqlite3.connect(db_path) as conn:
        # Contabilita
        conn.execute("CREATE TABLE contabilita (n_prev TEXT, attivita TEXT, odc TEXT, year INTEGER)")
        conn.execute(
            "INSERT INTO contabilita VALUES ('123/2025', 'Manutenzione Valvole', '5400123456', 2025)"
        )
        conn.execute("INSERT INTO contabilita VALUES ('124/2025', 'Ponteggi', '5400999999', 2025)")

        # Giornaliere
        conn.execute("CREATE TABLE giornaliere (data TEXT, personale TEXT, descrizione TEXT, year INTEGER)")
        conn.execute(
            "INSERT INTO giornaliere VALUES ('2025-01-01', 'Mario Rossi', 'Lavoro su ponteggi', 2025)"
        )

        # Scarico Ore
        conn.execute(
            "CREATE TABLE scarico_ore (data TEXT, pers1 TEXT, pers2 TEXT, descrizione TEXT, commessa TEXT)"
        )
        conn.execute(
            "INSERT INTO scarico_ore VALUES ('2025-01-02', 'Luigi Verdi', '', 'Cablaggio quadri', 'C123')"
        )

        # Certificati
        conn.execute("CREATE TABLE certificati_campione (modello TEXT, costruttore TEXT, matricola TEXT)")
        conn.execute("INSERT INTO certificati_campione VALUES ('Multimetro', 'Fluke', 'SN-8888')")

    return db_path


@pytest.fixture
def mock_timbrature_db(tmp_path):
    """Creates a temporary timbrature database."""
    db_path = tmp_path / "test_timbrature.db"

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE timbrature (
                data TEXT, 
                ingresso TEXT, 
                uscita TEXT, 
                nome TEXT, 
                cognome TEXT, 
                presenza_ts TEXT, 
                sito_timbratura TEXT
            )
        """
        )
        conn.execute(
            "INSERT INTO timbrature VALUES ('2025-01-01', '08:00', '17:00', 'Mario', 'Rossi', 'OK', 'Sito A')"
        )
        conn.execute(
            "INSERT INTO timbrature VALUES ('2025-01-01', '08:00', '17:00', 'Giuseppe', 'Bianchi', 'OK', 'Sito B')"
        )

    return db_path


def test_search_oda_found(mock_db):
    """Test searching for OdA by code."""
    results = ContabilitaManager.search_oda("123")
    assert len(results) == 1
    assert results[0]["codice_oda"] == "123/2025"
    assert results[0]["type"] == "ODA"


def test_search_oda_description(mock_db):
    """Test searching for OdA by description (case insensitive)."""
    results = ContabilitaManager.search_oda("valvole")
    assert len(results) == 1
    assert "Manutenzione" in results[0]["descrizione"]


def test_search_extended_giornaliere(mock_db):
    """Test searching in Giornaliere."""
    results = ContabilitaManager.search_extended("Rossi")
    assert len(results["GIORNALIERE"]) == 1
    assert results["GIORNALIERE"][0]["personale"] == "Mario Rossi"


def test_search_extended_cantiere(mock_db):
    """Test searching in Scarico Ore (Cantiere)."""
    results = ContabilitaManager.search_extended("Cablaggio")
    assert len(results["CANTIERE"]) == 1
    assert "Verdi" in results["CANTIERE"][0]["personale"]


def test_search_extended_certificati(mock_db):
    """Test searching in Certificati."""
    results = ContabilitaManager.search_extended("Fluke")
    assert len(results["CERTIFICATI"]) == 1
    assert results["CERTIFICATI"][0]["matricola"] == "SN-8888"


def test_search_employees(mock_timbrature_db):
    """Test searching for employees in TimbratureStorage."""
    with patch("src.bots.portale_fornitori.timbrature.storage.TimbratureStorage.DB_PATH", mock_timbrature_db):
        storage = TimbratureStorage(mock_timbrature_db)
        results = storage.search_employees("Bianchi")
        assert len(results) == 1
        assert results[0]["cognome"] == "Bianchi"
        assert results[0]["nome"] == "Giuseppe"


def test_search_empty_query(mock_db):
    """Test behavior with empty or short queries."""
    assert ContabilitaManager.search_oda("") == []
    assert ContabilitaManager.search_extended("a") == {}
