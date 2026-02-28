# SyncroJob Enterprise - Developer Context (V8.5)

**SyncroJob Enterprise** è una suite integrata di automazione industriale progettata per l'ecosistema ISAB e SafeWork. L'applicazione combina un'interfaccia grafica moderna in PyQt6 con un potente motore di automazione basato su Selenium e PyWin32, offrendo strumenti per la gestione di timesheet, ordini di acquisto (OdA), personale e generazione automatizzata di consuntivi Excel.

## 📂 Struttura del Progetto

```text
C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\
├── main.py                 # Entry point: gestisce splash screen e inizializzazione generativa
├── pyproject.toml          # Configurazione Poetry, Ruff, MyPy, Pytest
├── src/
│   ├── bots/               # Automazione (Selenium/Web drivers)
│   │   ├── base/           # Core Bot: BaseBot (State Machine, Signals, Logging)
│   │   ├── portale_fornitori/ # Bot ISAB (TS, OdA, Prenotazione BP, Timbrature)
│   │   └── safework/       # Bot SafeWork (Ricerca PDL, Certificati)
│   ├── core/               # Business Logic & Infrastructure
│   │   ├── database/       # SQLite Manager (WAL mode, Migrazioni)
│   │   ├── logging/        # Structured Logging (JSON, Context propagation, PII Masking)
│   │   ├── telegram/       # Integrazione Cloud (Notifiche push, Bot Bridge)
│   │   └── preventivi/     # Motore Consuntivi (Win32COM, XML Sanitizer)
│   ├── gui/                # PyQt6 Desktop Interface
│   │   ├── panels/         # Dashboard, Database, Contabilità, Lyra AI
│   │   ├── widgets/        # UI Kit (ModernButton, StandardInput, Sidebar)
│   │   └── controllers/    # Routing (NavigationController), SearchController
│   └── utils/              # Helper funzionali e gestione Asset
├── assets/                 # Risorse statiche (QSS, Icons SVG, Icons app)
├── admin/                  # Tooling (Release, Licenze, Setup, DB Maintenance)
└── tests/                  # Suite di test (Unit, GUI, Integration)
```

## 🛠️ Tech Stack & Standards

*   **Runtime**: Python 3.12.x (Encoding UTF-8 forzato).
*   **GUI**: PyQt6 (Stile Spectacular V8, animazioni hardware-accelerated).
*   **Automation**: Selenium 4.x, PyWin32 (Automazione Macro Excel "Out-of-Process").
*   **Data**: Pandas (Analisi), SQLite (Persistence), OpenPyXL/PyArrow (I/O).
*   **DevOps**: Poetry (Deps), PyInstaller (Build), PyArmor (Obfuscation), Inno Setup (Installer).
*   **Qualità**: Zero segnalazioni da Ruff, MyPy, Refurb e Bandit.

## 📐 Architettura & Pattern Fondamentali

### 1. Sistema di Navigazione (Premium Navigation)
*   **NavigationController**: Gestisce il routing tra 13 pannelli funzionali. Implementa il **Lazy Loading** per lo startup rapido, ma supporta l'**Eager Loading** per i moduli critici (es. Consuntivo) caricati in `finalize_init`.
*   **SidebarWidget**: Navigazione magnetica con track animato. Supporta gruppi a fisarmonica (Accordion) e badge dinamici per notifiche/scadenze.
*   **PageIndex**: Enumerazione centralizzata degli indici di pagina per prevenire conflitti di routing.

### 2. Bot Framework (Robust Automation)
*   **BaseBot**: Tutti i bot ereditano da questa classe che gestisce automaticamente:
    *   State Machine (IDLE, RUNNING, COMPLETED, ERROR).
    *   Reporting per step con avanzamento percentuale.
    *   Screenshot automatici in caso di errore.
    *   Logging contestuale con `trace_id` per ogni sessione di automazione.

### 3. Modulo Consuntivo (High Performance)
*   **Background Processing**: Calcolo progressivi e scansioni directory di rete eseguiti su thread dedicati per non bloccare l'UI.
*   **Smart Caching**: Cache temporale (60s per progressivi, 30s per liste file) per eliminare i caricamenti "a freddo" durante la navigazione.
*   **Professional UI**: Pulsanti centrati, assenza di emoji, input standardizzati e workflow guidato (WorkflowMap).

### 4. Core Services (Singleton Managers)
Accessibili esclusivamente tramite `.instance()`:
*   **DatabaseManager**: Gestione persistenza SQLite con supporto multi-thread.
*   **AuditManager**: Tracciamento di ogni azione amministrativa/operativa.
*   **NotificationManager**: Sistema centralizzato per Toast, Tray Notifications e Alert.
*   **ConfigManager**: Gestione cifrata delle credenziali e preferenze utente.

## 📋 Enterprise Logging System
Localizzato in `src/core/logging/`, il sistema produce log strutturati in `logs/app.json`:
*   **Context Propagation**: I log includono automaticamente `span_id` e `trace_id`.
*   **Performance Monitoring**: Decoratore `@measure_time` per individuare colli di bottiglia.
*   **PII Masking**: Filtro automatico di password, CF, email e dati sensibili.

## 📝 Regole d'Ingegneria del Software
1.  **Imports**: Sempre assoluti da `src` (es. `from src.core.constants import ...`).
2.  **Encoding**: Ogni file modificato deve mantenere l'encoding UTF-8.
3.  **UI Consistency**: Utilizzare esclusivamente i componenti in `src.gui.widgets.core_widgets` (es. `StandardInput` invece di `QLineEdit`).
4.  **Async Ops**: Mai eseguire operazioni di rete o I/O pesante nel thread GUI. Usare `QThread` o `threading.Thread` con segnali sicuri.
5.  **Clean Code**: Il progetto deve superare i controlli `ruff check .` e `mypy .` prima di ogni commit.
