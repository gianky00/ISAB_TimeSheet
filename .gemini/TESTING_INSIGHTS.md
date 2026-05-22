# SyncroJob - Testing Insights & QA Standards

Questo diario tiene traccia delle scoperte critiche e delle regole mandatorie per la suite di test.

## 🛡️ REGOLA MANDATORIA (MANDATORY)
**OGNI OPERAZIONE DI TEST DEVE UTILIZZARE IL RUNNER ROBUSTO.**
- **Comando**: `scripts/avvio_test.bat`
- **Engine**: `python tests/run_robust_tests.py`
- **DIVIETO**: Non usare `pytest` direttamente. Il runner robusto gestisce l'isolamento dei processi Qt, i timeout e previene i crash della GDI su Windows.

---

## 🔍 Scoperte Architetturali e Fix Storici

### 1. Gestione Crittografica (Marzo 2026)
*   **Problema**: Molteplici fallimenti nei test di licenza/secrets a causa di decodifica Base64 errata.
*   **Root Cause**: I test decodificavano i token Fernet prima di passarli alla libreria, mentre `cryptography.fernet` richiede la stringa Base64 originale (url-safe).
*   **Lezione**: `SecretsManager` ritorna stringhe Base64 in UTF-8. Non decodificarle mai manualmente nei test o nel codice client prima dell'uso con Fernet.

### 2. Incongruenza Chiavi Dizionario (Marzo 2026)
*   **Problema**: Crash nei test di integrazione SafeWork PDL.
*   **Root Cause**: Il test usava la chiave `"pdl_number"`, ma il bot/UI si aspettava `"numero_pdl"`.
*   **Standard**: Verificare sempre `get_columns()` nel bot per assicurare la parità tra dati mockati e aspettative del parser.

### 3. Crash Point Qt/Accessibility
*   **Problema**: `test_make_accessible` causava crash della suite intera.
*   **Soluzione**: Isolamento forzato nel runner robusto e pulizia dei widget Qt nel `tearDown`.

---

## 🛠️ Convenzioni di Testing

### 1. Struttura dei Test
- I file di test devono rispecchiare la struttura della cartella `src/` all'interno di `tests/` (es. `src/core/auth.py` -> `tests/unit/test_auth.py`).
- Utilizzare fixture globali definite in `tests/conftest.py`.

### 2. Mocking e Isolamento
- **Bot**: Mockare sempre il Selenium WebDriver per evitare l'apertura di browser reali durante i test unitari.
- **UI**: Mockare `QApplication` e utilizzare `qtbot` per interagire con i widget.
- **Database**: Utilizzare database in memoria (`:memory:`) o fixture che ripuliscono lo stato dopo ogni test.

---

## 📈 Metriche di Qualità Target (Stato Attuale)
- **Docstring Coverage**: >= 99% (via `poetry run interrogate src/`) — già raggiunto.
- **Test Coverage**: > 80% per i moduli Core e Bot Critici (target in corso).
- **Zero Warnings**: Ruff 0 | MyPy 0 — già raggiunto e monitorato via pre-commit.
