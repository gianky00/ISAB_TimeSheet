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

### 4. Integrità Segnali PySide6 (QT)
- **Signal Safety:** Non rimuovere MAI le `lambda` dalle connessioni dei segnali (es. FURB111) a meno che mittente e destinatario non abbiano la stessa firma. La stabilità della UI prevale sulla brevità del codice.
- **Explicit Disconnect:** Disconnetti sempre i segnali se il widget viene riutilizzato dinamicamente.

### 5. Testing & Validazione
- **Regressione:** Ogni fix richiede un nuovo test in `tests/`.
- **Validazione Unica:** L'esecuzione dei test deve avvenire esclusivamente tramite `python -m tests.run_robust_test`. È vietato l'uso diretto di `pytest` per evitare conflitti con il singleton QApplication.

### 6. Versionamento Dinamico
- La versione è gestita via `commitizen` e `pyproject.toml`. Non modificarla manualmente se non richiesto esplicitamente.

### 7. Tipizzazione Semantica & Pydantic V2
- **Validazione Pydantic:** Per tutti i nuovi modelli di scambio dati (es. payload estratti dai bot o configurazioni complesse), usa modelli `pydantic.BaseModel` per abilitare la validazione e il parsing automatico a runtime con zero allucinazioni di tipo.
- **Protocolli (typing.Protocol):** Disaccoppia i moduli definendo contratti formali tramite `Protocol` invece di ereditarietà rigida. Questo rende i test mocking nativi e aiuta i futuri LLM a capire immediatamente le interfacce disponibili.
- **Tipizzazione Semantica (typing.Annotated):** Arricchisci le firme dei metodi usando `Annotated` per associare metadati semantici o di validazione di business (es. `Annotated[str, Field(pattern="^[A-Z0-9]{16}$")]` per Codici Fiscali).

## 📂 STRUTTURA DOCUMENTALE
- `.ai-context.json`: **Fonte di verità architetturale** machine-readable (versione, layout, DB, bot, regole). Generato da `tools/generate_ai_context.py`.
- `CLAUDE.md`: Guida rapida operativa — comandi, pattern di codice, pitfall comuni.
- `PYSIDE6_OPTIMIZATION.md`: Best practices per le performance e signal safety in PySide6.
- `docs/`: Documentazione tecnica, schemi JSON, piani di refactoring.

## 🧠 ALGORITMO DI SVILUPPO (PLAN-ACT-VALIDATE)
1. **Analisi SRP:** La modifica proposta rompe la separazione delle responsabilità?
2. **Type-Safe Design:** Definisci prima i tipi (Pydantic/Dataclasses) e le interfacce.
3. **Implementazione:** Scrittura del codice seguendo gli standard Ruff/MyPy.
4. **Validazione QA:** Esecuzione di linter, type-checker e test.
5. **Update Memory:** Aggiorna `CHANGELOG.md` e le memorie del progetto.

---
*L'ordine regna dove la qualità è automatizzata.*
