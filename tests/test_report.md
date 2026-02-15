# 📊 Test Execution Report

**Date:** 2026-02-15 15:53:51
**Duration:** 51.41s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 4 |
| ✅ Passed | 3 |
| ❌ Failed | 1 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_ai_sentinel_hardened.py::TestAISentinelHardened::test_document_processor_merge_logic`
**Error:** `FAILED tests/unit/test_ai_sentinel_hardened.py::TestAISentinelHardened::test_document_processor_merge_logic`

**Timestamp:** `2026-02-15T15:53:51.552356`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_ai_sentinel_hardened.py F                                [100%]

================================== FAILURES ===================================
_________ TestAISentinelHardened.test_document_processor_merge_logic __________
tests\unit\test_ai_sentinel_hardened.py:141: in test_document_processor_merge_logic
    assert success is True
E   assert False is True
------------------------------ Captured log call ------------------------------
WARNING  src.utils.document_processor:document_processor.py:95 File PDF non valido o senza pagine: C:\Users\gianc\AppData\Local\Temp\pytest-of-gianc\pytest-1810\test_document_processor_merge_0\p1.pdf
WARNING  src.utils.document_processor:document_processor.py:95 File PDF non valido o senza pagine: C:\Users\gianc\AppData\Local\Temp\pytest-of-gianc\pytest-1810\test_document_processor_merge_0\p2.pdf
ERROR    src.utils.document_processor:document_processor.py:106 Risultato del merge vuoto per C:\Users\gianc\AppData\Local\Temp\pytest-of-gianc\pytest-1810\test_document_processor_merge_0\merged.pdf
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      24     24     0%   6-162
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                267    267     0%   6-488
src\bots\base\login_page.py                               94     94     0%   6-154
src\bots\base\wait_helpers.py                            166    166     0%   14-473
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               82     82     0%   5-156
src\core\app_updater.py                                   48     48     0%   6-97
src\core\audit\__init__.py                                 3      3     0%   1-4
src\core\audit\database.py                               100    100     0%   1-164
src\core\audit\integrity.py                               16     16     0%   1-27
src\core\audit\manager.py                                140    140     0%   1-284
src\core\audit\models.py                                   9      9     0%   1-13
src\core\audit\signals.py                                 28     28     0%   1-41
src\core\audit_manager.py                                  5      5     0%   6-11
src\core\auth_monitor.py                                  72     72     0%   6-131
src\core\backup_manager.py                               138    138     0%   6-250
src\core\bug_reporter.py                                 157    157     0%   11-339
src\core\config_manager.py                               237    194    18%   35, 69, 77-92, 97-119, 124-125, 130-150, 155-172, 181-182, 190-202, 207-208, 213-234, 239-249, 254, 259-261, 266, 271-286, 291-304, 309-319, 328-355, 360-364, 369-371, 376-378, 383-392, 401-419, 427-468
src\core\constants.py                                    101    101     0%   6-141
src\core\contabilita_manager.py                          102     53    48%   30, 35, 40, 49-61, 78-125, 134-141, 150-155, 164-171, 176, 181, 186, 191, 196, 201, 210, 220, 225
src\core\contabilita_queries.py                           87     70    20%   19-30, 35-48, 53-78, 83-94, 99-110, 115-126
src\core\contabilita_search.py                            92     73    21%   26-82, 89-113, 118-127, 134-146, 155-167, 181-185
src\core\contabilita_stats.py                             59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                           102    102     0%   1-216
src\core\data_synchronizer.py                            159    132    17%   19-23, 28-31, 38-55, 60-70, 76-103, 109-147, 157-194, 202-237, 243, 253, 268-325
src\core\database\__init__.py                              3      0   100%
src\core\database\manager.py                             121     78    36%   111-146, 152-182, 186-190, 193-197, 200, 208-227
src\core\database\migrations\contabilita.py               23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                17     13    24%   6-21, 26-28, 33-39
src\core\database\migrations\pdl.py                       34     27    21%   7-38, 43-91, 96-116, 121-125, 132-134
src\core\database\migrations\storico_oda.py               11      8    27%   6-49, 56-58
src\core\database\migrations\timbrature.py                27     22    19%   6-25, 30-32, 37-47, 52-69
src\core\database\pdl_queries.py                          80     66    18%   22-36, 46-75, 81-135, 140-176
src\core\employees.py                                     98     98     0%   1-196
src\core\excel_importer.py                                 4      0   100%
src\core\importers\__init__.py                            44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                            67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                59     36    39%   15-16, 24-26, 36-38, 43-58, 63-75, 80-87
src\core\importers\certificati.py                        116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                        133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                        181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\pdl_sync_manager.py                   151    151     0%   6-225
src\core\importers\scarico_ore.py                        187    151    19%   14-15, 22-24, 51-89, 97-115, 119-136, 150-181, 185-252, 256-265, 282-284, 288-312
src\core\importers\storico_oda.py                         81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                              153    153     0%   6-290
src\core\license_validator.py                            180    180     0%   6-353
src\core\logging\__init__.py                              10     10     0%   6-37
src\core\logging\alert_manager.py                        115    115     0%   7-240
src\core\logging\analytics.py                            136    136     0%   7-343
src\core\logging\config.py                                36     36     0%   5-85
src\core\logging\context.py                               57     57     0%   5-161
src\core\logging\decorators.py                            66     66     0%   5-225
src\core\logging\filters.py                               60     60     0%   5-206
src\core\logging\formatters.py                            83     83     0%   5-240
src\core\logging\logger.py                               109    109     0%   5-298
src\core\logging\metadata.py                              86     86     0%   5-198
src\core\logging\metrics.py                               98     98     0%   5-297
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              54     54     0%   5-201
src\core\logging\sinks.py                                100    100     0%   5-236
src\core\logging\viewer.py                               175    175     0%   5-420
src\core\lyra_client.py                                  162    162     0%   6-316
src\core\lyra_sentinel.py                                 29      5    83%   44-48
src\core\notification_manager.py                         111    111     0%   6-215
src\core\oda_manager.py                                   34     34     0%   6-115
src\core\report_history.py                                67     67     0%   7-157
src\core\schemas.py                                       77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                               94     58    38%   31-49, 53-57, 61-71, 75-77, 81-85, 90, 95, 100-105, 110-115, 120-124, 129-132, 137-143
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\sync_tracker.py                                  58     58     0%   1-105
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             207    207     0%   1-321
src\core\telegram_bridge.py                              344    344     0%   1-485
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           98     98     0%   6-164
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         66     66     0%   1-126
src\gui\dialogs\audit_detail_dialog.py                    59     59     0%   1-120
src\gui\dialogs\bug_report_dialog.py                     229    229     0%   10-477
src\gui\dialogs\command_palette.py                       306    306     0%   1-521
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-126
src\gui\dialogs\quick_actions_config.py                   86     86     0%   1-214
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-80
src\gui\dialogs\startup_dialog.py                        232    232     0%   6-372
src\gui\formatters.py                                    131    131     0%   1-236
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                73     73     0%   1-329
src\gui\main_window\components\status_bar.py             157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                26     26     0%   1-41
src\gui\main_window\components\tray_icon.py               17     17     0%   1-38
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-41
src\gui\main_window\main.py                              287    287     0%   1-473
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   197    197     0%   6-388
src\gui\panels\carico_ts.py                               90     90     0%   6-180
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 200    200     0%   1-370
src\gui\panels\contabilita_kpi\kpi_panel.py              159    159     0%   1-298
src\gui\panels\contabilita_panel.py                      249    249     0%   6-413
src\gui\panels\dashboard_panel.py                        166    166     0%   1-292
src\gui\panels\dettagli_oda.py                           137    137     0%   6-233
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-62
src\gui\panels\dipendenti\shared.py                      151    151     0%   1-273
src\gui\panels\dipendenti_manager_panel.py               186    186     0%   1-340
src\gui\panels\health_panel.py                           291    291     0%   8-573
src\gui\panels\help_panel.py                             122    122     0%   6-365
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          42     42     0%   1-67
src\gui\panels\lyra\header.py                             38     38     0%   1-80
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        160    160     0%   1-247
src\gui\panels\lyra\workers.py                            37     37     0%   1-65
src\gui\panels\notifications_panel.py                    254    254     0%   6-446
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        17     17     0%   1-26
src\gui\panels\pdl\pdl_detail_view.py                     47     47     0%   1-70
src\gui\panels\pdl\pdl_filter_widget.py                   66     66     0%   1-110
src\gui\panels\pdl\pdl_panel.py                          365    365     0%   6-618
src\gui\panels\pdl\programmazione_tab.py                 533    533     0%   6-918
src\gui\panels\prenota_bp.py                             107    107     0%   6-187
src\gui\panels\ricerca_pdl.py                             86     86     0%   6-152
src\gui\panels\scarico_ore_panel.py                      336    336     0%   7-541
src\gui\panels\scarico_pdl.py                            301    301     0%   6-532
src\gui\panels\scarico_ts.py                             122    122     0%   6-211
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                42     42     0%   1-73
src\gui\panels\storico_oda\oda_detail_view.py             48     48     0%   1-72
src\gui\panels\storico_oda\oda_filter_widget.py           40     40     0%   1-77
src\gui\panels\storico_oda\oda_panel.py                  253    253     0%   6-463
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       173    173     0%   1-299
src\gui\panels\timbrature_bot.py                         116    116     0%   6-193
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-155
src\gui\styles\theme_manager.py                           67     67     0%   6-123
src\gui\styles\widget_styles.py                           35     35     0%   6-391
src\gui\toast.py                                          45     45     0%   6-91
src\gui\widgets\__init__.py                               13     13     0%   6-25
src\gui\widgets\activity_feed.py                         136    136     0%   1-314
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-150
src\gui\widgets\audit_log_widget.py                      104    104     0%   7-174
src\gui\widgets\automazioni_widget.py                     55     55     0%   1-132
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-383
src\gui\widgets\autopilot\event_card.py                   67     67     0%   1-165
src\gui\widgets\autopilot\main_widget.py                 204    204     0%   6-350
src\gui\widgets\bot_parameters.py                        108    108     0%   6-205
src\gui\widgets\calendar_date_edit.py                     17     17     0%   6-76
src\gui\widgets\data_table.py                            108    108     0%   5-214
src\gui\widgets\excel_table.py                           335    335     0%   6-549
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   88     88     0%   1-121
src\gui\widgets\footer\components.py                      55     55     0%   1-94
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-50
src\gui\widgets\footer\telemetry.py                       55     55     0%   1-69
src\gui\widgets\info_widgets.py                           90     90     0%   6-170
src\gui\widgets\message_bubble.py                         53     53     0%   7-123
src\gui\widgets\modern_button.py                          62     62     0%   5-149
src\gui\widgets\multi_select_filter.py                    97     97     0%   6-146
src\gui\widgets\notification_card.py                     240    240     0%   6-542
src\gui\widgets\notification_group_header.py              47     47     0%   6-145
src\gui\widgets\notification_item.py                      72     72     0%   1-134
src\gui\widgets\notification_toolbar.py                  104    104     0%   6-279
src\gui\widgets\priority_badge.py                         47     47     0%   6-110
src\gui\widgets\quick_actions.py                          77     77     0%   1-358
src\gui\widgets\security_dashboard.py                    154    154     0%   1-251
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        245    245     0%   1-435
src\gui\widgets\simple_chart.py                           66     66     0%   1-105
src\gui\widgets\sortable_table_item.py                    47     47     0%   1-93
src\gui\widgets\statistics_widget.py                     107    107     0%   1-220
src\gui\widgets\status_card.py                            60     60     0%   1-126
src\gui\widgets\status_indicator.py                       43     43     0%   6-69
src\gui\widgets\timeline_widget.py                       203    203     0%   6-314
src\gui\widgets\toast.py                                 131    131     0%   5-255
src\gui\widgets\update_banner.py                          35     35     0%   1-49
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-295
src\utils\date_utils.py                                   70     70     0%   6-228
src\utils\document_generator.py                           17     17     0%   5-39
src\utils\document_processor.py                           83     34    59%   14-15, 24-32, 38, 50-51, 59, 63-64, 71-72, 78-79, 81-82, 86-87, 97-100, 103-104, 109-111
src\utils\helpers.py                                      91     71    22%   23-25, 30-34, 48-70, 83-85, 90, 117-118, 123, 136-151, 165-167, 182-188, 202-224, 232-250
src\utils\log_humanizer.py                                42     42     0%   6-119
src\utils\parsing.py                                      54     46    15%   14-34, 40-52, 57-67, 72-80, 85-98, 103-120
src\utils\printing.py                                     86     86     0%   1-144
src\utils\resource_manager.py                             56     56     0%   6-91
src\utils\secure_logger.py                                23     23     0%   5-70
src\utils\security.py                                     79     79     0%   6-141
src\utils\system_telemetry.py                             26     26     0%   6-74
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  18358  17683     4%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_ai_sentinel_hardened.py::TestAISentinelHardened::test_document_processor_merge_logic
============================== 1 failed in 6.51s ==============================

```
</details>

---
