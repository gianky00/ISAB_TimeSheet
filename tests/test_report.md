# 📊 Test Execution Report

**Date:** 2026-03-20 15:49:38
**Duration:** 3973.60s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1306 |
| ✅ Passed | 913 |
| ❌ Failed | 1 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_safework_pdl_bot_comprehensive.py::TestSafeWorkPDLBotComprehensive::test_validate_data_scenarios`
**Error:** `FAILED tests/unit/test_safework_pdl_bot_comprehensive.py::TestSafeWorkPDLBotComprehensive::test_validate_data_scenarios`

**Timestamp:** `2026-03-20T15:49:38.147990`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_safework_pdl_bot_comprehensive.py F                      [100%]

================================== FAILURES ===================================
________ TestSafeWorkPDLBotComprehensive.test_validate_data_scenarios _________
tests\unit\test_safework_pdl_bot_comprehensive.py:52: in test_validate_data_scenarios
    assert ok is True
E   assert False is True
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              338     50    85%   142-145, 158, 163, 267, 358-368, 402, 420, 432-433, 450-456, 460-462, 481, 485, 500, 508, 537, 541-545, 549-554, 565-567, 573-576
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                           99     84    15%   50-55, 74-78, 109-172, 195-252
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     11    82%   34, 64, 78, 82, 112, 118-119, 124-125, 136-137
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     21    80%   30, 35, 51, 76, 79, 92, 111, 120-123, 134, 153-155, 160-162, 174, 193-194
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207    133    36%   51-71, 86-88, 101-103, 113-118, 139-213, 217-228, 238-267, 271-280, 287, 292, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    180    31%   40, 45, 57, 61, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         157     95    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-232, 241-252, 257-292
src\bots\portale_fornitori\timbrature\storage.py                       187    142    24%   51, 55-81, 84-86, 88, 95-113, 128-145, 157, 176-184, 187, 197-204, 207-232, 235, 247-278, 288-301, 303, 308, 312-341, 349, 352-367, 385-387, 389, 393-406, 415-416
src\bots\safework\base.py                                               82     54    34%   41-45, 49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     55    19%   22-24, 30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     32    30%   25-27, 31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     45    29%   24-26, 30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    109    65%   55, 71, 75, 80-81, 86, 106, 132-137, 142, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     69    38%   61, 66, 71, 83-145, 149-156, 179, 185, 190-206, 210-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            149      6    96%   45, 57, 70-71, 106-107
src\core\app_updater.py                                                  9      5    44%   29-35
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             21      0   100%
src\core\audit\manager.py                                              168     29    83%   63, 67-69, 78, 90-91, 231, 233, 240-244, 246, 314, 336-354
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 34, 71-91
src\core\config\defaults.py                                              3      0   100%
src\core\config\migration.py                                            69     47    32%   23-30, 35-86, 97
src\core\config\security.py                                             44      4    91%   28, 33, 65, 68
src\core\config_manager.py                                             164     23    86%   74, 109, 195-199, 235, 240-251, 257-259, 267, 272, 289-290
src\core\constants.py                                                  125      0   100%
src\core\contabilita\certificati_engine.py                              97     24    75%   34-35, 45, 59-60, 69, 72, 85, 95, 103, 110, 114-117, 124-128, 136-142
src\core\contabilita\scarico_ore\controller.py                          53     34    36%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        115     24    79%   106, 114, 127-128, 137-144, 155, 171, 189, 194, 199, 204-213, 218
src\core\contabilita_queries.py                                         82      4    95%   52, 81, 96, 113
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
src\core\employees.py                                                   98     13    87%   61-63, 118-120, 129-130, 174-175, 190-192
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          44      0   100%
src\core\importers\attivita.py                                          67      5    93%   58-59, 77, 92-93
src\core\importers\base.py                                              60      7    88%   15-16, 24-26, 57-58
src\core\importers\certificati.py                                      126     14    89%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            192     52    73%   70-72, 88, 113, 134-135, 147, 151, 155-156, 161-163, 168-173, 187, 200-211, 214-215, 259-270, 286-291, 296-298, 300, 311, 313, 326-328
src\core\license_validator.py                                          176     40    77%   66-69, 86-115, 125-129, 148, 195, 197, 203-204, 213-215, 235-236, 258-259, 285-286, 289-290, 295-296, 301-302
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     27    64%   64, 66, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             74     30    59%   77-111, 163, 175-182, 201, 213
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     13    76%   58, 67, 100, 105, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             177    143    19%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-138, 142-143, 147-148, 152-153, 162-176, 185-193, 216-222, 226-230, 234-248, 252-267, 271-273, 277-313, 317-333, 352, 357, 362
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-108
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                            105     23    78%   32, 99, 104, 109, 115-116, 122, 130-135, 141, 149, 168-169, 176-179, 186-188
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               70     12    83%   51-53, 55-57, 68, 74-76, 95, 97, 113
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             31      1    97%   62
src\core\sync_tracker.py                                                77     38    51%   45-50, 56-60, 73-86, 91-102, 107-119, 149-161
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  56     47    16%   14-37, 42-49, 54-72, 79-80, 88-98
src\core\telegram\service.py                                           205    154    25%   57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             34      6    82%   60-74, 78-84
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\updater\__init__.py                                             0      0   100%
src\core\updater\engine.py                                             166    129    22%   46-50, 54, 58-69, 73-102, 106-178, 183-191, 197-206, 214, 225-234, 239-257
src\core\updater\gui.py                                                163     87    47%   40-54, 58-75, 79-80, 85-100, 105, 110-111, 116-117, 122-153, 206-210, 217-218, 221, 240-241, 254-273
src\core\version.py                                                      5      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     47    73%   133-134, 143-145, 153-154, 173-174, 199-219, 328-331, 348-364, 392-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     41    72%   99-106, 117-134, 158-164, 168-175, 204, 218-219, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                107     90    16%   28-34, 38-86, 91-107, 110-122, 125-133, 136-141, 144-149, 159-165
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     68    63%   74, 106-109, 141-144, 148-152, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 246, 256, 264, 268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168    136    19%   71-97, 108-121, 132-153, 157, 166-168, 178-192, 196-199, 203-210, 214-216, 220-222, 226-228, 232-258, 262-279, 285-287, 291-316
src\gui\controllers\bot_controller.py                                   51     23    55%   79-88, 93-98, 107-119
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           270    149    45%   60, 67, 71, 84, 104, 133-135, 147-151, 155-159, 163-167, 171-175, 179-183, 187-191, 195-199, 203-207, 211-215, 219-225, 240-283, 287-314, 332-333, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-533
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              165    139    16%   45-54, 58-65, 72-111, 115-131, 135-242, 248-250, 254-258, 262-278, 282-291, 295, 299-304
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         225     45    80%   166, 175, 181, 186-189, 362, 389, 401-498
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  96     72    25%   54-118, 122-130, 134-142, 146-158, 174-177, 182-185, 190-193, 198-201
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\splash_standalone.py                                    81     81     0%   8-133
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      262    262     0%   6-412
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              75     43    43%   43-49, 67-78, 82-91, 102-323
src\gui\main_window\components\status_bar.py                           132     71    46%   102-114, 118-130, 137-181, 209-222, 226-227
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    37     21    43%   32-33, 48-56, 60-72, 75-76, 80, 84-90
src\gui\main_window\controllers\monitoring_controller.py                36     25    31%   26-28, 32-34, 38-65
src\gui\main_window\controllers\signal_connector.py                     28      5    82%   54-57, 80
src\gui\main_window\controllers\workflow_controller.py                  83     69    17%   23-24, 28-53, 57-62, 69-74, 81-86, 93-98, 105-108, 112-117, 121-126, 130-155
src\gui\main_window\main.py                                            259    146    44%   116-131, 135-156, 161-174, 184-186, 220, 225, 228, 235, 237, 251-264, 266-270, 274, 277-279, 281, 287-291, 293, 298-310, 314-322, 330, 332, 341-344, 346-412, 414-422, 425-428, 430-441, 450, 453-455, 458-460, 464, 470, 473-498
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     24    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 211, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 281     32    89%   85-86, 91-93, 97, 130-134, 138-140, 199, 205-206, 210-211, 316, 325, 347, 356-357, 385-386, 455-456, 491-494, 502, 536
src\gui\panels\carico_ts.py                                             89     30    66%   59-61, 99, 107-109, 118-123, 132, 141-176
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   28-35, 42-84, 91-99, 102-105, 109-113, 116-187, 190-244, 247-309, 312-351, 354-400
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     41    75%   209-214, 238-309
src\gui\panels\contabilita_panel.py                                    266    104    61%   73-77, 226-230, 234, 253, 263-266, 284, 292-293, 296-299, 303-305, 311-313, 320, 329-333, 335-338, 342-384, 388-392, 396-413, 417-433
src\gui\panels\dashboard_panel.py                                      128     56    56%   86, 90-104, 157-172, 176-205, 208-247
src\gui\panels\dettagli_oda.py                                         181     92    49%   68-72, 158-169, 173-175, 179, 183-194, 198-221, 226, 241-243, 255-257, 261-328, 332-340
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      94     69    27%   35-55, 58-85, 89-101, 104-110, 113-117, 120-122, 125-147, 150-154, 159, 163
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     34    78%   30-36, 49-52, 79, 93-94, 121-122, 124-125, 141, 191-192, 204, 216-240, 268, 283-284, 302-304
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           137      6    96%   204, 220-224
src\gui\panels\notifications_panel.py                                  243     44    82%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 339-346, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    154    19%   48-93, 97-145, 150-164, 173-186, 199-209, 213-214, 219-235, 239-254, 258-260, 264-274, 278-296, 300, 304-307, 315-325
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           142     79    44%   65-68, 132-134, 145-156, 160-162, 166-175, 179-184, 188-190, 199-272
src\gui\panels\ricerca_pdl.py                                          109     45    59%   56-58, 127-130, 134-135, 139-194, 198-204, 212-214
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73     58    21%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        91     72    21%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          229     61    73%   78-79, 201-203, 207-227, 252-255, 280-284, 306-310, 314-317, 387, 396, 402-403, 414-428, 435-450
src\gui\panels\scarico_ts.py                                           137     21    85%   65-67, 134, 141-143, 160, 167, 175-177, 208-216, 266
src\gui\panels\settings\main_panel.py                                  132     63    52%   34, 40, 42, 68-70, 77-79, 85, 94, 110, 124, 126-128, 138, 140, 143, 151, 153, 155-159, 163-165, 171-173, 176-182, 186-189, 193, 197, 201-210, 214-226, 230-239
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                           46      0   100%
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-165, 190, 207-208, 211, 214-216, 219-221, 224-226, 229-231, 234-236, 239-241, 244-246, 249-251
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     29    65%   89-100, 104-107, 111-116, 120-124, 130-132
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    128    17%   47-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-292
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     221     30    86%   88-90, 227, 236, 316-334, 337-344, 359, 374-375, 380
src\gui\panels\timbrature_bot.py                                       106     67    37%   57-59, 63-67, 89-91, 95-96, 100-108, 112-117, 126-131, 135-196, 200-202
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     38    72%   48-49, 51-52, 90-92, 94-96, 152-153, 173-183, 190, 194-196, 270, 276, 282-290, 298-314
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      2    95%   60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                144     44    69%   164, 193, 197-212, 232-233, 239-241, 258-293
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     50    77%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 332-350, 362, 372, 382-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            209    178    15%   70-79, 83-154, 158, 162-177, 181-194, 198-209, 213-219, 223-228, 232-250, 254-257, 261-267, 271-274, 278-281, 285-288, 292-295, 299-303, 312-323
src\gui\widgets\contabilita\certificati\tree_widget.py                  98     31    68%   36-42, 46-50, 54-56, 64-65, 69-71, 75-77, 174-199
src\gui\widgets\contabilita\certificati_tab.py                         291    152    48%   55, 60-63, 66, 69, 72, 77, 96-97, 105, 107, 124, 128, 132, 146, 148-149, 152-156, 160, 165-169, 171, 176, 181, 184, 191-195, 211-214, 234, 236-240, 243-247, 251, 268, 288, 292, 297-302, 307-309, 313-323, 327-330, 334, 336-337, 346-360, 364-374, 376, 378-383, 385, 388-389, 395, 397-404, 407-412, 416-421, 425-428, 430, 434-438, 442-447, 451-475, 480-508
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         186     55    70%   95, 100, 134, 151, 179, 195-214, 217-237, 240-256
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462     96    79%   124, 128-129, 134, 138-139, 193, 205, 216, 223, 226, 228, 230-240, 245-252, 256-257, 261-263, 267-268, 272-278, 304-307, 329, 342, 356-363, 395-396, 459-468, 513-530, 544, 560, 586-591, 598, 604
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   359-376, 379-405, 409-423, 426-429, 436-486, 490-500, 503-530, 533-605, 608-618, 621
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43      8    81%   46-47, 53-54, 58-60, 71
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         232     65    72%   82-89, 108-109, 202, 216-223, 227-244, 289-291, 336-355, 376-399, 403-405
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54     54     0%   7-140
src\gui\widgets\mixins\clipboard_mixin.py                               87     15    83%   19, 26, 31, 36, 50, 61, 67, 78-82, 100-102
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     23    80%   145-156, 162-166, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   261-302, 308-312
src\gui\widgets\safework\status_list.py                                 60     18    70%   73-93
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     23    23%   16-36, 43-53
src\gui\widgets\sidebar\animations.py                                   34     16    53%   34-36, 40-43, 47-57
src\gui\widgets\sidebar\components.py                                  127     20    84%   31-33, 68-69, 100, 161-168, 172-174, 205, 215, 220, 236
src\gui\widgets\sidebar_button.py                                       57      3    95%   53, 58, 63
src\gui\widgets\sidebar_widget.py                                      267     80    70%   80-81, 269-272, 276-298, 317-319, 321-323, 325-327, 329-330, 336-337, 341-345, 349-401
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      6    90%   99-101, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     118     39    67%   67-97, 162-164, 174-191
src\gui\widgets\toast.py                                               157     51    68%   128-130, 150-159, 178-185, 189-194, 198-200, 204-205, 211-212, 218, 263-264, 271-278, 286, 300-303, 308-311, 316-319, 324-327
src\gui\widgets\update_banner.py                                        85     35    59%   106-126, 131-154, 157-161
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         66     15    77%   13-14, 24, 37, 41-42, 59-60, 73-74, 84-89
src\utils\helpers.py                                                   128     41    68%   34, 67-68, 113, 126-141, 182-195, 214, 221-223, 230-235, 252
src\utils\log_humanizer.py                                              43      8    81%   21-28
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   88     11    88%   14-15, 55-57, 121-124, 148-149
src\utils\resource_manager.py                                           86     18    79%   22-33, 63, 73, 102, 114, 117-119, 124-126, 161
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   78      9    88%   43-44, 80-82, 109-111, 136
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30850  13598    56%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_safework_pdl_bot_comprehensive.py::TestSafeWorkPDLBotComprehensive::test_validate_data_scenarios
============================= 1 failed in 18.62s ==============================

```
</details>

---
