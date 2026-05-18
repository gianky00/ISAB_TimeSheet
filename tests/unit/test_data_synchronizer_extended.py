import pytest

from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager


class TestDataSynchronizerDetailed:
    @pytest.fixture
    def real_db(self, tmp_path):
        db_path = tmp_path / "test_sync_ext.db"
        with db_manager.get_connection(db_path) as conn:
            # GIORNALIERE: 12 colonne
            conn.execute("""
                CREATE TABLE IF NOT EXISTS giornaliere (
                    year INTEGER, data TEXT, personale TEXT, descrizione TEXT,
                    tcl TEXT, odc TEXT, pdl TEXT, inizio TEXT, fine TEXT,
                    ore REAL, n_prev TEXT, nome_file TEXT
                )
            """)
            # ATTIVITA_PROGRAMMATE: 17 colonne
            conn.execute("""
                CREATE TABLE IF NOT EXISTS attivita_programmate (
                    ps TEXT, area TEXT, pdl TEXT, imp TEXT, descrizione TEXT,
                    lun TEXT, mar TEXT, mer TEXT, gio TEXT, ven TEXT,
                    stato_pdl TEXT, stato_attivita TEXT, data_controllo TEXT,
                    personale TEXT, po TEXT, avviso TEXT, styles TEXT
                )
            """)
            # SCARICO_ORE: 12 colonne
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scarico_ore (
                    data TEXT, pers1 TEXT, pers2 TEXT, odc TEXT, pos TEXT,
                    dalle TEXT, alle TEXT, totale_ore REAL, descrizione TEXT,
                    finito TEXT, commessa TEXT, styles TEXT
                )
            """)
            # CERTIFICATI: 12 colonne (10 mappate + 2 metadati)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS certificati_campione (
                    modello TEXT, costruttore TEXT, matricola TEXT, range_strumento TEXT,
                    errore_max TEXT, certificato TEXT, scadenza TEXT, emissione TEXT,
                    id_coemi TEXT, stato TEXT, ubicazione TEXT, annotazioni TEXT,
                    PRIMARY KEY (matricola, certificato)
                )
            """)
            # CONTABILITA: 15 colonne (year + 14 mappate)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS contabilita (
                    year INTEGER, data_prev TEXT, mese TEXT, n_prev TEXT,
                    totale_prev REAL, attivita TEXT, tcl TEXT, odc TEXT,
                    stato_attivita TEXT, tipologia TEXT, ore_sp REAL,
                    resa TEXT, annotazioni TEXT, indirizzo_consuntivo TEXT, nome_file TEXT
                )
            """)
        return db_path

    def test_sync_contabilita_dati_empty(self, real_db):
        added, removed = DataSynchronizer.sync_contabilita_dati(real_db, [], [])
        assert added == 0
        assert removed == 0

    def test_sync_giornaliere_logic(self, real_db):
        new_rows = [(2024, "2024-01-01", "P", "D", "T", "O", "P", "08", "17", 8.0, "100", "f.xlsx")]
        added, removed = DataSynchronizer.sync_giornaliere(real_db, new_rows, [2024])
        assert added == 1
        assert removed == 0

    def test_sync_attivita_programmate(self, real_db):
        with db_manager.get_connection(real_db) as conn:
            conn.execute("INSERT INTO attivita_programmate (ps) VALUES ('old1')")

        # 17 colonne per attivita_programmate
        new_rows = [("ps1", "a", "p", "i", "d", "l", "m", "m", "g", "v", "s", "s", "d", "p", "p", "a", "s")]
        added, removed = DataSynchronizer.sync_attivita_programmate(real_db, new_rows)
        # Delta netto: sync_full_replace restituisce len(final_rows)
        assert added == 1
        # Il removed è 0 perché sync_full_replace non calcola il delta dei rimossi ma svuota e reinserisce
        assert removed == 0

    def test_sync_scarico_ore(self, real_db):
        # 12 colonne per scarico_ore
        new_rows = [("2024-01-01", "p1", "p2", "o1", "p1", "08", "17", 8.0, "d1", "f", "c1", "s")]
        added, removed = DataSynchronizer.sync_scarico_ore(real_db, new_rows)
        assert added == 1
        assert removed == 0

    def test_sync_certificati_campione(self, real_db):
        # 10 colonne per certificati_campione
        new_rows = [("M", "C", "M1", "R", "E", "C1", "S", "E1", "ID1", "OK")]
        added, removed = DataSynchronizer.sync_certificati_campione(real_db, new_rows)
        assert added == 1
        assert removed == 0
