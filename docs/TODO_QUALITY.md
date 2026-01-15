# 📋 TODO QUALITY - SyncroJob

Questo file tiene traccia dei debiti tecnici e dei miglioramenti necessari per mantenere il codice a standard di eccellenza (Senior Level).

## 🏗️ Refactoring Complessità (Xenon Grade C -> B)
Le seguenti funzioni/moduli hanno superato la soglia di complessità desiderata (B) e devono essere spezzettate:

### Bots
- [ ] `src/bots/portale_fornitori/prenota_bp/bot.py`: Metodo `run`
- [ ] `src/bots/portale_fornitori/scarico_ts/bot.py`: Metodo `_download_excel`
- [ ] `src/bots/portale_fornitori/scarico_ts/pages/scarico_ts_page.py`: Metodo `_download_excel`

### Core
- [ ] `src/core/audit_manager.py`: Metodi `_generate_notification_if_needed` e `_get_current_user`
- [ ] `src/core/backup_manager.py`: Metodo `detect_cloud_paths`
- [ ] `src/core/data_synchronizer.py`: Metodi `sync_giornaliere`, `sync_contabilita_dati`, `_sync_generic`
- [ ] `src/core/excel_importer.py`: Metodi `scan_workload`, `import_certificati_campione`, `_get_cell_style`

### UI & Utils
- [ ] `src/gui/widgets/contabilita/helpers.py`: Intero modulo (media C)
- [ ] `src/utils/log_humanizer.py`: Intero modulo (media C)

## 🛡️ Sicurezza (Bandit)
- [ ] Valutare l'uso di un Query Builder o ORM leggero per `DataSynchronizer` per eliminare definitivamente gli avvisi B608 (SQL Injection) senza usare `# nosec`.

## 📖 Documentazione (Interrogate)
- [ ] Portare la copertura delle docstring dal attuale ~80% al 95%.

---
*Ultimo aggiornamento: 15 Gennaio 2026*
