# SyncroJob - AI Context & Architecture
Questo file fornisce il contesto architettonico per l'IA Gemini.

## Architettura Generale (MVC/Controller Pattern)
Il progetto segue una struttura ispirata al pattern Model-View-Controller, con un forte uso di **Controller** per disaccoppiare la logica dalla visualizzazione.

### 1. Core Services (`src/core/`)
- `DatabaseManager`: Gestore unico SQLite. Usa `db_manager` (singleton).
- `ConfigManager`: Gestione file `.json` per impostazioni utente.
- `NotificationManager`: Hub centrale per messaggi di sistema e segnali GUI.
- `LyraSentinel`: Motore di monitoraggio anomalie (background).
- `TelegramService`: Bot per notifiche e controllo remoto.

### 2. GUI Layer (`src/gui/`)
- `MainWindow`: Container principale, gestisce Sidebar e PageStack.
- `ThemeManager`: Gestisce QPalette e QSS (Material Design).
- **Controllers**:
    - `NavigationController`: Gestisce i cambi pagina e il caricamento on-demand (Lazy Loading).
    - `BotController`: Coordina i bot di automazione.
    - `ServiceController`: Gestisce il ciclo di vita dei servizi di background (Lyra, Telegram).

### 3. Automation Layer (`src/bots/`)
- Bot basati su Selenium per interagire con i portali ISAB.
- **Resilience**: Cattura automatica di screenshot e HTML in `logs/errors/` in caso di crash.

### 4. Stability & DevOps (`admin/`)
- **Release Pipeline**: `release.py` automatizza il ciclo Bump -> Sync -> Test -> Build -> Tag -> Notify.
- **Pre-Flight Check**: Impedisce release se ci sono divergenze tra Poetry e requirements.txt o versioni disallineate.
- **DB Migrations**: Sistema integrato in `DatabaseManager` tramite `PRAGMA user_version` per aggiornamenti di schema safe.

## Convenzioni di Codice
- **UI**: Sempre PyQt6. Stili definiti in `assets/styles/`.
- **Typing**: Uso obbligatorio di Python Type Hints.
- **Async**: Logica pesante delegata a `QThread` o `QProcess` per non bloccare la GUI.
- **GDI Safety**: Pulizia forzata dei widget Qt nei test per prevenire leak su Windows.
