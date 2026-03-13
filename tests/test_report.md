# 📊 Test Execution Report

**Date:** 2026-03-13 07:56:54
**Duration:** 110.76s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1407 |
| ✅ Passed | 2 |
| ❌ Failed | 1 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/integration/test_safework_pdl_flow.py::TestSafeWorkPDLIntegration::test_full_pdl_flow_simulation`
**Error:** `FAILED tests/integration/test_safework_pdl_flow.py::TestSafeWorkPDLIntegration::test_full_pdl_flow_simulation`

**Timestamp:** `2026-03-13T07:56:54.445817`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\integration\test_safework_pdl_flow.py F                            [100%]

================================== FAILURES ===================================
__________ TestSafeWorkPDLIntegration.test_full_pdl_flow_simulation ___________
tests\integration\test_safework_pdl_flow.py:36: in test_full_pdl_flow_simulation
    assert success is True
E   assert False is True
---------------------------- Captured stdout call -----------------------------
[2026-03-13 07:56:34] INFO     - src.core.license_updater       - Verifica stato licenza cloud... | trace=trace_f7b59a... | span=span_7c8de10b
[2026-03-13 07:56:34] INFO     - src.core.license_updater       - Cartella licenza creata | trace=trace_f7b59a... | span=span_7c8de10b
[2026-03-13 07:56:37] ERROR    - src.core.license_validator     - Errore decifratura config.dat:  | trace=trace_f7b59a... | span=span_7c8de10b
[2026-03-13 07:56:37] INFO     - src.core.license_updater       - Rilevato aggiornamento o licenza locale non valida, download in corso... | trace=trace_f7b59a... | span=span_7c8de10b
[2026-03-13 07:56:38] INFO     - src.core.license_updater       - ✓ Aggiornamento completato | trace=trace_f7b59a... | span=span_7c8de10b
[2026-03-13 07:56:40] INFO     - bot.SafeWorkPDLBot             - ⚙️ Avvio scarico_pdl | Headless: False | Timeout: 30s | trace=trace_5655c9... | span=span_7c8de10b | bot=scarico_pdl | trace_id=trace_5655c9b4482f4349 | bot_type=scarico_pdl | bot_status=IDLE | current_step= | step_index=-1
[2026-03-13 07:56:40] ERROR    - bot.SafeWorkPDLBot             - ❌ Validazione fallita: Nessun numero PDL trovato nei dati. | trace=trace_5655c9... | span=span_7c8de10b | bot=scarico_pdl | trace_id=trace_5655c9b4482f4349 | bot_type=scarico_pdl | bot_status=IDLE | current_step= | step_index=-1
[2026-03-13 07:56:40] INFO     - bot.SafeWorkPDLBot             - 🏁 Stato finale: ERROR | trace=trace_5655c9... | span=span_7c8de10b | bot=scarico_pdl | trace_id=trace_5655c9b4482f4349 | bot_type=scarico_pdl | bot_status=ERROR | current_step= | step_index=-1
[2026-03-13 07:56:40] WARNING  - src.bots.base.base_bot.BaseBot.execute - Function execute completed | trace=trace_f7b59a... | span=span_7c8de10b | duration_ms=6526.38 | threshold_ms=5000 | threshold_exceeded=True
============================== warnings summary ===============================
.venv\Lib\site-packages\_hypothesis_pytestplugin.py:469
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_hypothesis_pytestplugin.py:469: UserWarning: Skipping collection of '.hypothesis' directory - this usually means you've explicitly set the `norecursedirs` pytest config option, replacing rather than extending the default ignores.
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      8    67%   126, 139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              340    196    42%   140-164, 199, 201, 223, 230, 250-252, 256, 260, 264, 268, 272-273, 277-278, 283-294, 298-338, 342-374, 378-397, 404-409, 413-424, 428-436, 453-459, 463-465, 482-506, 510-536, 540, 544-548, 552-557, 561-571, 575-583
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     42    31%   29, 34, 39, 60, 64, 76-88, 100-137
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     82    23%   30, 35, 40, 47, 51, 60-66, 72-79, 83-115, 119-136, 146-173, 177-185
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207    179    14%   32-35, 39, 43-45, 51-71, 75-88, 92-118, 122-127, 139-213, 217-228, 238-267, 271-280, 284-292, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     88    18%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    220    15%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 289-321, 327-358, 362-373, 377-394, 398-418, 422-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     69    25%   29, 34, 39, 44, 49, 56-60, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159    135    15%   36-40, 44, 48-56, 60-77, 81-140, 150-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    159    15%   46-47, 51-111, 115-116, 123-150, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     54    34%   41-45, 49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     55    19%   22-24, 30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     32    30%   25-27, 31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     45    29%   24-26, 30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    263    16%   55, 60, 71, 75, 80-81, 86, 90-163, 167-171, 175-210, 214-250, 254-287, 291-327, 331-391, 395-408, 412-417, 421-432, 436-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     88    21%   55-56, 61, 66, 71, 83-145, 149-156, 165-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            120     98    18%   22-24, 44, 57-137, 151-185, 190-203, 214-222
src\core\app_updater.py                                                  9      9     0%   7-34
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     83    18%   19, 23-67, 71, 75-82, 94-101, 128-173, 177-182, 194-200
src\core\audit\integrity.py                                             16      4    75%   16-17, 22, 27
src\core\audit\manager.py                                              140    107    24%   30, 34-37, 41-45, 50, 54, 58-67, 102-181, 187-204, 208-235, 239-240, 244, 248, 252-255, 264-292
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     18    28%   15-48
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73     73     0%   6-132
src\core\backup_manager.py                                             138    138     0%   6-250
src\core\bug_reporter.py                                               157    157     0%   11-339
src\core\config\account_manager.py                                      53     32    40%   29, 38, 47-57, 62-68, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     55    21%   23-31, 36-87, 95-109
src\core\config\security.py                                             40      7    82%   28, 32-33, 59, 63-65
src\core\config_manager.py                                             162     77    52%   48-49, 54, 74, 83, 103-109, 127-128, 143, 149, 154-156, 161, 173-175, 180-182, 187-191, 196-199, 211-213, 218-227, 232-243, 249-251, 256-282
src\core\constants.py                                                  125      0   100%
src\core\contabilita_manager.py                                        102    102     0%   6-225
src\core\contabilita_queries.py                                         87     87     0%   6-126
src\core\contabilita_search.py                                          92     92     0%   6-185
src\core\contabilita_stats.py                                           59     59     0%   6-101
src\core\contabilita_worker.py                                         102    102     0%   1-216
src\core\data_synchronizer.py                                           25      6    76%   27, 34, 41, 46, 53, 63
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123     78    37%   113-148, 154-184, 188-192, 195-199, 202, 210-229
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-21, 26-28, 33-39
src\core\database\migrations\pdl.py                                     34     27    21%   7-38, 43-91, 96-116, 121-125, 132-134
src\core\database\migrations\storico_oda.py                             11      8    27%   6-49, 56-58
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-32, 37-47, 52-69
src\core\database\pdl_queries.py                                        92     77    16%   23-37, 43-95, 100-136, 144-209
src\core\employees.py                                                   98     98     0%   1-196
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              60     37    38%   15-16, 24-26, 36-38, 43-59, 64-76, 81-88
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                                      181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189    153    19%   14-15, 22-24, 61-101, 120-138, 142-161, 175-206, 210-277, 281-290, 307-309, 313-337
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            192    100    48%   70-72, 86-113, 124-156, 161-163, 168-173, 187, 200-211, 214-215, 220-221, 259-270, 281-296, 306-308, 321-323
src\core\license_validator.py                                          176     57    68%   63-69, 86-115, 120-129, 148, 183, 195, 197, 203-204, 213-215, 233-236, 241, 245, 254-259, 273-276, 284-286, 289-290, 295-296, 301-302
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     11    81%   31-32, 36, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     33    55%   64, 66, 90-91, 105-115, 121, 167-201
src\core\logging\filters.py                                             60     29    52%   114, 117, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83     12    86%   84, 88-90, 125, 138, 164-165, 224, 230-240
src\core\logging\logger.py                                             116     29    75%   84, 96, 123, 135-141, 145-148, 156-157, 170-174, 182-183, 208, 214, 222, 230, 241, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     13    76%   58, 67, 100, 105, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    134    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 188, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163    163     0%   6-317
src\core\lyra_sentinel.py                                               30     30     0%   6-51
src\core\notification_manager.py                                       116    116     0%   8-243
src\core\oda_manager.py                                                 42     26    38%   29, 38-91, 98-112
src\core\preventivi_manager.py                                         196    196     0%   8-312
src\core\report_history.py                                              68     68     0%   7-158
src\core\schemas.py                                                     57      9    84%   71-73, 78-80, 85-87
src\core\secrets_manager.py                                            105     33    69%   32, 99, 104, 109, 115-116, 122, 130-135, 141, 149, 155, 160, 165-170, 175-180, 187-189, 194-197
src\core\stats_manager.py                                               49     49     0%   8-104
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23     14    39%   16-18, 23-28, 33-37
src\core\sync\contabilita_sync.py                                       70     56    20%   22-46, 53-88, 95-112, 117-127
src\core\sync\operazioni_sync.py                                        42     32    24%   22-43, 48-71
src\core\sync\smart_sync.py                                             25     18    28%   21-54
src\core\sync_tracker.py                                                59     33    44%   40-51, 56-60, 73-82, 95-98, 112-124
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     76     0%   6-118
src\core\telegram\bridge\intent_handler.py                              75     75     0%   6-125
src\core\telegram\bridge\system_handler.py                             103    103     0%   6-139
src\core\telegram\bridge\ui_commands.py                                104    104     0%   6-144
src\core\telegram\service.py                                           205    205     0%   1-314
src\core\telegram_bridge.py                                             69     69     0%   7-127
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                20      5    75%   32, 35-38, 57
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\updater\__init__.py                                             0      0   100%
src\core\updater\engine.py                                             163    163     0%   6-236
src\core\updater\gui.py                                                159    159     0%   6-243
src\core\version.py                                                      5      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     69     0%   1-137
src\gui\dialogs\audit_detail_dialog.py                                  61     61     0%   1-123
src\gui\dialogs\bug_report_dialog.py                                   228    228     0%   7-455
src\gui\dialogs\certificati_analysis_dialog.py                         201    201     0%   6-455
src\gui\dialogs\command_palette.py                                     298    298     0%   7-432
src\gui\dialogs\confirmation_dialog.py                                  97     97     0%   7-202
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     40     0%   1-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135    135     0%   1-248
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     71     0%   7-327
src\gui\main_window\components\status_bar.py                           132    132     0%   7-232
src\gui\main_window\components\tool_bar.py                              82     82     0%   7-187
src\gui\main_window\components\tray_icon.py                             17     17     0%   7-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    37     37     0%   6-89
src\gui\main_window\controllers\monitoring_controller.py                42     42     0%   6-73
src\gui\main_window\controllers\signal_connector.py                     19     19     0%   7-65
src\gui\main_window\controllers\workflow_controller.py                  71     71     0%   6-135
src\gui\main_window\main.py                                            257    257     0%   7-469
src\gui\main_window\page_index.py                                       28     28     0%   7-53
src\gui\panels\__init__.py                                              22     22     0%   6-28
src\gui\panels\base.py                                                 248    248     0%   6-479
src\gui\panels\carico_ts.py                                             96     96     0%   6-184
src\gui\panels\consuntivo_panel.py                                      46     46     0%   7-77
src\gui\panels\contabilita_kpi\__init__.py                               2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py                             14     14     0%   1-32
src\gui\panels\contabilita_kpi\charts.py                               213    213     0%   1-397
src\gui\panels\contabilita_kpi\kpi_panel.py                            161    161     0%   1-307
src\gui\panels\contabilita_panel.py                                    263    263     0%   8-427
src\gui\panels\dashboard_panel.py                                      130    130     0%   7-249
src\gui\panels\dettagli_oda.py                                         183    183     0%   8-326
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 28     28     0%   7-77
src\gui\panels\dipendenti\shared.py                                    152    152     0%   6-329
src\gui\panels\dipendenti_manager_panel.py                             206    206     0%   1-369
src\gui\panels\health_panel.py                                         275    275     0%   8-437
src\gui\panels\help_panel.py                                           139    139     0%   6-383
src\gui\panels\lyra\__init__.py                                          2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                                        72     72     0%   1-114
src\gui\panels\lyra\header.py                                           40     40     0%   1-80
src\gui\panels\lyra\input_bar.py                                        63     63     0%   1-123
src\gui\panels\lyra\lyra_panel.py                                      169    169     0%   1-274
src\gui\panels\lyra\workers.py                                          37     37     0%   1-67
src\gui\panels\notifications_panel.py                                  243    243     0%   7-406
src\gui\panels\pdl\__init__.py                                           2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                                      17     17     0%   1-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     80     0%   7-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    119     0%   1-186
src\gui\panels\pdl\pdl_panel.py                                        189    189     0%   7-324
src\gui\panels\pdl\programmazione_tab.py                               218    218     0%   6-341
src\gui\panels\prenota_bp.py                                           142    142     0%   8-271
src\gui\panels\ricerca_pdl.py                                          113    113     0%   6-214
src\gui\panels\scarico_ore_panel.py                                    131    131     0%   7-261
src\gui\panels\scarico_pdl.py                                          236    236     0%   7-455
src\gui\panels\scarico_ts.py                                           161    161     0%   6-312
src\gui\panels\storico_oda\__init__.py                                   2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                              43     43     0%   1-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     49     0%   1-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     62     0%   1-114
src\gui\panels\storico_oda\oda_panel.py                                155    155     0%   8-290
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     207    207     0%   1-358
src\gui\panels\timbrature_bot.py                                       111    111     0%   8-197
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              9      9     0%   9-198
src\gui\styles\notification_styles.py                                   10     10     0%   6-53
src\gui\styles\palette_helpers.py                                       10     10     0%   6-25
src\gui\styles\theme_manager.py                                         85     85     0%   6-175
src\gui\styles\widget_styles.py                                         36     36     0%   6-392
src\gui\toast.py                                                        46     46     0%   6-93
src\gui\widgets\__init__.py                                             19     19     0%   6-31
src\gui\widgets\activity_feed.py                                       138    138     0%   1-320
src\gui\widgets\animated_progress_bar.py                                79     79     0%   7-174
src\gui\widgets\audit_log_widget.py                                    120    120     0%   7-194
src\gui\widgets\automazioni_widget.py                                   59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                              143    143     0%   1-383
src\gui\widgets\autopilot\event_card.py                                131    131     0%   1-275
src\gui\widgets\autopilot\main_widget.py                               208    208     0%   7-394
src\gui\widgets\bot_parameters.py                                      222    222     0%   6-396
src\gui\widgets\calendar_date_edit.py                                   18     18     0%   6-77
src\gui\widgets\core_widgets.py                                        106    106     0%   8-389
src\gui\widgets\dashboard_stat_card.py                                  49     49     0%   6-111
src\gui\widgets\data_table.py                                          158    158     0%   6-363
src\gui\widgets\effects.py                                              43     43     0%   6-89
src\gui\widgets\empty_state.py                                          29     29     0%   6-63
src\gui\widgets\excel_table.py                                         263    263     0%   6-446
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   6-152
src\gui\widgets\footer\components.py                                    57     57     0%   6-166
src\gui\widgets\footer\manager.py                                       20     20     0%   6-68
src\gui\widgets\footer\status_bar.py                                    36     36     0%   6-75
src\gui\widgets\footer\telemetry.py                                     55     55     0%   6-87
src\gui\widgets\info_widgets.py                                         92     92     0%   6-178
src\gui\widgets\message_bubble.py                                       54     54     0%   7-140
src\gui\widgets\modern_button.py                                        67     67     0%   5-158
src\gui\widgets\modern_card.py                                          42     42     0%   6-86
src\gui\widgets\multi_select_filter.py                                  99     99     0%   6-168
src\gui\widgets\notification_card.py                                   116    116     0%   7-199
src\gui\widgets\notification_group_header.py                            48     48     0%   6-142
src\gui\widgets\notification_item.py                                    74     74     0%   1-142
src\gui\widgets\notification_toolbar.py                                131    131     0%   6-283
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     78     0%   1-361
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     30     0%   6-53
src\gui\widgets\sidebar_button.py                                       82     82     0%   6-139
src\gui\widgets\sidebar_widget.py                                      264    264     0%   7-451
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     47     0%   1-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60     60     0%   6-122
src\gui\widgets\status_indicator.py                                     46     46     0%   6-83
src\gui\widgets\timeline_widget.py                                     118    118     0%   7-197
src\gui\widgets\toast.py                                               158    158     0%   5-328
src\gui\widgets\update_banner.py                                        85     85     0%   1-153
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74     74     0%   6-234
src\utils\document_generator.py                                         18     18     0%   5-41
src\utils\document_processor.py                                         83     83     0%   6-111
src\utils\helpers.py                                                   112     91    19%   22-24, 29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 201-223, 233-254, 262-284
src\utils\log_humanizer.py                                              41     41     0%   7-95
src\utils\parsing.py                                                    51     51     0%   6-98
src\utils\printing.py                                                   90     73    19%   14-15, 24-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           59     59     0%   7-157
src\utils\secure_logger.py                                              23     10    57%   47-54, 57-60
src\utils\security.py                                                   79     24    70%   43-44, 80-82, 102, 104, 109-111, 116, 119-124, 128-134
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73     73     0%   7-270
--------------------------------------------------------------------------------------------------
TOTAL                                                                22365  19765    12%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/integration/test_safework_pdl_flow.py::TestSafeWorkPDLIntegration::test_full_pdl_flow_simulation
======================== 1 failed, 1 warning in 28.10s ========================

```
</details>

---
