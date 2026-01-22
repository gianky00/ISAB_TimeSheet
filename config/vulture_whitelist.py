# vulture_whitelist.py
# Whitelist per sopprimere i falsi positivi di vulture

# Qt Framework Overrides & Slots
closeEvent  # unused method (src/gui/main_window.py)
dropEvent  # unused method (src/gui/lyra_panel.py)
dragEnterEvent  # unused method (src/gui/lyra_panel.py)
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
get_exa_api_key  # unused method (src/core/secrets_manager.py)
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
