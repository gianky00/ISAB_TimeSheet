# 📊 Test Execution Report

**Date:** 2026-02-09 18:54:36
**Duration:** 28.47s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1496 |
| ✅ Passed | 186 |
| ❌ Failed | 3 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_backup_manager.py::TestBackupManager::test_restore_backup_non_existent`
**Error:** `FAILED tests/unit/test_backup_manager.py::TestBackupManager::test_restore_backup_non_existent`

**Timestamp:** `2026-02-08T21:47:01.707888`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_backup_manager.py F                                      [100%]

================================== FAILURES ===================================
_____________ TestBackupManager.test_restore_backup_non_existent ______________
C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_backup_manager.py:178: in test_restore_backup_non_existent
    assert "non trovato" in message
                            ^^^^^^^
E   NameError: name 'message' is not defined
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    22      7    68%   121, 135-140
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    203    23%   52-72, 92, 97-99, 111-115, 126-142, 146, 150, 154, 158-159, 163-164, 169-185, 189-232, 236-258, 262-264, 271-276, 280-307, 319-368, 372-404, 409-418, 422-426, 430-432, 436, 440-446, 457-469, 473-476
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    138    17%   50-55, 76-81, 100-104, 135-198, 221, 250-304, 324-325, 328-332, 345, 348-352, 374-377, 380-390, 420-436, 466-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     27    43%   52, 56, 60-72, 77-100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-91, 95-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   39-42, 46, 50-52, 65-90, 101-114, 118-147, 151-158, 182-277, 281-299, 309-335, 339-348, 352-361, 365-376
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            84     67    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-104, 108-129
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           221    181    18%   57, 61, 73-76, 80-82, 86-101, 105-122, 127-142, 146-168, 172-199, 203-212, 216-241, 245-277, 283-312, 316-325, 329-344, 348-369, 374-384
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         105     83    21%   28-31, 35, 39-45, 49-66, 70-92, 96-125, 129-146, 150-155, 159-168
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-108
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-69, 75-118, 125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-85, 89-148, 152-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       178    105    41%   91-114, 120-149, 159-170, 180-187, 190-218, 225-261, 271-286, 331, 340-342, 370-371, 375-390, 397-398
src\bots\safework\base.py                                               42     27    36%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           391    347    11%   28, 33, 38, 43, 48, 59-63, 67, 71, 75-107, 111-170, 174-178, 182-210, 214-243, 247-255, 259-293, 297-325, 329-342, 346-374, 378-413, 417-431, 435-456, 460-472, 479-517, 520-560, 564-583
src\bots\safework\pdl\search_bot.py                                    182    155    15%   19-20, 24, 28, 32, 36-94, 98-115, 119-136, 140-149, 153-163, 167-172, 176-201, 205-230, 234-304
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82      0   100%
src\core\app_updater.py                                                 48      2    96%   38, 99
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             100     35    65%   61-63, 78-79, 110-112, 114-117, 119-122, 124-126, 128-132, 145-146, 150-155, 162-164
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     18    87%   51, 63-64, 175-178, 189, 191, 200-201, 215, 231-232, 242, 280, 282-283
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               28     13    54%   23-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      0   100%
src\core\backup_manager.py                                             138     19    86%   68, 95, 115, 119, 122, 179-188, 212-223, 249-250
src\core\bug_reporter.py                                               157    126    20%   60-107, 112-143, 148-158, 163-185, 190-210, 215-238, 243-295, 300-312, 321-339
src\core\config_manager.py                                             237    114    52%   35, 87, 109-115, 136, 141-142, 156-170, 179-180, 199-200, 222, 226-229, 247, 252, 264, 279, 289-302, 307-317, 326-353, 358-362, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     51    50%   30, 35, 40, 49-61, 78-125, 134-141, 150-155, 164-171, 176, 181, 186, 191, 201, 210, 223
src\core\contabilita_queries.py                                         87     61    30%   19-30, 35-48, 53-78, 83-94, 100, 109-110, 115-126
src\core\contabilita_search.py                                          92     43    53%   26-82, 90, 110-111, 118-127, 136-137, 155-156
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          159    103    35%   22, 38-55, 60-70, 76-103, 109-147, 155-192, 200-235, 249, 265, 281, 283
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           121     40    67%   131-140, 149-179, 193-194, 224-226
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              58     36    38%   15-16, 23-25, 35-37, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                                      181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    133    13%   21-63, 68-69, 74, 79, 84-100, 105-145, 150-190, 195-197, 202-208, 213-233, 238-246, 251-269, 274-283, 287-290
src\core\license_validator.py                                          180    133    26%   37-41, 50-57, 71-75, 95-110, 116-132, 137-144, 158-181, 191-217, 228-229, 238-262, 267-284, 289-337, 342-345, 350-353
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             57     25    56%   31-32, 40-41, 45-46, 54, 81-98, 108, 118, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          66     50    24%   69-132, 139, 188-225
src\core\logging\filters.py                                             60     29    52%   116, 119, 123, 142-153, 166-172, 190-191, 200-209
src\core\logging\formatters.py                                          83     25    70%   84, 88-90, 122, 125, 130, 132, 134, 136, 164-165, 205-215, 224, 230-240
src\core\logging\logger.py                                             109     25    77%   84, 96, 123, 137-139, 147-148, 161-165, 173-174, 179-180, 199, 205, 213, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     76    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 218-220, 226-228, 234-236
src\core\logging\viewer.py                                             175    141    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    110    12%   21-37, 55-69, 73-74, 78-106, 110-141, 150-205, 214-252
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                       111     80    28%   31-37, 40-47, 51-61, 65-78, 82-86, 105-150, 154-156, 160, 164-171, 175-184, 188-197, 201, 205-208, 212-215
src\core\oda_manager.py                                                 34     20    41%   23, 31-91, 100-115
src\core\report_history.py                                              67     44    34%   26-28, 36-42, 47-51, 62-86, 96, 114-134, 147-157
src\core\schemas.py                                                     77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                                             94     56    40%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 124-126, 131-134, 139-145
src\core\stats_manager.py                                               47     33    30%   24-27, 31, 35-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                58     23    60%   32-37, 47-48, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-37, 55-80, 88-91, 99-103
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           190    152    20%   41-51, 57-74, 78-87, 91, 95-107, 110, 119-161, 164-180, 184-194, 202-210, 219-227, 231-241, 244-257, 260-273, 276-291, 294-310, 313-330
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            344    290    16%   29-31, 35-44, 48-66, 70-73, 77-84, 88-95, 98-125, 128-151, 154-159, 163-177, 180-196, 201-204, 207-208, 211-219, 222-230, 233-258, 262-287, 290-294, 297-302, 306-323, 326-334, 337-350, 353-366, 370-375, 379-385, 389-397, 401-428, 432-445, 449-456, 461-467, 470-497, 500-512, 515-532
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 25-29, 33-63
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    99     85    14%   24-76, 79-86, 89-96, 99-106, 109, 112-113, 116-129, 132-137
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 111-132, 135, 138-140, 143-157, 160-163, 166-173, 176-179, 182-184, 187-189, 192-218, 221-237, 242-244, 247-272
src\gui\controllers\bot_controller.py                                   46     35    24%   20-23, 27-35, 39-42, 49-62, 66-80
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 61-63, 66, 69-70, 73
src\gui\controllers\navigation_controller.py                           153    123    20%   40-41, 45-61, 65-82, 85-99, 102-105, 108-111, 114-117, 120-123, 126-129, 132-135, 138-141, 144-147, 150-153, 156-159, 163-169, 173-177, 181-186, 198-234, 238-257, 261-263, 267-268, 272-273, 277-310, 314-315
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              205    179    13%   33-49, 54-69, 77-130, 137-165, 169-331, 343-346, 363-371, 384-423, 436-450, 454, 458-467
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   22-93, 96-107, 110
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-112, 115-120
src\gui\dialogs\bug_report_dialog.py                                   229    207    10%   51-55, 58-67, 74-79, 82-223, 227-235, 238-268, 271-297, 301-307, 311-456, 460-477
src\gui\dialogs\command_palette.py                                     306    276    10%   45-75, 79-190, 194-221, 224-232, 235-239, 242-249, 252-259, 262-297, 301-310, 313-320, 323-329, 332-338, 342-346, 350-362, 366-377, 380-387, 390-394, 397-441, 444-480, 484-500, 503-520
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   29-78, 81-89, 92-100, 105-106, 110-111, 115-116, 120-121
src\gui\dialogs\quick_actions_config.py                                 86     86     0%   2-215
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   22-70, 74, 79-81
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  131    113    14%   14-28, 38-68, 73, 90-96, 100-103, 107, 110, 113, 116-141, 146-148, 151-154, 158-237
src\gui\layouts\responsive.py                                           72     57    21%   18-22, 26-27, 31-32, 36-43, 47-51, 55-56, 60-75, 80-88, 92-94, 98-110
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     55    25%   18-23, 27-33, 37-49, 53-64, 69-78, 82-330
src\gui\main_window\components\status_bar.py                           157    140    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-277
src\gui\main_window\components\tool_bar.py                              26     17    35%   12-16, 20-23, 27-45
src\gui\main_window\components\tray_icon.py                             17     11    35%   12-17, 20, 31-44
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            282    206    27%   51-101, 105-139, 151-154, 157-181, 184-191, 195, 198, 201, 204, 207, 210, 213, 216, 220-245, 248, 251-270, 273-277, 285-289, 297-301, 307-311, 317-319, 322-324, 327-329, 332-334, 337-339, 342-346, 349-360, 363-365, 368-384, 387-390, 393-396, 399-403, 406-408, 411-414, 417, 420, 423-424, 429, 433, 437, 441, 445, 449
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          130     24    82%   53, 98, 111-112, 122, 128, 130, 140-142, 161-162, 167-170, 178, 180, 182, 185-186, 189-191
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 197    141    28%   52-56, 60-77, 89-93, 97-99, 124-132, 136-180, 187, 191-202, 212, 220, 229, 233-238, 242-245, 249-251, 255-266, 270-273, 277-293, 297-301, 305-310, 320-322, 326-339, 343, 347-362, 369-372, 376-381, 385-388
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-105, 109-117, 121-122, 126-180
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   11-15, 18-21
src\gui\panels\contabilita_kpi\charts.py                               200    183     8%   21-61, 68-76, 79-82, 86-90, 93-157, 160-214, 217-279, 282-321, 324-370
src\gui\panels\contabilita_kpi\kpi_panel.py                            159    140    12%   35-58, 61-179, 192-196, 199-212, 215-225, 228, 231-310
src\gui\panels\contabilita_panel.py                                    249    213    14%   39-46, 50-56, 60-162, 166-173, 177, 181, 204-221, 225-246, 251-276, 280-282, 286-289, 293-315, 319-337, 340-341, 344-348, 351-366, 369-371, 374-391, 395, 398-417
src\gui\panels\dashboard_panel.py                                      166    144    13%   26-90, 94, 98-105, 109-136, 140-142, 146-156, 160-175, 180-195, 200-218, 222-233, 237-243, 247-262, 266-288, 292-298
src\gui\panels\dettagli_oda.py                                         137    112    18%   27-35, 38-42, 46-90, 93-95, 99, 102-114, 117-127, 130-132, 136-142, 145-221, 225-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     398    360    10%   55-99, 102-240, 244-284, 288-301, 304-335, 338-380, 384-392, 396-410, 413-422, 426-457, 460-495, 498-538, 541-581, 584, 588-671, 674-679, 685-714
src\gui\panels\dipendenti\shared.py                                    151    134    11%   26-73, 90-175, 178-180, 183-185, 188-190, 193, 198-239, 244-279
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   9-11, 17-44, 55-67, 71-78
src\gui\panels\dipendenti\utils\report_generator.py                    153    127    17%   25-51, 56-99, 108-194, 199-210, 215-237, 242-299
src\gui\panels\dipendenti\widgets\employee_detail_view.py              104     91    12%   24-29, 32-141, 144-148, 156-168, 174-177
src\gui\panels\dipendenti_manager_panel.py                             186    166    11%   28-71, 74, 85-105, 108-133, 136-174, 177-215, 219-251, 255-272, 276-297, 302-317, 324-361
src\gui\panels\health_panel.py                                         291    259    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-525, 529-557, 561-566, 570-573
src\gui\panels\help_panel.py                                           122     98    20%   33-36, 39-172, 176-196, 199-208, 211-219, 222-226, 229, 249, 269, 281, 295, 306, 319, 331, 342, 352, 362, 370
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        35     26    26%   21-33, 37-49, 53-58
src\gui\panels\lyra\header.py                                           38     28    26%   24-28, 31-87
src\gui\panels\lyra\input_bar.py                                        41     30    27%   21-22, 25-78, 81-84, 87-89
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-122, 125-130, 133-140, 143-144, 147-148, 151-153, 156-161, 164-166, 169-178, 181-182, 185-188, 191-193, 197, 200-212
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 45-46, 49-57
src\gui\panels\notifications_panel.py                                  254    207    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-311, 315-316, 320-338, 342-374, 378-380, 384-403, 407-446
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 16-28
src\gui\panels\pdl\pdl_detail_view.py                                   47     36    23%   20-23, 26-48, 52-65, 69-70
src\gui\panels\pdl\pdl_filter_widget.py                                 66     51    23%   28-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        353    317    10%   44-108, 111-160, 164-218, 221-234, 238-267, 271-283, 287-319, 323-361, 365-367, 371-372, 376-387, 391-397, 401-420, 424-496, 500-504, 508-522, 526-550, 554-595
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-183
src\gui\panels\ricerca_pdl.py                                           86     70    19%   31-38, 41-70, 73-78, 81-84, 89-94, 104-146, 151-157, 160-162
src\gui\panels\scarico_ore_panel.py                                    338    298    12%   45-47, 52-86, 90-92, 103-127, 131-254, 258-273, 277-309, 313-315, 319-327, 331-355, 359-361, 365-383, 394-421, 425-429, 433-435, 440-449, 453-464, 468-469, 473-481, 485-499, 503-524, 528-531, 535-562
src\gui\panels\scarico_pdl.py                                          301    260    14%   42-59, 63-84, 88-121, 131-139, 142-146, 150-275, 278-286, 289-292, 295-308, 311-316, 320, 323-325, 329-337, 342-348, 352-353, 356-390, 394-406, 410-432, 436-450, 454-461, 465-497, 501-503, 507, 511-525, 529-531
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-79, 83-85, 89, 93-106, 110-118, 122-124, 128-133, 147-149, 155-211
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              33     21    36%   15-16, 19-40, 44-45, 48, 51
src\gui\panels\settings\pages\general_page.py                           44     34    23%   22-23, 26-66, 70-71, 75-78
src\gui\panels\settings\pages\lists_page.py                            336    281    16%   35-36, 39-65, 70-87, 90-113, 116-135, 138-157, 160-179, 182-201, 206-212, 215-216, 225, 235, 253-264, 267-277, 282-289, 292-299, 302-310, 313-329, 332-341, 344-350, 355-364, 367-381, 384-393, 396-402, 407-408, 411-416, 419-422, 425-432, 435-440, 444, 447, 450, 453, 456, 459, 462, 465, 468, 471, 474, 477, 482-489, 494-509
src\gui\panels\settings\pages\paths_page.py                            119     95    20%   29-30, 33-89, 92-114, 118-139, 156-157, 160, 163-167, 170-172, 175-177, 180-184, 187-189, 192-194, 199-219, 222-240
src\gui\panels\settings\shared.py                                       16      9    44%   8-26, 31, 58, 79, 101-103
src\gui\panels\settings\tabs\backup_tab.py                             134    115    14%   32-33, 36-146, 149-156, 159-161, 164, 167-172, 175-176, 179-198, 201-225
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           140    120    14%   30-31, 34-141, 144-151, 156-169, 174-190, 196-200, 208-218, 222-235
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              42     36    14%   11-12, 15-77
src\gui\panels\storico_oda\oda_detail_view.py                           48     37    23%   21-24, 27-53, 57-71, 75-76
src\gui\panels\storico_oda\oda_filter_widget.py                         40     27    32%   25-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                253    222    12%   43-106, 109-169, 173-181, 185-284, 287-302, 305, 308, 311-315, 318-324, 328-346, 350-408, 411-416, 419-439, 443-463
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     62     50    19%   16-39, 42-64, 72-112, 116-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    99     85    14%   28-33, 36-80, 84-105, 109-138, 141-148, 151-152, 157-159
src\gui\panels\timbrature\panel.py                                     173    149    14%   38-62, 65-97, 100-131, 134-178, 182-198, 202-237, 241-259, 262-269, 273, 276-299, 303
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         67     50    25%   26-29, 34, 41-51, 55-92, 97-118, 123
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   17-62, 66-84, 88-92
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       136    118    13%   29-180, 184, 188-190, 199-207, 210-258, 263, 268-314
src\gui\widgets\animated_progress_bar.py                                74     63    15%   39-51, 55-56, 60, 64-65, 69-70, 75-89, 93-151
src\gui\widgets\audit\audit_filter_bar.py                               78     14    82%   98-107, 118-119, 131, 133, 135
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   39, 47-48
src\gui\widgets\audit_log_widget.py                                    104     18    83%   96, 98, 127-137, 140, 143-144, 148, 180-182
src\gui\widgets\automazioni_widget.py                                   55     55     0%   1-134
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     10    93%   181, 185-197, 392, 396-408
src\gui\widgets\autopilot\event_card.py                                 67     11    84%   132-147, 163
src\gui\widgets\autopilot\main_widget.py                               204     27    87%   58, 61, 155, 181-182, 184-185, 224-231, 234-237, 246, 262, 280, 306-312
src\gui\widgets\bot_parameters.py                                      108     85    21%   39-43, 46-108, 118-125, 129, 148-150, 154-162, 167, 171-173, 177-179, 189-194, 198, 202-203
src\gui\widgets\calendar_date_edit.py                                   17      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            221    188    15%   53-63, 67-142, 145, 148-163, 167-183, 186-197, 200-206, 209-214, 217-235, 238-241, 245-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-296, 299-308
src\gui\widgets\contabilita\certificati_tab.py                         577    525     9%   43-52, 55-244, 248-274, 278-348, 352-465, 510-522, 526-530, 534-538, 546-713, 717-718, 722-733, 738-742, 746-750, 754, 758-893, 902-924, 930-967, 972-983, 987-995, 999-1002, 1006-1009, 1013-1027, 1030-1100, 1104-1106, 1110-1112, 1116-1152, 1159-1164, 1169-1212
src\gui\widgets\contabilita\giornaliere_tab.py                         189    158    16%   47-50, 54-95, 99, 102-129, 132-139, 143, 146-166, 169-189, 193-212, 215-240, 243-259
src\gui\widgets\contabilita\helpers.py                                  36     29    19%   11-35, 38-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                100     81    19%   25-26, 30-31, 34-51, 73-93, 96-137, 141, 145-166, 170-201, 205, 209
src\gui\widgets\data_table.py                                          108     84    22%   48-52, 55-126, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 214
src\gui\widgets\excel_table.py                                         335    295    12%   33-38, 49-61, 65-72, 76-93, 97-117, 120-121, 124-125, 129-140, 144-166, 170-193, 197-216, 220-240, 244-253, 256-261, 264-268, 271-275, 284-286, 289-311, 314-371, 374-377, 380-386, 389-421, 424-427, 430-432, 435, 439-456, 465-475, 479-519, 524-549
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   26-80, 83-90, 93-98, 101-105, 108-111, 115-121
src\gui\widgets\footer\components.py                                    55     36    35%   19-32, 35, 42-48, 51-58, 67-69, 72-73, 76-80, 83-84, 87-89, 96-97
src\gui\widgets\footer\manager.py                                       20     12    40%   19-23, 28-32, 35-36
src\gui\widgets\footer\status_bar.py                                    35     27    23%   12-32, 35-37, 40-43, 46-49
src\gui\widgets\footer\telemetry.py                                     55     40    27%   19-51, 54-57, 60-62, 65-69
src\gui\widgets\info_widgets.py                                         90     74    18%   29-62, 65, 72-80, 85-113, 127-170, 173, 176
src\gui\widgets\message_bubble.py                                       53     46    13%   39-41, 44-128
src\gui\widgets\modern_button.py                                        62     35    44%   43-55, 59-61, 65, 69-70, 76-79, 83-86, 90-91, 101-106, 110-149
src\gui\widgets\notification_card.py                                   240    209    13%   86-102, 106-354, 358-368, 372, 376-378, 392-423, 427-443, 447-452, 456-458, 462-463, 467-472, 476-480, 484-521, 525-531, 535-542
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    72     59    18%   22-25, 28-131, 135-137, 140
src\gui\widgets\notification_toolbar.py                                104     78    25%   36-48, 52-64, 68-70, 74-78, 82-101, 133-139, 143-228, 233-234, 238-239, 244-251, 255-256, 265-267, 271, 275, 279
src\gui\widgets\priority_badge.py                                       47     35    26%   30-37, 41-78, 82-90, 94-98, 102, 106-108
src\gui\widgets\quick_actions.py                                        77     61    21%   24-32, 236-237, 240-263, 267-308, 313-353, 358
src\gui\widgets\security_dashboard.py                                  154    154     0%   1-259
src\gui\widgets\sidebar_button.py                                       41     32    22%   12-25, 29-31, 35-42, 47-52, 56-90
src\gui\widgets\sidebar_widget.py                                      245    209    15%   17-22, 29-63, 67-71, 75, 78-79, 82-86, 89-101, 105-113, 125-150, 154-156, 160-162, 166-169, 173-196, 200-218, 221-371, 375, 379, 383, 387-388, 392-393, 399-435
src\gui\widgets\simple_chart.py                                         66     66     0%   2-106
src\gui\widgets\sortable_table_item.py                                  51     41    20%   21-26, 30-62, 67-80, 84-97
src\gui\widgets\statistics_widget.py                                   107     91    15%   27-28, 31-118, 121-159, 163-165, 169-184, 192-236
src\gui\widgets\status_card.py                                          60     47    22%   21-92, 96-99, 108-124, 128, 132-133
src\gui\widgets\status_indicator.py                                     43     36    16%   19-33, 43-60, 64-70
src\gui\widgets\timeline_widget.py                                     203    168    17%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 165-170, 173-186, 191-198, 204-214, 217-231, 234-240, 243-248, 259-275, 278, 281, 286-310
src\gui\widgets\toast.py                                               131     99    24%   59-80, 84-123, 127-149, 152-157, 161-163, 167-168, 171-183, 194-196, 206-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-297
src\utils\date_utils.py                                                 70     57    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-144, 157-164, 178-181, 194, 208, 222-228
src\utils\document_generator.py                                         17     14    18%   11-43
src\utils\document_processor.py                                         60     22    63%   14-15, 24-32, 38, 50-51, 59, 63-64, 71-72, 81-83
src\utils\helpers.py                                                    91     54    41%   30-34, 48-70, 83-85, 90, 117-118, 123, 136-151, 165-167, 182-188, 203, 222, 233, 239-242
src\utils\log_humanizer.py                                              42     30    29%   13-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    54     46    15%   14-34, 40-52, 57-67, 72-80, 85-98, 103-120
src\utils\printing.py                                                   86     70    19%   19-24, 29-40, 48-54, 65-144
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                24569  18213    26%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_backup_manager.py::TestBackupManager::test_restore_backup_non_existent
============================== 1 failed in 7.11s ==============================

```
</details>

---
### `tests/unit/test_base_bot.py::TestBaseBot::test_init_sets_credentials`
**Error:** `Unknown Error`

**Timestamp:** `2026-02-09T18:52:55.900698`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_base_bot.py E                                            [100%]

=================================== ERRORS ====================================
__________ ERROR at setup of TestBaseBot.test_init_sets_credentials ___________
tests\unit\test_base_bot.py:28: in mock_bot
    return TestBot("user", "pass", headless=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: Can't instantiate abstract class TestBot without an implementation for abstract method 'get_columns'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    22      7    68%   121, 135-141
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    203    23%   52-72, 92, 97-99, 111-115, 126-142, 146, 150, 154, 158-159, 163-164, 169-185, 189-232, 236-258, 262-264, 271-276, 280-307, 319-368, 372-404, 409-418, 422-426, 430-432, 436, 440-446, 457-469, 473-476
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    138    17%   50-55, 76-81, 100-104, 135-198, 221, 250-304, 324-325, 328-332, 345, 348-352, 374-377, 380-390, 420-436, 466-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     27    43%   52, 56, 60-72, 77-100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-91, 95-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   39-42, 46, 50-52, 65-90, 101-114, 118-147, 151-158, 182-277, 281-299, 309-335, 339-348, 352-361, 365-376
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            84     67    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-104, 108-129
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           221    181    18%   57, 61, 73-76, 80-82, 86-101, 105-122, 127-142, 146-168, 172-199, 203-212, 216-241, 245-277, 283-312, 316-325, 329-344, 348-369, 374-384
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         105     83    21%   28-31, 35, 39-45, 49-66, 70-92, 96-125, 129-146, 150-155, 159-168
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-108
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-69, 75-118, 125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-85, 89-148, 152-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       178    107    40%   91-109, 118, 124-141, 163-173, 184-188, 191, 194-222, 229-260, 275-287, 289-290, 302-303, 308, 319, 321-322, 335, 340-342, 345, 348, 353, 371-372, 374-375, 379-392, 401-402
src\bots\safework\base.py                                               42     27    36%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           391    335    14%   28, 33, 38, 43, 48, 59-63, 67, 71, 75-107, 111-170, 174-178, 182-210, 216-244, 249-256, 261-293, 299-326, 331-343, 348-375, 380-414, 419-431, 437-457, 462-473, 481-517, 522-560, 566-585
src\bots\safework\pdl\search_bot.py                                    182    155    15%   19-20, 24, 28, 32, 36-94, 98-115, 119-136, 140-149, 153-163, 167-172, 176-201, 205-230, 234-304
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82      0   100%
src\core\app_updater.py                                                 48     11    77%   38, 49-50, 54, 57, 73, 82, 92-97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             100     35    65%   61-63, 78-79, 110-112, 114-117, 119-122, 124-126, 128-132, 145-146, 150-155, 162-164
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     18    87%   51, 63-64, 175-178, 189, 191, 200-201, 215, 231-232, 242, 280, 282-283
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               28     13    54%   23-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157    126    20%   60-107, 112-143, 148-158, 163-185, 190-210, 215-238, 243-295, 300-312, 321-339
src\core\config_manager.py                                             237    114    52%   35, 87, 109-115, 136, 141-142, 156-170, 179-180, 199-200, 222, 226-229, 247, 252, 264, 279, 289-302, 307-317, 326-353, 358-362, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     53    48%   30, 35, 40, 49-61, 78-125, 134-141, 150-155, 164-171, 176, 181, 186, 191, 201, 210, 222-225
src\core\contabilita_queries.py                                         87     61    30%   19-30, 35-48, 53-78, 83-94, 100, 109-110, 115-126
src\core\contabilita_search.py                                          92     53    42%   26-82, 90, 110-111, 118-127, 136-138, 150, 155-157, 160, 165-166, 179, 182-185
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         102     87    15%   23-28, 32-63, 67-127, 132-154, 160-171, 178-211, 213-216
src\core\data_synchronizer.py                                          159    112    30%   22, 38-55, 60-70, 76-103, 109-147, 157-192, 202-235, 269, 272, 277-278, 283, 285, 287-295, 312-313, 322-325
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           121     41    66%   131-140, 149-179, 193-194, 212, 215, 222, 224
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     11    35%   6-21, 27-28, 33, 36-39
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      7    36%   6-49, 56-57
src\core\database\migrations\timbrature.py                              27     20    26%   6-25, 30-32, 37, 40-47, 52-54, 67-69
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              58     36    38%   15-16, 23-25, 35-37, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                                      181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    133    13%   21-63, 68-69, 74, 79, 84-100, 105-145, 150-190, 195-197, 202-208, 213-233, 238-246, 251-269, 274-283, 287-290
src\core\license_validator.py                                          180    133    26%   37-41, 50-57, 71-75, 95-110, 116-132, 137-144, 158-181, 191-217, 228-229, 238-262, 267-284, 289-337, 342-345, 350-353
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             57     25    56%   31-32, 40-41, 45-46, 54, 81-98, 108, 118, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          66     50    24%   69-132, 139, 188-225
src\core\logging\filters.py                                             60     28    53%   114, 117, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83     25    70%   84, 88-90, 122, 125, 130, 132, 134, 136, 164-165, 205-215, 224, 230-240
src\core\logging\logger.py                                             109     25    77%   84, 96, 123, 137-139, 147-148, 161-165, 173-174, 179-180, 199, 205, 213, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     76    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 218-220, 226-228, 234-236
src\core\logging\viewer.py                                             175    141    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    110    12%   21-37, 55-69, 73-74, 78-106, 110-141, 150-205, 214-252
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                       111     80    28%   31-37, 40-47, 51-61, 65-78, 82-86, 105-150, 154-156, 160, 164-171, 175-184, 188-197, 201, 205-208, 212-215
src\core\oda_manager.py                                                 34     20    41%   23, 31-91, 100-115
src\core\report_history.py                                              67     44    34%   26-28, 36-42, 47-51, 62-86, 96, 114-134, 147-157
src\core\schemas.py                                                     77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                                             94     41    56%   31-49, 55-57, 63-71, 77, 83-85, 103-105, 111-115, 121, 124, 130-132, 143
src\core\stats_manager.py                                               47     33    30%   24-27, 31, 35-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                58     23    60%   32-37, 47-48, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-82, 84-93, 95-97
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           190    157    17%   41-53, 56-75, 77-87, 90-91, 94-180, 189-195, 197, 201-228, 230-242, 244-258, 260-274, 276-290
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            344    299    13%   29-31, 35-44, 48-66, 70-73, 77-85, 87-121, 129-144, 159-178, 181-199, 201-220, 222-288, 290-302, 305-324, 327-335, 338-348, 353-366, 369-376, 379-385, 389-398, 401-429, 432-446, 448-459, 461-468, 470-485
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 25-29, 33-65
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    99     85    14%   24-76, 79-86, 89-96, 99-106, 109, 112-113, 116-129, 132-137
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 111-132, 135, 138-140, 143-157, 160-163, 166-173, 176-179, 182-184, 187-189, 192-218, 221-237, 242-244, 247-272
src\gui\controllers\bot_controller.py                                   46     35    24%   20-23, 27-35, 39-42, 49-62, 66-80
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 61-63, 66, 69-70, 73
src\gui\controllers\navigation_controller.py                           153    123    20%   40-41, 45-61, 65-82, 85-99, 102-105, 108-111, 114-117, 120-123, 126-129, 132-135, 138-141, 144-147, 150-153, 156-159, 163-169, 173-177, 181-186, 198-234, 238-257, 261-263, 267-268, 272-273, 277-310, 314-315
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              205    179    13%   33-49, 54-69, 77-130, 137-165, 169-332, 339-347, 350-368, 375-422, 427-451, 454, 458-469
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     53     7%   1, 12, 17-20, 22-101
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-112, 115-120
src\gui\dialogs\bug_report_dialog.py                                   229    207    10%   51-55, 58-67, 74-79, 82-223, 227-235, 238-268, 271-297, 301-307, 311-456, 460-477
src\gui\dialogs\command_palette.py                                     306    276    10%   45-76, 79-191, 194-222, 225-233, 236-240, 243-249, 253-260, 263-297, 301-311, 314-319, 324-330, 333-338, 342-347, 350-363, 366-378, 381-388, 391-395, 398-442, 445-480, 484-501, 504-522
src\gui\dialogs\confirmation_dialog.py                                  84     67    20%   1, 10, 15-21, 34-79, 81-90, 92-101, 104-107, 110-111, 115-116, 120-126
src\gui\dialogs\quick_actions_config.py                                 86     86     0%   1-214
src\gui\dialogs\standard_input_dialog.py                                37     34     8%   1, 11-14, 23-75, 78-80
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  131    113    14%   14-28, 38-68, 73, 90-96, 100-103, 107, 110, 113, 116-141, 146-148, 151-154, 158-237
src\gui\layouts\responsive.py                                           72     70     3%   5, 9-12, 15-109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     55    25%   18-23, 27-33, 37-49, 53-64, 69-78, 82-330
src\gui\main_window\components\status_bar.py                           157    140    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-277
src\gui\main_window\components\tool_bar.py                              26     17    35%   12-16, 20-23, 27-41
src\gui\main_window\components\tray_icon.py                             17     11    35%   12-17, 20, 29-38
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            282    214    24%   51-101, 105-139, 151-154, 157-181, 184-191, 195, 198, 201, 204, 207, 210, 213, 216, 220, 258-269, 273-283, 286-290, 298-302, 310-314, 320, 322-324, 330, 332-335, 337-340, 342-347, 350-360, 363-366, 368-385, 387-391, 393-397, 400-409, 412-415, 417, 420-421, 424-425, 430, 433-434, 437-442, 445-446, 449-463
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          130     30    77%   53, 98, 111-112, 122, 128, 130, 140-142, 155, 158, 161-163, 167-171, 178, 180, 182-183, 186-187, 190-193
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 197    141    28%   52-56, 60-77, 89-93, 97-99, 124-132, 136-180, 187, 191-202, 212, 220, 229, 233-238, 242-245, 249-251, 255-266, 270-273, 277-293, 297-301, 305-310, 320-322, 326-339, 343, 347-362, 369-372, 376-381, 385-388
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-105, 109-117, 121-122, 126-180
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14     12    14%   1-9, 11-16, 18-20
src\gui\panels\contabilita_kpi\charts.py                               200    183     8%   21-61, 68-76, 79-82, 86-90, 93-157, 160-214, 217-279, 282-321, 324-370
src\gui\panels\contabilita_kpi\kpi_panel.py                            159    140    12%   35-58, 61-188, 192-197, 199-213, 215-226, 228-229, 231-298
src\gui\panels\contabilita_panel.py                                    249    215    14%   39-46, 50-56, 60-162, 167-173, 177, 200, 203-221, 224-276, 279-282, 286-289, 292-316, 318-337, 340-342, 344-349, 351-372, 374-391, 394-396, 399-413
src\gui\panels\dashboard_panel.py                                      166    144    13%   26-90, 94, 98-105, 109-136, 140-142, 146-156, 160-175, 180-195, 200-218, 222-233, 237-243, 247-262, 266-288, 292-298
src\gui\panels\dettagli_oda.py                                         137    112    18%   27-35, 38-42, 46-90, 93-95, 99, 102-114, 117-127, 130-132, 136-142, 145-221, 225-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     398    360    10%   55-99, 102-240, 244-284, 288-301, 304-336, 338-380, 383-392, 395-411, 413-422, 431-458, 460-496, 498-538, 545-584, 588-672, 674-677, 684-712
src\gui\panels\dipendenti\shared.py                                    151    134    11%   26-73, 90-176, 178-181, 183-186, 190, 193-195, 197-241, 244-273
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   9-11, 17-44, 55-67, 71-78
src\gui\panels\dipendenti\utils\report_generator.py                    153    127    17%   25-51, 56-99, 108-194, 199-210, 215-237, 242-299
src\gui\panels\dipendenti\widgets\employee_detail_view.py              104     92    12%   24-29, 32-144, 151-170
src\gui\panels\dipendenti_manager_panel.py                             186    168    10%   28-71, 74, 85-105, 108-133, 136-214, 226-252, 254-273, 275-297, 305-341
src\gui\panels\health_panel.py                                         291    259    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-525, 529-557, 561-566, 570-573
src\gui\panels\help_panel.py                                           122    101    17%   6, 20, 25-31, 33-37, 39-169, 186-197, 199-209, 211-220, 223, 243, 263, 275, 289, 300, 313, 325, 336, 346, 356, 364
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        35     32     9%   1, 11-19, 21-57
src\gui\panels\lyra\header.py                                           38     33    13%   1, 11, 15-18, 22, 24-80
src\gui\panels\lyra\input_bar.py                                        41     34    17%   1, 9, 13-16, 19, 21-23, 25-79, 81-85, 87-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-122, 125-130, 133-140, 143-144, 147-148, 151-153, 156-161, 164-166, 169-178, 181-182, 185-188, 191-193, 197, 200-212
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 45-46, 49-57
src\gui\panels\notifications_panel.py                                  254    207    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-311, 315-316, 320-338, 342-374, 378-380, 384-403, 407-446
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 16-26
src\gui\panels\pdl\pdl_detail_view.py                                   47     36    23%   20-23, 26-48, 52-65, 69-70
src\gui\panels\pdl\pdl_filter_widget.py                                 66     55    17%   1, 11, 16-19, 26, 28-32, 34-109
src\gui\panels\pdl\pdl_panel.py                                        353    317    10%   44-108, 111-160, 164-218, 221-234, 238-267, 271-283, 287-319, 323-361, 365-367, 371-372, 376-387, 391-397, 401-420, 424-496, 500-504, 508-522, 526-550, 554-595
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-183
src\gui\panels\ricerca_pdl.py                                           86     72    16%   31-38, 41-71, 73-78, 81-84, 94-101, 103-152
src\gui\panels\scarico_ore_panel.py                                    338    303    10%   44-86, 89-99, 104-255, 257-273, 276-316, 318-328, 330-362, 364-383, 386, 392-420, 424-430, 432-436, 439-464, 467-525, 527-532, 535-543
src\gui\panels\scarico_pdl.py                                          301    271    10%   42-59, 63-84, 88-121, 131-139, 142-146, 150-275, 278-286, 289-292, 295-308, 311-316, 320, 323-325, 329-337, 342-532
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-79, 83-85, 89, 93-106, 110-118, 122-124, 128-133, 147-149, 155-211
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              33     23    30%   15-16, 19-40, 43-49
src\gui\panels\settings\pages\general_page.py                           44     34    23%   22-23, 26-66, 70-71, 75-76
src\gui\panels\settings\pages\lists_page.py                            336    283    16%   35-36, 39-65, 70-87, 90-114, 121-136, 143-158, 165-180, 187-204, 206-208, 217-218, 225, 235, 253-264, 274-280, 282-290, 292-300, 302-311, 313-330, 332-342, 344-353, 355-365, 367-382, 384-394, 396-409, 411-417, 419-423, 425-442, 445, 448, 451, 454, 457, 460, 463, 466, 469, 472, 475, 480, 482-492, 494
src\gui\panels\settings\pages\paths_page.py                            119    101    15%   29-30, 33-112, 127-153, 156-161, 163-184, 188-189, 192-197, 200-210
src\gui\panels\settings\shared.py                                       16     13    19%   1, 5-96, 100
src\gui\panels\settings\tabs\backup_tab.py                             134    115    14%   32-33, 36-146, 149-156, 159-161, 164, 167-172, 175-176, 179-198, 201-225
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           140    123    12%   30-31, 34-142, 144-154, 157-193, 195-213
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              42     38    10%   1, 6-9, 11-13, 15-73
src\gui\panels\storico_oda\oda_detail_view.py                           48     38    21%   21-24, 27-54, 56-72
src\gui\panels\storico_oda\oda_filter_widget.py                         40     32    20%   1, 10, 15-18, 23, 25-29, 31-77
src\gui\panels\storico_oda\oda_panel.py                                253    222    12%   43-106, 109-169, 173-181, 185-284, 287-302, 305, 308, 311-315, 318-324, 328-346, 350-408, 411-416, 419-439, 443-463
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     62     50    19%   16-39, 42-64, 72-112, 116-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    99     85    14%   28-33, 36-80, 84-105, 109-138, 143-149, 152-153, 156-161
src\gui\panels\timbrature\panel.py                                     173    150    13%   38-62, 65-97, 100-131, 134-179, 182-199, 203-238, 241-260, 263-269, 278-299
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         67     50    25%   26-29, 34, 41-51, 55-92, 97-118, 123
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     43     4%   6, 10-15, 17-91
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       136    118    13%   29-180, 184, 188-190, 199-207, 210-258, 263, 268-314
src\gui\widgets\animated_progress_bar.py                                74     72     3%   7, 18-37, 39-150
src\gui\widgets\audit\audit_filter_bar.py                               78     31    60%   31, 36-37, 43, 49, 54-55, 60-61, 68-69, 83-88, 91, 96, 98-120, 123, 126
src\gui\widgets\audit\audit_pagination_bar.py                           34     13    62%   1, 5-10, 14, 18, 22, 25, 29, 35, 40, 45, 47
src\gui\widgets\audit_log_widget.py                                    104     28    73%   76, 82-83, 87-88, 93, 108-111, 116, 125, 128-138, 140, 143-144, 155-156, 162-163, 172
src\gui\widgets\automazioni_widget.py                                   55     55     0%   1-132
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     82    42%   1, 13, 17, 30, 48, 52, 57, 68-70, 82, 85-88, 111, 115, 118, 127-129, 147, 151-158, 162, 165, 168-170, 176-201, 205, 219-229, 255, 261, 284-296, 299, 315-327, 343-354, 359, 362, 371-374, 379, 382
src\gui\widgets\autopilot\event_card.py                                 67     15    78%   27, 53-54, 59, 132-147, 163
src\gui\widgets\autopilot\main_widget.py                               204     57    72%   58, 61, 114, 123-124, 129-130, 137, 144, 149, 152, 155, 158, 162, 166, 169, 174, 181-182, 185-186, 191-192, 200-201, 214, 217, 222, 225-232, 234-238, 246, 249, 259, 268, 277, 287-288, 293, 303, 306-311, 342-343, 348, 354
src\gui\widgets\bot_parameters.py                                      108     87    19%   41-44, 47-109, 112-126, 129, 145-151, 154-167, 171-174, 177-180, 183-195, 198, 202-205
src\gui\widgets\calendar_date_edit.py                                   17      6    65%   6-8, 12-15, 22, 74
src\gui\widgets\contabilita\attivita_tab.py                            221    188    15%   53-63, 67-142, 145, 148-163, 167-183, 186-197, 200-206, 209-214, 217-235, 238-241, 245-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-296, 299-308
src\gui\widgets\contabilita\certificati_tab.py                         577    525     9%   43-52, 55-244, 248-274, 278-348, 352-465, 510-522, 526-530, 534-538, 546-713, 717-718, 722-733, 738-742, 746-750, 754, 758-893, 902-924, 930-967, 972-983, 987-995, 999-1002, 1006-1009, 1013-1027, 1030-1100, 1104-1106, 1110-1112, 1116-1152, 1159-1164, 1169-1212
src\gui\widgets\contabilita\giornaliere_tab.py                         189    158    16%   47-50, 54-95, 99, 102-129, 132-139, 143, 146-166, 169-189, 193-212, 215-240, 243-259
src\gui\widgets\contabilita\helpers.py                                  36     29    19%   11-35, 38-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                100     81    19%   25-26, 30-31, 34-51, 73-93, 96-137, 141, 145-166, 170-201, 205, 209
src\gui\widgets\data_table.py                                          108     84    22%   48-52, 55-126, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 214
src\gui\widgets\excel_table.py                                         335    295    12%   33-38, 49-61, 65-72, 76-93, 97-117, 120-121, 124-125, 129-140, 144-166, 170-193, 197-216, 220-240, 244-253, 256-261, 264-268, 271-275, 284-286, 289-311, 314-371, 374-377, 380-386, 389-421, 424-427, 430-432, 435, 439-456, 465-475, 479-519, 524-549
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   26-80, 83-90, 93-98, 101-105, 108-111, 115-121
src\gui\widgets\footer\components.py                                    55     38    31%   19-36, 40, 42-49, 51-59, 65, 67-70, 73, 77-85, 89, 94
src\gui\widgets\footer\manager.py                                       20     13    35%   1-3, 8, 19-22, 28-33, 35
src\gui\widgets\footer\status_bar.py                                    35     33     6%   1, 4-7, 13-50
src\gui\widgets\footer\telemetry.py                                     55     40    27%   19-51, 54-57, 60-62, 65-69
src\gui\widgets\info_widgets.py                                         90     76    16%   29-66, 72-80, 85-112, 135-170
src\gui\widgets\message_bubble.py                                       53     48     9%   7, 20-37, 39-42, 44-123
src\gui\widgets\modern_button.py                                        62     35    44%   43-55, 59-61, 65, 69-70, 76-79, 83-86, 90-91, 101-106, 110-149
src\gui\widgets\notification_card.py                                   240    209    13%   86-102, 106-354, 358-368, 372, 376-378, 392-423, 427-443, 447-452, 456-458, 462-463, 467-472, 476-480, 484-521, 525-531, 535-542
src\gui\widgets\notification_group_header.py                            47     44     6%   6, 11-23, 33-145
src\gui\widgets\notification_item.py                                    72     60    17%   22-25, 28-131, 134
src\gui\widgets\notification_toolbar.py                                104     78    25%   36-48, 52-64, 68-70, 74-78, 82-101, 133-139, 143-228, 233-234, 238-239, 244-251, 255-256, 265-267, 271, 275, 279
src\gui\widgets\priority_badge.py                                       47     35    26%   30-37, 41-78, 82-90, 94-98, 102, 106-108
src\gui\widgets\quick_actions.py                                        77     61    21%   24-32, 236-237, 240-263, 267-308, 313-353, 358
src\gui\widgets\security_dashboard.py                                  154    154     0%   1-251
src\gui\widgets\sidebar_button.py                                       41     39     5%   1, 4-10, 12-89
src\gui\widgets\sidebar_widget.py                                      245    209    15%   17-22, 29-63, 67-71, 75, 78-79, 82-86, 89-101, 105-113, 125-150, 154-156, 160-162, 166-169, 173-196, 200-218, 221-371, 375, 379, 383, 387-388, 392-393, 399-435
src\gui\widgets\simple_chart.py                                         66     66     0%   1-105
src\gui\widgets\sortable_table_item.py                                  51     41    20%   21-26, 30-62, 67-80, 84-97
src\gui\widgets\statistics_widget.py                                   107     92    14%   27-28, 31-117, 128-160, 162-166, 169-220
src\gui\widgets\status_card.py                                          60     52    13%   1, 5, 10-19, 21-91, 96-102, 105-125
src\gui\widgets\status_indicator.py                                     43     40     7%   6, 11-17, 19-69
src\gui\widgets\timeline_widget.py                                     203    171    16%   46-68, 73-80, 83-116, 119-132, 134-140, 142-152, 154-155, 158-162, 167-171, 173-188, 193-199, 201-215, 217-232, 234-241, 243-250, 255-276, 278-282, 288-314
src\gui\widgets\toast.py                                               131    103    21%   59-80, 84-123, 127-149, 152-157, 161-163, 167-168, 171-183, 194-196, 206-255
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     57    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-144, 157-164, 178-181, 194, 208, 222-228
src\utils\document_generator.py                                         17     14    18%   11-39
src\utils\document_processor.py                                         60     22    63%   14-15, 24-32, 38, 50-51, 59, 63-64, 71-72, 81-83
src\utils\helpers.py                                                    91     54    41%   30-34, 48-70, 83-85, 90, 117-118, 123, 136-151, 165-167, 182-188, 203, 222, 233, 239-242
src\utils\log_humanizer.py                                              42     30    29%   13-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    54     46    15%   14-34, 40-52, 57-67, 72-80, 85-98, 103-120
src\utils\printing.py                                                   86     70    19%   19-24, 29-40, 48-54, 65-144
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     34    57%   43-44, 72-75, 79, 81-88, 97-101, 103, 106, 110-115, 118, 120-127, 129-141
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                24569  18561    24%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_base_bot.py::TestBaseBot::test_init_sets_credentials - ...
============================== 1 error in 6.76s ===============================

```
</details>

---
### `tests/unit/test_base_bot_init_refactoring.py::test_init_driver_success`
**Error:** `Unknown Error`

**Timestamp:** `2026-02-09T18:54:36.122751`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_base_bot_init_refactoring.py E                           [100%]

=================================== ERRORS ====================================
_________________ ERROR at setup of test_init_driver_success __________________
tests\unit\test_base_bot_init_refactoring.py:34: in bot
    return ConcreteBot("user", "pass")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: Can't instantiate abstract class ConcreteBot without an implementation for abstract method 'get_columns'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    22      7    68%   121, 135-141
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    165    37%   115, 140-142, 169-185, 189-232, 236-258, 262-264, 271-276, 280-307, 319-368, 372-404, 409-418, 422-426, 430-432, 436, 440-446, 457-469, 474-476
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    138    17%   50-55, 76-81, 100-104, 135-198, 221, 250-304, 324-325, 328-332, 345, 348-352, 374-377, 380-390, 420-436, 466-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     27    43%   52, 56, 60-72, 77-100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-91, 95-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   39-42, 46, 50-52, 65-90, 101-114, 118-147, 151-158, 182-277, 281-299, 309-335, 339-348, 352-361, 365-376
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            84     67    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-104, 108-129
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           221    181    18%   57, 61, 73-76, 80-82, 86-101, 105-122, 127-142, 146-168, 172-199, 203-212, 216-241, 245-277, 283-312, 316-325, 329-344, 348-369, 374-384
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         105     83    21%   28-31, 35, 39-45, 49-66, 70-92, 96-125, 129-146, 150-155, 159-168
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-108
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-69, 75-118, 125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-85, 89-148, 152-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       178    107    40%   91-109, 118, 124-141, 163-173, 184-188, 191, 194-222, 229-260, 275-287, 289-290, 302-303, 308, 319, 321-322, 335, 340-342, 345, 348, 353, 371-372, 374-375, 379-392, 401-402
src\bots\safework\base.py                                               42     27    36%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           391    335    14%   28, 33, 38, 43, 48, 59-63, 67, 71, 75-107, 111-170, 174-178, 182-210, 216-244, 249-256, 261-293, 299-326, 331-343, 348-375, 380-414, 419-431, 437-457, 462-473, 481-517, 522-560, 566-585
src\bots\safework\pdl\search_bot.py                                    182    155    15%   19-20, 24, 28, 32, 36-94, 98-115, 119-136, 140-149, 153-163, 167-172, 176-201, 205-230, 234-304
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82      0   100%
src\core\app_updater.py                                                 48     11    77%   38, 49-50, 54, 57, 73, 82, 92-97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             100     35    65%   61-63, 78-79, 110-112, 114-117, 119-122, 124-126, 128-132, 145-146, 150-155, 162-164
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     18    87%   51, 63-64, 175-178, 189, 191, 200-201, 215, 231-232, 242, 280, 282-283
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               28     13    54%   23-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157    126    20%   60-107, 112-143, 148-158, 163-185, 190-210, 215-238, 243-295, 300-312, 321-339
src\core\config_manager.py                                             237    114    52%   35, 87, 109-115, 136, 141-142, 156-170, 179-180, 199-200, 222, 226-229, 247, 252, 264, 279, 289-302, 307-317, 326-353, 358-362, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     53    48%   30, 35, 40, 49-61, 78-125, 134-141, 150-155, 164-171, 176, 181, 186, 191, 201, 210, 222-225
src\core\contabilita_queries.py                                         87     61    30%   19-30, 35-48, 53-78, 83-94, 100, 109-110, 115-126
src\core\contabilita_search.py                                          92     53    42%   26-82, 90, 110-111, 118-127, 136-138, 150, 155-157, 160, 165-166, 179, 182-185
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         102     87    15%   23-28, 32-63, 67-127, 132-154, 160-171, 178-211, 213-216
src\core\data_synchronizer.py                                          159    112    30%   22, 38-55, 60-70, 76-103, 109-147, 157-192, 202-235, 269, 272, 277-278, 283, 285, 287-295, 312-313, 322-325
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           121     41    66%   131-140, 149-179, 193-194, 212, 215, 222, 224
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     11    35%   6-21, 27-28, 33, 36-39
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      7    36%   6-49, 56-57
src\core\database\migrations\timbrature.py                              27     20    26%   6-25, 30-32, 37, 40-47, 52-54, 67-69
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              58     36    38%   15-16, 23-25, 35-37, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                                      181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    133    13%   21-63, 68-69, 74, 79, 84-100, 105-145, 150-190, 195-197, 202-208, 213-233, 238-246, 251-269, 274-283, 287-290
src\core\license_validator.py                                          180    133    26%   37-41, 50-57, 71-75, 95-110, 116-132, 137-144, 158-181, 191-217, 228-229, 238-262, 267-284, 289-337, 342-345, 350-353
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             57     24    58%   31-32, 40-41, 45-46, 54, 81-98, 118, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          66     50    24%   69-132, 139, 188-225
src\core\logging\filters.py                                             60     28    53%   114, 117, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83     25    70%   84, 88-90, 122, 125, 130, 132, 134, 136, 164-165, 205-215, 224, 230-240
src\core\logging\logger.py                                             109     25    77%   84, 96, 123, 137-139, 147-148, 161-165, 173-174, 179-180, 199, 205, 213, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     76    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 218-220, 226-228, 234-236
src\core\logging\viewer.py                                             175    141    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    110    12%   21-37, 55-69, 73-74, 78-106, 110-141, 150-205, 214-252
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                       111     80    28%   31-37, 40-47, 51-61, 65-78, 82-86, 105-150, 154-156, 160, 164-171, 175-184, 188-197, 201, 205-208, 212-215
src\core\oda_manager.py                                                 34     20    41%   23, 31-91, 100-115
src\core\report_history.py                                              67     44    34%   26-28, 36-42, 47-51, 62-86, 96, 114-134, 147-157
src\core\schemas.py                                                     77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                                             94     41    56%   31-49, 55-57, 63-71, 77, 83-85, 103-105, 111-115, 121, 124, 130-132, 143
src\core\stats_manager.py                                               47     33    30%   24-27, 31, 35-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                58     23    60%   32-37, 47-48, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-82, 84-93, 95-97
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           190    157    17%   41-53, 56-75, 77-87, 90-91, 94-180, 189-195, 197, 201-228, 230-242, 244-258, 260-274, 276-290
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            344    299    13%   29-31, 35-44, 48-66, 70-73, 77-85, 87-121, 129-144, 159-178, 181-199, 201-220, 222-288, 290-302, 305-324, 327-335, 338-348, 353-366, 369-376, 379-385, 389-398, 401-429, 432-446, 448-459, 461-468, 470-485
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 25-29, 33-65
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    99     85    14%   24-76, 79-86, 89-96, 99-106, 109, 112-113, 116-129, 132-137
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 111-132, 135, 138-140, 143-157, 160-163, 166-173, 176-179, 182-184, 187-189, 192-218, 221-237, 242-244, 247-272
src\gui\controllers\bot_controller.py                                   46     35    24%   20-23, 27-35, 39-42, 49-62, 66-80
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 61-63, 66, 69-70, 73
src\gui\controllers\navigation_controller.py                           153    123    20%   40-41, 45-61, 65-82, 85-99, 102-105, 108-111, 114-117, 120-123, 126-129, 132-135, 138-141, 144-147, 150-153, 156-159, 163-169, 173-177, 181-186, 198-234, 238-257, 261-263, 267-268, 272-273, 277-310, 314-315
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              205    179    13%   33-49, 54-69, 77-130, 137-165, 169-332, 339-347, 350-368, 375-422, 427-451, 454, 458-469
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     53     7%   1, 12, 17-20, 22-101
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-112, 115-120
src\gui\dialogs\bug_report_dialog.py                                   229    207    10%   51-55, 58-67, 74-79, 82-223, 227-235, 238-268, 271-297, 301-307, 311-456, 460-477
src\gui\dialogs\command_palette.py                                     306    276    10%   45-76, 79-191, 194-222, 225-233, 236-240, 243-249, 253-260, 263-297, 301-311, 314-319, 324-330, 333-338, 342-347, 350-363, 366-378, 381-388, 391-395, 398-442, 445-480, 484-501, 504-522
src\gui\dialogs\confirmation_dialog.py                                  84     67    20%   1, 10, 15-21, 34-79, 81-90, 92-101, 104-107, 110-111, 115-116, 120-126
src\gui\dialogs\quick_actions_config.py                                 86     86     0%   1-214
src\gui\dialogs\standard_input_dialog.py                                37     34     8%   1, 11-14, 23-75, 78-80
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  131    113    14%   14-28, 38-68, 73, 90-96, 100-103, 107, 110, 113, 116-141, 146-148, 151-154, 158-237
src\gui\layouts\responsive.py                                           72     70     3%   5, 9-12, 15-109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     55    25%   18-23, 27-33, 37-49, 53-64, 69-78, 82-330
src\gui\main_window\components\status_bar.py                           157    140    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-277
src\gui\main_window\components\tool_bar.py                              26     17    35%   12-16, 20-23, 27-41
src\gui\main_window\components\tray_icon.py                             17     11    35%   12-17, 20, 29-38
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            282    214    24%   51-101, 105-139, 151-154, 157-181, 184-191, 195, 198, 201, 204, 207, 210, 213, 216, 220, 258-269, 273-283, 286-290, 298-302, 310-314, 320, 322-324, 330, 332-335, 337-340, 342-347, 350-360, 363-366, 368-385, 387-391, 393-397, 400-409, 412-415, 417, 420-421, 424-425, 430, 433-434, 437-442, 445-446, 449-463
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          130     30    77%   53, 98, 111-112, 122, 128, 130, 140-142, 155, 158, 161-163, 167-171, 178, 180, 182-183, 186-187, 190-193
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 197    141    28%   52-56, 60-77, 89-93, 97-99, 124-132, 136-180, 187, 191-202, 212, 220, 229, 233-238, 242-245, 249-251, 255-266, 270-273, 277-293, 297-301, 305-310, 320-322, 326-339, 343, 347-362, 369-372, 376-381, 385-388
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-105, 109-117, 121-122, 126-180
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14     12    14%   1-9, 11-16, 18-20
src\gui\panels\contabilita_kpi\charts.py                               200    183     8%   21-61, 68-76, 79-82, 86-90, 93-157, 160-214, 217-279, 282-321, 324-370
src\gui\panels\contabilita_kpi\kpi_panel.py                            159    140    12%   35-58, 61-188, 192-197, 199-213, 215-226, 228-229, 231-298
src\gui\panels\contabilita_panel.py                                    249    215    14%   39-46, 50-56, 60-162, 167-173, 177, 200, 203-221, 224-276, 279-282, 286-289, 292-316, 318-337, 340-342, 344-349, 351-372, 374-391, 394-396, 399-413
src\gui\panels\dashboard_panel.py                                      166    144    13%   26-90, 94, 98-105, 109-136, 140-142, 146-156, 160-175, 180-195, 200-218, 222-233, 237-243, 247-262, 266-288, 292-298
src\gui\panels\dettagli_oda.py                                         137    112    18%   27-35, 38-42, 46-90, 93-95, 99, 102-114, 117-127, 130-132, 136-142, 145-221, 225-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     398    360    10%   55-99, 102-240, 244-284, 288-301, 304-336, 338-380, 383-392, 395-411, 413-422, 431-458, 460-496, 498-538, 545-584, 588-672, 674-677, 684-712
src\gui\panels\dipendenti\shared.py                                    151    134    11%   26-73, 90-176, 178-181, 183-186, 190, 193-195, 197-241, 244-273
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   9-11, 17-44, 55-67, 71-78
src\gui\panels\dipendenti\utils\report_generator.py                    153    127    17%   25-51, 56-99, 108-194, 199-210, 215-237, 242-299
src\gui\panels\dipendenti\widgets\employee_detail_view.py              104     92    12%   24-29, 32-144, 151-170
src\gui\panels\dipendenti_manager_panel.py                             186    168    10%   28-71, 74, 85-105, 108-133, 136-214, 226-252, 254-273, 275-297, 305-341
src\gui\panels\health_panel.py                                         291    259    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-525, 529-557, 561-566, 570-573
src\gui\panels\help_panel.py                                           122    101    17%   6, 20, 25-31, 33-37, 39-169, 186-197, 199-209, 211-220, 223, 243, 263, 275, 289, 300, 313, 325, 336, 346, 356, 364
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        35     32     9%   1, 11-19, 21-57
src\gui\panels\lyra\header.py                                           38     33    13%   1, 11, 15-18, 22, 24-80
src\gui\panels\lyra\input_bar.py                                        41     34    17%   1, 9, 13-16, 19, 21-23, 25-79, 81-85, 87-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-122, 125-130, 133-140, 143-144, 147-148, 151-153, 156-161, 164-166, 169-178, 181-182, 185-188, 191-193, 197, 200-212
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 45-46, 49-57
src\gui\panels\notifications_panel.py                                  254    207    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-311, 315-316, 320-338, 342-374, 378-380, 384-403, 407-446
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 16-26
src\gui\panels\pdl\pdl_detail_view.py                                   47     36    23%   20-23, 26-48, 52-65, 69-70
src\gui\panels\pdl\pdl_filter_widget.py                                 66     55    17%   1, 11, 16-19, 26, 28-32, 34-109
src\gui\panels\pdl\pdl_panel.py                                        353    317    10%   44-108, 111-160, 164-218, 221-234, 238-267, 271-283, 287-319, 323-361, 365-367, 371-372, 376-387, 391-397, 401-420, 424-496, 500-504, 508-522, 526-550, 554-595
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-183
src\gui\panels\ricerca_pdl.py                                           86     72    16%   31-38, 41-71, 73-78, 81-84, 94-101, 103-152
src\gui\panels\scarico_ore_panel.py                                    338    303    10%   44-86, 89-99, 104-255, 257-273, 276-316, 318-328, 330-362, 364-383, 386, 392-420, 424-430, 432-436, 439-464, 467-525, 527-532, 535-543
src\gui\panels\scarico_pdl.py                                          301    271    10%   42-59, 63-84, 88-121, 131-139, 142-146, 150-275, 278-286, 289-292, 295-308, 311-316, 320, 323-325, 329-337, 342-532
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-79, 83-85, 89, 93-106, 110-118, 122-124, 128-133, 147-149, 155-211
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              33     23    30%   15-16, 19-40, 43-49
src\gui\panels\settings\pages\general_page.py                           44     34    23%   22-23, 26-66, 70-71, 75-76
src\gui\panels\settings\pages\lists_page.py                            336    283    16%   35-36, 39-65, 70-87, 90-114, 121-136, 143-158, 165-180, 187-204, 206-208, 217-218, 225, 235, 253-264, 274-280, 282-290, 292-300, 302-311, 313-330, 332-342, 344-353, 355-365, 367-382, 384-394, 396-409, 411-417, 419-423, 425-442, 445, 448, 451, 454, 457, 460, 463, 466, 469, 472, 475, 480, 482-492, 494
src\gui\panels\settings\pages\paths_page.py                            119    101    15%   29-30, 33-112, 127-153, 156-161, 163-184, 188-189, 192-197, 200-210
src\gui\panels\settings\shared.py                                       16     13    19%   1, 5-96, 100
src\gui\panels\settings\tabs\backup_tab.py                             134    115    14%   32-33, 36-146, 149-156, 159-161, 164, 167-172, 175-176, 179-198, 201-225
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           140    123    12%   30-31, 34-142, 144-154, 157-193, 195-213
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              42     38    10%   1, 6-9, 11-13, 15-73
src\gui\panels\storico_oda\oda_detail_view.py                           48     38    21%   21-24, 27-54, 56-72
src\gui\panels\storico_oda\oda_filter_widget.py                         40     32    20%   1, 10, 15-18, 23, 25-29, 31-77
src\gui\panels\storico_oda\oda_panel.py                                253    222    12%   43-106, 109-169, 173-181, 185-284, 287-302, 305, 308, 311-315, 318-324, 328-346, 350-408, 411-416, 419-439, 443-463
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     62     50    19%   16-39, 42-64, 72-112, 116-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    99     85    14%   28-33, 36-80, 84-105, 109-138, 143-149, 152-153, 156-161
src\gui\panels\timbrature\panel.py                                     173    150    13%   38-62, 65-97, 100-131, 134-179, 182-199, 203-238, 241-260, 263-269, 278-299
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         67     50    25%   26-29, 34, 41-51, 55-92, 97-118, 123
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     43     4%   6, 10-15, 17-91
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       136    118    13%   29-180, 184, 188-190, 199-207, 210-258, 263, 268-314
src\gui\widgets\animated_progress_bar.py                                74     72     3%   7, 18-37, 39-150
src\gui\widgets\audit\audit_filter_bar.py                               78     31    60%   31, 36-37, 43, 49, 54-55, 60-61, 68-69, 83-88, 91, 96, 98-120, 123, 126
src\gui\widgets\audit\audit_pagination_bar.py                           34     13    62%   1, 5-10, 14, 18, 22, 25, 29, 35, 40, 45, 47
src\gui\widgets\audit_log_widget.py                                    104     28    73%   76, 82-83, 87-88, 93, 108-111, 116, 125, 128-138, 140, 143-144, 155-156, 162-163, 172
src\gui\widgets\automazioni_widget.py                                   55     55     0%   1-132
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     82    42%   1, 13, 17, 30, 48, 52, 57, 68-70, 82, 85-88, 111, 115, 118, 127-129, 147, 151-158, 162, 165, 168-170, 176-201, 205, 219-229, 255, 261, 284-296, 299, 315-327, 343-354, 359, 362, 371-374, 379, 382
src\gui\widgets\autopilot\event_card.py                                 67     15    78%   27, 53-54, 59, 132-147, 163
src\gui\widgets\autopilot\main_widget.py                               204     57    72%   58, 61, 114, 123-124, 129-130, 137, 144, 149, 152, 155, 158, 162, 166, 169, 174, 181-182, 185-186, 191-192, 200-201, 214, 217, 222, 225-232, 234-238, 246, 249, 259, 268, 277, 287-288, 293, 303, 306-311, 342-343, 348, 354
src\gui\widgets\bot_parameters.py                                      108     87    19%   41-44, 47-109, 112-126, 129, 145-151, 154-167, 171-174, 177-180, 183-195, 198, 202-205
src\gui\widgets\calendar_date_edit.py                                   17      6    65%   6-8, 12-15, 22, 74
src\gui\widgets\contabilita\attivita_tab.py                            221    188    15%   53-63, 67-142, 145, 148-163, 167-183, 186-197, 200-206, 209-214, 217-235, 238-241, 245-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-296, 299-308
src\gui\widgets\contabilita\certificati_tab.py                         577    525     9%   43-52, 55-244, 248-274, 278-348, 352-465, 510-522, 526-530, 534-538, 546-713, 717-718, 722-733, 738-742, 746-750, 754, 758-893, 902-924, 930-967, 972-983, 987-995, 999-1002, 1006-1009, 1013-1027, 1030-1100, 1104-1106, 1110-1112, 1116-1152, 1159-1164, 1169-1212
src\gui\widgets\contabilita\giornaliere_tab.py                         189    158    16%   47-50, 54-95, 99, 102-129, 132-139, 143, 146-166, 169-189, 193-212, 215-240, 243-259
src\gui\widgets\contabilita\helpers.py                                  36     29    19%   11-35, 38-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                100     81    19%   25-26, 30-31, 34-51, 73-93, 96-137, 141, 145-166, 170-201, 205, 209
src\gui\widgets\data_table.py                                          108     84    22%   48-52, 55-126, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 214
src\gui\widgets\excel_table.py                                         335    295    12%   33-38, 49-61, 65-72, 76-93, 97-117, 120-121, 124-125, 129-140, 144-166, 170-193, 197-216, 220-240, 244-253, 256-261, 264-268, 271-275, 284-286, 289-311, 314-371, 374-377, 380-386, 389-421, 424-427, 430-432, 435, 439-456, 465-475, 479-519, 524-549
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   26-80, 83-90, 93-98, 101-105, 108-111, 115-121
src\gui\widgets\footer\components.py                                    55     38    31%   19-36, 40, 42-49, 51-59, 65, 67-70, 73, 77-85, 89, 94
src\gui\widgets\footer\manager.py                                       20     13    35%   1-3, 8, 19-22, 28-33, 35
src\gui\widgets\footer\status_bar.py                                    35     33     6%   1, 4-7, 13-50
src\gui\widgets\footer\telemetry.py                                     55     40    27%   19-51, 54-57, 60-62, 65-69
src\gui\widgets\info_widgets.py                                         90     76    16%   29-66, 72-80, 85-112, 135-170
src\gui\widgets\message_bubble.py                                       53     48     9%   7, 20-37, 39-42, 44-123
src\gui\widgets\modern_button.py                                        62     35    44%   43-55, 59-61, 65, 69-70, 76-79, 83-86, 90-91, 101-106, 110-149
src\gui\widgets\notification_card.py                                   240    209    13%   86-102, 106-354, 358-368, 372, 376-378, 392-423, 427-443, 447-452, 456-458, 462-463, 467-472, 476-480, 484-521, 525-531, 535-542
src\gui\widgets\notification_group_header.py                            47     44     6%   6, 11-23, 33-145
src\gui\widgets\notification_item.py                                    72     60    17%   22-25, 28-131, 134
src\gui\widgets\notification_toolbar.py                                104     78    25%   36-48, 52-64, 68-70, 74-78, 82-101, 133-139, 143-228, 233-234, 238-239, 244-251, 255-256, 265-267, 271, 275, 279
src\gui\widgets\priority_badge.py                                       47     35    26%   30-37, 41-78, 82-90, 94-98, 102, 106-108
src\gui\widgets\quick_actions.py                                        77     61    21%   24-32, 236-237, 240-263, 267-308, 313-353, 358
src\gui\widgets\security_dashboard.py                                  154    154     0%   1-251
src\gui\widgets\sidebar_button.py                                       41     39     5%   1, 4-10, 12-89
src\gui\widgets\sidebar_widget.py                                      245    209    15%   17-22, 29-63, 67-71, 75, 78-79, 82-86, 89-101, 105-113, 125-150, 154-156, 160-162, 166-169, 173-196, 200-218, 221-371, 375, 379, 383, 387-388, 392-393, 399-435
src\gui\widgets\simple_chart.py                                         66     66     0%   1-105
src\gui\widgets\sortable_table_item.py                                  51     41    20%   21-26, 30-62, 67-80, 84-97
src\gui\widgets\statistics_widget.py                                   107     92    14%   27-28, 31-117, 128-160, 162-166, 169-220
src\gui\widgets\status_card.py                                          60     52    13%   1, 5, 10-19, 21-91, 96-102, 105-125
src\gui\widgets\status_indicator.py                                     43     40     7%   6, 11-17, 19-69
src\gui\widgets\timeline_widget.py                                     203    171    16%   46-68, 73-80, 83-116, 119-132, 134-140, 142-152, 154-155, 158-162, 167-171, 173-188, 193-199, 201-215, 217-232, 234-241, 243-250, 255-276, 278-282, 288-314
src\gui\widgets\toast.py                                               131    103    21%   59-80, 84-123, 127-149, 152-157, 161-163, 167-168, 171-183, 194-196, 206-255
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     57    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-144, 157-164, 178-181, 194, 208, 222-228
src\utils\document_generator.py                                         17     14    18%   11-39
src\utils\document_processor.py                                         60     22    63%   14-15, 24-32, 38, 50-51, 59, 63-64, 71-72, 81-83
src\utils\helpers.py                                                    91     54    41%   30-34, 48-70, 83-85, 90, 117-118, 123, 136-151, 165-167, 182-188, 203, 222, 233, 239-242
src\utils\log_humanizer.py                                              42     30    29%   13-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    54     46    15%   14-34, 40-52, 57-67, 72-80, 85-98, 103-120
src\utils\printing.py                                                   86     70    19%   19-24, 29-40, 48-54, 65-144
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     34    57%   43-44, 72-75, 79, 81-88, 97-101, 103, 106, 110-115, 118, 120-127, 129-141
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                24569  18522    25%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_base_bot_init_refactoring.py::test_init_driver_success
============================== 1 error in 7.09s ===============================

```
</details>

---
