# 📊 Test Execution Report

**Date:** 2026-01-17 12:44:18
**Duration:** 3.85s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1038 |
| ✅ Passed | 1034 |
| ❌ Failed | 4 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_safework_bot.py::TestSafeWorkBot::test_name_and_description`
**Error:** `FAILED tests/unit/test_safework_bot.py::TestSafeWorkBot::test_name_and_description`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________________ TestSafeWorkBot.test_name_and_description __________________
tests\unit\test_safework_bot.py:25: in test_name_and_description
    assert bot.name == "scarico_pdl"
E   AssertionError: assert 'Scarico PDL' == 'scarico_pdl'
E     
E     - scarico_pdl
E     + Scarico PDL
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      6    70%   112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266     54    80%   71, 77, 123-124, 136, 160, 219, 230, 244, 312, 335-336, 342, 346-350, 356, 360, 366, 375-377, 386, 390-398, 402-410, 429-433, 438-442, 454
src\bots\base\login_page.py                                             94      7    93%   89-93, 101, 150-151
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     15    69%   56, 60-72, 86, 92, 95, 101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   34-43, 52-54, 77-79, 116-118
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          65      9    86%   42, 61, 64, 77, 87, 104-105, 107-108
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     216     70    68%   49-56, 91-94, 105-119, 136-138, 152-153, 156-157, 170-172, 232, 251-257, 274-278, 287-295, 317-318, 332, 336-337, 340-342, 352-353, 355-356, 370-371, 381-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            87     73    16%   19, 26, 30, 42-51, 56-63, 68-159
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         250    226    10%   28-31, 35, 39-44, 56-85, 96-102, 107-114, 118-149, 153-190, 194-202, 211-240, 244-251, 255-278, 290-412
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           226    140    38%   59, 78-80, 84-99, 103-120, 124-138, 142-163, 167-195, 199-208, 212-237, 242, 272-274, 281, 289, 298-305, 310, 316-318, 333-335, 343-363, 367-382
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     57    45%   38-45, 64-66, 91-93, 97-126, 130-171
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     49    35%   26, 31, 36, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   39-57, 77-79, 83-146, 163-164, 175-176, 179, 198-199, 204-205, 210-236, 240-251, 255-285
src\bots\portale_fornitori\timbrature\storage.py                       171     90    47%   69-92, 98-126, 136-148, 174-183, 186-194, 199-210, 225-226, 240-242, 250, 254-255, 268-269, 279-288, 297-298
src\bots\safework\base.py                                               43     28    35%   22-50, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           403    223    45%   25, 30, 35, 45, 56-78, 82-89, 93-103, 107-132, 136-195, 203-204, 223-227, 239-240, 247, 252, 257-258, 277, 283, 292-294, 297-299, 302-307, 316, 327-329, 333, 341-343, 357, 364, 375-377, 381, 387-388, 392-406, 411, 419-420, 437-441, 444-445, 450-461, 469, 487-489, 500-505, 510-539, 542-556
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-76
src\core\app_updater.py                                                 46      2    96%   32, 85
src\core\audit_manager.py                                              156     30    81%   94-95, 114-130, 145-146, 202-203, 234, 236, 246-247, 271, 281-282, 294-295, 306-307
src\core\backup_manager.py                                             119     25    79%   41-42, 53, 68, 70, 84-86, 91, 98, 154-163, 183-186, 194, 200-202, 209, 227-228
src\core\config_manager.py                                             177     13    93%   111, 124-125, 136, 199, 207-208, 261, 278-279, 324-325, 330
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     22    79%   28, 38, 78, 99-100, 118, 131-132, 141-148, 157-162, 175, 208, 217, 225
src\core\contabilita_queries.py                                         87      4    95%   52, 80, 96, 112
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           61      4    93%   78-79, 100-101
src\core\contabilita_worker.py                                          80      4    95%   77, 91-92, 158
src\core\data_synchronizer.py                                           99      3    97%   97, 184-185
src\core\database.py                                                   141     10    93%   117-122, 132-133, 159-161
src\core\excel_importer.py                                             586     67    89%   23-24, 31-33, 135-136, 267, 307-309, 333, 338, 364-365, 376-380, 394, 403, 415, 478, 488, 504, 507, 511, 541, 570-571, 599-600, 640, 643, 655-656, 670, 707, 720, 761, 797, 836, 839-842, 850-851, 858, 862-863, 882, 896-897, 947-948, 958-960, 975, 990-991, 1007-1008, 1017-1019
src\core\license_updater.py                                            159     22    86%   99-102, 150, 166-167, 198-199, 204-206, 213, 230, 251-253, 289-291, 295-298
src\core\license_validator.py                                          197     19    90%   90-112, 136-138, 165, 185-186, 216
src\core\lyra_client.py                                                129     20    84%   22, 67-69, 105-107, 150-152, 203-204, 208-212, 244, 252-254
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      2    97%   52-53
src\core\secrets_manager.py                                            111     62    44%   27-42, 46-52, 56-70, 74-76, 80-86, 90-142, 147, 152, 157, 172-173, 180-181, 188-189, 196-197, 202-208
src\core\stats_manager.py                                               48      7    85%   42-44, 49, 62, 64, 77
src\core\telegram_bridge.py                                            333    273    18%   46-64, 68-81, 84-104, 107-126, 129-132, 136-155, 158-168, 171-174, 177-178, 181-187, 190-196, 199-220, 223-229, 232-237, 241-256, 259-265, 268-281, 284-297, 301-306, 310-316, 320-326, 330-356, 360-373, 377-384, 387-393, 396-419, 422-434, 437-454
src\core\telegram_manager.py                                           529    434    18%   62-77, 81-88, 92-108, 112-126, 129, 132-139, 142-155, 159-169, 173-179, 183, 197, 200-210, 213-228, 235-238, 241-245, 248-271, 274-281, 284-288, 291-309, 312-321, 324-363, 366-376, 380-403, 407-408, 412-414, 418-490, 498-535, 542-560, 567-572, 575-584, 591-600, 607, 619, 632-633, 636-637, 640-648, 651, 670-681, 685-704, 707-712, 719-720, 725-728, 741-758, 763-776, 780-795, 798-805, 808-813, 816-819, 822-827, 830-840, 843-848, 851-856, 859-868, 872-875, 884-894, 904-915, 925-936, 939-949, 952-963, 966-978
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                        104     83    20%   25-65, 70-80, 85-90, 95-105, 111-147, 152-162, 167-171
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 342, 466-468, 499-513, 516-529, 564, 619-627, 638, 730-732, 770
src\gui\contabilita_panel.py                                           256     69    73%   48-52, 194-198, 202-205, 211-213, 219-223, 236, 238, 244-245, 250-254, 265-267, 275-276, 287, 294, 305-306, 311, 315-333, 336-337, 340-356
src\gui\controllers\bot_controller.py                                   37      8    78%   59-67
src\gui\controllers\navigation_controller.py                           121     27    78%   59-62, 73-85, 134-135, 166-168, 172-174, 193-194, 197-201
src\gui\controllers\search_controller.py                               116     84    28%   18-41, 56, 66-67, 71-81, 85-94, 98-107, 111-120, 124-138, 142-161
src\gui\controllers\service_controller.py                               43     34    21%   18-21, 26-41, 45-64, 68, 72-82
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 56
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 270-283, 314-316
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   176, 192, 195, 199-202
src\gui\layouts\responsive.py                                           54      7    87%   29-35, 59
src\gui\lyra_panel.py                                                  335    155    54%   56-60, 64-82, 99-108, 398-401, 414, 418-440, 444-448, 452-467, 475-477, 481-484, 488-491, 495-496, 502, 515-535, 542-545, 571-572, 575-577, 603-618, 622-640, 648-661, 665-677, 681-692, 696-701
src\gui\main_window.py                                                 259    100    61%   163, 166-167, 179-180, 190-197, 201-217, 221-224, 228-233, 242-249, 253, 346-356, 360-361, 364-365, 368-375, 378-382, 385-387, 396, 400-406, 410-415, 419-423, 427-431, 435, 439, 447-453, 455-456
src\gui\notifications_panel.py                                         208      7    97%   175-176, 195, 324-325, 372, 408
src\gui\panels.py                                                     1072    222    79%   113-117, 224, 261, 419-421, 463-465, 484, 491, 502-504, 545-549, 593-595, 636-638, 657, 661, 673-675, 683, 688-748, 768-769, 811-813, 819, 836-846, 851-899, 924-926, 981, 985-990, 996, 1000, 1006-1007, 1023-1030, 1046-1047, 1090-1092, 1129, 1201-1209, 1212-1215, 1221, 1227-1229, 1242-1252, 1256-1264, 1269-1276, 1283-1287, 1291-1294, 1338-1339, 1355, 1403, 1425-1427, 1459-1461, 1485, 1496-1501, 1510-1514, 1536-1537, 1558-1560, 1645, 1701-1702, 1767-1770, 1774-1776, 1803-1810, 1813-1820, 1921, 1926, 1942-1943
src\gui\scarico_ore_components.py                                      531    251    53%   43-104, 115-130, 141-157, 168-180, 192-200, 211-216, 227-232, 244-249, 313-319, 322, 332-333, 336, 373, 377-379, 386-420, 426-433, 438, 444, 449-478, 488-516, 539-542, 554-592, 655, 663, 703, 707-708, 729-734, 805, 809, 816-817, 836-839, 867-870, 875-879, 903-914, 918-921, 925-947, 951-955, 959-963, 967-968, 985, 993, 997, 1001-1006
src\gui\scarico_ore_panel.py                                           263    160    39%   40-42, 47-81, 197-199, 203-211, 215-238, 242-244, 248-266, 277-306, 310-315, 319-331, 343-344, 353-360, 365-366, 373-378, 382-401, 405-408, 412-433
src\gui\settings_panel.py                                             1145    380    67%   50-104, 107-114, 117, 124-182, 303-305, 351-352, 359-360, 1042-1055, 1059-1064, 1116-1118, 1215-1217, 1220-1227, 1230-1233, 1241-1243, 1252-1257, 1263-1294, 1418, 1428, 1432-1436, 1439-1450, 1453-1461, 1464-1475, 1478-1489, 1492-1503, 1528-1544, 1548-1553, 1556-1566, 1570-1594, 1598-1617, 1620-1626, 1639-1644, 1647-1655, 1658-1670, 1673-1684, 1687-1693, 1698-1699, 1703-1720, 1724-1728, 1731-1736, 1739-1746, 1750-1757, 1760-1765, 1768-1772, 1776-1781, 1784-1789, 1792-1796, 1800-1805, 1808-1813, 1816-1823, 1856, 1861, 1866, 1871, 1887, 1918, 1927, 1936-1943, 1946-1963
src\gui\styles.py                                                       58      3    95%   89-90, 94
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   33      0   100%
src\gui\widgets\bot_parameters.py                                      112      5    96%   145, 164, 175, 197-198
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   152, 162-166, 191, 196-220, 223-227, 231-242, 245-249
src\gui\widgets\contabilita\certificati_tab.py                         111     38    66%   125, 127, 133-143, 146-153, 156-161, 165-264
src\gui\widgets\contabilita\giornaliere_tab.py                         164     41    75%   94, 121, 145, 159-160, 167, 172-173, 188-191, 195-210, 213-229
src\gui\widgets\contabilita\helpers.py                                  33     12    64%   22-25, 29-34, 40-41
src\gui\widgets\contabilita\year_tab.py                                 46      4    91%   86, 103-104, 108
src\gui\widgets\data_table.py                                          106      0   100%
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         324     95    71%   61-68, 84, 95, 99, 106, 112, 139-155, 159-181, 187, 212, 217, 234-237, 244-249, 261, 337-372, 383, 416, 425-428, 431-433, 482-483, 504, 517
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 76-100
src\gui\widgets\modern_button.py                                        62     10    84%   68-69, 75-78, 82-85
src\gui\widgets\notification_item.py                                    61      9    85%   33-34, 36-37, 56, 117-119, 122
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       53      0   100%
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   63-68
src\gui\widgets\timeline_widget.py                                     238     59    75%   76-79, 139-145, 153-164, 172-174, 178-180, 197-216, 238-243, 271-281, 313
src\gui\widgets\toast.py                                                85      9    89%   174-178, 187, 201, 206, 211, 216
src\gui\widgets\update_banner.py                                        29      7    76%   33-36, 39-41
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79     17    78%   36, 69-70, 125, 138-152, 227
src\utils\log_humanizer.py                                              16      0   100%
src\utils\parsing.py                                                    53      4    92%   102-119
src\utils\printing.py                                                   82     14    83%   20-22, 36-38, 49-50, 112-115, 139-140
src\utils\resource_manager.py                                           33      1    97%   18
src\utils\secure_logger.py                                              22      5    77%   42, 47-50
src\utils\security.py                                                   85     12    86%   39-42, 83-87, 114-116
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                13654   4413    68%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_safework_bot.py::TestSafeWorkBot::test_name_and_description
1 failed in 9.06s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x000001C4A25C71A0>
Traceback (most recent call last):
  File "C:\Users\Coemi\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\Coemi\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
    if not left_dir.resolve().exists():
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\pathlib.py", line 860, in exists
    self.stat(follow_symlinks=follow_symlinks)
  File "C:\Program Files\Python312\Lib\pathlib.py", line 840, in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Accesso negato: 'C:\\Users\\Coemi\\AppData\\Local\\Temp\\pytest-of-Allegretti\\pytest-current'

```
</details>

---
### `tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_data_pdl`
**Error:** `FAILED tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_data_pdl`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________________ TestTelegramUIBridge.test_handle_data_pdl __________________
C:\Program Files\Python312\Lib\unittest\mock.py:949: in assert_called_with
    raise AssertionError(_error_message()) from cause
E   AssertionError: expected call not found.
E   Expected: navigate_to_panel(<MagicMock name='mock.pdl_panel.bot_id' id='1885935844336'>)
E     Actual: navigate_to_panel('scarico_pdl')

During handling of the above exception, another exception occurred:
C:\Program Files\Python312\Lib\unittest\mock.py:961: in assert_called_once_with
    return self.assert_called_with(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AssertionError: expected call not found.
E   Expected: navigate_to_panel(<MagicMock name='mock.pdl_panel.bot_id' id='1885935844336'>)
E     Actual: navigate_to_panel('scarico_pdl')
E   
E   pytest introspection follows:
E   
E   Args:
E   assert ('scarico_pdl',) == (<MagicMock n...5935844336'>,)
E     
E     At index 0 diff: 'scarico_pdl' != <MagicMock name='mock.pdl_panel.bot_id' id='1885935844336'>
E     Use -v to get more diff

During handling of the above exception, another exception occurred:
tests\unit\test_telegram_bridge.py:442: in test_handle_data_pdl
    self.mock_main_window.navigate_to_panel.assert_called_once_with(
E   AssertionError: expected call not found.
E   Expected: navigate_to_panel(<MagicMock name='mock.pdl_panel.bot_id' id='1885935844336'>)
E     Actual: navigate_to_panel('scarico_pdl')
E   
E   pytest introspection follows:
E   
E   Args:
E   assert ('scarico_pdl',) == (<MagicMock n...5935844336'>,)
E     
E     At index 0 diff: 'scarico_pdl' != <MagicMock name='mock.pdl_panel.bot_id' id='1885935844336'>
E     Use -v to get more diff
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      6    70%   112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266     52    80%   71, 77, 123-124, 136, 160, 219, 230, 244, 312, 335-336, 342, 347-349, 356, 360, 366, 375-377, 386, 390-398, 402-410, 429-433, 438-442, 454
src\bots\base\login_page.py                                             94      7    93%   89-93, 101, 150-151
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     15    69%   56, 60-72, 86, 92, 95, 101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   34-43, 52-54, 77-79, 116-118
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          65      9    86%   42, 61, 64, 77, 87, 104-105, 107-108
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     216     70    68%   49-56, 91-94, 105-119, 136-138, 152-153, 156-157, 170-172, 232, 251-257, 274-278, 287-295, 317-318, 332, 336-337, 340-342, 352-353, 355-356, 370-371, 381-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            87     73    16%   19, 26, 30, 42-51, 56-63, 68-159
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         250    226    10%   28-31, 35, 39-44, 56-85, 96-102, 107-114, 118-149, 153-190, 194-202, 211-240, 244-251, 255-278, 290-412
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           226     41    82%   59, 78-80, 91, 97, 107, 118-120, 152, 160-161, 168, 207, 213, 222-233, 242, 281, 289, 303-305, 310, 316-318, 358-361, 377-382
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     20    81%   44-45, 64-66, 91-93, 124-126, 147, 158-160, 166-171
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     14    77%   25, 30, 35, 42, 46, 60, 62-63, 68-69, 78, 82, 95-96
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     49    35%   26, 31, 36, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   39-57, 77-79, 83-146, 163-164, 175-176, 179, 198-199, 204-205, 210-236, 240-251, 255-285
src\bots\portale_fornitori\timbrature\storage.py                       171     77    55%   71, 90-91, 98-126, 136-148, 174-183, 186-194, 199-210, 225-226, 240-242, 250, 254-255, 268-269, 279-288, 297-298
src\bots\safework\base.py                                               43     19    56%   23, 29-30, 46-47, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           403    128    68%   25, 30, 35, 45, 74-76, 88-89, 93-103, 114-115, 125, 128-129, 136-195, 226-227, 239-240, 283, 292-294, 306-307, 316, 327-329, 341-343, 364, 375-377, 387-388, 392-406, 411, 419-420, 440-441, 444-445, 460-461, 469, 487-489, 500-505, 511, 525-526, 536-538
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-76
src\core\app_updater.py                                                 46      2    96%   32, 85
src\core\audit_manager.py                                              156     30    81%   94-95, 114-130, 145-146, 202-203, 234, 236, 246-247, 271, 281-282, 294-295, 306-307
src\core\backup_manager.py                                             119     24    80%   41-42, 53, 68, 70, 84-86, 91, 98, 154-163, 183-186, 194, 200-202, 227-228
src\core\config_manager.py                                             177     13    93%   111, 124-125, 136, 199, 207-208, 261, 278-279, 324-325, 330
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     20    81%   28, 38, 78, 99-100, 118, 131-132, 141-148, 157-162, 175, 208
src\core\contabilita_queries.py                                         87      4    95%   52, 80, 96, 112
src\core\contabilita_search.py                                          91     14    85%   26-27, 50, 78-79, 109-110, 119, 122-123, 132-133, 151-152
src\core\contabilita_stats.py                                           61      4    93%   78-79, 100-101
src\core\contabilita_worker.py                                          80      4    95%   77, 91-92, 158
src\core\data_synchronizer.py                                           99      3    97%   97, 184-185
src\core\database.py                                                   141     10    93%   117-122, 132-133, 159-161
src\core\excel_importer.py                                             586     67    89%   23-24, 31-33, 135-136, 267, 307-309, 333, 338, 364-365, 376-380, 394, 403, 415, 478, 488, 504, 507, 511, 541, 570-571, 599-600, 640, 643, 655-656, 670, 707, 720, 761, 797, 836, 839-842, 850-851, 858, 862-863, 882, 896-897, 947-948, 958-960, 975, 990-991, 1007-1008, 1017-1019
src\core\license_updater.py                                            159     22    86%   99-102, 150, 166-167, 198-199, 204-206, 213, 230, 251-253, 289-291, 295-298
src\core\license_validator.py                                          197     19    90%   90-112, 136-138, 165, 185-186, 216
src\core\lyra_client.py                                                129     19    85%   22, 67-69, 105-107, 151-152, 203-204, 208-212, 244, 252-254
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      2    97%   52-53
src\core\secrets_manager.py                                            111     13    88%   66-69, 84-85, 140-142, 188-189, 196-197
src\core\stats_manager.py                                               48      4    92%   49, 62, 64, 77
src\core\telegram_bridge.py                                            333    104    69%   100, 122, 140-155, 165-166, 184-185, 193-194, 199-220, 223-229, 250-251, 255-256, 265, 276, 281, 285-286, 297, 303-306, 320-326, 330-356, 401-412, 418-419, 424-425, 431-432, 439-440, 451-452
src\core\telegram_manager.py                                           529    434    18%   62-77, 81-88, 92-108, 112-126, 129, 132-139, 142-155, 159-169, 173-179, 183, 197, 200-210, 213-228, 235-238, 241-245, 248-271, 274-281, 284-288, 291-309, 312-321, 324-363, 366-376, 380-403, 407-408, 412-414, 418-490, 498-535, 542-560, 567-572, 575-584, 591-600, 607, 619, 632-633, 636-637, 640-648, 651, 670-681, 685-704, 707-712, 719-720, 725-728, 741-758, 763-776, 780-795, 798-805, 808-813, 816-819, 822-827, 830-840, 843-848, 851-856, 859-868, 872-875, 884-894, 904-915, 925-936, 939-949, 952-963, 966-978
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                        104     83    20%   25-65, 70-80, 85-90, 95-105, 111-147, 152-162, 167-171
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 342, 466-468, 499-513, 516-529, 564, 619-627, 638, 730-732, 770
src\gui\contabilita_panel.py                                           256     56    78%   48-52, 197-198, 219-223, 238, 244-245, 250-254, 275-276, 287, 294, 305-306, 311, 315-333, 336-337, 340-356
src\gui\controllers\bot_controller.py                                   37      8    78%   59-67
src\gui\controllers\navigation_controller.py                           121     27    78%   59-62, 73-85, 134-135, 166-168, 172-174, 193-194, 197-201
src\gui\controllers\search_controller.py                               116     12    90%   56, 80-81, 86, 99, 112, 127, 137-138, 152, 160-161
src\gui\controllers\service_controller.py                               43      0   100%
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 56
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 270-283, 314-316
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   176, 192, 195, 199-202
src\gui\layouts\responsive.py                                           54      7    87%   29-35, 59
src\gui\lyra_panel.py                                                  335    155    54%   56-60, 64-82, 99-108, 398-401, 414, 418-440, 444-448, 452-467, 475-477, 481-484, 488-491, 495-496, 502, 515-535, 542-545, 571-572, 575-577, 603-618, 622-640, 648-661, 665-677, 681-692, 696-701
src\gui\main_window.py                                                 259    100    61%   163, 166-167, 179-180, 190-197, 201-217, 221-224, 228-233, 242-249, 253, 346-356, 360-361, 364-365, 368-375, 378-382, 385-387, 396, 400-406, 410-415, 419-423, 427-431, 435, 439, 447-453, 455-456
src\gui\notifications_panel.py                                         208      7    97%   175-176, 195, 324-325, 372, 408
src\gui\panels.py                                                     1072    222    79%   113-117, 224, 261, 419-421, 463-465, 484, 491, 502-504, 545-549, 593-595, 636-638, 657, 661, 673-675, 683, 688-748, 768-769, 811-813, 819, 836-846, 851-899, 924-926, 981, 985-990, 996, 1000, 1006-1007, 1023-1030, 1046-1047, 1090-1092, 1129, 1201-1209, 1212-1215, 1221, 1227-1229, 1242-1252, 1256-1264, 1269-1276, 1283-1287, 1291-1294, 1338-1339, 1355, 1403, 1425-1427, 1459-1461, 1485, 1496-1501, 1510-1514, 1536-1537, 1558-1560, 1645, 1701-1702, 1767-1770, 1774-1776, 1803-1810, 1813-1820, 1921, 1926, 1942-1943
src\gui\scarico_ore_components.py                                      531    159    70%   43-104, 115-130, 169, 177-180, 215-216, 231-232, 244-249, 322, 332-333, 336, 373, 409-415, 427, 450, 456, 465-478, 488-516, 539-542, 554-592, 655, 663, 703, 707-708, 729-734, 805, 809, 816-817, 839, 870, 879, 903-914, 925-947, 967-968, 1001-1006
src\gui\scarico_ore_panel.py                                           263     74    72%   40-42, 47-81, 211, 218-219, 232-233, 237-238, 242-244, 248-266, 288-289, 299-300, 305-306, 310-315, 323-324, 354, 365-366, 373-378, 405-408, 415
src\gui\settings_panel.py                                             1145    318    72%   117, 124-182, 303-305, 351-352, 359-360, 1042-1055, 1059-1064, 1116-1118, 1215-1217, 1227, 1230-1233, 1241-1243, 1252-1257, 1263-1294, 1439-1450, 1453-1461, 1464-1475, 1478-1489, 1492-1503, 1528-1544, 1548-1553, 1556-1566, 1570-1594, 1598-1617, 1620-1626, 1639-1644, 1647-1655, 1658-1670, 1673-1684, 1687-1693, 1698-1699, 1703-1720, 1724-1728, 1731-1736, 1739-1746, 1754-1755, 1760-1765, 1768-1772, 1776-1781, 1784-1789, 1792-1796, 1800-1805, 1808-1813, 1816-1823, 1866, 1871, 1887, 1918, 1937-1941, 1946-1963
src\gui\styles.py                                                       58      3    95%   89-90, 94
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   33      0   100%
src\gui\widgets\bot_parameters.py                                      112      5    96%   145, 164, 175, 197-198
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   152, 162-166, 191, 196-220, 223-227, 231-242, 245-249
src\gui\widgets\contabilita\certificati_tab.py                         111     38    66%   125, 127, 133-143, 146-153, 156-161, 165-264
src\gui\widgets\contabilita\giornaliere_tab.py                         164     40    76%   121, 145, 159-160, 167, 172-173, 188-191, 195-210, 213-229
src\gui\widgets\contabilita\helpers.py                                  33     12    64%   22-25, 29-34, 40-41
src\gui\widgets\contabilita\year_tab.py                                 46      3    93%   103-104, 108
src\gui\widgets\data_table.py                                          106      0   100%
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         324     95    71%   61-68, 84, 95, 99, 106, 112, 139-155, 159-181, 187, 212, 217, 234-237, 244-249, 261, 337-372, 383, 416, 425-428, 431-433, 482-483, 504, 517
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 76-100
src\gui\widgets\modern_button.py                                        62     10    84%   68-69, 75-78, 82-85
src\gui\widgets\notification_item.py                                    61      9    85%   33-34, 36-37, 56, 117-119, 122
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       53      0   100%
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   63-68
src\gui\widgets\timeline_widget.py                                     238     59    75%   76-79, 139-145, 153-164, 172-174, 178-180, 197-216, 238-243, 271-281, 313
src\gui\widgets\toast.py                                                85      9    89%   174-178, 187, 201, 206, 211, 216
src\gui\widgets\update_banner.py                                        29      7    76%   33-36, 39-41
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79     17    78%   36, 69-70, 125, 138-152, 227
src\utils\log_humanizer.py                                              16      0   100%
src\utils\parsing.py                                                    53      4    92%   102-119
src\utils\printing.py                                                   82     14    83%   20-22, 36-38, 49-50, 112-115, 139-140
src\utils\resource_manager.py                                           33      1    97%   18
src\utils\secure_logger.py                                              22      5    77%   42, 47-50
src\utils\security.py                                                   85      9    89%   39-42, 83-87
src\utils\validators.py                                                 73     46    37%   35, 42-44, 52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                13715   3520    74%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_data_pdl
1 failed in 11.36s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x000001B702CB71A0>
Traceback (most recent call last):
  File "C:\Users\Coemi\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\Coemi\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
    if not left_dir.resolve().exists():
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\pathlib.py", line 860, in exists
    self.stat(follow_symlinks=follow_symlinks)
  File "C:\Program Files\Python312\Lib\pathlib.py", line 840, in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Accesso negato: 'C:\\Users\\Coemi\\AppData\\Local\\Temp\\pytest-of-Allegretti\\pytest-current'

```
</details>

---
### `tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_restart_app`
**Error:** `FAILED tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_restart_app`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
________________ TestTelegramUIBridge.test_handle_restart_app _________________
C:\Program Files\Python312\Lib\unittest\mock.py:1393: in patched
    with self.decoration_helper(patched,
C:\Program Files\Python312\Lib\contextlib.py:137: in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1375: in decoration_helper
    arg = exit_stack.enter_context(patching)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\contextlib.py:526: in enter_context
    result = _enter(cm)
             ^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1451: in __enter__
    self.target = self.getter()
                  ^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\pkgutil.py:528: in resolve_name
    result = getattr(result, p)
             ^^^^^^^^^^^^^^^^^^
E   AttributeError: module 'src.core.telegram_bridge' has no attribute 'subprocess'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      6    70%   112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266     52    80%   71, 77, 123-124, 136, 160, 219, 230, 244, 312, 335-336, 342, 347-349, 356, 360, 366, 375-377, 386, 390-398, 402-410, 429-433, 438-442, 454
src\bots\base\login_page.py                                             94      7    93%   89-93, 101, 150-151
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     15    69%   56, 60-72, 86, 92, 95, 101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   34-43, 52-54, 77-79, 116-118
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          65      9    86%   42, 61, 64, 77, 87, 104-105, 107-108
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     216     70    68%   49-56, 91-94, 105-119, 136-138, 152-153, 156-157, 170-172, 232, 251-257, 274-278, 287-295, 317-318, 332, 336-337, 340-342, 352-353, 355-356, 370-371, 381-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            87     73    16%   19, 26, 30, 42-51, 56-63, 68-159
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         250    226    10%   28-31, 35, 39-44, 56-85, 96-102, 107-114, 118-149, 153-190, 194-202, 211-240, 244-251, 255-278, 290-412
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           226     41    82%   59, 78-80, 91, 97, 107, 118-120, 152, 160-161, 168, 207, 213, 222-233, 242, 281, 289, 303-305, 310, 316-318, 358-361, 377-382
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     20    81%   44-45, 64-66, 91-93, 124-126, 147, 158-160, 166-171
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     14    77%   25, 30, 35, 42, 46, 60, 62-63, 68-69, 78, 82, 95-96
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     49    35%   26, 31, 36, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   39-57, 77-79, 83-146, 163-164, 175-176, 179, 198-199, 204-205, 210-236, 240-251, 255-285
src\bots\portale_fornitori\timbrature\storage.py                       171     77    55%   71, 90-91, 98-126, 136-148, 174-183, 186-194, 199-210, 225-226, 240-242, 250, 254-255, 268-269, 279-288, 297-298
src\bots\safework\base.py                                               43     19    56%   23, 29-30, 46-47, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           403    128    68%   25, 30, 35, 45, 74-76, 88-89, 93-103, 114-115, 125, 128-129, 136-195, 226-227, 239-240, 283, 292-294, 306-307, 316, 327-329, 341-343, 364, 375-377, 387-388, 392-406, 411, 419-420, 440-441, 444-445, 460-461, 469, 487-489, 500-505, 511, 525-526, 536-538
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-76
src\core\app_updater.py                                                 46      2    96%   32, 85
src\core\audit_manager.py                                              156     30    81%   94-95, 114-130, 145-146, 202-203, 234, 236, 246-247, 271, 281-282, 294-295, 306-307
src\core\backup_manager.py                                             119     24    80%   41-42, 53, 68, 70, 84-86, 91, 98, 154-163, 183-186, 194, 200-202, 227-228
src\core\config_manager.py                                             177     13    93%   111, 124-125, 136, 199, 207-208, 261, 278-279, 324-325, 330
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     20    81%   28, 38, 78, 99-100, 118, 131-132, 141-148, 157-162, 175, 208
src\core\contabilita_queries.py                                         87      4    95%   52, 80, 96, 112
src\core\contabilita_search.py                                          91     14    85%   26-27, 50, 78-79, 109-110, 119, 122-123, 132-133, 151-152
src\core\contabilita_stats.py                                           61      4    93%   78-79, 100-101
src\core\contabilita_worker.py                                          80      4    95%   77, 91-92, 158
src\core\data_synchronizer.py                                           99      3    97%   97, 184-185
src\core\database.py                                                   141     10    93%   117-122, 132-133, 159-161
src\core\excel_importer.py                                             586     67    89%   23-24, 31-33, 135-136, 267, 307-309, 333, 338, 364-365, 376-380, 394, 403, 415, 478, 488, 504, 507, 511, 541, 570-571, 599-600, 640, 643, 655-656, 670, 707, 720, 761, 797, 836, 839-842, 850-851, 858, 862-863, 882, 896-897, 947-948, 958-960, 975, 990-991, 1007-1008, 1017-1019
src\core\license_updater.py                                            159     22    86%   99-102, 150, 166-167, 198-199, 204-206, 213, 230, 251-253, 289-291, 295-298
src\core\license_validator.py                                          197     19    90%   90-112, 136-138, 165, 185-186, 216
src\core\lyra_client.py                                                129     19    85%   22, 67-69, 105-107, 151-152, 203-204, 208-212, 244, 252-254
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      2    97%   52-53
src\core\secrets_manager.py                                            111     13    88%   66-69, 84-85, 140-142, 188-189, 196-197
src\core\stats_manager.py                                               48      4    92%   49, 62, 64, 77
src\core\telegram_bridge.py                                            333    104    69%   100, 122, 140-155, 165-166, 184-185, 193-194, 199-220, 223-229, 250-251, 255-256, 265, 276, 281, 285-286, 297, 303-306, 320-326, 330-356, 401-412, 418-419, 424-425, 431-432, 439-440, 451-452
src\core\telegram_manager.py                                           529    434    18%   62-77, 81-88, 92-108, 112-126, 129, 132-139, 142-155, 159-169, 173-179, 183, 197, 200-210, 213-228, 235-238, 241-245, 248-271, 274-281, 284-288, 291-309, 312-321, 324-363, 366-376, 380-403, 407-408, 412-414, 418-490, 498-535, 542-560, 567-572, 575-584, 591-600, 607, 619, 632-633, 636-637, 640-648, 651, 670-681, 685-704, 707-712, 719-720, 725-728, 741-758, 763-776, 780-795, 798-805, 808-813, 816-819, 822-827, 830-840, 843-848, 851-856, 859-868, 872-875, 884-894, 904-915, 925-936, 939-949, 952-963, 966-978
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                        104     83    20%   25-65, 70-80, 85-90, 95-105, 111-147, 152-162, 167-171
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 342, 466-468, 499-513, 516-529, 564, 619-627, 638, 730-732, 770
src\gui\contabilita_panel.py                                           256     56    78%   48-52, 197-198, 219-223, 238, 244-245, 250-254, 275-276, 287, 294, 305-306, 311, 315-333, 336-337, 340-356
src\gui\controllers\bot_controller.py                                   37      8    78%   59-67
src\gui\controllers\navigation_controller.py                           121     27    78%   59-62, 73-85, 134-135, 166-168, 172-174, 193-194, 197-201
src\gui\controllers\search_controller.py                               116     12    90%   56, 80-81, 86, 99, 112, 127, 137-138, 152, 160-161
src\gui\controllers\service_controller.py                               43      0   100%
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 56
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 270-283, 314-316
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   176, 192, 195, 199-202
src\gui\layouts\responsive.py                                           54      7    87%   29-35, 59
src\gui\lyra_panel.py                                                  335    155    54%   56-60, 64-82, 99-108, 398-401, 414, 418-440, 444-448, 452-467, 475-477, 481-484, 488-491, 495-496, 502, 515-535, 542-545, 571-572, 575-577, 603-618, 622-640, 648-661, 665-677, 681-692, 696-701
src\gui\main_window.py                                                 259    100    61%   163, 166-167, 179-180, 190-197, 201-217, 221-224, 228-233, 242-249, 253, 346-356, 360-361, 364-365, 368-375, 378-382, 385-387, 396, 400-406, 410-415, 419-423, 427-431, 435, 439, 447-453, 455-456
src\gui\notifications_panel.py                                         208      7    97%   175-176, 195, 324-325, 372, 408
src\gui\panels.py                                                     1072    222    79%   113-117, 224, 261, 419-421, 463-465, 484, 491, 502-504, 545-549, 593-595, 636-638, 657, 661, 673-675, 683, 688-748, 768-769, 811-813, 819, 836-846, 851-899, 924-926, 981, 985-990, 996, 1000, 1006-1007, 1023-1030, 1046-1047, 1090-1092, 1129, 1201-1209, 1212-1215, 1221, 1227-1229, 1242-1252, 1256-1264, 1269-1276, 1283-1287, 1291-1294, 1338-1339, 1355, 1403, 1425-1427, 1459-1461, 1485, 1496-1501, 1510-1514, 1536-1537, 1558-1560, 1645, 1701-1702, 1767-1770, 1774-1776, 1803-1810, 1813-1820, 1921, 1926, 1942-1943
src\gui\scarico_ore_components.py                                      531    159    70%   43-104, 115-130, 169, 177-180, 215-216, 231-232, 244-249, 322, 332-333, 336, 373, 409-415, 427, 450, 456, 465-478, 488-516, 539-542, 554-592, 655, 663, 703, 707-708, 729-734, 805, 809, 816-817, 839, 870, 879, 903-914, 925-947, 967-968, 1001-1006
src\gui\scarico_ore_panel.py                                           263     74    72%   40-42, 47-81, 211, 218-219, 232-233, 237-238, 242-244, 248-266, 288-289, 299-300, 305-306, 310-315, 323-324, 354, 365-366, 373-378, 405-408, 415
src\gui\settings_panel.py                                             1145    318    72%   117, 124-182, 303-305, 351-352, 359-360, 1042-1055, 1059-1064, 1116-1118, 1215-1217, 1227, 1230-1233, 1241-1243, 1252-1257, 1263-1294, 1439-1450, 1453-1461, 1464-1475, 1478-1489, 1492-1503, 1528-1544, 1548-1553, 1556-1566, 1570-1594, 1598-1617, 1620-1626, 1639-1644, 1647-1655, 1658-1670, 1673-1684, 1687-1693, 1698-1699, 1703-1720, 1724-1728, 1731-1736, 1739-1746, 1754-1755, 1760-1765, 1768-1772, 1776-1781, 1784-1789, 1792-1796, 1800-1805, 1808-1813, 1816-1823, 1866, 1871, 1887, 1918, 1937-1941, 1946-1963
src\gui\styles.py                                                       58      3    95%   89-90, 94
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   33      0   100%
src\gui\widgets\bot_parameters.py                                      112      5    96%   145, 164, 175, 197-198
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   152, 162-166, 191, 196-220, 223-227, 231-242, 245-249
src\gui\widgets\contabilita\certificati_tab.py                         111     38    66%   125, 127, 133-143, 146-153, 156-161, 165-264
src\gui\widgets\contabilita\giornaliere_tab.py                         164     40    76%   121, 145, 159-160, 167, 172-173, 188-191, 195-210, 213-229
src\gui\widgets\contabilita\helpers.py                                  33     12    64%   22-25, 29-34, 40-41
src\gui\widgets\contabilita\year_tab.py                                 46      3    93%   103-104, 108
src\gui\widgets\data_table.py                                          106      0   100%
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         324     95    71%   61-68, 84, 95, 99, 106, 112, 139-155, 159-181, 187, 212, 217, 234-237, 244-249, 261, 337-372, 383, 416, 425-428, 431-433, 482-483, 504, 517
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 76-100
src\gui\widgets\modern_button.py                                        62     10    84%   68-69, 75-78, 82-85
src\gui\widgets\notification_item.py                                    61      9    85%   33-34, 36-37, 56, 117-119, 122
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       53      0   100%
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   63-68
src\gui\widgets\timeline_widget.py                                     238     59    75%   76-79, 139-145, 153-164, 172-174, 178-180, 197-216, 238-243, 271-281, 313
src\gui\widgets\toast.py                                                85      9    89%   174-178, 187, 201, 206, 211, 216
src\gui\widgets\update_banner.py                                        29      7    76%   33-36, 39-41
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79     17    78%   36, 69-70, 125, 138-152, 227
src\utils\log_humanizer.py                                              16      0   100%
src\utils\parsing.py                                                    53      4    92%   102-119
src\utils\printing.py                                                   82     14    83%   20-22, 36-38, 49-50, 112-115, 139-140
src\utils\resource_manager.py                                           33      1    97%   18
src\utils\secure_logger.py                                              22      5    77%   42, 47-50
src\utils\security.py                                                   85      9    89%   39-42, 83-87
src\utils\validators.py                                                 73     46    37%   35, 42-44, 52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                13715   3520    74%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_restart_app
1 failed in 11.14s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x00000162619971A0>
Traceback (most recent call last):
  File "C:\Users\Coemi\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\Coemi\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
    if not left_dir.resolve().exists():
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\pathlib.py", line 860, in exists
    self.stat(follow_symlinks=follow_symlinks)
  File "C:\Program Files\Python312\Lib\pathlib.py", line 840, in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Accesso negato: 'C:\\Users\\Coemi\\AppData\\Local\\Temp\\pytest-of-Allegretti\\pytest-current'

```
</details>

---
### `tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_run_timbrature`
**Error:** `FAILED tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_run_timbrature`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_______________ TestTelegramUIBridge.test_handle_run_timbrature _______________
C:\Program Files\Python312\Lib\unittest\mock.py:1393: in patched
    with self.decoration_helper(patched,
C:\Program Files\Python312\Lib\contextlib.py:137: in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1375: in decoration_helper
    arg = exit_stack.enter_context(patching)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\contextlib.py:526: in enter_context
    result = _enter(cm)
             ^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.core.telegram_bridge' from 'C:\\Users\\Coemi\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\telegram_bridge.py'> does not have the attribute 'QDate'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      6    70%   112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              266     52    80%   71, 77, 123-124, 136, 160, 219, 230, 244, 312, 335-336, 342, 347-349, 356, 360, 366, 375-377, 386, 390-398, 402-410, 429-433, 438-442, 454
src\bots\base\login_page.py                                             94      7    93%   89-93, 101, 150-151
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     15    69%   56, 60-72, 86, 92, 95, 101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            60     15    75%   34-43, 52-54, 77-79, 116-118
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          65      9    86%   42, 61, 64, 77, 87, 104-105, 107-108
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     216     70    68%   49-56, 91-94, 105-119, 136-138, 152-153, 156-157, 170-172, 232, 251-257, 274-278, 287-295, 317-318, 332, 336-337, 340-342, 352-353, 355-356, 370-371, 381-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            87     73    16%   19, 26, 30, 42-51, 56-63, 68-159
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         250    226    10%   28-31, 35, 39-44, 56-85, 96-102, 107-114, 118-149, 153-190, 194-202, 211-240, 244-251, 255-278, 290-412
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           226     41    82%   59, 78-80, 91, 97, 107, 118-120, 152, 160-161, 168, 207, 213, 222-233, 242, 281, 289, 303-305, 310, 316-318, 358-361, 377-382
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     20    81%   44-45, 64-66, 91-93, 124-126, 147, 158-160, 166-171
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 61     14    77%   25, 30, 35, 42, 46, 60, 62-63, 68-69, 78, 82, 95-96
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     49    35%   26, 31, 36, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         170    105    38%   39-57, 77-79, 83-146, 163-164, 175-176, 179, 198-199, 204-205, 210-236, 240-251, 255-285
src\bots\portale_fornitori\timbrature\storage.py                       171     77    55%   71, 90-91, 98-126, 136-148, 174-183, 186-194, 199-210, 225-226, 240-242, 250, 254-255, 268-269, 279-288, 297-298
src\bots\safework\base.py                                               43     19    56%   23, 29-30, 46-47, 54-70, 74, 78
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           403    128    68%   25, 30, 35, 45, 74-76, 88-89, 93-103, 114-115, 125, 128-129, 136-195, 226-227, 239-240, 283, 292-294, 306-307, 316, 327-329, 341-343, 364, 375-377, 387-388, 392-406, 411, 419-420, 440-441, 444-445, 460-461, 469, 487-489, 500-505, 511, 525-526, 536-538
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             60      5    92%   71-76
src\core\app_updater.py                                                 46      2    96%   32, 85
src\core\audit_manager.py                                              156     30    81%   94-95, 114-130, 145-146, 202-203, 234, 236, 246-247, 271, 281-282, 294-295, 306-307
src\core\backup_manager.py                                             119     24    80%   41-42, 53, 68, 70, 84-86, 91, 98, 154-163, 183-186, 194, 200-202, 227-228
src\core\config_manager.py                                             177     13    93%   111, 124-125, 136, 199, 207-208, 261, 278-279, 324-325, 330
src\core\constants.py                                                   23      0   100%
src\core\contabilita_manager.py                                        107     20    81%   28, 38, 78, 99-100, 118, 131-132, 141-148, 157-162, 175, 208
src\core\contabilita_queries.py                                         87      4    95%   52, 80, 96, 112
src\core\contabilita_search.py                                          91     14    85%   26-27, 50, 78-79, 109-110, 119, 122-123, 132-133, 151-152
src\core\contabilita_stats.py                                           61      4    93%   78-79, 100-101
src\core\contabilita_worker.py                                          80      4    95%   77, 91-92, 158
src\core\data_synchronizer.py                                           99      3    97%   97, 184-185
src\core\database.py                                                   141     10    93%   117-122, 132-133, 159-161
src\core\excel_importer.py                                             586     67    89%   23-24, 31-33, 135-136, 267, 307-309, 333, 338, 364-365, 376-380, 394, 403, 415, 478, 488, 504, 507, 511, 541, 570-571, 599-600, 640, 643, 655-656, 670, 707, 720, 761, 797, 836, 839-842, 850-851, 858, 862-863, 882, 896-897, 947-948, 958-960, 975, 990-991, 1007-1008, 1017-1019
src\core\license_updater.py                                            159     22    86%   99-102, 150, 166-167, 198-199, 204-206, 213, 230, 251-253, 289-291, 295-298
src\core\license_validator.py                                          197     19    90%   90-112, 136-138, 165, 185-186, 216
src\core\lyra_client.py                                                129     19    85%   22, 67-69, 105-107, 151-152, 203-204, 208-212, 244, 252-254
src\core\lyra_sentinel.py                                               32      4    88%   37-38, 49-50
src\core\notification_manager.py                                        77      2    97%   52-53
src\core\secrets_manager.py                                            111     13    88%   66-69, 84-85, 140-142, 188-189, 196-197
src\core\stats_manager.py                                               48      4    92%   49, 62, 64, 77
src\core\telegram_bridge.py                                            333    104    69%   100, 122, 140-155, 165-166, 184-185, 193-194, 199-220, 223-229, 250-251, 255-256, 265, 276, 281, 285-286, 297, 303-306, 320-326, 330-356, 401-412, 418-419, 424-425, 431-432, 439-440, 451-452
src\core\telegram_manager.py                                           529    434    18%   62-77, 81-88, 92-108, 112-126, 129, 132-139, 142-155, 159-169, 173-179, 183, 197, 200-210, 213-228, 235-238, 241-245, 248-271, 274-281, 284-288, 291-309, 312-321, 324-363, 366-376, 380-403, 407-408, 412-414, 418-490, 498-535, 542-560, 567-572, 575-584, 591-600, 607, 619, 632-633, 636-637, 640-648, 651, 670-681, 685-704, 707-712, 719-720, 725-728, 741-758, 763-776, 780-795, 798-805, 808-813, 816-819, 822-827, 830-840, 843-848, 851-856, 859-868, 872-875, 884-894, 904-915, 925-936, 939-949, 952-963, 966-978
src\core\time_manager.py                                                19      1    95%   31
src\core\timesheet_processor.py                                        104     83    20%   25-65, 70-80, 85-90, 95-105, 111-147, 152-162, 167-171
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\contabilita_kpi_panel.py                                       375     40    89%   49-50, 342, 466-468, 499-513, 516-529, 564, 619-627, 638, 730-732, 770
src\gui\contabilita_panel.py                                           256     56    78%   48-52, 197-198, 219-223, 238, 244-245, 250-254, 275-276, 287, 294, 305-306, 311, 315-333, 336-337, 340-356
src\gui\controllers\bot_controller.py                                   37      8    78%   59-67
src\gui\controllers\navigation_controller.py                           121     27    78%   59-62, 73-85, 134-135, 166-168, 172-174, 193-194, 197-201
src\gui\controllers\search_controller.py                               116     12    90%   56, 80-81, 86, 99, 112, 127, 137-138, 152, 160-161
src\gui\controllers\service_controller.py                               43      0   100%
src\gui\controllers\tray_controller.py                                  35      8    77%   35-36, 47-52, 56
src\gui\dashboard_panel.py                                             120     12    90%   61-66, 270-283, 314-316
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\formatters.py                                                   27      0   100%
src\gui\help_panel.py                                                  105      7    93%   176, 192, 195, 199-202
src\gui\layouts\responsive.py                                           54      7    87%   29-35, 59
src\gui\lyra_panel.py                                                  335    155    54%   56-60, 64-82, 99-108, 398-401, 414, 418-440, 444-448, 452-467, 475-477, 481-484, 488-491, 495-496, 502, 515-535, 542-545, 571-572, 575-577, 603-618, 622-640, 648-661, 665-677, 681-692, 696-701
src\gui\main_window.py                                                 259    100    61%   163, 166-167, 179-180, 190-197, 201-217, 221-224, 228-233, 242-249, 253, 346-356, 360-361, 364-365, 368-375, 378-382, 385-387, 396, 400-406, 410-415, 419-423, 427-431, 435, 439, 447-453, 455-456
src\gui\notifications_panel.py                                         208      7    97%   175-176, 195, 324-325, 372, 408
src\gui\panels.py                                                     1072    222    79%   113-117, 224, 261, 419-421, 463-465, 484, 491, 502-504, 545-549, 593-595, 636-638, 657, 661, 673-675, 683, 688-748, 768-769, 811-813, 819, 836-846, 851-899, 924-926, 981, 985-990, 996, 1000, 1006-1007, 1023-1030, 1046-1047, 1090-1092, 1129, 1201-1209, 1212-1215, 1221, 1227-1229, 1242-1252, 1256-1264, 1269-1276, 1283-1287, 1291-1294, 1338-1339, 1355, 1403, 1425-1427, 1459-1461, 1485, 1496-1501, 1510-1514, 1536-1537, 1558-1560, 1645, 1701-1702, 1767-1770, 1774-1776, 1803-1810, 1813-1820, 1921, 1926, 1942-1943
src\gui\scarico_ore_components.py                                      531    159    70%   43-104, 115-130, 169, 177-180, 215-216, 231-232, 244-249, 322, 332-333, 336, 373, 409-415, 427, 450, 456, 465-478, 488-516, 539-542, 554-592, 655, 663, 703, 707-708, 729-734, 805, 809, 816-817, 839, 870, 879, 903-914, 925-947, 967-968, 1001-1006
src\gui\scarico_ore_panel.py                                           263     74    72%   40-42, 47-81, 211, 218-219, 232-233, 237-238, 242-244, 248-266, 288-289, 299-300, 305-306, 310-315, 323-324, 354, 365-366, 373-378, 405-408, 415
src\gui\settings_panel.py                                             1145    318    72%   117, 124-182, 303-305, 351-352, 359-360, 1042-1055, 1059-1064, 1116-1118, 1215-1217, 1227, 1230-1233, 1241-1243, 1252-1257, 1263-1294, 1439-1450, 1453-1461, 1464-1475, 1478-1489, 1492-1503, 1528-1544, 1548-1553, 1556-1566, 1570-1594, 1598-1617, 1620-1626, 1639-1644, 1647-1655, 1658-1670, 1673-1684, 1687-1693, 1698-1699, 1703-1720, 1724-1728, 1731-1736, 1739-1746, 1754-1755, 1760-1765, 1768-1772, 1776-1781, 1784-1789, 1792-1796, 1800-1805, 1808-1813, 1816-1823, 1866, 1871, 1887, 1918, 1937-1941, 1946-1963
src\gui\styles.py                                                       58      3    95%   89-90, 94
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\automazioni_widget.py                                   33      0   100%
src\gui\widgets\bot_parameters.py                                      112      5    96%   145, 164, 175, 197-198
src\gui\widgets\calendar_date_edit.py                                   10      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            161     40    75%   152, 162-166, 191, 196-220, 223-227, 231-242, 245-249
src\gui\widgets\contabilita\certificati_tab.py                         111     38    66%   125, 127, 133-143, 146-153, 156-161, 165-264
src\gui\widgets\contabilita\giornaliere_tab.py                         164     40    76%   121, 145, 159-160, 167, 172-173, 188-191, 195-210, 213-229
src\gui\widgets\contabilita\helpers.py                                  33     12    64%   22-25, 29-34, 40-41
src\gui\widgets\contabilita\year_tab.py                                 46      3    93%   103-104, 108
src\gui\widgets\data_table.py                                          106      0   100%
src\gui\widgets\database_widget.py                                      17      0   100%
src\gui\widgets\excel_table.py                                         324     95    71%   61-68, 84, 95, 99, 106, 112, 139-155, 159-181, 187, 212, 217, 234-237, 244-249, 261, 337-372, 383, 416, 425-428, 431-433, 482-483, 504, 517
src\gui\widgets\info_widgets.py                                         91     38    58%   24-55, 58, 76-100
src\gui\widgets\modern_button.py                                        62     10    84%   68-69, 75-78, 82-85
src\gui\widgets\notification_item.py                                    61      9    85%   33-34, 36-37, 56, 117-119, 122
src\gui\widgets\sidebar_button.py                                       19      0   100%
src\gui\widgets\sidebar_widget.py                                       53      0   100%
src\gui\widgets\status_card.py                                          68      0   100%
src\gui\widgets\status_indicator.py                                     42      6    86%   63-68
src\gui\widgets\timeline_widget.py                                     238     59    75%   76-79, 139-145, 153-164, 172-174, 178-180, 197-216, 238-243, 271-281, 313
src\gui\widgets\toast.py                                                85      9    89%   174-178, 187, 201, 206, 211, 216
src\gui\widgets\update_banner.py                                        29      7    76%   33-36, 39-41
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         64      7    89%   12-13, 65-66, 84-86
src\utils\helpers.py                                                    79     17    78%   36, 69-70, 125, 138-152, 227
src\utils\log_humanizer.py                                              16      0   100%
src\utils\parsing.py                                                    53      4    92%   102-119
src\utils\printing.py                                                   82     14    83%   20-22, 36-38, 49-50, 112-115, 139-140
src\utils\resource_manager.py                                           33      1    97%   18
src\utils\secure_logger.py                                              22      5    77%   42, 47-50
src\utils\security.py                                                   85      9    89%   39-42, 83-87
src\utils\validators.py                                                 73     46    37%   35, 42-44, 52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                13715   3520    74%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_run_timbrature
1 failed in 11.32s
Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x00000289168271A0>
Traceback (most recent call last):
  File "C:\Users\Coemi\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 374, in cleanup_numbered_dir
    cleanup_dead_symlinks(root)
  File "C:\Users\Coemi\AppData\Roaming\Python\Python312\site-packages\_pytest\pathlib.py", line 359, in cleanup_dead_symlinks
    if not left_dir.resolve().exists():
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\pathlib.py", line 860, in exists
    self.stat(follow_symlinks=follow_symlinks)
  File "C:\Program Files\Python312\Lib\pathlib.py", line 840, in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Accesso negato: 'C:\\Users\\Coemi\\AppData\\Local\\Temp\\pytest-of-Allegretti\\pytest-current'

```
</details>

---
