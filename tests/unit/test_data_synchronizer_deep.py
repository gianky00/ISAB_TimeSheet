
import pytest

from src.core.data_synchronizer import DataSynchronizer
from src.core.database import DatabaseManager


class TestDataSynchronizerDeep:
    @pytest.fixture
    def db_path(self, tmp_path):
        p = tmp_path / "test_sync.db"
        # Inizializza schema minimo per il test
        manager = DatabaseManager()
        with manager.get_connection(p) as conn:
            manager._mig_contabilita_v1(conn)
        return p

    def test_sync_contabilita_dati_incremental(self, db_path):
        """Verifica il calcolo corretto di aggiunte e rimozioni in contabilità."""
        # 1. Popolamento iniziale (Stato A)
        initial_data = [
            (2024, "01/01/2024", "Gen", "P1", "100", "Attivita 1", "T1", "ODC1", "OK", "T", "8", "100%", "Note", "Path", "File")
        ]
        DataSynchronizer.sync_contabilita_dati(db_path, initial_data, [2024])

        # 2. Modifica dati (Stato B):
        # - Rimuovi riga 1
        # - Aggiungi riga 2
        # - Aggiungi riga 3
        new_data = [
            (2024, "02/01/2024", "Gen", "P2", "200", "Attivita 2", "T1", "ODC2", "OK", "T", "8", "100%", "Note", "Path", "File"),
            (2024, "03/01/2024", "Gen", "P3", "300", "Attivita 3", "T1", "ODC3", "OK", "T", "8", "100%", "Note", "Path", "File")
        ]

        added, removed = DataSynchronizer.sync_contabilita_dati(db_path, new_data, [2024])

        assert added == 2
        assert removed == 1

        # Verifica persistenza
        with DatabaseManager().get_connection(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM contabilita WHERE year = 2024").fetchone()[0]
            assert count == 2

    def test_sync_giornaliere_by_year_isolation(self, db_path):
        """Verifica che la sincronizzazione per anno non influenzi altri anni."""
        # Setup: dati per 2023 e 2024
        data_2023 = [("2023", "01/01/2023", "User", "Desc", "TCL", "ODC", "PDL", "08:00", "17:00", "9", "PREV", "File23")]
        data_2024 = [("2024", "01/01/2024", "User", "Desc", "TCL", "ODC", "PDL", "08:00", "17:00", "9", "PREV", "File24")]

        DataSynchronizer.sync_giornaliere(db_path, data_2023 + data_2024, [2023, 2024])

        # Sincronizza solo 2024 con nuovi dati
        new_data_2024 = [
            ("2024", "02/01/2024", "User", "Nuova", "TCL", "ODC", "PDL", "08:00", "17:00", "9", "PREV", "File24")
        ]

        # Passiamo solo 2024 come anno da pulire/sincronizzare
        added, removed = DataSynchronizer.sync_giornaliere(db_path, new_data_2024, [2024])

        assert removed == 1 # La riga del 2024 originale
        assert added == 1   # La nuova riga del 2024

        # Verifica che il 2023 sia intatto
        with DatabaseManager().get_connection(db_path) as conn:
            count_23 = conn.execute("SELECT COUNT(*) FROM giornaliere WHERE year = 2023").fetchone()[0]
            assert count_23 == 1

    def test_sync_generic_scarico_ore(self, db_path):
        """Verifica la sincronizzazione totale della tabella scarico ore."""
        # 11 colonne + styles = 12 totali come da SCARICO_ORE_COLS
        initial_row = ("2024-01-01", "P1", "", "ODC1", "10", "08:00", "17:00", "9.0", "Desc", "S", "C1", "{}")
        DataSynchronizer.sync_scarico_ore(db_path, [initial_row])

        # Sostituzione totale
        new_rows = [
            ("2024-01-02", "P2", "", "ODC2", "20", "09:00", "18:00", "9.0", "Desc2", "S", "C2", "{}"),
            ("2024-01-03", "P3", "", "ODC3", "30", "10:00", "19:00", "9.0", "Desc3", "S", "C3", "{}")
        ]

        added, removed = DataSynchronizer.sync_scarico_ore(db_path, new_rows)

        assert added == 2
        assert removed == 1

        with DatabaseManager().get_connection(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM scarico_ore").fetchone()[0]
            assert count == 2

    def test_normalization_strip_logic(self, db_path):
        """Verifica che la sincronizzazione faccia lo strip dei valori per il confronto."""
        # Dato nel DB con spazi
        initial = [(2024, "  01/01/2024  ", "Gen", "P1", "100", "Att", "T", "O", "S", "T", "8", "1", "N", "P", "F")]
        DataSynchronizer.sync_contabilita_dati(db_path, initial, [2024])

        # Nuovo dato "pulito"
        clean = [(2024, "01/01/2024", "Gen", "P1", "100", "Att", "T", "O", "S", "T", "8", "1", "N", "P", "F")]

        # Se la normalizzazione funziona, non dovrebbe vedere differenze (added=0, removed=0)
        # Perché entrambi i dati vengono normalizzati a "01/01/2024" prima del confronto EXCEPT
        added, removed = DataSynchronizer.sync_contabilita_dati(db_path, clean, [2024])

        # Nota: il calcolo del diff usa temp_contabilita (normalizzata) vs contabilita (già nel DB)
        # Se il dato nel DB non era normalizzato all'inserimento, removed sarà 1.
        # Ma sync_contabilita_dati normalizza PRIMA dell'inserimento finale.
        assert added == 0
        assert removed == 0
