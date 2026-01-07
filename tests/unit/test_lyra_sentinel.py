import sqlite3
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import QCoreApplication

# Simula QApplication prima di importare LyraSentinel per evitare errori di Qt
app = QCoreApplication([])

from src.core.lyra_sentinel import LyraSentinel


@pytest.fixture
def mock_db_path(tmp_path):
    db_file = tmp_path / "timbrature_Isab.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE timbrature (id INTEGER PRIMARY KEY, uscita TEXT, data TEXT)")
    conn.commit()
    conn.close()
    return db_file


def test_lyra_sentinel_timbrature_anomaly(mocker, mock_db_path):
    # Mock per il percorso del DB
    mocker.patch("src.core.lyra_sentinel.Path", return_value=mock_db_path)

    # Inserisci un'anomalia: uscita mancante
    conn = sqlite3.connect(mock_db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO timbrature (uscita, data) VALUES (?, ?)",
        ("", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")),
    )
    conn.commit()
    conn.close()

    # Mock per ContabilitaManager per non interferire
    mocker.patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[])

    sentinel = LyraSentinel()
    mock_anomalies_found = MagicMock()
    sentinel.anomalies_found.connect(mock_anomalies_found)

    sentinel.run()

    mock_anomalies_found.assert_called_once_with(1)


def test_lyra_sentinel_contabilita_anomaly(mocker):
    # Mock per il DB timbrature (nessuna anomalia)
    mocker.patch("src.core.lyra_sentinel.Path", return_value=MagicMock(exists=MagicMock(return_value=False)))

    # Mock per ContabilitaManager con anomalia (margine negativo)
    mocker.patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2026])
    mocker.patch(
        "src.core.contabilita_manager.ContabilitaManager.get_year_stats",
        return_value={"total_prev": 100.0, "total_ore": 10.0},
    )

    sentinel = LyraSentinel()
    mock_anomalies_found = MagicMock()
    sentinel.anomalies_found.connect(mock_anomalies_found)

    sentinel.run()

    mock_anomalies_found.assert_called_once_with(1)


def test_lyra_sentinel_no_anomalies(mocker, mock_db_path):
    # Mock per il DB timbrature (nessuna anomalia)
    mocker.patch("src.core.lyra_sentinel.Path", return_value=mock_db_path)
    conn = sqlite3.connect(mock_db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO timbrature (uscita, data) VALUES (?, ?)",
        ("17:00", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")),
    )
    conn.commit()
    conn.close()

    # Mock per ContabilitaManager (nessuna anomalia)
    mocker.patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2026])
    mocker.patch(
        "src.core.contabilita_manager.ContabilitaManager.get_year_stats",
        return_value={"total_prev": 100.0, "total_ore": 1.0},
    )

    sentinel = LyraSentinel()
    mock_anomalies_found = MagicMock()
    sentinel.anomalies_found.connect(mock_anomalies_found)

    sentinel.run()

    mock_anomalies_found.assert_called_once_with(0)
