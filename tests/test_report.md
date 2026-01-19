# 📊 Test Execution Report

**Date:** 2026-01-19 19:48:33
**Duration:** 907.53s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1030 |
| ✅ Passed | 299 |
| ❌ Failed | 1 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_dashboard_full.py::TestDashboardComponents::test_quick_actions_signals`
**Error:** `E   ImportError: cannot import name 'QGraphicsRotationEffect' from 'PyQt6.QtWidgets' (C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\PyQt6\QtWidgets.pyd)`

<details><summary>Full Output</summary>

```text

=================================== ERRORS ====================================
_____________ ERROR collecting tests/unit/test_dashboard_full.py ______________
ImportError while importing test module 'C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_dashboard_full.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Program Files\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests\unit\test_dashboard_full.py:5: in <module>
    from src.gui.dashboard_panel import DashboardPanel
src\gui\dashboard_panel.py:19: in <module>
    from src.gui.widgets.autopilot_widget import AutopilotWidget
src\gui\widgets\autopilot_widget.py:17: in <module>
    from PyQt6.QtWidgets import (
E   ImportError: cannot import name 'QGraphicsRotationEffect' from 'PyQt6.QtWidgets' (C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\PyQt6\QtWidgets.pyd)
=========================== short test summary info ===========================
ERROR tests/unit/test_dashboard_full.py
1 error in 1.48s
ERROR: found no collectors for C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_dashboard_full.py::TestDashboardComponents::test_quick_actions_signals


```
</details>

---
