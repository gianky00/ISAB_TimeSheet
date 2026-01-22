# 🤝 Contributing to SyncroJob

Grazie per l'interesse a contribuire a **SyncroJob Enterprise**!
Questo documento delinea le linee guida per lo sviluppo, il testing e il rilascio.

## 🛠️ Setup Ambiente di Sviluppo

### Prerequisiti

- Python 3.12+
- [Poetry](https://python-poetry.org/) (Gestore dipendenze)
- Git

### Installazione

1.  **Clone del repository**:
    ```bash
    git clone https://github.com/gianky00/bot-ts.git
    cd bot-ts
    ```
2.  **Installazione dipendenze e venv**:
    ```bash
    poetry install
    ```
3.  **Attivazione Virtual Environment**:
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
- **Test Rapidi (Pytest)**:
  ```bash
  pytest tests/unit
  ```

### Regole per Nuove Feature

1.  Ogni nuova funzionalità deve avere almeno un unit test.
2.  I test devono trovarsi in `tests/unit` o `tests/integration`.
3.  Usa `Mock` e `Patch` per isolare dipendenze esterne (Network, DB, UI).

---

## 🎨 Code Style & Quality

Utilizziamo strumenti di analisi statica per mantenere il codice pulito.

- **Linting**: `ruff check .`
- **Formatting**: `black .`
- **Type Checking**: `mypy src/core`

Prima di un commit, assicurati che `ruff` e `mypy` non segnalino errori.

---

## 🚀 Release Process

Per creare una build distribuibile:

1.  Incrementare la versione in `src/core/version.py`.
2.  Eseguire lo script di build:
    ```bash
    python "admin/Crea Setup/build_dist.py"
    ```
3.  L'installer verrà generato nella cartella `dist/`.

---

## 🏛️ Architettura

- **Core**: Logica di business pura (`src/core`). NO dipendenze PyQt.
- **GUI**: Interfaccia utente (`src/gui`). Dipende SOLO da Core.
- **Bots**: Automazione browser (`src/bots`). Orchestrati dalla GUI ma logica isolata.
