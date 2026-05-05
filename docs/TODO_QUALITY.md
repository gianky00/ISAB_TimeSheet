# 📋 TODO QUALITY - SyncroJob

Questo file tiene traccia dei debiti tecnici e dei miglioramenti necessari per mantenere il codice a standard di eccellenza (Senior Level).

## 🧩 Refactoring Architetturale (Violazioni SRP)
Le seguenti classi/file presentano responsabilità multiple mischiate (UI, Dati, API) e devono essere scomposte in componenti specializzati (Single Responsibility Principle):
- [x] `src/gui/widgets/dashboard/don_ciro_widget.py`
- [x] `src/gui/widgets/dashboard/weather_widget.py`
- [x] `src/bots/base/base_bot.py`
- [x] `src/gui/controllers/navigation_controller.py`
- [x] `src/gui/panels/base.py`
- [x] `src/bots/safework/pdl/bot.py`

## 🏗️ Refactoring Complessità (Xenon Grade C -> B)
Le seguenti funzioni/moduli hanno superato la soglia di complessità desiderata (B) e devono essere spezzettate:

### Bots
- [ ] `src/bots/portale_fornitori/prenota_bp/bot.py`: Metodo `run`
- [ ] `src/bots/portale_fornitori/scarico_ts/bot.py`: Metodo `_download_excel`
- [ ] `src/bots/portale_fornitori/scarico_ts/pages/scarico_ts_page.py`: Metodo `_download_excel`

### Core
- [x] `src/core/audit/manager.py`: Metodi `_generate_notification` e `_get_current_user`
- [ ] `src/core/backup_manager.py`: Metodo `detect_cloud_paths`
- [x] `src/core/data_synchronizer.py`: Metodi `sync_giornaliere` e `sync_contabilita_dati`
- [ ] `src/core/importers/`: Moduli e metodi complessi (es. `scan_workload` in `__init__.py`, `import_certificati_campione` in `certificati.py`)

### UI & Utils
- [x] `src/gui/widgets/contabilita/helpers.py`: Intero modulo (media C)
- [x] `src/utils/log_humanizer.py`: Intero modulo (media C)

## 🛡️ Sicurezza
- [x] Migrazione a `pip-audit` per scansione vulnerabilità (integrato in Toolbox GUI)
- [ ] Valutare l'uso di un Query Builder o ORM leggero per `DataSynchronizer` per eliminare definitivamente gli avvisi B608 (SQL Injection).

## 🧪 Infrastruttura Test
- [x] Fix doppio conteggio passed/failed in fase isolamento SHOTGUN (V5.1)
- [x] Fix parsing incompleto summary pytest (failed+error)
- [x] SNIPER retry mirato con `--last-failed`
- [x] `sys.exit()` centralizzato, runner utilizzabile come libreria
- [x] Report IA troncato a 2000 char per file (-80% dimensione)
- [x] Suite test per il runner: 34 unit test di regressione
- [x] Allineamento a Poetry e script batch `avvio_test.bat`
- [ ] Valutare sostituzione parallelismo custom con `pytest-xdist` (work-stealing nativo)
- [ ] Collection in-process con API pytest (`pytest.main()`) invece di subprocess

## 📖 Documentazione (Interrogate)
- [ ] Portare la copertura delle docstring dal attuale ~80% al 95%.

---
*Ultimo aggiornamento: 24 Aprile 2026*
