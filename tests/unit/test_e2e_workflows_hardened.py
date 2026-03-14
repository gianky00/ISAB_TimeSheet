import sqlite3

import pandas as pd
import pytest

from src.core.database import DatabaseManager
from src.core.database.migrations.contabilita import (
    mig_contabilita_v1,
    mig_contabilita_v2,
    mig_contabilita_v3,
)
from src.core.excel_importer import ExcelImporter
from src.core.lyra_sentinel import LyraSentinel
from src.core.notification_manager import NotificationManager


class TestE2EWorkflowsHardened:
    @pytest.fixture
    def db_mgr(self, tmp_path, mocker):
        mocker.patch("src.core.database.manager.CONFIG_DIR", tmp_path)
        return DatabaseManager()

    def test_workflow_import_to_search(self, db_mgr, tmp_path, mocker):
        """E2E: Simula download bot -> Importazione -> Ricerca FTS5."""
        # 1. Setup DB con migrazioni complete
        db_path = tmp_path / "data" / "contabilita.db"
        db_mgr.DB_CONTABILITA = db_path
        db_mgr._ensure_dirs()

        with db_mgr.get_connection(db_path) as conn:
            mig_contabilita_v1(conn)
            mig_contabilita_v2(conn)
            mig_contabilita_v3(conn)

        # 2. Crea file Excel "scaricato dal bot" con intestazioni esatte
        excel_path = tmp_path / "bot_download.xlsx"
        df_data = {
            "DATA PREV.": ["01/01/2024", "02/01/2024"],
            "MESE": ["Gennaio", "Gennaio"],
            "N° PREV.": ["P123", "P124"],
            "TOTALE PREV.": ["1000", "2000"],
            "ATTIVITA'": ["Manutenzione Speciale Meccanica", "Altra Attivita"],
            "ODC": ["54001234", "54001235"],
            "TCL": ["T1", "T1"],
            "STATO ATTIVITA'": ["IN CORSO", "COMPLETATO"],
            "TIPOLOGIA": ["VARIE", "VARIE"],
            "ORE SP": ["10", "20"],
            "RESA": ["100", "100"],
            "ANNOTAZIONI": ["Nessuna", "Note"],
            "INDIRIZZO CONSUNTIVO": ["C:/test", "C:/test2"],
            "NOME FILE": ["test.pdf", "test2.pdf"],
        }
        df = pd.DataFrame(df_data)
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            # Il nome del foglio deve contenere l'anno per essere riconosciuto
            df.to_excel(writer, sheet_name="DATI 2024", index=False)

        # 3. Importazione via ExcelImporter
        success, msg, rows, _years = ExcelImporter.import_contabilita_dati(str(excel_path))
        assert success is True, f"Import fallito: {msg}"
        assert len(rows) > 0

        # 4. Salvataggio nel DB
        # ExcelImporter restituisce tuple (year, data_prev, mese, n_prev, totale_prev, attivita, tcl, odc, ...)
        cols = [
            "year",
            "data_prev",
            "mese",
            "n_prev",
            "totale_prev",
            "attivita",
            "tcl",
            "odc",
            "stato_attivita",
            "tipologia",
            "ore_sp",
            "resa",
            "annotazioni",
            "indirizzo_consuntivo",
            "nome_file",
        ]
        placeholders = ", ".join(["?"] * len(cols))
        insert_query = f"INSERT INTO contabilita ({', '.join(cols)}) VALUES ({placeholders})"

        # Inserimento della prima riga importata
        # Assicuriamoci che la tupla abbia la lunghezza corretta (15 colonne)
        # Convertiamo Timestamp in stringa per SQLite
        data_row = []
        for val in rows[0]:
            if hasattr(val, "isoformat"):
                data_row.append(val.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                data_row.append(val)

        while len(data_row) < len(cols):
            data_row.append("")

        db_mgr.execute_query(db_path, insert_query, tuple(data_row))

        # 5. Verifica indicizzazione FTS5 (Ricerca testuale "Meccanica")
        # Il trigger AI inserisce in contabilita_fts(rowid, n_prev, attivita, odc, annotazioni)
        search_query = "SELECT attivita FROM contabilita_fts WHERE attivita MATCH 'Meccanica'"
        results = db_mgr.execute_query(db_path, search_query)

        assert len(results) > 0, "Dato non trovato in FTS5 dopo l'inserimento!"
        assert "Meccanica" in results[0][0]

    def test_workflow_anomalies_to_notifications(self, db_mgr, tmp_path, mocker):
        """E2E: Dati sporchi -> Sentinel -> NotificationManager."""
        mocker.patch("src.core.lyra_sentinel.CONFIG_DIR", tmp_path)
        mocker.patch("src.core.config_manager.CONFIG_DIR", tmp_path)
        (tmp_path / "data").mkdir()
        db_path = tmp_path / "data" / "timbrature_Isab.db"

        # 1. Inserimento timbratura senza uscita
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE timbrature (data TEXT, uscita TEXT)")
        conn.execute("INSERT INTO timbrature VALUES (date('now', '-1 day'), '')")
        conn.commit()
        conn.close()

        # 2. Avvio Sentinel
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_available_years",
            return_value=[],
        )
        sentinel = LyraSentinel()

        # Monitoriamo i segnali
        anomalies_count = []
        sentinel.anomalies_found.connect(lambda n: anomalies_count.append(n))

        sentinel.run()
        assert anomalies_count[0] == 1

        # 3. Trigger Notifica
        notif_mgr = NotificationManager.instance()
        notif_mgr.add_notification(
            "Anomalia Rilevata",
            f"Trovate {anomalies_count[0]} timbrature errate",
            level="error",
        )

        # 4. Verifica persistenza notifica
        assert notif_mgr.get_unread_count() == 1
        assert "timbrature errate" in notif_mgr.notifications[0]["message"]
