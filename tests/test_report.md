# 📊 Test Execution Report

**Date:** 2026-03-11 11:08:35
**Duration:** 1300.07s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1418 |
| ✅ Passed | 1427 |
| ❌ Failed | 8 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_license_updater_advanced.py::TestLicenseUpdaterAdvanced::test_run_update_full_success`
**Error:** `FAILED tests/unit/test_license_updater_advanced.py::TestLicenseUpdaterAdvanced::test_run_update_full_success`

**Timestamp:** `2026-03-11T10:09:20.882785`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_license_updater_advanced.py F                            [100%]

================================== FAILURES ===================================
___________ TestLicenseUpdaterAdvanced.test_run_update_full_success ___________
tests\unit\test_license_updater_advanced.py:111: in test_run_update_full_success
    assert success is True
E   assert False is True
---------------------------- Captured stdout call -----------------------------
[2026-03-11 10:09:09] INFO     - src.core.license_updater       - Verifica stato licenza cloud...
[2026-03-11 10:09:10] ERROR    - src.core.license_updater       - Errore inatteso durante update licenza: Expecting value: line 1 column 1 (char 0)
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
src\bots\base\base_bot.py                                              340     41    88%   143-144, 159, 268, 350, 356, 367, 369-370, 405, 423, 435-436, 453-459, 463-465, 488, 503, 511, 540, 544-548, 552-557, 568-570
src\bots\base\login_page.py                                             94     73    22%   44-54, 58-78, 82-94, 98-103, 110-154
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
src\bots\portale_fornitori\prenota_bp\bot.py                           107     88    18%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    178    31%   57, 61, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    142    24%   99-100, 123-150, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     42    33%   30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    176    44%   55, 60, 71, 75, 84, 106, 132-137, 147-155, 171, 176, 188-190, 196-210, 214-250, 254-287, 291-327, 332, 345-347, 364-367, 373, 383-391, 395-408, 412-417, 421-432, 437-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     69    38%   61, 66, 71, 83-145, 149-156, 179, 185, 190-206, 210-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            120     17    86%   44, 68-69, 77-80, 87-90, 103-106, 136-137
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
src\core\contabilita\scarico_ore\controller.py                          53     34    36%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     14    86%   103, 111, 124-125, 134-141, 152, 168, 186, 191, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
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
src\core\license_updater.py                                            192     51    73%   70-72, 88, 113, 134-135, 147, 151, 155-156, 161-163, 168-173, 187, 200-211, 214-215, 259-270, 281-286, 294, 306-308, 321-323
src\core\license_validator.py                                          176     57    68%   63-69, 86-115, 120-129, 148, 183, 195, 197, 203-204, 213-215, 233-236, 241, 245, 254-259, 273-276, 284-286, 289-290, 295-296, 301-302
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
src\core\lyra_client.py                                                163    143    12%   28-41, 59-61, 65-78, 82-90, 94-95, 99-127, 131-162, 171-173, 182-215, 224-279, 288-317
src\core\lyra_sentinel.py                                               30      5    83%   45-49
src\core\notification_manager.py                                       116     56    52%   64, 71-77, 81-93, 100-101, 162-167, 179-181, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-107
src\core\oda_manager.py                                                 42     26    38%   29, 38-91, 98-112
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68     44    35%   27-29, 37-43, 48-52, 63-87, 97, 115-135, 148-158
src\core\schemas.py                                                     57      5    91%   71-73, 79, 86
src\core\secrets_manager.py                                            105     23    78%   32, 99, 104, 109, 115-116, 122, 130-135, 141, 149, 155, 170, 177-180, 187-189
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      9    82%   50-53, 55-57, 74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59     24    59%   45-50, 56-60, 73-82, 112-124
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     64    16%   23-25, 29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     58    23%   27-30, 34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     81    21%   31-33, 37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     90    13%   21-23, 27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    165    20%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     49    29%   34-42, 46-62, 66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174    105    40%   133-134, 143-145, 153-154, 173-174, 199-219, 228-282, 292-304, 318-331, 344-394, 403-404
src\gui\components\animated_stack.py                                    85     11    87%   69-71, 134-141
src\gui\components\animated_tab_widget.py                              147     41    72%   99-106, 117-134, 158-164, 168-175, 204, 218-219, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185    163    12%   23-57, 60-68, 71-84, 93-111, 120-145, 148-152, 155, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 243-268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     84    15%   27-79, 82-89, 93-100, 104-111, 118-119, 128-141, 144-149
src\gui\components\scarico_ore\model.py                                168    137    18%   70-96, 105-118, 129-150, 154, 163-165, 175-189, 193-196, 200-207, 211-214, 218-220, 224-226, 230-256, 260-277, 283-285, 289-314
src\gui\controllers\bot_controller.py                                   44     25    43%   45-50, 77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           278    221    21%   58-84, 88-105, 109-130, 134-136, 140-144, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 238-242, 249-292, 296-323, 327-331, 336-364, 380-381, 397, 401-413, 419-424, 428-430, 434-435, 439-440, 444-472, 476-498, 502-503, 507-547
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  97     73    25%   54-118, 122-130, 134-142, 146-159, 175-178, 183-186, 191-194, 199-202
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     54    24%   34-39, 43-49, 53-63, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132    113    14%   43-47, 51-91, 95-98, 102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     62    24%   26-37, 41-81, 85-89, 93-97, 113-117, 129-130, 143-173, 177-181, 185-187
src\gui\main_window\components\tray_icon.py                             17     11    35%   25-29, 38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   26-28, 32-33, 44-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     30    29%   26-28, 32-34, 38-65, 69-73
src\gui\main_window\controllers\signal_connector.py                     19     12    37%   26-27, 36-48, 55-65
src\gui\main_window\controllers\workflow_controller.py                  71     59    17%   23-24, 28-53, 57-62, 69-74, 81-86, 93-98, 105-108, 112-135
src\gui\main_window\main.py                                            244    177    27%   55-116, 120-135, 139-160, 165-179, 191-205, 209-240, 244-251, 256, 260-271, 275-277, 282, 286, 290, 294, 298, 302, 306, 310, 314-317, 324-335, 340-385, 389-391, 399-401, 405-408, 412, 416-417, 423, 428, 433, 438, 443, 448
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 247     19    92%   97-101, 163, 169-170, 174-175, 280, 289, 309-311, 429-432, 440, 474
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   27-32, 39-81, 88-96, 99-102, 106-110, 113-184, 187-241, 244-306, 309-348, 351-397
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130    111    15%   39-82, 86, 90-104, 109-153, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         171     90    47%   53-55, 59-63, 146-151, 155-157, 161, 165-176, 180-203, 208, 218-220, 232-234, 238-302, 306-314
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
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
src\gui\panels\lyra\lyra_panel.py                                      169     51    70%   149, 157, 167-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     56    77%   165-169, 173-175, 179-181, 185-187, 191-192, 196-197, 201, 205-209, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 340, 342, 344, 347-348, 353-354, 361-365, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135    110    19%   39-47, 56-58, 62-65, 70-121, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     94    17%   41-48, 52-54, 59-119, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73     58    21%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        91     72    21%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          229     53    77%   78-79, 203-205, 209-228, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  106     24    77%   156, 160, 164-173, 177-189, 193-202
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
src\gui\panels\settings\widgets\editable_list_widget.py                 83     29    65%   89-100, 104-107, 111-116, 120-124, 130-132
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
src\gui\panels\timbrature_bot.py                                       111     84    24%   44-52, 56-58, 62-66, 71-84, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      4    91%   89-93
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     31    78%   48-49, 51-52, 90-92, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     65    18%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 220, 232-233, 239-241, 253-254, 256-257, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     26    88%   75, 79, 173, 200-201, 203-204, 246-253, 257-260, 270, 310, 346-352
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
src\gui\widgets\dashboard\multi_window_status.py                        86     70    19%   40-94, 107-121, 124-170, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146    125    14%   49-100, 113-121, 125-185, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179    155    13%   38-47, 53-70, 74-87, 91-120, 125-192, 196-202, 208-214, 226-273, 277-285, 292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    353     9%   48-63, 67-68, 71-91, 94-117, 120-193, 196-278, 281-289, 292-303, 308-316, 319-343, 346-352, 358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         233     75    68%   82-89, 106-124, 128-143, 149, 155, 239, 253, 280-282, 322-341, 351, 362-385, 389-391
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   40-94, 98-105, 117-122, 126-130, 134-137, 146-152
src\gui\widgets\footer\components.py                                    57     37    35%   38-50, 59, 75-81, 91-98, 116-118, 127-128, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     27    25%   30-50, 59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     40    27%   33-66, 70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     23    80%   145-156, 162-166, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131     15    89%   237-238, 242-243, 248-255, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     18    77%   270-311, 317-321, 327, 355-356
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     23    23%   16-36, 43-53
src\gui\widgets\sidebar\animations.py                                   26     20    23%   14-25, 29-31, 35-45
src\gui\widgets\sidebar\components.py                                  127    103    19%   27-31, 45-62, 66-67, 77-83, 92-101, 118-147, 151-155, 159-166, 170-172, 181-182, 191-219, 229-235
src\gui\widgets\sidebar_button.py                                       82     20    76%   56, 61-62, 65-73, 77-78, 82-84, 91-92, 103-105
src\gui\widgets\sidebar_widget.py                                      264    236    11%   48-67, 71, 75-76, 82-85, 95-273, 277-285, 294-302, 306-330, 341-385, 389-390, 394-398, 402-441, 445-451
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     118     48    59%   38-48, 67-97, 161-163, 173-190
src\gui\widgets\toast.py                                               158     51    68%   128-130, 150-160, 179-186, 190-195, 199-201, 205-206, 212-213, 219, 265, 272-279, 287, 301-304, 309-312, 317-320, 325-328
src\gui\widgets\update_banner.py                                        39     26    33%   27-32, 35-53, 57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     33    71%   29-33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41     28    32%   19-26, 54-68, 73-95
src\utils\parsing.py                                                    51      7    86%   15, 22, 46-47, 84, 91, 96
src\utils\printing.py                                                   90     70    22%   14-15, 27-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           59     19    68%   20-31, 61, 71, 112-118, 131-132, 145-146
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79     17    78%   43-44, 80-82, 102, 104, 109-111, 116, 122-124, 132-134
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30074  15247    49%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_license_updater_advanced.py::TestLicenseUpdaterAdvanced::test_run_update_full_success
======================== 1 failed, 1 warning in 11.61s ========================

```
</details>

---
### `tests/unit/test_license_validator.py::test_valid_license`
**Error:** `FAILED tests/unit/test_license_validator.py::test_valid_license - AssertionEr...`

**Timestamp:** `2026-03-11T10:12:20.727861`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_license_validator.py F                                   [100%]

================================== FAILURES ===================================
_____________________________ test_valid_license ______________________________
tests\unit\test_license_validator.py:83: in test_valid_license
    assert status == license_validator.LicenseStatus.VALID
E   AssertionError: assert <LicenseStatus.INVALID: 'Invalid'> == <LicenseStatus.VALID: 'Valid'>
E    +  where <LicenseStatus.VALID: 'Valid'> = <enum 'LicenseStatus'>.VALID
E    +    where <enum 'LicenseStatus'> = license_validator.LicenseStatus
---------------------------- Captured stdout call -----------------------------
[2026-03-11 10:12:09] ERROR    - src.core.license_validator     - Errore caricamento licenza: Fernet key must be 32 url-safe base64-encoded bytes.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              340     41    88%   143-144, 159, 268, 350, 356, 367, 369-370, 405, 423, 435-436, 453-459, 463-465, 488, 503, 511, 540, 544-548, 552-557, 568-570
src\bots\base\login_page.py                                             94     73    22%   44-54, 58-78, 82-94, 98-103, 110-154
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
src\bots\portale_fornitori\prenota_bp\bot.py                           107     88    18%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    178    31%   57, 61, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    142    24%   99-100, 123-150, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     42    33%   30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    176    44%   55, 60, 71, 75, 84, 106, 132-137, 147-155, 171, 176, 188-190, 196-210, 214-250, 254-287, 291-327, 332, 345-347, 364-367, 373, 383-391, 395-408, 412-417, 421-432, 437-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     69    38%   61, 66, 71, 83-145, 149-156, 179, 185, 190-206, 210-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            120     17    86%   44, 68-69, 77-80, 87-90, 103-106, 136-137
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
src\core\contabilita\scarico_ore\controller.py                          53     34    36%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     14    86%   103, 111, 124-125, 134-141, 152, 168, 186, 191, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
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
src\core\license_updater.py                                            192     51    73%   70-72, 88, 113, 134-135, 147, 151, 155-156, 161-163, 168-173, 187, 200-211, 214-215, 259-270, 281-286, 294, 306-308, 321-323
src\core\license_validator.py                                          176     49    72%   63-69, 86-115, 120-129, 148, 183, 195, 197, 203-204, 235-236, 241, 258-259, 273-276, 284-286, 289-290, 295-296, 301-302
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
src\core\lyra_client.py                                                163    143    12%   28-41, 59-61, 65-78, 82-90, 94-95, 99-127, 131-162, 171-173, 182-215, 224-279, 288-317
src\core\lyra_sentinel.py                                               30      5    83%   45-49
src\core\notification_manager.py                                       116     56    52%   64, 71-77, 81-93, 100-101, 162-167, 179-181, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-107
src\core\oda_manager.py                                                 42     26    38%   29, 38-91, 98-112
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68     44    35%   27-29, 37-43, 48-52, 63-87, 97, 115-135, 148-158
src\core\schemas.py                                                     57      5    91%   71-73, 79, 86
src\core\secrets_manager.py                                            105     23    78%   32, 99, 104, 109, 115-116, 122, 130-135, 141, 149, 155, 170, 177-180, 187-189
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      9    82%   50-53, 55-57, 74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59     24    59%   45-50, 56-60, 73-82, 112-124
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     64    16%   23-25, 29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     58    23%   27-30, 34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     81    21%   31-33, 37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     90    13%   21-23, 27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    165    20%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     49    29%   34-42, 46-62, 66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174    105    40%   133-134, 143-145, 153-154, 173-174, 199-219, 228-282, 292-304, 318-331, 344-394, 403-404
src\gui\components\animated_stack.py                                    85     11    87%   69-71, 134-141
src\gui\components\animated_tab_widget.py                              147     41    72%   99-106, 117-134, 158-164, 168-175, 204, 218-219, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185    163    12%   23-57, 60-68, 71-84, 93-111, 120-145, 148-152, 155, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 243-268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     84    15%   27-79, 82-89, 93-100, 104-111, 118-119, 128-141, 144-149
src\gui\components\scarico_ore\model.py                                168    137    18%   70-96, 105-118, 129-150, 154, 163-165, 175-189, 193-196, 200-207, 211-214, 218-220, 224-226, 230-256, 260-277, 283-285, 289-314
src\gui\controllers\bot_controller.py                                   44     25    43%   45-50, 77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           278    221    21%   58-84, 88-105, 109-130, 134-136, 140-144, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 238-242, 249-292, 296-323, 327-331, 336-364, 380-381, 397, 401-413, 419-424, 428-430, 434-435, 439-440, 444-472, 476-498, 502-503, 507-547
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  97     73    25%   54-118, 122-130, 134-142, 146-159, 175-178, 183-186, 191-194, 199-202
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     54    24%   34-39, 43-49, 53-63, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132    113    14%   43-47, 51-91, 95-98, 102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     62    24%   26-37, 41-81, 85-89, 93-97, 113-117, 129-130, 143-173, 177-181, 185-187
src\gui\main_window\components\tray_icon.py                             17     11    35%   25-29, 38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   26-28, 32-33, 44-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     30    29%   26-28, 32-34, 38-65, 69-73
src\gui\main_window\controllers\signal_connector.py                     19     12    37%   26-27, 36-48, 55-65
src\gui\main_window\controllers\workflow_controller.py                  71     59    17%   23-24, 28-53, 57-62, 69-74, 81-86, 93-98, 105-108, 112-135
src\gui\main_window\main.py                                            244    177    27%   55-116, 120-135, 139-160, 165-179, 191-205, 209-240, 244-251, 256, 260-271, 275-277, 282, 286, 290, 294, 298, 302, 306, 310, 314-317, 324-335, 340-385, 389-391, 399-401, 405-408, 412, 416-417, 423, 428, 433, 438, 443, 448
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 247     19    92%   97-101, 163, 169-170, 174-175, 280, 289, 309-311, 429-432, 440, 474
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   27-32, 39-81, 88-96, 99-102, 106-110, 113-184, 187-241, 244-306, 309-348, 351-397
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130    111    15%   39-82, 86, 90-104, 109-153, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         171     90    47%   53-55, 59-63, 146-151, 155-157, 161, 165-176, 180-203, 208, 218-220, 232-234, 238-302, 306-314
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
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
src\gui\panels\lyra\lyra_panel.py                                      169     51    70%   149, 157, 167-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     56    77%   165-169, 173-175, 179-181, 185-187, 191-192, 196-197, 201, 205-209, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 340, 342, 344, 347-348, 353-354, 361-365, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135    110    19%   39-47, 56-58, 62-65, 70-121, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     94    17%   41-48, 52-54, 59-119, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73     58    21%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        91     72    21%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          229     53    77%   78-79, 203-205, 209-228, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  106     24    77%   156, 160, 164-173, 177-189, 193-202
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
src\gui\panels\settings\widgets\editable_list_widget.py                 83     29    65%   89-100, 104-107, 111-116, 120-124, 130-132
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
src\gui\panels\timbrature_bot.py                                       111     84    24%   44-52, 56-58, 62-66, 71-84, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      4    91%   89-93
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     31    78%   48-49, 51-52, 90-92, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     65    18%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 220, 232-233, 239-241, 253-254, 256-257, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     26    88%   75, 79, 173, 200-201, 203-204, 246-253, 257-260, 270, 310, 346-352
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
src\gui\widgets\dashboard\multi_window_status.py                        86     70    19%   40-94, 107-121, 124-170, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146    125    14%   49-100, 113-121, 125-185, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179    155    13%   38-47, 53-70, 74-87, 91-120, 125-192, 196-202, 208-214, 226-273, 277-285, 292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    353     9%   48-63, 67-68, 71-91, 94-117, 120-193, 196-278, 281-289, 292-303, 308-316, 319-343, 346-352, 358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         233     75    68%   82-89, 106-124, 128-143, 149, 155, 239, 253, 280-282, 322-341, 351, 362-385, 389-391
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   40-94, 98-105, 117-122, 126-130, 134-137, 146-152
src\gui\widgets\footer\components.py                                    57     37    35%   38-50, 59, 75-81, 91-98, 116-118, 127-128, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     27    25%   30-50, 59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     40    27%   33-66, 70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     23    80%   145-156, 162-166, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131     15    89%   237-238, 242-243, 248-255, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     18    77%   270-311, 317-321, 327, 355-356
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     23    23%   16-36, 43-53
src\gui\widgets\sidebar\animations.py                                   26     20    23%   14-25, 29-31, 35-45
src\gui\widgets\sidebar\components.py                                  127    103    19%   27-31, 45-62, 66-67, 77-83, 92-101, 118-147, 151-155, 159-166, 170-172, 181-182, 191-219, 229-235
src\gui\widgets\sidebar_button.py                                       82     20    76%   56, 61-62, 65-73, 77-78, 82-84, 91-92, 103-105
src\gui\widgets\sidebar_widget.py                                      264    236    11%   48-67, 71, 75-76, 82-85, 95-273, 277-285, 294-302, 306-330, 341-385, 389-390, 394-398, 402-441, 445-451
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     118     48    59%   38-48, 67-97, 161-163, 173-190
src\gui\widgets\toast.py                                               158     51    68%   128-130, 150-160, 179-186, 190-195, 199-201, 205-206, 212-213, 219, 265, 272-279, 287, 301-304, 309-312, 317-320, 325-328
src\gui\widgets\update_banner.py                                        39     26    33%   27-32, 35-53, 57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     33    71%   29-33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41     28    32%   19-26, 54-68, 73-95
src\utils\parsing.py                                                    51      7    86%   15, 22, 46-47, 84, 91, 96
src\utils\printing.py                                                   90     70    22%   14-15, 27-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           59     19    68%   20-31, 61, 71, 112-118, 131-132, 145-146
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79     17    78%   43-44, 80-82, 102, 104, 109-111, 116, 122-124, 132-134
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30074  15239    49%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_license_validator.py::test_valid_license - AssertionEr...
============================= 1 failed in 11.66s ==============================

```
</details>

---
### `tests/unit/test_license_validator_advanced.py::TestLicenseValidatorAdvanced::test_license_data_validation_flow`
**Error:** `FAILED tests/unit/test_license_validator_advanced.py::TestLicenseValidatorAdvanced::test_license_data_validation_flow`

**Timestamp:** `2026-03-11T10:15:26.002729`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_license_validator_advanced.py F                          [100%]

================================== FAILURES ===================================
_______ TestLicenseValidatorAdvanced.test_license_data_validation_flow ________
tests\unit\test_license_validator_advanced.py:98: in test_license_data_validation_flow
    assert status == LicenseStatus.VALID
E   AssertionError: assert <LicenseStatus.INVALID: 'Invalid'> == <LicenseStatus.VALID: 'Valid'>
E    +  where <LicenseStatus.VALID: 'Valid'> = LicenseStatus.VALID
---------------------------- Captured stdout call -----------------------------
[2026-03-11 10:15:15] ERROR    - src.core.license_validator     - Errore caricamento licenza: Fernet key must be 32 url-safe base64-encoded bytes.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              340     41    88%   143-144, 159, 268, 350, 356, 367, 369-370, 405, 423, 435-436, 453-459, 463-465, 488, 503, 511, 540, 544-548, 552-557, 568-570
src\bots\base\login_page.py                                             94     73    22%   44-54, 58-78, 82-94, 98-103, 110-154
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
src\bots\portale_fornitori\prenota_bp\bot.py                           107     88    18%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    178    31%   57, 61, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    142    24%   99-100, 123-150, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     42    33%   30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    176    44%   55, 60, 71, 75, 84, 106, 132-137, 147-155, 171, 176, 188-190, 196-210, 214-250, 254-287, 291-327, 332, 345-347, 364-367, 373, 383-391, 395-408, 412-417, 421-432, 437-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     69    38%   61, 66, 71, 83-145, 149-156, 179, 185, 190-206, 210-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            120     17    86%   44, 68-69, 77-80, 87-90, 103-106, 136-137
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
src\core\contabilita\scarico_ore\controller.py                          53     34    36%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     14    86%   103, 111, 124-125, 134-141, 152, 168, 186, 191, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
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
src\core\license_updater.py                                            192     51    73%   70-72, 88, 113, 134-135, 147, 151, 155-156, 161-163, 168-173, 187, 200-211, 214-215, 259-270, 281-286, 294, 306-308, 321-323
src\core\license_validator.py                                          176     46    74%   63-69, 86-115, 120-129, 148, 183, 195, 197, 203-204, 235-236, 241, 258-259, 285-286, 289-290, 295-296, 301-302
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
src\core\lyra_client.py                                                163    143    12%   28-41, 59-61, 65-78, 82-90, 94-95, 99-127, 131-162, 171-173, 182-215, 224-279, 288-317
src\core\lyra_sentinel.py                                               30      5    83%   45-49
src\core\notification_manager.py                                       116     56    52%   64, 71-77, 81-93, 100-101, 162-167, 179-181, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-107
src\core\oda_manager.py                                                 42     26    38%   29, 38-91, 98-112
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68     44    35%   27-29, 37-43, 48-52, 63-87, 97, 115-135, 148-158
src\core\schemas.py                                                     57      5    91%   71-73, 79, 86
src\core\secrets_manager.py                                            105     23    78%   32, 99, 104, 109, 115-116, 122, 130-135, 141, 149, 155, 170, 177-180, 187-189
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      9    82%   50-53, 55-57, 74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59     24    59%   45-50, 56-60, 73-82, 112-124
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     64    16%   23-25, 29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     58    23%   27-30, 34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     81    21%   31-33, 37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     90    13%   21-23, 27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    165    20%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     49    29%   34-42, 46-62, 66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174    105    40%   133-134, 143-145, 153-154, 173-174, 199-219, 228-282, 292-304, 318-331, 344-394, 403-404
src\gui\components\animated_stack.py                                    85     11    87%   69-71, 134-141
src\gui\components\animated_tab_widget.py                              147     41    72%   99-106, 117-134, 158-164, 168-175, 204, 218-219, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185    163    12%   23-57, 60-68, 71-84, 93-111, 120-145, 148-152, 155, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 243-268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     84    15%   27-79, 82-89, 93-100, 104-111, 118-119, 128-141, 144-149
src\gui\components\scarico_ore\model.py                                168    137    18%   70-96, 105-118, 129-150, 154, 163-165, 175-189, 193-196, 200-207, 211-214, 218-220, 224-226, 230-256, 260-277, 283-285, 289-314
src\gui\controllers\bot_controller.py                                   44     25    43%   45-50, 77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           278    221    21%   58-84, 88-105, 109-130, 134-136, 140-144, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 238-242, 249-292, 296-323, 327-331, 336-364, 380-381, 397, 401-413, 419-424, 428-430, 434-435, 439-440, 444-472, 476-498, 502-503, 507-547
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  97     73    25%   54-118, 122-130, 134-142, 146-159, 175-178, 183-186, 191-194, 199-202
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     54    24%   34-39, 43-49, 53-63, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132    113    14%   43-47, 51-91, 95-98, 102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     62    24%   26-37, 41-81, 85-89, 93-97, 113-117, 129-130, 143-173, 177-181, 185-187
src\gui\main_window\components\tray_icon.py                             17     11    35%   25-29, 38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   26-28, 32-33, 44-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     30    29%   26-28, 32-34, 38-65, 69-73
src\gui\main_window\controllers\signal_connector.py                     19     12    37%   26-27, 36-48, 55-65
src\gui\main_window\controllers\workflow_controller.py                  71     59    17%   23-24, 28-53, 57-62, 69-74, 81-86, 93-98, 105-108, 112-135
src\gui\main_window\main.py                                            244    177    27%   55-116, 120-135, 139-160, 165-179, 191-205, 209-240, 244-251, 256, 260-271, 275-277, 282, 286, 290, 294, 298, 302, 306, 310, 314-317, 324-335, 340-385, 389-391, 399-401, 405-408, 412, 416-417, 423, 428, 433, 438, 443, 448
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 247     19    92%   97-101, 163, 169-170, 174-175, 280, 289, 309-311, 429-432, 440, 474
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   27-32, 39-81, 88-96, 99-102, 106-110, 113-184, 187-241, 244-306, 309-348, 351-397
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130    111    15%   39-82, 86, 90-104, 109-153, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         171     90    47%   53-55, 59-63, 146-151, 155-157, 161, 165-176, 180-203, 208, 218-220, 232-234, 238-302, 306-314
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
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
src\gui\panels\lyra\lyra_panel.py                                      169     51    70%   149, 157, 167-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     56    77%   165-169, 173-175, 179-181, 185-187, 191-192, 196-197, 201, 205-209, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 340, 342, 344, 347-348, 353-354, 361-365, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135    110    19%   39-47, 56-58, 62-65, 70-121, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     94    17%   41-48, 52-54, 59-119, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73     58    21%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        91     72    21%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          229     53    77%   78-79, 203-205, 209-228, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  106     24    77%   156, 160, 164-173, 177-189, 193-202
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
src\gui\panels\settings\widgets\editable_list_widget.py                 83     29    65%   89-100, 104-107, 111-116, 120-124, 130-132
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
src\gui\panels\timbrature_bot.py                                       111     84    24%   44-52, 56-58, 62-66, 71-84, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      4    91%   89-93
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     31    78%   48-49, 51-52, 90-92, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     65    18%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 220, 232-233, 239-241, 253-254, 256-257, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     26    88%   75, 79, 173, 200-201, 203-204, 246-253, 257-260, 270, 310, 346-352
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
src\gui\widgets\dashboard\multi_window_status.py                        86     70    19%   40-94, 107-121, 124-170, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146    125    14%   49-100, 113-121, 125-185, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179    155    13%   38-47, 53-70, 74-87, 91-120, 125-192, 196-202, 208-214, 226-273, 277-285, 292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    353     9%   48-63, 67-68, 71-91, 94-117, 120-193, 196-278, 281-289, 292-303, 308-316, 319-343, 346-352, 358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         233     75    68%   82-89, 106-124, 128-143, 149, 155, 239, 253, 280-282, 322-341, 351, 362-385, 389-391
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   40-94, 98-105, 117-122, 126-130, 134-137, 146-152
src\gui\widgets\footer\components.py                                    57     37    35%   38-50, 59, 75-81, 91-98, 116-118, 127-128, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     27    25%   30-50, 59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     40    27%   33-66, 70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     23    80%   145-156, 162-166, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131     15    89%   237-238, 242-243, 248-255, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     18    77%   270-311, 317-321, 327, 355-356
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     23    23%   16-36, 43-53
src\gui\widgets\sidebar\animations.py                                   26     20    23%   14-25, 29-31, 35-45
src\gui\widgets\sidebar\components.py                                  127    103    19%   27-31, 45-62, 66-67, 77-83, 92-101, 118-147, 151-155, 159-166, 170-172, 181-182, 191-219, 229-235
src\gui\widgets\sidebar_button.py                                       82     20    76%   56, 61-62, 65-73, 77-78, 82-84, 91-92, 103-105
src\gui\widgets\sidebar_widget.py                                      264    236    11%   48-67, 71, 75-76, 82-85, 95-273, 277-285, 294-302, 306-330, 341-385, 389-390, 394-398, 402-441, 445-451
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     118     48    59%   38-48, 67-97, 161-163, 173-190
src\gui\widgets\toast.py                                               158     51    68%   128-130, 150-160, 179-186, 190-195, 199-201, 205-206, 212-213, 219, 265, 272-279, 287, 301-304, 309-312, 317-320, 325-328
src\gui\widgets\update_banner.py                                        39     26    33%   27-32, 35-53, 57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     33    71%   29-33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41     28    32%   19-26, 54-68, 73-95
src\utils\parsing.py                                                    51      7    86%   15, 22, 46-47, 84, 91, 96
src\utils\printing.py                                                   90     70    22%   14-15, 27-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           59     19    68%   20-31, 61, 71, 112-118, 131-132, 145-146
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79     17    78%   43-44, 80-82, 102, 104, 109-111, 116, 122-124, 132-134
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30074  15236    49%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_license_validator_advanced.py::TestLicenseValidatorAdvanced::test_license_data_validation_flow
============================= 1 failed in 10.33s ==============================

```
</details>

---
### `tests/unit/test_license_validator_extended.py::test_get_detailed_license_status_valid`
**Error:** `FAILED tests/unit/test_license_validator_extended.py::test_get_detailed_license_status_valid`

**Timestamp:** `2026-03-11T10:17:41.676029`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_license_validator_extended.py F                          [100%]

================================== FAILURES ===================================
___________________ test_get_detailed_license_status_valid ____________________
tests\unit\test_license_validator_extended.py:73: in test_get_detailed_license_status_valid
    assert status == LicenseStatus.VALID
E   AssertionError: assert <LicenseStatus.INVALID: 'Invalid'> == <LicenseStatus.VALID: 'Valid'>
E    +  where <LicenseStatus.VALID: 'Valid'> = LicenseStatus.VALID
---------------------------- Captured stdout call -----------------------------
[2026-03-11 10:17:31] ERROR    - src.core.license_validator     - Errore caricamento licenza: Fernet key must be 32 url-safe base64-encoded bytes.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              340     41    88%   143-144, 159, 268, 350, 356, 367, 369-370, 405, 423, 435-436, 453-459, 463-465, 488, 503, 511, 540, 544-548, 552-557, 568-570
src\bots\base\login_page.py                                             94     73    22%   44-54, 58-78, 82-94, 98-103, 110-154
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
src\bots\portale_fornitori\prenota_bp\bot.py                           107     88    18%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    178    31%   57, 61, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    142    24%   99-100, 123-150, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     42    33%   30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    176    44%   55, 60, 71, 75, 84, 106, 132-137, 147-155, 171, 176, 188-190, 196-210, 214-250, 254-287, 291-327, 332, 345-347, 364-367, 373, 383-391, 395-408, 412-417, 421-432, 437-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     69    38%   61, 66, 71, 83-145, 149-156, 179, 185, 190-206, 210-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            120     17    86%   44, 68-69, 77-80, 87-90, 103-106, 136-137
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
src\core\contabilita\scarico_ore\controller.py                          53     34    36%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     14    86%   103, 111, 124-125, 134-141, 152, 168, 186, 191, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
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
src\core\license_updater.py                                            192     51    73%   70-72, 88, 113, 134-135, 147, 151, 155-156, 161-163, 168-173, 187, 200-211, 214-215, 259-270, 281-286, 294, 306-308, 321-323
src\core\license_validator.py                                          176     39    78%   66-69, 86-115, 125-129, 148, 183, 195, 197, 203-204, 235-236, 241, 258-259, 285-286, 289-290, 295-296, 301-302
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
src\core\lyra_client.py                                                163    143    12%   28-41, 59-61, 65-78, 82-90, 94-95, 99-127, 131-162, 171-173, 182-215, 224-279, 288-317
src\core\lyra_sentinel.py                                               30      5    83%   45-49
src\core\notification_manager.py                                       116     56    52%   64, 71-77, 81-93, 100-101, 162-167, 179-181, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-107
src\core\oda_manager.py                                                 42     26    38%   29, 38-91, 98-112
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68     44    35%   27-29, 37-43, 48-52, 63-87, 97, 115-135, 148-158
src\core\schemas.py                                                     57      5    91%   71-73, 79, 86
src\core\secrets_manager.py                                            105     23    78%   32, 99, 104, 109, 115-116, 122, 130-135, 141, 149, 155, 170, 177-180, 187-189
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      9    82%   50-53, 55-57, 74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59     24    59%   45-50, 56-60, 73-82, 112-124
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     64    16%   23-25, 29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     58    23%   27-30, 34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     81    21%   31-33, 37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     90    13%   21-23, 27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    165    20%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     49    29%   34-42, 46-62, 66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174    105    40%   133-134, 143-145, 153-154, 173-174, 199-219, 228-282, 292-304, 318-331, 344-394, 403-404
src\gui\components\animated_stack.py                                    85     11    87%   69-71, 134-141
src\gui\components\animated_tab_widget.py                              147     41    72%   99-106, 117-134, 158-164, 168-175, 204, 218-219, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185    163    12%   23-57, 60-68, 71-84, 93-111, 120-145, 148-152, 155, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 243-268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     84    15%   27-79, 82-89, 93-100, 104-111, 118-119, 128-141, 144-149
src\gui\components\scarico_ore\model.py                                168    137    18%   70-96, 105-118, 129-150, 154, 163-165, 175-189, 193-196, 200-207, 211-214, 218-220, 224-226, 230-256, 260-277, 283-285, 289-314
src\gui\controllers\bot_controller.py                                   44     25    43%   45-50, 77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           278    221    21%   58-84, 88-105, 109-130, 134-136, 140-144, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 238-242, 249-292, 296-323, 327-331, 336-364, 380-381, 397, 401-413, 419-424, 428-430, 434-435, 439-440, 444-472, 476-498, 502-503, 507-547
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  97     73    25%   54-118, 122-130, 134-142, 146-159, 175-178, 183-186, 191-194, 199-202
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     54    24%   34-39, 43-49, 53-63, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132    113    14%   43-47, 51-91, 95-98, 102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     62    24%   26-37, 41-81, 85-89, 93-97, 113-117, 129-130, 143-173, 177-181, 185-187
src\gui\main_window\components\tray_icon.py                             17     11    35%   25-29, 38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   26-28, 32-33, 44-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     30    29%   26-28, 32-34, 38-65, 69-73
src\gui\main_window\controllers\signal_connector.py                     19     12    37%   26-27, 36-48, 55-65
src\gui\main_window\controllers\workflow_controller.py                  71     59    17%   23-24, 28-53, 57-62, 69-74, 81-86, 93-98, 105-108, 112-135
src\gui\main_window\main.py                                            244    177    27%   55-116, 120-135, 139-160, 165-179, 191-205, 209-240, 244-251, 256, 260-271, 275-277, 282, 286, 290, 294, 298, 302, 306, 310, 314-317, 324-335, 340-385, 389-391, 399-401, 405-408, 412, 416-417, 423, 428, 433, 438, 443, 448
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 247     19    92%   97-101, 163, 169-170, 174-175, 280, 289, 309-311, 429-432, 440, 474
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   27-32, 39-81, 88-96, 99-102, 106-110, 113-184, 187-241, 244-306, 309-348, 351-397
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130    111    15%   39-82, 86, 90-104, 109-153, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         171     90    47%   53-55, 59-63, 146-151, 155-157, 161, 165-176, 180-203, 208, 218-220, 232-234, 238-302, 306-314
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
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
src\gui\panels\lyra\lyra_panel.py                                      169     51    70%   149, 157, 167-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     56    77%   165-169, 173-175, 179-181, 185-187, 191-192, 196-197, 201, 205-209, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 340, 342, 344, 347-348, 353-354, 361-365, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135    110    19%   39-47, 56-58, 62-65, 70-121, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     94    17%   41-48, 52-54, 59-119, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73     58    21%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        91     72    21%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          229     53    77%   78-79, 203-205, 209-228, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  106     24    77%   156, 160, 164-173, 177-189, 193-202
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
src\gui\panels\settings\widgets\editable_list_widget.py                 83     29    65%   89-100, 104-107, 111-116, 120-124, 130-132
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
src\gui\panels\timbrature_bot.py                                       111     84    24%   44-52, 56-58, 62-66, 71-84, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      4    91%   89-93
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     31    78%   48-49, 51-52, 90-92, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     65    18%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 220, 232-233, 239-241, 253-254, 256-257, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     26    88%   75, 79, 173, 200-201, 203-204, 246-253, 257-260, 270, 310, 346-352
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
src\gui\widgets\dashboard\multi_window_status.py                        86     70    19%   40-94, 107-121, 124-170, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146    125    14%   49-100, 113-121, 125-185, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179    155    13%   38-47, 53-70, 74-87, 91-120, 125-192, 196-202, 208-214, 226-273, 277-285, 292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    353     9%   48-63, 67-68, 71-91, 94-117, 120-193, 196-278, 281-289, 292-303, 308-316, 319-343, 346-352, 358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         233     75    68%   82-89, 106-124, 128-143, 149, 155, 239, 253, 280-282, 322-341, 351, 362-385, 389-391
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   40-94, 98-105, 117-122, 126-130, 134-137, 146-152
src\gui\widgets\footer\components.py                                    57     37    35%   38-50, 59, 75-81, 91-98, 116-118, 127-128, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     27    25%   30-50, 59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     40    27%   33-66, 70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     23    80%   145-156, 162-166, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131     15    89%   237-238, 242-243, 248-255, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     18    77%   270-311, 317-321, 327, 355-356
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     23    23%   16-36, 43-53
src\gui\widgets\sidebar\animations.py                                   26     20    23%   14-25, 29-31, 35-45
src\gui\widgets\sidebar\components.py                                  127    103    19%   27-31, 45-62, 66-67, 77-83, 92-101, 118-147, 151-155, 159-166, 170-172, 181-182, 191-219, 229-235
src\gui\widgets\sidebar_button.py                                       82     20    76%   56, 61-62, 65-73, 77-78, 82-84, 91-92, 103-105
src\gui\widgets\sidebar_widget.py                                      264    236    11%   48-67, 71, 75-76, 82-85, 95-273, 277-285, 294-302, 306-330, 341-385, 389-390, 394-398, 402-441, 445-451
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     118     48    59%   38-48, 67-97, 161-163, 173-190
src\gui\widgets\toast.py                                               158     51    68%   128-130, 150-160, 179-186, 190-195, 199-201, 205-206, 212-213, 219, 265, 272-279, 287, 301-304, 309-312, 317-320, 325-328
src\gui\widgets\update_banner.py                                        39     26    33%   27-32, 35-53, 57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     33    71%   29-33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41     28    32%   19-26, 54-68, 73-95
src\utils\parsing.py                                                    51      7    86%   15, 22, 46-47, 84, 91, 96
src\utils\printing.py                                                   90     70    22%   14-15, 27-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           59     19    68%   20-31, 61, 71, 112-118, 131-132, 145-146
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79     17    78%   43-44, 80-82, 102, 104, 109-111, 116, 122-124, 132-134
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30074  15229    49%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_license_validator_extended.py::test_get_detailed_license_status_valid
============================= 1 failed in 10.70s ==============================

```
</details>

---
### `tests/unit/test_license_validator_hardened.py::TestLicenseValidatorHardened::test_valid_license`
**Error:** `FAILED tests/unit/test_license_validator_hardened.py::TestLicenseValidatorHardened::test_valid_license`

**Timestamp:** `2026-03-11T10:20:52.630172`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_license_validator_hardened.py F                          [100%]

================================== FAILURES ===================================
_______________ TestLicenseValidatorHardened.test_valid_license _______________
tests\unit\test_license_validator_hardened.py:63: in test_valid_license
    assert status == LicenseStatus.VALID
E   AssertionError: assert <LicenseStatus.INVALID: 'Invalid'> == <LicenseStatus.VALID: 'Valid'>
E    +  where <LicenseStatus.VALID: 'Valid'> = LicenseStatus.VALID
---------------------------- Captured stdout call -----------------------------
[2026-03-11 10:20:42] ERROR    - src.core.license_validator     - Errore caricamento licenza: Fernet key must be 32 url-safe base64-encoded bytes.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              340     41    88%   143-144, 159, 268, 350, 356, 367, 369-370, 405, 423, 435-436, 453-459, 463-465, 488, 503, 511, 540, 544-548, 552-557, 568-570
src\bots\base\login_page.py                                             94     73    22%   44-54, 58-78, 82-94, 98-103, 110-154
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
src\bots\portale_fornitori\prenota_bp\bot.py                           107     88    18%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         217    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           259    178    31%   57, 61, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 290, 319-321, 327-358, 362-373, 391, 398-418, 427-428
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            92     64    30%   29, 34, 39, 44, 49, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159     97    39%   48-56, 75-77, 81-140, 163-164, 175-178, 181, 197-198, 202-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       186    142    24%   99-100, 123-150, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    22      0   100%
src\bots\safework\pages\login_page.py                                   68     52    24%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             46     29    37%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     63     42    33%   30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           314    176    44%   55, 60, 71, 75, 84, 106, 132-137, 147-155, 171, 176, 188-190, 196-210, 214-250, 254-287, 291-327, 332, 345-347, 364-367, 373, 383-391, 395-408, 412-417, 421-432, 437-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    107     82    23%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             2      0   100%
src\bots\safework\programmazione\bot.py                                111     69    38%   61, 66, 71, 83-145, 149-156, 179, 185, 190-206, 210-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            67     51    24%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                            120     17    86%   44, 68-69, 77-80, 87-90, 103-106, 136-137
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
src\core\contabilita\scarico_ore\controller.py                          53     34    36%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        102     14    86%   103, 111, 124-125, 134-141, 152, 168, 186, 191, 201
src\core\contabilita_queries.py                                         87      4    95%   54, 84, 100, 116
src\core\contabilita_search.py                                          92      8    91%   52-53, 79-80, 110-111, 126-127
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
src\core\license_updater.py                                            192     51    73%   70-72, 88, 113, 134-135, 147, 151, 155-156, 161-163, 168-173, 187, 200-211, 214-215, 259-270, 281-286, 294, 306-308, 321-323
src\core\license_validator.py                                          176     39    78%   66-69, 86-115, 125-129, 148, 183, 195, 197, 203-204, 235-236, 241, 258-259, 285-286, 289-290, 295-296, 301-302
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
src\core\lyra_client.py                                                163    143    12%   28-41, 59-61, 65-78, 82-90, 94-95, 99-127, 131-162, 171-173, 182-215, 224-279, 288-317
src\core\lyra_sentinel.py                                               30      5    83%   45-49
src\core\notification_manager.py                                       116     56    52%   64, 71-77, 81-93, 100-101, 162-167, 179-181, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-107
src\core\oda_manager.py                                                 42     26    38%   29, 38-91, 98-112
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68     44    35%   27-29, 37-43, 48-52, 63-87, 97, 115-135, 148-158
src\core\schemas.py                                                     57      5    91%   71-73, 79, 86
src\core\secrets_manager.py                                            105     23    78%   32, 99, 104, 109, 115-116, 122, 130-135, 141, 149, 155, 170, 177-180, 187-189
src\core\stats\pdl_stats_engine.py                                      89     66    26%   45-191
src\core\stats\roi_engine.py                                           134    107    20%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               49      9    82%   50-53, 55-57, 74, 76, 92
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   23      0   100%
src\core\sync\contabilita_sync.py                                       70      4    94%   54, 125-127
src\core\sync\operazioni_sync.py                                        42      0   100%
src\core\sync\smart_sync.py                                             25      0   100%
src\core\sync_tracker.py                                                59     24    59%   45-50, 56-60, 73-82, 112-124
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              76     64    16%   23-25, 29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              75     58    23%   27-30, 34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             103     81    21%   31-33, 37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                104     90    13%   21-23, 27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    165    20%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             69     49    29%   34-42, 46-62, 66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                20      1    95%   32
src\core\timesheet_processor.py                                         98     75    23%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\cleanup_final.py                                                57     57     0%   8-121
src\gui\components\activity_timeline.py                                174    105    40%   133-134, 143-145, 153-154, 173-174, 199-219, 228-282, 292-304, 318-331, 344-394, 403-404
src\gui\components\animated_stack.py                                    85     11    87%   69-71, 134-141
src\gui\components\animated_tab_widget.py                              147     41    72%   99-106, 117-134, 158-164, 168-175, 204, 218-219, 227, 230, 266, 270, 285
src\gui\components\popout\popout_manager.py                            116    101    13%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185    163    12%   23-57, 60-68, 71-84, 93-111, 120-145, 148-152, 155, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 243-268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     84    15%   27-79, 82-89, 93-100, 104-111, 118-119, 128-141, 144-149
src\gui\components\scarico_ore\model.py                                168    137    18%   70-96, 105-118, 129-150, 154, 163-165, 175-189, 193-196, 200-207, 211-214, 218-220, 224-226, 230-256, 260-277, 283-285, 289-314
src\gui\controllers\bot_controller.py                                   44     25    43%   45-50, 77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           278    221    21%   58-84, 88-105, 109-130, 134-136, 140-144, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 238-242, 249-292, 296-323, 327-331, 336-364, 380-381, 397, 401-413, 419-424, 428-430, 434-435, 439-440, 444-472, 476-498, 502-503, 507-547
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              169    143    15%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   228    202    11%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         201     45    78%   165, 174, 180, 185-188, 333, 353, 365-455
src\gui\dialogs\command_palette.py                                     298    265    11%   61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  97     73    25%   54-118, 122-130, 134-142, 146-159, 175-178, 183-186, 191-194, 199-202
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   1-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      236    236     0%   6-384
src\gui\formatters.py                                                  135     55    59%   15, 23-28, 39, 48, 51, 67-68, 107, 126-128, 142, 170-222, 232-234, 239-240, 246-248
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              71     54    24%   34-39, 43-49, 53-63, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           132    113    14%   43-47, 51-91, 95-98, 102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              82     62    24%   26-37, 41-81, 85-89, 93-97, 113-117, 129-130, 143-173, 177-181, 185-187
src\gui\main_window\components\tray_icon.py                             17     11    35%   25-29, 38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   26-28, 32-33, 44-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                42     30    29%   26-28, 32-34, 38-65, 69-73
src\gui\main_window\controllers\signal_connector.py                     19     12    37%   26-27, 36-48, 55-65
src\gui\main_window\controllers\workflow_controller.py                  71     59    17%   23-24, 28-53, 57-62, 69-74, 81-86, 93-98, 105-108, 112-135
src\gui\main_window\main.py                                            244    177    27%   55-116, 120-135, 139-160, 165-179, 191-205, 209-240, 244-251, 256, 260-271, 275-277, 282, 286, 290, 294, 298, 302, 306, 310, 314-317, 324-335, 340-385, 389-391, 399-401, 405-408, 412, 416-417, 423, 428, 433, 438, 443, 448
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 247     19    92%   97-101, 163, 169-170, 174-175, 280, 289, 309-311, 429-432, 440, 474
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   27-32, 39-81, 88-96, 99-102, 106-110, 113-184, 187-241, 244-306, 309-348, 351-397
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130    111    15%   39-82, 86, 90-104, 109-153, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         171     90    47%   53-55, 59-63, 146-151, 155-157, 161, 165-176, 180-203, 208, 218-220, 232-234, 238-302, 306-314
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 28     15    46%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      93     69    26%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    152    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
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
src\gui\panels\lyra\lyra_panel.py                                      169     51    70%   149, 157, 167-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     22    41%   23-30, 34-46, 62-67
src\gui\panels\notifications_panel.py                                  243     56    77%   165-169, 173-175, 179-181, 185-187, 191-192, 196-197, 201, 205-209, 244, 249, 251, 253, 256, 304-305, 311-319, 334-335, 340, 342, 344, 347-348, 353-354, 361-365, 377-382
src\gui\panels\pdl\__init__.py                                           2      0   100%
src\gui\panels\pdl\pdl_delegate.py                                      17     10    41%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   80     66    18%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        189    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               218    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 44     33    25%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           135    110    19%   39-47, 56-58, 62-65, 70-121, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          113     94    17%   41-48, 52-54, 59-119, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        73     58    21%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        91     72    21%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    131    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          229     53    77%   78-79, 203-205, 209-228, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  106     24    77%   156, 160, 164-173, 177-189, 193-202
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
src\gui\panels\settings\widgets\editable_list_widget.py                 83     29    65%   89-100, 104-107, 111-116, 120-124, 130-132
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
src\gui\panels\timbrature_bot.py                                       111     84    24%   44-52, 56-58, 62-66, 71-84, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              9      0   100%
src\gui\styles\notification_styles.py                                   10      0   100%
src\gui\styles\palette_helpers.py                                       10      3    70%   19-20, 25
src\gui\styles\theme_manager.py                                         85      5    94%   105-106, 109, 118-119
src\gui\styles\widget_styles.py                                         36      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                                        46      4    91%   89-93
src\gui\widgets\__init__.py                                             19      0   100%
src\gui\widgets\activity_feed.py                                       138     31    78%   48-49, 51-52, 90-92, 94-96, 152-153, 173-183, 190, 194-196, 269, 275, 286, 288, 297-313
src\gui\widgets\animated_progress_bar.py                                79     65    18%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit\audit_filter_bar.py                              120     14    88%   152-161, 178-179, 195, 197, 199
src\gui\widgets\audit\audit_pagination_bar.py                           37      3    92%   51, 60-61
src\gui\widgets\audit_log_widget.py                                    120     18    85%   116, 118, 137-147, 150, 153-154, 164, 192-194
src\gui\widgets\automazioni_widget.py                                   59     59     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143     10    93%   178, 182-186, 375, 379-383
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 220, 232-233, 239-241, 253-254, 256-257, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     26    88%   75, 79, 173, 200-201, 203-204, 246-253, 257-260, 270, 310, 346-352
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
src\gui\widgets\dashboard\multi_window_status.py                        86     70    19%   40-94, 107-121, 124-170, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          146    125    14%   49-100, 113-121, 125-185, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                179    155    13%   38-47, 53-70, 74-87, 91-120, 125-192, 196-202, 208-214, 226-273, 277-285, 292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            389    353     9%   48-63, 67-68, 71-91, 94-117, 120-193, 196-278, 281-289, 292-303, 308-316, 319-343, 346-352, 358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  49     41    16%   28-96, 100-111
src\gui\widgets\data_table.py                                          158     16    90%   75-76, 80-81, 85-87, 91-103
src\gui\widgets\effects.py                                              43     20    53%   46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         233     75    68%   82-89, 106-124, 128-143, 149, 155, 239, 253, 280-282, 322-341, 351, 362-385, 389-391
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 88     73    17%   40-94, 98-105, 117-122, 126-130, 134-137, 146-152
src\gui\widgets\footer\components.py                                    57     37    35%   38-50, 59, 75-81, 91-98, 116-118, 127-128, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       20     12    40%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    36     27    25%   30-50, 59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     55     40    27%   33-66, 70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         92     38    59%   30-63, 67, 89-113
src\gui\widgets\message_bubble.py                                       54      0   100%
src\gui\widgets\mixins\clipboard_mixin.py                               87     16    82%   19, 26, 31, 36, 50, 54, 61, 67, 78-82, 99-101
src\gui\widgets\modern_button.py                                        67     12    82%   67-68, 76-77, 83-86, 90-93
src\gui\widgets\modern_card.py                                          42     13    69%   55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                  99     80    19%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   116     23    80%   145-156, 162-166, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            48      9    81%   125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     13    82%   41-42, 44-45, 47-48, 64, 95-96, 137-139, 142
src\gui\widgets\notification_toolbar.py                                131     15    89%   237-238, 242-243, 248-255, 259-260, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                89     74    17%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     82     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   1-216
src\gui\widgets\priority_badge.py                                       48     48     0%   6-112
src\gui\widgets\quick_actions.py                                        78     18    77%   270-311, 317-321, 327, 355-356
src\gui\widgets\safework\status_list.py                                 45     18    60%   51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   1-275
src\gui\widgets\shimmer_widget.py                                       30     23    23%   16-36, 43-53
src\gui\widgets\sidebar\animations.py                                   26     20    23%   14-25, 29-31, 35-45
src\gui\widgets\sidebar\components.py                                  127    103    19%   27-31, 45-62, 66-67, 77-83, 92-101, 118-147, 151-155, 159-166, 170-172, 181-182, 191-219, 229-235
src\gui\widgets\sidebar_button.py                                       82     20    76%   56, 61-62, 65-73, 77-78, 82-84, 91-92, 103-105
src\gui\widgets\sidebar_widget.py                                      264    236    11%   48-67, 71, 75-76, 82-85, 95-273, 277-285, 294-302, 306-330, 341-385, 389-390, 394-398, 402-441, 445-451
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     118     48    59%   38-48, 67-97, 161-163, 173-190
src\gui\widgets\toast.py                                               158     51    68%   128-130, 150-160, 179-186, 190-195, 199-201, 205-206, 212-213, 219, 265, 272-279, 287, 301-304, 309-312, 317-320, 325-328
src\gui\widgets\update_banner.py                                        39     26    33%   27-32, 35-53, 57-60, 63-65
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 74      2    97%   55, 141
src\utils\document_generator.py                                         18      2    89%   40-41
src\utils\document_processor.py                                         83     16    81%   14-15, 25, 38, 59, 63-64, 81-82, 95-96, 106-111
src\utils\helpers.py                                                   112     33    71%   29-33, 66-67, 122, 135-150, 221, 240-253, 274
src\utils\log_humanizer.py                                              41     28    32%   19-26, 54-68, 73-95
src\utils\parsing.py                                                    51      7    86%   15, 22, 46-47, 84, 91, 96
src\utils\printing.py                                                   90     70    22%   14-15, 27-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           59     19    68%   20-31, 61, 71, 112-118, 131-132, 145-146
src\utils\secure_logger.py                                              23      5    78%   52, 57-60
src\utils\security.py                                                   79     17    78%   43-44, 80-82, 102, 104, 109-111, 116, 122-124, 132-134
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30074  15229    49%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_license_validator_hardened.py::TestLicenseValidatorHardened::test_valid_license
============================= 1 failed in 10.42s ==============================

```
</details>

---
### `tests/unit/test_secrets_manager_hardened.py::TestSecretsManagerHardened::test_get_license_key_env_priority`
**Error:** `FAILED tests/unit/test_secrets_manager_hardened.py::TestSecretsManagerHardened::test_get_license_key_env_priority`

**Timestamp:** `2026-03-11T10:41:23.461273`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_secrets_manager_hardened.py F                            [100%]

================================== FAILURES ===================================
________ TestSecretsManagerHardened.test_get_license_key_env_priority _________
tests\unit\test_secrets_manager_hardened.py:23: in test_get_license_key_env_priority
    assert key == b"my_env_key"
E   AssertionError: assert b'bXlfZW52X2tleQ==' == b'my_env_key'
E     
E     At index 0 diff: b'b' != b'm'
E     Use -v to get more diff
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              340     41    88%   143-144, 159, 268, 350, 356, 367, 369-370, 405, 423, 435-436, 453-459, 463-465, 488, 503, 511, 540, 544-548, 552-557, 568-570
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
src\core\app_initializer.py                                            120     17    86%   44, 68-69, 77-80, 87-90, 103-106, 136-137
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
src\core\license_updater.py                                            192     51    73%   70-72, 88, 113, 134-135, 147, 151, 155-156, 161-163, 168-173, 187, 200-211, 214-215, 259-270, 281-286, 294, 306-308, 321-323
src\core\license_validator.py                                          176     30    83%   66-69, 98-99, 113-114, 125-129, 148, 195, 197, 203-204, 235-236, 258-259, 285-286, 289-290, 295-296, 301-302
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
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-107
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                            105      7    93%   32, 115-116, 141, 187-189
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
src\gui\controllers\navigation_controller.py                           278    155    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 341-342, 349-350, 354-355, 363-364, 380-381, 397, 405, 408-413, 419-424, 428-430, 434-435, 439-440, 461, 464-472, 476-498, 502-503, 507-547
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
src\gui\dialogs\confirmation_dialog.py                                  97     73    25%   54-118, 122-130, 134-142, 146-159, 175-178, 183-186, 191-194, 199-202
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
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-65, 69-73
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   59
src\gui\main_window\controllers\workflow_controller.py                  71     57    20%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108, 112-135
src\gui\main_window\main.py                                            244    106    57%   120-135, 139-160, 165-179, 256, 260-271, 275-277, 282, 286, 294, 298, 302, 306, 310, 314-317, 324-335, 340-385, 389-391, 399-401, 405-408, 412, 416-417, 428, 433, 438, 443, 448
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 247     19    92%   97-101, 163, 169-170, 174-175, 280, 289, 309-311, 429-432, 440, 474
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   27-32, 39-81, 88-96, 99-102, 106-110, 113-184, 187-241, 244-306, 309-348, 351-397
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         171     90    47%   53-55, 59-63, 146-151, 155-157, 161, 165-176, 180-203, 208, 218-220, 232-234, 238-302, 306-314
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
src\gui\panels\lyra\lyra_panel.py                                      169     51    70%   149, 157, 167-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
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
src\gui\panels\scarico_pdl.py                                          229     53    77%   78-79, 203-205, 209-228, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  106     24    77%   156, 160, 164-173, 177-189, 193-202
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
src\gui\panels\settings\widgets\editable_list_widget.py                 83     29    65%   89-100, 104-107, 111-116, 120-124, 130-132
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
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 220, 232-233, 239-241, 253-254, 256-257, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     24    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 310, 346-352
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
src\gui\widgets\effects.py                                              43      8    81%   46-47, 53-54, 58-60, 71
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         233     75    68%   82-89, 106-124, 128-143, 149, 155, 239, 253, 280-282, 322-341, 351, 362-385, 389-391
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
src\gui\widgets\sidebar\animations.py                                   26     12    54%   29-31, 35-45
src\gui\widgets\sidebar\components.py                                  127     17    87%   66-67, 98, 159-166, 170-172, 203, 213, 218, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     76    71%   75-76, 84-85, 294-302, 306-330, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 402-441
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     118     39    67%   67-97, 161-163, 173-190
src\gui\widgets\toast.py                                               158     51    68%   128-130, 150-160, 179-186, 190-195, 199-201, 205-206, 212-213, 219, 265, 272-279, 287, 301-304, 309-312, 317-320, 325-328
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
src\utils\security.py                                                   79      8    90%   43-44, 80-82, 109-111
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30915  12594    59%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_secrets_manager_hardened.py::TestSecretsManagerHardened::test_get_license_key_env_priority
============================= 1 failed in 10.72s ==============================

```
</details>

---
### `tests/unit/test_secrets_manager_refactoring.py::test_get_key_from_env`
**Error:** `FAILED tests/unit/test_secrets_manager_refactoring.py::test_get_key_from_env`

**Timestamp:** `2026-03-11T10:43:08.237755`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_secrets_manager_refactoring.py F                         [100%]

================================== FAILURES ===================================
____________________________ test_get_key_from_env ____________________________
tests\unit\test_secrets_manager_refactoring.py:21: in test_get_key_from_env
    assert res == test_key_bytes
E   AssertionError: assert b'ZW52X3Rlc3Rfa2V5' == b'env_test_key'
E     
E     At index 0 diff: b'Z' != b'e'
E     Use -v to get more diff
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              340     41    88%   143-144, 159, 268, 350, 356, 367, 369-370, 405, 423, 435-436, 453-459, 463-465, 488, 503, 511, 540, 544-548, 552-557, 568-570
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
src\core\app_initializer.py                                            120     17    86%   44, 68-69, 77-80, 87-90, 103-106, 136-137
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
src\core\license_updater.py                                            192     51    73%   70-72, 88, 113, 134-135, 147, 151, 155-156, 161-163, 168-173, 187, 200-211, 214-215, 259-270, 281-286, 294, 306-308, 321-323
src\core\license_validator.py                                          176     30    83%   66-69, 98-99, 113-114, 125-129, 148, 195, 197, 203-204, 235-236, 258-259, 285-286, 289-290, 295-296, 301-302
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
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-107
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                            105      6    94%   32, 115-116, 187-189
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
src\gui\controllers\navigation_controller.py                           278    155    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 341-342, 349-350, 354-355, 363-364, 380-381, 397, 405, 408-413, 419-424, 428-430, 434-435, 439-440, 461, 464-472, 476-498, 502-503, 507-547
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
src\gui\dialogs\confirmation_dialog.py                                  97     73    25%   54-118, 122-130, 134-142, 146-159, 175-178, 183-186, 191-194, 199-202
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
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-65, 69-73
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   59
src\gui\main_window\controllers\workflow_controller.py                  71     57    20%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108, 112-135
src\gui\main_window\main.py                                            244    106    57%   120-135, 139-160, 165-179, 256, 260-271, 275-277, 282, 286, 294, 298, 302, 306, 310, 314-317, 324-335, 340-385, 389-391, 399-401, 405-408, 412, 416-417, 428, 433, 438, 443, 448
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 247     19    92%   97-101, 163, 169-170, 174-175, 280, 289, 309-311, 429-432, 440, 474
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   27-32, 39-81, 88-96, 99-102, 106-110, 113-184, 187-241, 244-306, 309-348, 351-397
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         171     90    47%   53-55, 59-63, 146-151, 155-157, 161, 165-176, 180-203, 208, 218-220, 232-234, 238-302, 306-314
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
src\gui\panels\lyra\lyra_panel.py                                      169     51    70%   149, 157, 167-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
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
src\gui\panels\scarico_pdl.py                                          229     53    77%   78-79, 203-205, 209-228, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  106     24    77%   156, 160, 164-173, 177-189, 193-202
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
src\gui\panels\settings\widgets\editable_list_widget.py                 83     29    65%   89-100, 104-107, 111-116, 120-124, 130-132
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
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 220, 232-233, 239-241, 253-254, 256-257, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     24    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 310, 346-352
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
src\gui\widgets\effects.py                                              43      8    81%   46-47, 53-54, 58-60, 71
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         233     75    68%   82-89, 106-124, 128-143, 149, 155, 239, 253, 280-282, 322-341, 351, 362-385, 389-391
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
src\gui\widgets\sidebar\animations.py                                   26     12    54%   29-31, 35-45
src\gui\widgets\sidebar\components.py                                  127     17    87%   66-67, 98, 159-166, 170-172, 203, 213, 218, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     76    71%   75-76, 84-85, 294-302, 306-330, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 402-441
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     118     39    67%   67-97, 161-163, 173-190
src\gui\widgets\toast.py                                               158     51    68%   128-130, 150-160, 179-186, 190-195, 199-201, 205-206, 212-213, 219, 265, 272-279, 287, 301-304, 309-312, 317-320, 325-328
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
src\utils\security.py                                                   79      8    90%   43-44, 80-82, 109-111
src\utils\system_telemetry.py                                           26     26     0%   6-74
src\utils\validators.py                                                 73      2    97%   121, 244
--------------------------------------------------------------------------------------------------
TOTAL                                                                30915  12593    59%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_secrets_manager_refactoring.py::test_get_key_from_env
============================= 1 failed in 10.59s ==============================

```
</details>

---
### `tests/unit/test_security_licensing_deep.py::TestSecretsManagerDeep::test_get_license_key_priority_env`
**Error:** `FAILED tests/unit/test_security_licensing_deep.py::TestSecretsManagerDeep::test_get_license_key_priority_env`

**Timestamp:** `2026-03-11T10:46:10.825127`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_security_licensing_deep.py F                             [100%]

================================== FAILURES ===================================
__________ TestSecretsManagerDeep.test_get_license_key_priority_env ___________
tests\unit\test_security_licensing_deep.py:20: in test_get_license_key_priority_env
    assert SecretsManager.get_license_key() == b"env_key"
E   AssertionError: assert b'ZW52X2tleQ==' == b'env_key'
E     
E     At index 0 diff: b'Z' != b'e'
E     Use -v to get more diff
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    24      7    71%   139, 153-159
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              340     41    88%   143-144, 159, 268, 350, 356, 367, 369-370, 405, 423, 435-436, 453-459, 463-465, 488, 503, 511, 540, 544-548, 552-557, 568-570
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
src\core\app_initializer.py                                            120     17    86%   44, 68-69, 77-80, 87-90, 103-106, 136-137
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
src\core\license_updater.py                                            192     51    73%   70-72, 88, 113, 134-135, 147, 151, 155-156, 161-163, 168-173, 187, 200-211, 214-215, 259-270, 281-286, 294, 306-308, 321-323
src\core\license_validator.py                                          176     28    84%   66-69, 113-114, 125-129, 148, 195, 197, 203-204, 235-236, 258-259, 285-286, 289-290, 295-296, 301-302
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
src\core\oda\oda_controller.py                                          40     25    38%   26-54, 59-72, 80-107
src\core\oda_manager.py                                                 42      3    93%   82-84
src\core\pdl\pdl_controller.py                                          66     55    17%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          18     10    44%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         196    164    16%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              68      5    93%   51-52, 133-135
src\core\schemas.py                                                     57      3    95%   72, 79, 86
src\core\secrets_manager.py                                            105      6    94%   32, 115-116, 187-189
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
src\gui\controllers\navigation_controller.py                           278    155    44%   60, 67, 71, 84, 105, 134-136, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 249-292, 296-323, 341-342, 349-350, 354-355, 363-364, 380-381, 397, 405, 408-413, 419-424, 428-430, 434-435, 439-440, 461, 464-472, 476-498, 502-503, 507-547
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
src\gui\dialogs\confirmation_dialog.py                                  97     73    25%   54-118, 122-130, 134-142, 146-159, 175-178, 183-186, 191-194, 199-202
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
src\gui\main_window\controllers\monitoring_controller.py                42     27    36%   32-34, 38-65, 69-73
src\gui\main_window\controllers\signal_connector.py                     19      1    95%   59
src\gui\main_window\controllers\workflow_controller.py                  71     57    20%   28-53, 57-62, 69-74, 81-86, 93-98, 105-108, 112-135
src\gui\main_window\main.py                                            244    106    57%   120-135, 139-160, 165-179, 256, 260-271, 275-277, 282, 286, 294, 298, 302, 306, 310, 314-317, 324-335, 340-385, 389-391, 399-401, 405-408, 412, 416-417, 428, 433, 438, 443, 448
src\gui\main_window\page_index.py                                       28      0   100%
src\gui\models\audit_model.py                                          131     23    82%   80, 125, 138-139, 149, 155, 157, 167-169, 191-192, 198-201, 209, 213, 215-216, 228-230
src\gui\panels\__init__.py                                              22      0   100%
src\gui\panels\base.py                                                 247     19    92%   97-101, 163, 169-170, 174-175, 280, 289, 309-311, 429-432, 440, 474
src\gui\panels\carico_ts.py                                             96     42    56%   54-58, 114-116, 120-122, 131-139, 158-201
src\gui\panels\consuntivo_panel.py                                      46     34    26%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               2      0   100%
src\gui\panels\contabilita_kpi\cards_row.py                             14      0   100%
src\gui\panels\contabilita_kpi\charts.py                               213    189    11%   27-32, 39-81, 88-96, 99-102, 106-110, 113-184, 187-241, 244-306, 309-348, 351-397
src\gui\panels\contabilita_kpi\kpi_panel.py                            161     40    75%   209-214, 238-307
src\gui\panels\contabilita_panel.py                                    263    103    61%   72-76, 225-229, 233, 252, 262-265, 286-287, 290-293, 297-299, 305-307, 314, 323-327, 329-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      130     58    55%   86, 90-104, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         171     90    47%   53-55, 59-63, 146-151, 155-157, 161, 165-176, 180-203, 208, 218-220, 232-234, 238-302, 306-314
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
src\gui\panels\lyra\lyra_panel.py                                      169     51    70%   149, 157, 167-171, 174-175, 178-179, 182-184, 187-192, 195-197, 202, 211, 221-225, 240-242, 246-249, 253-255, 259, 262-274
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
src\gui\panels\scarico_pdl.py                                          229     53    77%   78-79, 203-205, 209-228, 253-256, 284-285, 293-297, 330-333, 337, 385, 393, 402, 406-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           154     33    79%   64-66, 147-152, 156-158, 178, 186, 197-199, 205-214, 257-266, 274-278
src\gui\panels\settings\main_panel.py                                  106     24    77%   156, 160, 164-173, 177-189, 193-202
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
src\gui\panels\settings\widgets\editable_list_widget.py                 83     29    65%   89-100, 104-107, 111-116, 120-124, 130-132
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
src\gui\widgets\autopilot\event_card.py                                131     26    80%   164, 193, 197-212, 220, 232-233, 239-241, 253-254, 256-257, 265-266, 268-269
src\gui\widgets\autopilot\main_widget.py                               208     24    88%   173, 200-201, 203-204, 246-253, 257-260, 270, 310, 346-352
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
src\gui\widgets\effects.py                                              43      8    81%   46-47, 53-54, 58-60, 71
src\gui\widgets\empty_state.py                                          29     21    28%   26-27, 30-63
src\gui\widgets\excel_table.py                                         233     75    68%   82-89, 106-124, 128-143, 149, 155, 239, 253, 280-282, 322-341, 351, 362-385, 389-391
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
src\gui\widgets\sidebar\animations.py                                   26     12    54%   29-31, 35-45
src\gui\widgets\sidebar\components.py                                  127     17    87%   66-67, 98, 159-166, 170-172, 203, 213, 218, 234
src\gui\widgets\sidebar_button.py                                       82      5    94%   56, 61-62, 77-78
src\gui\widgets\sidebar_widget.py                                      264     76    71%   75-76, 84-85, 294-302, 306-330, 370-372, 374-376, 378-380, 382-383, 389-390, 394-398, 402-441
src\gui\widgets\simple_chart.py                                         67     67     0%   1-115
src\gui\widgets\sortable_table_item.py                                  47     33    30%   26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   1-205
src\gui\widgets\status_card.py                                          60      8    87%   98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     46      7    85%   77-83
src\gui\widgets\timeline_widget.py                                     118     39    67%   67-97, 161-163, 173-190
src\gui\widgets\toast.py                                               158     51    68%   128-130, 150-160, 179-186, 190-195, 199-201, 205-206, 212-213, 219, 265, 272-279, 287, 301-304, 309-312, 317-320, 325-328
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
TOTAL                                                                30915  12588    59%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_security_licensing_deep.py::TestSecretsManagerDeep::test_get_license_key_priority_env
============================= 1 failed in 10.63s ==============================

```
</details>

---
