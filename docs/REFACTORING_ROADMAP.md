# 🗺️ SYNCROJOB - REFACTORING & DECOMPOSITION ROADMAP

Questo documento traccia i moduli di SyncroJob che richiedono una scomposizione architettonica per aderire al **Single Responsibility Principle (SRP)**, al **Repository Pattern** e all'uso di **Pipelines** di processamento.

## 🎯 Obiettivi Architetturali
- **Models**: Ogni entità deve avere una `dataclass` in `src/models/`.
- **Repositories**: L'accesso al database deve avvenire esclusivamente tramite classi in `src/core/database/repositories/`.
- **Pipelines**: Le operazioni di importazione o trasformazione dati complesse devono usare il pattern `Pipeline`.
- **Controllers**: I pannelli della GUI non devono contenere logica di business, ma delegare a un `Controller`.

---

## 📋 Moduli da Scomporre

### 1. Modulo Timesheet & Calcolo Ore (Alta Priorità)
- **File core**: `src/core/timesheet_processor.py`
- **Problema**: Logica di calcolo ore, straordinari e validazione mescolata in un unico processore procedurale.
- **Azione**:
    - Creare `src/models/timesheet.py`.
    - Creare `TimesheetRepository`.
    - Scomporre la logica di calcolo in `ProcessingSteps`.

### 2. Standardizzazione Importers (Media Priorità)
- **File core**: `src/core/importers/certificati.py`, `src/core/importers/giornaliere.py`, `src/core/importers/scarico_ore.py`.
- **Problema**: Ogni importer ha una struttura leggermente diversa e gestisce internamente la connessione al DB.
- **Azione**:
    - Migrare tutti gli importer al pattern `Pipeline` definito in `src/core/processing/base.py`.
    - Delegare i salvataggi ai rispettivi `Repository`.

### 3. Refactoring Bot Automations (Alta Priorità - Complessità GUI)
- **File GUI**: `src/gui/panels/scarico_ts.py`, `src/gui/panels/scarico_pdl.py`, `src/gui/panels/prenota_bp.py`.
- **Problema**: I pannelli contengono centinaia di righe di codice che gestiscono l'automazione Selenium/Playwright direttamente negli eventi dei bottoni.
- **Azione**:
    - Estrarre la logica di automazione in `src/core/bots/services/`.
    - Implementare `BotController` per gestire lo stato dell'automazione e i segnali verso la GUI.

### 4. Consolidamento Stats & Reports (Bassa Priorità)
- **File core**: `src/core/stats/stats_manager.py`, `src/core/report_service.py`, `src/core/report_history.py`.
- **Problema**: Logica di aggregazione dati duplicata e generazione documenti hard-coded.
- **Azione**:
    - Creare `StatsRepository` per le query di aggregazione.
    - Estrarre i template di report in file esterni o classi dedicate.

### 5. Data Synchronization & Tracker (Media Priorità)
- **File core**: `src/core/data_synchronizer.py`, `src/core/sync/smart_sync.py`.
- **Problema**: Gestione complessa della sincronizzazione tra DB locale e remoto.
- **Azione**:
    - Isolare la logica di "confronto record" in servizi stateless.
    - Usare i `Repository` per le operazioni di I/O.

---

## ✅ Moduli Completati
- [x] **Timesheet & Calcolo Ore**: Pipeline, Model, Step SRP.
- [x] **Contabilità**: Repository, Pipeline, Model, Controller GUI.
- [x] **Certificati & Giornaliere**: Standardizzazione Pipeline e Sync Steps.
- [x] **Scarico Ore**: Migrazione totale a Pipeline SRP con persistenza delegata.
- [x] **Bot Automations**: Disaccoppiamento GUI tramite `BotExecutionController`.
- [x] **Storico OdA**: Repository, Model, Business Controller.
- [x] **Anagrafica Dipendenti**: Repository, Pipeline, Model, DTO.
- [x] **PDL (Permessi di Lavoro)**: Repository, Model, Controller.

---

## 🛠️ Strumenti di Validazione
Dopo ogni scomposizione, eseguire:
1. `python tests/run_robust_tests.py` (Unit & Integration tests)
2. `ruff check .` (Linting & SRP Violations)
3. `mypy src` (Type Safety)
