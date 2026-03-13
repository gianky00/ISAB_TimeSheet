# 📋 TODO QUALITY - SyncroJob

Questo file tiene traccia dei debiti tecnici e dei miglioramenti necessari per mantenere il codice a standard di eccellenza (Senior Level).

## 🧩 Refactoring Architetturale (Violazioni SRP)
Le seguenti classi/file presentano responsabilità multiple mischiate (UI, Dati, API) e devono essere scomposte in componenti specializzati (Single Responsibility Principle):
- [ ] `src/gui/widgets/dashboard/don_ciro_widget.py`
- [ ] `src/gui/widgets/dashboard/weather_widget.py`
- [ ] `src/bots/base/base_bot.py`
- [ ] `src/gui/controllers/navigation_controller.py`
- [ ] `src/gui/panels/base.py` (Monitorare: ~400 LOC)
- [ ] `src/bots/safework/pdl/bot.py` (Monitorare: complessità logica)

## 🏗️ Refactoring Complessità (Xenon Grade C -> B)
Le seguenti funzioni/moduli hanno superato la soglia di complessità desiderata (B) e devono essere spezzettate:

### Bots
- [ ] `src/bots/portale_fornitori/prenota_bp/bot.py`: Metodo `run`
- [ ] `src/bots/portale_fornitori/scarico_ts/bot.py`: Metodo `_download_excel`
- [ ] `src/bots/portale_fornitori/scarico_ts/pages/scarico_ts_page.py`: Metodo `_download_excel`

### Core
- [ ] `src/core/audit/manager.py`: Metodi `_generate_notification` e `_get_current_user`
- [ ] `src/core/backup_manager.py`: Metodo `detect_cloud_paths`
- [ ] `src/core/data_synchronizer.py`: Metodi `sync_giornaliere` e `sync_contabilita_dati`
- [ ] `src/core/importers/`: Moduli e metodi complessi (es. `scan_workload` in `__init__.py`, `import_certificati_campione` in `certificati.py`)

### UI & Utils
- [ ] `src/gui/widgets/contabilita/helpers.py`: Intero modulo (media C)
- [ ] `src/utils/log_humanizer.py`: Intero modulo (media C)

## 🛡️ Sicurezza (Bandit)
- [ ] Valutare l'uso di un Query Builder o ORM leggero per `DataSynchronizer` per eliminare definitivamente gli avvisi B608 (SQL Injection) senza usare `# nosec`.

## 📖 Documentazione (Interrogate)
- [ ] Portare la copertura delle docstring dal attuale ~80% al 95%.

---
*Ultimo aggiornamento: 13 Marzo 2026*
