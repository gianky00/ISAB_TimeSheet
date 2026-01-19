# 📊 Test Execution Report

**Date:** 2026-01-19 00:33:58
**Duration:** 10.07s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 474 |
| ✅ Passed | 467 |
| ❌ Failed | 4 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data`
**Error:** `FAILED tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_____________________ test_import_contabilita_valid_data ______________________
tests\unit\test_excel_importer_coverage.py:65: in test_import_contabilita_valid_data
    assert "01/01/2025" in row_str
E   assert '01/01/2025' in "(2025, Timestamp('2025-01-01 00:00:00'), 'Gennaio', '100', 1000, 'Manutenzione', 'TCL1', '123456', '', '', '', '', '', '', '')"
============================== warnings summary ===============================
tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
  C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\src\core\excel_importer.py:301: SettingWithCopyWarning:
  A value is trying to be set on a copy of a slice from a DataFrame

  See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    df.dropna(how="all", inplace=True)

tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
  C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\src\core\excel_importer.py:306: SettingWithCopyWarning:
  A value is trying to be set on a copy of a slice from a DataFrame.
  Try using .loc[row_indexer,col_indexer] = value instead

  See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    df["year"] = year

tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
  C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\src\core\excel_importer.py:213: SettingWithCopyWarning:
  A value is trying to be set on a copy of a slice from a DataFrame

  See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    df.rename(columns=rename_map, inplace=True)

tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
  C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\src\core\excel_importer.py:351: SettingWithCopyWarning:
  A value is trying to be set on a copy of a slice from a DataFrame.
  Try using .loc[row_indexer,col_indexer] = value instead

  See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    df[db_col] = ""

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
src\bots\__init__.py                       20     20     0%   6-133
src\bots\base\__init__.py                   2      2     0%   5-7
src\bots\base\base_bot.py                 270    270     0%   6-477
src\bots\base\login_page.py                94     94     0%   6-179
src\core\__init__.py                        2      0   100%
src\core\app_initializer.py                72     72     0%   1-124
src\core\app_updater.py                    46     46     0%   6-87
src\core\audit_manager.py                 164    164     0%   6-325
src\core\backup_manager.py                140    140     0%   6-253
src\core\config_manager.py                177    119    33%   64, 74, 88-89, 106-125, 133-147, 156-157, 165-177, 182-183, 188-211, 216-228, 233-234, 239-241, 246, 251-266, 271-284, 289-299, 304-308, 313-315, 320-325, 330
src\core\constants.py                      70     70     0%   6-102
src\core\contabilita_manager.py           107     60    44%   28, 33, 38, 47-59, 76-136, 145-154, 163-172, 181-190, 195, 200, 205, 210, 215, 220, 229, 239, 244
src\core\contabilita_queries.py            87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py             91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py              61     42    31%   29-49, 54-82, 87-105
src\core\contabilita_worker.py             80     80     0%   1-174
src\core\data_synchronizer.py             104     79    24%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 175, 183, 194-210
src\core\database.py                      152     54    64%   56, 80-83, 110-112, 118-129, 135-141, 144-147, 150, 156-177, 265-284, 289-293, 303-334
src\core\excel_importer.py                613    394    36%   23-24, 31-33, 143-144, 157-158, 169, 189, 209, 211, 249, 263-265, 279, 287, 304, 342-344, 359-402, 407-419, 424-436, 441-479, 485-507, 519-539, 553, 556, 560, 572-592, 601-620, 625-635, 640-660, 666-683, 692-710, 715-735, 742-769, 775-798, 816-824, 829-842, 847-850, 856-880, 889-907, 912-916, 923-926, 931-947, 954-978, 983-987, 992-998, 1004-1031, 1036-1056, 1061-1063, 1068-1079, 1084-1104
src\core\license_updater.py               159    159     0%   6-299
src\core\license_validator.py             197    197     0%   6-380
src\core\lyra_client.py                   128    128     0%   6-259
src\core\lyra_sentinel.py                  32      9    72%   38-39, 45-51
src\core\notification_manager.py           77     37    52%   38-45, 52-53, 79-81, 93-100, 104-113, 117-122, 126-129
src\core\secrets_manager.py               102     65    36%   27-41, 45-51, 55-69, 73-75, 79-85, 90, 95, 100, 105, 110-116, 121-124, 129-132, 137-140, 145-151
src\core\stats_manager.py                  48     48     0%   6-84
src\core\telegram_bridge.py               342    342     0%   1-530
src\core\telegram_manager.py              545    545     0%   1-1141
src\core\time_manager.py                   19     19     0%   6-56
src\core\timesheet_processor.py           104    104     0%   6-175
src\core\version.py                         4      4     0%   6-9
src\gui\__init__.py                         0      0   100%
src\gui\accessibility.py                   18     18     0%   5-49
src\gui\contabilita_kpi_panel.py          380    380     0%   8-922
src\gui\contabilita_panel.py              247    247     0%   6-424
src\gui\dashboard_panel.py                177    177     0%   1-407
src\gui\formatters.py                      93     93     0%   1-168
src\gui\help_panel.py                     120    120     0%   6-370
src\gui\lyra_panel.py                     397    397     0%   1-809
src\gui\main_window.py                    372    372     0%   7-770
src\gui\notifications_panel.py            216    216     0%   6-473
src\gui\panels.py                        1308   1308     0%   6-2451
src\gui\scarico_ore_components.py         539    539     0%   1-1030
src\gui\scarico_ore_panel.py              269    269     0%   7-461
src\gui\settings_panel.py                1197   1197     0%   7-2181
src\gui\styles.py                          58     58     0%   6-109
src\gui\toast.py                           45     45     0%   6-90
src\gui\widgets\__init__.py                12     12     0%   6-24
src\gui\widgets\automazioni_widget.py      42     42     0%   1-101
src\gui\widgets\bot_parameters.py         112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py      11     11     0%   6-23
src\gui\widgets\data_table.py             108    108     0%   5-219
src\gui\widgets\excel_table.py            324    324     0%   6-529
src\gui\widgets\footer_stats.py           440    440     0%   7-768
src\gui\widgets\info_widgets.py            95     95     0%   6-174
src\gui\widgets\modern_button.py           62     62     0%   5-152
src\gui\widgets\notification_item.py       70     70     0%   1-139
src\gui\widgets\sidebar_button.py          41     41     0%   1-89
src\gui\widgets\sidebar_widget.py         175    175     0%   1-328
src\gui\widgets\status_card.py             57     57     0%   1-127
src\gui\widgets\status_indicator.py        42     42     0%   6-68
src\gui\widgets\timeline_widget.py        191    191     0%   6-328
src\gui\widgets\toast.py                   91     91     0%   5-239
src\gui\widgets\update_banner.py           35     35     0%   1-53
src\utils\__init__.py                       2      0   100%
src\utils\document_generator.py            13     13     0%   5-39
src\utils\document_processor.py            64     64     0%   6-86
src\utils\helpers.py                       94     75    20%   21-31, 36-40, 56-78, 91-93, 98, 125-126, 134, 147-161, 175-177, 192-199, 213-238, 246-264
src\utils\log_humanizer.py                 27     27     0%   6-101
src\utils\parsing.py                       53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                      82     82     0%   1-144
src\utils\resource_manager.py              33     33     0%   6-60
src\utils\secure_logger.py                 22     22     0%   5-68
src\utils\security.py                      85     85     0%   6-147
src\utils\validators.py                    73     73     0%   5-208
---------------------------------------------------------------------
TOTAL                                   12001  11369     5%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_excel_importer_coverage.py::test_import_contabilita_valid_data
1 failed, 10 warnings in 3.19s

```
</details>

---
### `tests/unit/test_gui_contabilita_logic.py::TestContabilitaTableLogic::test_contabilita_year_tab_totals`
**Error:** `FAILED tests/unit/test_gui_contabilita_logic.py::TestContabilitaTableLogic::test_contabilita_year_tab_totals`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestContabilitaTableLogic.test_contabilita_year_tab_totals __________
tests\unit\test_gui_contabilita_logic.py:57: in test_contabilita_year_tab_totals
    assert "1000" in str(total_val)
E   AssertionError: assert '1000' in '1.000'
E    +  where '1.000' = str('1.000')
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                             Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------
src\bots\__init__.py                                20     20     0%   6-133
src\bots\base\__init__.py                            2      2     0%   5-7
src\bots\base\base_bot.py                          270    270     0%   6-477
src\bots\base\login_page.py                         94     94     0%   6-179
src\core\__init__.py                                 2      0   100%
src\core\app_initializer.py                         72     72     0%   1-124
src\core\app_updater.py                             46     46     0%   6-87
src\core\audit_manager.py                          164    164     0%   6-325
src\core\backup_manager.py                         140    140     0%   6-253
src\core\config_manager.py                         177    142    20%   54, 62-77, 82-92, 97-98, 103-125, 130-147, 156-157, 165-177, 182-183, 188-211, 216-228, 233-234, 239-241, 246, 251-266, 271-284, 289-299, 304-308, 313-315, 320-325, 330
src\core\constants.py                               70      0   100%
src\core\contabilita_manager.py                    107     60    44%   28, 33, 38, 47-59, 76-136, 145-154, 163-172, 181-190, 195, 200, 205, 210, 215, 220, 229, 239, 244
src\core\contabilita_queries.py                     87     16    82%   20, 27-28, 36, 52, 71-72, 80, 87-88, 96, 103-104, 112, 119-120
src\core\contabilita_search.py                      91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                       61     42    31%   29-49, 54-82, 87-105
src\core\contabilita_worker.py                      80     64    20%   22-27, 31-60, 64-75, 79-89, 94-102, 112-123, 133-145, 150-163, 168-174
src\core\data_synchronizer.py                      104     79    24%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 175, 183, 194-210
src\core\database.py                               152     89    41%   67-69, 77, 80-83, 97-129, 135-141, 144-147, 150, 156-177, 185-246, 251-257, 265-284, 289-293, 303-334, 339-379
src\core\excel_importer.py                         613    506    17%   23-24, 31-33, 130-148, 153-158, 163-170, 175-189, 194-214, 225-265, 272-289, 294-344, 349-352, 359-402, 407-419, 424-436, 441-479, 485-507, 519-539, 549-565, 572-592, 601-620, 625-635, 640-660, 666-683, 692-710, 715-735, 742-769, 775-798, 816-824, 829-842, 847-850, 856-880, 889-907, 912-916, 923-926, 931-947, 954-978, 983-987, 992-998, 1004-1031, 1036-1056, 1061-1063, 1068-1079, 1084-1104
src\core\license_updater.py                        159    159     0%   6-299
src\core\license_validator.py                      197    197     0%   6-380
src\core\lyra_client.py                            128    128     0%   6-259
src\core\lyra_sentinel.py                           32     32     0%   6-53
src\core\notification_manager.py                    77     55    29%   25-27, 30-32, 36-45, 49-53, 60-75, 79-81, 85, 93-100, 104-113, 117-122, 126-129
src\core\secrets_manager.py                        102     65    36%   27-41, 45-51, 55-69, 73-75, 79-85, 90, 95, 100, 105, 110-116, 121-124, 129-132, 137-140, 145-151
src\core\stats_manager.py                           48     48     0%   6-84
src\core\telegram_bridge.py                        342    342     0%   1-530
src\core\telegram_manager.py                       545    545     0%   1-1141
src\core\time_manager.py                            19     19     0%   6-56
src\core\timesheet_processor.py                    104    104     0%   6-175
src\core\version.py                                  4      4     0%   6-9
src\gui\__init__.py                                  0      0   100%
src\gui\accessibility.py                            18     18     0%   5-49
src\gui\contabilita_kpi_panel.py                   380    354     7%   47-58, 61-252, 262-305, 309-323, 327-345, 349, 353-475, 479-566, 569-639, 643-739, 742-809, 813-922
src\gui\contabilita_panel.py                       247    111    55%   51-55, 167-174, 178, 222, 228-233, 254-258, 262-265, 271-273, 280-282, 289, 299-302, 306-310, 314-318, 324-344, 347-348, 351-355, 360-381, 384-386, 389-406, 410, 413-424
src\gui\dashboard_panel.py                         177    177     0%   1-407
src\gui\design\colors.py                            27      0   100%
src\gui\design\spacing.py                           25      0   100%
src\gui\formatters.py                               93     30    68%   12, 20-28, 39, 48, 51, 68-69, 105, 115, 123-134, 155-161, 165-166
src\gui\help_panel.py                              120    120     0%   6-370
src\gui\lyra_panel.py                              397    397     0%   1-809
src\gui\main_window.py                             372    372     0%   7-770
src\gui\notifications_panel.py                     216    216     0%   6-473
src\gui\panels.py                                 1308   1308     0%   6-2451
src\gui\scarico_ore_components.py                  539    539     0%   1-1030
src\gui\scarico_ore_panel.py                       269    269     0%   7-461
src\gui\settings_panel.py                         1197   1197     0%   7-2181
src\gui\styles.py                                   58     58     0%   6-109
src\gui\toast.py                                    45     45     0%   6-90
src\gui\widgets\__init__.py                         12      0   100%
src\gui\widgets\automazioni_widget.py               42     42     0%   1-101
src\gui\widgets\bot_parameters.py                  112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py               11      6    45%   16-23
src\gui\widgets\contabilita\attivita_tab.py        192    167    13%   51-53, 57-121, 124, 127-140, 143-156, 159-169, 172-177, 180-198, 201-257, 260-264, 267-282, 285-290
src\gui\widgets\contabilita\certificati_tab.py     113     91    19%   55-57, 60-101, 105, 109-127, 131-144, 147-154, 157-167, 171-276
src\gui\widgets\contabilita\giornaliere_tab.py     165     50    70%   96, 132, 149, 176, 186-187, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py              33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py             48      4    92%   87, 108-109, 113
src\gui\widgets\data_table.py                      108     86    20%   46-50, 53-127, 131, 135-136, 139-164, 167-173, 177-185, 188-190, 194-211, 215, 219
src\gui\widgets\excel_table.py                     324    283    13%   49-62, 66-73, 77-94, 98-118, 121-122, 125-126, 130-140, 144-168, 172-198, 202-221, 225-245, 249-260, 263-268, 271-275, 278-282, 291-293, 296-319, 322-381, 384-387, 390-396, 399-431, 434-437, 440-442, 445, 449-466, 475-500, 505-529
src\gui\widgets\footer_stats.py                    440    440     0%   7-768
src\gui\widgets\info_widgets.py                     95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                    62     13    79%   52-54, 71-72, 78-81, 85-88, 150
src\gui\widgets\notification_item.py                70     59    16%   20-23, 26-130, 134-136, 139
src\gui\widgets\sidebar_button.py                   41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                  175    175     0%   1-328
src\gui\widgets\status_card.py                      57     46    19%   19-90, 94-97, 106-122, 126-127
src\gui\widgets\status_indicator.py                 42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                 191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 274-290, 293, 296, 301-328
src\gui\widgets\toast.py                            91     64    30%   55-68, 72-111, 116-130, 140-145, 160-162, 181-218, 224, 229, 234, 239
src\gui\widgets\update_banner.py                    35     35     0%   1-53
src\utils\__init__.py                                2      0   100%
src\utils\document_generator.py                     13     13     0%   5-39
src\utils\document_processor.py                     64     64     0%   6-86
src\utils\helpers.py                                94     63    33%   23, 36-40, 56-78, 91-93, 98, 125-126, 134, 147-161, 175-177, 192-199, 213-238, 247, 253-256
src\utils\log_humanizer.py                          27     18    33%   61-69, 74-93, 98-101
src\utils\parsing.py                                53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                               82     82     0%   1-144
src\utils\resource_manager.py                       33     33     0%   6-60
src\utils\secure_logger.py                          22     22     0%   5-68
src\utils\security.py                               85     85     0%   6-147
src\utils\validators.py                             73     73     0%   5-208
------------------------------------------------------------------------------
TOTAL                                            12604  11264    11%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_gui_contabilita_logic.py::TestContabilitaTableLogic::test_contabilita_year_tab_totals
1 failed in 3.47s

```
</details>

---
### `tests/unit/test_gui_contabilita_logic.py::TestContabilitaTableLogic::test_giornaliere_year_tab_format`
**Error:** `FAILED tests/unit/test_gui_contabilita_logic.py::TestContabilitaTableLogic::test_giornaliere_year_tab_format`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestContabilitaTableLogic.test_giornaliere_year_tab_format __________
tests\unit\test_gui_contabilita_logic.py:87: in test_giornaliere_year_tab_format
    assert model.data(model.index(0, 9)) == "8,5"
E   AssertionError: assert '8,50' == '8,5'
E
E     - 8,5
E     + 8,50
E     ?    +
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                             Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------
src\bots\__init__.py                                20     20     0%   6-133
src\bots\base\__init__.py                            2      2     0%   5-7
src\bots\base\base_bot.py                          270    270     0%   6-477
src\bots\base\login_page.py                         94     94     0%   6-179
src\core\__init__.py                                 2      0   100%
src\core\app_initializer.py                         72     72     0%   1-124
src\core\app_updater.py                             46     46     0%   6-87
src\core\audit_manager.py                          164    164     0%   6-325
src\core\backup_manager.py                         140    140     0%   6-253
src\core\config_manager.py                         177    142    20%   54, 62-77, 82-92, 97-98, 103-125, 130-147, 156-157, 165-177, 182-183, 188-211, 216-228, 233-234, 239-241, 246, 251-266, 271-284, 289-299, 304-308, 313-315, 320-325, 330
src\core\constants.py                               70      0   100%
src\core\contabilita_manager.py                    107     60    44%   28, 33, 38, 47-59, 76-136, 145-154, 163-172, 181-190, 195, 200, 205, 210, 215, 220, 229, 239, 244
src\core\contabilita_queries.py                     87     16    82%   20, 27-28, 36, 52, 71-72, 80, 87-88, 96, 103-104, 112, 119-120
src\core\contabilita_search.py                      91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                       61     42    31%   29-49, 54-82, 87-105
src\core\contabilita_worker.py                      80     64    20%   22-27, 31-60, 64-75, 79-89, 94-102, 112-123, 133-145, 150-163, 168-174
src\core\data_synchronizer.py                      104     79    24%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 175, 183, 194-210
src\core\database.py                               152     89    41%   67-69, 77, 80-83, 97-129, 135-141, 144-147, 150, 156-177, 185-246, 251-257, 265-284, 289-293, 303-334, 339-379
src\core\excel_importer.py                         613    506    17%   23-24, 31-33, 130-148, 153-158, 163-170, 175-189, 194-214, 225-265, 272-289, 294-344, 349-352, 359-402, 407-419, 424-436, 441-479, 485-507, 519-539, 549-565, 572-592, 601-620, 625-635, 640-660, 666-683, 692-710, 715-735, 742-769, 775-798, 816-824, 829-842, 847-850, 856-880, 889-907, 912-916, 923-926, 931-947, 954-978, 983-987, 992-998, 1004-1031, 1036-1056, 1061-1063, 1068-1079, 1084-1104
src\core\license_updater.py                        159    159     0%   6-299
src\core\license_validator.py                      197    197     0%   6-380
src\core\lyra_client.py                            128    128     0%   6-259
src\core\lyra_sentinel.py                           32     32     0%   6-53
src\core\notification_manager.py                    77     55    29%   25-27, 30-32, 36-45, 49-53, 60-75, 79-81, 85, 93-100, 104-113, 117-122, 126-129
src\core\secrets_manager.py                        102     65    36%   27-41, 45-51, 55-69, 73-75, 79-85, 90, 95, 100, 105, 110-116, 121-124, 129-132, 137-140, 145-151
src\core\stats_manager.py                           48     48     0%   6-84
src\core\telegram_bridge.py                        342    342     0%   1-530
src\core\telegram_manager.py                       545    545     0%   1-1141
src\core\time_manager.py                            19     19     0%   6-56
src\core\timesheet_processor.py                    104    104     0%   6-175
src\core\version.py                                  4      4     0%   6-9
src\gui\__init__.py                                  0      0   100%
src\gui\accessibility.py                            18     18     0%   5-49
src\gui\contabilita_kpi_panel.py                   380    354     7%   47-58, 61-252, 262-305, 309-323, 327-345, 349, 353-475, 479-566, 569-639, 643-739, 742-809, 813-922
src\gui\contabilita_panel.py                       247    111    55%   51-55, 167-174, 178, 222, 228-233, 254-258, 262-265, 271-273, 280-282, 289, 299-302, 306-310, 314-318, 324-344, 347-348, 351-355, 360-381, 384-386, 389-406, 410, 413-424
src\gui\dashboard_panel.py                         177    177     0%   1-407
src\gui\design\colors.py                            27      0   100%
src\gui\design\spacing.py                           25      0   100%
src\gui\formatters.py                               93     30    68%   12, 20-28, 39, 48, 51, 68-69, 105, 115, 123-134, 155-161, 165-166
src\gui\help_panel.py                              120    120     0%   6-370
src\gui\lyra_panel.py                              397    397     0%   1-809
src\gui\main_window.py                             372    372     0%   7-770
src\gui\notifications_panel.py                     216    216     0%   6-473
src\gui\panels.py                                 1308   1308     0%   6-2451
src\gui\scarico_ore_components.py                  539    539     0%   1-1030
src\gui\scarico_ore_panel.py                       269    269     0%   7-461
src\gui\settings_panel.py                         1197   1197     0%   7-2181
src\gui\styles.py                                   58     58     0%   6-109
src\gui\toast.py                                    45     45     0%   6-90
src\gui\widgets\__init__.py                         12      0   100%
src\gui\widgets\automazioni_widget.py               42     42     0%   1-101
src\gui\widgets\bot_parameters.py                  112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py               11      6    45%   16-23
src\gui\widgets\contabilita\attivita_tab.py        192    167    13%   51-53, 57-121, 124, 127-140, 143-156, 159-169, 172-177, 180-198, 201-257, 260-264, 267-282, 285-290
src\gui\widgets\contabilita\certificati_tab.py     113     91    19%   55-57, 60-101, 105, 109-127, 131-144, 147-154, 157-167, 171-276
src\gui\widgets\contabilita\giornaliere_tab.py     165     50    70%   96, 132, 149, 176, 186-187, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py              33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py             48      4    92%   87, 108-109, 113
src\gui\widgets\data_table.py                      108     86    20%   46-50, 53-127, 131, 135-136, 139-164, 167-173, 177-185, 188-190, 194-211, 215, 219
src\gui\widgets\excel_table.py                     324    283    13%   49-62, 66-73, 77-94, 98-118, 121-122, 125-126, 130-140, 144-168, 172-198, 202-221, 225-245, 249-260, 263-268, 271-275, 278-282, 291-293, 296-319, 322-381, 384-387, 390-396, 399-431, 434-437, 440-442, 445, 449-466, 475-500, 505-529
src\gui\widgets\footer_stats.py                    440    440     0%   7-768
src\gui\widgets\info_widgets.py                     95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                    62     13    79%   52-54, 71-72, 78-81, 85-88, 150
src\gui\widgets\notification_item.py                70     59    16%   20-23, 26-130, 134-136, 139
src\gui\widgets\sidebar_button.py                   41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                  175    175     0%   1-328
src\gui\widgets\status_card.py                      57     46    19%   19-90, 94-97, 106-122, 126-127
src\gui\widgets\status_indicator.py                 42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                 191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 274-290, 293, 296, 301-328
src\gui\widgets\toast.py                            91     64    30%   55-68, 72-111, 116-130, 140-145, 160-162, 181-218, 224, 229, 234, 239
src\gui\widgets\update_banner.py                    35     35     0%   1-53
src\utils\__init__.py                                2      0   100%
src\utils\document_generator.py                     13     13     0%   5-39
src\utils\document_processor.py                     64     64     0%   6-86
src\utils\helpers.py                                94     63    33%   23, 36-40, 56-78, 91-93, 98, 125-126, 134, 147-161, 175-177, 192-199, 213-238, 247, 253-256
src\utils\log_humanizer.py                          27     18    33%   61-69, 74-93, 98-101
src\utils\parsing.py                                53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                               82     82     0%   1-144
src\utils\resource_manager.py                       33     33     0%   6-60
src\utils\secure_logger.py                          22     22     0%   5-68
src\utils\security.py                               85     85     0%   6-147
src\utils\validators.py                             73     73     0%   5-208
------------------------------------------------------------------------------
TOTAL                                            12604  11264    11%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_gui_contabilita_logic.py::TestContabilitaTableLogic::test_giornaliere_year_tab_format
1 failed in 3.63s

```
</details>

---
### `tests/unit/test_gui_headless_hardened.py::TestGUIHeadlessHardened::test_dashboard_greeting_logic`
**Error:** `FAILED tests/unit/test_gui_headless_hardened.py::TestGUIHeadlessHardened::test_dashboard_greeting_logic`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________ TestGUIHeadlessHardened.test_dashboard_greeting_logic ____________
tests\unit\test_gui_headless_hardened.py:59: in test_dashboard_greeting_logic
    mock_datetime = mocker.patch("src.gui.dashboard_panel.datetime")
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
E   AttributeError: <module 'src.gui.dashboard_panel' from 'C:\\Users\\gianc\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\gui\\dashboard_panel.py'> does not have the attribute 'datetime'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              270    215    20%   49-65, 71, 77, 82, 87-89, 101-105, 114-128, 132, 136, 140, 144-145, 149-150, 154-168, 172-217, 222-239, 243-245, 254-259, 263-277, 288-322, 326-351, 355-357, 361-365, 369-371, 375, 379-396, 401, 405, 409-419, 423-433, 444-456, 460-465, 477
src\bots\base\login_page.py                                             94     78    17%   34-37, 45-61, 65-95, 99-115, 119-125, 132-179
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     46    23%   28-30, 34-43, 47-56, 67-87, 98-130
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          65     46    29%   21, 26, 31, 38, 42, 51-54, 60-67, 71-118
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     216    188    13%   40-43, 47, 51-58, 69-102, 113-133, 137-177, 181-194, 218-329, 333-354, 364-382, 386-398, 402-417, 421-434
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         239    211    12%   30-33, 37, 41-46, 58-89, 100-106, 111-118, 122-157, 163-206, 210-220, 229-260, 264-271, 275-298, 302-314, 318-334, 338-360, 364-392, 396-403
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           221    186    16%   38, 43, 48, 55, 59, 71-74, 78-80, 84-99, 103-120, 124-140, 146-169, 173-209, 213-222, 226-257, 261-300, 306-328, 332-341, 347-366, 372-394, 398-413
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    148    13%   31-34, 37, 41-59, 63-83, 87-154, 158-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       171    147    14%   33-34, 38-61, 65-66, 73-96, 102-132, 142-154, 164-172, 177-194, 197-205, 210-224, 231-257, 260-284, 288-307, 316-317
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           403    358    11%   25, 30, 35, 40, 45, 56-78, 82-89, 93-103, 107-132, 136-199, 203-208, 212-239, 243-272, 276-284, 288-319, 323-355, 359-371, 375-400, 404-420, 424-434, 438-459, 463-477, 484-527, 530-559, 562-578
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             72     72     0%   1-124
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              164     83    49%   96-97, 113-123, 127-139, 156-157, 219-220, 234-249, 255-263, 273-296, 300-312, 316-325
src\core\backup_manager.py                                             140     69    51%   41, 44, 47, 58-60, 67, 70, 83, 92, 94, 109-111, 116, 121-126, 135-188, 199-211, 219, 225-227, 232-253
src\core\config_manager.py                                             177     96    46%   64, 74, 86-92, 106-125, 133-147, 156-157, 176-177, 191-211, 225-228, 251-266, 271-284, 289-299, 308, 313-315, 320-325, 330
src\core\constants.py                                                   70      0   100%
src\core\contabilita_manager.py                                        107    107     0%   6-244
src\core\contabilita_queries.py                                         87     18    79%   20, 27-28, 36, 43-44, 52, 71-72, 80, 87-88, 96, 103-104, 112, 119-120
src\core\contabilita_search.py                                          91     91     0%   6-178
src\core\contabilita_stats.py                                           61     61     0%   6-105
src\core\contabilita_worker.py                                          80     80     0%   1-174
src\core\data_synchronizer.py                                          104    104     0%   6-210
src\core\database.py                                                   152     90    41%   67-69, 76-77, 80-83, 97-129, 135-141, 144-147, 150, 156-177, 185-246, 251-257, 265-284, 289-293, 303-334, 339-379
src\core\excel_importer.py                                             613    506    17%   23-24, 31-33, 130-148, 153-158, 163-170, 175-189, 194-214, 225-265, 272-289, 294-344, 349-352, 359-402, 407-419, 424-436, 441-479, 485-507, 519-539, 549-565, 572-592, 601-620, 625-635, 640-660, 666-683, 692-710, 715-735, 742-769, 775-798, 816-824, 829-842, 847-850, 856-880, 889-907, 912-916, 923-926, 931-947, 954-978, 983-987, 992-998, 1004-1031, 1036-1056, 1061-1063, 1068-1079, 1084-1104
src\core\license_updater.py                                            159    159     0%   6-299
src\core\license_validator.py                                          197    197     0%   6-380
src\core\lyra_client.py                                                128    128     0%   6-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        77     55    29%   25-27, 30-32, 36-45, 49-53, 60-75, 79-81, 85, 93-100, 104-113, 117-122, 126-129
src\core\secrets_manager.py                                            102     60    41%   27-41, 45-51, 55-69, 73-75, 79-85, 90, 95, 100, 110-116, 123-124, 131-132, 137-140, 145-151
src\core\stats_manager.py                                               48     17    65%   39-46, 49, 62, 64, 72-80
src\core\telegram_bridge.py                                            342    342     0%   1-530
src\core\telegram_manager.py                                           545    545     0%   1-1141
src\core\time_manager.py                                                19     19     0%   6-56
src\core\timesheet_processor.py                                        104     83    20%   25-67, 72-82, 87-92, 99-109, 115-151, 156-166, 171-175
src\core\version.py                                                      4      4     0%   6-9
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18     18     0%   5-49
src\gui\contabilita_kpi_panel.py                                       380    380     0%   8-922
src\gui\contabilita_panel.py                                           247    247     0%   6-424
src\gui\dashboard_panel.py                                             177    153    14%   31-68, 72, 76-78, 82-87, 90-92, 95-98, 101-104, 111-156, 160-161, 165-172, 176-292, 298-401, 405-407
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   93     78    16%   11-28, 38-69, 74, 86-92, 96-99, 105, 108, 111, 114-134, 137-142, 145-147, 151-168
src\gui\help_panel.py                                                  120    120     0%   6-370
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\lyra_panel.py                                                  397    397     0%   1-809
src\gui\main_window.py                                                 372    372     0%   7-770
src\gui\notifications_panel.py                                         216    216     0%   6-473
src\gui\panels.py                                                     1308   1035    21%   83-87, 91-104, 116-120, 124-126, 242, 246, 254, 258-263, 267-270, 274-276, 295-298, 302-318, 322-326, 330-339, 349-354, 358-371, 375, 379-394, 401-404, 410-415, 421, 440-444, 489-491, 495, 499-512, 517, 532-537, 541-546, 560-562, 566-606, 613-621, 624-628, 632-669, 672-674, 678, 681-693, 696-708, 713-718, 722-728, 731-793, 800-808, 811-814, 818-855, 859-861, 864-872, 875-881, 884-894, 899-947, 970-974, 1027-1030, 1034-1041, 1045-1053, 1057-1058, 1074-1118, 1130-1138, 1141-1145, 1149-1254, 1257-1265, 1268-1271, 1274-1287, 1290-1301, 1304-1314, 1318-1326, 1331-1338, 1341-1362, 1366-1380, 1384-1404, 1408-1422, 1426-1435, 1439-1463, 1467-1469, 1473-1487, 1491-1493, 1504-1511, 1514-1543, 1546-1551, 1554-1557, 1562-1567, 1578-1585, 1588-1590, 1597-1598, 1601-1611, 1618-1663, 1666-1752, 1756-1768, 1771, 1775-1786, 1790-1820, 1824-1831, 1835-1848, 1859-1868, 1871-1875, 1879-1906, 1909-1911, 1915-1916, 1919-1942, 1946-1964, 1968-1973, 1977-2027, 2030-2032, 2039-2064, 2068-2139, 2142-2160, 2164-2192, 2195-2250, 2254-2257, 2261-2268, 2272-2274, 2278-2323, 2328-2347, 2351-2416, 2419-2451
src\gui\scarico_ore_components.py                                      539    539     0%   1-1030
src\gui\scarico_ore_panel.py                                           269    269     0%   7-461
src\gui\settings_panel.py                                             1197    384    68%   52-110, 113-124, 127, 134-192, 338-340, 381-382, 389-390, 1144-1157, 1163-1170, 1224-1226, 1337-1339, 1342-1349, 1352-1355, 1363-1365, 1374-1379, 1385-1416, 1541, 1551, 1555-1559, 1562-1573, 1576-1584, 1587-1598, 1601-1612, 1615-1626, 1653-1671, 1675-1680, 1683-1693, 1697-1737, 1743-1772, 1775-1781, 1794-1801, 1804-1812, 1815-1829, 1832-1843, 1846-1852, 1857-1858, 1862-1895, 1899-1907, 1910-1917, 1920-1927, 1931-1940, 1943-1950, 1953-1960, 1964-1969, 1972-1979, 1982-1989, 1993-1998, 2001-2008, 2011-2018, 2053, 2058, 2063, 2068, 2084, 2136, 2145, 2154-2161, 2164-2181
src\gui\styles.py                                                       58     58     0%   6-109
src\gui\toast.py                                                        45      4    91%   87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   42     42     0%   1-101
src\gui\widgets\bot_parameters.py                                      112     20    82%   87-91, 153, 172, 181-183, 201-208, 216-217
src\gui\widgets\calendar_date_edit.py                                   11      0   100%
src\gui\widgets\data_table.py                                          108     86    20%   46-50, 53-127, 131, 135-136, 139-164, 167-173, 177-185, 188-190, 194-211, 215, 219
src\gui\widgets\excel_table.py                                         324    223    31%   49-62, 66-73, 77-94, 98-118, 121-122, 125-126, 130-140, 144-168, 172-198, 202-221, 225-245, 249-260, 263-268, 271-275, 278-282, 322-381, 390-396, 403-427, 434-437, 440-442, 457, 486-492, 498-499, 505-529
src\gui\widgets\footer_stats.py                                        440    440     0%   7-768
src\gui\widgets\info_widgets.py                                         95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                                        62     11    82%   71-72, 78-81, 85-88, 150
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-130, 134-136, 139
src\gui\widgets\sidebar_button.py                                       41      7    83%   28-30, 35-37, 76
src\gui\widgets\sidebar_widget.py                                      175    175     0%   1-328
src\gui\widgets\status_card.py                                          57      7    88%   106-122, 126-127
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    128    33%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 191-205, 224-234, 237-252, 257-262, 265-269, 293, 296, 301-328
src\gui\widgets\toast.py                                                91     12    87%   188-199, 208, 224, 229, 234, 239
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         64     64     0%   6-86
src\utils\helpers.py                                                    94     62    34%   23, 36-40, 56-78, 91-93, 98, 125-126, 134, 147-161, 175-177, 192-199, 213-238, 253-256
src\utils\log_humanizer.py                                              27     18    33%   61-69, 74-93, 98-101
src\utils\parsing.py                                                    53     53     0%   6-119
src\utils\printing.py                                                   82     68    17%   17-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33     33     0%   6-60
src\utils\secure_logger.py                                              22     10    55%   44-51, 54-57
src\utils\security.py                                                   85     85     0%   6-147
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                14007  11037    21%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_gui_headless_hardened.py::TestGUIHeadlessHardened::test_dashboard_greeting_logic
1 failed in 3.19s

```
</details>

---
