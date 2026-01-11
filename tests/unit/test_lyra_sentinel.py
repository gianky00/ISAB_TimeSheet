import sqlite3
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import QCoreApplication

# Simula QApplication prima di importare LyraSentinel per evitare errori di Qt
app = QCoreApplication([])

from src.core.lyra_sentinel import LyraSentinel  # noqa: E402


@pytest.fixture
def mock_db_path(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    db_file = data_dir / "timbrature_Isab.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE timbrature (id INTEGER PRIMARY KEY, uscita TEXT, data TEXT)")
    conn.commit()
    conn.close()
    return db_file


def test_lyra_sentinel_timbrature_anomaly(mocker, tmp_path, mock_db_path):
    # Patch CONFIG_DIR in lyra_sentinel to use tmp_path
    mocker.patch("src.core.lyra_sentinel.CONFIG_DIR", tmp_path)

    # Inserisci un'anomalia: uscita mancante (negli ultimi 30 giorni)
    conn = sqlite3.connect(mock_db_path)
    cursor = conn.cursor()
    # data < date('now') and data > date('now', '-30 days')
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO timbrature (uscita, data) VALUES (?, ?)",
        ("", yesterday),
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


def test_lyra_sentinel_contabilita_anomaly(mocker, tmp_path):
    # Patch CONFIG_DIR to avoid real DB access
    mocker.patch("src.core.lyra_sentinel.CONFIG_DIR", tmp_path)

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


def test_lyra_sentinel_no_anomalies(mocker, tmp_path, mock_db_path):
    # Patch CONFIG_DIR
    mocker.patch("src.core.lyra_sentinel.CONFIG_DIR", tmp_path)

    conn = sqlite3.connect(mock_db_path)
    cursor = conn.cursor()
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO timbrature (uscita, data) VALUES (?, ?)",
        ("17:00", yesterday),
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
