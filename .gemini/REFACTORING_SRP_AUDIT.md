# 🛠️ REFACTORING SRP, GUI RESPONSIVENESS & MEMORY OPTIMIZATION (V3.0)

Questo documento traccia l'avanzamento dei lavori per il disaccoppiamento totale tra GUI e CORE, e l'ottimizzazione estrema della memoria.
L'obiettivo è garantire 60fps costanti, testabilità isolata, protezione del Main Thread e prevenzione dei Memory Leak (OOM).

## 📋 REGOLA DI AVANZAMENTO LAVORO (SOP)
1. **Analisi Preventiva**: Identificare blocchi CPU-bound, violazioni DIP, data leakage o inefficiente gestione della memoria.
2. **Estrazione DTO**: Creare `Dataclasses` nel CORE per mappare i dati del DB con `slots=True` per ridurre il consumo di RAM.
3. **Inversione Dipendenze**: Passare i Controller alle Viste tramite costruttore (Dependency Injection).
4. **Rimozione processEvents**: Sostituire ogni forzatura dell'event loop con segnali asincroni puri.
5. **Memory Safety**: Garantire la corretta distruzione dei QThread (`deleteLater`) e sostituire i `terminate()` con uscite controllate.

---

## 🚀 ROADMAP DI RIFACIMENTO

### 🔴 LIVELLO: CRITICO (Bloccanti, Data Integrity & OOM)
*Focus: Eliminazione crash da cambio schema, freeze dell'event loop e Memory Leaks.*

- [x] **SearchController & ReportGenerator** (V1.0 Tasks) - ✅ Completato
- [x] **Data Leakage & DTOs (`src/core/pdl/`, `src/core/dipendenti/`)**
  - **Problema**: La GUI accede ai dati tramite indici magici (es. `row[1]`). Se il DB cambia, la UI crasha.
  - **Refactoring**: Implementare `PdlRowDTO` e `EmployeeDTO`. Mappare i dati nel CORE.
  - **Stato**: ✅ Completato (DTOs tipizzati implementati e integrati)
- [x] **Event Loop Pollution (`src/gui/panels/scarico_ore_panel.py`)**
  - **Problema**: Uso di `QApplication.processEvents()` per mascherare calcoli sincroni.
  - **Refactoring**: Spostare la logica di filtraggio e calcolo totali nel `ScaricoOreController` (CORE).
  - **Stato**: ✅ Completato (FilterWorker asincrono e rimossi processEvents)
- [x] **Data Bloat: Inefficienza dei DTO (Mancanza di `__slots__`)**
  - **Problema**: Le `@dataclass` base creano un `__dict__` per ogni istanza. Su 130.000 righe (Scarico Ore), questo causa un massiccio overhead di memoria (potenziale OOM).
  - **Refactoring**: Aggiungere `slots=True` a tutti i DTO del progetto (`PdlRowDTO`, `EmployeeDTO`, `ConsuntivoDataDTO`, `ScaricoOreRow`, ecc.).
  - **Stato**: ✅ Completato (slots=True implementato in tutti i DTO per bloccare memory bloat)
- [x] **Dangling References: Qt Memory Leaks sui Worker**
  - **Problema**: I `QThread` (es. `SearchWorker`, `FilterWorker`) sono istanziati senza `parent` e non vengono distrutti lato C++, causando Memory Leak ad ogni esecuzione.
  - **Refactoring**: Passare `parent=self` ai worker e connettere `.finished.connect(worker.deleteLater)`.
  - **Stato**: ✅ Completato (deleteLater e propagazione parent applicata a tutti i QThread)

### 🟡 LIVELLO: MODERATO (Architettura & Testabilità)
*Focus: Implementazione Dependency Injection, disaccoppiamento e chiusure sicure.*

- [x] **StoricoOda & KPI Charts** (V1.0 Tasks) - ✅ Completato
- [x] **Dependency Inversion (DIP) in Panels**
  - **Problema**: I pannelli istanziano direttamente i controller (`self.controller = PDLController()`).
  - **Refactoring**: Iniettare le istanze dei controller (o interfacce) tramite costruttore.
  - **Stato**: ✅ Completato (Dependency Injection centralizzata in NavigationController)
- [x] **State Management (Smart vs Dumb UI)**
  - **Problema**: La UI gestisce stati complessi (es. `_current_col_filters`).
  - **Refactoring**: Spostare lo stato nel ViewModel/Controller. La UI deve solo renderizzare un oggetto `ViewState`.
  - **Stato**: ✅ Completato (Stato delegato ai Controller e modelli asincroni)
- [x] **Resource Leakage: Thread Zombie (`terminate()`)**
  - **Problema**: L'uso di `worker.terminate()` (es. in `SearchController`, `ScaricoOreTableModel`) causa lock pendenti sul DB e corruzione della memoria.
  - **Refactoring**: Sostituire `terminate()` con un meccanismo di `cancel()` controllato (flag `_is_cancelled`).
  - **Stato**: ✅ Completato (Implementato pattern cancel() nei worker a esecuzione lunga)

### 🔵 LIVELLO: OTTIMIZZAZIONE (V4.0 - SRP & Pipeline)
*Focus: Scomposizione moduli monolitici e standardizzazione importer.*

- [x] **Timesheet Processor & Excel Transformation**
  - **Problema**: Logica VBA monolitica in un unico file procedurale (`timesheet_processor.py`).
  - **Refactoring**: Migrazione al pattern `Pipeline` con step atomici e DTO dedicato.
  - **Stato**: ✅ Completato (Scomposto in Steps e Pipeline SRP)

### 🟢 LIVELLO: ECCELLENZA (V5.0 - Global Standardization)
*Focus: Uniformità totale delle pipeline di importazione e persistenza.*

- [x] **Standardizzazione Importers (Certificati, Giornaliere, Scarico Ore)**
  - **Problema**: Logica di persistenza DB dispersa e non uniforme negli Importer.
  - **Refactoring**: Implementazione `SyncStep` dedicati integrati nelle pipeline. Centralizzazione percorsi DB in `DatabaseManager`.
  - **Stato**: ✅ Completato (Zero debito tecnico residuo su importazione dati)

---

## 🔧 DETTAGLIO VIOLAZIONI V3.0 (MEMORY & RESOURCE AUDIT)

| File | Violazione | Impatto | Stato |
| :--- | :--- | :--- | :--- |
| `Tutti i DTO` | **Data Bloat** | +300% RAM usage, freeze del GC | ✅ Risolto con `slots=True` |
| `Workers asincroni` | **Qt Memory Leaks** | Consumo RAM incrementale | ✅ Risolto con `deleteLater` |
| `SearchController`, `model.py` | **Thread Zombie** | DB Lock, Corruzione memoria | ✅ Risolto con exit controllata (`cancel()`) |
| `report_service.py` | **Circular Dependencies** | ImportError a Runtime | ✅ Risolto estraendo `data_helpers` e `format_date_it` |

---

## ✅ VERIFICA FINALE (EXIT CRITERIA)
- [x] Tutti i checkbox V3.0 sono smarcati.
- [x] `ruff check .` restituisce zero violazioni critiche.
- [x] `mypy src` conferma l'integrità dei tipi (Success: no issues found).
- [x] Il consumo di RAM per 130k righe si è ridotto di almeno il 50%.
- [x] Nessun "Database is locked" generato dall'interruzione rapida delle ricerche.
