## Unreleased

### Feat

- **certificati**: implement professional toolbar and layout optimization
- **pdf**: aggiunta categoria strumenti Assenti e perfezionamento layout padri
- **certificati**: ripristino logica scadenze e ottimizzazione report PDF
- **certificati**: aggiornamento elenco ubicazioni e migrazione dati
- **certificati**: implementazione full mirroring 1:1, ripristino metadati da PDF e ricerca avanzata per ID-COEMI

### Fix

- **certificati**: ottimizzazione layout PDF e risoluzione crash in analisi scadenze

### Refactor

- scomposizione logica statistiche e fix qualità core
- **certificati**: centralizzazione costanti e separazione logica statistiche

## v1.43.2 (2026-04-21)

## v1.43.1 (2026-04-21)

## v1.43.0 (2026-04-21)

### Feat

- align project and improve browser security (removed large binaries)

### Fix

- **pw**: change password input type to text before submit to completely bypass chromium password compromised alert
- **pw**: ultra-aggressive alert handling and hardened password suppression
- **portale-fornitori**: implement ultra-robust PW interaction pattern and accelerate login

## v1.42.1 (2026-04-20)

### Fix

- **portale-fornitori**: implement robust interaction pattern for PW bots and fix scarico_ts timeout

### Refactor

- rimozione globale emoji per risolvere l'errore di encoding charmap / cp1252

## v1.42.0 (2026-04-20)

### Feat

- automate CHANGELOG.md generation in release process via Commitizen
- aggiunto selettore SOCIETA' (ISAB/PSER) per login portale fornitori e aggiornata logica bot (Selenium/Playwright)
- consolidamento architettura Playwright, fix locatori SafeWork e controlli dinamici nel footer
- migrazione strutturale a Playwright con supporto dual-engine e migrazione di tutti i bot principali

### Fix

- **runner**: V5.3.1 - Fail-Fast aggressivo, isolamento coverage e bonifica suite test
- **runner**: V5.1 - Fix 6 bug + 2 miglioramenti architetturali\n\nBUG-1: Fix doppio conteggio passed/failed nella fase isolamento SHOTGUN\nBUG-2: _parse_pytest_summary ora cattura sia 'failed' che 'error' con findall\nBUG-3: Commento correttivo su AssertionError match\nBUG-4: SNIPER retry usa --last-failed invece di rieseguire tutti i target\nBUG-5: Pattern E-prefix non piu' limitato a 'not failures'\nBUG-6: _extract_traceback_block matching preciso con delimitatori pytest\nARCH-2: sys.exit() centralizzato in __main__, metodi usano _exit_code\nARCH-4: Report IA troncato a MAX_OUTPUT_CHARS, -80% dimensione\n\nAggiunto test suite: tests/unit/test_runner_internals.py (34 test)"
- implementato metodo show_settings in MainWindow per attivare l'ingranaggio dei parametri bot
- corretto locatore Società in 'Company' e migliorata robustezza login Playwright/Selenium
- Correzione nome attributo locatore ScaricoTSLocators
- Risoluzione errore 'Unknown engine name' e centralizzazione selettori Playwright
- risolto errore importazione PrenotaBP e implementato caricamento granulare bot Playwright
- risolto problema switch motore automazione invalidando la cache config

### Refactor

- allineamento suite di test, fix linting ruff/mypy e aggiornamento componenti GUI
- stabilizzazione Playwright, soppressione popup Chromium, bugfix switch account e 100% qualità (Ruff/MyPy/Interrogate)

## v1.41.2 (2026-04-01)

## v1.41.1 (2026-04-01)

## v1.41.0 (2026-03-31)

### Feat

- update engine optimization and premium wave animation integration

## v1.40.3 (2026-03-30)

### Fix

- resolve updater crash by removing duplicate signal connections and adding error handling
- update banner labels, progress formatting and completion handler
- resolve update banner version display and initialization hang; reset version to 1.40.1

## v1.40.2 (2026-03-30)

### Fix

- resolve command palette opening issue and F1 shortcut conflict
- add ESITO to Scarico TS, dynamic PDL filters and bot path fix

### Refactor

- QA cleanup main.py, splash_standalone and quality tools enforcement (ruff, mypy, refurb)
- optimize startup path, bot logic and GUI components

## v1.40.1 (2026-03-27)

### Fix

- **gui**: restore main branch sizing and fix all static analysis issues (ruff, mypy, refurb)
- **gui**: responsive startup sizing and tray icon type crash
- layout sidebar, startup sequence, menu routing and KPI charts crash
- resolve E402 and final startup tweaks

### Refactor

- **core,gui**: disaccoppiamento completo, DIP e ottimizzazione memoria

## v1.40.0 (2026-03-20)

### Feat

- **contabilita**: aggiunta opzione per esportare PDF certificati senza storico e fix robustezza

### Fix

- risoluzione bug critici e miglioramento integrità sistema

## v1.39.0 (2026-03-19)

## v1.38.0 (2026-03-19)

## v1.37.0 (2026-03-19)

### Fix

- risolto bug perdita dati in Certificati e migliorata qualità codice

## v1.36.0 (2026-03-18)

### Fix

- risolto problema avvio installer e riavvio post-aggiornamento

## v1.35.0 (2026-03-18)

## v1.34.0 (2026-03-18)

### Feat

- **splash**: implementazione animazioni high-tech avanzate
- **splash**: implementazione Zero-Stutter e look Enterprise finale
- **splash**: potenziamento log tecnici reali e fix import
- **setup**: permette all'utente di scegliere se avviare l'app dopo l'aggiornamento

### Fix

- **splash**: eliminati artefatti grafici negli angoli e rifinitura finale

### Perf

- **splash**: implementazione Zero-Stutter via processo standalone

## v1.33.1 (2026-03-17)

### Fix

- **sidebar**: risolte sovrapposizioni e artefatti grafici
- **sidebar**: ripristinato sfondo e ottimizzata fluidità animazione

### Refactor

- **sidebar**: pulizia codice e risoluzione segnalazioni linter

### Perf

- **sidebar**: ottimizzazione grafica aggressiva e rimozione ombre
- **sidebar**: eliminazione lag e ottimizzazione rendering
- **sidebar**: ottimizzazione reattività e fluidità animazioni

## v1.33.0 (2026-03-17)

### Feat

- **contabilita**: advanced certificate management with inline editing and professional PDF export

### Fix

- **certificati**: ordinamento globale ID-COEMI e fix troncamento PDF
- **certificati**: implementata dashboard riassuntiva e ordinamento naturale PDF
- **certificati**: forza larghezza colonne PDF con attributi HTML
- **certificati**: risolto wrap anomalo su colonne PDF
- **certificati**: migliora UI, export PDF e ordinamento colonne
- **core/gui**: persistent filters and duplicate removal for Certificati Campione
- **gui**: initialize footer_btns in SidebarWidget to resolve AttributeError
- **gui**: risolto AttributeError e ripristinata visibilità contenuti sidebar
- **gui**: ripristinata visibilità sidebar e ottimizzata fluidità animazione
- **gui**: corretto ordine chiamate animazione sidebar per evitare warning Qt
- **startup**: risolto freeze splash screen tramite caricamento differito e asincrono dei pannelli pesanti
- risolti errori critici di inizializzazione, NameError AuditManager e ImportError utils. Implementato sistema di cleanup processi stale per Selenium e riscrittura di sicurezza per conformita' Regola #1.
- **bot**: offload dell'importazione massiva storico OdA su ProcessPoolExecutor per evitare GIL freeze della GUI
- **gui**: rimozione type hint e migrazione completa asincrona pannelli per evitare freeze

### Refactor

- **core/gui**: code hardening via Ruff, Mypy and Refurb optimization

## v1.32.1 (2026-03-14)

### Refactor

- global timezone alignment (DTZ005) and general code quality cleanup

## v1.32.0 (2026-03-14)

### Feat

- migrazione del sistema di build da PyInstaller a Nuitka

### Fix

- sincronizzazione grafica status list con la pulizia tabella
- pulizia tabella asincrona per apertura browser immediata
- risolto crash QLocalSocket all'avvio e silenziati falsi positivi Vulture
- risoluzione bug runtime, ripristino moduli disconnessi e pulizia dead code

### Refactor

- rimozione integrale del sistema di intelligenza artificiale (Lyra)

### Perf

- rimosso il caricamento globale di pandas e matplotlib nei pannelli GUI per rendere istantaneo lo splash screen

## v1.31.3 (2026-03-13)

## v1.31.2 (2026-03-12)

## v1.31.1 (2026-03-12)

## v1.31.0 (2026-03-12)

### Feat

- **setup**: add EULA, UI flat design, Mica effect, and custom health check page

## v1.30.0 (2026-03-11)

### Feat

- implement resilient background auto-updater with inline UI progress

### Fix

- implement dynamic git binary detection in license generator
- smooth ETA calculation and format using EMA
- resolve QA warnings and refine UI styling

## v1.29.2 (2026-03-11)

## v1.29.1 (2026-03-10)

### Fix

- align HWID normalization and license key derivation between client and admin tool
- resolve startup crashes and standardize cryptographic key handling
- resolve duplicate Hot Reload notifications and implement toast spam filter
- resolve Chrome crash and implement mandatory cloud license enforcement
- restore automation tables, update ODA child view and background sync workflow
- architectural alignment V9.0, headless stability and core logic bugfixes

## v1.29.0 (2026-03-05)

### Feat

- **dashboard**: upgrade Don Ciro to v8.2 with anatomical fixes and spectacular UI
- **dashboard**: upgrade Don Ciro to v8.0 with AI State Machine and physics
- **dashboard**: implement hyper-realistic 3D procedural animation for Don Ciro

## v1.28.0 (2026-03-04)

### Feat

- **pdl**: integrate PDL database with automated printing bot

### Fix

- **config**: ensure account type persistence and global hot reload
- **config**: ensure account type persistence and extend global hot reload

## v1.27.0 (2026-03-04)

### Feat

- **gui**: add folder open functionality and force light mode in dialogs
- standardizzazione QToolTip (Light Mode) e logica freschezza dati specifica per Timbrature
- evoluzione Autopilot con stato database (SyncTracker) e trigger manuali da Dashboard
- input tempo ROI granulare (min/sec) e restyling layout WeatherWidget
- evoluzione ROI dinamico, nuovo tab impostazioni efficienza e compattazione layout dashboard
- evoluzione dashboard PDL con trend MTD/WoW e aree interattive
- standardizzazione UI light, ripristino PDL e classifica Top 3 bots

### Fix

- **gui**: correctly retrieve ComboBox values from table containers
- **gui**: clear default contracts on startup and improve general search
- **bot**: refine contract and oda field selectors for Dettagli OdA bot
- **gui**: global hot reload, enterprise light mode and contract persistence
- risoluzione errori static-analysis (ruff/mypy) e bug datetime-aware

## v1.26.2 (2026-03-02)

## v1.26.1 (2026-03-02)

## v1.26.0 (2026-03-02)

### Feat

- **pdl**: rifattorizzazione Scarico PDL (layout, esito read-only, fix avvio) e potenziamento card Efficienza

## v1.25.0 (2026-03-02)

### Feat

- **ui**: implementazione avanzata multi-window con custom title bar, pin-to-top, memory state e drag&drop
- **ui**: implementazione contestuale dello split button e dashboard card moduli esterni
- **ui**: restyling radicale placeholder popout con logo animato ad alta risoluzione e copywriting migliorato per codespell

### Fix

- **ui**: rimosso drag&drop da sidebar e ripristinato popout_manager nativo per risolvere crash C++ (Access Violation)
- **ui**: risolto AttributeError durante l'inizializzazione del componente toolbar e page_stack

## v1.24.0 (2026-03-01)

### Feat

- **ui**: centralizzazione split window nella TopBar e restyling professionale placeholder con logo SyncroJob. Uniformati tooltip globali in light mode alta visibilità. Fix crash importazioni e tipizzazione.
- **dashboard**: implementazione widget Meteo Cantiere e Bot ROI con fix stabilità e qualità
- **refactor**: scomposizione modulare core e UI con conformità V9.5
- **refactor**: modularizzazione ConfigManager e MainWindow con fix Storico OdA
- **refactor**: modularizzazione avanzata UI e risoluzione type warnings
- **gui**: implementazione navigazione a 3 livelli, ottimizzazione avvio e standardizzazione Consuntivo
- **contabilita**: implementazione Generatore Consuntivi con UI a card e automazione Macro VBA

### Refactor

- **contabilita**: modularizzazione suite consuntivi premium e ottimizzazione enterprise
- **contabilita**: separazione UI/Logica e implementazione Mappa Interattiva VBA con due Tab

## v1.22.2 (2026-02-27)

### Refactor

- code quality fixes (ruff, mypy, refurb)

## v1.22.1 (2026-02-27)

## v1.22.0 (2026-02-27)

### Feat

- **settings/quality**: implement Card Hub search, fix QPainter errors, and reach 99.7% docstring coverage

### Fix

- **gui**: ripristinato sfondo opaco originale della sidebar espansa
- **gui**: perfezionata sidebar fluttuante e allineamento logo
- **gui**: implementato sidebar come vero overlay fluttuante
- **gui**: risolto problema di rendering iniziale e layout pulsanti

### Refactor

- centralizzazione design system e rimozione totale stili hardcoded

## v1.21.2 (2026-02-26)

## v1.21.1 (2026-02-26)

## v1.21.0 (2026-02-26)

### Feat

- **ui**: implement premium snapshot animations and finalize project reorganization
- **gui**: refactor Mission Log Stream with multi-selection, improved copy, and Braille animations
- estensione standard Cyber-Stepper a tutti i bot
- implementazione standard Cyber-Stepper V2 e Terminal Log

### Fix

- **safework**: restore wait helpers and fix interactability on PDL search field
- risolto crash allo startup causato da regressioni nella sidebar e nel toast manager
- risolto problema timeline Scarico TS e rimosso bot duplicato

### Refactor

- **root**: reorganize project structure and cleanup dead code (Vulture audit)
- standardizzazione UI bot panels, widgets e componenti timeline
- risoluzione segnalazioni Ruff, Mypy e potenziamento documentazione (100% core/gui)
- consolidamento codebase e miglioramento documentazione componenti GUI e utility
- hardening del codice e miglioramenti all'analizzatore di dipendenze

## v1.20.0 (2026-02-19)

## v1.19.0 (2026-02-19)

## v1.18.0 (2026-02-19)

## v1.17.0 (2026-02-19)

## v1.16.0 (2026-02-19)

### Fix

- **core**: potenziamento migrazione dati e schema database da versioni legacy

## v1.15.1 (2026-02-18)

### Feat

- **tests**: blindatura suite bot e consolidamento unit test
- **core/safework**: blindatura totale automazione PDL e utility di parsing
- **pdl**: implement expandable rows and read-only tables

### Fix

- **safework**: stabilize PDL automation with proactive popup handling and silent browser logs
- remove selection borders, add focus highlight, exclusive cross-table selection

### Refactor

- rename Schedario database references to Report Attività in settings and UI

## v1.15.0 (2026-02-16)

## v1.14.0 (2026-02-16)

### Feat

- expand unit test suite and enhance Lyra panel with Ollama support
- redesign SafeWork programming tab with grouped tables and status bars
- implementation of massive SafeWork programming export and technical debt cleanup
- refactor SafeWork bot with account-specific login and improved Page Objects
- Add week selection (Current/Next) and modern header highlight to Programmazione
- Aggiunto widget MultiSelectFilter e aggiornato tab Programmazione PDL con fix pre-commit
- **safework**: integration of complex excel aggregation logic into ProgrammingSyncManager
- implementazione bot programmazione PDL e restyling UI
- **certificati**: add exclusion management and professional analysis dialog
- **apex**: enhance audit engine with modular targets and resilient toolbox

### Fix

- resolve all remaining mypy type errors in src
- resolve mypy type errors across the codebase
- ripristino file core e gui svuotati accidentalmente
- Resolve remaining asserts and type errors in bots/manager
- resolve linter and spelling issues (codespell)
- resolve critical test failures and boost coverage to 60%
- test discovery and pre-commit deptry hook

### Refactor

- **safework**: implementazione monitoraggio programmazione e architettura POM
- standardizzazione globale dei componenti GUI e della logica manager
- massive codebase cleanup and enterprise quality hardening
- use contextlib.suppress and improve code quality across codebase

## v1.13.2 (2026-02-05)

## v1.13.1 (2026-02-05)

## v1.13.0 (2026-02-05)

### Feat

- **apex**: upgrade audit engine to Apex Edition and modernize toolbox
- **oda**: enhance search to all columns and fix download path

## v1.12.4 (2026-02-02)

## v1.12.3 (2026-02-02)

### Fix

- **report**: improve Outlook integration and HTML fallback robustness
- **timbrature**: replace CTRL+A with robust backspace loop for date inputs

## v1.12.2 (2026-02-02)

## v1.12.1 (2026-02-02)

## v1.12.0 (2026-02-02)

### Feat

- **sync**: use smart upsert for PDL and Certificati + extensive unit test suite update
- **ui**: add Command Palette button + redesign Health panel
- **bug-reporter**: enterprise logging integration
- **logging**: Phase 4 Analytics + AlertManager + Health Panel
- **ui**: add highlighting for OdA status and stability fixes
- centralize bot automation in Monitoraggio and add sync tracking
- standardized update buttons for Dipendenti and PDL panels using specialized bots
- persistent sync tracking, Storico OdA bot integration, and intelligent diff logic
- Real-time status indicators for PDL bot, Storico OdA UI refactor, auto-refresh integration

### Fix

- **tests**: resolve robust test failures and optimize app initialization
- **types**: resolve final mypy errors in logger and health_panel
- **types**: resolve all remaining mypy errors in logging core
- **types**: resolve duplicates and import errors detected by mypy
- optimize vertical spacing in PDL and Storico OdA panels
- implement missing get_all_oda method in OdaManager
- correct credential retrieval in StoricoOdaPanel
- use SafeWork credentials and headless setting for Ricerca PDL bot

### Refactor

- deep modularization of core and gui monoblocks
- decompose AnagraficaPage into smaller components
- decompose AutopilotWidget into sub-components

## v1.11.0 (2026-01-30)

### Feat

- **pdl**: add global search and area/unit filters

### Fix

- **splash**: reduce log font size and margins to prevent truncation
- **splash**: remove ram/cpu resource monitor and fix log text wrapping
- **gui**: risolto crash all'avvio e refactoring modulo styles

### Refactor

- **gui**: scomposizione startup_dialog e separazione stili QSS

## v1.10.1 (2026-01-29)

## v1.10.0 (2026-01-29)

### Feat

- **gui**: implementazione refresh automatico e istantaneo dello stato Autopilot nel footer
- **gui**: implementazione switch account dal footer e fix aggiornamento status card
- **splash**: add real CPU monitor via GetProcessTimes
- **splash**: add live resource monitor and parallax drag effect

### Fix

- **gui**: optimize animations and resolve QPainter warnings
- **splash**: harden RAM monitor against ctypes crashes
- **splash**: use ctypes.c_size_t instead of wintypes.BASE_TSD_SIZE_T

### Perf

- **startup**: ultra-smooth startup with generator architecture and sprite rendering

## v1.9.0 (2026-01-28)

### Feat

- enhance splash screen with smooth 60fps animations and glowing borders
- stabilize spectacular splash screen architecture with synchronous UI yielding
- implement spectacular splash screen with particle background and glowing effects
- implement unified Zero-Lag startup with detailed splash screen logs and GUI preloading
- implement professional startup dialog and enhanced single-instance activation

## v1.8.11 (2026-01-28)

## v1.8.10 (2026-01-28)

## v1.8.9 (2026-01-28)

### Fix

- force include logging.handlers in build bundle

## v1.8.8 (2026-01-28)

## v1.8.7 (2026-01-28)

### Fix

- decouple netlify cloud build from local deploy cli

## v1.8.6 (2026-01-28)

### Fix

- improve netlify deploy command in build script

## v1.8.5 (2026-01-28)

## v1.8.4 (2026-01-28)

## v1.8.3 (2026-01-28)

## v1.8.2 (2026-01-28)

## v1.8.0 (2026-01-28)

### Feat

- **hr**: implement database-backed employee management and UI enhancements
- **report**: add advanced email report with Excel, trends and Autopilot scheduling
- **core**: enforce single instance and update dipendenti schema v3
- add bug reporting system and menu bar updates

### Fix

- **bots**: correct download path logic for Portale Fornitori bots
- **gui**: restore bug reporter, fix shortcuts and crash
- **bots**: resolve mypy type errors in wait_helpers.py
- **pdl**: ripristinato polling inline da main
- **tests**: handle both old and new unittest.mock call_args API for CI compatibility
- **tests**: deep debug CI failures - refactor test_init_driver to verify behavior not implementation
- **tests**: resolve all CI test failures - fix test_init_driver assertions and add TimelineWidget mocks
- restore missing scan_workload functionality in ExcelImporter
- restore visual validation for file paths in settings
- PyInstaller fitz import and license key fallback for frozen app

### Refactor

- **gui**: modularize Anagrafica page and enhance reporting logic
- **gui**: enhance Anagrafica dashboard and email reporting
- **quality**: fix linting and type errors
- **settings**: remove unused 'Cartella Export Consuntivi' path setting
- apply final quality fixes and code style improvements across the project
- fix linting and type checking errors in wait helpers and tests
- optimize scarico_ts bot timing and update test suites
- update main entry point and security utilities
- optimize core managers and improve bot logic
- cleanup temporary logs and update bot logic/tests
- broad update of GUI components, admin scripts and unit tests
- modularize MainWindow and TimbratureDBPanel components
- modularize TelegramService logic into handlers and UI components
- decompose ScaricoOreComponents into modular components
- decompose DipendentiPanel into modular package structure
- modularize excel importer logic into separate modules
- split SettingsPanel god file into modular components
- modularize gui panels and fix security vulnerabilities
- implement command palette and fix ruff linting issues

## v1.7.2 (2026-01-23)

## v1.7.1 (2026-01-23)

## v1.7.0 (2026-01-23)

### Feat

- **Settings/OdA**: add config Import/Export, Settings search and improve OdA history layout
- optimize dashboard layout, enhance PDL management, and proactive employee monitoring
- finalize toolbox with security audit, refurb, and project stats
- add engineering libraries (pydantic, tenacity, loguru, faker)
- enhance toolbox with db maintenance, radon metrics, and eradicate
- **ui**: implement rapid account switching and fix global tooltip rendering
- **data**: integrate Pandera validation for Excel and CSV imports
- **dx**: upgrade developer ecosystem with enterprise tools
- **gui**: implementazione audit model e miglioramento ordinamento/filtri tabelle
- **gui**: pannello dipendenti con monitoraggio scadenze abilitazioni ISAB
- **gui**: visualizzazione parallela task imminenti per sito nel footer
- **gui**: timer autopilot a 2 secondi e verifica associazioni portali
- ristrutturazione completa pagina Certificati Campione con logica intelligente
- add event-driven activity feed and autopilot widget
- add pulsing animation to the final startup toast
- add Storico OdA to Quick Actions configuration
- enhance search in Storico OdA to cover all fields
- toggle bold font on group expansion in StoricoOdaPanel
- enhance Storico OdA panel with numeric sorting, bold groups and extended description
- add Storico OdA GUI panel
- implement Storico OdA database and importer
- **ui**: fix calendar truncation, upgrade app icons to HQ design, and refactor icon generator location
- **ui**: overhaul dashboard with strict light theme, 3-level quick actions, and polished widgets

### Fix

- resolve pandas import error and complete employee/timbrature integration
- resolve startup crashes and apply refurb optimizations
- resolve pre-flight errors (security, linting, types)
- **bot**: fix start logic and database import for Ricerca PDL
- **dx**: resolve quality checks and update vulnerable dependencies
- **gui**: risolti errori ruff e migliorata logica countdown autopilot
- risolti errori QPainter e proprietà CSS non riconosciute, aggiunta icona check e migliorata resilienza importazione Excel
- center pulse animation in Toast
- import QVBoxLayout in toast.py
- ensure tree expand/collapse works on all columns
- resolve IndentationError in StoricoOdaPanel
- seamless text spanning and double-click toggle in StoricoOdaPanel
- resolve AttributeError for QStyle.StateFlag in StoricoOdaPanel
- prevent integer overflow and parsing errors in Storico OdA
- resolve IndentationError in StoricoOdaPanel
- enforce exact Excel match for Storico OdA import

### Refactor

- apply code quality fixes (lint, types, xenon)
- apply ruff/refurb modernization fixes
- modernize project structure, fix tests, and improve devops (Phase 4-5)
- **ui**: update notification manager, schemas, and main window widgets
- **gui**: spostamento countdown autopilot su status card imminente
- ottimizzazione UI, gestione servizi e aggiornamento report test (linting fix)
- upgrade StoricoOdaPanel to TreeView with Grouping

### Perf

- **data**: ultra-optimize Dataease import for maximum speed (5x faster)
- **gui**: ottimizzato timer footer a 5 secondi

## v1.5.0 (2026-01-18)

### Feat

- **bot**: add debug analysis for details window in Prenota BP
- **bot**: add material availability check in Prenota BP bot

## v1.1.0 (2026-01-14)

## v1.0.42 (2026-01-13)

## v1.0.41 (2026-01-13)

## v1.0.40 (2026-01-12)

## v1.0.39 (2026-01-12)

## v1.0.38 (2026-01-10)

### Feat

- **backup**: add UI and logic for restoring backups from cloud settings
- implement SafeWork PDL bot, settings and tests
- centralize statistics in config.json and remove obsolete files
- centralize all settings in config.json and SettingsPanel
- fix timbrature filters, improve DataEase UI, fix import ETA and consolidate config persistence
- implement ODC extraction from description, exclude 'Totale' rows from Giornaliere import, and fix year filtering logic
- **timbrature**: add Cantiere column, dynamic lists and empty data filter
- Implement Phase 3 UI/UX Design System
- Add GitHub Action to run tests
- decouple download paths and implement Elabora TS logic
- enhance contabilita selection summary and refactor elabora-ts logic
- enhance contabilita selection summary and refactor elabora-ts logic
- independent download paths and TS processing logic
- Optimize global ETA for multi-phase imports
- Add ETA tracking for Contabilità and Giornaliere imports
- Add ETA and progress tracking for Scarico Ore import
- Add global crash logging and native error popup
- **ai**: implement model fallback strategy for Lyra (2.0 -> 1.5)
- **ai**: add Lyra Sentinel and Contextual Analysis
- **ai**: enhance Lyra with deep context from Contabilita and Timbrature
- **core**: add Mission Control Dashboard and Lyra AI assistant
- **ui**: add toasts, shortcuts and date input improvements
- **ui**: add clear button to search inputs for better UX
- Setup, UI, Multi-Account, and Bot Logic Enhancements
- Setup, UI, Multi-Account, and Bot Logic Enhancements
- Setup, UI, Multi-Account, and Bot Logic Enhancements
- Setup, UI, Multi-Account, and Bot Logic Enhancements
- Setup, UI, Multi-Account, and Bot Logic Enhancements
- Setup, UI, Multi-Account, and Bot Logic Enhancements
- Setup, UI, Multi-Account, and Bot Logic Enhancements
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot
- Enable sequential row processing in Dettagli OdA bot

### Fix

- resolve all remaining test failures and enhance release scripts with progress feedback
- resolve remaining test failures and bot import bugs
- add missing time import in SafeworkBaseBot
- improve SafeWork loading synchronization
- robust print button click in SafeWork bot
- correct key for PDL number extraction in UI panel
- robust PDL key search logic
- resolve key mismatch for PDL number in SafeWork bot
- final path alignment in installer for absolute data safety
- ensure data persistence across upgrades by unifying app naming and securing AppData
- restore and migrate employee mappings to config.json
- exclude last row from Giornaliere import, remove 2026 ghost data, and update UI with light celeste headers and smaller row numbers
- **gui**: use valid variant for ModernButton in Timbrature panel
- **core**: remove missing 'calamine' engine dependency and improve error logging
- **core**: improve certificati campione import robustness
- Contabilità import resilience and Preventivi sheet detection
- Table UI visibility and Strumentale import logic
- Resolve SettingsPanel NameError, SecretsManager AttributeError, and License Path
- Resolve license path, text visibility in tables, and table height
- Resolve ModuleNotFoundError and complete Phase 3 UI/UX
- **ci**: Stabilizza la suite di test e corregge i fallimenti
- **ci**: Isola i test di TimbratureStorage e aggiorna .gitignore
- Ensure Setup filename uses correct version
- Silence noisy debug logs from 3rd party libs
- Redirect DB paths to user config dir and add crash logging
- **ai**: update Lyra fallback models to available versions

### Refactor

- final bot directory structure cleanup
- reorganize bots into portale_fornitori folder and fix imports
