# SyncroJob Enterprise - Developer Context

**SyncroJob Enterprise** is an advanced integrated software suite designed to automate, monitor, and optimize business workflows on the ISAB supplier portal and SafeWork. It features a modern PyQt6-based GUI and uses Selenium/automation bots to handle complex tasks like timesheet downloading, purchase order analysis, and personnel management.

## 📂 Project Structure

```
C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\
├── main.py                 # Application entry point
├── pyproject.toml          # Poetry configuration and dependencies
├── README.md               # General project documentation
├── generate_icons.py       # Utility to generate app icons
├── src/                    # Source code
│   ├── bots/               # Automation logic (Selenium/Web drivers)
│   │   ├── base/           # Base bot classes
│   │   ├── portale_fornitori/ # ISAB portal specific bots
│   │   └── safework/       # SafeWork portal bots
│   ├── core/               # Core business logic (DB, Config, Audit)
│   ├── gui/                # PyQt6 Graphical User Interface
│   └── utils/              # Helper functions
├── assets/                 # Icons, styles (QSS), images
├── admin/                  # Administrative scripts (Release, License, Cleanup)
├── tests/                  # Pytest test suite
└── docs/                   # Documentation and planning
```

## 🛠️ Tech Stack

* **Language:** Python 3.12+
* **GUI:** PyQt6
* **Automation:** Selenium, Requests
* **Data Processing:** Pandas, OpenPyXL, PyArrow
* **Database:** SQLite (managed via internal ORM/Helpers)
* **Build System:** Poetry / PyInstaller
* **Linting/Formatting:** Ruff, Black, Mypy

## 🚀 Getting Started

### Prerequisites

* Python 3.12 (recommended)
* Poetry (dependency manager)
* Google Chrome (latest version) for automation bots

### Installation

1. **Clone/Navigate to the repository:**

    ```bash
    cd C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet
    ```

2. **Install dependencies:**

    ```bash
    # Using Poetry (Recommended)
    poetry install

    # Or using pip
    pip install -r requirements.txt
    ```

### Running the Application

* **Start the GUI:**

    ```bash
    python main.py
    ```

    Or use the poetry script:

    ```bash
    poetry run syncrojob
    ```

## 🧪 Testing & Quality Assurance

* **Run Unit Tests:**

    ```bash
    pytest tests/
    ```

    *See `tests/TESTING_PLAN_2026.md` for the current testing strategy.*

* **Linting:**

    ```bash
    ruff check .
    ```

* **Type Checking:**

    ```bash
    mypy .
    ```

* **Formatting:**

    ```bash
    black .
    ```

## 📦 Building for Distribution

To create a standalone executable (EXE) and setup installer:

```bash
python "admin/Crea Setup/build_dist.py"
```

## 📐 Architecture & Patterns

### 1. Singleton Managers

Core services like `AuditManager` and `NotificationManager` use a strict Singleton pattern.

* **Usage:** ALWAYS access via `.instance()`, never instantiate directly.
* **Signals:** Signals are decoupled into a nested `MySignals` class to avoid QObject multi-inheritance issues.
  * Example: `AuditManager.instance().signals.log_added.connect(...)`

### 2. Bot Architecture

All bots reside in `src/bots/` and inherit from `BaseBot`.

* **Structure:** Logic is separated into `pages/` (Page Object Model) and `locators.py`.
* **State:** Bots use `BotStatus` enum (IDLE, RUNNING, ERROR, etc.).

### 3. GUI Lazy Loading

The `MainWindow` uses lazy loading for its panels to improve startup time. Panels are instantiated only when first accessed via the `NavigationController`.

## 📝 Conventions

* **Imports:** Absolute imports from `src` (e.g., `from src.core.constants import ...`).
* **GUI Styling:** Styles are separated in `assets/styles/*.qss`.
* **Logging:** Use the enterprise logging system in `src/core/logging/`. See section below.
* **Bots:** All bots should inherit from `src.bots.base.BaseBot` (or similar base classes) to ensure consistent error handling and logging.

## 📋 Enterprise Logging System

SyncroJob uses an AI-ready structured logging system in `src/core/logging/`.

### Quick Start

```python
from src.core.logging import get_logger, with_context, measure_time

logger = get_logger(__name__)

with with_context(bot_type="scarico_ts", cantiere="ISAB"):
    logger.info("Operation started", items=42)

@measure_time(threshold_ms=5000)  # Warning if > 5s
def slow_operation():
    pass
```

### Key Features

* **JSON Structured Logs**: AI-ready format in `logs/app.json`
* **Context Propagation**: trace_id, span_id automatic correlation
* **Performance Monitoring**: `@measure_time` decorator with baselines
* **PII Masking**: Automatic filtering of passwords, CF, emails
* **Audit Correlation**: `AuditManager.log_action()` returns audit_id

### Documentation

* **API Reference**: `src/core/logging/README.md`
* **Migration Guide**: `src/core/logging/MIGRATION_GUIDE.md`
* **Best Practices**: `src/core/logging/BEST_PRACTICES.md`

### CLI Tools

```bash
# Query logs
python tools/logs_cli.py query --level ERROR --bot scarico_ts

# Reconstruct trace timeline
python tools/logs_cli.py trace <trace_id>

# System health report
python tools/logs_cli.py health --hours 24
```
