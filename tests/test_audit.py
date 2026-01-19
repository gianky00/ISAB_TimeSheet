#!/usr/bin/env python3
"""Test script per verificare AuditManager"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    print("1. Importazione AuditManager...")
    from src.core.audit_manager import AuditManager

    print("   [OK] Import OK")

    print("\n2. Creazione istanza...")
    am = AuditManager()
    print(f"   [OK] Instance created: {type(am)}")

    print("\n3. Verifica segnali...")
    print(f"   - Has log_added: {hasattr(am, 'log_added')}")
    print(f"   - Has logs_updated: {hasattr(am, 'logs_updated')}")

    print("\n4. Test log_action...")
    am.log_action("Test Action", "test", "entity_test")
    print("   [OK] log_action OK")

    print("\n5. Test get_logs...")
    logs = am.get_logs(limit=5)
    print(f"   [OK] Retrieved {len(logs)} logs")

    print("\n[SUCCESS] Tutti i test passati!")

except Exception as e:
    print(f"\n[ERROR] ERRORE: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
