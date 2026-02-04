# 📊 Test Execution Report

**Date:** 2026-02-04 20:17:12
**Duration:** 2564.98s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1447 |
| ✅ Passed | 334 |
| ❌ Failed | 1 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_contabilita_kpi_panel_deep.py::TestContabilitaKPIPanelDeep::test_load_kpi_data_and_plotting`
**Error:** `FAILED tests/unit/test_contabilita_kpi_panel_deep.py::TestContabilitaKPIPanelDeep::test_load_kpi_data_and_plotting`

**Timestamp:** `2026-02-04T20:17:12.552255`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestContabilitaKPIPanelDeep.test_load_kpi_data_and_plotting _________
tests\unit\test_contabilita_kpi_panel_deep.py:58: in test_load_kpi_data_and_plotting
    assert len(panel.fig1.axes) > 0
E   AttributeError: 'ContabilitaKPIPanel' object has no attribute 'fig1'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266     34    87%   76, 82, 144-145, 234-236, 250, 277, 382, 411-413, 426-427, 431-435, 439-441, 445, 449-457, 476-478, 501
src\bots\base\login_page.py                                             94     58    38%   45-61, 65-95, 99-115, 141-142, 153-169, 174-179
src\bots\base\wait_helpers.py                                          171    144    16%   49-56, 77-82, 101-105, 136-208, 231, 260-320, 340-341, 344-348, 361, 364-368, 390-393, 396-408, 438-454, 484-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     15    69%   56, 60-72, 86, 92, 95, 101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     12    78%   34-36, 49-51, 79-81, 118-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    144    32%   51-57, 68-99, 110-129, 133-168, 172-184, 248, 267-275, 294-298, 309-317, 321-341, 351-385, 389-400, 404-417, 423-436
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    154    32%   61, 80-82, 86-101, 105-122, 126-147, 153-181, 185-221, 225-234, 238-269, 274, 309-311, 317-354, 358-367, 387, 396-418, 423-433
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     44    58%   45-46, 73-75, 107-109, 115-154, 160-185, 191-200
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     49    35%   26, 31, 36, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         161    100    38%   45-60, 84-86, 90-149, 168-169, 186-188, 191, 211-212, 216-217, 222-250, 254-267, 272-317
src\bots\portale_fornitori\timbrature\storage.py                       191    120    37%   95-120, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 344-346, 355, 361-363, 386-387, 391-410, 419-420
src\bots\safework\base.py                                               41     17    59%   21, 40-43, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    317    22%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 257, 268-270, 273-275, 281-282, 290-295, 301-333, 337-349, 353-381, 385-429, 433-453, 457-478, 482-496, 504, 515, 520-546, 550, 564-565, 585, 591-594, 598-621
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             84      0   100%
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 173-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              140     18    87%   50, 62-63, 179-182, 193, 195, 206-207, 223, 241-242, 252, 290, 292-293
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72      2    97%   55-56
src\core\backup_manager.py                                             137     21    85%   59-61, 68, 95, 110-112, 117, 124, 180-189, 216, 222-224, 231, 249-250
src\core\bug_reporter.py                                               160     42    74%   81, 85-86, 90-91, 95-96, 129-130, 135-138, 143-144, 186-188, 211-213, 218-241, 294-297, 307, 317-320, 348
src\core\config_manager.py                                             241     38    84%   119, 140, 163, 226, 284, 301-302, 331-358, 400-419, 431, 440, 472-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     47    56%   29, 34, 39, 55, 77-135, 144-153, 162-171, 184, 204, 209, 214, 219, 228, 238
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          139    112    19%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 250-307
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
src\core\importers\base.py                                              63     39    38%   14-15, 22-24, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     21    82%   37, 46, 50, 53-54, 63, 93, 107-108, 141, 150, 162, 166-167, 171, 174-179
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 219-239, 244-252, 257-275, 280-288, 292-295
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 72-76, 99-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          143     48    66%   52, 56, 79-83, 102, 135-144, 167-197, 234-236, 272-279, 283, 287, 326-327, 331, 344, 349, 354
src\core\logging\config.py                                              39      1    97%   74
src\core\logging\context.py                                             53      7    87%   29-30, 53, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 119, 148-186
src\core\logging\filters.py                                             64     32    50%   92, 112, 120, 127, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84      8    90%   84, 125, 168, 198, 234-244
src\core\logging\logger.py                                             111     17    85%   84, 95-98, 125, 151-152, 170-171, 181-182, 233, 261, 309-314
src\core\logging\metadata.py                                            85     85     0%   5-202
src\core\logging\metrics.py                                            109     59    46%   62-63, 80-113, 165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              103     65    37%   54, 71-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 231-233, 239-241
src\core\logging\viewer.py                                             187    155    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-90, 99-118
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     51    47%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 109, 116-119, 126-128, 135-136, 141-147
src\core\stats_manager.py                                               47     16    66%   40-45, 48, 61, 63, 71-79, 83
src\core\sync_tracker.py                                                59     22    63%   32-36, 47-48, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            343    290    15%   28-30, 34-43, 47-65, 69-72, 76-83, 87-94, 97-124, 127-150, 153-158, 162-177, 180-196, 201-204, 207-208, 211-219, 222-230, 233-258, 262-287, 290-294, 297-302, 306-323, 326-334, 337-350, 353-366, 370-375, 379-385, 389-397, 401-427, 431-444, 448-455, 460-466, 469-496, 499-511, 514-531
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\controllers\bot_controller.py                                   38     30    21%   17-20, 24-32, 36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           154    124    19%   37-38, 42-58, 62-78, 81-99, 102-105, 108-111, 114-117, 120-123, 126-129, 132-135, 138-141, 144-147, 150-153, 156-159, 163-169, 173-177, 181-186, 198-240, 244-260, 264-266, 270-271, 275-276, 280-313, 317-318
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-46, 50-52, 56-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\controllers\service_controller.py                              206    182    12%   28-40, 48-65, 73-131, 138-166, 170-337, 349-352, 371-379, 392-433, 446-466, 470, 476-487
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   231    209    10%   51-55, 58-67, 74-79, 82-233, 237-245, 248-278, 283-309, 313-319, 323-473, 477-495
src\gui\dialogs\command_palette.py                                     302    274     9%   39-70, 74-187, 191-217, 220-228, 231-237, 240-245, 248-255, 258-298, 302-311, 314-323, 326-332, 335-341, 345-349, 353-367, 371-382, 385-392, 397-401, 404-448, 451-487, 491-507, 510-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      239    239     0%   6-396
src\gui\formatters.py                                                  129     67    48%   13, 21-27, 37-68, 73, 98, 104, 114, 120-122, 138, 165-217, 227-229, 234-235
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     55    24%   17-22, 26-32, 38-52, 56-67, 72-81, 85-335
src\gui\main_window\components\status_bar.py                           158    141    11%   25-29, 32-104, 108-113, 117-130, 134-146, 150-211, 215-282
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-43
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 29-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21     14    33%   9-10, 15-29, 35-52
src\gui\main_window\main.py                                            280    206    26%   46-95, 99-135, 147-152, 155-179, 182-188, 192, 195, 198, 201, 204, 207, 210, 213, 217-257, 260, 263-285, 290-294, 302-306, 314-318, 326-330, 338-340, 343-345, 348-350, 353-357, 360-364, 367-371, 374-387, 390-392, 395-415, 418-421, 426-429, 432-438, 441-443, 446-449, 452, 455, 460-461, 468, 472, 476, 480, 484, 488
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          128     23    82%   56, 101, 114-115, 125, 131, 133, 143-145, 167-168, 173-175, 183, 185, 187, 190-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200     27    86%   60-77, 89-93, 214, 226, 235, 255-257, 382-385, 395, 402
src\gui\panels\carico_ts.py                                             91     23    75%   42-44, 100, 104-108, 114, 118, 124-125, 133-139, 143-150, 166-167
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            149      5    97%   189, 215, 220, 295-296
src\gui\panels\contabilita_panel.py                                    252    217    14%   38-45, 49-55, 59-163, 167-174, 178, 182, 206-222, 226-247, 252-276, 280-282, 286-289, 293-318, 324-344, 347-348, 351-355, 360-381, 384-386, 389-406, 410, 413-432
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-128, 132-134, 138-148, 152-167, 172-187, 192-210, 215-231, 236-245, 249-266, 270-300, 304-310
src\gui\panels\dettagli_oda.py                                         135     73    46%   38-42, 95-97, 101, 104-116, 120, 136-138, 146, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    152    128    16%   23-49, 56-99, 108-198, 203-216, 221-244, 249-313
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         293    261    11%   31-34, 38, 42-43, 46-53, 56-63, 66-101, 115-118, 121-163, 166-167, 174-175, 178-233, 236, 244, 256-270, 273-452, 456-503, 508-555, 561-591, 595-602, 606-613
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
src\gui\panels\pdl\pdl_detail_view.py                                   46     38    17%   17-20, 23-49, 53-68, 72-73
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        336    300    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-584
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    303    266    12%   44-46, 51-85, 96-105, 109-229, 233-248, 252-283, 287-289, 293-301, 305-326, 330-332, 336-354, 365-394, 398-403, 407-419, 423-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          296     80    73%   86-119, 142-144, 183, 280-288, 291-294, 300, 306-308, 328, 331-333, 337-345, 350-357, 368-371, 376, 381, 401-407, 410-413, 457, 467, 517, 522
src\gui\panels\scarico_ts.py                                           122     24    80%   38-40, 85-87, 106, 113, 128-130, 172-183, 193-197
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            321    268    17%   32-33, 36-62, 67-84, 87-110, 113-132, 135-154, 157-176, 179-198, 203-209, 212-213, 222, 232, 244-253, 256-264, 269-272, 275-282, 285-293, 296-312, 315-324, 327-333, 338-347, 350-364, 367-376, 379-385, 390-391, 394, 397-400, 403-410, 413-418, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 455, 460-467, 472-487
src\gui\panels\settings\pages\paths_page.py                            107     86    20%   26-27, 30-80, 83-104, 108-129, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179, 184-201, 204-219
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 100-102
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           47     39    17%   17-20, 23-49, 53-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                249    217    13%   44-107, 110-175, 179-189, 193-296, 299-311, 314, 317, 320-324, 327-333, 337-359, 365-425, 428-433, 438-460, 464-484
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     64     30    53%   73-117, 121-140
src\gui\panels\timbrature\components\settings_tab.py                    94      4    96%   147, 161-163
src\gui\panels\timbrature\panel.py                                     158     25    84%   223-241, 244-251, 265, 280-281, 285
src\gui\panels\timbrature_bot.py                                       116     35    70%   40-42, 62-64, 95, 106-111, 121-122, 134-142, 149-161, 184-186, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70     54    23%   25-28, 33, 40-50, 54-97, 102-127, 132
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     14    82%   94-103, 114-115, 127, 129, 131
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   38, 46-47
src\gui\widgets\audit_log_widget.py                                    102     16    84%   125-137, 140, 143-144, 148, 180-182
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 70     63    10%   19-125, 129-146, 150-167
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      112      6    95%   153, 157-159, 207-208
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-171, 174-187, 190-200, 203-208, 211-229, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    209    37%   47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 321-380, 389-395, 424, 433-436, 439-441, 516-520, 533-558
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   26-82, 85-92, 97-102, 105-109, 112-115, 119-125
src\gui\widgets\footer\components.py                                    48     33    31%   16-29, 32, 39-45, 48-55, 62-64, 67-68, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     27    23%   11-31, 34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     53     40    25%   17-49, 52-54, 57-58, 61-67
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
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
src\utils\date_utils.py                                                 69     55    20%   32-43, 59-70, 84-90, 103-106, 122-126, 142-152, 165-173, 189-191, 204-205, 219, 233-238
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     21    68%   15-16, 25-34, 51-52, 70-72, 79-80, 90-92
src\utils\helpers.py                                                    97     55    43%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 250, 259
src\utils\log_humanizer.py                                              41     14    66%   12-26, 112, 120
src\utils\parsing.py                                                    53     11    79%   14, 17, 21, 62, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     19    56%   22-36, 54-60, 65-66, 71-72
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           25     16    36%   46-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23909  15781    34%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_kpi_panel_deep.py::TestContabilitaKPIPanelDeep::test_load_kpi_data_and_plotting
1 failed in 37.23s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x000001CAAB544EA0>
Traceback (most recent call last):
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
    if not left_dir.resolve().exists():
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\pathlib.py", line 860, in exists
    self.stat(follow_symlinks=follow_symlinks)
  File "C:\Program Files\Python312\Lib\pathlib.py", line 840, in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Accesso negato: 'C:\\Users\\gianc\\AppData\\Local\\Temp\\pytest-of-gianc\\pytest-current'

```
</details>

---
