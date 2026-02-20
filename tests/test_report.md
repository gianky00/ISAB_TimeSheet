# 📊 Test Execution Report

**Date:** 2026-02-20 16:06:57
**Duration:** 1380.60s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1523 |
| ✅ Passed | 732 |
| ❌ Failed | 4 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_bot_base_cdp.py::TestBaseBotCDP::test_setup_driver_no_download_path`
**Error:** `FAILED tests/unit/test_bot_base_cdp.py::TestBaseBotCDP::test_setup_driver_no_download_path`

**Timestamp:** `2026-02-20T15:15:46.469075`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_bot_base_cdp.py F                                        [100%]

================================== FAILURES ===================================
______________ TestBaseBotCDP.test_setup_driver_no_download_path ______________
tests\unit\test_bot_base_cdp.py:66: in test_setup_driver_no_download_path
    assert "Page.setDownloadBehavior" not in calls
E   AssertionError: assert 'Page.setDownloadBehavior' not in ['Page.setDownloadBehavior', 'Page.addScriptToEvaluateOnNewDocument']
---------------------------- Captured stdout call -----------------------------
[2026-02-20 15:15:34] INFO     - bot.ConcreteBot                - 📁 Cartella download forzata: C:\Users\Coemi\Downloads | trace_id=trace_b71423b3df704f16 | bot_type=concretebot | bot_status=IDLE | current_step= | step_index=-1
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              303     32    89%   138-139, 144, 154, 330, 335, 346, 348-349, 382, 398, 423, 430-432, 438, 446, 458, 462-466, 470-475, 486-488
src\bots\base\login_page.py                                             94     73    22%   44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             60     39    35%   60, 64, 76-88, 100-137
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          98     72    27%   46, 50, 59-62, 68-75, 79-105, 109-121, 132-159, 163-171
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    177    14%   32-35, 39, 43-45, 51-71, 75-88, 92-118, 122-127, 139-211, 215-226, 236-265, 269-278, 282-290, 294-303
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            98     80    18%   29, 36, 40, 52-61, 66-73, 77-110, 114-120, 124-155
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           249    208    16%   56, 60, 72-75, 79-81, 85-100, 104-144, 149-169, 173-194, 198-229, 233-242, 246-271, 275-307, 313-344, 348-359, 363-380, 384-404, 408-419
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     87    20%   28-31, 35, 39-45, 49-66, 70-92, 96-125, 129-154, 158-163, 167-176
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     69    25%   29, 34, 39, 44, 49, 56-60, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159    135    15%   36-40, 43, 47-55, 59-76, 80-139, 149-202, 207-233, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       186    159    15%   46-47, 51-109, 113-114, 121-148, 154-183, 202-213, 223-230, 233-261, 268-304, 314-329, 334-374, 377-414, 418-433, 440-441
src\bots\safework\base.py                                               80     49    39%   39-42, 48-63, 67-102, 106-122, 126, 130
src\bots\safework\common\locators.py                                    30      0   100%
src\bots\safework\pages\login_page.py                                   71     55    23%   30-43, 47-79, 88-107, 115-116, 120-127
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     42    33%   30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           330    229    31%   50, 55, 67, 71, 80, 86, 106, 132-137, 145-149, 165, 169-209, 213-258, 262-302, 306-342, 346-406, 410-423, 427-432, 436-447, 452-463, 469-479, 483-485
src\bots\safework\pdl\search_bot.py                                    107     82    23%   47-48, 53, 58, 63, 75-115, 119-133, 145-159, 163-167, 176-219
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     88    21%   46-47, 52, 57, 62, 74-136, 140-147, 156-202, 206-208
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   40-41, 46, 51, 56, 68-132
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   53-54, 61-63, 69-71, 99-101
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             100     35    65%   61-63, 80-81, 135-137, 139-142, 144-147, 149-151, 153-157, 170-171, 176-181, 197-199
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     17    88%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 248, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   25-44
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157    126    20%   60-107, 112-143, 148-158, 163-185, 190-210, 215-238, 243-295, 300-312, 321-339
src\core\config_manager.py                                             293    165    44%   37, 76-85, 97-165, 182, 191, 213-219, 240, 245-246, 260-274, 283-284, 303-304, 326, 330-333, 351, 356, 368, 383, 393-406, 411-421, 430-457, 462-466, 478-480, 485-494, 503-521, 529-570
src\core\constants.py                                                  101      0   100%
src\core\contabilita_manager.py                                        102     51    50%   30, 35, 40, 49-61, 78-125, 134-141, 150-155, 164-171, 176, 181, 186, 191, 201, 210, 225
src\core\contabilita_queries.py                                         87     61    30%   19-30, 35-48, 53-78, 83-94, 100, 109-110, 115-126
src\core\contabilita_search.py                                          92     43    53%   26-82, 90, 110-111, 118-127, 138-139, 159-160
src\core\contabilita_stats.py                                           59     38    36%   32-52, 57-81, 86-100
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                          159    103    35%   36, 70-87, 100-110, 127-154, 171-209, 226-264, 279-314, 349, 374, 390, 392
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           121     40    67%   134-143, 152-182, 196-197, 225-227
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-21, 26-28, 33-39
src\core\database\migrations\pdl.py                                     34     27    21%   7-38, 43-91, 96-116, 121-125, 132-134
src\core\database\migrations\storico_oda.py                             11      8    27%   6-49, 56-58
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-32, 37-47, 52-69
src\core\database\pdl_queries.py                                       105     88    16%   23-37, 47-77, 83-137, 142-178, 186-251
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              59     36    39%   15-16, 24-26, 36-38, 43-58, 63-75, 80-87
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                                      181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      187    151    19%   14-15, 22-24, 61-99, 118-136, 140-157, 171-202, 206-273, 277-286, 303-305, 309-333
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            141     72    49%   72-74, 88-113, 124-156, 161-162, 167-172, 188, 194-195, 198, 208-210, 228-230, 243-245
src\core\license_validator.py                                          168    122    27%   42-46, 59-64, 79-100, 105-114, 119-123, 132-168, 178-196, 201-202, 212-227, 232-241, 246-271, 276-277, 282-283
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              36      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   63, 65, 86-87, 120, 166-199
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     20    83%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 222, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 60-68, 80-86, 90, 94, 107-119, 123-124, 128-129, 133-134, 143-157, 166-174, 197-203, 207-211, 215-228, 232-244, 248-250, 254-284, 288-304, 319, 324, 329
src\core\lyra_client.py                                                162    143    12%   27-40, 58-60, 64-77, 81-89, 93-94, 98-126, 130-161, 170-172, 181-214, 223-278, 287-316
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                       115     80    30%   51-55, 59-63, 67-75, 79-84, 88-92, 116-140, 152-154, 163, 167-174, 178-186, 190-198, 202, 206-209, 213-216
src\core\oda_manager.py                                                 34     19    44%   29, 43-75, 93-106
src\core\report_history.py                                              67     44    34%   26-28, 36-42, 47-51, 62-86, 96, 114-134, 147-157
src\core\schemas.py                                                     77     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             94     56    40%   31-49, 53-57, 61-71, 75-77, 81-85, 90, 95, 100-105, 110-115, 122-124, 129-132, 137-143
src\core\stats_manager.py                                               48     34    29%   27-30, 34, 44-55, 59, 69-78, 87-93, 102
src\core\sync_tracker.py                                                58     33    43%   39-50, 55-59, 72-81, 94-96, 110-122
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           207    167    19%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-143, 146-163, 167-178, 186-199, 210-218, 222-233, 237-249, 253-265, 268-282, 287-302, 307-323
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            344    290    16%   29-31, 35-44, 48-66, 70-73, 77-81, 85-89, 92-112, 115-134, 137-142, 146-160, 163-173, 176-179, 182-183, 186-192, 195-201, 204-225, 229-252, 255-259, 262-267, 271-286, 289-295, 298-311, 314-327, 331-336, 340-346, 350-356, 360-387, 391-404, 408-415, 418-424, 427-450, 453-465, 468-485
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      5    74%   30, 33-36, 55
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\activity_timeline.py                                143    121    15%   36-39, 53-96, 100-104, 108-111, 115, 119-120, 131-132, 145-165, 169-201, 205-210, 214-225, 229-264, 268-269
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 212-217, 221-226, 230-231, 240-265, 268-273
src\gui\components\scarico_ore\filters\popup_list.py                    98     84    14%   24-76, 79-86, 90-97, 101-108, 115-116, 125-138, 141-146
src\gui\components\scarico_ore\model.py                                168    137    18%   70-96, 105-118, 129-150, 154, 163-165, 175-189, 193-196, 200-207, 211-214, 218-220, 224-226, 230-256, 260-277, 283-285, 289-314
src\gui\controllers\bot_controller.py                                   44     33    25%   33-36, 45-50, 61-64, 77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           156    127    19%   33, 45-66, 70-86, 90-99, 103-107, 111-115, 119-123, 127-131, 135-139, 143-147, 151-155, 159-163, 167-171, 175-179, 183-189, 193-197, 201-205, 210-225, 235-251, 255-257, 261-262, 266-267, 271-289, 293-294
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              168    142    15%   47-54, 58-67, 74-111, 115-131, 135-232, 236-238, 242-246, 250-266, 270-279, 283, 287-292
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       66     57    14%   29-112, 115-122, 126
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-112, 115-120
src\gui\dialogs\bug_report_dialog.py                                   222    199    10%   61-65, 69-78, 95-100, 104-240, 244-252, 256-283, 290-311, 315-321, 335-417, 426-438
src\gui\dialogs\command_palette.py                                     296    265    10%   57-86, 90-146, 150-177, 181-189, 193-197, 201-207, 211-218, 222-250, 254-263, 267-273, 277-282, 286-289, 293-297, 301-309, 313-322, 326-333, 337-341, 345-382, 386-400, 404-410, 414-426
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   50-97, 101-109, 113-121, 136-137, 142-143, 148-149, 154-155
src\gui\dialogs\quick_actions_config.py                                 86     86     0%   1-214
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   23-69, 73, 78-80
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-377
src\gui\formatters.py                                                  131    113    14%   14-28, 38-68, 73, 90-96, 100-103, 107, 111, 115, 119-144, 150-152, 156-159, 163-242
src\gui\layouts\responsive.py                                           72     57    21%   17-21, 25-26, 30-31, 35-42, 46-50, 54-55, 59-74, 79-87, 91-93, 97-109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              70     52    26%   35-40, 44-50, 54-64, 68-79, 83-88, 98-185
src\gui\main_window\components\status_bar.py                           130    113    13%   39-43, 47-85, 89-92, 96-108, 112-124, 131-173, 180-215
src\gui\main_window\components\tool_bar.py                              26     17    35%   29-33, 45-47, 59-73
src\gui\main_window\components\tray_icon.py                             17     11    35%   25-28, 37, 52-61
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   26-28, 32-33, 44-59, 63, 67-73
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   26-27, 36-46, 53-64
src\gui\main_window\main.py                                            286    208    27%   59-109, 113-147, 160-163, 167-191, 195-202, 207, 211, 215, 219, 223, 227, 231, 235, 239-278, 282, 286-305, 309-313, 322-326, 335-339, 346-350, 357-359, 363-365, 369-371, 375-377, 381-383, 387-391, 395-406, 410-412, 416-436, 440-444, 451-454, 458-462, 466-468, 472-475, 482, 486-487, 493, 498, 503, 508, 513, 518
src\gui\main_window\page_index.py                                       26      0   100%
src\gui\models\audit_model.py                                          130     24    82%   79, 124, 137-138, 148, 154, 156, 166-168, 190-191, 197-200, 208, 210, 212, 214-215, 227-229
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 234     89    62%   55-59, 63-83, 95-99, 103-105, 159, 165-166, 170-171, 243-249, 262, 270, 279, 299-301, 335-355, 359-363, 367-372, 382-386, 390-403, 407, 419-422, 430, 435-445, 449-452
src\gui\panels\carico_ts.py                                             92     70    24%   35-43, 47-48, 52-56, 61-105, 109-111, 115-117, 126-134, 138-139, 143-196
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 29-32
src\gui\panels\contabilita_kpi\charts.py                               200    183     8%   21-61, 68-76, 79-82, 86-90, 93-157, 160-214, 217-279, 282-321, 324-370
src\gui\panels\contabilita_kpi\kpi_panel.py                            159    140    12%   38-61, 64-178, 191-195, 199-212, 215-225, 228, 231-302
src\gui\panels\contabilita_panel.py                                    228    197    14%   54-60, 64-70, 74-164, 168-172, 176, 187-198, 205-223, 227-244, 248-250, 254-257, 261-275, 279-321, 325-329, 333-350, 354-370
src\gui\panels\dashboard_panel.py                                      166    144    13%   42-96, 100, 104-111, 116-141, 145-147, 151-161, 165-179, 183-198, 203-219, 223-233, 237-242, 246-261, 265-287, 291-296
src\gui\panels\dettagli_oda.py                                         125     99    21%   39-46, 50-51, 55-59, 63-95, 99-101, 105, 109-118, 122-129, 133-135, 144-149, 153-210, 214-217
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 27     16    41%   34-35, 39-65, 74-76
src\gui\panels\dipendenti\pages\anagrafica_page.py                     398    360    10%   55-99, 102-240, 244-284, 288-301, 304-333, 336-378, 382-390, 394-408, 411-420, 424-455, 459-494, 503-543, 546-586, 589, 593-676, 679-684, 690-719
src\gui\panels\dipendenti\shared.py                                    151    134    11%   41-88, 119-198, 202-204, 208-210, 214-216, 225, 238-279, 292-327
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    153    127    17%   25-51, 56-99, 108-194, 199-210, 215-237, 242-299
src\gui\panels\dipendenti\widgets\employee_detail_view.py              104     91    12%   24-29, 32-135, 138-142, 150-162, 168-171
src\gui\panels\dipendenti_manager_panel.py                             185    165    11%   28-71, 75, 86-106, 109-134, 137-169, 172-198, 202-231, 235-252, 256-275, 278-293, 300-335
src\gui\panels\health_panel.py                                         233    200    14%   42-45, 50, 55-56, 60-66, 70-76, 80-97, 114-117, 121-139, 143-144, 158-159, 163-183, 187, 191, 202-210, 214-279, 283-298, 302-315, 319-334, 338-341, 345-347
src\gui\panels\help_panel.py                                           122     98    20%   39-42, 46-109, 113-133, 137-146, 150-158, 167-171, 175, 179, 183, 187, 191, 195, 199, 203, 207, 211, 215, 219
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        42     32    24%   20-32, 36-48, 52-58, 62-67
src\gui\panels\lyra\header.py                                           38     28    26%   23-25, 28-80
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 87-89
src\gui\panels\lyra\lyra_panel.py                                      163    134    18%   31-39, 42-96, 102-124, 127-140, 143-150, 153-154, 157-158, 161-163, 166-171, 174-176, 180-216, 219-221, 225-228, 232-234, 238, 241-253
src\gui\panels\lyra\workers.py                                          37     26    30%   23-30, 34-46, 55-58, 62-67
src\gui\panels\notifications_panel.py                                  243    196    19%   68-81, 85-143, 147-151, 155-157, 161-163, 167-169, 173-174, 178-179, 183, 187-188, 195-213, 217-232, 236-255, 259-264, 268-269, 273-283, 287-313, 317-318, 322-330, 334-364
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   78     66    15%   40-43, 47-86, 96-130, 134-136
src\gui\panels\pdl\pdl_filter_widget.py                                 66     51    23%   27-30, 33-107, 116
src\gui\panels\pdl\pdl_panel.py                                        373    336    10%   57-104, 108-174, 178-230, 234-247, 251-280, 284-296, 300-332, 336-374, 378-380, 384-385, 389-411, 415-421, 428-447, 451-506, 510-514, 518-532, 536-560, 564-596
src\gui\panels\pdl\programmazione_tab.py                               596    551     8%   54-63, 67-75, 79-91, 94-172, 179-187, 191-207, 210-371, 375-385, 389-390, 394-449, 452-456, 460, 464-465, 469-492, 496-544, 549-572, 576-577, 580-582, 586-589, 593-652, 655-709, 712-731, 736-873, 877-919, 922-1028
src\gui\panels\prenota_bp.py                                           109     89    18%   24-32, 35-36, 39-42, 46-81, 85-87, 90-98, 101-107, 110-112, 116-189
src\gui\panels\ricerca_pdl.py                                           88     71    19%   37-44, 48-49, 53-80, 84-87, 91-92, 96-101, 111-150, 155-161, 165-167
src\gui\panels\scarico_ore_panel.py                                    231    190    18%   56-58, 62-83, 87-89, 101-109, 113-166, 170-174, 178-190, 194, 198-201, 205-218, 222-225, 229-241, 247-262, 266-267, 271-275, 279-283, 287-288, 292-296, 300-311, 315-327, 331-334, 338-346
src\gui\panels\scarico_pdl.py                                          308    266    14%   43-60, 70-91, 101-134, 150-158, 162-163, 167-171, 175-300, 304-312, 316-319, 323-336, 340-345, 349, 353-355, 364-372, 377-383, 388-389, 393-426, 430-442, 446-468, 472-486, 490-497, 501-532, 536-538, 542, 546-560, 564-566
src\gui\panels\scarico_ts.py                                           126    102    19%   31-43, 49-50, 54-58, 62-97, 101-103, 107, 111-124, 128-136, 140-142, 148-157, 176-178, 189-243
src\gui\panels\settings\main_panel.py                                  108     80    26%   45-55, 59-105, 109-110, 114-116, 120-129, 133-136, 140, 144-146, 150-157, 161-171
src\gui\panels\settings\pages\diag_page.py                              31     19    39%   15-16, 19-38, 42-43
src\gui\panels\settings\pages\general_page.py                          117    102    13%   27-29, 32-123, 127-129, 133-145, 148-156, 160-171, 175-181
src\gui\panels\settings\pages\lists_page.py                            340    285    16%   35-36, 39-65, 70-87, 90-107, 110-129, 132-151, 154-173, 176-195, 202-208, 217-218, 225, 235, 253-264, 274-284, 289-296, 299-310, 313-321, 324-340, 343-350, 353-359, 364-373, 376-397, 400-407, 410-416, 421-422, 425-430, 433-436, 439-444, 447-450, 454, 457, 460, 463, 466, 469, 472, 475, 478, 481, 484, 487, 493-498, 502-507
src\gui\panels\settings\pages\paths_page.py                            128    103    20%   29-30, 33-81, 86-106, 110-131, 148-149, 152, 155-157, 160-162, 165-167, 170-172, 175-177, 180-182, 185-187, 193-214, 218-225
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 98-100
src\gui\panels\settings\tabs\backup_tab.py                             127    108    15%   48-49, 53-137, 146-153, 157-159, 163, 167-172, 176-177, 181-198, 202-212
src\gui\panels\settings\tabs\config_tab.py                              55     39    29%   41-43, 47-87, 99-101, 110-112
src\gui\panels\settings\tabs\telegram_tab.py                           139    117    16%   51-52, 56-142, 146-151, 155-161, 165-176, 180-184, 193-197, 206-218
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              42     36    14%   11-12, 15-74
src\gui\panels\storico_oda\oda_detail_view.py                           48     37    23%   21-24, 27-49, 53-67, 71-72
src\gui\panels\storico_oda\oda_filter_widget.py                         40     27    32%   24-27, 30-74, 78
src\gui\panels\storico_oda\oda_panel.py                                253    222    12%   43-106, 109-169, 173-181, 185-284, 287-302, 305, 308, 311-315, 318-324, 328-346, 350-408, 411-416, 419-439, 443-463
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     62     50    19%   16-39, 42-64, 72-112, 116-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    99     85    14%   28-33, 36-80, 84-105, 109-138, 143-150, 153-154, 159-161
src\gui\panels\timbrature\panel.py                                     173    149    14%   38-62, 65-97, 100-131, 134-174, 178-194, 198-233, 237-255, 258-265, 270, 273-296, 300
src\gui\panels\timbrature_bot.py                                       108     82    24%   43-51, 55-57, 61-65, 69-77, 81-83, 87-88, 92-100, 104-109, 118-123, 127-181, 185-187
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         67     50    25%   26-29, 34, 41-51, 55-92, 97-118, 123
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-91
src\gui\widgets\__init__.py                                             13      0   100%
src\gui\widgets\activity_feed.py                                       136    118    13%   29-180, 184, 188-190, 199-207, 210-258, 263, 268-314
src\gui\widgets\animated_progress_bar.py                                74     63    15%   38-50, 54-55, 59, 63-64, 68-69, 74-88, 92-150
src\gui\widgets\audit\audit_filter_bar.py                               79     14    82%   115-124, 141-142, 158, 160, 162
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   46, 60-61
src\gui\widgets\audit_log_widget.py                                    104     18    83%   92, 94, 123-133, 136, 139-140, 150, 178-180
src\gui\widgets\automazioni_widget.py                                   55     55     0%   1-132
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                 67     11    84%   132-147, 163
src\gui\widgets\autopilot\main_widget.py                               204     27    87%   69, 73, 167, 194-195, 197-198, 240-247, 251-254, 264, 280, 298, 323-329
src\gui\widgets\bot_parameters.py                                      110     85    23%   52-56, 60-122, 132-139, 143, 162-164, 168-176, 186, 195-197, 206-208, 218-223, 232, 241-242
src\gui\widgets\calendar_date_edit.py                                   17      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            221    188    15%   54-63, 67-140, 144, 148-162, 166-179, 183-194, 198-204, 208-213, 217-235, 239-242, 246-252, 256-259, 263-266, 270-273, 277-280, 284-288, 297-308, 312-321
src\gui\widgets\contabilita\certificati_tab.py                         571    519     9%   43-52, 55-242, 246-272, 276-346, 350-463, 508-520, 524-528, 532-536, 544-711, 715-716, 720-731, 736-738, 742-746, 750, 754-889, 898-920, 926-963, 968-979, 983-991, 995-998, 1002-1005, 1009-1023, 1026-1096, 1100-1102, 1106-1108, 1112-1148, 1155-1160, 1165-1207
src\gui\widgets\contabilita\giornaliere_tab.py                         189    158    16%   47-50, 54-95, 99, 102-129, 132-139, 143, 146-166, 169-189, 193-212, 215-240, 243-259
src\gui\widgets\contabilita\helpers.py                                  36     29    19%   11-35, 38-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                100     81    19%   25-26, 30-31, 35-52, 74-94, 97-138, 142, 146-167, 171-202, 206, 210
src\gui\widgets\data_table.py                                          108     84    22%   48-52, 55-126, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 214
src\gui\widgets\excel_table.py                                         336    295    12%   39-42, 56-68, 72-79, 83-99, 103-123, 127-128, 132-133, 137-148, 152-174, 178-201, 205-224, 228-248, 252-261, 265-270, 274-278, 282-286, 306-308, 312-331, 335-392, 396-399, 403-409, 413-435, 439-442, 446-448, 452, 461-478, 487-496, 500-528, 538-559
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   40-94, 98-105, 117-122, 126-130, 134-137, 146-152
src\gui\widgets\footer\components.py                                    55     36    35%   36-47, 56, 72-78, 88-95, 113-115, 124-125, 129-132, 136-137, 141-143, 161-162
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    35     27    23%   29-49, 58-60, 64-67, 71-74
src\gui\widgets\footer\telemetry.py                                     55     40    27%   33-64, 68-71, 75-77, 81-85
src\gui\widgets\info_widgets.py                                         90     74    18%   29-60, 64, 73-81, 86-110, 124-165, 169, 172
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        62     10    84%   69-70, 76-79, 83-86
src\gui\widgets\multi_select_filter.py                                  97     80    18%   26-78, 81-85, 88-91, 100-105, 114-129, 138-141, 150-151, 154-157, 160-164
src\gui\widgets\notification_card.py                                   240    209    13%   86-102, 106-354, 358-368, 372, 376-378, 392-423, 427-443, 447-452, 456-458, 462-463, 467-472, 476-480, 484-521, 525-531, 535-542
src\gui\widgets\notification_group_header.py                            47     36    23%   33-39, 43-124, 128-131, 135-136, 140, 144-145
src\gui\widgets\notification_item.py                                    72     59    18%   22-25, 28-125, 129-131, 134
src\gui\widgets\notification_toolbar.py                                104     78    25%   36-48, 52-64, 68-70, 74-78, 82-101, 133-139, 143-228, 233-234, 238-239, 244-251, 255-256, 265-267, 271, 275, 279
src\gui\widgets\pdl_timeline.py                                        127    127     0%   1-211
src\gui\widgets\priority_badge.py                                       47     35    26%   30-37, 41-78, 82-90, 94-98, 102, 106-108
src\gui\widgets\quick_actions.py                                        77     61    21%   24-32, 236-237, 240-263, 267-308, 313-353, 358
src\gui\widgets\security_dashboard.py                                  154    154     0%   1-252
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      237    205    14%   24-30, 48-81, 85-89, 93, 97-98, 102-105, 109-119, 123-131, 144-166, 170-172, 176-178, 182-185, 189-209, 213-231, 235-368, 372-373, 377-378, 382-412
src\gui\widgets\simple_chart.py                                         66     66     0%   1-113
src\gui\widgets\sortable_table_item.py                                  47     37    21%   21-26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   106     90    15%   27-28, 31-87, 92-124, 128-130, 134-147, 153-195
src\gui\widgets\status_card.py                                          60     47    22%   20-85, 89-92, 101-117, 121, 125-126
src\gui\widgets\status_indicator.py                                     43     36    16%   18-32, 42-59, 63-69
src\gui\widgets\timeline_widget.py                                     165     64    61%   51-80, 84-94, 117-142, 175-181, 185-187, 191-194, 198-202, 275, 279, 286, 291-292
src\gui\widgets\toast.py                                               131     99    24%   69-90, 94-133, 137-159, 163-168, 172-174, 178-179, 183-195, 207-209, 229-258, 264, 269, 274, 279
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-37, 41-44, 47-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     57    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-144, 157-164, 178-181, 194, 208, 222-228
src\utils\document_generator.py                                         17     14    18%   11-39
src\utils\document_processor.py                                         83     35    58%   14-15, 24-32, 38, 50-51, 59, 63-64, 71-72, 78-79, 81-82, 86-87, 95-96, 98-100, 106-111
src\utils\helpers.py                                                   111     66    41%   31-35, 49-71, 84-86, 91, 118-119, 124, 137-152, 166-168, 183-189, 204, 223, 237, 242-255, 265, 271-274
src\utils\log_humanizer.py                                              42     30    29%   13-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    51     44    14%   14-34, 40-56, 61-71, 76-84, 89-98
src\utils\printing.py                                                   90     73    19%   14-15, 24-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           59     19    68%   20-31, 61, 71, 112-118, 131-132, 145-146
src\utils\secure_logger.py                                              23     10    57%   47-54, 57-60
src\utils\security.py                                                   79     24    70%   43-44, 80-82, 102, 104, 109-111, 116, 119-124, 128-134
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   56-74, 87-98, 111-126, 139-160, 173-189, 202-205
--------------------------------------------------------------------------------------------------
TOTAL                                                                26239  18984    28%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_bot_base_cdp.py::TestBaseBotCDP::test_setup_driver_no_download_path
============================= 1 failed in 18.20s ==============================

```
</details>

---
### `tests/unit/test_bot_panels_deep_dive.py::TestBaseBotPanel::test_on_log_forward_to_telegram`
**Error:** `FAILED tests/unit/test_bot_panels_deep_dive.py::TestBaseBotPanel::test_on_log_forward_to_telegram`

**Timestamp:** `2026-02-20T15:23:00.344199`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_bot_panels_deep_dive.py F                                [100%]

================================== FAILURES ===================================
______________ TestBaseBotPanel.test_on_log_forward_to_telegram _______________
C:\Program Files\Python312\Lib\unittest\mock.py:918: in assert_called
    raise AssertionError(msg)
E   AssertionError: Expected 'send_message_sync' to have been called.

During handling of the above exception, another exception occurred:
tests\unit\test_bot_panels_deep_dive.py:139: in test_on_log_forward_to_telegram
    mock_win.telegram.send_message_sync.assert_called()
E   AssertionError: Expected 'send_message_sync' to have been called.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              303     32    89%   138-139, 144, 154, 330, 335, 346, 348-349, 382, 398, 423, 430-432, 438, 446, 458, 462-466, 470-475, 486-488
src\bots\base\login_page.py                                             94     73    22%   44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             60     39    35%   60, 64, 76-88, 100-137
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          98     72    27%   46, 50, 59-62, 68-75, 79-105, 109-121, 132-159, 163-171
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    177    14%   32-35, 39, 43-45, 51-71, 75-88, 92-118, 122-127, 139-211, 215-226, 236-265, 269-278, 282-290, 294-303
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            98     80    18%   29, 36, 40, 52-61, 66-73, 77-110, 114-120, 124-155
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           249    208    16%   56, 60, 72-75, 79-81, 85-100, 104-144, 149-169, 173-194, 198-229, 233-242, 246-271, 275-307, 313-344, 348-359, 363-380, 384-404, 408-419
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     87    20%   28-31, 35, 39-45, 49-66, 70-92, 96-125, 129-154, 158-163, 167-176
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     69    25%   29, 34, 39, 44, 49, 56-60, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159    135    15%   36-40, 43, 47-55, 59-76, 80-139, 149-202, 207-233, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       186    159    15%   46-47, 51-109, 113-114, 121-148, 154-183, 202-213, 223-230, 233-261, 268-304, 314-329, 334-374, 377-414, 418-433, 440-441
src\bots\safework\base.py                                               80     49    39%   39-42, 48-63, 67-102, 106-122, 126, 130
src\bots\safework\common\locators.py                                    30      0   100%
src\bots\safework\pages\login_page.py                                   71     55    23%   30-43, 47-79, 88-107, 115-116, 120-127
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     42    33%   30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           330    229    31%   50, 55, 67, 71, 80, 86, 106, 132-137, 145-149, 165, 169-209, 213-258, 262-302, 306-342, 346-406, 410-423, 427-432, 436-447, 452-463, 469-479, 483-485
src\bots\safework\pdl\search_bot.py                                    107     82    23%   47-48, 53, 58, 63, 75-115, 119-133, 145-159, 163-167, 176-219
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     88    21%   46-47, 52, 57, 62, 74-136, 140-147, 156-202, 206-208
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   40-41, 46, 51, 56, 68-132
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   53-54, 61-63, 69-71, 99-101
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             100     35    65%   61-63, 80-81, 135-137, 139-142, 144-147, 149-151, 153-157, 170-171, 176-181, 197-199
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     17    88%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 248, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   25-44
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157    126    20%   60-107, 112-143, 148-158, 163-185, 190-210, 215-238, 243-295, 300-312, 321-339
src\core\config_manager.py                                             293    155    47%   37, 76-85, 97-165, 182, 191, 213-219, 240, 245-246, 260-274, 283-284, 303-304, 326, 330-333, 351, 383, 393-406, 411-421, 430-457, 466, 478-480, 487-489, 494, 503-521, 529-570
src\core\constants.py                                                  101      0   100%
src\core\contabilita_manager.py                                        102     51    50%   30, 35, 40, 49-61, 78-125, 134-141, 150-155, 164-171, 176, 181, 186, 191, 201, 210, 225
src\core\contabilita_queries.py                                         87     61    30%   19-30, 35-48, 53-78, 83-94, 100, 109-110, 115-126
src\core\contabilita_search.py                                          92     43    53%   26-82, 90, 110-111, 118-127, 138-139, 159-160
src\core\contabilita_stats.py                                           59     38    36%   32-52, 57-81, 86-100
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                          159    103    35%   36, 70-87, 100-110, 127-154, 171-209, 226-264, 279-314, 349, 374, 390, 392
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           121     40    67%   134-143, 152-182, 196-197, 225-227
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-21, 26-28, 33-39
src\core\database\migrations\pdl.py                                     34     27    21%   7-38, 43-91, 96-116, 121-125, 132-134
src\core\database\migrations\storico_oda.py                             11      8    27%   6-49, 56-58
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-32, 37-47, 52-69
src\core\database\pdl_queries.py                                       105     88    16%   23-37, 47-77, 83-137, 142-178, 186-251
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              59     36    39%   15-16, 24-26, 36-38, 43-58, 63-75, 80-87
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                                      181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      187    151    19%   14-15, 22-24, 61-99, 118-136, 140-157, 171-202, 206-273, 277-286, 303-305, 309-333
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            141     72    49%   72-74, 88-113, 124-156, 161-162, 167-172, 188, 194-195, 198, 208-210, 228-230, 243-245
src\core\license_validator.py                                          168    122    27%   42-46, 59-64, 79-100, 105-114, 119-123, 132-168, 178-196, 201-202, 212-227, 232-241, 246-271, 276-277, 282-283
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              36      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   63, 65, 86-87, 120, 166-199
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     20    83%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 222, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 60-68, 80-86, 90, 94, 107-119, 123-124, 128-129, 133-134, 143-157, 166-174, 197-203, 207-211, 215-228, 232-244, 248-250, 254-284, 288-304, 319, 324, 329
src\core\lyra_client.py                                                162    143    12%   27-40, 58-60, 64-77, 81-89, 93-94, 98-126, 130-161, 170-172, 181-214, 223-278, 287-316
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                       115     80    30%   51-55, 59-63, 67-75, 79-84, 88-92, 116-140, 152-154, 163, 167-174, 178-186, 190-198, 202, 206-209, 213-216
src\core\oda_manager.py                                                 34     19    44%   29, 43-75, 93-106
src\core\report_history.py                                              67     44    34%   26-28, 36-42, 47-51, 62-86, 96, 114-134, 147-157
src\core\schemas.py                                                     77     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             94     56    40%   31-49, 53-57, 61-71, 75-77, 81-85, 90, 95, 100-105, 110-115, 122-124, 129-132, 137-143
src\core\stats_manager.py                                               48     16    67%   48-52, 54-55, 72, 74, 87-93, 102
src\core\sync_tracker.py                                                58     33    43%   39-50, 55-59, 72-81, 94-96, 110-122
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           207    167    19%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-143, 146-163, 167-178, 186-199, 210-218, 222-233, 237-249, 253-265, 268-282, 287-302, 307-323
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            344    290    16%   29-31, 35-44, 48-66, 70-73, 77-81, 85-89, 92-112, 115-134, 137-142, 146-160, 163-173, 176-179, 182-183, 186-192, 195-201, 204-225, 229-252, 255-259, 262-267, 271-286, 289-295, 298-311, 314-327, 331-336, 340-346, 350-356, 360-387, 391-404, 408-415, 418-424, 427-450, 453-465, 468-485
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      5    74%   30, 33-36, 55
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\activity_timeline.py                                143     85    41%   119-120, 145-165, 169-201, 205-210, 214-225, 229-264, 268-269
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 212-217, 221-226, 230-231, 240-265, 268-273
src\gui\components\scarico_ore\filters\popup_list.py                    98     84    14%   24-76, 79-86, 90-97, 101-108, 115-116, 125-138, 141-146
src\gui\components\scarico_ore\model.py                                168    137    18%   70-96, 105-118, 129-150, 154, 163-165, 175-189, 193-196, 200-207, 211-214, 218-220, 224-226, 230-256, 260-277, 283-285, 289-314
src\gui\controllers\bot_controller.py                                   44     33    25%   33-36, 45-50, 61-64, 77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           156    127    19%   33, 45-66, 70-86, 90-99, 103-107, 111-115, 119-123, 127-131, 135-139, 143-147, 151-155, 159-163, 167-171, 175-179, 183-189, 193-197, 201-205, 210-225, 235-251, 255-257, 261-262, 266-267, 271-289, 293-294
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              168    142    15%   47-54, 58-67, 74-111, 115-131, 135-232, 236-238, 242-246, 250-266, 270-279, 283, 287-292
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       66     57    14%   29-112, 115-122, 126
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-112, 115-120
src\gui\dialogs\bug_report_dialog.py                                   222    199    10%   61-65, 69-78, 95-100, 104-240, 244-252, 256-283, 290-311, 315-321, 335-417, 426-438
src\gui\dialogs\command_palette.py                                     296    265    10%   57-86, 90-146, 150-177, 181-189, 193-197, 201-207, 211-218, 222-250, 254-263, 267-273, 277-282, 286-289, 293-297, 301-309, 313-322, 326-333, 337-341, 345-382, 386-400, 404-410, 414-426
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   50-97, 101-109, 113-121, 136-137, 142-143, 148-149, 154-155
src\gui\dialogs\quick_actions_config.py                                 86     86     0%   1-214
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   23-69, 73, 78-80
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-377
src\gui\formatters.py                                                  131     67    49%   15, 23-28, 38-68, 73, 103, 107, 120, 126-128, 142, 170-222, 232-234, 239-240
src\gui\layouts\responsive.py                                           72     57    21%   17-21, 25-26, 30-31, 35-42, 46-50, 54-55, 59-74, 79-87, 91-93, 97-109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              70     52    26%   35-40, 44-50, 54-64, 68-79, 83-88, 98-185
src\gui\main_window\components\status_bar.py                           130    113    13%   39-43, 47-85, 89-92, 96-108, 112-124, 131-173, 180-215
src\gui\main_window\components\tool_bar.py                              26     17    35%   29-33, 45-47, 59-73
src\gui\main_window\components\tray_icon.py                             17     11    35%   25-28, 37, 52-61
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   26-28, 32-33, 44-59, 63, 67-73
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   26-27, 36-46, 53-64
src\gui\main_window\main.py                                            286    208    27%   59-109, 113-147, 160-163, 167-191, 195-202, 207, 211, 215, 219, 223, 227, 231, 235, 239-278, 282, 286-305, 309-313, 322-326, 335-339, 346-350, 357-359, 363-365, 369-371, 375-377, 381-383, 387-391, 395-406, 410-412, 416-436, 440-444, 451-454, 458-462, 466-468, 472-475, 482, 486-487, 493, 498, 503, 508, 513, 518
src\gui\main_window\page_index.py                                       26      0   100%
src\gui\models\audit_model.py                                          130     24    82%   79, 124, 137-138, 148, 154, 156, 166-168, 190-191, 197-200, 208, 210, 212, 214-215, 227-229
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 234     32    86%   63-83, 95-99, 159, 165-166, 170-171, 270, 279, 299-301, 419-422, 430, 451
src\gui\panels\carico_ts.py                                             92     27    71%   52-56, 109-111, 115-117, 128, 132, 138-139, 147-151, 155-162, 178-179
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 29-32
src\gui\panels\contabilita_kpi\charts.py                               200    183     8%   21-61, 68-76, 79-82, 86-90, 93-157, 160-214, 217-279, 282-321, 324-370
src\gui\panels\contabilita_kpi\kpi_panel.py                            159    140    12%   38-61, 64-178, 191-195, 199-212, 215-225, 228, 231-302
src\gui\panels\contabilita_panel.py                                    228    197    14%   54-60, 64-70, 74-164, 168-172, 176, 187-198, 205-223, 227-244, 248-250, 254-257, 261-275, 279-321, 325-329, 333-350, 354-370
src\gui\panels\dashboard_panel.py                                      166    144    13%   42-96, 100, 104-111, 116-141, 145-147, 151-161, 165-179, 183-198, 203-219, 223-233, 237-242, 246-261, 265-287, 291-296
src\gui\panels\dettagli_oda.py                                         125     65    48%   50-51, 55-59, 99-101, 105, 109-118, 123, 133-135, 146, 148, 153-210, 214-217
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 27     16    41%   34-35, 39-65, 74-76
src\gui\panels\dipendenti\pages\anagrafica_page.py                     398    360    10%   55-99, 102-240, 244-284, 288-301, 304-333, 336-378, 382-390, 394-408, 411-420, 424-455, 459-494, 503-543, 546-586, 589, 593-676, 679-684, 690-719
src\gui\panels\dipendenti\shared.py                                    151    134    11%   41-88, 119-198, 202-204, 208-210, 214-216, 225, 238-279, 292-327
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    153    127    17%   25-51, 56-99, 108-194, 199-210, 215-237, 242-299
src\gui\panels\dipendenti\widgets\employee_detail_view.py              104     91    12%   24-29, 32-135, 138-142, 150-162, 168-171
src\gui\panels\dipendenti_manager_panel.py                             185    165    11%   28-71, 75, 86-106, 109-134, 137-169, 172-198, 202-231, 235-252, 256-275, 278-293, 300-335
src\gui\panels\health_panel.py                                         233    200    14%   42-45, 50, 55-56, 60-66, 70-76, 80-97, 114-117, 121-139, 143-144, 158-159, 163-183, 187, 191, 202-210, 214-279, 283-298, 302-315, 319-334, 338-341, 345-347
src\gui\panels\help_panel.py                                           122     98    20%   39-42, 46-109, 113-133, 137-146, 150-158, 167-171, 175, 179, 183, 187, 191, 195, 199, 203, 207, 211, 215, 219
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        42     32    24%   20-32, 36-48, 52-58, 62-67
src\gui\panels\lyra\header.py                                           38     28    26%   23-25, 28-80
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 87-89
src\gui\panels\lyra\lyra_panel.py                                      163    134    18%   31-39, 42-96, 102-124, 127-140, 143-150, 153-154, 157-158, 161-163, 166-171, 174-176, 180-216, 219-221, 225-228, 232-234, 238, 241-253
src\gui\panels\lyra\workers.py                                          37     26    30%   23-30, 34-46, 55-58, 62-67
src\gui\panels\notifications_panel.py                                  243    196    19%   68-81, 85-143, 147-151, 155-157, 161-163, 167-169, 173-174, 178-179, 183, 187-188, 195-213, 217-232, 236-255, 259-264, 268-269, 273-283, 287-313, 317-318, 322-330, 334-364
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   78     66    15%   40-43, 47-86, 96-130, 134-136
src\gui\panels\pdl\pdl_filter_widget.py                                 66     51    23%   27-30, 33-107, 116
src\gui\panels\pdl\pdl_panel.py                                        373    336    10%   57-104, 108-174, 178-230, 234-247, 251-280, 284-296, 300-332, 336-374, 378-380, 384-385, 389-411, 415-421, 428-447, 451-506, 510-514, 518-532, 536-560, 564-596
src\gui\panels\pdl\programmazione_tab.py                               596    551     8%   54-63, 67-75, 79-91, 94-172, 179-187, 191-207, 210-371, 375-385, 389-390, 394-449, 452-456, 460, 464-465, 469-492, 496-544, 549-572, 576-577, 580-582, 586-589, 593-652, 655-709, 712-731, 736-873, 877-919, 922-1028
src\gui\panels\prenota_bp.py                                           109     89    18%   24-32, 35-36, 39-42, 46-81, 85-87, 90-98, 101-107, 110-112, 116-189
src\gui\panels\ricerca_pdl.py                                           88     71    19%   37-44, 48-49, 53-80, 84-87, 91-92, 96-101, 111-150, 155-161, 165-167
src\gui\panels\scarico_ore_panel.py                                    231    190    18%   56-58, 62-83, 87-89, 101-109, 113-166, 170-174, 178-190, 194, 198-201, 205-218, 222-225, 229-241, 247-262, 266-267, 271-275, 279-283, 287-288, 292-296, 300-311, 315-327, 331-334, 338-346
src\gui\panels\scarico_pdl.py                                          308     97    69%   101-134, 167-171, 208, 304-312, 316-319, 323-336, 340-345, 349, 353-355, 364-372, 377-383, 388-389, 401-404, 407, 412, 431-435, 438-441, 485, 495, 542, 547
src\gui\panels\scarico_ts.py                                           126     24    81%   56-58, 101-103, 122, 129, 140-142, 200-209, 217-221
src\gui\panels\settings\main_panel.py                                  108     80    26%   45-55, 59-105, 109-110, 114-116, 120-129, 133-136, 140, 144-146, 150-157, 161-171
src\gui\panels\settings\pages\diag_page.py                              31     19    39%   15-16, 19-38, 42-43
src\gui\panels\settings\pages\general_page.py                          117    102    13%   27-29, 32-123, 127-129, 133-145, 148-156, 160-171, 175-181
src\gui\panels\settings\pages\lists_page.py                            340    285    16%   35-36, 39-65, 70-87, 90-107, 110-129, 132-151, 154-173, 176-195, 202-208, 217-218, 225, 235, 253-264, 274-284, 289-296, 299-310, 313-321, 324-340, 343-350, 353-359, 364-373, 376-397, 400-407, 410-416, 421-422, 425-430, 433-436, 439-444, 447-450, 454, 457, 460, 463, 466, 469, 472, 475, 478, 481, 484, 487, 493-498, 502-507
src\gui\panels\settings\pages\paths_page.py                            128    103    20%   29-30, 33-81, 86-106, 110-131, 148-149, 152, 155-157, 160-162, 165-167, 170-172, 175-177, 180-182, 185-187, 193-214, 218-225
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 98-100
src\gui\panels\settings\tabs\backup_tab.py                             127    108    15%   48-49, 53-137, 146-153, 157-159, 163, 167-172, 176-177, 181-198, 202-212
src\gui\panels\settings\tabs\config_tab.py                              55     39    29%   41-43, 47-87, 99-101, 110-112
src\gui\panels\settings\tabs\telegram_tab.py                           139    117    16%   51-52, 56-142, 146-151, 155-161, 165-176, 180-184, 193-197, 206-218
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              42     36    14%   11-12, 15-74
src\gui\panels\storico_oda\oda_detail_view.py                           48     37    23%   21-24, 27-49, 53-67, 71-72
src\gui\panels\storico_oda\oda_filter_widget.py                         40     27    32%   24-27, 30-74, 78
src\gui\panels\storico_oda\oda_panel.py                                253    222    12%   43-106, 109-169, 173-181, 185-284, 287-302, 305, 308, 311-315, 318-324, 328-346, 350-408, 411-416, 419-439, 443-463
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     62     25    60%   72-112, 116-131
src\gui\panels\timbrature\components\settings_tab.py                    99      4    96%   147, 159-161
src\gui\panels\timbrature\panel.py                                     173     27    84%   148, 157, 237-255, 258-265, 280, 295-296, 300
src\gui\panels\timbrature_bot.py                                       108     25    77%   63-65, 81-83, 118-123, 129, 135-136, 139-143, 164-165, 185-187
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         67     50    25%   26-29, 34, 41-51, 55-92, 97-118, 123
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-91
src\gui\widgets\__init__.py                                             13      0   100%
src\gui\widgets\activity_feed.py                                       136    118    13%   29-180, 184, 188-190, 199-207, 210-258, 263, 268-314
src\gui\widgets\animated_progress_bar.py                                74     63    15%   38-50, 54-55, 59, 63-64, 68-69, 74-88, 92-150
src\gui\widgets\audit\audit_filter_bar.py                               79     14    82%   115-124, 141-142, 158, 160, 162
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   46, 60-61
src\gui\widgets\audit_log_widget.py                                    104     18    83%   92, 94, 123-133, 136, 139-140, 150, 178-180
src\gui\widgets\automazioni_widget.py                                   55     55     0%   1-132
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                 67     11    84%   132-147, 163
src\gui\widgets\autopilot\main_widget.py                               204     27    87%   69, 73, 167, 194-195, 197-198, 240-247, 251-254, 264, 280, 298, 323-329
src\gui\widgets\bot_parameters.py                                      110      3    97%   162-164
src\gui\widgets\calendar_date_edit.py                                   17      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            221    188    15%   54-63, 67-140, 144, 148-162, 166-179, 183-194, 198-204, 208-213, 217-235, 239-242, 246-252, 256-259, 263-266, 270-273, 277-280, 284-288, 297-308, 312-321
src\gui\widgets\contabilita\certificati_tab.py                         571    519     9%   43-52, 55-242, 246-272, 276-346, 350-463, 508-520, 524-528, 532-536, 544-711, 715-716, 720-731, 736-738, 742-746, 750, 754-889, 898-920, 926-963, 968-979, 983-991, 995-998, 1002-1005, 1009-1023, 1026-1096, 1100-1102, 1106-1108, 1112-1148, 1155-1160, 1165-1207
src\gui\widgets\contabilita\giornaliere_tab.py                         189    158    16%   47-50, 54-95, 99, 102-129, 132-139, 143, 146-166, 169-189, 193-212, 215-240, 243-259
src\gui\widgets\contabilita\helpers.py                                  36     29    19%   11-35, 38-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                100     81    19%   25-26, 30-31, 35-52, 74-94, 97-138, 142, 146-167, 171-202, 206, 210
src\gui\widgets\data_table.py                                          108     84    22%   48-52, 55-126, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 214
src\gui\widgets\excel_table.py                                         336    211    37%   56-68, 72-79, 83-99, 103-123, 127-128, 132-133, 137-148, 152-174, 178-201, 205-224, 228-248, 252-261, 265-270, 274-278, 282-286, 335-392, 403-409, 429, 439-442, 446-448, 517-521, 538-559
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   40-94, 98-105, 117-122, 126-130, 134-137, 146-152
src\gui\widgets\footer\components.py                                    55     36    35%   36-47, 56, 72-78, 88-95, 113-115, 124-125, 129-132, 136-137, 141-143, 161-162
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    35     27    23%   29-49, 58-60, 64-67, 71-74
src\gui\widgets\footer\telemetry.py                                     55     40    27%   33-64, 68-71, 75-77, 81-85
src\gui\widgets\info_widgets.py                                         90     74    18%   29-60, 64, 73-81, 86-110, 124-165, 169, 172
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        62     10    84%   69-70, 76-79, 83-86
src\gui\widgets\multi_select_filter.py                                  97     80    18%   26-78, 81-85, 88-91, 100-105, 114-129, 138-141, 150-151, 154-157, 160-164
src\gui\widgets\notification_card.py                                   240    209    13%   86-102, 106-354, 358-368, 372, 376-378, 392-423, 427-443, 447-452, 456-458, 462-463, 467-472, 476-480, 484-521, 525-531, 535-542
src\gui\widgets\notification_group_header.py                            47     36    23%   33-39, 43-124, 128-131, 135-136, 140, 144-145
src\gui\widgets\notification_item.py                                    72     59    18%   22-25, 28-125, 129-131, 134
src\gui\widgets\notification_toolbar.py                                104     78    25%   36-48, 52-64, 68-70, 74-78, 82-101, 133-139, 143-228, 233-234, 238-239, 244-251, 255-256, 265-267, 271, 275, 279
src\gui\widgets\pdl_timeline.py                                        127    127     0%   1-211
src\gui\widgets\priority_badge.py                                       47     35    26%   30-37, 41-78, 82-90, 94-98, 102, 106-108
src\gui\widgets\quick_actions.py                                        77     61    21%   24-32, 236-237, 240-263, 267-308, 313-353, 358
src\gui\widgets\security_dashboard.py                                  154    154     0%   1-252
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      237    205    14%   24-30, 48-81, 85-89, 93, 97-98, 102-105, 109-119, 123-131, 144-166, 170-172, 176-178, 182-185, 189-209, 213-231, 235-368, 372-373, 377-378, 382-412
src\gui\widgets\simple_chart.py                                         66     66     0%   1-113
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   106     90    15%   27-28, 31-87, 92-124, 128-130, 134-147, 153-195
src\gui\widgets\status_card.py                                          60      8    87%   101-117, 121, 125-126
src\gui\widgets\status_indicator.py                                     43     36    16%   18-32, 42-59, 63-69
src\gui\widgets\timeline_widget.py                                     165     37    78%   86-94, 117-142, 192-194, 198-202, 291-292
src\gui\widgets\toast.py                                               131     99    24%   69-90, 94-133, 137-159, 163-168, 172-174, 178-179, 183-195, 207-209, 229-258, 264, 269, 274, 279
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-37, 41-44, 47-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     57    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-144, 157-164, 178-181, 194, 208, 222-228
src\utils\document_generator.py                                         17     14    18%   11-39
src\utils\document_processor.py                                         83     35    58%   14-15, 24-32, 38, 50-51, 59, 63-64, 71-72, 78-79, 81-82, 86-87, 95-96, 98-100, 106-111
src\utils\helpers.py                                                   111     63    43%   31-35, 49-71, 84-86, 91, 118-119, 124, 137-152, 166-168, 183-189, 204, 223, 237, 242-255, 265, 274
src\utils\log_humanizer.py                                              42     14    67%   13-26, 110, 118
src\utils\parsing.py                                                    51     44    14%   14-34, 40-56, 61-71, 76-84, 89-98
src\utils\printing.py                                                   90     70    22%   14-15, 27-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           59     19    68%   20-31, 61, 71, 112-118, 131-132, 145-146
src\utils\secure_logger.py                                              23     10    57%   47-54, 57-60
src\utils\security.py                                                   79     24    70%   43-44, 80-82, 102, 104, 109-111, 116, 119-124, 128-134
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   56-74, 87-98, 111-126, 139-160, 173-189, 202-205
--------------------------------------------------------------------------------------------------
TOTAL                                                                26239  17950    32%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_bot_panels_deep_dive.py::TestBaseBotPanel::test_on_log_forward_to_telegram
============================= 1 failed in 18.77s ==============================

```
</details>

---
### `tests/unit/test_data_table_deep.py::test_data_table_init`
**Error:** `FAILED tests/unit/test_data_table_deep.py::test_data_table_init - NameError: ...`

**Timestamp:** `2026-02-20T15:43:21.060922`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_data_table_deep.py F                                     [100%]

================================== FAILURES ===================================
____________________________ test_data_table_init _____________________________
tests\unit\test_data_table_deep.py:26: in test_data_table_init
    table = DataTable(columns)
            ^^^^^^^^^^^^^^^^^^
src\gui\widgets\data_table.py:54: in __init__
    self._setup_ui()
src\gui\widgets\data_table.py:79: in _setup_ui
    border: 2px solid #00E5FF;
    ^^^^^^
E   NameError: name 'border' is not defined
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              303     28    91%   138-139, 154, 330, 335, 346, 348-349, 382, 398, 423, 438, 446, 458, 462-466, 470-475, 486-488
src\bots\base\login_page.py                                             94     73    22%   44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             60     10    83%   64, 78, 82, 112, 118-119, 124-125, 136-137
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          98     72    27%   46, 50, 59-62, 68-75, 79-105, 109-121, 132-159, 163-171
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    177    14%   32-35, 39, 43-45, 51-71, 75-88, 92-118, 122-127, 139-211, 215-226, 236-265, 269-278, 282-290, 294-303
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            98     80    18%   29, 36, 40, 52-61, 66-73, 77-110, 114-120, 124-155
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           249    169    32%   56, 60, 79-81, 85-100, 104-144, 149-169, 173-194, 198-229, 233-242, 246-271, 276, 305-307, 313-344, 348-359, 377, 384-404, 413-414
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     87    20%   28-31, 35, 39-45, 49-66, 70-92, 96-125, 129-154, 158-163, 167-176
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   47-55, 74-76, 80-139, 162-163, 174-177, 180, 196-197, 201-202, 207-233, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       186    142    24%   99-100, 121-148, 154-183, 202-213, 223-230, 233-261, 268-304, 314-329, 334-374, 377-414, 418-433, 440-441
src\bots\safework\base.py                                               80     49    39%   39-42, 48-63, 67-102, 106-122, 126, 130
src\bots\safework\common\locators.py                                    30      0   100%
src\bots\safework\pages\login_page.py                                   71     55    23%   30-43, 47-79, 88-107, 115-116, 120-127
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     42    33%   30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           330    189    43%   50, 55, 67, 71, 80, 86, 106, 132-137, 145-149, 165, 170, 179-181, 188-209, 213-258, 262-302, 306-342, 347, 360-362, 379-382, 388, 398-406, 410-423, 427-432, 436-447, 452-463, 469-479, 483-485
src\bots\safework\pdl\search_bot.py                                    107     82    23%   47-48, 53, 58, 63, 75-115, 119-133, 145-159, 163-167, 176-219
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     69    38%   52, 57, 62, 74-136, 140-147, 170, 176, 181-197, 201-202, 206-208
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   40-41, 46, 51, 56, 68-132
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   53-54, 61-63, 69-71, 99-101
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             100     35    65%   61-63, 80-81, 135-137, 139-142, 144-147, 149-151, 153-157, 170-171, 176-181, 197-199
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     17    88%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 248, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   25-44
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config_manager.py                                             293     89    70%   76-85, 97-165, 182, 219, 240, 263, 326, 383, 400-401, 430-457, 494, 503-521, 533, 541, 569-570
src\core\constants.py                                                  101      0   100%
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87     16    82%   29-30, 47-48, 54, 77-78, 84, 93-94, 100, 109-110, 116, 125-126
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                          159      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           121     20    83%   139-143, 172-182, 196-197, 225-227
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     34      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\database\pdl_queries.py                                       105     88    16%   23-37, 47-77, 83-137, 142-178, 186-251
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44      5    89%   50, 62, 73, 77, 99
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              59     17    71%   15-16, 24-26, 52-57, 71-75, 85-87
src\core\importers\certificati.py                                      116     21    82%   38, 47, 51, 54-55, 64, 91, 105-106, 141, 150, 162, 166-167, 171, 174-179
src\core\importers\contabilita.py                                      133     29    78%   42, 49-57, 70, 78, 88, 102-104, 118, 126, 138-139, 148, 186-187, 190-192, 213, 233, 235
src\core\importers\giornaliere.py                                      181    140    23%   44, 49-62, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      187    151    19%   14-15, 22-24, 61-99, 118-136, 140-157, 171-202, 206-273, 277-286, 303-305, 309-333
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            141     72    49%   72-74, 88-113, 124-156, 161-162, 167-172, 188, 194-195, 198, 208-210, 228-230, 243-245
src\core\license_validator.py                                          168    122    27%   42-46, 59-64, 79-100, 105-114, 119-123, 132-168, 178-196, 201-202, 212-227, 232-241, 246-271, 276-277, 282-283
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              36      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   63, 65, 86-87, 120, 166-199
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 60-68, 80-86, 90, 94, 107-119, 123-124, 128-129, 133-134, 143-157, 166-174, 197-203, 207-211, 215-228, 232-244, 248-250, 254-284, 288-304, 319, 324, 329
src\core\lyra_client.py                                                162    143    12%   27-40, 58-60, 64-77, 81-89, 93-94, 98-126, 130-161, 170-172, 181-214, 223-278, 287-316
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                       115     80    30%   51-55, 59-63, 67-75, 79-84, 88-92, 116-140, 152-154, 163, 167-174, 178-186, 190-198, 202, 206-209, 213-216
src\core\oda_manager.py                                                 34     19    44%   29, 43-75, 93-106
src\core\report_history.py                                              67     44    34%   26-28, 36-42, 47-51, 62-86, 96, 114-134, 147-157
src\core\schemas.py                                                     77     25    68%   68-73, 78-89, 94-96, 101-103, 109
src\core\secrets_manager.py                                             94     49    48%   31-49, 53-57, 61-71, 75-77, 81-85, 90, 95, 105, 112-115, 122-124, 131-132, 137-143
src\core\stats_manager.py                                               48     11    77%   48-52, 54-55, 72, 74, 90, 102
src\core\sync_tracker.py                                                58     33    43%   39-50, 55-59, 72-81, 94-96, 110-122
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           207    167    19%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-143, 146-163, 167-178, 186-199, 210-218, 222-233, 237-249, 253-265, 268-282, 287-302, 307-323
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            344    290    16%   29-31, 35-44, 48-66, 70-73, 77-81, 85-89, 92-112, 115-134, 137-142, 146-160, 163-173, 176-179, 182-183, 186-192, 195-201, 204-225, 229-252, 255-259, 262-267, 271-286, 289-295, 298-311, 314-327, 331-336, 340-346, 350-356, 360-387, 391-404, 408-415, 418-424, 427-450, 453-465, 468-485
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\activity_timeline.py                                143     85    41%   119-120, 145-165, 169-201, 205-210, 214-225, 229-264, 268-269
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 212-217, 221-226, 230-231, 240-265, 268-273
src\gui\components\scarico_ore\filters\popup_list.py                    98     84    14%   24-76, 79-86, 90-97, 101-108, 115-116, 125-138, 141-146
src\gui\components\scarico_ore\model.py                                168    137    18%   70-96, 105-118, 129-150, 154, 163-165, 175-189, 193-196, 200-207, 211-214, 218-220, 224-226, 230-256, 260-277, 283-285, 289-314
src\gui\controllers\bot_controller.py                                   44     17    61%   45-50, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           156    118    24%   45-66, 70-86, 90-99, 103-107, 111-115, 119-123, 127-131, 135-139, 143-147, 151-155, 159-163, 167-171, 175-179, 183-189, 193-197, 201-205, 210-225, 236-237, 255-257, 261-262, 266-267, 271-289, 293-294
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              168    142    15%   47-54, 58-67, 74-111, 115-131, 135-232, 236-238, 242-246, 250-266, 270-279, 283, 287-292
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       66     57    14%   29-112, 115-122, 126
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-112, 115-120
src\gui\dialogs\bug_report_dialog.py                                   222    199    10%   61-65, 69-78, 95-100, 104-240, 244-252, 256-283, 290-311, 315-321, 335-417, 426-438
src\gui\dialogs\command_palette.py                                     296    265    10%   57-86, 90-146, 150-177, 181-189, 193-197, 201-207, 211-218, 222-250, 254-263, 267-273, 277-282, 286-289, 293-297, 301-309, 313-322, 326-333, 337-341, 345-382, 386-400, 404-410, 414-426
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   50-97, 101-109, 113-121, 136-137, 142-143, 148-149, 154-155
src\gui\dialogs\quick_actions_config.py                                 86      1    99%   155
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   23-69, 73, 78-80
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-377
src\gui\formatters.py                                                  131     67    49%   15, 23-28, 38-68, 73, 103, 107, 120, 126-128, 142, 170-222, 232-234, 239-240
src\gui\layouts\responsive.py                                           72     57    21%   17-21, 25-26, 30-31, 35-42, 46-50, 54-55, 59-74, 79-87, 91-93, 97-109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              70     52    26%   35-40, 44-50, 54-64, 68-79, 83-88, 98-185
src\gui\main_window\components\status_bar.py                           130    113    13%   39-43, 47-85, 89-92, 96-108, 112-124, 131-173, 180-215
src\gui\main_window\components\tool_bar.py                              26     17    35%   29-33, 45-47, 59-73
src\gui\main_window\components\tray_icon.py                             17     11    35%   25-28, 37, 52-61
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   26-28, 32-33, 44-59, 63, 67-73
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   26-27, 36-46, 53-64
src\gui\main_window\main.py                                            286    208    27%   59-109, 113-147, 160-163, 167-191, 195-202, 207, 211, 215, 219, 223, 227, 231, 235, 239-278, 282, 286-305, 309-313, 322-326, 335-339, 346-350, 357-359, 363-365, 369-371, 375-377, 381-383, 387-391, 395-406, 410-412, 416-436, 440-444, 451-454, 458-462, 466-468, 472-475, 482, 486-487, 493, 498, 503, 508, 513, 518
src\gui\main_window\page_index.py                                       26      0   100%
src\gui\models\audit_model.py                                          130     24    82%   79, 124, 137-138, 148, 154, 156, 166-168, 190-191, 197-200, 208, 210, 212, 214-215, 227-229
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 234     32    86%   63-83, 95-99, 159, 165-166, 170-171, 270, 279, 299-301, 419-422, 430, 451
src\gui\panels\carico_ts.py                                             95     37    61%   52-56, 63-67, 78, 104, 106-108, 112, 114, 118, 120, 129, 133, 135-137, 142, 147-152, 156-164, 180-181, 188, 198-199
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               200     43    78%   96-97, 102-104, 129-137, 140-153, 165-166, 187, 220-221, 228-230, 287-288, 310-312, 327-328
src\gui\panels\contabilita_kpi\kpi_panel.py                            159      4    97%   207, 232, 301-302
src\gui\panels\contabilita_panel.py                                    228     93    59%   64-70, 168-172, 197, 205-223, 227-244, 248-250, 254-257, 265-275, 286, 290, 294-296, 318, 329, 333-350, 354-370
src\gui\panels\dashboard_panel.py                                      166     71    57%   100, 145-147, 154, 156, 159-161, 166-167, 169-178, 194-197, 204-206, 209, 216-219, 223-233, 237-242, 246-261, 265-287, 291-296
src\gui\panels\dettagli_oda.py                                         125     64    49%   50-51, 55-59, 99-101, 105, 109-118, 123, 133-135, 148, 153-210, 214-217
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 27     16    41%   34-35, 39-65, 74-76
src\gui\panels\dipendenti\pages\anagrafica_page.py                     398    360    10%   55-99, 102-240, 244-284, 288-301, 304-333, 336-378, 382-390, 394-408, 411-420, 424-455, 459-494, 503-543, 546-586, 589, 593-676, 679-684, 690-719
src\gui\panels\dipendenti\shared.py                                    151    134    11%   41-88, 119-198, 202-204, 208-210, 214-216, 225, 238-279, 292-327
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    153    127    17%   25-51, 56-99, 108-194, 199-210, 215-237, 242-299
src\gui\panels\dipendenti\widgets\employee_detail_view.py              104     91    12%   24-29, 32-135, 138-142, 150-162, 168-171
src\gui\panels\dipendenti_manager_panel.py                             185    165    11%   28-71, 75, 86-106, 109-134, 137-169, 172-198, 202-231, 235-252, 256-275, 278-293, 300-335
src\gui\panels\health_panel.py                                         233    200    14%   42-45, 50, 55-56, 60-66, 70-76, 80-97, 114-117, 121-139, 143-144, 158-159, 163-183, 187, 191, 202-210, 214-279, 283-298, 302-315, 319-334, 338-341, 345-347
src\gui\panels\help_panel.py                                           122     98    20%   39-42, 46-109, 113-133, 137-146, 150-158, 167-171, 175, 179, 183, 187, 191, 195, 199, 203, 207, 211, 215, 219
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        42     32    24%   20-32, 36-48, 52-58, 62-67
src\gui\panels\lyra\header.py                                           38     28    26%   23-25, 28-80
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 87-89
src\gui\panels\lyra\lyra_panel.py                                      163    134    18%   31-39, 42-96, 102-124, 127-140, 143-150, 153-154, 157-158, 161-163, 166-171, 174-176, 180-216, 219-221, 225-228, 232-234, 238, 241-253
src\gui\panels\lyra\workers.py                                          37     26    30%   23-30, 34-46, 55-58, 62-67
src\gui\panels\notifications_panel.py                                  243    196    19%   68-81, 85-143, 147-151, 155-157, 161-163, 167-169, 173-174, 178-179, 183, 187-188, 195-213, 217-232, 236-255, 259-264, 268-269, 273-283, 287-313, 317-318, 322-330, 334-364
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   78     66    15%   40-43, 47-86, 96-130, 134-136
src\gui\panels\pdl\pdl_filter_widget.py                                 66     51    23%   27-30, 33-107, 116
src\gui\panels\pdl\pdl_panel.py                                        373    336    10%   57-104, 108-174, 178-230, 234-247, 251-280, 284-296, 300-332, 336-374, 378-380, 384-385, 389-411, 415-421, 428-447, 451-506, 510-514, 518-532, 536-560, 564-596
src\gui\panels\pdl\programmazione_tab.py                               596    551     8%   54-63, 67-75, 79-91, 94-172, 179-187, 191-207, 210-371, 375-385, 389-390, 394-449, 452-456, 460, 464-465, 469-492, 496-544, 549-572, 576-577, 580-582, 586-589, 593-652, 655-709, 712-731, 736-873, 877-919, 922-1028
src\gui\panels\prenota_bp.py                                           110     85    23%   24-32, 35-36, 39-42, 47-81, 87-88, 92-99, 103-108, 112-113, 118-191
src\gui\panels\ricerca_pdl.py                                           88     71    19%   37-44, 48-49, 53-80, 84-87, 91-92, 96-101, 111-150, 155-161, 165-167
src\gui\panels\scarico_ore_panel.py                                    231    190    18%   56-58, 62-83, 87-89, 101-109, 113-166, 170-174, 178-190, 194, 198-201, 205-218, 222-225, 229-241, 247-262, 266-267, 271-275, 279-283, 287-288, 292-296, 300-311, 315-327, 331-334, 338-346
src\gui\panels\scarico_pdl.py                                          339    176    48%   42, 58, 69, 74, 77, 84, 89, 100-133, 155-157, 161, 166-170, 194-203, 207-212, 216, 219-220, 240-252, 254-261, 269, 273, 278, 289, 294, 303-313, 315-320, 322-334, 339, 346, 350, 352-353, 358-370, 375-379, 383, 387-389, 398, 400-404, 412-413, 423, 427, 431-436, 438-443, 445, 453-454, 466-467, 469-471, 473, 489, 502, 520, 524, 528, 535, 541-543, 553, 561-563, 570-572, 576, 580-594, 598-600
src\gui\panels\scarico_ts.py                                           127     53    58%   56-58, 65-66, 71-72, 76, 91, 96-98, 102-104, 108, 113, 118, 122-125, 129-130, 137, 141-143, 149, 153-156, 179, 190, 194-210, 213-222, 233, 237, 244
src\gui\panels\settings\main_panel.py                                  108     80    26%   45-55, 59-105, 109-110, 114-116, 120-129, 133-136, 140, 144-146, 150-157, 161-171
src\gui\panels\settings\pages\diag_page.py                              31     19    39%   15-16, 19-38, 42-43
src\gui\panels\settings\pages\general_page.py                          117    102    13%   27-29, 32-123, 127-129, 133-145, 148-156, 160-171, 175-181
src\gui\panels\settings\pages\lists_page.py                            340    285    16%   35-36, 39-65, 70-87, 90-107, 110-129, 132-151, 154-173, 176-195, 202-208, 217-218, 225, 235, 253-264, 274-284, 289-296, 299-310, 313-321, 324-340, 343-350, 353-359, 364-373, 376-397, 400-407, 410-416, 421-422, 425-430, 433-436, 439-444, 447-450, 454, 457, 460, 463, 466, 469, 472, 475, 478, 481, 484, 487, 493-498, 502-507
src\gui\panels\settings\pages\paths_page.py                            128    103    20%   29-30, 33-81, 86-106, 110-131, 148-149, 152, 155-157, 160-162, 165-167, 170-172, 175-177, 180-182, 185-187, 193-214, 218-225
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 98-100
src\gui\panels\settings\tabs\backup_tab.py                             127    108    15%   48-49, 53-137, 146-153, 157-159, 163, 167-172, 176-177, 181-198, 202-212
src\gui\panels\settings\tabs\config_tab.py                              55     39    29%   41-43, 47-87, 99-101, 110-112
src\gui\panels\settings\tabs\telegram_tab.py                           139    117    16%   51-52, 56-142, 146-151, 155-161, 165-176, 180-184, 193-197, 206-218
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              42     36    14%   11-12, 15-74
src\gui\panels\storico_oda\oda_detail_view.py                           48     37    23%   21-24, 27-49, 53-67, 71-72
src\gui\panels\storico_oda\oda_filter_widget.py                         40     27    32%   24-27, 30-74, 78
src\gui\panels\storico_oda\oda_panel.py                                253    222    12%   43-106, 109-169, 173-181, 185-284, 287-302, 305, 308, 311-315, 318-324, 328-346, 350-408, 411-416, 419-439, 443-463
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     62     25    60%   72-112, 116-131
src\gui\panels\timbrature\components\settings_tab.py                    99      4    96%   147, 159-161
src\gui\panels\timbrature\panel.py                                     173     27    84%   148, 157, 237-255, 258-265, 280, 295-296, 300
src\gui\panels\timbrature_bot.py                                       109     33    70%   63-65, 71, 76, 83-84, 89, 99, 110, 120-124, 129-130, 133, 136-137, 140-144, 147, 165-166, 175, 182, 187-189
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         67     50    25%   26-29, 34, 41-51, 55-92, 97-118, 123
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-91
src\gui\widgets\__init__.py                                             13      0   100%
src\gui\widgets\activity_feed.py                                       136     22    84%   39-40, 88-90, 146-147, 167-177, 184, 188-190, 263, 269, 280, 282
src\gui\widgets\animated_progress_bar.py                                74     63    15%   38-50, 54-55, 59, 63-64, 68-69, 74-88, 92-150
src\gui\widgets\audit\audit_filter_bar.py                               79     14    82%   115-124, 141-142, 158, 160, 162
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   46, 60-61
src\gui\widgets\audit_log_widget.py                                    104     18    83%   92, 94, 123-133, 136, 139-140, 150, 178-180
src\gui\widgets\automazioni_widget.py                                   55     55     0%   1-132
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                 67     11    84%   132-147, 163
src\gui\widgets\autopilot\main_widget.py                               204     27    87%   69, 73, 167, 194-195, 197-198, 240-247, 251-254, 264, 280, 298, 323-329
src\gui\widgets\bot_parameters.py                                      147     76    48%   57, 59, 64, 66, 100-101, 105, 120, 123, 125-131, 133, 136, 145-156, 158-159, 161-165, 170, 177-178, 180-185, 189-191, 194, 198, 209-217, 247-249, 253-261, 271, 280-282, 291-293, 303-308, 317, 326-327
src\gui\widgets\calendar_date_edit.py                                   17      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            221     61    72%   116, 138, 144, 168, 200, 210-213, 234, 239-242, 246-252, 256-259, 263-266, 270-273, 277-280, 284-288, 297-308, 312-321
src\gui\widgets\contabilita\certificati_tab.py                         571    142    75%   159, 167, 172-175, 320, 338, 443-446, 462-463, 559, 715-716, 723, 738, 746, 750, 775-776, 937-939, 942-944, 990, 995-998, 1002-1005, 1009-1023, 1026-1096, 1112-1148, 1155-1160, 1165-1207
src\gui\widgets\contabilita\giornaliere_tab.py                         189    158    16%   47-50, 54-95, 99, 102-129, 132-139, 143, 146-166, 169-189, 193-212, 215-240, 243-259
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                100     81    19%   25-26, 30-31, 35-52, 74-94, 97-138, 142, 146-167, 171-202, 206, 210
src\gui\widgets\data_table.py                                          120     78    35%   83-110, 137-163, 167-168, 175-176, 179-184, 187-204, 207-211, 213, 217-225, 228-230, 234-249, 256
src\gui\widgets\excel_table.py                                         349    250    28%   59-71, 75-82, 86-100, 102, 106-124, 126, 131, 136, 140-151, 155-175, 177, 181-202, 204, 208-225, 227, 231-249, 251, 255-262, 264, 268-271, 273, 277-279, 281, 285-288, 309, 311, 348-375, 379-392, 395, 405-406, 423-424, 432, 436, 440-443, 447-451, 453, 457-460, 470, 479, 483-486, 510-513, 517-522, 531-540, 544-572, 582-603
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   40-94, 98-105, 117-122, 126-130, 134-137, 146-152
src\gui\widgets\footer\components.py                                    55     36    35%   36-47, 56, 72-78, 88-95, 113-115, 124-125, 129-132, 136-137, 141-143, 161-162
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    35     27    23%   29-49, 58-60, 64-67, 71-74
src\gui\widgets\footer\telemetry.py                                     55     40    27%   33-64, 68-71, 75-77, 81-85
src\gui\widgets\info_widgets.py                                         90     39    57%   29-60, 64, 86-110, 172
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        62     10    84%   69-70, 76-79, 83-86
src\gui\widgets\multi_select_filter.py                                  97     80    18%   26-78, 81-85, 88-91, 100-105, 114-129, 138-141, 150-151, 154-157, 160-164
src\gui\widgets\notification_card.py                                   240    209    13%   86-102, 106-354, 358-368, 372, 376-378, 392-423, 427-443, 447-452, 456-458, 462-463, 467-472, 476-480, 484-521, 525-531, 535-542
src\gui\widgets\notification_group_header.py                            47     36    23%   33-39, 43-124, 128-131, 135-136, 140, 144-145
src\gui\widgets\notification_item.py                                    72     59    18%   22-25, 28-125, 129-131, 134
src\gui\widgets\notification_toolbar.py                                104     78    25%   36-48, 52-64, 68-70, 74-78, 82-101, 133-139, 143-228, 233-234, 238-239, 244-251, 255-256, 265-267, 271, 275, 279
src\gui\widgets\pdl_timeline.py                                        127    127     0%   1-211
src\gui\widgets\priority_badge.py                                       47     35    26%   30-37, 41-78, 82-90, 94-98, 102, 106-108
src\gui\widgets\quick_actions.py                                        77     13    83%   267-308, 324, 352-353
src\gui\widgets\security_dashboard.py                                  154    154     0%   1-252
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      237    205    14%   24-30, 48-81, 85-89, 93, 97-98, 102-105, 109-119, 123-131, 144-166, 170-172, 176-178, 182-185, 189-209, 213-231, 235-368, 372-373, 377-378, 382-412
src\gui\widgets\simple_chart.py                                         66     66     0%   1-113
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   106     90    15%   27-28, 31-87, 92-124, 128-130, 134-147, 153-195
src\gui\widgets\status_card.py                                          60      8    87%   101-117, 121, 125-126
src\gui\widgets\status_indicator.py                                     43     36    16%   18-32, 42-59, 63-69
src\gui\widgets\timeline_widget.py                                     165     37    78%   86-94, 117-142, 192-194, 198-202, 291-292
src\gui\widgets\toast.py                                               131     99    24%   69-90, 94-133, 137-159, 163-168, 172-174, 178-179, 183-195, 207-209, 229-258, 264, 269, 274, 279
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-37, 41-44, 47-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     57    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-144, 157-164, 178-181, 194, 208, 222-228
src\utils\document_generator.py                                         17     14    18%   11-39
src\utils\document_processor.py                                         83     31    63%   14-15, 24-32, 38, 50-51, 59, 63-64, 71-72, 81-82, 95-96, 98-100, 106-111
src\utils\helpers.py                                                   111     62    44%   31-35, 49-71, 84-86, 91, 118-119, 124, 137-152, 166-168, 183-189, 204, 223, 237, 242-255, 274
src\utils\log_humanizer.py                                              42     10    76%   19-26, 110, 118
src\utils\parsing.py                                                    51      6    88%   15, 18, 46-47, 84, 91
src\utils\printing.py                                                   90     70    22%   14-15, 27-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           59     19    68%   20-31, 61, 71, 112-118, 131-132, 145-146
src\utils\secure_logger.py                                              23     10    57%   47-54, 57-60
src\utils\security.py                                                   79     24    70%   43-44, 80-82, 102, 104, 109-111, 116, 119-124, 128-134
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   56-74, 87-98, 111-126, 139-160, 173-189, 202-205
--------------------------------------------------------------------------------------------------
TOTAL                                                                26338  15854    40%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_data_table_deep.py::test_data_table_init - NameError: ...
============================== 1 failed in 8.01s ==============================

```
</details>

---
### `tests/unit/test_horizontal_timeline.py::test_horizontal_timeline_functionality`
**Error:** `FAILED tests/unit/test_horizontal_timeline.py::test_horizontal_timeline_functionality`

**Timestamp:** `2026-02-20T16:06:57.617347`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_horizontal_timeline.py F                                 [100%]

================================== FAILURES ===================================
___________________ test_horizontal_timeline_functionality ____________________
tests\unit\test_horizontal_timeline.py:33: in test_horizontal_timeline_functionality
    layout = widget.timeline.container.main_layout
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'HorizontalTimelineContainer' object has no attribute 'main_layout'. Did you mean: 'log_layout'?
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              303     28    91%   138-139, 154, 330, 335, 346, 348-349, 382, 398, 423, 438, 446, 458, 462-466, 470-475, 486-488
src\bots\base\login_page.py                                             94     73    22%   44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             60     10    83%   64, 78, 82, 112, 118-119, 124-125, 136-137
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          98     24    76%   50, 69, 72, 85, 110-113, 141-159, 169
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205     81    60%   43-45, 86-88, 101-103, 113-115, 127, 169, 186-211, 223-226, 236-265, 274-275, 277-278, 284-289, 294-303
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            98     80    18%   29, 36, 40, 52-61, 66-73, 77-110, 114-120, 124-155
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           249    169    32%   56, 60, 79-81, 85-100, 104-144, 149-169, 173-194, 198-229, 233-242, 246-271, 276, 305-307, 313-344, 348-359, 377, 384-404, 413-414
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     87    20%   28-31, 35, 39-45, 49-66, 70-92, 96-125, 129-154, 158-163, 167-176
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   47-55, 74-76, 80-139, 162-163, 174-177, 180, 196-197, 201-202, 207-233, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       186    142    24%   99-100, 121-148, 154-183, 202-213, 223-230, 233-261, 268-304, 314-329, 334-374, 377-414, 418-433, 440-441
src\bots\safework\base.py                                               80     49    39%   39-42, 48-63, 67-102, 106-122, 126, 130
src\bots\safework\common\locators.py                                    30      0   100%
src\bots\safework\pages\login_page.py                                   71     55    23%   30-43, 47-79, 88-107, 115-116, 120-127
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     42    33%   30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           330    189    43%   50, 55, 67, 71, 80, 86, 106, 132-137, 145-149, 165, 170, 179-181, 188-209, 213-258, 262-302, 306-342, 347, 360-362, 379-382, 388, 398-406, 410-423, 427-432, 436-447, 452-463, 469-479, 483-485
src\bots\safework\pdl\search_bot.py                                    107     82    23%   47-48, 53, 58, 63, 75-115, 119-133, 145-159, 163-167, 176-219
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     69    38%   52, 57, 62, 74-136, 140-147, 170, 176, 181-197, 201-202, 206-208
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   40-41, 46, 51, 56, 68-132
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   53-54, 61-63, 69-71, 99-101
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             100     24    76%   61-63, 80-81, 144-147, 149-151, 153-157, 170-171, 180-181, 197-199
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   25-44
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config_manager.py                                             293     89    70%   76-85, 97-165, 182, 219, 240, 263, 326, 383, 400-401, 430-457, 494, 503-521, 533, 541, 569-570
src\core\constants.py                                                  101      0   100%
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                          159      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           121      7    94%   177, 182, 196-197, 225-227
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     34      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\database\pdl_queries.py                                       105     88    16%   23-37, 47-77, 83-137, 142-178, 186-251
src\core\employees.py                                                   98     13    87%   61-63, 118-120, 129-130, 174-175, 190-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44      0   100%
src\core\importers\attivita.py                                          67      5    93%   58-59, 77, 92-93
src\core\importers\base.py                                              59      7    88%   15-16, 24-26, 56-57
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     11    92%   42, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     37    80%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 223-226, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      187     34    82%   14-15, 22-24, 63, 79-80, 86-99, 120, 123, 135-136, 148, 196, 224, 228, 237, 241, 254, 270, 279, 312
src\core\importers\storico_oda.py                                       81     16    80%   60, 66, 71, 84-85, 95-96, 176-185
src\core\license_updater.py                                            141     72    49%   72-74, 88-113, 124-156, 161-162, 167-172, 188, 194-195, 198, 208-210, 228-230, 243-245
src\core\license_validator.py                                          168    122    27%   42-46, 59-64, 79-100, 105-114, 119-123, 132-168, 178-196, 201-202, 212-227, 232-241, 246-271, 276-277, 282-283
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              36      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   63, 65, 86-87, 120, 166-199
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 60-68, 80-86, 90, 94, 107-119, 123-124, 128-129, 133-134, 143-157, 166-174, 197-203, 207-211, 215-228, 232-244, 248-250, 254-284, 288-304, 319, 324, 329
src\core\lyra_client.py                                                162    143    12%   27-40, 58-60, 64-77, 81-89, 93-94, 98-126, 130-161, 170-172, 181-214, 223-278, 287-316
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                       115     56    51%   62, 69-75, 79-84, 91-92, 135-140, 152-154, 167-174, 178-186, 190-198, 202, 206-209, 213-216
src\core\oda_manager.py                                                 34     19    44%   29, 43-75, 93-106
src\core\report_history.py                                              67     44    34%   26-28, 36-42, 47-51, 62-86, 96, 114-134, 147-157
src\core\schemas.py                                                     77     23    70%   68-73, 78-89, 94-96, 102, 109
src\core\secrets_manager.py                                             94     48    49%   31-49, 53-57, 61-71, 75-77, 81-85, 90, 105, 112-115, 122-124, 131-132, 137-143
src\core\stats_manager.py                                               48     10    79%   48-52, 54-55, 72, 74, 90
src\core\sync_tracker.py                                                58     33    43%   39-50, 55-59, 72-81, 94-96, 110-122
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           207    167    19%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-143, 146-163, 167-178, 186-199, 210-218, 222-233, 237-249, 253-265, 268-282, 287-302, 307-323
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            344    290    16%   29-31, 35-44, 48-66, 70-73, 77-81, 85-89, 92-112, 115-134, 137-142, 146-160, 163-173, 176-179, 182-183, 186-192, 195-201, 204-225, 229-252, 255-259, 262-267, 271-286, 289-295, 298-311, 314-327, 331-336, 340-346, 350-356, 360-387, 391-404, 408-415, 418-424, 427-450, 453-465, 468-485
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\activity_timeline.py                                158     99    37%   119-120, 145-165, 169-214, 218-226, 231-242, 246-293, 297-298
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 212-217, 221-226, 230-231, 240-265, 268-273
src\gui\components\scarico_ore\filters\popup_list.py                    98     84    14%   24-76, 79-86, 90-97, 101-108, 115-116, 125-138, 141-146
src\gui\components\scarico_ore\model.py                                168    111    34%   87-93, 96, 105-118, 129-150, 154, 163-165, 175-189, 193-196, 200-207, 211-214, 219, 225, 230-256, 266-274, 289-314
src\gui\controllers\bot_controller.py                                   44     17    61%   45-50, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           156    118    24%   45-66, 70-86, 90-99, 103-107, 111-115, 119-123, 127-131, 135-139, 143-147, 151-155, 159-163, 167-171, 175-179, 183-189, 193-197, 201-205, 210-225, 236-237, 255-257, 261-262, 266-267, 271-289, 293-294
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              168    142    15%   47-54, 58-67, 74-111, 115-131, 135-232, 236-238, 242-246, 250-266, 270-279, 283, 287-292
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       66     57    14%   29-112, 115-122, 126
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-112, 115-120
src\gui\dialogs\bug_report_dialog.py                                   222    199    10%   61-65, 69-78, 95-100, 104-240, 244-252, 256-283, 290-311, 315-321, 335-417, 426-438
src\gui\dialogs\command_palette.py                                     296    265    10%   57-86, 90-146, 150-177, 181-189, 193-197, 201-207, 211-218, 222-250, 254-263, 267-273, 277-282, 286-289, 293-297, 301-309, 313-322, 326-333, 337-341, 345-382, 386-400, 404-410, 414-426
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   50-97, 101-109, 113-121, 136-137, 142-143, 148-149, 154-155
src\gui\dialogs\quick_actions_config.py                                 86      1    99%   155
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   23-69, 73, 78-80
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-377
src\gui\formatters.py                                                  131     52    60%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240
src\gui\layouts\responsive.py                                           72     57    21%   17-21, 25-26, 30-31, 35-42, 46-50, 54-55, 59-74, 79-87, 91-93, 97-109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              70     52    26%   35-40, 44-50, 54-64, 68-79, 83-88, 98-185
src\gui\main_window\components\status_bar.py                           130    113    13%   39-43, 47-85, 89-92, 96-108, 112-124, 131-173, 180-215
src\gui\main_window\components\tool_bar.py                              26     17    35%   29-33, 45-47, 59-73
src\gui\main_window\components\tray_icon.py                             17     11    35%   25-28, 37, 52-61
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   26-28, 32-33, 44-59, 63, 67-73
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   26-27, 36-46, 53-64
src\gui\main_window\main.py                                            286    208    27%   59-109, 113-147, 160-163, 167-191, 195-202, 207, 211, 215, 219, 223, 227, 231, 235, 239-278, 282, 286-305, 309-313, 322-326, 335-339, 346-350, 357-359, 363-365, 369-371, 375-377, 381-383, 387-391, 395-406, 410-412, 416-436, 440-444, 451-454, 458-462, 466-468, 472-475, 482, 486-487, 493, 498, 503, 508, 513, 518
src\gui\main_window\page_index.py                                       26      0   100%
src\gui\models\audit_model.py                                          130     23    82%   79, 124, 137-138, 148, 154, 156, 166-168, 190-191, 197-200, 208, 212, 214-215, 227-229
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 238     38    84%   95-99, 159, 165-166, 170-171, 269, 277, 299-302, 307-308, 337-338, 349, 358, 366, 369, 389, 404, 408-410, 418-419, 429, 434, 438, 442-443, 448-451, 458
src\gui\panels\carico_ts.py                                             95     22    77%   54-56, 114, 118, 120, 129, 133, 135-137, 142, 156-164, 180-181, 188, 198-199
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               200     43    78%   96-97, 102-104, 129-137, 140-153, 165-166, 187, 220-221, 228-230, 287-288, 310-312, 327-328
src\gui\panels\contabilita_kpi\kpi_panel.py                            159      4    97%   207, 232, 301-302
src\gui\panels\contabilita_panel.py                                    228     69    70%   66-70, 168-172, 197, 207-210, 229-230, 233-236, 240-242, 248-250, 257, 266-270, 272-275, 286, 290, 294-296, 318, 329, 333-350, 354-370
src\gui\panels\dashboard_panel.py                                      166     71    57%   100, 145-147, 154, 156, 159-161, 166-167, 169-178, 194-197, 204-206, 209, 216-219, 223-233, 237-242, 246-261, 265-287, 291-296
src\gui\panels\dettagli_oda.py                                         126     64    49%   50-51, 55-59, 66, 71, 85, 94, 101-102, 111-119, 130, 135-136, 148, 150, 155-211, 216-219
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 27     16    41%   34-35, 39-65, 74-76
src\gui\panels\dipendenti\pages\anagrafica_page.py                     398    360    10%   55-99, 102-240, 244-284, 288-301, 304-333, 336-378, 382-390, 394-408, 411-420, 424-455, 459-494, 503-543, 546-586, 589, 593-676, 679-684, 690-719
src\gui\panels\dipendenti\shared.py                                    151    134    11%   41-88, 119-198, 202-204, 208-210, 214-216, 225, 238-279, 292-327
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    153    127    17%   25-51, 56-99, 108-194, 199-210, 215-237, 242-299
src\gui\panels\dipendenti\widgets\employee_detail_view.py              104     91    12%   24-29, 32-135, 138-142, 150-162, 168-171
src\gui\panels\dipendenti_manager_panel.py                             185    101    45%   28-71, 75, 184, 188, 202-231, 235-252, 256-275, 278-293, 300-335
src\gui\panels\health_panel.py                                         233     42    82%   80-97, 297-298, 303-304, 314-315, 319-334, 338-341, 345-347
src\gui\panels\help_panel.py                                           122     19    84%   137-146, 154-156, 158, 167-171
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        42      7    83%   48, 62-67
src\gui\panels\lyra\header.py                                           38      0   100%
src\gui\panels\lyra\input_bar.py                                        41      4    90%   80-83
src\gui\panels\lyra\lyra_panel.py                                      163     48    71%   128, 136, 146-150, 153-154, 157-158, 161-163, 166-171, 174-176, 181, 190, 200-204, 225-228, 232-234, 238, 241-253
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     56    77%   147-151, 155-157, 161-163, 167-169, 173-174, 178-179, 183, 187-188, 218, 223, 225, 227, 230, 268-269, 275-283, 298-299, 304, 306, 308, 311-312, 317-318, 325-329, 341-346
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   78     66    15%   40-43, 47-86, 96-130, 134-136
src\gui\panels\pdl\pdl_filter_widget.py                                 66     51    23%   27-30, 33-107, 116
src\gui\panels\pdl\pdl_panel.py                                        373    336    10%   57-104, 108-174, 178-230, 234-247, 251-280, 284-296, 300-332, 336-374, 378-380, 384-385, 389-411, 415-421, 428-447, 451-506, 510-514, 518-532, 536-560, 564-596
src\gui\panels\pdl\programmazione_tab.py                               596    551     8%   54-63, 67-75, 79-91, 94-172, 179-187, 191-207, 210-371, 375-385, 389-390, 394-449, 452-456, 460, 464-465, 469-492, 496-544, 549-572, 576-577, 580-582, 586-589, 593-652, 655-709, 712-731, 736-873, 877-919, 922-1028
src\gui\panels\prenota_bp.py                                           110     85    23%   24-32, 35-36, 39-42, 47-81, 87-88, 92-99, 103-108, 112-113, 118-191
src\gui\panels\ricerca_pdl.py                                          109     85    22%   40, 47, 52, 57-81, 83-93, 95-108, 110-132, 136-139, 143-144, 148-153, 164-202, 207-213, 217-219
src\gui\panels\scarico_ore_panel.py                                    231    143    38%   56-58, 62-83, 87-89, 170-174, 178-190, 194, 198-201, 205-218, 222-225, 229-241, 247-262, 266-267, 271-275, 279-283, 287-288, 292-296, 300-311, 315-327, 331-334, 338-346
src\gui\panels\scarico_pdl.py                                          338    171    49%   42, 58, 69, 74, 77, 84, 89, 100-133, 155-157, 161, 166-170, 194-203, 207-212, 216, 219-220, 240-252, 254-261, 269, 273, 278, 289, 294, 303-313, 315-320, 323-333, 337, 339, 349-350, 352, 356, 358-369, 373, 375-378, 382, 387-388, 398, 401-405, 412, 421, 427, 432-436, 439-440, 443, 445, 453, 466-467, 471, 473, 489, 505, 517, 523-524, 528, 539, 541-548, 563, 569-571, 575, 579-593, 597-599
src\gui\panels\scarico_ts.py                                           127     38    70%   56-58, 102-104, 123, 130, 141-143, 149, 153-156, 179, 190, 194-210, 213-222, 233, 237, 244
src\gui\panels\settings\main_panel.py                                  108     23    79%   128-129, 140, 144-146, 150-157, 161-171
src\gui\panels\settings\pages\diag_page.py                              31      2    94%   42-43
src\gui\panels\settings\pages\general_page.py                          117      9    92%   134, 148-156
src\gui\panels\settings\pages\lists_page.py                            340    127    63%   225, 235, 253-264, 274-284, 291-295, 303, 324-340, 343-350, 353-359, 364-373, 376-397, 400-407, 410-416, 427-429, 433-436, 439-444, 447-450, 454, 457, 460, 463, 466, 469, 472, 475, 478, 481, 484, 487
src\gui\panels\settings\pages\paths_page.py                            128     28    78%   115-131, 148-149, 152, 155-157, 160-162, 165-167, 170-172, 175-177, 180-182, 185-187
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             127     27    79%   148-150, 157-159, 167-172, 176-177, 185-187, 195-196, 202-212
src\gui\panels\settings\tabs\config_tab.py                              55      0   100%
src\gui\panels\settings\tabs\telegram_tab.py                           139     30    78%   146-151, 155-161, 165-176, 180-184, 215-216
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              42     36    14%   11-12, 15-74
src\gui\panels\storico_oda\oda_detail_view.py                           48     37    23%   21-24, 27-49, 53-67, 71-72
src\gui\panels\storico_oda\oda_filter_widget.py                         40     27    32%   24-27, 30-74, 78
src\gui\panels\storico_oda\oda_panel.py                                253    222    12%   43-106, 109-169, 173-181, 185-284, 287-302, 305, 308, 311-315, 318-324, 328-346, 350-408, 411-416, 419-439, 443-463
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     62     25    60%   72-112, 116-131
src\gui\panels\timbrature\components\settings_tab.py                    99      4    96%   147, 159-161
src\gui\panels\timbrature\panel.py                                     173     27    84%   148, 157, 237-255, 258-265, 280, 295-296, 300
src\gui\panels\timbrature_bot.py                                       110     34    69%   63-65, 71, 76, 83, 89, 99, 101, 103, 110, 112, 114-115, 124, 126, 129, 133, 135-137, 140-144, 147, 149, 175, 182, 184, 186-187, 191-193
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         67     50    25%   26-29, 34, 41-51, 55-92, 97-118, 123
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-91
src\gui\widgets\__init__.py                                             13      0   100%
src\gui\widgets\activity_feed.py                                       136     22    84%   39-40, 88-90, 146-147, 167-177, 184, 188-190, 263, 269, 280, 282
src\gui\widgets\animated_progress_bar.py                                74     63    15%   38-50, 54-55, 59, 63-64, 68-69, 74-88, 92-150
src\gui\widgets\audit\audit_filter_bar.py                               79     14    82%   115-124, 141-142, 158, 160, 162
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   46, 60-61
src\gui\widgets\audit_log_widget.py                                    104     18    83%   92, 94, 123-133, 136, 139-140, 150, 178-180
src\gui\widgets\automazioni_widget.py                                   79     79     0%   1-142
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                 67     11    84%   132-147, 163
src\gui\widgets\autopilot\main_widget.py                               204     27    87%   69, 73, 167, 194-195, 197-198, 240-247, 251-254, 264, 280, 298, 323-329
src\gui\widgets\bot_parameters.py                                      147     11    93%   155-156, 158-159, 161, 194, 198, 261, 282, 307-308
src\gui\widgets\calendar_date_edit.py                                   17      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            221     61    72%   116, 138, 144, 168, 200, 210-213, 234, 239-242, 246-252, 256-259, 263-266, 270-273, 277-280, 284-288, 297-308, 312-321
src\gui\widgets\contabilita\certificati_tab.py                         571    142    75%   159, 167, 172-175, 320, 338, 443-446, 462-463, 559, 715-716, 723, 738, 746, 750, 775-776, 937-939, 942-944, 990, 995-998, 1002-1005, 1009-1023, 1026-1096, 1112-1148, 1155-1160, 1165-1207
src\gui\widgets\contabilita\giornaliere_tab.py                         189     60    68%   94, 99, 133, 150, 177, 193-212, 215-240, 243-259
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                100     31    69%   30-31, 38-52, 111, 116, 142, 166-167, 171-202, 206, 210
src\gui\widgets\data_table.py                                          120      0   100%
src\gui\widgets\excel_table.py                                         358     98    73%   75-82, 97, 108, 112, 119, 155-175, 177, 181-202, 204, 210, 237, 242, 259-260, 268-271, 273, 287, 379-392, 395, 405-406, 423-424, 432, 436, 449, 482-484, 497, 499, 504, 526, 529, 548, 554, 564-565, 573, 575-581, 600, 604-617
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   40-94, 98-105, 117-122, 126-130, 134-137, 146-152
src\gui\widgets\footer\components.py                                    55     36    35%   36-47, 56, 72-78, 88-95, 113-115, 124-125, 129-132, 136-137, 141-143, 161-162
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    35     27    23%   29-49, 58-60, 64-67, 71-74
src\gui\widgets\footer\telemetry.py                                     55     40    27%   33-64, 68-71, 75-77, 81-85
src\gui\widgets\info_widgets.py                                         90     38    58%   29-60, 64, 86-110
src\gui\widgets\message_bubble.py                                       53      0   100%
src\gui\widgets\modern_button.py                                        62     10    84%   69-70, 76-79, 83-86
src\gui\widgets\multi_select_filter.py                                  97     80    18%   26-78, 81-85, 88-91, 100-105, 114-129, 138-141, 150-151, 154-157, 160-164
src\gui\widgets\notification_card.py                                   240    105    56%   227-229, 279-285, 313-327, 332-333, 340-350, 354, 372, 376-378, 392-423, 432-438, 440, 442, 447-452, 456-458, 462-463, 467-472, 476-480, 484-521, 525-531, 535-542
src\gui\widgets\notification_group_header.py                            47      9    81%   128-131, 135-136, 140, 144-145
src\gui\widgets\notification_item.py                                    72     13    82%   37-38, 40-41, 43-44, 60, 91-92, 129-131, 134
src\gui\widgets\notification_toolbar.py                                104     15    86%   233-234, 238-239, 244-251, 255-256, 271, 275, 279
src\gui\widgets\pdl_timeline.py                                        127    127     0%   1-211
src\gui\widgets\priority_badge.py                                       47     35    26%   30-37, 41-78, 82-90, 94-98, 102, 106-108
src\gui\widgets\quick_actions.py                                        77     13    83%   267-308, 324, 352-353
src\gui\widgets\security_dashboard.py                                  154    154     0%   1-252
src\gui\widgets\sidebar_button.py                                       41      7    83%   28-30, 35-37, 76
src\gui\widgets\sidebar_widget.py                                      237    205    14%   24-30, 48-81, 85-89, 93, 97-98, 102-105, 109-119, 123-131, 144-166, 170-172, 176-178, 182-185, 189-209, 213-231, 235-368, 372-373, 377-378, 382-412
src\gui\widgets\simple_chart.py                                         66     66     0%   1-113
src\gui\widgets\sortable_table_item.py                                  47     32    32%   30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   106      9    92%   135-139, 176-177, 190-191
src\gui\widgets\status_card.py                                          60      8    87%   101-117, 121, 125-126
src\gui\widgets\status_indicator.py                                     43      7    84%   63-69
src\gui\widgets\timeline_widget.py                                     165     28    83%   117-142, 192-194, 198-202, 291-292
src\gui\widgets\toast.py                                               131     34    74%   152-159, 163-168, 172-174, 178-179, 185-186, 192, 235-242, 250, 264, 269, 274, 279
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-37, 41-44, 47-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70      1    99%   55
src\utils\document_generator.py                                         17      2    88%   38-39
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   111     33    70%   31-35, 68-69, 124, 137-152, 223, 242-255, 274
src\utils\log_humanizer.py                                              42     10    76%   19-26, 110, 118
src\utils\parsing.py                                                    51      6    88%   15, 18, 46-47, 84, 91
src\utils\printing.py                                                   90     70    22%   14-15, 27-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           59     19    68%   20-31, 61, 71, 112-118, 131-132, 145-146
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79     17    78%   43-44, 80-82, 102, 104, 109-111, 116, 122-124, 132-134
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   56-74, 87-98, 111-126, 139-160, 173-189, 202-205
--------------------------------------------------------------------------------------------------
TOTAL                                                                26412  12845    51%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_horizontal_timeline.py::test_horizontal_timeline_functionality
============================= 1 failed in 10.80s ==============================

```
</details>

---
