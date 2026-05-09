# SyncroJob - AI Architecture & Engineering Standards

Questo documento centralizza la conoscenza strutturale e le regole di codifica per Gemini CLI.

## 🏗️ Architettura Generale (MVC/Controller Pattern)
Il progetto segue una struttura ispirata al pattern Model-View-Controller, con un forte uso di **Controller** per disaccoppiare la logica dalla visualizzazione.

### 1. Core Services (`src/core/`)
- `DatabaseManager` (`src/core/database/manager.py`): Gestore unico SQLite. Implementa un singleton thread-safe con supporto WAL e migrazioni atomiche.
- `ConfigManager` (`src/core/config_manager.py`): Gestione file `.json` per impostazioni utente e costanti globali.
- `NotificationManager` (`src/core/notification_manager.py`): Hub centrale per messaggi di sistema e segnali GUI.
- `AuditManager` (`src/core/audit/manager.py`): Gestione log centralizzati delle azioni dell'utente e sistema per compliance enterprise.
- `TelegramService` (`src/core/telegram/service.py`): Bot per notifiche push e controllo remoto dello stato dei bot.

### 2. GUI Layer (`src/gui/`)
- `MainWindow`: Container principale, gestisce Sidebar e PageStack (SlidingStackedWidget).
- `ThemeManager`: Gestisce QPalette e QSS (Material Design proprietario).
- **Controllers**:
    - `NavigationController`: Gestisce i cambi pagina e il caricamento on-demand (**Lazy Loading**).
    - `BotController`: Coordina il ciclo di vita dei bot di automazione (Init -> Login -> Run -> Cleanup).
    - `ServiceController`: Gestisce il ciclo di vita dei servizi di background (Telegram).

### 3. Automation Layer (`src/bots/`)
- Bot basati su Selenium per interagire con i portali ISAB/SafeWork.
- **Resilience**: Ereditano da `BaseBot`. Cattura automatica di screenshot e HTML in caso di crash.
- **POM**: Uso rigoroso del Page Object Model.
- **State Machine**: I bot gestiscono lo stato tramite l'enum `BotStatus` (`IDLE`, `INITIALIZING`, `LOGGING_IN`, `RUNNING`, `COMPLETED`, `ERROR`, `STOPPED`).

---

## 🛠️ Pattern & Convenzioni Tecniche

### 1. PySide6 Singleton con Segnali
**NON** ereditare da `QObject` se si usa il pattern `__new__` per il singleton. Usare una classe segnali separata:
```python
class MyManager:
    _instance = None
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    def __init__(self):
        self.signals = MySignals.instance() # MySignals eredita da QObject
```

### 2. Lazy Loading Navigation
I pannelli della UI devono essere registrati nel `NavigationController` e creati solo tramite metodi `_create_*` al primo accesso.
**Procedura per aggiungere un nuovo pannello:**
1. Aggiungere il nome all'enum `PageIndex` in `main_window.py`.
2. Creare il placeholder nel loop `_setup_ui()` della `MainWindow`.
3. Aggiungere il metodo factory `_create_*` in `navigation_controller.py`.
4. Registrare il metodo nel dizionario `creators` associandolo al valore di `PageIndex`.

### 3. Localizzazione Termini di Dominio
- **Timbrature**: Attendance/clock-ins.
- **OdA**: Ordine di Acquisto.
- **PDL**: Permesso di Lavoro.
- **Scarico/Carico**: Download/Upload.

---

## 🛠️ DevOps & Manutenzione

### 1. Gestione Cache
Dopo aver modificato manager core o classi singleton, è consigliato pulire la cache per evitare import obsoleti:
```bash
# Windows (PowerShell)
Get-ChildItem -Path src -Filter "__pycache__" -Recurse | Remove-Item -Recurse -Force
```

### 2. Build Pipeline
Il processo di release è automatizzato via `admin/release.py` e include:
- Version Bumping.
- Gestione dipendenze via Poetry.
- Esecuzione Test Robustezza.
- Compilazione setup via Inno Setup.

---

## 🚨 Standard Architetturali (Ferrei)

### 1. Separazione delle Responsabilità (SoC & SRP)
*   **CORE**: Non deve mai importare nulla da `src/gui`.
*   **CONTROLLERS**: Unico punto di contatto tra GUI e Core. Gestiscono lo stato.
*   **SRP (Single Responsibility Principle)**: Nessuna classe deve avere responsabilità multiple (es. UI + Logica). Se un file accumula troppa complessità, va scomposto immediatamente in Componenti/Widget specializzati.

### 2. Modularità e Performance
*   **Lazy Loading**: I pannelli della `MainWindow` devono essere istanziati solo al primo accesso reale.
*   **Thread Safety**: Ogni operazione di I/O pesante (Bot, SQL massive, scansione file) **DEVE** essere eseguita in un thread separato (`QThread` or `QTimer` differiti).
*   **Strangler Fig Pattern**: For the refactoring of large modules, move incrementally by moving one function at a time and using temporary re-exporting so as not to break dependencies.

### 3. Comunicazione tra Layer
*   **Segnali (PySide6)**: È l'unico modo permesso per la comunicazione GUI -> Core e vice-versa.
*   **Singleton Access**: Manager globali acceduti esclusivamente tramite `.instance()`.
*   **Naming**: Suffissi `_requested` (comando), `_changed` (stato), `_failed` (errore).

### 4. Database & Sync
*   **Schema First**: Migrazioni definite in `src/core/database/migrations/`.
*   **Atomicità**: Salvataggi atomici e uso di tabelle temporanee per calcolare i delta (query `EXCEPT`).

### 5. Qualità e Static Analysis
*   **Zero Warnings**: `ruff`, `mypy` e `refurb` devono restituire 0 segnalazioni.
*   **Type Hinting**: Obbligatorio ovunque.
*   **Encoding**: Forza sempre **UTF-8**.
*   **Persistence**: Ogni fix tecnico o scoperta architetturale deve essere storicizzato nei file MD di questa cartella (`.gemini/`) per preservare la memoria del progetto.
