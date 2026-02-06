# 📊 Test Execution Report

**Date:** 2026-02-06 12:49:11
**Duration:** 48.77s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1483 |
| ✅ Passed | 670 |
| ❌ Failed | 25 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_bot_panels_deep_dive.py::TestScaricoPDLPanel::test_telegram_send_after_finish`
**Error:** `FAILED tests/unit/test_bot_panels_deep_dive.py::TestScaricoPDLPanel::test_telegram_send_after_finish`

**Timestamp:** `2026-02-06T11:41:57.831071`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_____________ TestScaricoPDLPanel.test_telegram_send_after_finish _____________
C:\Program Files\Python312\Lib\unittest\mock.py:918: in assert_called
    raise AssertionError(msg)
E   AssertionError: Expected 'send_document_sync' to have been called.

During handling of the above exception, another exception occurred:
tests\unit\test_bot_panels_deep_dive.py:296: in test_telegram_send_after_finish
    mock_win.telegram.send_document_sync.assert_called()
E   AssertionError: Expected 'send_document_sync' to have been called.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263     37    86%   76, 82, 230-232, 258, 279, 368-371, 384, 413-414, 420-428, 433-436, 441-442, 451-458, 478-480, 501
src\bots\base\login_page.py                                             94     69    27%   46-62, 66-96, 100-116, 132-179
src\bots\base\wait_helpers.py                                          168    145    14%   18, 24-26, 50-57, 78-83, 102-106, 137-209, 232, 261-342, 344-358, 361-362, 364-368, 389-394, 397-405, 435-451, 481-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     28    42%   52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    130    37%   52-54, 67-98, 109-128, 132-167, 171-180, 244, 263-271, 290-294, 305-311, 315-335, 350-379, 383-384, 388-394, 398-411, 417, 422-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    182    16%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112, 116-144, 150, 153-189, 193-195, 198-203, 212-242, 246-253, 257-259, 263-277, 281-285, 289-293, 297-311, 315-321, 323-335, 339-345, 347-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    185    18%   57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     44    58%   45-46, 73-75, 107-109, 115-154, 160-185, 191-200
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    133    18%   42, 46-61, 68-87, 91-150, 154-219, 224-251, 256-268, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    114    36%   45, 84, 89, 96-119, 125-154, 166-175, 189-192, 203-225, 232-268, 273-280, 282-288, 295-298, 302-303, 310, 314-315, 320-321, 334-335, 341-346, 369-373, 377, 386-388, 390-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    340    13%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 300-331, 336-347, 352-379, 384-421, 425-428, 433-445, 449-453, 456-470, 474-478, 482-488, 495-538, 541-582, 586-594, 597-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84      0   100%
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 173-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              139     11    92%   50, 62-63, 178-181, 205-206, 241, 292
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71      0   100%
src\core\backup_manager.py                                             137     22    84%   59-61, 68, 85, 95, 110-112, 117, 124, 180-189, 216, 222-224, 231, 249-250
src\core\bug_reporter.py                                               157    125    20%   60-111, 116-147, 152-162, 167-189, 194-214, 219-242, 247-300, 305-317, 328-344
src\core\config_manager.py                                             242    112    54%   35, 87, 113-119, 140, 145-146, 160-174, 183-184, 203-204, 226, 230-233, 250-251, 273, 276, 279-281, 285-287, 293-306, 311-321, 330-357, 366, 371, 378-380, 387, 392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     43    58%   29, 34, 39, 48-60, 77-129, 144-147, 162-165, 180-183, 188, 193, 198, 203, 208, 213, 237
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         101     79    22%   22-27, 31-62, 66-80, 101-127, 131-152, 158-167, 178-187, 198-207, 213-222, 228-233
src\core\data_synchronizer.py                                          159    124    22%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 170, 176-209, 223-229, 234-237, 246-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     63    47%   103, 124-135, 144-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     34    41%   15-16, 23-25, 35-37, 42-57, 63-74, 79-81, 84-86
src\core\importers\certificati.py                                      115     86    25%   35-54, 59-63, 70-74, 79-94, 101-123, 130-139, 146-150, 157-184
src\core\importers\contabilita.py                                      133    105    21%   38-55, 66-106, 113-130, 135-202, 207-218, 225-249, 256-257
src\core\importers\giornaliere.py                                      190    142    25%   39-57, 60, 70-88, 100-112, 117, 123-137, 142, 148-168, 185-186, 190-200, 205-207, 211-230, 235, 239-274, 289-291, 295-315
src\core\importers\scarico_ore.py                                      186    147    21%   12-13, 19-21, 46-86, 95-112, 117-134, 148, 162-179, 197-242, 246-251, 255, 272-276, 280-285, 288-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 219-239, 244-252, 257-275, 280-288, 292-295
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 79-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     42    69%   52, 56, 79-83, 102, 135-144, 167-197, 234-236, 272-279, 283, 287
src\core\logging\config.py                                              39      1    97%   74
src\core\logging\context.py                                             52      7    87%   29-30, 52, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 118, 147-184
src\core\logging\filters.py                                             64     32    50%   92, 112, 120, 127, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84      8    90%   84, 125, 168, 198, 234-244
src\core\logging\logger.py                                             109      9    92%   84, 96, 168-169, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     49    52%   79-109, 161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-274, 276, 290-299
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              102     61    40%   55, 72-73, 77-80, 93-106, 118-122, 132-139, 143-159, 171-172, 182-188, 200-210, 230-232, 238-240
src\core\logging\viewer.py                                             182    138    24%   20-22, 27, 33-41, 47-54, 70-83, 88, 93, 98, 103-127, 131-143, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    107    15%   21-37, 55-69, 73-74, 79-108, 113-145, 155-210, 221-257
src\core\lyra_sentinel.py                                               29      9    69%   23, 30, 38-41, 45-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             94     41    56%   31-51, 57-59, 65-73, 79, 85-87, 105-107, 113-117, 123, 126, 132-134, 145
src\core\stats_manager.py                                               47     16    66%   40-45, 48, 61, 63, 71-79, 83
src\core\sync_tracker.py                                                59     26    56%   32-39, 47-49, 64, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    133    24%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 237-249, 253-265, 269-280, 284-296, 300-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    289    16%   29-31, 35-44, 48-66, 70-73, 77-84, 88-95, 98-125, 128-151, 154-159, 163-177, 180-196, 201-204, 207-208, 211-219, 222-230, 233-258, 262-287, 290-294, 297-302, 306-323, 326-334, 337-350, 353-366, 370-375, 379-385, 389-397, 401-427, 431-444, 448-455, 460-466, 469-496, 499-511, 514-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    150    18%   22-56, 61-73, 78-91, 102-118, 129-156, 159, 161-163, 182-183, 185-187, 190-191, 193-194, 197-198, 201-222, 225-226, 228-230, 233-234, 236-238, 241-242, 245-246, 248-270, 273-274, 276-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\controllers\bot_controller.py                                   39     30    23%   18-21, 25-33, 37-40, 47-60, 64-72
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           155    125    19%   37-38, 42-58, 62-79, 82-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 157-160, 164-170, 174-178, 182-187, 199-241, 245-261, 265-267, 271-272, 276-277, 281-314, 318-319
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-46, 50-52, 56-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\controllers\service_controller.py                              203    176    13%   29-41, 49-66, 74-132, 139-167, 171-338, 350-353, 372-380, 393-432, 445-463, 473, 476-484
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    207    10%   52-56, 59-68, 75-80, 83-234, 238-246, 249-279, 284-310, 314-320, 324-473, 477-495
src\gui\dialogs\command_palette.py                                     301    268    11%   41-71, 76-188, 193-218, 222-229, 233-237, 240-245, 248-255, 258-298, 302-311, 314-323, 326-332, 335-341, 345-349, 353-367, 371-382, 385-392, 397-401, 404-448, 451-487, 491-507, 510-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127     62    51%   13, 21-25, 35-66, 96, 118-120, 136, 163-215, 225-227, 232-233
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     55    25%   18-23, 27-33, 39-53, 57-68, 73-82, 86-336
src\gui\main_window\components\status_bar.py                           158    141    11%   25-29, 32-104, 108-113, 117-130, 134-146, 150-211, 215-282
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-43
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 29-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            279    177    37%   46-95, 99-135, 147-152, 155-179, 182-188, 192, 195, 198, 201, 204, 207, 210, 213, 217-256, 263-284, 290-293, 302-305, 314-317, 326-329, 338-339, 343-344, 348-349, 355-356, 362-363, 367-370, 374-386, 390-391, 395-414, 418-420, 426-428, 432-437, 441-442, 447-448, 459-460
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          128     23    82%   56, 101, 114-115, 125, 131, 133, 143-145, 167-168, 173-175, 183, 185, 187, 190-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200     27    86%   60-77, 89-93, 214, 226, 235, 255-257, 382-385, 395, 402
src\gui\panels\carico_ts.py                                             90     23    74%   42-44, 99, 103-107, 113, 117, 123-124, 132-138, 142-149, 165-166
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-63, 70-78, 81-84, 88-92, 95-158, 161-217, 220-284, 287-328, 331-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            150    131    13%   35-41, 44-162, 175-179, 182-195, 198-208, 211, 214-297
src\gui\panels\contabilita_panel.py                                    245    200    18%   39-46, 50-56, 60-164, 168-175, 179, 183, 206-223, 227-248, 253-277, 281-283, 287-290, 294-315, 321, 323-339, 342-343, 347-349, 355-356, 361-374, 377-379, 382, 384-386, 389-399, 403, 406-407, 409-411, 414-425
src\gui\panels\dashboard_panel.py                                      159    135    15%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232, 235-238, 248-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135     74    45%   38-42, 95-97, 101, 104-116, 120, 136-138, 144, 146, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    247    15%   32-35, 39, 43-44, 47-53, 56-62, 66-100, 114-117, 135-162, 166, 174, 178-232, 256-269, 274-451, 455-502, 507-554, 560-590, 594-599, 603, 606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     63    20%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 151-152
src\gui\panels\scarico_ore_panel.py                                    299    252    16%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 397-401, 406-417, 422-432, 437, 442-449, 454-467, 472-490, 495-497, 502-520
src\gui\panels\scarico_pdl.py                                          296     87    71%   87-120, 143-145, 184, 281-289, 292-295, 301, 307-309, 314-325, 329, 332-334, 338-346, 351-357, 368-371, 376, 381, 401-407, 410-413, 457, 467, 517, 522, 533-534
src\gui\panels\scarico_ts.py                                           122     24    80%   38-40, 85-87, 106, 113, 128-130, 172-183, 193-197
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    251    21%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-273, 275-279, 282-283, 285-290, 293-294, 298-309, 312, 316-321, 324-325, 327-330, 335-336, 338-344, 347-348, 351-361, 364, 368-373, 376-377, 379-382, 387-388, 391, 394-395, 397, 400-401, 405-407, 410, 414-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-458, 460-464, 472-484
src\gui\panels\settings\pages\paths_page.py                            116     86    26%   26-27, 30-80, 85-86, 89-105, 107-110, 114-121, 153, 156, 162-163, 166-168, 171-173, 179-180, 184-185, 188-190, 195-202, 205-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     35    24%   19-21, 25-50, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    207    17%   47-106, 110-174, 178-188, 192-295, 299-309, 312, 315, 318, 320-322, 325, 327-331, 341-357, 364-423, 426, 428-431, 436, 438-458, 463-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     25    58%   74-118, 122-137
src\gui\panels\timbrature\components\settings_tab.py                    94      4    96%   147, 161-163
src\gui\panels\timbrature\panel.py                                     158     25    84%   223-241, 244-251, 265, 280-281, 285
src\gui\panels\timbrature_bot.py                                       116     35    70%   40-42, 62-64, 95, 106-111, 121-122, 134-142, 149-161, 184-186, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         68     51    25%   25-28, 33, 40-50, 54-97, 102-125
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     14    82%   94-103, 114-115, 127, 129, 131
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   38, 46-47
src\gui\widgets\audit_log_widget.py                                    102     13    87%   125-135, 138, 141, 178, 180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     10    93%   179, 183-195, 390, 394-406
src\gui\widgets\autopilot\event_card.py                                 67     11    84%   131-146, 162
src\gui\widgets\autopilot\main_widget.py                               197     25    87%   55, 58, 152, 178-179, 181-182, 221-228, 231-234, 241, 257, 275, 301-305
src\gui\widgets\bot_parameters.py                                      110      4    96%   154, 158-160
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            207    164    21%   53-55, 59-129, 132, 135-150, 154-172, 175-188, 191-199, 203-207, 211-228, 232-234, 242-250, 254-256, 260-262, 266-268, 272-274, 278-281, 285-299, 303-307
src\gui\widgets\contabilita\certificati_tab.py                         556    490    12%   58-186, 192, 198-275, 279-302, 305-307, 313-335, 339-382, 386-391, 395-409, 416-440, 450, 456-463, 477-516, 561-566, 570-574, 578-582, 590-757, 761-762, 766-775, 780-784, 788-792, 796, 800-941, 950-973, 981-1018, 1023-1034, 1038-1046, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    129    22%   46-48, 53-93, 101-129, 133-139, 147-165, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     73    22%   23-24, 28-29, 32-36, 38-49, 71-91, 94-95, 98-125, 127-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     82    23%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207
src\gui\widgets\excel_table.py                                         327    196    40%   47-59, 63-70, 74-91, 95-115, 119, 123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-260, 262-264, 267-268, 270-271, 274-275, 277-278, 318, 325-377, 386-387, 390-392, 421, 430-431, 433, 436-437, 513-517, 531-555
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   26-82, 85-92, 97-102, 105-109, 112-115, 119-125
src\gui\widgets\footer\components.py                                    48     33    31%   16-29, 32, 39-45, 48-55, 62-64, 67-68, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     27    23%   11-31, 34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     52     38    27%   18-50, 53-55, 58-59, 62-66
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      244    210    14%   15-22, 29-63, 67-71, 75, 78-79, 82-86, 89-101, 105-113, 125-150, 154-156, 160-162, 166-169, 173-196, 200-218, 221-390, 394, 398, 402, 406-407, 411-412, 420-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59      8    86%   106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191     42    78%   80-81, 83-84, 131-135, 137-141, 145, 148-153, 161-169, 172-173, 176-178, 191-205, 239-249
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     59    14%   32-43, 59-70, 84-90, 103-106, 122-126, 142-171, 187-236
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     21    68%   15-16, 25-34, 51-52, 70-72, 79-80, 90-92
src\utils\helpers.py                                                    90     41    54%   30-32, 53-72, 85-87, 119, 128, 141-143, 146-155, 169-170, 186, 189-192, 207, 226, 237, 246
src\utils\log_humanizer.py                                              41     14    66%   12-26, 112, 120
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     16    71%   16, 19-26, 45, 49, 65-67, 73, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           25     16    36%   46-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                24110  16163    33%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_bot_panels_deep_dive.py::TestScaricoPDLPanel::test_telegram_send_after_finish
1 failed in 20.86s

```
</details>

---
### `tests/unit/test_certificati_gui.py::TestCertificatiGUI::test_screenshot_generation_logic`
**Error:** `FAILED tests/unit/test_certificati_gui.py::TestCertificatiGUI::test_screenshot_generation_logic`

**Timestamp:** `2026-02-06T11:49:35.287363`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_____________ TestCertificatiGUI.test_screenshot_generation_logic _____________
tests\unit\test_certificati_gui.py:196: in test_screenshot_generation_logic
    assert mock_popen.called
E   AssertionError: assert False
E    +  where False = <MagicMock name='Popen' id='1825745102384'>.called
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263     26    90%   76, 82, 230-232, 258, 279, 384, 413-414, 428, 433-436, 441-442, 451-458, 478-480, 501
src\bots\base\login_page.py                                             94     58    38%   46-62, 66-96, 100-116, 141-142, 153-169, 174-179
src\bots\base\wait_helpers.py                                          168    145    14%   18, 24-26, 50-57, 78-83, 102-106, 137-209, 232, 261-342, 344-358, 361-362, 364-368, 389-394, 397-405, 435-451, 481-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     15    69%   56, 60-72, 86, 92, 95, 101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     12    78%   34-36, 49-51, 79-81, 118-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    130    37%   52-54, 67-98, 109-128, 132-167, 171-180, 244, 263-271, 290-294, 305-311, 315-335, 350-379, 383-384, 388-394, 398-411, 417, 422-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    182    16%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112, 116-144, 150, 153-189, 193-195, 198-203, 212-242, 246-253, 257-259, 263-277, 281-285, 289-293, 297-311, 315-321, 323-335, 339-345, 347-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    154    32%   61, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 274, 309-311, 317-354, 358-367, 387, 396-418, 423-433
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     44    58%   45-46, 73-75, 107-109, 115-154, 160-185, 191-200
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     47    36%   26, 31, 36, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163     99    39%   46-61, 85-87, 91-150, 169-170, 187-190, 193, 213-214, 218-219, 224-251, 256-268, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    111    37%   96-119, 125-154, 166-175, 189-192, 203-225, 232-268, 273-280, 282-288, 295-298, 302-303, 310, 314-315, 320-321, 334-335, 341-346, 369-373, 377, 386-388, 390-394, 403-404
src\bots\safework\base.py                                               40     17    58%   23, 42-45, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    297    24%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 257, 268-270, 273-275, 288-293, 300-331, 336-347, 352-379, 384-421, 425-428, 433-445, 449-453, 456-470, 474-478, 482-488, 496, 507, 512-538, 542, 575, 582, 586-594, 597-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84      0   100%
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 173-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              139     11    92%   50, 62-63, 178-181, 205-206, 241, 292
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71      0   100%
src\core\backup_manager.py                                             137     22    84%   59-61, 68, 85, 95, 110-112, 117, 124, 180-189, 216, 222-224, 231, 249-250
src\core\bug_reporter.py                                               157     38    76%   82, 86-87, 91-92, 96-97, 130-131, 136-139, 144-145, 187-189, 212-214, 219-242, 295-298, 308, 344
src\core\config_manager.py                                             242    111    54%   87, 113-119, 140, 145-146, 160-174, 183-184, 203-204, 226, 230-233, 250-251, 273, 276, 279-281, 285-287, 293-306, 311-321, 330-357, 366, 371, 378-380, 387, 392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     43    58%   29, 34, 39, 48-60, 77-129, 144-147, 162-165, 180-183, 188, 193, 198, 203, 208, 213, 237
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101     79    22%   22-27, 31-62, 66-80, 101-127, 131-152, 158-167, 178-187, 198-207, 213-222, 228-233
src\core\data_synchronizer.py                                          159    124    22%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 170, 176-209, 223-229, 234-237, 246-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     63    47%   103, 124-135, 144-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     34    41%   15-16, 23-25, 35-37, 42-57, 63-74, 79-81, 84-86
src\core\importers\certificati.py                                      115     86    25%   35-54, 59-63, 70-74, 79-94, 101-123, 130-139, 146-150, 157-184
src\core\importers\contabilita.py                                      133    105    21%   38-55, 66-106, 113-130, 135-202, 207-218, 225-249, 256-257
src\core\importers\giornaliere.py                                      190    142    25%   39-57, 60, 70-88, 100-112, 117, 123-137, 142, 148-168, 185-186, 190-200, 205-207, 211-230, 235, 239-274, 289-291, 295-315
src\core\importers\scarico_ore.py                                      186    147    21%   12-13, 19-21, 46-86, 95-112, 117-134, 148, 162-179, 197-242, 246-251, 255, 272-276, 280-285, 288-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 219-239, 244-252, 257-275, 280-288, 292-295
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 79-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     42    69%   52, 56, 79-83, 102, 135-144, 167-197, 234-236, 272-279, 283, 287
src\core\logging\config.py                                              39      1    97%   74
src\core\logging\context.py                                             52      7    87%   29-30, 52, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 118, 147-184
src\core\logging\filters.py                                             64     32    50%   92, 112, 120, 127, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84      8    90%   84, 125, 168, 198, 234-244
src\core\logging\logger.py                                             109      9    92%   84, 96, 168-169, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     49    52%   79-109, 161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-274, 276, 290-299
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              102     61    40%   55, 72-73, 77-80, 93-106, 118-122, 132-139, 143-159, 171-172, 182-188, 200-210, 230-232, 238-240
src\core\logging\viewer.py                                             182    138    24%   20-22, 27, 33-41, 47-54, 70-83, 88, 93, 98, 103-127, 131-143, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    107    15%   21-37, 55-69, 73-74, 79-108, 113-145, 155-210, 221-257
src\core\lyra_sentinel.py                                               29      9    69%   23, 30, 38-41, 45-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             94     41    56%   31-51, 57-59, 65-73, 79, 85-87, 105-107, 113-117, 123, 126, 132-134, 145
src\core\stats_manager.py                                               47     16    66%   40-45, 48, 61, 63, 71-79, 83
src\core\sync_tracker.py                                                59     26    56%   32-39, 47-49, 64, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    133    24%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 237-249, 253-265, 269-280, 284-296, 300-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    289    16%   29-31, 35-44, 48-66, 70-73, 77-84, 88-95, 98-125, 128-151, 154-159, 163-177, 180-196, 201-204, 207-208, 211-219, 222-230, 233-258, 262-287, 290-294, 297-302, 306-323, 326-334, 337-350, 353-366, 370-375, 379-385, 389-397, 401-427, 431-444, 448-455, 460-466, 469-496, 499-511, 514-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    150    18%   22-56, 61-73, 78-91, 102-118, 129-156, 159, 161-163, 182-183, 185-187, 190-191, 193-194, 197-198, 201-222, 225-226, 228-230, 233-234, 236-238, 241-242, 245-246, 248-270, 273-274, 276-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\controllers\bot_controller.py                                   39     30    23%   18-21, 25-33, 37-40, 47-60, 64-72
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           155    125    19%   37-38, 42-58, 62-79, 82-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 157-160, 164-170, 174-178, 182-187, 199-241, 245-261, 265-267, 271-272, 276-277, 281-314, 318-319
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-46, 50-52, 56-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\controllers\service_controller.py                              203    176    13%   29-41, 49-66, 74-132, 139-167, 171-338, 350-353, 372-380, 393-432, 445-463, 473, 476-484
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    207    10%   52-56, 59-68, 75-80, 83-234, 238-246, 249-279, 284-310, 314-320, 324-473, 477-495
src\gui\dialogs\command_palette.py                                     301    268    11%   41-71, 76-188, 193-218, 222-229, 233-237, 240-245, 248-255, 258-298, 302-311, 314-323, 326-332, 335-341, 345-349, 353-367, 371-382, 385-392, 397-401, 404-448, 451-487, 491-507, 510-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127     62    51%   13, 21-25, 35-66, 96, 118-120, 136, 163-215, 225-227, 232-233
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     55    25%   18-23, 27-33, 39-53, 57-68, 73-82, 86-336
src\gui\main_window\components\status_bar.py                           158    141    11%   25-29, 32-104, 108-113, 117-130, 134-146, 150-211, 215-282
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-43
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 29-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            279    177    37%   46-95, 99-135, 147-152, 155-179, 182-188, 192, 195, 198, 201, 204, 207, 210, 213, 217-256, 263-284, 290-293, 302-305, 314-317, 326-329, 338-339, 343-344, 348-349, 355-356, 362-363, 367-370, 374-386, 390-391, 395-414, 418-420, 426-428, 432-437, 441-442, 447-448, 459-460
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          128     23    82%   56, 101, 114-115, 125, 131, 133, 143-145, 167-168, 173-175, 183, 185, 187, 190-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200     27    86%   60-77, 89-93, 214, 226, 235, 255-257, 382-385, 395, 402
src\gui\panels\carico_ts.py                                             90     23    74%   42-44, 99, 103-107, 113, 117, 123-124, 132-138, 142-149, 165-166
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-63, 70-78, 81-84, 88-92, 95-158, 161-217, 220-284, 287-328, 331-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            150    131    13%   35-41, 44-162, 175-179, 182-195, 198-208, 211, 214-297
src\gui\panels\contabilita_panel.py                                    245    200    18%   39-46, 50-56, 60-164, 168-175, 179, 183, 206-223, 227-248, 253-277, 281-283, 287-290, 294-315, 321, 323-339, 342-343, 347-349, 355-356, 361-374, 377-379, 382, 384-386, 389-399, 403, 406-407, 409-411, 414-425
src\gui\panels\dashboard_panel.py                                      159    135    15%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232, 235-238, 248-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135     73    46%   38-42, 95-97, 101, 104-116, 120, 136-138, 146, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    247    15%   32-35, 39, 43-44, 47-53, 56-62, 66-100, 114-117, 135-162, 166, 174, 178-232, 256-269, 274-451, 455-502, 507-554, 560-590, 594-599, 603, 606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     63    20%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 151-152
src\gui\panels\scarico_ore_panel.py                                    299    252    16%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 397-401, 406-417, 422-432, 437, 442-449, 454-467, 472-490, 495-497, 502-520
src\gui\panels\scarico_pdl.py                                          296     79    73%   87-120, 143-145, 184, 281-289, 292-295, 301, 307-309, 329, 332-334, 338-346, 351-357, 368-371, 376, 381, 401-407, 410-413, 457, 467, 517, 522
src\gui\panels\scarico_ts.py                                           122     24    80%   38-40, 85-87, 106, 113, 128-130, 172-183, 193-197
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    251    21%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-273, 275-279, 282-283, 285-290, 293-294, 298-309, 312, 316-321, 324-325, 327-330, 335-336, 338-344, 347-348, 351-361, 364, 368-373, 376-377, 379-382, 387-388, 391, 394-395, 397, 400-401, 405-407, 410, 414-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-458, 460-464, 472-484
src\gui\panels\settings\pages\paths_page.py                            116     86    26%   26-27, 30-80, 85-86, 89-105, 107-110, 114-121, 153, 156, 162-163, 166-168, 171-173, 179-180, 184-185, 188-190, 195-202, 205-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     35    24%   19-21, 25-50, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    207    17%   47-106, 110-174, 178-188, 192-295, 299-309, 312, 315, 318, 320-322, 325, 327-331, 341-357, 364-423, 426, 428-431, 436, 438-458, 463-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     25    58%   74-118, 122-137
src\gui\panels\timbrature\components\settings_tab.py                    94      4    96%   147, 161-163
src\gui\panels\timbrature\panel.py                                     158     25    84%   223-241, 244-251, 265, 280-281, 285
src\gui\panels\timbrature_bot.py                                       116     35    70%   40-42, 62-64, 95, 106-111, 121-122, 134-142, 149-161, 184-186, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         68     51    25%   25-28, 33, 40-50, 54-97, 102-125
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     14    82%   94-103, 114-115, 127, 129, 131
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   38, 46-47
src\gui\widgets\audit_log_widget.py                                    102     13    87%   125-135, 138, 141, 178, 180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     10    93%   179, 183-195, 390, 394-406
src\gui\widgets\autopilot\event_card.py                                 67     11    84%   131-146, 162
src\gui\widgets\autopilot\main_widget.py                               197     25    87%   55, 58, 152, 178-179, 181-182, 221-228, 231-234, 241, 257, 275, 301-305
src\gui\widgets\bot_parameters.py                                      110      4    96%   154, 158-160
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            207    164    21%   53-55, 59-129, 132, 135-150, 154-172, 175-188, 191-199, 203-207, 211-228, 232-234, 242-250, 254-256, 260-262, 266-268, 272-274, 278-281, 285-299, 303-307
src\gui\widgets\contabilita\certificati_tab.py                         556    153    72%   199, 204-207, 359, 381, 463, 477-499, 515-516, 761-762, 773, 784, 792, 796, 820-822, 890, 904-907, 973, 982-984, 987-989, 995-1004, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    129    22%   46-48, 53-93, 101-129, 133-139, 147-165, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     73    22%   23-24, 28-29, 32-36, 38-49, 71-91, 94-95, 98-125, 127-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     82    23%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207
src\gui\widgets\excel_table.py                                         327    196    40%   47-59, 63-70, 74-91, 95-115, 119, 123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-260, 262-264, 267-268, 270-271, 274-275, 277-278, 318, 325-377, 386-387, 390-392, 421, 430-431, 433, 436-437, 513-517, 531-555
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   26-82, 85-92, 97-102, 105-109, 112-115, 119-125
src\gui\widgets\footer\components.py                                    48     33    31%   16-29, 32, 39-45, 48-55, 62-64, 67-68, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     27    23%   11-31, 34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     52     38    27%   18-50, 53-55, 58-59, 62-66
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      244    210    14%   15-22, 29-63, 67-71, 75, 78-79, 82-86, 89-101, 105-113, 125-150, 154-156, 160-162, 166-169, 173-196, 200-218, 221-390, 394, 398, 402, 406-407, 411-412, 420-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59      8    86%   106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191     42    78%   80-81, 83-84, 131-135, 137-141, 145, 148-153, 161-169, 172-173, 176-178, 191-205, 239-249
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     59    14%   32-43, 59-70, 84-90, 103-106, 122-126, 142-171, 187-236
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     21    68%   15-16, 25-34, 51-52, 70-72, 79-80, 90-92
src\utils\helpers.py                                                    90     41    54%   30-32, 53-72, 85-87, 119, 128, 141-143, 146-155, 169-170, 186, 189-192, 207, 226, 237, 246
src\utils\log_humanizer.py                                              41     14    66%   12-26, 112, 120
src\utils\parsing.py                                                    53     18    66%   14, 17, 21, 45-46, 62, 64, 79, 84-97, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     16    71%   16, 19-26, 45, 49, 65-67, 73, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           25     16    36%   46-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                24110  15475    36%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_certificati_gui.py::TestCertificatiGUI::test_screenshot_generation_logic
1 failed in 10.37s

```
</details>

---
### `tests/unit/test_contabilita_kpi_panel_deep.py::TestContabilitaKPIPanelDeep::test_load_kpi_data_and_plotting`
**Error:** `FAILED tests/unit/test_contabilita_kpi_panel_deep.py::TestContabilitaKPIPanelDeep::test_load_kpi_data_and_plotting`

**Timestamp:** `2026-02-06T11:54:03.512871`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestContabilitaKPIPanelDeep.test_load_kpi_data_and_plotting _________
tests\unit\test_contabilita_kpi_panel_deep.py:58: in test_load_kpi_data_and_plotting
    assert len(panel.fig1.axes) > 0
               ^^^^^^^^^^
E   AttributeError: 'ContabilitaKPIPanel' object has no attribute 'fig1'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263     26    90%   76, 82, 230-232, 258, 279, 384, 413-414, 428, 433-436, 441-442, 451-458, 478-480, 501
src\bots\base\login_page.py                                             94     58    38%   46-62, 66-96, 100-116, 141-142, 153-169, 174-179
src\bots\base\wait_helpers.py                                          168    145    14%   18, 24-26, 50-57, 78-83, 102-106, 137-209, 232, 261-342, 344-358, 361-362, 364-368, 389-394, 397-405, 435-451, 481-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     15    69%   56, 60-72, 86, 92, 95, 101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     12    78%   34-36, 49-51, 79-81, 118-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    130    37%   52-54, 67-98, 109-128, 132-167, 171-180, 244, 263-271, 290-294, 305-311, 315-335, 350-379, 383-384, 388-394, 398-411, 417, 422-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    182    16%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112, 116-144, 150, 153-189, 193-195, 198-203, 212-242, 246-253, 257-259, 263-277, 281-285, 289-293, 297-311, 315-321, 323-335, 339-345, 347-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    154    32%   61, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 274, 309-311, 317-354, 358-367, 387, 396-418, 423-433
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     44    58%   45-46, 73-75, 107-109, 115-154, 160-185, 191-200
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     47    36%   26, 31, 36, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163     99    39%   46-61, 85-87, 91-150, 169-170, 187-190, 193, 213-214, 218-219, 224-251, 256-268, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    111    37%   96-119, 125-154, 166-175, 189-192, 203-225, 232-268, 273-280, 282-288, 295-298, 302-303, 310, 314-315, 320-321, 334-335, 341-346, 369-373, 377, 386-388, 390-394, 403-404
src\bots\safework\base.py                                               40     17    58%   23, 42-45, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    297    24%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 257, 268-270, 273-275, 288-293, 300-331, 336-347, 352-379, 384-421, 425-428, 433-445, 449-453, 456-470, 474-478, 482-488, 496, 507, 512-538, 542, 575, 582, 586-594, 597-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84      0   100%
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 173-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              139     11    92%   50, 62-63, 178-181, 205-206, 241, 292
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71      0   100%
src\core\backup_manager.py                                             137     22    84%   59-61, 68, 85, 95, 110-112, 117, 124, 180-189, 216, 222-224, 231, 249-250
src\core\bug_reporter.py                                               157     38    76%   82, 86-87, 91-92, 96-97, 130-131, 136-139, 144-145, 187-189, 212-214, 219-242, 295-298, 308, 344
src\core\config_manager.py                                             242     38    84%   119, 140, 163, 226, 300-301, 330-357, 392, 401-420, 432, 441, 473-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     34    67%   29, 34, 39, 55, 77-129, 144-147, 162-165, 198, 203, 208, 213
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101     79    22%   22-27, 31-62, 66-80, 101-127, 131-152, 158-167, 178-187, 198-207, 213-222, 228-233
src\core\data_synchronizer.py                                          159    124    22%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 170, 176-209, 223-229, 234-237, 246-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     62    48%   124-135, 144-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      9    79%   32, 49, 63, 76, 80, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     31    47%   15-16, 23-25, 42-57, 63-74, 79-81, 84-86
src\core\importers\certificati.py                                      115     21    82%   37, 46, 50, 53-54, 63, 92, 106-107, 138, 147, 159, 163-164, 168, 171-176
src\core\importers\contabilita.py                                      133    105    21%   38-55, 66-106, 113-130, 135-202, 207-218, 225-249, 256-257
src\core\importers\giornaliere.py                                      190    142    25%   39-57, 60, 70-88, 100-112, 117, 123-137, 142, 148-168, 185-186, 190-200, 205-207, 211-230, 235, 239-274, 289-291, 295-315
src\core\importers\scarico_ore.py                                      186    147    21%   12-13, 19-21, 46-86, 95-112, 117-134, 148, 162-179, 197-242, 246-251, 255, 272-276, 280-285, 288-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 219-239, 244-252, 257-275, 280-288, 292-295
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 79-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     42    69%   52, 56, 79-83, 102, 135-144, 167-197, 234-236, 272-279, 283, 287
src\core\logging\config.py                                              39      1    97%   74
src\core\logging\context.py                                             52      7    87%   29-30, 52, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 118, 147-184
src\core\logging\filters.py                                             64     32    50%   92, 112, 120, 127, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84      8    90%   84, 125, 168, 198, 234-244
src\core\logging\logger.py                                             109      9    92%   84, 96, 168-169, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     49    52%   79-109, 161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-274, 276, 290-299
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              102     61    40%   55, 72-73, 77-80, 93-106, 118-122, 132-139, 143-159, 171-172, 182-188, 200-210, 230-232, 238-240
src\core\logging\viewer.py                                             182    138    24%   20-22, 27, 33-41, 47-54, 70-83, 88, 93, 98, 103-127, 131-143, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    107    15%   21-37, 55-69, 73-74, 79-108, 113-145, 155-210, 221-257
src\core\lyra_sentinel.py                                               29      9    69%   23, 30, 38-41, 45-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             94     37    61%   31-51, 57-59, 65-73, 79, 85-87, 107, 114-117, 123, 126, 133-134, 145
src\core\stats_manager.py                                               47     16    66%   40-45, 48, 61, 63, 71-79, 83
src\core\sync_tracker.py                                                59     26    56%   32-39, 47-49, 64, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    133    24%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 237-249, 253-265, 269-280, 284-296, 300-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    289    16%   29-31, 35-44, 48-66, 70-73, 77-84, 88-95, 98-125, 128-151, 154-159, 163-177, 180-196, 201-204, 207-208, 211-219, 222-230, 233-258, 262-287, 290-294, 297-302, 306-323, 326-334, 337-350, 353-366, 370-375, 379-385, 389-397, 401-427, 431-444, 448-455, 460-466, 469-496, 499-511, 514-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    150    18%   22-56, 61-73, 78-91, 102-118, 129-156, 159, 161-163, 182-183, 185-187, 190-191, 193-194, 197-198, 201-222, 225-226, 228-230, 233-234, 236-238, 241-242, 245-246, 248-270, 273-274, 276-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\controllers\bot_controller.py                                   39     30    23%   18-21, 25-33, 37-40, 47-60, 64-72
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           155    125    19%   37-38, 42-58, 62-79, 82-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 157-160, 164-170, 174-178, 182-187, 199-241, 245-261, 265-267, 271-272, 276-277, 281-314, 318-319
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-46, 50-52, 56-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\controllers\service_controller.py                              203    176    13%   29-41, 49-66, 74-132, 139-167, 171-338, 350-353, 372-380, 393-432, 445-463, 473, 476-484
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    207    10%   52-56, 59-68, 75-80, 83-234, 238-246, 249-279, 284-310, 314-320, 324-473, 477-495
src\gui\dialogs\command_palette.py                                     301    268    11%   41-71, 76-188, 193-218, 222-229, 233-237, 240-245, 248-255, 258-298, 302-311, 314-323, 326-332, 335-341, 345-349, 353-367, 371-382, 385-392, 397-401, 404-448, 451-487, 491-507, 510-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127     62    51%   13, 21-25, 35-66, 96, 118-120, 136, 163-215, 225-227, 232-233
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     55    25%   18-23, 27-33, 39-53, 57-68, 73-82, 86-336
src\gui\main_window\components\status_bar.py                           158    141    11%   25-29, 32-104, 108-113, 117-130, 134-146, 150-211, 215-282
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-43
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 29-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            279    177    37%   46-95, 99-135, 147-152, 155-179, 182-188, 192, 195, 198, 201, 204, 207, 210, 213, 217-256, 263-284, 290-293, 302-305, 314-317, 326-329, 338-339, 343-344, 348-349, 355-356, 362-363, 367-370, 374-386, 390-391, 395-414, 418-420, 426-428, 432-437, 441-442, 447-448, 459-460
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          128     23    82%   56, 101, 114-115, 125, 131, 133, 143-145, 167-168, 173-175, 183, 185, 187, 190-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200     27    86%   60-77, 89-93, 214, 226, 235, 255-257, 382-385, 395, 402
src\gui\panels\carico_ts.py                                             90     23    74%   42-44, 99, 103-107, 113, 117, 123-124, 132-138, 142-149, 165-166
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    200    18%   39-46, 50-56, 60-164, 168-175, 179, 183, 206-223, 227-248, 253-277, 281-283, 287-290, 294-315, 321, 323-339, 342-343, 347-349, 355-356, 361-374, 377-379, 382, 384-386, 389-399, 403, 406-407, 409-411, 414-425
src\gui\panels\dashboard_panel.py                                      159    135    15%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232, 235-238, 248-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135     73    46%   38-42, 95-97, 101, 104-116, 120, 136-138, 146, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    247    15%   32-35, 39, 43-44, 47-53, 56-62, 66-100, 114-117, 135-162, 166, 174, 178-232, 256-269, 274-451, 455-502, 507-554, 560-590, 594-599, 603, 606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     63    20%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 151-152
src\gui\panels\scarico_ore_panel.py                                    299    252    16%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 397-401, 406-417, 422-432, 437, 442-449, 454-467, 472-490, 495-497, 502-520
src\gui\panels\scarico_pdl.py                                          296     79    73%   87-120, 143-145, 184, 281-289, 292-295, 301, 307-309, 329, 332-334, 338-346, 351-357, 368-371, 376, 381, 401-407, 410-413, 457, 467, 517, 522
src\gui\panels\scarico_ts.py                                           122     24    80%   38-40, 85-87, 106, 113, 128-130, 172-183, 193-197
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    251    21%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-273, 275-279, 282-283, 285-290, 293-294, 298-309, 312, 316-321, 324-325, 327-330, 335-336, 338-344, 347-348, 351-361, 364, 368-373, 376-377, 379-382, 387-388, 391, 394-395, 397, 400-401, 405-407, 410, 414-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-458, 460-464, 472-484
src\gui\panels\settings\pages\paths_page.py                            116     86    26%   26-27, 30-80, 85-86, 89-105, 107-110, 114-121, 153, 156, 162-163, 166-168, 171-173, 179-180, 184-185, 188-190, 195-202, 205-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     35    24%   19-21, 25-50, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    207    17%   47-106, 110-174, 178-188, 192-295, 299-309, 312, 315, 318, 320-322, 325, 327-331, 341-357, 364-423, 426, 428-431, 436, 438-458, 463-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     25    58%   74-118, 122-137
src\gui\panels\timbrature\components\settings_tab.py                    94      4    96%   147, 161-163
src\gui\panels\timbrature\panel.py                                     158     25    84%   223-241, 244-251, 265, 280-281, 285
src\gui\panels\timbrature_bot.py                                       116     35    70%   40-42, 62-64, 95, 106-111, 121-122, 134-142, 149-161, 184-186, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         68     51    25%   25-28, 33, 40-50, 54-97, 102-125
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     14    82%   94-103, 114-115, 127, 129, 131
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   38, 46-47
src\gui\widgets\audit_log_widget.py                                    102     13    87%   125-135, 138, 141, 178, 180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     10    93%   179, 183-195, 390, 394-406
src\gui\widgets\autopilot\event_card.py                                 67     11    84%   131-146, 162
src\gui\widgets\autopilot\main_widget.py                               197     25    87%   55, 58, 152, 178-179, 181-182, 221-228, 231-234, 241, 257, 275, 301-305
src\gui\widgets\bot_parameters.py                                      110      4    96%   154, 158-160
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            207    164    21%   53-55, 59-129, 132, 135-150, 154-172, 175-188, 191-199, 203-207, 211-228, 232-234, 242-250, 254-256, 260-262, 266-268, 272-274, 278-281, 285-299, 303-307
src\gui\widgets\contabilita\certificati_tab.py                         556    146    74%   199, 204-207, 359, 381, 496-499, 515-516, 761-762, 773, 784, 792, 796, 820-822, 890, 904-907, 973, 982-984, 987-989, 995-1004, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    129    22%   46-48, 53-93, 101-129, 133-139, 147-165, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     73    22%   23-24, 28-29, 32-36, 38-49, 71-91, 94-95, 98-125, 127-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     82    23%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207
src\gui\widgets\excel_table.py                                         327    196    40%   47-59, 63-70, 74-91, 95-115, 119, 123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-260, 262-264, 267-268, 270-271, 274-275, 277-278, 318, 325-377, 386-387, 390-392, 421, 430-431, 433, 436-437, 513-517, 531-555
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   26-82, 85-92, 97-102, 105-109, 112-115, 119-125
src\gui\widgets\footer\components.py                                    48     33    31%   16-29, 32, 39-45, 48-55, 62-64, 67-68, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     27    23%   11-31, 34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     52     38    27%   18-50, 53-55, 58-59, 62-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      244    210    14%   15-22, 29-63, 67-71, 75, 78-79, 82-86, 89-101, 105-113, 125-150, 154-156, 160-162, 166-169, 173-196, 200-218, 221-390, 394, 398, 402, 406-407, 411-412, 420-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59      8    86%   106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191     42    78%   80-81, 83-84, 131-135, 137-141, 145, 148-153, 161-169, 172-173, 176-178, 191-205, 239-249
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     59    14%   32-43, 59-70, 84-90, 103-106, 122-126, 142-171, 187-236
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     21    68%   15-16, 25-34, 51-52, 70-72, 79-80, 90-92
src\utils\helpers.py                                                    90     41    54%   30-32, 53-72, 85-87, 119, 128, 141-143, 146-155, 169-170, 186, 189-192, 207, 226, 237, 246
src\utils\log_humanizer.py                                              41     14    66%   12-26, 112, 120
src\utils\parsing.py                                                    53     13    75%   14, 17, 21, 45-46, 62, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     16    71%   16, 19-26, 45, 49, 65-67, 73, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           25     16    36%   46-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                24110  14972    38%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_kpi_panel_deep.py::TestContabilitaKPIPanelDeep::test_load_kpi_data_and_plotting
1 failed in 15.94s

```
</details>

---
### `tests/unit/test_contabilita_kpi_panel_deep.py::TestContabilitaKPIPanelDeep::test_load_kpi_data_and_plotting`
**Error:** `FAILED tests/unit/test_contabilita_kpi_panel_deep.py::TestContabilitaKPIPanelDeep::test_load_kpi_data_and_plotting`

**Timestamp:** `2026-02-06T11:56:39.470226`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestContabilitaKPIPanelDeep.test_load_kpi_data_and_plotting _________
tests\unit\test_contabilita_kpi_panel_deep.py:60: in test_load_kpi_data_and_plotting
    assert len(panel.fig3.axes) > 0
               ^^^^^^^^^^
E   AttributeError: 'ContabilitaKPIPanel' object has no attribute 'fig3'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    199    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     51    50%   29, 34, 39, 48-60, 77-129, 138-147, 156-165, 174-183, 198, 203, 208, 213, 222, 232
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      3    95%   60, 66, 90
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          159    132    17%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     65    45%   114-116, 124-135, 144-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     36    38%   15-16, 23-25, 35-37, 42-57, 62-74, 79-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133    109    18%   38-55, 66-106, 113-130, 135-202, 207-218, 223-249, 254-257
src\core\importers\giornaliere.py                                      190    157    17%   39-60, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     29     0%   6-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    209    15%   39-46, 50-56, 60-164, 168-175, 179, 183, 206-223, 227-248, 253-277, 281-283, 287-290, 294-315, 321-339, 342-343, 346-350, 355-374, 377-379, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207    174    16%   53-55, 59-129, 132, 135-150, 154-172, 175-188, 191-199, 202-207, 210-228, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    505     9%   43-45, 48-275, 279-307, 313-391, 395-516, 561-566, 570-574, 578-582, 590-757, 761-762, 766-775, 780-784, 788-792, 796, 800-941, 950-973, 981-1018, 1023-1034, 1038-1046, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    289    12%   29-36, 47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  18924    19%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_kpi_panel_deep.py::TestContabilitaKPIPanelDeep::test_load_kpi_data_and_plotting
1 failed in 14.27s

```
</details>

---
### `tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`
**Error:** `FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`

**Timestamp:** `2026-02-06T11:59:00.142524`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________ TestContabilitaManagerBoost.test_cleanup_future_years ____________
tests\unit\test_contabilita_manager_boost.py:89: in test_cleanup_future_years
    assert count_cont == 0
E   assert 1 == 0
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     20    80%   79, 113, 128-129, 138-147, 160, 174-183, 198, 203, 208, 213, 232
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      3    95%   60, 66, 90
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     29     0%   6-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    209    15%   39-46, 50-56, 60-164, 168-175, 179, 183, 206-223, 227-248, 253-277, 281-283, 287-290, 294-315, 321-339, 342-343, 346-350, 355-374, 377-379, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207    174    16%   53-55, 59-129, 132, 135-150, 154-172, 175-188, 191-199, 202-207, 210-228, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    505     9%   43-45, 48-275, 279-307, 313-391, 395-516, 561-566, 570-574, 578-582, 590-757, 761-762, 766-775, 780-784, 788-792, 796, 800-941, 950-973, 981-1018, 1023-1034, 1038-1046, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    289    12%   29-36, 47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  18652    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years
1 failed in 10.02s

```
</details>

---
### `tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`
**Error:** `FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`

**Timestamp:** `2026-02-06T12:00:17.166292`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________ TestContabilitaManagerBoost.test_cleanup_future_years ____________
tests\unit\test_contabilita_manager_boost.py:89: in test_cleanup_future_years
    assert count_cont == 0
E   assert 1 == 0
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     20    80%   79, 113, 128-129, 138-147, 160, 174-183, 198, 203, 208, 213, 232
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      3    95%   60, 66, 90
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     29     0%   6-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    209    15%   39-46, 50-56, 60-164, 168-175, 179, 183, 206-223, 227-248, 253-277, 281-283, 287-290, 294-315, 321-339, 342-343, 346-350, 355-374, 377-379, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207    174    16%   53-55, 59-129, 132, 135-150, 154-172, 175-188, 191-199, 202-207, 210-228, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    505     9%   43-45, 48-275, 279-307, 313-391, 395-516, 561-566, 570-574, 578-582, 590-757, 761-762, 766-775, 780-784, 788-792, 796, 800-941, 950-973, 981-1018, 1023-1034, 1038-1046, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    289    12%   29-36, 47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  18652    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years
1 failed in 8.13s

```
</details>

---
### `tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`
**Error:** `FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`

**Timestamp:** `2026-02-06T12:02:13.432511`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________ TestContabilitaManagerBoost.test_cleanup_future_years ____________
tests\unit\test_contabilita_manager_boost.py:89: in test_cleanup_future_years
    assert count_cont == 0
E   assert 1 == 0
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     20    80%   79, 113, 128-129, 138-147, 160, 174-183, 198, 203, 208, 213, 232
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      3    95%   60, 66, 90
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     29     0%   6-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    209    15%   39-46, 50-56, 60-164, 168-175, 179, 183, 206-223, 227-248, 253-277, 281-283, 287-290, 294-315, 321-339, 342-343, 346-350, 355-374, 377-379, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207    174    16%   53-55, 59-129, 132, 135-150, 154-172, 175-188, 191-199, 202-207, 210-228, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    505     9%   43-45, 48-275, 279-307, 313-391, 395-516, 561-566, 570-574, 578-582, 590-757, 761-762, 766-775, 780-784, 788-792, 796, 800-941, 950-973, 981-1018, 1023-1034, 1038-1046, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    289    12%   29-36, 47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  18652    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years
1 failed in 7.99s

```
</details>

---
### `tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`
**Error:** `FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`

**Timestamp:** `2026-02-06T12:03:43.402086`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________ TestContabilitaManagerBoost.test_cleanup_future_years ____________
tests\unit\test_contabilita_manager_boost.py:89: in test_cleanup_future_years
    assert count_cont == 0
E   assert 1 == 0
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     20    80%   79, 113, 128-129, 138-147, 160, 174-183, 198, 203, 208, 213, 232
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      3    95%   60, 66, 90
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     29     0%   6-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    209    15%   39-46, 50-56, 60-164, 168-175, 179, 183, 206-223, 227-248, 253-277, 281-283, 287-290, 294-315, 321-339, 342-343, 346-350, 355-374, 377-379, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207    174    16%   53-55, 59-129, 132, 135-150, 154-172, 175-188, 191-199, 202-207, 210-228, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    505     9%   43-45, 48-275, 279-307, 313-391, 395-516, 561-566, 570-574, 578-582, 590-757, 761-762, 766-775, 780-784, 788-792, 796, 800-941, 950-973, 981-1018, 1023-1034, 1038-1046, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    289    12%   29-36, 47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  18652    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years
1 failed in 8.10s

```
</details>

---
### `tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`
**Error:** `FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`

**Timestamp:** `2026-02-06T12:05:14.825282`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________ TestContabilitaManagerBoost.test_cleanup_future_years ____________
tests\unit\test_contabilita_manager_boost.py:89: in test_cleanup_future_years
    assert count_cont == 0
E   assert 1 == 0
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     20    80%   79, 113, 128-129, 138-147, 160, 174-183, 198, 203, 208, 213, 232
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      3    95%   60, 66, 90
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     29     0%   6-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    209    15%   39-46, 50-56, 60-164, 168-175, 179, 183, 206-223, 227-248, 253-277, 281-283, 287-290, 294-315, 321-339, 342-343, 346-350, 355-374, 377-379, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207    174    16%   53-55, 59-129, 132, 135-150, 154-172, 175-188, 191-199, 202-207, 210-228, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    505     9%   43-45, 48-275, 279-307, 313-391, 395-516, 561-566, 570-574, 578-582, 590-757, 761-762, 766-775, 780-784, 788-792, 796, 800-941, 950-973, 981-1018, 1023-1034, 1038-1046, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    289    12%   29-36, 47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  18652    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years
1 failed in 8.02s

```
</details>

---
### `tests/unit/test_contabilita_manager_robust.py::TestContabilitaManagerRobust::test_import_giornaliere_flow`
**Error:** `FAILED tests/unit/test_contabilita_manager_robust.py::TestContabilitaManagerRobust::test_import_giornaliere_flow`

**Timestamp:** `2026-02-06T12:07:02.447584`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________ TestContabilitaManagerRobust.test_import_giornaliere_flow __________
C:\Program Files\Python312\Lib\unittest\mock.py:1020: in assert_any_call
    raise AssertionError(
E   AssertionError: execute('DELETE FROM giornaliere WHERE year >= 2026') call not found

During handling of the above exception, another exception occurred:
tests\unit\test_contabilita_manager_robust.py:92: in test_import_giornaliere_flow
    mock_conn.execute.assert_any_call("DELETE FROM giornaliere WHERE year >= 2026")
E   AssertionError: execute('DELETE FROM giornaliere WHERE year >= 2026') call not found
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     18    82%   113, 128-129, 138-147, 160, 174-183, 198, 203, 208, 213
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      3    95%   60, 66, 90
src\core\contabilita_worker.py                                         101     84    17%   22-27, 31-62, 66-80, 101-127, 131-152, 157-167, 177-187, 197-207, 212-222, 227-233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     29     0%   6-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    209    15%   39-46, 50-56, 60-164, 168-175, 179, 183, 206-223, 227-248, 253-277, 281-283, 287-290, 294-315, 321-339, 342-343, 346-350, 355-374, 377-379, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207    174    16%   53-55, 59-129, 132, 135-150, 154-172, 175-188, 191-199, 202-207, 210-228, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    505     9%   43-45, 48-275, 279-307, 313-391, 395-516, 561-566, 570-574, 578-582, 590-757, 761-762, 766-775, 780-784, 788-792, 796, 800-941, 950-973, 981-1018, 1023-1034, 1038-1046, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    289    12%   29-36, 47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  18650    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_manager_robust.py::TestContabilitaManagerRobust::test_import_giornaliere_flow
1 failed in 8.77s

```
</details>

---
### `tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_run_success_all_phases`
**Error:** `FAILED tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_run_success_all_phases`

**Timestamp:** `2026-02-06T12:10:21.642879`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
______________ TestContabilitaWorker.test_run_success_all_phases ______________
tests\unit\test_contabilita_worker_coverage.py:59: in test_run_success_all_phases
    assert "Contabilità: OK" in args[1]
E   AssertionError: assert 'Contabilità: OK' in 'Contabilità: File non trovato. | Giornaliere: OK (+5/-0) | Att. Prog: OK | Certificati: OK'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      8    92%   78, 118, 137-138, 144, 161-167, 233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  17961    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_run_success_all_phases
1 failed in 10.18s

```
</details>

---
### `tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing`
**Error:** `FAILED tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing`

**Timestamp:** `2026-02-06T12:12:31.751160`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________ TestContabilitaWorker.test_phases_skipped_if_path_missing __________
C:\Program Files\Python312\Lib\unittest\mock.py:928: in assert_called_once
    raise AssertionError(msg)
E   AssertionError: Expected 'import_data_from_excel' to have been called once. Called 0 times.

During handling of the above exception, another exception occurred:
tests\unit\test_contabilita_worker_coverage.py:87: in test_phases_skipped_if_path_missing
    mock_manager.import_data_from_excel.assert_called_once()
E   AssertionError: Expected 'import_data_from_excel' to have been called once. Called 0 times.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  17959    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing
1 failed in 11.89s

```
</details>

---
### `tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing`
**Error:** `FAILED tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing`

**Timestamp:** `2026-02-06T12:15:03.911757`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________ TestContabilitaWorker.test_phases_skipped_if_path_missing __________
C:\Program Files\Python312\Lib\unittest\mock.py:928: in assert_called_once
    raise AssertionError(msg)
E   AssertionError: Expected 'import_data_from_excel' to have been called once. Called 0 times.

During handling of the above exception, another exception occurred:
tests\unit\test_contabilita_worker_coverage.py:87: in test_phases_skipped_if_path_missing
    mock_manager.import_data_from_excel.assert_called_once()
E   AssertionError: Expected 'import_data_from_excel' to have been called once. Called 0 times.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  17959    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing
1 failed in 11.43s

```
</details>

---
### `tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing`
**Error:** `FAILED tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing`

**Timestamp:** `2026-02-06T12:17:14.810892`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________ TestContabilitaWorker.test_phases_skipped_if_path_missing __________
C:\Program Files\Python312\Lib\unittest\mock.py:928: in assert_called_once
    raise AssertionError(msg)
E   AssertionError: Expected 'import_data_from_excel' to have been called once. Called 0 times.

During handling of the above exception, another exception occurred:
tests\unit\test_contabilita_worker_coverage.py:91: in test_phases_skipped_if_path_missing
    mock_manager.import_data_from_excel.assert_called_once()
E   AssertionError: Expected 'import_data_from_excel' to have been called once. Called 0 times.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  17959    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing
1 failed in 11.64s

```
</details>

---
### `tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing`
**Error:** `FAILED tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing`

**Timestamp:** `2026-02-06T12:19:26.863598`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________ TestContabilitaWorker.test_phases_skipped_if_path_missing __________
C:\Program Files\Python312\Lib\unittest\mock.py:928: in assert_called_once
    raise AssertionError(msg)
E   AssertionError: Expected 'import_data_from_excel' to have been called once. Called 0 times.

During handling of the above exception, another exception occurred:
tests\unit\test_contabilita_worker_coverage.py:90: in test_phases_skipped_if_path_missing
    mock_manager.import_data_from_excel.assert_called_once()
E   AssertionError: Expected 'import_data_from_excel' to have been called once. Called 0 times.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  17959    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_worker_coverage.py::TestContabilitaWorker::test_phases_skipped_if_path_missing
1 failed in 11.40s

```
</details>

---
### `tests/unit/test_contabilita_worker_deep.py::TestContabilitaWorkerDeep::test_worker_run_success`
**Error:** `FAILED tests/unit/test_contabilita_worker_deep.py::TestContabilitaWorkerDeep::test_worker_run_success`

**Timestamp:** `2026-02-06T12:20:54.829201`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
______________ TestContabilitaWorkerDeep.test_worker_run_success ______________
C:\Program Files\Python312\Lib\unittest\mock.py:928: in assert_called_once
    raise AssertionError(msg)
E   AssertionError: Expected 'import_data_from_excel' to have been called once. Called 0 times.

During handling of the above exception, another exception occurred:
tests\unit\test_contabilita_worker_deep.py:28: in test_worker_run_success
    mock_import.assert_called_once()
E   AssertionError: Expected 'import_data_from_excel' to have been called once. Called 0 times.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  17959    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_worker_deep.py::TestContabilitaWorkerDeep::test_worker_run_success
1 failed in 11.56s

```
</details>

---
### `tests/unit/test_contabilita_worker_suite.py::TestContabilitaWorkerLogic::test_worker_run_sequence`
**Error:** `FAILED tests/unit/test_contabilita_worker_suite.py::TestContabilitaWorkerLogic::test_worker_run_sequence`

**Timestamp:** `2026-02-06T12:22:38.258365`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_____________ TestContabilitaWorkerLogic.test_worker_run_sequence _____________
tests\unit\test_contabilita_worker_suite.py:28: in test_worker_run_sequence
    assert "Contabilità: OK" in args[1]
E   AssertionError: assert 'Contabilità: OK' in 'Contabilità: File non trovato. | Giornaliere: OK (+20/-0) | Att. Prog: OK | Certificati: OK'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23242  17959    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_worker_suite.py::TestContabilitaWorkerLogic::test_worker_run_sequence
1 failed in 11.36s

```
</details>

---
### `tests/unit/test_controllers_coverage.py::TestControllersCoverage::test_bot_controller_handle_results`
**Error:** `FAILED tests/unit/test_controllers_coverage.py::TestControllersCoverage::test_bot_controller_handle_results`

**Timestamp:** `2026-02-06T12:24:30.036832`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestControllersCoverage.test_bot_controller_handle_results __________
C:\Program Files\Python312\Lib\unittest\mock.py:928: in assert_called_once
    raise AssertionError(msg)
E   AssertionError: Expected 'send_document_sync' to have been called once. Called 0 times.

During handling of the above exception, another exception occurred:
tests\unit\test_controllers_coverage.py:46: in test_bot_controller_handle_results
    mock_telegram.send_document_sync.assert_called_once()
E   AssertionError: Expected 'send_document_sync' to have been called once. Called 0 times.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              139    107    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-181, 187-206, 210-241, 244-245, 248, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71     71     0%   6-131
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    172    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256, 261-263, 268, 273-288, 293-306, 311-321, 330-357, 362-366, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159     90    43%   22, 72-74, 80-111, 118, 170-209, 219-257, 263, 275, 290-347
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     28    46%   23-25, 29-30, 34, 38-39, 43-44, 48, 52, 61, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             109     64    41%   74-96, 100-101, 120-188, 208-211, 215, 219, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     58    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\controllers\bot_controller.py                                   39     15    62%   25-33, 40, 64-72
src\gui\controllers\navigation_controller.py                           155    113    27%   42-58, 62-79, 82-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 157-160, 164-170, 174-178, 182-187, 199-241, 246-247, 265-267, 271-272, 276-277, 281-314, 318-319
src\gui\controllers\search_controller.py                               197    162    18%   18-46, 61, 73-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159    137    14%   26-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 173-188, 193-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     60    33%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 237, 243-246
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23633  18249    23%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_controllers_coverage.py::TestControllersCoverage::test_bot_controller_handle_results
1 failed in 12.94s

```
</details>

---
### `tests/unit/test_data_synchronizer_extended.py::TestDataSynchronizerDetailed::test_sync_attivita_programmate`
**Error:** `FAILED tests/unit/test_data_synchronizer_extended.py::TestDataSynchronizerDetailed::test_sync_attivita_programmate`

**Timestamp:** `2026-02-06T12:29:09.529622`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestDataSynchronizerDetailed.test_sync_attivita_programmate _________
tests\unit\test_data_synchronizer_extended.py:66: in test_sync_attivita_programmate
    assert added == 10
E   assert 0 == 10
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    208    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-139, 145, 149, 153, 157-158, 162-163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205    176    14%   41-44, 48, 52-54, 67-98, 109-128, 132-167, 171-180, 204-311, 315-335, 345-379, 383-394, 398-411, 417-428
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     39    61%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 167-175
src\core\audit\integrity.py                                             15      2    87%   21, 26
src\core\audit\manager.py                                              139     68    51%   46, 50, 58-63, 172, 178-181, 187-206, 210-241, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71      0   100%
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    116    52%   35, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 203-204, 226, 236, 250-251, 283, 300-301, 304, 311-321, 330-357, 364, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159     11    93%   22, 72-74, 118, 191, 193, 263, 291, 309, 311
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      6    86%   49, 63, 76, 80, 91, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              58     17    71%   15-16, 23-25, 51-56, 70-74, 84-86
src\core\importers\certificati.py                                      115     91    21%   35-54, 59-63, 70-74, 79-94, 101-123, 128-139, 144-150, 155-184
src\core\importers\contabilita.py                                      133     27    80%   40, 47-55, 68, 78, 90, 104-106, 120, 128, 142-143, 152, 200-202, 217, 237, 239
src\core\importers\giornaliere.py                                      190    151    21%   41, 46-59, 70-90, 100-117, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186    154    17%   12-13, 19-21, 46-86, 94-112, 116-134, 148-179, 183-242, 246-255, 272-276, 280-304
src\core\importers\storico_oda.py                                       84     64    24%   57-84, 89-95, 100-116, 121, 126-170, 178-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     22    58%   29-30, 38-39, 43-44, 52, 79-96, 106, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     33    48%   92, 112, 120, 123, 127, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     26    69%   84, 88-90, 122, 125, 130, 132, 134, 136, 138, 168, 198, 209-219, 228, 234-244
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 149-150, 165-169, 173-180, 187-188, 209, 215, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     17    70%   58, 67, 91, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29     20    31%   23-50
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     51    46%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 122-126, 133-134, 139-145
src\core\stats_manager.py                                               47     11    77%   40-45, 48, 61, 63, 76, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\controllers\bot_controller.py                                   39     14    64%   25-33, 64-72
src\gui\controllers\navigation_controller.py                           155    113    27%   42-58, 62-79, 82-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 157-160, 164-170, 174-178, 182-187, 199-241, 246-247, 265-267, 271-272, 276-277, 281-314, 318-319
src\gui\controllers\search_controller.py                               197    162    18%   18-46, 61, 73-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81      0   100%
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159     71    55%   85, 133-135, 142, 144, 147-149, 154-155, 157-167, 184-187, 194-197, 200, 208-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         68     68     0%   6-130
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     22    84%   39-40, 88-90, 151-152, 172-182, 189, 193-195, 272, 278, 292, 294
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     19    87%   169-195, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197     77    61%   55, 58, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 241, 248, 257, 266, 275, 293-297, 301-305
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     17    48%   21-31, 37-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107     84    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-207, 211, 215
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     14    82%   273-314, 328, 344, 361-362
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-236
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    90     59    34%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 206-228, 243-246
src\utils\log_humanizer.py                                              41     26    37%   18-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     37    53%   43-44, 54-58, 81-83, 102-112, 116-138
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23633  17229    27%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_data_synchronizer_extended.py::TestDataSynchronizerDetailed::test_sync_attivita_programmate
1 failed in 8.01s

```
</details>

---
### `tests/unit/test_excel_importer.py::TestExcelImporter::test_import_giornaliere`
**Error:** `FAILED tests/unit/test_excel_importer.py::TestExcelImporter::test_import_giornaliere`

**Timestamp:** `2026-02-06T12:36:56.226630`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________________ TestExcelImporter.test_import_giornaliere __________________
tests\unit\test_excel_importer.py:132: in test_import_giornaliere
    assert len(rows) > 0
E   assert 0 > 0
E    +  where 0 = len([])
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    186    29%   76, 82, 87, 92-94, 106-110, 122, 135-139, 145, 149, 153, 157-158, 163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     15    81%   21, 26, 31, 42, 61, 64, 75, 106, 111, 127-128, 130-131, 142, 149
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205     61    70%   52-54, 95-98, 109-128, 144-146, 164-167, 244, 263-271, 290-294, 305-311, 334-335, 351-352, 362, 367-374, 377-379, 390-391, 393-394, 411
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     39    61%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 167-175
src\core\audit\integrity.py                                             15      2    87%   21, 26
src\core\audit\manager.py                                              139     68    51%   46, 50, 58-63, 172, 178-181, 187-206, 210-241, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71      0   100%
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    116    52%   35, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 203-204, 226, 236, 250-251, 283, 300-301, 304, 311-321, 330-357, 364, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159      8    95%   72-74, 191, 193, 263, 291, 309
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     10    92%   169-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     13    87%   61-63, 120-122, 131-132, 178-179, 196-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      0   100%
src\core\importers\attivita.py                                          64     13    80%   43, 48, 52, 57-58, 67-76, 92-93, 96
src\core\importers\base.py                                              58     11    81%   15-16, 23-25, 55-56, 74, 84-86
src\core\importers\certificati.py                                      115     19    83%   37, 46, 50, 53-54, 63, 88-89, 106-107, 138, 163-164, 168, 174-178
src\core\importers\contabilita.py                                      133     23    83%   40, 47-55, 78, 90, 104-106, 120, 128, 152, 200-202, 237, 239
src\core\importers\giornaliere.py                                      190    136    28%   41, 46-59, 72, 83-90, 104, 107, 114-116, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186     54    71%   12-13, 19-21, 48, 66-67, 73-86, 96, 99, 104, 111-112, 116-134, 173, 201, 205, 214, 218, 226, 231, 239, 248, 251, 273, 275, 283
src\core\importers\storico_oda.py                                       84     15    82%   65, 70, 83-84, 94-95, 185-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     21    60%   29-30, 38-39, 43-44, 52, 79-96, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     33    48%   92, 112, 120, 123, 127, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     23    73%   84, 88-90, 122, 125, 132, 138, 168, 198, 209-219, 228, 234-244
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 149-150, 165-169, 173-180, 187-188, 209, 215, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     17    70%   58, 67, 91, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                        97     45    54%   44, 52-59, 63-76, 83-84, 135-150, 154-156, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     13    61%   30-90, 111-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     51    46%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 122-126, 133-134, 139-145
src\core\stats_manager.py                                               47     11    77%   40-45, 48, 61, 63, 76, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\controllers\bot_controller.py                                   39     14    64%   25-33, 64-72
src\gui\controllers\navigation_controller.py                           155    113    27%   42-58, 62-79, 82-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 157-160, 164-170, 174-178, 182-187, 199-241, 246-247, 265-267, 271-272, 276-277, 281-314, 318-319
src\gui\controllers\search_controller.py                               197    162    18%   18-46, 61, 73-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81      0   100%
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159     71    55%   85, 133-135, 142, 144, 147-149, 154-155, 157-167, 184-187, 194-197, 200, 208-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         68     52    24%   25-28, 33, 40-50, 54-97, 102-125, 130
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     22    84%   39-40, 88-90, 151-152, 172-182, 189, 193-195, 272, 278, 292, 294
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     19    87%   169-195, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197     77    61%   55, 58, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 241, 248, 257, 266, 275, 293-297, 301-305
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     17    48%   21-31, 37-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107      1    99%   129
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     14    82%   273-314, 328, 344, 361-362
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69      1    99%   60
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         66      7    89%   15-16, 70-72, 90-92
src\utils\helpers.py                                                    90     52    42%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 207, 226, 243-246
src\utils\log_humanizer.py                                              41     26    37%   18-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     23    71%   43-44, 81-83, 103, 105, 110-112, 117, 123-138
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23633  16340    31%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_excel_importer.py::TestExcelImporter::test_import_giornaliere
1 failed in 8.31s

```
</details>

---
### `tests/unit/test_excel_importer.py::TestExcelImporter::test_import_giornaliere`
**Error:** `FAILED tests/unit/test_excel_importer.py::TestExcelImporter::test_import_giornaliere`

**Timestamp:** `2026-02-06T12:38:34.497399`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________________ TestExcelImporter.test_import_giornaliere __________________
tests\unit\test_excel_importer.py:133: in test_import_giornaliere
    assert len(rows) > 0
E   assert 0 > 0
E    +  where 0 = len([])
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    186    29%   76, 82, 87, 92-94, 106-110, 122, 135-139, 145, 149, 153, 157-158, 163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     15    81%   21, 26, 31, 42, 61, 64, 75, 106, 111, 127-128, 130-131, 142, 149
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205     61    70%   52-54, 95-98, 109-128, 144-146, 164-167, 244, 263-271, 290-294, 305-311, 334-335, 351-352, 362, 367-374, 377-379, 390-391, 393-394, 411
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     39    61%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 167-175
src\core\audit\integrity.py                                             15      2    87%   21, 26
src\core\audit\manager.py                                              139     68    51%   46, 50, 58-63, 172, 178-181, 187-206, 210-241, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71      0   100%
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    116    52%   35, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 203-204, 226, 236, 250-251, 283, 300-301, 304, 311-321, 330-357, 364, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159      8    95%   72-74, 191, 193, 263, 291, 309
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     10    92%   169-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     13    87%   61-63, 120-122, 131-132, 178-179, 196-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      0   100%
src\core\importers\attivita.py                                          64     13    80%   43, 48, 52, 57-58, 67-76, 92-93, 96
src\core\importers\base.py                                              58     11    81%   15-16, 23-25, 55-56, 74, 84-86
src\core\importers\certificati.py                                      115     19    83%   37, 46, 50, 53-54, 63, 88-89, 106-107, 138, 163-164, 168, 174-178
src\core\importers\contabilita.py                                      133     23    83%   40, 47-55, 78, 90, 104-106, 120, 128, 152, 200-202, 237, 239
src\core\importers\giornaliere.py                                      190    136    28%   41, 46-59, 72, 83-90, 104, 107, 114-116, 123-142, 148-186, 190-207, 211-235, 239-291, 295-315
src\core\importers\scarico_ore.py                                      186     54    71%   12-13, 19-21, 48, 66-67, 73-86, 96, 99, 104, 111-112, 116-134, 173, 201, 205, 214, 218, 226, 231, 239, 248, 251, 273, 275, 283
src\core\importers\storico_oda.py                                       84     15    82%   65, 70, 83-84, 94-95, 185-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     21    60%   29-30, 38-39, 43-44, 52, 79-96, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     33    48%   92, 112, 120, 123, 127, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     23    73%   84, 88-90, 122, 125, 132, 138, 168, 198, 209-219, 228, 234-244
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 149-150, 165-169, 173-180, 187-188, 209, 215, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     17    70%   58, 67, 91, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                        97     45    54%   44, 52-59, 63-76, 83-84, 135-150, 154-156, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     13    61%   30-90, 111-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             94     51    46%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 122-126, 133-134, 139-145
src\core\stats_manager.py                                               47     11    77%   40-45, 48, 61, 63, 76, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\controllers\bot_controller.py                                   39     14    64%   25-33, 64-72
src\gui\controllers\navigation_controller.py                           155    113    27%   42-58, 62-79, 82-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 157-160, 164-170, 174-178, 182-187, 199-241, 246-247, 265-267, 271-272, 276-277, 281-314, 318-319
src\gui\controllers\search_controller.py                               197    162    18%   18-46, 61, 73-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81      0   100%
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159     71    55%   85, 133-135, 142, 144, 147-149, 154-155, 157-167, 184-187, 194-197, 200, 208-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         68     52    24%   25-28, 33, 40-50, 54-97, 102-125, 130
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     22    84%   39-40, 88-90, 151-152, 172-182, 189, 193-195, 272, 278, 292, 294
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     19    87%   169-195, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197     77    61%   55, 58, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 241, 248, 257, 266, 275, 293-297, 301-305
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     17    48%   21-31, 37-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107      1    99%   129
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     14    82%   273-314, 328, 344, 361-362
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69      1    99%   60
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         66      7    89%   15-16, 70-72, 90-92
src\utils\helpers.py                                                    90     52    42%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 207, 226, 243-246
src\utils\log_humanizer.py                                              41     26    37%   18-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     23    71%   43-44, 81-83, 103, 105, 110-112, 117, 123-138
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23633  16340    31%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_excel_importer.py::TestExcelImporter::test_import_giornaliere
1 failed in 7.88s

```
</details>

---
### `tests/unit/test_excel_importer.py::TestExcelImporter::test_import_contabilita_dati_success`
**Error:** `E   NameError: name 'pytest' is not defined`

**Timestamp:** `2026-02-06T12:40:04.267500`

<details><summary>Full Output</summary>

```text

=================================== ERRORS ====================================
_____________ ERROR collecting tests/unit/test_excel_importer.py ______________
tests\unit\test_excel_importer.py:8: in <module>
    class TestExcelImporter:
tests\unit\test_excel_importer.py:70: in TestExcelImporter
    @pytest.mark.skip(reason="Mock Path issues")
     ^^^^^^
E   NameError: name 'pytest' is not defined
=========================== short test summary info ===========================
ERROR tests/unit/test_excel_importer.py - NameError: name 'pytest' is not def...
1 error in 2.51s
ERROR: found no collectors for C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_excel_importer.py::TestExcelImporter::test_import_contabilita_dati_success


```
</details>

---
### `tests/unit/test_excel_importer_coverage.py::test_import_giornaliere_collection`
**Error:** `FAILED tests/unit/test_excel_importer_coverage.py::test_import_giornaliere_collection`

**Timestamp:** `2026-02-06T12:42:50.513851`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_____________________ test_import_giornaliere_collection ______________________
tests\unit\test_excel_importer_coverage.py:117: in test_import_giornaliere_collection
    assert len(tasks) >= 1
E   assert 0 >= 1
E    +  where 0 = len([])
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    186    29%   76, 82, 87, 92-94, 106-110, 122, 135-139, 145, 149, 153, 157-158, 163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     15    81%   21, 26, 31, 42, 61, 64, 75, 106, 111, 127-128, 130-131, 142, 149
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205     61    70%   52-54, 95-98, 109-128, 144-146, 164-167, 244, 263-271, 290-294, 305-311, 334-335, 351-352, 362, 367-374, 377-379, 390-391, 393-394, 411
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     39    61%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 167-175
src\core\audit\integrity.py                                             15      2    87%   21, 26
src\core\audit\manager.py                                              139     68    51%   46, 50, 58-63, 172, 178-181, 187-206, 210-241, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71      0   100%
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    116    52%   35, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 203-204, 226, 236, 250-251, 283, 300-301, 304, 311-321, 330-357, 364, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87     16    82%   29-30, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159      8    95%   72-74, 191, 193, 263, 291, 309
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     10    92%   169-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     13    87%   61-63, 120-122, 131-132, 178-179, 196-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      0   100%
src\core\importers\attivita.py                                          64     12    81%   48, 52, 57-58, 67-76, 92-93, 96
src\core\importers\base.py                                              58      8    86%   15-16, 23-25, 55-56, 74
src\core\importers\certificati.py                                      115     19    83%   37, 46, 50, 53-54, 63, 88-89, 106-107, 138, 163-164, 168, 174-178
src\core\importers\contabilita.py                                      133     21    84%   40, 47-55, 90, 104-106, 120, 128, 200-202, 237, 239
src\core\importers\giornaliere.py                                      190     65    66%   41, 46-59, 72, 83-90, 104, 107, 114-116, 123-142, 153, 157, 161, 185-186, 195-207, 218-221, 224, 240, 246, 254, 268, 272
src\core\importers\scarico_ore.py                                      186     54    71%   12-13, 19-21, 48, 66-67, 73-86, 96, 99, 104, 111-112, 116-134, 173, 201, 205, 214, 218, 226, 231, 239, 248, 251, 273, 275, 283
src\core\importers\storico_oda.py                                       84     15    82%   65, 70, 83-84, 94-95, 185-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     21    60%   29-30, 38-39, 43-44, 52, 79-96, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     33    48%   92, 112, 120, 123, 127, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     23    73%   84, 88-90, 122, 125, 132, 138, 168, 198, 209-219, 228, 234-244
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 149-150, 165-169, 173-180, 187-188, 209, 215, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     17    70%   58, 67, 91, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                        97     45    54%   44, 52-59, 63-76, 83-84, 135-150, 154-156, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     13    61%   30-90, 111-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     23    71%   67-72, 77-88, 93-95, 101, 108
src\core\secrets_manager.py                                             94     51    46%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 122-126, 133-134, 139-145
src\core\stats_manager.py                                               47     11    77%   40-45, 48, 61, 63, 76, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\controllers\bot_controller.py                                   39     14    64%   25-33, 64-72
src\gui\controllers\navigation_controller.py                           155    113    27%   42-58, 62-79, 82-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 157-160, 164-170, 174-178, 182-187, 199-241, 246-247, 265-267, 271-272, 276-277, 281-314, 318-319
src\gui\controllers\search_controller.py                               197    162    18%   18-46, 61, 73-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81      0   100%
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127    111    13%   12-25, 35-66, 71, 83-89, 93-96, 102, 105, 108, 111-138, 141-146, 149-152, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159     71    55%   85, 133-135, 142, 144, 147-149, 154-155, 157-167, 184-187, 194-197, 200, 208-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         68     52    24%   25-28, 33, 40-50, 54-97, 102-125, 130
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     22    84%   39-40, 88-90, 151-152, 172-182, 189, 193-195, 272, 278, 292, 294
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     19    87%   169-195, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197     77    61%   55, 58, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 241, 248, 257, 266, 275, 293-297, 301-305
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     17    48%   21-31, 37-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107      1    99%   129
src\gui\widgets\excel_table.py                                         327    286    13%   47-59, 63-70, 74-91, 95-115, 118-119, 122-123, 127-138, 142-166, 170-196, 200-219, 223-243, 247-256, 259-264, 267-271, 274-278, 287-289, 292-315, 318-377, 380-383, 386-392, 395-427, 430-433, 436-438, 441, 445-462, 471-481, 485-525, 530-555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     14    82%   273-314, 328, 344, 361-362
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69      1    99%   60
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         66      7    89%   15-16, 70-72, 90-92
src\utils\helpers.py                                                    90     52    42%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 207, 226, 243-246
src\utils\log_humanizer.py                                              41     26    37%   18-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     23    71%   43-44, 81-83, 103, 105, 110-112, 117, 123-138
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23633  16261    31%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_excel_importer_coverage.py::test_import_giornaliere_collection
1 failed in 10.92s

```
</details>

---
### `tests/unit/test_gui_advanced.py::TestGUIAdvanced::test_kpi_panel_initialization`
**Error:** `Unknown Error`

**Timestamp:** `2026-02-06T12:47:29.608368`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
_______ ERROR at setup of TestGUIAdvanced.test_kpi_panel_initialization _______
tests\unit\test_gui_advanced.py:16: in mock_manager
    return mocker.patch("src.gui.panels.contabilita_kpi_panel.ContabilitaManager")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:419: in __call__
    return self._start_patch(
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:229: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1451: in __enter__
    self.target = self.getter()
                  ^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\pkgutil.py:528: in resolve_name
    result = getattr(result, p)
             ^^^^^^^^^^^^^^^^^^
E   AttributeError: module 'src.gui.panels' has no attribute 'contabilita_kpi_panel'. Did you mean: 'contabilita_panel'?
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    186    29%   76, 82, 87, 92-94, 106-110, 122, 135-139, 145, 149, 153, 157-158, 163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     15    81%   21, 26, 31, 42, 61, 64, 75, 106, 111, 127-128, 130-131, 142, 149
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205     61    70%   52-54, 95-98, 109-128, 144-146, 164-167, 244, 263-271, 290-294, 305-311, 334-335, 351-352, 362, 367-374, 377-379, 390-391, 393-394, 411
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     39    61%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 167-175
src\core\audit\integrity.py                                             15      2    87%   21, 26
src\core\audit\manager.py                                              139     68    51%   46, 50, 58-63, 172, 178-181, 187-206, 210-241, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71      0   100%
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    116    52%   35, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 203-204, 226, 236, 250-251, 283, 300-301, 304, 311-321, 330-357, 364, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87      4    95%   52, 80, 96, 112
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159      8    95%   72-74, 191, 193, 263, 291, 309
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     10    92%   169-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     13    87%   61-63, 120-122, 131-132, 178-179, 196-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      0   100%
src\core\importers\attivita.py                                          64      4    94%   57-58, 92-93
src\core\importers\base.py                                              58      7    88%   15-16, 23-25, 55-56
src\core\importers\certificati.py                                      115     16    86%   46, 50, 53-54, 63, 106-107, 138, 163-164, 168, 174-178
src\core\importers\contabilita.py                                      133      9    93%   40, 49, 53-55, 120, 200-202
src\core\importers\giornaliere.py                                      190     31    84%   41, 52-59, 88, 104, 107, 140, 157, 161, 185-186, 197-207, 220-221, 224, 240, 246, 254, 268
src\core\importers\scarico_ore.py                                      186     34    82%   12-13, 19-21, 48, 66-67, 73-86, 96, 99, 111-112, 125, 173, 201, 205, 214, 218, 231, 239, 248, 283
src\core\importers\storico_oda.py                                       84     15    82%   65, 70, 83-84, 94-95, 185-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     21    60%   29-30, 38-39, 43-44, 52, 79-96, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     33    48%   92, 112, 120, 123, 127, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     23    73%   84, 88-90, 122, 125, 132, 138, 168, 198, 209-219, 228, 234-244
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 149-150, 165-169, 173-180, 187-188, 209, 215, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     17    70%   58, 67, 91, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                        97     45    54%   44, 52-59, 63-76, 83-84, 135-150, 154-156, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     13    61%   30-90, 111-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     23    71%   67-72, 77-88, 93-95, 101, 108
src\core\secrets_manager.py                                             94     51    46%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 122-126, 133-134, 139-145
src\core\stats_manager.py                                               47     11    77%   40-45, 48, 61, 63, 76, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\controllers\bot_controller.py                                   39     14    64%   25-33, 64-72
src\gui\controllers\navigation_controller.py                           155    113    27%   42-58, 62-79, 82-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 157-160, 164-170, 174-178, 182-187, 199-241, 246-247, 265-267, 271-272, 276-277, 281-314, 318-319
src\gui\controllers\search_controller.py                               197    162    18%   18-46, 61, 73-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81      0   100%
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127     84    34%   12-25, 35-66, 71, 93-96, 102, 118-120, 126, 136, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159     71    55%   85, 133-135, 142, 144, 147-149, 154-155, 157-167, 184-187, 194-197, 200, 208-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         68     52    24%   25-28, 33, 40-50, 54-97, 102-125, 130
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     22    84%   39-40, 88-90, 151-152, 172-182, 189, 193-195, 272, 278, 292, 294
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     19    87%   169-195, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197     77    61%   55, 58, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 241, 248, 257, 266, 275, 293-297, 301-305
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     17    48%   21-31, 37-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107      1    99%   129
src\gui\widgets\excel_table.py                                         327     94    71%   63-70, 86, 97, 101, 108, 114, 142-166, 170-196, 202, 229, 234, 251-252, 259-264, 276, 318-377, 388, 421, 430-433, 436-438, 479-480, 517-519, 538, 552
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     38    57%   26-59, 62, 82-110
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     14    82%   273-314, 328, 344, 361-362
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41      7    83%   28-30, 35-37, 76
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69      1    99%   60
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         66      7    89%   15-16, 70-72, 90-92
src\utils\helpers.py                                                    90     52    42%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 207, 226, 243-246
src\utils\log_humanizer.py                                              41     26    37%   18-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     23    71%   43-44, 81-83, 103, 105, 110-112, 117, 123-138
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23633  15917    33%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_gui_advanced.py::TestGUIAdvanced::test_kpi_panel_initialization
1 error in 16.13s

```
</details>

---
### `tests/unit/test_gui_advanced.py::TestGUIAdvanced::test_kpi_panel_initialization`
**Error:** `FAILED tests/unit/test_gui_advanced.py::TestGUIAdvanced::test_kpi_panel_initialization`

**Timestamp:** `2026-02-06T12:49:11.775674`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
________________ TestGUIAdvanced.test_kpi_panel_initialization ________________
tests\unit\test_gui_advanced.py:27: in test_kpi_panel_initialization
    panel = ContabilitaKPIPanel()
            ^^^^^^^^^^^^^^^^^^^^^
src\gui\panels\contabilita_kpi\kpi_panel.py:40: in __init__
    self._setup_ui()
src\gui\panels\contabilita_kpi\kpi_panel.py:122: in _setup_ui
    self.container1 = ChartContainer(
src\gui\panels\contabilita_kpi\charts.py:63: in __init__
    layout.addWidget(self.canvas)
E   TypeError: addWidget(self, a0: typing.Optional[QWidget], stretch: int = 0, alignment: Qt.AlignmentFlag = Qt.Alignment()): argument 1 has unexpected type 'MagicMock'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263    186    29%   76, 82, 87, 92-94, 106-110, 122, 135-139, 145, 149, 153, 157-158, 163, 168-186, 190-235, 239-263, 267-269, 278-283, 287-318, 330-379, 383-415, 420-429, 433-437, 441-443, 447, 451-459, 470-482, 486-489, 501
src\bots\base\login_page.py                                             94     77    18%   35-38, 46-62, 66-96, 100-116, 120-125, 132-179
src\bots\base\wait_helpers.py                                          168    168     0%   14-488
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     15    81%   21, 26, 31, 42, 61, 64, 75, 106, 111, 127-128, 130-131, 142, 149
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     205     61    70%   52-54, 95-98, 109-128, 144-146, 164-167, 244, 263-271, 290-294, 305-311, 334-335, 351-352, 362, 367-374, 377-379, 390-391, 393-394, 411
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            83     66    20%   20, 27, 31, 43-52, 57-64, 68-96, 100-105, 109-132
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   30-33, 37, 41-43, 55-82, 93-98, 103-108, 112-144, 150-189, 193-203, 212-242, 246-253, 257-277, 281-293, 297-311, 315-335, 339-365, 369-375
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    188    16%   40, 45, 50, 57, 61, 73-76, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 273-311, 317-354, 358-367, 373-390, 396-418, 423-433
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            73     53    27%   21, 26, 31, 36, 41-45, 49-65, 71-116, 123
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    140    14%   35-39, 42, 46-61, 68-87, 91-150, 154-219, 224-252, 256-269, 274-319
src\bots\portale_fornitori\timbrature\storage.py                       177    151    15%   44-45, 49-84, 88-89, 96-119, 125-154, 164-175, 185-192, 197-225, 232-268, 273-288, 295-335, 338-373, 377-394, 403-404
src\bots\safework\base.py                                               40     25    38%   22-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           393    348    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-295, 299-331, 335-347, 351-379, 383-421, 425-445, 449-470, 474-488, 495-538, 541-582, 586-609
src\bots\safework\pdl\search_bot.py                                    179    153    15%   22-23, 27, 31, 35-97, 101-118, 122-143, 147-158, 162-171, 175-179, 183-210, 214-244, 248-336
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84     84     0%   5-163
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     39    61%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 167-175
src\core\audit\integrity.py                                             15      2    87%   21, 26
src\core\audit\manager.py                                              139     68    51%   46, 50, 58-63, 172, 178-181, 187-206, 210-241, 251, 254-257, 265-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                71      0   100%
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               157    157     0%   11-344
src\core\config_manager.py                                             242    116    52%   35, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 203-204, 226, 236, 250-251, 283, 300-301, 304, 311-321, 330-357, 364, 371-373, 378-380, 385-392, 401-420, 428-474
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        102     16    84%   113, 128-129, 138-147, 160, 174-183, 198, 213
src\core\contabilita_queries.py                                         87      4    95%   52, 80, 96, 112
src\core\contabilita_search.py                                          91      6    93%   51-52, 78-79, 109-110
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         101      6    94%   78, 118, 137-138, 144, 233
src\core\data_synchronizer.py                                          159      8    95%   72-74, 191, 193, 263, 291, 309
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     10    92%   169-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17      0   100%
src\core\database\migrations\pdl.py                                     19      0   100%
src\core\database\migrations\storico_oda.py                             11      0   100%
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     13    87%   61-63, 120-122, 131-132, 178-179, 196-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      0   100%
src\core\importers\attivita.py                                          64      4    94%   57-58, 92-93
src\core\importers\base.py                                              58      7    88%   15-16, 23-25, 55-56
src\core\importers\certificati.py                                      115     16    86%   46, 50, 53-54, 63, 106-107, 138, 163-164, 168, 174-178
src\core\importers\contabilita.py                                      133      9    93%   40, 49, 53-55, 120, 200-202
src\core\importers\giornaliere.py                                      190     31    84%   41, 52-59, 88, 104, 107, 140, 157, 161, 185-186, 197-207, 220-221, 224, 240, 246, 254, 268
src\core\importers\scarico_ore.py                                      186     34    82%   12-13, 19-21, 48, 66-67, 73-86, 96, 99, 111-112, 125, 173, 201, 205, 214, 218, 231, 239, 248, 283
src\core\importers\storico_oda.py                                       84     15    82%   65, 70, 83-84, 94-95, 185-194
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      114     85    25%   51-53, 56-59, 64-69, 81-92, 96-115, 119-121, 125-157, 176-189, 201-218, 230-241, 247
src\core\logging\analytics.py                                          136     89    35%   52, 56, 70-75, 79-83, 92-120, 129-158, 167-197, 210-211, 215-217, 228-245, 268-289, 302-326, 337, 342, 347
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             52     21    60%   29-30, 38-39, 43-44, 52, 79-96, 116, 126, 136, 146, 156
src\core\logging\decorators.py                                          64     50    22%   48-111, 118, 147-184
src\core\logging\filters.py                                             64     33    48%   92, 112, 120, 123, 127, 144-158, 171-177, 195-196, 205-214
src\core\logging\formatters.py                                          84     23    73%   84, 88-90, 122, 125, 132, 138, 168, 198, 209-219, 228, 234-244
src\core\logging\logger.py                                             109     30    72%   84, 96, 123, 137-139, 149-150, 165-169, 173-180, 187-188, 209, 215, 223, 227, 231, 242, 259, 307-312
src\core\logging\metadata.py                                            86     86     0%   5-203
src\core\logging\metrics.py                                            102     73    28%   24-27, 31, 47-51, 60-62, 79-109, 127-129, 132-134, 151-161, 175-192, 202, 214, 233-243, 252-254, 263-265, 273-276, 285-299, 305
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     17    70%   58, 67, 91, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              102     78    24%   21-25, 50-73, 77-80, 93-106, 117-122, 132-139, 143-159, 170-172, 182-188, 200-210, 222-224, 230-232, 238-240
src\core\logging\viewer.py                                             182    149    18%   20-23, 27-28, 33-42, 47-55, 59, 63, 70-84, 88-89, 93-94, 98-99, 103-127, 131-143, 158, 170-177, 186-193, 205-231, 246-270, 282-287, 303-360, 370-408, 422, 435, 445
src\core\lyra_client.py                                                126    111    12%   21-37, 55-69, 73-74, 78-108, 112-145, 154-210, 219-257
src\core\lyra_sentinel.py                                               29      5    83%   44-48
src\core\notification_manager.py                                        97     45    54%   44, 52-59, 63-76, 83-84, 135-150, 154-156, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     13    61%   30-90, 111-118
src\core\report_history.py                                              66     43    35%   26-28, 36-41, 46-52, 63-87, 99, 119-139, 152-162
src\core\schemas.py                                                     78     23    71%   67-72, 77-88, 93-95, 101, 108
src\core\secrets_manager.py                                             94     51    46%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 122-126, 133-134, 139-145
src\core\stats_manager.py                                               47     11    77%   40-45, 48, 61, 63, 76, 83
src\core\sync_tracker.py                                                59     38    36%   25-39, 44-49, 64-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           174    138    21%   39-49, 55-72, 76-85, 89, 93-105, 108, 118-156, 159-172, 176-186, 194-202, 211-219, 223-233, 236-249, 252-265, 268-280, 283-296, 299-313
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    343     0%   1-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   184    163    11%   22-56, 61-73, 78-91, 100-118, 127-156, 159-163, 166, 182-187, 190-194, 197-222, 225-230, 233-238, 241-242, 245-270, 273-278
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                168    137    18%   59-85, 88-101, 104-125, 128, 131-135, 138-152, 155-158, 163-170, 173-176, 179-181, 184-186, 189-215, 220-237, 240-245, 248-273
src\gui\controllers\bot_controller.py                                   39     14    64%   25-33, 64-72
src\gui\controllers\navigation_controller.py                           155    113    27%   42-58, 62-79, 82-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 157-160, 164-170, 174-178, 182-187, 199-241, 246-247, 265-267, 271-272, 276-277, 281-314, 318-319
src\gui\controllers\search_controller.py                               197    162    18%   18-46, 61, 73-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   230    230     0%   10-495
src\gui\dialogs\command_palette.py                                     301    301     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81      0   100%
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      232    232     0%   6-390
src\gui\formatters.py                                                  127     84    34%   12-25, 35-66, 71, 93-96, 102, 118-120, 126, 136, 156-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              73     73     0%   1-336
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            279    279     0%   1-487
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             90     69    23%   29-37, 40-44, 49-93, 97-99, 103-107, 111-119, 123-124, 128-184
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            150      5    97%   190, 216, 221, 296-297
src\gui\panels\contabilita_panel.py                                    245    105    57%   50-56, 168-175, 179, 207-209, 219, 223, 227-248, 253-277, 281-283, 287-290, 298-303, 306-315, 328-330, 350, 361, 378, 382-399, 403, 406-425
src\gui\panels\dashboard_panel.py                                      159     71    55%   85, 133-135, 142, 144, 147-149, 154-155, 157-167, 184-187, 194-197, 200, 208-211, 215-228, 232-238, 242-259, 263-287, 291-297
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    153    128    16%   24-50, 57-100, 109-199, 204-217, 222-245, 250-314
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         290    257    11%   32-35, 39, 43-44, 47-53, 56-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-599, 603-606
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253    206    19%   57-70, 73-154, 157-161, 165-167, 171-173, 177-179, 183-184, 188-189, 193, 196-200, 205-243, 248-271, 277-305, 313-321, 325-326, 330-348, 352-384, 388-390, 394-413, 417-458
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   45     36    20%   18-21, 24-50, 54-67, 71-72
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        334    298    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-583
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           79     64    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-147, 150-152
src\gui\panels\scarico_ore_panel.py                                    299    261    13%   45-47, 52-86, 97-106, 110-230, 234-249, 253-284, 288-290, 294-302, 306-327, 331-333, 337-354, 365-392, 396-401, 405-417, 421-432, 436-437, 441-449, 453-467, 471-490, 494-497, 501-520
src\gui\panels\scarico_pdl.py                                          296    256    14%   41-58, 62-83, 87-120, 130-138, 141-145, 149-278, 281-289, 292-295, 298-311, 314-325, 329, 332-334, 338-346, 351-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            318    265    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269, 272-279, 282-290, 293-309, 312-321, 324-330, 335-344, 347-361, 364-373, 376-382, 387-388, 391, 394-397, 400-407, 410-415, 419, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 457-464, 469-484
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-86, 89-110, 114-135, 152-153, 156, 159-163, 166-168, 171-173, 176-180, 183-185, 188-190, 195-215, 218-236
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           46     37    20%   19-22, 25-51, 55-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                248    217    12%   43-106, 109-174, 178-188, 192-295, 298-309, 312, 315, 318-322, 325-331, 335-357, 363-423, 426-431, 436-458, 462-482
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     60     50    17%   14-37, 40-66, 74-118, 122-137, 141-142
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         68     52    24%   25-28, 33, 40-50, 54-97, 102-125, 130
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     22    84%   39-40, 88-90, 151-152, 172-182, 189, 193-195, 272, 278, 292, 294
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-135, 138, 141-142, 145-163, 166-175, 178-180
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     19    87%   169-195, 378-406
src\gui\widgets\autopilot\event_card.py                                 67     59    12%   21-127, 131-146, 151-164
src\gui\widgets\autopilot\main_widget.py                               197     77    61%   55, 58, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 241, 248, 257, 266, 275, 293-297, 301-305
src\gui\widgets\bot_parameters.py                                      110     86    22%   42-46, 49-117, 127-134, 138, 154, 158-160, 164-172, 177, 181-183, 187-191, 201-206, 210, 214-215
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            207     57    72%   132, 193, 204-207, 227, 231-234, 242-250, 253-256, 259-262, 265-268, 271-274, 277-281, 284-299, 302-307
src\gui\widgets\contabilita\certificati_tab.py                         556    320    42%   43-45, 48-275, 279-307, 313-391, 395-516, 578-582, 761-762, 784, 792, 796, 821-822, 939, 952, 969, 997-999, 1045, 1050-1053, 1057-1060, 1064-1077, 1080-1163, 1167-1169, 1173-1175, 1179-1217, 1224-1234, 1239-1281
src\gui\widgets\contabilita\giornaliere_tab.py                         166    136    18%   46-49, 53-94, 98, 101-130, 133-140, 144, 147-168, 171-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     17    48%   21-31, 37-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 94     76    19%   23-24, 28-29, 32-49, 71-91, 94-132, 136, 140-161, 165-194, 198, 202
src\gui\widgets\data_table.py                                          107      1    99%   129
src\gui\widgets\excel_table.py                                         327     94    71%   63-70, 86, 97, 101, 108, 114, 142-166, 170-196, 202, 229, 234, 251-252, 259-264, 276, 318-377, 388, 421, 430-433, 436-438, 479-480, 517-519, 538, 552
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     52     52     0%   1-66
src\gui\widgets\info_widgets.py                                         89     38    57%   26-59, 62, 82-110
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-435, 439-443, 447-449, 453-454, 458-462, 467-468, 472-513, 517-521, 525-530
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     14    82%   273-314, 328, 344, 361-362
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41      7    83%   28-30, 35-37, 76
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69      1    99%   60
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         66      7    89%   15-16, 70-72, 90-92
src\utils\helpers.py                                                    90     52    42%   30-34, 50-72, 85-87, 92, 119-120, 128, 141-155, 169-171, 186-192, 207, 226, 243-246
src\utils\log_humanizer.py                                              41     26    37%   18-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     14    74%   14, 17, 21, 32-33, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           56     21    62%   16-26, 45, 49, 62-68, 73-74, 79-80
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     23    71%   43-44, 81-83, 103, 105, 110-112, 117, 123-138
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23633  15917    33%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_gui_advanced.py::TestGUIAdvanced::test_kpi_panel_initialization
1 failed in 18.47s

```
</details>

---
