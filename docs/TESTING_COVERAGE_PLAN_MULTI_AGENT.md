# 🚀 Piano di Automazione Testing: Operazione 80% Coverage

Questo documento definisce la strategia per scalare la Test Coverage dell'applicativo ISAB_TimeSheet fino al target dell'80%, coordinando l'intervento simultaneo di **più Agenti IA in parallelo**.

L'architettura del software prevede un'alta modularità, permettendo la suddivisione del lavoro in **Stream (Corsie di Lavoro)** indipendenti, minimizzando i conflitti di merge e le race conditions durante il testing.

---

## 📊 Obiettivo
- **Target Coverage:** >= 80% globale
- **Strumenti:** `pytest`, `pytest-cov`, `unittest.mock`, `tests/run_robust_tests.py`
- **Requisiti Qualitativi:** Nessun test *flaky*, adozione di Fixtures riutilizzabili (`conftest.py`), no side-effects (isolamento tramite file in-memory o mock di I/O).

---

## 🔀 Stato degli Stream di Lavoro

### ✅ Stream A: Entità di Dominio e Utility (COMPLETATO)
- **Stato:** 100% Coverage sui modelli di dati.
- **File testati:** `src/models/*`, `src/utils/parsing.py`, `src/utils/validators.py`, `src/utils/date_utils.py`.

### ✅ Stream B: Accesso Dati e Repository (COMPLETATO)
- **Stato:** Copertura dei repository e del database manager.
- **Target raggiunto:** `src/core/database/repositories/`, `src/core/database/manager.py`, `src/core/audit/`.

### ✅ Stream C: Logica di Business Core (COMPLETATO)
- **Stato:** Coverage estesa su Importers, Configurazione e Boot.
- **File testati:**
  - `src/core/importers/*` (Giornaliere, Attività, Certificati, OdA, Contabilità, Scarico Ore, PDL Sync).
  - `src/core/config_manager.py` e `src/core/config/*` (Accounts, Migration, Security).
  - `src/core/app_initializer.py`.

### ✅ Stream D: Automazione Browser (Bots) & Web Scraping (COMPLETATO)
- **Stato:** Copertura delle classi base e dei bot principali.
- **File testati:**
  - `src/bots/base/*` (BaseBot, PlaywrightBase, StepManager, ExecutionGuard).
  - `src/bots/portale_fornitori/scarico_ts/bot.py`.
  - `src/bots/portale_fornitori/prenota_bp/bot.py`.
  - `src/bots/portale_fornitori/timbrature/bot.py` e `storage.py`.

### ✅ Stream E: Interfaccia Grafica - Design & Styles (COMPLETATO)
- **Stato:** Copertura del sistema di design e degli helper di stile.
- **File testati:**
  - `src/gui/design/*` (Colors, Spacing).
  - `src/gui/styles/*` (ThemeManager, PaletteHelpers, WidgetStyles, UIEffects).
  - `src/gui/formatters.py`.

### 🔵 Stream F: Telegram Bridge & Messaging (IN CORSO - Agente Attuale)
- **Stato:** Inizio analisi `src/core/telegram/`.
- **Target:** `src/core/telegram/service.py`, `src/core/telegram/bridge/`.
- **Istruzioni:** Mockare le API di Telegram (`python-telegram-bot`) e testare la gestione degli intenti e dei comandi.

---

## 🔄 Workflow Standard per ogni Agente

1. **Reconnaissance (Ricerca):** Controllare l'output di `pytest --cov=src` per il modulo bersaglio. Verificare se esistono test precedenti in `tests/unit/`.
2. **Setup:** Se il modulo non ha una sua folder di test dedicata, crearla (es: `tests/unit/core/database/`).
3. **Execution:** Creare i test utilizzando le classi standard (es: `class TestMyClass:`). Implementare Edge Cases (None, stringhe vuote, tipi incorretti).
4. **Validation:** Eseguire:
   ```bash
   # Usa il custom runner per validazione rapida del singolo file
   python tests/run_robust_tests.py tests/unit/<percorso_nuovo_test>.py
   ```
5. **Report & Passaggio:** Fornire all'utente il report del coverage raggiunto sul singolo file tramite `--cov=src.<percorso> --cov-report=term-missing`.

---

## ⚡ Prossimi Passi (Immediati)
- **Agente Attuale:** Focus su `src/core/telegram/service.py`. Implementazione test per l'invio messaggi e gestione bot.
