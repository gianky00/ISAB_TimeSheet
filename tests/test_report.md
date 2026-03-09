# 📊 Test Execution Report

**Date:** 2026-03-09 20:06:57
**Duration:** 171.78s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1438 |
| ✅ Passed | 50 |
| ❌ Failed | 1 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_app_initializer_coverage.py::TestAppInitializerCoverage::test_initialize_core_success`
**Error:** `FAILED tests/unit/test_app_initializer_coverage.py::TestAppInitializerCoverage::test_initialize_core_success`

**Timestamp:** `2026-03-09T20:06:57.038765`

<details><summary>Full Output</summary>

```text
============================= test session starts =============================
collected 1 item

tests\unit\test_app_initializer_coverage.py F                            [100%]

================================== FAILURES ===================================
___________ TestAppInitializerCoverage.test_initialize_core_success ___________
C:\Program Files\Python312\Lib\unittest\mock.py:910: in assert_not_called
    raise AssertionError(msg)
E   AssertionError: Expected 'run_update' to not have been called. Called 1 times.
E   Calls: [call()].

During handling of the above exception, another exception occurred:
tests\unit\test_app_initializer_coverage.py:33: in test_initialize_core_success
    mock_core_deps["run_update"].assert_not_called()
E   AssertionError: Expected 'run_update' to not have been called. Called 1 times.
E   Calls: [call()].
---------------------------- Captured stdout call -----------------------------
[2026-03-09 20:06:50] INFO     - AppInitializer                 - [INIT CORE] Inizializzazione Nucleo Sistema
[2026-03-09 20:06:50] INFO     - AppInitializer                 - [INIT CORE] Caricamento Motori Analisi Dati
[2026-03-09 20:06:52] INFO     - AppInitializer                 - Pandas/Numpy loaded successfully
[2026-03-09 20:06:52] INFO     - AppInitializer                 - [INIT CORE] Configurazione Driver Automazione
[2026-03-09 20:06:52] INFO     - AppInitializer                 - Selenium loaded successfully
[2026-03-09 20:06:52] INFO     - AppInitializer                 - [INIT CORE] Verifica Integrità Hardware
[2026-03-09 20:06:52] INFO     - AppInitializer                 - [INIT CORE] Sincronizzazione Licenza Cloud
[2026-03-09 20:06:52] INFO     - AppInitializer                 - [INIT CORE] Connessione Database Sistema
[2026-03-09 20:06:52] INFO     - AppInitializer                 - Database initialized successfully
============================== warnings summary ===============================
.venv\Lib\site-packages\coverage\pytracer.py:223
  C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\coverage\pytracer.py:223: DeprecationWarning: currentThread() is deprecated, use current_thread() instead
    self.thread = self.threading.currentThread()

.venv\Lib\site-packages\_hypothesis_pytestplugin.py:469
  C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_hypothesis_pytestplugin.py:469: UserWarning: Skipping collection of '.hypothesis' directory - this usually means you've explicitly set the `norecursedirs` pytest config option, replacing rather than extending the default ignores.
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

---------- coverage: platform win32, python 3.12.10-final-0 ----------
Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    25      7    72%   139, 153-159
src\bots\base\__init__.py                                                3      0   100%
src\bots\base\base_bot.py                                              320    104    68%   140-141, 146, 156, 196, 198, 220, 247-249, 253, 257, 261, 265, 269-270, 275, 288-291, 318-320, 345, 351, 356-369, 382-383, 400, 408-419, 423-431, 451-453, 458-461, 466-476, 482-491, 495, 499-503, 507-512, 522-526
src\bots\base\login_page.py                                             95     73    23%   44-54, 58-78, 82-94, 98-103, 110-154
src\bots\base\wait_helpers.py                                          170    141    17%   50-55, 76-81, 100-104, 135-198, 221, 250-307, 327-328, 331-335, 348, 351-355, 377-380, 383-393, 423-439, 469-476
src\bots\portale_fornitori\carico_ts\__init__.py                         3      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             62     39    37%   61, 65, 77-89, 101-138
src\bots\portale_fornitori\carico_ts\locators.py                         7      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            55     40    27%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           13      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      3      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                         107     79    26%   47, 51, 60-66, 72-79, 83-115, 119-136, 146-173, 177-185
src\bots\portale_fornitori\dettagli_oda\locators.py                     20      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     208    179    14%   32-35, 39, 43-45, 51-71, 75-88, 92-118, 122-127, 139-213, 217-228, 238-267, 271-280, 284-292, 296-305
src\bots\portale_fornitori\prenota_bp\__init__.py                        2      1    50%
src\bots\portale_fornitori\prenota_bp\bot.py                           108     88    19%   30, 37, 41, 53-65, 70-77, 81-114, 118-124, 128-171
src\bots\portale_fornitori\prenota_bp\locators.py                       34      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         218    189    13%   28-31, 35, 39-41, 53-79, 90-96, 101-106, 110-138, 142-175, 179-187, 196-224, 228-235, 239-259, 263-275, 279-291, 295-313, 317-341, 345-349
src\bots\portale_fornitori\scarico_ts\__init__.py                        3      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           260    217    17%   57, 61, 73-76, 80-82, 86-101, 105-145, 150-170, 174-208, 212-243, 247-256, 260-285, 289-321, 327-358, 362-373, 377-394, 398-418, 422-433
src\bots\portale_fornitori\scarico_ts\locators.py                       11      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         110     87    21%   28-31, 35, 39-45, 49-66, 70-92, 96-125, 129-154, 158-163, 167-176
src\bots\portale_fornitori\timbrature\__init__.py                        3      1    67%
src\bots\portale_fornitori\timbrature\bot.py                            93     69    26%   29, 34, 39, 44, 49, 56-60, 64-86, 92-149, 156
src\bots\portale_fornitori\timbrature\locators.py                       12      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         160    135    16%   36-40, 44, 48-56, 60-77, 81-140, 150-203, 208-234, 243-254, 259-294
src\bots\portale_fornitori\timbrature\storage.py                       187    159    15%   46-47, 51-111, 115-116, 123-150, 156-185, 204-215, 225-232, 235-263, 270-306, 316-331, 336-377, 380-417, 421-436, 443-444
src\bots\safework\base.py                                               82     49    40%   49-54, 60-78, 82-117, 124-141, 145, 149
src\bots\safework\common\locators.py                                    23      0   100%
src\bots\safework\pages\login_page.py                                   69     52    25%   30-46, 50-82, 90-105, 109, 113-119
src\bots\safework\pages\ricerca_pdl_page.py                             47     29    38%   31-40, 47-77, 81-85, 91-96
src\bots\safework\pages\visualizza_attivita_page.py                     64     42    34%   30-32, 36-40, 44, 48, 52, 56-62, 66-69, 73-104
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           315    215    32%   55, 60, 71, 75, 84, 106, 132-137, 147-155, 171, 175-210, 214-250, 254-287, 291-327, 331-391, 395-408, 412-417, 421-432, 437-448, 454-464, 468-470
src\bots\safework\pdl\search_bot.py                                    108     82    24%   56-57, 62, 67, 72, 84-124, 128-142, 154-168, 172-176, 185-228
src\bots\safework\programmazione\__init__.py                             3      1    67%
src\bots\safework\programmazione\bot.py                                112     88    21%   55-56, 61, 66, 71, 83-145, 149-156, 165-211, 215-217
src\bots\safework\programmazione_sync\bot.py                            68     51    25%   49-50, 55, 60, 65, 77-141
src\core\__init__.py                                                     3      0   100%
src\core\app_initializer.py                                            109     16    85%   55-56, 64-66, 73-75, 88-90, 107-109, 153-154
src\core\app_updater.py                                                 49     37    24%   23-51, 56-61, 72-93, 97
src\core\audit\__init__.py                                               4      1    75%
src\core\audit\database.py                                             101     39    61%   62-64, 81-82, 136-138, 140-143, 145-148, 150-152, 154-158, 171-172, 177-182, 194-200
src\core\audit\integrity.py                                             17      3    82%   22, 27
src\core\audit\manager.py                                              140     70    50%   30, 42, 50, 54, 62-67, 174, 178-181, 187-204, 208-235, 248, 252-255, 264-292
src\core\audit\models.py                                                10      1    90%
src\core\audit\signals.py                                               26     11    58%   26-47
src\core\audit_manager.py                                                6      0   100%
src\core\auth_monitor.py                                                74     63    15%   18, 25-57, 67-132
src\core\backup_manager.py                                             139    105    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-188, 199-207, 212-223, 228-250
src\core\bug_reporter.py                                               158    126    20%   60-107, 112-143, 148-158, 163-185, 190-210, 215-238, 243-295, 300-312, 321-339
src\core\config\account_manager.py                                      54     32    41%   29, 38, 47-57, 62-68, 75-95
src\core\config\defaults.py                                              5      0   100%
src\core\config\migration.py                                            71     55    23%   23-31, 36-87, 95-109
src\core\config\security.py                                             41      7    83%   28, 32-33, 59, 63-65
src\core\config_manager.py                                             163     74    55%   48-49, 54, 74, 83, 103-109, 127-128, 143, 149, 161, 173-175, 180-182, 187-191, 196-199, 211-213, 218-227, 232-243, 249-251, 256-282
src\core\constants.py                                                  125      0   100%
src\core\contabilita\certificati_engine.py                              77     56    27%   22-23, 27-34, 38-50, 58-76, 81-89, 94-112, 117-118
src\core\contabilita\scarico_ore\controller.py                          54     34    37%   30-32, 39-63, 74-75, 84-87, 100-109, 122
src\core\contabilita_manager.py                                        103     51    50%   30, 35, 40, 49-61, 78-125, 134-141, 150-155, 164-171, 176, 181, 186, 191, 201, 210, 225
src\core\contabilita_queries.py                                         88     61    31%   19-30, 35-48, 53-78, 83-94, 100, 109-110, 115-126
src\core\contabilita_search.py                                          93     43    54%   26-82, 90, 110-111, 118-127, 138-139, 159-160
src\core\contabilita_stats.py                                           60     38    37%   33-53, 58-82, 87-101
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                           26      5    81%   27, 34, 41, 46, 63
src\core\database\__init__.py                                            4      1    75%
src\core\database\manager.py                                           124     40    68%   136-145, 154-184, 198-199, 227-229
src\core\database\migrations\contabilita.py                             23      0   100%
src\core\database\migrations\dipendenti.py                              17     13    24%   6-21, 26-28, 33-39
src\core\database\migrations\pdl.py                                     34     27    21%   7-38, 43-91, 96-116, 121-125, 132-134
src\core\database\migrations\storico_oda.py                             11      8    27%   6-49, 56-58
src\core\database\migrations\timbrature.py                              27     22    19%   6-25, 30-32, 37-47, 52-69
src\core\database\pdl_queries.py                                        93     77    17%   23-37, 43-95, 100-136, 144-209
src\core\dipendenti\anagrafica_controller.py                            89     72    19%   27-40, 47-96, 101-139, 144-149
src\core\employees.py                                                   98     82    16%   25-63, 67-69, 76-99, 104-120, 127-192
src\core\excel_importer.py                                               5      0   100%
src\core\importers\__init__.py                                          44     10    77%   33, 50, 62, 73, 77, 88, 99, 104-106
src\core\importers\attivita.py                                          67     50    25%   42-59, 63-79, 83-99, 103-117
src\core\importers\base.py                                              61     38    38%   15-16, 24-26, 36-38, 43-59, 64-76, 81-88
src\core\importers\certificati.py                                      116     91    22%   36-55, 60-64, 69-73, 78-93, 100-122, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      133    107    20%   40-57, 68-104, 111-128, 133-192, 197-214, 219-237, 242-245
src\core\importers\giornaliere.py                                      181    146    19%   42-63, 73-91, 103-122, 130-149, 155-193, 197-212, 216-238, 242-270, 274-290
src\core\importers\pdl_sync_manager.py                                 164    164     0%   6-246
src\core\importers\scarico_ore.py                                      189    153    19%   14-15, 22-24, 61-101, 120-138, 142-161, 175-206, 210-277, 281-290, 307-309, 313-337
src\core\importers\storico_oda.py                                       81     60    26%   58-85, 90-96, 101-117, 122, 127-163, 171-185
src\core\license_updater.py                                            189    121    36%   89, 94, 102-116, 130-157, 168-200, 205-207, 212-217, 231, 244-251, 254-255, 260-261, 270-272, 293-306, 312-330, 340-342, 348-357
src\core\license_validator.py                                          169    120    29%   42-46, 59-64, 75-77, 94-108, 113-122, 127-131, 140-176, 186-204, 209-210, 220-235, 240-249, 254-279, 284-285, 290-291
src\core\logging\__init__.py                                            11      0   100%
src\core\logging\alert_manager.py                                      116     86    26%   51-53, 56-59, 64-69, 81-92, 96-113, 117-119, 123-151, 170-181, 193-210, 222-233, 239-240
src\core\logging\analytics.py                                          137     46    66%   50, 54, 77-81, 100, 129-138, 161-191, 226-228, 264-271, 275, 279, 320, 333, 338, 343
src\core\logging\config.py                                              38      0   100%
src\core\logging\context.py                                             58     10    83%   31-32, 54, 128-129, 139-140, 150, 160-161
src\core\logging\decorators.py                                          75     33    56%   64, 66, 87-88, 105-115, 121, 167-201
src\core\logging\filters.py                                             61     29    52%   114, 117, 121, 139-150, 163-169, 187-188, 197-206
src\core\logging\formatters.py                                          84     11    87%   84, 88-90, 125, 164-165, 224, 230-240
src\core\logging\logger.py                                             117     27    77%   84, 96, 123, 135-141, 145-148, 156-157, 170-174, 182-183, 214, 222, 241, 258, 302-307
src\core\logging\metadata.py                                            87     87     0%   5-198
src\core\logging\metrics.py                                             99     48    52%   78-105, 157, 169-186, 196, 208, 227-237, 246-247, 256-257, 265-268, 277-291
src\core\logging\migration.py                                           43     43     0%   5-120
src\core\logging\sampling.py                                            55     15    73%   58, 67, 95, 100, 105, 122, 144-154, 163, 201
src\core\logging\sinks.py                                              101     61    40%   55, 70-71, 75-78, 91-103, 114-119, 129-136, 140-156, 167-169, 179-184, 196-206, 226-228, 234-236
src\core\logging\viewer.py                                             168    133    21%   31-34, 46-47, 61-69, 82-88, 92, 96, 110-122, 126-127, 131-132, 136-137, 146-160, 169-177, 200-206, 210-214, 218-232, 236-251, 255-257, 261-297, 301-317, 336, 341, 346
src\core\lyra_client.py                                                164    143    13%   28-41, 59-61, 65-78, 82-90, 94-95, 99-127, 131-162, 171-173, 182-215, 224-279, 288-317
src\core\lyra_sentinel.py                                               31      5    84%   45-49
src\core\notification_manager.py                                       117     80    32%   53-57, 61-65, 69-77, 81-93, 97-101, 133-167, 179-181, 190, 194-201, 205-213, 217-225, 229, 233-236, 240-243
src\core\oda\oda_controller.py                                          41     25    39%   26-54, 59-72, 80-107
src\core\oda_manager.py                                                 43     26    40%   29, 38-91, 98-112
src\core\pdl\pdl_controller.py                                          67     55    18%   18, 24-36, 40, 44-109, 114-118
src\core\pdl\period_manager.py                                          19     10    47%   18-26, 31-32, 50-51
src\core\preventivi_manager.py                                         197    164    17%   26-27, 46-49, 53-59, 77-79, 83-113, 126-128, 140-157, 161-205, 212-243, 256-272, 276-312
src\core\report_history.py                                              69     44    36%   27-29, 37-43, 48-52, 63-87, 97, 115-135, 148-158
src\core\schemas.py                                                     58     10    83%   71-73, 78-80, 85-87
src\core\secrets_manager.py                                             95     35    63%   33, 38, 43, 49, 55-56, 64-70, 76, 84, 90, 95, 100-105, 110-115, 122-124, 129-132, 137-143
src\core\stats\pdl_stats_engine.py                                      90     66    27%   45-191
src\core\stats\roi_engine.py                                           135    107    21%   40-52, 57-234, 239-249
src\core\stats_manager.py                                               50     34    32%   28-31, 35, 45-57, 61, 71-80, 89-95, 104
src\core\sync\__init__.py                                                0      0   100%
src\core\sync\base.py                                                   24      3    88%   17, 34, 36
src\core\sync\contabilita_sync.py                                       71     56    21%   22-46, 53-88, 95-112, 117-127
src\core\sync\operazioni_sync.py                                        43     32    26%   22-43, 48-71
src\core\sync\smart_sync.py                                             26      1    96%   22
src\core\sync_tracker.py                                                60     33    45%   40-51, 56-60, 73-82, 95-98, 112-124
src\core\telegram\__init__.py                                            3      1    67%
src\core\telegram\bridge\__init__.py                                     0      0   100%
src\core\telegram\bridge\data_processor.py                              79     65    18%   14, 23-25, 29-39, 43-53, 57-85, 89-105, 109-118
src\core\telegram\bridge\intent_handler.py                              78     59    24%   18, 27-30, 34-56, 60-75, 78-90, 93-104, 107-115, 119-125
src\core\telegram\bridge\system_handler.py                             106     82    23%   22, 31-33, 37-44, 48-71, 75-90, 93-99, 102-115, 118-131, 135-139
src\core\telegram\bridge\ui_commands.py                                107     91    15%   12, 21-23, 27-45, 49-55, 59-62, 66-75, 79-88, 92-107, 111-135, 139-144
src\core\telegram\handlers\callbacks.py                                186    164    12%   14-31, 35-46, 50-51, 55-57, 61-98, 106-132, 140-148, 152-248, 252-255, 263-279, 283-286, 290-303, 307-325, 329-337, 341-350
src\core\telegram\handlers\commands.py                                  48     39    19%   15-35, 53-74, 82-85, 93-97
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-163
src\core\telegram\service.py                                           205    165    20%   43-53, 57-73, 77-90, 94, 98-111, 114, 117-139, 142-159, 163-174, 182-195, 201-209, 213-224, 228-240, 244-256, 259-273, 278-293, 298-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                             70     49    30%   34-42, 46-62, 66-80, 84-90, 94-106, 110-127
src\core\telegram_manager.py                                             3      0   100%
src\core\time_manager.py                                                21     14    33%   23-38, 51-57
src\core\timesheet_processor.py                                         99     75    24%   27-67, 72-82, 87-92, 97-104, 110-144, 149-157, 162-164
src\core\version.py                                                      5      0   100%
src\gui\__init__.py                                                      1      0   100%
src\gui\cleanup_final.py                                                58     58     0%   8-121
src\gui\components\activity_timeline.py                                175    145    17%   47-50, 66-107, 111-124, 133-134, 143-145, 149, 153-154, 160-165, 169, 173-174, 185-186, 199-219, 228-282, 292-304, 318-331, 344-394, 403-404
src\gui\components\animated_stack.py                                    86     76    12%   32-46, 56-130, 134-141, 145-148
src\gui\components\animated_tab_widget.py                              148    119    20%   36-95, 99-106, 115-134, 147-149, 158-164, 168-175, 184-190, 199-212, 216-230, 234-235, 239, 243, 252-254, 258, 262, 266, 270, 274, 285
src\gui\components\popout\popout_manager.py                            117    101    14%   35-46, 52-57, 64-65, 68-196
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                114     96    16%   24-26, 30-104, 107-122, 127-143, 146-158, 161-169, 172-177, 180-185, 195-200
src\gui\components\scarico_ore\filters\header.py                        38     27    29%   20-22, 26-30, 34-66
src\gui\components\scarico_ore\filters\popup_date.py                   185    163    12%   23-57, 60-68, 71-84, 93-111, 120-145, 148-152, 155, 171-176, 179-183, 186-211, 215-220, 224-229, 233-234, 243-268, 271-276
src\gui\components\scarico_ore\filters\popup_list.py                    99     84    15%   27-79, 82-89, 93-100, 104-111, 118-119, 128-141, 144-149
src\gui\components\scarico_ore\model.py                                169    137    19%   70-96, 105-118, 129-150, 154, 163-165, 175-189, 193-196, 200-207, 211-214, 218-220, 224-226, 230-256, 260-277, 283-285, 289-314
src\gui\controllers\bot_controller.py                                   45     33    27%   33-36, 45-50, 61-64, 77-86, 95-107
src\gui\controllers\command_registry.py                                 37     11    70%   42, 46-48, 62-64, 68, 72-73, 77
src\gui\controllers\navigation_controller.py                           282    238    16%   17, 43-46, 58-84, 88-105, 109-130, 134-136, 140-144, 148-152, 156-160, 164-168, 172-176, 180-184, 188-192, 196-200, 204-208, 212-216, 220-224, 228-234, 238-242, 249-292, 296-323, 327-331, 336-361, 373-412, 416-421, 425-427, 431-432, 436-437, 441-469, 473-495, 499-500, 504-544
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              170    143    16%   47-57, 61-72, 79-118, 122-138, 142-249, 255-257, 261-265, 269-285, 289-298, 302, 306-311
src\gui\design\colors.py                                                28      1    96%   105
src\gui\design\spacing.py                                               26      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       69     58    16%   29-123, 126-133, 137
src\gui\dialogs\audit_detail_dialog.py                                  61     47    23%   28-32, 35-115, 118-123
src\gui\dialogs\bug_report_dialog.py                                   229    202    12%   65-69, 73-82, 99-104, 108-250, 254-262, 266-293, 300-322, 326-332, 346-433, 442-455
src\gui\dialogs\certificati_analysis_dialog.py                         202    183     9%   36-45, 48-255, 259-285, 289-361, 365-455
src\gui\dialogs\command_palette.py                                     301    266    12%   40, 61-90, 94-150, 154-181, 185-193, 197-201, 205-211, 215-222, 226-254, 258-267, 271-277, 281-286, 290-293, 297-301, 305-313, 317-326, 330-337, 341-345, 349-386, 390-404, 408-416, 420-432
src\gui\dialogs\confirmation_dialog.py                                  87     63    28%   52-107, 111-119, 123-131, 146-147, 152-153, 158-159, 164-165
src\gui\dialogs\quick_actions_config.py                                 91     91     0%   2-216
src\gui\dialogs\standard_input_dialog.py                                40     30    25%   24-80, 84, 89-91
src\gui\dialogs\startup_dialog.py                                      237    237     0%   6-384
src\gui\formatters.py                                                  135    116    14%   14-28, 38-68, 73, 90-96, 100-103, 107, 111, 115, 119-144, 150-152, 156-159, 163-242, 246-248
src\gui\layouts\responsive.py                                           73     57    22%   17-21, 25-26, 30-31, 35-42, 46-50, 54-55, 59-74, 79-87, 91-93, 97-109
src\gui\main_window\__init__.py                                          3      1    67%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     54    25%   34-39, 43-49, 53-63, 67-78, 82-87, 98-327
src\gui\main_window\components\status_bar.py                           133    113    15%   43-47, 51-91, 95-98, 102-114, 118-130, 137-181, 188-232
src\gui\main_window\components\tool_bar.py                              83     62    25%   26-37, 41-81, 85-89, 93-97, 113-117, 129-130, 143-173, 177-181, 185-187
src\gui\main_window\components\tray_icon.py                             18     11    39%   25-29, 38, 53-62
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    31     21    32%   26-28, 32-33, 44-59, 63, 67-73
src\gui\main_window\controllers\monitoring_controller.py                45     31    31%   17, 26-28, 32-34, 38-63, 67-71
src\gui\main_window\controllers\signal_connector.py                     20     12    40%   26-27, 36-46, 53-63
src\gui\main_window\controllers\workflow_controller.py                  74     60    19%   13, 23-24, 28-53, 57-62, 69-74, 81-86, 93-98, 105-108, 112-134
src\gui\main_window\main.py                                            224    158    29%   55-110, 114-135, 140-154, 165-179, 183-214, 218-225, 230, 234-245, 249-251, 256, 260, 264, 268, 272, 276, 280, 284, 288-291, 298-309, 314-351, 358-360, 364-367, 371, 375-376, 382, 387, 392, 397, 402, 407
src\gui\main_window\page_index.py                                       29      0   100%
src\gui\models\audit_model.py                                          132    105    20%   44-47, 62-64, 68, 72, 79-103, 107-125, 129-139, 143-150, 154-158, 162-170, 174-176, 182-184, 188-192, 196-201, 205-216, 228-230
src\gui\panels\__init__.py                                              23      0   100%
src\gui\panels\base.py                                                 246    180    27%   56-60, 64-84, 96-100, 104-106, 132-145, 152-169, 173-174, 178-239, 246, 250-261, 271, 279, 288, 292-297, 301-304, 308-310, 314-333, 337-340, 344-364, 368-372, 376-381, 391-395, 399-412, 416, 420-421, 428-431, 435-440, 444-462, 466-469
src\gui\panels\carico_ts.py                                             97     73    25%   36-44, 48-50, 54-58, 63-110, 114-116, 120-122, 131-139, 143-144, 148-201
src\gui\panels\consuntivo_panel.py                                      47     34    28%   21-25, 28-44, 48-65, 70-77
src\gui\panels\contabilita_kpi\__init__.py                               3      1    67%
src\gui\panels\contabilita_kpi\cards_row.py                             14      9    36%   10-14, 29-32
src\gui\panels\contabilita_kpi\charts.py                               210    188    10%   9-13, 33-75, 82-90, 93-96, 100-104, 107-178, 181-235, 238-300, 303-342, 345-391
src\gui\panels\contabilita_kpi\kpi_panel.py                            161    141    12%   40-64, 67-183, 196-200, 204-217, 220-230, 233, 236-307
src\gui\panels\contabilita_panel.py                                    264    227    14%   60-66, 70-76, 80-221, 225-229, 233, 244-253, 260-278, 284-301, 305-307, 311-314, 318-332, 336-378, 382-386, 390-407, 411-427
src\gui\panels\dashboard_panel.py                                      131    111    15%   39-82, 86, 90-104, 109-153, 157-172, 176-205, 208-249
src\gui\panels\dettagli_oda.py                                         173    140    19%   42-49, 53-55, 59-63, 68-124, 133-135, 146-151, 155-157, 161, 165-177, 181-204, 208-215, 219-221, 230-235, 239-303, 307-315
src\gui\panels\dipendenti\__init__.py                                    3      1    67%
src\gui\panels\dipendenti\main_panel.py                                 29     15    48%   36-37, 41-66, 75-77
src\gui\panels\dipendenti\pages\anagrafica_page.py                      94     69    27%   34-54, 57-84, 88-100, 103-109, 112-116, 119-121, 124-146, 149-153, 158, 162
src\gui\panels\dipendenti\shared.py                                    153    134    12%   43-90, 121-200, 204-206, 210-212, 216-218, 227, 240-281, 294-329
src\gui\panels\dipendenti\utils\data_helpers.py                         55     46    16%   10-12, 27-55, 66-78, 83-90
src\gui\panels\dipendenti\utils\report_generator.py                    156    128    18%   27-53, 58-101, 110-196, 201-212, 217-239, 244-303
src\gui\panels\dipendenti\widgets\anagrafica_header.py                  87     65    25%   37-38, 42-141, 150, 159-162, 171-179
src\gui\panels\dipendenti\widgets\employee_detail_view.py              105     91    13%   25-30, 33-138, 141-145, 153-165, 171-174
src\gui\panels\dipendenti\widgets\employee_table.py                     78     59    24%   42-44, 48-72, 87-94, 98-103, 112-153
src\gui\panels\dipendenti_manager_panel.py                             206    183    11%   31-74, 78, 89-109, 112-137, 140-203, 206-232, 236-265, 269-286, 290-309, 312-327, 334-369
src\gui\panels\health_panel.py                                         276    240    13%   37-40, 44, 48-49, 52-58, 61-67, 71-105, 119-122, 125-157, 161, 168-169, 172-217, 220, 236-244, 248-363, 367-383, 387-402, 406-422, 426-430, 434-437
src\gui\panels\help_panel.py                                           140    113    19%   33-39, 43-177, 181-201, 204-210, 213-217, 221-225, 230, 246, 265, 281, 297, 312, 325, 341, 354, 368, 383
src\gui\panels\lyra\__init__.py                                          3      1    67%
src\gui\panels\lyra\chat_area.py                                        72     57    21%   21-37, 46-59, 63-72, 77-88, 92-95, 99-105, 109-114
src\gui\panels\lyra\header.py                                           40     28    30%   23-25, 28-80
src\gui\panels\lyra\input_bar.py                                        63     50    21%   22-23, 26-111, 114-117, 121-123
src\gui\panels\lyra\lyra_panel.py                                      169    136    20%   37-45, 48-102, 108-145, 148-161, 164-171, 174-175, 178-179, 182-184, 187-192, 195-197, 201-237, 240-242, 246-249, 253-255, 259, 262-274
src\gui\panels\lyra\workers.py                                          37     26    30%   23-30, 34-46, 55-58, 62-67
src\gui\panels\notifications_panel.py                                  244    194    20%   70-83, 87-161, 165-169, 173-175, 179-181, 185-187, 191-192, 196-197, 201, 205-209, 216-239, 243-263, 267-291, 295-300, 304-305, 309-319, 323-349, 353-354, 358-366, 370-406
src\gui\panels\pdl\__init__.py                                           3      1    67%
src\gui\panels\pdl\pdl_delegate.py                                      18     11    39%   12-13, 17-27
src\gui\panels\pdl\pdl_detail_view.py                                   81     66    19%   44-47, 51-94, 104-138, 142-144
src\gui\panels\pdl\pdl_filter_widget.py                                119    101    15%   30-33, 36-177, 186
src\gui\panels\pdl\pdl_panel.py                                        190    153    19%   49-94, 98-146, 151-165, 174-187, 200-210, 214-215, 220-236, 240-255, 259-261, 265-275, 279-297, 301, 305-308, 316-324
src\gui\panels\pdl\programmazione_tab.py                               219    184    16%   39-45, 48-138, 141-147, 150-153, 156-158, 161-162, 165-205, 208-211, 214-241, 244-253, 258-303, 307-311, 319-333, 337, 341
src\gui\panels\pdl\widgets\pdl_table.py                                 45     33    27%   21-23, 26-50, 54-66
src\gui\panels\prenota_bp.py                                           136    110    19%   39-47, 56-58, 62-65, 70-121, 130-132, 143-148, 152-154, 158-167, 171-176, 180-182, 191-264
src\gui\panels\ricerca_pdl.py                                          114     94    18%   41-48, 52-54, 59-119, 123-126, 130-131, 135-140, 151-190, 195-201, 209-211
src\gui\panels\scarico_ore\widgets\__init__.py                           0      0   100%
src\gui\panels\scarico_ore\widgets\filter_bar.py                        74     58    22%   24-26, 29-88, 93-105, 109-111
src\gui\panels\scarico_ore\widgets\table_view.py                        92     72    22%   24-26, 29-35, 39-44, 48-56, 60-75, 79-92, 96-110, 114-117, 121-133
src\gui\panels\scarico_ore_panel.py                                    132    100    24%   44-58, 62-98, 107-108, 112-124, 134-151, 155-167, 171-175, 179-182, 195, 205-209, 218-233, 237-238, 247-249, 258-261
src\gui\panels\scarico_pdl.py                                          230    193    16%   54-61, 70-72, 76-79, 84-188, 197-199, 203-205, 209-228, 232-242, 251-269, 281-285, 293-297, 311-314, 318-359, 370-381, 385, 389-407, 418-426, 433-448
src\gui\panels\scarico_ts.py                                           155    124    20%   37-50, 56-58, 62-66, 71-125, 134-136, 147-152, 156-158, 162, 166-181, 185-193, 197-199, 205-214, 233-235, 246-303
src\gui\panels\settings\main_panel.py                                  101     71    30%   48-50, 54-124, 128-132, 136-144, 148, 152, 156-165, 169-181, 185-194
src\gui\panels\settings\pages\diag_page.py                              33     19    42%   19-20, 23-42, 46-47
src\gui\panels\settings\pages\general_page.py                          120    102    15%   31-33, 36-127, 131-133, 137-149, 152-160, 164-175, 179-185
src\gui\panels\settings\pages\lists_page.py                             48     35    27%   29-30, 34-62, 66-71, 75-80
src\gui\panels\settings\pages\paths_page.py                            166    137    17%   33-34, 37-94, 99-137, 141-163, 167-188, 205-206, 209, 212-214, 217-219, 222-224, 227-229, 232-234, 237-239, 242-244, 247-249, 255-279, 283-291
src\gui\panels\settings\shared.py                                       18      9    50%   10-29, 34, 61, 83, 103-105
src\gui\panels\settings\tabs\backup_tab.py                             119    103    13%   42-96, 112-114, 118-216, 219-222, 231-232
src\gui\panels\settings\tabs\config_tab.py                             151    128    15%   50-106, 125-128, 132-275, 279-282, 286-288, 292-294
src\gui\panels\settings\tabs\roi_tab.py                                117     97    17%   32-33, 36-104, 108, 126-143, 147-153, 162-163, 166-213, 217, 221
src\gui\panels\settings\tabs\telegram_tab.py                           129    109    16%   48-102, 121-123, 127-225, 228-231, 240-241, 250-251
src\gui\panels\settings\widgets\__init__.py                              0      0   100%
src\gui\panels\settings\widgets\account_list_widget.py                 122     98    20%   51-54, 58-78, 82-87, 91-103, 107-115, 119-138, 142-149, 153-159, 163-170, 179-191
src\gui\panels\settings\widgets\editable_list_widget.py                 84     61    27%   50-53, 57-76, 80-85, 89-100, 104-107, 111-116, 120-124, 128-133, 142-143
src\gui\panels\storico_oda\__init__.py                                   3      1    67%
src\gui\panels\storico_oda\oda_delegate.py                              43     36    16%   13-14, 18-77
src\gui\panels\storico_oda\oda_detail_view.py                           49     37    24%   22-25, 28-52, 56-70, 74-75
src\gui\panels\storico_oda\oda_filter_widget.py                         62     46    26%   27-30, 33-110, 114
src\gui\panels\storico_oda\oda_panel.py                                156    127    19%   48-108, 112-140, 144-160, 164-195, 204-227, 231-244, 248-252, 256-272, 276-290
src\gui\panels\storico_oda\widgets\oda_tree.py                          56     42    25%   21-23, 26-48, 52-62, 66-69, 90-106
src\gui\panels\timbrature\__init__.py                                    3      1    67%
src\gui\panels\timbrature\components\detail_view.py                     63     50    21%   18-41, 44-68, 76-116, 120-135, 139-140
src\gui\panels\timbrature\components\settings_tab.py                   102     86    16%   31-36, 39-99, 103-124, 128-157, 162-169, 172-173, 178-180
src\gui\panels\timbrature\panel.py                                     207    180    13%   44-68, 71-104, 107-188, 191-231, 235-251, 255-290, 294-312, 315-322, 327, 330-353, 358
src\gui\panels\timbrature_bot.py                                       112     84    25%   44-52, 56-58, 62-66, 71-84, 88-90, 94-95, 99-107, 111-116, 125-130, 134-188, 192-194
src\gui\panels\timbrature_db.py                                          3      0   100%
src\gui\styles\__init__.py                                               5      0   100%
src\gui\styles\constants.py                                             10      0   100%
src\gui\styles\notification_styles.py                                   11      5    55%   46-53
src\gui\styles\palette_helpers.py                                       11      3    73%   19-20, 25
src\gui\styles\theme_manager.py                                         86     67    22%   26-29, 34, 42-53, 57-94, 99-122, 126-170, 175
src\gui\styles\widget_styles.py                                         37      7    81%   18, 139, 152, 345-346, 363-364
src\gui\toast.py                                                        47     39    17%   18-63, 67-85, 89-93
src\gui\widgets\__init__.py                                             20      0   100%
src\gui\widgets\activity_feed.py                                       138    118    14%   41-186, 190, 194-196, 205-213, 216-264, 269, 274-320
src\gui\widgets\animated_progress_bar.py                                80     65    19%   36-49, 58-59, 68, 77-78, 82, 86-87, 91-92, 96-106, 115-174
src\gui\widgets\audit\audit_filter_bar.py                              121    101    17%   38-39, 43-137, 146-148, 152-161, 178-179, 188-201
src\gui\widgets\audit\audit_pagination_bar.py                           37     27    27%   14-15, 18-43, 49-56, 60-61
src\gui\widgets\audit_log_widget.py                                    121     95    21%   45-57, 60-130, 133-134, 137-147, 150, 153-154, 163-179, 182-189, 192-194
src\gui\widgets\automazioni_widget.py                                   60     60     0%   7-171
src\gui\widgets\autopilot\__init__.py                                    4      0   100%
src\gui\widgets\autopilot\config_cards.py                              143    129    10%   25-154, 158-166, 170-186, 198-350, 354-363, 367-383
src\gui\widgets\autopilot\event_card.py                                131    113    14%   50-184, 188-189, 193, 197-212, 217-226, 231-275
src\gui\widgets\autopilot\main_widget.py                               209    183    12%   60-71, 75, 79, 83-168, 172-191, 195-204, 208-236, 240-242, 246-253, 257-260, 264-341, 345-394
src\gui\widgets\bot_parameters.py                                      223    185    17%   53-62, 67, 72-73, 77-78, 82-84, 88-105, 135-139, 143-288, 297-304, 308, 327-329, 333-350, 354-362, 366, 370-372, 376-378, 382-387, 391, 395-396
src\gui\widgets\calendar_date_edit.py                                   19     12    37%   17-77
src\gui\widgets\contabilita\attivita_tab.py                            224    188    16%   74-83, 87-160, 164, 168-182, 186-199, 203-214, 218-224, 228-233, 237-255, 259-262, 266-272, 276-279, 283-286, 290-293, 297-300, 304-308, 317-328, 332-341
src\gui\widgets\contabilita\certificati\tree_widget.py                  54     38    30%   48-49, 52-65, 96-132, 136-143
src\gui\widgets\contabilita\certificati_tab.py                         212    175    17%   47-51, 55-91, 95-106, 110, 114, 118-119, 123-129, 133, 137-215, 219-220, 224-227, 231-234, 243-257, 261-293, 297-302, 306-310, 314-321, 325-346
src\gui\widgets\contabilita\consuntivo\crea_nuovo_tab.py               207    178    14%   39-46, 49, 52-199, 202-218, 221-232, 236-262, 265-296, 299-313, 316-337, 340-348
src\gui\widgets\contabilita\consuntivo\impostazioni_tab.py              69     59    14%   24-25, 28-53, 56-103, 106-111
src\gui\widgets\contabilita\consuntivo\log_widget.py                    44     34    23%   34-98, 108-121, 125
src\gui\widgets\contabilita\consuntivo\modifica_esistente_tab.py       304    271    11%   47-56, 59, 62-194, 197-201, 205-245, 248-268, 271-279, 282-341, 345-407, 410-424, 427-435
src\gui\widgets\contabilita\consuntivo\workflow_widgets.py             182    147    19%   48-64, 68-93, 97-102, 106, 110-111, 122-128, 132-206, 210-212, 216-221, 225-226, 271-274, 278-357, 361-366, 376-377, 381-382, 394-399
src\gui\widgets\contabilita\giornaliere_tab.py                         191    159    17%   48-51, 55-96, 100, 103-130, 133-140, 144, 147-168, 171-191, 195-214, 217-242, 245-261
src\gui\widgets\contabilita\helpers.py                                  36     29    19%   11-35, 38-45, 48-53
src\gui\widgets\contabilita\year_tab.py                                102     82    20%   26-27, 31-32, 36-53, 75-95, 98-157, 161, 165-185, 189-220, 224, 228
src\gui\widgets\core_widgets.py                                        107     58    46%   34, 41, 48, 55, 62-63, 66-67, 91-94, 97-98, 116-117, 120-121, 139-140, 143-144, 165-166, 169-170, 205-206, 209-210, 233-234, 237-238, 259-264, 267-268, 296-297, 300-301, 327-328, 331-332, 357-358, 361-362, 384-385, 388-389
src\gui\widgets\dashboard\multi_window_status.py                        87     70    20%   40-94, 107-121, 124-170, 180-204
src\gui\widgets\dashboard\pdl_stats_widget.py                          147    125    15%   49-100, 113-121, 125-185, 190-198, 202-254
src\gui\widgets\dashboard\roi_widget.py                                180    155    14%   38-47, 53-70, 74-87, 91-120, 125-192, 196-202, 208-214, 226-273, 277-285, 292-300, 309-359
src\gui\widgets\dashboard\weather_widget.py                            390    353     9%   48-63, 67-68, 71-91, 94-117, 120-193, 196-278, 281-289, 292-303, 308-316, 319-343, 346-352, 358-375, 378-404, 408-422, 425-428, 435-485, 489-499, 502-529, 532-604, 607-617, 620
src\gui\widgets\dashboard_stat_card.py                                  50     41    18%   28-96, 100-111
src\gui\widgets\data_table.py                                          159    122    23%   56-65, 70, 75-76, 80-81, 85-87, 91-103, 132-136, 140-250, 262-263, 267-292, 296-302, 311-319, 328-330, 339-350, 362
src\gui\widgets\effects.py                                              44     30    32%   29-38, 42, 46-47, 53-54, 58-60, 69-89
src\gui\widgets\empty_state.py                                          30     21    30%   26-27, 30-63
src\gui\widgets\excel_table.py                                         217    178    18%   47-57, 67-78, 82-89, 93-102, 106-124, 128-143, 147-163, 179-181, 185-221, 225-249, 253, 257-268, 278-310, 322-341, 351, 355-357
src\gui\widgets\footer\__init__.py                                       6      0   100%
src\gui\widgets\footer\business_info.py                                 89     73    18%   40-94, 98-105, 117-122, 126-130, 134-137, 146-152
src\gui\widgets\footer\components.py                                    58     37    36%   38-50, 59, 75-81, 91-98, 116-118, 127-128, 132-136, 140-141, 145-147, 165-166
src\gui\widgets\footer\manager.py                                       21     12    43%   35-39, 53-57, 67-68
src\gui\widgets\footer\status_bar.py                                    37     27    27%   30-50, 59-61, 65-68, 72-75
src\gui\widgets\footer\telemetry.py                                     56     40    29%   33-66, 70-73, 77-79, 83-87
src\gui\widgets\info_widgets.py                                         93     75    19%   30-63, 67, 76-84, 89-113, 127-171, 175, 178
src\gui\widgets\message_bubble.py                                       55     47    15%   38-40, 43-140
src\gui\widgets\mixins\clipboard_mixin.py                               88     74    16%   18-43, 47-68, 71-75, 78-82, 85-89, 92-104, 107, 110-122
src\gui\widgets\modern_button.py                                        68     39    43%   43-57, 61-63, 67-68, 72, 76-77, 83-86, 90-93, 97-100, 110-115, 119-158
src\gui\widgets\modern_card.py                                          43     28    35%   23-26, 30-31, 41-51, 55-64, 68-71, 79-82, 86
src\gui\widgets\multi_select_filter.py                                 100     80    20%   26-80, 83-87, 90-93, 102-107, 116-133, 142-145, 154-155, 158-161, 164-168
src\gui\widgets\notification_card.py                                   117     91    22%   58-74, 78-156, 160-166, 170-176, 180-182, 186-189, 193, 197-199
src\gui\widgets\notification_group_header.py                            49     36    27%   35-41, 45-121, 125-128, 132-133, 137, 141-142
src\gui\widgets\notification_item.py                                    74     59    20%   26-29, 32-133, 137-139, 142
src\gui\widgets\notification_toolbar.py                                132    102    23%   42-54, 58-70, 74-76, 80-84, 88-107, 139-145, 149-232, 237-238, 242-243, 248-255, 259-260, 269-271, 275, 279, 283
src\gui\widgets\pdl\status_bar_widget.py                                90     74    18%   33-41, 45-53, 57-69, 73-137
src\gui\widgets\pdl\table_widget.py                                     83     66    20%   31-32, 35-61, 64-92, 96-124
src\gui\widgets\pdl_timeline.py                                        129    129     0%   2-216
src\gui\widgets\priority_badge.py                                       49     49     0%   6-112
src\gui\widgets\quick_actions.py                                        78     61    22%   25-33, 237-238, 241-266, 270-311, 316-356, 361
src\gui\widgets\safework\status_list.py                                 46     36    22%   19-26, 30-47, 51-71
src\gui\widgets\security_dashboard.py                                  159    159     0%   2-275
src\gui\widgets\shimmer_widget.py                                       31     23    26%   16-36, 43-53
src\gui\widgets\sidebar\animations.py                                   27     20    26%   14-25, 29-31, 35-45
src\gui\widgets\sidebar\components.py                                  130    104    20%   11, 27-31, 45-62, 66-67, 77-83, 92-101, 118-147, 151-155, 159-166, 170-172, 181-182, 191-219, 229-235
src\gui\widgets\sidebar_button.py                                       83     63    24%   24-51, 56, 61-62, 65-73, 77-78, 82-84, 87-95, 98-113, 133-139
src\gui\widgets\sidebar_widget.py                                      265    236    11%   48-67, 71, 75-76, 82-85, 95-273, 277-285, 294-302, 306-330, 341-385, 389-390, 394-398, 402-441, 445-451
src\gui\widgets\simple_chart.py                                         67     67     0%   2-115
src\gui\widgets\sortable_table_item.py                                  47     37    21%   21-26, 30-58, 63-76, 80-93
src\gui\widgets\statistics_widget.py                                   108    108     0%   2-205
src\gui\widgets\status_card.py                                          61     45    26%   26-85, 89-92, 98-113, 117, 121-122
src\gui\widgets\status_indicator.py                                     47     37    21%   31-46, 56-73, 77-83
src\gui\widgets\timeline_widget.py                                     116     91    22%   33-34, 38-48, 55-102, 111-112, 115-135, 139-147, 151, 155-158, 168-185
src\gui\widgets\toast.py                                               141    107    24%   70-91, 95-134, 138-160, 164-169, 173-175, 179-180, 184-196, 208-210, 230-259, 265-268, 273-276, 281-284, 289-292
src\gui\widgets\update_banner.py                                        39     26    33%   27-32, 35-53, 57-60, 63-65
src\utils\__init__.py                                                    3      0   100%
src\utils\animation_helpers.py                                         101    101     0%   6-295
src\utils\date_utils.py                                                 75     61    19%   29-40, 54-65, 79-85, 98-101, 115-121, 135-150, 163-170, 184-187, 200, 214, 228-234
src\utils\document_generator.py                                         19     14    26%   13-41
src\utils\document_processor.py                                         84     35    58%   14-15, 24-32, 38, 50-51, 59, 63-64, 71-72, 78-79, 81-82, 86-87, 95-96, 98-100, 106-111
src\utils\helpers.py                                                   113     78    31%   22-24, 29-33, 47-69, 82-84, 89, 116-117, 122, 135-150, 164-166, 181-187, 202, 221, 235, 240-253, 262-284
src\utils\log_humanizer.py                                              42     32    24%   13-26, 54-68, 73-95
src\utils\parsing.py                                                    52     44    15%   14-34, 40-56, 61-71, 76-84, 89-98
src\utils\printing.py                                                   90     73    19%   14-15, 24-29, 34-45, 53-59, 70-151
src\utils\resource_manager.py                                           60     22    63%   20-31, 61, 71, 96-99, 112-118, 131-132, 145-146
src\utils\secure_logger.py                                              24     10    58%   47-54, 57-60
src\utils\security.py                                                   80     24    70%   43-44, 80-82, 102, 104, 109-111, 116, 119-124, 128-134
src\utils\system_telemetry.py                                           27     16    41%   50-74
src\utils\validators.py                                                 74     51    31%   57-75, 88-99, 112-127, 140-225, 238-254, 267-270
--------------------------------------------------------------------------------------------------
TOTAL                                                                30555  23058    25%
Coverage HTML written to dir htmlcov

=========================== short test summary info ===========================
FAILED tests/unit/test_app_initializer_coverage.py::TestAppInitializerCoverage::test_initialize_core_success
======================== 1 failed, 2 warnings in 7.53s ========================

```
</details>

---
