# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

SyncroJob is a Windows-focused desktop application (PyQt6) that automates operations on the ISAB supplier portal (timesheet download, order details, accounting KPIs, etc.).

The app is structured as a service-heavy core (DB, config, licensing, telemetry) plus a PyQt GUI layer and Selenium-based automation bots. Most business logic lives in `src/core` and is orchestrated by controllers in `src/gui/controllers`.

## Environment & Runtime

- Python: project targets Python 3.12 (see `pyproject.toml`).
- OS: primary target is Windows 10/11; many scripts are `.bat` and some functionality (printing, pywin32) is Windows-specific.
- Entry point: `main.py` (also exposed as `syncrojob = "main:main"` in `pyproject.toml`).
- Virtualenv convention: local venv at `.venv/` in the repo root.

### Local setup

From the repo root:

```bash path=null start=null
python -m venv .venv
# Windows
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> Note: dependencies are defined in both `pyproject.toml` (Poetry) and `requirements.txt`. Admin tooling (`admin/pre_flight_check.py`, `admin/sync_requirements.py`) assumes these stay in sync.

### Running the application from source (Windows)

Preferred flow (handles venv + deps automatically):

```bash path=null start=null
scripts\avvio.bat
```

Manual alternative (inside an activated venv):

```bash path=null start=null
python main.py
```

## Testing

### Mandatory test runner (local)

Do **not** call `pytest` directly for normal local runs. Use the robust runner, which isolates tests by file, manages timeouts, accumulates coverage, and writes a Markdown report.

Preferred entrypoint (Windows):

```bash path=null start=null
scripts\avvio_test.bat
```

Core engine (any platform, from repo root, inside venv):

```bash path=null start=null
python tests/run_robust_tests.py --reset
```

Key options for `tests/run_robust_tests.py`:

- `--reset` — start a fresh session and erase previous coverage data.
- positional `targets` — restrict to specific test paths or node IDs (e.g. `tests/unit/test_backup_manager_coverage.py`, or `tests/unit/test_backup_manager_coverage.py::test_happy_path`).
- `--filter PATH` — run only tests whose paths match the given prefix (e.g. `--filter tests/unit`).
- `--timeout SECONDS` — per-file timeout (default 60s).
- `--retry N` — retry failing tests in isolation (helps with flaky GUI/async tests).
- `--coverage-only` — just compute and display global coverage.
- `-x/--exitfirst` — stop at first failing test.

The runner:

- Discovers tests via `pytest --collect-only -q`.
- Executes per-file `pytest` runs with `--cov=src --cov-append`, falling back to per-test isolation when needed.
- Persists state in `tests/.test_session_state.json` to allow resuming long sessions.
- Generates coverage reports (terminal + HTML in `htmlcov/`) and a detailed Markdown report at `tests/test_report.md`.

### Running a single test or subset

Examples (from repo root, venv active):

```bash path=null start=null
# Single test file (fast path via robust runner)
python tests/run_robust_tests.py --reset tests/unit/test_backup_manager_coverage.py

# Single test function by node id
python tests/run_robust_tests.py --reset \
  tests/unit/test_backup_manager_coverage.py::test_backup_manager_handles_missing_db

# Only unit tests subtree
python tests/run_robust_tests.py --reset --filter tests/unit
```

### Coverage-focused run

For an explicit coverage sweep using the helper script (Windows):

```bash path=null start=null
scripts/run_coverage_plan.bat
```

This assumes `.venv` exists, refreshes test dependencies, then runs:

- `pytest --cov=src --cov-report=html --cov-report=term-missing tests/`

HTML coverage lives in `htmlcov/index.html`.

### CI behavior

GitHub Actions workflow `.github/workflows/ci.yml` currently runs:

- System deps for Qt on Ubuntu (`xvfb`, GL/X11 libs).
- `pip install -r requirements.txt`.
- `xvfb-run -a pytest -v` (output captured to `test_output.txt`).

On failures, a separate automation (`Jules`) can be triggered to analyze logs and open a fixing PR. Local work should still prefer `tests/run_robust_tests.py` for stability.

### Disabled / fragile tests

- `tests/unit/DISABLED_TESTS_README.md` documents tests that were explicitly disabled because they crash the Python process in certain headless environments (e.g. `HorizontalTimelineWidget` with `pytest-qt`).
- When reworking complex widgets, consult this doc and re-enable tests only after addressing the underlying GUI/headless issues.

## Linting, Formatting, Type Checking

Tooling is configured via `pyproject.toml`, `ruff.toml`, and `.pre-commit-config.yaml`.

### Ruff (lint + formatting)

Config: `ruff.toml` (`[lint]` + `[format]`).

Typical commands (run in venv from repo root):

```bash path=null start=null
# Lint
ruff check .

# Auto-fix + format
ruff check . --fix
ruff format .
```

The pre-commit config also runs `ruff` and `ruff-format` on changed files.

### Black

Black is configured in `pyproject.toml` (line length 110):

```bash path=null start=null
black .
```

### Mypy

Static typing configuration is under `[tool.mypy]` in `pyproject.toml`.

```bash path=null start=null
mypy src tests
```

The codebase expects proper type hints in new/modified code.

### Pre-commit

Pre-commit is configured in `.pre-commit-config.yaml` (whitespace, YAML checks, ruff, `poetry check`).

```bash path=null start=null
pre-commit install
pre-commit run --all-files
```

## Build & Release Tooling

Release/deployment is orchestrated via `admin/` scripts and `scripts/release.bat`.

### Pre-flight + release shortcut (Windows)

```bash path=null start=null
scripts\release.bat
```

This script:

- Runs `admin/pre_flight_check.py` using `.venv\Scripts\python.exe`.
  - Verifies consistency between `pyproject.toml` and `requirements.txt`.
  - Checks version alignment and other safety conditions before a release.
- Interactively asks for:
  - Bump type: `auto` (default), `patch`, `minor`, `major`.
  - Mode: local build only vs full release with Netlify deploy.
  - Whether to run tests before releasing.
- Delegates to `admin/release.py` with the chosen options.

### Direct release script usage

From repo root, in an activated venv:

```bash path=null start=null
python admin/pre_flight_check.py
python admin/release.py auto            # or patch|minor|major
python admin/release.py auto --deploy   # with Netlify deploy
python admin/release.py auto --skip-tests
```

`admin/release.py` implements the full pipeline described in `.gemini/ARCHITECT.md`: version bump, syncing requirements, running tests, building the installer, tagging, and notifications.

## High-level Architecture

The project follows a controller-heavy variant of MVC:

- **Core services** under `src/core/` implement business logic, persistence, and infrastructure.
- **GUI layer** under `src/gui/` implements the PyQt6 UI components and user workflows.
- **Automation bots** under `src/bots/` implement Selenium-based interactions with external ISAB/SafeWork portals.
- **Utility layer** under `src/utils/` provides cross-cutting helpers (documents, security, logging, parsing, printing).

### Core services (`src/core/`)

Key responsibilities (see `.gemini/ARCHITECT.md` and the modules under `src/core/`):

- **Database & synchronization**
  - `database.py`: central SQLite access layer (single logical DB manager, uses `PRAGMA user_version` for schema migrations).
  - `data_synchronizer.py`, `timesheet_processor.py`, `excel_importer.py`, `contabilita_*` modules: ETL and business rules for timesheets, accounting data, statistics, and exports.
  - `backup_manager.py`, `stats_manager.py`: backup/restore and statistics aggregation.
- **Configuration & secrets**
  - `config_manager.py`: JSON-based user and app configuration (paths, credentials, feature toggles, last-used filters, etc.).
  - `secrets_manager.py`: higher-level management for sensitive data (potentially leveraging `keyring`).
- **Licensing & security**
  - `license_validator.py`, `license_updater.py`: license verification and update workflows; coordinate with external license repository and local files.
  - `security.py`, `validators.py`, `secure_logger.py`, `log_humanizer.py`: security checks, validation utilities, log hardening and human-readable log representation.
  - `audit_manager.py`: central audit trail recording significant operations into the DB/logs.
- **Time, scheduling, and services**
  - `time_manager.py`: shared time utilities and scheduling helpers.
  - `telegram_manager.py`, `telegram_bridge.py`: bidirectional integration with a Telegram bot (notifications, remote commands).
  - `lyra_client.py`, `lyra_sentinel.py`: "Lyra" anomaly detection / monitoring service, running in the background.
  - `notification_manager.py`: in-process hub that broadcasts events and status updates to the GUI (panels, widgets) and services.
- **App lifecycle**
  - `app_initializer.py`: orchestrates startup, including config, DB migrations, license validation, and service wiring.
  - `app_updater.py`, `version.py`: application version management and auto-update logic.

Pattern-wise, core modules are designed to be independent of the GUI; controllers and widgets should consume them via clean APIs.

### GUI layer (`src/gui/`)

The GUI is built fully on PyQt6 and is organized by domain panels, reusable widgets, and controllers.

- **Main window & panels**
  - `main_window.py`: application shell; wires sidebars, panel stack, and high-level actions.
  - `panels.py`: orchestration of feature panels (timesheet, accounting, dashboards, settings, notifications, help, etc.).
  - `dashboard_panel.py`, `scarico_ore_panel.py`, `contabilita_panel.py`, `contabilita_kpi_panel.py`, `lyra_panel.py`, `notifications_panel.py`, `help_panel.py`, `settings_panel.py`: individual feature panels bound to specific core services.
- **Controllers (`src/gui/controllers/`)**
  - `navigation_controller.py`: page routing and lazy loading of panels.
  - `bot_controller.py`: coordinates the Selenium bots in `src/bots/` with user actions and core services.
  - `service_controller.py`: lifecycle management for background services (Lyra sentinel, Telegram manager, etc.).
  - `search_controller.py`: higher-level search flows (e.g. querying accounting/DB via `contabilita_*`).
  - `tray_controller.py`: system tray integration and background-mode UX.
- **Design system & layouts**
  - `design/colors.py`, `design/spacing.py`, `design/typography.py`: Material 3-inspired design tokens (see `.gemini/DESIGN.md` for palettes and component guidelines).
  - `styles.py` and `assets/styles/*.qss`: global and window-level style sheets.
  - `layouts/responsive.py`: responsive layout helpers to adapt panels to window size.
- **Widgets (`src/gui/widgets/`)**
  - Higher-level composite widgets: `automazioni_widget.py`, `bot_parameters.py`, `database_widget.py`, `excel_table.py`, `data_table.py`, `timeline_widget.py`, `status_card.py`, `update_banner.py`, etc.
  - Navigation/status components: `sidebar_widget.py`, `sidebar_button.py`, `notification_item.py`.
  - Feedback components: `toast.py`, `status_indicator.py`, and log widgets.

General GUI conventions (from `.gemini/ARCHITECT.md` + existing code/tests):

- All UI must use PyQt6; styling is centralized via QSS and the design system.
- Expensive work must not block the GUI thread; use `QThread`, `QProcess`, or background services via controllers.
- Tests that instantiate widgets must be careful to tear down widgets and reuse the `qapp` fixture correctly to avoid GDI/resource leaks, especially on Windows.

### Automation bots (`src/bots/`)

The automation layer encapsulates browser-based workflows for ISAB-related portals.

- `base/` contains shared primitives:
  - `base_bot.py`: core state machine and boilerplate around Selenium drivers, configuration, logging, retries.
  - `login_page.py`: common login flow abstractions.
- `safework/` holds SafeWork-specific automation primitives (`base.py`, and additional bots/pages as the project evolves).

Bots do not talk directly to the GUI; they are orchestrated by `BotController` and use core services (`config_manager`, `database`, `audit_manager`, etc.) for persistence and logging.

### Utilities (`src/utils/`)

Utilities provide shared helpers and pure logic where possible:

- `document_generator.py`, `document_processor.py`: generate and process reports/exports (spreadsheets, PDFs, etc.).
- `log_humanizer.py`, `helpers.py`, `parsing.py`, `validators.py`: string and data munging, validation, and log presentation.
- `printing.py`: OS-specific printing (notably Windows via `pywin32`).
- `resource_manager.py`: access to packaged assets (icons, styles, templates).
- `security.py`: additional security hardening helpers.

New cross-cutting functionality should typically be placed here, then wired into core/GUI as needed.

### Admin & tooling (`admin/`)

`admin/` hosts scripts that are not part of the end-user app but support development and operations:

- `pre_flight_check.py`: guards the release process (dependency and version consistency checks).
- `release.py`: full release pipeline (bump, sync, test, build, tag, deploy, notify).
- `bump_version.py`: low-level version bumping, used by release tooling.
- `sync_requirements.py`: syncs Poetry/`pyproject.toml` with `requirements.txt`.
- `manage_secrets_gui.py`: GUI for managing encrypted/separate secrets.
- `Crea Licenze/`: tooling for license generation (GUI under `admin_license_gui.py`).
- `Crea Setup/`: build scripts for the installer (e.g. `build_dist.py`, Inno Setup script `setup_script.iss`).
- `log_inspector/` and `universal_inspector.py`: debug tooling for log and HTML snapshots generated by bots.

### Tests (`tests/`)

The test suite is large and structured by concern:

- Root tests (`tests/test_basic.py`, `tests/test_import.py`, etc.) provide smoke coverage on imports and critical flows.
- `tests/unit/`: exhaustive unit and component tests for virtually every manager, controller, and widget. Many files are suffixed with `*_coverage.py`, `*_deep.py`, `*_refactoring.py`, etc., reflecting focused campaigns.
- `tests/integration/`: integration tests that touch real DB/config/FS (e.g. security and configuration integration).
- `tests/security/`: security-specific tests (e.g. filename sanitization).
- `tests/benchmark_*.py`: performance/benchmark scripts.

Important docs:

- `tests/TESTING_SUMMARY_2026.md`: describes recent coverage gains and areas still lacking tests.
- `.gemini/TESTING_INSIGHTS.md`: details the rationale and rules for the robust test runner and records historical crash points.

When adding or modifying tests, align with the existing structure and prefer extending focused coverage files rather than creating ad-hoc new patterns.
