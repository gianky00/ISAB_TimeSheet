# 📊 Test Execution Report

**Date:** 2026-02-08 01:21:52
**Duration:** 1698.92s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1496 |
| ✅ Passed | 1532 |
| ❌ Failed | 15 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_ai_sentinel_hardened.py::TestAISentinelHardened::test_document_processor_image_conversion`
**Error:** `FAILED tests/unit/test_ai_sentinel_hardened.py::TestAISentinelHardened::test_document_processor_image_conversion`

**Timestamp:** `2026-02-07T22:06:57.306009`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_ai_sentinel_hardened.py F                                [100%]

================================== FAILURES ===================================
_______ TestAISentinelHardened.test_document_processor_image_conversion _______
tests\unit\test_ai_sentinel_hardened.py:69: in test_document_processor_image_conversion
    assert len(images) == 1
E   assert 0 == 1
E    +  where 0 = len([])
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              260    203    22%   52-72, 87, 92-94, 106-110, 121-137, 141, 145, 149, 153-154, 158-159, 164-180, 184-227, 231-253, 257-259, 266-271, 275-302, 314-363, 367-399, 404-413, 417-421, 425-427, 431, 435-441, 452-464, 468-471
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    138    17%   50-55, 76-81, 100-104, 135-198, 221, 250-304, 324-325, 328-332, 345, 348-352, 374-377, 380-390, 420-436, 466-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     27    43%   52, 56, 60-72, 77-100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          80     55    31%   38, 42, 51-54, 60-67, 71-91, 95-106, 117-135, 139-144
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   39-42, 46, 50-52, 65-90, 101-114, 118-147, 151-158, 182-277, 281-299, 309-335, 339-348, 352-361, 365-376
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-103, 107-128
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         218    190    13%   28-31, 35, 39-41, 53-79, 90-95, 100-105, 109-137, 141-174, 178-186, 195-223, 227-234, 238-258, 262-274, 278-290, 294-312, 316-340, 344-348
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           218    178    18%   57, 61, 73-76, 80-82, 86-99, 103-120, 124-139, 143-165, 169-196, 200-209, 213-238, 242-274, 280-309, 313-322, 326-341, 345-366, 371-381
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     83    20%   27-30, 34, 38-44, 48-65, 69-91, 95-124, 128-145, 149-154, 158-167
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-107
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            70     50    29%   21, 26, 31, 36, 39-43, 47-60, 66-109, 116
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-85, 89-148, 152-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       175    102    42%   91-110, 116-145, 155-166, 176-183, 186-214, 221-257, 260-275, 320, 329, 357-358, 362-376, 383-384
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           387    343    11%   25, 30, 35, 40, 45, 56-60, 64, 68, 72-97, 101-160, 164-168, 172-200, 204-233, 237-245, 249-283, 287-315, 319-332, 336-364, 368-403, 407-421, 425-446, 450-462, 469-507, 510-550, 554-573
src\bots\safework\pdl\search_bot.py                                    179    154    14%   19-20, 24, 28, 32-90, 94-111, 115-132, 136-145, 149-159, 163-168, 172-197, 201-226, 230-300
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82     67    18%   15-17, 29-68, 74-119, 124-143, 148-156
src\core\app_updater.py                                                 46     37    20%   17-47, 52-57, 62-83, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     39    61%   61-63, 78-79, 110-112, 114-117, 119-122, 124-126, 128-132, 144-145, 149-154, 157-163
src\core\audit\integrity.py                                             15      2    87%   21, 26
src\core\audit\manager.py                                              139     70    50%   28, 38, 46, 50, 58-63, 170, 174-177, 183-200, 204-231, 241, 244-247, 255-283
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     62    14%   18, 25-57, 67-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-187, 198-206, 211-222, 227-249
src\core\bug_reporter.py                                               157    126    20%   60-107, 112-143, 148-158, 163-185, 190-210, 215-238, 243-295, 300-312, 321-339
src\core\config_manager.py                                             237    117    51%   35, 87, 109-115, 136, 141-142, 156-170, 179-180, 199-200, 222, 226-229, 247, 252, 257-259, 264, 279, 289-302, 307-317, 326-353, 358-362, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        101     51    50%   29, 34, 39, 48-60, 77-124, 133-140, 149-154, 163-170, 175, 180, 185, 190, 200, 209, 222
src\core\contabilita_queries.py                                         86     61    29%   18-29, 34-47, 52-77, 82-93, 99, 108-109, 114-125
src\core\contabilita_search.py                                          91     43    53%   25-81, 89, 109-110, 117-128, 137-138, 156-157
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          158    103    35%   21, 37-54, 59-69, 75-102, 108-146, 154-191, 199-234, 248, 264, 280, 282
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           120     40    67%   125-134, 141-171, 184-185, 211-213
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          65     48    26%   42-59, 63-77, 81-97, 101-115
src\core\importers\base.py                                              58     36    38%   15-16, 23-25, 35-37, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      135    109    19%   40-57, 68-104, 111-128, 133-187, 192-210, 215-239, 244-247
src\core\importers\giornaliere.py                                      190    155    18%   42-63, 73-91, 101-120, 126-145, 149-187, 191-206, 210-232, 236-288, 292-308
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    133    13%   21-63, 68-69, 74, 79, 84-100, 105-145, 150-190, 195-197, 202-208, 213-233, 238-246, 251-269, 274-283, 287-290
src\core\license_validator.py                                          179    133    26%   36-40, 49-56, 70-74, 94-109, 115-131, 136-143, 157-180, 190-216, 227-228, 237-261, 266-283, 288-336, 341-344, 349-352
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             52     22    58%   29-30, 38-39, 43-44, 52, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             66     33    50%   92, 112, 118, 121, 125, 142-156, 169-175, 193-194, 203-212
src\core\logging\formatters.py                                          82     25    70%   84, 88-90, 122, 125, 130, 132, 134, 136, 138, 168, 206-216, 225, 231-241
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 147-148, 161-165, 169-174, 179-180, 199, 205, 213, 217, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     16    70%   58, 67, 91, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                               99     75    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-205, 217-219, 225-227, 233-235
src\core\logging\viewer.py                                             175    142    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 149, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    110    12%   21-37, 55-69, 73-74, 78-106, 110-141, 150-205, 214-252
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                        95     68    28%   29-35, 38-45, 49-57, 61-74, 78-82, 101-146, 150-152, 156, 160-167, 171-180, 184-187, 191-194
src\core\oda_manager.py                                                 34     20    41%   23, 31-91, 100-115
src\core\report_history.py                                              65     43    34%   25-27, 35-40, 45-49, 60-84, 94, 112-132, 145-155
src\core\schemas.py                                                     77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                                             94     56    40%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 124-126, 131-134, 139-145
src\core\stats_manager.py                                               46     33    28%   23-26, 30, 34-47, 51, 55-66, 70-78, 82
src\core\sync_tracker.py                                                58     23    60%   32-37, 47-48, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    289    16%   29-31, 35-44, 48-66, 70-73, 77-84, 88-95, 98-125, 128-151, 154-159, 163-177, 180-196, 201-204, 207-208, 211-219, 222-230, 233-258, 262-287, 290-294, 297-302, 306-323, 326-334, 337-350, 353-366, 370-375, 379-385, 389-397, 401-427, 431-444, 448-455, 460-466, 469-496, 499-511, 514-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         97     75    23%   26-66, 71-81, 86-91, 96-103, 109-143, 148-156, 161-163
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-133, 136-150, 153-156, 159-166, 169-172, 175-177, 180-182, 185-211, 214-230, 233-235, 238-263
src\gui\controllers\bot_controller.py                                   39     30    23%   18-21, 25-33, 37-40, 47-60, 64-72
src\gui\controllers\command_registry.py                                 38     11    71%   44, 48-50, 63-65, 68, 71-72, 75
src\gui\controllers\navigation_controller.py                           152    123    19%   36-37, 41-57, 61-78, 81-95, 98-101, 104-107, 110-113, 116-119, 122-125, 128-131, 134-137, 140-143, 146-149, 152-155, 159-165, 169-173, 177-182, 194-230, 234-253, 257-259, 263-264, 268-269, 273-306, 310-311
src\gui\controllers\search_controller.py                               196    179     9%   11-12, 16-42, 46-48, 52-68, 72-82, 86-95, 99-108, 112-121, 125-139, 143-187, 191-234, 238-280, 284-303
src\gui\controllers\service_controller.py                              199    174    13%   29-41, 49-64, 72-125, 132-160, 164-322, 334-337, 354-362, 375-414, 427-441, 445, 449-458
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  57     45    21%   25-29, 32-112, 115-117
src\gui\dialogs\bug_report_dialog.py                                   229    207    10%   51-55, 58-67, 74-79, 82-223, 227-235, 238-268, 271-297, 301-307, 311-456, 460-477
src\gui\dialogs\command_palette.py                                     301    272    10%   41-70, 74-185, 189-215, 218-226, 229-233, 236-241, 244-251, 254-289, 293-302, 305-312, 315-321, 324-330, 334-338, 342-354, 358-369, 372-379, 382-386, 389-433, 436-472, 476-492, 495-512
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-76, 79-87, 90-98, 103-104, 108-109, 113-114, 118-119
src\gui\dialogs\quick_actions_config.py                                 80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-65, 70, 82-88, 92-95, 99, 102, 105, 108-133, 136-138, 141-144, 148-227
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     55    25%   18-23, 27-33, 37-49, 53-64, 69-78, 82-330
src\gui\main_window\components\status_bar.py                           157    140    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-277
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-43
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 29-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            279    204    27%   47-96, 100-134, 146-149, 152-176, 179-185, 189, 192, 195, 198, 201, 204, 207, 210, 214-239, 242, 245-264, 267-271, 279-283, 291-295, 301-305, 311-313, 316-318, 321-323, 326-328, 331-333, 336-340, 343-354, 357-359, 362-378, 381-384, 387-390, 393-397, 400-402, 405-408, 411, 414, 417-418, 423, 427, 431, 435, 439, 443
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          129    104    19%   29-32, 41-43, 46, 49, 52-76, 80-98, 102-112, 116-123, 127-131, 135-143, 147-149, 152-154, 157-162, 165-169, 173-185, 188-190
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 198    142    28%   52-56, 60-77, 89-93, 97-99, 124-132, 136-180, 187, 191-202, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-311, 321-323, 327-340, 344, 348-363, 370-373, 377-382, 386-389
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-105, 109-117, 121-122, 126-180
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-61, 68-76, 79-82, 86-90, 93-154, 157-211, 214-276, 279-318, 321-367
src\gui\panels\contabilita_kpi\kpi_panel.py                            150    131    13%   35-41, 44-162, 175-179, 182-195, 198-208, 211, 214-297
src\gui\panels\contabilita_panel.py                                    246    210    15%   39-46, 50-56, 60-160, 164-171, 175, 179, 202-219, 223-244, 249-274, 278-280, 284-287, 291-312, 316-332, 335-336, 339-343, 346-361, 364-366, 369-386, 390, 393-412
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-127, 131-133, 137-147, 151-166, 171-186, 191-209, 213-224, 228-234, 238-253, 257-279, 283-289
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-90, 93-95, 99, 102-114, 117-127, 130-132, 136-142, 145-221, 225-231
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     368    330    10%   55-86, 89-219, 223-257, 261-274, 277-305, 308-350, 354-362, 366-380, 383-392, 396-427, 430-462, 465-505, 508-548, 551, 555-638, 641-646, 652-681
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         53     46    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    152    127    16%   24-50, 55-98, 107-193, 198-209, 214-236, 241-298
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         289    257    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-523, 527-555, 559-564, 568-571
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-32, 36-47, 51-54
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-122, 125-130, 133-140, 143-144, 147-148, 151-153, 156-161, 164-166, 169-178, 181-182, 185-188, 191-193, 197, 200-212
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 45-46, 49-57
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-310, 314-315, 319-337, 341-373, 377-379, 383-402, 406-445
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-46, 50-63, 67-68
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-147, 151-205, 208-214, 218-247, 251-263, 267-299, 303-341, 345-347, 351-352, 356-363, 367-373, 377-395, 399-471, 475-479, 483-494, 498-522, 526-567
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-183
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-274, 277-285, 288-291, 294-307, 310-315, 319, 322-324, 328-336, 341-347, 350-384, 388-400, 404-426, 430-444, 448-455, 459-489, 493-495, 499, 503-517, 521-523
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-79, 83-85, 89, 93-106, 110-118, 122-124, 128-133, 147-149, 155-211
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                247    217    12%   42-105, 108-167, 171-179, 183-282, 285-296, 299, 302, 305-309, 312-318, 322-340, 344-402, 405-410, 413-433, 437-457
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-62, 70-110, 114-129, 133-134
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         66     50    24%   25-28, 33, 40-50, 54-91, 96-117, 122
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       134    117    13%   28-179, 183, 187-189, 198-206, 209-257, 262, 267-313
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      108     85    21%   39-43, 46-108, 118-125, 129, 148-150, 154-162, 167, 171-173, 177-179, 189-194, 198, 202-203
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            205    172    16%   53-55, 59-129, 132, 135-150, 154-168, 171-182, 185-191, 194-199, 202-220, 223-226, 230-236, 239-242, 245-248, 251-254, 257-260, 263-267, 270-281, 284-289
src\gui\widgets\contabilita\certificati_tab.py                         557    505     9%   43-45, 48-237, 241-267, 271-341, 345-458, 503-508, 512-516, 520-524, 532-697, 701-702, 706-715, 720-724, 728-732, 736, 740-875, 884-906, 912-949, 954-965, 969-977, 981-984, 988-991, 995-1005, 1008-1077, 1081-1083, 1087-1089, 1093-1129, 1136-1141, 1146-1186
src\gui\widgets\contabilita\giornaliere_tab.py                         167    136    19%   47-50, 54-93, 97, 100-127, 130-137, 141, 144-160, 163-179, 183-195, 198-215, 218-234
src\gui\widgets\contabilita\helpers.py                                  32     26    19%   10-30, 33-40, 43-48
src\gui\widgets\contabilita\year_tab.py                                 95     76    20%   25-26, 30-31, 34-51, 73-93, 96-134, 138, 142-163, 167-196, 200, 204
src\gui\widgets\data_table.py                                          106     82    23%   48-52, 55-125, 132-133, 136-161, 164-170, 174-182, 185-187, 191-206, 213
src\gui\widgets\excel_table.py                                         325    287    12%   29-34, 45-57, 61-68, 72-89, 93-113, 116-117, 120-121, 125-136, 140-162, 166-188, 192-209, 213-231, 235-244, 247-252, 255-259, 262-266, 275-277, 280-301, 304-359, 362-365, 368-374, 377-409, 412-415, 418-420, 423, 427-444, 453-463, 467-507, 512-537
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 87     73    16%   24-78, 81-88, 91-96, 99-103, 106-109, 113-119
src\gui\widgets\footer\components.py                                    48     33    31%   16-29, 32, 39-45, 48-55, 62-64, 67-68, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     27    23%   11-31, 34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     52     38    27%   18-50, 53-55, 58-59, 62-66
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        60     35    42%   40-52, 56-58, 62, 66-67, 73-76, 80-83, 87-88, 98-103, 107-146
src\gui\widgets\notification_card.py                                   218    187    14%   86-92, 96-338, 342-352, 356, 360-362, 376-407, 411-427, 431-435, 439-441, 445-446, 450-454, 459-460, 464-499, 503-507, 511-516
src\gui\widgets\notification_group_header.py                            46     36    22%   32-38, 42-123, 127-130, 134-135, 139, 143-144
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                103     78    24%   34-46, 50-62, 66-68, 72-76, 80-99, 131-137, 141-226, 231-232, 236-237, 242-249, 253-254, 263-265, 269, 273, 277
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        74     59    20%   22-30, 234-235, 238-261, 265-306, 311-349, 354
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      243    210    14%   13-18, 25-59, 63-67, 71, 74-75, 78-82, 85-97, 101-109, 121-146, 150-152, 156-158, 162-165, 169-192, 196-214, 217-368, 372, 376, 380, 384-385, 389-390, 396-432
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     189    154    19%   43-68, 71-78, 81-114, 117-130, 133-138, 141-150, 153-154, 157-159, 164-169, 172-185, 190-197, 203-213, 216-229, 232-237, 240-244, 255-271, 274, 277, 282-307
src\gui\widgets\toast.py                                               129     98    24%   58-78, 82-121, 125-148, 151-155, 159-161, 165-166, 169-181, 192-194, 204-230, 235, 240, 245, 250
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     57    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-144, 157-164, 178-181, 194, 208, 222-228
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         54     23    57%   14-15, 24-30, 40-47, 57-58, 65-66, 75-77
src\utils\helpers.py                                                    90     64    29%   22-24, 29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 202, 221, 231-249
src\utils\log_humanizer.py                                              42     30    29%   13-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           56     24    57%   16-26, 45, 49, 54-57, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23997  18682    22%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_ai_sentinel_hardened.py::TestAISentinelHardened::test_document_processor_image_conversion
============================== 1 failed in 7.43s ==============================

```
</details>

---
### `tests/unit/test_ai_sentinel_hardened.py::TestAISentinelHardened::test_document_processor_searchable_check`
**Error:** `FAILED tests/unit/test_ai_sentinel_hardened.py::TestAISentinelHardened::test_document_processor_searchable_check`

**Timestamp:** `2026-02-07T22:08:58.341465`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_ai_sentinel_hardened.py F                                [100%]

================================== FAILURES ===================================
_______ TestAISentinelHardened.test_document_processor_searchable_check _______
tests\unit\test_ai_sentinel_hardened.py:95: in test_document_processor_searchable_check
    assert DocumentProcessor.is_pdf_searchable(dummy_pdf) is True
E   AssertionError: assert False is True
E    +  where False = <function DocumentProcessor.is_pdf_searchable at 0x000001F9A0484860>(WindowsPath('C:/Users/gianc/AppData/Local/Temp/pytest-of-gianc/pytest-6514/test_document_processor_search0/test.pdf'))
E    +    where <function DocumentProcessor.is_pdf_searchable at 0x000001F9A0484860> = DocumentProcessor.is_pdf_searchable
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              260    203    22%   52-72, 87, 92-94, 106-110, 121-137, 141, 145, 149, 153-154, 158-159, 164-180, 184-227, 231-253, 257-259, 266-271, 275-302, 314-363, 367-399, 404-413, 417-421, 425-427, 431, 435-441, 452-464, 468-471
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    138    17%   50-55, 76-81, 100-104, 135-198, 221, 250-304, 324-325, 328-332, 345, 348-352, 374-377, 380-390, 420-436, 466-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     27    43%   52, 56, 60-72, 77-100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          80     55    31%   38, 42, 51-54, 60-67, 71-91, 95-106, 117-135, 139-144
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   39-42, 46, 50-52, 65-90, 101-114, 118-147, 151-158, 182-277, 281-299, 309-335, 339-348, 352-361, 365-376
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-103, 107-128
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         218    190    13%   28-31, 35, 39-41, 53-79, 90-95, 100-105, 109-137, 141-174, 178-186, 195-223, 227-234, 238-258, 262-274, 278-290, 294-312, 316-340, 344-348
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           218    178    18%   57, 61, 73-76, 80-82, 86-99, 103-120, 124-139, 143-165, 169-196, 200-209, 213-238, 242-274, 280-309, 313-322, 326-341, 345-366, 371-381
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     83    20%   27-30, 34, 38-44, 48-65, 69-91, 95-124, 128-145, 149-154, 158-167
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-107
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            70     50    29%   21, 26, 31, 36, 39-43, 47-60, 66-109, 116
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-85, 89-148, 152-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       175    102    42%   91-110, 116-145, 155-166, 176-183, 186-214, 221-257, 260-275, 320, 329, 357-358, 362-376, 383-384
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           387    343    11%   25, 30, 35, 40, 45, 56-60, 64, 68, 72-97, 101-160, 164-168, 172-200, 204-233, 237-245, 249-283, 287-315, 319-332, 336-364, 368-403, 407-421, 425-446, 450-462, 469-507, 510-550, 554-573
src\bots\safework\pdl\search_bot.py                                    179    154    14%   19-20, 24, 28, 32-90, 94-111, 115-132, 136-145, 149-159, 163-168, 172-197, 201-226, 230-300
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82     67    18%   15-17, 29-68, 74-119, 124-143, 148-156
src\core\app_updater.py                                                 46     37    20%   17-47, 52-57, 62-83, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     39    61%   61-63, 78-79, 110-112, 114-117, 119-122, 124-126, 128-132, 144-145, 149-154, 157-163
src\core\audit\integrity.py                                             15      2    87%   21, 26
src\core\audit\manager.py                                              139     70    50%   28, 38, 46, 50, 58-63, 170, 174-177, 183-200, 204-231, 241, 244-247, 255-283
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     62    14%   18, 25-57, 67-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-187, 198-206, 211-222, 227-249
src\core\bug_reporter.py                                               157    126    20%   60-107, 112-143, 148-158, 163-185, 190-210, 215-238, 243-295, 300-312, 321-339
src\core\config_manager.py                                             237    117    51%   35, 87, 109-115, 136, 141-142, 156-170, 179-180, 199-200, 222, 226-229, 247, 252, 257-259, 264, 279, 289-302, 307-317, 326-353, 358-362, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        101     51    50%   29, 34, 39, 48-60, 77-124, 133-140, 149-154, 163-170, 175, 180, 185, 190, 200, 209, 222
src\core\contabilita_queries.py                                         86     61    29%   18-29, 34-47, 52-77, 82-93, 99, 108-109, 114-125
src\core\contabilita_search.py                                          91     43    53%   25-81, 89, 109-110, 117-128, 137-138, 156-157
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          158    103    35%   21, 37-54, 59-69, 75-102, 108-146, 154-191, 199-234, 248, 264, 280, 282
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           120     40    67%   125-134, 141-171, 184-185, 211-213
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          65     48    26%   42-59, 63-77, 81-97, 101-115
src\core\importers\base.py                                              58     36    38%   15-16, 23-25, 35-37, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      135    109    19%   40-57, 68-104, 111-128, 133-187, 192-210, 215-239, 244-247
src\core\importers\giornaliere.py                                      190    155    18%   42-63, 73-91, 101-120, 126-145, 149-187, 191-206, 210-232, 236-288, 292-308
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    133    13%   21-63, 68-69, 74, 79, 84-100, 105-145, 150-190, 195-197, 202-208, 213-233, 238-246, 251-269, 274-283, 287-290
src\core\license_validator.py                                          179    133    26%   36-40, 49-56, 70-74, 94-109, 115-131, 136-143, 157-180, 190-216, 227-228, 237-261, 266-283, 288-336, 341-344, 349-352
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             52     22    58%   29-30, 38-39, 43-44, 52, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             66     33    50%   92, 112, 118, 121, 125, 142-156, 169-175, 193-194, 203-212
src\core\logging\formatters.py                                          82     25    70%   84, 88-90, 122, 125, 130, 132, 134, 136, 138, 168, 206-216, 225, 231-241
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 147-148, 161-165, 169-174, 179-180, 199, 205, 213, 217, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     16    70%   58, 67, 91, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                               99     75    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-205, 217-219, 225-227, 233-235
src\core\logging\viewer.py                                             175    142    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 149, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    110    12%   21-37, 55-69, 73-74, 78-106, 110-141, 150-205, 214-252
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                        95     68    28%   29-35, 38-45, 49-57, 61-74, 78-82, 101-146, 150-152, 156, 160-167, 171-180, 184-187, 191-194
src\core\oda_manager.py                                                 34     20    41%   23, 31-91, 100-115
src\core\report_history.py                                              65     43    34%   25-27, 35-40, 45-49, 60-84, 94, 112-132, 145-155
src\core\schemas.py                                                     77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                                             94     56    40%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 124-126, 131-134, 139-145
src\core\stats_manager.py                                               46     33    28%   23-26, 30, 34-47, 51, 55-66, 70-78, 82
src\core\sync_tracker.py                                                58     23    60%   32-37, 47-48, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    289    16%   29-31, 35-44, 48-66, 70-73, 77-84, 88-95, 98-125, 128-151, 154-159, 163-177, 180-196, 201-204, 207-208, 211-219, 222-230, 233-258, 262-287, 290-294, 297-302, 306-323, 326-334, 337-350, 353-366, 370-375, 379-385, 389-397, 401-427, 431-444, 448-455, 460-466, 469-496, 499-511, 514-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         97     75    23%   26-66, 71-81, 86-91, 96-103, 109-143, 148-156, 161-163
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-133, 136-150, 153-156, 159-166, 169-172, 175-177, 180-182, 185-211, 214-230, 233-235, 238-263
src\gui\controllers\bot_controller.py                                   39     30    23%   18-21, 25-33, 37-40, 47-60, 64-72
src\gui\controllers\command_registry.py                                 38     11    71%   44, 48-50, 63-65, 68, 71-72, 75
src\gui\controllers\navigation_controller.py                           152    123    19%   36-37, 41-57, 61-78, 81-95, 98-101, 104-107, 110-113, 116-119, 122-125, 128-131, 134-137, 140-143, 146-149, 152-155, 159-165, 169-173, 177-182, 194-230, 234-253, 257-259, 263-264, 268-269, 273-306, 310-311
src\gui\controllers\search_controller.py                               196    179     9%   11-12, 16-42, 46-48, 52-68, 72-82, 86-95, 99-108, 112-121, 125-139, 143-187, 191-234, 238-280, 284-303
src\gui\controllers\service_controller.py                              199    174    13%   29-41, 49-64, 72-125, 132-160, 164-322, 334-337, 354-362, 375-414, 427-441, 445, 449-458
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  57     45    21%   25-29, 32-112, 115-117
src\gui\dialogs\bug_report_dialog.py                                   229    207    10%   51-55, 58-67, 74-79, 82-223, 227-235, 238-268, 271-297, 301-307, 311-456, 460-477
src\gui\dialogs\command_palette.py                                     301    272    10%   41-70, 74-185, 189-215, 218-226, 229-233, 236-241, 244-251, 254-289, 293-302, 305-312, 315-321, 324-330, 334-338, 342-354, 358-369, 372-379, 382-386, 389-433, 436-472, 476-492, 495-512
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-76, 79-87, 90-98, 103-104, 108-109, 113-114, 118-119
src\gui\dialogs\quick_actions_config.py                                 80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-65, 70, 82-88, 92-95, 99, 102, 105, 108-133, 136-138, 141-144, 148-227
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     55    25%   18-23, 27-33, 37-49, 53-64, 69-78, 82-330
src\gui\main_window\components\status_bar.py                           157    140    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-277
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-43
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 29-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            279    204    27%   47-96, 100-134, 146-149, 152-176, 179-185, 189, 192, 195, 198, 201, 204, 207, 210, 214-239, 242, 245-264, 267-271, 279-283, 291-295, 301-305, 311-313, 316-318, 321-323, 326-328, 331-333, 336-340, 343-354, 357-359, 362-378, 381-384, 387-390, 393-397, 400-402, 405-408, 411, 414, 417-418, 423, 427, 431, 435, 439, 443
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          129    104    19%   29-32, 41-43, 46, 49, 52-76, 80-98, 102-112, 116-123, 127-131, 135-143, 147-149, 152-154, 157-162, 165-169, 173-185, 188-190
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 198    142    28%   52-56, 60-77, 89-93, 97-99, 124-132, 136-180, 187, 191-202, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-311, 321-323, 327-340, 344, 348-363, 370-373, 377-382, 386-389
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-105, 109-117, 121-122, 126-180
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-61, 68-76, 79-82, 86-90, 93-154, 157-211, 214-276, 279-318, 321-367
src\gui\panels\contabilita_kpi\kpi_panel.py                            150    131    13%   35-41, 44-162, 175-179, 182-195, 198-208, 211, 214-297
src\gui\panels\contabilita_panel.py                                    246    210    15%   39-46, 50-56, 60-160, 164-171, 175, 179, 202-219, 223-244, 249-274, 278-280, 284-287, 291-312, 316-332, 335-336, 339-343, 346-361, 364-366, 369-386, 390, 393-412
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-127, 131-133, 137-147, 151-166, 171-186, 191-209, 213-224, 228-234, 238-253, 257-279, 283-289
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-90, 93-95, 99, 102-114, 117-127, 130-132, 136-142, 145-221, 225-231
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     368    330    10%   55-86, 89-219, 223-257, 261-274, 277-305, 308-350, 354-362, 366-380, 383-392, 396-427, 430-462, 465-505, 508-548, 551, 555-638, 641-646, 652-681
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         53     46    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    152    127    16%   24-50, 55-98, 107-193, 198-209, 214-236, 241-298
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         289    257    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-523, 527-555, 559-564, 568-571
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-32, 36-47, 51-54
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-122, 125-130, 133-140, 143-144, 147-148, 151-153, 156-161, 164-166, 169-178, 181-182, 185-188, 191-193, 197, 200-212
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 45-46, 49-57
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-310, 314-315, 319-337, 341-373, 377-379, 383-402, 406-445
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-46, 50-63, 67-68
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-147, 151-205, 208-214, 218-247, 251-263, 267-299, 303-341, 345-347, 351-352, 356-363, 367-373, 377-395, 399-471, 475-479, 483-494, 498-522, 526-567
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-183
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-274, 277-285, 288-291, 294-307, 310-315, 319, 322-324, 328-336, 341-347, 350-384, 388-400, 404-426, 430-444, 448-455, 459-489, 493-495, 499, 503-517, 521-523
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-79, 83-85, 89, 93-106, 110-118, 122-124, 128-133, 147-149, 155-211
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                247    217    12%   42-105, 108-167, 171-179, 183-282, 285-296, 299, 302, 305-309, 312-318, 322-340, 344-402, 405-410, 413-433, 437-457
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-62, 70-110, 114-129, 133-134
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         66     50    24%   25-28, 33, 40-50, 54-91, 96-117, 122
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       134    117    13%   28-179, 183, 187-189, 198-206, 209-257, 262, 267-313
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      108     85    21%   39-43, 46-108, 118-125, 129, 148-150, 154-162, 167, 171-173, 177-179, 189-194, 198, 202-203
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            205    172    16%   53-55, 59-129, 132, 135-150, 154-168, 171-182, 185-191, 194-199, 202-220, 223-226, 230-236, 239-242, 245-248, 251-254, 257-260, 263-267, 270-281, 284-289
src\gui\widgets\contabilita\certificati_tab.py                         557    505     9%   43-45, 48-237, 241-267, 271-341, 345-458, 503-508, 512-516, 520-524, 532-697, 701-702, 706-715, 720-724, 728-732, 736, 740-875, 884-906, 912-949, 954-965, 969-977, 981-984, 988-991, 995-1005, 1008-1077, 1081-1083, 1087-1089, 1093-1129, 1136-1141, 1146-1186
src\gui\widgets\contabilita\giornaliere_tab.py                         167    136    19%   47-50, 54-93, 97, 100-127, 130-137, 141, 144-160, 163-179, 183-195, 198-215, 218-234
src\gui\widgets\contabilita\helpers.py                                  32     26    19%   10-30, 33-40, 43-48
src\gui\widgets\contabilita\year_tab.py                                 95     76    20%   25-26, 30-31, 34-51, 73-93, 96-134, 138, 142-163, 167-196, 200, 204
src\gui\widgets\data_table.py                                          106     82    23%   48-52, 55-125, 132-133, 136-161, 164-170, 174-182, 185-187, 191-206, 213
src\gui\widgets\excel_table.py                                         325    287    12%   29-34, 45-57, 61-68, 72-89, 93-113, 116-117, 120-121, 125-136, 140-162, 166-188, 192-209, 213-231, 235-244, 247-252, 255-259, 262-266, 275-277, 280-301, 304-359, 362-365, 368-374, 377-409, 412-415, 418-420, 423, 427-444, 453-463, 467-507, 512-537
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 87     73    16%   24-78, 81-88, 91-96, 99-103, 106-109, 113-119
src\gui\widgets\footer\components.py                                    48     33    31%   16-29, 32, 39-45, 48-55, 62-64, 67-68, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     27    23%   11-31, 34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     52     38    27%   18-50, 53-55, 58-59, 62-66
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        60     35    42%   40-52, 56-58, 62, 66-67, 73-76, 80-83, 87-88, 98-103, 107-146
src\gui\widgets\notification_card.py                                   218    187    14%   86-92, 96-338, 342-352, 356, 360-362, 376-407, 411-427, 431-435, 439-441, 445-446, 450-454, 459-460, 464-499, 503-507, 511-516
src\gui\widgets\notification_group_header.py                            46     36    22%   32-38, 42-123, 127-130, 134-135, 139, 143-144
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                103     78    24%   34-46, 50-62, 66-68, 72-76, 80-99, 131-137, 141-226, 231-232, 236-237, 242-249, 253-254, 263-265, 269, 273, 277
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        74     59    20%   22-30, 234-235, 238-261, 265-306, 311-349, 354
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      243    210    14%   13-18, 25-59, 63-67, 71, 74-75, 78-82, 85-97, 101-109, 121-146, 150-152, 156-158, 162-165, 169-192, 196-214, 217-368, 372, 376, 380, 384-385, 389-390, 396-432
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     189    154    19%   43-68, 71-78, 81-114, 117-130, 133-138, 141-150, 153-154, 157-159, 164-169, 172-185, 190-197, 203-213, 216-229, 232-237, 240-244, 255-271, 274, 277, 282-307
src\gui\widgets\toast.py                                               129     98    24%   58-78, 82-121, 125-148, 151-155, 159-161, 165-166, 169-181, 192-194, 204-230, 235, 240, 245, 250
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     57    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-144, 157-164, 178-181, 194, 208, 222-228
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         54     18    67%   14-15, 24-30, 46-47, 57-58, 65-66, 75-77
src\utils\helpers.py                                                    90     64    29%   22-24, 29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 202, 221, 231-249
src\utils\log_humanizer.py                                              42     30    29%   13-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           56     24    57%   16-26, 45, 49, 54-57, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23997  18677    22%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_ai_sentinel_hardened.py::TestAISentinelHardened::test_document_processor_searchable_check
============================== 1 failed in 7.23s ==============================

```
</details>

---
### `tests/unit/test_auth_monitor_robust.py::TestAuthMonitorRobust::test_build_access_maps_formats`
**Error:** `FAILED tests/unit/test_auth_monitor_robust.py::TestAuthMonitorRobust::test_build_access_maps_formats`

**Timestamp:** `2026-02-07T22:12:11.374158`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_auth_monitor_robust.py F                                 [100%]

================================== FAILURES ===================================
____________ TestAuthMonitorRobust.test_build_access_maps_formats _____________
tests\unit\test_auth_monitor_robust.py:31: in test_build_access_maps_formats
    last_by_cf, _last_by_name = _build_access_maps(raw)
                                ^^^^^^^^^^^^^^^^^^^^^^^
src\core\auth_monitor.py:42: in _build_access_maps
    delta = (today - last_date).days
             ^^^^^^^^^^^^^^^^^
E   TypeError: can't subtract offset-naive and offset-aware datetimes
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              260    203    22%   52-72, 87, 92-94, 106-110, 121-137, 141, 145, 149, 153-154, 158-159, 164-180, 184-227, 231-253, 257-259, 266-271, 275-302, 314-363, 367-399, 404-413, 417-421, 425-427, 431, 435-441, 452-464, 468-471
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    138    17%   50-55, 76-81, 100-104, 135-198, 221, 250-304, 324-325, 328-332, 345, 348-352, 374-377, 380-390, 420-436, 466-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     27    43%   52, 56, 60-72, 77-100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          80     55    31%   38, 42, 51-54, 60-67, 71-91, 95-106, 117-135, 139-144
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   39-42, 46, 50-52, 65-90, 101-114, 118-147, 151-158, 182-277, 281-299, 309-335, 339-348, 352-361, 365-376
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-103, 107-128
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         218    190    13%   28-31, 35, 39-41, 53-79, 90-95, 100-105, 109-137, 141-174, 178-186, 195-223, 227-234, 238-258, 262-274, 278-290, 294-312, 316-340, 344-348
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           218    178    18%   57, 61, 73-76, 80-82, 86-99, 103-120, 124-139, 143-165, 169-196, 200-209, 213-238, 242-274, 280-309, 313-322, 326-341, 345-366, 371-381
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     83    20%   27-30, 34, 38-44, 48-65, 69-91, 95-124, 128-145, 149-154, 158-167
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-107
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            70     50    29%   21, 26, 31, 36, 39-43, 47-60, 66-109, 116
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-85, 89-148, 152-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       175    102    42%   91-110, 116-145, 155-166, 176-183, 186-214, 221-257, 260-275, 320, 329, 357-358, 362-376, 383-384
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           387    343    11%   25, 30, 35, 40, 45, 56-60, 64, 68, 72-97, 101-160, 164-168, 172-200, 204-233, 237-245, 249-283, 287-315, 319-332, 336-364, 368-403, 407-421, 425-446, 450-462, 469-507, 510-550, 554-573
src\bots\safework\pdl\search_bot.py                                    179    154    14%   19-20, 24, 28, 32-90, 94-111, 115-132, 136-145, 149-159, 163-168, 172-197, 201-226, 230-300
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82      0   100%
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-63, 78-79, 110-112, 114-117, 119-122, 124-126, 128-132, 144-145, 149-154, 161-163
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              139     19    86%   28, 50, 62-63, 174-177, 188, 190, 199-200, 214, 230-231, 241, 279, 281-282
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     40    44%   36-37, 40, 43-57, 80-127
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-187, 198-206, 211-222, 227-249
src\core\bug_reporter.py                                               157    126    20%   60-107, 112-143, 148-158, 163-185, 190-210, 215-238, 243-295, 300-312, 321-339
src\core\config_manager.py                                             237    114    52%   35, 87, 109-115, 136, 141-142, 156-170, 179-180, 199-200, 222, 226-229, 247, 252, 264, 279, 289-302, 307-317, 326-353, 358-362, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        101     51    50%   29, 34, 39, 48-60, 77-124, 133-140, 149-154, 163-170, 175, 180, 185, 190, 200, 209, 222
src\core\contabilita_queries.py                                         86     61    29%   18-29, 34-47, 52-77, 82-93, 99, 108-109, 114-125
src\core\contabilita_search.py                                          91     43    53%   25-81, 89, 109-110, 117-128, 137-138, 156-157
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          158    103    35%   21, 37-54, 59-69, 75-102, 108-146, 154-191, 199-234, 248, 264, 280, 282
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           120     40    67%   125-134, 141-171, 184-185, 211-213
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          65     48    26%   42-59, 63-77, 81-97, 101-115
src\core\importers\base.py                                              58     36    38%   15-16, 23-25, 35-37, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      135    109    19%   40-57, 68-104, 111-128, 133-187, 192-210, 215-239, 244-247
src\core\importers\giornaliere.py                                      190    155    18%   42-63, 73-91, 101-120, 126-145, 149-187, 191-206, 210-232, 236-288, 292-308
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    133    13%   21-63, 68-69, 74, 79, 84-100, 105-145, 150-190, 195-197, 202-208, 213-233, 238-246, 251-269, 274-283, 287-290
src\core\license_validator.py                                          179    133    26%   36-40, 49-56, 70-74, 94-109, 115-131, 136-143, 157-180, 190-216, 227-228, 237-261, 266-283, 288-336, 341-344, 349-352
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             52     22    58%   29-30, 38-39, 43-44, 52, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             66     33    50%   92, 112, 118, 121, 125, 142-156, 169-175, 193-194, 203-212
src\core\logging\formatters.py                                          82     24    71%   84, 88-90, 122, 125, 130, 132, 134, 136, 168, 206-216, 225, 231-241
src\core\logging\logger.py                                             109     25    77%   84, 96, 123, 137-139, 147-148, 161-165, 173-174, 179-180, 199, 205, 213, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                               99     75    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-205, 217-219, 225-227, 233-235
src\core\logging\viewer.py                                             175    141    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    110    12%   21-37, 55-69, 73-74, 78-106, 110-141, 150-205, 214-252
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                        95     68    28%   29-35, 38-45, 49-57, 61-74, 78-82, 101-146, 150-152, 156, 160-167, 171-180, 184-187, 191-194
src\core\oda_manager.py                                                 34     20    41%   23, 31-91, 100-115
src\core\report_history.py                                              65     43    34%   25-27, 35-40, 45-49, 60-84, 94, 112-132, 145-155
src\core\schemas.py                                                     77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                                             94     56    40%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 124-126, 131-134, 139-145
src\core\stats_manager.py                                               46     33    28%   23-26, 30, 34-47, 51, 55-66, 70-78, 82
src\core\sync_tracker.py                                                58     23    60%   32-37, 47-48, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    289    16%   29-31, 35-44, 48-66, 70-73, 77-84, 88-95, 98-125, 128-151, 154-159, 163-177, 180-196, 201-204, 207-208, 211-219, 222-230, 233-258, 262-287, 290-294, 297-302, 306-323, 326-334, 337-350, 353-366, 370-375, 379-385, 389-397, 401-427, 431-444, 448-455, 460-466, 469-496, 499-511, 514-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         97     75    23%   26-66, 71-81, 86-91, 96-103, 109-143, 148-156, 161-163
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-133, 136-150, 153-156, 159-166, 169-172, 175-177, 180-182, 185-211, 214-230, 233-235, 238-263
src\gui\controllers\bot_controller.py                                   39     30    23%   18-21, 25-33, 37-40, 47-60, 64-72
src\gui\controllers\command_registry.py                                 38     11    71%   44, 48-50, 63-65, 68, 71-72, 75
src\gui\controllers\navigation_controller.py                           152    123    19%   36-37, 41-57, 61-78, 81-95, 98-101, 104-107, 110-113, 116-119, 122-125, 128-131, 134-137, 140-143, 146-149, 152-155, 159-165, 169-173, 177-182, 194-230, 234-253, 257-259, 263-264, 268-269, 273-306, 310-311
src\gui\controllers\search_controller.py                               196    179     9%   11-12, 16-42, 46-48, 52-68, 72-82, 86-95, 99-108, 112-121, 125-139, 143-187, 191-234, 238-280, 284-303
src\gui\controllers\service_controller.py                              199    174    13%   29-41, 49-64, 72-125, 132-160, 164-322, 334-337, 354-362, 375-414, 427-441, 445, 449-458
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  57     45    21%   25-29, 32-112, 115-117
src\gui\dialogs\bug_report_dialog.py                                   229    207    10%   51-55, 58-67, 74-79, 82-223, 227-235, 238-268, 271-297, 301-307, 311-456, 460-477
src\gui\dialogs\command_palette.py                                     301    272    10%   41-70, 74-185, 189-215, 218-226, 229-233, 236-241, 244-251, 254-289, 293-302, 305-312, 315-321, 324-330, 334-338, 342-354, 358-369, 372-379, 382-386, 389-433, 436-472, 476-492, 495-512
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-76, 79-87, 90-98, 103-104, 108-109, 113-114, 118-119
src\gui\dialogs\quick_actions_config.py                                 80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-65, 70, 82-88, 92-95, 99, 102, 105, 108-133, 136-138, 141-144, 148-227
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     55    25%   18-23, 27-33, 37-49, 53-64, 69-78, 82-330
src\gui\main_window\components\status_bar.py                           157    140    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-277
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-43
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 29-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            279    204    27%   47-96, 100-134, 146-149, 152-176, 179-185, 189, 192, 195, 198, 201, 204, 207, 210, 214-239, 242, 245-264, 267-271, 279-283, 291-295, 301-305, 311-313, 316-318, 321-323, 326-328, 331-333, 336-340, 343-354, 357-359, 362-378, 381-384, 387-390, 393-397, 400-402, 405-408, 411, 414, 417-418, 423, 427, 431, 435, 439, 443
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          129     23    82%   53, 98, 111-112, 122, 128, 130, 140-142, 161-162, 167-169, 177, 179, 181, 184-185, 188-190
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 198    142    28%   52-56, 60-77, 89-93, 97-99, 124-132, 136-180, 187, 191-202, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-311, 321-323, 327-340, 344, 348-363, 370-373, 377-382, 386-389
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-105, 109-117, 121-122, 126-180
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-61, 68-76, 79-82, 86-90, 93-154, 157-211, 214-276, 279-318, 321-367
src\gui\panels\contabilita_kpi\kpi_panel.py                            150    131    13%   35-41, 44-162, 175-179, 182-195, 198-208, 211, 214-297
src\gui\panels\contabilita_panel.py                                    246    210    15%   39-46, 50-56, 60-160, 164-171, 175, 179, 202-219, 223-244, 249-274, 278-280, 284-287, 291-312, 316-332, 335-336, 339-343, 346-361, 364-366, 369-386, 390, 393-412
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-127, 131-133, 137-147, 151-166, 171-186, 191-209, 213-224, 228-234, 238-253, 257-279, 283-289
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-90, 93-95, 99, 102-114, 117-127, 130-132, 136-142, 145-221, 225-231
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     368    330    10%   55-86, 89-219, 223-257, 261-274, 277-305, 308-350, 354-362, 366-380, 383-392, 396-427, 430-462, 465-505, 508-548, 551, 555-638, 641-646, 652-681
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         53     46    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    152    127    16%   24-50, 55-98, 107-193, 198-209, 214-236, 241-298
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         289    257    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-523, 527-555, 559-564, 568-571
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-32, 36-47, 51-54
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-122, 125-130, 133-140, 143-144, 147-148, 151-153, 156-161, 164-166, 169-178, 181-182, 185-188, 191-193, 197, 200-212
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 45-46, 49-57
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-310, 314-315, 319-337, 341-373, 377-379, 383-402, 406-445
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-46, 50-63, 67-68
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-147, 151-205, 208-214, 218-247, 251-263, 267-299, 303-341, 345-347, 351-352, 356-363, 367-373, 377-395, 399-471, 475-479, 483-494, 498-522, 526-567
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-183
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-274, 277-285, 288-291, 294-307, 310-315, 319, 322-324, 328-336, 341-347, 350-384, 388-400, 404-426, 430-444, 448-455, 459-489, 493-495, 499, 503-517, 521-523
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-79, 83-85, 89, 93-106, 110-118, 122-124, 128-133, 147-149, 155-211
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                247    217    12%   42-105, 108-167, 171-179, 183-282, 285-296, 299, 302, 305-309, 312-318, 322-340, 344-402, 405-410, 413-433, 437-457
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-62, 70-110, 114-129, 133-134
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         66     50    24%   25-28, 33, 40-50, 54-91, 96-117, 122
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       134    117    13%   28-179, 183, 187-189, 198-206, 209-257, 262, 267-313
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     14    82%   94-103, 114-115, 127, 129, 131
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   38, 46-47
src\gui\widgets\audit_log_widget.py                                    102     16    84%   125-135, 138, 141-142, 146, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      108     85    21%   39-43, 46-108, 118-125, 129, 148-150, 154-162, 167, 171-173, 177-179, 189-194, 198, 202-203
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            205    172    16%   53-55, 59-129, 132, 135-150, 154-168, 171-182, 185-191, 194-199, 202-220, 223-226, 230-236, 239-242, 245-248, 251-254, 257-260, 263-267, 270-281, 284-289
src\gui\widgets\contabilita\certificati_tab.py                         557    505     9%   43-45, 48-237, 241-267, 271-341, 345-458, 503-508, 512-516, 520-524, 532-697, 701-702, 706-715, 720-724, 728-732, 736, 740-875, 884-906, 912-949, 954-965, 969-977, 981-984, 988-991, 995-1005, 1008-1077, 1081-1083, 1087-1089, 1093-1129, 1136-1141, 1146-1186
src\gui\widgets\contabilita\giornaliere_tab.py                         167    136    19%   47-50, 54-93, 97, 100-127, 130-137, 141, 144-160, 163-179, 183-195, 198-215, 218-234
src\gui\widgets\contabilita\helpers.py                                  32     26    19%   10-30, 33-40, 43-48
src\gui\widgets\contabilita\year_tab.py                                 95     76    20%   25-26, 30-31, 34-51, 73-93, 96-134, 138, 142-163, 167-196, 200, 204
src\gui\widgets\data_table.py                                          106     82    23%   48-52, 55-125, 132-133, 136-161, 164-170, 174-182, 185-187, 191-206, 213
src\gui\widgets\excel_table.py                                         325    287    12%   29-34, 45-57, 61-68, 72-89, 93-113, 116-117, 120-121, 125-136, 140-162, 166-188, 192-209, 213-231, 235-244, 247-252, 255-259, 262-266, 275-277, 280-301, 304-359, 362-365, 368-374, 377-409, 412-415, 418-420, 423, 427-444, 453-463, 467-507, 512-537
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 87     73    16%   24-78, 81-88, 91-96, 99-103, 106-109, 113-119
src\gui\widgets\footer\components.py                                    48     33    31%   16-29, 32, 39-45, 48-55, 62-64, 67-68, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     27    23%   11-31, 34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     52     38    27%   18-50, 53-55, 58-59, 62-66
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        60     35    42%   40-52, 56-58, 62, 66-67, 73-76, 80-83, 87-88, 98-103, 107-146
src\gui\widgets\notification_card.py                                   218    187    14%   86-92, 96-338, 342-352, 356, 360-362, 376-407, 411-427, 431-435, 439-441, 445-446, 450-454, 459-460, 464-499, 503-507, 511-516
src\gui\widgets\notification_group_header.py                            46     36    22%   32-38, 42-123, 127-130, 134-135, 139, 143-144
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                103     78    24%   34-46, 50-62, 66-68, 72-76, 80-99, 131-137, 141-226, 231-232, 236-237, 242-249, 253-254, 263-265, 269, 273, 277
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        74     59    20%   22-30, 234-235, 238-261, 265-306, 311-349, 354
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      243    210    14%   13-18, 25-59, 63-67, 71, 74-75, 78-82, 85-97, 101-109, 121-146, 150-152, 156-158, 162-165, 169-192, 196-214, 217-368, 372, 376, 380, 384-385, 389-390, 396-432
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     189    154    19%   43-68, 71-78, 81-114, 117-130, 133-138, 141-150, 153-154, 157-159, 164-169, 172-185, 190-197, 203-213, 216-229, 232-237, 240-244, 255-271, 274, 277, 282-307
src\gui\widgets\toast.py                                               129     98    24%   58-78, 82-121, 125-148, 151-155, 159-161, 165-166, 169-181, 192-194, 204-230, 235, 240, 245, 250
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     57    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-144, 157-164, 178-181, 194, 208, 222-228
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         54     18    67%   14-15, 24-30, 46-47, 57-58, 65-66, 75-77
src\utils\helpers.py                                                    90     54    40%   29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 202, 221, 232, 238-241
src\utils\log_humanizer.py                                              42     30    29%   13-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23997  18201    24%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_auth_monitor_robust.py::TestAuthMonitorRobust::test_build_access_maps_formats
============================== 1 failed in 7.56s ==============================

```
</details>

---
### `tests/unit/test_backup_manager.py::TestBackupManager::test_detect_cloud_paths_onedrive_env`
**Error:** `Unknown Error`

**Timestamp:** `2026-02-07T22:13:48.625558`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_backup_manager.py E                                      [100%]

=================================== ERRORS ====================================
__ ERROR at setup of TestBackupManager.test_detect_cloud_paths_onedrive_env ___
C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_backup_manager.py:22: in mock_fs
    fs.create_dir(CONFIG_DIR, parents=True)
E   TypeError: FakeFilesystem.create_dir() got an unexpected keyword argument 'parents'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              260    203    22%   52-72, 87, 92-94, 106-110, 121-137, 141, 145, 149, 153-154, 158-159, 164-180, 184-227, 231-253, 257-259, 266-271, 275-302, 314-363, 367-399, 404-413, 417-421, 425-427, 431, 435-441, 452-464, 468-471
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    138    17%   50-55, 76-81, 100-104, 135-198, 221, 250-304, 324-325, 328-332, 345, 348-352, 374-377, 380-390, 420-436, 466-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     27    43%   52, 56, 60-72, 77-100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          80     55    31%   38, 42, 51-54, 60-67, 71-91, 95-106, 117-135, 139-144
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   39-42, 46, 50-52, 65-90, 101-114, 118-147, 151-158, 182-277, 281-299, 309-335, 339-348, 352-361, 365-376
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-103, 107-128
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         218    190    13%   28-31, 35, 39-41, 53-79, 90-95, 100-105, 109-137, 141-174, 178-186, 195-223, 227-234, 238-258, 262-274, 278-290, 294-312, 316-340, 344-348
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           218    178    18%   57, 61, 73-76, 80-82, 86-99, 103-120, 124-139, 143-165, 169-196, 200-209, 213-238, 242-274, 280-309, 313-322, 326-341, 345-366, 371-381
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     83    20%   27-30, 34, 38-44, 48-65, 69-91, 95-124, 128-145, 149-154, 158-167
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-107
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            70     50    29%   21, 26, 31, 36, 39-43, 47-60, 66-109, 116
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-85, 89-148, 152-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       175    102    42%   91-110, 116-145, 155-166, 176-183, 186-214, 221-257, 260-275, 320, 329, 357-358, 362-376, 383-384
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           387    343    11%   25, 30, 35, 40, 45, 56-60, 64, 68, 72-97, 101-160, 164-168, 172-200, 204-233, 237-245, 249-283, 287-315, 319-332, 336-364, 368-403, 407-421, 425-446, 450-462, 469-507, 510-550, 554-573
src\bots\safework\pdl\search_bot.py                                    179    154    14%   19-20, 24, 28, 32-90, 94-111, 115-132, 136-145, 149-159, 163-168, 172-197, 201-226, 230-300
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82      0   100%
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-63, 78-79, 110-112, 114-117, 119-122, 124-126, 128-132, 144-145, 149-154, 161-163
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              139     18    87%   50, 62-63, 174-177, 188, 190, 199-200, 214, 230-231, 241, 279, 281-282
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      0   100%
src\core\backup_manager.py                                             137     44    68%   59-61, 68, 72, 85, 94-96, 101-129, 174-187, 211-222, 230, 248-249
src\core\bug_reporter.py                                               157    126    20%   60-107, 112-143, 148-158, 163-185, 190-210, 215-238, 243-295, 300-312, 321-339
src\core\config_manager.py                                             237    114    52%   35, 87, 109-115, 136, 141-142, 156-170, 179-180, 199-200, 222, 226-229, 247, 252, 264, 279, 289-302, 307-317, 326-353, 358-362, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        101     51    50%   29, 34, 39, 48-60, 77-124, 133-140, 149-154, 163-170, 175, 180, 185, 190, 200, 209, 222
src\core\contabilita_queries.py                                         86     61    29%   18-29, 34-47, 52-77, 82-93, 99, 108-109, 114-125
src\core\contabilita_search.py                                          91     43    53%   25-81, 89, 109-110, 117-128, 137-138, 156-157
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          158    103    35%   21, 37-54, 59-69, 75-102, 108-146, 154-191, 199-234, 248, 264, 280, 282
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           120     40    67%   125-134, 141-171, 184-185, 211-213
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          65     48    26%   42-59, 63-77, 81-97, 101-115
src\core\importers\base.py                                              58     36    38%   15-16, 23-25, 35-37, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      135    109    19%   40-57, 68-104, 111-128, 133-187, 192-210, 215-239, 244-247
src\core\importers\giornaliere.py                                      190    155    18%   42-63, 73-91, 101-120, 126-145, 149-187, 191-206, 210-232, 236-288, 292-308
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    133    13%   21-63, 68-69, 74, 79, 84-100, 105-145, 150-190, 195-197, 202-208, 213-233, 238-246, 251-269, 274-283, 287-290
src\core\license_validator.py                                          179    133    26%   36-40, 49-56, 70-74, 94-109, 115-131, 136-143, 157-180, 190-216, 227-228, 237-261, 266-283, 288-336, 341-344, 349-352
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             52     22    58%   29-30, 38-39, 43-44, 52, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             66     33    50%   92, 112, 118, 121, 125, 142-156, 169-175, 193-194, 203-212
src\core\logging\formatters.py                                          82     24    71%   84, 88-90, 122, 125, 130, 132, 134, 136, 168, 206-216, 225, 231-241
src\core\logging\logger.py                                             109     25    77%   84, 96, 123, 137-139, 147-148, 161-165, 173-174, 179-180, 199, 205, 213, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                               99     75    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-205, 217-219, 225-227, 233-235
src\core\logging\viewer.py                                             175    141    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    110    12%   21-37, 55-69, 73-74, 78-106, 110-141, 150-205, 214-252
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                        95     68    28%   29-35, 38-45, 49-57, 61-74, 78-82, 101-146, 150-152, 156, 160-167, 171-180, 184-187, 191-194
src\core\oda_manager.py                                                 34     20    41%   23, 31-91, 100-115
src\core\report_history.py                                              65     43    34%   25-27, 35-40, 45-49, 60-84, 94, 112-132, 145-155
src\core\schemas.py                                                     77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                                             94     56    40%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 124-126, 131-134, 139-145
src\core\stats_manager.py                                               46     33    28%   23-26, 30, 34-47, 51, 55-66, 70-78, 82
src\core\sync_tracker.py                                                58     23    60%   32-37, 47-48, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    289    16%   29-31, 35-44, 48-66, 70-73, 77-84, 88-95, 98-125, 128-151, 154-159, 163-177, 180-196, 201-204, 207-208, 211-219, 222-230, 233-258, 262-287, 290-294, 297-302, 306-323, 326-334, 337-350, 353-366, 370-375, 379-385, 389-397, 401-427, 431-444, 448-455, 460-466, 469-496, 499-511, 514-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         97     75    23%   26-66, 71-81, 86-91, 96-103, 109-143, 148-156, 161-163
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-133, 136-150, 153-156, 159-166, 169-172, 175-177, 180-182, 185-211, 214-230, 233-235, 238-263
src\gui\controllers\bot_controller.py                                   39     30    23%   18-21, 25-33, 37-40, 47-60, 64-72
src\gui\controllers\command_registry.py                                 38     11    71%   44, 48-50, 63-65, 68, 71-72, 75
src\gui\controllers\navigation_controller.py                           152    123    19%   36-37, 41-57, 61-78, 81-95, 98-101, 104-107, 110-113, 116-119, 122-125, 128-131, 134-137, 140-143, 146-149, 152-155, 159-165, 169-173, 177-182, 194-230, 234-253, 257-259, 263-264, 268-269, 273-306, 310-311
src\gui\controllers\search_controller.py                               196    179     9%   11-12, 16-42, 46-48, 52-68, 72-82, 86-95, 99-108, 112-121, 125-139, 143-187, 191-234, 238-280, 284-303
src\gui\controllers\service_controller.py                              199    174    13%   29-41, 49-64, 72-125, 132-160, 164-322, 334-337, 354-362, 375-414, 427-441, 445, 449-458
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  57     45    21%   25-29, 32-112, 115-117
src\gui\dialogs\bug_report_dialog.py                                   229    207    10%   51-55, 58-67, 74-79, 82-223, 227-235, 238-268, 271-297, 301-307, 311-456, 460-477
src\gui\dialogs\command_palette.py                                     301    272    10%   41-70, 74-185, 189-215, 218-226, 229-233, 236-241, 244-251, 254-289, 293-302, 305-312, 315-321, 324-330, 334-338, 342-354, 358-369, 372-379, 382-386, 389-433, 436-472, 476-492, 495-512
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-76, 79-87, 90-98, 103-104, 108-109, 113-114, 118-119
src\gui\dialogs\quick_actions_config.py                                 80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-65, 70, 82-88, 92-95, 99, 102, 105, 108-133, 136-138, 141-144, 148-227
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     55    25%   18-23, 27-33, 37-49, 53-64, 69-78, 82-330
src\gui\main_window\components\status_bar.py                           157    140    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-277
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-43
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 29-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            279    204    27%   47-96, 100-134, 146-149, 152-176, 179-185, 189, 192, 195, 198, 201, 204, 207, 210, 214-239, 242, 245-264, 267-271, 279-283, 291-295, 301-305, 311-313, 316-318, 321-323, 326-328, 331-333, 336-340, 343-354, 357-359, 362-378, 381-384, 387-390, 393-397, 400-402, 405-408, 411, 414, 417-418, 423, 427, 431, 435, 439, 443
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          129     23    82%   53, 98, 111-112, 122, 128, 130, 140-142, 161-162, 167-169, 177, 179, 181, 184-185, 188-190
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 198    142    28%   52-56, 60-77, 89-93, 97-99, 124-132, 136-180, 187, 191-202, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-311, 321-323, 327-340, 344, 348-363, 370-373, 377-382, 386-389
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-105, 109-117, 121-122, 126-180
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-61, 68-76, 79-82, 86-90, 93-154, 157-211, 214-276, 279-318, 321-367
src\gui\panels\contabilita_kpi\kpi_panel.py                            150    131    13%   35-41, 44-162, 175-179, 182-195, 198-208, 211, 214-297
src\gui\panels\contabilita_panel.py                                    246    210    15%   39-46, 50-56, 60-160, 164-171, 175, 179, 202-219, 223-244, 249-274, 278-280, 284-287, 291-312, 316-332, 335-336, 339-343, 346-361, 364-366, 369-386, 390, 393-412
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-127, 131-133, 137-147, 151-166, 171-186, 191-209, 213-224, 228-234, 238-253, 257-279, 283-289
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-90, 93-95, 99, 102-114, 117-127, 130-132, 136-142, 145-221, 225-231
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     368    330    10%   55-86, 89-219, 223-257, 261-274, 277-305, 308-350, 354-362, 366-380, 383-392, 396-427, 430-462, 465-505, 508-548, 551, 555-638, 641-646, 652-681
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         53     46    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    152    127    16%   24-50, 55-98, 107-193, 198-209, 214-236, 241-298
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         289    257    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-523, 527-555, 559-564, 568-571
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-32, 36-47, 51-54
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-122, 125-130, 133-140, 143-144, 147-148, 151-153, 156-161, 164-166, 169-178, 181-182, 185-188, 191-193, 197, 200-212
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 45-46, 49-57
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-310, 314-315, 319-337, 341-373, 377-379, 383-402, 406-445
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-46, 50-63, 67-68
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-147, 151-205, 208-214, 218-247, 251-263, 267-299, 303-341, 345-347, 351-352, 356-363, 367-373, 377-395, 399-471, 475-479, 483-494, 498-522, 526-567
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-183
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-274, 277-285, 288-291, 294-307, 310-315, 319, 322-324, 328-336, 341-347, 350-384, 388-400, 404-426, 430-444, 448-455, 459-489, 493-495, 499, 503-517, 521-523
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-79, 83-85, 89, 93-106, 110-118, 122-124, 128-133, 147-149, 155-211
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                247    217    12%   42-105, 108-167, 171-179, 183-282, 285-296, 299, 302, 305-309, 312-318, 322-340, 344-402, 405-410, 413-433, 437-457
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-62, 70-110, 114-129, 133-134
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         66     50    24%   25-28, 33, 40-50, 54-91, 96-117, 122
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       134    117    13%   28-179, 183, 187-189, 198-206, 209-257, 262, 267-313
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     14    82%   94-103, 114-115, 127, 129, 131
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   38, 46-47
src\gui\widgets\audit_log_widget.py                                    102     16    84%   125-135, 138, 141-142, 146, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     10    93%   179, 183-195, 390, 394-406
src\gui\widgets\autopilot\event_card.py                                 67     11    84%   131-146, 162
src\gui\widgets\autopilot\main_widget.py                               197     25    87%   55, 58, 152, 178-179, 181-182, 221-228, 231-234, 241, 257, 275, 301-305
src\gui\widgets\bot_parameters.py                                      108     85    21%   39-43, 46-108, 118-125, 129, 148-150, 154-162, 167, 171-173, 177-179, 189-194, 198, 202-203
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            205    172    16%   53-55, 59-129, 132, 135-150, 154-168, 171-182, 185-191, 194-199, 202-220, 223-226, 230-236, 239-242, 245-248, 251-254, 257-260, 263-267, 270-281, 284-289
src\gui\widgets\contabilita\certificati_tab.py                         557    505     9%   43-45, 48-237, 241-267, 271-341, 345-458, 503-508, 512-516, 520-524, 532-697, 701-702, 706-715, 720-724, 728-732, 736, 740-875, 884-906, 912-949, 954-965, 969-977, 981-984, 988-991, 995-1005, 1008-1077, 1081-1083, 1087-1089, 1093-1129, 1136-1141, 1146-1186
src\gui\widgets\contabilita\giornaliere_tab.py                         167    136    19%   47-50, 54-93, 97, 100-127, 130-137, 141, 144-160, 163-179, 183-195, 198-215, 218-234
src\gui\widgets\contabilita\helpers.py                                  32     26    19%   10-30, 33-40, 43-48
src\gui\widgets\contabilita\year_tab.py                                 95     76    20%   25-26, 30-31, 34-51, 73-93, 96-134, 138, 142-163, 167-196, 200, 204
src\gui\widgets\data_table.py                                          106     82    23%   48-52, 55-125, 132-133, 136-161, 164-170, 174-182, 185-187, 191-206, 213
src\gui\widgets\excel_table.py                                         325    287    12%   29-34, 45-57, 61-68, 72-89, 93-113, 116-117, 120-121, 125-136, 140-162, 166-188, 192-209, 213-231, 235-244, 247-252, 255-259, 262-266, 275-277, 280-301, 304-359, 362-365, 368-374, 377-409, 412-415, 418-420, 423, 427-444, 453-463, 467-507, 512-537
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 87     73    16%   24-78, 81-88, 91-96, 99-103, 106-109, 113-119
src\gui\widgets\footer\components.py                                    48     33    31%   16-29, 32, 39-45, 48-55, 62-64, 67-68, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     27    23%   11-31, 34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     52     38    27%   18-50, 53-55, 58-59, 62-66
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        60     35    42%   40-52, 56-58, 62, 66-67, 73-76, 80-83, 87-88, 98-103, 107-146
src\gui\widgets\notification_card.py                                   218    187    14%   86-92, 96-338, 342-352, 356, 360-362, 376-407, 411-427, 431-435, 439-441, 445-446, 450-454, 459-460, 464-499, 503-507, 511-516
src\gui\widgets\notification_group_header.py                            46     36    22%   32-38, 42-123, 127-130, 134-135, 139, 143-144
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                103     78    24%   34-46, 50-62, 66-68, 72-76, 80-99, 131-137, 141-226, 231-232, 236-237, 242-249, 253-254, 263-265, 269, 273, 277
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        74     59    20%   22-30, 234-235, 238-261, 265-306, 311-349, 354
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      243    210    14%   13-18, 25-59, 63-67, 71, 74-75, 78-82, 85-97, 101-109, 121-146, 150-152, 156-158, 162-165, 169-192, 196-214, 217-368, 372, 376, 380, 384-385, 389-390, 396-432
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     189    154    19%   43-68, 71-78, 81-114, 117-130, 133-138, 141-150, 153-154, 157-159, 164-169, 172-185, 190-197, 203-213, 216-229, 232-237, 240-244, 255-271, 274, 277, 282-307
src\gui\widgets\toast.py                                               129     98    24%   58-78, 82-121, 125-148, 151-155, 159-161, 165-166, 169-181, 192-194, 204-230, 235, 240, 245, 250
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     57    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-144, 157-164, 178-181, 194, 208, 222-228
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         54     18    67%   14-15, 24-30, 46-47, 57-58, 65-66, 75-77
src\utils\helpers.py                                                    90     54    40%   29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 202, 221, 232, 238-241
src\utils\log_humanizer.py                                              42     30    29%   13-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           26     16    38%   50-74
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23997  17782    26%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_backup_manager.py::TestBackupManager::test_detect_cloud_paths_onedrive_env
============================== 1 error in 6.00s ===============================

```
</details>

---
### `tests/unit/test_backup_manager.py::TestBackupManager::test_create_backup_success`
**Error:** `FAILED tests/unit/test_backup_manager.py::TestBackupManager::test_create_backup_success`

**Timestamp:** `2026-02-07T22:15:20.726945`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_backup_manager.py F                                      [100%]

================================== FAILURES ===================================
________________ TestBackupManager.test_create_backup_success _________________
C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_backup_manager.py:104: in test_create_backup_success
    assert success is True
E   assert False is True
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      21     21     0%   6-142
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                260    260     0%   6-474
src\bots\base\login_page.py                               94     94     0%   6-154
src\bots\base\wait_helpers.py                            166    166     0%   14-473
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               82     82     0%   5-156
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit\__init__.py                                 3      0   100%
src\core\audit\database.py                                99     82    17%   18, 22-66, 69, 72-79, 83-90, 102-146, 149-154, 157-163
src\core\audit\integrity.py                               15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-177, 183-200, 204-231, 234-235, 238, 241, 244-247, 255-283
src\core\audit\models.py                                   9      0   100%
src\core\audit\signals.py                                 27     21    22%   13-40
src\core\audit_manager.py                                  5      0   100%
src\core\auth_monitor.py                                  72     72     0%   6-131
src\core\backup_manager.py                               137     36    74%   45, 48, 68, 84, 93, 95, 115, 119, 122, 148-154, 158-172, 178-187, 211-222, 237-249
src\core\bug_reporter.py                                 157    157     0%   11-339
src\core\config_manager.py                               237    194    18%   35, 67, 75-90, 95-117, 122-123, 128-148, 153-170, 179-180, 188-200, 205-206, 211-232, 237-247, 252, 257-259, 264, 269-284, 289-302, 307-317, 326-353, 358-362, 367-369, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                     96     96     0%   6-134
src\core\contabilita_manager.py                          101    101     0%   6-222
src\core\contabilita_queries.py                           86     86     0%   6-125
src\core\contabilita_search.py                            91     91     0%   6-182
src\core\contabilita_stats.py                             59     59     0%   6-99
src\core\contabilita_worker.py                           101    101     0%   1-233
src\core\data_synchronizer.py                            158    158     0%   6-320
src\core\database\__init__.py                              2      2     0%   1-3
src\core\database\manager.py                             120    120     0%   6-216
src\core\employees.py                                     98     98     0%   1-196
src\core\excel_importer.py                                 4      4     0%   6-11
src\core\importers\__init__.py                            44     44     0%   1-106
src\core\importers\attivita.py                            65     65     0%   1-115
src\core\importers\base.py                                58     58     0%   1-86
src\core\importers\certificati.py                        116    116     0%   1-187
src\core\importers\contabilita.py                        135    135     0%   1-247
src\core\importers\giornaliere.py                        190    190     0%   1-308
src\core\importers\scarico_ore.py                        186    186     0%   1-311
src\core\importers\storico_oda.py                         81     81     0%   1-185
src\core\license_updater.py                              153    153     0%   6-290
src\core\license_validator.py                            179    179     0%   6-352
src\core\logging\__init__.py                              10      0   100%
src\core\logging\alert_manager.py                        114     85    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239
src\core\logging\analytics.py                            136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                36      2    94%   70-72
src\core\logging\context.py                               52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                            64     56    12%   44-118, 147-184
src\core\logging\filters.py                               66     48    27%   91-98, 111-129, 142-156, 169-175, 193-194, 203-212
src\core\logging\formatters.py                            82     60    27%   56-108, 118-140, 168, 194-227, 231-241
src\core\logging\logger.py                               109     64    41%   74-96, 100-101, 120-180, 198-201, 205, 209, 213, 217, 221, 232, 249, 293-298
src\core\logging\metadata.py                              86     86     0%   5-199
src\core\logging\metrics.py                               98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              54     41    24%   33-44, 48, 58, 67, 86-108, 121-128, 141-154, 163, 180-182, 201
src\core\logging\sinks.py                                 99     75    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-205, 217-219, 225-227, 233-235
src\core\logging\viewer.py                               175    142    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 149, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                  125    125     0%   6-252
src\core\lyra_sentinel.py                                 29     29     0%   6-50
src\core\notification_manager.py                          95     95     0%   6-194
src\core\oda_manager.py                                   34     34     0%   6-115
src\core\report_history.py                                65     65     0%   7-155
src\core\schemas.py                                       77     77     0%   1-107
src\core\secrets_manager.py                               94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                 46     46     0%   6-82
src\core\sync_tracker.py                                  58     58     0%   1-105
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             174    174     0%   1-313
src\core\telegram_bridge.py                              343    343     0%   1-531
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           97     97     0%   6-163
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                    57     57     0%   1-117
src\gui\dialogs\bug_report_dialog.py                     229    229     0%   10-477
src\gui\dialogs\command_palette.py                       301    301     0%   1-512
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-119
src\gui\dialogs\quick_actions_config.py                   80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                        232    232     0%   6-390
src\gui\formatters.py                                    127    127     0%   1-227
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                73     73     0%   1-330
src\gui\main_window\components\status_bar.py             157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                25     25     0%   1-43
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-52
src\gui\main_window\main.py                              279    279     0%   1-443
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   198    198     0%   6-389
src\gui\panels\carico_ts.py                               90     90     0%   6-180
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 197    197     0%   1-367
src\gui\panels\contabilita_kpi\kpi_panel.py              150    150     0%   1-297
src\gui\panels\contabilita_panel.py                      246    246     0%   6-412
src\gui\panels\dashboard_panel.py                        159    159     0%   1-289
src\gui\panels\dettagli_oda.py                           135    135     0%   6-231
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py               158    158     0%   1-334
src\gui\panels\health_panel.py                           289    289     0%   8-571
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          32     32     0%   1-54
src\gui\panels\lyra\header.py                             36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        146    146     0%   1-212
src\gui\panels\lyra\workers.py                            37     37     0%   1-57
src\gui\panels\notifications_panel.py                    253    253     0%   6-445
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                     45     45     0%   1-68
src\gui\panels\pdl\pdl_filter_widget.py                   67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                          334    334     0%   6-567
src\gui\panels\prenota_bp.py                             105    105     0%   6-183
src\gui\panels\ricerca_pdl.py                             79     79     0%   6-152
src\gui\panels\scarico_ore_panel.py                      299    299     0%   7-520
src\gui\panels\scarico_pdl.py                            296    296     0%   6-523
src\gui\panels\scarico_ts.py                             122    122     0%   6-211
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py             46     46     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py           41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                  247    247     0%   6-457
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       158    158     0%   1-285
src\gui\panels\timbrature_bot.py                         116    116     0%   6-200
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-156
src\gui\styles\theme_manager.py                           66     66     0%   6-122
src\gui\styles\widget_styles.py                           35     35     0%   6-391
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         134    134     0%   1-313
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-180
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                   67     67     0%   1-164
src\gui\widgets\autopilot\main_widget.py                 197    197     0%   6-349
src\gui\widgets\bot_parameters.py                        108    108     0%   6-203
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            106    106     0%   5-213
src\gui\widgets\excel_table.py                           325    325     0%   6-537
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   87     87     0%   1-119
src\gui\widgets\footer\components.py                      48     48     0%   1-87
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                       52     52     0%   1-66
src\gui\widgets\info_widgets.py                           89     89     0%   6-175
src\gui\widgets\message_bubble.py                         53     53     0%   7-127
src\gui\widgets\modern_button.py                          60     60     0%   5-146
src\gui\widgets\notification_card.py                     218    218     0%   6-516
src\gui\widgets\notification_group_header.py              46     46     0%   6-144
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  103    103     0%   6-277
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          74     74     0%   1-354
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        243    243     0%   1-432
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       189    189     0%   6-307
src\gui\widgets\toast.py                                 129    129     0%   5-250
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      2     0%   5-17
src\utils\animation_helpers.py                           100    100     0%   6-295
src\utils\date_utils.py                                   70     70     0%   6-228
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           54     54     0%   6-77
src\utils\helpers.py                                      90     90     0%   6-249
src\utils\log_humanizer.py                                42     42     0%   6-119
src\utils\parsing.py                                      53     53     0%   6-119
src\utils\printing.py                                     83     83     0%   1-141
src\utils\resource_manager.py                             56     56     0%   6-91
src\utils\secure_logger.py                                23     23     0%   5-70
src\utils\security.py                                     79     79     0%   6-142
src\utils\system_telemetry.py                             26     26     0%   6-74
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  16885  16280     4%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_backup_manager.py::TestBackupManager::test_create_backup_success
============================== 1 failed in 4.68s ==============================

```
</details>

---
### `tests/unit/test_backup_manager.py::TestBackupManager::test_restore_backup`
**Error:** `FAILED tests/unit/test_backup_manager.py::TestBackupManager::test_restore_backup`

**Timestamp:** `2026-02-07T22:20:31.621503`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_backup_manager.py F                                      [100%]

================================== FAILURES ===================================
____________________ TestBackupManager.test_restore_backup ____________________
C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_backup_manager.py:157: in test_restore_backup
    with zipfile.ZipFile(str(zip_path), 'w') as z:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\zipfile\__init__.py:1336: in __init__
    self.fp = io.open(file, filemode)
              ^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\site-packages\pyfakefs\fake_io.py:90: in open
    return fake_open(
C:\Program Files\Python312\Lib\site-packages\pyfakefs\fake_open.py:105: in fake_open
    return fake_file_open(
C:\Program Files\Python312\Lib\site-packages\pyfakefs\fake_open.py:136: in __call__
    return self.call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\site-packages\pyfakefs\fake_open.py:244: in call
    file_object = self._init_file_object(
C:\Program Files\Python312\Lib\site-packages\pyfakefs\fake_open.py:357: in _init_file_object
    file_object = self.filesystem.create_file_internally(
C:\Program Files\Python312\Lib\site-packages\pyfakefs\fake_filesystem.py:2601: in create_file_internally
    self.raise_os_error(errno.ENOENT, parent_directory)
C:\Program Files\Python312\Lib\site-packages\pyfakefs\fake_filesystem.py:494: in raise_os_error
    raise OSError(err_no, message, filename)
E   FileNotFoundError: [Errno 2] No such file or directory: 'C:\\tmp'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      21     21     0%   6-142
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                260    260     0%   6-474
src\bots\base\login_page.py                               94     94     0%   6-154
src\bots\base\wait_helpers.py                            166    166     0%   14-473
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               82     82     0%   5-156
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit\__init__.py                                 3      0   100%
src\core\audit\database.py                                99     82    17%   18, 22-66, 69, 72-79, 83-90, 102-146, 149-154, 157-163
src\core\audit\integrity.py                               15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-177, 183-200, 204-231, 234-235, 238, 241, 244-247, 255-283
src\core\audit\models.py                                   9      0   100%
src\core\audit\signals.py                                 27     21    22%   13-40
src\core\audit_manager.py                                  5      0   100%
src\core\auth_monitor.py                                  72     72     0%   6-131
src\core\backup_manager.py                               138     26    81%   45, 48, 68, 84, 93, 95, 115, 119, 122, 179-188, 213-223, 238-250
src\core\bug_reporter.py                                 157    157     0%   11-339
src\core\config_manager.py                               237    194    18%   35, 67, 75-90, 95-117, 122-123, 128-148, 153-170, 179-180, 188-200, 205-206, 211-232, 237-247, 252, 257-259, 264, 269-284, 289-302, 307-317, 326-353, 358-362, 367-369, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                     96     96     0%   6-134
src\core\contabilita_manager.py                          101    101     0%   6-222
src\core\contabilita_queries.py                           86     86     0%   6-125
src\core\contabilita_search.py                            91     91     0%   6-182
src\core\contabilita_stats.py                             59     59     0%   6-99
src\core\contabilita_worker.py                           101    101     0%   1-233
src\core\data_synchronizer.py                            158    158     0%   6-320
src\core\database\__init__.py                              2      2     0%   1-3
src\core\database\manager.py                             120    120     0%   6-216
src\core\employees.py                                     98     98     0%   1-196
src\core\excel_importer.py                                 4      4     0%   6-11
src\core\importers\__init__.py                            44     44     0%   1-106
src\core\importers\attivita.py                            65     65     0%   1-115
src\core\importers\base.py                                58     58     0%   1-86
src\core\importers\certificati.py                        116    116     0%   1-187
src\core\importers\contabilita.py                        135    135     0%   1-247
src\core\importers\giornaliere.py                        190    190     0%   1-308
src\core\importers\scarico_ore.py                        186    186     0%   1-311
src\core\importers\storico_oda.py                         81     81     0%   1-185
src\core\license_updater.py                              153    153     0%   6-290
src\core\license_validator.py                            179    179     0%   6-352
src\core\logging\__init__.py                              10      0   100%
src\core\logging\alert_manager.py                        114     85    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239
src\core\logging\analytics.py                            136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                36      2    94%   70-72
src\core\logging\context.py                               52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                            64     56    12%   44-118, 147-184
src\core\logging\filters.py                               66     48    27%   91-98, 111-129, 142-156, 169-175, 193-194, 203-212
src\core\logging\formatters.py                            82     60    27%   56-108, 118-140, 168, 194-227, 231-241
src\core\logging\logger.py                               109     64    41%   74-96, 100-101, 120-180, 198-201, 205, 209, 213, 217, 221, 232, 249, 293-298
src\core\logging\metadata.py                              86     86     0%   5-199
src\core\logging\metrics.py                               98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              54     41    24%   33-44, 48, 58, 67, 86-108, 121-128, 141-154, 163, 180-182, 201
src\core\logging\sinks.py                                 99     75    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-205, 217-219, 225-227, 233-235
src\core\logging\viewer.py                               175    142    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 149, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                  125    125     0%   6-252
src\core\lyra_sentinel.py                                 29     29     0%   6-50
src\core\notification_manager.py                          95     95     0%   6-194
src\core\oda_manager.py                                   34     34     0%   6-115
src\core\report_history.py                                65     65     0%   7-155
src\core\schemas.py                                       77     77     0%   1-107
src\core\secrets_manager.py                               94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                 46     46     0%   6-82
src\core\sync_tracker.py                                  58     58     0%   1-105
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             174    174     0%   1-313
src\core\telegram_bridge.py                              343    343     0%   1-531
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           97     97     0%   6-163
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                    57     57     0%   1-117
src\gui\dialogs\bug_report_dialog.py                     229    229     0%   10-477
src\gui\dialogs\command_palette.py                       301    301     0%   1-512
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-119
src\gui\dialogs\quick_actions_config.py                   80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                        232    232     0%   6-390
src\gui\formatters.py                                    127    127     0%   1-227
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                73     73     0%   1-330
src\gui\main_window\components\status_bar.py             157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                25     25     0%   1-43
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-52
src\gui\main_window\main.py                              279    279     0%   1-443
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   198    198     0%   6-389
src\gui\panels\carico_ts.py                               90     90     0%   6-180
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 197    197     0%   1-367
src\gui\panels\contabilita_kpi\kpi_panel.py              150    150     0%   1-297
src\gui\panels\contabilita_panel.py                      246    246     0%   6-412
src\gui\panels\dashboard_panel.py                        159    159     0%   1-289
src\gui\panels\dettagli_oda.py                           135    135     0%   6-231
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py               158    158     0%   1-334
src\gui\panels\health_panel.py                           289    289     0%   8-571
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          32     32     0%   1-54
src\gui\panels\lyra\header.py                             36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        146    146     0%   1-212
src\gui\panels\lyra\workers.py                            37     37     0%   1-57
src\gui\panels\notifications_panel.py                    253    253     0%   6-445
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                     45     45     0%   1-68
src\gui\panels\pdl\pdl_filter_widget.py                   67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                          334    334     0%   6-567
src\gui\panels\prenota_bp.py                             105    105     0%   6-183
src\gui\panels\ricerca_pdl.py                             79     79     0%   6-152
src\gui\panels\scarico_ore_panel.py                      299    299     0%   7-520
src\gui\panels\scarico_pdl.py                            296    296     0%   6-523
src\gui\panels\scarico_ts.py                             122    122     0%   6-211
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py             46     46     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py           41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                  247    247     0%   6-457
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       158    158     0%   1-285
src\gui\panels\timbrature_bot.py                         116    116     0%   6-200
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-156
src\gui\styles\theme_manager.py                           66     66     0%   6-122
src\gui\styles\widget_styles.py                           35     35     0%   6-391
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         134    134     0%   1-313
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-180
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                   67     67     0%   1-164
src\gui\widgets\autopilot\main_widget.py                 197    197     0%   6-349
src\gui\widgets\bot_parameters.py                        108    108     0%   6-203
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            106    106     0%   5-213
src\gui\widgets\excel_table.py                           325    325     0%   6-537
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   87     87     0%   1-119
src\gui\widgets\footer\components.py                      48     48     0%   1-87
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                       52     52     0%   1-66
src\gui\widgets\info_widgets.py                           89     89     0%   6-175
src\gui\widgets\message_bubble.py                         53     53     0%   7-127
src\gui\widgets\modern_button.py                          60     60     0%   5-146
src\gui\widgets\notification_card.py                     218    218     0%   6-516
src\gui\widgets\notification_group_header.py              46     46     0%   6-144
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  103    103     0%   6-277
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          74     74     0%   1-354
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        243    243     0%   1-432
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       189    189     0%   6-307
src\gui\widgets\toast.py                                 129    129     0%   5-250
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      2     0%   5-17
src\utils\animation_helpers.py                           100    100     0%   6-295
src\utils\date_utils.py                                   70     70     0%   6-228
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           54     54     0%   6-77
src\utils\helpers.py                                      90     90     0%   6-249
src\utils\log_humanizer.py                                42     42     0%   6-119
src\utils\parsing.py                                      53     53     0%   6-119
src\utils\printing.py                                     83     83     0%   1-141
src\utils\resource_manager.py                             56     56     0%   6-91
src\utils\secure_logger.py                                23     23     0%   5-70
src\utils\security.py                                     79     79     0%   6-142
src\utils\system_telemetry.py                             26     26     0%   6-74
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  16886  16270     4%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_backup_manager.py::TestBackupManager::test_restore_backup
============================== 1 failed in 4.93s ==============================

```
</details>

---
### `tests/unit/test_base_bot_init_refactoring.py::test_init_driver_fallback_local`
**Error:** `Unknown Error`

**Timestamp:** `2026-02-07T22:22:24.324251`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_base_bot_init_refactoring.py
INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\main.py", line 318, in wrap_session
INTERNALERROR>     session.exitstatus = doit(config, session) or 0
INTERNALERROR>                          ^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\main.py", line 372, in _main
INTERNALERROR>     config.hook.pytest_runtestloop(session=session)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_hooks.py", line 512, in __call__
INTERNALERROR>     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_manager.py", line 120, in _hookexec
INTERNALERROR>     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 167, in _multicall
INTERNALERROR>     raise exception
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\logging.py", line 801, in pytest_runtestloop
INTERNALERROR>     return (yield)  # Run all the tests.
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\terminal.py", line 714, in pytest_runtestloop
INTERNALERROR>     result = yield
INTERNALERROR>              ^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pytest_cov\plugin.py", line 345, in pytest_runtestloop
INTERNALERROR>     result = yield
INTERNALERROR>              ^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 121, in _multicall
INTERNALERROR>     res = hook_impl.function(*args)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\main.py", line 396, in pytest_runtestloop
INTERNALERROR>     item.config.hook.pytest_runtest_protocol(item=item, nextitem=nextitem)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_hooks.py", line 512, in __call__
INTERNALERROR>     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_manager.py", line 120, in _hookexec
INTERNALERROR>     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 167, in _multicall
INTERNALERROR>     raise exception
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\warnings.py", line 89, in pytest_runtest_protocol
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\assertion\__init__.py", line 192, in pytest_runtest_protocol
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\unittest.py", line 573, in pytest_runtest_protocol
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\faulthandler.py", line 102, in pytest_runtest_protocol
INTERNALERROR>     return (yield)
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 121, in _multicall
INTERNALERROR>     res = hook_impl.function(*args)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\runner.py", line 118, in pytest_runtest_protocol
INTERNALERROR>     runtestprotocol(item, nextitem=nextitem)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\runner.py", line 137, in runtestprotocol
INTERNALERROR>     reports.append(call_and_report(item, "call", log))
INTERNALERROR>                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\runner.py", line 249, in call_and_report
INTERNALERROR>     report: TestReport = ihook.pytest_runtest_makereport(item=item, call=call)
INTERNALERROR>                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_hooks.py", line 512, in __call__
INTERNALERROR>     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_manager.py", line 120, in _hookexec
INTERNALERROR>     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 167, in _multicall
INTERNALERROR>     raise exception
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\tmpdir.py", line 308, in pytest_runtest_makereport
INTERNALERROR>     rep = yield
INTERNALERROR>           ^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pytestqt\logging.py", line 45, in pytest_runtest_makereport
INTERNALERROR>     report = yield
INTERNALERROR>              ^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\skipping.py", line 280, in pytest_runtest_makereport
INTERNALERROR>     rep = yield
INTERNALERROR>           ^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\pluggy\_callers.py", line 121, in _multicall
INTERNALERROR>     res = hook_impl.function(*args)
INTERNALERROR>           ^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\runner.py", line 377, in pytest_runtest_makereport
INTERNALERROR>     return TestReport.from_item_and_call(item, call)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\reports.py", line 438, in from_item_and_call
INTERNALERROR>     longrepr = _format_failed_longrepr(item, call, excinfo)
INTERNALERROR>                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\reports.py", line 263, in _format_failed_longrepr
INTERNALERROR>     longrepr = item.repr_failure(excinfo)
INTERNALERROR>                ^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\python.py", line 1762, in repr_failure
INTERNALERROR>     return self._repr_failure_py(excinfo, style=style)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\nodes.py", line 456, in _repr_failure_py
INTERNALERROR>     return excinfo.getrepr(
INTERNALERROR>            ^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\_code\code.py", line 765, in getrepr
INTERNALERROR>     return fmt.repr_excinfo(self)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\_code\code.py", line 1200, in repr_excinfo
INTERNALERROR>     reprtraceback = self.repr_traceback(excinfo_)
INTERNALERROR>                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\_code\code.py", line 1133, in repr_traceback
INTERNALERROR>     self.repr_traceback_entry(entry, excinfo if last == entry else None)
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\_code\code.py", line 1090, in repr_traceback_entry
INTERNALERROR>     path = self._makepath(entry_path)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\_code\code.py", line 1106, in _makepath
INTERNALERROR>     np = bestrelpath(Path.cwd(), path)
INTERNALERROR>          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 1027, in bestrelpath
INTERNALERROR>     assert isinstance(directory, Path)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR> AssertionError

============================ no tests ran in 2.43s ============================

```
</details>

---
### `tests/unit/test_config_manager_advanced.py::TestConfigManagerAdvanced::test_load_base_config_malformed_json_fallback`
**Error:** `FAILED tests/unit/test_config_manager_advanced.py::TestConfigManagerAdvanced::test_load_base_config_malformed_json_fallback`

**Timestamp:** `2026-02-07T22:29:03.413296`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_config_manager_advanced.py F                             [100%]

================================== FAILURES ===================================
___ TestConfigManagerAdvanced.test_load_base_config_malformed_json_fallback ___
tests\unit\test_config_manager_advanced.py:81: in test_load_base_config_malformed_json_fallback
    config = _load_base_config()
             ^^^^^^^^^^^^^^^^^^^
src\core\config_manager.py:98: in _load_base_config
    config.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\json\__init__.py:339: in loads
    raise TypeError(f'the JSON object must be str, bytes or bytearray, '
E   TypeError: the JSON object must be str, bytes or bytearray, not MagicMock
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              260     29    89%   149, 224, 248, 267, 368, 397-399, 412-413, 417-421, 425-427, 431, 435-441, 460-462
src\bots\base\login_page.py                                             94     58    38%   44-54, 58-78, 82-94, 116-117, 128-144, 149-154
src\bots\base\wait_helpers.py                                          166    166     0%   14-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     18    62%   20, 25, 31, 56, 60-72, 86, 91, 94, 100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     12    78%   34-36, 49-51, 79-81, 118-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          80     58    28%   21, 26, 31, 38, 42, 51-54, 60-67, 71-91, 95-106, 117-135, 139-144
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    136    34%   50-52, 65-90, 101-114, 118-147, 151-158, 218, 233-241, 258-262, 271-277, 281-299, 309-335, 339-348, 352-361, 365-376
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-103, 107-128
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         218    190    13%   28-31, 35, 39-41, 53-79, 90-95, 100-105, 109-137, 141-174, 178-186, 195-223, 227-234, 238-258, 262-274, 278-290, 294-312, 316-340, 344-348
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           218    151    31%   40, 45, 50, 61, 80-82, 86-99, 103-120, 124-139, 143-165, 169-196, 200-209, 213-238, 243, 272-274, 280-309, 313-322, 338, 345-366, 371-381
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     44    58%   43-44, 63-65, 89-91, 95-124, 128-145, 149-154
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            70     44    37%   26, 31, 36, 47-60, 66-109, 116
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    101    38%   46-61, 83-85, 89-148, 165-166, 177-180, 183, 201-202, 206-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       175    137    22%   91-110, 116-145, 155-166, 176-183, 186-214, 221-257, 260-275, 280-320, 323-358, 362-376, 383-384
src\bots\safework\base.py                                               40     17    58%   23, 42-45, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           387    303    22%   25, 30, 35, 40, 45, 56-60, 64, 68, 72-97, 101-160, 164-168, 172-200, 204-233, 237-245, 250, 258-260, 263-265, 276-281, 287-315, 319-332, 336-364, 368-403, 407-421, 425-446, 450-462, 470, 478, 483-507, 511, 543, 550, 554-573
src\bots\safework\pdl\search_bot.py                                    179    154    14%   19-20, 24, 28, 32-90, 94-111, 115-132, 136-145, 149-159, 163-168, 172-197, 201-226, 230-300
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82     82     0%   5-156
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     59    40%   61-63, 78-79, 102-146, 149-154, 157-163
src\core\audit\integrity.py                                             15      2    87%   21, 26
src\core\audit\manager.py                                              139     71    49%   46, 50, 58-63, 170, 174-177, 183-200, 204-231, 234-235, 238, 241, 244-247, 255-283
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-131
src\core\backup_manager.py                                             138    105    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-188, 199-207, 212-223, 228-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config_manager.py                                             237     75    68%   87, 115, 131-148, 159, 199-200, 222, 232, 247, 279, 296-297, 300, 326-353, 374-376, 390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        101     49    51%   29, 34, 39, 48-60, 77-124, 133-140, 149-154, 167, 175, 180, 185, 190, 195, 200, 209, 217, 222
src\core\contabilita_queries.py                                         86     70    19%   18-29, 34-47, 52-77, 82-93, 98-109, 114-125
src\core\contabilita_search.py                                          91     73    20%   25-81, 88-112, 117-128, 133-145, 152-164, 178-182
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          158    132    16%   18-22, 27-30, 37-54, 59-69, 75-102, 108-146, 154-191, 199-234, 238, 248, 263-320
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           120     63    48%   104, 123-134, 141-171, 175-179, 182-185, 188, 194-213
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44      9    80%   33, 50, 62, 73, 77, 99, 104-106
src\core\importers\attivita.py                                          65     48    26%   42-59, 63-77, 81-97, 101-115
src\core\importers\base.py                                              58     33    43%   15-16, 23-25, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      116     21    82%   38, 47, 51, 54-55, 64, 91, 105-106, 141, 150, 162, 166-167, 171, 174-179
src\core\importers\contabilita.py                                      135    109    19%   40-57, 68-104, 111-128, 133-187, 192-210, 215-239, 244-247
src\core\importers\giornaliere.py                                      190    155    18%   42-63, 73-91, 101-120, 126-145, 149-187, 191-206, 210-232, 236-288, 292-308
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    153     0%   6-290
src\core\license_validator.py                                          179    179     0%   6-352
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              36      0   100%
src\core\logging\context.py                                             52      7    87%   29-30, 52, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 118, 147-184
src\core\logging\filters.py                                             66     32    52%   92, 112, 118, 125, 142-156, 169-175, 193-194, 203-212
src\core\logging\formatters.py                                          82      7    91%   84, 125, 168, 231-241
src\core\logging\logger.py                                             109     15    86%   84, 96, 123, 147-148, 164-165, 173-174, 221, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                               99     60    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-205, 225-227, 233-235
src\core\logging\viewer.py                                             175    142    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 149, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    110    12%   21-37, 55-69, 73-74, 78-106, 110-141, 150-205, 214-252
src\core\lyra_sentinel.py                                               29     29     0%   6-50
src\core\notification_manager.py                                        95     68    28%   29-35, 38-45, 49-57, 61-74, 78-82, 101-146, 150-152, 156, 160-167, 171-180, 184-187, 191-194
src\core\oda_manager.py                                                 34     20    41%   23, 31-91, 100-115
src\core\report_history.py                                              65     43    34%   25-27, 35-40, 45-49, 60-84, 94, 112-132, 145-155
src\core\schemas.py                                                     77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                                             94     51    46%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 122-126, 133-134, 139-145
src\core\stats_manager.py                                               46     15    67%   40-44, 47, 60, 62, 70-78, 82
src\core\sync_tracker.py                                                58     36    38%   26-39, 44-48, 61-73, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         97     75    23%   26-66, 71-81, 86-91, 96-103, 109-143, 148-156, 161-163
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-133, 136-150, 153-156, 159-166, 169-172, 175-177, 180-182, 185-211, 214-230, 233-235, 238-263
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  57     45    21%   25-29, 32-112, 115-117
src\gui\dialogs\bug_report_dialog.py                                   229    229     0%   10-477
src\gui\dialogs\command_palette.py                                     301    301     0%   1-512
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-76, 79-87, 90-98, 103-104, 108-109, 113-114, 118-119
src\gui\dialogs\quick_actions_config.py                                 80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127     65    49%   13, 21-25, 35-65, 70, 95, 99, 109, 115-117, 131, 155-207, 217-219, 224-225
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-330
src\gui\main_window\components\status_bar.py                           157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-443
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          129    104    19%   29-32, 41-43, 46, 49, 52-76, 80-98, 102-112, 116-123, 127-131, 135-143, 147-149, 152-154, 157-162, 165-169, 173-185, 188-190
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 198     27    86%   60-77, 89-93, 209, 221, 230, 250-252, 370-373, 381, 388
src\gui\panels\carico_ts.py                                             90     27    70%   40-44, 97-99, 103-105, 111, 115, 121-122, 130-134, 138-145, 161-162
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-61, 68-76, 79-82, 86-90, 93-154, 157-211, 214-276, 279-318, 321-367
src\gui\panels\contabilita_kpi\kpi_panel.py                            150    131    13%   35-41, 44-162, 175-179, 182-195, 198-208, 211, 214-297
src\gui\panels\contabilita_panel.py                                    246    210    15%   39-46, 50-56, 60-160, 164-171, 175, 179, 202-219, 223-244, 249-274, 278-280, 284-287, 291-312, 316-332, 335-336, 339-343, 346-361, 364-366, 369-386, 390, 393-412
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-127, 131-133, 137-147, 151-166, 171-186, 191-209, 213-224, 228-234, 238-253, 257-279, 283-289
src\gui\panels\dettagli_oda.py                                         135     73    46%   38-42, 93-95, 99, 102-114, 118, 130-132, 140, 145-221, 225-231
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     368    330    10%   55-86, 89-219, 223-257, 261-274, 277-305, 308-350, 354-362, 366-380, 383-392, 396-427, 430-462, 465-505, 508-548, 551, 555-638, 641-646, 652-681
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         53     46    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    152    127    16%   24-50, 55-98, 107-193, 198-209, 214-236, 241-298
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         289    257    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-523, 527-555, 559-564, 568-571
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-32, 36-47, 51-54
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-122, 125-130, 133-140, 143-144, 147-148, 151-153, 156-161, 164-166, 169-178, 181-182, 185-188, 191-193, 197, 200-212
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 45-46, 49-57
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-310, 314-315, 319-337, 341-373, 377-379, 383-402, 406-445
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-46, 50-63, 67-68
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-147, 151-205, 208-214, 218-247, 251-263, 267-299, 303-341, 345-347, 351-352, 356-363, 367-373, 377-395, 399-471, 475-479, 483-494, 498-522, 526-567
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-183
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296     79    73%   87-120, 143-145, 182, 277-285, 288-291, 297, 303-305, 319, 322-324, 328-336, 341-347, 358-361, 364, 369, 389-393, 396-399, 443, 453, 499, 504
src\gui\panels\scarico_ts.py                                           122     24    80%   38-40, 83-85, 104, 111, 122-124, 166-175, 183-187
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                247    217    12%   42-105, 108-167, 171-179, 183-282, 285-296, 299, 302, 305-309, 312-318, 322-340, 344-402, 405-410, 413-433, 437-457
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     25    58%   70-110, 114-129
src\gui\panels\timbrature\components\settings_tab.py                    94      4    96%   139, 151-153
src\gui\panels\timbrature\panel.py                                     158     25    84%   223-241, 244-251, 265, 280-281, 285
src\gui\panels\timbrature_bot.py                                       116     35    70%   40-42, 60-62, 89, 98-103, 113-114, 126-134, 139-149, 172-174, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         66     66     0%   6-122
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       134    117    13%   28-179, 183, 187-189, 198-206, 209-257, 262, 267-313
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      108      3    97%   148-150
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            205    172    16%   53-55, 59-129, 132, 135-150, 154-168, 171-182, 185-191, 194-199, 202-220, 223-226, 230-236, 239-242, 245-248, 251-254, 257-260, 263-267, 270-281, 284-289
src\gui\widgets\contabilita\certificati_tab.py                         557    146    74%   155, 163, 166-169, 315, 333, 438-441, 457-458, 701-702, 713, 724, 736, 760-762, 826, 840-843, 906, 913-915, 918-920, 926-935, 976, 981-984, 988-991, 995-1005, 1008-1077, 1093-1129, 1136-1141, 1146-1186
src\gui\widgets\contabilita\giornaliere_tab.py                         167    136    19%   47-50, 54-93, 97, 100-127, 130-137, 141, 144-160, 163-179, 183-195, 198-215, 218-234
src\gui\widgets\contabilita\helpers.py                                  32     26    19%   10-30, 33-40, 43-48
src\gui\widgets\contabilita\year_tab.py                                 95     76    20%   25-26, 30-31, 34-51, 73-93, 96-134, 138, 142-163, 167-196, 200, 204
src\gui\widgets\data_table.py                                          106     82    23%   48-52, 55-125, 132-133, 136-161, 164-170, 174-182, 185-187, 191-206, 213
src\gui\widgets\excel_table.py                                         325    204    37%   45-57, 61-68, 72-89, 93-113, 116-117, 120-121, 125-136, 140-162, 166-188, 192-209, 213-231, 235-244, 247-252, 255-259, 262-266, 304-359, 368-374, 403, 412-415, 418-420, 495-499, 512-537
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 87     87     0%   1-119
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        60     11    82%   66-67, 73-76, 80-83, 144
src\gui\widgets\notification_card.py                                   218    187    14%   86-92, 96-338, 342-352, 356, 360-362, 376-407, 411-427, 431-435, 439-441, 445-446, 450-454, 459-460, 464-499, 503-507, 511-516
src\gui\widgets\notification_group_header.py                            46     36    22%   32-38, 42-123, 127-130, 134-135, 139, 143-144
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                103     78    24%   34-46, 50-62, 66-68, 72-76, 80-99, 131-137, 141-226, 231-232, 236-237, 242-249, 253-254, 263-265, 269, 273, 277
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        74     59    20%   22-30, 234-235, 238-261, 265-306, 311-349, 354
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      243    243     0%   1-432
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59      8    86%   106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     189     42    78%   73-74, 76-77, 120-122, 124-126, 130, 133-138, 146-150, 153-154, 157-159, 172-185, 218-226
src\gui\widgets\toast.py                                               129     98    24%   58-78, 82-121, 125-148, 151-155, 159-161, 165-166, 169-181, 192-194, 204-230, 235, 240, 245, 250
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     70     0%   6-228
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         54     39    28%   14-15, 24-30, 35-49, 54-58, 63-77
src\utils\helpers.py                                                    90     51    43%   29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 202, 221, 232, 241
src\utils\log_humanizer.py                                              42     14    67%   13-26, 110, 118
src\utils\parsing.py                                                    53     18    66%   14, 17, 21, 45-46, 62, 64, 79, 84-97, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     37    53%   43-44, 54-58, 81-83, 102-112, 116-138
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23251  16597    29%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_config_manager_advanced.py::TestConfigManagerAdvanced::test_load_base_config_malformed_json_fallback
============================== 1 failed in 4.15s ==============================

```
</details>

---
### `tests/unit/test_config_safework.py::TestConfigSafeWork::test_load_save_safework_accounts`
**Error:** `FAILED tests/unit/test_config_safework.py::TestConfigSafeWork::test_load_save_safework_accounts`

**Timestamp:** `2026-02-07T22:30:32.493050`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_config_safework.py F                                     [100%]

================================== FAILURES ===================================
_____________ TestConfigSafeWork.test_load_save_safework_accounts _____________
tests\unit\test_config_safework.py:39: in test_load_save_safework_accounts
    config = config_manager.load_config()
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\core\config_manager.py:80: in load_config
    config = _load_base_config()
             ^^^^^^^^^^^^^^^^^^^
src\core\config_manager.py:98: in _load_base_config
    config.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\json\__init__.py:339: in loads
    raise TypeError(f'the JSON object must be str, bytes or bytearray, '
E   TypeError: the JSON object must be str, bytes or bytearray, not MagicMock
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      21     21     0%   6-142
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                260    260     0%   6-474
src\bots\base\login_page.py                               94     94     0%   6-154
src\bots\base\wait_helpers.py                            166    166     0%   14-473
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               82     82     0%   5-156
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit\__init__.py                                 3      3     0%   1-4
src\core\audit\database.py                                99     99     0%   1-163
src\core\audit\integrity.py                               15     15     0%   1-26
src\core\audit\manager.py                                139    139     0%   1-283
src\core\audit\models.py                                   9      9     0%   1-13
src\core\audit\signals.py                                 27     27     0%   1-40
src\core\audit_manager.py                                  5      5     0%   6-11
src\core\auth_monitor.py                                  72     72     0%   6-131
src\core\backup_manager.py                               138    138     0%   6-250
src\core\bug_reporter.py                                 157    157     0%   11-339
src\core\config_manager.py                               237     59    75%   35, 115, 136, 159, 222, 279, 295-297, 307-317, 326-353, 360, 381-390, 399-417, 429, 437, 465-466
src\core\constants.py                                     96     96     0%   6-134
src\core\contabilita_manager.py                          101    101     0%   6-222
src\core\contabilita_queries.py                           86     86     0%   6-125
src\core\contabilita_search.py                            91     91     0%   6-182
src\core\contabilita_stats.py                             59     59     0%   6-99
src\core\contabilita_worker.py                           101    101     0%   1-233
src\core\data_synchronizer.py                            158    158     0%   6-320
src\core\database\__init__.py                              2      2     0%   1-3
src\core\database\manager.py                             120    120     0%   6-216
src\core\employees.py                                     98     98     0%   1-196
src\core\excel_importer.py                                 4      4     0%   6-11
src\core\importers\__init__.py                            44     44     0%   1-106
src\core\importers\attivita.py                            65     65     0%   1-115
src\core\importers\base.py                                58     58     0%   1-86
src\core\importers\certificati.py                        116    116     0%   1-187
src\core\importers\contabilita.py                        135    135     0%   1-247
src\core\importers\giornaliere.py                        190    190     0%   1-308
src\core\importers\scarico_ore.py                        186    186     0%   1-311
src\core\importers\storico_oda.py                         81     81     0%   1-185
src\core\license_updater.py                              153    153     0%   6-290
src\core\license_validator.py                            179    179     0%   6-352
src\core\logging\__init__.py                              10     10     0%   6-37
src\core\logging\alert_manager.py                        114    114     0%   7-239
src\core\logging\analytics.py                            136    136     0%   7-343
src\core\logging\config.py                                36     36     0%   5-85
src\core\logging\context.py                               52     52     0%   5-156
src\core\logging\decorators.py                            64     64     0%   5-184
src\core\logging\filters.py                               66     66     0%   5-212
src\core\logging\formatters.py                            82     82     0%   5-241
src\core\logging\logger.py                               109    109     0%   5-298
src\core\logging\metadata.py                              86     86     0%   5-199
src\core\logging\metrics.py                               98     98     0%   5-297
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              54     54     0%   5-201
src\core\logging\sinks.py                                 99     99     0%   5-235
src\core\logging\viewer.py                               175    175     0%   5-420
src\core\lyra_client.py                                  125    125     0%   6-252
src\core\lyra_sentinel.py                                 29     29     0%   6-50
src\core\notification_manager.py                          95     95     0%   6-194
src\core\oda_manager.py                                   34     34     0%   6-115
src\core\report_history.py                                65     65     0%   7-155
src\core\schemas.py                                       77     77     0%   1-107
src\core\secrets_manager.py                               94     53    44%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                 46     46     0%   6-82
src\core\sync_tracker.py                                  58     58     0%   1-105
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             174    174     0%   1-313
src\core\telegram_bridge.py                              343    343     0%   1-531
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           97     97     0%   6-163
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                    57     57     0%   1-117
src\gui\dialogs\bug_report_dialog.py                     229    229     0%   10-477
src\gui\dialogs\command_palette.py                       301    301     0%   1-512
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-119
src\gui\dialogs\quick_actions_config.py                   80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                        232    232     0%   6-390
src\gui\formatters.py                                    127    127     0%   1-227
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                73     73     0%   1-330
src\gui\main_window\components\status_bar.py             157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                25     25     0%   1-43
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-52
src\gui\main_window\main.py                              279    279     0%   1-443
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   198    198     0%   6-389
src\gui\panels\carico_ts.py                               90     90     0%   6-180
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 197    197     0%   1-367
src\gui\panels\contabilita_kpi\kpi_panel.py              150    150     0%   1-297
src\gui\panels\contabilita_panel.py                      246    246     0%   6-412
src\gui\panels\dashboard_panel.py                        159    159     0%   1-289
src\gui\panels\dettagli_oda.py                           135    135     0%   6-231
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py               158    158     0%   1-334
src\gui\panels\health_panel.py                           289    289     0%   8-571
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          32     32     0%   1-54
src\gui\panels\lyra\header.py                             36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        146    146     0%   1-212
src\gui\panels\lyra\workers.py                            37     37     0%   1-57
src\gui\panels\notifications_panel.py                    253    253     0%   6-445
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                     45     45     0%   1-68
src\gui\panels\pdl\pdl_filter_widget.py                   67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                          334    334     0%   6-567
src\gui\panels\prenota_bp.py                             105    105     0%   6-183
src\gui\panels\ricerca_pdl.py                             79     79     0%   6-152
src\gui\panels\scarico_ore_panel.py                      299    299     0%   7-520
src\gui\panels\scarico_pdl.py                            296    296     0%   6-523
src\gui\panels\scarico_ts.py                             122    122     0%   6-211
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py             46     46     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py           41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                  247    247     0%   6-457
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       158    158     0%   1-285
src\gui\panels\timbrature_bot.py                         116    116     0%   6-200
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-156
src\gui\styles\theme_manager.py                           66     66     0%   6-122
src\gui\styles\widget_styles.py                           35     35     0%   6-391
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         134    134     0%   1-313
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-180
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                   67     67     0%   1-164
src\gui\widgets\autopilot\main_widget.py                 197    197     0%   6-349
src\gui\widgets\bot_parameters.py                        108    108     0%   6-203
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            106    106     0%   5-213
src\gui\widgets\excel_table.py                           325    325     0%   6-537
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   87     87     0%   1-119
src\gui\widgets\footer\components.py                      48     48     0%   1-87
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                       52     52     0%   1-66
src\gui\widgets\info_widgets.py                           89     89     0%   6-175
src\gui\widgets\message_bubble.py                         53     53     0%   7-127
src\gui\widgets\modern_button.py                          60     60     0%   5-146
src\gui\widgets\notification_card.py                     218    218     0%   6-516
src\gui\widgets\notification_group_header.py              46     46     0%   6-144
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  103    103     0%   6-277
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          74     74     0%   1-354
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        243    243     0%   1-432
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       189    189     0%   6-307
src\gui\widgets\toast.py                                 129    129     0%   5-250
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-295
src\utils\date_utils.py                                   70     70     0%   6-228
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           54     54     0%   6-77
src\utils\helpers.py                                      90     71    21%   22-24, 29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 201-223, 231-249
src\utils\log_humanizer.py                                42     42     0%   6-119
src\utils\parsing.py                                      53     53     0%   6-119
src\utils\printing.py                                     83     83     0%   1-141
src\utils\resource_manager.py                             56     56     0%   6-91
src\utils\secure_logger.py                                23     23     0%   5-70
src\utils\security.py                                     79     32    59%   43-44, 54-58, 81-83, 103, 105, 110-112, 116-138
src\utils\system_telemetry.py                             26     26     0%   6-74
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  16886  16593     2%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_config_safework.py::TestConfigSafeWork::test_load_save_safework_accounts
============================== 1 failed in 3.26s ==============================

```
</details>

---
### `tests/unit/test_contabilita_search.py::TestContabilitaSearch::test_fmt_date_invalid`
**Error:** `FAILED tests/unit/test_contabilita_search.py::TestContabilitaSearch::test_fmt_date_invalid`

**Timestamp:** `2026-02-07T22:33:58.700127`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_contabilita_search.py F                                  [100%]

================================== FAILURES ===================================
_________________ TestContabilitaSearch.test_fmt_date_invalid _________________
tests\unit\test_contabilita_search.py:79: in test_fmt_date_invalid
    assert result == "not-a-date"
E   AssertionError: assert 'date/a/not' == 'not-a-date'
E
E     - not-a-date
E     + date/a/not
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              260    203    22%   52-72, 87, 92-94, 106-110, 121-137, 141, 145, 149, 153-154, 158-159, 164-180, 184-227, 231-253, 257-259, 266-271, 275-302, 314-363, 367-399, 404-413, 417-421, 425-427, 431, 435-441, 452-464, 468-471
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    166     0%   14-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     30    36%   20, 25, 31, 52, 56, 60-72, 77-100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          80     58    28%   21, 26, 31, 38, 42, 51-54, 60-67, 71-91, 95-106, 117-135, 139-144
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   39-42, 46, 50-52, 65-90, 101-114, 118-147, 151-158, 182-277, 281-299, 309-335, 339-348, 352-361, 365-376
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-103, 107-128
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         218    190    13%   28-31, 35, 39-41, 53-79, 90-95, 100-105, 109-137, 141-174, 178-186, 195-223, 227-234, 238-258, 262-274, 278-290, 294-312, 316-340, 344-348
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           218    181    17%   40, 45, 50, 57, 61, 73-76, 80-82, 86-99, 103-120, 124-139, 143-165, 169-196, 200-209, 213-238, 242-274, 280-309, 313-322, 326-341, 345-366, 371-381
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            70     50    29%   21, 26, 31, 36, 39-43, 47-60, 66-109, 116
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-85, 89-148, 152-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       175    148    15%   45-46, 50-79, 83-84, 91-110, 116-145, 155-166, 176-183, 186-214, 221-257, 260-275, 280-320, 323-358, 362-376, 383-384
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           387    343    11%   25, 30, 35, 40, 45, 56-60, 64, 68, 72-97, 101-160, 164-168, 172-200, 204-233, 237-245, 249-283, 287-315, 319-332, 336-364, 368-403, 407-421, 425-446, 450-462, 469-507, 510-550, 554-573
src\bots\safework\pdl\search_bot.py                                    179    154    14%   19-20, 24, 28, 32-90, 94-111, 115-132, 136-145, 149-159, 163-168, 172-197, 201-226, 230-300
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82     82     0%   5-156
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-66, 69, 72-79, 83-90, 102-146, 149-154, 157-163
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-177, 183-200, 204-231, 234-235, 238, 241, 244-247, 255-283
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-131
src\core\backup_manager.py                                             138    105    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-188, 199-207, 212-223, 228-250
src\core\bug_reporter.py                                               157    157     0%   11-339
src\core\config_manager.py                                             237    130    45%   35, 77, 87, 109-115, 136, 141-142, 156-170, 179-180, 198, 222, 226-229, 243, 252, 257-259, 264, 269-284, 289-302, 307-317, 326-353, 358-362, 367-369, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        101     17    83%   102, 110, 123-124, 133-140, 151, 163-170, 185, 200
src\core\contabilita_queries.py                                         86     16    81%   28-29, 46-47, 53, 76-77, 83, 92-93, 99, 108-109, 115, 124-125
src\core\contabilita_search.py                                          91      9    90%   51-52, 78-79, 109-110, 126-128
src\core\contabilita_stats.py                                           59      3    95%   58, 64, 86
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          158     88    44%   21, 67-69, 78-102, 109, 154-191, 199-234, 238, 248, 263-320
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           120     25    79%   125-134, 161-171, 184-185, 211-213
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44      6    86%   50, 62, 73, 77, 88, 99
src\core\importers\attivita.py                                          65     48    26%   42-59, 63-77, 81-97, 101-115
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      135     27    80%   42, 49-57, 70, 78, 88, 102-104, 118, 126, 138-139, 148, 185-187, 209, 229, 231
src\core\importers\giornaliere.py                                      190    149    22%   44, 49-62, 73-91, 101-120, 126-145, 149-187, 191-206, 210-232, 236-288, 292-308
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    153     0%   6-290
src\core\license_validator.py                                          179    179     0%   6-352
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             66     48    27%   91-98, 111-129, 142-156, 169-175, 193-194, 203-212
src\core\logging\formatters.py                                          82     60    27%   56-108, 118-140, 168, 194-227, 231-241
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-180, 198-201, 205, 209, 213, 217, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     41    24%   33-44, 48, 58, 67, 86-108, 121-128, 141-154, 163, 180-182, 201
src\core\logging\sinks.py                                               99     75    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-205, 217-219, 225-227, 233-235
src\core\logging\viewer.py                                             175    142    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 149, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    110    12%   21-37, 55-69, 73-74, 78-106, 110-141, 150-205, 214-252
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                        95     68    28%   29-35, 38-45, 49-57, 61-74, 78-82, 101-146, 150-152, 156, 160-167, 171-180, 184-187, 191-194
src\core\oda_manager.py                                                 34     20    41%   23, 31-91, 100-115
src\core\report_history.py                                              65     43    34%   25-27, 35-40, 45-49, 60-84, 94, 112-132, 145-155
src\core\schemas.py                                                     77     25    68%   65-70, 75-86, 91-93, 98-100, 106
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               46     33    28%   23-26, 30, 34-47, 51, 55-66, 70-78, 82
src\core\sync_tracker.py                                                58     36    38%   26-39, 44-48, 61-73, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         97     75    23%   26-66, 71-81, 86-91, 96-103, 109-143, 148-156, 161-163
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-133, 136-150, 153-156, 159-166, 169-172, 175-177, 180-182, 185-211, 214-230, 233-235, 238-263
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  57     45    21%   25-29, 32-112, 115-117
src\gui\dialogs\bug_report_dialog.py                                   229    229     0%   10-477
src\gui\dialogs\command_palette.py                                     301    301     0%   1-512
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-76, 79-87, 90-98, 103-104, 108-109, 113-114, 118-119
src\gui\dialogs\quick_actions_config.py                                 80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-65, 70, 82-88, 92-95, 99, 102, 105, 108-133, 136-138, 141-144, 148-227
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-330
src\gui\main_window\components\status_bar.py                           157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-443
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          129    104    19%   29-32, 41-43, 46, 49, 52-76, 80-98, 102-112, 116-123, 127-131, 135-143, 147-149, 152-154, 157-162, 165-169, 173-185, 188-190
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 198    142    28%   52-56, 60-77, 89-93, 97-99, 124-132, 136-180, 187, 191-202, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-311, 321-323, 327-340, 344, 348-363, 370-373, 377-382, 386-389
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-105, 109-117, 121-122, 126-180
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   96-97, 102-104, 129-135, 138-150, 162-163, 184, 217-218, 225-227, 284-285, 307-309, 324-325
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    246    106    57%   50-56, 164-171, 175, 203-205, 215, 219, 223-244, 249-274, 278-280, 284-287, 295-300, 303-312, 323-325, 343, 350, 365, 369-386, 390, 393-412
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-127, 131-133, 137-147, 151-166, 171-186, 191-209, 213-224, 228-234, 238-253, 257-279, 283-289
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-90, 93-95, 99, 102-114, 117-127, 130-132, 136-142, 145-221, 225-231
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     368    330    10%   55-86, 89-219, 223-257, 261-274, 277-305, 308-350, 354-362, 366-380, 383-392, 396-427, 430-462, 465-505, 508-548, 551, 555-638, 641-646, 652-681
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         53     46    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    152    127    16%   24-50, 55-98, 107-193, 198-209, 214-236, 241-298
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         289    257    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-523, 527-555, 559-564, 568-571
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-32, 36-47, 51-54
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-122, 125-130, 133-140, 143-144, 147-148, 151-153, 156-161, 164-166, 169-178, 181-182, 185-188, 191-193, 197, 200-212
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 45-46, 49-57
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-310, 314-315, 319-337, 341-373, 377-379, 383-402, 406-445
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-46, 50-63, 67-68
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-147, 151-205, 208-214, 218-247, 251-263, 267-299, 303-341, 345-347, 351-352, 356-363, 367-373, 377-395, 399-471, 475-479, 483-494, 498-522, 526-567
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-183
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-274, 277-285, 288-291, 294-307, 310-315, 319, 322-324, 328-336, 341-347, 350-384, 388-400, 404-426, 430-444, 448-455, 459-489, 493-495, 499, 503-517, 521-523
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-79, 83-85, 89, 93-106, 110-118, 122-124, 128-133, 147-149, 155-211
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                247    217    12%   42-105, 108-167, 171-179, 183-282, 285-296, 299, 302, 305-309, 312-318, 322-340, 344-402, 405-410, 413-433, 437-457
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-62, 70-110, 114-129, 133-134
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         66     66     0%   6-122
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       134    117    13%   28-179, 183, 187-189, 198-206, 209-257, 262, 267-313
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      108     85    21%   39-43, 46-108, 118-125, 129, 148-150, 154-162, 167, 171-173, 177-179, 189-194, 198, 202-203
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            205     55    73%   132, 187, 196-199, 219, 223-226, 230-236, 239-242, 245-248, 251-254, 257-260, 263-267, 270-281, 284-289
src\gui\widgets\contabilita\certificati_tab.py                         557    329    41%   43-45, 48-237, 241-267, 271-341, 345-458, 514-516, 520-524, 701-702, 713, 724, 730, 736, 761-762, 826, 840-843, 873, 886, 902, 928-930, 976, 981-984, 988-991, 995-1005, 1008-1077, 1081-1083, 1087-1089, 1093-1129, 1136-1141, 1146-1186
src\gui\widgets\contabilita\giornaliere_tab.py                         167    136    19%   47-50, 54-93, 97, 100-127, 130-137, 141, 144-160, 163-179, 183-195, 198-215, 218-234
src\gui\widgets\contabilita\helpers.py                                  32     26    19%   10-30, 33-40, 43-48
src\gui\widgets\contabilita\year_tab.py                                 95     76    20%   25-26, 30-31, 34-51, 73-93, 96-134, 138, 142-163, 167-196, 200, 204
src\gui\widgets\data_table.py                                          106     82    23%   48-52, 55-125, 132-133, 136-161, 164-170, 174-182, 185-187, 191-206, 213
src\gui\widgets\excel_table.py                                         325    284    13%   45-57, 61-68, 72-89, 93-113, 116-117, 120-121, 125-136, 140-162, 166-188, 192-209, 213-231, 235-244, 247-252, 255-259, 262-266, 275-277, 280-301, 304-359, 362-365, 368-374, 377-409, 412-415, 418-420, 423, 427-444, 453-463, 467-507, 512-537
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 87     87     0%   1-119
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        60     11    82%   66-67, 73-76, 80-83, 144
src\gui\widgets\notification_card.py                                   218    187    14%   86-92, 96-338, 342-352, 356, 360-362, 376-407, 411-427, 431-435, 439-441, 445-446, 450-454, 459-460, 464-499, 503-507, 511-516
src\gui\widgets\notification_group_header.py                            46     36    22%   32-38, 42-123, 127-130, 134-135, 139, 143-144
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                103     78    24%   34-46, 50-62, 66-68, 72-76, 80-99, 131-137, 141-226, 231-232, 236-237, 242-249, 253-254, 263-265, 269, 273, 277
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        74     59    20%   22-30, 234-235, 238-261, 265-306, 311-349, 354
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      243    243     0%   1-432
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     189    154    19%   43-68, 71-78, 81-114, 117-130, 133-138, 141-150, 153-154, 157-159, 164-169, 172-185, 190-197, 203-213, 216-229, 232-237, 240-244, 255-271, 274, 277, 282-307
src\gui\widgets\toast.py                                               129     98    24%   58-78, 82-121, 125-148, 151-155, 159-161, 165-166, 169-181, 192-194, 204-230, 235, 240, 245, 250
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70     70     0%   6-228
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         54     39    28%   14-15, 24-30, 35-49, 54-58, 63-77
src\utils\helpers.py                                                    90     61    32%   29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 201-223, 232, 238-241
src\utils\log_humanizer.py                                              42     30    29%   13-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     19    64%   14, 17, 21, 32-33, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     37    53%   43-44, 54-58, 81-83, 102-112, 116-138
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23137  17865    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_search.py::TestContabilitaSearch::test_fmt_date_invalid
============================== 1 failed in 4.23s ==============================

```
</details>

---
### `tests/unit/test_date_utils.py::TestDateUtils::test_parse_datetime_flexible`
**Error:** `FAILED tests/unit/test_date_utils.py::TestDateUtils::test_parse_datetime_flexible`

**Timestamp:** `2026-02-07T22:38:27.815619`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_date_utils.py F                                          [100%]

================================== FAILURES ===================================
_________________ TestDateUtils.test_parse_datetime_flexible __________________
tests\unit\test_date_utils.py:32: in test_parse_datetime_flexible
    assert parse_datetime_flexible("2024-01-15 14:30:00") == datetime(
E   AssertionError: assert datetime.datetime(2024, 1, 15, 14, 30, tzinfo=datetime.timezone.utc) == datetime.datetime(2024, 1, 15, 14, 30)
E    +  where datetime.datetime(2024, 1, 15, 14, 30, tzinfo=datetime.timezone.utc) = parse_datetime_flexible('2024-01-15 14:30:00')
E    +  and   datetime.datetime(2024, 1, 15, 14, 30) = datetime(2024, 1, 15, 14, 30, 0)
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              260    203    22%   52-72, 87, 92-94, 106-110, 121-137, 141, 145, 149, 153-154, 158-159, 164-180, 184-227, 231-253, 257-259, 266-271, 275-302, 314-363, 367-399, 404-413, 417-421, 425-427, 431, 435-441, 452-464, 468-471
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    166     0%   14-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     30    36%   20, 25, 31, 52, 56, 60-72, 77-100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          80     58    28%   21, 26, 31, 38, 42, 51-54, 60-67, 71-91, 95-106, 117-135, 139-144
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   39-42, 46, 50-52, 65-90, 101-114, 118-147, 151-158, 182-277, 281-299, 309-335, 339-348, 352-361, 365-376
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-103, 107-128
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         218    190    13%   28-31, 35, 39-41, 53-79, 90-95, 100-105, 109-137, 141-174, 178-186, 195-223, 227-234, 238-258, 262-274, 278-290, 294-312, 316-340, 344-348
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           218    181    17%   40, 45, 50, 57, 61, 73-76, 80-82, 86-99, 103-120, 124-139, 143-165, 169-196, 200-209, 213-238, 242-274, 280-309, 313-322, 326-341, 345-366, 371-381
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            70     50    29%   21, 26, 31, 36, 39-43, 47-60, 66-109, 116
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-85, 89-148, 152-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       175    148    15%   45-46, 50-79, 83-84, 91-110, 116-145, 155-166, 176-183, 186-214, 221-257, 260-275, 280-320, 323-358, 362-376, 383-384
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           387    343    11%   25, 30, 35, 40, 45, 56-60, 64, 68, 72-97, 101-160, 164-168, 172-200, 204-233, 237-245, 249-283, 287-315, 319-332, 336-364, 368-403, 407-421, 425-446, 450-462, 469-507, 510-550, 554-573
src\bots\safework\pdl\search_bot.py                                    179    154    14%   19-20, 24, 28, 32-90, 94-111, 115-132, 136-145, 149-159, 163-168, 172-197, 201-226, 230-300
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82     82     0%   5-156
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     39    61%   61-63, 78-79, 110-112, 114-117, 119-122, 124-126, 128-132, 144-145, 149-154, 157-163
src\core\audit\integrity.py                                             15      2    87%   21, 26
src\core\audit\manager.py                                              139     68    51%   46, 50, 58-63, 170, 174-177, 183-200, 204-231, 241, 244-247, 255-283
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      0   100%
src\core\backup_manager.py                                             138    105    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-188, 199-207, 212-223, 228-250
src\core\bug_reporter.py                                               157    157     0%   11-339
src\core\config_manager.py                                             237    114    52%   35, 87, 97-98, 109-115, 131-148, 156-170, 179-180, 199-200, 222, 232, 247, 279, 296-297, 300, 307-317, 326-353, 360, 367-369, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        101     53    48%   29, 34, 39, 48-60, 77-124, 133-140, 149-154, 163-170, 175, 180, 185, 190, 195, 200, 209, 217, 222
src\core\contabilita_queries.py                                         86     52    40%   18-29, 35, 46-47, 53, 76-77, 82-93, 98-109, 114-125
src\core\contabilita_search.py                                          91      8    91%   51-52, 78-79, 109-110, 125-126
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101     13    87%   78, 106-108, 118, 137-138, 144, 158-159, 178, 198, 213, 233
src\core\data_synchronizer.py                                          158      0   100%
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           120     10    92%   166-171, 184-185, 211-213
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      3    73%   62-64
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          65     48    26%   42-59, 63-77, 81-97, 101-115
src\core\importers\base.py                                              58     36    38%   15-16, 23-25, 35-37, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      135    109    19%   40-57, 68-104, 111-128, 133-187, 192-210, 215-239, 244-247
src\core\importers\giornaliere.py                                      190    155    18%   42-63, 73-91, 101-120, 126-145, 149-187, 191-206, 210-232, 236-288, 292-308
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    153     0%   6-290
src\core\license_validator.py                                          179    179     0%   6-352
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             52     22    58%   29-30, 38-39, 43-44, 52, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             66     33    50%   92, 112, 118, 121, 125, 142-156, 169-175, 193-194, 203-212
src\core\logging\formatters.py                                          82     25    70%   84, 88-90, 122, 125, 130, 132, 134, 136, 138, 168, 206-216, 225, 231-241
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 147-148, 161-165, 169-174, 179-180, 199, 205, 213, 217, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     16    70%   58, 67, 91, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                               99     75    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-205, 217-219, 225-227, 233-235
src\core\logging\viewer.py                                             175    142    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 149, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    110    12%   21-37, 55-69, 73-74, 78-106, 110-141, 150-205, 214-252
src\core\lyra_sentinel.py                                               29     29     0%   6-50
src\core\notification_manager.py                                        95     68    28%   29-35, 38-45, 49-57, 61-74, 78-82, 101-146, 150-152, 156, 160-167, 171-180, 184-187, 191-194
src\core\oda_manager.py                                                 34     20    41%   23, 31-91, 100-115
src\core\report_history.py                                              65     43    34%   25-27, 35-40, 45-49, 60-84, 94, 112-132, 145-155
src\core\schemas.py                                                     77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                                             94     51    46%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 122-126, 133-134, 139-145
src\core\stats_manager.py                                               46     10    78%   40-44, 47, 60, 62, 75, 82
src\core\sync_tracker.py                                                58     36    38%   26-39, 44-48, 61-73, 78-79, 87-105
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         97     75    23%   26-66, 71-81, 86-91, 96-103, 109-143, 148-156, 161-163
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   20-54, 57-65, 68-81, 90-108, 117-142, 145-149, 152, 168-173, 176-180, 183-208, 211-216, 219-224, 227-228, 231-256, 259-264
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-133, 136-150, 153-156, 159-166, 169-172, 175-177, 180-182, 185-211, 214-230, 233-235, 238-263
src\gui\controllers\bot_controller.py                                   39     14    64%   25-33, 64-72
src\gui\controllers\navigation_controller.py                           152    113    26%   41-57, 61-78, 81-95, 98-101, 104-107, 110-113, 116-119, 122-125, 128-131, 134-137, 140-143, 146-149, 152-155, 159-165, 169-173, 177-182, 194-230, 235-236, 257-259, 263-264, 268-269, 273-306, 310-311
src\gui\controllers\search_controller.py                               196    162    17%   16-42, 57, 67-68, 72-82, 86-95, 99-108, 112-121, 125-139, 143-187, 191-234, 238-280, 284-303
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  57     45    21%   25-29, 32-112, 115-117
src\gui\dialogs\bug_report_dialog.py                                   229    229     0%   10-477
src\gui\dialogs\command_palette.py                                     301    301     0%   1-512
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-76, 79-87, 90-98, 103-104, 108-109, 113-114, 118-119
src\gui\dialogs\quick_actions_config.py                                 80      0   100%
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-65, 70, 82-88, 92-95, 99, 102, 105, 108-133, 136-138, 141-144, 148-227
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-330
src\gui\main_window\components\status_bar.py                           157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-443
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          129    104    19%   29-32, 41-43, 46, 49, 52-76, 80-98, 102-112, 116-123, 127-131, 135-143, 147-149, 152-154, 157-162, 165-169, 173-185, 188-190
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 198    142    28%   52-56, 60-77, 89-93, 97-99, 124-132, 136-180, 187, 191-202, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-311, 321-323, 327-340, 344, 348-363, 370-373, 377-382, 386-389
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-105, 109-117, 121-122, 126-180
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-61, 68-76, 79-82, 86-90, 93-154, 157-211, 214-276, 279-318, 321-367
src\gui\panels\contabilita_kpi\kpi_panel.py                            150    131    13%   35-41, 44-162, 175-179, 182-195, 198-208, 211, 214-297
src\gui\panels\contabilita_panel.py                                    246    210    15%   39-46, 50-56, 60-160, 164-171, 175, 179, 202-219, 223-244, 249-274, 278-280, 284-287, 291-312, 316-332, 335-336, 339-343, 346-361, 364-366, 369-386, 390, 393-412
src\gui\panels\dashboard_panel.py                                      159     71    55%   85, 131-133, 140, 142, 145-147, 152-153, 155-165, 182-185, 192-195, 198, 206-209, 213-224, 228-234, 238-253, 257-279, 283-289
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-90, 93-95, 99, 102-114, 117-127, 130-132, 136-142, 145-221, 225-231
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     368    330    10%   55-86, 89-219, 223-257, 261-274, 277-305, 308-350, 354-362, 366-380, 383-392, 396-427, 430-462, 465-505, 508-548, 551, 555-638, 641-646, 652-681
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         53     46    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    152    127    16%   24-50, 55-98, 107-193, 198-209, 214-236, 241-298
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         289    257    11%   31-34, 38, 42-43, 46-52, 55-61, 64-95, 109-112, 115-153, 156-157, 164-165, 168-219, 222, 230, 242-256, 259-426, 430-475, 480-523, 527-555, 559-564, 568-571
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-32, 36-47, 51-54
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-122, 125-130, 133-140, 143-144, 147-148, 151-153, 156-161, 164-166, 169-178, 181-182, 185-188, 191-193, 197, 200-212
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 45-46, 49-57
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-150, 153-157, 161-163, 167-169, 173-175, 179-180, 184-185, 189, 192-196, 201-236, 241-264, 268-294, 302-310, 314-315, 319-337, 341-373, 377-379, 383-402, 406-445
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-46, 50-63, 67-68
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-147, 151-205, 208-214, 218-247, 251-263, 267-299, 303-341, 345-347, 351-352, 356-363, 367-373, 377-395, 399-471, 475-479, 483-494, 498-522, 526-567
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-77, 81-83, 86-94, 97-103, 106-108, 112-183
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-274, 277-285, 288-291, 294-307, 310-315, 319, 322-324, 328-336, 341-347, 350-384, 388-400, 404-426, 430-444, 448-455, 459-489, 493-495, 499, 503-517, 521-523
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-79, 83-85, 89, 93-106, 110-118, 122-124, 128-133, 147-149, 155-211
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              54     39    28%   25-27, 30-104, 113-115, 118-120
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                247    217    12%   42-105, 108-167, 171-179, 183-282, 285-296, 299, 302, 305-309, 312-318, 322-340, 344-402, 405-410, 413-433, 437-457
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-62, 70-110, 114-129, 133-134
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         66     66     0%   6-122
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       134     22    84%   38-39, 87-89, 145-146, 166-176, 183, 187-189, 262, 268, 279, 281
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     19    87%   169-195, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197     77    61%   55, 58, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 241, 248, 257, 266, 275, 293-297, 301-305
src\gui\widgets\bot_parameters.py                                      108     85    21%   39-43, 46-108, 118-125, 129, 148-150, 154-162, 167, 171-173, 177-179, 189-194, 198, 202-203
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            205    172    16%   53-55, 59-129, 132, 135-150, 154-168, 171-182, 185-191, 194-199, 202-220, 223-226, 230-236, 239-242, 245-248, 251-254, 257-260, 263-267, 270-281, 284-289
src\gui\widgets\contabilita\certificati_tab.py                         557    505     9%   43-45, 48-237, 241-267, 271-341, 345-458, 503-508, 512-516, 520-524, 532-697, 701-702, 706-715, 720-724, 728-732, 736, 740-875, 884-906, 912-949, 954-965, 969-977, 981-984, 988-991, 995-1005, 1008-1077, 1081-1083, 1087-1089, 1093-1129, 1136-1141, 1146-1186
src\gui\widgets\contabilita\giornaliere_tab.py                         167    136    19%   47-50, 54-93, 97, 100-127, 130-137, 141, 144-160, 163-179, 183-195, 198-215, 218-234
src\gui\widgets\contabilita\helpers.py                                  32     17    47%   20-30, 38-40, 43-48
src\gui\widgets\contabilita\year_tab.py                                 95     76    20%   25-26, 30-31, 34-51, 73-93, 96-134, 138, 142-163, 167-196, 200, 204
src\gui\widgets\data_table.py                                          106      0   100%
src\gui\widgets\excel_table.py                                         325    284    13%   45-57, 61-68, 72-89, 93-113, 116-117, 120-121, 125-136, 140-162, 166-188, 192-209, 213-231, 235-244, 247-252, 255-259, 262-266, 275-277, 280-301, 304-359, 362-365, 368-374, 377-409, 412-415, 418-420, 423, 427-444, 453-463, 467-507, 512-537
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 87     87     0%   1-119
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        60     35    42%   40-52, 56-58, 62, 66-67, 73-76, 80-83, 87-88, 98-103, 107-146
src\gui\widgets\notification_card.py                                   218    187    14%   86-92, 96-338, 342-352, 356, 360-362, 376-407, 411-427, 431-435, 439-441, 445-446, 450-454, 459-460, 464-499, 503-507, 511-516
src\gui\widgets\notification_group_header.py                            46     36    22%   32-38, 42-123, 127-130, 134-135, 139, 143-144
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                103     78    24%   34-46, 50-62, 66-68, 72-76, 80-99, 131-137, 141-226, 231-232, 236-237, 242-249, 253-254, 263-265, 269, 273, 277
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        74     13    82%   265-306, 320, 348-349
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      243    243     0%   1-432
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     189    154    19%   43-68, 71-78, 81-114, 117-130, 133-138, 141-150, 153-154, 157-159, 164-169, 172-185, 190-197, 203-213, 216-229, 232-237, 240-244, 255-271, 274, 277, 282-307
src\gui\widgets\toast.py                                               129     98    24%   58-78, 82-121, 125-148, 151-155, 159-161, 165-166, 169-181, 192-194, 204-230, 235, 240, 245, 250
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70      7    90%   55, 65, 222-228
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         54     39    28%   14-15, 24-30, 35-49, 54-58, 63-77
src\utils\helpers.py                                                    90     60    33%   29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 201-223, 238-241
src\utils\log_humanizer.py                                              42     26    38%   19-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     23    71%   43-44, 81-83, 103, 105, 110-112, 117, 123-138
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23524  17916    24%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_date_utils.py::TestDateUtils::test_parse_datetime_flexible
============================== 1 failed in 4.52s ==============================

```
</details>

---
### `tests/unit/test_date_utils_robust.py::TestDateUtilsRobust::test_calculate_days_diff`
**Error:** `FAILED tests/unit/test_date_utils_robust.py::TestDateUtilsRobust::test_calculate_days_diff`

**Timestamp:** `2026-02-07T22:40:06.515117`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_date_utils_robust.py F                                   [100%]

================================== FAILURES ===================================
________________ TestDateUtilsRobust.test_calculate_days_diff _________________
tests\unit\test_date_utils_robust.py:66: in test_calculate_days_diff
    assert res == 9
E   assert 768 == 9
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      21     21     0%   6-142
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                260    260     0%   6-474
src\bots\base\login_page.py                               94     94     0%   6-154
src\bots\base\wait_helpers.py                            166    166     0%   14-473
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               82     82     0%   5-156
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit\__init__.py                                 3      3     0%   1-4
src\core\audit\database.py                                99     99     0%   1-163
src\core\audit\integrity.py                               15     15     0%   1-26
src\core\audit\manager.py                                139    139     0%   1-283
src\core\audit\models.py                                   9      9     0%   1-13
src\core\audit\signals.py                                 27     27     0%   1-40
src\core\audit_manager.py                                  5      5     0%   6-11
src\core\auth_monitor.py                                  72     72     0%   6-131
src\core\backup_manager.py                               138    138     0%   6-250
src\core\bug_reporter.py                                 157    157     0%   11-339
src\core\config_manager.py                               237    194    18%   35, 67, 75-90, 95-117, 122-123, 128-148, 153-170, 179-180, 188-200, 205-206, 211-232, 237-247, 252, 257-259, 264, 269-284, 289-302, 307-317, 326-353, 358-362, 367-369, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                     96     96     0%   6-134
src\core\contabilita_manager.py                          101    101     0%   6-222
src\core\contabilita_queries.py                           86     86     0%   6-125
src\core\contabilita_search.py                            91     91     0%   6-180
src\core\contabilita_stats.py                             59     59     0%   6-99
src\core\contabilita_worker.py                           101    101     0%   1-233
src\core\data_synchronizer.py                            158    158     0%   6-320
src\core\database\__init__.py                              2      2     0%   1-3
src\core\database\manager.py                             120    120     0%   6-216
src\core\employees.py                                     98     98     0%   1-196
src\core\excel_importer.py                                 4      4     0%   6-11
src\core\importers\__init__.py                            44     44     0%   1-106
src\core\importers\attivita.py                            65     65     0%   1-115
src\core\importers\base.py                                58     58     0%   1-86
src\core\importers\certificati.py                        116    116     0%   1-187
src\core\importers\contabilita.py                        135    135     0%   1-247
src\core\importers\giornaliere.py                        190    190     0%   1-308
src\core\importers\scarico_ore.py                        186    186     0%   1-311
src\core\importers\storico_oda.py                         81     81     0%   1-185
src\core\license_updater.py                              153    153     0%   6-290
src\core\license_validator.py                            179    179     0%   6-352
src\core\logging\__init__.py                              10     10     0%   6-37
src\core\logging\alert_manager.py                        114    114     0%   7-239
src\core\logging\analytics.py                            136    136     0%   7-343
src\core\logging\config.py                                36     36     0%   5-85
src\core\logging\context.py                               52     52     0%   5-156
src\core\logging\decorators.py                            64     64     0%   5-184
src\core\logging\filters.py                               66     66     0%   5-212
src\core\logging\formatters.py                            82     82     0%   5-241
src\core\logging\logger.py                               109    109     0%   5-298
src\core\logging\metadata.py                              86     86     0%   5-199
src\core\logging\metrics.py                               98     98     0%   5-297
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              54     54     0%   5-201
src\core\logging\sinks.py                                 99     99     0%   5-235
src\core\logging\viewer.py                               175    175     0%   5-420
src\core\lyra_client.py                                  125    125     0%   6-252
src\core\lyra_sentinel.py                                 29     29     0%   6-50
src\core\notification_manager.py                          95     95     0%   6-194
src\core\oda_manager.py                                   34     34     0%   6-115
src\core\report_history.py                                65     65     0%   7-155
src\core\schemas.py                                       77     77     0%   1-107
src\core\secrets_manager.py                               94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                 46     46     0%   6-82
src\core\sync_tracker.py                                  58     58     0%   1-105
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             174    174     0%   1-313
src\core\telegram_bridge.py                              343    343     0%   1-531
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           97     97     0%   6-163
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\design\colors.py                                  27      1    96%   105
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                    57     57     0%   1-117
src\gui\dialogs\bug_report_dialog.py                     229    229     0%   10-477
src\gui\dialogs\command_palette.py                       301    301     0%   1-512
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-119
src\gui\dialogs\quick_actions_config.py                   80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                        232    232     0%   6-390
src\gui\formatters.py                                    127    127     0%   1-227
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                73     73     0%   1-330
src\gui\main_window\components\status_bar.py             157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                25     25     0%   1-43
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-52
src\gui\main_window\main.py                              279    279     0%   1-443
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   198    198     0%   6-389
src\gui\panels\carico_ts.py                               90     90     0%   6-180
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 197    197     0%   1-367
src\gui\panels\contabilita_kpi\kpi_panel.py              150    150     0%   1-297
src\gui\panels\contabilita_panel.py                      246    246     0%   6-412
src\gui\panels\dashboard_panel.py                        159    159     0%   1-289
src\gui\panels\dettagli_oda.py                           135    135     0%   6-231
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py               158    158     0%   1-334
src\gui\panels\health_panel.py                           289    289     0%   8-571
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          32     32     0%   1-54
src\gui\panels\lyra\header.py                             36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        146    146     0%   1-212
src\gui\panels\lyra\workers.py                            37     37     0%   1-57
src\gui\panels\notifications_panel.py                    253    253     0%   6-445
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                     45     45     0%   1-68
src\gui\panels\pdl\pdl_filter_widget.py                   67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                          334    334     0%   6-567
src\gui\panels\prenota_bp.py                             105    105     0%   6-183
src\gui\panels\ricerca_pdl.py                             79     79     0%   6-152
src\gui\panels\scarico_ore_panel.py                      299    299     0%   7-520
src\gui\panels\scarico_pdl.py                            296    296     0%   6-523
src\gui\panels\scarico_ts.py                             122    122     0%   6-211
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py             46     46     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py           41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                  247    247     0%   6-457
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       158    158     0%   1-285
src\gui\panels\timbrature_bot.py                         116    116     0%   6-200
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      0   100%
src\gui\styles\constants.py                                8      0   100%
src\gui\styles\theme_manager.py                           66     50    24%   25-28, 33, 40-50, 54-91, 96-117, 122
src\gui\styles\widget_styles.py                           35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         134    134     0%   1-313
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-180
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                   67     67     0%   1-164
src\gui\widgets\autopilot\main_widget.py                 197    197     0%   6-349
src\gui\widgets\bot_parameters.py                        108    108     0%   6-203
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            106    106     0%   5-213
src\gui\widgets\excel_table.py                           325    325     0%   6-537
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   87     87     0%   1-119
src\gui\widgets\footer\components.py                      48     48     0%   1-87
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                       52     52     0%   1-66
src\gui\widgets\info_widgets.py                           89     89     0%   6-175
src\gui\widgets\message_bubble.py                         53     53     0%   7-127
src\gui\widgets\modern_button.py                          60     60     0%   5-146
src\gui\widgets\notification_card.py                     218    218     0%   6-516
src\gui\widgets\notification_group_header.py              46     46     0%   6-144
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  103    103     0%   6-277
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          74     74     0%   1-354
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        243    243     0%   1-432
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       189    189     0%   6-307
src\gui\widgets\toast.py                                 129    129     0%   5-250
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-295
src\utils\date_utils.py                                   70      1    99%   55
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           54     54     0%   6-77
src\utils\helpers.py                                      90     71    21%   22-24, 29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 201-223, 231-249
src\utils\log_humanizer.py                                42     42     0%   6-119
src\utils\parsing.py                                      53     53     0%   6-119
src\utils\printing.py                                     83     83     0%   1-141
src\utils\resource_manager.py                             56     56     0%   6-91
src\utils\secure_logger.py                                23     23     0%   5-70
src\utils\security.py                                     79     79     0%   6-142
src\utils\system_telemetry.py                             26     26     0%   6-74
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  16913  16656     2%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_date_utils_robust.py::TestDateUtilsRobust::test_calculate_days_diff
============================== 1 failed in 3.15s ==============================

```
</details>

---
### `tests/unit/test_document_processor_advanced.py::TestDocumentProcessorAdvanced::test_extract_text_success`
**Error:** `FAILED tests/unit/test_document_processor_advanced.py::TestDocumentProcessorAdvanced::test_extract_text_success`

**Timestamp:** `2026-02-07T22:41:51.631714`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_document_processor_advanced.py F                         [100%]

================================== FAILURES ===================================
___________ TestDocumentProcessorAdvanced.test_extract_text_success ___________
tests\unit\test_document_processor_advanced.py:30: in test_extract_text_success
    assert "Pagina 1" in text
E   AssertionError: assert 'Pagina 1' in ''
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              260    181    30%   87, 92-94, 106-110, 122, 135-137, 141, 145, 149, 153-154, 159, 164-180, 184-227, 231-253, 257-259, 266-271, 275-302, 314-363, 367-399, 404-413, 417-421, 425-427, 431, 435-441, 452-464, 468-471
src\bots\base\login_page.py                                             94     77    18%   35-38, 44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          166    166     0%   14-473
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             47     30    36%   20, 25, 31, 52, 56, 60-72, 77-100
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          80     15    81%   21, 26, 31, 42, 61, 64, 75, 101, 106, 122-123, 125-126, 135, 142
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205     61    70%   50-52, 87-90, 101-114, 128-130, 144-147, 218, 233-241, 258-262, 271-277, 298-299, 315-316, 322, 327-330, 333-335, 344-345, 347-348, 361
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-94, 98-103, 107-128
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         218    190    13%   28-31, 35, 39-41, 53-79, 90-95, 100-105, 109-137, 141-174, 178-186, 195-223, 227-234, 238-258, 262-274, 278-290, 294-312, 316-340, 344-348
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           218    181    17%   40, 45, 50, 57, 61, 73-76, 80-82, 86-99, 103-120, 124-139, 143-165, 169-196, 200-209, 213-238, 242-274, 280-309, 313-322, 326-341, 345-366, 371-381
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            70     50    29%   21, 26, 31, 36, 39-43, 47-60, 66-109, 116
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-85, 89-148, 152-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       175    148    15%   45-46, 50-79, 83-84, 91-110, 116-145, 155-166, 176-183, 186-214, 221-257, 260-275, 280-320, 323-358, 362-376, 383-384
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           387    343    11%   25, 30, 35, 40, 45, 56-60, 64, 68, 72-97, 101-160, 164-168, 172-200, 204-233, 237-245, 249-283, 287-315, 319-332, 336-364, 368-403, 407-421, 425-446, 450-462, 469-507, 510-550, 554-573
src\bots\safework\pdl\search_bot.py                                    179    154    14%   19-20, 24, 28, 32-90, 94-111, 115-132, 136-145, 149-159, 163-168, 172-197, 201-226, 230-300
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             82     82     0%   5-156
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      3     0%   1-4
src\core\audit\database.py                                              99     99     0%   1-163
src\core\audit\integrity.py                                             15     15     0%   1-26
src\core\audit\manager.py                                              139    139     0%   1-283
src\core\audit\models.py                                                 9      9     0%   1-13
src\core\audit\signals.py                                               27     27     0%   1-40
src\core\audit_manager.py                                                5      5     0%   6-11
src\core\auth_monitor.py                                                72     72     0%   6-131
src\core\backup_manager.py                                             138    138     0%   6-250
src\core\bug_reporter.py                                               157    157     0%   11-339
src\core\config_manager.py                                             237    194    18%   35, 67, 75-90, 95-117, 122-123, 128-148, 153-170, 179-180, 188-200, 205-206, 211-232, 237-247, 252, 257-259, 264, 269-284, 289-302, 307-317, 326-353, 358-362, 367-369, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        101    101     0%   6-222
src\core\contabilita_queries.py                                         86     86     0%   6-125
src\core\contabilita_search.py                                          91     91     0%   6-180
src\core\contabilita_stats.py                                           59     59     0%   6-99
src\core\contabilita_worker.py                                         101    101     0%   1-233
src\core\data_synchronizer.py                                          158    132    16%   18-22, 27-30, 37-54, 59-69, 75-102, 108-146, 154-191, 199-234, 238, 248, 263-320
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           120     52    57%   104, 123-134, 141-171, 184-185, 188, 199-213
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     98     0%   1-196
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44      9    80%   33, 50, 62, 73, 77, 88, 104-106
src\core\importers\attivita.py                                          65     48    26%   42-59, 63-77, 81-97, 101-115
src\core\importers\base.py                                              58     36    38%   15-16, 23-25, 35-37, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      135    109    19%   40-57, 68-104, 111-128, 133-187, 192-210, 215-239, 244-247
src\core\importers\giornaliere.py                                      190    155    18%   42-63, 73-91, 101-120, 126-145, 149-187, 191-206, 210-232, 236-288, 292-308
src\core\importers\scarico_ore.py                                      186    151    19%   14-15, 21-23, 50-88, 96-114, 118-135, 149-180, 184-251, 255-264, 281-283, 287-311
src\core\importers\storico_oda.py                                       81     57    30%   62-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            153    153     0%   6-290
src\core\license_validator.py                                          179    179     0%   6-352
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239
src\core\logging\analytics.py                                          136     89    35%   50, 54, 68-73, 77-81, 90-116, 125-152, 161-191, 204-205, 209-211, 220-237, 260-281, 294-322, 333, 338, 343
src\core\logging\config.py                                              36      2    94%   70-72
src\core\logging\context.py                                             52     22    58%   29-30, 34, 38-39, 43-44, 52, 79-96, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             66     35    47%   92, 112, 118, 121, 124-127, 142-156, 169-175, 193-194, 203-212
src\core\logging\formatters.py                                          82     22    73%   84, 88-90, 122, 125, 132, 138, 168, 206-216, 225, 231-241
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 147-148, 161-165, 169-174, 179-180, 199, 205, 213, 217, 221, 232, 249, 293-298
src\core\logging\metadata.py                                            86     86     0%   5-199
src\core\logging\metrics.py                                             98     69    30%   24-27, 31, 47-51, 60-61, 78-105, 123-125, 128-130, 147-157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291, 297
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     16    70%   58, 67, 91, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                               99     75    24%   21-25, 50-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-205, 217-219, 225-227, 233-235
src\core\logging\viewer.py                                             175    142    19%   20-23, 27-28, 33-42, 47-52, 56, 60, 65-77, 81-82, 86-87, 91-92, 96-119, 123-134, 149, 161-168, 177-184, 196-218, 231-253, 265-270, 284-337, 347-383, 397, 410, 420
src\core\lyra_client.py                                                125    125     0%   6-252
src\core\lyra_sentinel.py                                               29     29     0%   6-50
src\core\notification_manager.py                                        95     95     0%   6-194
src\core\oda_manager.py                                                 34     13    62%   31-91, 110-115
src\core\report_history.py                                              65     65     0%   7-155
src\core\schemas.py                                                     77     27    65%   65-70, 75-86, 91-93, 98-100, 105-107
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               46     46     0%   6-82
src\core\sync_tracker.py                                                58     36    38%   26-39, 44-48, 61-73, 78-79, 87-105
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\service.py                                           174    174     0%   1-313
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         97     75    23%   26-66, 71-81, 86-91, 96-103, 109-143, 148-156, 161-163
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\design\colors.py                                                27      1    96%   105
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                                  57     57     0%   1-117
src\gui\dialogs\bug_report_dialog.py                                   229    229     0%   10-477
src\gui\dialogs\command_palette.py                                     301    301     0%   1-512
src\gui\dialogs\confirmation_dialog.py                                  84     84     0%   1-119
src\gui\dialogs\quick_actions_config.py                                 80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                                37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    127     0%   1-227
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-330
src\gui\main_window\components\status_bar.py                           157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-443
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 198    198     0%   6-389
src\gui\panels\carico_ts.py                                             90     90     0%   6-180
src\gui\panels\contabilita_kpi\__init__.py                               2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py                             14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                               197    197     0%   1-367
src\gui\panels\contabilita_kpi\kpi_panel.py                            150    150     0%   1-297
src\gui\panels\contabilita_panel.py                                    246    246     0%   6-412
src\gui\panels\dashboard_panel.py                                      159    159     0%   1-289
src\gui\panels\dettagli_oda.py                                         135    135     0%   6-231
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py                             158    158     0%   1-334
src\gui\panels\health_panel.py                                         289    289     0%   8-571
src\gui\panels\help_panel.py                                           120    120     0%   6-368
src\gui\panels\lyra\__init__.py                                          2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                                        32     32     0%   1-54
src\gui\panels\lyra\header.py                                           36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                                        41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                                      146    146     0%   1-212
src\gui\panels\lyra\workers.py                                          37     37     0%   1-57
src\gui\panels\notifications_panel.py                                  253    253     0%   6-445
src\gui\panels\pdl\__init__.py                                           2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                                      13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     45     0%   1-68
src\gui\panels\pdl\pdl_filter_widget.py                                 67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                                        334    334     0%   6-567
src\gui\panels\prenota_bp.py                                           105    105     0%   6-183
src\gui\panels\ricerca_pdl.py                                           79     79     0%   6-152
src\gui\panels\scarico_ore_panel.py                                    299    299     0%   7-520
src\gui\panels\scarico_pdl.py                                          296    296     0%   6-523
src\gui\panels\scarico_ts.py                                           122    122     0%   6-211
src\gui\panels\storico_oda\__init__.py                                   2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                              39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     46     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                                247    247     0%   6-457
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     158    158     0%   1-285
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-200
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         66     50    24%   25-28, 33, 40-50, 54-91, 96-117, 122
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12     12     0%   6-24
src\gui\widgets\activity_feed.py                                       134    134     0%   1-313
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                                    102    102     0%   7-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                              141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                                 67     67     0%   1-164
src\gui\widgets\autopilot\main_widget.py                               197    197     0%   6-349
src\gui\widgets\bot_parameters.py                                      108    108     0%   6-203
src\gui\widgets\calendar_date_edit.py                                   16     16     0%   6-79
src\gui\widgets\data_table.py                                          106    106     0%   5-213
src\gui\widgets\excel_table.py                                         325    325     0%   6-537
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 87     87     0%   1-119
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     89     0%   6-175
src\gui\widgets\message_bubble.py                                       53     53     0%   7-127
src\gui\widgets\modern_button.py                                        60     60     0%   5-146
src\gui\widgets\notification_card.py                                   218    218     0%   6-516
src\gui\widgets\notification_group_header.py                            46     46     0%   6-144
src\gui\widgets\notification_item.py                                    70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                                103    103     0%   6-277
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        74     74     0%   1-354
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      243    243     0%   1-432
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     45     0%   1-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-229
src\gui\widgets\status_card.py                                          59     59     0%   1-131
src\gui\widgets\status_indicator.py                                     42     42     0%   6-68
src\gui\widgets\timeline_widget.py                                     189    189     0%   6-307
src\gui\widgets\toast.py                                               129    129     0%   5-250
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 70      3    96%   55, 65, 116
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         54     16    70%   14-15, 40-47, 57-58, 65-66, 75-77
src\utils\helpers.py                                                    90     64    29%   22-24, 29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 202, 221, 231-249
src\utils\log_humanizer.py                                              42     42     0%   6-119
src\utils\parsing.py                                                    53     53     0%   6-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           56     56     0%   6-91
src\utils\secure_logger.py                                              23     10    57%   46-53, 56-59
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                19019  16993    11%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_document_processor_advanced.py::TestDocumentProcessorAdvanced::test_extract_text_success
============================== 1 failed in 4.21s ==============================

```
</details>

---
### `tests/unit/test_document_processor_coverage.py::TestDocumentProcessorCoverage::test_extract_text_success`
**Error:** `FAILED tests/unit/test_document_processor_coverage.py::TestDocumentProcessorCoverage::test_extract_text_success`

**Timestamp:** `2026-02-07T22:43:37.720353`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_document_processor_coverage.py F                         [100%]

================================== FAILURES ===================================
___________ TestDocumentProcessorCoverage.test_extract_text_success ___________
tests\unit\test_document_processor_coverage.py:29: in test_extract_text_success
    assert text == "Pagina 1Pagina 2"
E   AssertionError: assert '' == 'Pagina 1Pagina 2'
E
E     - Pagina 1Pagina 2
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      21     21     0%   6-142
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                260    260     0%   6-474
src\bots\base\login_page.py                               94     94     0%   6-154
src\bots\base\wait_helpers.py                            166    166     0%   14-473
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               82     82     0%   5-156
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit\__init__.py                                 3      3     0%   1-4
src\core\audit\database.py                                99     99     0%   1-163
src\core\audit\integrity.py                               15     15     0%   1-26
src\core\audit\manager.py                                139    139     0%   1-283
src\core\audit\models.py                                   9      9     0%   1-13
src\core\audit\signals.py                                 27     27     0%   1-40
src\core\audit_manager.py                                  5      5     0%   6-11
src\core\auth_monitor.py                                  72     72     0%   6-131
src\core\backup_manager.py                               138    138     0%   6-250
src\core\bug_reporter.py                                 157    157     0%   11-339
src\core\config_manager.py                               237    194    18%   35, 67, 75-90, 95-117, 122-123, 128-148, 153-170, 179-180, 188-200, 205-206, 211-232, 237-247, 252, 257-259, 264, 269-284, 289-302, 307-317, 326-353, 358-362, 367-369, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                     96     96     0%   6-134
src\core\contabilita_manager.py                          101    101     0%   6-222
src\core\contabilita_queries.py                           86     86     0%   6-125
src\core\contabilita_search.py                            91     91     0%   6-180
src\core\contabilita_stats.py                             59     59     0%   6-99
src\core\contabilita_worker.py                           101    101     0%   1-233
src\core\data_synchronizer.py                            158    158     0%   6-320
src\core\database\__init__.py                              2      2     0%   1-3
src\core\database\manager.py                             120    120     0%   6-216
src\core\employees.py                                     98     98     0%   1-196
src\core\excel_importer.py                                 4      4     0%   6-11
src\core\importers\__init__.py                            44     44     0%   1-106
src\core\importers\attivita.py                            65     65     0%   1-115
src\core\importers\base.py                                58     58     0%   1-86
src\core\importers\certificati.py                        116    116     0%   1-187
src\core\importers\contabilita.py                        135    135     0%   1-247
src\core\importers\giornaliere.py                        190    190     0%   1-308
src\core\importers\scarico_ore.py                        186    186     0%   1-311
src\core\importers\storico_oda.py                         81     81     0%   1-185
src\core\license_updater.py                              153    153     0%   6-290
src\core\license_validator.py                            179    179     0%   6-352
src\core\logging\__init__.py                              10     10     0%   6-37
src\core\logging\alert_manager.py                        114    114     0%   7-239
src\core\logging\analytics.py                            136    136     0%   7-343
src\core\logging\config.py                                36     36     0%   5-85
src\core\logging\context.py                               52     52     0%   5-156
src\core\logging\decorators.py                            64     64     0%   5-184
src\core\logging\filters.py                               66     66     0%   5-212
src\core\logging\formatters.py                            82     82     0%   5-241
src\core\logging\logger.py                               109    109     0%   5-298
src\core\logging\metadata.py                              86     86     0%   5-199
src\core\logging\metrics.py                               98     98     0%   5-297
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              54     54     0%   5-201
src\core\logging\sinks.py                                 99     99     0%   5-235
src\core\logging\viewer.py                               175    175     0%   5-420
src\core\lyra_client.py                                  125    125     0%   6-252
src\core\lyra_sentinel.py                                 29     29     0%   6-50
src\core\notification_manager.py                          95     95     0%   6-194
src\core\oda_manager.py                                   34     34     0%   6-115
src\core\report_history.py                                65     65     0%   7-155
src\core\schemas.py                                       77     77     0%   1-107
src\core\secrets_manager.py                               94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                 46     46     0%   6-82
src\core\sync_tracker.py                                  58     58     0%   1-105
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             174    174     0%   1-313
src\core\telegram_bridge.py                              343    343     0%   1-531
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           97     97     0%   6-163
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                    57     57     0%   1-117
src\gui\dialogs\bug_report_dialog.py                     229    229     0%   10-477
src\gui\dialogs\command_palette.py                       301    301     0%   1-512
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-119
src\gui\dialogs\quick_actions_config.py                   80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                        232    232     0%   6-390
src\gui\formatters.py                                    127    127     0%   1-227
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                73     73     0%   1-330
src\gui\main_window\components\status_bar.py             157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                25     25     0%   1-43
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-52
src\gui\main_window\main.py                              279    279     0%   1-443
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   198    198     0%   6-389
src\gui\panels\carico_ts.py                               90     90     0%   6-180
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 197    197     0%   1-367
src\gui\panels\contabilita_kpi\kpi_panel.py              150    150     0%   1-297
src\gui\panels\contabilita_panel.py                      246    246     0%   6-412
src\gui\panels\dashboard_panel.py                        159    159     0%   1-289
src\gui\panels\dettagli_oda.py                           135    135     0%   6-231
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py               158    158     0%   1-334
src\gui\panels\health_panel.py                           289    289     0%   8-571
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          32     32     0%   1-54
src\gui\panels\lyra\header.py                             36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        146    146     0%   1-212
src\gui\panels\lyra\workers.py                            37     37     0%   1-57
src\gui\panels\notifications_panel.py                    253    253     0%   6-445
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                     45     45     0%   1-68
src\gui\panels\pdl\pdl_filter_widget.py                   67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                          334    334     0%   6-567
src\gui\panels\prenota_bp.py                             105    105     0%   6-183
src\gui\panels\ricerca_pdl.py                             79     79     0%   6-152
src\gui\panels\scarico_ore_panel.py                      299    299     0%   7-520
src\gui\panels\scarico_pdl.py                            296    296     0%   6-523
src\gui\panels\scarico_ts.py                             122    122     0%   6-211
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py             46     46     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py           41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                  247    247     0%   6-457
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       158    158     0%   1-285
src\gui\panels\timbrature_bot.py                         116    116     0%   6-200
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-156
src\gui\styles\theme_manager.py                           66     66     0%   6-122
src\gui\styles\widget_styles.py                           35     35     0%   6-391
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         134    134     0%   1-313
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-180
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                   67     67     0%   1-164
src\gui\widgets\autopilot\main_widget.py                 197    197     0%   6-349
src\gui\widgets\bot_parameters.py                        108    108     0%   6-203
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            106    106     0%   5-213
src\gui\widgets\excel_table.py                           325    325     0%   6-537
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   87     87     0%   1-119
src\gui\widgets\footer\components.py                      48     48     0%   1-87
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                       52     52     0%   1-66
src\gui\widgets\info_widgets.py                           89     89     0%   6-175
src\gui\widgets\message_bubble.py                         53     53     0%   7-127
src\gui\widgets\modern_button.py                          60     60     0%   5-146
src\gui\widgets\notification_card.py                     218    218     0%   6-516
src\gui\widgets\notification_group_header.py              46     46     0%   6-144
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  103    103     0%   6-277
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          74     74     0%   1-354
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        243    243     0%   1-432
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       189    189     0%   6-307
src\gui\widgets\toast.py                                 129    129     0%   5-250
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-295
src\utils\date_utils.py                                   70     70     0%   6-228
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           54      9    83%   14-15, 46-47, 57-58, 75-77
src\utils\helpers.py                                      90     71    21%   22-24, 29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 201-223, 231-249
src\utils\log_humanizer.py                                42     42     0%   6-119
src\utils\parsing.py                                      53     53     0%   6-119
src\utils\printing.py                                     83     83     0%   1-141
src\utils\resource_manager.py                             56     56     0%   6-91
src\utils\secure_logger.py                                23     23     0%   5-70
src\utils\security.py                                     79     79     0%   6-142
src\utils\system_telemetry.py                             26     26     0%   6-74
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  16886  16735     1%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_document_processor_coverage.py::TestDocumentProcessorCoverage::test_extract_text_success
============================== 1 failed in 3.80s ==============================

```
</details>

---
### `tests/unit/test_excel_importer.py::TestExcelImporter::test_import_contabilita_dati_success`
**Error:** `FAILED tests/unit/test_excel_importer.py::TestExcelImporter::test_import_contabilita_dati_success`

**Timestamp:** `2026-02-07T22:45:01.333179`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_excel_importer.py F                                      [100%]

================================== FAILURES ===================================
___________ TestExcelImporter.test_import_contabilita_dati_success ____________
tests\unit\test_excel_importer.py:56: in test_import_contabilita_dati_success
    assert success
E   assert False
------------------------------ Captured log call ------------------------------
WARNING  src.core.importers.contabilita:contabilita.py:186 Errore processamento foglio Dati 2024: Expected numeric dtype, got object instead.
============================== warnings summary ===============================
tests/unit/test_excel_importer.py::TestExcelImporter::test_import_contabilita_dati_success
  C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\src\core\importers\contabilita.py:145: SettingWithCopyWarning:
  A value is trying to be set on a copy of a slice from a DataFrame

  See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    df.dropna(how="all", inplace=True)

tests/unit/test_excel_importer.py::TestExcelImporter::test_import_contabilita_dati_success
  C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\src\core\importers\contabilita.py:150: SettingWithCopyWarning:
  A value is trying to be set on a copy of a slice from a DataFrame.
  Try using .loc[row_indexer,col_indexer] = value instead

  See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    df["year"] = year

tests/unit/test_excel_importer.py::TestExcelImporter::test_import_contabilita_dati_success
  C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\src\core\importers\contabilita.py:232: SettingWithCopyWarning:
  A value is trying to be set on a copy of a slice from a DataFrame

  See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    df.rename(columns=rename_map, inplace=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      21     21     0%   6-142
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                260    260     0%   6-474
src\bots\base\login_page.py                               94     94     0%   6-154
src\bots\base\wait_helpers.py                            166    166     0%   14-473
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               82     82     0%   5-156
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit\__init__.py                                 3      3     0%   1-4
src\core\audit\database.py                                99     99     0%   1-163
src\core\audit\integrity.py                               15     15     0%   1-26
src\core\audit\manager.py                                139    139     0%   1-283
src\core\audit\models.py                                   9      9     0%   1-13
src\core\audit\signals.py                                 27     27     0%   1-40
src\core\audit_manager.py                                  5      5     0%   6-11
src\core\auth_monitor.py                                  72     72     0%   6-131
src\core\backup_manager.py                               138    138     0%   6-250
src\core\bug_reporter.py                                 157    157     0%   11-339
src\core\config_manager.py                               237    171    28%   35, 77, 87, 97-98, 109-115, 131-148, 156-170, 179-180, 188-200, 205-206, 211-232, 237-247, 252, 257-259, 264, 269-284, 289-302, 307-317, 326-353, 358-362, 367-369, 374-376, 381-390, 399-417, 425-466
src\core\constants.py                                     96     96     0%   6-134
src\core\contabilita_manager.py                          101     53    48%   29, 34, 39, 48-60, 77-124, 133-140, 149-154, 163-170, 175, 180, 185, 190, 195, 200, 209, 217, 222
src\core\contabilita_queries.py                           86     70    19%   18-29, 34-47, 52-77, 82-93, 98-109, 114-125
src\core\contabilita_search.py                            91     73    20%   25-81, 88-112, 117-126, 131-143, 150-162, 176-180
src\core\contabilita_stats.py                             59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                           101    101     0%   1-233
src\core\data_synchronizer.py                            158    132    16%   18-22, 27-30, 37-54, 59-69, 75-102, 108-146, 154-191, 199-234, 238, 248, 263-320
src\core\database\__init__.py                              2      0   100%
src\core\database\manager.py                             120     47    61%   104, 125-134, 161-171, 175-179, 182-185, 188, 194-213
src\core\database\migrations\contabilita.py               23      0   100%
src\core\database\migrations\dipendenti.py                17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                       19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py               11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                     98     13    87%   61-63, 118-120, 129-130, 174-175, 190-192
src\core\excel_importer.py                                 4      0   100%
src\core\importers\__init__.py                            44      1    98%   50
src\core\importers\attivita.py                            65     13    80%   44, 49, 53, 58-59, 68-77, 90-91, 94
src\core\importers\base.py                                58     13    78%   15-16, 23-25, 55-56, 70-74, 84-86
src\core\importers\certificati.py                        116     19    84%   38, 47, 51, 54-55, 64, 87-88, 105-106, 141, 166-167, 171, 177-181
src\core\importers\contabilita.py                        135     27    80%   40-57, 78, 102-104, 118, 126, 148, 229, 231, 236-237, 246
src\core\importers\giornaliere.py                        190    155    18%   42-63, 73-91, 101-120, 126-145, 149-187, 191-206, 210-232, 236-288, 292-308
src\core\importers\scarico_ore.py                        186     52    72%   14-15, 21-23, 52, 68-69, 75-88, 98, 101, 106, 113-114, 118-135, 174, 202, 206, 215, 219, 227, 232, 248, 257, 260, 282, 290
src\core\importers\storico_oda.py                         81     16    80%   60, 66, 71, 84-85, 95-96, 176-185
src\core\license_updater.py                              153    153     0%   6-290
src\core\license_validator.py                            179    179     0%   6-352
src\core\logging\__init__.py                              10     10     0%   6-37
src\core\logging\alert_manager.py                        114    114     0%   7-239
src\core\logging\analytics.py                            136    136     0%   7-343
src\core\logging\config.py                                36     36     0%   5-85
src\core\logging\context.py                               52     52     0%   5-156
src\core\logging\decorators.py                            64     64     0%   5-184
src\core\logging\filters.py                               66     66     0%   5-212
src\core\logging\formatters.py                            82     82     0%   5-241
src\core\logging\logger.py                               109    109     0%   5-298
src\core\logging\metadata.py                              86     86     0%   5-199
src\core\logging\metrics.py                               98     98     0%   5-297
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              54     54     0%   5-201
src\core\logging\sinks.py                                 99     99     0%   5-235
src\core\logging\viewer.py                               175    175     0%   5-420
src\core\lyra_client.py                                  125    125     0%   6-252
src\core\lyra_sentinel.py                                 29      5    83%   44-48
src\core\notification_manager.py                          95     44    54%   43, 51-57, 61-74, 81-82, 133-146, 150-152, 160-167, 171-180, 184-187, 191-194
src\core\oda_manager.py                                   34     34     0%   6-115
src\core\report_history.py                                65     65     0%   7-155
src\core\schemas.py                                       77     25    68%   65-70, 75-86, 91-93, 98-100, 106
src\core\secrets_manager.py                               94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                 46     46     0%   6-82
src\core\sync_tracker.py                                  58     36    38%   26-39, 44-48, 61-73, 78-79, 87-105
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             174    174     0%   1-313
src\core\telegram_bridge.py                              343    343     0%   1-531
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           97     97     0%   6-163
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                    57     57     0%   1-117
src\gui\dialogs\bug_report_dialog.py                     229    229     0%   10-477
src\gui\dialogs\command_palette.py                       301    301     0%   1-512
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-119
src\gui\dialogs\quick_actions_config.py                   80     80     0%   1-206
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                        232    232     0%   6-390
src\gui\formatters.py                                    127    127     0%   1-227
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                73     73     0%   1-330
src\gui\main_window\components\status_bar.py             157    157     0%   1-277
src\gui\main_window\components\tool_bar.py                25     25     0%   1-43
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-52
src\gui\main_window\main.py                              279    279     0%   1-443
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   198    198     0%   6-389
src\gui\panels\carico_ts.py                               90     90     0%   6-180
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 197    197     0%   1-367
src\gui\panels\contabilita_kpi\kpi_panel.py              150    150     0%   1-297
src\gui\panels\contabilita_panel.py                      246    246     0%   6-412
src\gui\panels\dashboard_panel.py                        159    159     0%   1-289
src\gui\panels\dettagli_oda.py                           135    135     0%   6-231
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py               158    158     0%   1-334
src\gui\panels\health_panel.py                           289    289     0%   8-571
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          32     32     0%   1-54
src\gui\panels\lyra\header.py                             36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        146    146     0%   1-212
src\gui\panels\lyra\workers.py                            37     37     0%   1-57
src\gui\panels\notifications_panel.py                    253    253     0%   6-445
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                     45     45     0%   1-68
src\gui\panels\pdl\pdl_filter_widget.py                   67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                          334    334     0%   6-567
src\gui\panels\prenota_bp.py                             105    105     0%   6-183
src\gui\panels\ricerca_pdl.py                             79     79     0%   6-152
src\gui\panels\scarico_ore_panel.py                      299    299     0%   7-520
src\gui\panels\scarico_pdl.py                            296    296     0%   6-523
src\gui\panels\scarico_ts.py                             122    122     0%   6-211
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py             46     46     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py           41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                  247    247     0%   6-457
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       158    158     0%   1-285
src\gui\panels\timbrature_bot.py                         116    116     0%   6-200
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-156
src\gui\styles\theme_manager.py                           66     66     0%   6-122
src\gui\styles\widget_styles.py                           35     35     0%   6-391
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         134    134     0%   1-313
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-180
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                   67     67     0%   1-164
src\gui\widgets\autopilot\main_widget.py                 197    197     0%   6-349
src\gui\widgets\bot_parameters.py                        108    108     0%   6-203
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            106    106     0%   5-213
src\gui\widgets\excel_table.py                           325    325     0%   6-537
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   87     87     0%   1-119
src\gui\widgets\footer\components.py                      48     48     0%   1-87
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                       52     52     0%   1-66
src\gui\widgets\info_widgets.py                           89     89     0%   6-175
src\gui\widgets\message_bubble.py                         53     53     0%   7-127
src\gui\widgets\modern_button.py                          60     60     0%   5-146
src\gui\widgets\notification_card.py                     218    218     0%   6-516
src\gui\widgets\notification_group_header.py              46     46     0%   6-144
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  103    103     0%   6-277
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          74     74     0%   1-354
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        243    243     0%   1-432
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       189    189     0%   6-307
src\gui\widgets\toast.py                                 129    129     0%   5-250
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-295
src\utils\date_utils.py                                   70     70     0%   6-228
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           54      7    87%   14-15, 57-58, 75-77
src\utils\helpers.py                                      90     71    21%   22-24, 29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 201-223, 231-249
src\utils\log_humanizer.py                                42     42     0%   6-119
src\utils\parsing.py                                      53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                     83     83     0%   1-141
src\utils\resource_manager.py                             56     56     0%   6-91
src\utils\secure_logger.py                                23     23     0%   5-70
src\utils\security.py                                     79     79     0%   6-142
src\utils\system_telemetry.py                             26     26     0%   6-74
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  16983  15741     7%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_excel_importer.py::TestExcelImporter::test_import_contabilita_dati_success
======================== 1 failed, 3 warnings in 4.62s ========================

```
</details>

---
