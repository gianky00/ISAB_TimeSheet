# 🤝 Contributing to SyncroJob

Grazie per l'interesse a contribuire a **SyncroJob Enterprise**!
Questo documento delinea le linee guida per lo sviluppo, il testing e il rilascio.

## 🛠️ Setup Ambiente di Sviluppo

### Prerequisiti

- Python 3.12+
- [Poetry](https://python-poetry.org/) (Gestore dipendenze)
- Git

### Installazione

1. **Installazione dipendenze e venv**:
   ```bash
   poetry install
   ```
2. **Attivazione Virtual Environment**:
   ```bash
   poetry shell
   ```
   _(Oppure usa l'interprete `.venv/Scripts/python.exe` nel tuo IDE)_.

---

## 🧪 Testing Policy

Il progetto adotta una politica **Zero Regressions**.

### Eseguire i Test

- **Suite Completa (Robust Runner)**:
  ```bash
  python tests/run_robust_tests.py
  ```
- **Test Rapidi (solo unit)**:
  ```bash
  poetry run pytest -m "unit and not slow"
  ```
- **Test con coverage**:
  ```bash
  poetry run pytest --cov=src --cov-report=term-missing
  ```

### Regole per Nuove Feature

1. Ogni nuova funzionalità deve avere almeno un unit test in `tests/unit/`.
2. I test di integrazione vanno in `tests/integration/`.
3. Usa `Mock` e `Patch` per isolare dipendenze esterne (Network, DB, UI).
4. **Non eseguire mai** `pytest` globale senza il Robust Runner: potrebbe interferire con il QApplication singleton.

---

## 🎨 Code Style & Quality

Prima di un commit, **tutti** i seguenti controlli devono passare (già automatizzati nel pre-commit):

```bash
# Linting e formattazione
poetry run ruff check --fix
poetry run ruff format

# Type checking (strict)
poetry run mypy --strict src/

# Docstring coverage
poetry run interrogate src/

# Complessità ciclomatica
poetry run xenon src/ --max-absolute B --max-modules B --max-average A

# Coesione SRP (LCOM)
poetry run python scripts/check_cohesion.py

# Tutti in una volta
poetry run pre-commit run --all-files
```

---

## 🚀 Release Process

La versione è gestita automaticamente da **commitizen**. Non modificare mai `version.py` o `pyproject.toml` manualmente.

1. **Bump della versione** (calcola automaticamente major/minor/patch da commit convenzionali):
   ```bash
   poetry run cz bump
   ```
2. **Build distribuibile** (PyInstaller):
   ```bash
   python "admin/Crea Setup/build_dist.py"
   ```
3. L'installer viene generato nella cartella `dist/`.

---

## 🏛️ Architettura

Vedi [`.ai-context.json`](./.ai-context.json) per il contesto architetturale completo in formato machine-readable.

- **Core** (`src/core/`): Logica di business pura. ZERO dipendenze dalla GUI.
- **GUI** (`src/gui/`): Interfaccia PySide6. Dipende SOLO da Core. ZERO query SQL dirette.
- **Bots** (`src/bots/`): Automazione browser (Selenium/Playwright). Logica isolata.
- **Protocolli**: Vedi `src/core/interfaces.py` per i contratti formali `BotProtocol` e `DataImporterProtocol`.

---

## 🚨 Regole Anti-Breakage Critiche

1. **Signal Safety PySide6**: Non rimuovere mai le `lambda` dalle connessioni dei segnali.
2. **Settings Singleton**: Usa sempre `from src.core.config.settings import settings`. MAI istanziare `SyncroJobSettings` direttamente.
3. **Dialogs**: Usa `ConfirmationDialog` (non `QMessageBox`) e `StandardInputDialog` (non `QInputDialog`).
4. **Logging**: Solo `loguru`. Implementa `@logger.catch` sugli entry point critici.
