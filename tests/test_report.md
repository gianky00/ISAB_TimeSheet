# 📊 Test Execution Report

**Date:** 2026-01-12 20:39:45
**Duration:** 77.63s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 4 |
| ✅ Passed | 2 |
| ❌ Failed | 2 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_scarico_ts_bot_hardened.py::TestScaricoTSBotHardened::test_process_downloaded_files_vba_style_loop`
**Error:** `FAILED tests/unit/test_scarico_ts_bot_hardened.py::TestScaricoTSBotHardened::test_process_downloaded_files_vba_style_loop`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____ TestScaricoTSBotHardened.test_process_downloaded_files_vba_style_loop ____
tests\unit\test_scarico_ts_bot_hardened.py:72: in test_process_downloaded_files_vba_style_loop
    m_ask = mocker.patch.object(bot, "_ask_user")
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv\Lib\site-packages\pytest_mock\plugin.py:264: in object
    return self._start_patch(
.venv\Lib\site-packages\pytest_mock\plugin.py:229: in _start_patch
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
E   AttributeError: <src.bots.portale_fornitori.scarico_ts.bot.ScaricaTSBot object at 0x000002631A63C8F0> does not have the attribute '_ask_user'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      7    63%   87, 100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281    208    26%   60, 65, 69, 73-75, 83, 85, 92, 94-104, 107, 110, 113, 116-117, 121, 124-155, 158-246, 250-284, 288-318, 322-324, 328-332, 336-338, 342, 346-357, 362, 366, 370-378, 382-390, 393-405, 408-413, 417
src\bots\base\login_page.py                                             95     79    17%   34-37, 45-61, 65-95, 99-113, 117-123, 130-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     28    38%   17, 21, 26, 47, 51, 55-67, 71-91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     46    23%   20-22, 25-34, 37-46, 49-69, 72-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62     43    31%   18, 22, 26, 33, 37, 46-49, 55-62, 65-107
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210    185    12%   28-31, 34, 37-44, 47-80, 83-103, 106-146, 150-163, 174-285, 289-310, 319-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228    145    36%   37, 41, 45, 56, 77, 82, 86-90, 97-199, 203-233, 238, 252-271, 285, 305-306, 319-320, 324-327, 335, 379-383, 394-396, 399-400, 405-410, 416-471
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     52    28%   22, 26, 30, 34, 39-43, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    148    13%   31-34, 37, 41-59, 63-83, 87-154, 158-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170    150    12%   33-34, 38-61, 65-66, 73-96, 102-132, 142-154, 166-233, 249-316, 320-339, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    323     8%   27-51, 55-62, 66-74, 78, 82, 86-111, 115-174, 178-183, 187-431, 434-460, 463-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60     60     0%   1-97
src\core\app_updater.py                                                 38     38     0%   6-80
src\core\audit_manager.py                                              156    156     0%   6-306
src\core\backup_manager.py                                             119    119     0%   6-219
src\core\config_manager.py                                             180    151    16%   55, 64-139, 148-149, 160-233, 238-239, 244-246, 251, 256-271, 276-289, 294-304, 309-313, 318-320, 325-330, 335
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107    107     0%   6-229
src\core\contabilita_queries.py                                         87     87     0%   6-122
src\core\contabilita_search.py                                          85     85     0%   6-181
src\core\contabilita_stats.py                                           57     57     0%   6-92
src\core\contabilita_worker.py                                          91     91     0%   1-164
src\core\data_synchronizer.py                                           96     96     0%   6-220
src\core\database.py                                                   139     98    29%   52-89, 95-125, 129-132, 137-140, 143, 149-170, 178-231, 238-248, 258-273, 280-284, 291-323
src\core\excel_importer.py                                             530    530     0%   6-971
src\core\license_updater.py                                            155    155     0%   6-324
src\core\license_validator.py                                          173    173     0%   6-332
src\core\lyra_client.py                                                129    129     0%   6-268
src\core\lyra_sentinel.py                                               32     32     0%   6-52
src\core\notification_manager.py                                        77     77     0%   6-125
src\core\secrets_manager.py                                             75     47    37%   29-58, 63, 68, 73, 78, 83-89, 94-97, 102-105, 110-113, 118-124
src\core\stats_manager.py                                               48     48     0%   6-78
src\core\telegram_bridge.py                                            274    274     0%   1-388
src\core\telegram_manager.py                                           475    475     0%   1-1026
src\core\time_manager.py                                                19     19     0%   6-56
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      4     0%   6-9
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18     18     0%   5-49
src\gui\contabilita_kpi_panel.py                                       375    375     0%   8-898
src\gui\contabilita_panel.py                                           244    244     0%   6-365
src\gui\dashboard_panel.py                                             120    120     0%   7-324
src\gui\formatters.py                                                   27     27     0%   1-43
src\gui\help_panel.py                                                  105    105     0%   6-425
src\gui\lyra_panel.py                                                  330    330     0%   1-667
src\gui\main_window.py                                                 232    232     0%   7-420
src\gui\notifications_panel.py                                         194    194     0%   6-439
src\gui\panels.py                                                      975    975     0%   6-1794
src\gui\scarico_ore_components.py                                      526    526     0%   1-919
src\gui\scarico_ore_panel.py                                           286    286     0%   7-637
src\gui\settings_panel.py                                             1155   1155     0%   7-2082
src\gui\styles.py                                                       58     58     0%   6-108
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12     12     0%   6-24
src\gui\widgets\automazioni_widget.py                                   30     30     0%   1-55
src\gui\widgets\bot_parameters.py                                      112    112     0%   6-192
src\gui\widgets\calendar_date_edit.py                                   10     10     0%   6-22
src\gui\widgets\data_table.py                                          106    106     0%   5-249
src\gui\widgets\database_widget.py                                      17     17     0%   1-28
src\gui\widgets\excel_table.py                                         313    313     0%   6-522
src\gui\widgets\info_widgets.py                                         91     91     0%   6-144
src\gui\widgets\modern_button.py                                        62     62     0%   5-140
src\gui\widgets\notification_item.py                                    61     61     0%   1-121
src\gui\widgets\sidebar_button.py                                       19     19     0%   1-42
src\gui\widgets\sidebar_widget.py                                       75     75     0%   1-137
src\gui\widgets\status_card.py                                          68     68     0%   5-120
src\gui\widgets\status_indicator.py                                     42     42     0%   6-60
src\gui\widgets\timeline_widget.py                                     226    226     0%   6-354
src\gui\widgets\toast.py                                                85     85     0%   5-192
src\gui\widgets\update_banner.py                                        29     29     0%   1-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         64     64     0%   6-86
src\utils\helpers.py                                                    79     54    32%   19-29, 34-38, 54-76, 89-91, 96, 123-124, 132, 145-159, 173-175, 190-197, 212, 234
src\utils\log_humanizer.py                                              27     27     0%   6-96
src\utils\parsing.py                                                    48     48     0%   6-147
src\utils\printing.py                                                   82     68    17%   17-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33     33     0%   6-60
src\utils\secure_logger.py                                              22     10    55%   39-46, 49-52
src\utils\security.py                                                   85     85     0%   6-146
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                11697  11090     5%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_scarico_ts_bot_hardened.py::TestScaricoTSBotHardened::test_process_downloaded_files_vba_style_loop
1 failed in 8.57s

```
</details>

---
### `tests/unit/test_scarico_ts_bot_hardened.py::TestScaricoTSBotHardened::test_setup_filters_js_injection`
**Error:** `FAILED tests/unit/test_scarico_ts_bot_hardened.py::TestScaricoTSBotHardened::test_setup_filters_js_injection`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________ TestScaricoTSBotHardened.test_setup_filters_js_injection ___________
tests\unit\test_scarico_ts_bot_hardened.py:98: in test_setup_filters_js_injection
    assert res is True
E   assert False is True
---------------------------- Captured stdout call -----------------------------
[Scarico TS] \u274c Errore nell'impostazione dei filtri: move_to requires a WebElement
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      7    63%   87, 100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281    208    26%   60, 65, 69, 73-75, 83, 85, 92, 94-104, 107, 110, 113, 116-117, 121, 124-155, 158-246, 250-284, 288-318, 322-324, 328-332, 336-338, 342, 346-357, 362, 366, 370-378, 382-390, 393-405, 408-413, 417
src\bots\base\login_page.py                                             95     79    17%   34-37, 45-61, 65-95, 99-113, 117-123, 130-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     28    38%   17, 21, 26, 47, 51, 55-67, 71-91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     46    23%   20-22, 25-34, 37-46, 49-69, 72-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62     43    31%   18, 22, 26, 33, 37, 46-49, 55-62, 65-107
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210    185    12%   28-31, 34, 37-44, 47-80, 83-103, 106-146, 150-163, 174-285, 289-310, 319-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228    145    36%   37, 41, 45, 56, 77, 82, 86-90, 97-199, 203-233, 238, 252-271, 285, 305-306, 319-320, 324-327, 335, 379-383, 394-396, 399-400, 405-410, 416-471
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     52    28%   22, 26, 30, 34, 39-43, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    148    13%   31-34, 37, 41-59, 63-83, 87-154, 158-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170    150    12%   33-34, 38-61, 65-66, 73-96, 102-132, 142-154, 166-233, 249-316, 320-339, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    323     8%   27-51, 55-62, 66-74, 78, 82, 86-111, 115-174, 178-183, 187-431, 434-460, 463-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60     60     0%   1-97
src\core\app_updater.py                                                 38     38     0%   6-80
src\core\audit_manager.py                                              156    156     0%   6-306
src\core\backup_manager.py                                             119    119     0%   6-219
src\core\config_manager.py                                             180    151    16%   55, 64-139, 148-149, 160-233, 238-239, 244-246, 251, 256-271, 276-289, 294-304, 309-313, 318-320, 325-330, 335
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107    107     0%   6-229
src\core\contabilita_queries.py                                         87     87     0%   6-122
src\core\contabilita_search.py                                          85     85     0%   6-181
src\core\contabilita_stats.py                                           57     57     0%   6-92
src\core\contabilita_worker.py                                          91     91     0%   1-164
src\core\data_synchronizer.py                                           96     96     0%   6-220
src\core\database.py                                                   139     98    29%   52-89, 95-125, 129-132, 137-140, 143, 149-170, 178-231, 238-248, 258-273, 280-284, 291-323
src\core\excel_importer.py                                             530    530     0%   6-971
src\core\license_updater.py                                            155    155     0%   6-324
src\core\license_validator.py                                          173    173     0%   6-332
src\core\lyra_client.py                                                129    129     0%   6-268
src\core\lyra_sentinel.py                                               32     32     0%   6-52
src\core\notification_manager.py                                        77     77     0%   6-125
src\core\secrets_manager.py                                             75     47    37%   29-58, 63, 68, 73, 78, 83-89, 94-97, 102-105, 110-113, 118-124
src\core\stats_manager.py                                               48     48     0%   6-78
src\core\telegram_bridge.py                                            274    274     0%   1-388
src\core\telegram_manager.py                                           475    475     0%   1-1026
src\core\time_manager.py                                                19     19     0%   6-56
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      4     0%   6-9
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18     18     0%   5-49
src\gui\contabilita_kpi_panel.py                                       375    375     0%   8-898
src\gui\contabilita_panel.py                                           244    244     0%   6-365
src\gui\dashboard_panel.py                                             120    120     0%   7-324
src\gui\formatters.py                                                   27     27     0%   1-43
src\gui\help_panel.py                                                  105    105     0%   6-425
src\gui\lyra_panel.py                                                  330    330     0%   1-667
src\gui\main_window.py                                                 232    232     0%   7-420
src\gui\notifications_panel.py                                         194    194     0%   6-439
src\gui\panels.py                                                      975    975     0%   6-1794
src\gui\scarico_ore_components.py                                      526    526     0%   1-919
src\gui\scarico_ore_panel.py                                           286    286     0%   7-637
src\gui\settings_panel.py                                             1155   1155     0%   7-2082
src\gui\styles.py                                                       58     58     0%   6-108
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12     12     0%   6-24
src\gui\widgets\automazioni_widget.py                                   30     30     0%   1-55
src\gui\widgets\bot_parameters.py                                      112    112     0%   6-192
src\gui\widgets\calendar_date_edit.py                                   10     10     0%   6-22
src\gui\widgets\data_table.py                                          106    106     0%   5-249
src\gui\widgets\database_widget.py                                      17     17     0%   1-28
src\gui\widgets\excel_table.py                                         313    313     0%   6-522
src\gui\widgets\info_widgets.py                                         91     91     0%   6-144
src\gui\widgets\modern_button.py                                        62     62     0%   5-140
src\gui\widgets\notification_item.py                                    61     61     0%   1-121
src\gui\widgets\sidebar_button.py                                       19     19     0%   1-42
src\gui\widgets\sidebar_widget.py                                       75     75     0%   1-137
src\gui\widgets\status_card.py                                          68     68     0%   5-120
src\gui\widgets\status_indicator.py                                     42     42     0%   6-60
src\gui\widgets\timeline_widget.py                                     226    226     0%   6-354
src\gui\widgets\toast.py                                                85     85     0%   5-192
src\gui\widgets\update_banner.py                                        29     29     0%   1-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         64     64     0%   6-86
src\utils\helpers.py                                                    79     54    32%   19-29, 34-38, 54-76, 89-91, 96, 123-124, 132, 145-159, 173-175, 190-197, 212, 234
src\utils\log_humanizer.py                                              27     27     0%   6-96
src\utils\parsing.py                                                    48     48     0%   6-147
src\utils\printing.py                                                   82     68    17%   17-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33     33     0%   6-60
src\utils\secure_logger.py                                              22     10    55%   39-46, 49-52
src\utils\security.py                                                   85     85     0%   6-146
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                11697  11090     5%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_scarico_ts_bot_hardened.py::TestScaricoTSBotHardened::test_setup_filters_js_injection
1 failed in 8.29s

```
</details>

---
