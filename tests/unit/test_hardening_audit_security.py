import sqlite3
import time
from datetime import datetime
from unittest.mock import patch

import pytest

from src.core.audit.integrity import AuditIntegrity
from src.core.audit_manager import AuditManager
from src.core.database import DatabaseManager, db_manager
from src.utils.security import PasswordManager


class TestHardeningAuditSecurity:
    @pytest.fixture
    def audit_env(self, tmp_path, mocker):
        """Setup isolato per AuditManager modular V2."""
        db_path = tmp_path / "audit_hardening.db"
        # Patch the real location in AuditDatabase
        mocker.patch("src.core.audit.database.AuditDatabase.DB_PATH", db_path)
        # Patch signals
        mocker.patch("src.core.audit.manager.AuditSignals.instance")

        with patch("src.core.audit.manager.AuditManager._instance", None):
            manager = AuditManager()
            yield manager, db_path

    @pytest.fixture
    def db_env(self, tmp_path, mocker):
        """Setup isolato per DatabaseManager e FTS5."""
        # Patch CONFIG_DIR per altri usi
        mocker.patch("src.core.database.manager.CONFIG_DIR", tmp_path)

        # Patch i percorsi DB direttamente nella classe per sovrascrivere i valori statici
        data_dir = tmp_path / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        db_cont = data_dir / "contabilita.db"
        db_timb = data_dir / "timbrature.db"

        mocker.patch.object(DatabaseManager, "DB_CONTABILITA", db_cont)
        mocker.patch.object(DatabaseManager, "DB_TIMBRATURE", db_timb)

        # Inizializziamo i DB
        db_manager.init_db()
        return db_manager, db_cont

    # --- AUDIT HARDENING TESTS ---

    def test_audit_deletion_integrity_break(self, audit_env):
        """Test: La cancellazione di una riga intermedia deve rompere la catena."""
        manager, db_path = audit_env

        # Inseriamo 3 righe
        manager.log_action("Action 1")
        manager.log_action("Action 2")
        manager.log_action("Action 3")
        manager._log_queue.join()  # Attendi scrittura asincrona

        assert manager.verify_integrity() is True

        # Cancelliamo la riga 2
        with sqlite3.connect(db_path) as conn:
            conn.execute("DELETE FROM audit_logs WHERE id = 2")
            conn.commit()

        # L'integrità deve fallire perché l'hash della riga 3 si aspetta l'hash della 2 come prev_hash
        assert manager.verify_integrity() is False

    def test_audit_insertion_integrity_break(self, audit_env):
        """Test: L'inserimento di una riga valida (ma non sequenziale) rompe la catena."""
        manager, db_path = audit_env

        manager.log_action("First")
        manager.log_action("Third")  # Questa sarà ID 2
        manager._log_queue.join()

        with sqlite3.connect(db_path) as conn:
            # Recuperiamo l'ultimo hash per iniettare una riga "valida" a metà
            cursor = conn.cursor()
            cursor.execute("SELECT row_hash FROM audit_logs WHERE id = 1")
            h1 = cursor.fetchone()[0]

            # Calcoliamo un hash "valido" (V2) per una riga fake
            ts = datetime.now().isoformat()
            fake_data = f"{ts}|attacker|Exploit|general|-|{{}}|success|high|0||"
            fake_hash = AuditIntegrity.calculate_hash(fake_data, h1)

            conn.execute(
                """
                INSERT INTO audit_logs
                (timestamp, user_id, action, category, entity, params, status, severity,
                 duration_ms, module, error_code, row_hash)
                VALUES (?, 'attacker', 'Exploit', 'general', '-', '{}', 'success', 'high', 0, '', '', ?)
                """,
                (ts, fake_hash),
            )
            conn.commit()

        # L'integrità deve fallire perché la riga "Third" (che ora è dopo la riga fake)
        # ha un row_hash calcolato sul prev_hash della riga 1, non della riga fake.
        assert manager.verify_integrity() is False

    def test_audit_performance_stress(self, audit_env):
        """Test: Performance e stabilità con 500 inserimenti rapidi."""
        manager, _ = audit_env

        start_time = time.time()
        for i in range(500):
            manager.log_action(f"Performance Test {i}", category="stress")
        manager._log_queue.join()
        duration = time.time() - start_time

        # Media accettabile per test
        assert duration < 25.0
        assert manager.verify_integrity() is True

    # --- SECURITY MIGRATION TESTS ---

    def test_password_migration_v1_to_v2(self, tmp_path, mocker):
        """Test: Migrazione fluida dal formato ENC: al formato ENC:v2:."""
        sec_dir = tmp_path / "security"
        sec_dir.mkdir(parents=True, exist_ok=True)
        mocker.patch("src.utils.security.PasswordManager._KEY_DIR", sec_dir)
        mocker.patch("src.utils.security.PasswordManager._KEY_FILE", sec_dir / "secret.key")

        with patch("src.utils.security.PasswordManager._instance", None):
            pm = PasswordManager()
            plaintext = "LegacySecret123"

            # Simuliamo un dato salvato con il vecchio prefisso (ma usando il cipher attuale)
            raw_encrypted = pm._cipher.encrypt(plaintext.encode()).decode()
            legacy_ciphertext = f"ENC:{raw_encrypted}"

            # Verifica decriptazione legacy
            decrypted = pm.decrypt(legacy_ciphertext)
            assert decrypted == plaintext

            # Verifica che la nuova criptazione usi v2
            new_encrypted = pm.encrypt(plaintext)
            assert new_encrypted.startswith("ENC:v2:")

    def test_security_corrupted_key_regeneration(self, tmp_path, mocker):
        """Test: Se il file della chiave è corrotto, deve rigenerarlo (self-healing)."""
        sec_dir = tmp_path / "security"
        sec_dir.mkdir(parents=True, exist_ok=True)
        key_file = sec_dir / "secret.key"

        # Scriviamo spazzatura nel file chiave
        key_file.write_text("NOT_A_FERNET_KEY")

        mocker.patch("src.utils.security.PasswordManager._KEY_DIR", sec_dir)
        mocker.patch("src.utils.security.PasswordManager._KEY_FILE", key_file)

        with patch("src.utils.security.PasswordManager._instance", None):
            pm = PasswordManager()
            # Deve aver rigenerato una chiave valida
            assert pm._key != b"NOT_A_FERNET_KEY"
            test_data = "HealingTest"
            assert pm.decrypt(pm.encrypt(test_data)) == test_data

    # --- DATABASE FTS5 INTEGRITY TESTS ---

    def test_fts5_sync_on_update_delete(self, db_env):
        """Test: L'indice FTS5 deve restare sincronizzato dopo UPDATE e DELETE."""
        mgr, db_path = db_env

        # 1. Insert
        mgr.execute_query(
            db_path,
            """
            INSERT INTO contabilita (year, n_prev, attivita, odc)
            VALUES (2026, 'P123', 'Manutenzione Valvole', 'ODC_99')
        """,
        )

        # Verifica FTS
        res = mgr.execute_query(
            db_path,
            "SELECT * FROM contabilita_fts WHERE contabilita_fts MATCH 'Valvole'",
        )
        assert len(res) == 1

        # 2. Update
        mgr.execute_query(
            db_path,
            "UPDATE contabilita SET attivita = 'Revisione Pompe' WHERE n_prev = 'P123'",
        )

        res_old = mgr.execute_query(
            db_path,
            "SELECT * FROM contabilita_fts WHERE contabilita_fts MATCH 'Valvole'",
        )
        res_new = mgr.execute_query(
            db_path, "SELECT * FROM contabilita_fts WHERE contabilita_fts MATCH 'Pompe'"
        )
        assert len(res_old) == 0
        assert len(res_new) == 1

        # 3. Delete
        mgr.execute_query(db_path, "DELETE FROM contabilita WHERE n_prev = 'P123'")
        res_del = mgr.execute_query(
            db_path, "SELECT * FROM contabilita_fts WHERE contabilita_fts MATCH 'Pompe'"
        )
        assert len(res_del) == 0
