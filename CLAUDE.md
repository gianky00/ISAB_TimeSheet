# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Nota**: Per il contesto architetturale completo in formato machine-readable, vedi [`.ai-context.json`](./docs/resources/.ai-context.json).

## Project Overview

**SyncroJob Enterprise** is an automation platform for the ISAB supplier portal and SafeWork, built with PySide6 and Selenium/Playwright. It automates timesheet downloads/uploads, OdA management, attendance tracking, and safety portal integration.

## Development Commands

### Setup

```bash
# Installazione dipendenze e venv
uv sync

# Attivazione venv
uv venv
```

### Testing

```bash
# Suite completa e unica via per i test
python -m tests.run_robust_test

# Esempio per test mirati (il robust runner supporta i marker di pytest)
python -m tests.run_robust_test -m "unit and not slow"

# Per un singolo file
python -m tests.run_robust_test tests/unit/test_audit_manager_coverage.py
```

### Code Quality (tutti automatizzati nel pre-commit)

```bash
# Linting + autofix
uv run ruff check --fix

# Formattazione
uv run ruff format

# Type checking strict
uv run mypy --strict src/

# Docstring coverage >= 99%
uv run interrogate src/

# Complessità ciclomatica (max B)
uv run xenon src/ --max-absolute B --max-modules B --max-average A

# Coesione SRP / LCOM (script con filtri anti-falsi positivi)
uv run python devtools/maintenance/check_cohesion.py

# Tutto in una volta
uv run pre-commit run --all-files
```

### Building

```bash
# Build standard (PyInstaller)
python "devtools/gui/Crea Setup/build_dist.py"


```

### Versioning

```bash
# MAI modificare manualmente version.py o pyproject.toml
# Usa commitizen:
uv run cz bump
```

### Generatori AI

```bash
# Aggiorna .ai-context.json (eseguito automaticamente dal pre-commit)
uv run python devtools/cli/generate_ai_context.py

# Aggiorna docs/schemas/config.schema.json
uv run python devtools/cli/generate_schemas.py
```

## Architecture

### Layered Layout

```
src/
├── domain/         # Business logic pura, Modelli Pydantic — NESSUNA dipendenza esterna
├── application/    # Services e Orchestration — Coordina domain e infrastructure
│   └── services/   # Implementazioni concrete dei servizi core
├── infrastructure/ # Implementazioni tecniche (Bot, DB, Utils, Network)
│   ├── bots/       # Automazione Selenium/Playwright
│   ├── database/   # Persistenza dati
│   └── utils/      # Utility di sistema e helper
├── gui/            # Widget, Panel, Dialog PySide6 — NESSUNA logica di business
└── api/            # Interfacce verso l'esterno (Telegram Bridge)
```

### Entry Point

`main.py` → Inizializza PySide6 QApplication, MainWindow e Crash Handler

### Settings Singleton (AI-First)

```python
# CORRETTO — usa sempre il Singleton pre-caricato
from src.application.services.config.settings import settings
value = settings.browser_headless

# SBAGLIATO — non istanziare direttamente
s = SyncroJobSettings()  # NO!
```

### Formal Contracts (typing.Protocol)

```python
# src/application/services/interfaces.py
class BotProtocol(Protocol):
    def run(self, *args, **kwargs) -> bool: ...
    def force_stop(self) -> None: ...
    def cleanup(self) -> None: ...

class DataImporterProtocol(Protocol):
    def import_file(self, file_path: str, *args, **kwargs) -> Any: ...
```

### MainWindow Navigation

- `PageIndex` enum (0-10) per panel routing
- Lazy loading — panels creati al primo navigate
- Pattern: `navigation_controller.get_panel(PageIndex.X)`

### Bot Architecture

Tutti i bot ereditano da `BaseBot` o `SeleniumBaseBot` / `PlaywrightBaseBot`:

```
src/infrastructure/bots/
├── base/
│   ├── base_bot.py              # Classe astratta base + macchina a stati
│   ├── selenium_base_bot.py     # Specializzazione Selenium
│   ├── playwright_base_bot.py   # Specializzazione Playwright
│   └── login_page.py            # Automazione login portali
├── portale_fornitori/
│   ├── scarico_ts/              # Download timesheet
│   ├── carico_ts/               # Upload timesheet
│   ├── dettagli_oda/            # Estrazione OdA
│   ├── prenota_bp/              # Prenotazione BP
│   └── timbrature/              # Timbrature dipendenti
└── safework/
    ├── pdl/                     # Ricerca Piano di Lavoro
    ├── programmazione/          # Programmazione
    └── programmazione_sync/     # Sincronizzazione programmazione
```

**BotStatus** (macchina a stati): `IDLE → INITIALIZING → LOGGING_IN → RUNNING → COMPLETED | ERROR | STOPPED`

### UI Widget System

```python
# SEMPRE questi — mai i widget Qt nativi
from src.gui.widgets.modern_button import ModernButton         # non QPushButton
from src.gui.widgets.core_widgets import ConfirmationDialog    # non QMessageBox
from src.gui.widgets.core_widgets import StandardInputDialog   # non QInputDialog
from src.gui.styles.theme_manager import ThemeManager          # palette HSL
from src.gui.toast import ToastNotification                    # notifiche
```

### Manager Singleton Pattern

**AuditManager**: `AuditManager.instance()` (**non** `AuditManager()`)
- Audit immutabile con SHA-256 hash chaining
- Segnali: `AuditManager.instance().signals.log_added.connect(callback)`

**NotificationManager**: `NotificationManager.instance()`
- Segnali: `notification_added`, `notifications_updated`, `unread_count_changed`

## Critical Rules

### PySide6 Signal Safety

**Non rimuovere MAI le lambda dalle connessioni dei segnali** (FURB111 è un falso-allarme qui — ignorare):

```python
# CORRETTO — la lambda preserva la firma del segnale Qt
self.btn.clicked.connect(lambda: self._on_clicked())

# SBAGLIATO — rompe Qt a runtime se le firme differiscono
self.btn.clicked.connect(self._on_clicked)  # NO!
```

### Logging

```python
# SEMPRE loguru, mai logging stdlib
from loguru import logger

@logger.catch  # su tutti gli entry point critici
def critical_operation() -> None: ...
```

### SRP — Zero SQL in GUI

```python
# SBAGLIATO — logica di business nella GUI
class MyPanel(QWidget):
    def _load_data(self):
        conn = sqlite3.connect(...)  # NO!

# CORRETTO — delega al Service/Repository
class MyPanel(QWidget):
    def _load_data(self):
        data = self._service.get_data()  # OK
```

### Exception Hierarchy

```
SyncroJobError (src/application/services/exceptions.py)
├── StartupError
├── LicenseError
├── DatabaseError
├── ConfigError
├── ValidationError
└── BotError
    ├── BrowserInitError
    └── AutomationError
```

## Database Layout

| File | Scopo |
|------|-------|
| `contabilita.db` | Strumentali e certificati campione |
| `timbrature_Isab.db` | Timbrature giornaliere dipendenti |
| `pdl.db` | Piano di Lavoro (SafeWork) |
| `storico_oda.db` | Ordini di Acquisto (portale ISAB) |
| `anagrafica_dipendenti.db` | Anagrafica dipendenti e matricole |
| `scarico_ore.db` | Ore scaricate da DataEase (ERP) |
| `audit_log.db` | Registro audit immutabile (SHA-256) |

Tutti i DB risiedono in `%APPDATA%/SyncroJob/data/` (determinato da `src/application/services/paths.py`).

## Localization

UI in italiano. Termini chiave:
- **Timbrature** = Attendance/clock-ins
- **OdA** = Ordini di Acquisto (Purchase Orders)
- **PDL** = Piano di Lavoro (Work Plan)
- **Strumentale** = Equipment/Assets
- **Scarico** = Download / Export
- **Carico** = Upload / Import

## Testing Notes

- Fixtures pytest in `conftest.py`
- **Mai** `pytest` globale senza il Robust Runner: QApplication è singleton e causa conflitti
- Mock Selenium/Playwright WebDriver nei bot test
- Mock PySide6 QApplication nei test UI
- Test mirror `src/` structure in `tests/`
- Marker disponibili: `unit`, `gui`, `integration`, `slow`

## Common Pitfalls

1. **AuditManager**: usa sempre `.instance()`, mai il costruttore diretto
2. **Cache Python**: dopo aver modificato singleton, pulire `__pycache__` con `find src -name "*.pyc" -delete`
3. **Lazy loading panels**: non assumere che il panel esista — usa `navigation_controller.get_panel()`
4. **Bot credentials**: caricare sempre dalla config, mai hardcode
5. **Download paths**: sempre `Path` objects con `mkdir(parents=True, exist_ok=True)`
6. **WebDriver waits**: sempre `WebDriverWait` con condizioni esplicite, mai `time.sleep()`
7. **Versioning**: usa `cz bump`, non modificare `version.py` manualmente

## Security Notes

**Vulnerabilità note e standard obbligatori:**

- **GitHub PAT**: token in `license_updater.py` ricostruito da lista statica — non esporre, migrare a backend intermediario.
- **Grace Period**: `GRACE_PERIOD_KEY` non deve essere hardcoded — validazione lato server.
- **SQL Injection**: usare SEMPRE query parametrizzate (`cursor.execute("... WHERE id=?", (val,))`), mai f-string.
- **Credenziali**: MAI in chiaro. Usare `SecretsManager` con keyring di sistema.
- **RichText**: evitare `setTextFormat(Qt.RichText)` su input utente non filtrato (UI Injection).
- **File Integrity**: validare checksum dei file scaricati dai bot prima del processamento.
