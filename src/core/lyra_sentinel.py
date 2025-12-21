"""
Lyra Sentinel
Monitoraggio proattivo delle anomalie in background.
"""
from PyQt6.QtCore import QThread, pyqtSignal
from src.core.contabilita_manager import ContabilitaManager
from pathlib import Path
import sqlite3

class LyraSentinel(QThread):
    """Worker che controlla periodicamente lo stato del sistema."""

    anomalies_found = pyqtSignal(int) # Emette il numero di anomalie trovate

    def run(self):
        anomaly_count = 0

        # 1. Check Timbrature (Uscite mancanti recenti)
        try:
            db_path = Path("data/timbrature_Isab.db")
            if db_path.exists():
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                # Uscita mancante negli ultimi 30 giorni (escludendo oggi che potrebbe essere in corso)
                cursor.execute("SELECT COUNT(*) FROM timbrature WHERE (uscita IS NULL OR uscita = '') AND data > date('now', '-30 days') AND data < date('now')")
                res = cursor.fetchone()
                if res:
                    anomaly_count += res[0]
                conn.close()
        except:
            pass

        # 2. Check Contabilita (Margine negativo anno corrente)
        try:
            years = ContabilitaManager.get_available_years()
            if years:
                latest = max(years)
                stats = ContabilitaManager.get_year_stats(latest)
                margin = stats.get('total_prev', 0) - (stats.get('total_ore', 0) * 30.0)
                if margin < 0:
                    anomaly_count += 1
        except:
            pass

        self.anomalies_found.emit(anomaly_count)
