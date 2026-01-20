# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SyncroJob Enterprise** is an automation platform for the ISAB supplier portal and SafeWork, built with PyQt6 and Selenium. It automates timesheet downloads/uploads, OdA management, attendance tracking, and safety portal integration.

## Development Commands

### Running the Application
```bash
# Standard launch (from repository root)
python main.py

# Launch with batch script (Windows)
scripts\avvio.bat
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_audit_manager_coverage.py

# Run with verbose output
pytest -v tests/
```

### Code Quality
```bash
# Linting
ruff check .

# Type checking
mypy .

# Format code
ruff format .
```

### Building
```bash
# Create installer/executable
python "admin/Crea Setup/build_dist.py"
```

## Architecture

### Application Structure

**Entry Point**: `main.py` → Initializes PyQt6 QApplication and MainWindow

**Core Components**:
- **MainWindow** (`src/gui/main_window.py`): Central hub coordinating controllers and navigation
  - Uses `PageIndex` enum (0-10) for panel routing
  - Implements **lazy loading** - panels created on first navigation
  - Startup sequence with animated console and progress tracking

- **NavigationController** (`src/gui/controllers/navigation_controller.py`): Handles routing between 11 main panels
  - Factory pattern for panel creation (`_create_*` methods)
  - Tracks initialization state per panel (`_panel_initialized_{index}`)

- **Controllers** (`src/gui/controllers/`):
  - `BotController`: Manages automation bot lifecycle
  - `ServiceController`: Background services (Telegram, Lyra Sentinel)
  - `TrayController`: System tray integration
  - `SearchController`: Universal search across modules

### Bot Architecture

All automation bots inherit from `BaseBot` (`src/bots/base/base_bot.py`):
- **Selenium-based** with Chrome WebDriver
- **State machine pattern** using `BotStatus` enum
- **LoginPage** abstraction for portal authentication
- **Locators pattern**: CSS/XPath selectors in separate `locators.py` files
- **Page Object Model**: Each bot has `pages/` directory with page classes

Bot structure:
```
src/bots/
├── base/
│   ├── base_bot.py        # Abstract base class
│   └── login_page.py      # Login automation
├── portale_fornitori/     # ISAB portal bots
│   ├── scarico_ts/        # Timesheet download
│   ├── dettagli_oda/      # Order details extraction
│   ├── timbrature/        # Attendance tracking
│   └── carico_ts/         # Timesheet upload
└── safework/              # Safety portal bot
```

### Manager Pattern (Singleton)

Critical managers use singleton pattern:

**AuditManager** (`src/core/audit_manager.py`):
- **IMPORTANT**: Access via `AuditManager.instance()` NOT `AuditManager()`
- Immutable audit trail with SHA-256 hash chaining
- SQLite-based (`CONFIG_DIR/data/audit_log.db`)
- **Signals**: Separated into `AuditSignals` class (PyQt6 compatibility)
  - Connect to events: `AuditManager.instance().signals.log_added.connect(callback)`
  - Emits: `log_added`, `logs_updated`

**NotificationManager** (`src/core/notification_manager.py`):
- JSON-based notification storage
- Signals: `notification_added`, `notifications_updated`, `unread_count_changed`

**Configuration** (`src/core/config_manager.py`):
- Central config at `CONFIG_DIR/config.json` (typically `%APPDATA%/SyncroJob`)
- Use `get_config_value()` and `set_config_value()` functions

### UI Widget System

**Widget Hierarchy**:
- **Dashboard** (`src/gui/dashboard_panel.py`):
  - `ActivityFeed`: Real-time audit log (event-driven via `AuditSignals`)
  - `QuickActions`: Configurable action shortcuts
  - `AutopilotWidget`: Scheduled bot execution display

- **Toast System** (`src/gui/widgets/toast.py`):
  - Singleton `ToastManager.instance().show(message, type, duration, pulse=False)`
  - Types: `info`, `success`, `warning`, `error`
  - Position: `"top"` or `"bottom"`

- **Animations**:
  - Use `QPropertyAnimation` and `QVariantAnimation` (NOT `QGraphicsScaleEffect`)
  - Example: `toast.py` pulse animation with scale factor

### Data Storage

- **SQLite**: Audit logs, attendance records, timesheet data
- **JSON**: Configuration, notifications
- **Excel**: Import/export via `openpyxl` and `pandas`
- **Profile Data**: Chrome profile in `data/chrome_profile/`

## Important Patterns & Conventions

### PyQt6 Singleton with Signals

**DO NOT** inherit QObject when using `__new__` singleton pattern. Instead:

```python
# CORRECT - Separate signal class
class MySignals:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            from PyQt6.QtCore import QObject, pyqtSignal

            class _Signals(QObject):
                my_signal = pyqtSignal(dict)

            cls._instance = _Signals()
        return cls._instance

class MyManager:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.signals = MySignals.instance()
```

### Lazy Loading Navigation

When adding new panels:
1. Add to `PageIndex` enum in `main_window.py`
2. Create placeholder in `main_window._setup_ui()` loop
3. Add factory method in `navigation_controller.py` (`_create_*`)
4. Register in `creators` dict with PageIndex value

### Cache Management

After modifying core managers or singleton classes:
```bash
# Clean Python cache to avoid stale imports
find src -name "*.pyc" -delete
find src -type d -name "__pycache__" -exec rm -rf {} +
```

### Bot State Management

Bots track state via `_status` property:
- `IDLE`: Ready to run
- `INITIALIZING`: Setting up driver
- `LOGGING_IN`: Authentication in progress
- `RUNNING`: Main operation executing
- `COMPLETED`: Successful finish
- `ERROR`: Fatal error occurred
- `STOPPED`: User-requested stop

Use `_stop_requested` flag for graceful termination during long operations.

### Localization

UI is Italian language. Key terms:
- "Timbrature" = Attendance/clock-ins
- "OdA" = Ordini di Acquisto (Purchase Orders)
- "PDL" = Piano di Lavoro (Work Plan)
- "Strumentale" = Equipment/Assets
- "Scarico" = Download
- "Carico" = Upload

## Critical Files

- `src/core/version.py`: Version number for releases
- `src/core/constants.py`: Enums, URLs, timeouts, browser config
- `src/core/license_validator.py`: Hardware-bound license validation
- `assets/styles/`: QSS stylesheets for UI theming
- `data/config/`: User configuration and databases (not in git)

## Testing Notes

- Use pytest fixtures in `conftest.py`
- Mock Selenium WebDriver for bot tests
- Mock PyQt6 QApplication when testing UI components
- Test files mirror `src/` structure in `tests/`

## Common Pitfalls

1. **Never call `AuditManager()` directly** - always use `.instance()`
2. **Clear Python cache** after modifying singleton managers
3. **Lazy loading**: Don't assume panels exist - use `navigation_controller.get_panel()`
4. **Signals from managers**: Access via `.signals` attribute (e.g., `manager.signals.my_signal`)
5. **Bot credentials**: Load from config, never hardcode
6. **Download paths**: Always use `Path` objects and ensure parent dirs exist
7. **WebDriver waits**: Use `WebDriverWait` with explicit conditions, not `time.sleep()`
