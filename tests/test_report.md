# 📊 Test Execution Report

**Date:** 2026-02-01 12:54:34
**Duration:** 94.29s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1004 |
| ✅ Passed | 949 |
| ❌ Failed | 21 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_base_bot_init_refactoring.py::test_init_driver_failure_handling`
**Error:** `FAILED tests/unit/test_base_bot_init_refactoring.py::test_init_driver_failure_handling`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
______________________ test_init_driver_failure_handling ______________________
tests\unit\test_base_bot_init_refactoring.py:103: in test_init_driver_failure_handling
    assert any("SUGGERIMENTO: Chrome è crashato" in log for log in logs)
E   assert False
E    +  where False = any(<generator object test_init_driver_failure_handling.<locals>.<genexpr> at 0x00000146AD01ECF0>)
---------------------------- Captured stdout call -----------------------------
[2026-02-01 09:08:10] INFO     - bot.ConcreteBot                - Inizializzazione browser... | trace=trace_f64b00... | span=span_af52931d | trace_id=trace_d7c6eb1d88f14bf2 | bot_type=testbot | bot_status=IDLE\n[2026-02-01 09:08:10] INFO     - bot.ConcreteBot                - Stato: INITIALIZING | trace=trace_f64b00... | span=span_af52931d | trace_id=trace_d7c6eb1d88f14bf2 | bot_type=testbot | bot_status=INITIALIZING\n[2026-02-01 09:08:10] INFO     - bot.ConcreteBot                - Verifica aggiornamenti driver... | trace=trace_f64b00... | span=span_af52931d | trace_id=trace_d7c6eb1d88f14bf2 | bot_type=testbot | bot_status=INITIALIZING\n[2026-02-01 09:08:10] ERROR    - bot.ConcreteBot                - Chrome driver initialization failed - browser crashed | trace=trace_f64b00... | span=span_af52931d | exc=chrome instance exited | error_type=chrome_crashed | suggestion=Ensure Chrome is updated\n[2026-02-01 09:08:10] ERROR    - bot.ConcreteBot                - \u274c ERRORE CRITICO DRIVER: Chrome \xe8 crashato all'avvio | trace=trace_f64b00... | span=span_af52931d | trace_id=trace_d7c6eb1d88f14bf2 | bot_type=testbot | bot_status=INITIALIZING\n[2026-02-01 09:08:10] INFO     - bot.ConcreteBot                - \U0001f4a1 SUGGERIMENTO: Assicurati che Chrome sia aggiornato. | trace=trace_f64b00... | span=span_af52931d | trace_id=trace_d7c6eb1d88f14bf2 | bot_type=testbot | bot_status=INITIALIZING\n[2026-02-01 09:08:10] ERROR    - src.bots.base.base_bot.BaseBot._init_driver - Function _init_driver failed after 26.73ms | trace=trace_f64b00... | span=span_af52931d | extra={'duration_ms': 26.73, 'threshold_ms': 10000}\n  Exception: Exception: chrome instance exited\nTraceback (most recent call last):\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\logging\\decorators.py", line 66, in wrapper\n    result = f(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 190, in _init_driver\n    self._handle_driver_error(e)\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 316, in _handle_driver_error\n    raise e\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 186, in _init_driver\n    self._setup_driver_instance(service, options)\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 265, in _setup_driver_instance\n    self.driver = webdriver.Chrome(service=service, options=options)\n                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Python312\\Lib\\unittest\\mock.py", line 1139, in __call__\n    return self._mock_call(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Python312\\Lib\\unittest\\mock.py", line 1143, in _mock_call\n    return self._execute_mock_call(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Python312\\Lib\\unittest\\mock.py", line 1198, in _execute_mock_call\n    raise effect\nException: chrome instance exited\n
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266    122    54%   76, 82, 106-110, 135-145, 153, 157, 161-162, 166-167, 185, 234-236, 248-250, 261, 277, 311-314, 328-377, 381-413, 418-427, 431-435, 439-441, 445, 449-457, 468-480, 484-489, 501
src\bots\base\login_page.py                                             94     74    21%   45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     28    42%   52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   40-43, 47, 51-57, 68-99, 110-129, 133-168, 172-184, 208-317, 321-341, 351-385, 389-400, 404-417, 423-436
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    186    17%   56, 60, 72-75, 79-81, 85-100, 104-121, 125-146, 152-180, 184-220, 224-233, 237-268, 272-310, 316-353, 357-366, 372-389, 395-417, 421-434
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    120    37%   95-120, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 344-346, 355, 361-363, 386-387, 391-410, 419-420
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    360    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-297, 301-333, 337-349, 353-381, 385-429, 433-453, 457-478, 482-496, 503-546, 549-594, 598-621
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86      9    90%   134-153
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 173-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              140     31    78%   50, 62-63, 179-182, 193, 195, 206-207, 223, 241-242, 252, 266-294
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137     22    84%   59-61, 68, 95, 110-112, 117, 121, 124, 180-189, 216, 222-224, 231, 249-250
src\core\bug_reporter.py                                               160    130    19%   59-110, 115-146, 151-161, 166-188, 193-213, 218-241, 246-299, 304-320, 329-348
src\core\config_manager.py                                             241    115    52%   35, 87, 113-119, 140, 145-146, 160-174, 183-184, 203-204, 226, 230-233, 250-251, 256-257, 269, 284, 294-307, 312-322, 331-358, 363-367, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102    102     0%   1-234
src\core\data_synchronizer.py                                          139    112    19%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 250-307
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     63    47%   103, 124-135, 144-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     98     0%   1-202
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 219-239, 244-252, 257-275, 280-288, 292-295
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 72-76, 99-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     48    66%   52, 56, 79-83, 100, 133-142, 165-195, 232-234, 270-277, 281, 285, 324-325, 329, 342, 347, 352
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             53      7    87%   29-30, 53, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 119, 148-186
src\core\logging\filters.py                                             64     32    50%   92, 112, 120, 127, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84     10    88%   84, 122, 125, 168, 198, 216, 234-244
src\core\logging\logger.py                                             111     20    82%   79, 90-93, 120, 146-147, 165-166, 176-177, 184-185, 220, 228, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     59    46%   62-63, 80-113, 165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              103     80    22%   20-24, 49-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 223-225, 231-233, 239-241
src\core\logging\viewer.py                                             187    155    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-66, 75-94
src\core\report_history.py                                              67     67     0%   7-163
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     58    40%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 104-109, 114-119, 126-128, 133-136, 141-147
src\core\stats_manager.py                                               47     47     0%   6-83
src\core\sync_tracker.py                                                59     22    63%   32-36, 47-48, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    289    15%   28-30, 34-43, 47-65, 69-72, 76-83, 87-94, 97-124, 127-150, 153-156, 160-175, 178-194, 199-202, 205-206, 209-217, 220-228, 231-256, 260-285, 288-292, 295-300, 304-321, 324-332, 335-348, 351-364, 368-373, 377-383, 387-395, 399-425, 429-442, 446-453, 458-464, 467-494, 497-509, 512-529
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\controllers\bot_controller.py                                   38     30    21%   17-20, 24-32, 36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           154    125    19%   36-37, 41-57, 61-77, 80-98, 101-104, 107-110, 113-116, 119-122, 125-128, 131-134, 137-140, 143-146, 149-152, 155-158, 162-168, 172-176, 180-186, 198-240, 244-260, 264-266, 270-271, 275-276, 280-313, 317-318
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-46, 50-52, 56-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-55, 63-125, 132-162, 166-350, 362-365, 384-392, 405-446, 459-479, 483, 489-500
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   231    209    10%   51-55, 58-67, 74-79, 82-233, 237-245, 248-278, 283-309, 313-319, 323-473, 477-495
src\gui\dialogs\command_palette.py                                     302    274     9%   39-70, 74-187, 191-217, 220-228, 231-237, 240-245, 248-255, 258-298, 302-311, 314-323, 326-332, 335-341, 345-349, 353-367, 371-382, 385-392, 397-401, 404-448, 451-487, 491-507, 510-527
src\gui\dialogs\confirmation_dialog.py                                  84     84     0%   1-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                                      239    239     0%   6-396
src\gui\formatters.py                                                  129    129     0%   1-237
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
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 200    200     0%   6-403
src\gui\panels\carico_ts.py                                             91     91     0%   6-185
src\gui\panels\contabilita_kpi\__init__.py                               2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py                             14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                               197    197     0%   1-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            149    149     0%   1-296
src\gui\panels\contabilita_panel.py                                    252    252     0%   6-432
src\gui\panels\dashboard_panel.py                                      168    168     0%   1-310
src\gui\panels\dettagli_oda.py                                         135    135     0%   6-241
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py                             158    158     0%   1-334
src\gui\panels\health_panel.py                                         292    292     0%   8-612
src\gui\panels\help_panel.py                                           120    120     0%   6-368
src\gui\panels\lyra\__init__.py                                          2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                                        32     32     0%   1-56
src\gui\panels\lyra\header.py                                           36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                                        41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                                      146    146     0%   1-220
src\gui\panels\lyra\workers.py                                          37     37     0%   1-59
src\gui\panels\notifications_panel.py                                  253    253     0%   6-458
src\gui\panels\pdl\__init__.py                                           2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                                      13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                                   68     68     0%   1-108
src\gui\panels\pdl\pdl_filter_widget.py                                 67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                                        336    336     0%   6-584
src\gui\panels\prenota_bp.py                                           105    105     0%   6-189
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                                    303    303     0%   7-524
src\gui\panels\scarico_pdl.py                                          296    296     0%   6-541
src\gui\panels\scarico_ts.py                                           122    122     0%   6-221
src\gui\panels\storico_oda\__init__.py                                   2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                              39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py                           47     47     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                                245    245     0%   6-477
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     158    158     0%   1-285
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-212
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70     54    23%   25-28, 33, 40-50, 54-97, 102-127, 132
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    137     0%   1-326
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     14    82%   94-103, 114-115, 127, 129, 131
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   38, 46-47
src\gui\widgets\audit_log_widget.py                                    102     16    84%   125-137, 140, 143-144, 148, 180-182
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                              141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                                 70     70     0%   1-167
src\gui\widgets\autopilot\main_widget.py                               197    197     0%   6-349
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    292    12%   29-36, 47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   26-82, 85-92, 97-102, 105-109, 112-115, 119-125
src\gui\widgets\footer\components.py                                    48     33    31%   16-29, 32, 39-45, 48-55, 62-64, 67-68, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     27    23%   11-31, 34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     53     40    25%   17-49, 52-54, 57-58, 61-67
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     53     0%   7-127
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    220     0%   6-531
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-284
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      244    210    14%   15-22, 29-63, 67-71, 75, 78-79, 82-86, 89-101, 105-113, 125-150, 154-156, 160-162, 166-169, 173-196, 200-218, 221-390, 394, 398, 402, 406-407, 411-412, 420-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     21    68%   15-16, 25-34, 51-52, 70-72, 79-80, 90-92
src\utils\helpers.py                                                    97     58    40%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 250, 256-259
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                20620  16476    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_base_bot_init_refactoring.py::test_init_driver_failure_handling
1 failed in 15.97s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x0000014685A07560>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_base_bot_init_refactoring.py::test_init_driver_version_error`
**Error:** `FAILED tests/unit/test_base_bot_init_refactoring.py::test_init_driver_version_error`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_______________________ test_init_driver_version_error ________________________
tests\unit\test_base_bot_init_refactoring.py:122: in test_init_driver_version_error
    assert any("SUGGERIMENTO: La tua versione di Chrome" in log for log in logs)
E   assert False
E    +  where False = any(<generator object test_init_driver_version_error.<locals>.<genexpr> at 0x0000016B02BD2CF0>)
---------------------------- Captured stdout call -----------------------------
[2026-02-01 09:11:25] INFO     - bot.ConcreteBot                - Inizializzazione browser... | trace=trace_20cdbe... | span=span_fd1c06a8 | trace_id=trace_02a3754e05e04928 | bot_type=testbot | bot_status=IDLE\n[2026-02-01 09:11:25] INFO     - bot.ConcreteBot                - Stato: INITIALIZING | trace=trace_20cdbe... | span=span_fd1c06a8 | trace_id=trace_02a3754e05e04928 | bot_type=testbot | bot_status=INITIALIZING\n[2026-02-01 09:11:25] INFO     - bot.ConcreteBot                - Verifica aggiornamenti driver... | trace=trace_20cdbe... | span=span_fd1c06a8 | trace_id=trace_02a3754e05e04928 | bot_type=testbot | bot_status=INITIALIZING\n[2026-02-01 09:11:25] ERROR    - bot.ConcreteBot                - Chrome driver initialization failed - version mismatch | trace=trace_20cdbe... | span=span_fd1c06a8 | exc=sessionnotcreatedexception: version mismatch | error_type=version_mismatch | suggestion=Update Chrome or download compatible chromedriver\n[2026-02-01 09:11:25] ERROR    - bot.ConcreteBot                - \u274c ERRORE CRITICO DRIVER: Versione incompatibile | trace=trace_20cdbe... | span=span_fd1c06a8 | trace_id=trace_02a3754e05e04928 | bot_type=testbot | bot_status=INITIALIZING\n[2026-02-01 09:11:25] INFO     - bot.ConcreteBot                - \U0001f4a1 SUGGERIMENTO: Aggiorna Chrome o scarica chromedriver compatibile. | trace=trace_20cdbe... | span=span_fd1c06a8 | trace_id=trace_02a3754e05e04928 | bot_type=testbot | bot_status=INITIALIZING\n[2026-02-01 09:11:25] ERROR    - src.bots.base.base_bot.BaseBot._init_driver - Function _init_driver failed after 20.04ms | trace=trace_20cdbe... | span=span_fd1c06a8 | extra={'duration_ms': 20.04, 'threshold_ms': 10000}\n  Exception: Exception: sessionnotcreatedexception: version mismatch\nTraceback (most recent call last):\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\logging\\decorators.py", line 66, in wrapper\n    result = f(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 190, in _init_driver\n    self._handle_driver_error(e)\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 316, in _handle_driver_error\n    raise e\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 186, in _init_driver\n    self._setup_driver_instance(service, options)\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 265, in _setup_driver_instance\n    self.driver = webdriver.Chrome(service=service, options=options)\n                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Python312\\Lib\\unittest\\mock.py", line 1139, in __call__\n    return self._mock_call(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Python312\\Lib\\unittest\\mock.py", line 1143, in _mock_call\n    return self._execute_mock_call(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Python312\\Lib\\unittest\\mock.py", line 1198, in _execute_mock_call\n    raise effect\nException: sessionnotcreatedexception: version mismatch\n
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266    122    54%   76, 82, 106-110, 135-145, 153, 157, 161-162, 166-167, 185, 234-236, 248-250, 261, 277, 311-314, 328-377, 381-413, 418-427, 431-435, 439-441, 445, 449-457, 468-480, 484-489, 501
src\bots\base\login_page.py                                             94     74    21%   45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     28    42%   52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   40-43, 47, 51-57, 68-99, 110-129, 133-168, 172-184, 208-317, 321-341, 351-385, 389-400, 404-417, 423-436
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    186    17%   56, 60, 72-75, 79-81, 85-100, 104-121, 125-146, 152-180, 184-220, 224-233, 237-268, 272-310, 316-353, 357-366, 372-389, 395-417, 421-434
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    120    37%   95-120, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 344-346, 355, 361-363, 386-387, 391-410, 419-420
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    360    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-297, 301-333, 337-349, 353-381, 385-429, 433-453, 457-478, 482-496, 503-546, 549-594, 598-621
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86      9    90%   134-153
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 173-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              140     31    78%   50, 62-63, 179-182, 193, 195, 206-207, 223, 241-242, 252, 266-294
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137     22    84%   59-61, 68, 95, 110-112, 117, 121, 124, 180-189, 216, 222-224, 231, 249-250
src\core\bug_reporter.py                                               160    130    19%   59-110, 115-146, 151-161, 166-188, 193-213, 218-241, 246-299, 304-320, 329-348
src\core\config_manager.py                                             241    115    52%   35, 87, 113-119, 140, 145-146, 160-174, 183-184, 203-204, 226, 230-233, 250-251, 256-257, 269, 284, 294-307, 312-322, 331-358, 363-367, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102    102     0%   1-234
src\core\data_synchronizer.py                                          139    112    19%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 250-307
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     63    47%   103, 124-135, 144-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     98     0%   1-202
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 219-239, 244-252, 257-275, 280-288, 292-295
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 72-76, 99-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     48    66%   52, 56, 79-83, 100, 133-142, 165-195, 232-234, 270-277, 281, 285, 324-325, 329, 342, 347, 352
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             53      7    87%   29-30, 53, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 119, 148-186
src\core\logging\filters.py                                             64     32    50%   92, 112, 120, 127, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84     10    88%   84, 122, 125, 168, 198, 216, 234-244
src\core\logging\logger.py                                             111     20    82%   79, 90-93, 120, 146-147, 165-166, 176-177, 184-185, 220, 228, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     59    46%   62-63, 80-113, 165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              103     80    22%   20-24, 49-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 223-225, 231-233, 239-241
src\core\logging\viewer.py                                             187    155    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-66, 75-94
src\core\report_history.py                                              67     67     0%   7-163
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     58    40%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 104-109, 114-119, 126-128, 133-136, 141-147
src\core\stats_manager.py                                               47     47     0%   6-83
src\core\sync_tracker.py                                                59     22    63%   32-36, 47-48, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    289    15%   28-30, 34-43, 47-65, 69-72, 76-83, 87-94, 97-124, 127-150, 153-156, 160-175, 178-194, 199-202, 205-206, 209-217, 220-228, 231-256, 260-285, 288-292, 295-300, 304-321, 324-332, 335-348, 351-364, 368-373, 377-383, 387-395, 399-425, 429-442, 446-453, 458-464, 467-494, 497-509, 512-529
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\controllers\bot_controller.py                                   38     30    21%   17-20, 24-32, 36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           154    125    19%   36-37, 41-57, 61-77, 80-98, 101-104, 107-110, 113-116, 119-122, 125-128, 131-134, 137-140, 143-146, 149-152, 155-158, 162-168, 172-176, 180-186, 198-240, 244-260, 264-266, 270-271, 275-276, 280-313, 317-318
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-46, 50-52, 56-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-55, 63-125, 132-162, 166-350, 362-365, 384-392, 405-446, 459-479, 483, 489-500
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   231    209    10%   51-55, 58-67, 74-79, 82-233, 237-245, 248-278, 283-309, 313-319, 323-473, 477-495
src\gui\dialogs\command_palette.py                                     302    274     9%   39-70, 74-187, 191-217, 220-228, 231-237, 240-245, 248-255, 258-298, 302-311, 314-323, 326-332, 335-341, 345-349, 353-367, 371-382, 385-392, 397-401, 404-448, 451-487, 491-507, 510-527
src\gui\dialogs\confirmation_dialog.py                                  84     84     0%   1-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                                      239    239     0%   6-396
src\gui\formatters.py                                                  129    129     0%   1-237
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
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 200    200     0%   6-403
src\gui\panels\carico_ts.py                                             91     91     0%   6-185
src\gui\panels\contabilita_kpi\__init__.py                               2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py                             14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                               197    197     0%   1-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            149    149     0%   1-296
src\gui\panels\contabilita_panel.py                                    252    252     0%   6-432
src\gui\panels\dashboard_panel.py                                      168    168     0%   1-310
src\gui\panels\dettagli_oda.py                                         135    135     0%   6-241
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py                             158    158     0%   1-334
src\gui\panels\health_panel.py                                         292    292     0%   8-612
src\gui\panels\help_panel.py                                           120    120     0%   6-368
src\gui\panels\lyra\__init__.py                                          2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                                        32     32     0%   1-56
src\gui\panels\lyra\header.py                                           36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                                        41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                                      146    146     0%   1-220
src\gui\panels\lyra\workers.py                                          37     37     0%   1-59
src\gui\panels\notifications_panel.py                                  253    253     0%   6-458
src\gui\panels\pdl\__init__.py                                           2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                                      13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                                   68     68     0%   1-108
src\gui\panels\pdl\pdl_filter_widget.py                                 67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                                        336    336     0%   6-584
src\gui\panels\prenota_bp.py                                           105    105     0%   6-189
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                                    303    303     0%   7-524
src\gui\panels\scarico_pdl.py                                          296    296     0%   6-541
src\gui\panels\scarico_ts.py                                           122    122     0%   6-221
src\gui\panels\storico_oda\__init__.py                                   2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                              39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py                           47     47     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                                245    245     0%   6-477
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     158    158     0%   1-285
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-212
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70     54    23%   25-28, 33, 40-50, 54-97, 102-127, 132
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    137     0%   1-326
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     14    82%   94-103, 114-115, 127, 129, 131
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   38, 46-47
src\gui\widgets\audit_log_widget.py                                    102     16    84%   125-137, 140, 143-144, 148, 180-182
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                              141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                                 70     70     0%   1-167
src\gui\widgets\autopilot\main_widget.py                               197    197     0%   6-349
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    292    12%   29-36, 47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   26-82, 85-92, 97-102, 105-109, 112-115, 119-125
src\gui\widgets\footer\components.py                                    48     33    31%   16-29, 32, 39-45, 48-55, 62-64, 67-68, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     27    23%   11-31, 34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     53     40    25%   17-49, 52-54, 57-58, 61-67
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     53     0%   7-127
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    220     0%   6-531
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-284
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      244    210    14%   15-22, 29-63, 67-71, 75, 78-79, 82-86, 89-101, 105-113, 125-150, 154-156, 160-162, 166-169, 173-196, 200-218, 221-390, 394, 398, 402, 406-407, 411-412, 420-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-39, 43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     21    68%   15-16, 25-34, 51-52, 70-72, 79-80, 90-92
src\utils\helpers.py                                                    97     58    40%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 250, 256-259
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                20620  16476    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_base_bot_init_refactoring.py::test_init_driver_version_error
1 failed in 17.14s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x0000016B5B477560>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_base_bot_panel.py::TestBaseBotPanel::test_ask_user_input`
**Error:** `Timeout`

<details><summary>Full Output</summary>

```text
Execution Timed Out
```
</details>

---
### `tests/unit/test_bot_panels_deep_dive.py::TestBaseBotPanel::test_ask_user_input`
**Error:** `Timeout`

<details><summary>Full Output</summary>

```text
Execution Timed Out
```
</details>

---
### `tests/unit/test_contabilita_panel_refactoring.py::test_update_selection_total_table`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
_____________ ERROR at setup of test_update_selection_total_table _____________
tests\unit\test_contabilita_panel_refactoring.py:28: in panel
    mocker.patch(
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:448: in __call__
    return self._start_patch(
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:266: in _start_patch
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
src\bots\__init__.py                                                    21      6    71%   121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266     47    82%   76, 82, 144-145, 157, 185, 234-236, 248-250, 261, 277, 311-314, 382, 411-413, 426-427, 431-435, 439-441, 445, 449-457, 476-480, 485-489, 501
src\bots\base\login_page.py                                             94     63    33%   45-61, 65-95, 99-115, 119-125, 141-142, 153-169, 174-179
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
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
src\bots\portale_fornitori\scarico_ts\bot.py                           225    155    31%   60, 79-81, 85-100, 104-121, 125-146, 152-180, 184-220, 224-233, 237-268, 273, 308-310, 316-353, 357-366, 386, 395-417, 421-434
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     56    46%   40-46, 73-75, 107-109, 115-154, 160-185, 191-200, 206-215
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     49    35%   26, 31, 36, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    102    37%   45-60, 84-86, 90-155, 174-175, 192-194, 197, 217-218, 222-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    120    37%   95-120, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 344-346, 355, 361-363, 386-387, 391-410, 419-420
src\bots\safework\base.py                                               41     17    59%   21, 40-43, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    317    22%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 257, 268-270, 273-275, 281-282, 290-295, 301-333, 337-349, 353-381, 385-429, 433-453, 457-478, 482-496, 504, 515, 520-546, 550, 564-565, 585, 591-594, 598-621
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86      9    90%   134-153
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 173-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              140     31    78%   50, 62-63, 179-182, 193, 195, 206-207, 223, 241-242, 252, 266-294
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137     22    84%   59-61, 68, 95, 110-112, 117, 121, 124, 180-189, 216, 222-224, 231, 249-250
src\core\bug_reporter.py                                               160    130    19%   59-110, 115-146, 151-161, 166-188, 193-213, 218-241, 246-299, 304-320, 329-348
src\core\config_manager.py                                             241     65    73%   35, 113-119, 140, 163, 226, 284, 301-302, 331-358, 379-381, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     25    76%   29, 39, 79, 119, 134-135, 144-153, 162-171, 184, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     63    28%   20, 29-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          139     70    50%   22, 72-74, 80-111, 118, 166-167, 179-217, 223, 235, 250-307
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      5    88%   49, 63, 76, 80, 104
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     21    67%   14-15, 22-24, 50-55, 70-80, 90-92
src\core\importers\certificati.py                                      119     21    82%   37, 46, 50, 53-54, 63, 93, 107-108, 141, 150, 162, 166-167, 171, 174-179
src\core\importers\contabilita.py                                      140     27    81%   39, 46-54, 67, 77, 89, 103-105, 119, 127, 141-142, 151, 200-202, 220, 240, 242
src\core\importers\giornaliere.py                                      189    151    20%   38, 43-55, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 219-239, 244-252, 257-275, 280-288, 292-295
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 72-76, 99-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     48    66%   52, 56, 79-83, 100, 133-142, 165-195, 232-234, 270-277, 281, 285, 324-325, 329, 342, 347, 352
src\core\logging\config.py                                              39      1    97%   74
src\core\logging\context.py                                             53      7    87%   29-30, 53, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 119, 148-186
src\core\logging\filters.py                                             64     32    50%   92, 112, 120, 127, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84      8    90%   84, 125, 168, 198, 234-244
src\core\logging\logger.py                                             111     17    85%   79, 90-93, 120, 146-147, 165-166, 176-177, 228, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     59    46%   62-63, 80-113, 165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              103     65    37%   54, 71-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 231-233, 239-241
src\core\logging\viewer.py                                             187    155    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-66, 75-94
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             96     51    47%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 109, 116-119, 126-128, 135-136, 141-147
src\core\stats_manager.py                                               47     16    66%   40-45, 48, 61, 63, 71-79, 83
src\core\sync_tracker.py                                                59     22    63%   32-36, 47-48, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    289    15%   28-30, 34-43, 47-65, 69-72, 76-83, 87-94, 97-124, 127-150, 153-156, 160-175, 178-194, 199-202, 205-206, 209-217, 220-228, 231-256, 260-285, 288-292, 295-300, 304-321, 324-332, 335-348, 351-364, 368-373, 377-383, 387-395, 399-425, 429-442, 446-453, 458-464, 467-494, 497-509, 512-529
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
src\gui\controllers\navigation_controller.py                           154    125    19%   36-37, 41-57, 61-77, 80-98, 101-104, 107-110, 113-116, 119-122, 125-128, 131-134, 137-140, 143-146, 149-152, 155-158, 162-168, 172-176, 180-186, 198-240, 244-260, 264-266, 270-271, 275-276, 280-313, 317-318
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-46, 50-52, 56-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-55, 63-125, 132-162, 166-350, 362-365, 384-392, 405-446, 459-479, 483, 489-500
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
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-63, 70-78, 81-84, 88-92, 95-158, 161-217, 220-284, 287-328, 331-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            149    130    13%   35-41, 44-162, 175-179, 182-194, 197-207, 210, 213-296
src\gui\panels\contabilita_panel.py                                    252    217    14%   38-45, 49-55, 59-163, 167-174, 178, 182, 206-222, 226-247, 252-276, 280-282, 286-289, 293-318, 324-344, 347-348, 351-355, 360-381, 384-386, 389-406, 410, 413-432
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-128, 132-134, 138-148, 152-167, 172-187, 192-210, 215-231, 236-245, 249-266, 270-300, 304-310
src\gui\panels\dettagli_oda.py                                         135     73    46%   38-42, 95-97, 101, 104-116, 120, 136-138, 146, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    142    118    17%   23-49, 56-99, 108-198, 203-216, 221-244, 249-282
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         292    261    11%   30-33, 37, 41-42, 45-52, 55-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-601, 605-612
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
src\gui\panels\pdl\pdl_detail_view.py                                   68     58    15%   17-20, 23-49, 54, 58-84, 88-103, 107-108
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
src\gui\panels\storico_oda\oda_panel.py                                245    214    13%   43-106, 109-174, 178-188, 192-295, 298-310, 313, 316, 319-323, 326-332, 336-358, 364-418, 421-426, 431-453, 457-477
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     29    54%   73-117, 121-139
src\gui\panels\timbrature\components\settings_tab.py                    94      4    96%   147, 161-163
src\gui\panels\timbrature\panel.py                                     158     25    84%   223-241, 244-251, 265, 280-281, 285
src\gui\panels\timbrature_bot.py                                       116     35    70%   40-42, 62-64, 95, 106-111, 121-122, 134-142, 149-161, 184-186, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70     54    23%   25-28, 33, 40-50, 54-97, 102-127, 132
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45     45     0%   6-90
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
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
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
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     21    68%   15-16, 25-34, 51-52, 70-72, 79-80, 90-92
src\utils\helpers.py                                                    97     55    43%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 250, 259
src\utils\log_humanizer.py                                              41     14    66%   12-26, 112, 120
src\utils\parsing.py                                                    53     18    66%   14, 17, 21, 45-46, 62, 64, 79, 84-97, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     24    70%   43-44, 81-83, 103, 105, 110-112, 117, 120-125, 129-135
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23796  16115    32%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_contabilita_panel_refactoring.py::test_update_selection_total_table
1 error in 21.02s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x00000231AEEE7560>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_data_synchronizer_deep.py::TestDataSynchronizerDeep::test_sync_contabilita_dati_incremental`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
_ ERROR at setup of TestDataSynchronizerDeep.test_sync_contabilita_dati_incremental _
tests\unit\test_data_synchronizer_deep.py:14: in db_path
    manager._mig_contabilita_v1(conn)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'DatabaseManager' object has no attribute '_mig_contabilita_v1'
----------------------------- Captured log setup ------------------------------
ERROR    src.core.database.manager:manager.py:132 Unexpected Database Error (test_sync.db): 'DatabaseManager' object has no attribute '_mig_contabilita_v1'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266    120    55%   76, 82, 106-110, 135-145, 153, 157, 161-162, 166-167, 185, 234-236, 250, 261, 277, 311-314, 328-377, 381-413, 418-427, 431-435, 439-441, 445, 449-457, 468-480, 484-489, 501
src\bots\base\login_page.py                                             94     74    21%   45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   40-43, 47, 51-57, 68-99, 110-129, 133-168, 172-184, 208-317, 321-341, 351-385, 389-400, 404-417, 423-436
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-146, 152-180, 184-220, 224-233, 237-268, 272-310, 316-353, 357-366, 372-389, 395-417, 421-434
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    166    13%   43-44, 48-83, 87-88, 95-120, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 304-346, 349-387, 391-410, 419-420
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    360    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-297, 301-333, 337-349, 353-381, 385-429, 433-453, 457-478, 482-496, 503-546, 549-594, 598-621
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86     86     0%   5-166
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      3     0%   1-4
src\core\audit\database.py                                              99     99     0%   1-175
src\core\audit\integrity.py                                             15     15     0%   1-26
src\core\audit\manager.py                                              140    140     0%   1-294
src\core\audit\models.py                                                 9      9     0%   1-13
src\core\audit\signals.py                                               27     27     0%   1-40
src\core\audit_manager.py                                                5      5     0%   6-11
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    137     0%   6-250
src\core\bug_reporter.py                                               160    160     0%   11-348
src\core\config_manager.py                                             241    171    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106    106     0%   6-243
src\core\contabilita_queries.py                                         87     87     0%   6-122
src\core\contabilita_search.py                                          91     91     0%   6-178
src\core\contabilita_stats.py                                           59     59     0%   6-105
src\core\contabilita_worker.py                                         102    102     0%   1-234
src\core\data_synchronizer.py                                          139    112    19%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 250-307
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     58    51%   103, 123-124, 127-130, 144-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     98     0%   1-202
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     94    33%   52, 56, 70-75, 79-83, 92-118, 127-156, 165-195, 208-209, 213-215, 226-243, 266-287, 300-331, 342, 347, 352
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             53      9    83%   29-30, 34-35, 53, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 119, 148-186
src\core\logging\filters.py                                             64     32    50%   92, 112, 120, 127, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84     11    87%   84, 122, 125, 138, 168, 198, 216, 234-244
src\core\logging\logger.py                                             111     20    82%   79, 90-93, 120, 146-147, 165-166, 176-177, 184-185, 220, 228, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     59    46%   62-63, 80-113, 165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              103     80    22%   20-24, 49-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 223-225, 231-233, 239-241
src\core\logging\viewer.py                                             187    156    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 161, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128    128     0%   6-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     97     0%   6-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-66, 75-94
src\core\report_history.py                                              67     67     0%   7-163
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     60    38%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 104-109, 114-119, 124-128, 133-136, 141-147
src\core\stats_manager.py                                               47     47     0%   6-83
src\core\sync_tracker.py                                                59     38    36%   25-38, 43-48, 63-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\service.py                                           175    175     0%   1-314
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                                  59     59     0%   1-120
src\gui\dialogs\bug_report_dialog.py                                   231    231     0%   10-495
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     84     0%   1-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                                      239    239     0%   6-396
src\gui\formatters.py                                                  129    129     0%   1-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-335
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            280    280     0%   1-488
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 200    200     0%   6-403
src\gui\panels\carico_ts.py                                             91     91     0%   6-185
src\gui\panels\contabilita_kpi\__init__.py                               2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py                             14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                               197    197     0%   1-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            149    149     0%   1-296
src\gui\panels\contabilita_panel.py                                    252    252     0%   6-432
src\gui\panels\dashboard_panel.py                                      168    168     0%   1-310
src\gui\panels\dettagli_oda.py                                         135    135     0%   6-241
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py                             158    158     0%   1-334
src\gui\panels\health_panel.py                                         292    292     0%   8-612
src\gui\panels\help_panel.py                                           120    120     0%   6-368
src\gui\panels\lyra\__init__.py                                          2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                                        32     32     0%   1-56
src\gui\panels\lyra\header.py                                           36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                                        41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                                      146    146     0%   1-220
src\gui\panels\lyra\workers.py                                          37     37     0%   1-59
src\gui\panels\notifications_panel.py                                  253    253     0%   6-458
src\gui\panels\pdl\__init__.py                                           2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                                      13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                                   68     68     0%   1-108
src\gui\panels\pdl\pdl_filter_widget.py                                 67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                                        336    336     0%   6-584
src\gui\panels\prenota_bp.py                                           105    105     0%   6-189
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                                    303    303     0%   7-524
src\gui\panels\scarico_pdl.py                                          296    296     0%   6-541
src\gui\panels\scarico_ts.py                                           122    122     0%   6-221
src\gui\panels\storico_oda\__init__.py                                   2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                              39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py                           47     47     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                                245    245     0%   6-477
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     158    158     0%   1-285
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-212
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-132
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12     12     0%   6-24
src\gui\widgets\activity_feed.py                                       137    137     0%   1-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                                    102    102     0%   7-182
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                              141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                                 70     70     0%   1-167
src\gui\widgets\autopilot\main_widget.py                               197    197     0%   6-349
src\gui\widgets\bot_parameters.py                                      112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                                   16     16     0%   6-79
src\gui\widgets\data_table.py                                          109    109     0%   5-217
src\gui\widgets\excel_table.py                                         330    330     0%   6-558
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     53     53     0%   1-67
src\gui\widgets\info_widgets.py                                         89     89     0%   6-175
src\gui\widgets\message_bubble.py                                       53     53     0%   7-127
src\gui\widgets\modern_button.py                                        61     61     0%   5-151
src\gui\widgets\notification_card.py                                   220    220     0%   6-531
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-284
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     45     0%   1-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-229
src\gui\widgets\status_card.py                                          59     59     0%   1-131
src\gui\widgets\status_indicator.py                                     42     42     0%   6-68
src\gui\widgets\timeline_widget.py                                     191    191     0%   6-334
src\gui\widgets\toast.py                                               128    128     0%   5-253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     66     0%   6-92
src\utils\helpers.py                                                    97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                              41     41     0%   6-121
src\utils\parsing.py                                                    53     53     0%   6-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                19263  17463     9%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_data_synchronizer_deep.py::TestDataSynchronizerDeep::test_sync_contabilita_dati_incremental
1 error in 15.13s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x0000023FA86176A0>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_data_synchronizer_extended.py::TestDataSynchronizerDetailed::test_sync_attivita_programmate`
**Error:** `FAILED tests/unit/test_data_synchronizer_extended.py::TestDataSynchronizerDetailed::test_sync_attivita_programmate`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestDataSynchronizerDetailed.test_sync_attivita_programmate _________
tests\unit\test_data_synchronizer_extended.py:62: in test_sync_attivita_programmate
    added, removed = DataSynchronizer.sync_attivita_programmate(
src\core\data_synchronizer.py:167: in sync_attivita_programmate
    return cls._sync_generic(
           ^^^^^^^^^^^^^^^^^
E   AttributeError: type object 'DataSynchronizer' has no attribute '_sync_generic'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266    211    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-145, 149, 153, 157, 161-162, 166-167, 172-190, 194-239, 244-261, 265-267, 276-281, 285-316, 328-377, 381-413, 418-427, 431-435, 439-441, 445, 449-457, 468-480, 484-489, 501
src\bots\base\login_page.py                                             94     78    17%   34-37, 45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   40-43, 47, 51-57, 68-99, 110-129, 133-168, 172-184, 208-317, 321-341, 351-385, 389-400, 404-417, 423-436
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-146, 152-180, 184-220, 224-233, 237-268, 272-310, 316-353, 357-366, 372-389, 395-417, 421-434
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    166    13%   43-44, 48-83, 87-88, 95-120, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 304-346, 349-387, 391-410, 419-420
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    360    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-297, 301-333, 337-349, 353-381, 385-429, 433-453, 457-478, 482-496, 503-546, 549-594, 598-621
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86     86     0%   5-166
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              140    108    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-182, 188-207, 211-242, 245-246, 249, 252, 255-258, 266-294
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               160    160     0%   11-348
src\core\config_manager.py                                             241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     53    50%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 204, 219, 228, 238
src\core\contabilita_queries.py                                         87     27    69%   20, 29-30, 36, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      3    95%   60, 66, 90
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          139     31    78%   22, 72-74, 118, 223, 235, 250-307
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     62    48%   124-135, 144-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py                             23     11    52%   72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     94    33%   52, 56, 70-75, 79-83, 92-118, 127-156, 165-195, 208-209, 213-215, 226-243, 266-287, 300-331, 342, 347, 352
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             53     29    45%   23-25, 29-30, 34-35, 39-40, 44-45, 49, 53, 62, 80-97, 107, 117, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     50    22%   48-111, 119, 148-186
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             111     66    41%   74-93, 97-98, 117-185, 205-208, 212, 216, 220, 224, 228, 239, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     81    26%   23-26, 30, 46-50, 59-63, 80-113, 131-133, 136-138, 155-165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307, 313
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              103     80    22%   20-24, 49-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 223-225, 231-233, 239-241
src\core\logging\viewer.py                                             187    156    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 161, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32     24    25%   22-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-66, 75-94
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     60    38%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 104-109, 114-119, 124-128, 133-136, 141-147
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-38, 43-48, 63-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   231    231     0%   10-495
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      239    239     0%   6-396
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 104, 107, 110, 113-140, 143-148, 151-154, 158-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-335
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            280    280     0%   1-488
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             91     70    23%   29-37, 40-44, 49-93, 97-100, 104-108, 112-120, 124-125, 129-185
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            149      5    97%   189, 215, 220, 295-296
src\gui\panels\contabilita_panel.py                                    252    112    56%   49-55, 167-174, 178, 211-213, 222, 226-247, 252-276, 280-282, 286-289, 297-302, 305-318, 331-333, 343-344, 355, 366, 379-380, 385, 389-406, 410, 413-432
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-128, 132-134, 138-148, 152-167, 172-187, 192-210, 215-231, 236-245, 249-266, 270-300, 304-310
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    142    118    17%   23-49, 56-99, 108-198, 203-216, 221-244, 249-282
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         292    261    11%   30-33, 37, 41-42, 45-52, 55-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-601, 605-612
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
src\gui\panels\pdl\pdl_detail_view.py                                   68     58    15%   17-20, 23-49, 54, 58-84, 88-103, 107-108
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        336    300    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-584
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    303    266    12%   44-46, 51-85, 96-105, 109-229, 233-248, 252-283, 287-289, 293-301, 305-326, 330-332, 336-354, 365-394, 398-403, 407-419, 423-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          296    257    13%   40-57, 61-82, 86-119, 129-137, 140-144, 148-277, 280-288, 291-294, 297-310, 313-324, 328, 331-333, 337-345, 350-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
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
src\gui\panels\storico_oda\oda_panel.py                                245    214    13%   43-106, 109-174, 178-188, 192-295, 298-310, 313, 316, 319-323, 326-332, 336-358, 364-418, 421-426, 431-453, 457-477
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-132
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-137, 140, 143-144, 147-165, 168-177, 180-182
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 70     63    10%   19-125, 129-146, 150-167
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            208     57    73%   131, 192, 205-208, 228, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222     54    76%   192, 217-218, 313, 330, 360-362, 408, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    289    12%   47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     53     53     0%   1-67
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
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     65    33%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 250, 256-259
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     19    64%   14, 17, 21, 32-33, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23045  18304    21%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_data_synchronizer_extended.py::TestDataSynchronizerDetailed::test_sync_attivita_programmate
1 failed in 14.41s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x00000176131D76A0>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_database_coverage.py::TestDatabaseManager::test_init_db_and_migrations`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
______ ERROR at setup of TestDatabaseManager.test_init_db_and_migrations ______
tests\unit\test_database_coverage.py:21: in manager
    mocker.patch("src.core.database.CONFIG_DIR", tmp_path)
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:448: in __call__
    return self._start_patch(
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:266: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.core.database' from 'C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\database\\__init__.py'> does not have the attribute 'CONFIG_DIR'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      21     21     0%   6-142
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                266    266     0%   6-501
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               86     86     0%   5-166
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit\__init__.py                                 3      3     0%   1-4
src\core\audit\database.py                                99     99     0%   1-175
src\core\audit\integrity.py                               15     15     0%   1-26
src\core\audit\manager.py                                140    140     0%   1-294
src\core\audit\models.py                                   9      9     0%   1-13
src\core\audit\signals.py                                 27     27     0%   1-40
src\core\audit_manager.py                                  5      5     0%   6-11
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                 160    160     0%   11-348
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     96      0   100%
src\core\contabilita_manager.py                          106    106     0%   6-243
src\core\contabilita_queries.py                           87     87     0%   6-122
src\core\contabilita_search.py                            91     91     0%   6-178
src\core\contabilita_stats.py                             59     59     0%   6-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            139     25    82%   22, 72-74, 83-111, 118, 223, 235, 251, 269, 271
src\core\database\__init__.py                              2      0   100%
src\core\database\manager.py                             119     15    87%   103, 127-130, 169-176, 199-200, 228-230
src\core\database\migrations\contabilita.py               23      0   100%
src\core\database\migrations\dipendenti.py                17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                       19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py               11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                27      0   100%
src\core\employees.py                                     98     98     0%   1-202
src\core\excel_importer.py                                 4      0   100%
src\core\importers\__init__.py                            43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                            64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                        119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                        140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                        189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                        198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                         85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\logging\__init__.py                              10     10     0%   6-37
src\core\logging\alert_manager.py                        121    121     0%   7-252
src\core\logging\analytics.py                            141    141     0%   7-352
src\core\logging\config.py                                39     39     0%   5-89
src\core\logging\context.py                               53     53     0%   5-157
src\core\logging\decorators.py                            64     64     0%   5-186
src\core\logging\filters.py                               64     64     0%   5-215
src\core\logging\formatters.py                            84     84     0%   5-244
src\core\logging\logger.py                               111    111     0%   5-309
src\core\logging\metadata.py                              83     83     0%   5-200
src\core\logging\metrics.py                              109    109     0%   5-313
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              56     56     0%   5-204
src\core\logging\sinks.py                                103    103     0%   5-241
src\core\logging\viewer.py                               187    187     0%   5-451
src\core\lyra_client.py                                  128    128     0%   6-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                   33     33     0%   6-94
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                               96     60    38%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 104-109, 114-119, 124-128, 133-136, 141-147
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\sync_tracker.py                                  59     59     0%   1-108
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             175    175     0%   1-314
src\core\telegram_bridge.py                              342    342     0%   1-529
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\design\colors.py                                  27      0   100%
src\gui\design\spacing.py                                 25      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                    59     59     0%   1-120
src\gui\dialogs\bug_report_dialog.py                     231    231     0%   10-495
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-131
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                        239    239     0%   6-396
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-335
src\gui\main_window\components\status_bar.py             158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                25     25     0%   1-43
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-52
src\gui\main_window\main.py                              280    280     0%   1-488
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   200    200     0%   6-403
src\gui\panels\carico_ts.py                               91     91     0%   6-185
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 197    197     0%   1-389
src\gui\panels\contabilita_kpi\kpi_panel.py              149    149     0%   1-296
src\gui\panels\contabilita_panel.py                      252    252     0%   6-432
src\gui\panels\dashboard_panel.py                        168    168     0%   1-310
src\gui\panels\dettagli_oda.py                           135    135     0%   6-241
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py               158    158     0%   1-334
src\gui\panels\health_panel.py                           292    292     0%   8-612
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          32     32     0%   1-56
src\gui\panels\lyra\header.py                             36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        146    146     0%   1-220
src\gui\panels\lyra\workers.py                            37     37     0%   1-59
src\gui\panels\notifications_panel.py                    253    253     0%   6-458
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                     68     68     0%   1-108
src\gui\panels\pdl\pdl_filter_widget.py                   67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                          336    336     0%   6-584
src\gui\panels\prenota_bp.py                             105    105     0%   6-189
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      303    303     0%   7-524
src\gui\panels\scarico_pdl.py                            296    296     0%   6-541
src\gui\panels\scarico_ts.py                             122    122     0%   6-221
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py             47     47     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py           41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                  245    245     0%   6-477
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       158    158     0%   1-285
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-156
src\gui\styles\theme_manager.py                           70     70     0%   6-132
src\gui\styles\widget_styles.py                           35     35     0%   6-391
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12      0   100%
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-182
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                   70     70     0%   1-167
src\gui\widgets\autopilot\main_widget.py                 197    197     0%   6-349
src\gui\widgets\bot_parameters.py                        112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                     16     11    31%   16-79
src\gui\widgets\data_table.py                            109      1    99%   129
src\gui\widgets\excel_table.py                           330    289    12%   47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   88     88     0%   1-125
src\gui\widgets\footer\components.py                      48     48     0%   1-87
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                       53     53     0%   1-67
src\gui\widgets\info_widgets.py                           89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                         53     53     0%   7-127
src\gui\widgets\modern_button.py                          61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        244    244     0%   1-456
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                       42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                       191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                 128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-299
src\utils\date_utils.py                                   69     69     0%   6-238
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     65    33%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 250, 256-259
src\utils\log_humanizer.py                                41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                      53     53     0%   6-119
src\utils\printing.py                                     83     83     0%   1-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-142
src\utils\system_telemetry.py                             25     25     0%   6-70
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  17238  16058     7%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_database_coverage.py::TestDatabaseManager::test_init_db_and_migrations
1 error in 8.70s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x000002105AC47560>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_database_security_stress.py::TestDatabaseSecurityStress::test_database_wal_mode_concurrency`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
_ ERROR at setup of TestDatabaseSecurityStress.test_database_wal_mode_concurrency _
tests\unit\test_database_security_stress.py:16: in db_mgr
    mocker.patch("src.core.database.CONFIG_DIR", tmp_path)
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:448: in __call__
    return self._start_patch(
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:266: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.core.database' from 'C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\database\\__init__.py'> does not have the attribute 'CONFIG_DIR'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      21     21     0%   6-142
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                266    266     0%   6-501
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               86     86     0%   5-166
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit\__init__.py                                 3      3     0%   1-4
src\core\audit\database.py                                99     99     0%   1-175
src\core\audit\integrity.py                               15     15     0%   1-26
src\core\audit\manager.py                                140    140     0%   1-294
src\core\audit\models.py                                   9      9     0%   1-13
src\core\audit\signals.py                                 27     27     0%   1-40
src\core\audit_manager.py                                  5      5     0%   6-11
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                 160    160     0%   11-348
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     96     96     0%   6-134
src\core\contabilita_manager.py                          106    106     0%   6-243
src\core\contabilita_queries.py                           87     87     0%   6-122
src\core\contabilita_search.py                            91     91     0%   6-178
src\core\contabilita_stats.py                             59     59     0%   6-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            139    139     0%   6-307
src\core\database\__init__.py                              2      0   100%
src\core\database\manager.py                             119     16    87%   103, 131-135, 169-176, 199-200, 228-230
src\core\database\migrations\contabilita.py               23      0   100%
src\core\database\migrations\dipendenti.py                17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                       19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py               11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                27      0   100%
src\core\employees.py                                     98     98     0%   1-202
src\core\excel_importer.py                                 4      4     0%   6-11
src\core\importers\__init__.py                            43     43     0%   1-111
src\core\importers\attivita.py                            64     64     0%   1-117
src\core\importers\base.py                                63     63     0%   1-92
src\core\importers\certificati.py                        119    119     0%   1-187
src\core\importers\contabilita.py                        140    140     0%   1-260
src\core\importers\giornaliere.py                        189    189     0%   1-309
src\core\importers\scarico_ore.py                        198    198     0%   1-316
src\core\importers\storico_oda.py                         85     85     0%   1-195
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\logging\__init__.py                              10     10     0%   6-37
src\core\logging\alert_manager.py                        121    121     0%   7-252
src\core\logging\analytics.py                            141    141     0%   7-352
src\core\logging\config.py                                39     39     0%   5-89
src\core\logging\context.py                               53     53     0%   5-157
src\core\logging\decorators.py                            64     64     0%   5-186
src\core\logging\filters.py                               64     64     0%   5-215
src\core\logging\formatters.py                            84     84     0%   5-244
src\core\logging\logger.py                               111    111     0%   5-309
src\core\logging\metadata.py                              83     83     0%   5-200
src\core\logging\metrics.py                              109    109     0%   5-313
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              56     56     0%   5-204
src\core\logging\sinks.py                                103    103     0%   5-241
src\core\logging\viewer.py                               187    187     0%   5-451
src\core\lyra_client.py                                  128    128     0%   6-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     97     0%   6-204
src\core\oda_manager.py                                   33     33     0%   6-94
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     78     0%   1-109
src\core\secrets_manager.py                               96     60    38%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 104-109, 114-119, 124-128, 133-136, 141-147
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\sync_tracker.py                                  59     59     0%   1-108
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             175    175     0%   1-314
src\core\telegram_bridge.py                              342    342     0%   1-529
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                    59     59     0%   1-120
src\gui\dialogs\bug_report_dialog.py                     231    231     0%   10-495
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-131
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                        239    239     0%   6-396
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-335
src\gui\main_window\components\status_bar.py             158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                25     25     0%   1-43
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-52
src\gui\main_window\main.py                              280    280     0%   1-488
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   200    200     0%   6-403
src\gui\panels\carico_ts.py                               91     91     0%   6-185
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 197    197     0%   1-389
src\gui\panels\contabilita_kpi\kpi_panel.py              149    149     0%   1-296
src\gui\panels\contabilita_panel.py                      252    252     0%   6-432
src\gui\panels\dashboard_panel.py                        168    168     0%   1-310
src\gui\panels\dettagli_oda.py                           135    135     0%   6-241
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py               158    158     0%   1-334
src\gui\panels\health_panel.py                           292    292     0%   8-612
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          32     32     0%   1-56
src\gui\panels\lyra\header.py                             36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        146    146     0%   1-220
src\gui\panels\lyra\workers.py                            37     37     0%   1-59
src\gui\panels\notifications_panel.py                    253    253     0%   6-458
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                     68     68     0%   1-108
src\gui\panels\pdl\pdl_filter_widget.py                   67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                          336    336     0%   6-584
src\gui\panels\prenota_bp.py                             105    105     0%   6-189
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      303    303     0%   7-524
src\gui\panels\scarico_pdl.py                            296    296     0%   6-541
src\gui\panels\scarico_ts.py                             122    122     0%   6-221
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py             47     47     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py           41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                  245    245     0%   6-477
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       158    158     0%   1-285
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-156
src\gui\styles\theme_manager.py                           70     70     0%   6-132
src\gui\styles\widget_styles.py                           35     35     0%   6-391
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-182
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                   70     70     0%   1-167
src\gui\widgets\autopilot\main_widget.py                 197    197     0%   6-349
src\gui\widgets\bot_parameters.py                        112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            109    109     0%   5-217
src\gui\widgets\excel_table.py                           330    330     0%   6-558
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   88     88     0%   1-125
src\gui\widgets\footer\components.py                      48     48     0%   1-87
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                       53     53     0%   1-67
src\gui\widgets\info_widgets.py                           89     89     0%   6-175
src\gui\widgets\message_bubble.py                         53     53     0%   7-127
src\gui\widgets\modern_button.py                          61     61     0%   5-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        244    244     0%   1-456
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       191    191     0%   6-334
src\gui\widgets\toast.py                                 128    128     0%   5-253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-299
src\utils\date_utils.py                                   69     69     0%   6-238
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                41     41     0%   6-121
src\utils\parsing.py                                      53     53     0%   6-119
src\utils\printing.py                                     83     83     0%   1-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     23    71%   43-44, 81-83, 103, 105, 110-112, 117, 123-138
src\utils\system_telemetry.py                             25     25     0%   6-70
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  17186  16858     2%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_database_security_stress.py::TestDatabaseSecurityStress::test_database_wal_mode_concurrency
1 error in 8.82s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x0000020A0FB576A0>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_e2e_workflows_hardened.py::TestE2EWorkflowsHardened::test_workflow_import_to_search`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
__ ERROR at setup of TestE2EWorkflowsHardened.test_workflow_import_to_search __
tests\unit\test_e2e_workflows_hardened.py:15: in db_mgr
    mocker.patch("src.core.database.CONFIG_DIR", tmp_path)
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:448: in __call__
    return self._start_patch(
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:266: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.core.database' from 'C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\database\\__init__.py'> does not have the attribute 'CONFIG_DIR'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266    189    29%   76, 82, 87, 92-94, 106-110, 122, 135-145, 149, 153, 157, 161-162, 167, 172-190, 194-239, 244-261, 265-267, 276-281, 285-316, 328-377, 381-413, 418-427, 431-435, 439-441, 445, 449-457, 468-480, 484-489, 501
src\bots\base\login_page.py                                             94     78    17%   34-37, 45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     15    81%   21, 26, 31, 42, 61, 64, 75, 106, 111, 127-128, 130-131, 142, 149
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212     67    68%   51-57, 96-99, 110-129, 145-147, 165-168, 182-184, 248, 267-275, 294-298, 309-317, 340-341, 357-358, 368, 373-380, 383-385, 396-397, 399-400, 417
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-146, 152-180, 184-220, 224-233, 237-268, 272-310, 316-353, 357-366, 372-389, 395-417, 421-434
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    166    13%   43-44, 48-83, 87-88, 95-120, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 304-346, 349-387, 391-410, 419-420
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    360    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-297, 301-333, 337-349, 353-381, 385-429, 433-453, 457-478, 482-496, 503-546, 549-594, 598-621
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86     86     0%   5-166
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      3     0%   1-4
src\core\audit\database.py                                              99     99     0%   1-175
src\core\audit\integrity.py                                             15     15     0%   1-26
src\core\audit\manager.py                                              140    140     0%   1-294
src\core\audit\models.py                                                 9      9     0%   1-13
src\core\audit\signals.py                                               27     27     0%   1-40
src\core\audit_manager.py                                                5      5     0%   6-11
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    137     0%   6-250
src\core\bug_reporter.py                                               160    160     0%   11-348
src\core\config_manager.py                                             241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102    102     0%   1-234
src\core\data_synchronizer.py                                          139    112    19%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 250-307
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     36    70%   103, 126-135, 164-176, 199-200, 203, 214-230
src\core\database\migrations\contabilita.py                             23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     98     0%   1-202
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      9    79%   32, 49, 63, 76, 80, 91, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     62    27%   61-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     94    33%   52, 56, 70-75, 79-83, 92-118, 127-156, 165-195, 208-209, 213-215, 226-243, 266-287, 300-331, 342, 347, 352
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             53     23    57%   29-30, 34-35, 39-40, 44-45, 53, 80-97, 117, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     50    22%   48-111, 119, 148-186
src\core\logging\filters.py                                             64     35    45%   92, 112, 120, 123, 126-129, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84     23    73%   84, 88-90, 122, 125, 132, 138, 168, 198, 209-219, 228, 234-244
src\core\logging\logger.py                                             111     32    71%   79, 90-93, 120, 134-136, 146-147, 162-166, 170-177, 184-185, 206, 212, 220, 224, 228, 239, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     81    26%   23-26, 30, 46-50, 59-63, 80-113, 131-133, 136-138, 155-165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307, 313
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     17    70%   58, 67, 91, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              103     80    22%   20-24, 49-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 223-225, 231-233, 239-241
src\core\logging\viewer.py                                             187    156    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 161, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128    128     0%   6-259
src\core\lyra_sentinel.py                                               32     24    25%   22-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     13    61%   30-66, 87-94
src\core\report_history.py                                              67     67     0%   7-163
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     60    38%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 104-109, 114-119, 124-128, 133-136, 141-147
src\core\stats_manager.py                                               47     47     0%   6-83
src\core\sync_tracker.py                                                59     38    36%   25-38, 43-48, 63-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\service.py                                           175    175     0%   1-314
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                                  59     59     0%   1-120
src\gui\dialogs\bug_report_dialog.py                                   231    231     0%   10-495
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     84     0%   1-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                                      239    239     0%   6-396
src\gui\formatters.py                                                  129    129     0%   1-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-335
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            280    280     0%   1-488
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 200    200     0%   6-403
src\gui\panels\carico_ts.py                                             91     91     0%   6-185
src\gui\panels\contabilita_kpi\__init__.py                               2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py                             14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                               197    197     0%   1-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            149    149     0%   1-296
src\gui\panels\contabilita_panel.py                                    252    252     0%   6-432
src\gui\panels\dashboard_panel.py                                      168    168     0%   1-310
src\gui\panels\dettagli_oda.py                                         135    135     0%   6-241
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py                             158    158     0%   1-334
src\gui\panels\health_panel.py                                         292    292     0%   8-612
src\gui\panels\help_panel.py                                           120    120     0%   6-368
src\gui\panels\lyra\__init__.py                                          2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                                        32     32     0%   1-56
src\gui\panels\lyra\header.py                                           36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                                        41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                                      146    146     0%   1-220
src\gui\panels\lyra\workers.py                                          37     37     0%   1-59
src\gui\panels\notifications_panel.py                                  253    253     0%   6-458
src\gui\panels\pdl\__init__.py                                           2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                                      13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                                   68     68     0%   1-108
src\gui\panels\pdl\pdl_filter_widget.py                                 67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                                        336    336     0%   6-584
src\gui\panels\prenota_bp.py                                           105    105     0%   6-189
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                                    303    303     0%   7-524
src\gui\panels\scarico_pdl.py                                          296    296     0%   6-541
src\gui\panels\scarico_ts.py                                           122    122     0%   6-221
src\gui\panels\storico_oda\__init__.py                                   2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                              39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py                           47     47     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                                245    245     0%   6-477
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     158    158     0%   1-285
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-212
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-132
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12     12     0%   6-24
src\gui\widgets\activity_feed.py                                       137    137     0%   1-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                                    102    102     0%   7-182
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                              141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                                 70     70     0%   1-167
src\gui\widgets\autopilot\main_widget.py                               197    197     0%   6-349
src\gui\widgets\bot_parameters.py                                      112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                                   16     16     0%   6-79
src\gui\widgets\data_table.py                                          109    109     0%   5-217
src\gui\widgets\excel_table.py                                         330    330     0%   6-558
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     53     53     0%   1-67
src\gui\widgets\info_widgets.py                                         89     89     0%   6-175
src\gui\widgets\message_bubble.py                                       53     53     0%   7-127
src\gui\widgets\modern_button.py                                        61     61     0%   5-151
src\gui\widgets\notification_card.py                                   220    220     0%   6-531
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-284
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     45     0%   1-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-229
src\gui\widgets\status_card.py                                          59     59     0%   1-131
src\gui\widgets\status_indicator.py                                     42     42     0%   6-68
src\gui\widgets\timeline_widget.py                                     191    191     0%   6-334
src\gui\widgets\toast.py                                               128    128     0%   5-253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         66      7    89%   15-16, 70-72, 90-92
src\utils\helpers.py                                                    97     70    28%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 249-267
src\utils\log_humanizer.py                                              41     41     0%   6-121
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     23    71%   43-44, 81-83, 103, 105, 110-112, 117, 123-138
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                19263  17171    11%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_e2e_workflows_hardened.py::TestE2EWorkflowsHardened::test_workflow_import_to_search
1 error in 12.93s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x000002048FF67560>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_gui_contabilita_extra.py::TestContabilitaExtra::test_contabilita_panel_init`
**Error:** `FAILED tests/unit/test_gui_contabilita_extra.py::TestContabilitaExtra::test_contabilita_panel_init`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
______________ TestContabilitaExtra.test_contabilita_panel_init _______________
tests\unit\test_gui_contabilita_extra.py:26: in test_contabilita_panel_init
    patch(
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
src\bots\base\base_bot.py                                              266    211    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-145, 149, 153, 157, 161-162, 166-167, 172-190, 194-239, 244-261, 265-267, 276-281, 285-316, 328-377, 381-413, 418-427, 431-435, 439-441, 445, 449-457, 468-480, 484-489, 501
src\bots\base\login_page.py                                             94     78    17%   34-37, 45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   40-43, 47, 51-57, 68-99, 110-129, 133-168, 172-184, 208-317, 321-341, 351-385, 389-400, 404-417, 423-436
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-146, 152-180, 184-220, 224-233, 237-268, 272-310, 316-353, 357-366, 372-389, 395-417, 421-434
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    166    13%   43-44, 48-83, 87-88, 95-120, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 304-346, 349-387, 391-410, 419-420
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    360    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-297, 301-333, 337-349, 353-381, 385-429, 433-453, 457-478, 482-496, 503-546, 549-594, 598-621
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86     86     0%   5-166
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     82    17%   18, 22-72, 75, 78-87, 91-98, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      4    73%   15-16, 21, 26
src\core\audit\manager.py                                              140    108    23%   28, 31-34, 37-41, 46, 50, 54-63, 98-182, 188-207, 211-242, 245-246, 249, 252, 255-258, 266-294
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     21    22%   13-40
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               160    160     0%   11-348
src\core\config_manager.py                                             241    171    29%   35, 77, 87, 99-100, 113-119, 135-152, 160-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     18    79%   20, 27-28, 36, 43-44, 52, 71-72, 80, 87-88, 96, 103-104, 112, 119-120
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          139    112    19%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 250-307
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     40    66%   127-130, 164-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      1    98%   104
src\core\importers\attivita.py                                          64      4    94%   57-58, 92-93
src\core\importers\base.py                                              63      7    89%   14-15, 22-24, 54-55
src\core\importers\certificati.py                                      119     16    87%   46, 50, 53-54, 63, 93, 107-108, 141, 166-167, 177-181
src\core\importers\contabilita.py                                      140     10    93%   39, 44, 48, 52-54, 119, 200-202
src\core\importers\giornaliere.py                                      189     32    83%   49-55, 72, 84, 99, 102, 106, 134, 151, 155, 179-180, 191-201, 214-215, 218, 234, 240, 248, 262
src\core\importers\scarico_ore.py                                      198     40    80%   11-12, 18-20, 47, 65-66, 72-87, 97, 100, 112-113, 126, 176, 204, 208, 217, 221, 235, 247, 256, 291, 301-302, 313-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     94    33%   52, 56, 70-75, 79-83, 92-118, 127-156, 165-195, 208-209, 213-215, 226-243, 266-287, 300-331, 342, 347, 352
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             53     29    45%   23-25, 29-30, 34-35, 39-40, 44-45, 49, 53, 62, 80-97, 107, 117, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     50    22%   48-111, 119, 148-186
src\core\logging\filters.py                                             64     48    25%   91-98, 111-131, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84     62    26%   56-108, 118-140, 168, 194-230, 234-244
src\core\logging\logger.py                                             111     66    41%   74-93, 97-98, 117-185, 205-208, 212, 216, 220, 224, 228, 239, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     81    26%   23-26, 30, 46-50, 59-63, 80-113, 131-133, 136-138, 155-165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307, 313
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     43    23%   33-44, 48, 58, 67, 86-108, 121-131, 144-157, 166, 183-185, 204
src\core\logging\sinks.py                                              103     80    22%   20-24, 49-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 223-225, 231-233, 239-241
src\core\logging\viewer.py                                             187    156    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 161, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                        97     45    54%   44, 52-59, 63-76, 83-84, 135-150, 154-156, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-66, 75-94
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     23    71%   67-72, 77-88, 93-95, 101, 108
src\core\secrets_manager.py                                             96     60    38%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 104-109, 114-119, 124-128, 133-136, 141-147
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\sync_tracker.py                                                59     38    36%   25-38, 43-48, 63-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   231    231     0%   10-495
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      239    239     0%   6-396
src\gui\formatters.py                                                  129     86    33%   12-27, 37-68, 73, 95-98, 104, 120-122, 128, 138, 158-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-335
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            280    280     0%   1-488
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             91     70    23%   29-37, 40-44, 49-93, 97-100, 104-108, 112-120, 124-125, 129-185
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-63, 70-78, 81-84, 88-92, 95-158, 161-217, 220-284, 287-328, 331-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            149    130    13%   35-41, 44-162, 175-179, 182-194, 197-207, 210, 213-296
src\gui\panels\contabilita_panel.py                                    252    217    14%   38-45, 49-55, 59-163, 167-174, 178, 182, 206-222, 226-247, 252-276, 280-282, 286-289, 293-318, 324-344, 347-348, 351-355, 360-381, 384-386, 389-406, 410, 413-432
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-128, 132-134, 138-148, 152-167, 172-187, 192-210, 215-231, 236-245, 249-266, 270-300, 304-310
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    142    118    17%   23-49, 56-99, 108-198, 203-216, 221-244, 249-282
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         292    261    11%   30-33, 37, 41-42, 45-52, 55-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-601, 605-612
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
src\gui\panels\pdl\pdl_detail_view.py                                   68     58    15%   17-20, 23-49, 54, 58-84, 88-103, 107-108
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        336    300    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-584
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    303    266    12%   44-46, 51-85, 96-105, 109-229, 233-248, 252-283, 287-289, 293-301, 305-326, 330-332, 336-354, 365-394, 398-403, 407-419, 423-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          296    257    13%   40-57, 61-82, 86-119, 129-137, 140-144, 148-277, 280-288, 291-294, 297-310, 313-324, 328, 331-333, 337-345, 350-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
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
src\gui\panels\storico_oda\oda_panel.py                                245    214    13%   43-106, 109-174, 178-188, 192-295, 298-310, 313, 316, 319-323, 326-332, 336-358, 364-418, 421-426, 431-453, 457-477
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-132
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-137, 140, 143-144, 147-165, 168-177, 180-182
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 70     63    10%   19-125, 129-146, 150-167
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-171, 174-187, 190-200, 203-208, 211-229, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330     96    71%   64-71, 87, 98, 102, 109, 115, 143-167, 171-197, 203, 230, 235, 252-255, 262-267, 279, 321-380, 391, 424, 433-436, 439-441, 482-483, 520-522, 541, 555
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     53     53     0%   1-67
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     13    79%   52-54, 71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
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
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     75    23%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 253-267
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23045  18244    21%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_gui_contabilita_extra.py::TestContabilitaExtra::test_contabilita_panel_init
1 failed in 21.53s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x000001DC7DB87560>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_hardening_audit_security.py::TestHardeningAuditSecurity::test_fts5_sync_on_update_delete`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
_ ERROR at setup of TestHardeningAuditSecurity.test_fts5_sync_on_update_delete _
tests\unit\test_hardening_audit_security.py:32: in db_env
    mocker.patch("src.core.database.CONFIG_DIR", tmp_path)
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:448: in __call__
    return self._start_patch(
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:266: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.core.database' from 'C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\database\\__init__.py'> does not have the attribute 'CONFIG_DIR'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266    211    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-145, 149, 153, 157, 161-162, 166-167, 172-190, 194-239, 244-261, 265-267, 276-281, 285-316, 328-377, 381-413, 418-427, 431-435, 439-441, 445, 449-457, 468-480, 484-489, 501
src\bots\base\login_page.py                                             94     78    17%   34-37, 45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   40-43, 47, 51-57, 68-99, 110-129, 133-168, 172-184, 208-317, 321-341, 351-385, 389-400, 404-417, 423-436
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-146, 152-180, 184-220, 224-233, 237-268, 272-310, 316-353, 357-366, 372-389, 395-417, 421-434
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    166    13%   43-44, 48-83, 87-88, 95-120, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 304-346, 349-387, 391-410, 419-420
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    360    11%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 177-207, 211-240, 244-252, 256-297, 301-333, 337-349, 353-381, 385-429, 433-453, 457-478, 482-496, 503-546, 549-594, 598-621
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86     86     0%   5-166
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     59    40%   61-65, 86-87, 110-154, 157-164, 167-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              140     55    61%   38, 46, 50, 58-63, 173, 179-182, 188-207, 223, 241-242, 245-246, 249, 252, 255-258, 266-294
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     65    53%   42, 45, 48, 59-61, 68, 71, 84, 93, 95, 110-112, 117, 122-127, 136-189, 200-208, 216, 222-224, 229-250
src\core\bug_reporter.py                                               160    160     0%   11-348
src\core\config_manager.py                                             241    136    44%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 226, 236, 250-251, 274-289, 294-307, 312-322, 331-358, 367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     53    50%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 204, 219, 228, 238
src\core\contabilita_queries.py                                         87     27    69%   20, 29-30, 36, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      3    95%   60, 66, 90
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          139    112    19%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 250-307
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
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     94    33%   52, 56, 70-75, 79-83, 92-118, 127-156, 165-195, 208-209, 213-215, 226-243, 266-287, 300-331, 342, 347, 352
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             53     22    58%   29-30, 39-40, 44-45, 53, 80-97, 107, 117, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     50    22%   48-111, 119, 148-186
src\core\logging\filters.py                                             64     33    48%   92, 112, 120, 123, 127, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84     26    69%   84, 88-90, 122, 125, 130, 132, 134, 136, 138, 168, 198, 209-219, 228, 234-244
src\core\logging\logger.py                                             111     32    71%   79, 90-93, 120, 134-136, 146-147, 162-166, 170-177, 184-185, 206, 212, 220, 224, 228, 239, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     81    26%   23-26, 30, 46-50, 59-63, 80-113, 131-133, 136-138, 155-165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307, 313
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     17    70%   58, 67, 91, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              103     80    22%   20-24, 49-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 223-225, 231-233, 239-241
src\core\logging\viewer.py                                             187    156    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 161, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32     24    25%   22-53
src\core\notification_manager.py                                        97     58    40%   44, 52-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-66, 75-94
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     53    45%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 109, 116-119, 126-128, 133-136, 141-147
src\core\stats_manager.py                                               47     15    68%   40-45, 48, 61, 63, 71-79
src\core\sync_tracker.py                                                59     38    36%   25-38, 43-48, 63-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     18    40%   22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    113    33%   75-81, 84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 179, 184, 188-214, 224-233, 247-274
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57     48    16%   20-91, 94-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   231    231     0%   10-495
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37     29    22%   20-68, 72, 77-79
src\gui\dialogs\startup_dialog.py                                      239    239     0%   6-396
src\gui\formatters.py                                                  129     58    55%   13, 21-27, 38, 47, 50, 67-68, 104, 114, 120-122, 129-140, 165-217, 227-229, 234-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-335
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            280    280     0%   1-488
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200     75    62%   89-93, 97-99, 214, 218, 226, 235, 244, 248-251, 255-257, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 402
src\gui\panels\carico_ts.py                                             91     41    55%   42-44, 100, 104-108, 112-120, 124-125, 141-185
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               197     40    80%   98-99, 106-108, 133-139, 142-154, 166-167, 190, 223-224, 231-233, 292-293, 317-319, 334-335
src\gui\panels\contabilita_kpi\kpi_panel.py                            149      5    97%   189, 215, 220, 295-296
src\gui\panels\contabilita_panel.py                                    252    117    54%   51-55, 167-174, 178, 222, 228-233, 254-258, 262-265, 271-273, 280-282, 289, 299-302, 306-310, 314-318, 324-344, 347-348, 351-355, 360-381, 384-386, 389-406, 410, 413-432
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-128, 132-134, 138-148, 152-167, 172-187, 192-210, 215-231, 236-245, 249-266, 270-300, 304-310
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    142    118    17%   23-49, 56-99, 108-198, 203-216, 221-244, 249-282
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158     83    47%   28-70, 73, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         292    261    11%   30-33, 37, 41-42, 45-52, 55-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-601, 605-612
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
src\gui\panels\pdl\pdl_detail_view.py                                   68     58    15%   17-20, 23-49, 54, 58-84, 88-103, 107-108
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        336    300    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-584
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    303    200    34%   44-46, 51-85, 233-248, 252-283, 287-289, 293-301, 305-326, 330-332, 336-354, 365-394, 398-403, 407-419, 423-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          296    257    13%   40-57, 61-82, 86-119, 129-137, 140-144, 148-277, 280-288, 291-294, 297-310, 313-324, 328, 331-333, 337-345, 350-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     56    54%   38-40, 85-87, 106, 113, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     23    78%   130-131, 140, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32      2    94%   42-43
src\gui\panels\settings\pages\general_page.py                           43      0   100%
src\gui\panels\settings\pages\lists_page.py                            321    114    64%   222, 232, 244-253, 256-264, 271, 296-312, 315-324, 327-333, 338-347, 350-364, 367-376, 379-385, 397-400, 403-410, 413-418, 422, 425, 428, 431, 434, 437, 440, 443, 446, 449, 452, 455
src\gui\panels\settings\pages\paths_page.py                            107     22    79%   113-129, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     33    75%   158-160, 166-168, 176-181, 184-185, 192-194, 202-205, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55      1    98%   113
src\gui\panels\settings\tabs\telegram_tab.py                           136     27    80%   142-149, 154-167, 172-181, 187-191, 201, 223-224
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           47     39    17%   17-20, 23-49, 53-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                245    214    13%   43-106, 109-174, 178-188, 192-295, 298-310, 313, 316, 319-323, 326-332, 336-358, 364-418, 421-426, 431-453, 457-477
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-132
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-137, 140, 143-144, 147-165, 168-177, 180-182
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 70     63    10%   19-125, 129-146, 150-167
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      112     12    89%   87-91, 153, 172, 183, 205-208
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208     57    73%   131, 192, 205-208, 228, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222     54    76%   192, 217-218, 313, 330, 360-362, 408, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166     50    70%   96, 132, 149, 176, 186-187, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     13    81%   99, 123-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    230    30%   47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 321-380, 389-395, 402-426, 433-436, 439-441, 456, 482-483, 494-524, 533-558
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     53     53     0%   1-67
src\gui\widgets\info_widgets.py                                         89     39    56%   26-59, 62, 82-110, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     13    81%   35-36, 38-39, 41-42, 58, 91-92, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      244    244     0%   1-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     32    29%   28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100      7    93%   165-167, 208-209, 224-225
src\gui\widgets\status_card.py                                          59      8    86%   106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42      6    86%   63-68
src\gui\widgets\timeline_widget.py                                     191    128    33%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 191-205, 224-234, 237-252, 257-262, 265-269, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     34    73%   141-149, 152-156, 160-162, 166-167, 172-173, 179, 210-217, 225, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     65    33%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 250, 256-259
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     19    64%   14, 17, 21, 32-33, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22      5    77%   50, 55-58
src\utils\security.py                                                   79     18    77%   43-44, 81-83, 103, 105, 110-112, 117, 123-125, 133-138
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23045  16535    28%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_hardening_audit_security.py::TestHardeningAuditSecurity::test_fts5_sync_on_update_delete
1 error in 10.20s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x000001EBD80876A0>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_safework_bot_deep.py::TestSafeWorkPDLBotDeep::test_merge_all_session_logic`
**Error:** `FAILED tests/unit/test_safework_bot_deep.py::TestSafeWorkPDLBotDeep::test_merge_all_session_logic`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_____________ TestSafeWorkPDLBotDeep.test_merge_all_session_logic _____________
tests\unit\test_safework_bot_deep.py:136: in test_merge_all_session_logic
    assert result is True
E   assert False is True
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266    211    21%   50-70, 76, 82, 87, 92-94, 106-110, 121-145, 149, 153, 157, 161-162, 166-167, 172-190, 194-239, 244-261, 265-267, 276-281, 285-316, 328-377, 381-413, 418-427, 431-435, 439-441, 445, 449-457, 468-480, 484-489, 501
src\bots\base\login_page.py                                             94     10    89%   111-115, 123, 152, 171-172, 175-176
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   40-43, 47, 51-57, 68-99, 110-129, 133-168, 172-184, 208-317, 321-341, 351-385, 389-400, 404-417, 423-436
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-146, 152-180, 184-220, 224-233, 237-268, 272-310, 316-353, 357-366, 372-389, 395-417, 421-434
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    166    13%   43-44, 48-83, 87-88, 95-120, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 304-346, 349-387, 391-410, 419-420
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    272    33%   26, 31, 36, 41, 46, 57-61, 65, 69, 73-98, 102-165, 169-173, 193-196, 198-199, 213-214, 221, 226, 231-232, 246-249, 256-297, 301-333, 337-349, 353-381, 385-429, 433-453, 470-474, 477-478, 495-496, 503-546, 550, 564-565, 586-588, 591-594, 620-621
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86     86     0%   5-166
src\core\app_updater.py                                                 46     37    20%   17-47, 52-57, 62-83, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     28    72%   61-65, 86-87, 127-130, 132-134, 136-140, 152-153, 163-164, 167-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              140     49    65%   50, 58-63, 173, 179-182, 188-207, 223, 241-242, 255-258, 266-294
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                               160    130    19%   59-110, 115-146, 151-161, 166-188, 193-213, 218-241, 246-299, 304-320, 329-348
src\core\config_manager.py                                             241    147    39%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 218-236, 250-251, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     56    47%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 199, 204, 209, 214, 219, 228, 238
src\core\contabilita_queries.py                                         87     44    49%   29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      3    95%   60, 66, 90
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          139    112    19%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 250-307
src\core\database\__init__.py                                            2      0   100%
src\core\database\manager.py                                           119     25    79%   126-135, 164-176, 199-200, 228-230
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                                     19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py                             11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                              27      0   100%
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-101, 106-122, 129-198
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155     22    86%   98-101, 149, 164-165, 195-196, 201-203, 210, 227, 249-251, 286-288, 292-295
src\core\license_validator.py                                          183     13    93%   99-117, 143, 170, 187-191
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     94    33%   52, 56, 70-75, 79-83, 92-118, 127-156, 165-195, 208-209, 213-215, 226-243, 266-287, 300-331, 342, 347, 352
src\core\logging\config.py                                              39      4    90%   71-76
src\core\logging\context.py                                             53     22    58%   29-30, 39-40, 44-45, 53, 80-97, 107, 117, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     50    22%   48-111, 119, 148-186
src\core\logging\filters.py                                             64     33    48%   92, 112, 120, 123, 127, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84     26    69%   84, 88-90, 122, 125, 130, 132, 134, 136, 138, 168, 198, 209-219, 228, 234-244
src\core\logging\logger.py                                             111     27    76%   79, 90-93, 120, 134-136, 146-147, 162-166, 176-177, 184-185, 206, 212, 220, 228, 239, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     81    26%   23-26, 30, 46-50, 59-63, 80-113, 131-133, 136-138, 155-165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307, 313
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              103     80    22%   20-24, 49-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 223-225, 231-233, 239-241
src\core\logging\viewer.py                                             187    156    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 161, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128     20    84%   22, 67-69, 83, 109-110, 117, 146-147, 203-204, 208-212, 249, 257-259
src\core\lyra_sentinel.py                                               32      4    88%   38-39, 50-51
src\core\notification_manager.py                                        97      9    91%   44, 83-84, 135-150
src\core\oda_manager.py                                                 33     20    39%   22, 30-66, 75-94
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 94, 100-102, 107-109
src\core\secrets_manager.py                                             96     39    59%   33, 38, 43, 50-53, 59-60, 68-74, 80, 88, 94, 99, 104-109, 114-119, 124-128, 133-136, 141-147
src\core\stats_manager.py                                               47      7    85%   43-45, 48, 61, 63, 76
src\core\sync_tracker.py                                                59     38    36%   25-38, 43-48, 63-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    129    26%   54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    278    19%   47-65, 69-72, 76-83, 87-94, 97-124, 127-150, 153-156, 160-175, 178-194, 199-202, 205-206, 209-217, 220-228, 231-256, 260-285, 288-292, 295-300, 304-321, 324-332, 335-348, 351-364, 368-373, 377-383, 387-395, 399-425, 429-442, 446-453, 458-464, 467-494, 497-509, 512-529
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      5    74%   30, 33-36, 55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-108, 111-126, 129-147, 150-162, 165-173, 176-181, 184-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187     71    62%   80, 84, 91-92, 115-118, 154-157, 161-165, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 251, 261, 269, 273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     11    88%   57, 65, 101, 104-105, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\controllers\bot_controller.py                                   38     20    47%   36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           154     53    66%   107-110, 113-116, 119-122, 125-128, 131-134, 137-140, 143-146, 149-152, 155-158, 203-210, 218-225, 233-240, 270-271, 275-276, 304-313
src\gui\controllers\search_controller.py                               197    177    10%   18-46, 50-52, 56-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-55, 63-125, 132-162, 166-350, 362-365, 384-392, 405-446, 459-479, 483, 489-500
src\gui\controllers\tray_controller.py                                  38      8    79%   37-38, 50-55, 61
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
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 104, 107, 110, 113-140, 143-148, 151-154, 158-237
src\gui\layouts\responsive.py                                           64     10    84%   33-39, 73, 78, 96-97
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     40    44%   26-32, 56-67, 72-81, 85-335
src\gui\main_window\components\status_bar.py                           158    107    32%   117-130, 134-146, 150-211, 215-282
src\gui\main_window\components\tool_bar.py                              25      0   100%
src\gui\main_window\components\tray_icon.py                             16      7    56%   18, 29-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   15-16, 25-34, 37-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     21      1    95%   39
src\gui\main_window\main.py                                            280    144    49%   99-135, 192, 195, 201, 204, 207, 210, 213, 217-257, 260, 263-285, 290-294, 302-306, 314-318, 326-330, 338-340, 343-345, 348-350, 360-364, 367-371, 374-387, 390-392, 395-415, 418-421, 426-429, 432-438, 441-443, 446-449, 452, 455, 460-461, 472, 476, 480, 484, 488
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          128     22    83%   56, 101, 114-115, 125, 131, 133, 143-145, 167-168, 173-175, 183, 187, 190-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    110    45%   52-56, 60-77, 89-93, 97-99, 195-206, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             91     54    41%   40-44, 97-100, 104-108, 112-120, 124-125, 129-185
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-63, 70-78, 81-84, 88-92, 95-158, 161-217, 220-284, 287-328, 331-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            149    130    13%   35-41, 44-162, 175-179, 182-194, 197-207, 210, 213-296
src\gui\panels\contabilita_panel.py                                    252    217    14%   38-45, 49-55, 59-163, 167-174, 178, 182, 206-222, 226-247, 252-276, 280-282, 286-289, 293-318, 324-344, 347-348, 351-355, 360-381, 384-386, 389-406, 410, 413-432
src\gui\panels\dashboard_panel.py                                      168     98    42%   84, 132-134, 138-148, 152-167, 172-187, 192-210, 215-231, 236-245, 249-266, 270-300, 304-310
src\gui\panels\dettagli_oda.py                                         135     86    36%   38-42, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    142    118    17%   23-49, 56-99, 108-198, 203-216, 221-244, 249-282
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         292     63    78%   65-100, 501-502, 508-510, 552-554, 560-590, 594-601, 605-612
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        32     23    28%   20-34, 38-49, 53-56
src\gui\panels\lyra\header.py                                           36     26    28%   22-26, 29-88
src\gui\panels\lyra\input_bar.py                                        41     30    27%   20-21, 24-77, 80-83, 86-88
src\gui\panels\lyra\lyra_panel.py                                      146    117    20%   31-37, 40-94, 100-124, 127-132, 135-142, 145-146, 149-150, 153-157, 160-165, 168-170, 173-184, 187-188, 191-194, 197-199, 203, 206-220
src\gui\panels\lyra\workers.py                                          37     25    32%   21-25, 28-36, 47-48, 51-59
src\gui\panels\notifications_panel.py                                  253     49    81%   157-161, 165-167, 177-179, 193, 249, 255, 257, 259, 263, 325-326, 332-348, 366-367, 375-380, 388-390, 427-438
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      13      8    38%   9-10, 13-23
src\gui\panels\pdl\pdl_detail_view.py                                   68     58    15%   17-20, 23-49, 54, 58-84, 88-103, 107-108
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        336    300    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-584
src\gui\panels\prenota_bp.py                                           105     63    40%   35-38, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           80     43    46%   71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    303    266    12%   44-46, 51-85, 96-105, 109-229, 233-248, 252-283, 287-289, 293-301, 305-326, 330-332, 336-354, 365-394, 398-403, 407-419, 423-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          296    186    37%   61-82, 86-119, 140-144, 183, 280-288, 291-294, 297-310, 313-324, 328, 331-333, 337-345, 350-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     74    39%   36-40, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
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
src\gui\panels\storico_oda\oda_panel.py                                245    214    13%   43-106, 109-174, 178-188, 192-295, 298-310, 313, 316, 319-323, 326-332, 336-358, 364-418, 421-426, 431-453, 457-477
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     83    28%   38-42, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70      5    93%   108-109, 112, 123-124
src\gui\styles\widget_styles.py                                         35      7    80%   17, 138, 151, 344-345, 362-363
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     26    81%   39-40, 88-90, 151-152, 172-182, 189, 193-195, 272, 278, 292, 294, 303-319
src\gui\widgets\animated_progress_bar.py                                74     53    28%   45-46, 50, 54-55, 59-60, 65-79, 83-141
src\gui\widgets\audit\audit_filter_bar.py                               76     14    82%   94-103, 114-115, 127, 129, 131
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   38, 46-47
src\gui\widgets\audit_log_widget.py                                    102     16    84%   125-137, 140, 143-144, 148, 180-182
src\gui\widgets\automazioni_widget.py                                   54      2    96%   124-125
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141     19    87%   169-195, 378-406
src\gui\widgets\autopilot\event_card.py                                 70     63    10%   19-125, 129-146, 150-167
src\gui\widgets\autopilot\main_widget.py                               197     75    62%   151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 241, 248, 257, 266, 275, 293-297, 301-305
src\gui\widgets\bot_parameters.py                                      112     26    77%   153, 157-159, 169-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-171, 174-187, 190-200, 203-208, 211-229, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    252    24%   47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 321-380, 389-395, 424, 433-436, 439-441, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   97-102, 113-114, 119-125
src\gui\widgets\footer\components.py                                    48     23    52%   16-29, 32, 48-55, 71-75, 78-79, 86-87
src\gui\widgets\footer\manager.py                                       20     12    40%   18-22, 27-31, 34-35
src\gui\widgets\footer\status_bar.py                                    35     11    69%   34-36, 39-42, 45-48
src\gui\widgets\footer\telemetry.py                                     53      2    96%   66-67
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61     10    84%   71-72, 78-81, 85-88
src\gui\widgets\notification_card.py                                   220     90    59%   113, 270-275, 302-316, 321-322, 329-339, 343, 361, 365-367, 381-415, 429-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47      9    81%   129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106      9    92%   238-239, 243-244, 260-261, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     11    86%   273-314, 344
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41      4    90%   47-51
src\gui\widgets\sidebar_widget.py                                      244     25    90%   82-86, 100, 109-110, 154-156, 160-162, 166-169, 398, 402, 411-412, 438-441
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     12    80%   94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42      6    86%   63-68
src\gui\widgets\timeline_widget.py                                     191     53    72%   83-84, 137-141, 161-169, 172-173, 176-178, 191-205, 221, 239-249, 265-269, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35      7    80%   43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     22    77%   28, 47, 82-83, 141, 154-168, 239, 256-259
src\utils\log_humanizer.py                                              41      3    93%   16, 20, 112
src\utils\parsing.py                                                    53      4    92%   102-119
src\utils\printing.py                                                   83     14    83%   21-23, 37-39, 50-51, 115-120, 144-145
src\utils\resource_manager.py                                           43     10    77%   22-36, 55
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79      9    89%   43-44, 81-83, 110-112, 138
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23784  15207    36%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_safework_bot_deep.py::TestSafeWorkPDLBotDeep::test_merge_all_session_logic
1 failed in 13.35s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x000001350D257560>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_settings_panel_coverage.py::TestSettingsPanelCoverage::test_add_fornitore`
**Error:** `Timeout`

<details><summary>Full Output</summary>

```text
Execution Timed Out
```
</details>

---
### `tests/unit/test_sprint_d_bot_resilience.py::TestSprintDBotResilience::test_bot_driver_initialization_failure_handling`
**Error:** `FAILED tests/unit/test_sprint_d_bot_resilience.py::TestSprintDBotResilience::test_bot_driver_initialization_failure_handling`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__ TestSprintDBotResilience.test_bot_driver_initialization_failure_handling ___
tests\unit\test_sprint_d_bot_resilience.py:113: in test_bot_driver_initialization_failure_handling
    assert any("Chrome è troppo recente" in m for m in logs)
E   assert False
E    +  where False = any(<generator object TestSprintDBotResilience.test_bot_driver_initialization_failure_handling.<locals>.<genexpr> at 0x0000016BA7C0ADC0>)
---------------------------- Captured stdout call -----------------------------
[2026-02-01 12:21:26] INFO     - bot.DummyBot                   - Inizializzazione browser... | trace=trace_fcc737... | span=span_5f89d1a0 | trace_id=trace_465b978374aa43ec | bot_type=dummy | bot_status=IDLE\n[2026-02-01 12:21:26] INFO     - bot.DummyBot                   - Stato: INITIALIZING | trace=trace_fcc737... | span=span_5f89d1a0 | trace_id=trace_465b978374aa43ec | bot_type=dummy | bot_status=INITIALIZING\n[2026-02-01 12:21:26] INFO     - bot.DummyBot                   - Verifica aggiornamenti driver... | trace=trace_fcc737... | span=span_5f89d1a0 | trace_id=trace_465b978374aa43ec | bot_type=dummy | bot_status=INITIALIZING\n[2026-02-01 12:21:29] ERROR    - bot.DummyBot                   - Chrome driver initialization failed - version mismatch | trace=trace_fcc737... | span=span_5f89d1a0 | exc=SessionNotCreatedException: version mismatch | error_type=version_mismatch | suggestion=Update Chrome or download compatible chromedriver\n[2026-02-01 12:21:29] ERROR    - bot.DummyBot                   - \u274c ERRORE CRITICO DRIVER: Versione incompatibile | trace=trace_fcc737... | span=span_5f89d1a0 | trace_id=trace_465b978374aa43ec | bot_type=dummy | bot_status=INITIALIZING\n[2026-02-01 12:21:29] INFO     - bot.DummyBot                   - \U0001f4a1 SUGGERIMENTO: Aggiorna Chrome o scarica chromedriver compatibile. | trace=trace_fcc737... | span=span_5f89d1a0 | trace_id=trace_465b978374aa43ec | bot_type=dummy | bot_status=INITIALIZING\n[2026-02-01 12:21:29] ERROR    - src.bots.base.base_bot.BaseBot._init_driver - Function _init_driver failed after 2628.47ms | trace=trace_fcc737... | span=span_5f89d1a0 | extra={'duration_ms': 2628.47, 'threshold_ms': 10000}\n  Exception: Exception: SessionNotCreatedException: version mismatch\nTraceback (most recent call last):\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\logging\\decorators.py", line 66, in wrapper\n    result = f(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 190, in _init_driver\n    self._handle_driver_error(e)\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 316, in _handle_driver_error\n    raise e\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 186, in _init_driver\n    self._setup_driver_instance(service, options)\n  File "C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\bots\\base\\base_bot.py", line 265, in _setup_driver_instance\n    self.driver = webdriver.Chrome(service=service, options=options)\n                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Python312\\Lib\\unittest\\mock.py", line 1139, in __call__\n    return self._mock_call(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Python312\\Lib\\unittest\\mock.py", line 1143, in _mock_call\n    return self._execute_mock_call(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Program Files\\Python312\\Lib\\unittest\\mock.py", line 1198, in _execute_mock_call\n    raise effect\nException: SessionNotCreatedException: version mismatch\n
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266     93    65%   76, 82, 109, 135-145, 153, 157, 185, 187-188, 219-221, 234-236, 250, 252-261, 267, 276-281, 289-297, 311-314, 346-349, 354-355, 361-363, 370-375, 382, 411-413, 418-427, 432-434, 439-441, 445, 449-457, 476-480, 485-489, 501
src\bots\base\login_page.py                                             94     78    17%   34-37, 45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   40-43, 47, 51-57, 68-99, 110-129, 133-168, 172-184, 208-317, 321-341, 351-385, 389-400, 404-417, 423-436
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225     49    78%   39, 44, 49, 60, 79-81, 92, 98, 108, 119-121, 167, 177-178, 185, 232, 238, 249-264, 273, 317, 324-325, 336, 342-347, 358, 364-366, 377, 388-389, 412-415, 431-434
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     20    81%   45-46, 73-75, 107-109, 152-154, 172-173, 183-185, 200, 212-214
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     14    76%   24, 29, 34, 41, 45, 59, 61-62, 67-68, 77, 81, 99-100
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    142    26%   97, 118-119, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 304-346, 349-387, 391-410, 419-420
src\bots\safework\base.py                                               41     19    54%   21, 27-28, 44-45, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    138    66%   26, 31, 36, 46, 65, 69, 80-81, 91, 94-95, 102-165, 193, 213-214, 257, 268-270, 281-282, 290-293, 302, 317-319, 331-333, 340-345, 354, 368-370, 380-381, 386, 391-420, 427-429, 434, 450-453, 473-474, 477-478, 495-496, 504, 516-517, 526-528, 539-544, 550, 564-565, 586-588, 591-592
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86     86     0%   5-166
src\core\app_updater.py                                                 46     37    20%   17-47, 52-57, 62-83, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 173-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              140     46    67%   50, 58-63, 173, 179-182, 188-207, 223, 241-242, 252, 266-294
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     35    74%   42, 45, 48, 59-61, 68, 71, 84, 93, 95, 110-112, 117, 122-127, 176-189, 216, 222-224, 238-250
src\core\bug_reporter.py                                               160    160     0%   11-348
src\core\config_manager.py                                             241    152    37%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 218-236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     54    49%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 199, 204, 209, 214, 219
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     14    85%   26-27, 50, 78-79, 109-110, 119, 122-123, 132-133, 152-153
src\core\contabilita_stats.py                                           59      2    97%   60, 90
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
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     94    33%   52, 56, 70-75, 79-83, 92-118, 127-156, 165-195, 208-209, 213-215, 226-243, 266-287, 300-331, 342, 347, 352
src\core\logging\config.py                                              39      1    97%   74
src\core\logging\context.py                                             53      7    87%   29-30, 53, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 119, 148-186
src\core\logging\filters.py                                             64     32    50%   92, 112, 120, 127, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84      9    89%   84, 125, 138, 168, 198, 234-244
src\core\logging\logger.py                                             111     17    85%   79, 90-93, 120, 146-147, 165-166, 176-177, 228, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     59    46%   62-63, 80-113, 165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              103     65    37%   54, 71-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 231-233, 239-241
src\core\logging\viewer.py                                             187    156    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 161, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128     30    77%   22, 55-69, 83, 109-110, 134, 146-147, 161, 169-170, 203-204, 208-212, 249, 257-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-66, 75-94
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96      8    92%   50-53, 126-128, 135-136
src\core\stats_manager.py                                               47     23    51%   40-45, 48, 52, 56-67, 71-79
src\core\sync_tracker.py                                                59     38    36%   25-38, 43-48, 63-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     55    49%   28-108, 111-126, 151, 159-162, 180-181, 188-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     18    40%   22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187     43    77%   80, 84, 91-92, 118, 157, 165, 185-190, 200-225, 244-245, 251, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169     54    68%   84, 87-100, 127, 155, 165-169, 173, 189, 193, 201-214, 227-233, 247-274
src\gui\controllers\search_controller.py                               197     69    65%   61, 93-94, 101, 118, 135, 152, 164-165, 178-215, 228-264, 277-312, 327, 335-336
src\gui\controllers\service_controller.py                              211    142    33%   117, 135-162, 166-350, 362-365, 386-387, 406-407, 425-426, 432-439, 459-479
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57      4    93%   101-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   231    231     0%   10-495
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37      0   100%
src\gui\dialogs\startup_dialog.py                                      239    239     0%   6-396
src\gui\formatters.py                                                  129     92    29%   12-27, 37-68, 73, 95-98, 104, 120-122, 128, 132, 138, 147, 151-154, 158-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-335
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            280    280     0%   1-488
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             91     70    23%   29-37, 40-44, 49-93, 97-100, 104-108, 112-120, 124-125, 129-185
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-63, 70-78, 81-84, 88-92, 95-158, 161-217, 220-284, 287-328, 331-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            149    130    13%   35-41, 44-162, 175-179, 182-194, 197-207, 210, 213-296
src\gui\panels\contabilita_panel.py                                    252    217    14%   38-45, 49-55, 59-163, 167-174, 178, 182, 206-222, 226-247, 252-276, 280-282, 286-289, 293-318, 324-344, 347-348, 351-355, 360-381, 384-386, 389-406, 410, 413-432
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-128, 132-134, 138-148, 152-167, 172-187, 192-210, 215-231, 236-245, 249-266, 270-300, 304-310
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    142    118    17%   23-49, 56-99, 108-198, 203-216, 221-244, 249-282
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         292    261    11%   30-33, 37, 41-42, 45-52, 55-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-601, 605-612
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
src\gui\panels\pdl\pdl_detail_view.py                                   68     58    15%   17-20, 23-49, 54, 58-84, 88-103, 107-108
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        336    300    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-584
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    303    102    66%   44-46, 51-85, 239-248, 255-283, 301, 308-309, 325-326, 330-332, 336-354, 376-377, 387-388, 393-394, 398-403, 411-412, 427-429, 444, 455-469, 496-499, 506
src\gui\panels\scarico_pdl.py                                          296    257    13%   40-57, 61-82, 86-119, 129-137, 140-144, 148-277, 280-288, 291-294, 297-310, 313-324, 328, 331-333, 337-345, 350-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     23    78%   103, 130-131, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32      0   100%
src\gui\panels\settings\pages\general_page.py                           43      0   100%
src\gui\panels\settings\pages\lists_page.py                            321    109    66%   222, 232, 244-253, 256-264, 271, 296-312, 315-324, 327-333, 338-347, 350-364, 367-376, 379-385, 403-410, 413-418, 422, 425, 428, 434, 437, 440, 443, 446, 449, 452, 455
src\gui\panels\settings\pages\paths_page.py                            107     19    82%   115, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     29    78%   158-160, 166-168, 181, 184-185, 192-194, 202-205, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55      1    98%   113
src\gui\panels\settings\tabs\telegram_tab.py                           136     27    80%   142-149, 154-167, 172-181, 187-191, 201, 223-224
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           47     39    17%   17-20, 23-49, 53-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                245    214    13%   43-106, 109-174, 178-188, 192-295, 298-310, 313, 316, 319-323, 326-332, 336-358, 364-418, 421-426, 431-453, 457-477
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-132
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-137, 140, 143-144, 147-165, 168-177, 180-182
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 70     63    10%   19-125, 129-146, 150-167
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-171, 174-187, 190-200, 203-208, 211-229, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    292    12%   29-36, 47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     53     53     0%   1-67
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61      4    93%   85-88
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41      7    83%   17, 46-51, 76
src\gui\widgets\sidebar_widget.py                                      244     50    80%   82-86, 100, 105-113, 154-156, 160-162, 166-169, 238, 394, 402, 406-407, 411-412, 420-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     24    76%   165-167, 194-227
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     34    73%   141-149, 152-156, 160-162, 166-167, 172-173, 179, 210-217, 225, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     55    43%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 250, 259
src\utils\log_humanizer.py                                              41     15    63%   12-26, 86, 112-113
src\utils\parsing.py                                                    53     13    75%   14, 17, 21, 32-33, 66, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79      8    90%   43-44, 81-83, 133-135
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23626  16622    30%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_sprint_d_bot_resilience.py::TestSprintDBotResilience::test_bot_driver_initialization_failure_handling
1 failed in 19.75s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x0000016B806376A0>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_telegram_manager_extended.py::test_handle_run_pdl_on`
**Error:** `FAILED tests/unit/test_telegram_manager_extended.py::test_handle_run_pdl_on`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
___________________________ test_handle_run_pdl_on ____________________________
tests\unit\test_telegram_manager_extended.py:66: in test_handle_run_pdl_on
    await telegram_service._handle_run_pdl_on(query)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   RuntimeError: super-class __init__() of type TelegramService was never called
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    21      7    67%   108, 121, 135-139
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266     93    65%   76, 82, 109, 135-145, 153, 157, 185, 187-188, 219-221, 234-236, 250, 252-261, 267, 276-281, 289-297, 311-314, 346-349, 354-355, 361-363, 370-375, 382, 411-413, 418-427, 432-434, 439-441, 445, 449-457, 476-480, 485-489, 501
src\bots\base\login_page.py                                             94     78    17%   34-37, 45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          171    171     0%   14-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-96, 100-111, 122-142, 146-151
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   40-43, 47, 51-57, 68-99, 110-129, 133-168, 172-184, 208-317, 321-341, 351-385, 389-400, 404-417, 423-436
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225     49    78%   39, 44, 49, 60, 79-81, 92, 98, 108, 119-121, 167, 177-178, 185, 232, 238, 249-264, 273, 317, 324-325, 336, 342-347, 358, 364-366, 377, 388-389, 412-415, 431-434
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     20    81%   45-46, 73-75, 107-109, 152-154, 172-173, 183-185, 200, 212-214
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     14    76%   24, 29, 34, 41, 45, 59, 61-62, 67-68, 77, 81, 99-100
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       191    142    26%   97, 118-119, 126-158, 168-180, 190-198, 203-231, 238-277, 282-297, 304-346, 349-387, 391-410, 419-420
src\bots\safework\base.py                                               41     19    54%   21, 27-28, 44-45, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           405    138    66%   26, 31, 36, 46, 65, 69, 80-81, 91, 94-95, 102-165, 193, 213-214, 257, 268-270, 281-282, 290-293, 302, 317-319, 331-333, 340-345, 354, 368-370, 380-381, 386, 391-420, 427-429, 434, 450-453, 473-474, 477-478, 495-496, 504, 516-517, 526-528, 539-544, 550, 564-565, 586-588, 591-592
src\bots\safework\pdl\search_bot.py                                    178    153    14%   21-22, 26, 30, 34-96, 100-117, 121-142, 146-157, 161-170, 174-178, 182-209, 213-243, 247-335
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             86     86     0%   5-166
src\core\app_updater.py                                                 46     37    20%   17-47, 52-57, 62-83, 87
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              99     35    65%   61-65, 86-87, 118-120, 122-125, 127-130, 132-134, 136-140, 152-153, 157-164, 173-175
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              140     46    67%   50, 58-63, 173, 179-182, 188-207, 223, 241-242, 252, 266-294
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               27     13    52%   22-39
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     35    74%   42, 45, 48, 59-61, 68, 71, 84, 93, 95, 110-112, 117, 122-127, 176-189, 216, 222-224, 238-250
src\core\bug_reporter.py                                               160    160     0%   11-348
src\core\config_manager.py                                             241    152    37%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 218-236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   96      0   100%
src\core\contabilita_manager.py                                        106     54    49%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 199, 204, 209, 214, 219
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     14    85%   26-27, 50, 78-79, 109-110, 119, 122-123, 132-133, 152-153
src\core\contabilita_stats.py                                           59      2    97%   60, 90
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
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      121     93    23%   50-52, 55-58, 63-70, 82-93, 97-116, 120-122, 126-159, 178-191, 203-222, 234-246, 252
src\core\logging\analytics.py                                          141     94    33%   52, 56, 70-75, 79-83, 92-118, 127-156, 165-195, 208-209, 213-215, 226-243, 266-287, 300-331, 342, 347, 352
src\core\logging\config.py                                              39      1    97%   74
src\core\logging\context.py                                             53      7    87%   29-30, 53, 127, 137, 147, 157
src\core\logging\decorators.py                                          64     29    55%   49, 52, 80-81, 119, 148-186
src\core\logging\filters.py                                             64     32    50%   92, 112, 120, 127, 144-158, 171-178, 196-197, 206-215
src\core\logging\formatters.py                                          84      9    89%   84, 125, 138, 168, 198, 234-244
src\core\logging\logger.py                                             111     17    85%   79, 90-93, 120, 146-147, 165-166, 176-177, 228, 256, 304-309
src\core\logging\metadata.py                                            83     83     0%   5-200
src\core\logging\metrics.py                                            109     59    46%   62-63, 80-113, 165, 179-196, 206, 218, 237-247, 256-260, 269-273, 281-284, 293-307
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            56     16    71%   58, 67, 95, 100, 105, 122, 129, 147-157, 166, 204
src\core\logging\sinks.py                                              103     65    37%   54, 71-72, 76-81, 94-107, 118-123, 133-140, 144-160, 171-173, 183-189, 201-211, 231-233, 239-241
src\core\logging\viewer.py                                             187    156    17%   18-21, 25-26, 31-40, 45-53, 57, 61, 68-82, 86-87, 91-92, 96-97, 101-128, 132-146, 161, 173-180, 189-196, 208-234, 249-273, 285-290, 306-363, 373-411, 425-426, 439-440, 450-451
src\core\lyra_client.py                                                128     30    77%   22, 55-69, 83, 109-110, 134, 146-147, 161, 169-170, 203-204, 208-212, 249, 257-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 33     20    39%   22, 30-66, 75-94
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96      8    92%   50-53, 126-128, 135-136
src\core\stats_manager.py                                               47      4    91%   48, 61, 63, 76
src\core\sync_tracker.py                                                59     38    36%   25-38, 43-48, 63-76, 81-82, 90-108
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187     94    50%   16, 19, 26-31, 36, 39-40, 47-48, 52-54, 106-110, 116-129, 142-147, 162-167, 198, 205-206, 209-210, 213-214, 219-220, 226, 249, 253-256, 264-280, 286-289, 293-306, 311, 313, 317, 321-324, 331-332, 342-348, 355, 363-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     69    30%   19-42, 47-54, 59-63, 68-90, 101, 103, 118, 120, 135-170
src\core\telegram\service.py                                           175     51    71%   56-58, 84, 88, 99-102, 107, 118, 170-171, 175-185, 211, 214-219, 225-226, 233-234, 238-239, 249-250, 254-255, 265-266, 272, 280-281, 287, 296-297, 303, 313-314
src\core\telegram\ui\keyboards.py                                       98     16    84%   113-114, 198-203, 208-217, 222-223, 242-249, 280-285, 290-295
src\core\telegram_bridge.py                                            342    167    51%   59, 61, 63, 65, 71-72, 87-94, 120, 127-150, 153-156, 178-194, 199-202, 205-206, 212-215, 220-228, 231-256, 272-274, 278-281, 291-292, 295-300, 304-321, 324-332, 335-348, 351-364, 370-373, 387-395, 399-425, 472-485, 493-494, 499-500, 506-507, 514-515, 526-527
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     55    49%   28-108, 111-126, 151, 159-162, 180-181, 188-189, 192-197
src\gui\components\scarico_ore\filters\header.py                        30     18    40%   22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187     43    77%   80, 84, 91-92, 118, 157, 165, 185-190, 200-225, 244-245, 251, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169     54    68%   84, 87-100, 127, 155, 165-169, 173, 189, 193, 201-214, 227-233, 247-274
src\gui\controllers\search_controller.py                               197     69    65%   61, 93-94, 101, 118, 135, 152, 164-165, 178-215, 228-264, 277-312, 327, 335-336
src\gui\controllers\service_controller.py                              211    142    33%   117, 135-162, 166-350, 362-365, 386-387, 406-407, 425-426, 432-439, 459-479
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       57      4    93%   101-105, 108
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   25-29, 32-115, 118-120
src\gui\dialogs\bug_report_dialog.py                                   231    231     0%   10-495
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  84     62    26%   27-80, 83-91, 94-102, 107-110, 114-117, 121-124, 128-131
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                                37      0   100%
src\gui\dialogs\startup_dialog.py                                      239    239     0%   6-396
src\gui\formatters.py                                                  129     92    29%   12-27, 37-68, 73, 95-98, 104, 120-122, 128, 132, 138, 147, 151-154, 158-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-335
src\gui\main_window\components\status_bar.py                           158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-43
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     21     21     0%   1-52
src\gui\main_window\main.py                                            280    280     0%   1-488
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 200    144    28%   52-56, 60-77, 89-93, 97-99, 126-134, 138-184, 191, 195-206, 210, 214, 218, 226, 235, 239-244, 248-251, 255-257, 261-272, 276-279, 283-299, 303-307, 311-320, 330-335, 339-352, 356, 360-375, 382-385, 391-396, 400-403
src\gui\panels\carico_ts.py                                             91     70    23%   29-37, 40-44, 49-93, 97-100, 104-108, 112-120, 124-125, 129-185
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 17-20
src\gui\panels\contabilita_kpi\charts.py                               197    180     9%   21-63, 70-78, 81-84, 88-92, 95-158, 161-217, 220-284, 287-328, 331-389
src\gui\panels\contabilita_kpi\kpi_panel.py                            149    130    13%   35-41, 44-162, 175-179, 182-194, 197-207, 210, 213-296
src\gui\panels\contabilita_panel.py                                    252    217    14%   38-45, 49-55, 59-163, 167-174, 178, 182, 206-222, 226-247, 252-276, 280-282, 286-289, 293-318, 324-344, 347-348, 351-355, 360-381, 384-386, 389-406, 410, 413-432
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-128, 132-134, 138-148, 152-167, 172-187, 192-210, 215-231, 236-245, 249-266, 270-300, 304-310
src\gui\panels\dettagli_oda.py                                         135    110    19%   27-35, 38-42, 46-92, 95-97, 101, 104-116, 119-131, 136-138, 142-148, 151-231, 235-241
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-64
src\gui\panels\dipendenti\pages\anagrafica_page.py                     370    332    10%   55-86, 89-219, 223-259, 263-278, 283-315, 318-362, 366-374, 378-395, 398-407, 411-442, 445-481, 484-527, 530-572, 575, 579-668, 671-676, 682-715
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\dipendenti\utils\data_helpers.py                         54     47    13%   7-9, 13-40, 46-58, 62-69
src\gui\panels\dipendenti\utils\report_generator.py                    142    118    17%   23-49, 56-99, 108-198, 203-216, 221-244, 249-282
src\gui\panels\dipendenti\widgets\employee_detail_view.py              102     90    12%   23-28, 31-140, 143-146, 154-166, 172-175
src\gui\panels\dipendenti_manager_panel.py                             158    138    13%   28-70, 73, 84-96, 99-124, 127-165, 168-200, 204-236, 240-256, 260-281, 286-298, 305-334
src\gui\panels\health_panel.py                                         292    261    11%   30-33, 37, 41-42, 45-52, 55-62, 65-100, 114-117, 120-162, 165-166, 173-174, 177-232, 235, 243, 255-269, 272-451, 455-502, 507-554, 560-590, 594-601, 605-612
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
src\gui\panels\pdl\pdl_detail_view.py                                   68     58    15%   17-20, 23-49, 54, 58-84, 88-103, 107-108
src\gui\panels\pdl\pdl_filter_widget.py                                 67     52    22%   26-31, 34-112, 115
src\gui\panels\pdl\pdl_panel.py                                        336    300    11%   44-98, 101-151, 155-209, 212-218, 222-253, 257-269, 273-305, 309-347, 351-353, 357-358, 362-369, 373-381, 385-407, 411-483, 487-493, 497-510, 514-538, 542-584
src\gui\panels\prenota_bp.py                                           105     86    18%   24-32, 35-38, 42-79, 83-85, 88-96, 99-105, 108-112, 116-189
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    303    102    66%   44-46, 51-85, 239-248, 255-283, 301, 308-309, 325-326, 330-332, 336-354, 376-377, 387-388, 393-394, 398-403, 411-412, 427-429, 444, 455-469, 496-499, 506
src\gui\panels\scarico_pdl.py                                          296    257    13%   40-57, 61-82, 86-119, 129-137, 140-144, 148-277, 280-288, 291-294, 297-310, 313-324, 328, 331-333, 337-345, 350-357, 360-396, 400-414, 418-440, 444-458, 462-471, 475-507, 511-513, 517, 521-535, 539-541
src\gui\panels\scarico_ts.py                                           122     99    19%   25-33, 36-40, 44-81, 85-87, 91, 95-108, 112-124, 128-130, 134-139, 153-155, 161-221
src\gui\panels\settings\main_panel.py                                  105     23    78%   103, 130-131, 145-147, 150-163, 166-184
src\gui\panels\settings\pages\diag_page.py                              32      0   100%
src\gui\panels\settings\pages\general_page.py                           43      0   100%
src\gui\panels\settings\pages\lists_page.py                            321    109    66%   222, 232, 244-253, 256-264, 271, 296-312, 315-324, 327-333, 338-347, 350-364, 367-376, 379-385, 403-410, 413-418, 422, 425, 428, 434, 437, 440, 443, 446, 449, 452, 455
src\gui\panels\settings\pages\paths_page.py                            107     19    82%   115, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     29    78%   158-160, 166-168, 181, 184-185, 192-194, 202-205, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55      1    98%   113
src\gui\panels\settings\tabs\telegram_tab.py                           136     27    80%   142-149, 154-167, 172-181, 187-191, 201, 223-224
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              39     33    15%   10-11, 15-75
src\gui\panels\storico_oda\oda_detail_view.py                           47     39    17%   17-20, 23-49, 53-69, 73-74
src\gui\panels\storico_oda\oda_filter_widget.py                         41     28    32%   23-28, 31-79, 82
src\gui\panels\storico_oda\oda_panel.py                                245    214    13%   43-106, 109-174, 178-188, 192-295, 298-310, 313, 316, 319-323, 326-332, 336-358, 364-418, 421-426, 431-453, 457-477
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     158    134    15%   38-48, 51-83, 86-117, 120-160, 164-180, 184-219, 223-241, 244-251, 255, 258-281, 285
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-132
src\gui\styles\widget_styles.py                                         35     35     0%   6-391
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-141
src\gui\widgets\audit\audit_filter_bar.py                               76     63    17%   22-26, 29-86, 89-91, 94-103, 114-115, 118-133
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   11-12, 15-33, 36-43, 46-47
src\gui\widgets\audit_log_widget.py                                    102     80    22%   40-52, 55-118, 121-122, 125-137, 140, 143-144, 147-165, 168-177, 180-182
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              141    129     9%   22-153, 157-165, 169-195, 207-361, 365-374, 378-406
src\gui\widgets\autopilot\event_card.py                                 70     63    10%   19-125, 129-146, 150-167
src\gui\widgets\autopilot\main_widget.py                               197    176    11%   44-52, 55, 58, 61-148, 151-170, 173-182, 185-213, 216-218, 221-228, 231-234, 237-297, 300-349
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-171, 174-187, 190-200, 203-208, 211-229, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    292    12%   29-36, 47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer\__init__.py                                       6      6     0%   1-7
src\gui\widgets\footer\business_info.py                                 88     88     0%   1-125
src\gui\widgets\footer\components.py                                    48     48     0%   1-87
src\gui\widgets\footer\manager.py                                       20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                                    35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                                     53     53     0%   1-67
src\gui\widgets\info_widgets.py                                         89     74    17%   26-59, 62, 69-77, 82-110, 117-169, 172, 175
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-127
src\gui\widgets\modern_button.py                                        61      4    93%   85-88
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41      7    83%   17, 46-51, 76
src\gui\widgets\sidebar_widget.py                                      244     50    80%   82-86, 100, 105-113, 154-156, 160-162, 166-169, 238, 394, 402, 406-407, 411-412, 420-456
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     24    76%   165-167, 194-227
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     34    73%   141-149, 152-156, 160-162, 166-167, 172-173, 179, 210-217, 225, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-299
src\utils\date_utils.py                                                 69     69     0%   6-238
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     55    43%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 250, 259
src\utils\log_humanizer.py                                              41     15    63%   12-26, 86, 112-113
src\utils\parsing.py                                                    53     13    75%   14, 17, 21, 32-33, 66, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79      8    90%   43-44, 81-83, 133-135
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     46    37%   35, 42-44, 52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                23626  16184    31%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_manager_extended.py::test_handle_run_pdl_on
1 failed in 20.51s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x00000227E0707560>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_telegram_manager_logic.py::TestTelegramManagerLogic::test_cmd_stop`
**Error:** `FAILED tests/unit/test_telegram_manager_logic.py::TestTelegramManagerLogic::test_cmd_stop`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
___________________ TestTelegramManagerLogic.test_cmd_stop ____________________
tests\unit\test_telegram_manager_logic.py:58: in test_cmd_stop
    await telegram_service._cmd_stop(mock_update, None)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'TelegramService' object has no attribute '_cmd_stop'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      21     21     0%   6-142
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                266    266     0%   6-501
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               86     86     0%   5-166
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit\__init__.py                                 3      3     0%   1-4
src\core\audit\database.py                                99     99     0%   1-175
src\core\audit\integrity.py                               15     15     0%   1-26
src\core\audit\manager.py                                140    140     0%   1-294
src\core\audit\models.py                                   9      9     0%   1-13
src\core\audit\signals.py                                 27     27     0%   1-40
src\core\audit_manager.py                                  5      5     0%   6-11
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                 160    160     0%   11-348
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     96     96     0%   6-134
src\core\contabilita_manager.py                          106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                           87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                            91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                             59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            139    112    19%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 250-307
src\core\database\__init__.py                              2      0   100%
src\core\database\manager.py                             119     77    35%   101-138, 144-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py               23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                       19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py               11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                     98     98     0%   1-202
src\core\excel_importer.py                                 4      0   100%
src\core\importers\__init__.py                            43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                            64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                        119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                        140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                        189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                        198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                         85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\logging\__init__.py                              10     10     0%   6-37
src\core\logging\alert_manager.py                        121    121     0%   7-252
src\core\logging\analytics.py                            141    141     0%   7-352
src\core\logging\config.py                                39     39     0%   5-89
src\core\logging\context.py                               53     53     0%   5-157
src\core\logging\decorators.py                            64     64     0%   5-186
src\core\logging\filters.py                               64     64     0%   5-215
src\core\logging\formatters.py                            84     84     0%   5-244
src\core\logging\logger.py                               111    111     0%   5-309
src\core\logging\metadata.py                              83     83     0%   5-200
src\core\logging\metrics.py                              109    109     0%   5-313
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              56     56     0%   5-204
src\core\logging\sinks.py                                103    103     0%   5-241
src\core\logging\viewer.py                               187    187     0%   5-451
src\core\lyra_client.py                                  128    128     0%   6-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     97     0%   6-204
src\core\oda_manager.py                                   33     33     0%   6-94
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                               96     60    38%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 104-109, 114-119, 124-128, 133-136, 141-147
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\sync_tracker.py                                  59     59     0%   1-108
src\core\telegram\__init__.py                              2      0   100%
src\core\telegram\handlers\callbacks.py                  187    102    45%   16, 19, 25, 27, 30-31, 36, 40, 52-54, 58-95, 103-129, 142-147, 154-155, 162-167, 170, 177, 184, 191, 198, 205-206, 209-210, 213-214, 249, 271, 293-306, 318-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                    47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                    98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                             175     92    47%   54-71, 75-84, 88, 92-104, 107, 117-155, 170-171, 175-185, 211, 217-218, 224-234, 237-250, 253-266, 272, 280-281, 287, 296-297, 303, 313-314
src\core\telegram\ui\keyboards.py                         98     44    55%   10, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                              342    342     0%   1-529
src\core\telegram_manager.py                               2      0   100%
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                    59     59     0%   1-120
src\gui\dialogs\bug_report_dialog.py                     231    231     0%   10-495
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-131
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                        239    239     0%   6-396
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-335
src\gui\main_window\components\status_bar.py             158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                25     25     0%   1-43
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-52
src\gui\main_window\main.py                              280    280     0%   1-488
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   200    200     0%   6-403
src\gui\panels\carico_ts.py                               91     91     0%   6-185
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 197    197     0%   1-389
src\gui\panels\contabilita_kpi\kpi_panel.py              149    149     0%   1-296
src\gui\panels\contabilita_panel.py                      252    252     0%   6-432
src\gui\panels\dashboard_panel.py                        168    168     0%   1-310
src\gui\panels\dettagli_oda.py                           135    135     0%   6-241
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py               158    158     0%   1-334
src\gui\panels\health_panel.py                           292    292     0%   8-612
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          32     32     0%   1-56
src\gui\panels\lyra\header.py                             36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        146    146     0%   1-220
src\gui\panels\lyra\workers.py                            37     37     0%   1-59
src\gui\panels\notifications_panel.py                    253    253     0%   6-458
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                     68     68     0%   1-108
src\gui\panels\pdl\pdl_filter_widget.py                   67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                          336    336     0%   6-584
src\gui\panels\prenota_bp.py                             105    105     0%   6-189
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      303    303     0%   7-524
src\gui\panels\scarico_pdl.py                            296    296     0%   6-541
src\gui\panels\scarico_ts.py                             122    122     0%   6-221
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py             47     47     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py           41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                  245    245     0%   6-477
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       158    158     0%   1-285
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-156
src\gui\styles\theme_manager.py                           70     70     0%   6-132
src\gui\styles\widget_styles.py                           35     35     0%   6-391
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-182
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                   70     70     0%   1-167
src\gui\widgets\autopilot\main_widget.py                 197    197     0%   6-349
src\gui\widgets\bot_parameters.py                        112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            109    109     0%   5-217
src\gui\widgets\excel_table.py                           330    330     0%   6-558
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   88     88     0%   1-125
src\gui\widgets\footer\components.py                      48     48     0%   1-87
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                       53     53     0%   1-67
src\gui\widgets\info_widgets.py                           89     89     0%   6-175
src\gui\widgets\message_bubble.py                         53     53     0%   7-127
src\gui\widgets\modern_button.py                          61     61     0%   5-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        244    244     0%   1-456
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       191    191     0%   6-334
src\gui\widgets\toast.py                                 128    128     0%   5-253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-299
src\utils\date_utils.py                                   69     69     0%   6-238
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                41     41     0%   6-121
src\utils\parsing.py                                      53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                     83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-142
src\utils\system_telemetry.py                             25     25     0%   6-70
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  17616  16788     5%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_manager_logic.py::TestTelegramManagerLogic::test_cmd_stop
1 failed in 15.77s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x00000216A3657560>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_telegram_manager_logic.py::TestTelegramManagerLogic::test_handle_text_input_ai_trigger`
**Error:** `Timeout`

<details><summary>Full Output</summary>

```text
Execution Timed Out
```
</details>

---
### `tests/unit/test_telegram_manager_logic.py::TestTelegramManagerLogic::test_handle_text_input_ai_trigger`
**Error:** `FAILED tests/unit/test_telegram_manager_logic.py::TestTelegramManagerLogic::test_handle_text_input_ai_trigger`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestTelegramManagerLogic.test_handle_text_input_ai_trigger __________
tests\unit\test_telegram_manager_logic.py:100: in test_handle_text_input_ai_trigger
    with patch(
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.core.telegram.handlers.messages' from 'C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\telegram\\handlers\\messages.py'> does not have the attribute 'NLUManager'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      21     21     0%   6-142
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                266    266     0%   6-501
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               86     86     0%   5-166
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit\__init__.py                                 3      3     0%   1-4
src\core\audit\database.py                                99     99     0%   1-175
src\core\audit\integrity.py                               15     15     0%   1-26
src\core\audit\manager.py                                140    140     0%   1-294
src\core\audit\models.py                                   9      9     0%   1-13
src\core\audit\signals.py                                 27     27     0%   1-40
src\core\audit_manager.py                                  5      5     0%   6-11
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                 160    160     0%   11-348
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     96     96     0%   6-134
src\core\contabilita_manager.py                          106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                           87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                            91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                             59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            139    112    19%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 250-307
src\core\database\__init__.py                              2      0   100%
src\core\database\manager.py                             119     77    35%   101-138, 144-176, 182-192, 197-200, 203, 209-230
src\core\database\migrations\contabilita.py               23     19    17%   6-67, 72-76, 81-121
src\core\database\migrations\dipendenti.py                17     13    24%   6-23, 28-30, 37-45
src\core\database\migrations\pdl.py                       19     16    16%   6-37, 42-90
src\core\database\migrations\storico_oda.py               11      8    27%   6-53, 62-64
src\core\database\migrations\timbrature.py                27     22    19%   6-25, 30-34, 41-51, 58-75
src\core\employees.py                                     98     98     0%   1-202
src\core\excel_importer.py                                 4      0   100%
src\core\importers\__init__.py                            43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                            64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                        119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                        140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                        189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                        198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                         85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 179-195
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\logging\__init__.py                              10     10     0%   6-37
src\core\logging\alert_manager.py                        121    121     0%   7-252
src\core\logging\analytics.py                            141    141     0%   7-352
src\core\logging\config.py                                39     39     0%   5-89
src\core\logging\context.py                               53     53     0%   5-157
src\core\logging\decorators.py                            64     64     0%   5-186
src\core\logging\filters.py                               64     64     0%   5-215
src\core\logging\formatters.py                            84     84     0%   5-244
src\core\logging\logger.py                               111    111     0%   5-309
src\core\logging\metadata.py                              83     83     0%   5-200
src\core\logging\metrics.py                              109    109     0%   5-313
src\core\logging\migration.py                             42     42     0%   5-120
src\core\logging\sampling.py                              56     56     0%   5-204
src\core\logging\sinks.py                                103    103     0%   5-241
src\core\logging\viewer.py                               187    187     0%   5-451
src\core\lyra_client.py                                  128    128     0%   6-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     97     0%   6-204
src\core\oda_manager.py                                   33     33     0%   6-94
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                               96     60    38%   31-53, 57-61, 65-75, 79-81, 85-89, 94, 99, 104-109, 114-119, 124-128, 133-136, 141-147
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\sync_tracker.py                                  59     59     0%   1-108
src\core\telegram\__init__.py                              2      0   100%
src\core\telegram\handlers\callbacks.py                  187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                    47     35    26%   13-35, 53-78, 86-89, 98
src\core\telegram\handlers\messages.py                    98     66    33%   25, 33-34, 47-54, 61, 74, 78-87, 100-109, 117-127, 135-170
src\core\telegram\service.py                             175    121    31%   54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 211, 217-218, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                         98     51    48%   28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                              342    342     0%   1-529
src\core\telegram_manager.py                               2      0   100%
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         57     57     0%   1-108
src\gui\dialogs\audit_detail_dialog.py                    59     59     0%   1-120
src\gui\dialogs\bug_report_dialog.py                     231    231     0%   10-495
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    84     84     0%   1-131
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\dialogs\standard_input_dialog.py                  37     37     0%   1-79
src\gui\dialogs\startup_dialog.py                        239    239     0%   6-396
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-335
src\gui\main_window\components\status_bar.py             158    158     0%   1-282
src\gui\main_window\components\tool_bar.py                25     25     0%   1-43
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       21     21     0%   1-52
src\gui\main_window\main.py                              280    280     0%   1-488
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   200    200     0%   6-403
src\gui\panels\carico_ts.py                               91     91     0%   6-185
src\gui\panels\contabilita_kpi\__init__.py                 2      2     0%   1-3
src\gui\panels\contabilita_kpi\cards_row.py               14     14     0%   1-20
src\gui\panels\contabilita_kpi\charts.py                 197    197     0%   1-389
src\gui\panels\contabilita_kpi\kpi_panel.py              149    149     0%   1-296
src\gui\panels\contabilita_panel.py                      252    252     0%   6-432
src\gui\panels\dashboard_panel.py                        168    168     0%   1-310
src\gui\panels\dettagli_oda.py                           135    135     0%   6-241
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-64
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\dipendenti_manager_panel.py               158    158     0%   1-334
src\gui\panels\health_panel.py                           292    292     0%   8-612
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra\__init__.py                            2      2     0%   1-3
src\gui\panels\lyra\chat_area.py                          32     32     0%   1-56
src\gui\panels\lyra\header.py                             36     36     0%   1-88
src\gui\panels\lyra\input_bar.py                          41     41     0%   1-88
src\gui\panels\lyra\lyra_panel.py                        146    146     0%   1-220
src\gui\panels\lyra\workers.py                            37     37     0%   1-59
src\gui\panels\notifications_panel.py                    253    253     0%   6-458
src\gui\panels\pdl\__init__.py                             2      2     0%   1-3
src\gui\panels\pdl\pdl_delegate.py                        13     13     0%   1-23
src\gui\panels\pdl\pdl_detail_view.py                     68     68     0%   1-108
src\gui\panels\pdl\pdl_filter_widget.py                   67     67     0%   1-115
src\gui\panels\pdl\pdl_panel.py                          336    336     0%   6-584
src\gui\panels\prenota_bp.py                             105    105     0%   6-189
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      303    303     0%   7-524
src\gui\panels\scarico_pdl.py                            296    296     0%   6-541
src\gui\panels\scarico_ts.py                             122    122     0%   6-221
src\gui\panels\storico_oda\__init__.py                     2      2     0%   1-3
src\gui\panels\storico_oda\oda_delegate.py                39     39     0%   1-75
src\gui\panels\storico_oda\oda_detail_view.py             47     47     0%   1-74
src\gui\panels\storico_oda\oda_filter_widget.py           41     41     0%   1-82
src\gui\panels\storico_oda\oda_panel.py                  245    245     0%   6-477
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       158    158     0%   1-285
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-156
src\gui\styles\theme_manager.py                           70     70     0%   6-132
src\gui\styles\widget_styles.py                           35     35     0%   6-391
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-141
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-182
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot\__init__.py                      4      4     0%   1-5
src\gui\widgets\autopilot\config_cards.py                141    141     0%   1-406
src\gui\widgets\autopilot\event_card.py                   70     70     0%   1-167
src\gui\widgets\autopilot\main_widget.py                 197    197     0%   6-349
src\gui\widgets\bot_parameters.py                        112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            109    109     0%   5-217
src\gui\widgets\excel_table.py                           330    330     0%   6-558
src\gui\widgets\footer\__init__.py                         6      6     0%   1-7
src\gui\widgets\footer\business_info.py                   88     88     0%   1-125
src\gui\widgets\footer\components.py                      48     48     0%   1-87
src\gui\widgets\footer\manager.py                         20     20     0%   1-35
src\gui\widgets\footer\status_bar.py                      35     35     0%   1-48
src\gui\widgets\footer\telemetry.py                       53     53     0%   1-67
src\gui\widgets\info_widgets.py                           89     89     0%   6-175
src\gui\widgets\message_bubble.py                         53     53     0%   7-127
src\gui\widgets\modern_button.py                          61     61     0%   5-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        244    244     0%   1-456
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       191    191     0%   6-334
src\gui\widgets\toast.py                                 128    128     0%   5-253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-299
src\utils\date_utils.py                                   69     69     0%   6-238
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                41     41     0%   6-121
src\utils\parsing.py                                      53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                     83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-142
src\utils\system_telemetry.py                             25     25     0%   6-70
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  17616  16865     4%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_manager_logic.py::TestTelegramManagerLogic::test_handle_text_input_ai_trigger
1 failed in 16.27s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x000002590E207560>
Traceback (most recent call last):
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\gianc\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
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
### `tests/unit/test_telegram_service.py::test_check_auth_success`
**Error:** `Timeout`

<details><summary>Full Output</summary>

```text
Execution Timed Out
```
</details>

---
### `tests/unit/test_telegram_service_advanced.py::TestTelegramServiceAdvanced::test_start_stop_service_logic`
**Error:** `Timeout`

<details><summary>Full Output</summary>

```text
Execution Timed Out
```
</details>

---
