# 📊 Test Execution Report

**Date:** 2026-01-27 19:58:10
**Duration:** 87.44s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1013 |
| ✅ Passed | 881 |
| ❌ Failed | 20 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_gui_headless_hardened.py::TestGUIHeadlessHardened::test_dashboard_greeting_logic`
**Error:** `FAILED tests/unit/test_gui_headless_hardened.py::TestGUIHeadlessHardened::test_dashboard_greeting_logic`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________ TestGUIHeadlessHardened.test_dashboard_greeting_logic ____________
tests\unit\test_gui_headless_hardened.py:49: in test_dashboard_greeting_logic
    mock_datetime = mocker.patch("src.gui.panels.dashboard_panel.datetime")
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:419: in __call__
    return self._start_patch(
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:229: in _start_patch
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
E   AttributeError: <module 'src.gui.panels.dashboard_panel' from 'C:\\Users\\Coemi\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\gui\\panels\\dashboard_panel.py'> does not have the attribute 'datetime'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242     43    82%   75, 81, 134-135, 147, 171, 219-221, 233-235, 246, 262, 334, 357-358, 364, 368-372, 376-378, 382, 386-394, 413-417, 422-426, 438
src\bots\base\login_page.py                                             94     63    33%   45-61, 65-95, 99-115, 119-125, 141-142, 153-169, 174-179
src\bots\base\wait_helpers.py                                          171    144    16%   49-56, 77-82, 101-105, 136-208, 231, 260-320, 340-341, 344-348, 361, 364-368, 390-393, 396-408, 438-454, 484-491
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     18    62%   20, 25, 31, 56, 60-72, 86, 92, 95, 101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     12    78%   34-36, 49-51, 79-81, 118-120
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
src\bots\portale_fornitori\scarico_ts\bot.py                           225    158    30%   39, 44, 49, 60, 79-81, 85-100, 104-121, 125-146, 152-180, 184-220, 224-233, 237-268, 273, 308-310, 316-353, 357-366, 386, 395-417, 421-434
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     56    46%   40-46, 73-75, 107-109, 115-154, 160-185, 191-200, 206-215
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     28    63%   26, 31, 36, 49-65, 81, 88-89, 93-94, 104-105, 111-114, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163     37    77%   54-60, 84-86, 153-155, 174-175, 192-194, 197, 217-218, 222-223, 235-236, 246-247, 254-256, 271-273, 306, 310-314, 321-323
src\bots\portale_fornitori\timbrature\storage.py                       189    124    34%   94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 312, 323, 334-336, 345, 351-353, 374-377, 381-400, 409-410
src\bots\safework\base.py                                               41     17    59%   21, 40-43, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    313    22%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 172-199, 203-232, 236-244, 249, 260-262, 265-267, 273-274, 282-287, 293-325, 329-341, 345-373, 377-421, 425-445, 449-470, 474-488, 496, 507, 512-538, 542, 556-557, 577, 583-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     15    84%   74-76, 93, 137-142, 159-164
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit_manager.py                                              226     64    72%   120-122, 142, 158-159, 247-249, 259, 261, 285, 309-310, 350-352, 354-357, 359-362, 364-366, 368-372, 385-386, 392-399, 418-419, 426-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     22    84%   59-61, 68, 85, 95, 110-112, 117, 124, 180-189, 216, 222-224, 231, 249-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241     62    74%   35, 113-119, 140, 163, 226, 284, 301-302, 331-358, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     21    80%   29, 39, 79, 119, 134-135, 144-153, 162-171, 184, 204, 219, 228, 238
src\core\contabilita_queries.py                                         87      5    94%   36, 52, 80, 96, 112
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102      8    92%   79, 119, 138-139, 145, 159-160, 234
src\core\data_synchronizer.py                                          143     19    87%   22, 118, 223, 235, 269-293
src\core\database.py                                                   220     10    95%   124-131, 154-155, 183-185
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      0   100%
src\core\importers\attivita.py                                          64      4    94%   57-58, 92-93
src\core\importers\base.py                                              63      7    89%   14-15, 22-24, 54-55
src\core\importers\certificati.py                                      119     14    88%   46, 50, 53-54, 63, 93, 107-108, 141, 166-167, 177-179
src\core\importers\contabilita.py                                      140      9    94%   39, 48, 52-54, 119, 200-202
src\core\importers\giornaliere.py                                      189     32    83%   49-55, 72, 84, 99, 102, 106, 134, 151, 155, 179-180, 191-201, 214-215, 218, 234, 240, 248, 262
src\core\importers\scarico_ore.py                                      198     40    80%   11-12, 18-20, 47, 65-66, 72-87, 97, 100, 112-113, 126, 176, 204, 208, 217, 221, 235, 247, 256, 291, 301-302, 313-314
src\core\importers\storico_oda.py                                       85     62    27%   61-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 219-239, 244-252, 257-275, 280-288, 292-295
src\core\license_validator.py                                          183    146    20%   38-42, 49-58, 64-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                        97     45    54%   44, 52-59, 63-76, 83-84, 135-150, 154-156, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 17      2    88%   37-40
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     23    71%   68-73, 78-89, 94-96, 102, 109
src\core\secrets_manager.py                                             87     44    49%   28-50, 54-58, 62-72, 76-78, 82-86, 91, 96, 106, 119, 130-136
src\core\stats_manager.py                                               47     10    79%   40-45, 48, 61, 63, 76
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\controllers\bot_controller.py                                   38     14    63%   24-32, 63-71
src\gui\controllers\navigation_controller.py                           151    110    27%   41-57, 61-77, 80-92, 95-98, 101-104, 107-110, 113-116, 119-122, 125-128, 131-134, 137-140, 143-146, 149-152, 156-162, 166-170, 174-180, 192-234, 239-240, 258-260, 264-265, 269-270, 274-307, 311-312
src\gui\controllers\search_controller.py                               197    162    18%   18-46, 61, 73-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-76, 79-90, 93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81      0   100%
src\gui\formatters.py                                                  129     52    60%   13, 21-27, 38, 47, 50, 67-68, 104, 120-122, 138, 165-217, 227-229, 234-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128     23    82%   56, 101, 114-115, 125, 131, 133, 143-145, 167-168, 173-175, 183, 185, 187, 190-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196     25    87%   59-72, 84-88, 209, 221, 230, 250-252, 377-380, 390, 397
src\gui\panels\carico_ts.py                                             90     23    74%   39-43, 96-99, 103-110, 116, 120, 126-127, 145-152, 168-169
src\gui\panels\contabilita_kpi_panel.py                                379     41    89%   308, 347, 466-467, 485-487, 523-537, 540-553, 590, 648-656, 669, 765-767, 814
src\gui\panels\contabilita_panel.py                                    255     84    67%   51-55, 190-197, 201, 245, 251-256, 277-281, 285-288, 294-296, 303-305, 312, 322-325, 329-333, 337-341, 354-356, 366-367, 378, 389, 402-403, 408, 412-429, 433, 436-455
src\gui\panels\dashboard_panel.py                                      175     81    54%   85, 133-135, 142, 144, 147-149, 154-155, 157-167, 184-187, 194-197, 200, 208-211, 216-232, 237-246, 250-267, 271-301, 305-311
src\gui\panels\dettagli_oda.py                                         127     67    47%   37-41, 94-96, 100, 103-115, 119, 135-140, 148, 153-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 17      9    47%   17-18, 21-33, 37-38
src\gui\panels\dipendenti\pages\anagrafica_page.py                     538    493     8%   53-83, 86-220, 223-333, 336-341, 345-381, 385-400, 405-430, 433-477, 481-489, 493-510, 513-543, 546-558, 561-570, 574-605, 608-645, 650-657, 660-703, 706-708, 711-749, 753-777, 783-826, 834-924, 928-941, 945-968, 972-1005
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra_panel.py                                           397    349    12%   38-40, 43-111, 138-142, 146-164, 178-179, 183-192, 204-212, 216-492, 499-512, 516-521, 525-545, 549-552, 556-560, 564-581, 589-591, 595-598, 602-605, 609-610, 614-619, 629-651, 657-660, 664-678, 682-701, 705-741, 749-766, 772-784, 788-799, 803-808
src\gui\panels\notifications_panel.py                                  475    277    42%   66-70, 73-156, 159-161, 342-353, 356, 360, 371, 373, 375, 410, 419-420, 423-425, 436-443, 446-448, 455-468, 471-543, 546-547, 551-553, 557-559, 563-565, 569-570, 574-575, 579, 582-586, 591-629, 634-657, 663-691, 699-707, 711-712, 716-734, 738-772, 776-778, 782-801, 805-846
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-51, 58-110, 113-207, 211-222, 226-246, 250-258, 262-280, 284-337, 343-349, 353-367
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-78, 82-84, 87-95, 98-104, 107-117, 121-194
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   44-46, 51-85, 96-105, 109-252, 256-271, 275-306, 310-312, 316-324, 328-349, 353-355, 359-377, 388-417, 421-426, 430-442, 446-457, 461-462, 466-474, 478-492, 496-515, 519-522, 526-547
src\gui\panels\scarico_pdl.py                                          223     54    76%   53-55, 94, 165-173, 176-179, 185, 191-193, 212-222, 226-234, 239-246, 257-260, 265, 270, 287-293, 296-299, 343, 353, 396
src\gui\panels\scarico_ts.py                                           121     24    80%   37-39, 84-86, 105, 112, 127-132, 174-185, 195-199
src\gui\panels\settings\main_panel.py                                  104     30    71%   112-130, 139, 144-146, 149-162, 165-183
src\gui\panels\settings\pages\diag_page.py                              32      3    91%   42-43, 49
src\gui\panels\settings\pages\general_page.py                           43      2    95%   73-76
src\gui\panels\settings\pages\lists_page.py                            317    119    62%   226, 236, 248-257, 260-268, 275, 300-313, 316-327, 330-336, 341-350, 353-366, 369-380, 383-389, 398, 401-404, 407-412, 415-422, 426, 429, 432, 435, 438, 441, 444, 447, 450, 453, 456, 459, 476-491
src\gui\panels\settings\pages\paths_page.py                            107     28    74%   113-129, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179, 204-219
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     33    75%   158-160, 166-168, 176-181, 184-185, 192-194, 202-205, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55      4    93%   113, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136     34    75%   142-149, 154-167, 172-181, 187-191, 213-226
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-254, 258-271, 275-285, 289, 293, 297-308, 312-319, 323-332, 336-388, 392-509, 513-541
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     29    54%   73-117, 121-139
src\gui\panels\timbrature\components\settings_tab.py                    94      4    96%   147, 161-163
src\gui\panels\timbrature\panel.py                                     148     16    89%   216-222, 225-232, 246, 261-262, 266
src\gui\panels\timbrature_bot.py                                       116     35    70%   40-42, 62-64, 95, 106-111, 121-122, 134-142, 149-161, 184-186, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles.py                                                       63     47    25%   25-28, 33, 40-50, 54-97, 101-228, 233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     22    84%   39-40, 88-90, 151-152, 172-182, 189, 193-195, 272, 278, 292, 294
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    157    58%   41-135, 139-156, 312-330, 513-525, 546, 635-647, 655-768, 776-828, 845-846, 858-859, 871-872, 884-886, 919-925, 931-933
src\gui\widgets\bot_parameters.py                                      112      3    97%   153, 207-208
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208     57    73%   131, 192, 205-208, 228, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222     49    78%   192, 217-218, 313, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166     50    70%   96, 132, 149, 176, 186-187, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     17    48%   21-31, 37-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     13    81%   99, 123-124, 128-157, 161
src\gui\widgets\data_table.py                                          109      1    99%   129
src\gui\widgets\excel_table.py                                         330     93    72%   64-71, 87, 98, 102, 109, 115, 143-167, 171-197, 203, 230, 235, 252-255, 262-267, 279, 321-380, 391, 424, 433-436, 439-441, 520, 541, 555
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     38    60%   27-60, 63, 83-111
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     14    82%   273-314, 328, 344, 361-362
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41      7    83%   28-30, 35-37, 76
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     32    29%   28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100      7    93%   165-167, 208-209, 224-225
src\gui\widgets\status_card.py                                          59      8    86%   106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191     42    78%   80-81, 83-84, 131-135, 137-141, 145, 148-153, 161-169, 172-173, 176-178, 191-205, 239-249
src\gui\widgets\toast.py                                               128     34    73%   141-149, 152-156, 160-162, 166-167, 172-173, 179, 210-217, 225, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         66      7    89%   15-16, 70-72, 90-92
src\utils\helpers.py                                                    97     54    44%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 259
src\utils\log_humanizer.py                                              41     10    76%   18-26, 112, 120
src\utils\parsing.py                                                    53     12    77%   14, 17, 21, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     23    71%   43-44, 81-83, 103, 105, 110-112, 117, 123-138
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                20053  10789    46%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_gui_headless_hardened.py::TestGUIHeadlessHardened::test_dashboard_greeting_logic
1 failed in 15.05s

```
</details>

---
### `tests/unit/test_printing.py::TestPrinting::test_print_pdf_split_jobs`
**Error:** `FAILED tests/unit/test_printing.py::TestPrinting::test_print_pdf_split_jobs`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
___________________ TestPrinting.test_print_pdf_split_jobs ____________________
tests\unit\test_printing.py:50: in test_print_pdf_split_jobs
    assert result is True
E   assert False is True
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    188    22%   53-69, 75, 81, 86, 91-93, 105-109, 119-135, 139, 143, 147, 151-152, 156-157, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 368-372, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-82, 86-87, 94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 172-199, 203-232, 236-244, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 449-470, 474-488, 495-538, 541-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     37    20%   17-47, 52-57, 62-83, 87
src\core\audit_manager.py                                              226     74    67%   120-122, 138-142, 158-159, 243-249, 255-269, 285, 309-310, 359-362, 364-366, 368-372, 385-386, 398-399, 403-419, 426-461
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137     64    53%   42, 48, 59-61, 68, 71, 85, 93, 95, 110-112, 117, 122-127, 136-189, 200-208, 216, 222-224, 229-250
src\core\bug_reporter.py                                                60     45    25%   32-102, 107-121
src\core\config_manager.py                                             241    140    42%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 226, 236, 250-251, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     53    50%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 204, 219, 228, 238
src\core\contabilita_queries.py                                         87     26    70%   29-30, 36, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     18    69%   62-84, 90
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220     62    72%   81-90, 119-131, 154-155, 183-185, 311-342, 350-397, 406-408, 416-433, 485-533, 538-540, 547-555
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155     22    86%   98-101, 149, 164-165, 195-196, 201-203, 210, 227, 249-251, 286-288, 292-295
src\core\license_validator.py                                          183     13    93%   99-117, 143, 170, 187-191
src\core\lyra_client.py                                                128     20    84%   22, 67-69, 83, 109-110, 117, 146-147, 203-204, 208-212, 249, 257-259
src\core\lyra_sentinel.py                                               32      4    88%   38-39, 50-51
src\core\notification_manager.py                                        97      9    91%   44, 83-84, 135-150
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     25    68%   68-73, 78-89, 95, 101-103, 108-110
src\core\secrets_manager.py                                             87     25    71%   30, 35, 40, 47-50, 56-57, 65-71, 77, 85, 91, 96, 106, 119, 124-125, 130-136
src\core\stats_manager.py                                               47      7    85%   43-45, 48, 61, 63, 76
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
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     18    40%   22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187     71    62%   80, 84, 91-92, 115-118, 154-157, 161-165, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 251, 261, 269, 273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     11    88%   57, 65, 101, 104-105, 123-128
src\gui\components\scarico_ore\model.py                                169    113    33%   75-81, 84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 179, 184, 188-214, 224-233, 247-274
src\gui\controllers\bot_controller.py                                   38     20    47%   36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           151     53    65%   101-104, 107-110, 113-116, 119-122, 125-128, 131-134, 137-140, 143-146, 149-152, 197-204, 212-219, 227-234, 264-265, 269-270, 298-307
src\gui\controllers\search_controller.py                               197    177    10%   18-46, 50-52, 56-74, 78-94, 100-111, 117-128, 134-145, 149-165, 169-215, 219-264, 268-312, 316-336
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-55, 63-125, 132-162, 166-350, 362-365, 384-392, 405-446, 459-479, 483, 489-500
src\gui\controllers\tray_controller.py                                  38      8    79%   37-38, 50-55, 61
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-76, 79-90, 93
src\gui\dialogs\bug_report_dialog.py                                   158    139    12%   31-32, 35-42, 49-53, 56-127, 130-149, 152-174, 178-336, 340-357
src\gui\dialogs\command_palette.py                                     302    274     9%   39-70, 74-187, 191-217, 220-228, 231-237, 240-245, 248-255, 258-298, 302-311, 314-323, 326-332, 335-341, 345-349, 353-367, 371-382, 385-392, 397-401, 404-448, 451-487, 491-507, 510-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 104, 107, 110, 113-140, 143-148, 151-154, 158-237
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     40    44%   26-32, 56-67, 72-81, 85-333
src\gui\main_window\components\status_bar.py                           139     91    35%   111-124, 128-140, 145-182, 186-253
src\gui\main_window\components\tool_bar.py                              25      0   100%
src\gui\main_window\components\tray_icon.py                             16      7    56%   18, 29-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   15-16, 25-34, 37-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     20      1    95%   39
src\gui\main_window\main.py                                            336    189    44%   187, 190, 196, 199, 202, 205-207, 213, 217-243, 247, 251-277, 283-287, 295-299, 307-311, 319-323, 331-333, 336-338, 341-343, 353-357, 360-364, 373-386, 389-392, 397-500, 503-530, 533-558, 561-583, 587-590, 596-601, 604-620, 623-625, 629-632, 637, 641, 647-648, 659, 663, 667, 671, 675
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          128     22    83%   56, 101, 114-115, 125, 131, 133, 143-145, 167-168, 173-175, 183, 187, 190-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196     85    57%   84-88, 92-94, 192-198, 209, 213, 221, 230, 239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-315, 325-330, 334-347, 351, 355-370, 377-380, 386-391, 395-398
src\gui\panels\carico_ts.py                                             90     49    46%   41-43, 99, 103-110, 114-122, 126-127, 131-187
src\gui\panels\contabilita_kpi_panel.py                                379    141    63%   308, 347, 355, 466-467, 479-558, 568-631, 642-731, 741-801, 812-914
src\gui\panels\contabilita_panel.py                                    255    145    43%   49-55, 190-197, 201, 234-236, 245, 249-270, 275-299, 303-305, 309-312, 320-325, 328-341, 347-367, 370-371, 374-378, 383-404, 407-409, 412-429, 433, 436-455
src\gui\panels\dashboard_panel.py                                      181     98    46%   96, 144-146, 150-160, 164-179, 184-199, 204-222, 227-243, 248-257, 261-278, 282-312, 316-322
src\gui\panels\dettagli_oda.py                                         127     80    37%   37-41, 94-96, 100, 103-115, 118-130, 135-140, 144-150, 153-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 17      9    47%   17-18, 21-33, 37-38
src\gui\panels\dipendenti\pages\anagrafica_page.py                     538    493     8%   53-83, 86-220, 223-333, 336-341, 345-381, 385-400, 405-430, 433-477, 481-489, 493-510, 513-543, 546-558, 561-570, 574-605, 608-645, 650-657, 660-703, 706-708, 711-749, 753-777, 783-826, 834-924, 928-941, 945-968, 972-1005
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\help_panel.py                                           120     18    85%   198-207, 214-216, 218, 221-224
src\gui\panels\lyra_panel.py                                           397    171    57%   68-75, 138-142, 146-164, 183-192, 501-504, 521, 525-545, 549-552, 556-560, 564-581, 589-591, 595-598, 602-605, 609-610, 616, 629-651, 657-660, 677-678, 682-701, 705-741, 749-766, 772-784, 788-799, 803-808
src\gui\panels\notifications_panel.py                                  475    115    76%   66-70, 73-156, 159-161, 342-353, 356, 360, 371, 373, 375, 410, 419-420, 423-425, 446-448, 546-547, 551-553, 563-565, 579, 635, 641, 643, 645, 649, 711-712, 718-734, 754-755, 764, 766, 776-778, 815-826
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-51, 58-110, 113-207, 211-222, 226-246, 250-258, 262-280, 284-337, 343-349, 353-367
src\gui\panels\prenota_bp.py                                           104     63    39%   34-37, 82-84, 87-95, 98-104, 107-117, 121-194
src\gui\panels\ricerca_pdl.py                                           80     43    46%   71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    306    200    35%   44-46, 51-85, 256-271, 275-306, 310-312, 316-324, 328-349, 353-355, 359-377, 388-417, 421-426, 430-442, 446-457, 461-462, 466-474, 478-492, 496-515, 519-522, 526-547
src\gui\panels\scarico_pdl.py                                          223    139    38%   51-55, 94, 165-173, 176-179, 182-195, 198-209, 212-222, 226-234, 239-246, 249-282, 286-300, 304-326, 330-344, 348-357, 361-385, 389-391, 395-409, 413-415
src\gui\panels\scarico_ts.py                                           121     56    54%   37-39, 84-86, 105, 112, 127-132, 136-141, 155-157, 163-223
src\gui\panels\settings\main_panel.py                                  104     23    78%   129-130, 139, 144-146, 149-162, 165-183
src\gui\panels\settings\pages\diag_page.py                              32      2    94%   42-43
src\gui\panels\settings\pages\general_page.py                           43      0   100%
src\gui\panels\settings\pages\lists_page.py                            317    112    65%   226, 236, 248-257, 260-268, 275, 300-313, 316-327, 330-336, 341-350, 353-366, 369-380, 383-389, 401-404, 407-412, 415-422, 426, 429, 432, 435, 438, 441, 444, 447, 450, 453, 456, 459
src\gui\panels\settings\pages\paths_page.py                            107     22    79%   113-129, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     33    75%   158-160, 166-168, 176-181, 184-185, 192-194, 202-205, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55      1    98%   113
src\gui\panels\settings\tabs\telegram_tab.py                           136     26    81%   142-149, 154-167, 172-181, 187-191, 223-224
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-254, 258-271, 275-285, 289, 293, 297-308, 312-319, 323-332, 336-388, 392-509, 513-541
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-158, 162-178, 182-213, 216-222, 225-232, 236, 239-262, 266
src\gui\panels\timbrature_bot.py                                       116     83    28%   38-42, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles.py                                                       63      3    95%   108-109, 113
src\gui\toast.py                                                        45      4    91%   87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     26    81%   39-40, 88-90, 151-152, 172-182, 189, 193-195, 272, 278, 292, 294, 303-319
src\gui\widgets\automazioni_widget.py                                   54      2    96%   124-125
src\gui\widgets\autopilot_widget.py                                    371    156    58%   41-135, 139-156, 312-330, 513-525, 635-647, 655-768, 776-828, 845-846, 858-859, 871-872, 884-886, 919-925, 931-933
src\gui\widgets\bot_parameters.py                                      112     13    88%   153, 157-159, 169-172, 183, 205-208
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208     57    73%   131, 192, 205-208, 228, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222     49    78%   192, 217-218, 313, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    223    32%   47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 321-380, 389-395, 424, 433-436, 439-441, 456, 462, 464, 482-483, 494-524, 533-558
src\gui\widgets\footer_stats.py                                        474    152    68%   31-46, 49, 74-82, 86, 90, 107-111, 114-115, 119, 138-140, 143-144, 148-152, 155-156, 160, 280-291, 297-302, 322, 329, 341-345, 349, 537, 550-551, 562, 578-580, 592, 617-618, 643-644, 647, 650-651, 654-655, 660-674, 677-741, 777-779, 783-789, 793-796, 812-816, 825-834, 838, 842-843
src\gui\widgets\info_widgets.py                                         95     39    59%   27-60, 63, 83-111, 174
src\gui\widgets\modern_button.py                                        61     10    84%   71-72, 78-81, 85-88
src\gui\widgets\notification_card.py                                   220     87    60%   113, 270-275, 302-316, 321-322, 329-339, 343, 361, 365-367, 381-415, 429-430, 432, 434, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47      9    81%   129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     13    81%   35-36, 38-39, 41-42, 58, 91-92, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106      9    92%   238-239, 243-244, 260-261, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     11    86%   273-314, 344
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41      4    90%   47-51
src\gui\widgets\sidebar_widget.py                                      183     20    89%   55-58, 71, 79, 122-124, 128-130, 134-137, 290, 299-300, 326-327
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     24    76%   165-167, 194-227
src\gui\widgets\status_card.py                                          59      8    86%   106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42      6    86%   63-68
src\gui\widgets\timeline_widget.py                                     191     53    72%   83-84, 137-141, 161-169, 172-173, 176-178, 191-205, 221, 239-249, 265-269, 302, 307-334
src\gui\widgets\toast.py                                               128     49    62%   141-149, 152-156, 160-162, 166-167, 172-173, 179, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35      7    80%   43-48, 51-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     22    77%   28, 47, 82-83, 141, 154-168, 239, 256-259
src\utils\log_humanizer.py                                              41      5    88%   16, 20, 25-26, 112
src\utils\parsing.py                                                    53      4    92%   102-119
src\utils\printing.py                                                   83     63    24%   21-23, 28-39, 47-51, 65-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22      5    77%   50, 55-58
src\utils\security.py                                                   79      9    89%   43-44, 81-83, 110-112, 138
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                20231  11211    45%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_printing.py::TestPrinting::test_print_pdf_split_jobs
1 failed in 8.24s

```
</details>

---
### `tests/unit/test_safework_bot_deep.py::TestSafeWorkPDLBotDeep::test_polling_logic_simulated`
**Error:** `FAILED tests/unit/test_safework_bot_deep.py::TestSafeWorkPDLBotDeep::test_polling_logic_simulated`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_____________ TestSafeWorkPDLBotDeep.test_polling_logic_simulated _____________
tests\unit\test_safework_bot_deep.py:38: in test_polling_logic_simulated
    m_glob = mocker.patch("src.bots.safework.pdl.bot.glob.glob")
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:419: in __call__
    return self._start_patch(
..\..\..\AppData\Roaming\Python\Python312\site-packages\pytest_mock\plugin.py:229: in _start_patch
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
E   AttributeError: module 'src.bots.safework.pdl.bot' has no attribute 'glob'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    188    22%   53-69, 75, 81, 86, 91-93, 105-109, 119-135, 139, 143, 147, 151-152, 156-157, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 368-372, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-82, 86-87, 94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    285    29%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 189-193, 205-206, 213, 218, 223-224, 238-241, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 462-466, 469-470, 487-488, 495-538, 542, 556-557, 578-580, 583-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    137     0%   6-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    149    38%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 218-236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106    106     0%   6-243
src\core\contabilita_queries.py                                         87     87     0%   6-122
src\core\contabilita_search.py                                          91     91     0%   6-178
src\core\contabilita_stats.py                                           59     59     0%   6-105
src\core\contabilita_worker.py                                         102    102     0%   1-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    102    34%   75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 227, 235-236, 249-251, 268-272, 275, 280-288, 292-295
src\core\license_validator.py                                          183    146    20%   38-42, 49-58, 64-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\lyra_client.py                                                128    128     0%   6-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     67     0%   7-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             87     53    39%   28-50, 54-58, 62-72, 76-78, 82-86, 91, 96, 101-106, 111-112, 117-119, 124-125, 130-136
src\core\stats_manager.py                                               47     15    68%   40-45, 48, 61, 63, 71-79
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\service.py                                           175    175     0%   1-314
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129    129     0%   1-237
src\gui\layouts\responsive.py                                           64     10    84%   33-39, 73, 78, 96-97
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 196    196     0%   6-398
src\gui\panels\carico_ts.py                                             90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                                379    379     0%   1-914
src\gui\panels\contabilita_panel.py                                    255    255     0%   6-455
src\gui\panels\dashboard_panel.py                                      181    181     0%   1-322
src\gui\panels\dettagli_oda.py                                         127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-282
src\gui\panels\help_panel.py                                           120    120     0%   6-368
src\gui\panels\lyra_panel.py                                           397    397     0%   1-808
src\gui\panels\notifications_panel.py                                  475    475     0%   6-846
src\gui\panels\pdl_db.py                                               202    202     0%   6-367
src\gui\panels\prenota_bp.py                                           104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                                    306    306     0%   7-547
src\gui\panels\scarico_pdl.py                                          223    223     0%   6-415
src\gui\panels\scarico_ts.py                                           121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                                    225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     148    148     0%   1-266
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-212
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    371     0%   5-989
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    292    12%   29-36, 47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    220     0%   6-531
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-284
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42      6    86%   63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     53     0%   6-119
src\utils\printing.py                                                   83     14    83%   21-23, 37-39, 50-51, 115-120, 144-145
src\utils\resource_manager.py                                           43     10    77%   22-36, 55
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                16138  14216    12%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_safework_bot_deep.py::TestSafeWorkPDLBotDeep::test_polling_logic_simulated
1 failed in 9.32s

```
</details>

---
### `tests/unit/test_safework_bot_refactoring.py::test_run_success_full_workflow`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
______________ ERROR at setup of test_run_success_full_workflow _______________
tests\unit\test_safework_bot_refactoring.py:41: in mock_settings
    with patch("src.bots.safework.pdl.bot.config_manager.CONFIG_DIR", tmp_path):
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1451: in __enter__
    self.target = self.getter()
                  ^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\pkgutil.py:528: in resolve_name
    result = getattr(result, p)
             ^^^^^^^^^^^^^^^^^^
E   AttributeError: module 'src.bots.safework.pdl.bot' has no attribute 'config_manager'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    188    22%   53-69, 75, 81, 86, 91-93, 105-109, 119-135, 139, 143, 147, 151-152, 156-157, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 368-372, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-82, 86-87, 94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    270    32%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 189-193, 205-206, 213, 218, 223-224, 238-241, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 462-466, 469-470, 487-488, 495-538, 542, 556-557, 578-580, 583-586, 612-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              226    226     0%   6-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    137     0%   6-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106    106     0%   6-243
src\core\contabilita_queries.py                                         87     87     0%   6-122
src\core\contabilita_search.py                                          91     91     0%   6-178
src\core\contabilita_stats.py                                           59     59     0%   6-105
src\core\contabilita_worker.py                                         102    102     0%   1-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\lyra_client.py                                                128    128     0%   6-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     97     0%   6-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     67     0%   7-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             87     53    39%   28-50, 54-58, 62-72, 76-78, 82-86, 91, 96, 101-106, 111-112, 117-119, 124-125, 130-136
src\core\stats_manager.py                                               47     47     0%   6-83
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\service.py                                           175    175     0%   1-314
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129    129     0%   1-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 196    196     0%   6-398
src\gui\panels\carico_ts.py                                             90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                                379    379     0%   1-914
src\gui\panels\contabilita_panel.py                                    255    255     0%   6-455
src\gui\panels\dashboard_panel.py                                      181    181     0%   1-322
src\gui\panels\dettagli_oda.py                                         127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-282
src\gui\panels\help_panel.py                                           120    120     0%   6-368
src\gui\panels\lyra_panel.py                                           397    397     0%   1-808
src\gui\panels\notifications_panel.py                                  475    475     0%   6-846
src\gui\panels\pdl_db.py                                               202    202     0%   6-367
src\gui\panels\prenota_bp.py                                           104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                                    306    306     0%   7-547
src\gui\panels\scarico_pdl.py                                          223    223     0%   6-415
src\gui\panels\scarico_ts.py                                           121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                                    225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     148    148     0%   1-266
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-212
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12     12     0%   6-24
src\gui\widgets\activity_feed.py                                       137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    371     0%   5-989
src\gui\widgets\bot_parameters.py                                      112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                                   16     16     0%   6-79
src\gui\widgets\data_table.py                                          109    109     0%   5-217
src\gui\widgets\excel_table.py                                         330    330     0%   6-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     95     0%   6-174
src\gui\widgets\modern_button.py                                        61     61     0%   5-151
src\gui\widgets\notification_card.py                                   220    220     0%   6-531
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-284
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     45     0%   1-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-229
src\gui\widgets\status_card.py                                          59     59     0%   1-131
src\gui\widgets\status_indicator.py                                     42     42     0%   6-68
src\gui\widgets\timeline_widget.py                                     191    191     0%   6-334
src\gui\widgets\toast.py                                               128    128     0%   5-253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                              41     41     0%   6-121
src\utils\parsing.py                                                    53     53     0%   6-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                16022  14856     7%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_safework_bot_refactoring.py::test_run_success_full_workflow
1 error in 9.13s

```
</details>

---
### `tests/unit/test_scarico_ore_components_extended.py::TestScaricoOreComponentsExtended::test_cache_worker_build`
**Error:** `FAILED tests/unit/test_scarico_ore_components_extended.py::TestScaricoOreComponentsExtended::test_cache_worker_build`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________ TestScaricoOreComponentsExtended.test_cache_worker_build ___________
tests\unit\test_scarico_ore_components_extended.py:39: in test_cache_worker_build
    display, search, totals, styles = worker._build_caches(data)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ValueError: too many values to unpack (expected 4)
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    160    34%   75, 81, 86, 91-93, 108, 120, 125-135, 139, 143, 147, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 369-371, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\scarico_ts\bot.py                           225     59    74%   39, 44, 49, 60, 79-81, 92, 98, 108, 119-121, 167, 177-178, 185, 232, 238, 249-264, 273, 283-306, 317, 324-325, 336, 342-347, 358, 364-366, 377, 388-389, 412-415, 431-434
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-82, 86-87, 94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     19    54%   21, 27-28, 44-45, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    159    60%   26, 31, 36, 46, 64, 75-76, 86, 89-90, 97-160, 192-193, 205-206, 249, 260-262, 273-274, 282-285, 294, 309-311, 323-325, 332-337, 346, 360-362, 372-373, 378, 383-412, 419-421, 426, 442-445, 465-466, 469-470, 483-488, 496, 508-509, 518-520, 531-536, 542, 547-584, 605-610
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              226    226     0%   6-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    137     0%   6-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106    106     0%   6-243
src\core\contabilita_queries.py                                         87     87     0%   6-122
src\core\contabilita_search.py                                          91     91     0%   6-178
src\core\contabilita_stats.py                                           59     59     0%   6-105
src\core\contabilita_worker.py                                         102    102     0%   1-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\lyra_client.py                                                128    128     0%   6-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     97     0%   6-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     67     0%   7-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             87     53    39%   28-50, 54-58, 62-72, 76-78, 82-86, 91, 96, 101-106, 111-112, 117-119, 124-125, 130-136
src\core\stats_manager.py                                               47     47     0%   6-83
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\service.py                                           175    175     0%   1-314
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     58    46%   28-102, 105-120, 145, 148, 153-156, 172, 174-175, 179, 182-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    103    39%   75-81, 84, 87-100, 103-124, 127, 130-134, 155, 165-169, 172-175, 188-214, 219-236, 239-244, 247-274
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129    129     0%   1-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 196    196     0%   6-398
src\gui\panels\carico_ts.py                                             90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                                379    379     0%   1-914
src\gui\panels\contabilita_panel.py                                    255    255     0%   6-455
src\gui\panels\dashboard_panel.py                                      181    181     0%   1-322
src\gui\panels\dettagli_oda.py                                         127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-282
src\gui\panels\help_panel.py                                           120    120     0%   6-368
src\gui\panels\lyra_panel.py                                           397    397     0%   1-808
src\gui\panels\notifications_panel.py                                  475    475     0%   6-846
src\gui\panels\pdl_db.py                                               202    202     0%   6-367
src\gui\panels\prenota_bp.py                                           104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                                    306    306     0%   7-547
src\gui\panels\scarico_pdl.py                                          223    223     0%   6-415
src\gui\panels\scarico_ts.py                                           121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                                    225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     148    148     0%   1-266
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-212
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12     12     0%   6-24
src\gui\widgets\activity_feed.py                                       137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    371     0%   5-989
src\gui\widgets\bot_parameters.py                                      112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                                   16     16     0%   6-79
src\gui\widgets\data_table.py                                          109    109     0%   5-217
src\gui\widgets\excel_table.py                                         330    330     0%   6-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     95     0%   6-174
src\gui\widgets\modern_button.py                                        61     61     0%   5-151
src\gui\widgets\notification_card.py                                   220    220     0%   6-531
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-284
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     45     0%   1-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-229
src\gui\widgets\status_card.py                                          59     59     0%   1-131
src\gui\widgets\status_indicator.py                                     42     42     0%   6-68
src\gui\widgets\timeline_widget.py                                     191    191     0%   6-334
src\gui\widgets\toast.py                                               128    128     0%   5-253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     70    28%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 249-267
src\utils\log_humanizer.py                                              41     41     0%   6-121
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                16613  14968    10%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_scarico_ore_components_extended.py::TestScaricoOreComponentsExtended::test_cache_worker_build
1 failed in 5.75s

```
</details>

---
### `tests/unit/test_scarico_ore_components_refactoring.py::test_cache_worker_build_caches_logic`
**Error:** `FAILED tests/unit/test_scarico_ore_components_refactoring.py::test_cache_worker_build_caches_logic`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________________ test_cache_worker_build_caches_logic _____________________
tests\unit\test_scarico_ore_components_refactoring.py:32: in test_cache_worker_build_caches_logic
    display, search, totals, styles = worker._build_caches(raw_data)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ValueError: too many values to unpack (expected 4)
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      20     20     0%   6-133
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                242    242     0%   6-438
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               92     92     0%   1-164
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit_manager.py                                226    226     0%   6-461
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                  60     60     0%   1-121
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     90     90     0%   6-128
src\core\contabilita_manager.py                          106    106     0%   6-243
src\core\contabilita_queries.py                           87     87     0%   6-122
src\core\contabilita_search.py                            91     91     0%   6-178
src\core\contabilita_stats.py                             59     59     0%   6-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            143    143     0%   6-293
src\core\database.py                                     220    220     0%   6-623
src\core\excel_importer.py                                 4      4     0%   6-11
src\core\importers\__init__.py                            43     43     0%   1-111
src\core\importers\attivita.py                            64     64     0%   1-117
src\core\importers\base.py                                63     63     0%   1-92
src\core\importers\certificati.py                        119    119     0%   1-187
src\core\importers\contabilita.py                        140    140     0%   1-260
src\core\importers\giornaliere.py                        189    189     0%   1-309
src\core\importers\scarico_ore.py                        198    198     0%   1-316
src\core\importers\storico_oda.py                         85     85     0%   1-190
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\lyra_client.py                                  128    128     0%   6-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     97     0%   6-204
src\core\oda_manager.py                                   17     17     0%   6-40
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     78     0%   1-110
src\core\secrets_manager.py                               87     53    39%   28-50, 54-58, 62-72, 76-78, 82-86, 91, 96, 101-106, 111-112, 117-119, 124-125, 130-136
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             175    175     0%   1-314
src\core\telegram_bridge.py                              342    342     0%   1-529
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\components\scarico_ore\__init__.py                 6      0   100%
src\gui\components\scarico_ore\cache.py                  108     55    49%   28-102, 105-120, 145, 153-156, 174-175, 182-183, 186-191
src\gui\components\scarico_ore\filters\header.py          30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py     187     43    77%   80, 84, 91-92, 118, 157, 165, 185-190, 200-225, 244-245, 251, 276-281
src\gui\components\scarico_ore\filters\popup_list.py      91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                  169    103    39%   75-81, 84, 87-100, 103-124, 127, 130-134, 155, 165-169, 172-175, 188-214, 219-236, 239-244, 247-274
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                     158    158     0%   1-357
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-333
src\gui\main_window\components\status_bar.py             139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                25     25     0%   1-45
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       20     20     0%   1-49
src\gui\main_window\main.py                              336    336     0%   1-675
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   196    196     0%   6-398
src\gui\panels\carico_ts.py                               90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                  379    379     0%   1-914
src\gui\panels\contabilita_panel.py                      255    255     0%   6-455
src\gui\panels\dashboard_panel.py                        181    181     0%   1-322
src\gui\panels\dettagli_oda.py                           127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra_panel.py                             397    397     0%   1-808
src\gui\panels\notifications_panel.py                    475    475     0%   6-846
src\gui\panels\pdl_db.py                                 202    202     0%   6-367
src\gui\panels\prenota_bp.py                             104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      306    306     0%   7-547
src\gui\panels\scarico_pdl.py                            223    223     0%   6-415
src\gui\panels\scarico_ts.py                             121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                      225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       148    148     0%   1-266
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles.py                                         63     63     0%   6-233
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                      371    371     0%   5-989
src\gui\widgets\bot_parameters.py                        112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            109    109     0%   5-217
src\gui\widgets\excel_table.py                           330    330     0%   6-558
src\gui\widgets\footer_stats.py                          474    474     0%   7-843
src\gui\widgets\info_widgets.py                           95     95     0%   6-174
src\gui\widgets\modern_button.py                          61     61     0%   5-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        183    183     0%   1-340
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       191    191     0%   6-334
src\gui\widgets\toast.py                                 128    128     0%   5-253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                41     41     0%   6-121
src\utils\parsing.py                                      53     20    62%   14, 17, 21, 32-33, 45-46, 60, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                     83     83     0%   1-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-142
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  14721  14293     3%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_scarico_ore_components_refactoring.py::test_cache_worker_build_caches_logic
1 failed in 5.13s

```
</details>

---
### `tests/unit/test_scarico_ore_panel_deep.py::TestScaricoOrePanelDeep::test_update_finished_ui_restore`
**Error:** `FAILED tests/unit/test_scarico_ore_panel_deep.py::TestScaricoOrePanelDeep::test_update_finished_ui_restore`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
___________ TestScaricoOrePanelDeep.test_update_finished_ui_restore ___________
tests\unit\test_scarico_ore_panel_deep.py:122: in test_update_finished_ui_restore
    assert "\u2705" in panel.status_label.text()
E   assert '\u2705' in "27/01/2026 18:54 <font color='green'><b>+10</b></font> <font color='red'><b>-2</b></font> (Tempo: 15.5s)"
E    +  where "27/01/2026 18:54 <font color='green'><b>+10</b></font> <font color='red'><b>-2</b></font> (Tempo: 15.5s)" = <built-in method text of QLabel object at 0x0000016115BEB6B0>()
E    +    where <built-in method text of QLabel object at 0x0000016115BEB6B0> = <PyQt6.QtWidgets.QLabel object at 0x0000016115BEB6B0>.text
E    +      where <PyQt6.QtWidgets.QLabel object at 0x0000016115BEB6B0> = <src.gui.panels.scarico_ore_panel.ScaricoOrePanel object at 0x0000016115BEADF0>.status_label
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    188    22%   53-69, 75, 81, 86, 91-93, 105-109, 119-135, 139, 143, 147, 151-152, 156-157, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 368-372, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-82, 86-87, 94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 172-199, 203-232, 236-244, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 449-470, 474-488, 495-538, 541-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             87     53    39%   28-50, 54-58, 62-72, 76-78, 82-86, 91, 96, 101-106, 111-112, 117-119, 124-125, 130-136
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
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
src\gui\components\scarico_ore\cache.py                                108     55    49%   28-102, 105-120, 145, 153-156, 174-175, 182-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     18    40%   22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187     43    77%   80, 84, 91-92, 118, 157, 165, 185-190, 200-225, 244-245, 251, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169     71    58%   84, 87-100, 127, 137-151, 154-157, 162-169, 173, 184, 189, 193, 201-214, 227-233, 247-274
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-76, 79-90, 93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 104, 107, 110, 113-140, 143-148, 151-154, 158-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 121-129, 133-179, 186, 190-201, 205, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-315, 325-330, 334-347, 351, 355-370, 377-380, 386-391, 395-398
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-110, 114-122, 126-127, 131-187
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-244, 254-297, 301-315, 319-337, 341, 345-467, 471-558, 561-631, 635-731, 734-801, 805-914
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-186, 190-197, 201, 205, 229-245, 249-270, 275-299, 303-305, 309-312, 316-341, 347-367, 370-371, 374-378, 383-404, 407-409, 412-429, 433, 436-455
src\gui\panels\dashboard_panel.py                                      181    158    13%   28-92, 96, 100-107, 111-140, 144-146, 150-160, 164-179, 184-199, 204-222, 227-243, 248-257, 261-278, 282-312, 316-322
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-91, 94-96, 100, 103-115, 118-130, 135-140, 144-150, 153-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 17      9    47%   17-18, 21-33, 37-38
src\gui\panels\dipendenti\pages\anagrafica_page.py                     538    493     8%   53-83, 86-220, 223-333, 336-341, 345-381, 385-400, 405-430, 433-477, 481-489, 493-510, 513-543, 546-558, 561-570, 574-605, 608-645, 650-657, 660-703, 706-708, 711-749, 753-777, 783-826, 834-924, 928-941, 945-968, 972-1005
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra_panel.py                                           397    349    12%   38-40, 43-111, 138-142, 146-164, 178-179, 183-192, 204-212, 216-492, 499-512, 516-521, 525-545, 549-552, 556-560, 564-581, 589-591, 595-598, 602-605, 609-610, 614-619, 629-651, 657-660, 664-678, 682-701, 705-741, 749-766, 772-784, 788-799, 803-808
src\gui\panels\notifications_panel.py                                  475    407    14%   66-70, 73-156, 159-161, 172-184, 187-335, 338-339, 342-353, 356, 359-405, 408-416, 419-420, 423-425, 428-443, 446-448, 455-468, 471-543, 546-547, 551-553, 557-559, 563-565, 569-570, 574-575, 579, 582-586, 591-629, 634-657, 663-691, 699-707, 711-712, 716-734, 738-772, 776-778, 782-801, 805-846
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-51, 58-110, 113-207, 211-222, 226-246, 250-258, 262-280, 284-337, 343-349, 353-367
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-78, 82-84, 87-95, 98-104, 107-117, 121-194
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    306    101    67%   44-46, 51-85, 262-271, 278-306, 331-332, 348-349, 353-355, 359-377, 399-400, 410-411, 416-417, 421-426, 434-435, 450-452, 467, 478-492, 519-522, 529
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-162, 165-173, 176-179, 182-195, 198-209, 212-222, 226-234, 239-246, 249-282, 286-300, 304-326, 330-344, 348-357, 361-385, 389-391, 395-409, 413-415
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-80, 84-86, 90, 94-107, 111-123, 127-132, 136-141, 155-157, 163-223
src\gui\panels\settings\main_panel.py                                  104     79    24%   23-33, 36-98, 101-102, 106-108, 112-130, 133-136, 139, 144-146, 149-162, 165-183
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            317    266    16%   32-33, 36-66, 71-88, 91-114, 117-136, 139-158, 161-180, 183-202, 207-213, 216-217, 226, 236, 248-257, 260-268, 273-276, 279-286, 289-297, 300-313, 316-327, 330-336, 341-350, 353-366, 369-380, 383-389, 394-395, 398, 401-404, 407-412, 415-422, 426, 429, 432, 435, 438, 441, 444, 447, 450, 453, 456, 459, 464-471, 476-491
src\gui\panels\settings\pages\paths_page.py                            107     86    20%   26-27, 30-80, 83-104, 108-129, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179, 184-201, 204-219
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 50, 71, 93-95
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-254, 258-271, 275-285, 289, 293, 297-308, 312-319, 323-332, 336-388, 392-509, 513-541
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-158, 162-178, 182-213, 216-222, 225-232, 236, 239-262, 266
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    346     7%   41-135, 139-156, 165-296, 300-308, 312-330, 342-496, 500-509, 513-525, 534-542, 546, 550-631, 635-647, 655-768, 776-828, 833-925, 930-989
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-171, 174-187, 190-200, 203-208, 211-229, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    292    12%   29-36, 47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     65    33%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 250, 256-259
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     20    62%   14, 17, 21, 32-33, 45-46, 60, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                19559  16082    18%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_scarico_ore_panel_deep.py::TestScaricoOrePanelDeep::test_update_finished_ui_restore
1 failed in 14.47s

```
</details>

---
### `tests/unit/test_search_controller_coverage.py::TestSearchControllerCoverage::test_perform_search_no_results`
**Error:** `FAILED tests/unit/test_search_controller_coverage.py::TestSearchControllerCoverage::test_perform_search_no_results`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestSearchControllerCoverage.test_perform_search_no_results _________
C:\Program Files\Python312\Lib\unittest\mock.py:949: in assert_called_with
    raise AssertionError(_error_message()) from cause
E   AssertionError: expected call not found.
E   Expected: addAction('\u274c Nessun risultato trovato')
E     Actual: addAction('Nessun risultato trovato')

During handling of the above exception, another exception occurred:
tests\unit\test_search_controller_coverage.py:38: in test_perform_search_no_results
    mock_menu_instance.addAction.assert_called_with("\u274c Nessun risultato trovato")
E   AssertionError: expected call not found.
E   Expected: addAction('\u274c Nessun risultato trovato')
E     Actual: addAction('Nessun risultato trovato')
E   
E   pytest introspection follows:
E   
E   Args:
E   assert ('Nessun risultato trovato',) == ('\u274c Nessun ri...ato trovato',)
E     
E     At index 0 diff: 'Nessun risultato trovato' != '\u274c Nessun risultato trovato'
E     Use -v to get more diff
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    164    32%   75, 81, 86, 91-93, 106, 108, 120, 125-135, 139, 143, 147, 151-152, 157, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 369-371, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\scarico_ts\bot.py                           225    118    48%   39, 44, 49, 60, 79-81, 87, 92, 98, 108, 115, 119-121, 126-131, 167, 177-178, 185, 224-233, 237-268, 273, 308-310, 316-353, 357-366, 372-389, 395-417, 421-434
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     20    81%   45-46, 73-75, 107-109, 152-154, 172-173, 183-185, 200, 212-214
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     14    76%   24, 29, 34, 41, 45, 59, 61-62, 67-68, 77, 81, 99-100
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-86, 90-155, 159-223, 228-256, 260-273, 278-323
src\bots\portale_fornitori\timbrature\storage.py                       189    141    25%   96, 117-118, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 172-199, 203-232, 236-244, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 449-470, 474-488, 495-538, 541-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    140    36%   79-90, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             87     53    39%   28-50, 54-58, 62-72, 76-78, 82-86, 91, 96, 101-106, 111-112, 117-119, 124-125, 130-136
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
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
src\gui\components\scarico_ore\cache.py                                108     58    46%   28-102, 105-120, 145, 153-156, 172, 174-175, 180-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     18    40%   22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169     71    58%   84, 87-100, 127, 137-151, 154-157, 162-169, 173, 184, 189, 193, 201-214, 227-233, 247-274
src\gui\controllers\search_controller.py                               197     74    62%   61, 93-94, 101, 118, 135, 152, 164-165, 178-215, 228-264, 277-312, 329-336
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-76, 79-90, 93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 104, 107, 110, 113-140, 143-148, 151-154, 158-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 121-129, 133-179, 186, 190-201, 205, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-315, 325-330, 334-347, 351, 355-370, 377-380, 386-391, 395-398
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-110, 114-122, 126-127, 131-187
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-244, 254-297, 301-315, 319-337, 341, 345-467, 471-558, 561-631, 635-731, 734-801, 805-914
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-186, 190-197, 201, 205, 229-245, 249-270, 275-299, 303-305, 309-312, 316-341, 347-367, 370-371, 374-378, 383-404, 407-409, 412-429, 433, 436-455
src\gui\panels\dashboard_panel.py                                      181    158    13%   28-92, 96, 100-107, 111-140, 144-146, 150-160, 164-179, 184-199, 204-222, 227-243, 248-257, 261-278, 282-312, 316-322
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-91, 94-96, 100, 103-115, 118-130, 135-140, 144-150, 153-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 17      9    47%   17-18, 21-33, 37-38
src\gui\panels\dipendenti\pages\anagrafica_page.py                     538    493     8%   53-83, 86-220, 223-333, 336-341, 345-381, 385-400, 405-430, 433-477, 481-489, 493-510, 513-543, 546-558, 561-570, 574-605, 608-645, 650-657, 660-703, 706-708, 711-749, 753-777, 783-826, 834-924, 928-941, 945-968, 972-1005
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra_panel.py                                           397    349    12%   38-40, 43-111, 138-142, 146-164, 178-179, 183-192, 204-212, 216-492, 499-512, 516-521, 525-545, 549-552, 556-560, 564-581, 589-591, 595-598, 602-605, 609-610, 614-619, 629-651, 657-660, 664-678, 682-701, 705-741, 749-766, 772-784, 788-799, 803-808
src\gui\panels\notifications_panel.py                                  475    407    14%   66-70, 73-156, 159-161, 172-184, 187-335, 338-339, 342-353, 356, 359-405, 408-416, 419-420, 423-425, 428-443, 446-448, 455-468, 471-543, 546-547, 551-553, 557-559, 563-565, 569-570, 574-575, 579, 582-586, 591-629, 634-657, 663-691, 699-707, 711-712, 716-734, 738-772, 776-778, 782-801, 805-846
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-51, 58-110, 113-207, 211-222, 226-246, 250-258, 262-280, 284-337, 343-349, 353-367
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-78, 82-84, 87-95, 98-104, 107-117, 121-194
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    306    102    67%   44-46, 51-85, 262-271, 278-306, 324, 331-332, 348-349, 353-355, 359-377, 399-400, 410-411, 416-417, 421-426, 434-435, 450-452, 467, 478-492, 519-522, 529
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-162, 165-173, 176-179, 182-195, 198-209, 212-222, 226-234, 239-246, 249-282, 286-300, 304-326, 330-344, 348-357, 361-385, 389-391, 395-409, 413-415
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-80, 84-86, 90, 94-107, 111-123, 127-132, 136-141, 155-157, 163-223
src\gui\panels\settings\main_panel.py                                  104     79    24%   23-33, 36-98, 101-102, 106-108, 112-130, 133-136, 139, 144-146, 149-162, 165-183
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            317    266    16%   32-33, 36-66, 71-88, 91-114, 117-136, 139-158, 161-180, 183-202, 207-213, 216-217, 226, 236, 248-257, 260-268, 273-276, 279-286, 289-297, 300-313, 316-327, 330-336, 341-350, 353-366, 369-380, 383-389, 394-395, 398, 401-404, 407-412, 415-422, 426, 429, 432, 435, 438, 441, 444, 447, 450, 453, 456, 459, 464-471, 476-491
src\gui\panels\settings\pages\paths_page.py                            107     86    20%   26-27, 30-80, 83-104, 108-129, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179, 184-201, 204-219
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 50, 71, 93-95
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-254, 258-271, 275-285, 289, 293, 297-308, 312-319, 323-332, 336-388, 392-509, 513-541
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-158, 162-178, 182-213, 216-222, 225-232, 236, 239-262, 266
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    346     7%   41-135, 139-156, 165-296, 300-308, 312-330, 342-496, 500-509, 513-525, 534-542, 546, 550-631, 635-647, 655-768, 776-828, 833-925, 930-989
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-171, 174-187, 190-200, 203-208, 211-229, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    292    12%   29-36, 47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     65    33%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 250, 256-259
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                19929  16185    19%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_search_controller_coverage.py::TestSearchControllerCoverage::test_perform_search_no_results
1 failed in 10.24s

```
</details>

---
### `tests/unit/test_search_features.py::test_search_employees`
**Error:** `FAILED tests/unit/test_search_features.py::test_search_employees - sqlite3.Op...`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________________________ test_search_employees ____________________________
tests\unit\test_search_features.py:131: in test_search_employees
    storage = TimbratureStorage(mock_timbrature_db)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\bots\portale_fornitori\timbrature\storage.py:43: in __init__
    self._ensure_db_exists()
src\bots\portale_fornitori\timbrature\storage.py:87: in _ensure_db_exists
    self._init_schema()
src\bots\portale_fornitori\timbrature\storage.py:79: in _init_schema
    cursor.execute(
E   sqlite3.OperationalError: no such column: codice_fiscale
------------------------------ Captured log call ------------------------------
ERROR    src.core.database:database.py:82 Database Operational Error (test_timbrature.db): no such column: codice_fiscale
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    188    22%   53-69, 75, 81, 86, 91-93, 105-109, 119-135, 139, 143, 147, 151-152, 156-157, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 368-372, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\timbrature\storage.py                       189    155    18%   82, 94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 172-199, 203-232, 236-244, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 449-470, 474-488, 495-538, 541-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    137     0%   6-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     56    47%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     14    85%   26-27, 50, 78-79, 109-110, 119, 122-123, 132-133, 152-153
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102    102     0%   1-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    135    39%   79, 86-90, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\lyra_client.py                                                128    128     0%   6-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     97     0%   6-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     67     0%   7-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             87     53    39%   28-50, 54-58, 62-72, 76-78, 82-86, 91, 96, 101-106, 111-112, 117-119, 124-125, 130-136
src\core\stats_manager.py                                               47     47     0%   6-83
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\service.py                                           175    175     0%   1-314
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\controllers\search_controller.py                               197     69    65%   61, 93-94, 101, 118, 135, 152, 164-165, 178-215, 228-264, 277-312, 327, 335-336
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129    129     0%   1-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 196    196     0%   6-398
src\gui\panels\carico_ts.py                                             90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                                379    379     0%   1-914
src\gui\panels\contabilita_panel.py                                    255    255     0%   6-455
src\gui\panels\dashboard_panel.py                                      181    181     0%   1-322
src\gui\panels\dettagli_oda.py                                         127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-282
src\gui\panels\help_panel.py                                           120    120     0%   6-368
src\gui\panels\lyra_panel.py                                           397    397     0%   1-808
src\gui\panels\notifications_panel.py                                  475    475     0%   6-846
src\gui\panels\pdl_db.py                                               202    202     0%   6-367
src\gui\panels\prenota_bp.py                                           104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                                    306    306     0%   7-547
src\gui\panels\scarico_pdl.py                                          223    223     0%   6-415
src\gui\panels\scarico_ts.py                                           121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                                    225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     148    148     0%   1-266
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-212
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12     12     0%   6-24
src\gui\widgets\activity_feed.py                                       137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    371     0%   5-989
src\gui\widgets\bot_parameters.py                                      112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                                   16     16     0%   6-79
src\gui\widgets\data_table.py                                          109    109     0%   5-217
src\gui\widgets\excel_table.py                                         330    330     0%   6-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     95     0%   6-174
src\gui\widgets\modern_button.py                                        61     61     0%   5-151
src\gui\widgets\notification_card.py                                   220    220     0%   6-531
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-284
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     45     0%   1-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-229
src\gui\widgets\status_card.py                                          59     59     0%   1-131
src\gui\widgets\status_indicator.py                                     42     42     0%   6-68
src\gui\widgets\timeline_widget.py                                     191    191     0%   6-334
src\gui\widgets\toast.py                                               128    128     0%   5-253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     66     0%   6-92
src\utils\helpers.py                                                    97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                              41     41     0%   6-121
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                16219  14781     9%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_search_features.py::test_search_employees - sqlite3.Op...
1 failed in 9.36s

```
</details>

---
### `tests/unit/test_secrets_manager_coverage.py::TestSecretsManager::test_get_api_keys`
**Error:** `FAILED tests/unit/test_secrets_manager_coverage.py::TestSecretsManager::test_get_api_keys`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________________ TestSecretsManager.test_get_api_keys _____________________
tests\unit\test_secrets_manager_coverage.py:73: in test_get_api_keys
    assert SecretsManager.get_github_token() == "secret_value"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: type object 'SecretsManager' has no attribute 'get_github_token'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    188    22%   53-69, 75, 81, 86, 91-93, 105-109, 119-135, 139, 143, 147, 151-152, 156-157, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 368-372, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\timbrature\storage.py                       189    141    25%   96, 117-118, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 172-199, 203-232, 236-244, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 449-470, 474-488, 495-538, 541-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              226    226     0%   6-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    137     0%   6-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     56    47%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     14    85%   26-27, 50, 78-79, 109-110, 119, 122-123, 132-133, 152-153
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102    102     0%   1-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    140    36%   79-90, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\lyra_client.py                                                128    128     0%   6-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     97     0%   6-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     67     0%   7-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             87      8    91%   47-50, 76-78, 96, 119
src\core\stats_manager.py                                               47     47     0%   6-83
src\core\telegram\__init__.py                                            2      2     0%   1-3
src\core\telegram\service.py                                           175    175     0%   1-314
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      2     0%   6-8
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129    129     0%   1-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 196    196     0%   6-398
src\gui\panels\carico_ts.py                                             90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                                379    379     0%   1-914
src\gui\panels\contabilita_panel.py                                    255    255     0%   6-455
src\gui\panels\dashboard_panel.py                                      181    181     0%   1-322
src\gui\panels\dettagli_oda.py                                         127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-282
src\gui\panels\help_panel.py                                           120    120     0%   6-368
src\gui\panels\lyra_panel.py                                           397    397     0%   1-808
src\gui\panels\notifications_panel.py                                  475    475     0%   6-846
src\gui\panels\pdl_db.py                                               202    202     0%   6-367
src\gui\panels\prenota_bp.py                                           104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                                    306    306     0%   7-547
src\gui\panels\scarico_pdl.py                                          223    223     0%   6-415
src\gui\panels\scarico_ts.py                                           121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                                    225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     148    148     0%   1-266
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-212
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12     12     0%   6-24
src\gui\widgets\activity_feed.py                                       137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    371     0%   5-989
src\gui\widgets\bot_parameters.py                                      112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                                   16     16     0%   6-79
src\gui\widgets\data_table.py                                          109    109     0%   5-217
src\gui\widgets\excel_table.py                                         330    330     0%   6-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     95     0%   6-174
src\gui\widgets\modern_button.py                                        61     61     0%   5-151
src\gui\widgets\notification_card.py                                   220    220     0%   6-531
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-284
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     45     0%   1-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-229
src\gui\widgets\status_card.py                                          59     59     0%   1-131
src\gui\widgets\status_indicator.py                                     42     42     0%   6-68
src\gui\widgets\timeline_widget.py                                     191    191     0%   6-334
src\gui\widgets\toast.py                                               128    128     0%   5-253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     66     0%   6-92
src\utils\helpers.py                                                    97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                              41     41     0%   6-121
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                16022  14702     8%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_secrets_manager_coverage.py::TestSecretsManager::test_get_api_keys
1 failed in 5.24s

```
</details>

---
### `tests/unit/test_secrets_manager_refactoring.py::test_get_fallback_key`
**Error:** `FAILED tests/unit/test_secrets_manager_refactoring.py::test_get_fallback_key`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________________________ test_get_fallback_key ____________________________
tests\unit\test_secrets_manager_refactoring.py:70: in test_get_fallback_key
    res = SecretsManager._get_fallback_key()
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: type object 'SecretsManager' has no attribute '_get_fallback_key'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      20     20     0%   6-133
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                242    242     0%   6-438
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               92     92     0%   1-164
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit_manager.py                                226    226     0%   6-461
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                  60     60     0%   1-121
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     90     90     0%   6-128
src\core\contabilita_manager.py                          106    106     0%   6-243
src\core\contabilita_queries.py                           87     87     0%   6-122
src\core\contabilita_search.py                            91     91     0%   6-178
src\core\contabilita_stats.py                             59     59     0%   6-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            143    143     0%   6-293
src\core\database.py                                     220    220     0%   6-623
src\core\excel_importer.py                                 4      4     0%   6-11
src\core\importers\__init__.py                            43     43     0%   1-111
src\core\importers\attivita.py                            64     64     0%   1-117
src\core\importers\base.py                                63     63     0%   1-92
src\core\importers\certificati.py                        119    119     0%   1-187
src\core\importers\contabilita.py                        140    140     0%   1-260
src\core\importers\giornaliere.py                        189    189     0%   1-309
src\core\importers\scarico_ore.py                        198    198     0%   1-316
src\core\importers\storico_oda.py                         85     85     0%   1-190
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\lyra_client.py                                  128    128     0%   6-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     97     0%   6-204
src\core\oda_manager.py                                   17     17     0%   6-40
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     78     0%   1-110
src\core\secrets_manager.py                               96      8    92%   51-54, 127-129, 136-137
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             175    175     0%   1-314
src\core\telegram_bridge.py                              342    342     0%   1-529
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                     158    158     0%   1-357
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-333
src\gui\main_window\components\status_bar.py             139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                25     25     0%   1-45
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       20     20     0%   1-49
src\gui\main_window\main.py                              336    336     0%   1-675
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   196    196     0%   6-398
src\gui\panels\carico_ts.py                               90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                  379    379     0%   1-914
src\gui\panels\contabilita_panel.py                      255    255     0%   6-455
src\gui\panels\dashboard_panel.py                        181    181     0%   1-322
src\gui\panels\dettagli_oda.py                           127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra_panel.py                             397    397     0%   1-808
src\gui\panels\notifications_panel.py                    475    475     0%   6-846
src\gui\panels\pdl_db.py                                 202    202     0%   6-367
src\gui\panels\prenota_bp.py                             104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      306    306     0%   7-547
src\gui\panels\scarico_pdl.py                            223    223     0%   6-415
src\gui\panels\scarico_ts.py                             121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                      225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       148    148     0%   1-266
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles.py                                         63     63     0%   6-233
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                      371    371     0%   5-989
src\gui\widgets\bot_parameters.py                        112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            109    109     0%   5-217
src\gui\widgets\excel_table.py                           330    330     0%   6-558
src\gui\widgets\footer_stats.py                          474    474     0%   7-843
src\gui\widgets\info_widgets.py                           95     95     0%   6-174
src\gui\widgets\modern_button.py                          61     61     0%   5-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        183    183     0%   1-340
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       191    191     0%   6-334
src\gui\widgets\toast.py                                 128    128     0%   5-253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      2     0%   5-17
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     97     0%   6-267
src\utils\log_humanizer.py                                41     41     0%   6-121
src\utils\parsing.py                                      53     53     0%   6-119
src\utils\printing.py                                     83     83     0%   1-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-142
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  14139  14002     1%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_secrets_manager_refactoring.py::test_get_fallback_key
1 failed in 4.86s

```
</details>

---
### `tests/unit/test_settings_panel_coverage.py::TestSettingsPanelCoverage::test_init_ui`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
__________ ERROR at setup of TestSettingsPanelCoverage.test_init_ui ___________
tests\unit\test_settings_panel_coverage.py:52: in panel
    panel = SettingsPanel()
            ^^^^^^^^^^^^^^^
src\gui\panels\settings\main_panel.py:33: in __init__
    self.load_settings()
src\gui\panels\settings\main_panel.py:136: in load_settings
    self.telegram_tab.load_from_config(config)
src\gui\panels\settings\tabs\telegram_tab.py:202: in load_from_config
    self.tg_token_edit.setText(token)
E   TypeError: setText(self, a0: Optional[str]): argument 1 has unexpected type 'MagicMock'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    188    22%   53-69, 75, 81, 86, 91-93, 105-109, 119-135, 139, 143, 147, 151-152, 156-157, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 368-372, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-82, 86-87, 94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 172-199, 203-232, 236-244, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 449-470, 474-488, 495-538, 541-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     37    20%   17-47, 52-57, 62-83, 87
src\core\audit_manager.py                                              226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     64    53%   42, 48, 59-61, 68, 71, 85, 93, 95, 110-112, 117, 122-127, 136-189, 200-208, 216, 222-224, 229-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    152    37%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 218-236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             96     15    84%   51-54, 76, 90, 117-120, 125-129, 136-137
src\core\stats_manager.py                                               47     23    51%   40-45, 48, 52, 56-67, 71-79
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
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\controllers\service_controller.py                              211    142    33%   117, 135-162, 166-350, 362-365, 386-387, 406-407, 425-426, 432-439, 459-479
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51      1    98%   93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 104, 107, 110, 113-140, 143-148, 151-154, 158-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 121-129, 133-179, 186, 190-201, 205, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-315, 325-330, 334-347, 351, 355-370, 377-380, 386-391, 395-398
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-110, 114-122, 126-127, 131-187
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-244, 254-297, 301-315, 319-337, 341, 345-467, 471-558, 561-631, 635-731, 734-801, 805-914
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-186, 190-197, 201, 205, 229-245, 249-270, 275-299, 303-305, 309-312, 316-341, 347-367, 370-371, 374-378, 383-404, 407-409, 412-429, 433, 436-455
src\gui\panels\dashboard_panel.py                                      181    158    13%   28-92, 96, 100-107, 111-140, 144-146, 150-160, 164-179, 184-199, 204-222, 227-243, 248-257, 261-278, 282-312, 316-322
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-91, 94-96, 100, 103-115, 118-130, 135-140, 144-150, 153-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 17      9    47%   17-18, 21-33, 37-38
src\gui\panels\dipendenti\pages\anagrafica_page.py                     538    493     8%   53-83, 86-220, 223-333, 336-341, 345-381, 385-400, 405-430, 433-477, 481-489, 493-510, 513-543, 546-558, 561-570, 574-605, 608-645, 650-657, 660-703, 706-708, 711-749, 753-777, 783-826, 834-924, 928-941, 945-968, 972-1005
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra_panel.py                                           397    349    12%   38-40, 43-111, 138-142, 146-164, 178-179, 183-192, 204-212, 216-492, 499-512, 516-521, 525-545, 549-552, 556-560, 564-581, 589-591, 595-598, 602-605, 609-610, 614-619, 629-651, 657-660, 664-678, 682-701, 705-741, 749-766, 772-784, 788-799, 803-808
src\gui\panels\notifications_panel.py                                  475    407    14%   66-70, 73-156, 159-161, 172-184, 187-335, 338-339, 342-353, 356, 359-405, 408-416, 419-420, 423-425, 428-443, 446-448, 455-468, 471-543, 546-547, 551-553, 557-559, 563-565, 569-570, 574-575, 579, 582-586, 591-629, 634-657, 663-691, 699-707, 711-712, 716-734, 738-772, 776-778, 782-801, 805-846
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-51, 58-110, 113-207, 211-222, 226-246, 250-258, 262-280, 284-337, 343-349, 353-367
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-78, 82-84, 87-95, 98-104, 107-117, 121-194
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   44-46, 51-85, 96-105, 109-252, 256-271, 275-306, 310-312, 316-324, 328-349, 353-355, 359-377, 388-417, 421-426, 430-442, 446-457, 461-462, 466-474, 478-492, 496-515, 519-522, 526-547
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-162, 165-173, 176-179, 182-195, 198-209, 212-222, 226-234, 239-246, 249-282, 286-300, 304-326, 330-344, 348-357, 361-385, 389-391, 395-409, 413-415
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-80, 84-86, 90, 94-107, 111-123, 127-132, 136-141, 155-157, 163-223
src\gui\panels\settings\main_panel.py                                  104     25    76%   101-102, 129-130, 139, 144-146, 149-162, 165-183
src\gui\panels\settings\pages\diag_page.py                              32      2    94%   42-43
src\gui\panels\settings\pages\general_page.py                           43      0   100%
src\gui\panels\settings\pages\lists_page.py                            317    127    60%   226, 236, 248-257, 260-268, 275, 281-286, 289-297, 300-313, 316-327, 330-336, 341-350, 353-366, 369-380, 383-389, 401-404, 407-412, 415-422, 426, 429, 432, 435, 438, 441, 444, 447, 450, 453, 456, 459
src\gui\panels\settings\pages\paths_page.py                            107     19    82%   115, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     33    75%   158-160, 166-168, 176-181, 184-185, 192-194, 202-205, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55      1    98%   113
src\gui\panels\settings\tabs\telegram_tab.py                           136     32    76%   142-149, 154-167, 172-181, 187-191, 201, 204-209, 223-224
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-254, 258-271, 275-285, 289, 293, 297-308, 312-319, 323-332, 336-388, 392-509, 513-541
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-158, 162-178, 182-213, 216-222, 225-232, 236, 239-262, 266
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    346     7%   41-135, 139-156, 165-296, 300-308, 312-330, 342-496, 500-509, 513-525, 534-542, 546, 550-631, 635-647, 655-768, 776-828, 833-925, 930-989
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-171, 174-187, 190-200, 203-208, 211-229, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    292    12%   29-36, 47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     24    76%   165-167, 194-227
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     65    33%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 250, 256-259
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79      8    90%   43-44, 81-83, 133-135
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                19779  15805    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_settings_panel_coverage.py::TestSettingsPanelCoverage::test_init_ui
1 error in 15.03s

```
</details>

---
### `tests/unit/test_settings_panel_deep.py::TestSettingsPanelComplete::test_account_settings_logic`
**Error:** `FAILED tests/unit/test_settings_panel_deep.py::TestSettingsPanelComplete::test_account_settings_logic`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________ TestSettingsPanelComplete.test_account_settings_logic ____________
C:\Program Files\Python312\Lib\unittest\mock.py:918: in assert_called
    raise AssertionError(msg)
E   AssertionError: Expected '_save_settings' to have been called.

During handling of the above exception, another exception occurred:
tests\unit\test_settings_panel_deep.py:47: in test_account_settings_logic
    mock_save.assert_called()
E   AssertionError: Expected '_save_settings' to have been called.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    188    22%   53-69, 75, 81, 86, 91-93, 105-109, 119-135, 139, 143, 147, 151-152, 156-157, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 368-372, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-82, 86-87, 94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 172-199, 203-232, 236-244, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 449-470, 474-488, 495-538, 541-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     64    53%   42, 48, 59-61, 68, 71, 85, 93, 95, 110-112, 117, 122-127, 136-189, 200-208, 216, 222-224, 229-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    142    41%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 226, 236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             96     53    45%   32-54, 58-62, 66-76, 80-82, 86-90, 95, 100, 110, 117-120, 127-129, 134-137, 143-149
src\core\stats_manager.py                                               47     23    51%   40-45, 48, 52, 56-67, 71-79
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
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51      4    92%   86-90, 93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 104, 107, 110, 113-140, 143-148, 151-154, 158-237
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 121-129, 133-179, 186, 190-201, 205, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-315, 325-330, 334-347, 351, 355-370, 377-380, 386-391, 395-398
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-110, 114-122, 126-127, 131-187
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-244, 254-297, 301-315, 319-337, 341, 345-467, 471-558, 561-631, 635-731, 734-801, 805-914
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-186, 190-197, 201, 205, 229-245, 249-270, 275-299, 303-305, 309-312, 316-341, 347-367, 370-371, 374-378, 383-404, 407-409, 412-429, 433, 436-455
src\gui\panels\dashboard_panel.py                                      181    158    13%   28-92, 96, 100-107, 111-140, 144-146, 150-160, 164-179, 184-199, 204-222, 227-243, 248-257, 261-278, 282-312, 316-322
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-91, 94-96, 100, 103-115, 118-130, 135-140, 144-150, 153-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 17      9    47%   17-18, 21-33, 37-38
src\gui\panels\dipendenti\pages\anagrafica_page.py                     538    493     8%   53-83, 86-220, 223-333, 336-341, 345-381, 385-400, 405-430, 433-477, 481-489, 493-510, 513-543, 546-558, 561-570, 574-605, 608-645, 650-657, 660-703, 706-708, 711-749, 753-777, 783-826, 834-924, 928-941, 945-968, 972-1005
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra_panel.py                                           397    349    12%   38-40, 43-111, 138-142, 146-164, 178-179, 183-192, 204-212, 216-492, 499-512, 516-521, 525-545, 549-552, 556-560, 564-581, 589-591, 595-598, 602-605, 609-610, 614-619, 629-651, 657-660, 664-678, 682-701, 705-741, 749-766, 772-784, 788-799, 803-808
src\gui\panels\notifications_panel.py                                  475    407    14%   66-70, 73-156, 159-161, 172-184, 187-335, 338-339, 342-353, 356, 359-405, 408-416, 419-420, 423-425, 428-443, 446-448, 455-468, 471-543, 546-547, 551-553, 557-559, 563-565, 569-570, 574-575, 579, 582-586, 591-629, 634-657, 663-691, 699-707, 711-712, 716-734, 738-772, 776-778, 782-801, 805-846
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-51, 58-110, 113-207, 211-222, 226-246, 250-258, 262-280, 284-337, 343-349, 353-367
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-78, 82-84, 87-95, 98-104, 107-117, 121-194
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   44-46, 51-85, 96-105, 109-252, 256-271, 275-306, 310-312, 316-324, 328-349, 353-355, 359-377, 388-417, 421-426, 430-442, 446-457, 461-462, 466-474, 478-492, 496-515, 519-522, 526-547
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-162, 165-173, 176-179, 182-195, 198-209, 212-222, 226-234, 239-246, 249-282, 286-300, 304-326, 330-344, 348-357, 361-385, 389-391, 395-409, 413-415
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-80, 84-86, 90, 94-107, 111-123, 127-132, 136-141, 155-157, 163-223
src\gui\panels\settings\main_panel.py                                  105     23    78%   104, 131-132, 146-148, 151-164, 167-185
src\gui\panels\settings\pages\diag_page.py                              32      0   100%
src\gui\panels\settings\pages\general_page.py                           43      0   100%
src\gui\panels\settings\pages\lists_page.py                            317    106    67%   226, 236, 248-257, 260-268, 300-313, 316-327, 330-336, 341-350, 353-366, 369-380, 383-389, 407-412, 415-422, 426, 429, 432, 438, 441, 444, 447, 450, 453, 456, 459
src\gui\panels\settings\pages\paths_page.py                            107     19    82%   115, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     29    78%   158-160, 166-168, 181, 184-185, 192-194, 202-205, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55      1    98%   113
src\gui\panels\settings\tabs\telegram_tab.py                           136     26    81%   142-149, 154-167, 172-181, 187-191, 223-224
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-254, 258-271, 275-285, 289, 293, 297-308, 312-319, 323-332, 336-388, 392-509, 513-541
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-158, 162-178, 182-213, 216-222, 225-232, 236, 239-262, 266
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    346     7%   41-135, 139-156, 165-296, 300-308, 312-330, 342-496, 500-509, 513-525, 534-542, 546, 550-631, 635-647, 655-768, 776-828, 833-925, 930-989
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-171, 174-187, 190-200, 203-208, 211-229, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    292    12%   29-36, 47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     24    76%   165-167, 194-227
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     34    73%   141-149, 152-156, 160-162, 166-167, 172-173, 179, 210-217, 225, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     65    33%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 250, 256-259
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     37    53%   43-44, 54-58, 81-83, 102-112, 116-138
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                19569  15632    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_settings_panel_deep.py::TestSettingsPanelComplete::test_account_settings_logic
1 failed in 15.93s

```
</details>

---
### `tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_search_filtering_proxy`
**Error:** `FAILED tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_search_filtering_proxy`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_______________ TestSprintCGUIDeep.test_search_filtering_proxy ________________
tests\unit\test_sprint_c_gui_deep.py:127: in test_search_filtering_proxy
    panel.main_tabs.setCurrentWidget(panel.tab_attivita)
                                     ^^^^^^^^^^^^^^^^^^
E   AttributeError: 'ContabilitaPanel' object has no attribute 'tab_attivita'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242    188    22%   53-69, 75, 81, 86, 91-93, 105-109, 119-135, 139, 143, 147, 151-152, 156-157, 161-175, 179-224, 229-246, 250-252, 261-266, 270-284, 295-329, 333-358, 362-364, 368-372, 376-378, 382, 386-394, 405-417, 421-426, 438
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
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-82, 86-87, 94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 172-199, 203-232, 236-244, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 449-470, 474-488, 495-538, 541-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              226     78    65%   120-122, 138-142, 158-159, 243-249, 255-269, 285, 309-310, 350-352, 354-357, 359-362, 364-366, 368-372, 385-386, 392-399, 418-419, 426-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     34    75%   42, 48, 59-61, 68, 71, 85, 93, 95, 110-112, 117, 122-127, 176-189, 216, 222-224, 238-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    172    29%   35, 79-90, 95-121, 126-127, 132-152, 157-174, 183-184, 203-204, 218-236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     52    51%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 219, 228, 238
src\core\contabilita_queries.py                                         87     27    69%   20, 29-30, 36, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59      1    98%   90
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    143    35%   69-71, 79-90, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\lyra_client.py                                                128     30    77%   22, 55-69, 83, 109-110, 134, 146-147, 161, 169-170, 203-204, 208-212, 249, 257-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             96     58    40%   32-54, 58-62, 66-76, 80-82, 86-90, 95, 100, 105-110, 115-120, 127-129, 134-137, 143-149
src\core\stats_manager.py                                               47     23    51%   40-45, 48, 52, 56-67, 71-79
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
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51      8    84%   79-90, 93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129     48    63%   21-27, 47, 50, 104, 120-122, 138, 165-217, 227-229, 234-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 121-129, 133-179, 186, 190-201, 205, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-315, 325-330, 334-347, 351, 355-370, 377-380, 386-391, 395-398
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-110, 114-122, 126-127, 131-187
src\gui\panels\contabilita_kpi_panel.py                                379    140    63%   347, 355, 466-467, 479-558, 568-631, 642-731, 741-801, 812-914
src\gui\panels\contabilita_panel.py                                    255     79    69%   51-55, 190-197, 201, 234-236, 245, 251-256, 280-281, 303-305, 312, 320-325, 331-332, 336-341, 349-350, 366-367, 370-371, 378, 389, 402-403, 408, 412-429, 433, 436-455
src\gui\panels\dashboard_panel.py                                      181    158    13%   28-92, 96, 100-107, 111-140, 144-146, 150-160, 164-179, 184-199, 204-222, 227-243, 248-257, 261-278, 282-312, 316-322
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-91, 94-96, 100, 103-115, 118-130, 135-140, 144-150, 153-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 17      9    47%   17-18, 21-33, 37-38
src\gui\panels\dipendenti\pages\anagrafica_page.py                     538    493     8%   53-83, 86-220, 223-333, 336-341, 345-381, 385-400, 405-430, 433-477, 481-489, 493-510, 513-543, 546-558, 561-570, 574-605, 608-645, 650-657, 660-703, 706-708, 711-749, 753-777, 783-826, 834-924, 928-941, 945-968, 972-1005
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra_panel.py                                           397    349    12%   38-40, 43-111, 138-142, 146-164, 178-179, 183-192, 204-212, 216-492, 499-512, 516-521, 525-545, 549-552, 556-560, 564-581, 589-591, 595-598, 602-605, 609-610, 614-619, 629-651, 657-660, 664-678, 682-701, 705-741, 749-766, 772-784, 788-799, 803-808
src\gui\panels\notifications_panel.py                                  475    407    14%   66-70, 73-156, 159-161, 172-184, 187-335, 338-339, 342-353, 356, 359-405, 408-416, 419-420, 423-425, 428-443, 446-448, 455-468, 471-543, 546-547, 551-553, 557-559, 563-565, 569-570, 574-575, 579, 582-586, 591-629, 634-657, 663-691, 699-707, 711-712, 716-734, 738-772, 776-778, 782-801, 805-846
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-51, 58-110, 113-207, 211-222, 226-246, 250-258, 262-280, 284-337, 343-349, 353-367
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-78, 82-84, 87-95, 98-104, 107-117, 121-194
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   44-46, 51-85, 96-105, 109-252, 256-271, 275-306, 310-312, 316-324, 328-349, 353-355, 359-377, 388-417, 421-426, 430-442, 446-457, 461-462, 466-474, 478-492, 496-515, 519-522, 526-547
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-162, 165-173, 176-179, 182-195, 198-209, 212-222, 226-234, 239-246, 249-282, 286-300, 304-326, 330-344, 348-357, 361-385, 389-391, 395-409, 413-415
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-80, 84-86, 90, 94-107, 111-123, 127-132, 136-141, 155-157, 163-223
src\gui\panels\settings\main_panel.py                                  105     31    70%   104, 114-132, 141, 146-148, 151-164, 167-185
src\gui\panels\settings\pages\diag_page.py                              32      1    97%   49
src\gui\panels\settings\pages\general_page.py                           43      2    95%   73-76
src\gui\panels\settings\pages\lists_page.py                            317    119    62%   226, 236, 248-257, 260-268, 275, 300-313, 316-327, 330-336, 341-350, 353-366, 369-380, 383-389, 398, 401-404, 407-412, 415-422, 426, 429, 432, 435, 438, 441, 444, 447, 450, 453, 456, 459, 476-491
src\gui\panels\settings\pages\paths_page.py                            107     28    74%   113-129, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179, 204-219
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     29    78%   158-160, 166-168, 181, 184-185, 192-194, 202-205, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55      4    93%   113, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136     34    75%   142-149, 154-167, 172-181, 187-191, 213-226
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-254, 258-271, 275-285, 289, 293, 297-308, 312-319, 323-332, 336-388, 392-509, 513-541
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-158, 162-178, 182-213, 216-222, 225-232, 236, 239-262, 266
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    346     7%   41-135, 139-156, 165-296, 300-308, 312-330, 342-496, 500-509, 513-525, 534-542, 546, 550-631, 635-647, 655-768, 776-828, 833-925, 930-989
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            208     56    73%   192, 205-208, 228, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222     48    78%   217-218, 313, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166     49    70%   132, 149, 176, 186-187, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69      3    96%   123-124, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    289    12%   47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     39    59%   27-60, 63, 83-111, 174
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     24    76%   165-167, 194-227
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     34    73%   141-149, 152-156, 160-162, 166-167, 172-173, 179, 210-217, 225, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     65    33%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 250, 256-259
src\utils\log_humanizer.py                                              41     15    63%   12-26, 86, 112-113
src\utils\parsing.py                                                    53     15    72%   14, 17, 21, 32-33, 45-46, 66, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                19569  14523    26%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_sprint_c_gui_deep.py::TestSprintCGUIDeep::test_search_filtering_proxy
1 failed in 20.95s

```
</details>

---
### `tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_photo`
**Error:** `FAILED tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_photo`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
___________________ TestTelegramUIBridge.test_handle_photo ____________________
C:\Program Files\Python312\Lib\unittest\mock.py:1020: in assert_any_call
    raise AssertionError(
E   AssertionError: send_message_sync('\U0001f4cb **Dati Estratti**\\n\\nPhoto analysis response') call not found

During handling of the above exception, another exception occurred:
tests\unit\test_telegram_bridge.py:242: in test_handle_photo
    self.mock_telegram_service.send_message_sync.assert_any_call(
E   AssertionError: send_message_sync('\U0001f4cb **Dati Estratti**\\n\\nPhoto analysis response') call not found
E   
E   pytest introspection follows:
E   
E   Args:
E   assert ('\U0001f4dd **Dati Es...is response',) == ('\U0001f4cb **Dati Es...is response',)
E     
E     At index 0 diff: '\U0001f4dd **Dati Estratti**\\n\\nPhoto analysis response' != '\U0001f4cb **Dati Estratti**\\n\\nPhoto analysis response'
E     Use -v to get more diff
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              242     81    67%   75, 81, 106, 108, 125-135, 143, 147, 171, 173, 204-206, 219-221, 235, 237-246, 252, 261-266, 274-277, 302-304, 309-310, 316-317, 323-327, 334, 357-358, 362-364, 368-372, 376-378, 382, 386-394, 413-417, 422-426, 438
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
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-82, 86-87, 94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 303-336, 339-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-160, 164-168, 172-199, 203-232, 236-244, 248-289, 293-325, 329-341, 345-373, 377-421, 425-445, 449-470, 474-488, 495-538, 541-586, 590-613
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             92     92     0%   1-164
src\core\app_updater.py                                                 46     46     0%   6-87
src\core\audit_manager.py                                              226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-131, 136-189, 200-208, 213-224, 229-250
src\core\bug_reporter.py                                                60     60     0%   1-121
src\core\config_manager.py                                             241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     54    49%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     34    61%   19-30, 36, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   220    143    35%   69-71, 79-90, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    155     0%   6-295
src\core\license_validator.py                                          183    183     0%   6-366
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-52, 63-87, 99-100, 120-140, 153-163
src\core\schemas.py                                                     78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                                             96     60    38%   32-54, 58-62, 66-76, 80-82, 86-90, 95, 100, 105-110, 115-120, 125-129, 134-137, 143-149
src\core\stats_manager.py                                               47      4    91%   48, 61, 63, 76
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    176    49%   59, 61, 63, 65, 71-72, 87-94, 120, 127-150, 153-156, 160-175, 178-194, 199-202, 205-206, 209-217, 220-228, 231-256, 272-274, 278-281, 291-292, 295-300, 304-321, 324-332, 335-348, 351-364, 370-373, 387-395, 399-425, 472-485, 493-494, 499-500, 506-507, 514-515, 526-527
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   21-55, 60-72, 77-93, 102-120, 129-158, 161-165, 168-182, 185-190, 193-197, 200-225, 228-233, 236-241, 244-245, 248-273, 276-281
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-76, 79-90, 93
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-357
src\gui\dialogs\command_palette.py                                     302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\formatters.py                                                  129     49    62%   21-27, 47, 50, 104, 114, 120-122, 138, 165-217, 227-229, 234-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-333
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            336    336     0%   1-675
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 44-46, 49, 52, 55-79, 83-101, 105-115, 119-126, 130-134, 138-146, 150-152, 155-160, 163-168, 171-175, 179-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 121-129, 133-179, 186, 190-201, 205, 209, 213, 221, 230, 234-239, 243-246, 250-252, 256-267, 271-274, 278-294, 298-302, 306-315, 325-330, 334-347, 351, 355-370, 377-380, 386-391, 395-398
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-110, 114-122, 126-127, 131-187
src\gui\panels\contabilita_kpi_panel.py                                379    140    63%   347, 355, 466-467, 479-558, 568-631, 642-731, 741-801, 812-914
src\gui\panels\contabilita_panel.py                                    255     72    72%   51-55, 194, 201, 234-236, 245, 251-256, 280-281, 303-305, 312, 321, 324-325, 331-332, 336-341, 349-350, 366-367, 370-371, 378, 389, 402-403, 408, 412-429, 433, 436-455
src\gui\panels\dashboard_panel.py                                      181    158    13%   28-92, 96, 100-107, 111-140, 144-146, 150-160, 164-179, 184-199, 204-222, 227-243, 248-257, 261-278, 282-312, 316-322
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-91, 94-96, 100, 103-115, 118-130, 135-140, 144-150, 153-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 17      9    47%   17-18, 21-33, 37-38
src\gui\panels\dipendenti\pages\anagrafica_page.py                     538    493     8%   53-83, 86-220, 223-333, 336-341, 345-381, 385-400, 405-430, 433-477, 481-489, 493-510, 513-543, 546-558, 561-570, 574-605, 608-645, 650-657, 660-703, 706-708, 711-749, 753-777, 783-826, 834-924, 928-941, 945-968, 972-1005
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-165, 168-170, 173-175, 178-180, 183, 188-229, 234-282
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra_panel.py                                           397    349    12%   38-40, 43-111, 138-142, 146-164, 178-179, 183-192, 204-212, 216-492, 499-512, 516-521, 525-545, 549-552, 556-560, 564-581, 589-591, 595-598, 602-605, 609-610, 614-619, 629-651, 657-660, 664-678, 682-701, 705-741, 749-766, 772-784, 788-799, 803-808
src\gui\panels\notifications_panel.py                                  475    407    14%   66-70, 73-156, 159-161, 172-184, 187-335, 338-339, 342-353, 356, 359-405, 408-416, 419-420, 423-425, 428-443, 446-448, 455-468, 471-543, 546-547, 551-553, 557-559, 563-565, 569-570, 574-575, 579, 582-586, 591-629, 634-657, 663-691, 699-707, 711-712, 716-734, 738-772, 776-778, 782-801, 805-846
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-51, 58-110, 113-207, 211-222, 226-246, 250-258, 262-280, 284-337, 343-349, 353-367
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-78, 82-84, 87-95, 98-104, 107-117, 121-194
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   44-46, 51-85, 96-105, 109-252, 256-271, 275-306, 310-312, 316-324, 328-349, 353-355, 359-377, 388-417, 421-426, 430-442, 446-457, 461-462, 466-474, 478-492, 496-515, 519-522, 526-547
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-162, 165-173, 176-179, 182-195, 198-209, 212-222, 226-234, 239-246, 249-282, 286-300, 304-326, 330-344, 348-357, 361-385, 389-391, 395-409, 413-415
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-80, 84-86, 90, 94-107, 111-123, 127-132, 136-141, 155-157, 163-223
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 38-100, 103-104, 108-110, 114-132, 135-138, 141, 146-148, 151-164, 167-185
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            317    266    16%   32-33, 36-66, 71-88, 91-114, 117-136, 139-158, 161-180, 183-202, 207-213, 216-217, 226, 236, 248-257, 260-268, 273-276, 279-286, 289-297, 300-313, 316-327, 330-336, 341-350, 353-366, 369-380, 383-389, 394-395, 398, 401-404, 407-412, 415-422, 426, 429, 432, 435, 438, 441, 444, 447, 450, 453, 456, 459, 464-471, 476-491
src\gui\panels\settings\pages\paths_page.py                            107     86    20%   26-27, 30-80, 83-104, 108-129, 146-147, 150, 153-157, 160-162, 165-167, 170-174, 177-179, 184-201, 204-219
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 50, 71, 93-95
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-254, 258-271, 275-285, 289, 293, 297-308, 312-319, 323-332, 336-388, 392-509, 513-541
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-65, 73-117, 121-139, 143-144
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-82, 86-107, 111-140, 143-150, 153-156, 161-163
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-158, 162-178, 182-213, 216-222, 225-232, 236, 239-262, 266
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles.py                                                       63     63     0%   6-233
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    371    346     7%   41-135, 139-156, 165-296, 300-308, 312-330, 342-496, 500-509, 513-525, 534-542, 546, 550-631, 635-647, 655-768, 776-828, 833-925, 930-989
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-79
src\gui\widgets\contabilita\attivita_tab.py                            208     56    73%   192, 205-208, 228, 232-235, 243-251, 254-257, 260-263, 266-269, 272-275, 278-282, 285-300, 303-308
src\gui\widgets\contabilita\certificati_tab.py                         222     48    78%   217-218, 313, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166     49    70%   132, 149, 176, 186-187, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69      3    96%   123-124, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         330    289    12%   47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-484, 488-528, 533-558
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     39    59%   27-60, 63, 83-111, 174
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 61-63, 67, 71-72, 78-81, 85-88, 92-93, 103-108, 112-151
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-269, 273-314, 319-362, 367
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59     47    20%   19-90, 94-97, 106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-73, 78-85, 88-125, 128-145, 148-153, 156-169, 172-173, 176-178, 183-188, 191-205, 210-217, 221, 224-234, 237-252, 257-262, 265-269, 280-296, 299, 302, 307-334
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     10    23%   11-39
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-56, 61-72, 77-92
src\utils\helpers.py                                                    97     65    33%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 250, 256-259
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-142
src\utils\validators.py                                                 73     46    37%   35, 42-44, 52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                19569  15253    22%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_bridge.py::TestTelegramUIBridge::test_handle_photo
1 failed in 12.33s

```
</details>

---
### `tests/unit/test_telegram_core_deep.py::TestTelegramCoreDeep::test_handle_voice_logic`
**Error:** `FAILED tests/unit/test_telegram_core_deep.py::TestTelegramCoreDeep::test_handle_voice_logic`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
________________ TestTelegramCoreDeep.test_handle_voice_logic _________________
tests\unit\test_telegram_core_deep.py:27: in test_handle_voice_logic
    with patch.object(
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <src.core.telegram.service.TelegramService object at 0x0000016B3BB45E50> does not have the attribute '_process_with_ai'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      20     20     0%   6-133
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                242    242     0%   6-438
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               92     92     0%   1-164
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit_manager.py                                226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                  60     60     0%   1-121
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     90     90     0%   6-128
src\core\contabilita_manager.py                          106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                           87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                            91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                             59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                     220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                 4      0   100%
src\core\importers\__init__.py                            43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                            64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                        119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                        140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                        189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                        198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                         85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\lyra_client.py                                  128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                   17     17     0%   6-40
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                               96     60    38%   32-54, 58-62, 66-76, 80-82, 86-90, 95, 100, 105-110, 115-120, 125-129, 134-137, 143-149
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\telegram\__init__.py                              2      0   100%
src\core\telegram\handlers\callbacks.py                  187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                    47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                    98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                             175    121    31%   54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 225-226, 233-234, 238-239, 249-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                         98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                              342    176    49%   59, 61, 63, 65, 71-72, 87-94, 120, 127-150, 153-156, 160-175, 178-194, 199-202, 205-206, 209-217, 220-228, 231-256, 272-274, 278-281, 291-292, 295-300, 304-321, 324-332, 335-348, 351-364, 370-373, 387-395, 399-425, 472-485, 493-494, 499-500, 506-507, 514-515, 526-527
src\core\telegram_manager.py                               2      0   100%
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                     158    158     0%   1-357
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-333
src\gui\main_window\components\status_bar.py             139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                25     25     0%   1-45
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       20     20     0%   1-49
src\gui\main_window\main.py                              336    336     0%   1-675
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   196    196     0%   6-398
src\gui\panels\carico_ts.py                               90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                  379    379     0%   1-914
src\gui\panels\contabilita_panel.py                      255    255     0%   6-455
src\gui\panels\dashboard_panel.py                        181    181     0%   1-322
src\gui\panels\dettagli_oda.py                           127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra_panel.py                             397    397     0%   1-808
src\gui\panels\notifications_panel.py                    475    475     0%   6-846
src\gui\panels\pdl_db.py                                 202    202     0%   6-367
src\gui\panels\prenota_bp.py                             104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      306    306     0%   7-547
src\gui\panels\scarico_pdl.py                            223    223     0%   6-415
src\gui\panels\scarico_ts.py                             121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                      225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       148    148     0%   1-266
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles.py                                         63     63     0%   6-233
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                      371    371     0%   5-989
src\gui\widgets\bot_parameters.py                        112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            109    109     0%   5-217
src\gui\widgets\excel_table.py                           330    330     0%   6-558
src\gui\widgets\footer_stats.py                          474    474     0%   7-843
src\gui\widgets\info_widgets.py                           95     95     0%   6-174
src\gui\widgets\modern_button.py                          61     61     0%   5-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        183    183     0%   1-340
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       191    191     0%   6-334
src\gui\widgets\toast.py                                 128    128     0%   5-253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\document_generator.py                           13     10    23%   11-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                41     41     0%   6-121
src\utils\parsing.py                                      53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                     83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-142
src\utils\validators.py                                   73     46    37%   35, 42-44, 52, 57-68, 73-88, 94-179, 184-200, 205-208
------------------------------------------------------------------------------------
TOTAL                                                  14569  13554     7%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_core_deep.py::TestTelegramCoreDeep::test_handle_voice_logic
1 failed in 11.88s

```
</details>

---
### `tests/unit/test_telegram_coverage.py::TestTelegramCoverage::test_async_loop_lifecycle`
**Error:** `FAILED tests/unit/test_telegram_coverage.py::TestTelegramCoverage::test_async_loop_lifecycle`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_______________ TestTelegramCoverage.test_async_loop_lifecycle ________________
C:\Program Files\Python312\Lib\unittest\mock.py:2325: in assert_awaited
    raise AssertionError(msg)
E   AssertionError: Expected initialize to have been awaited.

During handling of the above exception, another exception occurred:
tests\unit\test_telegram_coverage.py:51: in test_async_loop_lifecycle
    mock_app.initialize.assert_awaited()
E   AssertionError: Expected initialize to have been awaited.
============================== warnings summary ===============================
tests/unit/test_telegram_coverage.py::TestTelegramCoverage::test_async_loop_lifecycle
  C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\core\telegram\service.py:88: RuntimeWarning: coroutine 'TestTelegramCoverage.test_async_loop_lifecycle.<locals>.mock_execute' was never awaited
    self._execute_loop(lambda: self._main_loop_logic(token))
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      20     20     0%   6-133
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                242    242     0%   6-438
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               92     92     0%   1-164
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit_manager.py                                226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                  60     60     0%   1-121
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     90     90     0%   6-128
src\core\contabilita_manager.py                          106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                           87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                            91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                             59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                     220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                 4      0   100%
src\core\importers\__init__.py                            43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                            64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                        119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                        140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                        189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                        198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                         85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\lyra_client.py                                  128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                   17     17     0%   6-40
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                               96     60    38%   32-54, 58-62, 66-76, 80-82, 86-90, 95, 100, 105-110, 115-120, 125-129, 134-137, 143-149
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\telegram\__init__.py                              2      0   100%
src\core\telegram\handlers\callbacks.py                  187    147    21%   16, 19, 26-31, 36, 39-40, 47-48, 52-54, 59, 71, 77, 88-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                    47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                    98     69    30%   19-42, 47-54, 59-63, 68-90, 101, 103, 118, 120, 135-170
src\core\telegram\service.py                             175    120    31%   54-71, 75-84, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 225-226, 233-234, 238-239, 249-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                         98     47    52%   10, 43-57, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                              342    254    26%   34-43, 58-65, 71-72, 87-94, 120, 127-150, 153-156, 178-194, 199-202, 205-206, 212-215, 220-228, 231-256, 260-285, 288-292, 295-300, 304-321, 324-332, 335-348, 351-364, 368-373, 377-383, 387-395, 399-425, 429-442, 446-453, 458-464, 467-494, 497-509, 512-529
src\core\telegram_manager.py                               2      0   100%
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                     158    158     0%   1-357
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-333
src\gui\main_window\components\status_bar.py             139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                25     25     0%   1-45
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       20     20     0%   1-49
src\gui\main_window\main.py                              336    336     0%   1-675
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   196    196     0%   6-398
src\gui\panels\carico_ts.py                               90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                  379    379     0%   1-914
src\gui\panels\contabilita_panel.py                      255    255     0%   6-455
src\gui\panels\dashboard_panel.py                        181    181     0%   1-322
src\gui\panels\dettagli_oda.py                           127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra_panel.py                             397    397     0%   1-808
src\gui\panels\notifications_panel.py                    475    475     0%   6-846
src\gui\panels\pdl_db.py                                 202    202     0%   6-367
src\gui\panels\prenota_bp.py                             104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      306    306     0%   7-547
src\gui\panels\scarico_pdl.py                            223    223     0%   6-415
src\gui\panels\scarico_ts.py                             121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                      225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       148    148     0%   1-266
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles.py                                         63     63     0%   6-233
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                      371    371     0%   5-989
src\gui\widgets\bot_parameters.py                        112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            109    109     0%   5-217
src\gui\widgets\excel_table.py                           330    330     0%   6-558
src\gui\widgets\footer_stats.py                          474    474     0%   7-843
src\gui\widgets\info_widgets.py                           95     95     0%   6-174
src\gui\widgets\modern_button.py                          61     61     0%   5-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        183    183     0%   1-340
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       191    191     0%   6-334
src\gui\widgets\toast.py                                 128    128     0%   5-253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\document_generator.py                           13     10    23%   11-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                41     41     0%   6-121
src\utils\parsing.py                                      53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                     83     65    22%   21-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-142
src\utils\validators.py                                   73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
------------------------------------------------------------------------------------
TOTAL                                                  14569  13595     7%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_coverage.py::TestTelegramCoverage::test_async_loop_lifecycle
1 failed, 1 warning in 11.87s

```
</details>

---
### `tests/unit/test_telegram_deep_dive.py::TestTelegramDeepDive::test_all_nav_menus`
**Error:** `FAILED tests/unit/test_telegram_deep_dive.py::TestTelegramDeepDive::test_all_nav_menus`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
___________________ TestTelegramDeepDive.test_all_nav_menus ___________________
tests\unit\test_telegram_deep_dive.py:28: in test_all_nav_menus
    await service._handle_nav_actions(menu, mock_query)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'TelegramService' object has no attribute '_handle_nav_actions'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      20     20     0%   6-133
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                242    242     0%   6-438
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               92     92     0%   1-164
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit_manager.py                                226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                  60     60     0%   1-121
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     90     90     0%   6-128
src\core\contabilita_manager.py                          106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                           87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                            91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                             59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                     220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                 4      0   100%
src\core\importers\__init__.py                            43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                            64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                        119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                        140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                        189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                        198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                         85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\lyra_client.py                                  128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204
src\core\oda_manager.py                                   17     17     0%   6-40
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                               96     60    38%   32-54, 58-62, 66-76, 80-82, 86-90, 95, 100, 105-110, 115-120, 125-129, 134-137, 143-149
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\telegram\__init__.py                              2      0   100%
src\core\telegram\handlers\callbacks.py                  187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                    47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                    98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                             175     99    43%   54-71, 75-84, 88, 99-102, 107, 118, 170-171, 175-185, 193-201, 210-220, 225-226, 233-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                         98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                              342    254    26%   34-43, 58-65, 71-72, 87-94, 120, 127-150, 153-156, 178-194, 199-202, 205-206, 212-215, 220-228, 231-256, 260-285, 288-292, 295-300, 304-321, 324-332, 335-348, 351-364, 368-373, 377-383, 387-395, 399-425, 429-442, 446-453, 458-464, 467-494, 497-509, 512-529
src\core\telegram_manager.py                               2      0   100%
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                     158    158     0%   1-357
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-333
src\gui\main_window\components\status_bar.py             139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                25     25     0%   1-45
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       20     20     0%   1-49
src\gui\main_window\main.py                              336    336     0%   1-675
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   196    196     0%   6-398
src\gui\panels\carico_ts.py                               90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                  379    379     0%   1-914
src\gui\panels\contabilita_panel.py                      255    255     0%   6-455
src\gui\panels\dashboard_panel.py                        181    181     0%   1-322
src\gui\panels\dettagli_oda.py                           127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra_panel.py                             397    397     0%   1-808
src\gui\panels\notifications_panel.py                    475    475     0%   6-846
src\gui\panels\pdl_db.py                                 202    202     0%   6-367
src\gui\panels\prenota_bp.py                             104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      306    306     0%   7-547
src\gui\panels\scarico_pdl.py                            223    223     0%   6-415
src\gui\panels\scarico_ts.py                             121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                      225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       148    148     0%   1-266
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles.py                                         63     63     0%   6-233
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                      371    371     0%   5-989
src\gui\widgets\bot_parameters.py                        112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            109    109     0%   5-217
src\gui\widgets\excel_table.py                           330    330     0%   6-558
src\gui\widgets\footer_stats.py                          474    474     0%   7-843
src\gui\widgets\info_widgets.py                           95     95     0%   6-174
src\gui\widgets\modern_button.py                          61     61     0%   5-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        183    183     0%   1-340
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       191    191     0%   6-334
src\gui\widgets\toast.py                                 128    128     0%   5-253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\document_generator.py                           13     10    23%   11-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                41     41     0%   6-121
src\utils\parsing.py                                      53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                     83     65    22%   21-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-142
src\utils\validators.py                                   73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
------------------------------------------------------------------------------------
TOTAL                                                  14569  13612     7%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_deep_dive.py::TestTelegramDeepDive::test_all_nav_menus
1 failed in 11.67s

```
</details>

---
### `tests/unit/test_telegram_handlers_deep.py::TestTelegramHandlersDeep::test_db_actions_strumentale_flow`
**Error:** `FAILED tests/unit/test_telegram_handlers_deep.py::TestTelegramHandlersDeep::test_db_actions_strumentale_flow`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________ TestTelegramHandlersDeep.test_db_actions_strumentale_flow __________
tests\unit\test_telegram_handlers_deep.py:26: in test_db_actions_strumentale_flow
    await service._handle_db_actions(
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'TelegramService' object has no attribute '_handle_db_actions'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      20     20     0%   6-133
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                242    242     0%   6-438
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               92     92     0%   1-164
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit_manager.py                                226    226     0%   6-461
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                  60     60     0%   1-121
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     90     90     0%   6-128
src\core\contabilita_manager.py                          106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                           87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                            91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                             59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                     220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                 4      0   100%
src\core\importers\__init__.py                            43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                            64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                        119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                        140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                        189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                        198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                         85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\lyra_client.py                                  128    128     0%   6-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     97     0%   6-204
src\core\oda_manager.py                                   17     17     0%   6-40
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                               96     60    38%   32-54, 58-62, 66-76, 80-82, 86-90, 95, 100, 105-110, 115-120, 125-129, 134-137, 143-149
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\telegram\__init__.py                              2      0   100%
src\core\telegram\handlers\callbacks.py                  187    110    41%   14-31, 35-43, 47-48, 52-54, 106-110, 116-129, 142-147, 162-167, 198, 205-206, 209-210, 213-214, 219-220, 226, 249, 253-256, 264-280, 286-289, 293-306, 311, 313, 317, 319, 321-324, 331-332, 342-348, 354-367
src\core\telegram\handlers\commands.py                    47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                    98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                             175    129    26%   54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                         98     16    84%   113-114, 198-203, 208-217, 222-223, 242-249, 280-285, 290-295
src\core\telegram_bridge.py                              342    342     0%   1-529
src\core\telegram_manager.py                               2      0   100%
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                     158    158     0%   1-357
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-333
src\gui\main_window\components\status_bar.py             139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                25     25     0%   1-45
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       20     20     0%   1-49
src\gui\main_window\main.py                              336    336     0%   1-675
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   196    196     0%   6-398
src\gui\panels\carico_ts.py                               90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                  379    379     0%   1-914
src\gui\panels\contabilita_panel.py                      255    255     0%   6-455
src\gui\panels\dashboard_panel.py                        181    181     0%   1-322
src\gui\panels\dettagli_oda.py                           127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra_panel.py                             397    397     0%   1-808
src\gui\panels\notifications_panel.py                    475    475     0%   6-846
src\gui\panels\pdl_db.py                                 202    202     0%   6-367
src\gui\panels\prenota_bp.py                             104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      306    306     0%   7-547
src\gui\panels\scarico_pdl.py                            223    223     0%   6-415
src\gui\panels\scarico_ts.py                             121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                      225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       148    148     0%   1-266
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles.py                                         63     63     0%   6-233
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                      371    371     0%   5-989
src\gui\widgets\bot_parameters.py                        112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            109    109     0%   5-217
src\gui\widgets\excel_table.py                           330    330     0%   6-558
src\gui\widgets\footer_stats.py                          474    474     0%   7-843
src\gui\widgets\info_widgets.py                           95     95     0%   6-174
src\gui\widgets\modern_button.py                          61     61     0%   5-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        183    183     0%   1-340
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       191    191     0%   6-334
src\gui\widgets\toast.py                                 128    128     0%   5-253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                41     41     0%   6-121
src\utils\parsing.py                                      53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                     83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-142
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  14569  13754     6%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_handlers_deep.py::TestTelegramHandlersDeep::test_db_actions_strumentale_flow
1 failed in 11.86s

```
</details>

---
### `tests/unit/test_telegram_manager_coverage.py::TestTelegramManagerCoverage::test_cmd_start`
**Error:** `FAILED tests/unit/test_telegram_manager_coverage.py::TestTelegramManagerCoverage::test_cmd_start`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________________ TestTelegramManagerCoverage.test_cmd_start __________________
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
E   AttributeError: module 'src.core.telegram_manager' has no attribute 'config_manager'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      20     20     0%   6-133
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                242    242     0%   6-438
src\bots\base\login_page.py                               94     94     0%   6-179
src\bots\base\wait_helpers.py                            171    171     0%   14-491
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               92     92     0%   1-164
src\core\app_updater.py                                   46     46     0%   6-87
src\core\audit_manager.py                                226    182    19%   29-37, 61, 64-67, 70-74, 78-130, 134-142, 146-147, 150-159, 177-249, 255-269, 275-310, 314-315, 342-388, 392-399, 403-419, 426-461
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-250
src\core\bug_reporter.py                                  60     60     0%   1-121
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-473
src\core\constants.py                                     90     90     0%   6-128
src\core\contabilita_manager.py                          106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                           87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                            91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                             59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                           102    102     0%   1-234
src\core\data_synchronizer.py                            143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                     220    155    30%   56-93, 99-131, 137-147, 152-155, 158, 164-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-555, 562-572, 579-596
src\core\excel_importer.py                                 4      0   100%
src\core\importers\__init__.py                            43     10    77%   32, 49, 63, 76, 80, 91, 104, 109-111
src\core\importers\attivita.py                            64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                        119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                        140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                        189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                        198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                         85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                              155    155     0%   6-295
src\core\license_validator.py                            183    183     0%   6-366
src\core\lyra_client.py                                  128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     97     0%   6-204
src\core\oda_manager.py                                   17     17     0%   6-40
src\core\report_history.py                                67     67     0%   7-163
src\core\schemas.py                                       78     27    65%   68-73, 78-89, 94-96, 101-103, 108-110
src\core\secrets_manager.py                               96     60    38%   32-54, 58-62, 66-76, 80-82, 86-90, 95, 100, 105-110, 115-120, 125-129, 134-137, 143-149
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\telegram\__init__.py                              2      0   100%
src\core\telegram\handlers\callbacks.py                  187    153    18%   14-31, 35-43, 47-48, 52-54, 58-95, 106-110, 116-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 311, 313, 317, 321-324, 329-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                    47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                    98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                             175    115    34%   54-71, 84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 211, 217-218, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                         98     40    59%   10, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 113-114, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                              342    342     0%   1-529
src\core\telegram_manager.py                               2      0   100%
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-170
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         51     51     0%   1-93
src\gui\dialogs\bug_report_dialog.py                     158    158     0%   1-357
src\gui\dialogs\command_palette.py                       302    302     0%   1-527
src\gui\dialogs\confirmation_dialog.py                    27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\formatters.py                                    129    129     0%   1-237
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-333
src\gui\main_window\components\status_bar.py             139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                25     25     0%   1-45
src\gui\main_window\components\tray_icon.py               16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       20     20     0%   1-49
src\gui\main_window\main.py                              336    336     0%   1-675
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   196    196     0%   6-398
src\gui\panels\carico_ts.py                               90     90     0%   6-187
src\gui\panels\contabilita_kpi_panel.py                  379    379     0%   1-914
src\gui\panels\contabilita_panel.py                      255    255     0%   6-455
src\gui\panels\dashboard_panel.py                        181    181     0%   1-322
src\gui\panels\dettagli_oda.py                           127    127     0%   6-233
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   17     17     0%   1-38
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-282
src\gui\panels\help_panel.py                             120    120     0%   6-368
src\gui\panels\lyra_panel.py                             397    397     0%   1-808
src\gui\panels\notifications_panel.py                    475    475     0%   6-846
src\gui\panels\pdl_db.py                                 202    202     0%   6-367
src\gui\panels\prenota_bp.py                             104    104     0%   6-194
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-153
src\gui\panels\scarico_ore_panel.py                      306    306     0%   7-547
src\gui\panels\scarico_pdl.py                            223    223     0%   6-415
src\gui\panels\scarico_ts.py                             121    121     0%   6-223
src\gui\panels\storico_oda_panel.py                      225    225     0%   6-541
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       148    148     0%   1-266
src\gui\panels\timbrature_bot.py                         116    116     0%   6-212
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles.py                                         63     63     0%   6-233
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12     12     0%   6-24
src\gui\widgets\activity_feed.py                         137    137     0%   1-326
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                      371    371     0%   5-989
src\gui\widgets\bot_parameters.py                        112    112     0%   6-217
src\gui\widgets\calendar_date_edit.py                     16     16     0%   6-79
src\gui\widgets\data_table.py                            109    109     0%   5-217
src\gui\widgets\excel_table.py                           330    330     0%   6-558
src\gui\widgets\footer_stats.py                          474    474     0%   7-843
src\gui\widgets\info_widgets.py                           95     95     0%   6-174
src\gui\widgets\modern_button.py                          61     61     0%   5-151
src\gui\widgets\notification_card.py                     220    220     0%   6-531
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     70     0%   1-138
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-284
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-367
src\gui\widgets\security_dashboard.py                    143    143     0%   1-245
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        183    183     0%   1-340
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     45     0%   1-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-229
src\gui\widgets\status_card.py                            59     59     0%   1-131
src\gui\widgets\status_indicator.py                       42     42     0%   6-68
src\gui\widgets\timeline_widget.py                       191    191     0%   6-334
src\gui\widgets\toast.py                                 128    128     0%   5-253
src\gui\widgets\update_banner.py                          35     35     0%   1-53
src\utils\__init__.py                                      2      0   100%
src\utils\document_generator.py                           13     13     0%   5-39
src\utils\document_processor.py                           66     66     0%   6-92
src\utils\helpers.py                                      97     77    21%   22-38, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 219-241, 249-267
src\utils\log_humanizer.py                                41     41     0%   6-121
src\utils\parsing.py                                      53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                     83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-142
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  14569  13748     6%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_telegram_manager_coverage.py::TestTelegramManagerCoverage::test_cmd_start
1 failed in 11.75s

```
</details>

---
