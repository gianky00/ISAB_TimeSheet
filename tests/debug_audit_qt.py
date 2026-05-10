#!/usr/bin/env python3
"""Test AuditManager con PySide6"""

import sys
from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.core.audit_manager import AuditManager  # noqa: E402

print("1. Import PySide6...")
print("2. Create QApplication...")
app = QApplication(sys.argv)

print("3. Import AuditManager...")

print("4. Create AuditManager instance...")
am = AuditManager.instance()

print("5. Check signals...")
print(f"   - Type: {type(am)}")
print(f"   - Has signals: {hasattr(am, 'signals')}")
print(f"   - Signal object type: {type(am.signals)}")
print(f"   - Has log_added: {hasattr(am.signals, 'log_added')}")
print(f"   - Is QObject: {isinstance(am.signals, QObject)}")

print("6. Test log_action...")
am.log_action("Test", "category", "entity")

print("\n[SUCCESS] AuditManager funziona correttamente con PySide6!")
