"""
Lyra Sentinel
Monitoraggio proattivo delle anomalie in background.
"""

import sqlite3
from contextlib import suppress
from pathlib import Path  # noqa: F401

from PyQt6.QtCore import QThread, pyqtSignal

from src.core.config_manager import CONFIG_DIR
from src.core.constants import Business, FileNames
from src.core.contabilita_manager import ContabilitaManager


class LyraSentinel(QThread):
    """Worker che controlla periodicamente lo stato del sistema."""

    anomalies_found = pyqtSignal(int)  # Emette il numero di anomalie trovate

    def run(self):
        """Esegue i controlli di integrità in background su Timbrature e Contabilità."""
        anomaly_count = 0

        # 1. Check Timbrature (Uscite mancanti recenti)
        with suppress(Exception):
            db_path = CONFIG_DIR / "data" / FileNames.DB_TIMBRATURE
            if db_path.exists():
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                # Uscita mancante negli ultimi 30 giorni (escludendo oggi che potrebbe essere in corso)
                cursor.execute(
                    "SELECT COUNT(*) FROM timbrature WHERE (uscita IS NULL OR uscita = '') AND data > date('now', '-30 days') AND data < date('now')"
                )
                res = cursor.fetchone()
                if res:
                    anomaly_count += res[0]
                conn.close()

        # 2. Check Contabilita (Margine negativo anno corrente)
        with suppress(Exception):
            years = ContabilitaManager.get_available_years()
            if years:
                latest = max(years)
                stats = ContabilitaManager.get_year_stats(latest)
                margin = stats.get("total_prev", 0) - (stats.get("total_ore", 0) * Business.HOURLY_COST_STD)
                if margin < 0:
                    anomaly_count += 1

        self.anomalies_found.emit(anomaly_count)
