"""
Unit tests for LyraSentinel.
"""

import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from src.core.lyra_sentinel import LyraSentinel


class TestLyraSentinel:
    @pytest.fixture
    def sentinel(self):
        return LyraSentinel()

    def test_run_timbrature_anomalies(self, sentinel, tmp_path, mocker):
        """Verifica il rilevamento di timbrature senza uscita."""
        # Setup mock database
        db_dir = tmp_path / "data"
        db_dir.mkdir()
        db_path = db_dir / "timbrature_Isab.db"

        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE timbrature (data TEXT, ingresso TEXT, uscita TEXT)")
        # Anomalia: uscita nulla negli ultimi 30 giorni (escludendo oggi)
        # Assumiamo che date('now') sia simulata o che i dati siano vecchi abbastanza
        conn.execute("INSERT INTO timbrature VALUES (date('now', '-5 days'), '08:00', NULL)")
        conn.execute("INSERT INTO timbrature VALUES (date('now', '-10 days'), '08:00', '')")
        conn.execute("INSERT INTO timbrature VALUES (date('now'), '08:00', NULL)")  # Oggi, ignorata
        conn.commit()
        conn.close()

        with (
            patch("src.core.lyra_sentinel.CONFIG_DIR", tmp_path),
            patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[]),
        ):
            # Usiamo un signal spy o mock
            mock_signal = MagicMock()
            sentinel.anomalies_found.connect(mock_signal)

            sentinel.run()

            # Dovrebbe aver trovato 2 anomalie (i record a -5 e -10 giorni)
            mock_signal.assert_called_once_with(2)

    def test_run_contabilita_negative_margin(self, sentinel, mocker):
        """Verifica il rilevamento di margine negativo in contabilità."""
        with (
            patch("src.core.lyra_sentinel.CONFIG_DIR", MagicMock()),
            patch("src.core.lyra_sentinel.Path.exists", return_value=False),  # Salta timbrature
            patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2026]),
            patch(
                "src.core.contabilita_manager.ContabilitaManager.get_year_stats",
                return_value={
                    "total_prev": 1000,
                    "total_ore": 50,  # 50 * 30 = 1500 -> Margine = 1000 - 1500 = -500 (Negativo!)
                },
            ),
        ):
            mock_signal = MagicMock()
            sentinel.anomalies_found.connect(mock_signal)

            sentinel.run()

            # Dovrebbe aver trovato 1 anomalia (margine negativo)
            mock_signal.assert_called_once_with(1)

    def test_run_no_anomalies(self, sentinel, mocker):
        """Verifica che emetta 0 se tutto è in regola."""
        with (
            patch("src.core.lyra_sentinel.CONFIG_DIR", MagicMock()),
            patch("src.core.lyra_sentinel.Path.exists", return_value=False),
            patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2026]),
            patch(
                "src.core.contabilita_manager.ContabilitaManager.get_year_stats",
                return_value={
                    "total_prev": 5000,
                    "total_ore": 100,  # Margine = 5000 - 3000 = 2000 (Positivo)
                },
            ),
        ):
            mock_signal = MagicMock()
            sentinel.anomalies_found.connect(mock_signal)

            sentinel.run()

            mock_signal.assert_called_once_with(0)
