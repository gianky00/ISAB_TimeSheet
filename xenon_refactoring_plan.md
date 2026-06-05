# Piano di Refactoring Xenon (Riduzione Complessità Ciclomatica)

Questo documento traccia tutte le funzioni del codice che hanno un "Rank C" assegnato da Xenon a causa della loro elevata complessità ciclomatica.
Le funzioni relative ai bot (`src/infrastructure/bots/`) sono state intenzionalmente escluse da questo piano.

**Obiettivo:** Snellire questi blocchi suddividendoli in sotto-metodi più piccoli o utilizzando dizionari di mappatura, in modo da portare la complessità a Rank A o B.

## 📡 API (Telegram)
- `src/api/telegram/bridge/data_processor.py:58` -> `process_bp_items`
- `src/api/telegram/bridge/intent_handler.py:37` -> `handle_intent`
- `src/api/telegram/bridge/intent_handler.py:59` -> `_process_intent_data`
- `src/api/telegram/handlers/callbacks.py:336` -> `_handle_utility_actions`
- `src/api/telegram/handlers/messages.py:65` -> `_handle_sequential_input`

## ⚙️ Application Services
- `src/application/services/auth_monitor.py:65` -> `_process_employee_match`
- `src/application/services/config_manager.py:177` -> `_atomic_write_json`
- `src/application/services/license_updater.py:180` -> `run_update`
- `src/application/services/preventivi_manager.py:164` -> `read_existing_data`
- `src/application/services/report_service.py:104` -> `_build_access_maps`
- `src/application/services/audit/database.py:120` -> `fetch_filtered`
- `src/application/services/config/migration.py:40` -> `check_and_migrate_local_config`
- `src/application/services/contabilita/certificati_engine.py:514` -> `prepare_groups_with_priority`
- `src/application/services/database/repositories/contabilita_repository.py:182` -> `get_certificati_campione`
- `src/application/services/database/repositories/pdl_repository.py:44` -> `get_filtered`
- `src/application/services/dipendenti/data_helpers.py:17` -> `build_timbrature_maps`
- `src/application/services/dipendenti/report_service.py:84` -> `build_report_html`
- `src/application/services/importers/pdl_sync_manager.py:158` -> `_analyze_downloaded_file`
- `src/application/services/logging/formatters.py:104` -> `_generate_tags`
- `src/application/services/logging/formatters.py:161` -> `format`
- `src/application/services/mascot/don_ciro_engine.py:136` -> `update_physics`
- `src/application/services/processing/certificati/steps.py:186` -> `_build_rename_map`
- `src/application/services/processing/employees/import_steps.py:12` -> `EmployeeCsvReadStep`
- `src/application/services/processing/giornaliere/steps.py:49` -> `NormalizeGiornalieraStep`
- `src/application/services/processing/scarico_ore/steps.py:197` -> `_extract_row_styles`
- `src/application/services/stats/pdl_stats_engine.py:121` -> `_process_pdl_rows`
- `src/application\services/stats/roi_engine.py:97` -> `_process_audit_row`
- `src/application/services/updater/engine.py:87` -> `_run_network_copy`

## 🖥️ GUI (Interfaccia Grafica)
### Componenti & Dialog
- `src/gui/components/activity_timeline.py:213` -> `on_step_changed`
- `src/gui/components/scarico_ore/filter_worker.py:46` -> `run`
- `src/gui/dialogs/certificati_analysis_dialog.py:487` -> `_generate_audit_pdf`
- `src/gui/dialogs/certificati_analysis_dialog.py:550` -> `_capture_widgets_as_images`
- `src/gui/dialogs/guasto_dialog.py:59` -> `_setup_ui`
- `src/gui/dialogs/startup_dialog.py:363` -> `_get_build_date`

### Main Window & Controllers
- `src/gui/controllers/navigation_controller.py:100` -> `navigate_to`
- `src/gui/main_window/components/status_bar.py:200` -> `update_autopilot_ui`
- `src/gui/main_window/controllers/monitoring_controller.py:40` -> `check_isab_authorizations`

### Modelli e Workers
- `src/gui/models/audit_model.py:121` -> `_get_display_data`
- `src/gui/workers/autopilot_cert_worker.py:19` -> `AutopilotCertWorker`
- `src/gui/workers/autopilot_cert_worker.py:24` -> `run`

### Panels
- `src/gui/panels/changelog_panel.py:939` -> `_on_changelog_ready`
- `src/gui/panels/changelog_panel.py:236` -> `_setup_header`
- `src/gui/panels/contabilita_panel.py:323` -> `refresh_tabs`
- `src/gui/panels/dashboard_panel.py:221` -> `_handle_quick_action`
- `src/gui/panels/dashboard_panel.py:102` -> `refresh_live_data`
- `src/gui/panels/notifications_panel.py:272` -> `_get_filtered_sorted_notifications`
- `src/gui/panels/pdl/pdl_detail_view.py:95` -> `update_details`
- `src/gui/panels/pdl/programmazione_tab.py:184` -> `_update_tables`
- `src/gui/panels/timbrature/components/detail_view.py:73` -> `display_data`

### Widgets
- `src/gui/widgets/activity_feed.py:254` -> `refresh_feed`
- `src/gui/widgets/toast.py:245` -> `show`
- `src/gui/widgets/contabilita/certificati_tab.py:534` -> `_add_parent_context_actions`
- `src/gui/widgets/contabilita/certificati_tab.py:364` -> `_create_parent_item`
- `src/gui/widgets/dashboard/roi_widget.py:312` -> `_update_ui`
- `src/gui/widgets/dashboard/weather_widget.py:1001` -> `_determine_weather_style`
- `src/gui/widgets/sidebar/components.py:186` -> `set_collapsed`

## 🛠️ Infrastructure (Utils)
- `src/infrastructure/utils/printing.py:69` -> `print_pdf`
