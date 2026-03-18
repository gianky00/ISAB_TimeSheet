# 📊 Test Execution Report

**Date:** 2026-03-18 11:59:55
**Duration:** 254.69s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1320 |
| ✅ Passed | 623 |
| ❌ Failed | 9 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_contabilita_queries_coverage.py::TestContabilitaQueriesCoverage::test_get_data_by_year_columns_alignment`
**Error:** `Timeout`

**Timestamp:** `2026-03-18T11:00:40.161455`

<details><summary>Full Output</summary>

```text
Execution Timed Out
```
</details>

---
### `tests/unit/test_dettagli_oda_comprehensive.py::TestDettagliOdaComprehensive::test_page_setup_supplier_success`
**Error:** `FAILED tests/unit/test_dettagli_oda_comprehensive.py::TestDettagliOdaComprehensive::test_page_setup_supplier_success`

**Timestamp:** `2026-03-18T11:18:09.990148`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_dettagli_oda_comprehensive.py F                          [100%]

================================== FAILURES ===================================
________ TestDettagliOdaComprehensive.test_page_setup_supplier_success ________
tests\unit\test_dettagli_oda_comprehensive.py:99: in test_page_setup_supplier_success
    assert res is True
E   assert False is True
---------------------------- Captured stdout call -----------------------------
Selezione fornitore: COEMI
✗ Selezione fornitore fallita: Message: 

=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      8    67%   126, 139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              338    202    40%   142-145, 158, 163, 178, 183-188, 197-201, 222, 249-251, 255, 259, 263, 267, 271-272, 277, 282-297, 301-341, 345-371, 375-394, 401-406, 410-421, 425-433, 441-503, 507-533, 537, 541-545, 549-554, 558-568, 572-580
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                           99     84    15%   50-55, 74-78, 109-172, 195-252
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     42    31%   29, 34, 39, 60, 64, 76-88, 100-137
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     28    74%   30, 35, 40, 51, 76, 79, 92, 111, 120-123, 128-130, 134, 153-155, 160-162, 170-172, 174, 192-194
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207    162    22%   43-45, 51-71, 78-85, 92-118, 139-213, 217-228, 238-267, 271-280, 284-292, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     88    18%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    220    15%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 289-321, 327-358, 362-373, 377-394, 398-418, 422-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     69    25%   29, 34, 39, 44, 49, 56-60, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         157    133    15%   36-40, 44, 48-56, 60-77, 81-140, 150-203, 208-232, 241-252, 257-292
src\bots\portale_fornitori\timbrature\storage.py                       166    141    15%   46, 54-81, 87-116, 135-146, 156-163, 166-194, 201-237, 247-262, 267-308, 311-348, 352-367, 374-375
src\bots\safework\base.py                                               82     59    28%   33-37, 41-45, 49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     55    19%   22-24, 30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     32    30%   25-27, 31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     45    29%   24-26, 30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    276    12%   48-50, 55, 60, 65, 69-86, 90-163, 167-171, 175-210, 214-250, 254-287, 291-327, 331-391, 395-408, 412-417, 421-432, 436-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     88    21%   55-56, 61, 66, 71, 83-145, 149-156, 165-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            149    149     0%   10-263
src\core\app_updater.py                                                  9      9     0%   7-35
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     39    61%   62-64, 81-82, 136-138, 140-143, 145-148, 150-152, 154-158, 171-172, 177-182, 194-200
src\core\audit\integrity.py                                             16      2    88%   22, 27
src\core\audit\manager.py                                              162     74    54%   34, 46, 63, 67-69, 74, 78, 86-91, 213, 217-220, 226-243, 247-274, 287, 291-294, 303-331
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138    138     0%   6-250
src\core\bug_reporter.py                                               157    157     0%   11-339
src\core\config\account_manager.py                                      53     25    53%   29, 34, 51, 58-64, 71-91
src\core\config\defaults.py                                              3      0   100%
src\core\config\migration.py                                            69     54    22%   23-30, 35-86, 94-108
src\core\config\security.py                                             44     18    59%   23-43, 65, 68, 78
src\core\config_manager.py                                             164     71    57%   48-49, 54, 74, 83, 93-94, 103-109, 127-128, 143, 188-190, 195-199, 206, 212-214, 219-221, 226-235, 240-251, 257-259, 264-290
src\core\constants.py                                                  125      0   100%
src\core\contabilita\certificati_engine.py                              91     69    24%   22-23, 27-34, 38-50, 58-79, 84-94, 99-109, 114-132, 137-138
src\core\contabilita\scarico_ore\controller.py                          53     34    36%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        115     62    46%   33, 38, 43, 52-64, 81-128, 137-144, 153-158, 167-174, 179, 184, 189, 194, 199, 204-213, 218, 227, 237, 242
src\core\contabilita_queries.py                                         82     39    52%   21-29, 35, 45-46, 52, 74-75, 80-90, 95-107, 113, 121-122
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   183, 188, 202-203, 231-233
src\core\database\migrations\contabilita.py                             34      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     34      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\database\pdl_queries.py                                        92     77    16%   23-37, 43-95, 100-136, 144-209
src\core\dipendenti\anagrafica_controller.py                            88     72    18%   27-40, 47-96, 101-139, 144-149
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              60     37    38%   15-16, 24-26, 36-38, 43-59, 64-76, 81-88
src\core\importers\certificati.py                                      126    101    20%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-200
src\core\importers\contabilita.py                                      133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                                      181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189    153    19%   14-15, 22-24, 61-101, 120-138, 142-161, 175-206, 210-277, 281-290, 307-309, 313-337
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            192    192     0%   7-323
src\core\license_validator.py                                          176    176     0%   8-302
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              37      2    95%   71-73
src\core\logging\context.py                                             57     24    58%   31-32, 40-41, 45-46, 54, 81-98, 118, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     50    32%   63-115, 121, 167-201
src\core\logging\filters.py                                             60     29    52%   114, 117, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83     23    72%   84, 88-90, 122, 125, 130, 138, 164-165, 205-215, 224, 230-240
src\core\logging\logger.py                                             116     36    69%   84, 96, 123, 135-141, 145-148, 156-157, 170-174, 178-183, 188-189, 208, 214, 222, 226, 230, 241, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             74     51    31%   23-26, 30, 46-50, 59-60, 77-111, 129-131, 134-136, 153-163, 175-182, 201, 213, 219
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     16    70%   58, 67, 91, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     76    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 218-220, 226-228, 234-236
src\core\logging\viewer.py                                             177    144    19%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-138, 142-143, 147-148, 152-153, 162-176, 185-193, 204, 216-222, 226-230, 234-248, 252-267, 271-273, 277-313, 317-333, 352, 357, 362
src\core\notification_manager.py                                       116     80    31%   53-57, 61-65, 69-77, 81-93, 97-101, 133-167, 179-181, 190, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-108
src\core\oda_manager.py                                                 42     26    38%   29, 38-91, 98-112
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68     44    35%   27-29, 37-43, 48-52, 63-87, 97, 115-135, 148-158
src\core\schemas.py                                                     57      9    84%   71-73, 78-80, 85-87
src\core\secrets_manager.py                                            105     57    46%   30-77, 85-89, 97-116, 120-123, 127-136, 140-142, 146-150, 168-169, 176-179, 184-188, 195-196, 201-207
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               70     14    80%   49-53, 55-57, 68, 74-76, 95, 97, 113
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                77     47    39%   40-51, 56-60, 73-86, 91-102, 107-119, 132-135, 149-161
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     76     0%   6-118
src\core\telegram\bridge\intent_handler.py                              75     75     0%   6-125
src\core\telegram\bridge\system_handler.py                             103    103     0%   6-139
src\core\telegram\bridge\ui_commands.py                                104    104     0%   6-144
src\core\telegram\service.py                                           205    205     0%   1-314
src\core\telegram_bridge.py                                             34     34     0%   7-84
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\updater\__init__.py                                             0      0   100%
src\core\updater\engine.py                                             165    165     0%   6-249
src\core\updater\gui.py                                                163    163     0%   6-273
src\core\version.py                                                      5      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174    145    17%   47-50, 66-107, 111-124, 133-134, 143-145, 149, 153-154, 160-165, 169, 173-174, 185-186, 199-219, 228-282, 292-304, 318-331, 344-394, 403-404
src\gui\components\animated_stack.py                                    85     76    11%   32-46, 56-130, 134-141, 145-148
src\gui\components\animated_tab_widget.py                              147    119    19%   36-95, 99-106, 115-134, 147-149, 158-164, 168-175, 184-190, 199-212, 216-230, 234-235, 239, 243, 252-254, 258, 262, 266, 270, 274, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                107     90    16%   28-34, 38-86, 91-107, 110-122, 125-133, 136-141, 144-149, 159-165
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185    163    12%   23-57, 60-68, 71-84, 93-111, 120-145, 148-152, 155, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 243-268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     84    15%   27-79, 82-89, 93-100, 104-111, 118-119, 128-141, 144-149
src\gui\components\scarico_ore\model.py                                168    136    19%   71-97, 108-121, 132-153, 157, 166-168, 178-192, 196-199, 203-210, 214-216, 220-222, 226-228, 232-258, 262-279, 285-287, 291-316
src\gui\controllers\bot_controller.py                                   51     31    39%   45-52, 79-88, 93-98, 107-119
src\gui\controllers\navigation_controller.py                           270    215    20%   58-84, 88-104, 108-129, 133-135, 139-143, 147-151, 155-159, 163-167, 171-175, 179-183, 187-191, 195-199, 203-207, 211-215, 219-225, 229-233, 240-283, 287-314, 318-322, 327-355, 371-372, 388, 392-404, 410-415, 419-421, 425-426, 430-431, 435-463, 467-489, 493-533
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    228     0%   7-455
src\gui\dialogs\certificati_analysis_dialog.py                         225    207     8%   36-46, 49-256, 260-286, 290-397, 401-498
src\gui\dialogs\command_palette.py                                     298    298     0%   7-432
src\gui\dialogs\confirmation_dialog.py                                  96     72    25%   54-118, 122-130, 134-142, 146-158, 174-177, 182-185, 190-193, 198-201
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\splash_standalone.py                                    81     81     0%   8-133
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      262    262     0%   6-412
src\gui\formatters.py                                                  135    116    14%   14-28, 38-68, 73, 90-96, 100-103, 107, 111, 115, 119-144, 150-152, 156-159, 163-242, 246-248
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              75     75     0%   7-323
src\gui\main_window\components\status_bar.py                           132    132     0%   7-232
src\gui\main_window\components\tool_bar.py                              82     82     0%   7-187
src\gui\main_window\components\tray_icon.py                             17     17     0%   7-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    37     37     0%   6-90
src\gui\main_window\controllers\monitoring_controller.py                36     36     0%   6-65
src\gui\main_window\controllers\signal_connector.py                     19     19     0%   7-65
src\gui\main_window\controllers\workflow_controller.py                  83     83     0%   6-155
src\gui\main_window\main.py                                            252    252     0%   7-474
src\gui\main_window\page_index.py                                       28     28     0%   7-53
src\gui\models\audit_model.py                                          131    105    20%   44-47, 62-64, 68, 72, 79-103, 107-125, 129-139, 143-150, 154-158, 162-170, 174-176, 182-184, 188-192, 196-201, 205-216, 228-230
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 281    211    25%   70-76, 80-118, 130-134, 138-140, 167-181, 185, 189-206, 210-211, 215-276, 283, 287-298, 308, 316, 325, 329-334, 338-341, 345-347, 351-373, 377-386, 390-393, 397-417, 421-425, 429-435, 448-459, 463-475, 479, 483-484, 491-494, 498-503, 507-530, 534-537
src\gui\panels\carico_ts.py                                             89     66    26%   39-47, 51-53, 57-61, 66-93, 97-99, 103, 107-109, 118-123, 127-176
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 29-32
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   28-35, 42-84, 91-99, 102-105, 109-113, 116-187, 190-244, 247-309, 312-351, 354-400
src\gui\panels\contabilita_kpi\kpi_panel.py                            161    143    11%   38-64, 67-183, 196-200, 204-217, 220-230, 233, 236-309
src\gui\panels\contabilita_panel.py                                    266    230    14%   60-67, 71-77, 81-222, 226-230, 234, 245-254, 261-284, 290-307, 311-313, 317-320, 324-338, 342-384, 388-392, 396-413, 417-433
src\gui\panels\dashboard_panel.py                                      128    109    15%   39-82, 86, 90-104, 109-153, 157-172, 176-205, 208-247
src\gui\panels\dettagli_oda.py                                         181    149    18%   45-58, 62-64, 68-72, 77-136, 145-147, 158-169, 173-175, 179, 183-194, 198-221, 225-237, 241-243, 252-257, 261-328, 332-340
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      94     69    27%   35-55, 58-85, 89-101, 104-110, 113-117, 120-122, 125-147, 150-154, 159, 163
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156    129    17%   26-52, 57-100, 109-195, 200-211, 216-240, 245-304
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    183    11%   31-74, 78, 89-109, 112-137, 140-203, 206-232, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275    240    13%   37-40, 44, 48-49, 52-58, 61-67, 71-105, 119-122, 125-157, 161, 168-169, 172-217, 220, 236-244, 248-363, 367-383, 387-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           137    112    18%   33-39, 43-177, 181-200, 203-209, 212-216, 220-224, 229, 244, 263, 279, 294, 307, 323, 336, 350, 365
src\gui\panels\notifications_panel.py                                  243    194    20%   70-83, 87-161, 165-169, 173-175, 179-181, 185-187, 191-192, 196-197, 201, 205-209, 216-239, 243-263, 267-291, 295-300, 304-305, 309-319, 323-349, 353-354, 358-366, 370-406
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    154    19%   48-93, 97-145, 150-164, 173-186, 199-209, 213-214, 219-235, 239-254, 258-260, 264-274, 278-296, 300, 304-307, 315-325
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           142    117    18%   42-50, 59-61, 65-68, 73-123, 132-134, 145-156, 160-162, 166-175, 179-184, 188-190, 199-272
src\gui\panels\ricerca_pdl.py                                          109     91    17%   44-52, 56-58, 63-123, 127-130, 134-135, 139-194, 198-204, 212-214
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73     58    21%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        91     72    21%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          229    195    15%   54-61, 70-72, 76-79, 84-186, 195-197, 201-203, 207-227, 231-241, 250-268, 280-284, 295-298, 302-358, 368-379, 383-403, 414-428, 435-450
src\gui\panels\scarico_ts.py                                           137    109    20%   38-51, 57-59, 63-67, 72-124, 128-130, 134, 141-143, 147-148, 152-162, 166-171, 175-177, 186-188, 197-262, 266
src\gui\panels\settings\main_panel.py                                  106     77    27%   48-51, 55-125, 129-137, 141-152, 156, 160, 164-173, 177-189, 193-202
src\gui\panels\settings\pages\diag_page.py                              33     19    42%   19-20, 23-42, 46-47
src\gui\panels\settings\pages\general_page.py                           46     34    26%   25-26, 29-69, 73-74, 78-79
src\gui\panels\settings\pages\lists_page.py                             47     35    26%   29-30, 34-62, 66-71, 75-80
src\gui\panels\settings\pages\paths_page.py                            166    137    17%   33-34, 37-94, 99-137, 141-165, 169-190, 207-208, 211, 214-216, 219-221, 224-226, 229-231, 234-236, 239-241, 244-246, 249-251, 257-281, 285-293
src\gui\panels\settings\shared.py                                       18      9    50%   10-29, 34, 61, 83, 103-105
src\gui\panels\settings\tabs\backup_tab.py                             118    103    13%   42-96, 112-114, 118-216, 219-222, 231-232
src\gui\panels\settings\tabs\config_tab.py                             150    128    15%   50-106, 125-128, 132-275, 279-282, 286-288, 292-294
src\gui\panels\settings\tabs\roi_tab.py                                116     97    16%   32-33, 36-104, 108, 126-143, 147-153, 162-163, 166-213, 217, 221
src\gui\panels\settings\tabs\telegram_tab.py                           128    109    15%   48-102, 121-123, 127-225, 228-231, 240-241, 250-251
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     98    19%   51-54, 58-78, 82-87, 91-103, 107-115, 119-138, 142-149, 153-159, 163-170, 179-191
src\gui\panels\settings\widgets\editable_list_widget.py                 83     61    27%   50-53, 57-76, 80-85, 89-100, 104-107, 111-116, 120-124, 128-133, 142-143
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    128    17%   47-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-292
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     50    21%   18-41, 44-68, 76-116, 120-135, 139-140
src\gui\panels\timbrature\components\settings_tab.py                   102     86    16%   31-36, 39-99, 103-124, 128-157, 162-169, 172-173, 178-180
src\gui\panels\timbrature\panel.py                                     221    193    13%   44-69, 73-90, 93-126, 129-210, 213-253, 257-273, 277-312, 316-334, 337-344, 349, 352-375, 380
src\gui\panels\timbrature_bot.py                                       106     81    24%   44-53, 57-59, 63-67, 72-85, 89-91, 95-96, 100-108, 112-117, 126-131, 135-196, 200-202
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      5    50%   46-53
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85     67    21%   26-29, 34, 42-53, 57-94, 99-122, 126-170, 175
src\gui\styles\widget_styles.py                                         36      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                                        46     46     0%   6-93
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     38    72%   48-49, 51-52, 90-92, 94-96, 152-153, 173-183, 190, 194-196, 270, 276, 282-290, 298-314
src\gui\widgets\animated_progress_bar.py                                79     65    18%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit\audit_filter_bar.py                              120    101    16%   38-39, 43-137, 146-148, 152-161, 178-179, 188-201
src\gui\widgets\audit\audit_pagination_bar.py                           37     27    27%   14-15, 18-43, 49-56, 60-61
src\gui\widgets\audit_log_widget.py                                    120     95    21%   45-57, 60-130, 133-134, 137-147, 150, 153-154, 163-179, 182-189, 192-194
src\gui\widgets\automazioni_widget.py                                   59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143    129    10%   25-154, 158-166, 170-186, 198-350, 354-363, 367-383
src\gui\widgets\autopilot\event_card.py                                144    126    12%   50-184, 188-189, 193, 197-212, 217-226, 231-293
src\gui\widgets\autopilot\main_widget.py                               208    183    12%   60-71, 75, 79, 83-168, 172-191, 195-204, 208-236, 240-242, 246-253, 257-260, 264-341, 345-394
src\gui\widgets\bot_parameters.py                                      222    185    17%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 135-139, 143-287, 296-303, 307, 326-328, 332-350, 354-362, 366, 370-372, 376-378, 382-387, 391, 395-396
src\gui\widgets\calendar_date_edit.py                                   18     12    33%   17-77
src\gui\widgets\contabilita\attivita_tab.py                            209    178    15%   70-79, 83-154, 158, 162-177, 181-194, 198-209, 213-219, 223-228, 232-250, 254-257, 261-267, 271-274, 278-281, 285-288, 292-295, 299-303, 312-323
src\gui\widgets\contabilita\certificati\tree_widget.py                  98     71    28%   31-32, 36-42, 46-50, 54-56, 64-65, 69-71, 75-77, 116-118, 121-141, 172-214, 218-225, 229-232
src\gui\widgets\contabilita\certificati_tab.py                         258    219    15%   50-54, 58-100, 104-115, 119, 123, 127-128, 132-138, 143-164, 168-279, 283-285, 289-290, 294-297, 301-304, 313-327, 331-369, 373-378, 382-386, 390-423, 428-451
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         186    154    17%   48-51, 55-96, 100, 103-130, 133-140, 144, 147-168, 171-191, 195-214, 217-237, 240-256
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     82    20%   26-27, 31-32, 36-53, 75-95, 98-157, 161, 165-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     51    52%   41, 48, 55, 62-63, 66-67, 116-117, 120-121, 139-140, 143-144, 165-166, 169-170, 205-206, 209-210, 233-234, 237-238, 259-264, 267-268, 296-297, 300-301, 327-328, 331-332, 357-358, 361-362, 384-385, 388-389
src\gui\widgets\dashboard\multi_window_status.py                        86     70    19%   40-94, 107-121, 124-170, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146    125    14%   49-100, 113-121, 125-185, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179    155    13%   38-47, 53-70, 74-87, 91-120, 125-192, 196-202, 208-214, 226-273, 277-285, 292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    353     9%   48-63, 67-68, 71-91, 94-117, 120-193, 196-279, 282-290, 293-304, 309-317, 320-344, 347-353, 359-376, 379-405, 409-423, 426-429, 436-486, 490-500, 503-530, 533-605, 608-618, 621
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     30    30%   29-38, 42, 46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         232    189    19%   56-57, 67-78, 82-89, 93-102, 107-121, 140-143, 147-184, 188-212, 216-223, 227-244, 248-261, 265-277, 287-324, 336-355, 365, 376-399, 403-405
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   6-152
src\gui\widgets\footer\components.py                                    57     57     0%   6-166
src\gui\widgets\footer\manager.py                                       20     20     0%   6-68
src\gui\widgets\footer\status_bar.py                                    36     36     0%   6-75
src\gui\widgets\footer\telemetry.py                                     55     55     0%   6-87
src\gui\widgets\info_widgets.py                                         92     75    18%   30-63, 67, 76-84, 89-113, 127-171, 175, 178
src\gui\widgets\message_bubble.py                                       54     54     0%   7-140
src\gui\widgets\mixins\clipboard_mixin.py                               87     74    15%   18-43, 47-68, 71-75, 78-82, 85-89, 92-105, 108, 111-123
src\gui\widgets\modern_button.py                                        67     16    76%   53-57, 67-68, 76-77, 83-86, 90-93, 156
src\gui\widgets\modern_card.py                                          42     28    33%   23-26, 30-31, 41-51, 55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     91    22%   58-74, 78-156, 160-166, 170-176, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48     36    25%   35-41, 45-121, 125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     59    20%   26-29, 32-133, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131    102    22%   42-54, 58-70, 74-76, 80-84, 88-107, 139-145, 149-232, 237-238, 242-243, 248-255, 259-260, 269-271, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     18    77%   261-302, 308-312, 318, 346-347
src\gui\widgets\safework\status_list.py                                 60     50    17%   19-26, 31-57, 61-67, 73-93
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     23    23%   16-36, 43-53
src\gui\widgets\sidebar_button.py                                       57     57     0%   6-125
src\gui\widgets\sidebar_widget.py                                      267    267     0%   7-406
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60     45    25%   26-85, 89-92, 98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46     37    20%   31-46, 56-73, 77-83
src\gui\widgets\timeline_widget.py                                     118     94    20%   33-34, 38-48, 55-102, 111-112, 115-135, 139-153, 157, 161-164, 174-191
src\gui\widgets\toast.py                                               157    123    22%   72-95, 99-146, 150-159, 163-185, 189-194, 198-200, 204-205, 209-221, 233-235, 259-294, 300-303, 308-311, 316-319, 324-327
src\gui\widgets\update_banner.py                                        85     85     0%   1-161
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18     18     0%   5-41
src\utils\document_processor.py                                         66     66     0%   6-89
src\utils\helpers.py                                                   128     94    27%   30-34, 48-70, 83-85, 90, 107-108, 113, 126-141, 148, 155-159, 166-175, 182-195, 203-235, 245, 249-252
src\utils\log_humanizer.py                                              43     28    35%   21-28, 56-70, 75-100
src\utils\parsing.py                                                    51     10    80%   15, 18, 22, 33-34, 46-47, 84, 91, 96
src\utils\printing.py                                                   88     71    19%   14-15, 24-28, 33-43, 51-57, 68-149
src\utils\resource_manager.py                                           86     45    48%   22-33, 63, 73, 83-85, 97-131, 160-166, 179-180, 193-194
src\utils\secure_logger.py                                              23     10    57%   47-54, 57-60
src\utils\security.py                                                   78     22    72%   43-44, 80-82, 102, 104, 109-111, 116, 122-136
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73     73     0%   7-270
--------------------------------------------------------------------------------------------------
TOTAL                                                                29393  22714    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_dettagli_oda_comprehensive.py::TestDettagliOdaComprehensive::test_page_setup_supplier_success
============================= 1 failed in 41.54s ==============================

```
</details>

---
### `tests/unit/test_dettagli_oda_comprehensive.py::TestDettagliOdaComprehensive::test_page_setup_supplier_success`
**Error:** `FAILED tests/unit/test_dettagli_oda_comprehensive.py::TestDettagliOdaComprehensive::test_page_setup_supplier_success`

**Timestamp:** `2026-03-18T11:23:14.375641`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_dettagli_oda_comprehensive.py F                          [100%]

================================== FAILURES ===================================
________ TestDettagliOdaComprehensive.test_page_setup_supplier_success ________
tests\unit\test_dettagli_oda_comprehensive.py:100: in test_page_setup_supplier_success
    assert res is True
E   assert False is True
---------------------------- Captured stdout call -----------------------------
Selezione fornitore: COEMI
✗ Selezione fornitore fallita: Message: 

=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      8    67%   126, 139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              338    202    40%   142-145, 158, 163, 178, 183-188, 197-201, 222, 249-251, 255, 259, 263, 267, 271-272, 277, 282-297, 301-341, 345-371, 375-394, 401-406, 410-421, 425-433, 441-503, 507-533, 537, 541-545, 549-554, 558-568, 572-580
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                           99     84    15%   50-55, 74-78, 109-172, 195-252
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     42    31%   29, 34, 39, 60, 64, 76-88, 100-137
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     28    74%   30, 35, 40, 51, 76, 79, 92, 111, 120-123, 128-130, 134, 153-155, 160-162, 170-172, 174, 192-194
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207    162    22%   43-45, 51-71, 78-85, 92-118, 139-213, 217-228, 238-267, 271-280, 284-292, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     88    18%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    220    15%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 289-321, 327-358, 362-373, 377-394, 398-418, 422-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     69    25%   29, 34, 39, 44, 49, 56-60, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         157    133    15%   36-40, 44, 48-56, 60-77, 81-140, 150-203, 208-232, 241-252, 257-292
src\bots\portale_fornitori\timbrature\storage.py                       166    141    15%   46, 54-81, 87-116, 135-146, 156-163, 166-194, 201-237, 247-262, 267-308, 311-348, 352-367, 374-375
src\bots\safework\base.py                                               82     59    28%   33-37, 41-45, 49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     55    19%   22-24, 30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     32    30%   25-27, 31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     45    29%   24-26, 30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    276    12%   48-50, 55, 60, 65, 69-86, 90-163, 167-171, 175-210, 214-250, 254-287, 291-327, 331-391, 395-408, 412-417, 421-432, 436-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     88    21%   55-56, 61, 66, 71, 83-145, 149-156, 165-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            149    149     0%   10-263
src\core\app_updater.py                                                  9      9     0%   7-35
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     39    61%   62-64, 81-82, 136-138, 140-143, 145-148, 150-152, 154-158, 171-172, 177-182, 194-200
src\core\audit\integrity.py                                             16      2    88%   22, 27
src\core\audit\manager.py                                              162     74    54%   34, 46, 63, 67-69, 74, 78, 86-91, 213, 217-220, 226-243, 247-274, 287, 291-294, 303-331
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138    138     0%   6-250
src\core\bug_reporter.py                                               157    157     0%   11-339
src\core\config\account_manager.py                                      53     25    53%   29, 34, 51, 58-64, 71-91
src\core\config\defaults.py                                              3      0   100%
src\core\config\migration.py                                            69     54    22%   23-30, 35-86, 94-108
src\core\config\security.py                                             44     18    59%   23-43, 65, 68, 78
src\core\config_manager.py                                             164     71    57%   48-49, 54, 74, 83, 93-94, 103-109, 127-128, 143, 188-190, 195-199, 206, 212-214, 219-221, 226-235, 240-251, 257-259, 264-290
src\core\constants.py                                                  125      0   100%
src\core\contabilita\certificati_engine.py                              91     69    24%   22-23, 27-34, 38-50, 58-79, 84-94, 99-109, 114-132, 137-138
src\core\contabilita\scarico_ore\controller.py                          53     34    36%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        115     62    46%   33, 38, 43, 52-64, 81-128, 137-144, 153-158, 167-174, 179, 184, 189, 194, 199, 204-213, 218, 227, 237, 242
src\core\contabilita_queries.py                                         82     39    52%   21-29, 35, 45-46, 52, 74-75, 80-90, 95-107, 113, 121-122
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   183, 188, 202-203, 231-233
src\core\database\migrations\contabilita.py                             34      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     34      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\database\pdl_queries.py                                        92     77    16%   23-37, 43-95, 100-136, 144-209
src\core\dipendenti\anagrafica_controller.py                            88     72    18%   27-40, 47-96, 101-139, 144-149
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              60     37    38%   15-16, 24-26, 36-38, 43-59, 64-76, 81-88
src\core\importers\certificati.py                                      126    101    20%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-200
src\core\importers\contabilita.py                                      133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                                      181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189    153    19%   14-15, 22-24, 61-101, 120-138, 142-161, 175-206, 210-277, 281-290, 307-309, 313-337
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            192    192     0%   7-323
src\core\license_validator.py                                          176    176     0%   8-302
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              37      2    95%   71-73
src\core\logging\context.py                                             57     24    58%   31-32, 40-41, 45-46, 54, 81-98, 118, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     50    32%   63-115, 121, 167-201
src\core\logging\filters.py                                             60     29    52%   114, 117, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83     23    72%   84, 88-90, 122, 125, 130, 138, 164-165, 205-215, 224, 230-240
src\core\logging\logger.py                                             116     36    69%   84, 96, 123, 135-141, 145-148, 156-157, 170-174, 178-183, 188-189, 208, 214, 222, 226, 230, 241, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             74     51    31%   23-26, 30, 46-50, 59-60, 77-111, 129-131, 134-136, 153-163, 175-182, 201, 213, 219
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     16    70%   58, 67, 91, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     76    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 218-220, 226-228, 234-236
src\core\logging\viewer.py                                             177    144    19%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-138, 142-143, 147-148, 152-153, 162-176, 185-193, 204, 216-222, 226-230, 234-248, 252-267, 271-273, 277-313, 317-333, 352, 357, 362
src\core\notification_manager.py                                       116     80    31%   53-57, 61-65, 69-77, 81-93, 97-101, 133-167, 179-181, 190, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-108
src\core\oda_manager.py                                                 42     26    38%   29, 38-91, 98-112
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68     44    35%   27-29, 37-43, 48-52, 63-87, 97, 115-135, 148-158
src\core\schemas.py                                                     57      9    84%   71-73, 78-80, 85-87
src\core\secrets_manager.py                                            105     57    46%   30-77, 85-89, 97-116, 120-123, 127-136, 140-142, 146-150, 168-169, 176-179, 184-188, 195-196, 201-207
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               70     14    80%   49-53, 55-57, 68, 74-76, 95, 97, 113
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                77     47    39%   40-51, 56-60, 73-86, 91-102, 107-119, 132-135, 149-161
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     76     0%   6-118
src\core\telegram\bridge\intent_handler.py                              75     75     0%   6-125
src\core\telegram\bridge\system_handler.py                             103    103     0%   6-139
src\core\telegram\bridge\ui_commands.py                                104    104     0%   6-144
src\core\telegram\service.py                                           205    205     0%   1-314
src\core\telegram_bridge.py                                             34     34     0%   7-84
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\updater\__init__.py                                             0      0   100%
src\core\updater\engine.py                                             165    165     0%   6-249
src\core\updater\gui.py                                                163    163     0%   6-273
src\core\version.py                                                      5      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174    145    17%   47-50, 66-107, 111-124, 133-134, 143-145, 149, 153-154, 160-165, 169, 173-174, 185-186, 199-219, 228-282, 292-304, 318-331, 344-394, 403-404
src\gui\components\animated_stack.py                                    85     76    11%   32-46, 56-130, 134-141, 145-148
src\gui\components\animated_tab_widget.py                              147    119    19%   36-95, 99-106, 115-134, 147-149, 158-164, 168-175, 184-190, 199-212, 216-230, 234-235, 239, 243, 252-254, 258, 262, 266, 270, 274, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                107     90    16%   28-34, 38-86, 91-107, 110-122, 125-133, 136-141, 144-149, 159-165
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185    163    12%   23-57, 60-68, 71-84, 93-111, 120-145, 148-152, 155, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 243-268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     84    15%   27-79, 82-89, 93-100, 104-111, 118-119, 128-141, 144-149
src\gui\components\scarico_ore\model.py                                168    136    19%   71-97, 108-121, 132-153, 157, 166-168, 178-192, 196-199, 203-210, 214-216, 220-222, 226-228, 232-258, 262-279, 285-287, 291-316
src\gui\controllers\bot_controller.py                                   51     31    39%   45-52, 79-88, 93-98, 107-119
src\gui\controllers\navigation_controller.py                           270    215    20%   58-84, 88-104, 108-129, 133-135, 139-143, 147-151, 155-159, 163-167, 171-175, 179-183, 187-191, 195-199, 203-207, 211-215, 219-225, 229-233, 240-283, 287-314, 318-322, 327-355, 371-372, 388, 392-404, 410-415, 419-421, 425-426, 430-431, 435-463, 467-489, 493-533
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    228     0%   7-455
src\gui\dialogs\certificati_analysis_dialog.py                         225    207     8%   36-46, 49-256, 260-286, 290-397, 401-498
src\gui\dialogs\command_palette.py                                     298    298     0%   7-432
src\gui\dialogs\confirmation_dialog.py                                  96     72    25%   54-118, 122-130, 134-142, 146-158, 174-177, 182-185, 190-193, 198-201
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\splash_standalone.py                                    81     81     0%   8-133
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      262    262     0%   6-412
src\gui\formatters.py                                                  135    116    14%   14-28, 38-68, 73, 90-96, 100-103, 107, 111, 115, 119-144, 150-152, 156-159, 163-242, 246-248
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              75     75     0%   7-323
src\gui\main_window\components\status_bar.py                           132    132     0%   7-232
src\gui\main_window\components\tool_bar.py                              82     82     0%   7-187
src\gui\main_window\components\tray_icon.py                             17     17     0%   7-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    37     37     0%   6-90
src\gui\main_window\controllers\monitoring_controller.py                36     36     0%   6-65
src\gui\main_window\controllers\signal_connector.py                     19     19     0%   7-65
src\gui\main_window\controllers\workflow_controller.py                  83     83     0%   6-155
src\gui\main_window\main.py                                            252    252     0%   7-474
src\gui\main_window\page_index.py                                       28     28     0%   7-53
src\gui\models\audit_model.py                                          131    105    20%   44-47, 62-64, 68, 72, 79-103, 107-125, 129-139, 143-150, 154-158, 162-170, 174-176, 182-184, 188-192, 196-201, 205-216, 228-230
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 281    211    25%   70-76, 80-118, 130-134, 138-140, 167-181, 185, 189-206, 210-211, 215-276, 283, 287-298, 308, 316, 325, 329-334, 338-341, 345-347, 351-373, 377-386, 390-393, 397-417, 421-425, 429-435, 448-459, 463-475, 479, 483-484, 491-494, 498-503, 507-530, 534-537
src\gui\panels\carico_ts.py                                             89     66    26%   39-47, 51-53, 57-61, 66-93, 97-99, 103, 107-109, 118-123, 127-176
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 29-32
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   28-35, 42-84, 91-99, 102-105, 109-113, 116-187, 190-244, 247-309, 312-351, 354-400
src\gui\panels\contabilita_kpi\kpi_panel.py                            161    143    11%   38-64, 67-183, 196-200, 204-217, 220-230, 233, 236-309
src\gui\panels\contabilita_panel.py                                    266    230    14%   60-67, 71-77, 81-222, 226-230, 234, 245-254, 261-284, 290-307, 311-313, 317-320, 324-338, 342-384, 388-392, 396-413, 417-433
src\gui\panels\dashboard_panel.py                                      128    109    15%   39-82, 86, 90-104, 109-153, 157-172, 176-205, 208-247
src\gui\panels\dettagli_oda.py                                         181    149    18%   45-58, 62-64, 68-72, 77-136, 145-147, 158-169, 173-175, 179, 183-194, 198-221, 225-237, 241-243, 252-257, 261-328, 332-340
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      94     69    27%   35-55, 58-85, 89-101, 104-110, 113-117, 120-122, 125-147, 150-154, 159, 163
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156    129    17%   26-52, 57-100, 109-195, 200-211, 216-240, 245-304
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    183    11%   31-74, 78, 89-109, 112-137, 140-203, 206-232, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275    240    13%   37-40, 44, 48-49, 52-58, 61-67, 71-105, 119-122, 125-157, 161, 168-169, 172-217, 220, 236-244, 248-363, 367-383, 387-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           137    112    18%   33-39, 43-177, 181-200, 203-209, 212-216, 220-224, 229, 244, 263, 279, 294, 307, 323, 336, 350, 365
src\gui\panels\notifications_panel.py                                  243    194    20%   70-83, 87-161, 165-169, 173-175, 179-181, 185-187, 191-192, 196-197, 201, 205-209, 216-239, 243-263, 267-291, 295-300, 304-305, 309-319, 323-349, 353-354, 358-366, 370-406
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    154    19%   48-93, 97-145, 150-164, 173-186, 199-209, 213-214, 219-235, 239-254, 258-260, 264-274, 278-296, 300, 304-307, 315-325
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           142    117    18%   42-50, 59-61, 65-68, 73-123, 132-134, 145-156, 160-162, 166-175, 179-184, 188-190, 199-272
src\gui\panels\ricerca_pdl.py                                          109     91    17%   44-52, 56-58, 63-123, 127-130, 134-135, 139-194, 198-204, 212-214
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73     58    21%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        91     72    21%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          229    195    15%   54-61, 70-72, 76-79, 84-186, 195-197, 201-203, 207-227, 231-241, 250-268, 280-284, 295-298, 302-358, 368-379, 383-403, 414-428, 435-450
src\gui\panels\scarico_ts.py                                           137    109    20%   38-51, 57-59, 63-67, 72-124, 128-130, 134, 141-143, 147-148, 152-162, 166-171, 175-177, 186-188, 197-262, 266
src\gui\panels\settings\main_panel.py                                  106     77    27%   48-51, 55-125, 129-137, 141-152, 156, 160, 164-173, 177-189, 193-202
src\gui\panels\settings\pages\diag_page.py                              33     19    42%   19-20, 23-42, 46-47
src\gui\panels\settings\pages\general_page.py                           46     34    26%   25-26, 29-69, 73-74, 78-79
src\gui\panels\settings\pages\lists_page.py                             47     35    26%   29-30, 34-62, 66-71, 75-80
src\gui\panels\settings\pages\paths_page.py                            166    137    17%   33-34, 37-94, 99-137, 141-165, 169-190, 207-208, 211, 214-216, 219-221, 224-226, 229-231, 234-236, 239-241, 244-246, 249-251, 257-281, 285-293
src\gui\panels\settings\shared.py                                       18      9    50%   10-29, 34, 61, 83, 103-105
src\gui\panels\settings\tabs\backup_tab.py                             118    103    13%   42-96, 112-114, 118-216, 219-222, 231-232
src\gui\panels\settings\tabs\config_tab.py                             150    128    15%   50-106, 125-128, 132-275, 279-282, 286-288, 292-294
src\gui\panels\settings\tabs\roi_tab.py                                116     97    16%   32-33, 36-104, 108, 126-143, 147-153, 162-163, 166-213, 217, 221
src\gui\panels\settings\tabs\telegram_tab.py                           128    109    15%   48-102, 121-123, 127-225, 228-231, 240-241, 250-251
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     98    19%   51-54, 58-78, 82-87, 91-103, 107-115, 119-138, 142-149, 153-159, 163-170, 179-191
src\gui\panels\settings\widgets\editable_list_widget.py                 83     61    27%   50-53, 57-76, 80-85, 89-100, 104-107, 111-116, 120-124, 128-133, 142-143
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    128    17%   47-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-292
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     50    21%   18-41, 44-68, 76-116, 120-135, 139-140
src\gui\panels\timbrature\components\settings_tab.py                   102     86    16%   31-36, 39-99, 103-124, 128-157, 162-169, 172-173, 178-180
src\gui\panels\timbrature\panel.py                                     221    193    13%   44-69, 73-90, 93-126, 129-210, 213-253, 257-273, 277-312, 316-334, 337-344, 349, 352-375, 380
src\gui\panels\timbrature_bot.py                                       106     81    24%   44-53, 57-59, 63-67, 72-85, 89-91, 95-96, 100-108, 112-117, 126-131, 135-196, 200-202
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      5    50%   46-53
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85     67    21%   26-29, 34, 42-53, 57-94, 99-122, 126-170, 175
src\gui\styles\widget_styles.py                                         36      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                                        46     46     0%   6-93
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     38    72%   48-49, 51-52, 90-92, 94-96, 152-153, 173-183, 190, 194-196, 270, 276, 282-290, 298-314
src\gui\widgets\animated_progress_bar.py                                79     65    18%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit\audit_filter_bar.py                              120    101    16%   38-39, 43-137, 146-148, 152-161, 178-179, 188-201
src\gui\widgets\audit\audit_pagination_bar.py                           37     27    27%   14-15, 18-43, 49-56, 60-61
src\gui\widgets\audit_log_widget.py                                    120     95    21%   45-57, 60-130, 133-134, 137-147, 150, 153-154, 163-179, 182-189, 192-194
src\gui\widgets\automazioni_widget.py                                   59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143    129    10%   25-154, 158-166, 170-186, 198-350, 354-363, 367-383
src\gui\widgets\autopilot\event_card.py                                144    126    12%   50-184, 188-189, 193, 197-212, 217-226, 231-293
src\gui\widgets\autopilot\main_widget.py                               208    183    12%   60-71, 75, 79, 83-168, 172-191, 195-204, 208-236, 240-242, 246-253, 257-260, 264-341, 345-394
src\gui\widgets\bot_parameters.py                                      222    185    17%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 135-139, 143-287, 296-303, 307, 326-328, 332-350, 354-362, 366, 370-372, 376-378, 382-387, 391, 395-396
src\gui\widgets\calendar_date_edit.py                                   18     12    33%   17-77
src\gui\widgets\contabilita\attivita_tab.py                            209    178    15%   70-79, 83-154, 158, 162-177, 181-194, 198-209, 213-219, 223-228, 232-250, 254-257, 261-267, 271-274, 278-281, 285-288, 292-295, 299-303, 312-323
src\gui\widgets\contabilita\certificati\tree_widget.py                  98     71    28%   31-32, 36-42, 46-50, 54-56, 64-65, 69-71, 75-77, 116-118, 121-141, 172-214, 218-225, 229-232
src\gui\widgets\contabilita\certificati_tab.py                         258    219    15%   50-54, 58-100, 104-115, 119, 123, 127-128, 132-138, 143-164, 168-279, 283-285, 289-290, 294-297, 301-304, 313-327, 331-369, 373-378, 382-386, 390-423, 428-451
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         186    154    17%   48-51, 55-96, 100, 103-130, 133-140, 144, 147-168, 171-191, 195-214, 217-237, 240-256
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     82    20%   26-27, 31-32, 36-53, 75-95, 98-157, 161, 165-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     51    52%   41, 48, 55, 62-63, 66-67, 116-117, 120-121, 139-140, 143-144, 165-166, 169-170, 205-206, 209-210, 233-234, 237-238, 259-264, 267-268, 296-297, 300-301, 327-328, 331-332, 357-358, 361-362, 384-385, 388-389
src\gui\widgets\dashboard\multi_window_status.py                        86     70    19%   40-94, 107-121, 124-170, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146    125    14%   49-100, 113-121, 125-185, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179    155    13%   38-47, 53-70, 74-87, 91-120, 125-192, 196-202, 208-214, 226-273, 277-285, 292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    353     9%   48-63, 67-68, 71-91, 94-117, 120-193, 196-279, 282-290, 293-304, 309-317, 320-344, 347-353, 359-376, 379-405, 409-423, 426-429, 436-486, 490-500, 503-530, 533-605, 608-618, 621
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     30    30%   29-38, 42, 46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         232    189    19%   56-57, 67-78, 82-89, 93-102, 107-121, 140-143, 147-184, 188-212, 216-223, 227-244, 248-261, 265-277, 287-324, 336-355, 365, 376-399, 403-405
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   6-152
src\gui\widgets\footer\components.py                                    57     57     0%   6-166
src\gui\widgets\footer\manager.py                                       20     20     0%   6-68
src\gui\widgets\footer\status_bar.py                                    36     36     0%   6-75
src\gui\widgets\footer\telemetry.py                                     55     55     0%   6-87
src\gui\widgets\info_widgets.py                                         92     75    18%   30-63, 67, 76-84, 89-113, 127-171, 175, 178
src\gui\widgets\message_bubble.py                                       54     54     0%   7-140
src\gui\widgets\mixins\clipboard_mixin.py                               87     74    15%   18-43, 47-68, 71-75, 78-82, 85-89, 92-105, 108, 111-123
src\gui\widgets\modern_button.py                                        67     16    76%   53-57, 67-68, 76-77, 83-86, 90-93, 156
src\gui\widgets\modern_card.py                                          42     28    33%   23-26, 30-31, 41-51, 55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     91    22%   58-74, 78-156, 160-166, 170-176, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48     36    25%   35-41, 45-121, 125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     59    20%   26-29, 32-133, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131    102    22%   42-54, 58-70, 74-76, 80-84, 88-107, 139-145, 149-232, 237-238, 242-243, 248-255, 259-260, 269-271, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     18    77%   261-302, 308-312, 318, 346-347
src\gui\widgets\safework\status_list.py                                 60     50    17%   19-26, 31-57, 61-67, 73-93
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     23    23%   16-36, 43-53
src\gui\widgets\sidebar_button.py                                       57     57     0%   6-125
src\gui\widgets\sidebar_widget.py                                      267    267     0%   7-406
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60     45    25%   26-85, 89-92, 98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46     37    20%   31-46, 56-73, 77-83
src\gui\widgets\timeline_widget.py                                     118     94    20%   33-34, 38-48, 55-102, 111-112, 115-135, 139-153, 157, 161-164, 174-191
src\gui\widgets\toast.py                                               157    123    22%   72-95, 99-146, 150-159, 163-185, 189-194, 198-200, 204-205, 209-221, 233-235, 259-294, 300-303, 308-311, 316-319, 324-327
src\gui\widgets\update_banner.py                                        85     85     0%   1-161
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18     18     0%   5-41
src\utils\document_processor.py                                         66     66     0%   6-89
src\utils\helpers.py                                                   128     94    27%   30-34, 48-70, 83-85, 90, 107-108, 113, 126-141, 148, 155-159, 166-175, 182-195, 203-235, 245, 249-252
src\utils\log_humanizer.py                                              43     28    35%   21-28, 56-70, 75-100
src\utils\parsing.py                                                    51     10    80%   15, 18, 22, 33-34, 46-47, 84, 91, 96
src\utils\printing.py                                                   88     71    19%   14-15, 24-28, 33-43, 51-57, 68-149
src\utils\resource_manager.py                                           86     45    48%   22-33, 63, 73, 83-85, 97-131, 160-166, 179-180, 193-194
src\utils\secure_logger.py                                              23     10    57%   47-54, 57-60
src\utils\security.py                                                   78     22    72%   43-44, 80-82, 102, 104, 109-111, 116, 122-136
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73     73     0%   7-270
--------------------------------------------------------------------------------------------------
TOTAL                                                                29393  22714    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_dettagli_oda_comprehensive.py::TestDettagliOdaComprehensive::test_page_setup_supplier_success
============================= 1 failed in 41.75s ==============================

```
</details>

---
### `tests/unit/test_document_processor_advanced.py::TestDocumentProcessorAdvanced::test_get_pages_as_images_limit`
**Error:** `FAILED tests/unit/test_document_processor_advanced.py::TestDocumentProcessorAdvanced::test_get_pages_as_images_limit`

**Timestamp:** `2026-03-18T11:26:17.584743`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_document_processor_advanced.py F                         [100%]

================================== FAILURES ===================================
________ TestDocumentProcessorAdvanced.test_get_pages_as_images_limit _________
tests\unit\test_document_processor_advanced.py:51: in test_get_pages_as_images_limit
    images = DocumentProcessor.get_pages_as_images(Path("long.pdf"), max_pages=3)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: type object 'DocumentProcessor' has no attribute 'get_pages_as_images'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      8    67%   126, 139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              338    197    42%   142-145, 158, 163, 178, 183-188, 197-201, 222, 249-251, 255, 259, 263, 267, 271-272, 277, 282-297, 301-341, 345-371, 375-394, 401-406, 410-421, 425-433, 441-503, 507-533, 537, 541-545, 549-554, 558-568, 573-576
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                           99     84    15%   50-55, 74-78, 109-172, 195-252
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     42    31%   29, 34, 39, 60, 64, 76-88, 100-137
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     22    79%   30, 35, 40, 51, 76, 79, 92, 111, 120-123, 134, 153-155, 160-162, 174, 193-194
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207    130    37%   51-71, 101-103, 113-118, 139-213, 217-228, 238-267, 271-280, 287, 292, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     88    18%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    220    15%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 289-321, 327-358, 362-373, 377-394, 398-418, 422-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     69    25%   29, 34, 39, 44, 49, 56-60, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         157    133    15%   36-40, 44, 48-56, 60-77, 81-140, 150-203, 208-232, 241-252, 257-292
src\bots\portale_fornitori\timbrature\storage.py                       166    141    15%   46, 54-81, 87-116, 135-146, 156-163, 166-194, 201-237, 247-262, 267-308, 311-348, 352-367, 374-375
src\bots\safework\base.py                                               82     59    28%   33-37, 41-45, 49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     55    19%   22-24, 30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     32    30%   25-27, 31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     45    29%   24-26, 30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    276    12%   48-50, 55, 60, 65, 69-86, 90-163, 167-171, 175-210, 214-250, 254-287, 291-327, 331-391, 395-408, 412-417, 421-432, 436-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     88    21%   55-56, 61, 66, 71, 83-145, 149-156, 165-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            149    149     0%   10-263
src\core\app_updater.py                                                  9      9     0%   7-35
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     39    61%   62-64, 81-82, 136-138, 140-143, 145-148, 150-152, 154-158, 171-172, 177-182, 194-200
src\core\audit\integrity.py                                             16      2    88%   22, 27
src\core\audit\manager.py                                              162     74    54%   34, 46, 63, 67-69, 74, 78, 86-91, 213, 217-220, 226-243, 247-274, 287, 291-294, 303-331
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138    138     0%   6-250
src\core\bug_reporter.py                                               157    157     0%   11-339
src\core\config\account_manager.py                                      53     25    53%   29, 34, 51, 58-64, 71-91
src\core\config\defaults.py                                              3      0   100%
src\core\config\migration.py                                            69     54    22%   23-30, 35-86, 94-108
src\core\config\security.py                                             44     18    59%   23-43, 65, 68, 78
src\core\config_manager.py                                             164     71    57%   48-49, 54, 74, 83, 93-94, 103-109, 127-128, 143, 188-190, 195-199, 206, 212-214, 219-221, 226-235, 240-251, 257-259, 264-290
src\core\constants.py                                                  125      0   100%
src\core\contabilita\certificati_engine.py                              91     69    24%   22-23, 27-34, 38-50, 58-79, 84-94, 99-109, 114-132, 137-138
src\core\contabilita\scarico_ore\controller.py                          53     34    36%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        115     62    46%   33, 38, 43, 52-64, 81-128, 137-144, 153-158, 167-174, 179, 184, 189, 194, 199, 204-213, 218, 227, 237, 242
src\core\contabilita_queries.py                                         82     39    52%   21-29, 35, 45-46, 52, 74-75, 80-90, 95-107, 113, 121-122
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   183, 188, 202-203, 231-233
src\core\database\migrations\contabilita.py                             34      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     34      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\database\pdl_queries.py                                        92     77    16%   23-37, 43-95, 100-136, 144-209
src\core\dipendenti\anagrafica_controller.py                            88     72    18%   27-40, 47-96, 101-139, 144-149
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              60     37    38%   15-16, 24-26, 36-38, 43-59, 64-76, 81-88
src\core\importers\certificati.py                                      126    101    20%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-200
src\core\importers\contabilita.py                                      133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                                      181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189    153    19%   14-15, 22-24, 61-101, 120-138, 142-161, 175-206, 210-277, 281-290, 307-309, 313-337
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            192    192     0%   7-323
src\core\license_validator.py                                          176    176     0%   8-302
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              37      2    95%   71-73
src\core\logging\context.py                                             57     24    58%   31-32, 40-41, 45-46, 54, 81-98, 118, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     50    32%   63-115, 121, 167-201
src\core\logging\filters.py                                             60     29    52%   114, 117, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83     22    73%   84, 88-90, 122, 125, 138, 164-165, 205-215, 224, 230-240
src\core\logging\logger.py                                             116     36    69%   84, 96, 123, 135-141, 145-148, 156-157, 170-174, 178-183, 188-189, 208, 214, 222, 226, 230, 241, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             74     51    31%   23-26, 30, 46-50, 59-60, 77-111, 129-131, 134-136, 153-163, 175-182, 201, 213, 219
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     16    70%   58, 67, 91, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     76    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 218-220, 226-228, 234-236
src\core\logging\viewer.py                                             177    144    19%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-138, 142-143, 147-148, 152-153, 162-176, 185-193, 204, 216-222, 226-230, 234-248, 252-267, 271-273, 277-313, 317-333, 352, 357, 362
src\core\notification_manager.py                                       116     80    31%   53-57, 61-65, 69-77, 81-93, 97-101, 133-167, 179-181, 190, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-108
src\core\oda_manager.py                                                 42     26    38%   29, 38-91, 98-112
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68     44    35%   27-29, 37-43, 48-52, 63-87, 97, 115-135, 148-158
src\core\schemas.py                                                     57      9    84%   71-73, 78-80, 85-87
src\core\secrets_manager.py                                            105     57    46%   30-77, 85-89, 97-116, 120-123, 127-136, 140-142, 146-150, 168-169, 176-179, 184-188, 195-196, 201-207
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               70     14    80%   49-53, 55-57, 68, 74-76, 95, 97, 113
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                77     47    39%   40-51, 56-60, 73-86, 91-102, 107-119, 132-135, 149-161
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     76     0%   6-118
src\core\telegram\bridge\intent_handler.py                              75     75     0%   6-125
src\core\telegram\bridge\system_handler.py                             103    103     0%   6-139
src\core\telegram\bridge\ui_commands.py                                104    104     0%   6-144
src\core\telegram\service.py                                           205    205     0%   1-314
src\core\telegram_bridge.py                                             34     34     0%   7-84
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\updater\__init__.py                                             0      0   100%
src\core\updater\engine.py                                             165    165     0%   6-249
src\core\updater\gui.py                                                163    163     0%   6-273
src\core\version.py                                                      5      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174    145    17%   47-50, 66-107, 111-124, 133-134, 143-145, 149, 153-154, 160-165, 169, 173-174, 185-186, 199-219, 228-282, 292-304, 318-331, 344-394, 403-404
src\gui\components\animated_stack.py                                    85     76    11%   32-46, 56-130, 134-141, 145-148
src\gui\components\animated_tab_widget.py                              147    119    19%   36-95, 99-106, 115-134, 147-149, 158-164, 168-175, 184-190, 199-212, 216-230, 234-235, 239, 243, 252-254, 258, 262, 266, 270, 274, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                107     90    16%   28-34, 38-86, 91-107, 110-122, 125-133, 136-141, 144-149, 159-165
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185    163    12%   23-57, 60-68, 71-84, 93-111, 120-145, 148-152, 155, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 243-268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     84    15%   27-79, 82-89, 93-100, 104-111, 118-119, 128-141, 144-149
src\gui\components\scarico_ore\model.py                                168    136    19%   71-97, 108-121, 132-153, 157, 166-168, 178-192, 196-199, 203-210, 214-216, 220-222, 226-228, 232-258, 262-279, 285-287, 291-316
src\gui\controllers\bot_controller.py                                   51     31    39%   45-52, 79-88, 93-98, 107-119
src\gui\controllers\navigation_controller.py                           270    215    20%   58-84, 88-104, 108-129, 133-135, 139-143, 147-151, 155-159, 163-167, 171-175, 179-183, 187-191, 195-199, 203-207, 211-215, 219-225, 229-233, 240-283, 287-314, 318-322, 327-355, 371-372, 388, 392-404, 410-415, 419-421, 425-426, 430-431, 435-463, 467-489, 493-533
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    228     0%   7-455
src\gui\dialogs\certificati_analysis_dialog.py                         225    207     8%   36-46, 49-256, 260-286, 290-397, 401-498
src\gui\dialogs\command_palette.py                                     298    298     0%   7-432
src\gui\dialogs\confirmation_dialog.py                                  96     72    25%   54-118, 122-130, 134-142, 146-158, 174-177, 182-185, 190-193, 198-201
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\splash_standalone.py                                    81     81     0%   8-133
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      262    262     0%   6-412
src\gui\formatters.py                                                  135    116    14%   14-28, 38-68, 73, 90-96, 100-103, 107, 111, 115, 119-144, 150-152, 156-159, 163-242, 246-248
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              75     75     0%   7-323
src\gui\main_window\components\status_bar.py                           132    132     0%   7-232
src\gui\main_window\components\tool_bar.py                              82     82     0%   7-187
src\gui\main_window\components\tray_icon.py                             17     17     0%   7-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    37     37     0%   6-90
src\gui\main_window\controllers\monitoring_controller.py                36     36     0%   6-65
src\gui\main_window\controllers\signal_connector.py                     19     19     0%   7-65
src\gui\main_window\controllers\workflow_controller.py                  83     83     0%   6-155
src\gui\main_window\main.py                                            252    252     0%   7-474
src\gui\main_window\page_index.py                                       28     28     0%   7-53
src\gui\models\audit_model.py                                          131    105    20%   44-47, 62-64, 68, 72, 79-103, 107-125, 129-139, 143-150, 154-158, 162-170, 174-176, 182-184, 188-192, 196-201, 205-216, 228-230
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 281    211    25%   70-76, 80-118, 130-134, 138-140, 167-181, 185, 189-206, 210-211, 215-276, 283, 287-298, 308, 316, 325, 329-334, 338-341, 345-347, 351-373, 377-386, 390-393, 397-417, 421-425, 429-435, 448-459, 463-475, 479, 483-484, 491-494, 498-503, 507-530, 534-537
src\gui\panels\carico_ts.py                                             89     66    26%   39-47, 51-53, 57-61, 66-93, 97-99, 103, 107-109, 118-123, 127-176
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 29-32
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   28-35, 42-84, 91-99, 102-105, 109-113, 116-187, 190-244, 247-309, 312-351, 354-400
src\gui\panels\contabilita_kpi\kpi_panel.py                            161    143    11%   38-64, 67-183, 196-200, 204-217, 220-230, 233, 236-309
src\gui\panels\contabilita_panel.py                                    266    230    14%   60-67, 71-77, 81-222, 226-230, 234, 245-254, 261-284, 290-307, 311-313, 317-320, 324-338, 342-384, 388-392, 396-413, 417-433
src\gui\panels\dashboard_panel.py                                      128    109    15%   39-82, 86, 90-104, 109-153, 157-172, 176-205, 208-247
src\gui\panels\dettagli_oda.py                                         181    149    18%   45-58, 62-64, 68-72, 77-136, 145-147, 158-169, 173-175, 179, 183-194, 198-221, 225-237, 241-243, 252-257, 261-328, 332-340
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      94     69    27%   35-55, 58-85, 89-101, 104-110, 113-117, 120-122, 125-147, 150-154, 159, 163
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156    129    17%   26-52, 57-100, 109-195, 200-211, 216-240, 245-304
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    183    11%   31-74, 78, 89-109, 112-137, 140-203, 206-232, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275    240    13%   37-40, 44, 48-49, 52-58, 61-67, 71-105, 119-122, 125-157, 161, 168-169, 172-217, 220, 236-244, 248-363, 367-383, 387-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           137    112    18%   33-39, 43-177, 181-200, 203-209, 212-216, 220-224, 229, 244, 263, 279, 294, 307, 323, 336, 350, 365
src\gui\panels\notifications_panel.py                                  243    194    20%   70-83, 87-161, 165-169, 173-175, 179-181, 185-187, 191-192, 196-197, 201, 205-209, 216-239, 243-263, 267-291, 295-300, 304-305, 309-319, 323-349, 353-354, 358-366, 370-406
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    154    19%   48-93, 97-145, 150-164, 173-186, 199-209, 213-214, 219-235, 239-254, 258-260, 264-274, 278-296, 300, 304-307, 315-325
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           142    117    18%   42-50, 59-61, 65-68, 73-123, 132-134, 145-156, 160-162, 166-175, 179-184, 188-190, 199-272
src\gui\panels\ricerca_pdl.py                                          109     91    17%   44-52, 56-58, 63-123, 127-130, 134-135, 139-194, 198-204, 212-214
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73     58    21%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        91     72    21%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          229    195    15%   54-61, 70-72, 76-79, 84-186, 195-197, 201-203, 207-227, 231-241, 250-268, 280-284, 295-298, 302-358, 368-379, 383-403, 414-428, 435-450
src\gui\panels\scarico_ts.py                                           137    109    20%   38-51, 57-59, 63-67, 72-124, 128-130, 134, 141-143, 147-148, 152-162, 166-171, 175-177, 186-188, 197-262, 266
src\gui\panels\settings\main_panel.py                                  106     77    27%   48-51, 55-125, 129-137, 141-152, 156, 160, 164-173, 177-189, 193-202
src\gui\panels\settings\pages\diag_page.py                              33     19    42%   19-20, 23-42, 46-47
src\gui\panels\settings\pages\general_page.py                           46     34    26%   25-26, 29-69, 73-74, 78-79
src\gui\panels\settings\pages\lists_page.py                             47     35    26%   29-30, 34-62, 66-71, 75-80
src\gui\panels\settings\pages\paths_page.py                            166    137    17%   33-34, 37-94, 99-137, 141-165, 169-190, 207-208, 211, 214-216, 219-221, 224-226, 229-231, 234-236, 239-241, 244-246, 249-251, 257-281, 285-293
src\gui\panels\settings\shared.py                                       18      9    50%   10-29, 34, 61, 83, 103-105
src\gui\panels\settings\tabs\backup_tab.py                             118    103    13%   42-96, 112-114, 118-216, 219-222, 231-232
src\gui\panels\settings\tabs\config_tab.py                             150    128    15%   50-106, 125-128, 132-275, 279-282, 286-288, 292-294
src\gui\panels\settings\tabs\roi_tab.py                                116     97    16%   32-33, 36-104, 108, 126-143, 147-153, 162-163, 166-213, 217, 221
src\gui\panels\settings\tabs\telegram_tab.py                           128    109    15%   48-102, 121-123, 127-225, 228-231, 240-241, 250-251
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     98    19%   51-54, 58-78, 82-87, 91-103, 107-115, 119-138, 142-149, 153-159, 163-170, 179-191
src\gui\panels\settings\widgets\editable_list_widget.py                 83     61    27%   50-53, 57-76, 80-85, 89-100, 104-107, 111-116, 120-124, 128-133, 142-143
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    128    17%   47-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-292
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     50    21%   18-41, 44-68, 76-116, 120-135, 139-140
src\gui\panels\timbrature\components\settings_tab.py                   102     86    16%   31-36, 39-99, 103-124, 128-157, 162-169, 172-173, 178-180
src\gui\panels\timbrature\panel.py                                     221    193    13%   44-69, 73-90, 93-126, 129-210, 213-253, 257-273, 277-312, 316-334, 337-344, 349, 352-375, 380
src\gui\panels\timbrature_bot.py                                       106     81    24%   44-53, 57-59, 63-67, 72-85, 89-91, 95-96, 100-108, 112-117, 126-131, 135-196, 200-202
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      5    50%   46-53
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85     67    21%   26-29, 34, 42-53, 57-94, 99-122, 126-170, 175
src\gui\styles\widget_styles.py                                         36      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                                        46     46     0%   6-93
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     38    72%   48-49, 51-52, 90-92, 94-96, 152-153, 173-183, 190, 194-196, 270, 276, 282-290, 298-314
src\gui\widgets\animated_progress_bar.py                                79     65    18%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit\audit_filter_bar.py                              120    101    16%   38-39, 43-137, 146-148, 152-161, 178-179, 188-201
src\gui\widgets\audit\audit_pagination_bar.py                           37     27    27%   14-15, 18-43, 49-56, 60-61
src\gui\widgets\audit_log_widget.py                                    120     95    21%   45-57, 60-130, 133-134, 137-147, 150, 153-154, 163-179, 182-189, 192-194
src\gui\widgets\automazioni_widget.py                                   59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143    129    10%   25-154, 158-166, 170-186, 198-350, 354-363, 367-383
src\gui\widgets\autopilot\event_card.py                                144    126    12%   50-184, 188-189, 193, 197-212, 217-226, 231-293
src\gui\widgets\autopilot\main_widget.py                               208    183    12%   60-71, 75, 79, 83-168, 172-191, 195-204, 208-236, 240-242, 246-253, 257-260, 264-341, 345-394
src\gui\widgets\bot_parameters.py                                      222    185    17%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 135-139, 143-287, 296-303, 307, 326-328, 332-350, 354-362, 366, 370-372, 376-378, 382-387, 391, 395-396
src\gui\widgets\calendar_date_edit.py                                   18     12    33%   17-77
src\gui\widgets\contabilita\attivita_tab.py                            209    178    15%   70-79, 83-154, 158, 162-177, 181-194, 198-209, 213-219, 223-228, 232-250, 254-257, 261-267, 271-274, 278-281, 285-288, 292-295, 299-303, 312-323
src\gui\widgets\contabilita\certificati\tree_widget.py                  98     71    28%   31-32, 36-42, 46-50, 54-56, 64-65, 69-71, 75-77, 116-118, 121-141, 172-214, 218-225, 229-232
src\gui\widgets\contabilita\certificati_tab.py                         258    219    15%   50-54, 58-100, 104-115, 119, 123, 127-128, 132-138, 143-164, 168-279, 283-285, 289-290, 294-297, 301-304, 313-327, 331-369, 373-378, 382-386, 390-423, 428-451
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         186    154    17%   48-51, 55-96, 100, 103-130, 133-140, 144, 147-168, 171-191, 195-214, 217-237, 240-256
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     82    20%   26-27, 31-32, 36-53, 75-95, 98-157, 161, 165-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     51    52%   41, 48, 55, 62-63, 66-67, 116-117, 120-121, 139-140, 143-144, 165-166, 169-170, 205-206, 209-210, 233-234, 237-238, 259-264, 267-268, 296-297, 300-301, 327-328, 331-332, 357-358, 361-362, 384-385, 388-389
src\gui\widgets\dashboard\multi_window_status.py                        86     70    19%   40-94, 107-121, 124-170, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146    125    14%   49-100, 113-121, 125-185, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179    155    13%   38-47, 53-70, 74-87, 91-120, 125-192, 196-202, 208-214, 226-273, 277-285, 292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    353     9%   48-63, 67-68, 71-91, 94-117, 120-193, 196-279, 282-290, 293-304, 309-317, 320-344, 347-353, 359-376, 379-405, 409-423, 426-429, 436-486, 490-500, 503-530, 533-605, 608-618, 621
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     30    30%   29-38, 42, 46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         232    189    19%   56-57, 67-78, 82-89, 93-102, 107-121, 140-143, 147-184, 188-212, 216-223, 227-244, 248-261, 265-277, 287-324, 336-355, 365, 376-399, 403-405
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   6-152
src\gui\widgets\footer\components.py                                    57     57     0%   6-166
src\gui\widgets\footer\manager.py                                       20     20     0%   6-68
src\gui\widgets\footer\status_bar.py                                    36     36     0%   6-75
src\gui\widgets\footer\telemetry.py                                     55     55     0%   6-87
src\gui\widgets\info_widgets.py                                         92     75    18%   30-63, 67, 76-84, 89-113, 127-171, 175, 178
src\gui\widgets\message_bubble.py                                       54     54     0%   7-140
src\gui\widgets\mixins\clipboard_mixin.py                               87     74    15%   18-43, 47-68, 71-75, 78-82, 85-89, 92-105, 108, 111-123
src\gui\widgets\modern_button.py                                        67     16    76%   53-57, 67-68, 76-77, 83-86, 90-93, 156
src\gui\widgets\modern_card.py                                          42     28    33%   23-26, 30-31, 41-51, 55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     91    22%   58-74, 78-156, 160-166, 170-176, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48     36    25%   35-41, 45-121, 125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     59    20%   26-29, 32-133, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131    102    22%   42-54, 58-70, 74-76, 80-84, 88-107, 139-145, 149-232, 237-238, 242-243, 248-255, 259-260, 269-271, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     18    77%   261-302, 308-312, 318, 346-347
src\gui\widgets\safework\status_list.py                                 60     50    17%   19-26, 31-57, 61-67, 73-93
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     23    23%   16-36, 43-53
src\gui\widgets\sidebar_button.py                                       57     57     0%   6-125
src\gui\widgets\sidebar_widget.py                                      267    267     0%   7-406
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60     45    25%   26-85, 89-92, 98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46     37    20%   31-46, 56-73, 77-83
src\gui\widgets\timeline_widget.py                                     118     94    20%   33-34, 38-48, 55-102, 111-112, 115-135, 139-153, 157, 161-164, 174-191
src\gui\widgets\toast.py                                               157    123    22%   72-95, 99-146, 150-159, 163-185, 189-194, 198-200, 204-205, 209-221, 233-235, 259-294, 300-303, 308-311, 316-319, 324-327
src\gui\widgets\update_banner.py                                        85     85     0%   1-161
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         66     24    64%   13-14, 24, 37, 41-42, 49-50, 56-57, 59-60, 64-65, 73-74, 76-78, 84-89
src\utils\helpers.py                                                   128     94    27%   30-34, 48-70, 83-85, 90, 107-108, 113, 126-141, 148, 155-159, 166-175, 182-195, 203-235, 245, 249-252
src\utils\log_humanizer.py                                              43     28    35%   21-28, 56-70, 75-100
src\utils\parsing.py                                                    51     10    80%   15, 18, 22, 33-34, 46-47, 84, 91, 96
src\utils\printing.py                                                   88     71    19%   14-15, 24-28, 33-43, 51-57, 68-149
src\utils\resource_manager.py                                           86     45    48%   22-33, 63, 73, 83-85, 97-131, 160-166, 179-180, 193-194
src\utils\secure_logger.py                                              23     10    57%   47-54, 57-60
src\utils\security.py                                                   78     22    72%   43-44, 80-82, 102, 104, 109-111, 116, 122-136
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73     73     0%   7-270
--------------------------------------------------------------------------------------------------
TOTAL                                                                29393  22612    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_document_processor_advanced.py::TestDocumentProcessorAdvanced::test_get_pages_as_images_limit
============================= 1 failed in 10.81s ==============================

```
</details>

---
### `tests/unit/test_document_processor_coverage.py::TestDocumentProcessorCoverage::test_get_pages_as_images_limit`
**Error:** `FAILED tests/unit/test_document_processor_coverage.py::TestDocumentProcessorCoverage::test_get_pages_as_images_limit`

**Timestamp:** `2026-03-18T11:36:11.626540`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_document_processor_coverage.py F                         [100%]

================================== FAILURES ===================================
________ TestDocumentProcessorCoverage.test_get_pages_as_images_limit _________
tests\unit\test_document_processor_coverage.py:48: in test_get_pages_as_images_limit
    images = DocumentProcessor.get_pages_as_images(Path("test.pdf"), max_pages=2)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: type object 'DocumentProcessor' has no attribute 'get_pages_as_images'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                       Stmts   Miss  Cover   Missing
----------------------------------------------------------------------------------------
src\bots\__init__.py                                          24     24     0%   6-162
src\bots\base\__init__.py                                      2      2     0%   5-7
src\bots\base\base_bot.py                                    338    338     0%   9-583
src\bots\base\login_page.py                                   94     94     0%   6-154
src\bots\base\wait_helpers.py                                 99     99     0%   14-252
src\core\__init__.py                                           2      0   100%
src\core\app_initializer.py                                  149    149     0%   10-263
src\core\app_updater.py                                        9      9     0%   7-35
src\core\audit\__init__.py                                     3      3     0%   1-4
src\core\audit\database.py                                   101    101     0%   1-200
src\core\audit\integrity.py                                   16     16     0%   1-27
src\core\audit\manager.py                                    162    162     0%   1-331
src\core\audit\models.py                                       9      9     0%   1-17
src\core\audit\signals.py                                     25     25     0%   1-48
src\core\audit_manager.py                                      5      5     0%   6-11
src\core\auth_monitor.py                                      73     73     0%   6-132
src\core\backup_manager.py                                   138    138     0%   6-250
src\core\bug_reporter.py                                     157    157     0%   11-339
src\core\config\account_manager.py                            53     46    13%   16-38, 43-53, 58-64, 71-91
src\core\config\defaults.py                                    3      0   100%
src\core\config\migration.py                                  69     56    19%   23-30, 35-86, 91-108
src\core\config\security.py                                   44     37    16%   14-15, 20-43, 48-49, 54-78
src\core\config_manager.py                                   164    121    26%   48-49, 54, 59, 65-86, 91-111, 117-128, 133-143, 149, 154, 162-164, 169, 174-176, 181-183, 188-190, 195-199, 204-207, 212-214, 219-221, 226-235, 240-251, 257-259, 264-290
src\core\constants.py                                        125      0   100%
src\core\contabilita_manager.py                              115    115     0%   6-242
src\core\contabilita_queries.py                               82     82     0%   6-122
src\core\contabilita_search.py                                92     92     0%   6-185
src\core\contabilita_stats.py                                 59     59     0%   6-101
src\core\contabilita_worker.py                               102    102     0%   1-216
src\core\data_synchronizer.py                                 25     25     0%   7-63
src\core\database\__init__.py                                  3      3     0%   1-4
src\core\database\manager.py                                 123    123     0%   6-236
src\core\database\pdl_queries.py                              92     92     0%   6-209
src\core\employees.py                                         98     98     0%   1-196
src\core\excel_importer.py                                     4      4     0%   6-11
src\core\importers\__init__.py                                44     44     0%   1-106
src\core\importers\attivita.py                                67     67     0%   1-117
src\core\importers\base.py                                    60     60     0%   1-88
src\core\importers\certificati.py                            126    126     0%   1-200
src\core\importers\contabilita.py                            133    133     0%   1-245
src\core\importers\giornaliere.py                            181    181     0%   1-290
src\core\importers\pdl_sync_manager.py                       163    163     0%   6-246
src\core\importers\scarico_ore.py                            189    189     0%   1-337
src\core\importers\storico_oda.py                             81     81     0%   1-185
src\core\license_updater.py                                  192    192     0%   7-323
src\core\license_validator.py                                176    176     0%   8-302
src\core\logging\__init__.py                                  10     10     0%   6-37
src\core\logging\alert_manager.py                            115    115     0%   7-240
src\core\logging\analytics.py                                136    136     0%   7-343
src\core\logging\config.py                                    37     37     0%   5-86
src\core\logging\context.py                                   57     57     0%   5-161
src\core\logging\decorators.py                                74     74     0%   6-201
src\core\logging\filters.py                                   60     60     0%   5-206
src\core\logging\formatters.py                                83     83     0%   5-240
src\core\logging\logger.py                                   116    116     0%   5-307
src\core\logging\metadata.py                                  86     86     0%   5-198
src\core\logging\metrics.py                                   74     74     0%   5-219
src\core\logging\migration.py                                 42     42     0%   5-120
src\core\logging\sampling.py                                  54     54     0%   5-201
src\core\logging\sinks.py                                    100    100     0%   5-236
src\core\logging\viewer.py                                   177    177     0%   7-362
src\core\notification_manager.py                             116    116     0%   8-243
src\core\oda_manager.py                                       42     42     0%   7-112
src\core\preventivi_manager.py                               196    196     0%   8-312
src\core\report_history.py                                    68     68     0%   7-158
src\core\schemas.py                                           57     57     0%   1-87
src\core\secrets_manager.py                                  105     67    36%   30-77, 85-89, 97-116, 120-123, 127-136, 140-142, 146-150, 158-169, 174-179, 184-188, 193-196, 201-207
src\core\stats_manager.py                                     70     70     0%   1-125
src\core\sync\__init__.py                                      0      0   100%
src\core\sync\base.py                                         23     23     0%   6-37
src\core\sync\contabilita_sync.py                             70     70     0%   6-127
src\core\sync\operazioni_sync.py                              42     42     0%   6-71
src\core\sync\smart_sync.py                                   25     25     0%   6-54
src\core\sync_tracker.py                                      77     77     0%   8-161
src\core\telegram\__init__.py                                  2      2     0%   1-3
src\core\telegram\bridge\__init__.py                           0      0   100%
src\core\telegram\bridge\data_processor.py                    76     76     0%   6-118
src\core\telegram\bridge\intent_handler.py                    75     75     0%   6-125
src\core\telegram\bridge\system_handler.py                   103    103     0%   6-139
src\core\telegram\bridge\ui_commands.py                      104    104     0%   6-144
src\core\telegram\service.py                                 205    205     0%   1-314
src\core\telegram_bridge.py                                   34     34     0%   7-84
src\core\telegram_manager.py                                   2      2     0%   6-8
src\core\time_manager.py                                      20     20     0%   6-57
src\core\timesheet_processor.py                               98     98     0%   6-164
src\core\updater\__init__.py                                   0      0   100%
src\core\updater\engine.py                                   165    165     0%   6-249
src\core\updater\gui.py                                      163    163     0%   6-273
src\core\version.py                                            5      0   100%
src\gui\__init__.py                                            0      0   100%
src\gui\cleanup_final.py                                      57     57     0%   8-121
src\gui\dialogs\__init__.py                                    0      0   100%
src\gui\dialogs\account_dialog.py                             69     69     0%   1-137
src\gui\dialogs\audit_detail_dialog.py                        61     61     0%   1-123
src\gui\dialogs\bug_report_dialog.py                         228    228     0%   7-455
src\gui\dialogs\certificati_analysis_dialog.py               225    225     0%   6-498
src\gui\dialogs\command_palette.py                           298    298     0%   7-432
src\gui\dialogs\confirmation_dialog.py                        96     96     0%   7-201
src\gui\dialogs\quick_actions_config.py                       91     91     0%   1-216
src\gui\dialogs\splash_standalone.py                          81     81     0%   8-133
src\gui\dialogs\standard_input_dialog.py                      40     40     0%   1-91
src\gui\dialogs\startup_dialog.py                            262    262     0%   6-412
src\gui\formatters.py                                        135    135     0%   1-248
src\gui\main_window\__init__.py                                2      2     0%   1-3
src\gui\main_window\components\__init__.py                     0      0   100%
src\gui\main_window\components\menu_bar.py                    75     75     0%   7-323
src\gui\main_window\components\status_bar.py                 132    132     0%   7-232
src\gui\main_window\components\tool_bar.py                    82     82     0%   7-187
src\gui\main_window\components\tray_icon.py                   17     17     0%   7-62
src\gui\main_window\controllers\__init__.py                    0      0   100%
src\gui\main_window\controllers\app_event_handler.py          37     37     0%   6-90
src\gui\main_window\controllers\monitoring_controller.py      36     36     0%   6-65
src\gui\main_window\controllers\signal_connector.py           19     19     0%   7-65
src\gui\main_window\controllers\workflow_controller.py        83     83     0%   6-155
src\gui\main_window\main.py                                  252    252     0%   7-474
src\gui\main_window\page_index.py                             28     28     0%   7-53
src\gui\panels\__init__.py                                    21     21     0%   6-27
src\gui\panels\base.py                                       281    281     0%   6-537
src\gui\panels\carico_ts.py                                   89     89     0%   6-176
src\gui\panels\consuntivo_panel.py                            46     46     0%   7-77
src\gui\panels\contabilita_kpi\__init__.py                     2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py                   14     14     0%   1-32
src\gui\panels\contabilita_kpi\charts.py                     213    213     0%   1-400
src\gui\panels\contabilita_kpi\kpi_panel.py                  161    161     0%   1-309
src\gui\panels\contabilita_panel.py                          266    266     0%   8-433
src\gui\panels\dashboard_panel.py                            128    128     0%   7-247
src\gui\panels\dettagli_oda.py                               181    181     0%   8-340
src\gui\panels\dipendenti\__init__.py                          2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                       28     28     0%   7-77
src\gui\panels\dipendenti\shared.py                          152    152     0%   6-329
src\gui\panels\dipendenti_manager_panel.py                   206    206     0%   1-369
src\gui\panels\health_panel.py                               275    275     0%   8-437
src\gui\panels\help_panel.py                                 137    137     0%   6-365
src\gui\panels\notifications_panel.py                        243    243     0%   7-406
src\gui\panels\pdl\__init__.py                                 2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                            17     17     0%   1-27
src\gui\panels\pdl\pdl_detail_view.py                         80     80     0%   7-144
src\gui\panels\pdl\pdl_filter_widget.py                      119    119     0%   1-186
src\gui\panels\pdl\pdl_panel.py                              189    189     0%   7-325
src\gui\panels\pdl\programmazione_tab.py                     218    218     0%   6-341
src\gui\panels\prenota_bp.py                                 142    142     0%   9-272
src\gui\panels\ricerca_pdl.py                                109    109     0%   6-214
src\gui\panels\scarico_ore_panel.py                          131    131     0%   7-261
src\gui\panels\scarico_pdl.py                                229    229     0%   7-450
src\gui\panels\scarico_ts.py                                 137    137     0%   6-266
src\gui\panels\storico_oda\__init__.py                         2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                    43     43     0%   1-77
src\gui\panels\storico_oda\oda_detail_view.py                 49     49     0%   1-75
src\gui\panels\storico_oda\oda_filter_widget.py               62     62     0%   1-114
src\gui\panels\storico_oda\oda_panel.py                      155    155     0%   8-292
src\gui\panels\timbrature\__init__.py                          2      2     0%   1-3
src\gui\panels\timbrature\panel.py                           221    221     0%   1-380
src\gui\panels\timbrature_bot.py                             106    106     0%   8-202
src\gui\panels\timbrature_db.py                                2      2     0%   6-8
src\gui\styles\__init__.py                                     4      4     0%   6-45
src\gui\styles\constants.py                                    9      9     0%   9-198
src\gui\styles\notification_styles.py                         10     10     0%   6-53
src\gui\styles\palette_helpers.py                             10     10     0%   6-25
src\gui\styles\theme_manager.py                               85     85     0%   6-175
src\gui\styles\widget_styles.py                               36     36     0%   6-392
src\gui\toast.py                                              46     46     0%   6-93
src\gui\widgets\__init__.py                                   19     19     0%   6-31
src\gui\widgets\activity_feed.py                             138    138     0%   1-321
src\gui\widgets\animated_progress_bar.py                      79     79     0%   7-174
src\gui\widgets\audit_log_widget.py                          120    120     0%   7-194
src\gui\widgets\automazioni_widget.py                         59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                          4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                    143    143     0%   1-383
src\gui\widgets\autopilot\event_card.py                      144    144     0%   1-293
src\gui\widgets\autopilot\main_widget.py                     208    208     0%   7-394
src\gui\widgets\bot_parameters.py                            222    222     0%   6-396
src\gui\widgets\calendar_date_edit.py                         18     18     0%   6-77
src\gui\widgets\core_widgets.py                              106    106     0%   8-389
src\gui\widgets\dashboard_stat_card.py                        49     49     0%   6-111
src\gui\widgets\data_table.py                                158    158     0%   6-363
src\gui\widgets\effects.py                                    43     43     0%   6-89
src\gui\widgets\empty_state.py                                29     29     0%   6-63
src\gui\widgets\excel_table.py                               232    232     0%   6-405
src\gui\widgets\footer\__init__.py                             6      6     0%   1-7
src\gui\widgets\footer\business_info.py                       88     88     0%   6-152
src\gui\widgets\footer\components.py                          57     57     0%   6-166
src\gui\widgets\footer\manager.py                             20     20     0%   6-68
src\gui\widgets\footer\status_bar.py                          36     36     0%   6-75
src\gui\widgets\footer\telemetry.py                           55     55     0%   6-87
src\gui\widgets\info_widgets.py                               92     92     0%   6-178
src\gui\widgets\message_bubble.py                             54     54     0%   7-140
src\gui\widgets\modern_button.py                              67     67     0%   5-158
src\gui\widgets\modern_card.py                                42     42     0%   6-86
src\gui\widgets\multi_select_filter.py                        99     99     0%   6-168
src\gui\widgets\notification_card.py                         116    116     0%   7-199
src\gui\widgets\notification_group_header.py                  48     48     0%   6-142
src\gui\widgets\notification_item.py                          74     74     0%   1-142
src\gui\widgets\notification_toolbar.py                      131    131     0%   6-283
src\gui\widgets\pdl_timeline.py                              129    129     0%   1-216
src\gui\widgets\priority_badge.py                             48     48     0%   6-112
src\gui\widgets\quick_actions.py                              78     78     0%   1-352
src\gui\widgets\security_dashboard.py                        159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                             30     30     0%   6-53
src\gui\widgets\sidebar_button.py                             57     57     0%   6-125
src\gui\widgets\sidebar_widget.py                            267    267     0%   7-406
src\gui\widgets\simple_chart.py                               67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                        47     47     0%   1-93
src\gui\widgets\statistics_widget.py                         108    108     0%   1-205
src\gui\widgets\status_card.py                                60     60     0%   6-122
src\gui\widgets\status_indicator.py                           46     46     0%   6-83
src\gui\widgets\timeline_widget.py                           118    118     0%   7-198
src\gui\widgets\toast.py                                     157    157     0%   5-327
src\gui\widgets\update_banner.py                              85     85     0%   1-161
src\utils\__init__.py                                          2      0   100%
src\utils\animation_helpers.py                               100    100     0%   6-295
src\utils\date_utils.py                                       74     74     0%   6-234
src\utils\document_generator.py                               18     18     0%   5-41
src\utils\document_processor.py                               66     22    67%   13-14, 24, 37, 41-42, 56-57, 59-60, 64-65, 73-74, 76-78, 84-89
src\utils\helpers.py                                         128    106    17%   23-25, 30-34, 48-70, 83-85, 90, 107-108, 113, 126-141, 148, 155-159, 166-175, 182-195, 203-235, 242-261
src\utils\log_humanizer.py                                    43     43     0%   7-100
src\utils\parsing.py                                          51     51     0%   6-98
src\utils\printing.py                                         88     88     0%   1-149
src\utils\resource_manager.py                                 86     86     0%   7-205
src\utils\secure_logger.py                                    23     23     0%   5-71
src\utils\security.py                                         78     78     0%   6-140
src\utils\system_telemetry.py                                 26     26     0%   6-74
src\utils\validators.py                                       73     73     0%   7-270
----------------------------------------------------------------------------------------
TOTAL                                                      19369  19058     2%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_document_processor_coverage.py::TestDocumentProcessorCoverage::test_get_pages_as_images_limit
============================== 1 failed in 7.42s ==============================

```
</details>

---
### `tests/unit/test_document_processor_simple.py::TestDocumentProcessorSimple::test_get_pages_as_images_error`
**Error:** `FAILED tests/unit/test_document_processor_simple.py::TestDocumentProcessorSimple::test_get_pages_as_images_error`

**Timestamp:** `2026-03-18T11:42:22.255238`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_document_processor_simple.py F                           [100%]

================================== FAILURES ===================================
_________ TestDocumentProcessorSimple.test_get_pages_as_images_error __________
tests\unit\test_document_processor_simple.py:44: in test_get_pages_as_images_error
    res = DocumentProcessor.get_pages_as_images(Path("invalid.pdf"))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: type object 'DocumentProcessor' has no attribute 'get_pages_as_images'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                       Stmts   Miss  Cover   Missing
----------------------------------------------------------------------------------------
src\bots\__init__.py                                          24     24     0%   6-162
src\bots\base\__init__.py                                      2      2     0%   5-7
src\bots\base\base_bot.py                                    338    338     0%   9-583
src\bots\base\login_page.py                                   94     94     0%   6-154
src\bots\base\wait_helpers.py                                 99     99     0%   14-252
src\core\__init__.py                                           2      0   100%
src\core\app_initializer.py                                  149    149     0%   10-263
src\core\app_updater.py                                        9      9     0%   7-35
src\core\audit\__init__.py                                     3      3     0%   1-4
src\core\audit\database.py                                   101    101     0%   1-200
src\core\audit\integrity.py                                   16     16     0%   1-27
src\core\audit\manager.py                                    162    162     0%   1-331
src\core\audit\models.py                                       9      9     0%   1-17
src\core\audit\signals.py                                     25     25     0%   1-48
src\core\audit_manager.py                                      5      5     0%   6-11
src\core\auth_monitor.py                                      73     73     0%   6-132
src\core\backup_manager.py                                   138    138     0%   6-250
src\core\bug_reporter.py                                     157    157     0%   11-339
src\core\config\account_manager.py                            53     46    13%   16-38, 43-53, 58-64, 71-91
src\core\config\defaults.py                                    3      0   100%
src\core\config\migration.py                                  69     56    19%   23-30, 35-86, 91-108
src\core\config\security.py                                   44     37    16%   14-15, 20-43, 48-49, 54-78
src\core\config_manager.py                                   164    121    26%   48-49, 54, 59, 65-86, 91-111, 117-128, 133-143, 149, 154, 162-164, 169, 174-176, 181-183, 188-190, 195-199, 204-207, 212-214, 219-221, 226-235, 240-251, 257-259, 264-290
src\core\constants.py                                        125      0   100%
src\core\contabilita_manager.py                              115    115     0%   6-242
src\core\contabilita_queries.py                               82     82     0%   6-122
src\core\contabilita_search.py                                92     92     0%   6-185
src\core\contabilita_stats.py                                 59     59     0%   6-101
src\core\contabilita_worker.py                               102    102     0%   1-216
src\core\data_synchronizer.py                                 25     25     0%   7-63
src\core\database\__init__.py                                  3      3     0%   1-4
src\core\database\manager.py                                 123    123     0%   6-236
src\core\database\pdl_queries.py                              92     92     0%   6-209
src\core\employees.py                                         98     98     0%   1-196
src\core\excel_importer.py                                     4      4     0%   6-11
src\core\importers\__init__.py                                44     44     0%   1-106
src\core\importers\attivita.py                                67     67     0%   1-117
src\core\importers\base.py                                    60     60     0%   1-88
src\core\importers\certificati.py                            126    126     0%   1-200
src\core\importers\contabilita.py                            133    133     0%   1-245
src\core\importers\giornaliere.py                            181    181     0%   1-290
src\core\importers\pdl_sync_manager.py                       163    163     0%   6-246
src\core\importers\scarico_ore.py                            189    189     0%   1-337
src\core\importers\storico_oda.py                             81     81     0%   1-185
src\core\license_updater.py                                  192    192     0%   7-323
src\core\license_validator.py                                176    176     0%   8-302
src\core\logging\__init__.py                                  10     10     0%   6-37
src\core\logging\alert_manager.py                            115    115     0%   7-240
src\core\logging\analytics.py                                136    136     0%   7-343
src\core\logging\config.py                                    37     37     0%   5-86
src\core\logging\context.py                                   57     57     0%   5-161
src\core\logging\decorators.py                                74     74     0%   6-201
src\core\logging\filters.py                                   60     60     0%   5-206
src\core\logging\formatters.py                                83     83     0%   5-240
src\core\logging\logger.py                                   116    116     0%   5-307
src\core\logging\metadata.py                                  86     86     0%   5-198
src\core\logging\metrics.py                                   74     74     0%   5-219
src\core\logging\migration.py                                 42     42     0%   5-120
src\core\logging\sampling.py                                  54     54     0%   5-201
src\core\logging\sinks.py                                    100    100     0%   5-236
src\core\logging\viewer.py                                   177    177     0%   7-362
src\core\notification_manager.py                             116    116     0%   8-243
src\core\oda_manager.py                                       42     42     0%   7-112
src\core\preventivi_manager.py                               196    196     0%   8-312
src\core\report_history.py                                    68     68     0%   7-158
src\core\schemas.py                                           57     57     0%   1-87
src\core\secrets_manager.py                                  105     67    36%   30-77, 85-89, 97-116, 120-123, 127-136, 140-142, 146-150, 158-169, 174-179, 184-188, 193-196, 201-207
src\core\stats_manager.py                                     70     70     0%   1-125
src\core\sync\__init__.py                                      0      0   100%
src\core\sync\base.py                                         23     23     0%   6-37
src\core\sync\contabilita_sync.py                             70     70     0%   6-127
src\core\sync\operazioni_sync.py                              42     42     0%   6-71
src\core\sync\smart_sync.py                                   25     25     0%   6-54
src\core\sync_tracker.py                                      77     77     0%   8-161
src\core\telegram\__init__.py                                  2      2     0%   1-3
src\core\telegram\bridge\__init__.py                           0      0   100%
src\core\telegram\bridge\data_processor.py                    76     76     0%   6-118
src\core\telegram\bridge\intent_handler.py                    75     75     0%   6-125
src\core\telegram\bridge\system_handler.py                   103    103     0%   6-139
src\core\telegram\bridge\ui_commands.py                      104    104     0%   6-144
src\core\telegram\service.py                                 205    205     0%   1-314
src\core\telegram_bridge.py                                   34     34     0%   7-84
src\core\telegram_manager.py                                   2      2     0%   6-8
src\core\time_manager.py                                      20     20     0%   6-57
src\core\timesheet_processor.py                               98     98     0%   6-164
src\core\updater\__init__.py                                   0      0   100%
src\core\updater\engine.py                                   165    165     0%   6-249
src\core\updater\gui.py                                      163    163     0%   6-273
src\core\version.py                                            5      0   100%
src\gui\__init__.py                                            0      0   100%
src\gui\cleanup_final.py                                      57     57     0%   8-121
src\gui\dialogs\__init__.py                                    0      0   100%
src\gui\dialogs\account_dialog.py                             69     69     0%   1-137
src\gui\dialogs\audit_detail_dialog.py                        61     61     0%   1-123
src\gui\dialogs\bug_report_dialog.py                         228    228     0%   7-455
src\gui\dialogs\certificati_analysis_dialog.py               225    225     0%   6-498
src\gui\dialogs\command_palette.py                           298    298     0%   7-432
src\gui\dialogs\confirmation_dialog.py                        96     96     0%   7-201
src\gui\dialogs\quick_actions_config.py                       91     91     0%   1-216
src\gui\dialogs\splash_standalone.py                          81     81     0%   8-133
src\gui\dialogs\standard_input_dialog.py                      40     40     0%   1-91
src\gui\dialogs\startup_dialog.py                            262    262     0%   6-412
src\gui\formatters.py                                        135    135     0%   1-248
src\gui\main_window\__init__.py                                2      2     0%   1-3
src\gui\main_window\components\__init__.py                     0      0   100%
src\gui\main_window\components\menu_bar.py                    75     75     0%   7-323
src\gui\main_window\components\status_bar.py                 132    132     0%   7-232
src\gui\main_window\components\tool_bar.py                    82     82     0%   7-187
src\gui\main_window\components\tray_icon.py                   17     17     0%   7-62
src\gui\main_window\controllers\__init__.py                    0      0   100%
src\gui\main_window\controllers\app_event_handler.py          37     37     0%   6-90
src\gui\main_window\controllers\monitoring_controller.py      36     36     0%   6-65
src\gui\main_window\controllers\signal_connector.py           19     19     0%   7-65
src\gui\main_window\controllers\workflow_controller.py        83     83     0%   6-155
src\gui\main_window\main.py                                  252    252     0%   7-474
src\gui\main_window\page_index.py                             28     28     0%   7-53
src\gui\panels\__init__.py                                    21     21     0%   6-27
src\gui\panels\base.py                                       281    281     0%   6-537
src\gui\panels\carico_ts.py                                   89     89     0%   6-176
src\gui\panels\consuntivo_panel.py                            46     46     0%   7-77
src\gui\panels\contabilita_kpi\__init__.py                     2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py                   14     14     0%   1-32
src\gui\panels\contabilita_kpi\charts.py                     213    213     0%   1-400
src\gui\panels\contabilita_kpi\kpi_panel.py                  161    161     0%   1-309
src\gui\panels\contabilita_panel.py                          266    266     0%   8-433
src\gui\panels\dashboard_panel.py                            128    128     0%   7-247
src\gui\panels\dettagli_oda.py                               181    181     0%   8-340
src\gui\panels\dipendenti\__init__.py                          2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                       28     28     0%   7-77
src\gui\panels\dipendenti\shared.py                          152    152     0%   6-329
src\gui\panels\dipendenti_manager_panel.py                   206    206     0%   1-369
src\gui\panels\health_panel.py                               275    275     0%   8-437
src\gui\panels\help_panel.py                                 137    137     0%   6-365
src\gui\panels\notifications_panel.py                        243    243     0%   7-406
src\gui\panels\pdl\__init__.py                                 2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                            17     17     0%   1-27
src\gui\panels\pdl\pdl_detail_view.py                         80     80     0%   7-144
src\gui\panels\pdl\pdl_filter_widget.py                      119    119     0%   1-186
src\gui\panels\pdl\pdl_panel.py                              189    189     0%   7-325
src\gui\panels\pdl\programmazione_tab.py                     218    218     0%   6-341
src\gui\panels\prenota_bp.py                                 142    142     0%   9-272
src\gui\panels\ricerca_pdl.py                                109    109     0%   6-214
src\gui\panels\scarico_ore_panel.py                          131    131     0%   7-261
src\gui\panels\scarico_pdl.py                                229    229     0%   7-450
src\gui\panels\scarico_ts.py                                 137    137     0%   6-266
src\gui\panels\storico_oda\__init__.py                         2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                    43     43     0%   1-77
src\gui\panels\storico_oda\oda_detail_view.py                 49     49     0%   1-75
src\gui\panels\storico_oda\oda_filter_widget.py               62     62     0%   1-114
src\gui\panels\storico_oda\oda_panel.py                      155    155     0%   8-292
src\gui\panels\timbrature\__init__.py                          2      2     0%   1-3
src\gui\panels\timbrature\panel.py                           221    221     0%   1-380
src\gui\panels\timbrature_bot.py                             106    106     0%   8-202
src\gui\panels\timbrature_db.py                                2      2     0%   6-8
src\gui\styles\__init__.py                                     4      4     0%   6-45
src\gui\styles\constants.py                                    9      9     0%   9-198
src\gui\styles\notification_styles.py                         10     10     0%   6-53
src\gui\styles\palette_helpers.py                             10     10     0%   6-25
src\gui\styles\theme_manager.py                               85     85     0%   6-175
src\gui\styles\widget_styles.py                               36     36     0%   6-392
src\gui\toast.py                                              46     46     0%   6-93
src\gui\widgets\__init__.py                                   19     19     0%   6-31
src\gui\widgets\activity_feed.py                             138    138     0%   1-321
src\gui\widgets\animated_progress_bar.py                      79     79     0%   7-174
src\gui\widgets\audit_log_widget.py                          120    120     0%   7-194
src\gui\widgets\automazioni_widget.py                         59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                          4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                    143    143     0%   1-383
src\gui\widgets\autopilot\event_card.py                      144    144     0%   1-293
src\gui\widgets\autopilot\main_widget.py                     208    208     0%   7-394
src\gui\widgets\bot_parameters.py                            222    222     0%   6-396
src\gui\widgets\calendar_date_edit.py                         18     18     0%   6-77
src\gui\widgets\core_widgets.py                              106    106     0%   8-389
src\gui\widgets\dashboard_stat_card.py                        49     49     0%   6-111
src\gui\widgets\data_table.py                                158    158     0%   6-363
src\gui\widgets\effects.py                                    43     43     0%   6-89
src\gui\widgets\empty_state.py                                29     29     0%   6-63
src\gui\widgets\excel_table.py                               232    232     0%   6-405
src\gui\widgets\footer\__init__.py                             6      6     0%   1-7
src\gui\widgets\footer\business_info.py                       88     88     0%   6-152
src\gui\widgets\footer\components.py                          57     57     0%   6-166
src\gui\widgets\footer\manager.py                             20     20     0%   6-68
src\gui\widgets\footer\status_bar.py                          36     36     0%   6-75
src\gui\widgets\footer\telemetry.py                           55     55     0%   6-87
src\gui\widgets\info_widgets.py                               92     92     0%   6-178
src\gui\widgets\message_bubble.py                             54     54     0%   7-140
src\gui\widgets\modern_button.py                              67     67     0%   5-158
src\gui\widgets\modern_card.py                                42     42     0%   6-86
src\gui\widgets\multi_select_filter.py                        99     99     0%   6-168
src\gui\widgets\notification_card.py                         116    116     0%   7-199
src\gui\widgets\notification_group_header.py                  48     48     0%   6-142
src\gui\widgets\notification_item.py                          74     74     0%   1-142
src\gui\widgets\notification_toolbar.py                      131    131     0%   6-283
src\gui\widgets\pdl_timeline.py                              129    129     0%   1-216
src\gui\widgets\priority_badge.py                             48     48     0%   6-112
src\gui\widgets\quick_actions.py                              78     78     0%   1-352
src\gui\widgets\security_dashboard.py                        159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                             30     30     0%   6-53
src\gui\widgets\sidebar_button.py                             57     57     0%   6-125
src\gui\widgets\sidebar_widget.py                            267    267     0%   7-406
src\gui\widgets\simple_chart.py                               67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                        47     47     0%   1-93
src\gui\widgets\statistics_widget.py                         108    108     0%   1-205
src\gui\widgets\status_card.py                                60     60     0%   6-122
src\gui\widgets\status_indicator.py                           46     46     0%   6-83
src\gui\widgets\timeline_widget.py                           118    118     0%   7-198
src\gui\widgets\toast.py                                     157    157     0%   5-327
src\gui\widgets\update_banner.py                              85     85     0%   1-161
src\utils\__init__.py                                          2      0   100%
src\utils\animation_helpers.py                               100    100     0%   6-295
src\utils\date_utils.py                                       74     74     0%   6-234
src\utils\document_generator.py                               18     18     0%   5-41
src\utils\document_processor.py                               66     15    77%   13-14, 24, 37, 41-42, 59-60, 73-74, 84-89
src\utils\helpers.py                                         128    106    17%   23-25, 30-34, 48-70, 83-85, 90, 107-108, 113, 126-141, 148, 155-159, 166-175, 182-195, 203-235, 242-261
src\utils\log_humanizer.py                                    43     43     0%   7-100
src\utils\parsing.py                                          51     51     0%   6-98
src\utils\printing.py                                         88     88     0%   1-149
src\utils\resource_manager.py                                 86     86     0%   7-205
src\utils\secure_logger.py                                    23     23     0%   5-71
src\utils\security.py                                         78     78     0%   6-140
src\utils\system_telemetry.py                                 26     26     0%   6-74
src\utils\validators.py                                       73     73     0%   7-270
----------------------------------------------------------------------------------------
TOTAL                                                      19369  19051     2%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_document_processor_simple.py::TestDocumentProcessorSimple::test_get_pages_as_images_error
============================== 1 failed in 6.33s ==============================

```
</details>

---
### `tests/unit/test_excel_importer_refactoring.py::test_import_certificati_campione_success`
**Error:** `FAILED tests/unit/test_excel_importer_refactoring.py::test_import_certificati_campione_success`

**Timestamp:** `2026-03-18T11:51:35.093187`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_excel_importer_refactoring.py F                          [100%]

================================== FAILURES ===================================
__________________ test_import_certificati_campione_success ___________________
tests\unit\test_excel_importer_refactoring.py:500: in test_import_certificati_campione_success
    assert rows[0][0] == "M1"
E   AssertionError: assert 'ID1' == 'M1'
E     
E     - M1
E     + ID1
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                       Stmts   Miss  Cover   Missing
----------------------------------------------------------------------------------------
src\bots\__init__.py                                          24     24     0%   6-162
src\bots\base\__init__.py                                      2      2     0%   5-7
src\bots\base\base_bot.py                                    338    338     0%   9-583
src\bots\base\login_page.py                                   94     94     0%   6-154
src\bots\base\wait_helpers.py                                 99     99     0%   14-252
src\core\__init__.py                                           2      0   100%
src\core\app_initializer.py                                  149    149     0%   10-263
src\core\app_updater.py                                        9      9     0%   7-35
src\core\audit\__init__.py                                     3      3     0%   1-4
src\core\audit\database.py                                   101    101     0%   1-200
src\core\audit\integrity.py                                   16     16     0%   1-27
src\core\audit\manager.py                                    162    162     0%   1-331
src\core\audit\models.py                                       9      9     0%   1-17
src\core\audit\signals.py                                     25     25     0%   1-48
src\core\audit_manager.py                                      5      5     0%   6-11
src\core\auth_monitor.py                                      73     73     0%   6-132
src\core\backup_manager.py                                   138    138     0%   6-250
src\core\bug_reporter.py                                     157    157     0%   11-339
src\core\config\account_manager.py                            53     46    13%   16-38, 43-53, 58-64, 71-91
src\core\config\defaults.py                                    3      0   100%
src\core\config\migration.py                                  69     54    22%   23-30, 35-86, 94-108
src\core\config\security.py                                   44     33    25%   23-43, 48-49, 54-78
src\core\config_manager.py                                   164    101    38%   48-49, 54, 67, 74, 83, 103-109, 117-128, 133-143, 149, 154, 162-164, 169, 174-176, 181-183, 188-190, 195-199, 204-207, 212-214, 219-221, 226-235, 240-251, 257-259, 264-290
src\core\constants.py                                        125      0   100%
src\core\contabilita_manager.py                              115    115     0%   6-242
src\core\contabilita_queries.py                               82     82     0%   6-122
src\core\contabilita_search.py                                92     92     0%   6-185
src\core\contabilita_stats.py                                 59     59     0%   6-101
src\core\contabilita_worker.py                               102    102     0%   1-216
src\core\data_synchronizer.py                                 25     25     0%   7-63
src\core\database\__init__.py                                  3      0   100%
src\core\database\manager.py                                 123     78    37%   117-152, 158-188, 192-196, 199-203, 206, 214-233
src\core\database\migrations\contabilita.py                   34     27    21%   7-68, 73-77, 82-122, 129-142, 149-154
src\core\database\migrations\dipendenti.py                    17     13    24%   6-21, 26-28, 33-39
src\core\database\migrations\pdl.py                           34     27    21%   7-38, 43-91, 96-116, 121-125, 132-134
src\core\database\migrations\storico_oda.py                   11      8    27%   6-49, 56-58
src\core\database\migrations\timbrature.py                    27     22    19%   6-25, 30-32, 37-47, 52-69
src\core\database\pdl_queries.py                              92     77    16%   23-37, 43-95, 100-136, 144-209
src\core\employees.py                                         98     13    87%   61-63, 118-120, 129-130, 174-175, 190-192
src\core\excel_importer.py                                     4      0   100%
src\core\importers\__init__.py                                44      0   100%
src\core\importers\attivita.py                                67      5    93%   58-59, 77, 92-93
src\core\importers\base.py                                    60      7    88%   15-16, 24-26, 57-58
src\core\importers\certificati.py                            126     18    86%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-181, 190-192
src\core\importers\contabilita.py                            133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                            181     37    80%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 223-226, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                       163    163     0%   6-246
src\core\importers\scarico_ore.py                            189     35    81%   14-15, 22-24, 63, 79-80, 86-101, 122, 125, 137-138, 152, 200, 228, 232, 241, 245, 258, 274, 283, 316
src\core\importers\storico_oda.py                             81     16    80%   60, 66, 71, 84-85, 95-96, 176-185
src\core\license_updater.py                                  192    192     0%   7-323
src\core\license_validator.py                                176    176     0%   8-302
src\core\logging\__init__.py                                  10     10     0%   6-37
src\core\logging\alert_manager.py                            115    115     0%   7-240
src\core\logging\analytics.py                                136    136     0%   7-343
src\core\logging\config.py                                    37     37     0%   5-86
src\core\logging\context.py                                   57     57     0%   5-161
src\core\logging\decorators.py                                74     74     0%   6-201
src\core\logging\filters.py                                   60     60     0%   5-206
src\core\logging\formatters.py                                83     83     0%   5-240
src\core\logging\logger.py                                   116    116     0%   5-307
src\core\logging\metadata.py                                  86     86     0%   5-198
src\core\logging\metrics.py                                   74     74     0%   5-219
src\core\logging\migration.py                                 42     42     0%   5-120
src\core\logging\sampling.py                                  54     54     0%   5-201
src\core\logging\sinks.py                                    100    100     0%   5-236
src\core\logging\viewer.py                                   177    177     0%   7-362
src\core\notification_manager.py                             116    116     0%   8-243
src\core\oda_manager.py                                       42     42     0%   7-112
src\core\preventivi_manager.py                               196    196     0%   8-312
src\core\report_history.py                                    68     68     0%   7-158
src\core\schemas.py                                           57      5    91%   71-73, 79, 86
src\core\secrets_manager.py                                  105     67    36%   30-77, 85-89, 97-116, 120-123, 127-136, 140-142, 146-150, 158-169, 174-179, 184-188, 193-196, 201-207
src\core\stats_manager.py                                     70     70     0%   1-125
src\core\sync\__init__.py                                      0      0   100%
src\core\sync\base.py                                         23     23     0%   6-37
src\core\sync\contabilita_sync.py                             70     70     0%   6-127
src\core\sync\operazioni_sync.py                              42     42     0%   6-71
src\core\sync\smart_sync.py                                   25     25     0%   6-54
src\core\sync_tracker.py                                      77     47    39%   40-51, 56-60, 73-86, 91-102, 107-119, 132-135, 149-161
src\core\telegram\__init__.py                                  2      2     0%   1-3
src\core\telegram\bridge\__init__.py                           0      0   100%
src\core\telegram\bridge\data_processor.py                    76     76     0%   6-118
src\core\telegram\bridge\intent_handler.py                    75     75     0%   6-125
src\core\telegram\bridge\system_handler.py                   103    103     0%   6-139
src\core\telegram\bridge\ui_commands.py                      104    104     0%   6-144
src\core\telegram\service.py                                 205    205     0%   1-314
src\core\telegram_bridge.py                                   34     34     0%   7-84
src\core\telegram_manager.py                                   2      2     0%   6-8
src\core\time_manager.py                                      20     20     0%   6-57
src\core\timesheet_processor.py                               98     98     0%   6-164
src\core\updater\__init__.py                                   0      0   100%
src\core\updater\engine.py                                   165    165     0%   6-249
src\core\updater\gui.py                                      163    163     0%   6-273
src\core\version.py                                            5      0   100%
src\gui\__init__.py                                            0      0   100%
src\gui\cleanup_final.py                                      57     57     0%   8-121
src\gui\dialogs\__init__.py                                    0      0   100%
src\gui\dialogs\account_dialog.py                             69     69     0%   1-137
src\gui\dialogs\audit_detail_dialog.py                        61     61     0%   1-123
src\gui\dialogs\bug_report_dialog.py                         228    228     0%   7-455
src\gui\dialogs\certificati_analysis_dialog.py               225    225     0%   6-498
src\gui\dialogs\command_palette.py                           298    298     0%   7-432
src\gui\dialogs\confirmation_dialog.py                        96     96     0%   7-201
src\gui\dialogs\quick_actions_config.py                       91     91     0%   1-216
src\gui\dialogs\splash_standalone.py                          81     81     0%   8-133
src\gui\dialogs\standard_input_dialog.py                      40     40     0%   1-91
src\gui\dialogs\startup_dialog.py                            262    262     0%   6-412
src\gui\formatters.py                                        135    135     0%   1-248
src\gui\main_window\__init__.py                                2      2     0%   1-3
src\gui\main_window\components\__init__.py                     0      0   100%
src\gui\main_window\components\menu_bar.py                    75     75     0%   7-323
src\gui\main_window\components\status_bar.py                 132    132     0%   7-232
src\gui\main_window\components\tool_bar.py                    82     82     0%   7-187
src\gui\main_window\components\tray_icon.py                   17     17     0%   7-62
src\gui\main_window\controllers\__init__.py                    0      0   100%
src\gui\main_window\controllers\app_event_handler.py          37     37     0%   6-90
src\gui\main_window\controllers\monitoring_controller.py      36     36     0%   6-65
src\gui\main_window\controllers\signal_connector.py           19     19     0%   7-65
src\gui\main_window\controllers\workflow_controller.py        83     83     0%   6-155
src\gui\main_window\main.py                                  252    252     0%   7-474
src\gui\main_window\page_index.py                             28     28     0%   7-53
src\gui\panels\__init__.py                                    21     21     0%   6-27
src\gui\panels\base.py                                       281    281     0%   6-537
src\gui\panels\carico_ts.py                                   89     89     0%   6-176
src\gui\panels\consuntivo_panel.py                            46     46     0%   7-77
src\gui\panels\contabilita_kpi\__init__.py                     2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py                   14     14     0%   1-32
src\gui\panels\contabilita_kpi\charts.py                     213    213     0%   1-400
src\gui\panels\contabilita_kpi\kpi_panel.py                  161    161     0%   1-309
src\gui\panels\contabilita_panel.py                          266    266     0%   8-433
src\gui\panels\dashboard_panel.py                            128    128     0%   7-247
src\gui\panels\dettagli_oda.py                               181    181     0%   8-340
src\gui\panels\dipendenti\__init__.py                          2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                       28     28     0%   7-77
src\gui\panels\dipendenti\shared.py                          152    152     0%   6-329
src\gui\panels\dipendenti_manager_panel.py                   206    206     0%   1-369
src\gui\panels\health_panel.py                               275    275     0%   8-437
src\gui\panels\help_panel.py                                 137    137     0%   6-365
src\gui\panels\notifications_panel.py                        243    243     0%   7-406
src\gui\panels\pdl\__init__.py                                 2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                            17     17     0%   1-27
src\gui\panels\pdl\pdl_detail_view.py                         80     80     0%   7-144
src\gui\panels\pdl\pdl_filter_widget.py                      119    119     0%   1-186
src\gui\panels\pdl\pdl_panel.py                              189    189     0%   7-325
src\gui\panels\pdl\programmazione_tab.py                     218    218     0%   6-341
src\gui\panels\prenota_bp.py                                 142    142     0%   9-272
src\gui\panels\ricerca_pdl.py                                109    109     0%   6-214
src\gui\panels\scarico_ore_panel.py                          131    131     0%   7-261
src\gui\panels\scarico_pdl.py                                229    229     0%   7-450
src\gui\panels\scarico_ts.py                                 137    137     0%   6-266
src\gui\panels\storico_oda\__init__.py                         2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                    43     43     0%   1-77
src\gui\panels\storico_oda\oda_detail_view.py                 49     49     0%   1-75
src\gui\panels\storico_oda\oda_filter_widget.py               62     62     0%   1-114
src\gui\panels\storico_oda\oda_panel.py                      155    155     0%   8-292
src\gui\panels\timbrature\__init__.py                          2      2     0%   1-3
src\gui\panels\timbrature\panel.py                           221    221     0%   1-380
src\gui\panels\timbrature_bot.py                             106    106     0%   8-202
src\gui\panels\timbrature_db.py                                2      2     0%   6-8
src\gui\styles\__init__.py                                     4      4     0%   6-45
src\gui\styles\constants.py                                    9      9     0%   9-198
src\gui\styles\notification_styles.py                         10     10     0%   6-53
src\gui\styles\palette_helpers.py                             10     10     0%   6-25
src\gui\styles\theme_manager.py                               85     85     0%   6-175
src\gui\styles\widget_styles.py                               36     36     0%   6-392
src\gui\toast.py                                              46     46     0%   6-93
src\gui\widgets\__init__.py                                   19     19     0%   6-31
src\gui\widgets\activity_feed.py                             138    138     0%   1-321
src\gui\widgets\animated_progress_bar.py                      79     79     0%   7-174
src\gui\widgets\audit_log_widget.py                          120    120     0%   7-194
src\gui\widgets\automazioni_widget.py                         59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                          4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                    143    143     0%   1-383
src\gui\widgets\autopilot\event_card.py                      144    144     0%   1-293
src\gui\widgets\autopilot\main_widget.py                     208    208     0%   7-394
src\gui\widgets\bot_parameters.py                            222    222     0%   6-396
src\gui\widgets\calendar_date_edit.py                         18     18     0%   6-77
src\gui\widgets\core_widgets.py                              106    106     0%   8-389
src\gui\widgets\dashboard_stat_card.py                        49     49     0%   6-111
src\gui\widgets\data_table.py                                158    158     0%   6-363
src\gui\widgets\effects.py                                    43     43     0%   6-89
src\gui\widgets\empty_state.py                                29     29     0%   6-63
src\gui\widgets\excel_table.py                               232    232     0%   6-405
src\gui\widgets\footer\__init__.py                             6      6     0%   1-7
src\gui\widgets\footer\business_info.py                       88     88     0%   6-152
src\gui\widgets\footer\components.py                          57     57     0%   6-166
src\gui\widgets\footer\manager.py                             20     20     0%   6-68
src\gui\widgets\footer\status_bar.py                          36     36     0%   6-75
src\gui\widgets\footer\telemetry.py                           55     55     0%   6-87
src\gui\widgets\info_widgets.py                               92     92     0%   6-178
src\gui\widgets\message_bubble.py                             54     54     0%   7-140
src\gui\widgets\modern_button.py                              67     67     0%   5-158
src\gui\widgets\modern_card.py                                42     42     0%   6-86
src\gui\widgets\multi_select_filter.py                        99     99     0%   6-168
src\gui\widgets\notification_card.py                         116    116     0%   7-199
src\gui\widgets\notification_group_header.py                  48     48     0%   6-142
src\gui\widgets\notification_item.py                          74     74     0%   1-142
src\gui\widgets\notification_toolbar.py                      131    131     0%   6-283
src\gui\widgets\pdl_timeline.py                              129    129     0%   1-216
src\gui\widgets\priority_badge.py                             48     48     0%   6-112
src\gui\widgets\quick_actions.py                              78     78     0%   1-352
src\gui\widgets\security_dashboard.py                        159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                             30     30     0%   6-53
src\gui\widgets\sidebar_button.py                             57     57     0%   6-125
src\gui\widgets\sidebar_widget.py                            267    267     0%   7-406
src\gui\widgets\simple_chart.py                               67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                        47     47     0%   1-93
src\gui\widgets\statistics_widget.py                         108    108     0%   1-205
src\gui\widgets\status_card.py                                60     60     0%   6-122
src\gui\widgets\status_indicator.py                           46     46     0%   6-83
src\gui\widgets\timeline_widget.py                           118    118     0%   7-198
src\gui\widgets\toast.py                                     157    157     0%   5-327
src\gui\widgets\update_banner.py                              85     85     0%   1-161
src\utils\__init__.py                                          2      0   100%
src\utils\animation_helpers.py                               100    100     0%   6-295
src\utils\date_utils.py                                       74     74     0%   6-234
src\utils\document_generator.py                               18     18     0%   5-41
src\utils\document_processor.py                               66     15    77%   13-14, 24, 37, 41-42, 59-60, 73-74, 84-89
src\utils\helpers.py                                         128    106    17%   23-25, 30-34, 48-70, 83-85, 90, 107-108, 113, 126-141, 148, 155-159, 166-175, 182-195, 203-235, 242-261
src\utils\log_humanizer.py                                    43     43     0%   7-100
src\utils\parsing.py                                          51     51     0%   6-98
src\utils\printing.py                                         88     88     0%   1-149
src\utils\resource_manager.py                                 86     86     0%   7-205
src\utils\secure_logger.py                                    23     23     0%   5-71
src\utils\security.py                                         78     78     0%   6-140
src\utils\system_telemetry.py                                 26     26     0%   6-74
src\utils\validators.py                                       73     73     0%   7-270
----------------------------------------------------------------------------------------
TOTAL                                                      19492  18137     7%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_excel_importer_refactoring.py::test_import_certificati_campione_success
============================== 1 failed in 9.12s ==============================

```
</details>

---
### `tests/unit/test_excel_table_coverage.py::TestExcelTableCoverage::test_analyze_with_lyra_selection`
**Error:** `FAILED tests/unit/test_excel_table_coverage.py::TestExcelTableCoverage::test_analyze_with_lyra_selection`

**Timestamp:** `2026-03-18T11:54:18.930331`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_excel_table_coverage.py F                                [100%]

================================== FAILURES ===================================
___________ TestExcelTableCoverage.test_analyze_with_lyra_selection ___________
tests\unit\test_excel_table_coverage.py:91: in test_analyze_with_lyra_selection
    table._analyze_selection()
    ^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'ExcelTableWidget' object has no attribute '_analyze_selection'. Did you mean: 'paste_selection'?
============================== warnings summary ===============================
tests/unit/test_excel_table_coverage.py::TestExcelTableCoverage::test_analyze_with_lyra_selection
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\excel_table.py:47: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(*args, **kwargs)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                       Stmts   Miss  Cover   Missing
----------------------------------------------------------------------------------------
src\bots\__init__.py                                          24     24     0%   6-162
src\bots\base\__init__.py                                      2      2     0%   5-7
src\bots\base\base_bot.py                                    338    338     0%   9-583
src\bots\base\login_page.py                                   94     94     0%   6-154
src\bots\base\wait_helpers.py                                 99     99     0%   14-252
src\core\__init__.py                                           2      0   100%
src\core\app_initializer.py                                  149    149     0%   10-263
src\core\app_updater.py                                        9      9     0%   7-35
src\core\audit\__init__.py                                     3      3     0%   1-4
src\core\audit\database.py                                   101    101     0%   1-200
src\core\audit\integrity.py                                   16     16     0%   1-27
src\core\audit\manager.py                                    162    162     0%   1-331
src\core\audit\models.py                                       9      9     0%   1-17
src\core\audit\signals.py                                     25     25     0%   1-48
src\core\audit_manager.py                                      5      5     0%   6-11
src\core\auth_monitor.py                                      73     73     0%   6-132
src\core\backup_manager.py                                   138    138     0%   6-250
src\core\bug_reporter.py                                     157    157     0%   11-339
src\core\config\account_manager.py                            53     46    13%   16-38, 43-53, 58-64, 71-91
src\core\config\defaults.py                                    3      0   100%
src\core\config\migration.py                                  69     54    22%   23-30, 35-86, 94-108
src\core\config\security.py                                   44     33    25%   23-43, 48-49, 54-78
src\core\config_manager.py                                   164    101    38%   48-49, 54, 67, 74, 83, 103-109, 117-128, 133-143, 149, 154, 162-164, 169, 174-176, 181-183, 188-190, 195-199, 204-207, 212-214, 219-221, 226-235, 240-251, 257-259, 264-290
src\core\constants.py                                        125      0   100%
src\core\contabilita_manager.py                              115    115     0%   6-242
src\core\contabilita_queries.py                               82     82     0%   6-122
src\core\contabilita_search.py                                92     92     0%   6-185
src\core\contabilita_stats.py                                 59     59     0%   6-101
src\core\contabilita_worker.py                               102    102     0%   1-216
src\core\data_synchronizer.py                                 25     25     0%   7-63
src\core\database\__init__.py                                  3      0   100%
src\core\database\manager.py                                 123     78    37%   117-152, 158-188, 192-196, 199-203, 206, 214-233
src\core\database\migrations\contabilita.py                   34     27    21%   7-68, 73-77, 82-122, 129-142, 149-154
src\core\database\migrations\dipendenti.py                    17     13    24%   6-21, 26-28, 33-39
src\core\database\migrations\pdl.py                           34     27    21%   7-38, 43-91, 96-116, 121-125, 132-134
src\core\database\migrations\storico_oda.py                   11      8    27%   6-49, 56-58
src\core\database\migrations\timbrature.py                    27     22    19%   6-25, 30-32, 37-47, 52-69
src\core\database\pdl_queries.py                              92     77    16%   23-37, 43-95, 100-136, 144-209
src\core\employees.py                                         98     13    87%   61-63, 118-120, 129-130, 174-175, 190-192
src\core\excel_importer.py                                     4      0   100%
src\core\importers\__init__.py                                44      0   100%
src\core\importers\attivita.py                                67      5    93%   58-59, 77, 92-93
src\core\importers\base.py                                    60      7    88%   15-16, 24-26, 57-58
src\core\importers\certificati.py                            126     18    86%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-181, 190-192
src\core\importers\contabilita.py                            133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                            181     37    80%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 223-226, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                       163    163     0%   6-246
src\core\importers\scarico_ore.py                            189     35    81%   14-15, 22-24, 63, 79-80, 86-101, 122, 125, 137-138, 152, 200, 228, 232, 241, 245, 258, 274, 283, 316
src\core\importers\storico_oda.py                             81     16    80%   60, 66, 71, 84-85, 95-96, 176-185
src\core\license_updater.py                                  192    192     0%   7-323
src\core\license_validator.py                                176    176     0%   8-302
src\core\logging\__init__.py                                  10     10     0%   6-37
src\core\logging\alert_manager.py                            115    115     0%   7-240
src\core\logging\analytics.py                                136    136     0%   7-343
src\core\logging\config.py                                    37     37     0%   5-86
src\core\logging\context.py                                   57     57     0%   5-161
src\core\logging\decorators.py                                74     74     0%   6-201
src\core\logging\filters.py                                   60     60     0%   5-206
src\core\logging\formatters.py                                83     83     0%   5-240
src\core\logging\logger.py                                   116    116     0%   5-307
src\core\logging\metadata.py                                  86     86     0%   5-198
src\core\logging\metrics.py                                   74     74     0%   5-219
src\core\logging\migration.py                                 42     42     0%   5-120
src\core\logging\sampling.py                                  54     54     0%   5-201
src\core\logging\sinks.py                                    100    100     0%   5-236
src\core\logging\viewer.py                                   177    177     0%   7-362
src\core\notification_manager.py                             116     80    31%   53-57, 61-65, 69-77, 81-93, 97-101, 133-167, 179-181, 190, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda_manager.py                                       42     42     0%   7-112
src\core\preventivi_manager.py                               196    196     0%   8-312
src\core\report_history.py                                    68     68     0%   7-158
src\core\schemas.py                                           57      5    91%   71-73, 79, 86
src\core\secrets_manager.py                                  105     67    36%   30-77, 85-89, 97-116, 120-123, 127-136, 140-142, 146-150, 158-169, 174-179, 184-188, 193-196, 201-207
src\core\stats_manager.py                                     70     70     0%   1-125
src\core\sync\__init__.py                                      0      0   100%
src\core\sync\base.py                                         23     23     0%   6-37
src\core\sync\contabilita_sync.py                             70     70     0%   6-127
src\core\sync\operazioni_sync.py                              42     42     0%   6-71
src\core\sync\smart_sync.py                                   25     25     0%   6-54
src\core\sync_tracker.py                                      77     47    39%   40-51, 56-60, 73-86, 91-102, 107-119, 132-135, 149-161
src\core\telegram\__init__.py                                  2      2     0%   1-3
src\core\telegram\bridge\__init__.py                           0      0   100%
src\core\telegram\bridge\data_processor.py                    76     76     0%   6-118
src\core\telegram\bridge\intent_handler.py                    75     75     0%   6-125
src\core\telegram\bridge\system_handler.py                   103    103     0%   6-139
src\core\telegram\bridge\ui_commands.py                      104    104     0%   6-144
src\core\telegram\service.py                                 205    205     0%   1-314
src\core\telegram_bridge.py                                   34     34     0%   7-84
src\core\telegram_manager.py                                   2      2     0%   6-8
src\core\time_manager.py                                      20     20     0%   6-57
src\core\timesheet_processor.py                               98     98     0%   6-164
src\core\updater\__init__.py                                   0      0   100%
src\core\updater\engine.py                                   165    165     0%   6-249
src\core\updater\gui.py                                      163    163     0%   6-273
src\core\version.py                                            5      0   100%
src\gui\__init__.py                                            0      0   100%
src\gui\cleanup_final.py                                      57     57     0%   8-121
src\gui\design\colors.py                                      27      0   100%
src\gui\design\spacing.py                                     25      0   100%
src\gui\dialogs\__init__.py                                    0      0   100%
src\gui\dialogs\account_dialog.py                             69     69     0%   1-137
src\gui\dialogs\audit_detail_dialog.py                        61     61     0%   1-123
src\gui\dialogs\bug_report_dialog.py                         228    228     0%   7-455
src\gui\dialogs\certificati_analysis_dialog.py               225    225     0%   6-498
src\gui\dialogs\command_palette.py                           298    298     0%   7-432
src\gui\dialogs\confirmation_dialog.py                        96     96     0%   7-201
src\gui\dialogs\quick_actions_config.py                       91     91     0%   1-216
src\gui\dialogs\splash_standalone.py                          81     81     0%   8-133
src\gui\dialogs\standard_input_dialog.py                      40     40     0%   1-91
src\gui\dialogs\startup_dialog.py                            262    262     0%   6-412
src\gui\formatters.py                                        135    135     0%   1-248
src\gui\main_window\__init__.py                                2      2     0%   1-3
src\gui\main_window\components\__init__.py                     0      0   100%
src\gui\main_window\components\menu_bar.py                    75     75     0%   7-323
src\gui\main_window\components\status_bar.py                 132    132     0%   7-232
src\gui\main_window\components\tool_bar.py                    82     82     0%   7-187
src\gui\main_window\components\tray_icon.py                   17     17     0%   7-62
src\gui\main_window\controllers\__init__.py                    0      0   100%
src\gui\main_window\controllers\app_event_handler.py          37     37     0%   6-90
src\gui\main_window\controllers\monitoring_controller.py      36     36     0%   6-65
src\gui\main_window\controllers\signal_connector.py           19     19     0%   7-65
src\gui\main_window\controllers\workflow_controller.py        83     83     0%   6-155
src\gui\main_window\main.py                                  252    252     0%   7-474
src\gui\main_window\page_index.py                             28     28     0%   7-53
src\gui\panels\__init__.py                                    21     21     0%   6-27
src\gui\panels\base.py                                       281    281     0%   6-537
src\gui\panels\carico_ts.py                                   89     89     0%   6-176
src\gui\panels\consuntivo_panel.py                            46     46     0%   7-77
src\gui\panels\contabilita_kpi\__init__.py                     2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py                   14     14     0%   1-32
src\gui\panels\contabilita_kpi\charts.py                     213    213     0%   1-400
src\gui\panels\contabilita_kpi\kpi_panel.py                  161    161     0%   1-309
src\gui\panels\contabilita_panel.py                          266    266     0%   8-433
src\gui\panels\dashboard_panel.py                            128    128     0%   7-247
src\gui\panels\dettagli_oda.py                               181    181     0%   8-340
src\gui\panels\dipendenti\__init__.py                          2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                       28     28     0%   7-77
src\gui\panels\dipendenti\shared.py                          152    152     0%   6-329
src\gui\panels\dipendenti_manager_panel.py                   206    206     0%   1-369
src\gui\panels\health_panel.py                               275    275     0%   8-437
src\gui\panels\help_panel.py                                 137    137     0%   6-365
src\gui\panels\notifications_panel.py                        243    243     0%   7-406
src\gui\panels\pdl\__init__.py                                 2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                            17     17     0%   1-27
src\gui\panels\pdl\pdl_detail_view.py                         80     80     0%   7-144
src\gui\panels\pdl\pdl_filter_widget.py                      119    119     0%   1-186
src\gui\panels\pdl\pdl_panel.py                              189    189     0%   7-325
src\gui\panels\pdl\programmazione_tab.py                     218    218     0%   6-341
src\gui\panels\prenota_bp.py                                 142    142     0%   9-272
src\gui\panels\ricerca_pdl.py                                109    109     0%   6-214
src\gui\panels\scarico_ore_panel.py                          131    131     0%   7-261
src\gui\panels\scarico_pdl.py                                229    229     0%   7-450
src\gui\panels\scarico_ts.py                                 137    137     0%   6-266
src\gui\panels\storico_oda\__init__.py                         2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                    43     43     0%   1-77
src\gui\panels\storico_oda\oda_detail_view.py                 49     49     0%   1-75
src\gui\panels\storico_oda\oda_filter_widget.py               62     62     0%   1-114
src\gui\panels\storico_oda\oda_panel.py                      155    155     0%   8-292
src\gui\panels\timbrature\__init__.py                          2      2     0%   1-3
src\gui\panels\timbrature\panel.py                           221    221     0%   1-380
src\gui\panels\timbrature_bot.py                             106    106     0%   8-202
src\gui\panels\timbrature_db.py                                2      2     0%   6-8
src\gui\styles\__init__.py                                     4      0   100%
src\gui\styles\constants.py                                    9      0   100%
src\gui\styles\notification_styles.py                         10     10     0%   6-53
src\gui\styles\palette_helpers.py                             10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                               85     67    21%   26-29, 34, 42-53, 57-94, 99-122, 126-170, 175
src\gui\styles\widget_styles.py                               36      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                              46     46     0%   6-93
src\gui\widgets\__init__.py                                   19      0   100%
src\gui\widgets\activity_feed.py                             138    118    14%   41-186, 190, 194-196, 205-213, 216-265, 270, 275-321
src\gui\widgets\animated_progress_bar.py                      79     65    18%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit_log_widget.py                          120    120     0%   7-194
src\gui\widgets\automazioni_widget.py                         59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                          4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                    143    143     0%   1-383
src\gui\widgets\autopilot\event_card.py                      144    144     0%   1-293
src\gui\widgets\autopilot\main_widget.py                     208    208     0%   7-394
src\gui\widgets\bot_parameters.py                            222    185    17%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 135-139, 143-287, 296-303, 307, 326-328, 332-350, 354-362, 366, 370-372, 376-378, 382-387, 391, 395-396
src\gui\widgets\calendar_date_edit.py                         18     12    33%   17-77
src\gui\widgets\core_widgets.py                              106     54    49%   34, 41, 48, 55, 62-63, 66-67, 91-94, 97-98, 116-117, 120-121, 139-140, 143-144, 205-206, 209-210, 233-234, 237-238, 259-264, 267-268, 296-297, 300-301, 327-328, 331-332, 357-358, 361-362, 384-385, 388-389
src\gui\widgets\dashboard_stat_card.py                        49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                158    122    23%   56-65, 70, 75-76, 80-81, 85-87, 91-103, 132-136, 140-250, 262-263, 267-293, 297-303, 312-320, 329-331, 340-351, 363
src\gui\widgets\effects.py                                    43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                               232     78    66%   56-57, 82-89, 108-109, 202, 211, 216-223, 227-244, 265-277, 289-291, 336-355, 365, 376-399, 403-405
src\gui\widgets\footer\__init__.py                             6      6     0%   1-7
src\gui\widgets\footer\business_info.py                       88     88     0%   6-152
src\gui\widgets\footer\components.py                          57     57     0%   6-166
src\gui\widgets\footer\manager.py                             20     20     0%   6-68
src\gui\widgets\footer\status_bar.py                          36     36     0%   6-75
src\gui\widgets\footer\telemetry.py                           55     55     0%   6-87
src\gui\widgets\info_widgets.py                               92     75    18%   30-63, 67, 76-84, 89-113, 127-171, 175, 178
src\gui\widgets\message_bubble.py                             54     54     0%   7-140
src\gui\widgets\mixins\clipboard_mixin.py                     87     67    23%   18-43, 47-68, 71-75, 78-82, 85-89, 100-102, 108, 111-123
src\gui\widgets\modern_button.py                              67     39    42%   43-57, 61-63, 67-68, 72, 76-77, 83-86, 90-93, 97-100, 110-115, 119-158
src\gui\widgets\modern_card.py                                42     28    33%   23-26, 30-31, 41-51, 55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                        99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                         116    116     0%   7-199
src\gui\widgets\notification_group_header.py                  48     48     0%   6-142
src\gui\widgets\notification_item.py                          74     59    20%   26-29, 32-133, 137-139, 142
src\gui\widgets\notification_toolbar.py                      131    131     0%   6-283
src\gui\widgets\pdl_timeline.py                              129    129     0%   1-216
src\gui\widgets\priority_badge.py                             48     48     0%   6-112
src\gui\widgets\quick_actions.py                              78     78     0%   1-352
src\gui\widgets\security_dashboard.py                        159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                             30     23    23%   16-36, 43-53
src\gui\widgets\sidebar_button.py                             57     57     0%   6-125
src\gui\widgets\sidebar_widget.py                            267    267     0%   7-406
src\gui\widgets\simple_chart.py                               67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                        47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                         108    108     0%   1-205
src\gui\widgets\status_card.py                                60     45    25%   26-85, 89-92, 98-113, 117, 121-122
src\gui\widgets\status_indicator.py                           46     37    20%   31-46, 56-73, 77-83
src\gui\widgets\timeline_widget.py                           118     94    20%   33-34, 38-48, 55-102, 111-112, 115-135, 139-153, 157, 161-164, 174-191
src\gui\widgets\toast.py                                     157    123    22%   72-95, 99-146, 150-159, 163-185, 189-194, 198-200, 204-205, 209-221, 233-235, 259-294, 300-303, 308-311, 316-319, 324-327
src\gui\widgets\update_banner.py                              85     85     0%   1-161
src\utils\__init__.py                                          2      0   100%
src\utils\animation_helpers.py                               100    100     0%   6-295
src\utils\date_utils.py                                       74     74     0%   6-234
src\utils\document_generator.py                               18     18     0%   5-41
src\utils\document_processor.py                               66     15    77%   13-14, 24, 37, 41-42, 59-60, 73-74, 84-89
src\utils\helpers.py                                         128     94    27%   30-34, 48-70, 83-85, 90, 107-108, 113, 126-141, 148, 155-159, 166-175, 182-195, 203-235, 245, 249-252
src\utils\log_humanizer.py                                    43     34    21%   13-28, 56-70, 75-100
src\utils\parsing.py                                          51     51     0%   6-98
src\utils\printing.py                                         88     88     0%   1-149
src\utils\resource_manager.py                                 86     45    48%   22-33, 63, 73, 83-85, 97-131, 160-166, 179-180, 193-194
src\utils\secure_logger.py                                    23     23     0%   5-71
src\utils\security.py                                         78     78     0%   6-140
src\utils\system_telemetry.py                                 26     26     0%   6-74
src\utils\validators.py                                       73     73     0%   7-270
----------------------------------------------------------------------------------------
TOTAL                                                      19631  17466    11%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_excel_table_coverage.py::TestExcelTableCoverage::test_analyze_with_lyra_selection
======================== 1 failed, 1 warning in 6.97s =========================

```
</details>

---
### `tests/unit/test_gui_general_page_ai.py::TestGeneralPageAI::test_provider_switch_visibility`
**Error:** `Unknown Error`

**Timestamp:** `2026-03-18T11:59:55.272316`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_gui_general_page_ai.py E                                 [100%]

=================================== ERRORS ====================================
_____ ERROR at setup of TestGeneralPageAI.test_provider_switch_visibility _____
tests\unit\test_gui_general_page_ai.py:12: in page
    with patch("src.core.secrets_manager.SecretsManager.get_gemini_api_key", return_value="fake_key"):
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <class 'src.core.secrets_manager.SecretsManager'> does not have the attribute 'get_gemini_api_key'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      8    67%   126, 139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              338    252    25%   95-116, 128, 139-163, 178, 183-188, 197-201, 219-251, 255, 259, 263, 267, 271-272, 276-277, 282-297, 301-341, 345-371, 375-394, 401-406, 410-421, 425-433, 441-503, 507-533, 537, 541-545, 549-554, 558-568, 572-580
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                           99     84    15%   50-55, 74-78, 109-172, 195-252
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     41    33%   29, 34, 60, 64, 76-88, 100-137
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     82    23%   30, 35, 40, 47, 51, 62-68, 75-82, 86-115, 119-136, 147-174, 178-194
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207    179    14%   32-35, 39, 43-45, 51-71, 75-88, 92-118, 122-127, 139-213, 217-228, 238-267, 271-280, 284-292, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     88    18%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    219    15%   40, 45, 57, 61, 73-76, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 289-321, 327-358, 362-373, 377-394, 398-418, 422-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     69    25%   29, 34, 39, 44, 49, 56-60, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         157    133    15%   36-40, 44, 48-56, 60-77, 81-140, 150-203, 208-232, 241-252, 257-292
src\bots\portale_fornitori\timbrature\storage.py                       166    141    15%   46, 54-81, 87-116, 135-146, 156-163, 166-194, 201-237, 247-262, 267-308, 311-348, 352-367, 374-375
src\bots\safework\base.py                                               82     59    28%   33-37, 41-45, 49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     55    19%   22-24, 30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     32    30%   25-27, 31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     45    29%   24-26, 30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    276    12%   48-50, 55, 60, 65, 69-86, 90-163, 167-171, 175-210, 214-250, 254-287, 291-327, 331-391, 395-408, 412-417, 421-432, 436-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     88    21%   55-56, 61, 66, 71, 83-145, 149-156, 165-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            149    149     0%   10-263
src\core\app_updater.py                                                  9      9     0%   7-35
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     83    18%   19, 23-67, 71, 75-82, 94-101, 128-173, 177-182, 194-200
src\core\audit\integrity.py                                             16      4    75%   16-17, 22, 27
src\core\audit\manager.py                                              162    123    24%   34, 38-41, 45-55, 59-69, 74, 78, 82-91, 111-128, 145-220, 226-243, 247-274, 278-279, 283, 287, 291-294, 303-331
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     18    28%   15-48
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73     73     0%   6-132
src\core\backup_manager.py                                             138    138     0%   6-250
src\core\bug_reporter.py                                               157    157     0%   11-339
src\core\config\account_manager.py                                      53     46    13%   16-38, 43-53, 58-64, 71-91
src\core\config\defaults.py                                              3      0   100%
src\core\config\migration.py                                            69     54    22%   23-30, 35-86, 94-108
src\core\config\security.py                                             44     29    34%   23-43, 57-78
src\core\config_manager.py                                             164     76    54%   48-49, 54, 67, 74, 83, 103-109, 127-128, 143, 174-176, 181-183, 188-190, 195-199, 207, 212-214, 219-221, 226-235, 240-251, 257-259, 264-290
src\core\constants.py                                                  125      0   100%
src\core\contabilita\certificati_engine.py                              91     69    24%   22-23, 27-34, 38-50, 58-79, 84-94, 99-109, 114-132, 137-138
src\core\contabilita\scarico_ore\controller.py                          53     34    36%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        115     62    46%   33, 38, 43, 52-64, 81-128, 137-144, 153-158, 167-174, 179, 184, 189, 194, 199, 204-213, 218, 227, 237, 242
src\core\contabilita_queries.py                                         82     12    85%   20, 27, 35, 44, 52, 73, 81, 88, 96, 105, 113, 120
src\core\contabilita_search.py                                          92     73    21%   26-82, 89-113, 118-127, 134-146, 155-167, 181-185
src\core\contabilita_stats.py                                           59     38    36%   33-53, 58-82, 87-101
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                           25      6    76%   27, 34, 41, 46, 53, 63
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123     61    50%   128-130, 137-138, 141-144, 158-188, 192-196, 199-203, 206, 214-233
src\core\database\migrations\contabilita.py                             34     27    21%   7-68, 73-77, 82-122, 129-142, 149-154
src\core\database\migrations\dipendenti.py                              17     13    24%   6-21, 26-28, 33-39
src\core\database\migrations\pdl.py                                     34     27    21%   7-38, 43-91, 96-116, 121-125, 132-134
src\core\database\migrations\storico_oda.py                             11      8    27%   6-49, 56-58
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-32, 37-47, 52-69
src\core\database\pdl_queries.py                                        92     77    16%   23-37, 43-95, 100-136, 144-209
src\core\dipendenti\anagrafica_controller.py                            88     72    18%   27-40, 47-96, 101-139, 144-149
src\core\employees.py                                                   98     13    87%   61-63, 118-120, 129-130, 174-175, 190-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44      0   100%
src\core\importers\attivita.py                                          67      5    93%   58-59, 77, 92-93
src\core\importers\base.py                                              60      7    88%   15-16, 24-26, 57-58
src\core\importers\certificati.py                                      126     18    86%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-181, 190-192
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     37    80%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 223-226, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     35    81%   14-15, 22-24, 63, 79-80, 86-101, 122, 125, 137-138, 152, 200, 228, 232, 241, 245, 258, 274, 283, 316
src\core\importers\storico_oda.py                                       81     16    80%   60, 66, 71, 84-85, 95-96, 176-185
src\core\license_updater.py                                            192    192     0%   7-323
src\core\license_validator.py                                          176    176     0%   8-302
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              37      2    95%   71-73
src\core\logging\context.py                                             57     32    44%   24-27, 31-32, 36, 40-41, 45-46, 50, 54, 63, 81-98, 108, 118, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     50    32%   63-115, 121, 167-201
src\core\logging\filters.py                                             60     42    30%   92-96, 110-125, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83     61    27%   56-108, 118-140, 164-165, 193-226, 230-240
src\core\logging\logger.py                                             116     71    39%   74-96, 100-101, 120-189, 207-210, 214, 218, 222, 226, 230, 241, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             74     51    31%   23-26, 30, 46-50, 59-60, 77-111, 129-131, 134-136, 153-163, 175-182, 201, 213, 219
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     41    24%   33-44, 48, 58, 67, 86-108, 121-128, 141-154, 163, 180-182, 201
src\core\logging\sinks.py                                              100     76    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 218-220, 226-228, 234-236
src\core\logging\viewer.py                                             177    144    19%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-138, 142-143, 147-148, 152-153, 162-176, 185-193, 204, 216-222, 226-230, 234-248, 252-267, 271-273, 277-313, 317-333, 352, 357, 362
src\core\notification_manager.py                                       116     80    31%   53-57, 61-65, 69-77, 81-93, 97-101, 133-167, 179-181, 190, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-108
src\core\oda_manager.py                                                 42     26    38%   29, 38-91, 98-112
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68     44    35%   27-29, 37-43, 48-52, 63-87, 97, 115-135, 148-158
src\core\schemas.py                                                     57      5    91%   71-73, 79, 86
src\core\secrets_manager.py                                            105     67    36%   30-77, 85-89, 97-116, 120-123, 127-136, 140-142, 146-150, 158-169, 174-179, 184-188, 193-196, 201-207
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               70     51    27%   23-26, 30-35, 45-57, 61-76, 81-82, 92-101, 110-116, 125
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23     14    39%   16-18, 23-28, 33-37
src\core\sync\contabilita_sync.py                                       70     56    20%   22-46, 53-88, 95-112, 117-127
src\core\sync\operazioni_sync.py                                        42     32    24%   22-43, 48-71
src\core\sync\smart_sync.py                                             25     18    28%   21-54
src\core\sync_tracker.py                                                77     47    39%   40-51, 56-60, 73-86, 91-102, 107-119, 132-135, 149-161
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     76     0%   6-118
src\core\telegram\bridge\intent_handler.py                              75     75     0%   6-125
src\core\telegram\bridge\system_handler.py                             103    103     0%   6-139
src\core\telegram\bridge\ui_commands.py                                104    104     0%   6-144
src\core\telegram\service.py                                           205    205     0%   1-314
src\core\telegram_bridge.py                                             34     34     0%   7-84
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                20     20     0%   6-57
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\updater\__init__.py                                             0      0   100%
src\core\updater\engine.py                                             165    165     0%   6-249
src\core\updater\gui.py                                                163    163     0%   6-273
src\core\version.py                                                      5      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174    107    39%   133-134, 143-145, 153-154, 160-165, 173-174, 199-219, 228-282, 292-304, 318-331, 344-394, 403-404
src\gui\components\animated_stack.py                                    85     11    87%   69-71, 134-141
src\gui\components\animated_tab_widget.py                              147     41    72%   99-106, 117-134, 158-164, 168-175, 204, 218-219, 227, 230, 266, 270, 285
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                107     90    16%   28-34, 38-86, 91-107, 110-122, 125-133, 136-141, 144-149, 159-165
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185    163    12%   23-57, 60-68, 71-84, 93-111, 120-145, 148-152, 155, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 243-268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     84    15%   27-79, 82-89, 93-100, 104-111, 118-119, 128-141, 144-149
src\gui\components\scarico_ore\model.py                                168    136    19%   71-97, 108-121, 132-153, 157, 166-168, 178-192, 196-199, 203-210, 214-216, 220-222, 226-228, 232-258, 262-279, 285-287, 291-316
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    228     0%   7-455
src\gui\dialogs\certificati_analysis_dialog.py                         225    207     8%   36-46, 49-256, 260-286, 290-397, 401-498
src\gui\dialogs\command_palette.py                                     298    298     0%   7-432
src\gui\dialogs\confirmation_dialog.py                                  96     72    25%   54-118, 122-130, 134-142, 146-158, 174-177, 182-185, 190-193, 198-201
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\splash_standalone.py                                    81     81     0%   8-133
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      262    262     0%   6-412
src\gui\formatters.py                                                  135     65    52%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 163-242, 246-248
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              75     75     0%   7-323
src\gui\main_window\components\status_bar.py                           132    132     0%   7-232
src\gui\main_window\components\tool_bar.py                              82     82     0%   7-187
src\gui\main_window\components\tray_icon.py                             17     17     0%   7-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    37     37     0%   6-90
src\gui\main_window\controllers\monitoring_controller.py                36     36     0%   6-65
src\gui\main_window\controllers\signal_connector.py                     19     19     0%   7-65
src\gui\main_window\controllers\workflow_controller.py                  83     83     0%   6-155
src\gui\main_window\main.py                                            252    252     0%   7-474
src\gui\main_window\page_index.py                                       28     28     0%   7-53
src\gui\models\audit_model.py                                          131    105    20%   44-47, 62-64, 68, 72, 79-103, 107-125, 129-139, 143-150, 154-158, 162-170, 174-176, 182-184, 188-192, 196-201, 205-216, 228-230
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 281    145    48%   70-76, 80-118, 130-134, 138-140, 185, 189-206, 210-211, 308, 316, 325, 329-334, 338-341, 345-347, 356-357, 377-386, 390-393, 397-417, 421-425, 429-435, 448-459, 463-475, 479, 483-484, 491-494, 498-503, 507-530, 536
src\gui\panels\carico_ts.py                                             89     34    62%   57-61, 97-99, 107-109, 118-123, 132, 141-176
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 29-32
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   28-35, 42-84, 91-99, 102-105, 109-113, 116-187, 190-244, 247-309, 312-351, 354-400
src\gui\panels\contabilita_kpi\kpi_panel.py                            161    143    11%   38-64, 67-183, 196-200, 204-217, 220-230, 233, 236-309
src\gui\panels\contabilita_panel.py                                    266    104    61%   73-77, 226-230, 234, 253, 263-266, 284, 292-293, 296-299, 303-305, 311-313, 320, 329-333, 335-338, 342-384, 388-392, 396-413, 417-433
src\gui\panels\dashboard_panel.py                                      128    109    15%   39-82, 86, 90-104, 109-153, 157-172, 176-205, 208-247
src\gui\panels\dettagli_oda.py                                         181    149    18%   45-58, 62-64, 68-72, 77-136, 145-147, 158-169, 173-175, 179, 183-194, 198-221, 225-237, 241-243, 252-257, 261-328, 332-340
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      94     69    27%   35-55, 58-85, 89-101, 104-110, 113-117, 120-122, 125-147, 150-154, 159, 163
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156    129    17%   26-52, 57-100, 109-195, 200-211, 216-240, 245-304
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275    240    13%   37-40, 44, 48-49, 52-58, 61-67, 71-105, 119-122, 125-157, 161, 168-169, 172-217, 220, 236-244, 248-363, 367-383, 387-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           137    112    18%   33-39, 43-177, 181-200, 203-209, 212-216, 220-224, 229, 244, 263, 279, 294, 307, 323, 336, 350, 365
src\gui\panels\notifications_panel.py                                  243    194    20%   70-83, 87-161, 165-169, 173-175, 179-181, 185-187, 191-192, 196-197, 201, 205-209, 216-239, 243-263, 267-291, 295-300, 304-305, 309-319, 323-349, 353-354, 358-366, 370-406
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    154    19%   48-93, 97-145, 150-164, 173-186, 199-209, 213-214, 219-235, 239-254, 258-260, 264-274, 278-296, 300, 304-307, 315-325
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           142    117    18%   42-50, 59-61, 65-68, 73-123, 132-134, 145-156, 160-162, 166-175, 179-184, 188-190, 199-272
src\gui\panels\ricerca_pdl.py                                          109     91    17%   44-52, 56-58, 63-123, 127-130, 134-135, 139-194, 198-204, 212-214
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73     58    21%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        91     72    21%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          229    195    15%   54-61, 70-72, 76-79, 84-186, 195-197, 201-203, 207-227, 231-241, 250-268, 280-284, 295-298, 302-358, 368-379, 383-403, 414-428, 435-450
src\gui\panels\scarico_ts.py                                           137     63    54%   63-67, 128-130, 134, 141-143, 147-148, 152-162, 167, 175-177, 186-188, 197-262, 266
src\gui\panels\settings\main_panel.py                                  106     40    62%   129-137, 141-152, 156, 160, 164-173, 177-189, 193-202
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                           46      4    91%   73-74, 78-79
src\gui\panels\settings\pages\lists_page.py                             47     12    74%   66-71, 75-80
src\gui\panels\settings\pages\paths_page.py                            166     78    53%   141-165, 169-190, 207-208, 211, 214-216, 219-221, 224-226, 229-231, 234-236, 239-241, 244-246, 249-251, 257-281, 285-293
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      6    95%   219-222, 231-232
src\gui\panels\settings\tabs\config_tab.py                             150     10    93%   279-282, 286-288, 292-294
src\gui\panels\settings\tabs\roi_tab.py                                116     22    81%   126-143, 147-153, 217, 221
src\gui\panels\settings\tabs\telegram_tab.py                           128      8    94%   228-231, 240-241, 250-251
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     70    42%   91-103, 107-115, 119-138, 142-149, 153-159, 163-170, 179-191
src\gui\panels\settings\widgets\editable_list_widget.py                 83     34    59%   89-100, 104-107, 111-116, 120-124, 128-133, 142-143
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    128    17%   47-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-292
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     50    21%   18-41, 44-68, 76-116, 120-135, 139-140
src\gui\panels\timbrature\components\settings_tab.py                   102     86    16%   31-36, 39-99, 103-124, 128-157, 162-169, 172-173, 178-180
src\gui\panels\timbrature\panel.py                                     221    193    13%   44-69, 73-90, 93-126, 129-210, 213-253, 257-273, 277-312, 316-334, 337-344, 349, 352-375, 380
src\gui\panels\timbrature_bot.py                                       106     81    24%   44-53, 57-59, 63-67, 72-85, 89-91, 95-96, 100-108, 112-117, 126-131, 135-196, 200-202
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      5    50%   46-53
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85     67    21%   26-29, 34, 42-53, 57-94, 99-122, 126-170, 175
src\gui\styles\widget_styles.py                                         36      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                                        46     46     0%   6-93
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138    118    14%   41-186, 190, 194-196, 205-213, 216-265, 270, 275-321
src\gui\widgets\animated_progress_bar.py                                79     65    18%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit\audit_filter_bar.py                              120    101    16%   38-39, 43-137, 146-148, 152-161, 178-179, 188-201
src\gui\widgets\audit\audit_pagination_bar.py                           37     27    27%   14-15, 18-43, 49-56, 60-61
src\gui\widgets\audit_log_widget.py                                    120     95    21%   45-57, 60-130, 133-134, 137-147, 150, 153-154, 163-179, 182-189, 192-194
src\gui\widgets\automazioni_widget.py                                   59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143    129    10%   25-154, 158-166, 170-186, 198-350, 354-363, 367-383
src\gui\widgets\autopilot\event_card.py                                144    126    12%   50-184, 188-189, 193, 197-212, 217-226, 231-293
src\gui\widgets\autopilot\main_widget.py                               208    183    12%   60-71, 75, 79, 83-168, 172-191, 195-204, 208-236, 240-242, 246-253, 257-260, 264-341, 345-394
src\gui\widgets\bot_parameters.py                                      222     68    69%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 216-226, 332-350, 362, 370-372, 376-378, 382-387, 395-396
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            209    178    15%   70-79, 83-154, 158, 162-177, 181-194, 198-209, 213-219, 223-228, 232-250, 254-257, 261-267, 271-274, 278-281, 285-288, 292-295, 299-303, 312-323
src\gui\widgets\contabilita\certificati\tree_widget.py                  98     71    28%   31-32, 36-42, 46-50, 54-56, 64-65, 69-71, 75-77, 116-118, 121-141, 172-214, 218-225, 229-232
src\gui\widgets\contabilita\certificati_tab.py                         258    219    15%   50-54, 58-100, 104-115, 119, 123, 127-128, 132-138, 143-164, 168-279, 283-285, 289-290, 294-297, 301-304, 313-327, 331-369, 373-378, 382-386, 390-423, 428-451
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         186     55    70%   95, 100, 134, 151, 179, 195-214, 217-237, 240-256
src\gui\widgets\contabilita\helpers.py                                  36     29    19%   11-35, 38-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     15    86%   41, 48, 55, 139-140, 143-144, 327-328, 331-332, 384-385, 388-389
src\gui\widgets\dashboard\multi_window_status.py                        86     70    19%   40-94, 107-121, 124-170, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146    125    14%   49-100, 113-121, 125-185, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179    155    13%   38-47, 53-70, 74-87, 91-120, 125-192, 196-202, 208-214, 226-273, 277-285, 292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    353     9%   48-63, 67-68, 71-91, 94-117, 120-193, 196-279, 282-290, 293-304, 309-317, 320-344, 347-353, 359-376, 379-405, 409-423, 426-429, 436-486, 490-500, 503-530, 533-605, 608-618, 621
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158    122    23%   56-65, 70, 75-76, 80-81, 85-87, 91-103, 132-136, 140-250, 262-263, 267-293, 297-303, 312-320, 329-331, 340-351, 363
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         232     76    67%   82-89, 108-109, 202, 211, 216-223, 227-244, 265-277, 289-291, 336-355, 365, 376-399, 403-405
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   6-152
src\gui\widgets\footer\components.py                                    57     57     0%   6-166
src\gui\widgets\footer\manager.py                                       20     20     0%   6-68
src\gui\widgets\footer\status_bar.py                                    36     36     0%   6-75
src\gui\widgets\footer\telemetry.py                                     55     55     0%   6-87
src\gui\widgets\info_widgets.py                                         92     42    54%   30-63, 67, 89-113, 166-171
src\gui\widgets\message_bubble.py                                       54     54     0%   7-140
src\gui\widgets\mixins\clipboard_mixin.py                               87     15    83%   19, 26, 31, 36, 54, 61, 67, 78-82, 100-102
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     91    22%   58-74, 78-156, 160-166, 170-176, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48     36    25%   35-41, 45-121, 125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     59    20%   26-29, 32-133, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131    102    22%   42-54, 58-70, 74-76, 80-84, 88-107, 139-145, 149-232, 237-238, 242-243, 248-255, 259-260, 269-271, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     61    22%   25-33, 228-229, 232-257, 261-302, 307-347, 352
src\gui\widgets\safework\status_list.py                                 60     45    25%   31-57, 61-67, 73-93
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     23    23%   16-36, 43-53
src\gui\widgets\sidebar_button.py                                       57     12    79%   53, 58, 62-70, 78-79
src\gui\widgets\sidebar_widget.py                                      267    267     0%   7-406
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46     37    20%   31-46, 56-73, 77-83
src\gui\widgets\timeline_widget.py                                     118     73    38%   38-48, 55-102, 139-153, 157, 161-164, 174-191
src\gui\widgets\toast.py                                               157     51    68%   128-130, 150-159, 178-185, 189-194, 198-200, 204-205, 211-212, 218, 263-264, 271-278, 286, 300-303, 308-311, 316-319, 324-327
src\gui\widgets\update_banner.py                                        85     85     0%   1-161
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74     74     0%   6-234
src\utils\document_generator.py                                         18     18     0%   5-41
src\utils\document_processor.py                                         66     15    77%   13-14, 24, 37, 41-42, 59-60, 73-74, 84-89
src\utils\helpers.py                                                   128     93    27%   30-34, 48-70, 83-85, 90, 107-108, 113, 126-141, 148, 155-159, 166-175, 182-195, 203-235, 249-252
src\utils\log_humanizer.py                                              43     34    21%   13-28, 56-70, 75-100
src\utils\parsing.py                                                    51     44    14%   14-34, 40-56, 61-71, 76-84, 89-98
src\utils\printing.py                                                   88     71    19%   14-15, 24-28, 33-43, 51-57, 68-149
src\utils\resource_manager.py                                           86     45    48%   22-33, 63, 73, 83-85, 97-131, 160-166, 179-180, 193-194
src\utils\secure_logger.py                                              23     10    57%   47-54, 57-60
src\utils\security.py                                                   78     78     0%   6-140
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73     73     0%   7-270
--------------------------------------------------------------------------------------------------
TOTAL                                                                28759  20957    27%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_gui_general_page_ai.py::TestGeneralPageAI::test_provider_switch_visibility
============================== 1 error in 15.65s ==============================

```
</details>

---
