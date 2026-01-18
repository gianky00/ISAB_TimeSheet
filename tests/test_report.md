# 📊 Test Execution Report

**Date:** 2026-01-18 21:00:42
**Duration:** 207.02s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 474 |
| ✅ Passed | 141 |
| ❌ Failed | 1 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_base_bot_panel.py::TestBaseBotPanel::test_update_status`
**Error:** `FAILED tests/unit/test_base_bot_panel.py::TestBaseBotPanel::test_update_status`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_____________________ TestBaseBotPanel.test_update_status _____________________
C:\Program Files\Python312\Lib\unittest\mock.py:949: in assert_called_with
    raise AssertionError(_error_message()) from cause
E   AssertionError: expected call not found.
E   Expected: setStatus('#0d6efd', 'Bot is running')
E     Actual: setStatus('Bot is running', '#0d6efd')

During handling of the above exception, another exception occurred:
C:\Program Files\Python312\Lib\unittest\mock.py:961: in assert_called_once_with
    return self.assert_called_with(*args, **kwargs)
E   AssertionError: expected call not found.
E   Expected: setStatus('#0d6efd', 'Bot is running')
E     Actual: setStatus('Bot is running', '#0d6efd')
E
E   pytest introspection follows:
E
E   Args:
E   assert ('Bot is running', '#0d6efd') == ('#0d6efd', 'Bot is running')
E
E     At index 0 diff: 'Bot is running' != '#0d6efd'
E     Use -v to get more diff

During handling of the above exception, another exception occurred:
tests\unit\test_base_bot_panel.py:274: in test_update_status
    self.mock_status_card_instance.setStatus.assert_called_once_with(
E   AssertionError: expected call not found.
E   Expected: setStatus('#0d6efd', 'Bot is running')
E     Actual: setStatus('Bot is running', '#0d6efd')
E
E   pytest introspection follows:
E
E   Args:
E   assert ('Bot is running', '#0d6efd') == ('#0d6efd', 'Bot is running')
E
E     At index 0 diff: 'Bot is running' != '#0d6efd'
E     Use -v to get more diff
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      6    70%   112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              270     68    75%   71, 77, 127-128, 140, 164, 212-214, 228, 239, 255, 313-315, 327, 350-351, 357, 361-365, 371, 375, 379-396, 401, 405, 409-419, 423-433, 452-456, 461-465, 477
src\bots\base\login_page.py                                             94     74    21%   45-61, 65-95, 99-115, 119-125, 132-179
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     28    42%   52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     46    23%   28-30, 34-43, 47-56, 67-87, 98-130
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          65     43    34%   38, 42, 51-54, 60-67, 71-118
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     216    188    13%   40-43, 47, 51-58, 69-102, 113-133, 137-177, 181-194, 218-329, 333-354, 364-382, 386-398, 402-417, 421-434
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         239    211    12%   30-33, 37, 41-46, 58-89, 100-106, 111-118, 122-157, 163-206, 210-220, 229-260, 264-271, 275-298, 302-314, 318-334, 338-360, 364-392, 396-403
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           221    183    17%   55, 59, 71-74, 78-80, 84-99, 103-120, 124-140, 146-169, 173-209, 213-222, 226-257, 261-300, 306-328, 332-341, 347-366, 372-394, 398-413
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    148    13%   31-34, 37, 41-59, 63-83, 87-154, 158-223, 228-256, 260-273, 277-311
src\bots\portale_fornitori\timbrature\storage.py                       171    109    36%   73-96, 102-132, 142-154, 164-172, 177-194, 197-205, 210-224, 240-241, 255-257, 265, 269-270, 283-284, 288-307, 316-317
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           403    358    11%   25, 30, 35, 40, 45, 56-78, 82-89, 93-103, 107-132, 136-199, 203-208, 212-239, 243-272, 276-284, 288-319, 323-355, 359-371, 375-400, 404-420, 424-434, 438-459, 463-477, 484-527, 530-559, 562-578
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             72      6    92%   53, 97-102
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit_manager.py                                              164     33    80%   96-97, 119-123, 127-139, 156-157, 219-220, 242, 244, 261-263, 285, 295-296, 310-311, 324-325
src\core\backup_manager.py                                             140     30    79%   44, 47, 58-60, 70, 83, 92, 94, 109-111, 116, 120, 123, 179-188, 208-211, 219, 225-227, 234, 252-253
src\core\config_manager.py                                             177     63    64%   74, 111, 116-117, 124-125, 133-147, 156-157, 176-177, 199, 203-208, 225-228, 233-234, 246, 261, 271-284, 289-299, 304-308, 320-325, 330
src\core\constants.py                                                   70      0   100%
src\core\contabilita_manager.py                                        107     60    44%   28, 33, 38, 47-59, 76-136, 145-154, 163-172, 181-190, 195, 200, 205, 210, 215, 220, 229, 239, 244
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           61     42    31%   29-49, 54-82, 87-105
src\core\contabilita_worker.py                                          80     80     0%   1-174
src\core\data_synchronizer.py                                          104     79    24%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 175, 183, 194-210
src\core\database.py                                                   152     84    45%   56, 77-88, 97-129, 146-147, 150, 161-177, 185-246, 251-257, 265-284, 289-293, 303-334, 339-379
src\core\excel_importer.py                                             613    506    17%   23-24, 31-33, 130-148, 153-158, 163-170, 175-189, 194-214, 225-265, 272-289, 294-344, 349-352, 359-402, 407-419, 424-436, 441-479, 485-507, 519-539, 549-565, 572-592, 601-620, 625-635, 640-660, 666-683, 692-710, 715-735, 742-769, 775-798, 816-824, 829-842, 847-850, 856-880, 889-907, 912-916, 923-926, 931-947, 954-978, 983-987, 992-998, 1004-1031, 1036-1056, 1061-1063, 1068-1079, 1084-1104
src\core\license_updater.py                                            159    138    13%   22-64, 69-70, 75, 80, 85-102, 107-151, 156-200, 205-207, 212-218, 223-243, 248-255, 260-278, 283-292, 296-299
src\core\license_validator.py                                          197    148    25%   36-40, 49-56, 67-71, 97-124, 130-154, 159-166, 180-206, 216-243, 254-255, 264-288, 293-311, 316-364, 369-372, 377-380
src\core\lyra_client.py                                                128    128     0%   6-259
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                        77     55    29%   25-27, 30-32, 36-45, 49-53, 60-75, 79-81, 85, 93-100, 104-113, 117-122, 126-129
src\core\secrets_manager.py                                            102     63    38%   27-41, 45-51, 55-69, 73-75, 79-85, 90, 95, 100, 105, 110-116, 121-124, 131-132, 137-140, 145-151
src\core\stats_manager.py                                               48     36    25%   22-25, 29, 33-49, 53, 57-68, 72-80, 84
src\core\telegram_bridge.py                                            342    342     0%   1-530
src\core\telegram_manager.py                                           545    545     0%   1-1141
src\core\time_manager.py                                                19     14    26%   21-37, 50-56
src\core\timesheet_processor.py                                        104     83    20%   25-67, 72-82, 87-92, 99-109, 115-151, 156-166, 171-175
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       380    380     0%   8-922
src\gui\contabilita_panel.py                                           247    247     0%   6-424
src\gui\dashboard_panel.py                                             177    177     0%   1-407
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   93     78    16%   11-28, 38-69, 74, 86-92, 96-99, 105, 108, 111, 114-134, 137-142, 145-147, 151-168
src\gui\help_panel.py                                                  120    120     0%   6-370
src\gui\lyra_panel.py                                                  397    397     0%   1-809
src\gui\main_window.py                                                 372    372     0%   7-770
src\gui\notifications_panel.py                                         216    101    53%   221-222, 250-255, 263-272, 275-361, 364-365, 369-412, 415-418, 441-445, 448, 452-473
src\gui\panels.py                                                     1308   1027    21%   83-87, 91-104, 116-120, 124-126, 225-231, 242, 276, 323, 371, 375, 429-437, 440-444, 448-485, 489-491, 495, 499-512, 516-528, 532-537, 541-546, 560-562, 566-606, 613-621, 624-628, 632-669, 672-674, 678, 681-693, 696-708, 713-718, 722-728, 731-793, 800-808, 811-814, 818-855, 859-861, 864-872, 875-881, 884-894, 899-947, 959-967, 970-974, 979-1023, 1027-1030, 1034-1041, 1045-1053, 1057-1058, 1062-1118, 1130-1138, 1141-1145, 1149-1254, 1257-1265, 1268-1271, 1274-1287, 1290-1301, 1304-1314, 1318-1326, 1331-1338, 1341-1362, 1366-1380, 1384-1404, 1408-1422, 1426-1435, 1439-1463, 1467-1469, 1473-1487, 1491-1493, 1504-1511, 1514-1543, 1546-1551, 1554-1557, 1562-1567, 1578-1585, 1588-1590, 1597-1598, 1601-1611, 1618-1663, 1666-1752, 1756-1768, 1771, 1775-1786, 1790-1820, 1824-1831, 1835-1848, 1859-1868, 1871-1875, 1879-1906, 1909-1911, 1915-1916, 1919-1942, 1946-1964, 1968-1973, 1977-2027, 2030-2032, 2039-2064, 2068-2139, 2142-2160, 2164-2192, 2195-2250, 2254-2257, 2261-2268, 2272-2274, 2278-2323, 2328-2347, 2351-2416, 2419-2451
src\gui\scarico_ore_components.py                                      539    539     0%   1-1030
src\gui\scarico_ore_panel.py                                           269    269     0%   7-461
src\gui\settings_panel.py                                             1197   1197     0%   7-2181
src\gui\styles.py                                                       58      3    95%   95-96, 100
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   42     42     0%   1-101
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   11      6    45%   16-23
src\gui\widgets\data_table.py                                          108     86    20%   46-50, 53-127, 131, 135-136, 139-164, 167-173, 177-185, 188-190, 194-211, 215, 219
src\gui\widgets\excel_table.py                                         324    288    11%   29-38, 49-62, 66-73, 77-94, 98-118, 121-122, 125-126, 130-140, 144-168, 172-198, 202-221, 225-245, 249-260, 263-268, 271-275, 278-282, 291-293, 296-319, 322-381, 384-387, 390-396, 399-431, 434-437, 440-442, 445, 449-466, 475-500, 505-529
src\gui\widgets\footer_stats.py                                        440    440     0%   7-768
src\gui\widgets\info_widgets.py                                         95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                                        62     36    42%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-100, 104-109, 113-152
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-130, 134-136, 139
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      175    175     0%   1-328
src\gui\widgets\status_card.py                                          57     46    19%   19-90, 94-97, 106-122, 126-127
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     189    154    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 220-230, 233-248, 253-258, 261-265, 270-286, 289, 292, 297-324
src\gui\widgets\toast.py                                                91     64    30%   55-68, 72-111, 116-130, 140-145, 160-162, 181-218, 224, 229, 234, 239
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         64     21    67%   12-13, 22-31, 48-49, 65-66, 73-74, 84-86
src\utils\helpers.py                                                    94     55    41%   23, 36-40, 56-78, 91-93, 98, 125-126, 134, 147-161, 175-177, 192-199, 214, 236, 247, 253-256
src\utils\log_humanizer.py                                              27     18    33%   61-69, 74-93, 98-101
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   82     68    17%   17-22, 27-38, 46-50, 61-144
src\utils\resource_manager.py                                           33     33     0%   6-60
src\utils\secure_logger.py                                              22     10    55%   44-51, 54-57
src\utils\security.py                                                   85     30    65%   39-42, 58-59, 84-88, 108, 110, 115-117, 122, 125-130, 134-140
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                13941  11299    19%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_base_bot_panel.py::TestBaseBotPanel::test_update_status
1 failed in 4.55s

```
</details>

---
