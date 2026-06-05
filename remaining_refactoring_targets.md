# Piano di Refactoring Xenon - Ultimi Target

Questo documento traccia le rimanenti funzioni del codice che hanno un "Rank C" assegnato da Xenon a causa della loro elevata complessità ciclomatica, escludendo rigorosamente tutte le funzioni all'interno di `src/infrastructure/bots/` come richiesto.

## Obiettivo
Snellire questi blocchi (ad esempio, estraendo la logica in sotto-metodi) per portarli a Rank A o B, in modo da avere tutto il codice pulito.

## ⚙️ Application Services
- `src/application/services/dipendenti/data_helpers.py:29` -> `build_timbrature_maps`
- `src/application/services/mascot/don_ciro_engine.py:159` -> `_update_state_machine`
- `src/application/services/stats/roi_engine.py:124` -> `_process_audit_row`

## 🖥️ GUI (Interfaccia Grafica)
- `src/gui/dialogs/certificati_analysis_dialog.py:487` -> `_hide_excluded_items`
- `src/gui/main_window/controllers/monitoring_controller.py:44` -> `_show_toast_notification`
- `src/gui/workers/autopilot_cert_worker.py:19` -> `AutopilotCertWorker`
- `src/gui/workers/autopilot_cert_worker.py:24` -> `run`

---
*Nota: i moduli in `src/infrastructure/bots/` vengono volutamente saltati come da direttive.*
