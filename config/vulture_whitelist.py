# vulture_whitelist.py
# Whitelist per sopprimere i falsi positivi di vulture

# Qt Framework Overrides & Slots
closeEvent  # unused method (src/gui/main_window.py)
paintEvent  # unused method (src/gui/widgets/status_indicator.py)
headerData  # unused method (src/gui/formatters.py)
contextMenuEvent  # unused method (src/gui/widgets/excel_table.py)

# Bot Interfaces (Plugin System)
get_name  # unused method (src/bots/...)
get_description  # unused method (src/bots/...)
get_columns  # unused method (src/bots/...)
set_telegram_service  # unused method (BaseBot)
navigate_to_menu  # unused method (BaseBot)
_handle_unsaved_changes_popup  # unused method (BaseBot)
_handle_session_popup  # unused method (BaseBot)
_handle_ok_popup  # unused method (BaseBot)
_logout  # unused method (BaseBot)

# Logic API (Public Interface preserved for future use/scripts)
add_account  # unused function (src/core/config_manager.py)
remove_account  # unused function (src/core/config_manager.py)
set_default_account  # unused function (src/core/config_manager.py)
run_retention_policy  # unused method (src/core/audit_manager.py)
validate_codice_fiscale  # unused method (src/utils/validators.py)
sanitize_sql_string  # unused method (src/utils/validators.py)
get_fornitori  # unused function (src/core/config_manager.py)
get_openai_key  # unused method (src/core/secrets_manager.py)
derive_key  # unused method (src/core/secrets_manager.py)

# Test Helpers & Debug
_reset_configuration_for_testing  # unused function (src/core/config_manager.py)

# Data Structures & Constants
LOGGING_IN  # unused variable (src/core/constants.py)
USER_AGENT  # unused variable (src/core/constants.py)
POPUP_ATTENTION_HEADER  # unused variable (src/bots/...)
POPUP_YES_BUTTON  # unused variable (src/bots/...)
BT_SI_SESSIONE_ATTIVA  # unused variable (src/bots/...)
GRID_CHECKER_ROWS  # unused variable (src/bots/...)
ROW_CHECKBOX  # unused variable (src/bots/...)
GRID_ROWS  # unused variable (src/bots/...)
HAS_OPENPYXL  # unused variable (src/core/excel_importer.py)
GRACE  # unused variable (src/core/license_validator.py)

# GUI Style & Attributes (Accessed dynamically or Qt Properties)
row_factory  # unused attribute
merged_pdf_path  # unused attribute
number_format  # unused attribute
last_mood  # unused attribute
xy  # unused attribute
primary_variant  # unused variable
secondary_variant  # unused variable
gutter  # unused variable
none  # unused variable
xl  # unused variable
xxl  # unused variable
full  # unused variable
h1  # unused variable
h2  # unused variable
h3  # unused variable
h4  # unused variable
body1  # unused variable
body2  # unused variable
overline  # unused variable
code  # unused variable
dwFlags  # unused attribute (src/core/license_validator.py)
_is_running  # unused attribute (src/gui/panels.py)
bot_stopped  # unused variable (src/gui/panels.py)
_current_search_terms  # unused attribute (src/gui/scarico_ore_components.py)
all_values  # unused attribute (src/gui/scarico_ore_components.py)
original_rows  # unused attribute (src/gui/scarico_ore_components.py)
raw_dates  # unused attribute (src/gui/scarico_ore_components.py)
prenota_panel  # unused attribute (src/gui/widgets/automazioni_widget.py)
texts  # unused variable (src/gui/contabilita_kpi_panel.py)
hoverOpacity  # unused variable (src/gui/widgets/modern_button.py)
pulseOpacity  # unused variable (src/gui/widgets/status_card.py)

# Specific Panel Logic / Helpers
_refresh_printers  # unused method (src/gui/panels.py)
_manage_list  # unused method (src/gui/panels.py)
_on_bot_finished  # unused method (src/gui/panels.py)
_reset_settings  # unused method (src/gui/settings_panel.py)
logout  # unused method (src/bots/.../dettagli_oda_page.py)
verifica_disponibilita_materiali  # unused method (src/bots/.../prenota_bp_page.py)
prenota_nuovo_bp  # unused method (src/bots/.../prenota_bp_page.py)
_espandi_parte_seconda  # unused method (src/bots/.../bot.py)
setup_app_style  # unused method (src/core/app_initializer.py)
increment_error  # unused method (src/core/stats_manager.py)
execute_query  # unused method (src/core/database.py)
_update_dest_width  # unused method (src/gui/widgets/bot_parameters.py)
getSelectedRows  # unused method (src/gui/widgets/data_table.py)
get_table_widget  # unused method (src/gui/widgets/data_table.py)
set_row_status  # unused method (src/gui/widgets/excel_table.py)
update_column_options  # unused method (src/gui/widgets/excel_table.py)
set_status  # unused method (src/gui/widgets/status_indicator.py)
append_log  # unused method (src/gui/widgets/timeline_widget.py)
toast_info  # unused function (src/gui/widgets/toast.py)
toast_success  # unused function (src/gui/widgets/toast.py)
toast_warning  # unused function (src/gui/widgets/toast.py)
toast_error  # unused function (src/gui/widgets/toast.py)
navigate_to_extended  # unused method (src/gui/controllers/navigation_controller.py)
navigate_to_dataease  # unused method (src/gui/controllers/navigation_controller.py)
_build_style_cache_only  # unused method (src/gui/scarico_ore_components.py)
strict  # unused variable (src/gui/panels/timbrature/components/detail_view.py)

# Accessibility Module (Future Use)
make_accessible  # unused function (src/gui/accessibility.py)
setup_tab_order  # unused function (src/gui/accessibility.py)
KeyboardShortcuts  # unused class (src/gui/accessibility.py)
setup  # unused method (src/gui/accessibility.py)

# Legacy / To Be Reviewed
check_grace_period  # unused function (src/core/license_updater.py)
is_running_from_source  # unused function (src/core/license_updater.py)
is_license_folder_empty  # unused function (src/core/license_updater.py)
verify_license  # unused function (src/core/license_validator.py)
get_license_expiry  # unused function (src/core/license_validator.py)
get_license_client  # unused function (src/core/license_validator.py)
import_to_db_static  # unused method (src/bots/portale_fornitori/timbrature/bot.py)
validate_date_italian  # unused method (src/utils/validators.py)
get_icon  # unused method (src/utils/resource_manager.py)
get_style  # unused method (src/utils/resource_manager.py)
get_temp_path  # unused method (src/utils/resource_manager.py)
total_prev  # unused variable (src/core/contabilita_stats.py)
count_total  # unused variable (src/core/contabilita_stats.py)
status_counts  # unused variable (src/core/contabilita_stats.py)
top_commesse  # unused variable (src/core/contabilita_stats.py)
IDX_MODELLO  # unused variable
IDX_MATRICOLA  # unused variable
IDX_RANGE  # unused variable
IDX_ERRORE  # unused variable
IDX_CERTIFICATO  # unused variable
IDX_EMISSIONE  # unused variable
IDX_ID  # unused variable
ToastOverlay  # unused class

# Phase 1 Modernization Audit (2026-01-22)
pulseScale  # unused variable (src/gui/widgets/priority_badge.py - Qt Property)
StatCard  # unused class (src/gui/widgets/simple_chart.py)
get_phase  # unused method (src/gui/widgets/footer_stats.py)
log_boot_message  # unused method (src/gui/widgets/footer_stats.py)
_copy_link  # unused method (src/gui/widgets/notification_card.py)
set_expanded  # unused method (src/gui/widgets/notification_group_header.py)
bulk_action_triggered  # unused variable (src/gui/widgets/notification_toolbar.py)
get_current_filter  # unused method (src/gui/widgets/notification_toolbar.py)
get_search_query  # unused method (src/gui/widgets/notification_toolbar.py)
get_sort_key  # unused method (src/gui/widgets/notification_toolbar.py)
category_color  # unused attribute (src/gui/widgets/timeline_widget.py)

# WIP / Planned Features (Vulture Audit 2026-02-26)
ProgrammingSyncManager  # unused class (src/core/importers/pdl_sync_manager.py)
TerminalLogWidget  # unused class (src/gui/components/terminal_log.py)
SecurityDashboard  # unused class (src/gui/widgets/security_dashboard.py)
StartupDialog  # unused class (src/gui/dialogs/startup_dialog.py)
ConnectionTestWorker  # unused class (src/gui/workers/connection_worker.py)
alert_appears_with_text  # unused class (src/bots/base/wait_helpers.py)
SamplingFilter  # unused class (src/core/logging/filters.py)

# Pandera Schemas & Fields (False Positives)
DipendenteSchema
GiornaliereSchema
ContabilitaSchema
id_risorsa
Cognome
Nome
Data_nascita
Badge
Data_assunzione
personale
descrizione
tcl
odc
pdl
inizio
fine
ore
n_prev
data_prev
mese
totale_prev
attivita
stato_attivita
tipologia
ore_sp
resa
annotazioni
indirizzo_consuntivo
nome_file
coerce
strict

# Logging Configuration (Future/External Config)
rotation_size
rotation_time
retention
errors_retention
compression
performance_threshold_ms
sampling_rate
console_level
file_level
errors_level
has_critical_issues
_json_file
_human_file
_errors_file

# Pytest Hooks & Test Helpers (Vulture False Positives)
pytest_sessionstart
pytest_configure
session
create_mock_html
_isolate_config
cleanup_widgets
BLUE
UNDERLINE
collected_count
sig
isolate
mock_font
mock_app_version
mock_update_url
mock_bot_deps
mock_login_page_cls
mock_ui_deps
mock_is_avail
mock_years
mock_scan
mock_exec
mock_get_text
mock_history
mock_from_local
mock_platform
mock_hwid
mock_no_migration
mock_ctx
mock_sys
mock_linux
mock_painter_cls
mock_printers
mock_click
mock_overlay
mock_wf
mock_layout
mock_validate
mock_scan_files
mock_scan_sheets

# COM Object Properties (win32com)
To
CC
Subject
HTMLBody

# UI Design System (Tokens in via di espansione/utilizzo)
xxs
xs
sm
md
lg

# Vulture Auto-Generated Whitelist
wait_for_overlay_to_disappear
wait_for_element_clickable
poll_for_file
_get_row_value
_ask_user
ScaricoTSPage
navigate_to_timesheet
setup_filters
search_and_download
_attendi_caricamento_sistema
get_rows
missing_pdls
_yield
get_alerts
initialize_core
init_generator
HIGH
list_backups
restore_backup
cleanup_old_reports
export_configuration
LICENSE_MANIFEST
EXTREME
DEFAULT_SITE
PROG_CC
get_employee_by_badge
updated_count
openpyxl_mod
xlCalculationAutomatic
Visible
DisplayAlerts
run_sync_macros
process_downloaded_report
ScreenUpdating
EnableEvents
check_emergency_grace_period
configure
alert_on_critical
examples
first_seen
last_seen
generated_at
has
get_full_metadata
enrich_entry
read_metrics
get_statistics
set_baseline
get_baseline
_std_logger
migrate_logging_call
set_operation_rate
add_trace_to_always_log
get_stats
close_all
get_bot_run_logs
write_daily_summary
read_daily_summary
contains_message
has_exception
get_level_stats
pin_notification
clear_cache
read_existing_data
get_history
Config
validate_dipendenti
active_count
closed_count
total_minutes_saved
merge_all_session_from_telegram
border_pulse
tabBar
ScaricoOreRow
register_root
get_root_nodes
dashboard_panel
consuntivo_panel
notifications_panel
family
line_height
Typography
mouseMoveEvent
_on_finished
get_result
set_column_alignment
get_raw_row
ResponsiveContainer
_console_anim
_telemetry_anim
handle_f5
tray_controller
finalize_init
get_rows_count
scroll_area_area
status_labels
update_buttons
_last_status_html
_get_subtab_style
deselected
remove_last_message
FilterState
priorities
date_range
show_read
show_unread
show_archived
search_query
sort_by
group_by
features
displayAlignment
textElideMode
get_glass_gradient
get_status_color
current_theme
_step_number
glowOpacity
reset_all
COL_DESC
filterAcceptsRow
DangerButton
GhostButton
refresh_requested
update_value
_apply_table_style
transition_to_operational
set_global_progress
show_loading
last_net
session_id
PriorityBadge
_drag_start_pos
_current_drag
animated
sidebar_width
get_opacity
ResourceMonitor
trigger_activity
_phase
StatisticsWidget
mood
create_pulse_animation
create_position_animation
cleanup_animation_safely
cleanup_effect_safely
create_animation_timer
delayed_call
staggered_fade_in
parse_date_flexible
parse_datetime_flexible
format_date_iso
calculate_days_diff
get_status_by_days
format_days_ago
get_date_range
format_datetime_for_filename
is_same_day
get_month_name_it
humanize
get_logs_dir
get_data_dir
