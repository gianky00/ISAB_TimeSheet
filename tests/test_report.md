# 📊 Test Execution Report

**Date:** 2026-01-12 23:38:29
**Duration:** 2789.53s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 815 |
| ✅ Passed | 801 |
| ❌ Failed | 14 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_import_giornaliere_lookup_logic`
**Error:** `FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_import_giornaliere_lookup_logic`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
______ TestContabilitaManagerBoost.test_import_giornaliere_lookup_logic _______
tests\unit\test_contabilita_manager_boost.py:26: in test_import_giornaliere_lookup_logic
    manager.execute_query(db_path, query)
src\core\database.py:107: in execute_query
    cursor.execute(query, params)
E   sqlite3.OperationalError: no such table: contabilita
------------------------------ Captured log call ------------------------------
ERROR    src.core.database:database.py:78 Database Operational Error (contabilita.db): no such table: contabilita
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     85    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 328-332, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62     40    35%   33, 37, 46-49, 55-62, 65-107
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210    144    31%   37-44, 47-80, 83-103, 106-146, 150-163, 214, 237-243, 262-266, 277-285, 289-310, 319-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228    159    30%   56, 75-90, 97-199, 203-233, 238, 273-275, 285, 313-318, 323-403, 408-410, 416-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   39-46, 73-75, 108-110, 116-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     42    31%   24, 28, 32, 39, 43, 47-50, 56-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170    111    35%   73-96, 102-132, 142-154, 166-233, 251, 264-265, 284, 289-290, 304-305, 314-316, 320-339, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    210    40%   27-51, 55-62, 66-74, 78, 82, 86-111, 115-174, 182-183, 205-206, 216, 230-232, 238-246, 269-271, 276-277, 285-287, 295-305, 313-320, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 434-460, 463-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     51    67%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 281-293, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     26    76%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 190, 195, 200, 205, 214, 224
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          85     74    13%   25-83, 93-181
src\core\contabilita_stats.py                                           57      6    89%   68-69, 79, 81, 89-90
src\core\contabilita_worker.py                                          91     82    10%   22-27, 30-164
src\core\data_synchronizer.py                                           96     79    18%   24-86, 93-148, 155-156, 163-164, 171-172, 177-220
src\core\database.py                                                   139     55    60%   75, 82-86, 108-110, 117-119, 122-125, 139-140, 143, 154-170, 178-231, 238-248, 258-273, 280-284, 291-323
src\core\excel_importer.py                                             530    313    41%   23-24, 31-33, 133-138, 151-152, 162-164, 181, 202, 204, 222, 240, 252, 275-279, 282, 296-298, 305-421, 434-490, 504-574, 583-658, 663-737, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 861, 868, 872-873, 880, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155    137    12%   21-63, 68-69, 74, 79, 84-106, 113-152, 160-205, 210-212, 217-226, 234, 242-317, 321-324
src\core\license_validator.py                                          173    127    27%   34-38, 47-54, 64-68, 94-121, 126-150, 155-162, 176-200, 211-212, 221-241, 246-264, 268-316, 321-324, 329-332
src\core\lyra_client.py                                                129    116    10%   21-37, 55-69, 73-162, 168-224, 230-268
src\core\lyra_sentinel.py                                               32      9    72%   37-38, 44-50
src\core\notification_manager.py                                        77     55    29%   25-27, 30-32, 36-45, 49-53, 60-75, 79-81, 85, 89-96, 100-109, 113-118, 122-125
src\core\secrets_manager.py                                             75     38    49%   29-58, 63, 68, 73, 78, 88-89, 96-97, 104-105, 112-113, 118-124
src\core\stats_manager.py                                               48     18    62%   33-40, 43, 56, 58, 66-74, 78
src\core\telegram_bridge.py                                            274    237    14%   27-29, 33-42, 46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    418    12%   46-56, 62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19     14    26%   21-37, 50-56
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     55    85%   49-50, 307, 346, 354, 427, 465-466, 474-475, 484-486, 517-531, 534-547, 559-560, 584, 630-631, 639-647, 660, 729-730, 756-758, 793-794, 798
src\gui\contabilita_panel.py                                           244    216    11%   35-42, 45-50, 53-112, 115-153, 156-158, 161, 164-168, 172-193, 198-222, 225-229, 232, 235-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     28    24%   17-20, 24-32, 36-39, 46-50, 54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     99    12%   20-21, 26-98, 106-118, 122-138, 142-145, 149-151, 155-157, 161-183, 187-188
src\gui\controllers\search_controller.py                                96     86    10%   11-12, 16-41, 45-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35     27    23%   15-17, 21-44, 47-52, 58
src\gui\dashboard_panel.py                                             120    107    11%   31-50, 54-55, 59-66, 70-190, 194-318, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      1    96%   22
src\gui\help_panel.py                                                  105     84    20%   27-30, 33-153, 157-175, 178-192, 196-203, 207-210, 213, 235, 257, 285, 307, 324, 342, 359, 375, 392, 409, 425
src\gui\layouts\responsive.py                                           56     46    18%   15-18, 21-22, 25-26, 29-35, 38-42, 46-84
src\gui\lyra_panel.py                                                  330    289    12%   42-46, 49-67, 76-77, 80-89, 94-102, 105-368, 375-388, 392-397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 480-485, 489-511, 517-520, 524-545, 548-566, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232    175    25%   57-97, 102-148, 152-178, 182-188, 192-195, 201-206, 217-226, 230, 234-238, 242-296, 300-303, 309-313, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 362, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 410-420
src\gui\notifications_panel.py                                         194    174    10%   35-38, 41-135, 140-211, 218-227, 230-332, 335-336, 340-383, 386-389, 412-415, 418, 422-439
src\gui\panels.py                                                      975    321    67%   77-90, 94-98, 215, 252, 305, 372-376, 420-422, 426-427, 431-444, 449, 464-469, 474, 478, 494-498, 518-519, 557-561, 604-606, 609-617, 620-632, 636, 652-657, 664, 669-727, 745-749, 801-804, 808-815, 820, 824, 839-845, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1466, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    468    11%   36-38, 41-103, 107-122, 129-224, 227-232, 271-299, 302-315, 318-339, 342, 349-385, 391-398, 401-403, 406-408, 411-440, 443-448, 451-479, 486-488, 491-494, 499-537, 550-606, 609-615, 618-623, 626-631, 634, 637-638, 642-654, 657-662, 669-707, 711-801, 804-818, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 887-911, 914-919
src\gui\scarico_ore_panel.py                                           286    255    11%   39-41, 45-84, 91-101, 104-339, 345-347, 352-360, 364-390, 394-396, 400-421, 431-468, 472-480, 484-497, 501-515, 530-533, 537-550, 554-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155   1071     7%   51-105, 108-115, 118, 125-183, 190-191, 194-276, 279-305, 309-405, 419-429, 433-987, 990-1104, 1108-1121, 1127-1132, 1135-1281, 1285-1287, 1290-1297, 1300-1303, 1307-1329, 1333-1364, 1367-1368, 1371-1389, 1392, 1410, 1429, 1447-1448, 1469-1484, 1488, 1492-1494, 1498, 1502-1506, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1577-1584, 1587-1594, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1703-1707, 1711-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1772-1776, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1923-1980, 1984-2052, 2055-2062, 2065-2082
src\gui\styles.py                                                       58     42    28%   24-27, 32, 39-46, 50-83, 87-103, 108
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30     30     0%   1-55
src\gui\widgets\bot_parameters.py                                      112      8    93%   141, 144-146, 184-185, 191-192
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161    142    12%   48-50, 53-125, 128, 131-170, 173-190, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     91    18%   53-55, 58-101, 104, 107-125, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164    140    15%   41-44, 47-89, 93, 96-118, 121-142, 145-159, 164-169, 172-185, 188-210, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     29    12%   10-45
src\gui\widgets\contabilita\year_tab.py                                 46     34    26%   34-39, 42-80, 84, 88-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17     17     0%   1-28
src\gui\widgets\excel_table.py                                         313    208    34%   46-59, 63-70, 74-91, 95-138, 142-158, 162-188, 192-211, 215-271, 347-382, 391-397, 426, 435-438, 441-443, 481-486, 498-522
src\gui\widgets\info_widgets.py                                         91     39    57%   24-55, 58, 74-96, 144
src\gui\widgets\modern_button.py                                        62     11    82%   64-65, 70-73, 76-79, 138
src\gui\widgets\notification_item.py                                    61     52    15%   12-15, 18-113, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19     14    26%   8-15, 19-22, 26-42
src\gui\widgets\sidebar_widget.py                                       75     62    17%   18-32, 35-114, 117-131, 135-137
src\gui\widgets\status_card.py                                          68      2    97%   102-103
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 35-52, 55-60
src\gui\widgets\timeline_widget.py                                     226     66    71%   66-69, 72-75, 126-132, 135-141, 149-158, 162, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85     60    29%   41-54, 57-96, 100-114, 118-123, 134-136, 143-175, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29     21    28%   11-15, 18-29, 33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         64     21    67%   12-13, 22-31, 48-49, 65-66, 73-74, 84-86
src\utils\helpers.py                                                    79     50    37%   21, 34-38, 54-76, 89-91, 96, 123-124, 132, 145-159, 173-175, 190-197, 212, 234
src\utils\log_humanizer.py                                              27      6    78%   73, 79, 81, 83, 87, 94
src\utils\parsing.py                                                    48     10    79%   22, 25, 48, 69, 77, 91, 130-147
src\utils\printing.py                                                   82     65    21%   20-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33      9    73%   18, 35-38, 43-44, 49-50
src\utils\secure_logger.py                                              22     10    55%   39-46, 49-52
src\utils\security.py                                                   85     27    68%   38-41, 57-58, 83-87, 107, 109, 114-116, 121, 127-129, 133-139
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   8072    37%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_import_giornaliere_lookup_logic
1 failed in 6.77s

```
</details>

---
### `tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`
**Error:** `FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________ TestContabilitaManagerBoost.test_cleanup_future_years ____________
tests\unit\test_contabilita_manager_boost.py:49: in test_cleanup_future_years
    manager.execute_query(db_path, "INSERT INTO contabilita (year, attivita) VALUES (2026, 'Dirty Data')")
src\core\database.py:107: in execute_query
    cursor.execute(query, params)
E   sqlite3.OperationalError: no such table: contabilita
------------------------------ Captured log call ------------------------------
ERROR    src.core.database:database.py:78 Database Operational Error (contabilita.db): no such table: contabilita
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     85    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 328-332, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62     40    35%   33, 37, 46-49, 55-62, 65-107
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210    144    31%   37-44, 47-80, 83-103, 106-146, 150-163, 214, 237-243, 262-266, 277-285, 289-310, 319-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228    159    30%   56, 75-90, 97-199, 203-233, 238, 273-275, 285, 313-318, 323-403, 408-410, 416-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   39-46, 73-75, 108-110, 116-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     42    31%   24, 28, 32, 39, 43, 47-50, 56-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170    111    35%   73-96, 102-132, 142-154, 166-233, 251, 264-265, 284, 289-290, 304-305, 314-316, 320-339, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    210    40%   27-51, 55-62, 66-74, 78, 82, 86-111, 115-174, 182-183, 205-206, 216, 230-232, 238-246, 269-271, 276-277, 285-287, 295-305, 313-320, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 434-460, 463-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     51    67%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 281-293, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     26    76%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 190, 195, 200, 205, 214, 224
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          85     74    13%   25-83, 93-181
src\core\contabilita_stats.py                                           57      6    89%   68-69, 79, 81, 89-90
src\core\contabilita_worker.py                                          91     82    10%   22-27, 30-164
src\core\data_synchronizer.py                                           96     79    18%   24-86, 93-148, 155-156, 163-164, 171-172, 177-220
src\core\database.py                                                   139     55    60%   75, 82-86, 108-110, 117-119, 122-125, 139-140, 143, 154-170, 178-231, 238-248, 258-273, 280-284, 291-323
src\core\excel_importer.py                                             530    313    41%   23-24, 31-33, 133-138, 151-152, 162-164, 181, 202, 204, 222, 240, 252, 275-279, 282, 296-298, 305-421, 434-490, 504-574, 583-658, 663-737, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 861, 868, 872-873, 880, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155    137    12%   21-63, 68-69, 74, 79, 84-106, 113-152, 160-205, 210-212, 217-226, 234, 242-317, 321-324
src\core\license_validator.py                                          173    127    27%   34-38, 47-54, 64-68, 94-121, 126-150, 155-162, 176-200, 211-212, 221-241, 246-264, 268-316, 321-324, 329-332
src\core\lyra_client.py                                                129    116    10%   21-37, 55-69, 73-162, 168-224, 230-268
src\core\lyra_sentinel.py                                               32      9    72%   37-38, 44-50
src\core\notification_manager.py                                        77     55    29%   25-27, 30-32, 36-45, 49-53, 60-75, 79-81, 85, 89-96, 100-109, 113-118, 122-125
src\core\secrets_manager.py                                             75     38    49%   29-58, 63, 68, 73, 78, 88-89, 96-97, 104-105, 112-113, 118-124
src\core\stats_manager.py                                               48     18    62%   33-40, 43, 56, 58, 66-74, 78
src\core\telegram_bridge.py                                            274    237    14%   27-29, 33-42, 46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    418    12%   46-56, 62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19     14    26%   21-37, 50-56
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     55    85%   49-50, 307, 346, 354, 427, 465-466, 474-475, 484-486, 517-531, 534-547, 559-560, 584, 630-631, 639-647, 660, 729-730, 756-758, 793-794, 798
src\gui\contabilita_panel.py                                           244    216    11%   35-42, 45-50, 53-112, 115-153, 156-158, 161, 164-168, 172-193, 198-222, 225-229, 232, 235-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     28    24%   17-20, 24-32, 36-39, 46-50, 54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     99    12%   20-21, 26-98, 106-118, 122-138, 142-145, 149-151, 155-157, 161-183, 187-188
src\gui\controllers\search_controller.py                                96     86    10%   11-12, 16-41, 45-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35     27    23%   15-17, 21-44, 47-52, 58
src\gui\dashboard_panel.py                                             120    107    11%   31-50, 54-55, 59-66, 70-190, 194-318, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      1    96%   22
src\gui\help_panel.py                                                  105     84    20%   27-30, 33-153, 157-175, 178-192, 196-203, 207-210, 213, 235, 257, 285, 307, 324, 342, 359, 375, 392, 409, 425
src\gui\layouts\responsive.py                                           56     46    18%   15-18, 21-22, 25-26, 29-35, 38-42, 46-84
src\gui\lyra_panel.py                                                  330    289    12%   42-46, 49-67, 76-77, 80-89, 94-102, 105-368, 375-388, 392-397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 480-485, 489-511, 517-520, 524-545, 548-566, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232    175    25%   57-97, 102-148, 152-178, 182-188, 192-195, 201-206, 217-226, 230, 234-238, 242-296, 300-303, 309-313, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 362, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 410-420
src\gui\notifications_panel.py                                         194    174    10%   35-38, 41-135, 140-211, 218-227, 230-332, 335-336, 340-383, 386-389, 412-415, 418, 422-439
src\gui\panels.py                                                      975    321    67%   77-90, 94-98, 215, 252, 305, 372-376, 420-422, 426-427, 431-444, 449, 464-469, 474, 478, 494-498, 518-519, 557-561, 604-606, 609-617, 620-632, 636, 652-657, 664, 669-727, 745-749, 801-804, 808-815, 820, 824, 839-845, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1466, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    468    11%   36-38, 41-103, 107-122, 129-224, 227-232, 271-299, 302-315, 318-339, 342, 349-385, 391-398, 401-403, 406-408, 411-440, 443-448, 451-479, 486-488, 491-494, 499-537, 550-606, 609-615, 618-623, 626-631, 634, 637-638, 642-654, 657-662, 669-707, 711-801, 804-818, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 887-911, 914-919
src\gui\scarico_ore_panel.py                                           286    255    11%   39-41, 45-84, 91-101, 104-339, 345-347, 352-360, 364-390, 394-396, 400-421, 431-468, 472-480, 484-497, 501-515, 530-533, 537-550, 554-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155   1071     7%   51-105, 108-115, 118, 125-183, 190-191, 194-276, 279-305, 309-405, 419-429, 433-987, 990-1104, 1108-1121, 1127-1132, 1135-1281, 1285-1287, 1290-1297, 1300-1303, 1307-1329, 1333-1364, 1367-1368, 1371-1389, 1392, 1410, 1429, 1447-1448, 1469-1484, 1488, 1492-1494, 1498, 1502-1506, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1577-1584, 1587-1594, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1703-1707, 1711-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1772-1776, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1923-1980, 1984-2052, 2055-2062, 2065-2082
src\gui\styles.py                                                       58     42    28%   24-27, 32, 39-46, 50-83, 87-103, 108
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30     30     0%   1-55
src\gui\widgets\bot_parameters.py                                      112      8    93%   141, 144-146, 184-185, 191-192
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161    142    12%   48-50, 53-125, 128, 131-170, 173-190, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     91    18%   53-55, 58-101, 104, 107-125, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164    140    15%   41-44, 47-89, 93, 96-118, 121-142, 145-159, 164-169, 172-185, 188-210, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     29    12%   10-45
src\gui\widgets\contabilita\year_tab.py                                 46     34    26%   34-39, 42-80, 84, 88-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17     17     0%   1-28
src\gui\widgets\excel_table.py                                         313    208    34%   46-59, 63-70, 74-91, 95-138, 142-158, 162-188, 192-211, 215-271, 347-382, 391-397, 426, 435-438, 441-443, 481-486, 498-522
src\gui\widgets\info_widgets.py                                         91     39    57%   24-55, 58, 74-96, 144
src\gui\widgets\modern_button.py                                        62     11    82%   64-65, 70-73, 76-79, 138
src\gui\widgets\notification_item.py                                    61     52    15%   12-15, 18-113, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19     14    26%   8-15, 19-22, 26-42
src\gui\widgets\sidebar_widget.py                                       75     62    17%   18-32, 35-114, 117-131, 135-137
src\gui\widgets\status_card.py                                          68      2    97%   102-103
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 35-52, 55-60
src\gui\widgets\timeline_widget.py                                     226     66    71%   66-69, 72-75, 126-132, 135-141, 149-158, 162, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85     60    29%   41-54, 57-96, 100-114, 118-123, 134-136, 143-175, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29     21    28%   11-15, 18-29, 33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         64     21    67%   12-13, 22-31, 48-49, 65-66, 73-74, 84-86
src\utils\helpers.py                                                    79     50    37%   21, 34-38, 54-76, 89-91, 96, 123-124, 132, 145-159, 173-175, 190-197, 212, 234
src\utils\log_humanizer.py                                              27      6    78%   73, 79, 81, 83, 87, 94
src\utils\parsing.py                                                    48     10    79%   22, 25, 48, 69, 77, 91, 130-147
src\utils\printing.py                                                   82     65    21%   20-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33      9    73%   18, 35-38, 43-44, 49-50
src\utils\secure_logger.py                                              22     10    55%   39-46, 49-52
src\utils\security.py                                                   85     27    68%   38-41, 57-58, 83-87, 107, 109, 114-116, 121, 127-129, 133-139
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   8072    37%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_cleanup_future_years
1 failed in 7.81s

```
</details>

---
### `tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_get_available_years_logic`
**Error:** `FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_get_available_years_logic`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestContabilitaManagerBoost.test_get_available_years_logic __________
tests\unit\test_contabilita_manager_boost.py:74: in test_get_available_years_logic
    manager.execute_query(db_setup, "INSERT INTO contabilita (year) VALUES (2022)")
src\core\database.py:107: in execute_query
    cursor.execute(query, params)
E   sqlite3.OperationalError: no such table: contabilita
------------------------------ Captured log call ------------------------------
ERROR    src.core.database:database.py:78 Database Operational Error (contabilita.db): no such table: contabilita
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     85    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 328-332, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62     40    35%   33, 37, 46-49, 55-62, 65-107
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210    144    31%   37-44, 47-80, 83-103, 106-146, 150-163, 214, 237-243, 262-266, 277-285, 289-310, 319-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228    159    30%   56, 75-90, 97-199, 203-233, 238, 273-275, 285, 313-318, 323-403, 408-410, 416-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   39-46, 73-75, 108-110, 116-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     42    31%   24, 28, 32, 39, 43, 47-50, 56-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170    111    35%   73-96, 102-132, 142-154, 166-233, 251, 264-265, 284, 289-290, 304-305, 314-316, 320-339, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    210    40%   27-51, 55-62, 66-74, 78, 82, 86-111, 115-174, 182-183, 205-206, 216, 230-232, 238-246, 269-271, 276-277, 285-287, 295-305, 313-320, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 434-460, 463-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     51    67%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 281-293, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     26    76%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 190, 195, 200, 205, 214, 224
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          85     74    13%   25-83, 93-181
src\core\contabilita_stats.py                                           57      6    89%   68-69, 79, 81, 89-90
src\core\contabilita_worker.py                                          91     82    10%   22-27, 30-164
src\core\data_synchronizer.py                                           96     79    18%   24-86, 93-148, 155-156, 163-164, 171-172, 177-220
src\core\database.py                                                   139     55    60%   75, 82-86, 108-110, 117-119, 122-125, 139-140, 143, 154-170, 178-231, 238-248, 258-273, 280-284, 291-323
src\core\excel_importer.py                                             530    313    41%   23-24, 31-33, 133-138, 151-152, 162-164, 181, 202, 204, 222, 240, 252, 275-279, 282, 296-298, 305-421, 434-490, 504-574, 583-658, 663-737, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 861, 868, 872-873, 880, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155    137    12%   21-63, 68-69, 74, 79, 84-106, 113-152, 160-205, 210-212, 217-226, 234, 242-317, 321-324
src\core\license_validator.py                                          173    127    27%   34-38, 47-54, 64-68, 94-121, 126-150, 155-162, 176-200, 211-212, 221-241, 246-264, 268-316, 321-324, 329-332
src\core\lyra_client.py                                                129    116    10%   21-37, 55-69, 73-162, 168-224, 230-268
src\core\lyra_sentinel.py                                               32      9    72%   37-38, 44-50
src\core\notification_manager.py                                        77     55    29%   25-27, 30-32, 36-45, 49-53, 60-75, 79-81, 85, 89-96, 100-109, 113-118, 122-125
src\core\secrets_manager.py                                             75     38    49%   29-58, 63, 68, 73, 78, 88-89, 96-97, 104-105, 112-113, 118-124
src\core\stats_manager.py                                               48     18    62%   33-40, 43, 56, 58, 66-74, 78
src\core\telegram_bridge.py                                            274    237    14%   27-29, 33-42, 46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    418    12%   46-56, 62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19     14    26%   21-37, 50-56
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     55    85%   49-50, 307, 346, 354, 427, 465-466, 474-475, 484-486, 517-531, 534-547, 559-560, 584, 630-631, 639-647, 660, 729-730, 756-758, 793-794, 798
src\gui\contabilita_panel.py                                           244    216    11%   35-42, 45-50, 53-112, 115-153, 156-158, 161, 164-168, 172-193, 198-222, 225-229, 232, 235-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     28    24%   17-20, 24-32, 36-39, 46-50, 54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     99    12%   20-21, 26-98, 106-118, 122-138, 142-145, 149-151, 155-157, 161-183, 187-188
src\gui\controllers\search_controller.py                                96     86    10%   11-12, 16-41, 45-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35     27    23%   15-17, 21-44, 47-52, 58
src\gui\dashboard_panel.py                                             120    107    11%   31-50, 54-55, 59-66, 70-190, 194-318, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      1    96%   22
src\gui\help_panel.py                                                  105     84    20%   27-30, 33-153, 157-175, 178-192, 196-203, 207-210, 213, 235, 257, 285, 307, 324, 342, 359, 375, 392, 409, 425
src\gui\layouts\responsive.py                                           56     46    18%   15-18, 21-22, 25-26, 29-35, 38-42, 46-84
src\gui\lyra_panel.py                                                  330    289    12%   42-46, 49-67, 76-77, 80-89, 94-102, 105-368, 375-388, 392-397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 480-485, 489-511, 517-520, 524-545, 548-566, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232    175    25%   57-97, 102-148, 152-178, 182-188, 192-195, 201-206, 217-226, 230, 234-238, 242-296, 300-303, 309-313, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 362, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 410-420
src\gui\notifications_panel.py                                         194    174    10%   35-38, 41-135, 140-211, 218-227, 230-332, 335-336, 340-383, 386-389, 412-415, 418, 422-439
src\gui\panels.py                                                      975    321    67%   77-90, 94-98, 215, 252, 305, 372-376, 420-422, 426-427, 431-444, 449, 464-469, 474, 478, 494-498, 518-519, 557-561, 604-606, 609-617, 620-632, 636, 652-657, 664, 669-727, 745-749, 801-804, 808-815, 820, 824, 839-845, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1466, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    468    11%   36-38, 41-103, 107-122, 129-224, 227-232, 271-299, 302-315, 318-339, 342, 349-385, 391-398, 401-403, 406-408, 411-440, 443-448, 451-479, 486-488, 491-494, 499-537, 550-606, 609-615, 618-623, 626-631, 634, 637-638, 642-654, 657-662, 669-707, 711-801, 804-818, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 887-911, 914-919
src\gui\scarico_ore_panel.py                                           286    255    11%   39-41, 45-84, 91-101, 104-339, 345-347, 352-360, 364-390, 394-396, 400-421, 431-468, 472-480, 484-497, 501-515, 530-533, 537-550, 554-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155   1071     7%   51-105, 108-115, 118, 125-183, 190-191, 194-276, 279-305, 309-405, 419-429, 433-987, 990-1104, 1108-1121, 1127-1132, 1135-1281, 1285-1287, 1290-1297, 1300-1303, 1307-1329, 1333-1364, 1367-1368, 1371-1389, 1392, 1410, 1429, 1447-1448, 1469-1484, 1488, 1492-1494, 1498, 1502-1506, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1577-1584, 1587-1594, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1703-1707, 1711-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1772-1776, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1923-1980, 1984-2052, 2055-2062, 2065-2082
src\gui\styles.py                                                       58     42    28%   24-27, 32, 39-46, 50-83, 87-103, 108
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30     30     0%   1-55
src\gui\widgets\bot_parameters.py                                      112      8    93%   141, 144-146, 184-185, 191-192
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161    142    12%   48-50, 53-125, 128, 131-170, 173-190, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     91    18%   53-55, 58-101, 104, 107-125, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164    140    15%   41-44, 47-89, 93, 96-118, 121-142, 145-159, 164-169, 172-185, 188-210, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     29    12%   10-45
src\gui\widgets\contabilita\year_tab.py                                 46     34    26%   34-39, 42-80, 84, 88-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17     17     0%   1-28
src\gui\widgets\excel_table.py                                         313    208    34%   46-59, 63-70, 74-91, 95-138, 142-158, 162-188, 192-211, 215-271, 347-382, 391-397, 426, 435-438, 441-443, 481-486, 498-522
src\gui\widgets\info_widgets.py                                         91     39    57%   24-55, 58, 74-96, 144
src\gui\widgets\modern_button.py                                        62     11    82%   64-65, 70-73, 76-79, 138
src\gui\widgets\notification_item.py                                    61     52    15%   12-15, 18-113, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19     14    26%   8-15, 19-22, 26-42
src\gui\widgets\sidebar_widget.py                                       75     62    17%   18-32, 35-114, 117-131, 135-137
src\gui\widgets\status_card.py                                          68      2    97%   102-103
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 35-52, 55-60
src\gui\widgets\timeline_widget.py                                     226     66    71%   66-69, 72-75, 126-132, 135-141, 149-158, 162, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85     60    29%   41-54, 57-96, 100-114, 118-123, 134-136, 143-175, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29     21    28%   11-15, 18-29, 33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         64     21    67%   12-13, 22-31, 48-49, 65-66, 73-74, 84-86
src\utils\helpers.py                                                    79     50    37%   21, 34-38, 54-76, 89-91, 96, 123-124, 132, 145-159, 173-175, 190-197, 212, 234
src\utils\log_humanizer.py                                              27      6    78%   73, 79, 81, 83, 87, 94
src\utils\parsing.py                                                    48     10    79%   22, 25, 48, 69, 77, 91, 130-147
src\utils\printing.py                                                   82     65    21%   20-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33      9    73%   18, 35-38, 43-44, 49-50
src\utils\secure_logger.py                                              22     10    55%   39-46, 49-52
src\utils\security.py                                                   85     27    68%   38-41, 57-58, 83-87, 107, 109, 114-116, 121, 127-129, 133-139
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   8072    37%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_manager_boost.py::TestContabilitaManagerBoost::test_get_available_years_logic
1 failed in 7.33s

```
</details>

---
### `tests/unit/test_contabilita_queries_coverage.py::TestContabilitaQueriesCoverage::test_get_data_by_year_columns_alignment`
**Error:** `FAILED tests/unit/test_contabilita_queries_coverage.py::TestContabilitaQueriesCoverage::test_get_data_by_year_columns_alignment`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
___ TestContabilitaQueriesCoverage.test_get_data_by_year_columns_alignment ____
tests\unit\test_contabilita_queries_coverage.py:23: in test_get_data_by_year_columns_alignment
    manager.execute_query(db_path, "INSERT INTO contabilita (year, n_prev, attivita, odc) VALUES (2024, 'P1', 'A1', 'O1')")
src\core\database.py:105: in execute_query
    with self.get_connection(db_path) as conn:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1139: in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1143: in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1204: in _execute_mock_call
    result = effect(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^
tests\unit\test_contabilita_queries_coverage.py:18: in <lambda>
    mocker.patch("src.core.database.db_manager.get_connection", side_effect=lambda p, read_only=False: DatabaseManager().get_connection(db_path, read_only))
                                                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1139: in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1143: in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1204: in _execute_mock_call
    result = effect(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^
tests\unit\test_contabilita_queries_coverage.py:18: in <lambda>
    mocker.patch("src.core.database.db_manager.get_connection", side_effect=lambda p, read_only=False: DatabaseManager().get_connection(db_path, read_only))
                                                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   RecursionError: maximum recursion depth exceeded
!!! Recursion detected (same locals & position)
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     85    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 328-332, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62     40    35%   33, 37, 46-49, 55-62, 65-107
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210    144    31%   37-44, 47-80, 83-103, 106-146, 150-163, 214, 237-243, 262-266, 277-285, 289-310, 319-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228    159    30%   56, 75-90, 97-199, 203-233, 238, 273-275, 285, 313-318, 323-403, 408-410, 416-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   39-46, 73-75, 108-110, 116-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     42    31%   24, 28, 32, 39, 43, 47-50, 56-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170    111    35%   73-96, 102-132, 142-154, 166-233, 251, 264-265, 284, 289-290, 304-305, 314-316, 320-339, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    210    40%   27-51, 55-62, 66-74, 78, 82, 86-111, 115-174, 182-183, 205-206, 216, 230-232, 238-246, 269-271, 276-277, 285-287, 295-305, 313-320, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 434-460, 463-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     51    67%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 281-293, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     26    76%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 190, 195, 200, 205, 214, 224
src\core\contabilita_queries.py                                         87     44    49%   29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          85     74    13%   25-83, 93-181
src\core\contabilita_stats.py                                           57      6    89%   68-69, 79, 81, 89-90
src\core\contabilita_worker.py                                          91     82    10%   22-27, 30-164
src\core\data_synchronizer.py                                           96     79    18%   24-86, 93-148, 155-156, 163-164, 171-172, 177-220
src\core\database.py                                                   139     55    60%   75, 82-86, 108-110, 117-119, 122-125, 139-140, 143, 154-170, 178-231, 238-248, 258-273, 280-284, 291-323
src\core\excel_importer.py                                             530    313    41%   23-24, 31-33, 133-138, 151-152, 162-164, 181, 202, 204, 222, 240, 252, 275-279, 282, 296-298, 305-421, 434-490, 504-574, 583-658, 663-737, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 861, 868, 872-873, 880, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155    137    12%   21-63, 68-69, 74, 79, 84-106, 113-152, 160-205, 210-212, 217-226, 234, 242-317, 321-324
src\core\license_validator.py                                          173    127    27%   34-38, 47-54, 64-68, 94-121, 126-150, 155-162, 176-200, 211-212, 221-241, 246-264, 268-316, 321-324, 329-332
src\core\lyra_client.py                                                129    116    10%   21-37, 55-69, 73-162, 168-224, 230-268
src\core\lyra_sentinel.py                                               32      9    72%   37-38, 44-50
src\core\notification_manager.py                                        77     55    29%   25-27, 30-32, 36-45, 49-53, 60-75, 79-81, 85, 89-96, 100-109, 113-118, 122-125
src\core\secrets_manager.py                                             75     38    49%   29-58, 63, 68, 73, 78, 88-89, 96-97, 104-105, 112-113, 118-124
src\core\stats_manager.py                                               48     18    62%   33-40, 43, 56, 58, 66-74, 78
src\core\telegram_bridge.py                                            274    237    14%   27-29, 33-42, 46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    418    12%   46-56, 62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19     14    26%   21-37, 50-56
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     55    85%   49-50, 307, 346, 354, 427, 465-466, 474-475, 484-486, 517-531, 534-547, 559-560, 584, 630-631, 639-647, 660, 729-730, 756-758, 793-794, 798
src\gui\contabilita_panel.py                                           244    216    11%   35-42, 45-50, 53-112, 115-153, 156-158, 161, 164-168, 172-193, 198-222, 225-229, 232, 235-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     28    24%   17-20, 24-32, 36-39, 46-50, 54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     99    12%   20-21, 26-98, 106-118, 122-138, 142-145, 149-151, 155-157, 161-183, 187-188
src\gui\controllers\search_controller.py                                96     86    10%   11-12, 16-41, 45-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35     27    23%   15-17, 21-44, 47-52, 58
src\gui\dashboard_panel.py                                             120    107    11%   31-50, 54-55, 59-66, 70-190, 194-318, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      1    96%   22
src\gui\help_panel.py                                                  105     84    20%   27-30, 33-153, 157-175, 178-192, 196-203, 207-210, 213, 235, 257, 285, 307, 324, 342, 359, 375, 392, 409, 425
src\gui\layouts\responsive.py                                           56     46    18%   15-18, 21-22, 25-26, 29-35, 38-42, 46-84
src\gui\lyra_panel.py                                                  330    289    12%   42-46, 49-67, 76-77, 80-89, 94-102, 105-368, 375-388, 392-397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 480-485, 489-511, 517-520, 524-545, 548-566, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232    175    25%   57-97, 102-148, 152-178, 182-188, 192-195, 201-206, 217-226, 230, 234-238, 242-296, 300-303, 309-313, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 362, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 410-420
src\gui\notifications_panel.py                                         194    174    10%   35-38, 41-135, 140-211, 218-227, 230-332, 335-336, 340-383, 386-389, 412-415, 418, 422-439
src\gui\panels.py                                                      975    321    67%   77-90, 94-98, 215, 252, 305, 372-376, 420-422, 426-427, 431-444, 449, 464-469, 474, 478, 494-498, 518-519, 557-561, 604-606, 609-617, 620-632, 636, 652-657, 664, 669-727, 745-749, 801-804, 808-815, 820, 824, 839-845, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1466, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    468    11%   36-38, 41-103, 107-122, 129-224, 227-232, 271-299, 302-315, 318-339, 342, 349-385, 391-398, 401-403, 406-408, 411-440, 443-448, 451-479, 486-488, 491-494, 499-537, 550-606, 609-615, 618-623, 626-631, 634, 637-638, 642-654, 657-662, 669-707, 711-801, 804-818, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 887-911, 914-919
src\gui\scarico_ore_panel.py                                           286    255    11%   39-41, 45-84, 91-101, 104-339, 345-347, 352-360, 364-390, 394-396, 400-421, 431-468, 472-480, 484-497, 501-515, 530-533, 537-550, 554-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155   1071     7%   51-105, 108-115, 118, 125-183, 190-191, 194-276, 279-305, 309-405, 419-429, 433-987, 990-1104, 1108-1121, 1127-1132, 1135-1281, 1285-1287, 1290-1297, 1300-1303, 1307-1329, 1333-1364, 1367-1368, 1371-1389, 1392, 1410, 1429, 1447-1448, 1469-1484, 1488, 1492-1494, 1498, 1502-1506, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1577-1584, 1587-1594, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1703-1707, 1711-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1772-1776, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1923-1980, 1984-2052, 2055-2062, 2065-2082
src\gui\styles.py                                                       58     42    28%   24-27, 32, 39-46, 50-83, 87-103, 108
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30     30     0%   1-55
src\gui\widgets\bot_parameters.py                                      112      8    93%   141, 144-146, 184-185, 191-192
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161    142    12%   48-50, 53-125, 128, 131-170, 173-190, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     91    18%   53-55, 58-101, 104, 107-125, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164    140    15%   41-44, 47-89, 93, 96-118, 121-142, 145-159, 164-169, 172-185, 188-210, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     29    12%   10-45
src\gui\widgets\contabilita\year_tab.py                                 46     34    26%   34-39, 42-80, 84, 88-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17     17     0%   1-28
src\gui\widgets\excel_table.py                                         313    208    34%   46-59, 63-70, 74-91, 95-138, 142-158, 162-188, 192-211, 215-271, 347-382, 391-397, 426, 435-438, 441-443, 481-486, 498-522
src\gui\widgets\info_widgets.py                                         91     39    57%   24-55, 58, 74-96, 144
src\gui\widgets\modern_button.py                                        62     11    82%   64-65, 70-73, 76-79, 138
src\gui\widgets\notification_item.py                                    61     52    15%   12-15, 18-113, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19     14    26%   8-15, 19-22, 26-42
src\gui\widgets\sidebar_widget.py                                       75     62    17%   18-32, 35-114, 117-131, 135-137
src\gui\widgets\status_card.py                                          68      2    97%   102-103
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 35-52, 55-60
src\gui\widgets\timeline_widget.py                                     226     66    71%   66-69, 72-75, 126-132, 135-141, 149-158, 162, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85     60    29%   41-54, 57-96, 100-114, 118-123, 134-136, 143-175, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29     21    28%   11-15, 18-29, 33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         64     21    67%   12-13, 22-31, 48-49, 65-66, 73-74, 84-86
src\utils\helpers.py                                                    79     50    37%   21, 34-38, 54-76, 89-91, 96, 123-124, 132, 145-159, 173-175, 190-197, 212, 234
src\utils\log_humanizer.py                                              27      6    78%   73, 79, 81, 83, 87, 94
src\utils\parsing.py                                                    48     10    79%   22, 25, 48, 69, 77, 91, 130-147
src\utils\printing.py                                                   82     65    21%   20-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33      9    73%   18, 35-38, 43-44, 49-50
src\utils\secure_logger.py                                              22     10    55%   39-46, 49-52
src\utils\security.py                                                   85     27    68%   38-41, 57-58, 83-87, 107, 109, 114-116, 121, 127-129, 133-139
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   8071    37%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_queries_coverage.py::TestContabilitaQueriesCoverage::test_get_data_by_year_columns_alignment
1 failed in 7.74s

```
</details>

---
### `tests/unit/test_contabilita_queries_coverage.py::TestContabilitaQueriesCoverage::test_get_scarico_ore_data_sorting`
**Error:** `FAILED tests/unit/test_contabilita_queries_coverage.py::TestContabilitaQueriesCoverage::test_get_scarico_ore_data_sorting`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
______ TestContabilitaQueriesCoverage.test_get_scarico_ore_data_sorting _______
tests\unit\test_contabilita_queries_coverage.py:41: in test_get_scarico_ore_data_sorting
    manager.execute_query(db_path, "INSERT INTO scarico_ore (descrizione) VALUES ('Prima')")
src\core\database.py:105: in execute_query
    with self.get_connection(db_path) as conn:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1139: in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1143: in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1204: in _execute_mock_call
    result = effect(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^
tests\unit\test_contabilita_queries_coverage.py:38: in <lambda>
    mocker.patch("src.core.database.db_manager.get_connection", side_effect=lambda p, read_only=False: DatabaseManager().get_connection(db_path, read_only))
                                                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1139: in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1143: in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1204: in _execute_mock_call
    result = effect(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^
tests\unit\test_contabilita_queries_coverage.py:38: in <lambda>
    mocker.patch("src.core.database.db_manager.get_connection", side_effect=lambda p, read_only=False: DatabaseManager().get_connection(db_path, read_only))
                                                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   RecursionError: maximum recursion depth exceeded
!!! Recursion detected (same locals & position)
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     85    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 328-332, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62     40    35%   33, 37, 46-49, 55-62, 65-107
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210    144    31%   37-44, 47-80, 83-103, 106-146, 150-163, 214, 237-243, 262-266, 277-285, 289-310, 319-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228    159    30%   56, 75-90, 97-199, 203-233, 238, 273-275, 285, 313-318, 323-403, 408-410, 416-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   39-46, 73-75, 108-110, 116-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     42    31%   24, 28, 32, 39, 43, 47-50, 56-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170    111    35%   73-96, 102-132, 142-154, 166-233, 251, 264-265, 284, 289-290, 304-305, 314-316, 320-339, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    210    40%   27-51, 55-62, 66-74, 78, 82, 86-111, 115-174, 182-183, 205-206, 216, 230-232, 238-246, 269-271, 276-277, 285-287, 295-305, 313-320, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 434-460, 463-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     51    67%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 281-293, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     26    76%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 190, 195, 200, 205, 214, 224
src\core\contabilita_queries.py                                         87     44    49%   29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          85     74    13%   25-83, 93-181
src\core\contabilita_stats.py                                           57      6    89%   68-69, 79, 81, 89-90
src\core\contabilita_worker.py                                          91     82    10%   22-27, 30-164
src\core\data_synchronizer.py                                           96     79    18%   24-86, 93-148, 155-156, 163-164, 171-172, 177-220
src\core\database.py                                                   139     55    60%   75, 82-86, 108-110, 117-119, 122-125, 139-140, 143, 154-170, 178-231, 238-248, 258-273, 280-284, 291-323
src\core\excel_importer.py                                             530    313    41%   23-24, 31-33, 133-138, 151-152, 162-164, 181, 202, 204, 222, 240, 252, 275-279, 282, 296-298, 305-421, 434-490, 504-574, 583-658, 663-737, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 861, 868, 872-873, 880, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155    137    12%   21-63, 68-69, 74, 79, 84-106, 113-152, 160-205, 210-212, 217-226, 234, 242-317, 321-324
src\core\license_validator.py                                          173    127    27%   34-38, 47-54, 64-68, 94-121, 126-150, 155-162, 176-200, 211-212, 221-241, 246-264, 268-316, 321-324, 329-332
src\core\lyra_client.py                                                129    116    10%   21-37, 55-69, 73-162, 168-224, 230-268
src\core\lyra_sentinel.py                                               32      9    72%   37-38, 44-50
src\core\notification_manager.py                                        77     55    29%   25-27, 30-32, 36-45, 49-53, 60-75, 79-81, 85, 89-96, 100-109, 113-118, 122-125
src\core\secrets_manager.py                                             75     38    49%   29-58, 63, 68, 73, 78, 88-89, 96-97, 104-105, 112-113, 118-124
src\core\stats_manager.py                                               48     18    62%   33-40, 43, 56, 58, 66-74, 78
src\core\telegram_bridge.py                                            274    237    14%   27-29, 33-42, 46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    418    12%   46-56, 62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19     14    26%   21-37, 50-56
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     55    85%   49-50, 307, 346, 354, 427, 465-466, 474-475, 484-486, 517-531, 534-547, 559-560, 584, 630-631, 639-647, 660, 729-730, 756-758, 793-794, 798
src\gui\contabilita_panel.py                                           244    216    11%   35-42, 45-50, 53-112, 115-153, 156-158, 161, 164-168, 172-193, 198-222, 225-229, 232, 235-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     28    24%   17-20, 24-32, 36-39, 46-50, 54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     99    12%   20-21, 26-98, 106-118, 122-138, 142-145, 149-151, 155-157, 161-183, 187-188
src\gui\controllers\search_controller.py                                96     86    10%   11-12, 16-41, 45-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35     27    23%   15-17, 21-44, 47-52, 58
src\gui\dashboard_panel.py                                             120    107    11%   31-50, 54-55, 59-66, 70-190, 194-318, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      1    96%   22
src\gui\help_panel.py                                                  105     84    20%   27-30, 33-153, 157-175, 178-192, 196-203, 207-210, 213, 235, 257, 285, 307, 324, 342, 359, 375, 392, 409, 425
src\gui\layouts\responsive.py                                           56     46    18%   15-18, 21-22, 25-26, 29-35, 38-42, 46-84
src\gui\lyra_panel.py                                                  330    289    12%   42-46, 49-67, 76-77, 80-89, 94-102, 105-368, 375-388, 392-397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 480-485, 489-511, 517-520, 524-545, 548-566, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232    175    25%   57-97, 102-148, 152-178, 182-188, 192-195, 201-206, 217-226, 230, 234-238, 242-296, 300-303, 309-313, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 362, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 410-420
src\gui\notifications_panel.py                                         194    174    10%   35-38, 41-135, 140-211, 218-227, 230-332, 335-336, 340-383, 386-389, 412-415, 418, 422-439
src\gui\panels.py                                                      975    321    67%   77-90, 94-98, 215, 252, 305, 372-376, 420-422, 426-427, 431-444, 449, 464-469, 474, 478, 494-498, 518-519, 557-561, 604-606, 609-617, 620-632, 636, 652-657, 664, 669-727, 745-749, 801-804, 808-815, 820, 824, 839-845, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1466, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    468    11%   36-38, 41-103, 107-122, 129-224, 227-232, 271-299, 302-315, 318-339, 342, 349-385, 391-398, 401-403, 406-408, 411-440, 443-448, 451-479, 486-488, 491-494, 499-537, 550-606, 609-615, 618-623, 626-631, 634, 637-638, 642-654, 657-662, 669-707, 711-801, 804-818, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 887-911, 914-919
src\gui\scarico_ore_panel.py                                           286    255    11%   39-41, 45-84, 91-101, 104-339, 345-347, 352-360, 364-390, 394-396, 400-421, 431-468, 472-480, 484-497, 501-515, 530-533, 537-550, 554-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155   1071     7%   51-105, 108-115, 118, 125-183, 190-191, 194-276, 279-305, 309-405, 419-429, 433-987, 990-1104, 1108-1121, 1127-1132, 1135-1281, 1285-1287, 1290-1297, 1300-1303, 1307-1329, 1333-1364, 1367-1368, 1371-1389, 1392, 1410, 1429, 1447-1448, 1469-1484, 1488, 1492-1494, 1498, 1502-1506, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1577-1584, 1587-1594, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1703-1707, 1711-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1772-1776, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1923-1980, 1984-2052, 2055-2062, 2065-2082
src\gui\styles.py                                                       58     42    28%   24-27, 32, 39-46, 50-83, 87-103, 108
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30     30     0%   1-55
src\gui\widgets\bot_parameters.py                                      112      8    93%   141, 144-146, 184-185, 191-192
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161    142    12%   48-50, 53-125, 128, 131-170, 173-190, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     91    18%   53-55, 58-101, 104, 107-125, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164    140    15%   41-44, 47-89, 93, 96-118, 121-142, 145-159, 164-169, 172-185, 188-210, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     29    12%   10-45
src\gui\widgets\contabilita\year_tab.py                                 46     34    26%   34-39, 42-80, 84, 88-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17     17     0%   1-28
src\gui\widgets\excel_table.py                                         313    208    34%   46-59, 63-70, 74-91, 95-138, 142-158, 162-188, 192-211, 215-271, 347-382, 391-397, 426, 435-438, 441-443, 481-486, 498-522
src\gui\widgets\info_widgets.py                                         91     39    57%   24-55, 58, 74-96, 144
src\gui\widgets\modern_button.py                                        62     11    82%   64-65, 70-73, 76-79, 138
src\gui\widgets\notification_item.py                                    61     52    15%   12-15, 18-113, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19     14    26%   8-15, 19-22, 26-42
src\gui\widgets\sidebar_widget.py                                       75     62    17%   18-32, 35-114, 117-131, 135-137
src\gui\widgets\status_card.py                                          68      2    97%   102-103
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 35-52, 55-60
src\gui\widgets\timeline_widget.py                                     226     66    71%   66-69, 72-75, 126-132, 135-141, 149-158, 162, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85     60    29%   41-54, 57-96, 100-114, 118-123, 134-136, 143-175, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29     21    28%   11-15, 18-29, 33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         64     21    67%   12-13, 22-31, 48-49, 65-66, 73-74, 84-86
src\utils\helpers.py                                                    79     50    37%   21, 34-38, 54-76, 89-91, 96, 123-124, 132, 145-159, 173-175, 190-197, 212, 234
src\utils\log_humanizer.py                                              27      6    78%   73, 79, 81, 83, 87, 94
src\utils\parsing.py                                                    48     10    79%   22, 25, 48, 69, 77, 91, 130-147
src\utils\printing.py                                                   82     65    21%   20-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33      9    73%   18, 35-38, 43-44, 49-50
src\utils\secure_logger.py                                              22     10    55%   39-46, 49-52
src\utils\security.py                                                   85     27    68%   38-41, 57-58, 83-87, 107, 109, 114-116, 121, 127-129, 133-139
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   8071    37%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_contabilita_queries_coverage.py::TestContabilitaQueriesCoverage::test_get_scarico_ore_data_sorting
1 failed in 7.96s

```
</details>

---
### `tests/unit/test_e2e_workflows_hardened.py::TestE2EWorkflowsHardened::test_workflow_import_to_search`
**Error:** `FAILED tests/unit/test_e2e_workflows_hardened.py::TestE2EWorkflowsHardened::test_workflow_import_to_search`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
___________ TestE2EWorkflowsHardened.test_workflow_import_to_search ___________
tests\unit\test_e2e_workflows_hardened.py:57: in test_workflow_import_to_search
    assert success is True, f"Import fallito: {msg}"
E   AssertionError: Import fallito: Nessun anno importato (Controlla nomi fogli: YYYY o 'Dati/Preventivi').
E   assert False is True
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     85    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 328-332, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62      8    87%   37, 56, 59, 71, 93-94, 96-97
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210     70    67%   37-44, 77-80, 83-103, 121-123, 141-142, 145-146, 161-163, 214, 237-243, 262-266, 277-285, 309-310, 333-334, 355, 360-363, 371-374, 383-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228    159    30%   56, 75-90, 97-199, 203-233, 238, 273-275, 285, 313-318, 323-403, 408-410, 416-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   39-46, 73-75, 108-110, 116-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     42    31%   24, 28, 32, 39, 43, 47-50, 56-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170    111    35%   73-96, 102-132, 142-154, 166-233, 251, 264-265, 284, 289-290, 304-305, 314-316, 320-339, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    210    40%   27-51, 55-62, 66-74, 78, 82, 86-111, 115-174, 182-183, 205-206, 216, 230-232, 238-246, 269-271, 276-277, 285-287, 295-305, 313-320, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 434-460, 463-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     42    73%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 291-292, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     26    76%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 190, 195, 200, 205, 214, 224
src\core\contabilita_queries.py                                         87     44    49%   29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          85     74    13%   25-83, 93-181
src\core\contabilita_stats.py                                           57      4    93%   68-69, 89-90
src\core\contabilita_worker.py                                          91     17    81%   53, 61, 66-75, 87, 98-100, 105, 118, 135, 154
src\core\data_synchronizer.py                                           96      3    97%   94, 171-172
src\core\database.py                                                   139      7    95%   122-125, 139-140, 168-170
src\core\excel_importer.py                                             530    306    42%   23-24, 31-33, 137-138, 151-152, 162-164, 202, 204, 222, 240, 275-279, 296-298, 305-421, 434-490, 504-574, 583-658, 663-737, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 861, 868, 872-873, 880, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155    137    12%   21-63, 68-69, 74, 79, 84-106, 113-152, 160-205, 210-212, 217-226, 234, 242-317, 321-324
src\core\license_validator.py                                          173    127    27%   34-38, 47-54, 64-68, 94-121, 126-150, 155-162, 176-200, 211-212, 221-241, 246-264, 268-316, 321-324, 329-332
src\core\lyra_client.py                                                129    116    10%   21-37, 55-69, 73-162, 168-224, 230-268
src\core\lyra_sentinel.py                                               32      9    72%   37-38, 44-50
src\core\notification_manager.py                                        77     37    52%   38-45, 52-53, 79-81, 89-96, 100-109, 113-118, 122-125
src\core\secrets_manager.py                                             75     38    49%   29-58, 63, 68, 73, 78, 88-89, 96-97, 104-105, 112-113, 118-124
src\core\stats_manager.py                                               48     13    73%   33-40, 43, 56, 58, 71, 78
src\core\telegram_bridge.py                                            274    237    14%   27-29, 33-42, 46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    418    12%   46-56, 62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     55    85%   49-50, 307, 346, 354, 427, 465-466, 474-475, 484-486, 517-531, 534-547, 559-560, 584, 630-631, 639-647, 660, 729-730, 756-758, 793-794, 798
src\gui\contabilita_panel.py                                           244    216    11%   35-42, 45-50, 53-112, 115-153, 156-158, 161, 164-168, 172-193, 198-222, 225-229, 232, 235-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     16    57%   24-32, 54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     87    22%   26-98, 106-118, 123-124, 142-145, 149-151, 155-157, 161-183, 187-188
src\gui\controllers\search_controller.py                                96     73    24%   16-41, 50, 61-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35     27    23%   15-17, 21-44, 47-52, 58
src\gui\dashboard_panel.py                                             120    107    11%   31-50, 54-55, 59-66, 70-190, 194-318, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      1    96%   22
src\gui\help_panel.py                                                  105     84    20%   27-30, 33-153, 157-175, 178-192, 196-203, 207-210, 213, 235, 257, 285, 307, 324, 342, 359, 375, 392, 409, 425
src\gui\layouts\responsive.py                                           56     46    18%   15-18, 21-22, 25-26, 29-35, 38-42, 46-84
src\gui\lyra_panel.py                                                  330    289    12%   42-46, 49-67, 76-77, 80-89, 94-102, 105-368, 375-388, 392-397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 480-485, 489-511, 517-520, 524-545, 548-566, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232    175    25%   57-97, 102-148, 152-178, 182-188, 192-195, 201-206, 217-226, 230, 234-238, 242-296, 300-303, 309-313, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 362, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 410-420
src\gui\notifications_panel.py                                         194    174    10%   35-38, 41-135, 140-211, 218-227, 230-332, 335-336, 340-383, 386-389, 412-415, 418, 422-439
src\gui\panels.py                                                      975    321    67%   77-90, 94-98, 215, 252, 305, 372-376, 420-422, 426-427, 431-444, 449, 464-469, 474, 478, 494-498, 518-519, 557-561, 604-606, 609-617, 620-632, 636, 652-657, 664, 669-727, 745-749, 801-804, 808-815, 820, 824, 839-845, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1466, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    468    11%   36-38, 41-103, 107-122, 129-224, 227-232, 271-299, 302-315, 318-339, 342, 349-385, 391-398, 401-403, 406-408, 411-440, 443-448, 451-479, 486-488, 491-494, 499-537, 550-606, 609-615, 618-623, 626-631, 634, 637-638, 642-654, 657-662, 669-707, 711-801, 804-818, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 887-911, 914-919
src\gui\scarico_ore_panel.py                                           286    255    11%   39-41, 45-84, 91-101, 104-339, 345-347, 352-360, 364-390, 394-396, 400-421, 431-468, 472-480, 484-497, 501-515, 530-533, 537-550, 554-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155   1071     7%   51-105, 108-115, 118, 125-183, 190-191, 194-276, 279-305, 309-405, 419-429, 433-987, 990-1104, 1108-1121, 1127-1132, 1135-1281, 1285-1287, 1290-1297, 1300-1303, 1307-1329, 1333-1364, 1367-1368, 1371-1389, 1392, 1410, 1429, 1447-1448, 1469-1484, 1488, 1492-1494, 1498, 1502-1506, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1577-1584, 1587-1594, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1703-1707, 1711-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1772-1776, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1923-1980, 1984-2052, 2055-2062, 2065-2082
src\gui\styles.py                                                       58     42    28%   24-27, 32, 39-46, 50-83, 87-103, 108
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30     30     0%   1-55
src\gui\widgets\bot_parameters.py                                      112      8    93%   141, 144-146, 184-185, 191-192
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161    142    12%   48-50, 53-125, 128, 131-170, 173-190, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     91    18%   53-55, 58-101, 104, 107-125, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164    140    15%   41-44, 47-89, 93, 96-118, 121-142, 145-159, 164-169, 172-185, 188-210, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     19    42%   22-45
src\gui\widgets\contabilita\year_tab.py                                 46     34    26%   34-39, 42-80, 84, 88-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17     17     0%   1-28
src\gui\widgets\excel_table.py                                         313    208    34%   46-59, 63-70, 74-91, 95-138, 142-158, 162-188, 192-211, 215-271, 347-382, 391-397, 426, 435-438, 441-443, 481-486, 498-522
src\gui\widgets\info_widgets.py                                         91     39    57%   24-55, 58, 74-96, 144
src\gui\widgets\modern_button.py                                        62     11    82%   64-65, 70-73, 76-79, 138
src\gui\widgets\notification_item.py                                    61     52    15%   12-15, 18-113, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19     14    26%   8-15, 19-22, 26-42
src\gui\widgets\sidebar_widget.py                                       75     62    17%   18-32, 35-114, 117-131, 135-137
src\gui\widgets\status_card.py                                          68      2    97%   102-103
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 35-52, 55-60
src\gui\widgets\timeline_widget.py                                     226     66    71%   66-69, 72-75, 126-132, 135-141, 149-158, 162, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85     60    29%   41-54, 57-96, 100-114, 118-123, 134-136, 143-175, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29     21    28%   11-15, 18-29, 33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79     50    37%   21, 34-38, 54-76, 89-91, 96, 123-124, 132, 145-159, 173-175, 190-197, 212, 234
src\utils\log_humanizer.py                                              27      6    78%   73, 79, 81, 83, 87, 94
src\utils\parsing.py                                                    48      9    81%   22, 25, 48, 69, 91, 130-147
src\utils\printing.py                                                   82     65    21%   20-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33      9    73%   18, 35-38, 43-44, 49-50
src\utils\secure_logger.py                                              22     10    55%   39-46, 49-52
src\utils\security.py                                                   85     27    68%   38-41, 57-58, 83-87, 107, 109, 114-116, 121, 127-129, 133-139
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   7650    40%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_e2e_workflows_hardened.py::TestE2EWorkflowsHardened::test_workflow_import_to_search
1 failed in 7.43s

```
</details>

---
### `tests/unit/test_notification_manager_coverage.py::TestNotificationManagerCoverage::test_add_notification_and_signals`
**Error:** `FAILED tests/unit/test_notification_manager_coverage.py::TestNotificationManagerCoverage::test_add_notification_and_signals`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
______ TestNotificationManagerCoverage.test_add_notification_and_signals ______
C:\Program Files\Python312\Lib\unittest\mock.py:1581: in __enter__
    setattr(self.target, self.attribute, new_attr)
E   AttributeError: 'PyQt6.QtCore.pyqtBoundSignal' object attribute 'emit' is read-only

During handling of the above exception, another exception occurred:
tests\unit\test_notification_manager_coverage.py:19: in test_add_notification_and_signals
    mock_added = mocker.patch.object(manager.notification_added, "emit")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv\Lib\site-packages\pytest_mock\plugin.py:264: in object
    return self._start_patch(
.venv\Lib\site-packages\pytest_mock\plugin.py:229: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1594: in __enter__
    if not self.__exit__(*sys.exc_info()):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1605: in __exit__
    delattr(self.target, self.attribute)
E   AttributeError: 'PyQt6.QtCore.pyqtBoundSignal' object attribute 'emit' is read-only
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     85    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 328-332, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62      8    87%   37, 56, 59, 71, 93-94, 96-97
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210     70    67%   37-44, 77-80, 83-103, 121-123, 141-142, 145-146, 161-163, 214, 237-243, 262-266, 277-285, 309-310, 333-334, 355, 360-363, 371-374, 383-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228    159    30%   56, 75-90, 97-199, 203-233, 238, 273-275, 285, 313-318, 323-403, 408-410, 416-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   39-46, 73-75, 108-110, 116-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     42    31%   24, 28, 32, 39, 43, 47-50, 56-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170     91    46%   73-96, 102-132, 142-154, 178-193, 196, 207-231, 251, 264-265, 284, 289-290, 304-305, 314-316, 328-337, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    210    40%   27-51, 55-62, 66-74, 78, 82, 86-111, 115-174, 182-183, 205-206, 216, 230-232, 238-246, 269-271, 276-277, 285-287, 295-305, 313-320, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 434-460, 463-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     42    73%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 291-292, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     23    79%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 205, 214, 224
src\core\contabilita_queries.py                                         87      6    93%   52, 80, 96, 112, 119-120
src\core\contabilita_search.py                                          85     74    13%   25-83, 93-181
src\core\contabilita_stats.py                                           57      4    93%   68-69, 89-90
src\core\contabilita_worker.py                                          91     17    81%   53, 61, 66-75, 87, 98-100, 105, 118, 135, 154
src\core\data_synchronizer.py                                           96      3    97%   94, 171-172
src\core\database.py                                                   139      7    95%   122-125, 139-140, 168-170
src\core\excel_importer.py                                             530    119    78%   23-24, 31-33, 137-138, 151-152, 202, 204, 222, 275-279, 296-298, 311-319, 331, 419-421, 436, 443, 446, 450, 470, 477, 481, 513-521, 535-536, 539, 561, 573-574, 585, 588, 595-602, 619, 645, 657-658, 665, 676, 679, 694, 704, 725, 732, 735, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 872-873, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155     33    79%   103-106, 116, 152, 176-177, 190, 195, 204-205, 210-212, 220, 234, 251-256, 286-292, 313-314, 321-324
src\core\license_validator.py                                          173     16    91%   94-121, 148-150, 189
src\core\lyra_client.py                                                129     20    84%   22, 67-69, 113-115, 158-160, 215-216, 220-224, 258, 266-268
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      5    94%   43-45, 52-53
src\core\secrets_manager.py                                             75     37    51%   29-58, 63, 68, 73, 88-89, 96-97, 104-105, 112-113, 118-124
src\core\stats_manager.py                                               48      7    85%   36-38, 43, 56, 58, 71
src\core\telegram_bridge.py                                            274    226    18%   46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    407    14%   62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 346, 484-486, 517-531, 534-547, 584, 639-647, 660, 756-758, 798
src\gui\contabilita_panel.py                                           244     96    61%   47-50, 200-204, 208-211, 217-219, 225-229, 241-244, 250-251, 256-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     10    73%   54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     48    57%   51-54, 60-84, 98, 117-118, 123-124, 142-145, 149-151, 155-157, 175-176, 179-183, 187-188
src\gui\controllers\search_controller.py                                96     73    24%   16-41, 50, 61-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 58
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 274-287, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   184, 200, 203, 207-210
src\gui\layouts\responsive.py                                           56     23    59%   29-35, 38-42, 60-62, 65-73
src\gui\lyra_panel.py                                                  330    153    54%   42-46, 49-67, 80-89, 377-380, 397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 482, 489-511, 517-520, 539-540, 543-545, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232     86    63%   155, 158-159, 171-172, 182-188, 192-195, 201-206, 217-226, 230, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 411-417, 419-420
src\gui\notifications_panel.py                                         194     26    87%   142-143, 181-182, 203, 335-336, 340-383, 412-415, 418, 430-435
src\gui\panels.py                                                      975    273    72%   94-98, 215, 252, 305, 374-376, 420-422, 442, 449, 464-469, 474, 478, 494-498, 518-519, 559-561, 604-606, 632, 636, 652-657, 664, 669-727, 747-749, 804, 808-815, 820, 824, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    261    50%   41-103, 107-122, 129-224, 227-232, 290-296, 299, 303-304, 307, 342, 349-385, 391-398, 402, 407, 411-440, 451-479, 491-494, 499-537, 590, 598, 634, 637-638, 657-662, 716, 721, 729-730, 767, 775-778, 785-795, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 899, 907, 911, 914-919
src\gui\scarico_ore_panel.py                                           286    165    42%   39-41, 45-84, 345-347, 352-360, 364-390, 394-396, 400-421, 431-468, 472-480, 484-497, 511-515, 537-550, 555-556, 564-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155    380    67%   51-105, 108-115, 118, 125-183, 314-316, 371-372, 379-380, 1108-1121, 1127-1132, 1184-1186, 1285-1287, 1290-1297, 1300-1303, 1311-1313, 1322-1327, 1333-1364, 1488, 1498, 1502-1506, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1713-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1774-1775, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1954, 1959, 1964, 1969, 1985, 2037, 2046, 2055-2062, 2065-2082
src\gui\styles.py                                                       58      3    95%   94-95, 99
src\gui\toast.py                                                        45      4    91%   87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30      0   100%
src\gui\widgets\bot_parameters.py                                      112      3    97%   141, 184-185
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   148, 160-164, 189, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     46    59%   112-123, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164     41    75%   93, 125, 152, 168-169, 176, 181-182, 200-207, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     19    42%   22-45
src\gui\widgets\contabilita\year_tab.py                                 46      4    91%   84, 103-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         313     96    69%   63-70, 86, 98, 102, 115, 121, 124, 130-132, 142-158, 162-188, 194, 220, 238, 243-249, 253, 259, 347-382, 393, 426, 435-438, 441-443, 485-486, 506
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 74-96
src\gui\widgets\modern_button.py                                        62     10    84%   64-65, 70-73, 76-79
src\gui\widgets\notification_item.py                                    61     13    79%   27-28, 30-31, 33-34, 50, 77-78, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       75      7    91%   119-128
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   55-60
src\gui\widgets\timeline_widget.py                                     226     54    76%   72-75, 135-141, 149-158, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85      9    89%   152-156, 165, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29      7    76%   33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79      0   100%
src\utils\log_humanizer.py                                              27      0   100%
src\utils\parsing.py                                                    48      9    81%   22, 25, 48, 69, 91, 130-147
src\utils\printing.py                                                   82     65    21%   20-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33      9    73%   18, 35-38, 43-44, 49-50
src\utils\secure_logger.py                                              22      5    77%   44, 49-52
src\utils\security.py                                                   85     21    75%   38-41, 83-87, 107, 109, 114-116, 121, 127-129, 137-139
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   4422    66%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_notification_manager_coverage.py::TestNotificationManagerCoverage::test_add_notification_and_signals
1 failed in 5.55s

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
tests\unit\test_safework_bot_deep.py:78: in test_merge_all_session_logic
    mocker.patch.object(bot, "_setup_filters", return_value=True)
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
E   AttributeError: <MagicMock spec='SafeWorkPDLBot' id='2401962312000'> does not have the attribute '_setup_filters'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     85    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 328-332, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62      8    87%   37, 56, 59, 71, 93-94, 96-97
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210     70    67%   37-44, 77-80, 83-103, 121-123, 141-142, 145-146, 161-163, 214, 237-243, 262-266, 277-285, 309-310, 333-334, 355, 360-363, 371-374, 383-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228    159    30%   56, 75-90, 97-199, 203-233, 238, 273-275, 285, 313-318, 323-403, 408-410, 416-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   39-46, 73-75, 108-110, 116-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     42    31%   24, 28, 32, 39, 43, 47-50, 56-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170     91    46%   73-96, 102-132, 142-154, 178-193, 196, 207-231, 251, 264-265, 284, 289-290, 304-305, 314-316, 328-337, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    168    52%   27-51, 55-62, 66-74, 86-111, 115-174, 182-183, 205-206, 216, 230-232, 238-246, 269-271, 276-277, 285-287, 304-305, 316-317, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 435, 446-447, 457-460, 476-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     42    73%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 291-292, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     23    79%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 205, 214, 224
src\core\contabilita_queries.py                                         87      6    93%   52, 80, 96, 112, 119-120
src\core\contabilita_search.py                                          85     74    13%   25-83, 93-181
src\core\contabilita_stats.py                                           57      4    93%   68-69, 89-90
src\core\contabilita_worker.py                                          91     17    81%   53, 61, 66-75, 87, 98-100, 105, 118, 135, 154
src\core\data_synchronizer.py                                           96      3    97%   94, 171-172
src\core\database.py                                                   139      7    95%   122-125, 139-140, 168-170
src\core\excel_importer.py                                             530    119    78%   23-24, 31-33, 137-138, 151-152, 202, 204, 222, 275-279, 296-298, 311-319, 331, 419-421, 436, 443, 446, 450, 470, 477, 481, 513-521, 535-536, 539, 561, 573-574, 585, 588, 595-602, 619, 645, 657-658, 665, 676, 679, 694, 704, 725, 732, 735, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 872-873, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155     30    81%   103-106, 116, 152, 176-177, 190, 195, 204-205, 210-212, 220, 234, 254-256, 286-292, 313-314, 321-324
src\core\license_validator.py                                          173     16    91%   94-121, 148-150, 189
src\core\lyra_client.py                                                129     20    84%   22, 67-69, 113-115, 158-160, 215-216, 220-224, 258, 266-268
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      5    94%   43-45, 52-53
src\core\secrets_manager.py                                             75     37    51%   29-58, 63, 68, 73, 88-89, 96-97, 104-105, 112-113, 118-124
src\core\stats_manager.py                                               48      7    85%   36-38, 43, 56, 58, 71
src\core\telegram_bridge.py                                            274    226    18%   46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    407    14%   62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 346, 484-486, 517-531, 534-547, 584, 639-647, 660, 756-758, 798
src\gui\contabilita_panel.py                                           244     96    61%   47-50, 200-204, 208-211, 217-219, 225-229, 241-244, 250-251, 256-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     10    73%   54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     48    57%   51-54, 60-84, 98, 117-118, 123-124, 142-145, 149-151, 155-157, 175-176, 179-183, 187-188
src\gui\controllers\search_controller.py                                96     73    24%   16-41, 50, 61-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 58
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 274-287, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   184, 200, 203, 207-210
src\gui\layouts\responsive.py                                           56     23    59%   29-35, 38-42, 60-62, 65-73
src\gui\lyra_panel.py                                                  330    153    54%   42-46, 49-67, 80-89, 377-380, 397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 482, 489-511, 517-520, 539-540, 543-545, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232     86    63%   155, 158-159, 171-172, 182-188, 192-195, 201-206, 217-226, 230, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 411-417, 419-420
src\gui\notifications_panel.py                                         194      7    96%   181-182, 203, 335-336, 383, 418
src\gui\panels.py                                                      975    273    72%   94-98, 215, 252, 305, 374-376, 420-422, 442, 449, 464-469, 474, 478, 494-498, 518-519, 559-561, 604-606, 632, 636, 652-657, 664, 669-727, 747-749, 804, 808-815, 820, 824, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    261    50%   41-103, 107-122, 129-224, 227-232, 290-296, 299, 303-304, 307, 342, 349-385, 391-398, 402, 407, 411-440, 451-479, 491-494, 499-537, 590, 598, 634, 637-638, 657-662, 716, 721, 729-730, 767, 775-778, 785-795, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 899, 907, 911, 914-919
src\gui\scarico_ore_panel.py                                           286    165    42%   39-41, 45-84, 345-347, 352-360, 364-390, 394-396, 400-421, 431-468, 472-480, 484-497, 511-515, 537-550, 555-556, 564-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155    380    67%   51-105, 108-115, 118, 125-183, 314-316, 371-372, 379-380, 1108-1121, 1127-1132, 1184-1186, 1285-1287, 1290-1297, 1300-1303, 1311-1313, 1322-1327, 1333-1364, 1488, 1498, 1502-1506, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1713-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1774-1775, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1954, 1959, 1964, 1969, 1985, 2037, 2046, 2055-2062, 2065-2082
src\gui\styles.py                                                       58      3    95%   94-95, 99
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30      0   100%
src\gui\widgets\bot_parameters.py                                      112      3    97%   141, 184-185
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   148, 160-164, 189, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     46    59%   112-123, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164     41    75%   93, 125, 152, 168-169, 176, 181-182, 200-207, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     19    42%   22-45
src\gui\widgets\contabilita\year_tab.py                                 46      4    91%   84, 103-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         313     96    69%   63-70, 86, 98, 102, 115, 121, 124, 130-132, 142-158, 162-188, 194, 220, 238, 243-249, 253, 259, 347-382, 393, 426, 435-438, 441-443, 485-486, 506
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 74-96
src\gui\widgets\modern_button.py                                        62     10    84%   64-65, 70-73, 76-79
src\gui\widgets\notification_item.py                                    61     11    82%   27-28, 30-31, 33-34, 50, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       75      7    91%   119-128
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   55-60
src\gui\widgets\timeline_widget.py                                     226     54    76%   72-75, 135-141, 149-158, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85      9    89%   152-156, 165, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29      7    76%   33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79      0   100%
src\utils\log_humanizer.py                                              27      0   100%
src\utils\parsing.py                                                    48      4    92%   130-147
src\utils\printing.py                                                   82     14    83%   20-22, 36-38, 49-50, 114-119, 143-144
src\utils\resource_manager.py                                           33      1    97%   18
src\utils\secure_logger.py                                              22      5    77%   44, 49-52
src\utils\security.py                                                   85     12    86%   38-41, 83-87, 114-116
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   4279    67%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_safework_bot_deep.py::TestSafeWorkPDLBotDeep::test_merge_all_session_logic
1 failed in 8.54s

```
</details>

---
### `tests/unit/test_scarico_ore_panel_deep.py::TestScaricoOrePanelDeep::test_update_selection_totals`
**Error:** `FAILED tests/unit/test_scarico_ore_panel_deep.py::TestScaricoOrePanelDeep::test_update_selection_totals`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________ TestScaricoOrePanelDeep.test_update_selection_totals _____________
tests\unit\test_scarico_ore_panel_deep.py:21: in test_update_selection_totals
    panel.source_model.set_data(mock_data)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'ScaricoOreTableModel' object has no attribute 'set_data'. Did you mean: 'setData'?
---------------------------- Captured Qt messages -----------------------------
QtWarningMsg: "Unable to open monitor interface to \\\\.\\DISPLAY1:" "Operazione completata."
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     83    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 329-331, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62      8    87%   37, 56, 59, 71, 93-94, 96-97
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210     70    67%   37-44, 77-80, 83-103, 121-123, 141-142, 145-146, 161-163, 214, 237-243, 262-266, 277-285, 309-310, 333-334, 355, 360-363, 371-374, 383-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228     85    63%   56, 77, 82, 88, 103, 112, 116, 137, 181-183, 188-193, 197-199, 203-233, 238, 273-275, 285, 324-327, 335, 394-396, 399-400, 408-410, 416-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   39-46, 73-75, 108-110, 116-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     42    31%   24, 28, 32, 39, 43, 47-50, 56-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170     91    46%   73-96, 102-132, 142-154, 178-193, 196, 207-231, 251, 264-265, 284, 289-290, 304-305, 314-316, 328-337, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    130    63%   47-49, 61-62, 66-74, 93-94, 104, 107-108, 115-174, 205-206, 230-232, 238-246, 269-271, 276-277, 285-287, 316-317, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 435, 446-447, 457-460, 476-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     42    73%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 291-292, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     23    79%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 205, 214, 224
src\core\contabilita_queries.py                                         87      6    93%   52, 80, 96, 112, 119-120
src\core\contabilita_search.py                                          85     74    13%   25-83, 93-181
src\core\contabilita_stats.py                                           57      4    93%   68-69, 89-90
src\core\contabilita_worker.py                                          91     17    81%   53, 61, 66-75, 87, 98-100, 105, 118, 135, 154
src\core\data_synchronizer.py                                           96      3    97%   94, 171-172
src\core\database.py                                                   139      7    95%   122-125, 139-140, 168-170
src\core\excel_importer.py                                             530    119    78%   23-24, 31-33, 137-138, 151-152, 202, 204, 222, 275-279, 296-298, 311-319, 331, 419-421, 436, 443, 446, 450, 470, 477, 481, 513-521, 535-536, 539, 561, 573-574, 585, 588, 595-602, 619, 645, 657-658, 665, 676, 679, 694, 704, 725, 732, 735, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 872-873, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155     30    81%   103-106, 116, 152, 176-177, 190, 195, 204-205, 210-212, 220, 234, 254-256, 286-292, 313-314, 321-324
src\core\license_validator.py                                          173     16    91%   94-121, 148-150, 189
src\core\lyra_client.py                                                129     20    84%   22, 67-69, 113-115, 158-160, 215-216, 220-224, 258, 266-268
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      5    94%   43-45, 52-53
src\core\secrets_manager.py                                             75     37    51%   29-58, 63, 68, 73, 88-89, 96-97, 104-105, 112-113, 118-124
src\core\stats_manager.py                                               48      7    85%   36-38, 43, 56, 58, 71
src\core\telegram_bridge.py                                            274    226    18%   46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    407    14%   62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 346, 484-486, 517-531, 534-547, 584, 639-647, 660, 756-758, 798
src\gui\contabilita_panel.py                                           244     96    61%   47-50, 200-204, 208-211, 217-219, 225-229, 241-244, 250-251, 256-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     10    73%   54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     48    57%   51-54, 60-84, 98, 117-118, 123-124, 142-145, 149-151, 155-157, 175-176, 179-183, 187-188
src\gui\controllers\search_controller.py                                96     73    24%   16-41, 50, 61-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 58
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 274-287, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   184, 200, 203, 207-210
src\gui\layouts\responsive.py                                           56     23    59%   29-35, 38-42, 60-62, 65-73
src\gui\lyra_panel.py                                                  330    153    54%   42-46, 49-67, 80-89, 377-380, 397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 482, 489-511, 517-520, 539-540, 543-545, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232     86    63%   155, 158-159, 171-172, 182-188, 192-195, 201-206, 217-226, 230, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 411-417, 419-420
src\gui\notifications_panel.py                                         194      7    96%   181-182, 203, 335-336, 383, 418
src\gui\panels.py                                                      975    273    72%   94-98, 215, 252, 305, 374-376, 420-422, 442, 449, 464-469, 474, 478, 494-498, 518-519, 559-561, 604-606, 632, 636, 652-657, 664, 669-727, 747-749, 804, 808-815, 820, 824, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    207    61%   41-103, 107-122, 155-163, 172, 205, 208-209, 217-222, 227-232, 290-296, 299, 303-304, 307, 342, 374-380, 391-398, 411-440, 451-479, 491-494, 499-537, 590, 598, 634, 637-638, 657-662, 716, 721, 729-730, 767, 775-778, 785-795, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 899, 907, 911, 914-919
src\gui\scarico_ore_panel.py                                           286    138    52%   39-41, 45-84, 345-347, 356-358, 364-390, 394-396, 400-421, 445-446, 458-459, 467-468, 472-480, 488-489, 511-515, 537-550, 555-556, 564-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155    380    67%   51-105, 108-115, 118, 125-183, 314-316, 371-372, 379-380, 1108-1121, 1127-1132, 1184-1186, 1285-1287, 1290-1297, 1300-1303, 1311-1313, 1322-1327, 1333-1364, 1488, 1498, 1502-1506, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1713-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1774-1775, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1954, 1959, 1964, 1969, 1985, 2037, 2046, 2055-2062, 2065-2082
src\gui\styles.py                                                       58      3    95%   94-95, 99
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30      0   100%
src\gui\widgets\bot_parameters.py                                      112      3    97%   141, 184-185
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   148, 160-164, 189, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     46    59%   112-123, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164     41    75%   93, 125, 152, 168-169, 176, 181-182, 200-207, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     19    42%   22-45
src\gui\widgets\contabilita\year_tab.py                                 46      4    91%   84, 103-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         313     96    69%   63-70, 86, 98, 102, 115, 121, 124, 130-132, 142-158, 162-188, 194, 220, 238, 243-249, 253, 259, 347-382, 393, 426, 435-438, 441-443, 485-486, 506
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 74-96
src\gui\widgets\modern_button.py                                        62     10    84%   64-65, 70-73, 76-79
src\gui\widgets\notification_item.py                                    61     11    82%   27-28, 30-31, 33-34, 50, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       75      7    91%   119-128
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   55-60
src\gui\widgets\timeline_widget.py                                     226     54    76%   72-75, 135-141, 149-158, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85      9    89%   152-156, 165, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29      7    76%   33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79      0   100%
src\utils\log_humanizer.py                                              27      0   100%
src\utils\parsing.py                                                    48      4    92%   130-147
src\utils\printing.py                                                   82     14    83%   20-22, 36-38, 49-50, 114-119, 143-144
src\utils\resource_manager.py                                           33      1    97%   18
src\utils\secure_logger.py                                              22      5    77%   44, 49-52
src\utils\security.py                                                   85     12    86%   38-41, 83-87, 114-116
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   4084    68%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_scarico_ore_panel_deep.py::TestScaricoOrePanelDeep::test_update_selection_totals
1 failed in 8.16s

```
</details>

---
### `tests/unit/test_scarico_ore_panel_deep.py::TestScaricoOrePanelDeep::test_copy_selection_tsv_format`
**Error:** `FAILED tests/unit/test_scarico_ore_panel_deep.py::TestScaricoOrePanelDeep::test_copy_selection_tsv_format`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
___________ TestScaricoOrePanelDeep.test_copy_selection_tsv_format ____________
tests\unit\test_scarico_ore_panel_deep.py:59: in test_copy_selection_tsv_format
    panel.source_model.set_data(mock_data)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'ScaricoOreTableModel' object has no attribute 'set_data'. Did you mean: 'setData'?
---------------------------- Captured Qt messages -----------------------------
QtWarningMsg: "Unable to open monitor interface to \\\\.\\DISPLAY1:" "Operazione completata."
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     83    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 329-331, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62      8    87%   37, 56, 59, 71, 93-94, 96-97
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210     70    67%   37-44, 77-80, 83-103, 121-123, 141-142, 145-146, 161-163, 214, 237-243, 262-266, 277-285, 309-310, 333-334, 355, 360-363, 371-374, 383-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228     85    63%   56, 77, 82, 88, 103, 112, 116, 137, 181-183, 188-193, 197-199, 203-233, 238, 273-275, 285, 324-327, 335, 394-396, 399-400, 408-410, 416-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   39-46, 73-75, 108-110, 116-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     42    31%   24, 28, 32, 39, 43, 47-50, 56-111
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170     91    46%   73-96, 102-132, 142-154, 178-193, 196, 207-231, 251, 264-265, 284, 289-290, 304-305, 314-316, 328-337, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    130    63%   47-49, 61-62, 66-74, 93-94, 104, 107-108, 115-174, 205-206, 230-232, 238-246, 269-271, 276-277, 285-287, 316-317, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 435, 446-447, 457-460, 476-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     42    73%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 291-292, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     23    79%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 205, 214, 224
src\core\contabilita_queries.py                                         87      6    93%   52, 80, 96, 112, 119-120
src\core\contabilita_search.py                                          85     74    13%   25-83, 93-181
src\core\contabilita_stats.py                                           57      4    93%   68-69, 89-90
src\core\contabilita_worker.py                                          91     17    81%   53, 61, 66-75, 87, 98-100, 105, 118, 135, 154
src\core\data_synchronizer.py                                           96      3    97%   94, 171-172
src\core\database.py                                                   139      7    95%   122-125, 139-140, 168-170
src\core\excel_importer.py                                             530    119    78%   23-24, 31-33, 137-138, 151-152, 202, 204, 222, 275-279, 296-298, 311-319, 331, 419-421, 436, 443, 446, 450, 470, 477, 481, 513-521, 535-536, 539, 561, 573-574, 585, 588, 595-602, 619, 645, 657-658, 665, 676, 679, 694, 704, 725, 732, 735, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 872-873, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155     30    81%   103-106, 116, 152, 176-177, 190, 195, 204-205, 210-212, 220, 234, 254-256, 286-292, 313-314, 321-324
src\core\license_validator.py                                          173     16    91%   94-121, 148-150, 189
src\core\lyra_client.py                                                129     20    84%   22, 67-69, 113-115, 158-160, 215-216, 220-224, 258, 266-268
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      5    94%   43-45, 52-53
src\core\secrets_manager.py                                             75     37    51%   29-58, 63, 68, 73, 88-89, 96-97, 104-105, 112-113, 118-124
src\core\stats_manager.py                                               48      7    85%   36-38, 43, 56, 58, 71
src\core\telegram_bridge.py                                            274    226    18%   46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    407    14%   62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 346, 484-486, 517-531, 534-547, 584, 639-647, 660, 756-758, 798
src\gui\contabilita_panel.py                                           244     96    61%   47-50, 200-204, 208-211, 217-219, 225-229, 241-244, 250-251, 256-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     10    73%   54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     48    57%   51-54, 60-84, 98, 117-118, 123-124, 142-145, 149-151, 155-157, 175-176, 179-183, 187-188
src\gui\controllers\search_controller.py                                96     73    24%   16-41, 50, 61-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 58
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 274-287, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   184, 200, 203, 207-210
src\gui\layouts\responsive.py                                           56     23    59%   29-35, 38-42, 60-62, 65-73
src\gui\lyra_panel.py                                                  330    153    54%   42-46, 49-67, 80-89, 377-380, 397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 482, 489-511, 517-520, 539-540, 543-545, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232     86    63%   155, 158-159, 171-172, 182-188, 192-195, 201-206, 217-226, 230, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 411-417, 419-420
src\gui\notifications_panel.py                                         194      7    96%   181-182, 203, 335-336, 383, 418
src\gui\panels.py                                                      975    273    72%   94-98, 215, 252, 305, 374-376, 420-422, 442, 449, 464-469, 474, 478, 494-498, 518-519, 559-561, 604-606, 632, 636, 652-657, 664, 669-727, 747-749, 804, 808-815, 820, 824, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    207    61%   41-103, 107-122, 155-163, 172, 205, 208-209, 217-222, 227-232, 290-296, 299, 303-304, 307, 342, 374-380, 391-398, 411-440, 451-479, 491-494, 499-537, 590, 598, 634, 637-638, 657-662, 716, 721, 729-730, 767, 775-778, 785-795, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 899, 907, 911, 914-919
src\gui\scarico_ore_panel.py                                           286    138    52%   39-41, 45-84, 345-347, 356-358, 364-390, 394-396, 400-421, 445-446, 458-459, 467-468, 472-480, 488-489, 511-515, 537-550, 555-556, 564-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155    380    67%   51-105, 108-115, 118, 125-183, 314-316, 371-372, 379-380, 1108-1121, 1127-1132, 1184-1186, 1285-1287, 1290-1297, 1300-1303, 1311-1313, 1322-1327, 1333-1364, 1488, 1498, 1502-1506, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1713-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1774-1775, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1954, 1959, 1964, 1969, 1985, 2037, 2046, 2055-2062, 2065-2082
src\gui\styles.py                                                       58      3    95%   94-95, 99
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30      0   100%
src\gui\widgets\bot_parameters.py                                      112      3    97%   141, 184-185
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   148, 160-164, 189, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     46    59%   112-123, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164     41    75%   93, 125, 152, 168-169, 176, 181-182, 200-207, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     19    42%   22-45
src\gui\widgets\contabilita\year_tab.py                                 46      4    91%   84, 103-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         313     96    69%   63-70, 86, 98, 102, 115, 121, 124, 130-132, 142-158, 162-188, 194, 220, 238, 243-249, 253, 259, 347-382, 393, 426, 435-438, 441-443, 485-486, 506
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 74-96
src\gui\widgets\modern_button.py                                        62     10    84%   64-65, 70-73, 76-79
src\gui\widgets\notification_item.py                                    61     11    82%   27-28, 30-31, 33-34, 50, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       75      7    91%   119-128
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   55-60
src\gui\widgets\timeline_widget.py                                     226     54    76%   72-75, 135-141, 149-158, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85      9    89%   152-156, 165, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29      7    76%   33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79      0   100%
src\utils\log_humanizer.py                                              27      0   100%
src\utils\parsing.py                                                    48      4    92%   130-147
src\utils\printing.py                                                   82     14    83%   20-22, 36-38, 49-50, 114-119, 143-144
src\utils\resource_manager.py                                           33      1    97%   18
src\utils\secure_logger.py                                              22      5    77%   44, 49-52
src\utils\security.py                                                   85     12    86%   38-41, 83-87, 114-116
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   4084    68%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_scarico_ore_panel_deep.py::TestScaricoOrePanelDeep::test_copy_selection_tsv_format
1 failed in 8.03s

```
</details>

---
### `tests/unit/test_sprint_a_audit_backup.py::TestSprintAAuditBackup::test_audit_integrity_chain`
**Error:** `FAILED tests/unit/test_sprint_a_audit_backup.py::TestSprintAAuditBackup::test_audit_integrity_chain`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
______________ TestSprintAAuditBackup.test_audit_integrity_chain ______________
tests\unit\test_sprint_a_audit_backup.py:27: in test_audit_integrity_chain
    assert audit_mgr.verify_integrity() is True
E   assert False is True
E    +  where False = verify_integrity()
E    +    where verify_integrity = <src.core.audit_manager.AuditManager object at 0x00000223AD3680E0>.verify_integrity
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     83    70%   60, 65, 103-104, 113, 124-155, 200-202, 205-206, 210-213, 236-246, 289, 315-318, 324, 329-331, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62      8    87%   37, 56, 59, 71, 93-94, 96-97
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210     70    67%   37-44, 77-80, 83-103, 121-123, 141-142, 145-146, 161-163, 214, 237-243, 262-266, 277-285, 309-310, 333-334, 355, 360-363, 371-374, 383-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228     62    73%   56, 77, 82, 88, 112, 116, 137, 181-183, 188-193, 197-199, 203-233, 238, 273-275, 285, 324-327, 335, 394-396, 399-400, 408-410, 419-420, 426, 449-450, 462-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     44    58%   39-46, 73-75, 108-110, 153-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     14    77%   24, 28, 32, 39, 43, 57, 59-60, 65-66, 75, 79, 96-97
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170     78    54%   75, 94-95, 102-132, 142-154, 178-193, 196, 207-231, 251, 264-265, 284, 289-290, 304-305, 314-316, 328-337, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    130    63%   47-49, 61-62, 66-74, 93-94, 104, 107-108, 115-174, 205-206, 230-232, 238-246, 269-271, 276-277, 285-287, 316-317, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 435, 446-447, 457-460, 476-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     42    73%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 291-292, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     21    80%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 205
src\core\contabilita_queries.py                                         87      6    93%   52, 80, 96, 112, 119-120
src\core\contabilita_search.py                                          85     15    82%   26-27, 50, 80-81, 94, 110, 113-114, 124-125, 147-148, 178-179
src\core\contabilita_stats.py                                           57      4    93%   68-69, 89-90
src\core\contabilita_worker.py                                          91     17    81%   53, 61, 66-75, 87, 98-100, 105, 118, 135, 154
src\core\data_synchronizer.py                                           96      3    97%   94, 171-172
src\core\database.py                                                   139      7    95%   122-125, 139-140, 168-170
src\core\excel_importer.py                                             530    119    78%   23-24, 31-33, 137-138, 151-152, 202, 204, 222, 275-279, 296-298, 311-319, 331, 419-421, 436, 443, 446, 450, 470, 477, 481, 513-521, 535-536, 539, 561, 573-574, 585, 588, 595-602, 619, 645, 657-658, 665, 676, 679, 694, 704, 725, 732, 735, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 872-873, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155     30    81%   103-106, 116, 152, 176-177, 190, 195, 204-205, 210-212, 220, 234, 254-256, 286-292, 313-314, 321-324
src\core\license_validator.py                                          173     16    91%   94-121, 148-150, 189
src\core\lyra_client.py                                                129     20    84%   22, 67-69, 113-115, 158-160, 215-216, 220-224, 258, 266-268
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      5    94%   43-45, 52-53
src\core\secrets_manager.py                                             75      9    88%   47-48, 55-56, 68, 96-97, 104-105
src\core\stats_manager.py                                               48      7    85%   36-38, 43, 56, 58, 71
src\core\telegram_bridge.py                                            274    226    18%   46-127, 131-148, 151-161, 164-167, 170-171, 174-180, 183-189, 192-204, 207-213, 216-221, 225-277, 281-312, 317-323, 326-353, 356-368, 371-388
src\core\telegram_manager.py                                           475    407    14%   62-78, 82-91, 94-153, 157, 173, 176-186, 189-205, 212-215, 218-222, 227-283, 288-297, 300-339, 342-352, 355-390, 394-485, 493-538, 545-571, 578-583, 586-595, 602-615, 622, 638, 659-660, 663-664, 667-679, 684, 707-808, 812-930, 936-939, 942-952, 955-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 346, 484-486, 517-531, 534-547, 584, 639-647, 660, 756-758, 798
src\gui\contabilita_panel.py                                           244     96    61%   47-50, 200-204, 208-211, 217-219, 225-229, 241-244, 250-251, 256-260, 265-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     10    73%   54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     48    57%   51-54, 60-84, 98, 117-118, 123-124, 142-145, 149-151, 155-157, 175-176, 179-183, 187-188
src\gui\controllers\search_controller.py                                96     73    24%   16-41, 50, 61-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 58
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 274-287, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   184, 200, 203, 207-210
src\gui\layouts\responsive.py                                           56     23    59%   29-35, 38-42, 60-62, 65-73
src\gui\lyra_panel.py                                                  330    153    54%   42-46, 49-67, 80-89, 377-380, 397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 482, 489-511, 517-520, 539-540, 543-545, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232     86    63%   155, 158-159, 171-172, 182-188, 192-195, 201-206, 217-226, 230, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 411-417, 419-420
src\gui\notifications_panel.py                                         194      7    96%   181-182, 203, 335-336, 383, 418
src\gui\panels.py                                                      975    273    72%   94-98, 215, 252, 305, 374-376, 420-422, 442, 449, 464-469, 474, 478, 494-498, 518-519, 559-561, 604-606, 632, 636, 652-657, 664, 669-727, 747-749, 804, 808-815, 820, 824, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    207    61%   41-103, 107-122, 155-163, 172, 205, 208-209, 217-222, 227-232, 290-296, 299, 303-304, 307, 342, 374-380, 391-398, 411-440, 451-479, 491-494, 499-537, 590, 598, 634, 637-638, 657-662, 716, 721, 729-730, 767, 775-778, 785-795, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 899, 907, 911, 914-919
src\gui\scarico_ore_panel.py                                           286    138    52%   39-41, 45-84, 345-347, 356-358, 364-390, 394-396, 400-421, 445-446, 458-459, 467-468, 472-480, 488-489, 511-515, 537-550, 555-556, 564-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155    337    71%   108-115, 118, 125-183, 314-316, 371-372, 379-380, 1108-1121, 1127-1132, 1184-1186, 1285-1287, 1297, 1300-1303, 1311-1313, 1322-1327, 1333-1364, 1498, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1713-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1774-1775, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1954, 1959, 1964, 1969, 1985, 2037, 2046, 2055-2062, 2065-2082
src\gui\styles.py                                                       58      3    95%   94-95, 99
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30      0   100%
src\gui\widgets\bot_parameters.py                                      112      3    97%   141, 184-185
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   148, 160-164, 189, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     46    59%   112-123, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164     41    75%   93, 125, 152, 168-169, 176, 181-182, 200-207, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     19    42%   22-45
src\gui\widgets\contabilita\year_tab.py                                 46      4    91%   84, 103-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         313     96    69%   63-70, 86, 98, 102, 115, 121, 124, 130-132, 142-158, 162-188, 194, 220, 238, 243-249, 253, 259, 347-382, 393, 426, 435-438, 441-443, 485-486, 506
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 74-96
src\gui\widgets\modern_button.py                                        62     10    84%   64-65, 70-73, 76-79
src\gui\widgets\notification_item.py                                    61     11    82%   27-28, 30-31, 33-34, 50, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       75      7    91%   119-128
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   55-60
src\gui\widgets\timeline_widget.py                                     226     54    76%   72-75, 135-141, 149-158, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85      9    89%   152-156, 165, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29      7    76%   33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79      0   100%
src\utils\log_humanizer.py                                              27      0   100%
src\utils\parsing.py                                                    48      4    92%   130-147
src\utils\printing.py                                                   82     14    83%   20-22, 36-38, 49-50, 114-119, 143-144
src\utils\resource_manager.py                                           33      1    97%   18
src\utils\secure_logger.py                                              22      5    77%   44, 49-52
src\utils\security.py                                                   85     12    86%   38-41, 83-87, 114-116
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   3875    70%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_sprint_a_audit_backup.py::TestSprintAAuditBackup::test_audit_integrity_chain
1 failed in 5.13s

```
</details>

---
### `tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_selection_sum_calculation`
**Error:** `Timeout`

<details><summary>Full Output</summary>

```text
Windows fatal exception: access violation

Current thread 0x0000957c (most recent call first):
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\tests\unit\test_sprint_c_gui_deep.py", line 88 in test_selection_sum_calculation
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\python.py", line 166 in pytest_pyfunc_call
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_callers.py", line 121 in _multicall
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_manager.py", line 120 in _hookexec
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_hooks.py", line 512 in __call__
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\python.py", line 1720 in runtest
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\runner.py", line 179 in pytest_runtest_call
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_callers.py", line 121 in _multicall
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_manager.py", line 120 in _hookexec
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_hooks.py", line 512 in __call__
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\runner.py", line 245 in <lambda>
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\runner.py", line 353 in from_call
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\runner.py", line 244 in call_and_report
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\runner.py", line 137 in runtestprotocol
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\runner.py", line 118 in pytest_runtest_protocol
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_callers.py", line 121 in _multicall
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_manager.py", line 120 in _hookexec
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_hooks.py", line 512 in __call__
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\main.py", line 396 in pytest_runtestloop
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_callers.py", line 121 in _multicall
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_manager.py", line 120 in _hookexec
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_hooks.py", line 512 in __call__
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\main.py", line 372 in _main
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\main.py", line 318 in wrap_session
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\main.py", line 365 in pytest_cmdline_main
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_callers.py", line 121 in _multicall
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_manager.py", line 120 in _hookexec
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pluggy\_hooks.py", line 512 in __call__
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\config\__init__.py", line 199 in main
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\_pytest\config\__init__.py", line 223 in console_main
  File "C:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\.venv\Lib\site-packages\pytest\__main__.py", line 9 in <module>
  File "<frozen runpy>", line 88 in _run_code
  File "<frozen runpy>", line 198 in _run_module_as_main

```
</details>

---
### `tests/unit/test_telegram_manager_extended.py::TestTelegramManagerExtended::test_handle_text_input_db_query_state`
**Error:** `FAILED tests/unit/test_telegram_manager_extended.py::TestTelegramManagerExtended::test_handle_text_input_db_query_state`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
______ TestTelegramManagerExtended.test_handle_text_input_db_query_state ______
C:\Program Files\Python312\Lib\unittest\mock.py:1581: in __enter__
    setattr(self.target, self.attribute, new_attr)
E   AttributeError: 'PyQt6.QtCore.pyqtBoundSignal' object attribute 'emit' is read-only

During handling of the above exception, another exception occurred:
tests\unit\test_telegram_manager_extended.py:45: in test_handle_text_input_db_query_state
    mock_signal = mocker.patch.object(service.command_received, "emit")
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv\Lib\site-packages\pytest_mock\plugin.py:264: in object
    return self._start_patch(
.venv\Lib\site-packages\pytest_mock\plugin.py:229: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1594: in __enter__
    if not self.__exit__(*sys.exc_info()):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1605: in __exit__
    delattr(self.target, self.attribute)
E   AttributeError: 'PyQt6.QtCore.pyqtBoundSignal' object attribute 'emit' is read-only
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     73    74%   60, 65, 103-104, 113, 124-155, 202, 205-206, 210-213, 289, 315-318, 324, 329-331, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62      8    87%   37, 56, 59, 71, 93-94, 96-97
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210     70    67%   37-44, 77-80, 83-103, 121-123, 141-142, 145-146, 161-163, 214, 237-243, 262-266, 277-285, 309-310, 333-334, 355, 360-363, 371-374, 383-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228     62    73%   56, 77, 82, 88, 112, 116, 137, 181-183, 188-193, 197-199, 203-233, 238, 273-275, 285, 324-327, 335, 394-396, 399-400, 408-410, 419-420, 426, 449-450, 462-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     44    58%   39-46, 73-75, 108-110, 153-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     14    77%   24, 28, 32, 39, 43, 57, 59-60, 65-66, 75, 79, 96-97
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170     78    54%   75, 94-95, 102-132, 142-154, 178-193, 196, 207-231, 251, 264-265, 284, 289-290, 304-305, 314-316, 328-337, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    130    63%   47-49, 61-62, 66-74, 93-94, 104, 107-108, 115-174, 205-206, 230-232, 238-246, 269-271, 276-277, 285-287, 316-317, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 435, 446-447, 457-460, 476-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     42    73%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 291-292, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     21    80%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 205
src\core\contabilita_queries.py                                         87      6    93%   52, 80, 96, 112, 119-120
src\core\contabilita_search.py                                          85     15    82%   26-27, 50, 80-81, 94, 110, 113-114, 124-125, 147-148, 178-179
src\core\contabilita_stats.py                                           57      4    93%   68-69, 89-90
src\core\contabilita_worker.py                                          91     17    81%   53, 61, 66-75, 87, 98-100, 105, 118, 135, 154
src\core\data_synchronizer.py                                           96      3    97%   94, 171-172
src\core\database.py                                                   139      7    95%   122-125, 139-140, 168-170
src\core\excel_importer.py                                             530    119    78%   23-24, 31-33, 137-138, 151-152, 202, 204, 222, 275-279, 296-298, 311-319, 331, 419-421, 436, 443, 446, 450, 470, 477, 481, 513-521, 535-536, 539, 561, 573-574, 585, 588, 595-602, 619, 645, 657-658, 665, 676, 679, 694, 704, 725, 732, 735, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 872-873, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155     30    81%   103-106, 116, 152, 176-177, 190, 195, 204-205, 210-212, 220, 234, 254-256, 286-292, 313-314, 321-324
src\core\license_validator.py                                          173     16    91%   94-121, 148-150, 189
src\core\lyra_client.py                                                129     19    85%   22, 67-69, 113-115, 159-160, 215-216, 220-224, 258, 266-268
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      5    94%   43-45, 52-53
src\core\secrets_manager.py                                             75      9    88%   47-48, 55-56, 68, 96-97, 104-105
src\core\stats_manager.py                                               48      7    85%   36-38, 43, 56, 58, 71
src\core\telegram_bridge.py                                            274     53    81%   135-148, 158-159, 177-178, 186-187, 201-202, 212-213, 244-245, 259-260, 275-277, 331-344, 352-353, 358-359, 365-366, 373-374, 385-386
src\core\telegram_manager.py                                           475    309    35%   62-78, 82-91, 94-153, 177, 183-184, 189-205, 212-215, 218-222, 227-283, 289, 291, 300-339, 343, 345, 355-390, 496-502, 513-514, 523-538, 579, 659-660, 663-664, 667-679, 684, 725-808, 813, 815, 828, 830, 834, 836, 881-930, 936-939, 943-944, 951-952, 956-957, 967-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 346, 484-486, 517-531, 534-547, 584, 639-647, 660, 756-758, 798
src\gui\contabilita_panel.py                                           244     78    68%   47-50, 203-204, 225-229, 243-244, 250-251, 256-260, 267-271, 279-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     10    73%   54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     48    57%   51-54, 60-84, 98, 117-118, 123-124, 142-145, 149-151, 155-157, 175-176, 179-183, 187-188
src\gui\controllers\search_controller.py                                96     73    24%   16-41, 50, 61-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 58
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 274-287, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   184, 200, 203, 207-210
src\gui\layouts\responsive.py                                           56     23    59%   29-35, 38-42, 60-62, 65-73
src\gui\lyra_panel.py                                                  330    153    54%   42-46, 49-67, 80-89, 377-380, 397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 482, 489-511, 517-520, 539-540, 543-545, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232     86    63%   155, 158-159, 171-172, 182-188, 192-195, 201-206, 217-226, 230, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 411-417, 419-420
src\gui\notifications_panel.py                                         194      7    96%   181-182, 203, 335-336, 383, 418
src\gui\panels.py                                                      975    273    72%   94-98, 215, 252, 305, 374-376, 420-422, 442, 449, 464-469, 474, 478, 494-498, 518-519, 559-561, 604-606, 632, 636, 652-657, 664, 669-727, 747-749, 804, 808-815, 820, 824, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    207    61%   41-103, 107-122, 155-163, 172, 205, 208-209, 217-222, 227-232, 290-296, 299, 303-304, 307, 342, 374-380, 391-398, 411-440, 451-479, 491-494, 499-537, 590, 598, 634, 637-638, 657-662, 716, 721, 729-730, 767, 775-778, 785-795, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 899, 907, 911, 914-919
src\gui\scarico_ore_panel.py                                           286    138    52%   39-41, 45-84, 345-347, 356-358, 364-390, 394-396, 400-421, 445-446, 458-459, 467-468, 472-480, 488-489, 511-515, 537-550, 555-556, 564-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155    337    71%   108-115, 118, 125-183, 314-316, 371-372, 379-380, 1108-1121, 1127-1132, 1184-1186, 1285-1287, 1297, 1300-1303, 1311-1313, 1322-1327, 1333-1364, 1498, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1713-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1774-1775, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1954, 1959, 1964, 1969, 1985, 2037, 2046, 2055-2062, 2065-2082
src\gui\styles.py                                                       58      3    95%   94-95, 99
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30      0   100%
src\gui\widgets\bot_parameters.py                                      112      3    97%   141, 184-185
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   148, 160-164, 189, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     46    59%   112-123, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164     40    76%   125, 152, 168-169, 176, 181-182, 200-207, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     19    42%   22-45
src\gui\widgets\contabilita\year_tab.py                                 46      3    93%   103-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         313     96    69%   63-70, 86, 98, 102, 115, 121, 124, 130-132, 142-158, 162-188, 194, 220, 238, 243-249, 253, 259, 347-382, 393, 426, 435-438, 441-443, 485-486, 506
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 74-96
src\gui\widgets\modern_button.py                                        62     10    84%   64-65, 70-73, 76-79
src\gui\widgets\notification_item.py                                    61     11    82%   27-28, 30-31, 33-34, 50, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       75      7    91%   119-128
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   55-60
src\gui\widgets\timeline_widget.py                                     226     54    76%   72-75, 135-141, 149-158, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85      9    89%   152-156, 165, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29      7    76%   33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79      0   100%
src\utils\log_humanizer.py                                              27      0   100%
src\utils\parsing.py                                                    48      4    92%   130-147
src\utils\printing.py                                                   82     14    83%   20-22, 36-38, 49-50, 114-119, 143-144
src\utils\resource_manager.py                                           33      1    97%   18
src\utils\secure_logger.py                                              22      5    77%   44, 49-52
src\utils\security.py                                                   85     12    86%   38-41, 83-87, 114-116
src\utils\validators.py                                                 73     46    37%   35, 42-44, 52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   3568    72%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_manager_extended.py::TestTelegramManagerExtended::test_handle_text_input_db_query_state
1 failed in 12.58s

```
</details>

---
### `tests/unit/test_telegram_manager_extended.py::TestTelegramManagerExtended::test_process_with_ai_intent_detection`
**Error:** `FAILED tests/unit/test_telegram_manager_extended.py::TestTelegramManagerExtended::test_process_with_ai_intent_detection`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
______ TestTelegramManagerExtended.test_process_with_ai_intent_detection ______
C:\Program Files\Python312\Lib\unittest\mock.py:1581: in __enter__
    setattr(self.target, self.attribute, new_attr)
E   AttributeError: 'PyQt6.QtCore.pyqtBoundSignal' object attribute 'emit' is read-only

During handling of the above exception, another exception occurred:
tests\unit\test_telegram_manager_extended.py:69: in test_process_with_ai_intent_detection
    mock_intent_signal = mocker.patch.object(service.intent_received, "emit")
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv\Lib\site-packages\pytest_mock\plugin.py:264: in object
    return self._start_patch(
.venv\Lib\site-packages\pytest_mock\plugin.py:229: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1594: in __enter__
    if not self.__exit__(*sys.exc_info()):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1605: in __exit__
    delattr(self.target, self.attribute)
E   AttributeError: 'PyQt6.QtCore.pyqtBoundSignal' object attribute 'emit' is read-only
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    19      6    68%   100, 114-118
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              281     73    74%   60, 65, 103-104, 113, 124-155, 202, 205-206, 210-213, 289, 315-318, 324, 329-331, 338, 342, 355-357, 366, 370-378, 382-390, 409-413, 417
src\bots\base\login_page.py                                             95     56    41%   45-61, 65-95, 109-113, 117-123, 151-167, 172-177
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             45     14    69%   51, 55-67, 82, 85, 91
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   25-34, 44-46, 67-69, 102-104
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          62      8    87%   37, 56, 59, 71, 93-94, 96-97
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     210     70    67%   37-44, 77-80, 83-103, 121-123, 141-142, 145-146, 161-163, 214, 237-243, 262-266, 277-285, 309-310, 333-334, 355, 360-363, 371-374, 383-387
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           228     62    73%   56, 77, 82, 88, 112, 116, 137, 181-183, 188-193, 197-199, 203-233, 238, 273-275, 285, 324-327, 335, 394-396, 399-400, 408-410, 419-420, 426, 449-450, 462-471
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     44    58%   39-46, 73-75, 108-110, 153-155, 161-218
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     14    77%   24, 28, 32, 39, 43, 57, 59-60, 65-66, 75, 79, 96-97
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            72     46    36%   26, 30, 34, 47-63, 69-111, 118-119
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   41-59, 81-83, 87-154, 173-174, 191-192, 195, 216-217, 222-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       170     78    54%   75, 94-95, 102-132, 142-154, 178-193, 196, 207-231, 251, 264-265, 284, 289-290, 304-305, 314-316, 328-337, 348-349
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           350    130    63%   47-49, 61-62, 66-74, 93-94, 104, 107-108, 115-174, 205-206, 230-232, 238-246, 269-271, 276-277, 285-287, 316-317, 325-326, 348-353, 358-360, 367-369, 390-395, 399, 404-408, 413-428, 435, 446-447, 457-460, 476-477
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-75
src\core\app_updater.py                                                 38      1    97%   80
src\core\audit_manager.py                                              156     42    73%   91-92, 111-112, 118-127, 146-147, 209-210, 222-250, 266, 276-277, 291-292, 305-306
src\core\backup_manager.py                                             119      0   100%
src\core\config_manager.py                                             180      8    96%   205-206, 228-231, 266, 287
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     21    80%   28, 38, 66, 87-88, 97, 105, 120-121, 130-139, 148-157, 170, 205
src\core\contabilita_queries.py                                         87      6    93%   52, 80, 96, 112, 119-120
src\core\contabilita_search.py                                          85     15    82%   26-27, 50, 80-81, 94, 110, 113-114, 124-125, 147-148, 178-179
src\core\contabilita_stats.py                                           57      4    93%   68-69, 89-90
src\core\contabilita_worker.py                                          91     17    81%   53, 61, 66-75, 87, 98-100, 105, 118, 135, 154
src\core\data_synchronizer.py                                           96      3    97%   94, 171-172
src\core\database.py                                                   139      7    95%   122-125, 139-140, 168-170
src\core\excel_importer.py                                             530    119    78%   23-24, 31-33, 137-138, 151-152, 202, 204, 222, 275-279, 296-298, 311-319, 331, 419-421, 436, 443, 446, 450, 470, 477, 481, 513-521, 535-536, 539, 561, 573-574, 585, 588, 595-602, 619, 645, 657-658, 665, 676, 679, 694, 704, 725, 732, 735, 761, 782, 785-788, 800-801, 808, 812-813, 832, 849-850, 872-873, 883-889, 911-931, 949-950, 956-963
src\core\license_updater.py                                            155     30    81%   103-106, 116, 152, 176-177, 190, 195, 204-205, 210-212, 220, 234, 254-256, 286-292, 313-314, 321-324
src\core\license_validator.py                                          173     16    91%   94-121, 148-150, 189
src\core\lyra_client.py                                                129     19    85%   22, 67-69, 113-115, 159-160, 215-216, 220-224, 258, 266-268
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      5    94%   43-45, 52-53
src\core\secrets_manager.py                                             75      9    88%   47-48, 55-56, 68, 96-97, 104-105
src\core\stats_manager.py                                               48      7    85%   36-38, 43, 56, 58, 71
src\core\telegram_bridge.py                                            274     53    81%   135-148, 158-159, 177-178, 186-187, 201-202, 212-213, 244-245, 259-260, 275-277, 331-344, 352-353, 358-359, 365-366, 373-374, 385-386
src\core\telegram_manager.py                                           475    309    35%   62-78, 82-91, 94-153, 177, 183-184, 189-205, 212-215, 218-222, 227-283, 289, 291, 300-339, 343, 345, 355-390, 496-502, 513-514, 523-538, 579, 659-660, 663-664, 667-679, 684, 725-808, 813, 815, 828, 830, 834, 836, 881-930, 936-939, 943-944, 951-952, 956-957, 967-968, 971-984, 987-997, 1000-1011, 1014-1026
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                         24     17    29%   25-53
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 346, 484-486, 517-531, 534-547, 584, 639-647, 660, 756-758, 798
src\gui\contabilita_panel.py                                           244     78    68%   47-50, 203-204, 225-229, 243-244, 250-251, 256-260, 267-271, 279-319, 322-340, 343-344, 347-365
src\gui\controllers\bot_controller.py                                   37     10    73%   54-59, 63-66
src\gui\controllers\navigation_controller.py                           112     48    57%   51-54, 60-84, 98, 117-118, 123-124, 142-145, 149-151, 155-157, 175-176, 179-183, 187-188
src\gui\controllers\search_controller.py                                96     73    24%   16-41, 50, 61-62, 66-112, 116-131, 135-154
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-43, 47-66, 70, 76-86
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 58
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 274-287, 322-324
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   184, 200, 203, 207-210
src\gui\layouts\responsive.py                                           56     23    59%   29-35, 38-42, 60-62, 65-73
src\gui\lyra_panel.py                                                  330    153    54%   42-46, 49-67, 80-89, 377-380, 397, 400-424, 427-431, 434-451, 458-460, 463-466, 469-472, 476-477, 482, 489-511, 517-520, 539-540, 543-545, 570-585, 588-608, 616-667
src\gui\main_window.py                                                 232     86    63%   155, 158-159, 171-172, 182-188, 192-195, 201-206, 217-226, 230, 317-327, 331-332, 335-336, 339-346, 349-353, 356-358, 366, 370-376, 380-385, 389-393, 397-401, 404, 407, 411-417, 419-420
src\gui\notifications_panel.py                                         194      7    96%   181-182, 203, 335-336, 383, 418
src\gui\panels.py                                                      975    273    72%   94-98, 215, 252, 305, 374-376, 420-422, 442, 449, 464-469, 474, 478, 494-498, 518-519, 559-561, 604-606, 632, 636, 652-657, 664, 669-727, 747-749, 804, 808-815, 820, 824, 849-856, 872-873, 909-911, 948, 1020-1028, 1031-1034, 1040, 1046-1048, 1067-1077, 1080-1088, 1093-1100, 1107-1115, 1119-1122, 1168-1169, 1181, 1227, 1249-1251, 1285-1287, 1314, 1330-1335, 1344-1348, 1370-1371, 1388-1390, 1476, 1532-1533, 1600-1603, 1606-1609, 1613-1615, 1619-1664, 1669-1688, 1692-1757, 1762-1794
src\gui\scarico_ore_components.py                                      526    207    61%   41-103, 107-122, 155-163, 172, 205, 208-209, 217-222, 227-232, 290-296, 299, 303-304, 307, 342, 374-380, 391-398, 411-440, 451-479, 491-494, 499-537, 590, 598, 634, 637-638, 657-662, 716, 721, 729-730, 767, 775-778, 785-795, 823-834, 837-840, 843-865, 868-872, 875-879, 882-883, 899, 907, 911, 914-919
src\gui\scarico_ore_panel.py                                           286    138    52%   39-41, 45-84, 345-347, 356-358, 364-390, 394-396, 400-421, 445-446, 458-459, 467-468, 472-480, 488-489, 511-515, 537-550, 555-556, 564-570, 575-600, 604-607, 610-637
src\gui\settings_panel.py                                             1155    337    71%   108-115, 118, 125-183, 314-316, 371-372, 379-380, 1108-1121, 1127-1132, 1184-1186, 1285-1287, 1297, 1300-1303, 1311-1313, 1322-1327, 1333-1364, 1498, 1509-1520, 1523-1531, 1534-1545, 1548-1559, 1562-1573, 1598-1616, 1620-1625, 1628-1638, 1642-1666, 1672-1691, 1694-1700, 1713-1718, 1721-1729, 1732-1746, 1749-1760, 1763-1769, 1774-1775, 1779-1796, 1800-1808, 1811-1818, 1821-1828, 1832-1841, 1844-1851, 1854-1861, 1865-1870, 1873-1880, 1883-1890, 1894-1899, 1902-1909, 1912-1919, 1954, 1959, 1964, 1969, 1985, 2037, 2046, 2055-2062, 2065-2082
src\gui\styles.py                                                       58      3    95%   94-95, 99
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   30      0   100%
src\gui\widgets\bot_parameters.py                                      112      3    97%   141, 184-185
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   148, 160-164, 189, 193-227, 230-234, 237-252, 255-259
src\gui\widgets\contabilita\certificati_tab.py                         111     46    59%   112-123, 128-141, 144-151, 154-164, 168-274
src\gui\widgets\contabilita\giornaliere_tab.py                         164     40    76%   125, 152, 168-169, 176, 181-182, 200-207, 213-228, 231-247
src\gui\widgets\contabilita\helpers.py                                  33     19    42%   22-45
src\gui\widgets\contabilita\year_tab.py                                 46      3    93%   103-104, 108
src\gui\widgets\data_table.py                                          106     86    19%   43-47, 50-118, 121-122, 165-166, 169-194, 197-203, 207-215, 218-220, 224-241, 245, 249
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         313     96    69%   63-70, 86, 98, 102, 115, 121, 124, 130-132, 142-158, 162-188, 194, 220, 238, 243-249, 253, 259, 347-382, 393, 426, 435-438, 441-443, 485-486, 506
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 74-96
src\gui\widgets\modern_button.py                                        62     10    84%   64-65, 70-73, 76-79
src\gui\widgets\notification_item.py                                    61     11    82%   27-28, 30-31, 33-34, 50, 116-118, 121
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       75      7    91%   119-128
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   55-60
src\gui\widgets\timeline_widget.py                                     226     54    76%   72-75, 135-141, 149-158, 165-167, 170-172, 187-200, 220-225, 248-255, 283-285
src\gui\widgets\toast.py                                                85      9    89%   152-156, 165, 180, 184, 188, 192
src\gui\widgets\update_banner.py                                        29      7    76%   33-38, 41-43
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79      0   100%
src\utils\log_humanizer.py                                              27      0   100%
src\utils\parsing.py                                                    48      4    92%   130-147
src\utils\printing.py                                                   82     14    83%   20-22, 36-38, 49-50, 114-119, 143-144
src\utils\resource_manager.py                                           33      1    97%   18
src\utils\secure_logger.py                                              22      5    77%   44, 49-52
src\utils\security.py                                                   85     12    86%   38-41, 83-87, 114-116
src\utils\validators.py                                                 73     46    37%   35, 42-44, 52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                12818   3568    72%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_manager_extended.py::TestTelegramManagerExtended::test_process_with_ai_intent_detection
1 failed in 12.68s

```
</details>

---
