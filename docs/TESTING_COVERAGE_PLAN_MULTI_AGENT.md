# 🚀 Piano di Automazione Testing: Operazione 80% Coverage

Questo documento definisce la strategia per scalare la Test Coverage dell'applicativo ISAB_TimeSheet fino al target dell'80%, coordinando l'intervento simultaneo di **più Agenti IA in parallelo**.

L'architettura del software prevede un'alta modularità, permettendo la suddivisione del lavoro in **Stream (Corsie di Lavoro)** indipendenti, minimizzando i conflitti di merge e le race conditions durante il testing.

---

## 📊 Stato Attuale (Aggiornato al 17/05/2026)
- **Target Coverage:** 80%
- **Coverage Reale:** **49%** ⚠️
- **Test Totali:** 1624
- **Passati:** 1537
- **Falliti:** 87 ❌ (Necessaria fase di fix)

---

## 🔀 Stato degli Stream di Lavoro

### ✅ Stream A: Entità di Dominio e Utility (COMPLETATO)
- **Stato:** 100% Coverage sui modelli di dati.
- **File testati:** `src/models/*`, `src/utils/parsing.py`, `src/utils/validators.py`, `src/utils/date_utils.py`.

### ✅ Stream B: Accesso Dati e Repository (COMPLETATO)
- **Stato:** Copertura dei repository e del database manager.
- **Target raggiunto:** `src/core/database/repositories/`, `src/core/database/manager.py`.

### ✅ Stream C: Logica di Business Core (COMPLETATO)
- **Stato:** Coverage estesa su Importers, Configurazione e Boot.
- **File testati:**
  - `src/core/importers/*` (tutti gli importatori Excel/CSV).
  - `src/core/config_manager.py` e `src/core/config/*`.
  - `src/core/app_initializer.py`.

### ✅ Stream D: Automazione Browser (Bots) & Web Scraping (COMPLETATO)
- **Stato:** Copertura delle classi base e dei bot principali.
- **File testati:** `src/bots/base/*`, `src/bots/portale_fornitori/*`.

### ✅ Stream E: Interfaccia Grafica - Design & Styles (COMPLETATO)
- **Stato:** Copertura del sistema di design e degli helper di stile.
- **File testati:** `src/gui/design/*`, `src/gui/styles/*`, `src/gui/formatters.py`.

### ✅ Stream F: Telegram Bridge & Messaging (COMPLETATO)
- **Stato:** Copertura completa del controllo remoto.
- **File testati:** `src/core/telegram/*`.

### ✅ Stream G: Sistemi Critici di Integrità e Sicurezza (COMPLETATO)
- **Stato:** Messi in sicurezza i componenti vitali.
- **File testati:** `license_validator.py`, `security.py`, `audit/*`, `bug_reporter.py`, `auth_monitor.py`, `updater/engine.py`.

### ✅ Stream H: Widget Grafici Complessi (COMPLETATO)
- **Stato:** Testati i widget custom e le basi dei pannelli.
- **File testati:** `src/gui/widgets/`, `src/gui/panels/base.py`.

### ✅ Stream I: Orchestrazione e Manager (COMPLETATO)
- **Stato:** Copertura di tutte le classi "Manager" che coordinano i flussi di dati.
- **File testati:** `src/core/contabilita_manager.py`, `src/core/oda_manager.py`, `src/core/stats_manager.py`, `src/core/notification_manager.py`, `src/core/sync_tracker.py`.

### 🔵 Stream J: Pannelli Specifici (IN CORSO - Agente Attuale)
- **Stato:** Inizio implementazione test per i pannelli operativi via `pytest-qt`.
- **Target:** `src/gui/panels/` (es. `scarico_ore_panel.py`, `carico_ts.py`, `pdl_panel.py`).
- **Gap:** Coverage attuale ~15-20% per modulo.

### 🔴 Stream K: Analisi, KPI e Stabilità (PROSSIMO)
- **Obiettivo:** Coprire la logica di calcolo avanzata in `src/core/contabilita/stats_service.py` e risolvere i 87 fallimenti attuali.

---

## 🔄 Workflow Standard per ogni Agente
1. **Reconnaissance (Ricerca):** Controllare l'output di `pytest --cov=src` per il modulo bersaglio. Verificare se esistono test precedenti in `tests/unit/`.
2. **Setup:** Se il modulo non ha una sua folder di test dedicata, crearla.
3. **Execution:** Creare i test utilizzando le classi standard. Implementare Edge Cases.
4. **Validation:** Eseguire `tests/run_robust_tests.py`.
5. **Report & Passaggio:** Fornire all'utente il report del coverage raggiunto.

---

## ⚡ Prossimi Passi (Consigliati)
- **Stream K: Analisi e KPI:** Coprire la logica di calcolo avanzata in `src/core/contabilita/stats_service.py` e i relativi pannelli grafici.
- **Stream L: Integrazione End-to-End:** Test di integrazione che simulano il caricamento di un file e la sincronizzazione verso il database reale/temporaneo.
