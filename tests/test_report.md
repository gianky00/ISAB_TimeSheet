# 📊 Test Execution Report

**Date:** 2026-03-06 21:55:19
**Duration:** 226.65s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1459 |
| ✅ Passed | 1480 |
| ❌ Failed | 14 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_sidebar_widget.py::TestSidebarWidget::test_sidebar_monitoraggio_group_exists`
**Error:** `FAILED tests/unit/test_sidebar_widget.py::TestSidebarWidget::test_sidebar_monitoraggio_group_exists`

**Timestamp:** `2026-03-06T21:09:09.547760`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_sidebar_widget.py F                                      [100%]

================================== FAILURES ===================================
__________ TestSidebarWidget.test_sidebar_monitoraggio_group_exists ___________
tests\unit\test_sidebar_widget.py:46: in test_sidebar_monitoraggio_group_exists
    assert "Notifiche" in texts
E   AssertionError: assert 'Notifiche' in ['', '', '']
============================== warnings summary ===============================
.venv\Lib\site-packages\_hypothesis_pytestplugin.py:469
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_hypothesis_pytestplugin.py:469: UserWarning: Skipping collection of '.hypothesis' directory - this usually means you've explicitly set the `norecursedirs` pytest config option, replacing rather than extending the default ignores.
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    128    31%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     20    74%   32-33, 49-50, 59, 72, 75-76, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     14    86%   103, 111, 124-125, 134-141, 152, 168, 186, 191, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     24    85%   35, 76-78, 88-90, 102, 126-127, 134, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      8    84%   51-53, 55-57, 74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59     24    59%   45-50, 56-60, 73-82, 112-124
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    154    25%   57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     33    52%   66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     41    72%   99-106, 117-134, 158-164, 168-175, 204, 218-219, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    188    10%   9-13, 33-75, 82-90, 93-96, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223    188    16%   74-83, 87-160, 164, 168-182, 186-199, 203-214, 218-224, 228-233, 237-255, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      6    89%   97, 104-117
src\gui\widgets\contabilita\certificati_tab.py                         211     87    59%   110, 114, 118-119, 126, 158-159, 199-202, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     32    88%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403, 413-414, 420-423, 440
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  12431    59%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_sidebar_widget.py::TestSidebarWidget::test_sidebar_monitoraggio_group_exists
======================== 1 failed, 1 warning in 12.80s ========================

```
</details>

---
### `tests/unit/test_simple_coverage_boost.py::TestLogHumanizer::test_humanize_categories`
**Error:** `FAILED tests/unit/test_simple_coverage_boost.py::TestLogHumanizer::test_humanize_categories`

**Timestamp:** `2026-03-06T21:11:19.041609`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_simple_coverage_boost.py F                               [100%]

================================== FAILURES ===================================
__________________ TestLogHumanizer.test_humanize_categories __________________
tests\unit\test_simple_coverage_boost.py:28: in test_humanize_categories
    assert c == "start"
E   AssertionError: assert 'info' == 'start'
E     
E     - start
E     + info
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    128    31%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     20    74%   32-33, 49-50, 59, 72, 75-76, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     14    86%   103, 111, 124-125, 134-141, 152, 168, 186, 191, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     24    85%   35, 76-78, 88-90, 102, 126-127, 134, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      8    84%   51-53, 55-57, 74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59     24    59%   45-50, 56-60, 73-82, 112-124
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    154    25%   57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     33    52%   66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     41    72%   99-106, 117-134, 158-164, 168-175, 204, 218-219, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    188    10%   9-13, 33-75, 82-90, 93-96, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223    188    16%   74-83, 87-160, 164, 168-182, 186-199, 203-214, 218-224, 228-233, 237-255, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      6    89%   97, 104-117
src\gui\widgets\contabilita\certificati_tab.py                         211     87    59%   110, 114, 118-119, 126, 158-159, 199-202, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  12424    59%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_simple_coverage_boost.py::TestLogHumanizer::test_humanize_categories
============================= 1 failed in 10.50s ==============================

```
</details>

---
### `tests/unit/test_simple_coverage_boost.py::TestDesignSystem::test_colors`
**Error:** `E   ImportError: cannot import name 'SPACING' from 'src.gui.styles' (C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\styles\__init__.py)`

**Timestamp:** `2026-03-06T21:12:03.835584`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 0 items / 1 error

=================================== ERRORS ====================================
__________ ERROR collecting tests/unit/test_simple_coverage_boost.py __________
ImportError while importing test module 'C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_simple_coverage_boost.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Program Files\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\unit\test_simple_coverage_boost.py:2: in <module>
    from src.gui.styles import COLORS, SPACING
E   ImportError: cannot import name 'SPACING' from 'src.gui.styles' (C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\styles\__init__.py)
=========================== short test summary info ===========================
ERROR tests/unit/test_simple_coverage_boost.py
============================== 1 error in 0.60s ===============================
ERROR: found no collectors for C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_simple_coverage_boost.py::TestDesignSystem::test_colors


```
</details>

---
### `tests/unit/test_sprint_b_intelligence.py::TestSprintBIntelligence::test_lyra_system_context_assembly`
**Error:** `FAILED tests/unit/test_sprint_b_intelligence.py::TestSprintBIntelligence::test_lyra_system_context_assembly`

**Timestamp:** `2026-03-06T21:14:20.405974`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_sprint_b_intelligence.py F                               [100%]

================================== FAILURES ===================================
__________ TestSprintBIntelligence.test_lyra_system_context_assembly __________
tests\unit\test_sprint_b_intelligence.py:123: in test_lyra_system_context_assembly
    assert "€ 2,000.00" in context
E   AssertionError: assert '€ 2,000.00' in '=== REPORT CONTABILITÀ (2024) ===\n- Valore Totale Preventivato: € 5,000.00\n- Ore Spese Totali: 100.0 h\n- Margine O...ento:\n  • IN CORSO: 5\n- Top 5 Commesse (per Valore):\n  • Test: € 1,000\n\n=== TIMBRATURE ===\nDatabase non trovato.'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    128    31%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     20    74%   32-33, 49-50, 59, 72, 75-76, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     14    86%   103, 111, 124-125, 134-141, 152, 168, 186, 191, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     23    86%   35, 76-78, 88-90, 102, 126-127, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      8    84%   51-53, 55-57, 74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59     24    59%   45-50, 56-60, 73-82, 112-124
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    154    25%   57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     33    52%   66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     41    72%   99-106, 117-134, 158-164, 168-175, 204, 218-219, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    188    10%   9-13, 33-75, 82-90, 93-96, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223    188    16%   74-83, 87-160, 164, 168-182, 186-199, 203-214, 218-224, 228-233, 237-255, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      6    89%   97, 104-117
src\gui\widgets\contabilita\certificati_tab.py                         211     87    59%   110, 114, 118-119, 126, 158-159, 199-202, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  12423    59%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_sprint_b_intelligence.py::TestSprintBIntelligence::test_lyra_system_context_assembly
============================= 1 failed in 13.53s ==============================

```
</details>

---
### `tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization`
**Error:** `Unknown Error`

**Timestamp:** `2026-03-06T21:16:32.753886`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_sprint_c_gui_deep.py E                                   [100%]

=================================== ERRORS ====================================
__ ERROR at setup of TestSprintCGUIDeep.test_contabilita_tab_synchronization __
tests\unit\test_sprint_c_gui_deep.py:39: in panel
    p = ContabilitaPanel()
        ^^^^^^^^^^^^^^^^^^
src\gui\panels\contabilita_panel.py:65: in __init__
    self._setup_ui()
src\gui\panels\contabilita_panel.py:214: in _setup_ui
    self.kpi_panel = ContabilitaKPIPanel()
                     ^^^^^^^^^^^^^^^^^^^^^
src\gui\panels\contabilita_kpi\kpi_panel.py:63: in __init__
    self._setup_ui()
src\gui\panels\contabilita_kpi\kpi_panel.py:143: in _setup_ui
    self.container1 = ChartContainer(
src\gui\panels\contabilita_kpi\charts.py:75: in __init__
    layout.addWidget(self.canvas)
E   TypeError: addWidget(self, a0: typing.Optional[QWidget], stretch: int = 0, alignment: Qt.AlignmentFlag = Qt.Alignment()): argument 1 has unexpected type 'MagicMock'
============================== warnings summary ===============================
tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\contabilita_panel.py:60: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\modern_card.py:23: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:91: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\modern_button.py:43: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(text, parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\components\animated_tab_widget.py:36: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\components\animated_stack.py:32: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\contabilita\attivita_tab.py:74: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:205: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(text, parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:165: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\excel_table.py:47: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(*args, **kwargs)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\contabilita\certificati_tab.py:47: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:327: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\contabilita_kpi\kpi_panel.py:40: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\contabilita_kpi\cards_row.py:10: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\info_widgets.py:127: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\info_widgets.py:76: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__("", parent)

tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\contabilita_kpi\charts.py:33: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    128    31%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     18    76%   32-33, 49-50, 59, 72, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     23    86%   35, 76-78, 88-90, 102, 126-127, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      8    84%   51-53, 55-57, 74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59     24    59%   45-50, 56-60, 73-82, 112-124
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    154    25%   57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     33    52%   66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     39    73%   99-106, 117-134, 158-164, 168-175, 204, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    152    28%   9-13, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223     61    73%   136, 158, 164, 188, 220, 230-233, 254, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      2    96%   105, 111
src\gui\widgets\contabilita\certificati_tab.py                         211     83    61%   110, 114, 118-119, 126, 158-159, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  12247    60%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_contabilita_tab_synchronization
======================= 19 warnings, 1 error in 20.06s ========================

```
</details>

---
### `tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_command_run_ts`
**Error:** `FAILED tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_command_run_ts`

**Timestamp:** `2026-03-06T21:21:18.470423`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_telegram_bridge.py F                                     [100%]

================================== FAILURES ===================================
_______________ TestTelegramUIBridge.test_handle_command_run_ts _______________
tests\unit\test_telegram_bridge.py:36: in test_handle_command_run_ts
    bridge._handle_command("run_ts", {})
    ^^^^^^^^^^^^^^^^^^^^^^
E   RuntimeError: super-class __init__() of type TelegramUIBridge was never called
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    128    31%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     18    76%   32-33, 49-50, 59, 72, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     23    86%   35, 76-78, 88-90, 102, 126-127, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      3    94%   74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59      0   100%
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    154    25%   57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     33    52%   66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     39    73%   99-106, 117-134, 158-164, 168-175, 204, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    152    28%   9-13, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223     61    73%   136, 158, 164, 188, 220, 230-233, 254, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      2    96%   105, 111
src\gui\widgets\contabilita\certificati_tab.py                         211     83    61%   110, 114, 118-119, 126, 158-159, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26      4    85%   59-64, 72-73
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  12196    60%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_command_run_ts
============================= 1 failed in 18.60s ==============================

```
</details>

---
### `tests/unit/test_telegram_bridge_robust.py::TestTelegramUIBridgeRobust::test_handle_intent_add_pdl`
**Error:** `Unknown Error`

**Timestamp:** `2026-03-06T21:23:32.690355`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_telegram_bridge_robust.py E                              [100%]

=================================== ERRORS ====================================
___ ERROR at setup of TestTelegramUIBridgeRobust.test_handle_intent_add_pdl ___
tests\unit\test_telegram_bridge_robust.py:25: in bridge
    return TelegramUIBridge(mock_mw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
src\core\telegram_bridge.py:39: in __init__
    self.ui_commands = TelegramUICommands(self.mw, self.telegram)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\core\telegram\bridge\ui_commands.py:21: in __init__
    super().__init__(main_window)
E   TypeError: QObject(parent: typing.Optional[QObject] = None): argument 1 has unexpected type 'MagicMock'
============================== warnings summary ===============================
tests/unit/test_telegram_bridge_robust.py::TestTelegramUIBridgeRobust::test_handle_intent_add_pdl
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\core\telegram_bridge.py:34: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    128    31%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     18    76%   32-33, 49-50, 59, 72, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     23    86%   35, 76-78, 88-90, 102, 126-127, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      3    94%   74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59      0   100%
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    154    25%   57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     18    74%   103-104, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     39    73%   99-106, 117-134, 158-164, 168-175, 204, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    152    28%   9-13, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223     61    73%   136, 158, 164, 188, 220, 230-233, 254, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      2    96%   105, 111
src\gui\widgets\contabilita\certificati_tab.py                         211     83    61%   110, 114, 118-119, 126, 158-159, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26      4    85%   59-64, 72-73
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  12181    60%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_telegram_bridge_robust.py::TestTelegramUIBridgeRobust::test_handle_intent_add_pdl
======================== 1 warning, 1 error in 18.58s =========================

```
</details>

---
### `tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_intent_processing_pdl`
**Error:** `Unknown Error`

**Timestamp:** `2026-03-06T21:26:44.860472`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_telegram_coverage.py E                                   [100%]

=================================== ERRORS ====================================
_______ ERROR at setup of TestTelegramBridge.test_intent_processing_pdl _______
tests\unit\test_telegram_coverage.py:66: in bridge
    return TelegramUIBridge(mw)
           ^^^^^^^^^^^^^^^^^^^^
src\core\telegram_bridge.py:39: in __init__
    self.ui_commands = TelegramUICommands(self.mw, self.telegram)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\core\telegram\bridge\ui_commands.py:21: in __init__
    super().__init__(main_window)
E   TypeError: QObject(parent: typing.Optional[QObject] = None): argument 1 has unexpected type 'MagicMock'
============================== warnings summary ===============================
tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_intent_processing_pdl
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\core\telegram_bridge.py:34: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    128    31%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     18    76%   32-33, 49-50, 59, 72, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     23    86%   35, 76-78, 88-90, 102, 126-127, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      3    94%   74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59      0   100%
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    146    22%   16, 19, 26-31, 36, 43, 50-51, 55-57, 62, 74, 80, 91-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     69    30%   17-40, 45-52, 57-61, 66-84, 93, 95, 110, 112, 127-163
src\core\telegram\service.py                                           205    117    43%   57-73, 77-90, 94, 106-109, 114, 118, 145, 157-159, 163-174, 182-195, 201-209, 214-215, 222-224, 229-230, 238-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     47    52%   10, 41-47, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     13    81%   103-104, 112-113, 117-125
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     39    73%   99-106, 117-134, 158-164, 168-175, 204, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    152    28%   9-13, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223     61    73%   136, 158, 164, 188, 220, 230-233, 254, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      2    96%   105, 111
src\gui\widgets\contabilita\certificati_tab.py                         211     83    61%   110, 114, 118-119, 126, 158-159, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26      4    85%   59-64, 72-73
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  12101    61%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_intent_processing_pdl
======================== 1 warning, 1 error in 19.23s =========================

```
</details>

---
### `tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_intent_processing_pdl`
**Error:** `Unknown Error`

**Timestamp:** `2026-03-06T21:29:12.896649`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_telegram_coverage.py E                                   [100%]

=================================== ERRORS ====================================
_______ ERROR at setup of TestTelegramBridge.test_intent_processing_pdl _______
tests\unit\test_telegram_coverage.py:57: in bridge
    return TelegramUIBridge(mw)
           ^^^^^^^^^^^^^^^^^^^^
src\core\telegram_bridge.py:39: in __init__
    self.ui_commands = TelegramUICommands(self.mw, self.telegram)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\core\telegram\bridge\ui_commands.py:21: in __init__
    super().__init__(main_window)
E   TypeError: QObject(parent: typing.Optional[QObject] = None): argument 1 has unexpected type 'MagicMock'
============================== warnings summary ===============================
tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_intent_processing_pdl
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\core\telegram_bridge.py:34: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    128    31%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     18    76%   32-33, 49-50, 59, 72, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     23    86%   35, 76-78, 88-90, 102, 126-127, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      3    94%   74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59      0   100%
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    146    22%   16, 19, 26-31, 36, 43, 50-51, 55-57, 62, 74, 80, 91-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     69    30%   17-40, 45-52, 57-61, 66-84, 93, 95, 110, 112, 127-163
src\core\telegram\service.py                                           205    117    43%   57-73, 77-90, 94, 106-109, 114, 118, 145, 157-159, 163-174, 182-195, 201-209, 214-215, 222-224, 229-230, 238-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     47    52%   10, 41-47, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     13    81%   103-104, 112-113, 117-125
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     39    73%   99-106, 117-134, 158-164, 168-175, 204, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    152    28%   9-13, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223     61    73%   136, 158, 164, 188, 220, 230-233, 254, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      2    96%   105, 111
src\gui\widgets\contabilita\certificati_tab.py                         211     83    61%   110, 114, 118-119, 126, 158-159, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26      4    85%   59-64, 72-73
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  12101    61%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_intent_processing_pdl
======================== 1 warning, 1 error in 18.53s =========================

```
</details>

---
### `tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_intent_processing_pdl`
**Error:** `Unknown Error`

**Timestamp:** `2026-03-06T21:31:38.645724`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_telegram_coverage.py E                                   [100%]

=================================== ERRORS ====================================
_______ ERROR at setup of TestTelegramBridge.test_intent_processing_pdl _______
tests\unit\test_telegram_coverage.py:42: in bridge
    return TelegramUIBridge(mw)
           ^^^^^^^^^^^^^^^^^^^^
src\core\telegram_bridge.py:39: in __init__
    self.ui_commands = TelegramUICommands(self.mw, self.telegram)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\core\telegram\bridge\ui_commands.py:21: in __init__
    super().__init__(main_window)
E   TypeError: QObject(parent: typing.Optional[QObject] = None): argument 1 has unexpected type 'MagicMock'
============================== warnings summary ===============================
tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_intent_processing_pdl
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\core\telegram_bridge.py:34: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    128    31%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     18    76%   32-33, 49-50, 59, 72, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     23    86%   35, 76-78, 88-90, 102, 126-127, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      3    94%   74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59      0   100%
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    146    22%   16, 19, 26-31, 36, 43, 50-51, 55-57, 62, 74, 80, 91-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     69    30%   17-40, 45-52, 57-61, 66-84, 93, 95, 110, 112, 127-163
src\core\telegram\service.py                                           205    114    44%   57-73, 77-90, 94, 106-109, 114, 118, 145, 163-174, 182-195, 201-209, 214-215, 222-224, 229-230, 238-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     47    52%   10, 41-47, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     13    81%   103-104, 112-113, 117-125
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     39    73%   99-106, 117-134, 158-164, 168-175, 204, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    152    28%   9-13, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223     61    73%   136, 158, 164, 188, 220, 230-233, 254, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      2    96%   105, 111
src\gui\widgets\contabilita\certificati_tab.py                         211     83    61%   110, 114, 118-119, 126, 158-159, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26      4    85%   59-64, 72-73
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  12098    61%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_intent_processing_pdl
======================== 1 warning, 1 error in 18.48s =========================

```
</details>

---
### `tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_handle_command_run_ts`
**Error:** `Unknown Error`

**Timestamp:** `2026-03-06T21:34:08.340306`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 0 items

============================ no tests ran in 7.89s ============================
ERROR: not found: C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_telegram_coverage.py::TestTelegramBridge::test_handle_command_run_ts
(no match in any of [<Class TestTelegramBridge>])


```
</details>

---
### `tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_handle_command_run_ts`
**Error:** `Unknown Error`

**Timestamp:** `2026-03-06T21:37:21.807593`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_telegram_coverage.py E                                   [100%]

=================================== ERRORS ====================================
_______ ERROR at setup of TestTelegramBridge.test_handle_command_run_ts _______
tests\unit\test_telegram_coverage.py:42: in bridge
    return TelegramUIBridge(mw)
           ^^^^^^^^^^^^^^^^^^^^
src\core\telegram_bridge.py:39: in __init__
    self.ui_commands = TelegramUICommands(self.mw, self.telegram)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\core\telegram\bridge\ui_commands.py:21: in __init__
    super().__init__(main_window)
E   TypeError: QObject(parent: typing.Optional[QObject] = None): argument 1 has unexpected type 'MagicMock'
============================== warnings summary ===============================
tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_handle_command_run_ts
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\core\telegram_bridge.py:34: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    128    31%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     18    76%   32-33, 49-50, 59, 72, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     23    86%   35, 76-78, 88-90, 102, 126-127, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      3    94%   74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59      0   100%
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    146    22%   16, 19, 26-31, 36, 43, 50-51, 55-57, 62, 74, 80, 91-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     69    30%   17-40, 45-52, 57-61, 66-84, 93, 95, 110, 112, 127-163
src\core\telegram\service.py                                           205    114    44%   57-73, 77-90, 94, 106-109, 114, 118, 145, 163-174, 182-195, 201-209, 214-215, 222-224, 229-230, 238-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     47    52%   10, 41-47, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     13    81%   103-104, 112-113, 117-125
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     39    73%   99-106, 117-134, 158-164, 168-175, 204, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    152    28%   9-13, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223     61    73%   136, 158, 164, 188, 220, 230-233, 254, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      2    96%   105, 111
src\gui\widgets\contabilita\certificati_tab.py                         211     83    61%   110, 114, 118-119, 126, 158-159, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26      4    85%   59-64, 72-73
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  12098    61%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_telegram_coverage.py::TestTelegramBridge::test_handle_command_run_ts
======================== 1 warning, 1 error in 22.13s =========================

```
</details>

---
### `tests/unit/test_utils_extra.py::test_log_humanizer_fixit_tag`
**Error:** `FAILED tests/unit/test_utils_extra.py::test_log_humanizer_fixit_tag - Asserti...`

**Timestamp:** `2026-03-06T21:48:51.361951`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_utils_extra.py F                                         [100%]

================================== FAILURES ===================================
________________________ test_log_humanizer_fixit_tag _________________________
tests\unit\test_utils_extra.py:33: in test_log_humanizer_fixit_tag
    assert "[FIXIT:ACCOUNT]" in t
E   AssertionError: assert '[FIXIT:ACCOUNT]' in 'Errore credenziali'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     32    65%   34, 39, 44, 49, 64-86, 103, 110-112, 118-120, 135-137, 145-146, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     76    52%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 279, 283-285, 292-294
src\bots\portale_fornitori\timbrature\storage.py                       186     95    49%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 377, 386-388, 414-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     18    76%   32-33, 49-50, 59, 72, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     23    86%   35, 76-78, 88-90, 102, 126-127, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      3    94%   74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59      0   100%
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186     49    74%   16, 19, 36, 43, 109-113, 119-132, 144, 146, 161-166, 197, 204-205, 208-209, 212-213, 270, 316-319, 324-325, 333-337, 342, 346-350
src\core\telegram\handlers\commands.py                                  48      9    81%   16, 25-27, 57-59, 83, 94
src\core\telegram\handlers\messages.py                                  98     26    73%   23, 68, 72-81, 93, 95, 110, 112, 129-130, 146-161
src\core\telegram\service.py                                           205     55    73%   59-61, 90, 94, 106-109, 118, 145, 163-174, 214-215, 222-224, 229-230, 238-240, 245-246, 254-256, 261, 263, 265, 271-273, 280, 282, 284, 291-293, 300, 302, 304, 312-314
src\core\telegram\ui\keyboards.py                                       98      9    91%   101-102, 182-187, 249-254, 259-263
src\core\telegram_bridge.py                                             69     13    81%   103-104, 112-113, 117-125
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98      2    98%   90-91
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     39    73%   99-106, 117-134, 158-164, 168-175, 204, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    152    28%   9-13, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223     61    73%   136, 158, 164, 188, 220, 230-233, 254, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      2    96%   105, 111
src\gui\widgets\contabilita\certificati_tab.py                         211     83    61%   110, 114, 118-119, 126, 158-159, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     15    82%   14-15, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     30    73%   33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26      4    85%   59-64, 72-73
src\utils\validators.py                                                 73      1    99%   121
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  11670    62%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_utils_extra.py::test_log_humanizer_fixit_tag - Asserti...
============================= 1 failed in 10.49s ==============================

```
</details>

---
### `tests/unit/test_ux_settings_menus.py::test_context_menu_setup`
**Error:** `FAILED tests/unit/test_ux_settings_menus.py::test_context_menu_setup - Attrib...`

**Timestamp:** `2026-03-06T21:51:01.665950`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_ux_settings_menus.py F                                   [100%]

================================== FAILURES ===================================
___________________________ test_context_menu_setup ___________________________
tests\unit\test_ux_settings_menus.py:21: in test_context_menu_setup
    assert lists_page.account_list.contextMenuPolicy() == Qt.ContextMenuPolicy.CustomContextMenu
           ^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'ListsPage' object has no attribute 'account_list'
============================== warnings summary ===============================
tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\main_panel.py:48: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\components\animated_tab_widget.py:36: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\components\animated_stack.py:32: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\tabs\config_tab.py:125: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:91: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\pages\general_page.py:31: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:357: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(title, parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:205: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(text, parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:165: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:116: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(text, parent) if text else super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\modern_button.py:43: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(text, parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:233: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\tabs\config_tab.py:50: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__()

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\pages\lists_page.py:29: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\widgets\account_list_widget.py:51: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:296: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\widgets\core_widgets.py:62: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\widgets\editable_list_widget.py:50: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\pages\paths_page.py:33: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\pages\diag_page.py:19: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\tabs\roi_tab.py:162: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\tabs\roi_tab.py:32: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\tabs\backup_tab.py:112: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\tabs\backup_tab.py:42: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__()

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\tabs\telegram_tab.py:121: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__(parent)

tests/unit/test_ux_settings_menus.py::test_context_menu_setup
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui\panels\settings\tabs\telegram_tab.py:48: DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
    super().__init__()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              306     29    91%   139-140, 155, 264, 342, 348, 359, 361-362, 397, 413, 443, 458, 466, 478, 482-486, 490-495, 506-508
src\bots\base\login_page.py                                             94     10    89%   90-94, 102, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          169    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             61     10    84%   65, 79, 83, 113, 119-120, 125-126, 137-138
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54      9    83%   47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         106     26    75%   51, 73, 76, 89, 111, 120-123, 134, 155-173, 183
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     207     81    61%   43-45, 86-88, 101-103, 113-115, 127, 171, 188-213, 225-228, 238-267, 276-277, 279-280, 286-291, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                           107     21    80%   85, 87, 108-112, 124, 132-133, 156, 159-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217     77    65%   75-76, 79, 101-106, 116-117, 124-125, 160-162, 179-187, 196-224, 228-235, 239-259, 268, 272, 289-291, 297-298, 337-341, 348-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259     99    62%   61, 80-82, 88, 95, 99, 112-113, 130, 135-137, 143-145, 151-156, 196-198, 206, 213, 224-240, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         109     18    83%   39-45, 54-62, 143-144, 152-154, 160-162
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     32    65%   34, 39, 44, 49, 64-86, 103, 110-112, 118-120, 135-137, 145-146, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     76    52%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 279, 283-285, 292-294
src\bots\portale_fornitori\timbrature\storage.py                       186     95    49%   125, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 377, 386-388, 414-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     20    68%   30-32, 39-40, 44, 52, 60-62, 66-69, 74, 96-97, 102-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    107    66%   55, 60, 71, 75, 84, 106, 132-137, 147, 149, 155, 176, 188-190, 197-198, 208-210, 217, 246-250, 257, 260-261, 283-287, 291-327, 332, 345-347, 364-367, 373, 389-391, 395-408, 413, 421-432, 437-448, 462, 464, 469-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     16    86%   66, 91, 97-99, 111-113, 123, 140-142, 156, 179, 210-211
src\bots\safework\programmazione_sync\bot.py                            67      9    87%   65, 92-94, 105-107, 140-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            101     11    89%   55-56, 64-66, 73-75, 105-107
src\core\app_updater.py                                                 48      2    96%   38, 97
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                             101     24    76%   62-64, 81-82, 145-148, 150-152, 154-158, 171-172, 181-182, 198-200
src\core\audit\integrity.py                                             16      0   100%
src\core\audit\manager.py                                              140     16    89%   66-67, 178-181, 192, 194, 203-204, 218, 234-235, 288, 290-291
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               25     10    60%   26-47
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                73      0   100%
src\core\backup_manager.py                                             138     14    90%   68, 95, 115, 122, 179-188, 215, 221-223, 249-250
src\core\bug_reporter.py                                               157     38    76%   80, 84-85, 89-90, 94-95, 126-127, 132-135, 140-141, 183-185, 208-210, 215-238, 290-293, 303, 339
src\core\config\account_manager.py                                      53     17    68%   29, 38, 75-95
src\core\config\defaults.py                                              4      0   100%
src\core\config\migration.py                                            70     48    31%   23-31, 36-87, 98
src\core\config\security.py                                             40      2    95%   28, 59
src\core\config_manager.py                                             162     26    84%   74, 109, 187-191, 224-227, 232-243, 249-251, 259, 264, 281-282
src\core\constants.py                                                  124      0   100%
src\core\contabilita\certificati_engine.py                              76     18    76%   32-33, 49-50, 59, 72, 88, 94-112
src\core\contabilita\scarico_ore\controller.py                          53     32    40%   30-32, 39-63, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     13    87%   103, 111, 124-125, 134-141, 152, 168, 186, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      6    93%   79-80, 110-111, 126-127
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102     13    87%   75, 101-103, 113, 132-133, 139, 153-154, 171, 189, 200, 216
src\core\data_synchronizer.py                                           25      0   100%
src\core\database\__init__.py                                            3      0   100%
src\core\database\manager.py                                           123      7    94%   179, 184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
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
src\core\importers\certificati.py                                      116     14    88%   47, 51, 54-55, 64, 105-106, 141, 166-167, 171, 177-179
src\core\importers\contabilita.py                                      133     12    91%   42, 47, 51, 55-57, 118, 186-187, 190-192
src\core\importers\giornaliere.py                                      181     33    82%   44, 55-62, 79, 89, 107, 110, 115, 147, 164, 168, 192-193, 204-212, 229, 243, 249, 257, 281-283
src\core\importers\pdl_sync_manager.py                                 163    163     0%   6-246
src\core\importers\scarico_ore.py                                      189     20    89%   14-15, 22-24, 63, 86-87, 101, 125, 137-138, 152, 200, 232, 241, 245, 258, 274, 316
src\core\importers\storico_oda.py                                       81      9    89%   60, 66, 71, 84-85, 95-96, 184-185
src\core\license_updater.py                                            141     19    87%   113-115, 156, 177-178, 198-199, 204-206, 213, 232, 242, 252-254, 287-289
src\core\license_validator.py                                          168     43    74%   61-64, 94-108, 118-122, 127-131, 141, 174-175, 188, 190, 196, 203-204, 209-210, 222-225, 247-248, 274-275, 278-279, 284-285, 290-291
src\core\logging\__init__.py                                            10      0   100%
src\core\logging\alert_manager.py                                      115     86    25%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          136     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              37      0   100%
src\core\logging\context.py                                             57     10    82%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          74     29    61%   64, 66, 87-88, 121, 167-201
src\core\logging\filters.py                                             60     28    53%   114, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          83      8    90%   84, 125, 164-165, 230-240
src\core\logging\logger.py                                             116     19    84%   84, 96, 123, 135-141, 156-157, 173-174, 182-183, 258, 302-307
src\core\logging\metadata.py                                            86     86     0%   5-198
src\core\logging\metrics.py                                             98     48    51%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           42     42     0%   5-120
src\core\logging\sampling.py                                            54     15    72%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              100     61    39%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             167    133    20%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                163     23    86%   35, 76-78, 88-90, 102, 126-127, 151, 161-162, 214-215, 238, 272-273, 278-279, 315-317
src\core\lyra_sentinel.py                                               30      0   100%
src\core\notification_manager.py                                       116     15    87%   64, 74, 100-101, 166, 217-225, 229
src\core\oda\oda_controller.py                                          32     17    47%   26-54, 59-72, 78-90
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                             94      4    96%   49, 122-124
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      3    94%   74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59      0   100%
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     61    20%   29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     54    28%   34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     78    24%   37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     87    16%   27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186     49    74%   16, 19, 36, 43, 109-113, 119-132, 144, 146, 161-166, 197, 204-205, 208-209, 212-213, 270, 316-319, 324-325, 333-337, 342, 346-350
src\core\telegram\handlers\commands.py                                  48      9    81%   16, 25-27, 57-59, 83, 94
src\core\telegram\handlers\messages.py                                  98     26    73%   23, 68, 72-81, 93, 95, 110, 112, 129-130, 146-161
src\core\telegram\service.py                                           205     55    73%   59-61, 90, 94, 106-109, 118, 145, 163-174, 214-215, 222-224, 229-230, 238-240, 245-246, 254-256, 261, 263, 265, 271-273, 280, 282, 284, 291-293, 300, 302, 304, 312-314
src\core\telegram\ui\keyboards.py                                       98      9    91%   101-102, 182-187, 249-254, 259-263
src\core\telegram_bridge.py                                             69     13    81%   103-104, 112-113, 117-125
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98      2    98%   90-91
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174     78    55%   133-134, 143-145, 153-154, 173-174, 199-219, 254-280, 318-331, 344-394
src\gui\components\animated_stack.py                                    85      3    96%   69-71
src\gui\components\animated_tab_widget.py                              147     39    73%   99-106, 117-134, 158-164, 168-175, 204, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     55    52%   30-104, 107-122, 147, 155-158, 176-177, 184-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     24    37%   26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185     40    78%   74, 109, 144, 152, 171-176, 186-211, 233-234, 246, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     10    90%   63, 71, 118-119, 144-149
src\gui\components\scarico_ore\model.py                                168     98    42%   87-93, 96, 105-118, 129-150, 154, 163-165, 194, 203-207, 211-214, 230-256, 260-277, 289-314
src\gui\controllers\bot_controller.py                                   44     19    57%   77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           275    153    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 340-341, 345-346, 354-355, 371-372, 388, 396, 399-404, 410-415, 419-421, 425-426, 430-431, 452, 455-463, 467-489, 493-494, 498-538
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\controllers\tray_controller.py                                  42     10    76%   40-43, 55-60, 70
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  86     63    27%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\layouts\responsive.py                                           72     13    82%   35-42, 65, 80, 85, 103-104, 109
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     39    45%   43-49, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132     82    38%   102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     18    78%   43-60, 85-89, 93-97, 177-181
src\gui\main_window\components\tray_icon.py                             17      7    59%   38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   32-33, 46-55, 58-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   57
src\gui\main_window\controllers\workflow_controller.py                  59     46    22%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108
src\gui\main_window\main.py                                            223     90    60%   114-135, 140-154, 230, 234-245, 249-251, 256, 260, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 242     19    92%   96-100, 161, 167-168, 172-173, 278, 287, 307-309, 427-430, 438, 463
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               210    152    28%   9-13, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         166     85    49%   53-55, 59-63, 146-151, 155-157, 161, 165-177, 181-198, 203, 213-215, 227-229, 233-295, 299-307
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156     33    79%   31-37, 50-53, 80, 94-95, 122-123, 125-126, 142, 192-193, 205, 217-239, 267, 282-283, 301-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  86     65    24%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     77     59    23%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    101    51%   31-74, 78, 218, 222, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         275     55    80%   64, 66, 71-105, 382-383, 388-389, 401-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           139      6    96%   205, 221-225
src\gui\panels\lyra\__init__.py                                          2      0   100%
src\gui\panels\lyra\chat_area.py                                        72     16    78%   69-71, 88, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40      0   100%
src\gui\panels\lyra\input_bar.py                                        63      4    94%   114-117
src\gui\panels\lyra\lyra_panel.py                                      169     54    68%   149, 157, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     39    84%   165-169, 173-175, 185-187, 201, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 342, 344, 353-354, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135     75    44%   56-58, 62-65, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     49    57%   52-54, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73      0   100%
src\gui\panels\scarico_ore\widgets\table_view.py                        91     59    35%   48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131     41    69%   112-124, 150-151, 155-167, 171-175, 206, 218-233, 247-249
src\gui\panels\scarico_pdl.py                                          229     65    72%   76-79, 203-205, 209-228, 232-242, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  100     24    76%   148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33      2    94%   46-47
src\gui\panels\settings\pages\general_page.py                          120      9    92%   138, 152-160
src\gui\panels\settings\pages\lists_page.py                             47      0   100%
src\gui\panels\settings\pages\paths_page.py                            166     45    73%   141-163, 188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249
src\gui\panels\settings\shared.py                                       18      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             118      4    97%   219-222
src\gui\panels\settings\tabs\config_tab.py                             150      4    97%   279-282
src\gui\panels\settings\tabs\roi_tab.py                                116      2    98%   135-136
src\gui\panels\settings\tabs\telegram_tab.py                           128      4    97%   228-231
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 121     41    66%   91-103, 119-138, 142-149, 153-159
src\gui\panels\settings\widgets\editable_list_widget.py                 83     26    69%   89-100, 104-107, 111-116, 120-124
src\gui\panels\storico_oda\__init__.py                                   2      0   100%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                155    127    18%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          55     42    24%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     25    60%   76-116, 120-135
src\gui\panels\timbrature\components\settings_tab.py                   102      4    96%   166, 178-180
src\gui\panels\timbrature\panel.py                                     207     27    87%   205, 214, 294-312, 315-322, 337, 352-353, 358
src\gui\panels\timbrature_bot.py                                       111     71    36%   56-58, 62-66, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      6    83%   139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      0   100%
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     26    81%   51-52, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     37    53%   68, 77-78, 82, 86-87, 91-92, 96-106, 129-161
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59      5    92%   146, 168-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 232-233, 239-241, 255-260, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     25    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 288, 310, 346-352
src\gui\widgets\bot_parameters.py                                      222     46    79%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 333-350, 362, 372, 386-387
src\gui\widgets\calendar_date_edit.py                                   18      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            223     61    73%   136, 158, 164, 188, 220, 230-233, 254, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  53      2    96%   105, 111
src\gui\widgets\contabilita\certificati_tab.py                         211     83    61%   110, 114, 118-119, 126, 158-159, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               206    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              68     59    13%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    43     34    21%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       303    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             181    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191     60    69%   95, 100, 134, 151, 179, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     18    50%   13, 25-35, 43-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     31    70%   31-32, 39-53, 130, 135, 161, 184-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        106     11    90%   41, 48, 55, 139-140, 143-144, 384-385, 388-389
src\gui\widgets\dashboard\don_ciro_widget.py                           462    111    76%   124, 128-129, 134, 138-139, 144, 148-149, 193, 207, 218, 227, 230, 232, 234-244, 249-256, 260-261, 265-267, 271-272, 276-282, 286-291, 308-313, 345, 358, 372-381, 411-412, 468-475, 498-503, 520-537, 551, 567, 593-598, 605, 613
src\gui\widgets\dashboard\multi_window_status.py                        86     39    55%   40-94, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146     71    51%   49-100, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179     38    79%   292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    175    55%   358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         190     42    78%   82-89, 106-124, 128-143, 149, 155, 240, 267-269, 301-303
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     15    83%   117-122, 135-136, 146-152
src\gui\widgets\footer\components.py                                    57     27    53%   38-50, 59, 91-98, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     11    69%   59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     12    78%   70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     21    82%   145-156, 163-165, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131      9    93%   237-238, 242-243, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     15    81%   270-311, 317-321
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30      0   100%
src\gui\widgets\sidebar\animations.py                                   26      9    65%   35-45
src\gui\widgets\sidebar\components.py                                  127     14    89%   66-67, 159-166, 170-172, 203, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     25    91%   294-302, 328-329, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 403
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     115     39    66%   67-97, 156-158, 168-185
src\gui\widgets\toast.py                                               140     42    70%   153-160, 164-169, 173-175, 179-180, 186-187, 193, 236-243, 251, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39      7    82%   57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     15    82%   14-15, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     20    82%   66-67, 144-147, 149-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41      3    93%   21, 25-26
src\utils\parsing.py                                                    51      0   100%
src\utils\printing.py                                                   90     11    88%   14-15, 57-59, 123-126, 150-151
src\utils\resource_manager.py                                           59     10    83%   20-31, 61, 71, 113
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           26      4    85%   59-64, 72-73
src\utils\validators.py                                                 73      1    99%   121
--------------------------------------------------------------------------------------------------
TOTAL                                                                30654  11660    62%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_ux_settings_menus.py::test_context_menu_setup - Attrib...
======================= 1 failed, 27 warnings in 18.64s =======================

```
</details>

---
