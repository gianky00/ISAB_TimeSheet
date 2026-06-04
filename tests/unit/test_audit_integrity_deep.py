"""Deep tests for AuditIntegrity and chain verification."""

from src.application.services.audit.integrity import AuditIntegrity


class TestAuditIntegrityDeep:
    def test_hash_chain_consistency(self):
        """Verifica che la catena di hash sia deterministica e sequenziale."""
        data1 = "action1|category1"
        data2 = "action2|category2"

        initial_hash = "0" * 64

        hash1 = AuditIntegrity.calculate_hash(data1, initial_hash)
        hash2 = AuditIntegrity.calculate_hash(data2, hash1)

        assert hash1 != initial_hash
        assert hash2 != hash1

        # Rigenerazione deve dare stessi risultati
        assert AuditIntegrity.calculate_hash(data1, initial_hash) == hash1
        assert AuditIntegrity.calculate_hash(data2, hash1) == hash2

    def test_tamper_detection(self):
        """Verifica che una minima modifica rompa la catena."""
        data1 = "valore_originale"
        prev = "0" * 64

        original_hash = AuditIntegrity.calculate_hash(data1, prev)

        # Modifica un carattere
        tampered_data = "valore_originaLe"
        tampered_hash = AuditIntegrity.calculate_hash(tampered_data, prev)

        assert original_hash != tampered_hash

    def test_build_hash_strings(self):
        """Verifica la costruzione delle stringhe per V2 e Legacy."""
        row = {
            "timestamp": "2026-01-01",
            "user_id": "user",
            "action": "login",
            "category": "auth",
            "entity": "-",
            "params": "{}",
            "status": "success",
            "severity": "low",
            "duration_ms": 100,
            "module": "core",
            "error_code": "0",
        }

        s_v2 = AuditIntegrity.build_hash_string_v2(row)
        s_legacy = AuditIntegrity.build_hash_string_legacy(row)

        # V2 deve contenere duration_ms
        assert "100" in s_v2
        assert "core" in s_v2

        # Legacy non deve contenerli (in base alla firma in integrity.py)
        assert "100" not in s_legacy
        assert "core" not in s_legacy

        # Entrambi contengono i campi base
        assert "login" in s_v2 and "login" in s_legacy
        assert "auth" in s_v2 and "auth" in s_legacy
