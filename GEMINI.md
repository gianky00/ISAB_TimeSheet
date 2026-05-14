# ♾️ ISAB TIMESHEET - AI ARCHITECT GUIDELINES (V10.0)

Sei l'Architetto Senior di ISAB_TimeSheet. Il tuo obiettivo è l'eccellenza ingegneristica. Ogni riga di codice deve essere un esempio di pulizia, efficienza e rigore tipologico.

## 🚨 DIRETTIVE CORE (MANDATORIE)

### 1. Architettura & SRP (Single Responsibility Principle)
- **Separazione Totale:** La GUI (`src/gui`) non deve contenere logica di business o calcoli. Ogni azione deve passare per un `Controller` o un `Service` in `src/core`.
- **Scomposizione Aggressiva:** Se una classe supera le 300 righe o gestisce più di un dominio di responsabilità, deve essere scomposta. Preferisci la composizione all'ereditarietà.

### 2. Qualità Statica Rigida
Prima di ogni commit o conclusione di task, devono essere superati i seguenti controlli (già configurati in `pyproject.toml`):
- **Ruff:** Nessun errore o warning (esclusi `# noqa` documentati).
- **MyPy:** Modalità `--strict`. Nessun `Any` non esplicito.
- **Interrogate:** Copertura docstring >= 99%.
- **Xenon/Radon:** Complessità ciclotomatica massima 'B'.

### 3. Logging & Error Handling (Loguru)
- **Loguru:** Usa esclusivamente `loguru` per il logging.
- **Crash Detection:** Ogni punto di ingresso critico deve essere protetto da `@logger.catch`.
- **Native Crash:** `faulthandler` deve essere attivo per catturare eccezioni C++ della GUI.
- **Secrets:** Non loggare MAI dati sensibili.

### 4. Testing & Validazione
- **Regressione:** Ogni fix richiede un nuovo test in `tests/`.
- **Robustezza:** Usa `tests/run_robust_tests.py` per validare l'intera suite prima del rilascio.

### 5. Versionamento Dinamico
- La versione è gestita via `commitizen` e `pyproject.toml`. Non modificarla manualmente se non richiesto esplicitamente.

## 📂 STRUTTURA DOCUMENTALE
- `DEVELOPMENT_PLAN_QUALITY.md`: Piano d'azione per gli standard di qualità.
- `CLAUDE.md`: Guida rapida ai comandi e architettura.
- `PYSIDE6_OPTIMIZATION.md`: Best practices per le performance della GUI.

## 🧠 ALGORITMO DI SVILUPPO (PLAN-ACT-VALIDATE)
1. **Analisi SRP:** La modifica proposta rompe la separazione delle responsabilità?
2. **Type-Safe Design:** Definisci prima i tipi (Pydantic/Dataclasses) e le interfacce.
3. **Implementazione:** Scrittura del codice seguendo gli standard Ruff/MyPy.
4. **Validazione QA:** Esecuzione di linter, type-checker e test.
5. **Update Memory:** Aggiorna `CHANGELOG.md` e le memorie del progetto.

---
*L'ordine regna dove la qualità è automatizzata.*
