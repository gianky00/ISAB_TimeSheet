# 📊 Test Execution Report

**Date:** 2026-01-25 17:44:31
**Duration:** 165.49s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1031 |
| ✅ Passed | 146 |
| ❌ Failed | 2 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_bot_panels_coverage_boost.py::test_employee_detail_update`
**Error:** `FAILED tests/unit/test_bot_panels_coverage_boost.py::test_employee_detail_update`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________________________ test_employee_detail_update _________________________
C:\Program Files\Python312\Lib\unittest\mock.py:940: in assert_called_with
    raise AssertionError(error_message)
E   AssertionError: expected call not found.
E   Expected: update_employee_details('Mario', 'Rossi', reparto='NUOVO_REPARTO')
E     Actual: not called.

During handling of the above exception, another exception occurred:
tests\unit\test_bot_panels_coverage_boost.py:67: in test_employee_detail_update
    panel.storage.update_employee_details.assert_called_with(
E   AssertionError: expected call not found.
E   Expected: update_employee_details('Mario', 'Rossi', reparto='NUOVO_REPARTO')
E     Actual: not called.
---------------------------- Captured Qt messages -----------------------------
QtWarningMsg: QFSFileEngine::open: No file name specified
QtWarningMsg: QFSFileEngine::open: No file name specified
QtWarningMsg: QFSFileEngine::open: No file name specified
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      6    70%   112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263     74    72%   71, 77, 127-128, 140, 164, 212-214, 226-228, 239, 255, 312-320, 327, 350-351, 355-357, 361-365, 369-371, 375, 379-395, 400, 404, 408-416, 420-428, 447-451, 456-460, 472
src\bots\base\login_page.py                                             94     74    21%   45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          119    119     0%   14-379
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     28    42%   52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-91, 95-106, 117-137, 141-146
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     204    136    33%   51-57, 68-99, 110-129, 133-168, 172-184, 248, 267-275, 294-298, 309-317, 321-341, 351-369, 373-384, 388-401, 407-420
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           216    177    18%   56, 60, 72-75, 79-81, 85-100, 104-121, 125-141, 147-170, 174-210, 214-223, 227-258, 262-300, 306-328, 332-341, 347-362, 368-390, 394-407
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     56    46%   40-46, 73-75, 107-109, 115-154, 160-185, 191-200, 206-215
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159    133    16%   37, 41-56, 63-82, 86-151, 155-219, 224-252, 256-269, 273-307
src\bots\portale_fornitori\timbrature\storage.py                       189    120    37%   94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 334-336, 345, 351-353, 376-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           401    356    11%   25, 30, 35, 40, 45, 56-78, 82-87, 91-99, 103-128, 132-195, 199-203, 207-234, 238-267, 271-279, 283-324, 328-360, 364-376, 380-405, 409-425, 429-449, 453-474, 478-492, 499-542, 545-574, 578-601
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             72      6    92%   53, 97-102
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit_manager.py                                              254     86    66%   56-62, 65-66, 74-100, 183-185, 205, 221-222, 310-312, 319, 321, 345, 369-370, 395-397, 399-402, 404-407, 409-411, 413-417, 430-431, 436-443, 461-462, 469-504
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     22    84%   59-61, 68, 95, 110-112, 117, 121, 124, 180-189, 216, 222-224, 231, 249-250
src\core\config_manager.py                                             240    115    52%   80, 106-112, 133, 138-139, 153-167, 176-177, 196-197, 219, 223-226, 243-244, 249-250, 262, 277, 287-300, 305-315, 324-351, 356-360, 372-374, 379-384, 389, 398-417, 425-471
src\core\constants.py                                                   92      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   212    124    42%   58, 79-90, 99-131, 154-155, 158, 169-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-557, 564-581
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   26, 37, 50, 62, 66, 77, 90, 95-97
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 219-239, 244-252, 257-275, 280-288, 292-295
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 72-76, 99-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                       148    112    24%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204, 216-221, 225, 229, 233, 237-243, 261-275, 287-299, 310-322
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\schemas.py                                                     93     41    56%   67-72, 77-88, 99-127, 132-134, 139-141, 146-148
src\core\secrets_manager.py                                             93     53    43%   28-50, 54-58, 62-72, 76-78, 82-86, 91, 96, 101, 106, 111-116, 121-122, 129, 134-135, 140-146
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   178    158    11%   19-52, 55-67, 72-88, 93-111, 116-145, 148-152, 155-169, 172-177, 180-183, 186-208, 211-215, 218-222, 225-226, 229-249, 252-257
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-76, 79-90, 93
src\gui\formatters.py                                                  129     86    33%   12-27, 37-68, 73, 98, 104, 113-140, 165-217, 227-229, 234-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              56     56     0%   1-314
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            332    332     0%   1-668
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128     23    82%   56, 101, 114-115, 125, 131, 133, 143-145, 167-168, 173-175, 183, 185, 187, 190-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196     72    63%   51-55, 59-72, 84-88, 92-94, 192-198, 209, 213, 221, 230, 250-252, 278-294, 298-302, 306-315, 325-330, 334-347, 351, 377-380, 390, 395-398
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-110, 114-122, 126-127, 131-187
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-244, 254-297, 301-315, 319-337, 341, 345-467, 471-558, 561-631, 635-731, 734-801, 805-914
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-186, 190-197, 201, 205, 229-245, 249-270, 275-299, 303-305, 309-312, 316-341, 347-367, 370-371, 374-378, 383-404, 407-409, 412-429, 433, 436-455
src\gui\panels\dashboard_panel.py                                      174    152    13%   27-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 172-183, 188-206, 211-227, 232-241, 245-262, 266-296, 300-306
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-91, 94-96, 100, 103-115, 118-130, 135-140, 144-150, 153-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 17      9    47%   17-18, 21-33, 37-38
src\gui\panels\dipendenti\pages\anagrafica_page.py                     362    331     9%   50-80, 83-174, 177-294, 297-302, 305-330, 333-392, 395-425, 428-440, 443-452, 455-467, 470-507, 512-519, 522-565, 568-570, 573-611
src\gui\panels\dipendenti\shared.py                                    144    128    11%   24-71, 80-149, 152-154, 157-159, 162-164, 167, 172-213, 218-266
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra_panel.py                                           397    349    12%   38-40, 43-111, 138-142, 146-164, 178-179, 183-192, 204-212, 216-492, 499-512, 516-521, 525-545, 549-552, 556-560, 564-581, 589-591, 595-598, 602-605, 609-610, 614-619, 629-651, 657-660, 664-678, 682-701, 705-741, 749-766, 772-784, 788-799, 803-808
src\gui\panels\notifications_panel.py                                  475    277    42%   66-70, 73-156, 159-161, 342-353, 356, 360, 371, 373, 375, 410, 419-420, 423-425, 436-443, 446-448, 455-468, 471-543, 546-547, 551-553, 557-559, 563-565, 569-570, 574-575, 579, 582-586, 591-629, 634-657, 663-691, 699-707, 711-712, 716-734, 738-772, 776-778, 782-801, 805-846
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-51, 58-110, 113-207, 211-222, 226-246, 250-258, 262-280, 284-337, 343-349, 353-367
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-78, 82-84, 87-95, 98-104, 107-117, 121-194
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   44-46, 51-85, 96-105, 109-252, 256-271, 275-306, 310-312, 316-324, 328-349, 353-355, 359-377, 388-417, 421-426, 430-442, 446-457, 461-462, 466-474, 478-492, 496-515, 519-522, 526-547
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-162, 165-173, 176-179, 182-195, 198-209, 212-222, 226-234, 239-246, 249-282, 286-300, 304-326, 330-344, 348-357, 361-385, 389-391, 395-409, 413-415
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-80, 84-86, 90, 94-107, 111-123, 127-132, 136-141, 155-157, 163-223
src\gui\panels\settings\main_panel.py                                  104     79    24%   23-33, 36-98, 101-102, 106-108, 112-130, 133-136, 139, 144-146, 149-162, 165-183
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            317    266    16%   32-33, 36-66, 71-88, 91-114, 117-136, 139-158, 161-180, 183-202, 207-213, 216-217, 226, 236, 248-257, 260-268, 273-276, 279-286, 289-297, 300-313, 316-327, 330-336, 341-350, 353-366, 369-380, 383-389, 394-395, 398, 401-404, 407-412, 415-422, 426, 429, 432, 435, 438, 441, 444, 447, 450, 453, 456, 459, 464-471, 476-491
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-85, 88-109, 113-134, 151-152, 155, 158-162, 165-167, 170-172, 175-179, 182-184, 187-189, 194-214, 217-235
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 50, 71, 93-95
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-254, 258-271, 275-285, 289, 293, 297-308, 312-319, 323-332, 336-388, 392-509, 513-541
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     29    54%   73-117, 121-139
src\gui\panels\timbrature\components\settings_tab.py                    94     10    89%   143-150, 161-163
src\gui\panels\timbrature\panel.py                                     148     20    86%   198-208, 216-222, 225-232, 236, 246, 261-262, 266
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles.py                                                       63      3    95%   108-109, 113
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    288    267     7%   40-134, 138-155, 164-295, 299-307, 311-329, 340-348, 352, 356-437, 441-453, 461-574, 582-634, 639-717, 722-759
src\gui\widgets\bot_parameters.py                                      112     89    21%   41-45, 48-116, 126-133, 137, 153, 157-159, 163-172, 177, 181-183, 187-191, 201-208, 212, 216-217
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            199    173    13%   52-54, 58-134, 137, 140-153, 156-169, 172-182, 185-190, 193-211, 214-270, 273-277, 280-295, 298-303
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 50     38    24%   38-54, 57-86, 90, 94-112, 116
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         322    285    11%   29-36, 47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 290-292, 295-318, 321-380, 383-386, 389-395, 398-430, 433-436, 439-441, 444, 448-465, 474-501, 506-531
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                                        61     13    79%   52-54, 71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 219-220, 223-254, 258-299, 304-347, 352
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
src\utils\document_processor.py                                         64     21    67%   12-13, 22-31, 48-49, 65-66, 73-74, 84-86
src\utils\helpers.py                                                    97     60    38%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 250, 259-267
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-113, 118-121
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   77     24    69%   40-41, 78-80, 100, 102, 107-109, 114, 117-122, 126-132
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                18689  14148    24%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_bot_panels_coverage_boost.py::test_employee_detail_update
1 failed in 18.43s

```
</details>

---
### `tests/unit/test_bot_panels_deep.py::test_bot_worker_integration`
**Error:** `FAILED tests/unit/test_bot_panels_deep.py::test_bot_worker_integration - Asse...`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________________________ test_bot_worker_integration _________________________
C:\Program Files\Python312\Lib\unittest\mock.py:928: in assert_called_once
    raise AssertionError(msg)
E   AssertionError: Expected 'BotWorker' to have been called once. Called 0 times.

During handling of the above exception, another exception occurred:
tests\unit\test_bot_panels_deep.py:95: in test_bot_worker_integration
    mock_worker_cls.assert_called_once()
E   AssertionError: Expected 'BotWorker' to have been called once. Called 0 times.
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      6    70%   112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              263     74    72%   71, 77, 127-128, 140, 164, 212-214, 226-228, 239, 255, 312-320, 327, 350-351, 355-357, 361-365, 369-371, 375, 379-395, 400, 404, 408-416, 420-428, 447-451, 456-460, 472
src\bots\base\login_page.py                                             94     74    21%   45-61, 65-95, 99-115, 119-125, 132-179
src\bots\base\wait_helpers.py                                          119    119     0%   14-379
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     28    42%   52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-51, 62-81, 92-120
src\bots\portale_fornitori\common\locators.py                           15      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-91, 95-106, 117-137, 141-146
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     204    136    33%   51-57, 68-99, 110-129, 133-168, 172-184, 248, 267-275, 294-298, 309-317, 321-341, 351-369, 373-384, 388-401, 407-420
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-95, 99-104, 108-135
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   29-32, 36, 40-44, 56-83, 94-99, 104-111, 115-149, 155-194, 198-208, 217-247, 251-258, 262-284, 288-300, 304-320, 324-344, 348-376, 380-386
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           216    177    18%   56, 60, 72-75, 79-81, 85-100, 104-121, 125-141, 147-170, 174-210, 214-223, 227-258, 262-300, 306-328, 332-341, 347-362, 368-390, 394-407
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     56    46%   40-46, 73-75, 107-109, 115-154, 160-185, 191-200, 206-215
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 41-45, 49-65, 71-117, 124-125
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         159    133    16%   37, 41-56, 63-82, 86-151, 155-219, 224-252, 256-269, 273-307
src\bots\portale_fornitori\timbrature\storage.py                       189    120    37%   94-119, 125-157, 167-179, 189-197, 202-230, 237-276, 281-296, 334-336, 345, 351-353, 376-377, 381-400, 409-410
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           401    356    11%   25, 30, 35, 40, 45, 56-78, 82-87, 91-99, 103-128, 132-195, 199-203, 207-234, 238-267, 271-279, 283-324, 328-360, 364-376, 380-405, 409-425, 429-449, 453-474, 478-492, 499-542, 545-574, 578-601
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             72      6    92%   53, 97-102
src\core\app_updater.py                                                 46      2    96%   32, 87
src\core\audit_manager.py                                              254     86    66%   56-62, 65-66, 74-100, 183-185, 205, 221-222, 310-312, 319, 321, 345, 369-370, 395-397, 399-402, 404-407, 409-411, 413-417, 430-431, 436-443, 461-462, 469-504
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     22    84%   59-61, 68, 95, 110-112, 117, 121, 124, 180-189, 216, 222-224, 231, 249-250
src\core\config_manager.py                                             240    109    55%   80, 106-112, 133, 138-139, 153-167, 176-177, 196-197, 219, 223-226, 243-244, 277, 287-300, 305-315, 324-351, 360, 372-374, 379-384, 389, 398-417, 425-471
src\core\constants.py                                                   92      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-135, 144-153, 162-171, 180-189, 194, 199, 204, 209, 214, 219, 228, 238, 243
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 148-160, 174-178
src\core\contabilita_stats.py                                           59     38    36%   31-53, 58-84, 89-105
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-81, 102-128, 132-153, 158-168, 178-188, 198-208, 213-223, 228-234
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-57, 64-74, 80-111, 117-160, 166-167, 179-217, 223, 235, 246-262, 269-293
src\core\database.py                                                   212    124    42%   58, 79-90, 99-131, 154-155, 158, 169-185, 193-254, 259-265, 273-292, 297-301, 311-342, 350-397, 406-408, 416-433, 438-478, 485-533, 538-540, 547-557, 564-581
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   26, 37, 50, 62, 66, 77, 90, 95-97
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-99, 103-117
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 70-74, 79-95, 102-126, 131-142, 147-153, 158-187
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-105, 112-129, 134-202, 207-221, 226-252, 257-260
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-86, 95-111, 117-136, 142-180, 184-201, 205-229, 233-285, 289-309
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-87, 95-113, 117-137, 151-182, 186-250, 254-263, 280-284, 288-316
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-171, 176-190
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-149, 154-196, 201-203, 208-214, 219-239, 244-252, 257-275, 280-288, 292-295
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 72-76, 99-117, 123-143, 148-155, 169-193, 203-229, 240-241, 250-274, 279-297, 302-350, 355-358, 363-366
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-110, 114-147, 156-212, 221-259
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                       148    112    24%   30-36, 39-46, 50-59, 63-76, 80-84, 103-150, 154-156, 160, 168-175, 179-188, 192-197, 201-204, 216-221, 225, 229, 233, 237-243, 261-275, 287-299, 310-322
src\core\oda_manager.py                                                 17      6    65%   22, 31-40
src\core\schemas.py                                                     93     41    56%   67-72, 77-88, 99-127, 132-134, 139-141, 146-148
src\core\secrets_manager.py                                             93     53    43%   28-50, 54-58, 62-72, 76-78, 82-86, 91, 96, 101, 106, 111-116, 121-122, 129, 134-135, 140-146
src\core\stats_manager.py                                               47     16    66%   40-45, 48, 61, 63, 71-79, 83
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-147, 153-249, 253-256, 264-280, 286-289, 293-306, 310-332, 336-348, 354-367
src\core\telegram\handlers\commands.py                                  47     39    17%   13-35, 53-78, 86-89, 97-101
src\core\telegram\handlers\messages.py                                  98     84    14%   19-42, 47-54, 59-63, 68-90, 100-109, 117-127, 135-170
src\core\telegram\service.py                                           175    140    20%   38-48, 54-71, 75-84, 88, 92-104, 107, 117-155, 158-171, 175-185, 193-201, 210-220, 224-234, 237-250, 253-266, 269-281, 284-297, 300-314
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 28, 33-38, 43-57, 62-74, 79-87, 92-96, 101, 106-118, 123-140, 145-154, 159-168, 173, 183, 198-203, 208-217, 222-223, 242-249, 254-259, 264-275, 280-285, 290-295
src\core\telegram_bridge.py                                            342    342     0%   1-529
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-68, 73-83, 88-93, 100-110, 116-150, 155-163, 168-170
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\accessibility.py                                                18      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   178    158    11%   19-52, 55-67, 72-88, 93-111, 116-145, 148-152, 155-169, 172-177, 180-183, 186-208, 211-215, 218-222, 225-226, 229-249, 252-257
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-134, 137-151, 154-157, 162-169, 172-175, 178-180, 183-185, 188-214, 219-236, 239-244, 247-274
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-76, 79-90, 93
src\gui\formatters.py                                                  129     86    33%   12-27, 37-68, 73, 98, 104, 113-140, 165-217, 227-229, 234-235
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              56     56     0%   1-314
src\gui\main_window\components\status_bar.py                           139    139     0%   1-253
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-45
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-42
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-49
src\gui\main_window\main.py                                            332    332     0%   1-668
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128     23    82%   56, 101, 114-115, 125, 131, 133, 143-145, 167-168, 173-175, 183, 185, 187, 190-191, 194-196
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196     33    83%   59-72, 84-88, 92-94, 209, 221, 230, 250-252, 336-345, 377-380, 390, 397
src\gui\panels\carico_ts.py                                             90     54    40%   39-43, 96-99, 103-110, 114-122, 126-127, 131-187
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-244, 254-297, 301-315, 319-337, 341, 345-467, 471-558, 561-631, 635-731, 734-801, 805-914
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-186, 190-197, 201, 205, 229-245, 249-270, 275-299, 303-305, 309-312, 316-341, 347-367, 370-371, 374-378, 383-404, 407-409, 412-429, 433, 436-455
src\gui\panels\dashboard_panel.py                                      174    152    13%   27-81, 85, 89-96, 100-129, 133-135, 139-149, 153-168, 172-183, 188-206, 211-227, 232-241, 245-262, 266-296, 300-306
src\gui\panels\dettagli_oda.py                                         127     72    43%   37-41, 94-96, 100, 103-115, 119, 135-140, 144-150, 153-233
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 17      9    47%   17-18, 21-33, 37-38
src\gui\panels\dipendenti\pages\anagrafica_page.py                     362    331     9%   50-80, 83-174, 177-294, 297-302, 305-330, 333-392, 395-425, 428-440, 443-452, 455-467, 470-507, 512-519, 522-565, 568-570, 573-611
src\gui\panels\dipendenti\shared.py                                    144    128    11%   24-71, 80-149, 152-154, 157-159, 162-164, 167, 172-213, 218-266
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-171, 175-195, 198-207, 210-218, 221-224, 227, 247, 267, 279, 293, 304, 317, 329, 340, 350, 360, 368
src\gui\panels\lyra_panel.py                                           397    349    12%   38-40, 43-111, 138-142, 146-164, 178-179, 183-192, 204-212, 216-492, 499-512, 516-521, 525-545, 549-552, 556-560, 564-581, 589-591, 595-598, 602-605, 609-610, 614-619, 629-651, 657-660, 664-678, 682-701, 705-741, 749-766, 772-784, 788-799, 803-808
src\gui\panels\notifications_panel.py                                  475    277    42%   66-70, 73-156, 159-161, 342-353, 356, 360, 371, 373, 375, 410, 419-420, 423-425, 436-443, 446-448, 455-468, 471-543, 546-547, 551-553, 557-559, 563-565, 569-570, 574-575, 579, 582-586, 591-629, 634-657, 663-691, 699-707, 711-712, 716-734, 738-772, 776-778, 782-801, 805-846
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-51, 58-110, 113-207, 211-222, 226-246, 250-258, 262-280, 284-337, 343-349, 353-367
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-78, 82-84, 87-95, 98-104, 107-117, 121-194
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-68, 71-76, 79-82, 87-92, 102-136, 141-148, 151-153
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   44-46, 51-85, 96-105, 109-252, 256-271, 275-306, 310-312, 316-324, 328-349, 353-355, 359-377, 388-417, 421-426, 430-442, 446-457, 461-462, 466-474, 478-492, 496-515, 519-522, 526-547
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-162, 165-173, 176-179, 182-195, 198-209, 212-222, 226-234, 239-246, 249-282, 286-300, 304-326, 330-344, 348-357, 361-385, 389-391, 395-409, 413-415
src\gui\panels\scarico_ts.py                                           121     29    76%   37-39, 84-86, 105, 112, 127-132, 136-141, 174-185, 195-199
src\gui\panels\settings\main_panel.py                                  104     79    24%   23-33, 36-98, 101-102, 106-108, 112-130, 133-136, 139, 144-146, 149-162, 165-183
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-38, 42-43, 46, 49
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-76
src\gui\panels\settings\pages\lists_page.py                            317    266    16%   32-33, 36-66, 71-88, 91-114, 117-136, 139-158, 161-180, 183-202, 207-213, 216-217, 226, 236, 248-257, 260-268, 273-276, 279-286, 289-297, 300-313, 316-327, 330-336, 341-350, 353-366, 369-380, 383-389, 394-395, 398, 401-404, 407-412, 415-422, 426, 429, 432, 435, 438, 441, 444, 447, 450, 453, 456, 459, 464-471, 476-491
src\gui\panels\settings\pages\paths_page.py                            116     94    19%   26-27, 30-85, 88-109, 113-134, 151-152, 155, 158-162, 165-167, 170-172, 175-179, 182-184, 187-189, 194-214, 217-235
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 50, 71, 93-95
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-153, 156-163, 166-168, 171, 176-181, 184-185, 188-207, 210-236
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-106, 113, 116-118, 121-123
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-139, 142-149, 154-167, 172-181, 187-191, 199-209, 213-226
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-254, 258-271, 275-285, 289, 293, 297-308, 312-319, 323-332, 336-388, 392-509, 513-541
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     29    54%   73-117, 121-139
src\gui\panels\timbrature\components\settings_tab.py                    94      4    96%   147, 161-163
src\gui\panels\timbrature\panel.py                                     148     19    87%   198-208, 216-222, 225-232, 246, 261-262, 266
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-57, 62-64, 68-69, 72-87, 91-102, 106-111, 116-207, 210-212
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles.py                                                       63      3    95%   108-109, 113
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-185, 189, 193-195, 204-212, 215-267, 272, 277-326
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-133
src\gui\widgets\autopilot_widget.py                                    288    267     7%   40-134, 138-155, 164-295, 299-307, 311-329, 340-348, 352, 356-437, 441-453, 461-574, 582-634, 639-717, 722-759
src\gui\widgets\bot_parameters.py                                      112     13    88%   153, 157-159, 169-172, 183, 205-208
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            199    173    13%   52-54, 58-134, 137, 140-153, 156-169, 172-182, 185-190, 193-211, 214-270, 273-277, 280-295, 298-303
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-302, 311-336, 344-381, 386-397, 401-410, 414-417, 421-424, 428-441, 444-451, 454-464, 468-575
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-92, 96, 99-128, 131-138, 142, 145-166, 169-188, 194-216, 219-238, 241-257
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 50     38    24%   38-54, 57-86, 90, 94-112, 116
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-125, 129, 133-134, 137-162, 165-171, 175-183, 186-188, 192-209, 213, 217
src\gui\widgets\excel_table.py                                         322    211    34%   47-60, 64-71, 75-92, 96-116, 119-120, 123-124, 128-139, 143-167, 171-197, 201-220, 224-244, 248-259, 262-267, 270-274, 277-281, 321-380, 389-395, 424, 433-436, 439-441, 486-493, 499-500, 506-531
src\gui\widgets\footer_stats.py                                        474    474     0%   7-843
src\gui\widgets\info_widgets.py                                         95     80    16%   27-60, 63, 70-78, 83-111, 118-168, 171, 174
src\gui\widgets\modern_button.py                                        61     11    82%   71-72, 78-81, 85-88, 149
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-343, 347-357, 361, 365-367, 381-415, 419-436, 440-444, 448-450, 454-455, 459-463, 468-469, 473-514, 518-522, 526-531
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-129, 133-135, 138
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-233, 238-239, 243-244, 249-256, 260-261, 270-272, 276, 280, 284
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 219-220, 223-254, 258-299, 304-347, 352
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-245
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-340
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-113, 116-154, 158-160, 164-177, 185-229
src\gui\widgets\status_card.py                                          59      8    86%   106-122, 126, 130-131
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191     43    77%   80-81, 83-84, 131-135, 137-141, 145, 148-153, 161-169, 172-173, 176-178, 191-205, 239-249, 268
src\gui\widgets\toast.py                                               128     98    23%   55-77, 81-122, 126-149, 152-156, 160-162, 166-167, 170-182, 193-195, 205-233, 238, 243, 248, 253
src\gui\widgets\update_banner.py                                        35     35     0%   1-53
src\utils\__init__.py                                                    2      0   100%
src\utils\document_generator.py                                         13     13     0%   5-39
src\utils\document_processor.py                                         64     21    67%   12-13, 22-31, 48-49, 65-66, 73-74, 84-86
src\utils\helpers.py                                                    97     55    43%   24-30, 43-47, 63-85, 98-100, 105, 132-133, 141, 154-168, 182-184, 199-205, 220, 239, 250, 259
src\utils\log_humanizer.py                                              41     14    66%   12-26, 112, 120
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-145
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   77     24    69%   40-41, 78-80, 100, 102, 107-109, 114, 117-122, 126-132
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                18689  13632    27%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_bot_panels_deep.py::test_bot_worker_integration - Asse...
1 failed in 14.92s

```
</details>

---
