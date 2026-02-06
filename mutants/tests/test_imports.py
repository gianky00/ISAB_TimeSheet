#!/usr/bin/env python3
"""Test imports dei moduli modificati"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("Test import moduli modificati...")
print("-" * 50)

try:
    print("1. PyQt6.QtCore...")
    print("   OK")
except Exception as e:
    print(f"   ERRORE: {e}")
    sys.exit(1)

try:
    print("2. AuditManager...")
    print("   OK")
except Exception as e:
    print(f"   ERRORE: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

try:
    print("3. ActivityFeed...")
    print("   OK")
except Exception as e:
    print(f"   ERRORE: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

try:
    print("4. Toast...")
    print("   OK")
except Exception as e:
    print(f"   ERRORE: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

try:
    print("5. AutopilotWidget...")
    print("   OK")
except Exception as e:
    print(f"   ERRORE: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

try:
    print("6. DashboardPanel...")
    print("   OK")
except Exception as e:
    print(f"   ERRORE: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("-" * 50)
print("Tutti gli import completati con successo!")
