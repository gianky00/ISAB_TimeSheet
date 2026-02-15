# 📊 Test Execution Report

**Date:** 2026-02-15 16:29:10
**Duration:** 620.70s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1553 |
| ✅ Passed | 567 |
| ❌ Failed | 2 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_bug_reporter.py::TestBugReporter::test_collect_diagnostics_creates_zip`
**Error:** `Timeout`

**Timestamp:** `2026-02-15T16:11:26.469037`

<details><summary>Full Output</summary>

```text
Execution Timed Out
```
</details>

---
### `tests/unit/test_document_processor_advanced.py::TestDocumentProcessorAdvanced::test_merge_pdfs_logic`
**Error:** `FAILED tests/unit/test_document_processor_advanced.py::TestDocumentProcessorAdvanced::test_merge_pdfs_logic`

**Timestamp:** `2026-02-15T16:29:10.069068`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_document_processor_advanced.py F                         [100%]

================================== FAILURES ===================================
_____________ TestDocumentProcessorAdvanced.test_merge_pdfs_logic _____________
tests\unit\test_document_processor_advanced.py:104: in test_merge_pdfs_logic
    assert success is True
E   assert False is True
------------------------------ Captured log call ------------------------------
WARNING  src.utils.document_processor:document_processor.py:78 File non trovato per il merge: f1.pdf
WARNING  src.utils.document_processor:document_processor.py:78 File non trovato per il merge: f2.pdf
ERROR    src.utils.document_processor:document_processor.py:86 Nessun file valido fornito per l'unione.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      8    67%   126, 139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              267    181    32%   92, 97-99, 114, 127, 140-142, 146, 150, 154, 158-159, 164, 169-185, 189-232, 236-258, 262-273, 280-285, 289-316, 328-377, 381-413, 418-427, 431-435, 439-441, 445, 449-455, 466-478, 482-485
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    138    17%   50-55, 76-81, 100-104, 135-198, 221, 250-304, 324-325, 328-332, 345, 348-352, 374-377, 380-390, 420-436, 466-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47      6    87%   20, 25, 66, 86, 94, 100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   34-36, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     16    80%   21, 26, 31, 42, 61, 64, 75, 101, 106-107, 123-124, 126-127, 136, 143
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205     61    70%   50-52, 87-90, 101-114, 128-130, 144-147, 218, 233-241, 258-262, 271-277, 298-299, 315-316, 322, 327-330, 333-335, 344-345, 347-348, 361
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            84     67    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-104, 108-129
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           221    184    17%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 127-142, 146-168, 172-199, 203-212, 216-241, 245-277, 283-312, 316-325, 329-344, 348-369, 374-384
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            78     56    28%   21, 26, 31, 36, 41, 48-52, 56-78, 84-127, 134
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159    135    15%   36-40, 43, 47-55, 59-76, 80-139, 143-196, 201-227, 231-242, 247-282
src\bots\portale_fornitori\timbrature\storage.py                       178    151    15%   45-46, 50-79, 83-84, 91-118, 124-153, 163-174, 184-191, 194-222, 229-265, 275-290, 295-335, 338-375, 379-394, 401-402
src\bots\safework\base.py                                               76     54    29%   24-27, 31-35, 39-42, 48-63, 67-95, 99-115, 119, 123
src\bots\safework\common\locators.py                                    30      0   100%
src\bots\safework\pages\login_page.py                                   71     58    18%   22-24, 30-43, 47-79, 88-107, 115-116, 120-127
src\bots\safework\pages\ricerca_pdl_page.py                             46     32    30%   25-27, 31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     45    29%   24-26, 30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           245    209    15%   31-34, 38, 42, 46, 50-68, 71, 75-116, 120-124, 128-157, 161-193, 197-227, 231-262, 266-284, 288-301, 305-310, 314-325, 329-341, 347-357, 360-362
src\bots\safework\pdl\search_bot.py                                     95     72    24%   25-26, 30, 34, 38, 42-71, 74-88, 91-105, 108-112, 116-162
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                 97     76    22%   24-25, 29, 33, 37, 41-91, 95-102, 106-159, 162-164
src\bots\safework\programmazione_sync\bot.py                            55     41    25%   19-20, 24, 28, 32, 36-91
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82     82     0%   5-156
src\core\app_updater.py                                                 48     48     0%   6-97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             100     39    61%   61-63, 78-79, 110-112, 114-117, 119-122, 124-126, 128-132, 145-146, 150-155, 158-164
src\core\audit\integrity.py                                             16      2    88%   22, 27
src\core\audit\manager.py                                              140     68    51%   47, 51, 59-64, 171, 175-178, 184-201, 205-232, 242, 245-248, 256-284
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               28     13    54%   23-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      0   100%
src\core\backup_manager.py                                             138    105    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-188, 199-207, 212-223, 228-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config_manager.py                                             237     42    82%   117, 138, 161, 224, 281, 298-299, 328-355, 362, 389-392, 401-419, 431, 439, 467-468
src\core\constants.py                                                  101      0   100%
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87     16    82%   29-30, 47-48, 54, 77-78, 84, 93-94, 100, 109-110, 116, 125-126
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                          159      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           121     10    92%   177-182, 196-197, 225-227
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     34      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\database\pdl_queries.py                                        80     66    18%   22-36, 46-75, 81-135, 140-176
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44      4    91%   50, 62, 73, 77
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              59     17    71%   15-16, 24-26, 52-57, 71-75, 85-87
src\core\importers\certificati.py                                      116     21    82%   38, 47, 51, 54-55, 64, 91, 105-106, 141, 150, 162, 166-167, 171, 174-179
src\core\importers\contabilita.py                                      133     29    78%   42, 49-57, 70, 78, 88, 102-104, 118, 126, 138-139, 148, 186-187, 190-192, 213, 233, 235
src\core\importers\giornaliere.py                                      181    140    23%   44, 49-62, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\pdl_sync_manager.py                                 151    151     0%   6-225
src\core\importers\scarico_ore.py                                      187    151    19%   14-15, 22-24, 51-89, 97-115, 119-136, 150-181, 185-252, 256-265, 282-284, 288-312
src\core\importers\storico_oda.py                                       81     57    30%   62-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    153     0%   6-290
src\core\license_validator.py                                          180    180     0%   6-353
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             57     24    58%   31-32, 40-41, 45-46, 54, 81-98, 118, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          66     50    24%   69-132, 139, 188-225
src\core\logging\filters.py                                             60     29    52%   114, 117, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83     22    73%   84, 88-90, 122, 125, 138, 164-165, 205-215, 224, 230-240
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 147-148, 161-165, 169-174, 179-180, 199, 205, 213, 217, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     16    70%   58, 67, 91, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     76    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 218-220, 226-228, 234-236
src\core\logging\viewer.py                                             175    142    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 149, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                162    143    12%   27-40, 58-60, 64-77, 81-89, 93-94, 98-126, 130-161, 170-172, 181-214, 223-278, 287-316
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                       111     80    28%   31-37, 40-47, 51-61, 65-78, 82-86, 105-150, 154-156, 160, 164-171, 175-184, 188-197, 201, 205-208, 212-215
src\core\oda_manager.py                                                 34     13    62%   31-91, 110-115
src\core\report_history.py                                              67     44    34%   26-28, 36-42, 47-51, 62-86, 96, 114-134, 147-157
src\core\schemas.py                                                     77     25    68%   65-70, 75-86, 91-93, 98-100, 106
src\core\secrets_manager.py                                             94     51    46%   31-49, 53-57, 61-71, 75-77, 81-85, 90, 95, 105, 112-115, 120-124, 131-132, 137-143
src\core\stats_manager.py                                               47     10    79%   41-45, 48, 61, 63, 76, 83
src\core\sync_tracker.py                                                58     36    38%   26-39, 44-48, 61-73, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           207    167    19%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-143, 146-163, 167-178, 186-199, 210-218, 222-233, 236-248, 251-263, 266-280, 285-300, 305-321
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            344    344     0%   1-485
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 25-29, 33-65
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    99     85    14%   24-76, 79-86, 89-96, 99-106, 109, 112-113, 116-129, 132-137
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 111-132, 135, 138-140, 143-157, 160-163, 166-173, 176-179, 182-184, 187-189, 192-218, 221-237, 242-244, 247-272
src\gui\controllers\bot_controller.py                                   46     19    59%   27-35, 66-80
src\gui\controllers\navigation_controller.py                           153    113    26%   45-61, 65-82, 85-99, 102-105, 108-111, 114-117, 120-123, 126-129, 132-135, 138-141, 144-147, 150-153, 156-159, 163-169, 173-177, 181-186, 198-234, 239-240, 261-263, 267-268, 272-273, 277-309, 313-314
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       66     57    14%   29-112, 115-122, 126
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-112, 115-120
src\gui\dialogs\bug_report_dialog.py                                   229    229     0%   10-477
src\gui\dialogs\command_palette.py                                     306    306     0%   1-521
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   34-83, 86-94, 97-105, 110-111, 115-116, 120-121, 125-126
src\gui\dialogs\quick_actions_config.py                                 86      1    99%   155
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   23-69, 73, 78-80
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-372
src\gui\formatters.py                                                  131    113    14%   14-28, 38-68, 73, 90-96, 100-103, 107, 110, 113, 116-141, 146-148, 151-154, 158-236
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-329
src\gui\main_window\components\status_bar.py                           157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                              26     26     0%   1-41
src\gui\main_window\components\tray_icon.py                             17     17     0%   1-38
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-41
src\gui\main_window\main.py                                            287    287     0%   1-473
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          130    105    19%   29-32, 41-43, 46, 49, 52-76, 80-98, 102-112, 116-123, 127-131, 135-143, 147-149, 154-156, 159-164, 167-172, 176-188, 191-193
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 197    141    28%   52-56, 60-77, 89-93, 97-99, 124-132, 136-180, 187, 191-202, 212, 220, 229, 233-238, 242-245, 249-251, 255-266, 270-273, 277-293, 297-301, 305-310, 320-322, 326-339, 343, 347-362, 369-372, 376-381, 385-388
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-105, 109-117, 121-122, 126-180
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               200     43    78%   96-97, 102-104, 129-137, 140-153, 165-166, 187, 220-221, 228-230, 287-288, 310-312, 327-328
src\gui\panels\contabilita_kpi\kpi_panel.py                            159      4    97%   203, 228, 297-298
src\gui\panels\contabilita_panel.py                                    249    108    57%   50-56, 164-171, 175, 203-205, 215, 219, 223-244, 249-274, 278-280, 284-287, 295-300, 303-311, 321, 324-326, 344, 351, 366, 370-387, 391, 394-413
src\gui\panels\dashboard_panel.py                                      166     71    57%   88, 134-136, 143, 145, 148-150, 155-156, 158-168, 185-188, 195-198, 201, 209-212, 216-227, 231-237, 241-256, 260-282, 286-292
src\gui\panels\dettagli_oda.py                                         137    112    18%   27-35, 38-42, 46-90, 93-95, 99, 102-114, 117-127, 130-132, 136-142, 145-221, 225-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     398    360    10%   55-99, 102-240, 244-284, 288-301, 304-333, 336-378, 382-390, 394-408, 411-420, 424-455, 458-493, 496-536, 539-579, 582, 586-669, 672-677, 683-712
src\gui\panels\dipendenti\shared.py                                    151    134    11%   26-73, 90-169, 172-174, 177-179, 182-184, 187, 192-233, 238-273
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   9-11, 17-44, 55-67, 71-78
src\gui\panels\dipendenti\utils\report_generator.py                    153    127    17%   25-51, 56-99, 108-194, 199-210, 215-237, 242-299
src\gui\panels\dipendenti\widgets\employee_detail_view.py              104     91    12%   24-29, 32-135, 138-142, 150-162, 168-171
src\gui\panels\dipendenti_manager_panel.py                             186    166    11%   28-71, 74, 85-105, 108-133, 136-168, 171-203, 207-236, 240-257, 261-280, 283-298, 305-340
src\gui\panels\health_panel.py                                         291    259    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-525, 529-557, 561-566, 570-573
src\gui\panels\help_panel.py                                           122     98    20%   32-35, 38-167, 171-191, 194-203, 206-214, 217-221, 224, 244, 264, 276, 290, 301, 314, 326, 337, 347, 357, 365
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        42     32    24%   20-32, 36-48, 52-58, 62-67
src\gui\panels\lyra\header.py                                           38     28    26%   23-25, 28-80
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      161    132    18%   31-37, 40-94, 100-122, 125-138, 141-148, 151-152, 155-156, 159-161, 164-169, 172-174, 177-213, 216-218, 221-224, 227-229, 233, 236-248
src\gui\panels\lyra\workers.py                                          37     26    30%   23-30, 33-45, 54-57, 60-65
src\gui\panels\notifications_panel.py                                  254    207    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-311, 315-316, 320-338, 342-374, 378-380, 384-403, 407-446
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 16-26
src\gui\panels\pdl\pdl_detail_view.py                                   47     36    23%   20-23, 26-48, 52-65, 69-70
src\gui\panels\pdl\pdl_filter_widget.py                                 66     51    23%   27-30, 33-107, 110
src\gui\panels\pdl\pdl_panel.py                                        365    328    10%   46-110, 113-179, 183-237, 240-257, 261-290, 294-306, 310-342, 346-384, 388-390, 394-395, 399-410, 414-420, 424-443, 447-519, 523-527, 531-545, 549-573, 577-618
src\gui\panels\pdl\programmazione_tab.py                               533    490     8%   54-63, 67-75, 79-91, 94-172, 179-187, 191-207, 210-371, 375-385, 389-390, 394-447, 450-454, 458, 462-463, 467-480, 484-525, 529-550, 554-555, 558-560, 563-617, 620-639, 644-765, 769-809, 812-918
src\gui\panels\prenota_bp.py                                           107     88    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-187
src\gui\panels\ricerca_pdl.py                                           86     70    19%   31-38, 41-68, 71-74, 77-78, 81-86, 96-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    336    296    12%   43-45, 50-84, 88-90, 101-123, 127-240, 244-259, 263-292, 296-298, 302-310, 314-338, 342-344, 348-366, 377-404, 408-410, 414-416, 421-430, 434-443, 447-448, 452-460, 464-478, 482-503, 507-510, 514-541
src\gui\panels\scarico_pdl.py                                          301    260    14%   42-59, 63-84, 88-121, 131-139, 142-146, 150-275, 278-286, 289-292, 295-308, 311-316, 320, 323-325, 329-337, 342-348, 353-354, 357-391, 395-407, 411-433, 437-451, 455-462, 466-498, 502-504, 508, 512-526, 530-532
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-79, 83-85, 89, 93-106, 110-118, 122-124, 128-133, 147-149, 155-211
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-130, 133-136, 139, 144-146, 149-162, 165-181
src\gui\panels\settings\pages\diag_page.py                              33     21    36%   15-16, 19-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                          117    102    13%   27-29, 32-123, 127-129, 133-145, 148-156, 160-171, 175-181
src\gui\panels\settings\pages\lists_page.py                            340    285    16%   35-36, 39-65, 70-87, 90-107, 110-129, 132-151, 154-173, 176-195, 202-208, 217-218, 225, 235, 253-264, 274-284, 289-296, 299-310, 313-321, 324-340, 343-350, 353-359, 364-373, 376-397, 400-407, 410-416, 421-422, 425-430, 433-436, 439-444, 447-450, 454, 457, 460, 463, 466, 469, 472, 475, 478, 481, 484, 487, 492-497, 500-505
src\gui\panels\settings\pages\paths_page.py                            119     95    20%   29-30, 33-77, 82-102, 106-127, 144-145, 148, 151-153, 156-158, 161-163, 166-168, 171-173, 176-178, 183-201, 204-210
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 98-100
src\gui\panels\settings\tabs\backup_tab.py                             134    115    14%   32-33, 36-146, 149-156, 159-161, 164, 167-172, 175-176, 179-198, 201-225
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           140    120    14%   30-31, 34-131, 134-139, 142-155, 158-170, 174-178, 186-196, 200-213
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              42     36    14%   10-11, 14-73
src\gui\panels\storico_oda\oda_detail_view.py                           48     37    23%   21-24, 27-49, 53-67, 71-72
src\gui\panels\storico_oda\oda_filter_widget.py                         40     27    32%   24-27, 30-74, 77
src\gui\panels\storico_oda\oda_panel.py                                253    222    12%   43-106, 109-169, 173-181, 185-284, 287-302, 305, 308, 311-315, 318-324, 328-346, 350-408, 411-416, 419-439, 443-463
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     62     50    19%   16-39, 42-64, 72-112, 116-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    99     85    14%   28-33, 36-80, 84-105, 109-138, 143-150, 153-154, 159-161
src\gui\panels\timbrature\panel.py                                     173    149    14%   38-62, 65-97, 100-131, 134-174, 178-194, 198-233, 237-255, 258-265, 269, 272-295, 299
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 107-188, 191-193
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         67     50    25%   26-29, 34, 41-51, 55-92, 97-118, 123
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     45     0%   6-91
src\gui\widgets\__init__.py                                             13      0   100%
src\gui\widgets\activity_feed.py                                       136     22    84%   39-40, 88-90, 146-147, 167-177, 184, 188-190, 263, 269, 280, 282
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-150
src\gui\widgets\audit\audit_filter_bar.py                               78     63    19%   26-28, 31-84, 87-89, 92-101, 112-113, 116-129
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    104     82    21%   40-52, 55-116, 119-120, 123-133, 136, 139-140, 143-159, 162-169, 172-174
src\gui\widgets\automazioni_widget.py                                   55     55     0%   1-132
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     19    87%   170-186, 367-383
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   24-128, 132-147, 152-165
src\gui\widgets\autopilot\main_widget.py                               204     79    61%   58, 61, 152-171, 174-183, 186-214, 217-219, 222-229, 232-235, 244, 251, 260, 269, 278, 296-298, 302-308
src\gui\widgets\bot_parameters.py                                      108     85    21%   41-45, 48-110, 120-127, 131, 150-152, 156-164, 169, 173-175, 179-181, 191-196, 200, 204-205
src\gui\widgets\calendar_date_edit.py                                   17     12    29%   16-76
src\gui\widgets\contabilita\attivita_tab.py                            221     61    72%   116, 140, 145, 169, 202, 211-214, 234, 238-241, 245-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-296, 299-308
src\gui\widgets\contabilita\certificati_tab.py                         571    147    74%   159, 167, 172-175, 320, 338, 443-446, 462-463, 559, 715-716, 723, 729, 738, 750, 775-776, 840, 854-857, 937-939, 942-944, 990, 995-998, 1002-1005, 1009-1023, 1026-1096, 1112-1148, 1155-1160, 1165-1207
src\gui\widgets\contabilita\giornaliere_tab.py                         189    158    16%   47-50, 54-95, 99, 102-129, 132-139, 143, 146-166, 169-189, 193-212, 215-240, 243-259
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                100     81    19%   25-26, 30-31, 34-51, 73-93, 96-137, 141, 145-166, 170-201, 205, 209
src\gui\widgets\data_table.py                                          108      0   100%
src\gui\widgets\excel_table.py                                         335    292    13%   49-61, 65-72, 76-93, 97-117, 120-121, 124-125, 129-140, 144-166, 170-193, 197-216, 220-240, 244-253, 256-261, 264-268, 271-275, 284-286, 289-311, 314-371, 374-377, 380-386, 389-421, 424-427, 430-432, 435, 439-456, 465-475, 479-519, 524-549
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-121
src\gui\widgets\footer\components.py                                    55     55     0%   1-94
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-50
src\gui\widgets\footer\telemetry.py                                     55     55     0%   1-69
src\gui\widgets\info_widgets.py                                         90     39    57%   29-60, 63, 85-109, 170
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        62     11    82%   69-70, 76-79, 83-86, 147
src\gui\widgets\multi_select_filter.py                                  97     80    18%   26-78, 81-85, 88-91, 94-99, 108-123, 126-129, 132-133, 136-139, 142-146
src\gui\widgets\notification_card.py                                   240    209    13%   86-102, 106-354, 358-368, 372, 376-378, 392-423, 427-443, 447-452, 456-458, 462-463, 467-472, 476-480, 484-521, 525-531, 535-542
src\gui\widgets\notification_group_header.py                            47     36    23%   33-39, 43-124, 128-131, 135-136, 140, 144-145
src\gui\widgets\notification_item.py                                    72     59    18%   22-25, 28-125, 129-131, 134
src\gui\widgets\notification_toolbar.py                                104     78    25%   36-48, 52-64, 68-70, 74-78, 82-101, 133-139, 143-228, 233-234, 238-239, 244-251, 255-256, 265-267, 271, 275, 279
src\gui\widgets\priority_badge.py                                       47     35    26%   30-37, 41-78, 82-90, 94-98, 102, 106-108
src\gui\widgets\quick_actions.py                                        77     13    83%   267-308, 324, 352-353
src\gui\widgets\security_dashboard.py                                  154    154     0%   1-251
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      245    245     0%   1-435
src\gui\widgets\simple_chart.py                                         66     66     0%   1-105
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   107     91    15%   27-28, 31-112, 117-149, 153-155, 159-172, 178-220
src\gui\widgets\status_card.py                                          60     47    22%   20-85, 89-92, 101-117, 121, 125-126
src\gui\widgets\status_indicator.py                                     43     36    16%   18-32, 42-59, 63-69
src\gui\widgets\timeline_widget.py                                     203    168    17%   46-71, 74-81, 84-117, 122-135, 138-143, 146-155, 158-159, 162-164, 169-174, 177-190, 195-202, 208-218, 221-235, 238-244, 247-252, 263-279, 282, 285, 290-314
src\gui\widgets\toast.py                                               131     99    24%   59-80, 84-123, 127-149, 152-157, 161-163, 167-168, 171-183, 194-196, 206-235, 240, 245, 250, 255
src\gui\widgets\update_banner.py                                        35     35     0%   1-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70      1    99%   55
src\utils\document_generator.py                                         17      2    88%   38-39
src\utils\document_processor.py                                         83     34    59%   14-15, 25, 38, 50-51, 59, 63-64, 71-72, 80-83, 89-111
src\utils\helpers.py                                                    91     53    42%   30-34, 48-70, 83-85, 90, 117-118, 123, 136-151, 165-167, 182-188, 203, 222, 239-242
src\utils\log_humanizer.py                                              42     26    38%   19-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    54     10    81%   15, 18, 22, 80, 87, 96, 103-120
src\utils\printing.py                                                   86     70    19%   19-24, 29-40, 48-54, 65-144
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     23    71%   43-44, 80-82, 102, 104, 109-111, 116, 122-137
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                25328  17544    31%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_document_processor_advanced.py::TestDocumentProcessorAdvanced::test_merge_pdfs_logic
============================== 1 failed in 7.55s ==============================

```
</details>

---
