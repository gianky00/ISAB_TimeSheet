# TODO QUALITY - SyncroJob

Questo file tiene traccia dei debiti tecnici e dei miglioramenti necessari per mantenere il codice a standard di eccellenza (Senior Level).

## Refactoring Architetturale (Violazioni SRP)
Le seguenti classi/file presentano responsabilità multiple mischiate (UI, Dati, API) e devono essere scomposte in componenti specializzati (Single Responsibility Principle):
- [x] `src/gui/widgets/dashboard/don_ciro_widget.py`
- [x] `src/gui/widgets/dashboard/weather_widget.py`
- [x] `src/bots/base/base_bot.py`
- [x] `src/gui/controllers/navigation_controller.py`
- [x] `src/gui/panels/base.py`
- [x] `src/bots/safework/pdl/bot.py`

## Refactoring Complessità (Xenon Grade C -> B)
Le seguenti funzioni/moduli hanno superato la soglia di complessità desiderata (B) e sono stati spezzettati:

### Bots
- [x] `src/bots/portale_fornitori/prenota_bp/bot.py`: Metodo `run` (Modularizzato V9.1)
- [x] `src/bots/portale_fornitori/scarico_ts/bot.py`: Metodo `_download_excel`
- [x] `src/bots/portale_fornitori/scarico_ts/pages/scarico_ts_page.py`: Metodo `_download_excel` (Modularizzato V9.1)

### Core
- [x] `src/core/audit/manager.py`: Metodi `_generate_notification` e `_get_current_user`
- [x] `src/core/backup_manager.py`: Metodo `detect_cloud_paths`
- [x] `src/core/data_synchronizer.py`: Metodi `sync_giornaliere` e `sync_contabilita_dati`
- [x] `src/core/importers/`: Moduli e metodi complessi (es. `_process_single_sheet` in `contabilita.py`)
- [x] `src/core/sync/smart_sync.py`: Metodi `sync_upsert_smart` e `sync_full_replace_with_metadata` (Refactored V9.1)
- [x] `src/core/dipendenti/anagrafica_controller.py`: Metodo `process_rows` (Refactored V9.1)

### UI & Utils
- [x] `src/gui/widgets/contabilita/helpers.py`: Intero modulo (media C)
- [x] `src/utils/log_humanizer.py`: Intero modulo (media C)
- [x] `src/gui/panels/dipendenti/utils/report_generator.py`: Hook UI integrato in `AnagraficaPage`.
- [x] `src/bots/base/wait_helpers.py`: Metodi `poll_for_new_file` e `poll_for_file` (Refactored V9.1 - Rank B)

## Sicurezza
- [x] Migrazione a `pip-audit` per scansione vulnerabilità (integrato in Toolbox GUI)
- [x] Parametrizzazione SQL in `SmartSyncEngine` (B608 risolto con prepared statements).

## Infrastruttura Test
- [x] Fix doppio conteggio passed/failed in fase isolamento SHOTGUN (V5.1)
- [x] Fix parsing incompleto summary pytest (failed+error)
- [x] SNIPER retry mirato con `--last-failed`
- [x] `sys.exit()` centralizzato, runner utilizzabile come libreria
- [x] Report IA troncato a 2000 char per file (-80% dimensione)
- [x] Suite test per il runner: 34 unit test di regressione
- [x] Allineamento a Poetry e script batch `avvio_test.bat`
- [x] Collection in-process con API pytest (`pytest.main()`) invece di subprocess

## Documentazione (Interrogate)
- [x] Portare la copertura delle docstring dal attuale ~80% al 95%. (Raggiunto 99.6% in V9.1)

## Static Analysis — Industrial Grade (completato 10 Maggio 2026)
- [x] **Ruff: 0 segnalazioni** sull'intera codebase (incluso `scratch/`).
- [x] **MyPy: 0 errori** su 406 file sorgente con strict mode.
- [x] Rimossi tutti i `# type: ignore` e `# mypy: disable-error-code` dall'intera codebase.
- [x] Rimossi override ridondanti in `pyproject.toml` per moduli non installati (`PyInstaller`, `win32api`, `faker`).
- [x] Import pesanti della GUI spostati nel blocco `TYPE_CHECKING` per ottimizzare i tempi di caricamento.

## Stabilità Startup
- [x] **Crash `access violation` al boot risolto (10 Maggio 2026).**
    - Root cause: `NotificationManager` e `AuditSignals` (QObject singletons) venivano istanziati nel `Phase1Worker` thread di background, causando un crash nativo C++ di PySide6 quando il thread terminava e i segnali venivano emessi dal loop `AuditManager`.
    - Fix: Pre-inizializzazione esplicita sul Main Thread in `main.py` prima di `_run_phase1`.

---

## Backlog Aperto (Prossime Sessioni)

| Priorità | Area | Descrizione |
|---|---|---|
| Media | Test | Aumentare la coverage dei test di regressione per i bot (target: >80%). |
| Media | GUI | Ridurre ulteriormente i `# noqa: PLR0913` rimasti (metodi con >5 argomenti). |
| Bassa | Docs | Mantenere aggiornato `.gemini/ARCHITECTURE.md` con le ultime modifiche architetturali. |
| Bassa | DevOps | Valutare l'aggiunta di un job CI/CD su GitHub Actions che esegua `ruff check` e `mypy src` ad ogni push. |

---
*Ultimo aggiornamento: 10 Maggio 2026 — Stato: INDUSTRIAL GRADE (Ruff 0 | MyPy 0)*
