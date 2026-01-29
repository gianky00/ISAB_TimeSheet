# 📊 Test Execution Report

**Date:** 2026-01-29 11:51:54
**Duration:** 466.91s

## Summary
| Metric | Count |
|---|---|
| 🧪 Total | 1001 |
| ✅ Passed | 809 |
| ❌ Failed | 13 |
| ⏩ Skipped | 0 |

## ❌ Failures Details
### `tests/unit/test_app_initializer_coverage.py::TestAppInitializerCoverage::test_check_license_valid_immediate`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
_ ERROR at setup of TestAppInitializerCoverage.test_check_license_valid_immediate _
tests\unit\test_app_initializer_coverage.py:14: in mock_license
    "get_status": mocker.patch("src.core.app_initializer.get_detailed_license_status"),
.venv\Lib\site-packages\pytest_mock\plugin.py:419: in __call__
    return self._start_patch(
.venv\Lib\site-packages\pytest_mock\plugin.py:229: in _start_patch
    mocked: MockType = p.start()
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.core.app_initializer' from 'C:\\Users\\Coemi\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\app_initializer.py'> does not have the attribute 'get_detailed_license_status'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      6    70%   112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              241    188    22%   52-68, 74, 80, 85, 90-92, 104-108, 118-130, 134, 138, 142, 146-147, 151-152, 156-170, 174-219, 224-241, 245-247, 254-259, 263-273, 284-318, 322-347, 351-353, 357-361, 365-367, 371, 375-381, 392-404, 408-413, 425
src\bots\base\login_page.py                                             94     78    17%   34-37, 43-53, 57-77, 81-93, 97-103, 110-154
src\bots\base\wait_helpers.py                                          171    144    16%   49-54, 75-80, 99-103, 134-197, 220, 249-307, 327-328, 331-335, 348, 351-355, 377-380, 383-395, 425-441, 471-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     28    42%   52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-92, 96-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   38-41, 45, 49-55, 66-91, 102-115, 119-148, 152-162, 186-283, 287-305, 315-341, 345-354, 358-367, 371-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    186    17%   56, 60, 72-75, 79-81, 85-100, 104-121, 125-140, 144-166, 170-198, 202-211, 215-240, 244-276, 282-311, 315-324, 328-343, 347-367, 371-384
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     83    20%   27-30, 34, 38-44, 48-65, 69-91, 95-124, 128-145, 149-154, 158-167
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-107
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-84, 88-149, 153-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    120    37%   88-111, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 320-322, 331, 337-339, 362-363, 367-384, 391-392
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-156, 160-164, 168-193, 197-226, 230-238, 242-279, 283-311, 315-327, 331-359, 363-405, 409-425, 429-450, 454-466, 473-512, 515-560, 564-583
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     74    18%   16-18, 30-69, 75-126, 130-145, 150-158
src\core\app_updater.py                                                 46     37    20%   17-45, 50-55, 60-81, 85
src\core\audit_manager.py                                              226    103    54%   61, 71, 120-122, 134-138, 152-153, 233-237, 243-257, 261-294, 334-336, 338-341, 343-346, 348-350, 352-356, 369-370, 376-381, 385-399, 406-441
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-187, 198-206, 211-222, 227-248
src\core\bug_reporter.py                                                60     45    25%   32-102, 107-119
src\core\config_manager.py                                             241    120    50%   35, 87, 101-102, 113-119, 140, 145-146, 160-174, 183-184, 203-204, 226, 230-233, 250-251, 256-257, 262-264, 269, 284, 294-307, 312-322, 331-358, 363-367, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-131, 140-147, 156-161, 170-177, 182, 187, 192, 197, 202, 207, 216, 224, 229
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-55, 60-70, 76-102, 108-146, 150-151, 159-194, 198, 208, 219-232, 239-260
src\core\database.py                                                   220    141    36%   58, 77-88, 95-125, 129-133, 136-139, 142, 148-167, 175-236, 241-245, 253-272, 277-279, 287-318, 326-369, 376-378, 386-401, 406-446, 453-501, 506-508, 513-519, 526-536, 541-558
src\core\employees.py                                                   89     73    18%   25-63, 67-69, 76-99, 104-120, 127-182
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 61, 72, 76, 87, 98, 103-105
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-96, 100-114
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 68-72, 77-93, 100-124, 129-140, 145-151, 156-185
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-101, 108-125, 130-183, 188-202, 207-231, 236-239
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-84, 93-109, 115-134, 140-178, 182-197, 201-223, 227-279, 283-299
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-85, 93-111, 115-135, 149-180, 184-248, 252-261, 278-282, 286-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-148, 153-195, 200-202, 207-213, 218-238, 243-251, 256-274, 279-287, 291-294
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 79-111, 117-133, 138-145, 159-183, 193-219, 230-231, 240-264, 269-287, 292-340, 345-348, 353-356
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-108, 112-143, 152-206, 215-253
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-148, 152-154, 158, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                                 17      6    65%   22, 31-36
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-50, 61-85, 95-96, 114-134, 147-157
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     58    40%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 124-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    140    20%   38-48, 52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    289    15%   28-30, 34-43, 47-65, 69-72, 76-80, 84-88, 91-111, 114-133, 136-139, 143-158, 161-171, 174-177, 180-181, 184-190, 193-199, 202-223, 227-250, 253-257, 260-265, 269-284, 287-293, 296-309, 312-325, 329-334, 338-344, 348-354, 358-384, 388-401, 405-412, 415-421, 424-447, 450-462, 465-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   19-53, 56-64, 67-83, 92-110, 119-144, 147-151, 154-168, 171-176, 179-183, 186-211, 214-219, 222-227, 230-231, 234-259, 262-267
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-132, 135-149, 152-155, 158-165, 168-171, 174-176, 179-181, 184-210, 213-230, 233-235, 238-265
src\gui\controllers\bot_controller.py                                   38     30    21%   17-20, 24-32, 36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           154    125    19%   36-37, 41-57, 61-77, 80-94, 97-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 158-164, 168-172, 176-182, 194-230, 234-250, 254-256, 260-261, 265-266, 270-303, 307-308
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-53, 61-123, 130-160, 164-340, 352-355, 372-380, 393-434, 447-463, 467, 471-480
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-74, 77-84, 87
src\gui\dialogs\bug_report_dialog.py                                   158    139    12%   31-32, 35-42, 49-53, 56-125, 128-147, 150-172, 176-328, 332-349
src\gui\dialogs\command_palette.py                                     302    274     9%   39-68, 72-183, 187-213, 216-224, 227-233, 236-241, 244-251, 254-289, 293-302, 305-312, 315-321, 324-330, 334-338, 342-354, 358-369, 372-379, 382-386, 389-433, 436-472, 476-492, 495-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 102, 105, 108, 111-136, 139-141, 144-147, 151-230
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     55    24%   17-22, 26-32, 36-48, 52-63, 68-77, 81-329
src\gui\main_window\components\status_bar.py                           158    141    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-278
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-39
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 27-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     20     13    35%   9-10, 15-26, 30-40
src\gui\main_window\main.py                                            280    206    26%   46-95, 99-133, 145-150, 153-177, 180-186, 190, 193, 196, 199, 202, 205, 208, 211, 215-241, 244, 247-266, 269-273, 281-285, 293-297, 303-307, 313-315, 318-320, 323-325, 328-330, 333-335, 338-342, 345-356, 359-361, 364-380, 383-386, 389-392, 395-399, 402-404, 407-410, 413, 416, 419-420, 425, 429, 433, 437, 441, 445
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          128    104    19%   28-31, 40-42, 45, 48, 51-75, 79-97, 101-111, 115-122, 126-130, 134-142, 146-148, 151-153, 156-161, 164-168, 172-184, 187-189
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 119-127, 131-175, 182, 186-197, 201, 205, 209, 217, 226, 230-235, 239-242, 246-248, 252-263, 267-270, 274-290, 294-298, 302-307, 317-320, 324-337, 341, 345-360, 367-370, 374-379, 383-386
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-108, 112-120, 124-125, 129-183
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-240, 250-291, 295-309, 313-331, 335, 339-449, 453-538, 541-609, 613-705, 708-773, 777-878
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-180, 184-191, 195, 199, 223-239, 243-264, 269-293, 297-299, 303-306, 310-335, 339-357, 360-361, 364-368, 371-388, 391-393, 396-413, 417, 420-439
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-126, 130-132, 136-146, 150-165, 170-185, 190-208, 213-227, 232-241, 245-260, 264-292, 296-302
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-89, 92-94, 98, 101-113, 116-126, 129-131, 135-141, 144-220
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     530    485     8%   53-83, 86-206, 209-314, 317-322, 326-360, 364-377, 380-408, 411-455, 459-467, 471-488, 491-518, 521-533, 536-545, 549-580, 583-616, 621-626, 629-670, 673-675, 678-714, 718-740, 744-787, 795-881, 885-896, 900-922, 926-959
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-159, 162-164, 167-169, 172-174, 177, 182-223, 228-276
src\gui\panels\dipendenti_manager_panel.py                             156    137    12%   27-69, 72, 83-95, 98-123, 126-157, 160-190, 194-223, 227-243, 247-266, 269-281, 288-315
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-167, 171-191, 194-203, 206-214, 217-220, 223, 243, 263, 275, 289, 300, 313, 325, 336, 346, 356, 364
src\gui\panels\lyra_panel.py                                           349    303    13%   60-64, 68-86, 98-99, 103-112, 124-132, 136-400, 407-420, 424-425, 429-449, 453-456, 460-464, 468-483, 491-493, 497-500, 504-507, 511-512, 516-521, 531-551, 557-560, 564-578, 582-599, 603-635, 643-656, 660-672, 676-687, 691-696
src\gui\panels\notifications_panel.py                                  247    201    19%   56-69, 72-140, 143-144, 148-150, 154-156, 160-162, 166-167, 171-172, 176, 179-183, 188-223, 228-251, 255-281, 289-297, 301-302, 306-324, 328-360, 364-366, 370-389, 393-432
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-49, 56-108, 111-201, 205-216, 220-240, 244-250, 254-270, 274-327, 333-337, 341-353
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-76, 80-82, 85-93, 96-102, 105-115, 119-190
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-66, 69-72, 75-76, 79-84, 94-126, 131-138, 141-143
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   42-44, 49-83, 94-101, 105-234, 238-253, 257-285, 289-291, 295-303, 307-328, 332-334, 338-356, 367-396, 400-405, 409-421, 425-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-160, 163-171, 174-177, 180-193, 196-201, 204-214, 218-226, 231-238, 241-272, 276-288, 292-314, 318-332, 336-343, 347-369, 373-375, 379-393, 397-399
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-78, 82-84, 88, 92-105, 109-117, 121-123, 127-132, 146-148, 154-210
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-182
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-36, 40-41, 44, 47
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-74
src\gui\panels\settings\pages\lists_page.py                            319    268    16%   32-33, 36-62, 67-84, 87-104, 107-126, 129-148, 151-170, 173-192, 197-203, 206-207, 214, 224, 234-243, 246-254, 259-262, 265-272, 275-283, 286-302, 305-315, 318-324, 329-338, 341-355, 358-368, 371-377, 382-383, 386, 389-392, 395-400, 403-410, 414, 417, 420, 423, 426, 429, 432, 435, 438, 441, 444, 447, 452-457, 460-465
src\gui\panels\settings\pages\paths_page.py                            107     86    20%   26-27, 30-68, 71-90, 94-115, 132-133, 136, 139-141, 144-146, 149-151, 154-156, 159-161, 166-181, 184-189
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 98-100
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-104, 111, 114-116, 119-121
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-129, 132-137, 140-153, 156-165, 169-173, 181-191, 195-208
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-248, 252-265, 269-279, 283, 287, 291-302, 306-313, 317-324, 328-380, 384-497, 501-525
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-61, 69-109, 113-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-154, 158-174, 178-209, 212-218, 221-228, 232, 235-258, 262
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70     54    23%   25-28, 33, 40-50, 54-95, 100-123, 128
src\gui\styles\widget_styles.py                                         35      7    80%   17, 152, 165, 382-383, 400-401
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-183, 187, 191-193, 202-210, 213-261, 266, 271-317
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-139
src\gui\widgets\audit_log_widget.py                                    233    205    12%   42-46, 49-132, 135-137, 149-161, 164-302, 305-306, 309-320, 323, 326-371, 374-380, 383-384, 387-389, 392-404, 407-409
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                                    486    452     7%   43-147, 151-168, 172-189, 198-327, 331-339, 343-359, 369-521, 525-534, 538-554, 563-572, 576, 580, 584-694, 698-712, 716-741, 745-749, 753-773, 777-787, 791-817, 822-847, 855-882, 890-912, 916-1021, 1025-1097
src\gui\widgets\bot_parameters.py                                      112     89    21%   39-43, 46-108, 118-125, 129, 145, 149-151, 155-164, 169, 173-175, 179-181, 191-198, 202, 206-207
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-75
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-167, 170-181, 184-192, 195-200, 203-221, 224-227, 231-239, 242-245, 248-251, 254-257, 260-263, 266-270, 273-284, 287-292
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-296, 305-330, 336-373, 378-389, 393-402, 406-409, 413-416, 420-430, 433-438, 441-446, 450-553
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-90, 94, 97-124, 127-134, 138, 141-157, 160-178, 182-194, 197-214, 217-233
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                                         330    292    12%   29-34, 45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 280-282, 285-306, 309-364, 367-370, 373-379, 382-414, 417-420, 423-425, 428, 432-449, 458-468, 472-512, 517-542
src\gui\widgets\footer_stats.py                                        400    342    14%   30-43, 46, 53-67, 71-79, 83, 87, 94-96, 99-100, 104-107, 110-111, 115, 134-136, 139-140, 144-147, 150-151, 155, 174-238, 242-260, 265-276, 280-285, 289-312, 317-324, 328, 341-474, 478-496, 499-501, 504-505, 509-590, 602-625, 629-631, 635-641, 645-648, 664-668, 675-684, 688, 692-693
src\gui\widgets\info_widgets.py                                         89     74    17%   26-57, 60, 67-75, 80-104, 111-161, 164, 167
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 58-60, 64, 68-69, 75-78, 82-85, 89-90, 100-105, 109-148
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-341, 345-355, 359, 363-365, 379-410, 414-431, 435-439, 443-445, 449-450, 454-458, 463-464, 468-503, 507-511, 515-520
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-231, 236-237, 241-242, 247-254, 258-259, 268-270, 274, 278, 282
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-261, 265-306, 311-354, 359
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      183    154    16%   15-20, 27-46, 49-50, 53-56, 59-69, 73-80, 91-116, 120-122, 126-128, 132-135, 139-154, 157-266, 270, 274, 278-279, 283-284, 290-322
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-107, 110-142, 146-148, 152-163, 169-211
src\gui\widgets\status_card.py                                          59     47    20%   19-84, 88-91, 100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 165-170, 173-186, 191-198, 202, 205-215, 218-231, 234-239, 242-246, 257-273, 276, 279, 284-309
src\gui\widgets\toast.py                                               128     98    23%   55-75, 79-118, 122-145, 148-152, 156-158, 162-163, 166-178, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-37, 41-44, 47-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13     10    23%   11-35
src\utils\document_processor.py                                         66     21    68%   15-16, 25-34, 51-52, 68-70, 77-78, 88-90
src\utils\helpers.py                                                    97     70    28%   22-36, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 213, 232, 242-260
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           43     19    56%   22-36, 54-60, 65-66, 71-72
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     24    70%   43-44, 80-82, 102, 104, 109-111, 116, 119-124, 128-134
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                21252  17025    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_app_initializer_coverage.py::TestAppInitializerCoverage::test_check_license_valid_immediate
1 error in 5.59s

```
</details>

---
### `tests/unit/test_app_initializer_coverage.py::TestAppInitializerCoverage::test_check_license_valid_immediate`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
_ ERROR at setup of TestAppInitializerCoverage.test_check_license_valid_immediate _
tests\unit\test_app_initializer_coverage.py:18: in mock_license
    "check_grace": mocker.patch(
.venv\Lib\site-packages\pytest_mock\plugin.py:419: in __call__
    return self._start_patch(
.venv\Lib\site-packages\pytest_mock\plugin.py:229: in _start_patch
    mocked: MockType = p.start()
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.core.license_validator' from 'C:\\Users\\Coemi\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\license_validator.py'> does not have the attribute 'check_emergency_grace_period'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      6    70%   112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              241    188    22%   52-68, 74, 80, 85, 90-92, 104-108, 118-130, 134, 138, 142, 146-147, 151-152, 156-170, 174-219, 224-241, 245-247, 254-259, 263-273, 284-318, 322-347, 351-353, 357-361, 365-367, 371, 375-381, 392-404, 408-413, 425
src\bots\base\login_page.py                                             94     78    17%   34-37, 43-53, 57-77, 81-93, 97-103, 110-154
src\bots\base\wait_helpers.py                                          171    144    16%   49-54, 75-80, 99-103, 134-197, 220, 249-307, 327-328, 331-335, 348, 351-355, 377-380, 383-395, 425-441, 471-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     28    42%   52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     56    31%   38, 42, 51-54, 60-67, 71-92, 96-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   38-41, 45, 49-55, 66-91, 102-115, 119-148, 152-162, 186-283, 287-305, 315-341, 345-354, 358-367, 371-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    186    17%   56, 60, 72-75, 79-81, 85-100, 104-121, 125-140, 144-166, 170-198, 202-211, 215-240, 244-276, 282-311, 315-324, 328-343, 347-367, 371-384
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     83    20%   27-30, 34, 38-44, 48-65, 69-91, 95-124, 128-145, 149-154, 158-167
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     41    31%   24, 29, 34, 41, 45, 49-52, 58-107
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-84, 88-149, 153-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    120    37%   88-111, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 320-322, 331, 337-339, 362-363, 367-384, 391-392
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-156, 160-164, 168-193, 197-226, 230-238, 242-279, 283-311, 315-327, 331-359, 363-405, 409-425, 429-450, 454-466, 473-512, 515-560, 564-583
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     67    26%   16-18, 30-69, 75-126, 130-145
src\core\app_updater.py                                                 46     37    20%   17-45, 50-55, 60-81, 85
src\core\audit_manager.py                                              226    103    54%   61, 71, 120-122, 134-138, 152-153, 233-237, 243-257, 261-294, 334-336, 338-341, 343-346, 348-350, 352-356, 369-370, 376-381, 385-399, 406-441
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-187, 198-206, 211-222, 227-248
src\core\bug_reporter.py                                                60     45    25%   32-102, 107-119
src\core\config_manager.py                                             241    120    50%   35, 87, 101-102, 113-119, 140, 145-146, 160-174, 183-184, 203-204, 226, 230-233, 250-251, 256-257, 262-264, 269, 284, 294-307, 312-322, 331-358, 363-367, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-131, 140-147, 156-161, 170-177, 182, 187, 192, 197, 202, 207, 216, 224, 229
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-55, 60-70, 76-102, 108-146, 150-151, 159-194, 198, 208, 219-232, 239-260
src\core\database.py                                                   220    141    36%   58, 77-88, 95-125, 129-133, 136-139, 142, 148-167, 175-236, 241-245, 253-272, 277-279, 287-318, 326-369, 376-378, 386-401, 406-446, 453-501, 506-508, 513-519, 526-536, 541-558
src\core\employees.py                                                   89     73    18%   25-63, 67-69, 76-99, 104-120, 127-182
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 61, 72, 76, 87, 98, 103-105
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-96, 100-114
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 68-72, 77-93, 100-124, 129-140, 145-151, 156-185
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-101, 108-125, 130-183, 188-202, 207-231, 236-239
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-84, 93-109, 115-134, 140-178, 182-197, 201-223, 227-279, 283-299
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-85, 93-111, 115-135, 149-180, 184-248, 252-261, 278-282, 286-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-148, 153-195, 200-202, 207-213, 218-238, 243-251, 256-274, 279-287, 291-294
src\core\license_validator.py                                          183    135    26%   38-42, 51-58, 79-111, 117-133, 138-145, 159-183, 193-219, 230-231, 240-264, 269-287, 292-340, 345-348, 353-356
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-108, 112-143, 152-206, 215-253
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-148, 152-154, 158, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                                 17      6    65%   22, 31-36
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-50, 61-85, 95-96, 114-134, 147-157
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     58    40%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 124-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    140    20%   38-48, 52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    289    15%   28-30, 34-43, 47-65, 69-72, 76-80, 84-88, 91-111, 114-133, 136-139, 143-158, 161-171, 174-177, 180-181, 184-190, 193-199, 202-223, 227-250, 253-257, 260-265, 269-284, 287-293, 296-309, 312-325, 329-334, 338-344, 348-354, 358-384, 388-401, 405-412, 415-421, 424-447, 450-462, 465-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   19-53, 56-64, 67-83, 92-110, 119-144, 147-151, 154-168, 171-176, 179-183, 186-211, 214-219, 222-227, 230-231, 234-259, 262-267
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-132, 135-149, 152-155, 158-165, 168-171, 174-176, 179-181, 184-210, 213-230, 233-235, 238-265
src\gui\controllers\bot_controller.py                                   38     30    21%   17-20, 24-32, 36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           154    125    19%   36-37, 41-57, 61-77, 80-94, 97-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 158-164, 168-172, 176-182, 194-230, 234-250, 254-256, 260-261, 265-266, 270-303, 307-308
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-53, 61-123, 130-160, 164-340, 352-355, 372-380, 393-434, 447-463, 467, 471-480
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-74, 77-84, 87
src\gui\dialogs\bug_report_dialog.py                                   158    139    12%   31-32, 35-42, 49-53, 56-125, 128-147, 150-172, 176-328, 332-349
src\gui\dialogs\command_palette.py                                     302    274     9%   39-68, 72-183, 187-213, 216-224, 227-233, 236-241, 244-251, 254-289, 293-302, 305-312, 315-321, 324-330, 334-338, 342-354, 358-369, 372-379, 382-386, 389-433, 436-472, 476-492, 495-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 102, 105, 108, 111-136, 139-141, 144-147, 151-230
src\gui\layouts\responsive.py                                           64     50    22%   16-19, 23-24, 28-29, 33-39, 43-47, 51-52, 56-67, 72-80, 84-86, 90-100
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     55    24%   17-22, 26-32, 36-48, 52-63, 68-77, 81-329
src\gui\main_window\components\status_bar.py                           158    141    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-278
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-39
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 27-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     20     13    35%   9-10, 15-26, 30-40
src\gui\main_window\main.py                                            280    206    26%   46-95, 99-133, 145-150, 153-177, 180-186, 190, 193, 196, 199, 202, 205, 208, 211, 215-241, 244, 247-266, 269-273, 281-285, 293-297, 303-307, 313-315, 318-320, 323-325, 328-330, 333-335, 338-342, 345-356, 359-361, 364-380, 383-386, 389-392, 395-399, 402-404, 407-410, 413, 416, 419-420, 425, 429, 433, 437, 441, 445
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          128    104    19%   28-31, 40-42, 45, 48, 51-75, 79-97, 101-111, 115-122, 126-130, 134-142, 146-148, 151-153, 156-161, 164-168, 172-184, 187-189
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 119-127, 131-175, 182, 186-197, 201, 205, 209, 217, 226, 230-235, 239-242, 246-248, 252-263, 267-270, 274-290, 294-298, 302-307, 317-320, 324-337, 341, 345-360, 367-370, 374-379, 383-386
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-108, 112-120, 124-125, 129-183
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-240, 250-291, 295-309, 313-331, 335, 339-449, 453-538, 541-609, 613-705, 708-773, 777-878
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-180, 184-191, 195, 199, 223-239, 243-264, 269-293, 297-299, 303-306, 310-335, 339-357, 360-361, 364-368, 371-388, 391-393, 396-413, 417, 420-439
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-126, 130-132, 136-146, 150-165, 170-185, 190-208, 213-227, 232-241, 245-260, 264-292, 296-302
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-89, 92-94, 98, 101-113, 116-126, 129-131, 135-141, 144-220
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     530    485     8%   53-83, 86-206, 209-314, 317-322, 326-360, 364-377, 380-408, 411-455, 459-467, 471-488, 491-518, 521-533, 536-545, 549-580, 583-616, 621-626, 629-670, 673-675, 678-714, 718-740, 744-787, 795-881, 885-896, 900-922, 926-959
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-159, 162-164, 167-169, 172-174, 177, 182-223, 228-276
src\gui\panels\dipendenti_manager_panel.py                             156    137    12%   27-69, 72, 83-95, 98-123, 126-157, 160-190, 194-223, 227-243, 247-266, 269-281, 288-315
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-167, 171-191, 194-203, 206-214, 217-220, 223, 243, 263, 275, 289, 300, 313, 325, 336, 346, 356, 364
src\gui\panels\lyra_panel.py                                           349    303    13%   60-64, 68-86, 98-99, 103-112, 124-132, 136-400, 407-420, 424-425, 429-449, 453-456, 460-464, 468-483, 491-493, 497-500, 504-507, 511-512, 516-521, 531-551, 557-560, 564-578, 582-599, 603-635, 643-656, 660-672, 676-687, 691-696
src\gui\panels\notifications_panel.py                                  247    201    19%   56-69, 72-140, 143-144, 148-150, 154-156, 160-162, 166-167, 171-172, 176, 179-183, 188-223, 228-251, 255-281, 289-297, 301-302, 306-324, 328-360, 364-366, 370-389, 393-432
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-49, 56-108, 111-201, 205-216, 220-240, 244-250, 254-270, 274-327, 333-337, 341-353
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-76, 80-82, 85-93, 96-102, 105-115, 119-190
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-66, 69-72, 75-76, 79-84, 94-126, 131-138, 141-143
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   42-44, 49-83, 94-101, 105-234, 238-253, 257-285, 289-291, 295-303, 307-328, 332-334, 338-356, 367-396, 400-405, 409-421, 425-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-160, 163-171, 174-177, 180-193, 196-201, 204-214, 218-226, 231-238, 241-272, 276-288, 292-314, 318-332, 336-343, 347-369, 373-375, 379-393, 397-399
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-78, 82-84, 88, 92-105, 109-117, 121-123, 127-132, 146-148, 154-210
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-182
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-36, 40-41, 44, 47
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-74
src\gui\panels\settings\pages\lists_page.py                            319    268    16%   32-33, 36-62, 67-84, 87-104, 107-126, 129-148, 151-170, 173-192, 197-203, 206-207, 214, 224, 234-243, 246-254, 259-262, 265-272, 275-283, 286-302, 305-315, 318-324, 329-338, 341-355, 358-368, 371-377, 382-383, 386, 389-392, 395-400, 403-410, 414, 417, 420, 423, 426, 429, 432, 435, 438, 441, 444, 447, 452-457, 460-465
src\gui\panels\settings\pages\paths_page.py                            107     86    20%   26-27, 30-68, 71-90, 94-115, 132-133, 136, 139-141, 144-146, 149-151, 154-156, 159-161, 166-181, 184-189
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 98-100
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-104, 111, 114-116, 119-121
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-129, 132-137, 140-153, 156-165, 169-173, 181-191, 195-208
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-248, 252-265, 269-279, 283, 287, 291-302, 306-313, 317-324, 328-380, 384-497, 501-525
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-61, 69-109, 113-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-154, 158-174, 178-209, 212-218, 221-228, 232, 235-258, 262
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70     54    23%   25-28, 33, 40-50, 54-95, 100-123, 128
src\gui\styles\widget_styles.py                                         35      7    80%   17, 152, 165, 382-383, 400-401
src\gui\toast.py                                                        45     39    13%   16-61, 65-83, 87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-183, 187, 191-193, 202-210, 213-261, 266, 271-317
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-139
src\gui\widgets\audit_log_widget.py                                    233    205    12%   42-46, 49-132, 135-137, 149-161, 164-302, 305-306, 309-320, 323, 326-371, 374-380, 383-384, 387-389, 392-404, 407-409
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                                    486    452     7%   43-147, 151-168, 172-189, 198-327, 331-339, 343-359, 369-521, 525-534, 538-554, 563-572, 576, 580, 584-694, 698-712, 716-741, 745-749, 753-773, 777-787, 791-817, 822-847, 855-882, 890-912, 916-1021, 1025-1097
src\gui\widgets\bot_parameters.py                                      112     89    21%   39-43, 46-108, 118-125, 129, 145, 149-151, 155-164, 169, 173-175, 179-181, 191-198, 202, 206-207
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-75
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-167, 170-181, 184-192, 195-200, 203-221, 224-227, 231-239, 242-245, 248-251, 254-257, 260-263, 266-270, 273-284, 287-292
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-296, 305-330, 336-373, 378-389, 393-402, 406-409, 413-416, 420-430, 433-438, 441-446, 450-553
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-90, 94, 97-124, 127-134, 138, 141-157, 160-178, 182-194, 197-214, 217-233
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                                         330    292    12%   29-34, 45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 280-282, 285-306, 309-364, 367-370, 373-379, 382-414, 417-420, 423-425, 428, 432-449, 458-468, 472-512, 517-542
src\gui\widgets\footer_stats.py                                        400    342    14%   30-43, 46, 53-67, 71-79, 83, 87, 94-96, 99-100, 104-107, 110-111, 115, 134-136, 139-140, 144-147, 150-151, 155, 174-238, 242-260, 265-276, 280-285, 289-312, 317-324, 328, 341-474, 478-496, 499-501, 504-505, 509-590, 602-625, 629-631, 635-641, 645-648, 664-668, 675-684, 688, 692-693
src\gui\widgets\info_widgets.py                                         89     74    17%   26-57, 60, 67-75, 80-104, 111-161, 164, 167
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 58-60, 64, 68-69, 75-78, 82-85, 89-90, 100-105, 109-148
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-341, 345-355, 359, 363-365, 379-410, 414-431, 435-439, 443-445, 449-450, 454-458, 463-464, 468-503, 507-511, 515-520
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-231, 236-237, 241-242, 247-254, 258-259, 268-270, 274, 278, 282
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-261, 265-306, 311-354, 359
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      183    154    16%   15-20, 27-46, 49-50, 53-56, 59-69, 73-80, 91-116, 120-122, 126-128, 132-135, 139-154, 157-266, 270, 274, 278-279, 283-284, 290-322
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-107, 110-142, 146-148, 152-163, 169-211
src\gui\widgets\status_card.py                                          59     47    20%   19-84, 88-91, 100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 165-170, 173-186, 191-198, 202, 205-215, 218-231, 234-239, 242-246, 257-273, 276, 279, 284-309
src\gui\widgets\toast.py                                               128     98    23%   55-75, 79-118, 122-145, 148-152, 156-158, 162-163, 166-178, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-37, 41-44, 47-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13     10    23%   11-35
src\utils\document_processor.py                                         66     21    68%   15-16, 25-34, 51-52, 68-70, 77-78, 88-90
src\utils\helpers.py                                                    97     70    28%   22-36, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 213, 232, 242-260
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           43     19    56%   22-36, 54-60, 65-66, 71-72
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     24    70%   43-44, 80-82, 102, 104, 109-111, 116, 119-124, 128-134
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                21252  17018    20%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_app_initializer_coverage.py::TestAppInitializerCoverage::test_check_license_valid_immediate
1 error in 5.87s

```
</details>

---
### `tests/unit/test_app_initializer_coverage_hardened.py::TestAppInitializer::test_initialize_success`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
________ ERROR at setup of TestAppInitializer.test_initialize_success _________
tests\unit\test_app_initializer_coverage_hardened.py:13: in mock_deps
    "db": mocker.patch("src.core.app_initializer.db_manager"),
.venv\Lib\site-packages\pytest_mock\plugin.py:419: in __call__
    return self._start_patch(
.venv\Lib\site-packages\pytest_mock\plugin.py:229: in _start_patch
    mocked: MockType = p.start()
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.core.app_initializer' from 'C:\\Users\\Coemi\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\app_initializer.py'> does not have the attribute 'db_manager'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              241    188    22%   52-68, 74, 80, 85, 90-92, 104-108, 118-130, 134, 138, 142, 146-147, 151-152, 156-170, 174-219, 224-241, 245-247, 254-259, 263-273, 284-318, 322-347, 351-353, 357-361, 365-367, 371, 375-381, 392-404, 408-413, 425
src\bots\base\login_page.py                                             94     78    17%   34-37, 43-53, 57-77, 81-93, 97-103, 110-154
src\bots\base\wait_helpers.py                                          171    171     0%   14-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-92, 96-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   38-41, 45, 49-55, 66-91, 102-115, 119-148, 152-162, 186-283, 287-305, 315-341, 345-354, 358-367, 371-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-140, 144-166, 170-198, 202-211, 215-240, 244-276, 282-311, 315-324, 328-343, 347-367, 371-384
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-84, 88-149, 153-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-76, 80-81, 88-111, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 289-322, 325-363, 367-384, 391-392
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-156, 160-164, 168-193, 197-226, 230-238, 242-279, 283-311, 315-327, 331-359, 363-405, 409-425, 429-450, 454-466, 473-512, 515-560, 564-583
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     19    79%   16-18, 111-115, 130-145
src\core\app_updater.py                                                 46     37    20%   17-45, 50-55, 60-81, 85
src\core\audit_manager.py                                              226    182    19%   29-37, 61, 64-67, 70-74, 78-126, 130-138, 142-143, 146-153, 171-237, 243-257, 261-294, 298-299, 326-372, 376-381, 385-399, 406-441
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-187, 198-206, 211-222, 227-248
src\core\bug_reporter.py                                                60     45    25%   32-102, 107-119
src\core\config_manager.py                                             241    175    27%   35, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 203-204, 218-236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-131, 140-147, 156-161, 170-177, 182, 187, 192, 197, 202, 207, 216, 224, 229
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         102    102     0%   1-216
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-55, 60-70, 76-102, 108-146, 150-151, 159-194, 198, 208, 219-232, 239-260
src\core\database.py                                                   220    155    30%   56-91, 95-125, 129-133, 136-139, 142, 148-167, 175-236, 241-245, 253-272, 277-279, 287-318, 326-369, 376-378, 386-401, 406-446, 453-501, 506-508, 513-519, 526-536, 541-558
src\core\employees.py                                                   89     89     0%   1-186
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 61, 72, 76, 87, 98, 103-105
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-96, 100-114
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 68-72, 77-93, 100-124, 129-140, 145-151, 156-185
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-101, 108-125, 130-183, 188-202, 207-231, 236-239
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-84, 93-109, 115-134, 140-178, 182-197, 201-223, 227-279, 283-299
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-85, 93-111, 115-135, 149-180, 184-248, 252-261, 278-282, 286-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-148, 153-195, 200-202, 207-213, 218-238, 243-251, 256-274, 279-287, 291-294
src\core\license_validator.py                                          183    146    20%   38-42, 49-58, 64-111, 117-133, 138-145, 159-183, 193-219, 230-231, 240-264, 269-287, 292-340, 345-348, 353-356
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-108, 112-143, 152-206, 215-253
src\core\lyra_sentinel.py                                               32     24    25%   22-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-148, 152-154, 158, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                                 17      6    65%   22, 31-36
src\core\report_history.py                                              67     67     0%   7-157
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     60    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     47     0%   6-83
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    140    20%   38-48, 52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    289    15%   28-30, 34-43, 47-65, 69-72, 76-80, 84-88, 91-111, 114-133, 136-139, 143-158, 161-171, 174-177, 180-181, 184-190, 193-199, 202-223, 227-250, 253-257, 260-265, 269-284, 287-293, 296-309, 312-325, 329-334, 338-344, 348-354, 358-384, 388-401, 405-412, 415-421, 424-447, 450-462, 465-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\controllers\bot_controller.py                                   38     30    21%   17-20, 24-32, 36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           154    125    19%   36-37, 41-57, 61-77, 80-94, 97-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 158-164, 168-172, 176-182, 194-230, 234-250, 254-256, 260-261, 265-266, 270-303, 307-308
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-53, 61-123, 130-160, 164-340, 352-355, 372-380, 393-434, 447-463, 467, 471-480
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     51     0%   1-87
src\gui\dialogs\bug_report_dialog.py                                   158    139    12%   31-32, 35-42, 49-53, 56-125, 128-147, 150-172, 176-328, 332-349
src\gui\dialogs\command_palette.py                                     302    274     9%   39-68, 72-183, 187-213, 216-224, 227-233, 236-241, 244-251, 254-289, 293-302, 305-312, 315-321, 324-330, 334-338, 342-354, 358-369, 372-379, 382-386, 389-433, 436-472, 476-492, 495-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129    129     0%   1-230
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     55    24%   17-22, 26-32, 36-48, 52-63, 68-77, 81-329
src\gui\main_window\components\status_bar.py                           158    141    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-278
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-39
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 27-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     20     13    35%   9-10, 15-26, 30-40
src\gui\main_window\main.py                                            280    206    26%   46-95, 99-133, 145-150, 153-177, 180-186, 190, 193, 196, 199, 202, 205, 208, 211, 215-241, 244, 247-266, 269-273, 281-285, 293-297, 303-307, 313-315, 318-320, 323-325, 328-330, 333-335, 338-342, 345-356, 359-361, 364-380, 383-386, 389-392, 395-399, 402-404, 407-410, 413, 416, 419-420, 425, 429, 433, 437, 441, 445
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 196    196     0%   6-386
src\gui\panels\carico_ts.py                                             90     90     0%   6-183
src\gui\panels\contabilita_kpi_panel.py                                379    379     0%   1-878
src\gui\panels\contabilita_panel.py                                    255    255     0%   6-439
src\gui\panels\dashboard_panel.py                                      168    168     0%   1-302
src\gui\panels\dettagli_oda.py                                         127    127     0%   6-220
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 29     29     0%   1-62
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-276
src\gui\panels\dipendenti_manager_panel.py                             156    156     0%   1-315
src\gui\panels\help_panel.py                                           120    120     0%   6-364
src\gui\panels\lyra_panel.py                                           349    349     0%   1-696
src\gui\panels\notifications_panel.py                                  247    247     0%   6-432
src\gui\panels\pdl_db.py                                               202    202     0%   6-353
src\gui\panels\prenota_bp.py                                           104    104     0%   6-190
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-143
src\gui\panels\scarico_ore_panel.py                                    306    306     0%   7-524
src\gui\panels\scarico_pdl.py                                          223    223     0%   6-399
src\gui\panels\scarico_ts.py                                           121    121     0%   6-210
src\gui\panels\storico_oda_panel.py                                    225    225     0%   6-525
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     148    148     0%   1-262
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-200
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70      5    93%   106-107, 110, 119-120
src\gui\styles\widget_styles.py                                         35      7    80%   17, 152, 165, 382-383, 400-401
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    137     0%   1-317
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-139
src\gui\widgets\audit_log_widget.py                                    233    233     0%   7-409
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                                    486    486     0%   5-1097
src\gui\widgets\bot_parameters.py                                      112     89    21%   39-43, 46-108, 118-125, 129, 145, 149-151, 155-164, 169, 173-175, 179-181, 191-198, 202, 206-207
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-75
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                                         330    292    12%   29-34, 45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 280-282, 285-306, 309-364, 367-370, 373-379, 382-414, 417-420, 423-425, 428, 432-449, 458-468, 472-512, 517-542
src\gui\widgets\footer_stats.py                                        400    342    14%   30-43, 46, 53-67, 71-79, 83, 87, 94-96, 99-100, 104-107, 110-111, 115, 134-136, 139-140, 144-147, 150-151, 155, 174-238, 242-260, 265-276, 280-285, 289-312, 317-324, 328, 341-474, 478-496, 499-501, 504-505, 509-590, 602-625, 629-631, 635-641, 645-648, 664-668, 675-684, 688, 692-693
src\gui\widgets\info_widgets.py                                         89     74    17%   26-57, 60, 67-75, 80-104, 111-161, 164, 167
src\gui\widgets\message_bubble.py                                       53     53     0%   7-123
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 58-60, 64, 68-69, 75-78, 82-85, 89-90, 100-105, 109-148
src\gui\widgets\notification_card.py                                   220    220     0%   6-520
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-282
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-359
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      183    154    16%   15-20, 27-46, 49-50, 53-56, 59-69, 73-80, 91-116, 120-122, 126-128, 132-135, 139-154, 157-266, 270, 274, 278-279, 283-284, 290-322
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-211
src\gui\widgets\status_card.py                                          59     47    20%   19-84, 88-91, 100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 165-170, 173-186, 191-198, 202, 205-215, 218-231, 234-239, 242-246, 257-273, 276, 279, 284-309
src\gui\widgets\toast.py                                               128     98    23%   55-75, 79-118, 122-145, 148-152, 156-158, 162-163, 166-178, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-37, 41-44, 47-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13     10    23%   11-35
src\utils\document_processor.py                                         66     66     0%   6-90
src\utils\helpers.py                                                    97     73    25%   24-30, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 212-234, 242-260
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-141
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                17965  15433    14%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_app_initializer_coverage_hardened.py::TestAppInitializer::test_initialize_success
1 error in 4.88s

```
</details>

---
### `tests/unit/test_app_initializer_deep.py::TestAppInitializerDeep::test_initialize_full_success`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
____ ERROR at setup of TestAppInitializerDeep.test_initialize_full_success ____
tests\unit\test_app_initializer_deep.py:11: in mock_msgbox
    return mocker.patch("src.core.app_initializer.QMessageBox")
.venv\Lib\site-packages\pytest_mock\plugin.py:419: in __call__
    return self._start_patch(
.venv\Lib\site-packages\pytest_mock\plugin.py:229: in _start_patch
    mocked: MockType = p.start()
C:\Program Files\Python312\Lib\unittest\mock.py:1624: in start
    result = self.__enter__()
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.core.app_initializer' from 'C:\\Users\\Coemi\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\core\\app_initializer.py'> does not have the attribute 'QMessageBox'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              241    188    22%   52-68, 74, 80, 85, 90-92, 104-108, 118-130, 134, 138, 142, 146-147, 151-152, 156-170, 174-219, 224-241, 245-247, 254-259, 263-273, 284-318, 322-347, 351-353, 357-361, 365-367, 371, 375-381, 392-404, 408-413, 425
src\bots\base\login_page.py                                             94     78    17%   34-37, 43-53, 57-77, 81-93, 97-103, 110-154
src\bots\base\wait_helpers.py                                          171    171     0%   14-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-92, 96-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   38-41, 45, 49-55, 66-91, 102-115, 119-148, 152-162, 186-283, 287-305, 315-341, 345-354, 358-367, 371-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-140, 144-166, 170-198, 202-211, 215-240, 244-276, 282-311, 315-324, 328-343, 347-367, 371-384
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-84, 88-149, 153-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-76, 80-81, 88-111, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 289-322, 325-363, 367-384, 391-392
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-156, 160-164, 168-193, 197-226, 230-238, 242-279, 283-311, 315-327, 331-359, 363-405, 409-425, 429-450, 454-466, 473-512, 515-560, 564-583
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     19    79%   16-18, 111-115, 130-145
src\core\app_updater.py                                                 46     37    20%   17-45, 50-55, 60-81, 85
src\core\audit_manager.py                                              226    182    19%   29-37, 61, 64-67, 70-74, 78-126, 130-138, 142-143, 146-153, 171-237, 243-257, 261-294, 298-299, 326-372, 376-381, 385-399, 406-441
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-187, 198-206, 211-222, 227-248
src\core\bug_reporter.py                                                60     45    25%   32-102, 107-119
src\core\config_manager.py                                             241    175    27%   35, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 203-204, 218-236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-131, 140-147, 156-161, 170-177, 182, 187, 192, 197, 202, 207, 216, 224, 229
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         102    102     0%   1-216
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-55, 60-70, 76-102, 108-146, 150-151, 159-194, 198, 208, 219-232, 239-260
src\core\database.py                                                   220    155    30%   56-91, 95-125, 129-133, 136-139, 142, 148-167, 175-236, 241-245, 253-272, 277-279, 287-318, 326-369, 376-378, 386-401, 406-446, 453-501, 506-508, 513-519, 526-536, 541-558
src\core\employees.py                                                   89     89     0%   1-186
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 61, 72, 76, 87, 98, 103-105
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-96, 100-114
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 68-72, 77-93, 100-124, 129-140, 145-151, 156-185
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-101, 108-125, 130-183, 188-202, 207-231, 236-239
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-84, 93-109, 115-134, 140-178, 182-197, 201-223, 227-279, 283-299
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-85, 93-111, 115-135, 149-180, 184-248, 252-261, 278-282, 286-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155    134    14%   22-64, 69-70, 75, 80, 85-101, 106-148, 153-195, 200-202, 207-213, 218-238, 243-251, 256-274, 279-287, 291-294
src\core\license_validator.py                                          183    146    20%   38-42, 49-58, 64-111, 117-133, 138-145, 159-183, 193-219, 230-231, 240-264, 269-287, 292-340, 345-348, 353-356
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-108, 112-143, 152-206, 215-253
src\core\lyra_sentinel.py                                               32     24    25%   22-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-148, 152-154, 158, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                                 17      6    65%   22, 31-36
src\core\report_history.py                                              67     67     0%   7-157
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     60    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     47     0%   6-83
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    140    20%   38-48, 52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    289    15%   28-30, 34-43, 47-65, 69-72, 76-80, 84-88, 91-111, 114-133, 136-139, 143-158, 161-171, 174-177, 180-181, 184-190, 193-199, 202-223, 227-250, 253-257, 260-265, 269-284, 287-293, 296-309, 312-325, 329-334, 338-344, 348-354, 358-384, 388-401, 405-412, 415-421, 424-447, 450-462, 465-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\controllers\bot_controller.py                                   38     30    21%   17-20, 24-32, 36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           154    125    19%   36-37, 41-57, 61-77, 80-94, 97-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 158-164, 168-172, 176-182, 194-230, 234-250, 254-256, 260-261, 265-266, 270-303, 307-308
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-53, 61-123, 130-160, 164-340, 352-355, 372-380, 393-434, 447-463, 467, 471-480
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     51     0%   1-87
src\gui\dialogs\bug_report_dialog.py                                   158    139    12%   31-32, 35-42, 49-53, 56-125, 128-147, 150-172, 176-328, 332-349
src\gui\dialogs\command_palette.py                                     302    274     9%   39-68, 72-183, 187-213, 216-224, 227-233, 236-241, 244-251, 254-289, 293-302, 305-312, 315-321, 324-330, 334-338, 342-354, 358-369, 372-379, 382-386, 389-433, 436-472, 476-492, 495-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129    129     0%   1-230
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     55    24%   17-22, 26-32, 36-48, 52-63, 68-77, 81-329
src\gui\main_window\components\status_bar.py                           158    141    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-278
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-39
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 27-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     20     13    35%   9-10, 15-26, 30-40
src\gui\main_window\main.py                                            280    206    26%   46-95, 99-133, 145-150, 153-177, 180-186, 190, 193, 196, 199, 202, 205, 208, 211, 215-241, 244, 247-266, 269-273, 281-285, 293-297, 303-307, 313-315, 318-320, 323-325, 328-330, 333-335, 338-342, 345-356, 359-361, 364-380, 383-386, 389-392, 395-399, 402-404, 407-410, 413, 416, 419-420, 425, 429, 433, 437, 441, 445
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\panels\__init__.py                                              21     21     0%   6-27
src\gui\panels\base.py                                                 196    196     0%   6-386
src\gui\panels\carico_ts.py                                             90     90     0%   6-183
src\gui\panels\contabilita_kpi_panel.py                                379    379     0%   1-878
src\gui\panels\contabilita_panel.py                                    255    255     0%   6-439
src\gui\panels\dashboard_panel.py                                      168    168     0%   1-302
src\gui\panels\dettagli_oda.py                                         127    127     0%   6-220
src\gui\panels\dipendenti\__init__.py                                    2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                                 29     29     0%   1-62
src\gui\panels\dipendenti\shared.py                                    150    150     0%   1-276
src\gui\panels\dipendenti_manager_panel.py                             156    156     0%   1-315
src\gui\panels\help_panel.py                                           120    120     0%   6-364
src\gui\panels\lyra_panel.py                                           349    349     0%   1-696
src\gui\panels\notifications_panel.py                                  247    247     0%   6-432
src\gui\panels\pdl_db.py                                               202    202     0%   6-353
src\gui\panels\prenota_bp.py                                           104    104     0%   6-190
src\gui\panels\ricerca_pdl.py                                           80     80     0%   6-143
src\gui\panels\scarico_ore_panel.py                                    306    306     0%   7-524
src\gui\panels\scarico_pdl.py                                          223    223     0%   6-399
src\gui\panels\scarico_ts.py                                           121    121     0%   6-210
src\gui\panels\storico_oda_panel.py                                    225    225     0%   6-525
src\gui\panels\timbrature\__init__.py                                    2      2     0%   1-3
src\gui\panels\timbrature\panel.py                                     148    148     0%   1-262
src\gui\panels\timbrature_bot.py                                       116    116     0%   6-200
src\gui\panels\timbrature_db.py                                          2      2     0%   6-8
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70      5    93%   106-107, 110, 119-120
src\gui\styles\widget_styles.py                                         35      7    80%   17, 152, 165, 382-383, 400-401
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    137     0%   1-317
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-139
src\gui\widgets\audit_log_widget.py                                    233    233     0%   7-409
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                                    486    486     0%   5-1097
src\gui\widgets\bot_parameters.py                                      112     89    21%   39-43, 46-108, 118-125, 129, 145, 149-151, 155-164, 169, 173-175, 179-181, 191-198, 202, 206-207
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-75
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                                         330    292    12%   29-34, 45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 280-282, 285-306, 309-364, 367-370, 373-379, 382-414, 417-420, 423-425, 428, 432-449, 458-468, 472-512, 517-542
src\gui\widgets\footer_stats.py                                        400    342    14%   30-43, 46, 53-67, 71-79, 83, 87, 94-96, 99-100, 104-107, 110-111, 115, 134-136, 139-140, 144-147, 150-151, 155, 174-238, 242-260, 265-276, 280-285, 289-312, 317-324, 328, 341-474, 478-496, 499-501, 504-505, 509-590, 602-625, 629-631, 635-641, 645-648, 664-668, 675-684, 688, 692-693
src\gui\widgets\info_widgets.py                                         89     74    17%   26-57, 60, 67-75, 80-104, 111-161, 164, 167
src\gui\widgets\message_bubble.py                                       53     53     0%   7-123
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 58-60, 64, 68-69, 75-78, 82-85, 89-90, 100-105, 109-148
src\gui\widgets\notification_card.py                                   220    220     0%   6-520
src\gui\widgets\notification_group_header.py                            47     47     0%   6-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106    106     0%   6-282
src\gui\widgets\priority_badge.py                                       46     46     0%   6-109
src\gui\widgets\quick_actions.py                                        76     76     0%   1-359
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      183    154    16%   15-20, 27-46, 49-50, 53-56, 59-69, 73-80, 91-116, 120-122, 126-128, 132-135, 139-154, 157-266, 270, 274, 278-279, 283-284, 290-322
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100    100     0%   1-211
src\gui\widgets\status_card.py                                          59     47    20%   19-84, 88-91, 100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 165-170, 173-186, 191-198, 202, 205-215, 218-231, 234-239, 242-246, 257-273, 276, 279, 284-309
src\gui\widgets\toast.py                                               128     98    23%   55-75, 79-118, 122-145, 148-152, 156-158, 162-163, 166-178, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-37, 41-44, 47-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13     10    23%   11-35
src\utils\document_processor.py                                         66     66     0%   6-90
src\utils\helpers.py                                                    97     73    25%   24-30, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 212-234, 242-260
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-141
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                17965  15433    14%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_app_initializer_deep.py::TestAppInitializerDeep::test_initialize_full_success
1 error in 5.01s

```
</details>

---
### `tests/unit/test_audit_log_refactoring.py::test_audit_refresh_population`
**Error:** `Unknown Error`

<details><summary>Full Output</summary>

```text
E                                                                        [100%]
=================================== ERRORS ====================================
_______________ ERROR at setup of test_audit_refresh_population _______________
tests\unit\test_audit_log_refactoring.py:17: in audit_widget
    m_manager_class = mocker.patch("src.gui.panels.notifications_panel.AuditManager")
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
E   AttributeError: <module 'src.gui.panels.notifications_panel' from 'C:\\Users\\Coemi\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\gui\\panels\\notifications_panel.py'> does not have the attribute 'AuditManager'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              241    188    22%   52-68, 74, 80, 85, 90-92, 104-108, 118-130, 134, 138, 142, 146-147, 151-152, 156-170, 174-219, 224-241, 245-247, 254-259, 263-273, 284-318, 322-347, 351-353, 357-361, 365-367, 371, 375-381, 392-404, 408-413, 425
src\bots\base\login_page.py                                             94     78    17%   34-37, 43-53, 57-77, 81-93, 97-103, 110-154
src\bots\base\wait_helpers.py                                          171    171     0%   14-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-92, 96-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   38-41, 45, 49-55, 66-91, 102-115, 119-148, 152-162, 186-283, 287-305, 315-341, 345-354, 358-367, 371-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-140, 144-166, 170-198, 202-211, 215-240, 244-276, 282-311, 315-324, 328-343, 347-367, 371-384
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-84, 88-149, 153-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-76, 80-81, 88-111, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 289-322, 325-363, 367-384, 391-392
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-156, 160-164, 168-193, 197-226, 230-238, 242-279, 283-311, 315-327, 331-359, 363-405, 409-425, 429-450, 454-466, 473-512, 515-560, 564-583
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     42    53%   31, 37-69, 130-145, 150-158
src\core\app_updater.py                                                 46      2    96%   32, 85
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              98     35    64%   59-61, 76-77, 106-108, 110-113, 115-118, 120-122, 124-128, 140-141, 145-150, 157-159
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              133     32    76%   27, 37, 49, 60-61, 116-118, 126, 128, 134, 137-138, 151, 167-168, 178, 192-213
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               24     18    25%   12-31
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-187, 198-206, 211-222, 227-248
src\core\bug_reporter.py                                                60     45    25%   32-102, 107-119
src\core\config_manager.py                                             241    175    27%   35, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 203-204, 218-236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-131, 140-147, 156-161, 170-177, 182, 187, 192, 197, 202, 207, 216, 224, 229
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-55, 60-70, 76-102, 108-146, 150-151, 159-194, 198, 208, 219-232, 239-260
src\core\database.py                                                   220    155    30%   56-91, 95-125, 129-133, 136-139, 142, 148-167, 175-236, 241-245, 253-272, 277-279, 287-318, 326-369, 376-378, 386-401, 406-446, 453-501, 506-508, 513-519, 526-536, 541-558
src\core\employees.py                                                   89     73    18%   25-63, 67-69, 76-99, 104-120, 127-182
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 61, 72, 76, 87, 98, 103-105
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-96, 100-114
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 68-72, 77-93, 100-124, 129-140, 145-151, 156-185
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-101, 108-125, 130-183, 188-202, 207-231, 236-239
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-84, 93-109, 115-134, 140-178, 182-197, 201-223, 227-279, 283-299
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-85, 93-111, 115-135, 149-180, 184-248, 252-261, 278-282, 286-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155    155     0%   6-294
src\core\license_validator.py                                          183    146    20%   38-42, 49-58, 64-111, 117-133, 138-145, 159-183, 193-219, 230-231, 240-264, 269-287, 292-340, 345-348, 353-356
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-108, 112-143, 152-206, 215-253
src\core\lyra_sentinel.py                                               32     24    25%   22-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-148, 152-154, 158, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                                 17      6    65%   22, 31-36
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-50, 61-85, 95-96, 114-134, 147-157
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     60    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47     34    28%   23-26, 30, 34-48, 52, 56-67, 71-79, 83
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    140    20%   38-48, 52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    289    15%   28-30, 34-43, 47-65, 69-72, 76-80, 84-88, 91-111, 114-133, 136-139, 143-158, 161-171, 174-177, 180-181, 184-190, 193-199, 202-223, 227-250, 253-257, 260-265, 269-284, 287-293, 296-309, 312-325, 329-334, 338-344, 348-354, 358-384, 388-401, 405-412, 415-421, 424-447, 450-462, 465-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   19-53, 56-64, 67-83, 92-110, 119-144, 147-151, 154-168, 171-176, 179-183, 186-211, 214-219, 222-227, 230-231, 234-259, 262-267
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-132, 135-149, 152-155, 158-165, 168-171, 174-176, 179-181, 184-210, 213-230, 233-235, 238-265
src\gui\controllers\bot_controller.py                                   38     30    21%   17-20, 24-32, 36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           154    125    19%   36-37, 41-57, 61-77, 80-94, 97-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 158-164, 168-172, 176-182, 194-230, 234-250, 254-256, 260-261, 265-266, 270-303, 307-308
src\gui\controllers\search_controller.py                               197    179     9%   13-14, 18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-53, 61-123, 130-160, 164-340, 352-355, 372-380, 393-434, 447-463, 467, 471-480
src\gui\design\colors.py                                                27      1    96%   105
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-74, 77-84, 87
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   24-28, 31-114, 117-119
src\gui\dialogs\bug_report_dialog.py                                   158    139    12%   31-32, 35-42, 49-53, 56-125, 128-147, 150-172, 176-328, 332-349
src\gui\dialogs\command_palette.py                                     302    274     9%   39-68, 72-183, 187-213, 216-224, 227-233, 236-241, 244-251, 254-289, 293-302, 305-312, 315-321, 324-330, 334-338, 342-354, 358-369, 372-379, 382-386, 389-433, 436-472, 476-492, 495-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 102, 105, 108, 111-136, 139-141, 144-147, 151-230
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     55    24%   17-22, 26-32, 36-48, 52-63, 68-77, 81-329
src\gui\main_window\components\status_bar.py                           158    141    11%   25-29, 32-102, 106-111, 115-128, 132-144, 148-207, 211-278
src\gui\main_window\components\tool_bar.py                              25     17    32%   10-14, 18-21, 25-39
src\gui\main_window\components\tray_icon.py                             16     11    31%   10-15, 18, 27-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     21    30%   9-11, 15-16, 23-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     20     13    35%   9-10, 15-26, 30-40
src\gui\main_window\main.py                                            280    206    26%   46-95, 99-133, 145-150, 153-177, 180-186, 190, 193, 196, 199, 202, 205, 208, 211, 215-241, 244, 247-266, 269-273, 281-285, 293-297, 303-307, 313-315, 318-320, 323-325, 328-330, 333-335, 338-342, 345-356, 359-361, 364-380, 383-386, 389-392, 395-399, 402-404, 407-410, 413, 416, 419-420, 425, 429, 433, 437, 441, 445
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          128    104    19%   28-31, 40-42, 45, 48, 51-75, 79-97, 101-111, 115-122, 126-130, 134-142, 146-148, 151-153, 156-161, 164-168, 172-184, 187-189
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 119-127, 131-175, 182, 186-197, 201, 205, 209, 217, 226, 230-235, 239-242, 246-248, 252-263, 267-270, 274-290, 294-298, 302-307, 317-320, 324-337, 341, 345-360, 367-370, 374-379, 383-386
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-108, 112-120, 124-125, 129-183
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-240, 250-291, 295-309, 313-331, 335, 339-449, 453-538, 541-609, 613-705, 708-773, 777-878
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-180, 184-191, 195, 199, 223-239, 243-264, 269-293, 297-299, 303-306, 310-335, 339-357, 360-361, 364-368, 371-388, 391-393, 396-413, 417, 420-439
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-126, 130-132, 136-146, 150-165, 170-185, 190-208, 213-227, 232-241, 245-260, 264-292, 296-302
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-89, 92-94, 98, 101-113, 116-126, 129-131, 135-141, 144-220
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     530    485     8%   53-83, 86-206, 209-314, 317-322, 326-360, 364-377, 380-408, 411-455, 459-467, 471-488, 491-518, 521-533, 536-545, 549-580, 583-616, 621-626, 629-670, 673-675, 678-714, 718-740, 744-787, 795-881, 885-896, 900-922, 926-959
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-159, 162-164, 167-169, 172-174, 177, 182-223, 228-276
src\gui\panels\dipendenti_manager_panel.py                             156    137    12%   27-69, 72, 83-95, 98-123, 126-157, 160-190, 194-223, 227-243, 247-266, 269-281, 288-315
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-167, 171-191, 194-203, 206-214, 217-220, 223, 243, 263, 275, 289, 300, 313, 325, 336, 346, 356, 364
src\gui\panels\lyra_panel.py                                           349    303    13%   60-64, 68-86, 98-99, 103-112, 124-132, 136-400, 407-420, 424-425, 429-449, 453-456, 460-464, 468-483, 491-493, 497-500, 504-507, 511-512, 516-521, 531-551, 557-560, 564-578, 582-599, 603-635, 643-656, 660-672, 676-687, 691-696
src\gui\panels\notifications_panel.py                                  247    201    19%   56-69, 72-140, 143-144, 148-150, 154-156, 160-162, 166-167, 171-172, 176, 179-183, 188-223, 228-251, 255-281, 289-297, 301-302, 306-324, 328-360, 364-366, 370-389, 393-432
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-49, 56-108, 111-201, 205-216, 220-240, 244-250, 254-270, 274-327, 333-337, 341-353
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-76, 80-82, 85-93, 96-102, 105-115, 119-190
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-66, 69-72, 75-76, 79-84, 94-126, 131-138, 141-143
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   42-44, 49-83, 94-101, 105-234, 238-253, 257-285, 289-291, 295-303, 307-328, 332-334, 338-356, 367-396, 400-405, 409-421, 425-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-160, 163-171, 174-177, 180-193, 196-201, 204-214, 218-226, 231-238, 241-272, 276-288, 292-314, 318-332, 336-343, 347-369, 373-375, 379-393, 397-399
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-78, 82-84, 88, 92-105, 109-117, 121-123, 127-132, 146-148, 154-210
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-182
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-36, 40-41, 44, 47
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-74
src\gui\panels\settings\pages\lists_page.py                            319    268    16%   32-33, 36-62, 67-84, 87-104, 107-126, 129-148, 151-170, 173-192, 197-203, 206-207, 214, 224, 234-243, 246-254, 259-262, 265-272, 275-283, 286-302, 305-315, 318-324, 329-338, 341-355, 358-368, 371-377, 382-383, 386, 389-392, 395-400, 403-410, 414, 417, 420, 423, 426, 429, 432, 435, 438, 441, 444, 447, 452-457, 460-465
src\gui\panels\settings\pages\paths_page.py                            107     86    20%   26-27, 30-68, 71-90, 94-115, 132-133, 136, 139-141, 144-146, 149-151, 154-156, 159-161, 166-181, 184-189
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 98-100
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-104, 111, 114-116, 119-121
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-129, 132-137, 140-153, 156-165, 169-173, 181-191, 195-208
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-248, 252-265, 269-279, 283, 287, 291-302, 306-313, 317-324, 328-380, 384-497, 501-525
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-61, 69-109, 113-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-154, 158-174, 178-209, 212-218, 221-228, 232, 235-258, 262
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70     54    23%   25-28, 33, 40-50, 54-95, 100-123, 128
src\gui\styles\widget_styles.py                                         35      7    80%   17, 152, 165, 382-383, 400-401
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-183, 187, 191-193, 202-210, 213-261, 266, 271-317
src\gui\widgets\animated_progress_bar.py                                74     63    15%   29-41, 45-46, 50, 54-55, 59-60, 65-79, 83-139
src\gui\widgets\audit\audit_filter_bar.py                               70     57    19%   21-25, 28-81, 84-86, 89-95, 104-105, 108-117
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   10-11, 14-32, 35-42, 45-46
src\gui\widgets\audit_log_widget.py                                    102     80    22%   38-50, 53-112, 115-116, 119-129, 132, 135-136, 139-155, 158-165, 168-170
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                                    486    452     7%   43-147, 151-168, 172-189, 198-327, 331-339, 343-359, 369-521, 525-534, 538-554, 563-572, 576, 580, 584-694, 698-712, 716-741, 745-749, 753-773, 777-787, 791-817, 822-847, 855-882, 890-912, 916-1021, 1025-1097
src\gui\widgets\bot_parameters.py                                      112     89    21%   39-43, 46-108, 118-125, 129, 145, 149-151, 155-164, 169, 173-175, 179-181, 191-198, 202, 206-207
src\gui\widgets\calendar_date_edit.py                                   16     11    31%   16-75
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-167, 170-181, 184-192, 195-200, 203-221, 224-227, 231-239, 242-245, 248-251, 254-257, 260-263, 266-270, 273-284, 287-292
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-296, 305-330, 336-373, 378-389, 393-402, 406-409, 413-416, 420-430, 433-438, 441-446, 450-553
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-90, 94, 97-124, 127-134, 138, 141-157, 160-178, 182-194, 197-214, 217-233
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                                         330    292    12%   29-34, 45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 280-282, 285-306, 309-364, 367-370, 373-379, 382-414, 417-420, 423-425, 428, 432-449, 458-468, 472-512, 517-542
src\gui\widgets\footer_stats.py                                        400    342    14%   30-43, 46, 53-67, 71-79, 83, 87, 94-96, 99-100, 104-107, 110-111, 115, 134-136, 139-140, 144-147, 150-151, 155, 174-238, 242-260, 265-276, 280-285, 289-312, 317-324, 328, 341-474, 478-496, 499-501, 504-505, 509-590, 602-625, 629-631, 635-641, 645-648, 664-668, 675-684, 688, 692-693
src\gui\widgets\info_widgets.py                                         89     74    17%   26-57, 60, 67-75, 80-104, 111-161, 164, 167
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        61     35    43%   42-54, 58-60, 64, 68-69, 75-78, 82-85, 89-90, 100-105, 109-148
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-341, 345-355, 359, 363-365, 379-410, 414-431, 435-439, 443-445, 449-450, 454-458, 463-464, 468-503, 507-511, 515-520
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-231, 236-237, 241-242, 247-254, 258-259, 268-270, 274, 278, 282
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-261, 265-306, 311-354, 359
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41     32    22%   11-24, 28-30, 34-41, 46-51, 55-89
src\gui\widgets\sidebar_widget.py                                      183    154    16%   15-20, 27-46, 49-50, 53-56, 59-69, 73-80, 91-116, 120-122, 126-128, 132-135, 139-154, 157-266, 270, 274, 278-279, 283-284, 290-322
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-107, 110-142, 146-148, 152-163, 169-211
src\gui\widgets\status_card.py                                          59     47    20%   19-84, 88-91, 100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 165-170, 173-186, 191-198, 202, 205-215, 218-231, 234-239, 242-246, 257-273, 276, 279, 284-309
src\gui\widgets\toast.py                                               128     98    23%   55-75, 79-118, 122-145, 148-152, 156-158, 162-163, 166-178, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35     25    29%   14-18, 21-37, 41-44, 47-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13     10    23%   11-35
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-54, 59-70, 75-90
src\utils\helpers.py                                                    97     77    21%   22-36, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 212-234, 242-260
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-141
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                21108  17092    19%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
ERROR tests/unit/test_audit_log_refactoring.py::test_audit_refresh_population
1 error in 13.00s

```
</details>

---
### `tests/unit/test_audit_manager_coverage.py::TestAuditManager::test_init_db_creation`
**Error:** `FAILED tests/unit/test_audit_manager_coverage.py::TestAuditManager::test_init_db_creation`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
___________________ TestAuditManager.test_init_db_creation ____________________
tests\unit\test_audit_manager_coverage.py:46: in test_init_db_creation
    assert cursor.fetchone() is not None
E   assert None is not None
E    +  where None = <built-in method fetchone of sqlite3.Cursor object at 0x000002D4C3D8D240>()
E    +    where <built-in method fetchone of sqlite3.Cursor object at 0x000002D4C3D8D240> = <sqlite3.Cursor object at 0x000002D4C3D8D240>.fetchone
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      20     20     0%   6-133
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                241    241     0%   6-425
src\bots\base\login_page.py                               94     94     0%   6-154
src\bots\base\wait_helpers.py                            171    171     0%   14-478
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               90     90     0%   5-158
src\core\app_updater.py                                   46     46     0%   6-85
src\core\audit\__init__.py                                 3      0   100%
src\core\audit\database.py                                98     39    60%   59-61, 76-77, 106-108, 110-113, 115-118, 120-122, 124-128, 140-141, 145-150, 153-159
src\core\audit\integrity.py                               15      2    87%   20, 25
src\core\audit\manager.py                                133     55    59%   27, 45, 49, 57-61, 116-118, 126, 128, 137-138, 142-168, 178, 181-184, 192-213
src\core\audit\models.py                                   9      0   100%
src\core\audit\signals.py                                 24     10    58%   21-30
src\core\audit_manager.py                                  5      0   100%
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-248
src\core\bug_reporter.py                                  60     60     0%   1-119
src\core\config_manager.py                               241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                     90      0   100%
src\core\contabilita_manager.py                          106    106     0%   6-229
src\core\contabilita_queries.py                           87     87     0%   6-122
src\core\contabilita_search.py                            91     91     0%   6-177
src\core\contabilita_stats.py                             59     59     0%   6-99
src\core\contabilita_worker.py                           102    102     0%   1-216
src\core\data_synchronizer.py                            143    143     0%   6-260
src\core\database.py                                     220    220     0%   6-585
src\core\employees.py                                     89     89     0%   1-186
src\core\excel_importer.py                                 4      4     0%   6-11
src\core\importers\__init__.py                            43     43     0%   1-105
src\core\importers\attivita.py                            64     64     0%   1-114
src\core\importers\base.py                                63     63     0%   1-92
src\core\importers\certificati.py                        119    119     0%   1-185
src\core\importers\contabilita.py                        140    140     0%   1-239
src\core\importers\giornaliere.py                        189    189     0%   1-299
src\core\importers\scarico_ore.py                        198    198     0%   1-314
src\core\importers\storico_oda.py                         85     85     0%   1-180
src\core\license_updater.py                              155    155     0%   6-294
src\core\license_validator.py                            183    183     0%   6-356
src\core\lyra_client.py                                  128    128     0%   6-253
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-148, 152-154, 158, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                   17     17     0%   6-36
src\core\report_history.py                                67     67     0%   7-157
src\core\schemas.py                                       78     78     0%   1-109
src\core\secrets_manager.py                               96     60    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                 47     47     0%   6-83
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             175    175     0%   1-274
src\core\telegram_bridge.py                              342    342     0%   1-482
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-166
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\design\colors.py                                  27      1    96%   105
src\gui\design\spacing.py                                 25      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         51     51     0%   1-87
src\gui\dialogs\audit_detail_dialog.py                    59     47    20%   24-28, 31-114, 117-119
src\gui\dialogs\bug_report_dialog.py                     158    158     0%   1-349
src\gui\dialogs\command_palette.py                       302    302     0%   1-512
src\gui\dialogs\confirmation_dialog.py                    27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                        244    244     0%   6-382
src\gui\formatters.py                                    129    129     0%   1-230
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-329
src\gui\main_window\components\status_bar.py             158    158     0%   1-278
src\gui\main_window\components\tool_bar.py                25     25     0%   1-39
src\gui\main_window\components\tray_icon.py               16     16     0%   1-36
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       20     20     0%   1-40
src\gui\main_window\main.py                              280    280     0%   1-445
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\models\audit_model.py                            128     23    82%   52, 97, 110-111, 121, 127, 129, 139-141, 160-161, 166-168, 176, 178, 180, 183-184, 187-189
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   196    196     0%   6-386
src\gui\panels\carico_ts.py                               90     90     0%   6-183
src\gui\panels\contabilita_kpi_panel.py                  379    379     0%   1-878
src\gui\panels\contabilita_panel.py                      255    255     0%   6-439
src\gui\panels\dashboard_panel.py                        168    168     0%   1-302
src\gui\panels\dettagli_oda.py                           127    127     0%   6-220
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-62
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-276
src\gui\panels\dipendenti_manager_panel.py               156    156     0%   1-315
src\gui\panels\help_panel.py                             120    120     0%   6-364
src\gui\panels\lyra_panel.py                             349    349     0%   1-696
src\gui\panels\notifications_panel.py                    247    247     0%   6-432
src\gui\panels\pdl_db.py                                 202    202     0%   6-353
src\gui\panels\prenota_bp.py                             104    104     0%   6-190
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-143
src\gui\panels\scarico_ore_panel.py                      306    306     0%   7-524
src\gui\panels\scarico_pdl.py                            223    223     0%   6-399
src\gui\panels\scarico_ts.py                             121    121     0%   6-210
src\gui\panels\storico_oda_panel.py                      225    225     0%   6-525
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       148    148     0%   1-262
src\gui\panels\timbrature_bot.py                         116    116     0%   6-200
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      4     0%   6-45
src\gui\styles\constants.py                                8      8     0%   9-156
src\gui\styles\theme_manager.py                           70     70     0%   6-128
src\gui\styles\widget_styles.py                           35     35     0%   6-431
src\gui\toast.py                                          45     45     0%   6-90
src\gui\widgets\__init__.py                               12      0   100%
src\gui\widgets\activity_feed.py                         137    137     0%   1-317
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-139
src\gui\widgets\audit\audit_filter_bar.py                 70      8    89%   89-95, 104-105
src\gui\widgets\audit\audit_pagination_bar.py             34      3    91%   37, 45-46
src\gui\widgets\audit_log_widget.py                      102     16    84%   119-129, 132, 135-136, 140, 168-170
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                      486    486     0%   5-1097
src\gui\widgets\bot_parameters.py                        112     89    21%   39-43, 46-108, 118-125, 129, 145, 149-151, 155-164, 169, 173-175, 179-181, 191-198, 202, 206-207
src\gui\widgets\calendar_date_edit.py                     16      0   100%
src\gui\widgets\data_table.py                            109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                           330    292    12%   29-34, 45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 280-282, 285-306, 309-364, 367-370, 373-379, 382-414, 417-420, 423-425, 428, 432-449, 458-468, 472-512, 517-542
src\gui\widgets\footer_stats.py                          400    400     0%   7-693
src\gui\widgets\info_widgets.py                           89     74    17%   26-57, 60, 67-75, 80-104, 111-161, 164, 167
src\gui\widgets\message_bubble.py                         53     53     0%   7-123
src\gui\widgets\modern_button.py                          61     35    43%   42-54, 58-60, 64, 68-69, 75-78, 82-85, 89-90, 100-105, 109-148
src\gui\widgets\notification_card.py                     220    220     0%   6-520
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-282
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-359
src\gui\widgets\security_dashboard.py                    143    143     0%   1-237
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        183    183     0%   1-322
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-211
src\gui\widgets\status_card.py                            59     47    20%   19-84, 88-91, 100-116, 120, 124-125
src\gui\widgets\status_indicator.py                       42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                       191    155    19%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 165-170, 173-186, 191-198, 202, 205-215, 218-231, 234-239, 242-246, 257-273, 276, 279, 284-309
src\gui\widgets\toast.py                                 128     98    23%   55-75, 79-118, 122-145, 148-152, 156-158, 162-163, 166-178, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                          35     35     0%   1-49
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-295
src\utils\date_utils.py                                   69     69     0%   6-230
src\utils\document_generator.py                           13     13     0%   5-35
src\utils\document_processor.py                           66     66     0%   6-90
src\utils\helpers.py                                      97     65    33%   24-30, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 212-234, 243, 249-252
src\utils\log_humanizer.py                                41     30    27%   12-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                      53     53     0%   6-119
src\utils\printing.py                                     83     83     0%   1-141
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     79     0%   6-141
src\utils\system_telemetry.py                             25     25     0%   6-70
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  15227  14194     7%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_audit_manager_coverage.py::TestAuditManager::test_init_db_creation
1 failed in 5.27s

```
</details>

---
### `tests/unit/test_core_logic_boost.py::TestCoreLogicRefined::test_audit_manager_singleton_and_init`
**Error:** `FAILED tests/unit/test_core_logic_boost.py::TestCoreLogicRefined::test_audit_manager_singleton_and_init`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________ TestCoreLogicRefined.test_audit_manager_singleton_and_init __________
tests\unit\test_core_logic_boost.py:21: in test_audit_manager_singleton_and_init
    assert res is not None
E   assert None is not None
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              241     43    82%   74, 80, 129-130, 142, 166, 214-216, 228-230, 241, 255, 323, 346-347, 353, 357-361, 365-367, 371, 375-381, 400-404, 409-413, 425
src\bots\base\login_page.py                                             94     63    33%   43-53, 57-77, 81-93, 97-103, 116-117, 128-144, 149-154
src\bots\base\wait_helpers.py                                          171    171     0%   14-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     18    62%   20, 25, 31, 56, 60-72, 86, 92, 95, 101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     12    78%   34-36, 47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-92, 96-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    144    32%   49-55, 66-91, 102-115, 119-148, 152-162, 222, 237-245, 262-266, 275-283, 287-305, 315-341, 345-354, 358-367, 371-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    158    30%   39, 44, 49, 60, 79-81, 85-100, 104-121, 125-140, 144-166, 170-198, 202-211, 215-240, 245, 274-276, 282-311, 315-324, 340, 347-367, 371-384
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     56    46%   38-44, 63-65, 89-91, 95-124, 128-145, 149-154, 158-167
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     49    35%   26, 31, 36, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    102    37%   45-60, 82-84, 88-149, 166-167, 178-180, 183, 201-202, 206-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    154    19%   88-111, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 289-322, 325-363, 367-384, 391-392
src\bots\safework\base.py                                               41     17    59%   21, 40-43, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    313    22%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-156, 160-164, 168-193, 197-226, 230-238, 243, 252-254, 257-259, 265-266, 272-277, 283-311, 315-327, 331-359, 363-405, 409-425, 429-450, 454-466, 474, 483, 488-512, 516, 530-531, 551, 557-560, 564-583
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     90     0%   5-158
src\core\app_updater.py                                                 46     46     0%   6-85
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              98     35    64%   59-61, 76-77, 106-108, 110-113, 115-118, 120-122, 124-128, 140-141, 145-150, 157-159
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              133     29    78%   49, 60-61, 116-118, 126, 128, 137-138, 151, 167-168, 178, 192-213
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               24     10    58%   21-30
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     23    83%   59-61, 68, 85, 95, 108-110, 115, 119, 122, 178-187, 214, 220-222, 229, 247-248
src\core\bug_reporter.py                                                60     60     0%   1-119
src\core\config_manager.py                                             241     65    73%   35, 113-119, 140, 163, 226, 284, 301-302, 331-358, 379-381, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     21    80%   29, 39, 79, 117, 130-131, 140-147, 156-161, 174, 192, 207, 216, 224
src\core\contabilita_queries.py                                         87     17    80%   29-30, 36, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 112, 121-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102      8    92%   75, 113, 132-133, 139, 153-154, 216
src\core\data_synchronizer.py                                          143     55    62%   22, 68-70, 109, 150-151, 159-194, 198, 208, 219-232, 239-260
src\core\database.py                                                   220     25    89%   79-88, 115-125, 138-139, 165-167
src\core\employees.py                                                   89     73    18%   25-63, 67-69, 76-99, 104-120, 127-182
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      5    88%   49, 61, 72, 76, 98
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-96, 100-114
src\core\importers\base.py                                              63     21    67%   14-15, 22-24, 50-55, 70-80, 90-92
src\core\importers\certificati.py                                      119     21    82%   37, 46, 50, 53-54, 63, 91, 105-106, 139, 148, 160, 164-165, 169, 172-177
src\core\importers\contabilita.py                                      140     27    81%   39, 46-54, 67, 75, 85, 99-101, 115, 123, 135-136, 145, 181-183, 201, 221, 223
src\core\importers\giornaliere.py                                      189    151    20%   38, 43-55, 66-84, 93-109, 115-134, 140-178, 182-197, 201-223, 227-279, 283-299
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-85, 93-111, 115-135, 149-180, 184-248, 252-261, 278-282, 286-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155    155     0%   6-294
src\core\license_validator.py                                          183    183     0%   6-356
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-108, 112-143, 152-206, 215-253
src\core\lyra_sentinel.py                                               32     24    25%   22-53
src\core\notification_manager.py                                        97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-148, 152-154, 158, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                                 17      6    65%   22, 31-36
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-50, 61-85, 95-96, 114-134, 147-157
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 93-95, 100-102, 108
src\core\secrets_manager.py                                             96     53    45%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 122-126, 133-134, 139-145
src\core\stats_manager.py                                               47     12    74%   40-45, 48, 61, 63, 72, 76, 83
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    140    20%   38-48, 52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    342     0%   1-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      5    74%   30, 33-36, 52
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   19-53, 56-64, 67-83, 92-110, 119-144, 147-151, 154-168, 171-176, 179-183, 186-211, 214-219, 222-227, 230-231, 234-259, 262-267
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-132, 135-149, 152-155, 158-165, 168-171, 174-176, 179-181, 184-210, 213-230, 233-235, 238-265
src\gui\controllers\bot_controller.py                                   38     14    63%   24-32, 63-71
src\gui\controllers\navigation_controller.py                           154    113    27%   41-57, 61-77, 80-94, 97-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 158-164, 168-172, 176-182, 194-230, 235-236, 254-256, 260-261, 265-266, 270-303, 307-308
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-74, 77-84, 87
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   24-28, 31-114, 117-119
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-349
src\gui\dialogs\command_palette.py                                     302    302     0%   1-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129     67    48%   13, 21-27, 37-68, 73, 98, 102, 112, 118-120, 134, 158-210, 220-222, 227-228
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-329
src\gui\main_window\components\status_bar.py                           158    158     0%   1-278
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-39
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-40
src\gui\main_window\main.py                                            280    280     0%   1-445
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 40-42, 45, 48, 51-75, 79-97, 101-111, 115-122, 126-130, 134-142, 146-148, 151-153, 156-161, 164-168, 172-184, 187-189
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196     25    87%   59-72, 84-88, 205, 217, 226, 246-248, 367-370, 378, 385
src\gui\panels\carico_ts.py                                             90     28    69%   39-43, 96-99, 103-108, 114, 118, 124-125, 133-137, 141-148, 164-165
src\gui\panels\contabilita_kpi_panel.py                                379     42    89%   302, 341, 349, 448-449, 465-467, 503-517, 520-533, 568, 626-634, 645, 737-739, 786
src\gui\panels\contabilita_panel.py                                    255    112    56%   49-55, 184-191, 195, 228-230, 239, 243-264, 269-293, 297-299, 303-306, 314-319, 322-335, 346-348, 356-357, 368, 375, 386-387, 392, 396-413, 417, 420-439
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-126, 130-132, 136-146, 150-165, 170-185, 190-208, 213-227, 232-241, 245-260, 264-292, 296-302
src\gui\panels\dettagli_oda.py                                         127     67    47%   37-41, 92-94, 98, 101-113, 117, 129-131, 139, 144-220
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     530    485     8%   53-83, 86-206, 209-314, 317-322, 326-360, 364-377, 380-408, 411-455, 459-467, 471-488, 491-518, 521-533, 536-545, 549-580, 583-616, 621-626, 629-670, 673-675, 678-714, 718-740, 744-787, 795-881, 885-896, 900-922, 926-959
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-159, 162-164, 167-169, 172-174, 177, 182-223, 228-276
src\gui\panels\dipendenti_manager_panel.py                             156    137    12%   27-69, 72, 83-95, 98-123, 126-157, 160-190, 194-223, 227-243, 247-266, 269-281, 288-315
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-167, 171-191, 194-203, 206-214, 217-220, 223, 243, 263, 275, 289, 300, 313, 325, 336, 346, 356, 364
src\gui\panels\lyra_panel.py                                           349    303    13%   60-64, 68-86, 98-99, 103-112, 124-132, 136-400, 407-420, 424-425, 429-449, 453-456, 460-464, 468-483, 491-493, 497-500, 504-507, 511-512, 516-521, 531-551, 557-560, 564-578, 582-599, 603-635, 643-656, 660-672, 676-687, 691-696
src\gui\panels\notifications_panel.py                                  247    201    19%   56-69, 72-140, 143-144, 148-150, 154-156, 160-162, 166-167, 171-172, 176, 179-183, 188-223, 228-251, 255-281, 289-297, 301-302, 306-324, 328-360, 364-366, 370-389, 393-432
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-49, 56-108, 111-201, 205-216, 220-240, 244-250, 254-270, 274-327, 333-337, 341-353
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-76, 80-82, 85-93, 96-102, 105-115, 119-190
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-66, 69-72, 75-76, 79-84, 94-126, 131-138, 141-143
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   42-44, 49-83, 94-101, 105-234, 238-253, 257-285, 289-291, 295-303, 307-328, 332-334, 338-356, 367-396, 400-405, 409-421, 425-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          223     54    76%   53-55, 92, 163-171, 174-177, 183, 189-191, 204-214, 218-226, 231-238, 249-252, 255, 260, 277-281, 284-287, 331, 341, 380
src\gui\panels\scarico_ts.py                                           121     24    80%   37-39, 82-84, 103, 110, 121-123, 165-174, 182-186
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-182
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-36, 40-41, 44, 47
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-74
src\gui\panels\settings\pages\lists_page.py                            319    268    16%   32-33, 36-62, 67-84, 87-104, 107-126, 129-148, 151-170, 173-192, 197-203, 206-207, 214, 224, 234-243, 246-254, 259-262, 265-272, 275-283, 286-302, 305-315, 318-324, 329-338, 341-355, 358-368, 371-377, 382-383, 386, 389-392, 395-400, 403-410, 414, 417, 420, 423, 426, 429, 432, 435, 438, 441, 444, 447, 452-457, 460-465
src\gui\panels\settings\pages\paths_page.py                            107     86    20%   26-27, 30-68, 71-90, 94-115, 132-133, 136, 139-141, 144-146, 149-151, 154-156, 159-161, 166-181, 184-189
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 98-100
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-104, 111, 114-116, 119-121
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-129, 132-137, 140-153, 156-165, 169-173, 181-191, 195-208
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-248, 252-265, 269-279, 283, 287, 291-302, 306-313, 317-324, 328-380, 384-497, 501-525
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     29    54%   69-109, 113-131
src\gui\panels\timbrature\components\settings_tab.py                    94      4    96%   139, 151-153
src\gui\panels\timbrature\panel.py                                     148     16    89%   212-218, 221-228, 242, 257-258, 262
src\gui\panels\timbrature_bot.py                                       116     35    70%   40-42, 60-62, 89, 98-103, 113-114, 126-134, 139-149, 172-174, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-128
src\gui\styles\widget_styles.py                                         35     35     0%   6-431
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-183, 187, 191-193, 202-210, 213-261, 266, 271-317
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-139
src\gui\widgets\audit\audit_filter_bar.py                               70     57    19%   21-25, 28-81, 84-86, 89-95, 104-105, 108-117
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   10-11, 14-32, 35-42, 45-46
src\gui\widgets\audit_log_widget.py                                    102     80    22%   38-50, 53-112, 115-116, 119-129, 132, 135-136, 139-155, 158-165, 168-170
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                                    486    452     7%   43-147, 151-168, 172-189, 198-327, 331-339, 343-359, 369-521, 525-534, 538-554, 563-572, 576, 580, 584-694, 698-712, 716-741, 745-749, 753-773, 777-787, 791-817, 822-847, 855-882, 890-912, 916-1021, 1025-1097
src\gui\widgets\bot_parameters.py                                      112      6    95%   145, 149-151, 197-198
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208     57    73%   131, 186, 197-200, 220, 224-227, 231-239, 242-245, 248-251, 254-257, 260-263, 266-270, 273-284, 287-292
src\gui\widgets\contabilita\certificati_tab.py                         222     54    76%   192, 217-218, 307, 324, 352-354, 400, 406-409, 413-416, 420-430, 433-438, 441-446, 450-553
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-90, 94, 97-124, 127-134, 138, 141-157, 160-178, 182-194, 197-214, 217-233
src\gui\widgets\contabilita\helpers.py                                  33     17    48%   21-31, 37-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                                         330    209    37%   45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 309-364, 373-379, 408, 417-420, 423-425, 500-504, 517-542
src\gui\widgets\footer_stats.py                                        400    400     0%   7-693
src\gui\widgets\info_widgets.py                                         89     39    56%   26-57, 60, 80-104, 167
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        61     11    82%   68-69, 75-78, 82-85, 146
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-341, 345-355, 359, 363-365, 379-410, 414-431, 435-439, 443-445, 449-450, 454-458, 463-464, 468-503, 507-511, 515-520
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-231, 236-237, 241-242, 247-254, 258-259, 268-270, 274, 278, 282
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-261, 265-306, 311-354, 359
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-322
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-107, 110-142, 146-148, 152-163, 169-211
src\gui\widgets\status_card.py                                          59      8    86%   100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191     42    78%   74-75, 77-78, 121-123, 125-127, 131, 134-139, 147-151, 154-155, 158-160, 173-186, 220-228
src\gui\widgets\toast.py                                               128     98    23%   55-75, 79-118, 122-145, 148-152, 156-158, 162-163, 166-178, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35     35     0%   1-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13     13     0%   5-35
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-54, 59-70, 75-90
src\utils\helpers.py                                                    97     55    43%   24-30, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 213, 232, 243, 252
src\utils\log_humanizer.py                                              41     14    66%   12-26, 110, 118
src\utils\parsing.py                                                    53     12    77%   14, 17, 21, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     37    53%   43-44, 54-58, 80-82, 101-111, 115-137
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                20974  14371    31%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_core_logic_boost.py::TestCoreLogicRefined::test_audit_manager_singleton_and_init
1 failed in 7.55s

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
tests\unit\test_gui_headless_hardened.py:45: in test_dashboard_greeting_logic
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
src\bots\base\base_bot.py                                              241     43    82%   74, 80, 129-130, 142, 166, 214-216, 228-230, 241, 255, 323, 346-347, 353, 357-361, 365-367, 371, 375-381, 400-404, 409-413, 425
src\bots\base\login_page.py                                             94     63    33%   43-53, 57-77, 81-93, 97-103, 116-117, 128-144, 149-154
src\bots\base\wait_helpers.py                                          171    171     0%   14-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     18    62%   20, 25, 31, 56, 60-72, 86, 92, 95, 101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     12    78%   34-36, 47-49, 71-73, 106-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     15    81%   21, 26, 31, 42, 61, 64, 75, 102, 107, 123-124, 126-127, 136, 143
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212     67    68%   49-55, 88-91, 102-115, 129-131, 145-148, 160-162, 222, 237-245, 262-266, 275-283, 304-305, 321-322, 328, 333-336, 339-341, 350-351, 353-354, 367
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    158    30%   39, 44, 49, 60, 79-81, 85-100, 104-121, 125-140, 144-166, 170-198, 202-211, 215-240, 245, 274-276, 282-311, 315-324, 340, 347-367, 371-384
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     56    46%   38-44, 63-65, 89-91, 95-124, 128-145, 149-154, 158-167
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     49    35%   26, 31, 36, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    102    37%   45-60, 82-84, 88-149, 166-167, 178-180, 183, 201-202, 206-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    154    19%   88-111, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 289-322, 325-363, 367-384, 391-392
src\bots\safework\base.py                                               41     17    59%   21, 40-43, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    313    22%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-156, 160-164, 168-193, 197-226, 230-238, 243, 252-254, 257-259, 265-266, 272-277, 283-311, 315-327, 331-359, 363-405, 409-425, 429-450, 454-466, 474, 483, 488-512, 516, 530-531, 551, 557-560, 564-583
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     90     0%   5-158
src\core\app_updater.py                                                 46     46     0%   6-85
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              98     35    64%   59-61, 76-77, 106-108, 110-113, 115-118, 120-122, 124-128, 140-141, 145-150, 157-159
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              133     29    78%   49, 60-61, 116-118, 126, 128, 137-138, 151, 167-168, 178, 192-213
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               24     10    58%   21-30
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     22    84%   59-61, 68, 85, 95, 108-110, 115, 122, 178-187, 214, 220-222, 229, 247-248
src\core\bug_reporter.py                                                60     60     0%   1-119
src\core\config_manager.py                                             241     65    73%   35, 113-119, 140, 163, 226, 284, 301-302, 331-358, 379-381, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     21    80%   29, 39, 79, 117, 130-131, 140-147, 156-161, 174, 192, 207, 216, 224
src\core\contabilita_queries.py                                         87      5    94%   36, 52, 80, 96, 112
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           59      0   100%
src\core\contabilita_worker.py                                         102      8    92%   75, 113, 132-133, 139, 153-154, 216
src\core\data_synchronizer.py                                          143     19    87%   22, 109, 198, 208, 239-260
src\core\database.py                                                   220     10    95%   120-125, 138-139, 165-167
src\core\employees.py                                                   89     73    18%   25-63, 67-69, 76-99, 104-120, 127-182
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43      0   100%
src\core\importers\attivita.py                                          64      4    94%   57-58, 89-90
src\core\importers\base.py                                              63      7    89%   14-15, 22-24, 54-55
src\core\importers\certificati.py                                      119     14    88%   46, 50, 53-54, 63, 91, 105-106, 139, 164-165, 175-177
src\core\importers\contabilita.py                                      140      9    94%   39, 48, 52-54, 115, 181-183
src\core\importers\giornaliere.py                                      189     32    83%   49-55, 72, 82, 97, 100, 104, 132, 149, 153, 177-178, 189-197, 210-211, 214, 228, 234, 242, 256
src\core\importers\scarico_ore.py                                      198     40    80%   11-12, 18-20, 47, 63-64, 70-85, 95, 98, 110-111, 124, 174, 202, 206, 215, 219, 233, 245, 254, 289, 299-300, 311-312
src\core\importers\storico_oda.py                                       85     62    27%   61-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155    155     0%   6-294
src\core\license_validator.py                                          183    183     0%   6-356
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-108, 112-143, 152-206, 215-253
src\core\lyra_sentinel.py                                               32      9    72%   38-39, 45-51
src\core\notification_manager.py                                        97     45    54%   44, 52-59, 63-76, 83-84, 135-148, 152-154, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                                 17      2    88%   35-36
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-50, 61-85, 95-96, 114-134, 147-157
src\core\schemas.py                                                     78     23    71%   67-72, 77-88, 93-95, 101, 108
src\core\secrets_manager.py                                             96     51    47%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 124-126, 133-134, 139-145
src\core\stats_manager.py                                               47     10    79%   40-45, 48, 61, 63, 76
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    140    20%   38-48, 52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    342     0%   1-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      1    95%   30
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   19-53, 56-64, 67-83, 92-110, 119-144, 147-151, 154-168, 171-176, 179-183, 186-211, 214-219, 222-227, 230-231, 234-259, 262-267
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-132, 135-149, 152-155, 158-165, 168-171, 174-176, 179-181, 184-210, 213-230, 233-235, 238-265
src\gui\controllers\bot_controller.py                                   38     14    63%   24-32, 63-71
src\gui\controllers\navigation_controller.py                           154    113    27%   41-57, 61-77, 80-94, 97-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 158-164, 168-172, 176-182, 194-230, 235-236, 254-256, 260-261, 265-266, 270-303, 307-308
src\gui\controllers\search_controller.py                               197    162    18%   18-44, 59, 69-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-74, 77-84, 87
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   24-28, 31-114, 117-119
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-349
src\gui\dialogs\command_palette.py                                     302    302     0%   1-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81      0   100%
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129     52    60%   13, 21-27, 38, 47, 50, 67-68, 102, 118-120, 134, 158-210, 220-222, 227-228
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-329
src\gui\main_window\components\status_bar.py                           158    158     0%   1-278
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-39
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-40
src\gui\main_window\main.py                                            280    280     0%   1-445
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128    104    19%   28-31, 40-42, 45, 48, 51-75, 79-97, 101-111, 115-122, 126-130, 134-142, 146-148, 151-153, 156-161, 164-168, 172-184, 187-189
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196     25    87%   59-72, 84-88, 205, 217, 226, 246-248, 367-370, 378, 385
src\gui\panels\carico_ts.py                                             90     23    74%   39-43, 96-99, 103-108, 114, 118, 124-125, 141-148, 164-165
src\gui\panels\contabilita_kpi_panel.py                                379     41    89%   302, 341, 448-449, 465-467, 503-517, 520-533, 568, 626-634, 645, 737-739, 786
src\gui\panels\contabilita_panel.py                                    255     84    67%   51-55, 184-191, 195, 239, 245-250, 271-275, 279-282, 288-290, 297-299, 306, 316-319, 323-327, 331-335, 346-348, 356-357, 368, 375, 386-387, 392, 396-413, 417, 420-439
src\gui\panels\dashboard_panel.py                                      168     81    52%   84, 130-132, 139, 141, 144-146, 151-152, 154-164, 181-184, 191-194, 197, 205-208, 213-227, 232-241, 245-260, 264-292, 296-302
src\gui\panels\dettagli_oda.py                                         127     67    47%   37-41, 92-94, 98, 101-113, 117, 129-131, 139, 144-220
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     530    485     8%   53-83, 86-206, 209-314, 317-322, 326-360, 364-377, 380-408, 411-455, 459-467, 471-488, 491-518, 521-533, 536-545, 549-580, 583-616, 621-626, 629-670, 673-675, 678-714, 718-740, 744-787, 795-881, 885-896, 900-922, 926-959
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-159, 162-164, 167-169, 172-174, 177, 182-223, 228-276
src\gui\panels\dipendenti_manager_panel.py                             156     82    47%   27-69, 72, 194-223, 227-243, 247-266, 269-281, 288-315
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-167, 171-191, 194-203, 206-214, 217-220, 223, 243, 263, 275, 289, 300, 313, 325, 336, 346, 356, 364
src\gui\panels\lyra_panel.py                                           349    303    13%   60-64, 68-86, 98-99, 103-112, 124-132, 136-400, 407-420, 424-425, 429-449, 453-456, 460-464, 468-483, 491-493, 497-500, 504-507, 511-512, 516-521, 531-551, 557-560, 564-578, 582-599, 603-635, 643-656, 660-672, 676-687, 691-696
src\gui\panels\notifications_panel.py                                  247    201    19%   56-69, 72-140, 143-144, 148-150, 154-156, 160-162, 166-167, 171-172, 176, 179-183, 188-223, 228-251, 255-281, 289-297, 301-302, 306-324, 328-360, 364-366, 370-389, 393-432
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-49, 56-108, 111-201, 205-216, 220-240, 244-250, 254-270, 274-327, 333-337, 341-353
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-76, 80-82, 85-93, 96-102, 105-115, 119-190
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-66, 69-72, 75-76, 79-84, 94-126, 131-138, 141-143
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   42-44, 49-83, 94-101, 105-234, 238-253, 257-285, 289-291, 295-303, 307-328, 332-334, 338-356, 367-396, 400-405, 409-421, 425-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          223     54    76%   53-55, 92, 163-171, 174-177, 183, 189-191, 204-214, 218-226, 231-238, 249-252, 255, 260, 277-281, 284-287, 331, 341, 380
src\gui\panels\scarico_ts.py                                           121     24    80%   37-39, 82-84, 103, 110, 121-123, 165-174, 182-186
src\gui\panels\settings\main_panel.py                                  105     30    71%   113-131, 140, 145-147, 150-163, 166-182
src\gui\panels\settings\pages\diag_page.py                              32      3    91%   40-41, 47
src\gui\panels\settings\pages\general_page.py                           43      2    95%   73-74
src\gui\panels\settings\pages\lists_page.py                            319    121    62%   214, 224, 234-243, 246-254, 261, 286-302, 305-315, 318-324, 329-338, 341-355, 358-368, 371-377, 386, 389-392, 395-400, 403-410, 414, 417, 420, 423, 426, 429, 432, 435, 438, 441, 444, 447, 460-465
src\gui\panels\settings\pages\paths_page.py                            107     28    74%   99-115, 132-133, 136, 139-141, 144-146, 149-151, 154-156, 159-161, 184-189
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     33    75%   150-152, 158-160, 166-171, 174-175, 182-184, 192-195, 200-224
src\gui\panels\settings\tabs\config_tab.py                              55      4    93%   111, 119-121
src\gui\panels\settings\tabs\telegram_tab.py                           136     34    75%   132-137, 140-153, 156-165, 169-173, 195-208
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-248, 252-265, 269-279, 283, 287, 291-302, 306-313, 317-324, 328-380, 384-497, 501-525
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     29    54%   69-109, 113-131
src\gui\panels\timbrature\components\settings_tab.py                    94      4    96%   139, 151-153
src\gui\panels\timbrature\panel.py                                     148     16    89%   212-218, 221-228, 242, 257-258, 262
src\gui\panels\timbrature_bot.py                                       116     35    70%   40-42, 60-62, 89, 98-103, 113-114, 126-134, 139-149, 172-174, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-128
src\gui\styles\widget_styles.py                                         35     35     0%   6-431
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     22    84%   39-40, 88-90, 149-150, 170-180, 187, 191-193, 266, 272, 283, 285
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-139
src\gui\widgets\audit\audit_filter_bar.py                               70     57    19%   21-25, 28-81, 84-86, 89-95, 104-105, 108-117
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   10-11, 14-32, 35-42, 45-46
src\gui\widgets\audit_log_widget.py                                    102     80    22%   38-50, 53-112, 115-116, 119-129, 132, 135-136, 139-155, 158-165, 168-170
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                                    486    230    53%   43-147, 151-168, 172-189, 343-359, 538-554, 576, 580, 698-712, 716-741, 745-749, 753-773, 777-787, 791-817, 822-847, 855-882, 890-912, 926, 943-944, 956-957, 969-970, 982-984, 1017-1021, 1030-1036, 1040
src\gui\widgets\bot_parameters.py                                      112      3    97%   145, 197-198
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208     57    73%   131, 186, 197-200, 220, 224-227, 231-239, 242-245, 248-251, 254-257, 260-263, 266-270, 273-284, 287-292
src\gui\widgets\contabilita\certificati_tab.py                         222     54    76%   192, 217-218, 307, 324, 352-354, 400, 406-409, 413-416, 420-430, 433-438, 441-446, 450-553
src\gui\widgets\contabilita\giornaliere_tab.py                         166     50    70%   94, 128, 142, 166, 176-177, 182-194, 197-214, 217-233
src\gui\widgets\contabilita\helpers.py                                  33     17    48%   21-31, 37-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     13    81%   99, 123-124, 128-157, 161
src\gui\widgets\data_table.py                                          109      1    99%   127
src\gui\widgets\excel_table.py                                         330     93    72%   62-69, 85, 96, 100, 107, 113, 141-163, 167-189, 195, 220, 225, 242-245, 252-257, 269, 309-364, 375, 408, 417-420, 423-425, 504, 525, 539
src\gui\widgets\footer_stats.py                                        400    400     0%   7-693
src\gui\widgets\info_widgets.py                                         89     38    57%   26-57, 60, 80-104
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        61     10    84%   68-69, 75-78, 82-85
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-341, 345-355, 359, 363-365, 379-410, 414-431, 435-439, 443-445, 449-450, 454-458, 463-464, 468-503, 507-511, 515-520
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-231, 236-237, 241-242, 247-254, 258-259, 268-270, 274, 278, 282
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     14    82%   265-306, 320, 336, 353-354
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41      7    83%   28-30, 35-37, 76
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-322
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     32    29%   28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100      7    93%   153-155, 192-193, 206-207
src\gui\widgets\status_card.py                                          59      8    86%   100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191     42    78%   74-75, 77-78, 121-123, 125-127, 131, 134-139, 147-151, 154-155, 158-160, 173-186, 220-228
src\gui\widgets\toast.py                                               128     34    73%   137-145, 148-152, 156-158, 162-163, 168-169, 175, 206-213, 221, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35     35     0%   1-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13      0   100%
src\utils\document_processor.py                                         66      7    89%   15-16, 68-70, 88-90
src\utils\helpers.py                                                    97     54    44%   24-30, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 213, 232, 252
src\utils\log_humanizer.py                                              41     10    76%   18-26, 110, 118
src\utils\parsing.py                                                    53     12    77%   14, 17, 21, 45-46, 79, 86, 95, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     23    71%   43-44, 80-82, 102, 104, 109-111, 116, 122-137
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                20974  12075    42%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_gui_headless_hardened.py::TestGUIHeadlessHardened::test_dashboard_greeting_logic
1 failed in 12.68s

```
</details>

---
### `tests/unit/test_hardening_audit_security.py::TestHardeningAuditSecurity::test_audit_deletion_integrity_break`
**Error:** `FAILED tests/unit/test_hardening_audit_security.py::TestHardeningAuditSecurity::test_audit_deletion_integrity_break`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_______ TestHardeningAuditSecurity.test_audit_deletion_integrity_break ________
tests\unit\test_hardening_audit_security.py:54: in test_audit_deletion_integrity_break
    assert manager.verify_integrity() is True
E   assert False is True
E    +  where False = verify_integrity()
E    +    where verify_integrity = <src.core.audit.manager.AuditManager object at 0x000001BCEAEA9550>.verify_integrity
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              241    188    22%   52-68, 74, 80, 85, 90-92, 104-108, 118-130, 134, 138, 142, 146-147, 151-152, 156-170, 174-219, 224-241, 245-247, 254-259, 263-273, 284-318, 322-347, 351-353, 357-361, 365-367, 371, 375-381, 392-404, 408-413, 425
src\bots\base\login_page.py                                             94     78    17%   34-37, 43-53, 57-77, 81-93, 97-103, 110-154
src\bots\base\wait_helpers.py                                          171    171     0%   14-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-92, 96-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   38-41, 45, 49-55, 66-91, 102-115, 119-148, 152-162, 186-283, 287-305, 315-341, 345-354, 358-367, 371-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-140, 144-166, 170-198, 202-211, 215-240, 244-276, 282-311, 315-324, 328-343, 347-367, 371-384
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-84, 88-149, 153-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-76, 80-81, 88-111, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 289-322, 325-363, 367-384, 391-392
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-156, 160-164, 168-193, 197-226, 230-238, 242-279, 283-311, 315-327, 331-359, 363-405, 409-425, 429-450, 454-466, 473-512, 515-560, 564-583
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     90     0%   5-158
src\core\app_updater.py                                                 46     46     0%   6-85
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              98     28    71%   59-61, 76-77, 115-118, 120-122, 124-128, 140-141, 149-150, 153-159
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              133     52    61%   45, 49, 57-61, 114-118, 122-138, 151, 165-168, 171-172, 181-184, 192-213
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               24     10    58%   21-30
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     64    53%   42, 48, 59-61, 68, 71, 85, 93, 95, 108-110, 115, 120-125, 134-187, 198-206, 214, 220-222, 227-248
src\core\bug_reporter.py                                                60     60     0%   1-119
src\core\config_manager.py                                             241    142    41%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 226, 236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     53    50%   29, 34, 39, 48-60, 77-131, 140-147, 156-161, 170-177, 192, 207, 216, 224
src\core\contabilita_queries.py                                         87     27    69%   20, 29-30, 36, 45-46, 52, 73-74, 80, 89-90, 96, 105-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           59     18    69%   60-80, 86
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-55, 60-70, 76-102, 108-146, 150-151, 159-194, 198, 208, 219-232, 239-260
src\core\database.py                                                   220     62    72%   79-88, 115-125, 138-139, 165-167, 287-318, 326-369, 376-378, 386-401, 453-501, 506-508, 513-519
src\core\employees.py                                                   89     73    18%   25-63, 67-69, 76-99, 104-120, 127-182
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 61, 72, 76, 87, 98, 103-105
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-96, 100-114
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 68-72, 77-93, 100-124, 129-140, 145-151, 156-185
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-101, 108-125, 130-183, 188-202, 207-231, 236-239
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-84, 93-109, 115-134, 140-178, 182-197, 201-223, 227-279, 283-299
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-85, 93-111, 115-135, 149-180, 184-248, 252-261, 278-282, 286-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155    155     0%   6-294
src\core\license_validator.py                                          183    183     0%   6-356
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-108, 112-143, 152-206, 215-253
src\core\lyra_sentinel.py                                               32     24    25%   22-53
src\core\notification_manager.py                                        97     58    40%   44, 52-59, 63-76, 80-84, 103-148, 152-154, 158, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                                 17      6    65%   22, 31-36
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-50, 61-85, 95-96, 114-134, 147-157
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     53    45%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 107, 114-117, 124-126, 131-134, 139-145
src\core\stats_manager.py                                               47     23    51%   40-45, 48, 52, 56-67, 71-79
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    140    20%   38-48, 52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    342     0%   1-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     18    40%   22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   19-53, 56-64, 67-83, 92-110, 119-144, 147-151, 154-168, 171-176, 179-183, 186-211, 214-219, 222-227, 230-231, 234-259, 262-267
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    113    33%   75-81, 84, 87-100, 103-124, 127, 130-132, 135-149, 152-155, 158-165, 168-171, 175, 180, 184-210, 218-227, 238-265
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-74, 77-84, 87
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   24-28, 31-114, 117-119
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-349
src\gui\dialogs\command_palette.py                                     302    302     0%   1-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 102, 105, 108, 111-136, 139-141, 144-147, 151-230
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-329
src\gui\main_window\components\status_bar.py                           158    158     0%   1-278
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-39
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-40
src\gui\main_window\main.py                                            280    280     0%   1-445
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128     21    84%   52, 97, 110-111, 121, 127, 129, 139-141, 160-161, 166-168, 180, 183-184, 187-189
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196     85    57%   84-88, 92-94, 188-194, 205, 209, 217, 226, 235, 239-242, 246-248, 252-263, 267-270, 274-290, 294-298, 302-307, 317-320, 324-337, 341, 345-360, 367-370, 374-379, 383-386
src\gui\panels\carico_ts.py                                             90     49    46%   41-43, 99, 103-108, 112-120, 124-125, 129-183
src\gui\panels\contabilita_kpi_panel.py                                379    141    63%   302, 341, 349, 448-449, 461-538, 548-609, 620-705, 715-773, 784-878
src\gui\panels\contabilita_panel.py                                    255    145    43%   49-55, 184-191, 195, 228-230, 239, 243-264, 269-293, 297-299, 303-306, 314-319, 322-335, 339-357, 360-361, 364-368, 371-388, 391-393, 396-413, 417, 420-439
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-126, 130-132, 136-146, 150-165, 170-185, 190-208, 213-227, 232-241, 245-260, 264-292, 296-302
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-89, 92-94, 98, 101-113, 116-126, 129-131, 135-141, 144-220
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     530    485     8%   53-83, 86-206, 209-314, 317-322, 326-360, 364-377, 380-408, 411-455, 459-467, 471-488, 491-518, 521-533, 536-545, 549-580, 583-616, 621-626, 629-670, 673-675, 678-714, 718-740, 744-787, 795-881, 885-896, 900-922, 926-959
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-159, 162-164, 167-169, 172-174, 177, 182-223, 228-276
src\gui\panels\dipendenti_manager_panel.py                             156    137    12%   27-69, 72, 83-95, 98-123, 126-157, 160-190, 194-223, 227-243, 247-266, 269-281, 288-315
src\gui\panels\help_panel.py                                           120     18    85%   194-203, 210-212, 214, 217-220
src\gui\panels\lyra_panel.py                                           349    165    53%   60-64, 68-86, 103-112, 409-412, 425, 429-449, 453-456, 460-464, 468-483, 491-493, 497-500, 504-507, 511-512, 518, 531-551, 557-560, 577-578, 582-599, 603-635, 643-656, 660-672, 676-687, 691-696
src\gui\panels\notifications_panel.py                                  247     60    76%   143-144, 148-150, 154-156, 160-162, 166-167, 171-172, 176, 179-183, 229, 235, 237, 239, 243, 301-302, 308-324, 342-343, 350, 352, 354, 357-358, 364-366, 382-387, 403-414
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-49, 56-108, 111-201, 205-216, 220-240, 244-250, 254-270, 274-327, 333-337, 341-353
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-76, 80-82, 85-93, 96-102, 105-115, 119-190
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-66, 69-72, 75-76, 79-84, 94-126, 131-138, 141-143
src\gui\panels\scarico_ore_panel.py                                    306    200    35%   42-44, 49-83, 238-253, 257-285, 289-291, 295-303, 307-328, 332-334, 338-356, 367-396, 400-405, 409-421, 425-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-160, 163-171, 174-177, 180-193, 196-201, 204-214, 218-226, 231-238, 241-272, 276-288, 292-314, 318-332, 336-343, 347-369, 373-375, 379-393, 397-399
src\gui\panels\scarico_ts.py                                           121     56    54%   37-39, 82-84, 103, 110, 121-123, 127-132, 146-148, 154-210
src\gui\panels\settings\main_panel.py                                  105     23    78%   130-131, 140, 145-147, 150-163, 166-182
src\gui\panels\settings\pages\diag_page.py                              32      2    94%   40-41
src\gui\panels\settings\pages\general_page.py                           43      0   100%
src\gui\panels\settings\pages\lists_page.py                            319    114    64%   214, 224, 234-243, 246-254, 261, 286-302, 305-315, 318-324, 329-338, 341-355, 358-368, 371-377, 389-392, 395-400, 403-410, 414, 417, 420, 423, 426, 429, 432, 435, 438, 441, 444, 447
src\gui\panels\settings\pages\paths_page.py                            107     22    79%   99-115, 132-133, 136, 139-141, 144-146, 149-151, 154-156, 159-161
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     33    75%   150-152, 158-160, 166-171, 174-175, 182-184, 192-195, 200-224
src\gui\panels\settings\tabs\config_tab.py                              55      1    98%   111
src\gui\panels\settings\tabs\telegram_tab.py                           136     26    81%   132-137, 140-153, 156-165, 169-173, 205-206
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-248, 252-265, 269-279, 283, 287, 291-302, 306-313, 317-324, 328-380, 384-497, 501-525
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-61, 69-109, 113-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-154, 158-174, 178-209, 212-218, 221-228, 232, 235-258, 262
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-128
src\gui\styles\widget_styles.py                                         35     35     0%   6-431
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-183, 187, 191-193, 202-210, 213-261, 266, 271-317
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-139
src\gui\widgets\audit\audit_filter_bar.py                               70      8    89%   89-95, 104-105
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   37, 45-46
src\gui\widgets\audit_log_widget.py                                    102     16    84%   119-129, 132, 135-136, 140, 168-170
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                                    486    452     7%   43-147, 151-168, 172-189, 198-327, 331-339, 343-359, 369-521, 525-534, 538-554, 563-572, 576, 580, 584-694, 698-712, 716-741, 745-749, 753-773, 777-787, 791-817, 822-847, 855-882, 890-912, 916-1021, 1025-1097
src\gui\widgets\bot_parameters.py                                      112     18    84%   81-85, 145, 149-151, 161-164, 175, 195-198
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208     57    73%   131, 186, 197-200, 220, 224-227, 231-239, 242-245, 248-251, 254-257, 260-263, 266-270, 273-284, 287-292
src\gui\widgets\contabilita\certificati_tab.py                         222     54    76%   192, 217-218, 307, 324, 352-354, 400, 406-409, 413-416, 420-430, 433-438, 441-446, 450-553
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-90, 94, 97-124, 127-134, 138, 141-157, 160-178, 182-194, 197-214, 217-233
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                                         330    232    30%   45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 309-364, 373-379, 386-410, 417-420, 423-425, 440, 446, 448, 466-467, 478-508, 517-542
src\gui\widgets\footer_stats.py                                        400    400     0%   7-693
src\gui\widgets\info_widgets.py                                         89     39    56%   26-57, 60, 80-104, 167
src\gui\widgets\message_bubble.py                                       53      6    89%   71-78
src\gui\widgets\modern_button.py                                        61     10    84%   68-69, 75-78, 82-85
src\gui\widgets\notification_card.py                                   220     94    57%   113, 217-218, 268-273, 300-314, 319-320, 327-337, 341, 359, 363-365, 379-410, 419-425, 427, 429, 435-439, 443-445, 449-450, 454-458, 463-464, 468-503, 507-511, 515-520
src\gui\widgets\notification_group_header.py                            47      9    81%   129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     13    81%   35-36, 38-39, 41-42, 58, 89-90, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106     16    85%   53, 236-237, 241-242, 247-254, 258-259, 274, 278, 282
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-261, 265-306, 311-354, 359
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-322
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     24    76%   153-155, 178-209
src\gui\widgets\status_card.py                                          59      8    86%   100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42      6    86%   63-68
src\gui\widgets\timeline_widget.py                                     191    129    32%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 173-186, 202, 205-215, 218-231, 234-239, 242-246, 276, 279, 284-309
src\gui\widgets\toast.py                                               128     49    62%   137-145, 148-152, 156-158, 162-163, 168-169, 175, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35     35     0%   1-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13     13     0%   5-35
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-54, 59-70, 75-90
src\utils\helpers.py                                                    97     65    33%   24-30, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 212-234, 243, 249-252
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22      5    77%   50, 55-58
src\utils\security.py                                                   79     18    77%   43-44, 80-82, 102, 104, 109-111, 116, 122-124, 132-137
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                20471  14227    31%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_hardening_audit_security.py::TestHardeningAuditSecurity::test_audit_deletion_integrity_break
1 failed in 6.76s

```
</details>

---
### `tests/unit/test_last_simple_boost.py::TestLastSimpleBoost::test_apply_theme_logic`
**Error:** `FAILED tests/unit/test_last_simple_boost.py::TestLastSimpleBoost::test_apply_theme_logic`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
_________________ TestLastSimpleBoost.test_apply_theme_logic __________________
tests\unit\test_last_simple_boost.py:22: in test_apply_theme_logic
    patch("src.gui.styles.get_asset_path", return_value="fake.qss"),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1437: in get_original
    raise AttributeError(
E   AttributeError: <module 'src.gui.styles' from 'C:\\Users\\Coemi\\Desktop\\SCRIPT\\ISAB_TimeSheet\\src\\gui\\styles\\__init__.py'> does not have the attribute 'get_asset_path'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                   Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------------
src\bots\__init__.py                                      20     20     0%   6-133
src\bots\base\__init__.py                                  2      2     0%   5-7
src\bots\base\base_bot.py                                241    241     0%   6-425
src\bots\base\login_page.py                               94     94     0%   6-154
src\bots\base\wait_helpers.py                            171    171     0%   14-478
src\core\__init__.py                                       2      0   100%
src\core\app_initializer.py                               90     90     0%   5-158
src\core\app_updater.py                                   46     46     0%   6-85
src\core\audit\__init__.py                                 3      0   100%
src\core\audit\database.py                                98     59    40%   59-61, 76-77, 98-142, 145-150, 153-159
src\core\audit\integrity.py                               15      0   100%
src\core\audit\manager.py                                133     54    59%   27, 37, 45, 49, 57-61, 114-118, 122-138, 151, 167-168, 171-172, 175, 178, 181-184, 192-213
src\core\audit\models.py                                   9      0   100%
src\core\audit\signals.py                                 24     18    25%   12-31
src\core\audit_manager.py                                  5      0   100%
src\core\auth_monitor.py                                  72     72     0%   6-132
src\core\backup_manager.py                               137    137     0%   6-248
src\core\bug_reporter.py                                  60     60     0%   1-119
src\core\config_manager.py                               241    152    37%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 218-236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                     90      0   100%
src\core\contabilita_manager.py                          106    106     0%   6-229
src\core\contabilita_queries.py                           87     87     0%   6-122
src\core\contabilita_search.py                            91     91     0%   6-177
src\core\contabilita_stats.py                             59     59     0%   6-99
src\core\contabilita_worker.py                           102    102     0%   1-216
src\core\data_synchronizer.py                            143    143     0%   6-260
src\core\database.py                                     220     63    71%   58, 79-88, 115-125, 138-139, 165-167, 287-318, 326-369, 376-378, 386-401, 453-501, 506-508, 513-519
src\core\employees.py                                     89     89     0%   1-186
src\core\excel_importer.py                                 4      4     0%   6-11
src\core\importers\__init__.py                            43     43     0%   1-105
src\core\importers\attivita.py                            64     64     0%   1-114
src\core\importers\base.py                                63     63     0%   1-92
src\core\importers\certificati.py                        119    119     0%   1-185
src\core\importers\contabilita.py                        140    140     0%   1-239
src\core\importers\giornaliere.py                        189    189     0%   1-299
src\core\importers\scarico_ore.py                        198    198     0%   1-314
src\core\importers\storico_oda.py                         85     85     0%   1-180
src\core\license_updater.py                              155    155     0%   6-294
src\core\license_validator.py                            183    183     0%   6-356
src\core\lyra_client.py                                  128    128     0%   6-253
src\core\lyra_sentinel.py                                 32     32     0%   6-53
src\core\notification_manager.py                          97     69    29%   30-36, 39-46, 50-59, 63-76, 80-84, 103-148, 152-154, 158, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                   17     17     0%   6-36
src\core\report_history.py                                67     67     0%   7-157
src\core\schemas.py                                       78     78     0%   1-109
src\core\secrets_manager.py                               96     60    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                 47     15    68%   40-45, 48, 61, 63, 71-79
src\core\telegram\__init__.py                              2      2     0%   1-3
src\core\telegram\service.py                             175    175     0%   1-274
src\core\telegram_bridge.py                              342    342     0%   1-482
src\core\telegram_manager.py                               2      2     0%   6-8
src\core\time_manager.py                                  19     19     0%   6-55
src\core\timesheet_processor.py                           99     99     0%   6-166
src\core\version.py                                        4      0   100%
src\gui\__init__.py                                        0      0   100%
src\gui\design\colors.py                                  27      0   100%
src\gui\design\spacing.py                                 25      0   100%
src\gui\dialogs\__init__.py                                0      0   100%
src\gui\dialogs\account_dialog.py                         51     51     0%   1-87
src\gui\dialogs\audit_detail_dialog.py                    59     59     0%   1-119
src\gui\dialogs\bug_report_dialog.py                     158    158     0%   1-349
src\gui\dialogs\command_palette.py                       302    302     0%   1-512
src\gui\dialogs\confirmation_dialog.py                    27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                   81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                        244    244     0%   6-382
src\gui\formatters.py                                    129    129     0%   1-230
src\gui\main_window\__init__.py                            2      2     0%   1-3
src\gui\main_window\components\__init__.py                 0      0   100%
src\gui\main_window\components\menu_bar.py                72     72     0%   1-329
src\gui\main_window\components\status_bar.py             158    158     0%   1-278
src\gui\main_window\components\tool_bar.py                25     25     0%   1-39
src\gui\main_window\components\tray_icon.py               16     16     0%   1-36
src\gui\main_window\controllers\__init__.py                0      0   100%
src\gui\main_window\controllers\app_event_handler.py      30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py       20     20     0%   1-40
src\gui\main_window\main.py                              280    280     0%   1-445
src\gui\main_window\page_index.py                         14     14     0%   1-18
src\gui\panels\__init__.py                                21     21     0%   6-27
src\gui\panels\base.py                                   196    196     0%   6-386
src\gui\panels\carico_ts.py                               90     90     0%   6-183
src\gui\panels\contabilita_kpi_panel.py                  379    379     0%   1-878
src\gui\panels\contabilita_panel.py                      255    255     0%   6-439
src\gui\panels\dashboard_panel.py                        168    168     0%   1-302
src\gui\panels\dettagli_oda.py                           127    127     0%   6-220
src\gui\panels\dipendenti\__init__.py                      2      2     0%   1-3
src\gui\panels\dipendenti\main_panel.py                   29     29     0%   1-62
src\gui\panels\dipendenti\shared.py                      150    150     0%   1-276
src\gui\panels\dipendenti_manager_panel.py               156    156     0%   1-315
src\gui\panels\help_panel.py                             120    120     0%   6-364
src\gui\panels\lyra_panel.py                             349    349     0%   1-696
src\gui\panels\notifications_panel.py                    247    247     0%   6-432
src\gui\panels\pdl_db.py                                 202    202     0%   6-353
src\gui\panels\prenota_bp.py                             104    104     0%   6-190
src\gui\panels\ricerca_pdl.py                             80     80     0%   6-143
src\gui\panels\scarico_ore_panel.py                      306    306     0%   7-524
src\gui\panels\scarico_pdl.py                            223    223     0%   6-399
src\gui\panels\scarico_ts.py                             121    121     0%   6-210
src\gui\panels\storico_oda_panel.py                      225    225     0%   6-525
src\gui\panels\timbrature\__init__.py                      2      2     0%   1-3
src\gui\panels\timbrature\panel.py                       148    148     0%   1-262
src\gui\panels\timbrature_bot.py                         116    116     0%   6-200
src\gui\panels\timbrature_db.py                            2      2     0%   6-8
src\gui\styles\__init__.py                                 4      0   100%
src\gui\styles\constants.py                                8      0   100%
src\gui\styles\theme_manager.py                           70     54    23%   25-28, 33, 40-50, 54-95, 100-123, 128
src\gui\styles\widget_styles.py                           35      7    80%   17, 152, 165, 382-383, 400-401
src\gui\toast.py                                          45      4    91%   87-90
src\gui\widgets\__init__.py                               12      0   100%
src\gui\widgets\activity_feed.py                         137    137     0%   1-317
src\gui\widgets\animated_progress_bar.py                  74     74     0%   7-139
src\gui\widgets\audit_log_widget.py                      102    102     0%   7-170
src\gui\widgets\automazioni_widget.py                     54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                      486    486     0%   5-1097
src\gui\widgets\bot_parameters.py                        112     89    21%   39-43, 46-108, 118-125, 129, 145, 149-151, 155-164, 169, 173-175, 179-181, 191-198, 202, 206-207
src\gui\widgets\calendar_date_edit.py                     16     11    31%   16-75
src\gui\widgets\data_table.py                            109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                           330    292    12%   29-34, 45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 280-282, 285-306, 309-364, 367-370, 373-379, 382-414, 417-420, 423-425, 428, 432-449, 458-468, 472-512, 517-542
src\gui\widgets\footer_stats.py                          400    400     0%   7-693
src\gui\widgets\info_widgets.py                           89     74    17%   26-57, 60, 67-75, 80-104, 111-161, 164, 167
src\gui\widgets\message_bubble.py                         53     53     0%   7-123
src\gui\widgets\modern_button.py                          61     11    82%   68-69, 75-78, 82-85, 146
src\gui\widgets\notification_card.py                     220    220     0%   6-520
src\gui\widgets\notification_group_header.py              47     47     0%   6-146
src\gui\widgets\notification_item.py                      70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                  106    106     0%   6-282
src\gui\widgets\priority_badge.py                         46     46     0%   6-109
src\gui\widgets\quick_actions.py                          76     76     0%   1-359
src\gui\widgets\security_dashboard.py                    143    143     0%   1-237
src\gui\widgets\sidebar_button.py                         41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                        183    183     0%   1-322
src\gui\widgets\simple_chart.py                           64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                    45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                     100    100     0%   1-211
src\gui\widgets\status_card.py                            59     47    20%   19-84, 88-91, 100-116, 120, 124-125
src\gui\widgets\status_indicator.py                       42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                       191     53    72%   77-78, 125-127, 147-151, 154-155, 158-160, 173-186, 202, 220-228, 242-246, 279, 284-309
src\gui\widgets\toast.py                                 128     98    23%   55-75, 79-118, 122-145, 148-152, 156-158, 162-163, 166-178, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                          35     35     0%   1-49
src\utils\__init__.py                                      2      0   100%
src\utils\animation_helpers.py                           100    100     0%   6-295
src\utils\date_utils.py                                   69     69     0%   6-230
src\utils\document_generator.py                           13     13     0%   5-35
src\utils\document_processor.py                           66     66     0%   6-90
src\utils\helpers.py                                      97     26    73%   28, 41-45, 78-79, 134, 147-161, 232, 243, 249-252
src\utils\log_humanizer.py                                41     14    66%   12-26, 110, 118
src\utils\parsing.py                                      53     53     0%   6-119
src\utils\printing.py                                     83     65    22%   21-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                             43     43     0%   6-82
src\utils\secure_logger.py                                22     22     0%   5-69
src\utils\security.py                                     79     18    77%   43-44, 80-82, 102, 104, 109-111, 116, 122-124, 132-137
src\utils\system_telemetry.py                             25     25     0%   6-70
src\utils\validators.py                                   73     73     0%   5-208
------------------------------------------------------------------------------------
TOTAL                                                  14995  13701     9%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_last_simple_boost.py::TestLastSimpleBoost::test_apply_theme_logic
1 failed in 6.69s

```
</details>

---
### `tests/unit/test_managers_suite.py::TestAuditManager::test_integrity_check`
**Error:** `FAILED tests/unit/test_managers_suite.py::TestAuditManager::test_integrity_check`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
____________________ TestAuditManager.test_integrity_check ____________________
tests\unit\test_managers_suite.py:46: in test_integrity_check
    assert manager.verify_integrity() is True
E   assert False is True
E    +  where False = verify_integrity()
E    +    where verify_integrity = <src.core.audit.manager.AuditManager object at 0x00000160DE67B2F0>.verify_integrity
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              241    188    22%   52-68, 74, 80, 85, 90-92, 104-108, 118-130, 134, 138, 142, 146-147, 151-152, 156-170, 174-219, 224-241, 245-247, 254-259, 263-273, 284-318, 322-347, 351-353, 357-361, 365-367, 371, 375-381, 392-404, 408-413, 425
src\bots\base\login_page.py                                             94     10    89%   89-93, 101, 127, 146-147, 150-151
src\bots\base\wait_helpers.py                                          171    171     0%   14-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-92, 96-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   38-41, 45, 49-55, 66-91, 102-115, 119-148, 152-162, 186-283, 287-305, 315-341, 345-354, 358-367, 371-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-140, 144-166, 170-198, 202-211, 215-240, 244-276, 282-311, 315-324, 328-343, 347-367, 371-384
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-84, 88-149, 153-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-76, 80-81, 88-111, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 289-322, 325-363, 367-384, 391-392
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-156, 160-164, 168-193, 197-226, 230-238, 242-279, 283-311, 315-327, 331-359, 363-405, 409-425, 429-450, 454-466, 473-512, 515-560, 564-583
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     90     0%   5-158
src\core\app_updater.py                                                 46     37    20%   17-45, 50-55, 60-81, 85
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              98     39    60%   59-61, 76-77, 106-108, 110-113, 115-118, 120-122, 124-128, 140-141, 145-150, 153-159
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              133     51    62%   45, 49, 57-61, 114-118, 122-138, 151, 165-168, 178, 181-184, 192-213
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               24     10    58%   21-30
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     63    12%   17, 24-58, 68-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-187, 198-206, 211-222, 227-248
src\core\bug_reporter.py                                                60     45    25%   32-102, 107-119
src\core\config_manager.py                                             241    150    38%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 218-236, 250-251, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     56    47%   29, 34, 39, 48-60, 77-131, 140-147, 156-161, 170-177, 187, 192, 197, 202, 207, 216, 224
src\core\contabilita_queries.py                                         87     45    48%   20, 29-30, 36, 45-46, 52, 73-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           59     18    69%   60-80, 86
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-55, 60-70, 76-102, 108-146, 150-151, 159-194, 198, 208, 219-232, 239-260
src\core\database.py                                                   220    143    35%   67-69, 77-88, 95-125, 129-133, 136-139, 142, 148-167, 175-236, 241-245, 253-272, 277-279, 287-318, 326-369, 376-378, 386-401, 406-446, 453-501, 506-508, 513-519, 526-536, 541-558
src\core\employees.py                                                   89     73    18%   25-63, 67-69, 76-99, 104-120, 127-182
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 61, 72, 76, 87, 98, 103-105
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-96, 100-114
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 68-72, 77-93, 100-124, 129-140, 145-151, 156-185
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-101, 108-125, 130-183, 188-202, 207-231, 236-239
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-84, 93-109, 115-134, 140-178, 182-197, 201-223, 227-279, 283-299
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-85, 93-111, 115-135, 149-180, 184-248, 252-261, 278-282, 286-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155     22    86%   98-101, 148, 163-164, 194-195, 200-202, 209, 226, 248-250, 285-287, 291-294
src\core\license_validator.py                                          183     13    93%   96-111, 133, 160, 177-181
src\core\lyra_client.py                                                128     20    84%   22, 67-69, 83, 107-108, 115, 142-143, 197-198, 202-206, 243, 251-253
src\core\lyra_sentinel.py                                               32      4    88%   38-39, 50-51
src\core\notification_manager.py                                        97     57    41%   44, 52-59, 63-76, 80-84, 103-148, 152-154, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                                 17      6    65%   22, 31-36
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-50, 61-85, 95-96, 114-134, 147-157
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     39    59%   33, 38, 43, 48-51, 57-58, 66-72, 78, 86, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47      7    85%   43-45, 48, 61, 63, 76
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    129    26%   52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    278    19%   47-65, 69-72, 76-80, 84-88, 91-111, 114-133, 136-139, 143-158, 161-171, 174-177, 180-181, 184-190, 193-199, 202-223, 227-250, 253-257, 260-265, 269-284, 287-293, 296-309, 312-325, 329-334, 338-344, 348-354, 358-384, 388-401, 405-412, 415-421, 424-447, 450-462, 465-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19      5    74%   30, 33-36, 55
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187    167    11%   19-53, 56-64, 67-83, 92-110, 119-144, 147-151, 154-168, 171-176, 179-183, 186-211, 214-219, 222-227, 230-231, 234-259, 262-267
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-132, 135-149, 152-155, 158-165, 168-171, 174-176, 179-181, 184-210, 213-230, 233-235, 238-265
src\gui\controllers\bot_controller.py                                   38     20    47%   36-39, 46-59, 63-71
src\gui\controllers\command_registry.py                                 37     11    70%   43, 47-49, 62-64, 67, 70-71, 74
src\gui\controllers\navigation_controller.py                           154     78    49%   54-57, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 158-164, 176-182, 199-204, 212-217, 225-230, 235-236, 240-243, 254-256, 260-261, 265-266, 294-303, 307-308
src\gui\controllers\search_controller.py                               197    177    10%   18-44, 48-50, 54-70, 74-84, 88-97, 101-110, 114-123, 127-141, 145-189, 193-236, 240-282, 286-305
src\gui\controllers\service_controller.py                              211    196     7%   18-30, 38-53, 61-123, 130-160, 164-340, 352-355, 372-380, 393-434, 447-463, 467, 471-480
src\gui\controllers\tray_controller.py                                  38      8    79%   37-38, 50-55, 59
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-74, 77-84, 87
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   24-28, 31-114, 117-119
src\gui\dialogs\bug_report_dialog.py                                   158    139    12%   31-32, 35-42, 49-53, 56-125, 128-147, 150-172, 176-328, 332-349
src\gui\dialogs\command_palette.py                                     302    274     9%   39-68, 72-183, 187-213, 216-224, 227-233, 236-241, 244-251, 254-289, 293-302, 305-312, 315-321, 324-330, 334-338, 342-354, 358-369, 372-379, 382-386, 389-433, 436-472, 476-492, 495-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 102, 105, 108, 111-136, 139-141, 144-147, 151-230
src\gui\main_window\__init__.py                                          2      0   100%
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     40    44%   26-32, 52-63, 68-77, 81-329
src\gui\main_window\components\status_bar.py                           158    107    32%   115-128, 132-144, 148-207, 211-278
src\gui\main_window\components\tool_bar.py                              25      0   100%
src\gui\main_window\components\tray_icon.py                             16      7    56%   18, 27-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     16    47%   15-16, 25-34, 37-38, 42, 46-52
src\gui\main_window\controllers\signal_connector.py                     20      1    95%   34
src\gui\main_window\main.py                                            280    144    49%   99-133, 190, 193, 199, 202, 205, 208, 211, 215-241, 244, 247-266, 269-273, 281-285, 293-297, 303-307, 313-315, 318-320, 323-325, 333-335, 338-342, 345-356, 359-361, 364-380, 383-386, 389-392, 395-399, 402-404, 407-410, 413, 416, 419-420, 429, 433, 437, 441, 445
src\gui\main_window\page_index.py                                       14      0   100%
src\gui\models\audit_model.py                                          128    104    19%   28-31, 40-42, 45, 48, 51-75, 79-97, 101-111, 115-122, 126-130, 134-142, 146-148, 151-153, 156-161, 164-168, 172-184, 187-189
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    108    45%   51-55, 59-72, 84-88, 92-94, 186-197, 205, 209, 217, 226, 230-235, 239-242, 246-248, 252-263, 267-270, 274-290, 294-298, 302-307, 317-320, 324-337, 341, 345-360, 367-370, 374-379, 383-386
src\gui\panels\carico_ts.py                                             90     54    40%   39-43, 96-99, 103-108, 112-120, 124-125, 129-183
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-240, 250-291, 295-309, 313-331, 335, 339-449, 453-538, 541-609, 613-705, 708-773, 777-878
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-180, 184-191, 195, 199, 223-239, 243-264, 269-293, 297-299, 303-306, 310-335, 339-357, 360-361, 364-368, 371-388, 391-393, 396-413, 417, 420-439
src\gui\panels\dashboard_panel.py                                      168     98    42%   84, 130-132, 136-146, 150-165, 170-185, 190-208, 213-227, 232-241, 245-260, 264-292, 296-302
src\gui\panels\dettagli_oda.py                                         127     80    37%   37-41, 92-94, 98, 101-113, 116-126, 129-131, 135-141, 144-220
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     530    485     8%   53-83, 86-206, 209-314, 317-322, 326-360, 364-377, 380-408, 411-455, 459-467, 471-488, 491-518, 521-533, 536-545, 549-580, 583-616, 621-626, 629-670, 673-675, 678-714, 718-740, 744-787, 795-881, 885-896, 900-922, 926-959
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-159, 162-164, 167-169, 172-174, 177, 182-223, 228-276
src\gui\panels\dipendenti_manager_panel.py                             156    137    12%   27-69, 72, 83-95, 98-123, 126-157, 160-190, 194-223, 227-243, 247-266, 269-281, 288-315
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-167, 171-191, 194-203, 206-214, 217-220, 223, 243, 263, 275, 289, 300, 313, 325, 336, 346, 356, 364
src\gui\panels\lyra_panel.py                                           349    303    13%   60-64, 68-86, 98-99, 103-112, 124-132, 136-400, 407-420, 424-425, 429-449, 453-456, 460-464, 468-483, 491-493, 497-500, 504-507, 511-512, 516-521, 531-551, 557-560, 564-578, 582-599, 603-635, 643-656, 660-672, 676-687, 691-696
src\gui\panels\notifications_panel.py                                  247    201    19%   56-69, 72-140, 143-144, 148-150, 154-156, 160-162, 166-167, 171-172, 176, 179-183, 188-223, 228-251, 255-281, 289-297, 301-302, 306-324, 328-360, 364-366, 370-389, 393-432
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-49, 56-108, 111-201, 205-216, 220-240, 244-250, 254-270, 274-327, 333-337, 341-353
src\gui\panels\prenota_bp.py                                           104     63    39%   34-37, 80-82, 85-93, 96-102, 105-115, 119-190
src\gui\panels\ricerca_pdl.py                                           80     43    46%   69-72, 75-76, 79-84, 94-126, 131-138, 141-143
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   42-44, 49-83, 94-101, 105-234, 238-253, 257-285, 289-291, 295-303, 307-328, 332-334, 338-356, 367-396, 400-405, 409-421, 425-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          223    139    38%   51-55, 92, 163-171, 174-177, 180-193, 196-201, 204-214, 218-226, 231-238, 241-272, 276-288, 292-314, 318-332, 336-343, 347-369, 373-375, 379-393, 397-399
src\gui\panels\scarico_ts.py                                           121     74    39%   35-39, 82-84, 88, 92-105, 109-117, 121-123, 127-132, 146-148, 154-210
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-182
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-36, 40-41, 44, 47
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-74
src\gui\panels\settings\pages\lists_page.py                            319    268    16%   32-33, 36-62, 67-84, 87-104, 107-126, 129-148, 151-170, 173-192, 197-203, 206-207, 214, 224, 234-243, 246-254, 259-262, 265-272, 275-283, 286-302, 305-315, 318-324, 329-338, 341-355, 358-368, 371-377, 382-383, 386, 389-392, 395-400, 403-410, 414, 417, 420, 423, 426, 429, 432, 435, 438, 441, 444, 447, 452-457, 460-465
src\gui\panels\settings\pages\paths_page.py                            107     86    20%   26-27, 30-68, 71-90, 94-115, 132-133, 136, 139-141, 144-146, 149-151, 154-156, 159-161, 166-181, 184-189
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 98-100
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-104, 111, 114-116, 119-121
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-129, 132-137, 140-153, 156-165, 169-173, 181-191, 195-208
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-248, 252-265, 269-279, 283, 287, 291-302, 306-313, 317-324, 328-380, 384-497, 501-525
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-61, 69-109, 113-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-154, 158-174, 178-209, 212-218, 221-228, 232, 235-258, 262
src\gui\panels\timbrature_bot.py                                       116     83    28%   38-42, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      0   100%
src\gui\styles\constants.py                                              8      0   100%
src\gui\styles\theme_manager.py                                         70      5    93%   106-107, 110, 119-120
src\gui\styles\widget_styles.py                                         35      7    80%   17, 152, 165, 382-383, 400-401
src\gui\toast.py                                                        45      4    91%   87-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137     26    81%   39-40, 88-90, 149-150, 170-180, 187, 191-193, 266, 272, 283, 285, 294-310
src\gui\widgets\animated_progress_bar.py                                74     53    28%   45-46, 50, 54-55, 59-60, 65-79, 83-139
src\gui\widgets\audit\audit_filter_bar.py                               70     57    19%   21-25, 28-81, 84-86, 89-95, 104-105, 108-117
src\gui\widgets\audit\audit_pagination_bar.py                           34     26    24%   10-11, 14-32, 35-42, 45-46
src\gui\widgets\audit_log_widget.py                                    102     80    22%   38-50, 53-112, 115-116, 119-129, 132, 135-136, 139-155, 158-165, 168-170
src\gui\widgets\automazioni_widget.py                                   54      2    96%   122-123
src\gui\widgets\autopilot_widget.py                                    486    228    53%   43-147, 151-168, 172-189, 343-359, 538-554, 698-712, 716-741, 745-749, 753-773, 777-787, 791-817, 822-847, 855-882, 890-912, 926, 943-944, 956-957, 969-970, 982-984, 1017-1021, 1030-1036, 1040
src\gui\widgets\bot_parameters.py                                      112     26    77%   145, 149-151, 161-164, 169, 173-175, 179-181, 191-198, 202, 206-207
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-167, 170-181, 184-192, 195-200, 203-221, 224-227, 231-239, 242-245, 248-251, 254-257, 260-263, 266-270, 273-284, 287-292
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-296, 305-330, 336-373, 378-389, 393-402, 406-409, 413-416, 420-430, 433-438, 441-446, 450-553
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-90, 94, 97-124, 127-134, 138, 141-157, 160-178, 182-194, 197-214, 217-233
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                                         330    252    24%   45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 309-364, 373-379, 408, 417-420, 423-425, 432-449, 458-468, 472-512, 517-542
src\gui\widgets\footer_stats.py                                        400     95    76%   30-43, 46, 71-79, 83, 87, 104-107, 110-111, 115, 134-136, 139-140, 144-147, 150-151, 155, 265-276, 280-285, 305, 310, 320-324, 328, 516, 529-530, 541, 557-559, 571, 589-590, 629-631, 635-641, 645-648, 664-668, 675-684, 688, 692-693
src\gui\widgets\info_widgets.py                                         89     74    17%   26-57, 60, 67-75, 80-104, 111-161, 164, 167
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        61     11    82%   68-69, 75-78, 82-85, 146
src\gui\widgets\notification_card.py                                   220    189    14%   86-92, 96-341, 345-355, 359, 363-365, 379-410, 414-431, 435-439, 443-445, 449-450, 454-458, 463-464, 468-503, 507-511, 515-520
src\gui\widgets\notification_group_header.py                            47     36    23%   34-40, 44-125, 129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106     80    25%   36-48, 52-67, 71-73, 77-81, 85-104, 136-142, 146-231, 236-237, 241-242, 247-254, 258-259, 268-270, 274, 278, 282
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     11    86%   265-306, 336
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41      4    90%   47-51
src\gui\widgets\sidebar_widget.py                                      183     20    89%   53-56, 69, 77, 120-122, 126-128, 132-135, 274, 283-284, 308-309
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     33    27%   24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-107, 110-142, 146-148, 152-163, 169-211
src\gui\widgets\status_card.py                                          59     12    80%   88-91, 100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    129    32%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 173-186, 202, 205-215, 218-231, 234-239, 242-246, 276, 279, 284-309
src\gui\widgets\toast.py                                               128     98    23%   55-75, 79-118, 122-145, 148-152, 156-158, 162-163, 166-178, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35      7    80%   41-44, 47-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13     10    23%   11-35
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-54, 59-70, 75-90
src\utils\helpers.py                                                    97     61    37%   24-30, 45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 212-234, 249-252
src\utils\log_humanizer.py                                              41      5    88%   16, 20, 25-26, 110
src\utils\parsing.py                                                    53     21    60%   14, 17, 21, 32-33, 45-46, 60, 62, 66, 71-79, 86, 95, 102-119
src\utils\printing.py                                                   83     65    22%   21-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-141
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     51    30%   34-52, 57-68, 73-88, 94-179, 184-200, 205-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                21146  14893    30%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_managers_suite.py::TestAuditManager::test_integrity_check
1 failed in 5.02s

```
</details>

---
### `tests/unit/test_notifications_panel_deep.py::TestNotificationsPanelDeep::test_audit_log_widget_refresh`
**Error:** `FAILED tests/unit/test_notifications_panel_deep.py::TestNotificationsPanelDeep::test_audit_log_widget_refresh`

<details><summary>Full Output</summary>

```text
F                                                                        [100%]
================================== FAILURES ===================================
__________ TestNotificationsPanelDeep.test_audit_log_widget_refresh ___________
tests\unit\test_notifications_panel_deep.py:114: in test_audit_log_widget_refresh
    with patch("src.gui.panels.notifications_panel.AuditManager.instance") as mock_audit:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\unittest\mock.py:1451: in __enter__
    self.target = self.getter()
                  ^^^^^^^^^^^^^
C:\Program Files\Python312\Lib\pkgutil.py:528: in resolve_name
    result = getattr(result, p)
             ^^^^^^^^^^^^^^^^^^
E   AttributeError: module 'src.gui.panels.notifications_panel' has no attribute 'AuditManager'
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              241    188    22%   52-68, 74, 80, 85, 90-92, 104-108, 118-130, 134, 138, 142, 146-147, 151-152, 156-170, 174-219, 224-241, 245-247, 254-259, 263-273, 284-318, 322-347, 351-353, 357-361, 365-367, 371, 375-381, 392-404, 408-413, 425
src\bots\base\login_page.py                                             94     78    17%   34-37, 43-53, 57-77, 81-93, 97-103, 110-154
src\bots\base\wait_helpers.py                                          171    171     0%   14-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-92, 96-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   38-41, 45, 49-55, 66-91, 102-115, 119-148, 152-162, 186-283, 287-305, 315-341, 345-354, 358-367, 371-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225    189    16%   39, 44, 49, 56, 60, 72-75, 79-81, 85-100, 104-121, 125-140, 144-166, 170-198, 202-211, 215-240, 244-276, 282-311, 315-324, 328-343, 347-367, 371-384
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-84, 88-149, 153-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    165    13%   42-43, 47-76, 80-81, 88-111, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 289-322, 325-363, 367-384, 391-392
src\bots\safework\base.py                                               41     27    34%   20-48, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    356    11%   26, 31, 36, 41, 46, 57-60, 64, 68-93, 97-156, 160-164, 168-193, 197-226, 230-238, 242-279, 283-311, 315-327, 331-359, 363-405, 409-425, 429-450, 454-466, 473-512, 515-560, 564-583
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     90     0%   5-158
src\core\app_updater.py                                                 46     46     0%   6-85
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              98     28    71%   59-61, 76-77, 115-118, 120-122, 124-128, 140-141, 149-150, 153-159
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              133     47    65%   49, 57-61, 114-118, 122-138, 151, 167-168, 181-184, 192-213
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               24     10    58%   21-30
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137    104    24%   35-50, 55-61, 66-72, 77-85, 90-96, 101-129, 134-187, 198-206, 211-222, 227-248
src\core\bug_reporter.py                                                60     60     0%   1-119
src\core\config_manager.py                                             241    198    18%   35, 67, 75-90, 95-121, 126-127, 132-152, 157-174, 183-184, 192-204, 209-210, 215-236, 241-251, 256-257, 262-264, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 372-374, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     58    45%   29, 34, 39, 48-60, 77-131, 140-147, 156-161, 170-177, 182, 187, 192, 197, 202, 207, 216, 224, 229
src\core\contabilita_queries.py                                         87     68    22%   21-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     72    21%   25-81, 88-112, 117-123, 128-140, 147-159, 173-177
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-55, 60-70, 76-102, 108-146, 150-151, 159-194, 198, 208, 219-232, 239-260
src\core\database.py                                                   220    155    30%   56-91, 95-125, 129-133, 136-139, 142, 148-167, 175-236, 241-245, 253-272, 277-279, 287-318, 326-369, 376-378, 386-401, 406-446, 453-501, 506-508, 513-519, 526-536, 541-558
src\core\employees.py                                                   89     73    18%   25-63, 67-69, 76-99, 104-120, 127-182
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 61, 72, 76, 87, 98, 103-105
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-96, 100-114
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 68-72, 77-93, 100-124, 129-140, 145-151, 156-185
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-101, 108-125, 130-183, 188-202, 207-231, 236-239
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-84, 93-109, 115-134, 140-178, 182-197, 201-223, 227-279, 283-299
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-85, 93-111, 115-135, 149-180, 184-248, 252-261, 278-282, 286-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155    155     0%   6-294
src\core\license_validator.py                                          183    183     0%   6-356
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-108, 112-143, 152-206, 215-253
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97      9    91%   44, 83-84, 135-148
src\core\oda_manager.py                                                 17      6    65%   22, 31-36
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-50, 61-85, 95-96, 114-134, 147-157
src\core\schemas.py                                                     78     27    65%   67-72, 77-88, 93-95, 100-102, 107-109
src\core\secrets_manager.py                                             96     60    38%   31-51, 55-59, 63-73, 77-79, 83-87, 92, 97, 102-107, 112-117, 122-126, 131-134, 139-145
src\core\stats_manager.py                                               47      7    85%   43-45, 48, 61, 63, 76
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    140    20%   38-48, 52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    342     0%   1-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     19     0%   6-55
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     92    15%   22-24, 28-102, 105-120, 123-141, 144-156, 159-167, 170-175, 178-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     21    30%   17-19, 22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187     71    62%   70, 74, 81-82, 105-108, 140-143, 147-151, 171-176, 179-183, 186-211, 214-219, 222-227, 230-231, 237, 247, 255, 259, 262-267
src\gui\components\scarico_ore\filters\popup_list.py                    91     11    88%   57, 65, 101, 104-105, 123-128
src\gui\components\scarico_ore\model.py                                169    139    18%   58-84, 87-100, 103-124, 127, 130-132, 135-149, 152-155, 158-165, 168-171, 174-176, 179-181, 184-210, 213-230, 233-235, 238-265
src\gui\controllers\navigation_controller.py                           154     56    64%   97-100, 103-106, 109-112, 115-118, 121-124, 127-130, 133-136, 139-142, 145-148, 151-154, 199-204, 212-217, 225-230, 260-261, 265-266, 294-303
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51     43    16%   18-74, 77-84, 87
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   24-28, 31-114, 117-119
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-349
src\gui\dialogs\command_palette.py                                     302    302     0%   1-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129    113    12%   12-27, 37-68, 73, 85-91, 95-98, 102, 105, 108, 111-136, 139-141, 144-147, 151-230
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-329
src\gui\main_window\components\status_bar.py                           158    158     0%   1-278
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-39
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-40
src\gui\main_window\main.py                                            280    280     0%   1-445
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128     23    82%   52, 97, 110-111, 121, 127, 129, 139-141, 160-161, 166-168, 176, 178, 180, 183-184, 187-189
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 119-127, 131-175, 182, 186-197, 201, 205, 209, 217, 226, 230-235, 239-242, 246-248, 252-263, 267-270, 274-290, 294-298, 302-307, 317-320, 324-337, 341, 345-360, 367-370, 374-379, 383-386
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-108, 112-120, 124-125, 129-183
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-240, 250-291, 295-309, 313-331, 335, 339-449, 453-538, 541-609, 613-705, 708-773, 777-878
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-180, 184-191, 195, 199, 223-239, 243-264, 269-293, 297-299, 303-306, 310-335, 339-357, 360-361, 364-368, 371-388, 391-393, 396-413, 417, 420-439
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-126, 130-132, 136-146, 150-165, 170-185, 190-208, 213-227, 232-241, 245-260, 264-292, 296-302
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-89, 92-94, 98, 101-113, 116-126, 129-131, 135-141, 144-220
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     530    485     8%   53-83, 86-206, 209-314, 317-322, 326-360, 364-377, 380-408, 411-455, 459-467, 471-488, 491-518, 521-533, 536-545, 549-580, 583-616, 621-626, 629-670, 673-675, 678-714, 718-740, 744-787, 795-881, 885-896, 900-922, 926-959
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-159, 162-164, 167-169, 172-174, 177, 182-223, 228-276
src\gui\panels\dipendenti_manager_panel.py                             156    137    12%   27-69, 72, 83-95, 98-123, 126-157, 160-190, 194-223, 227-243, 247-266, 269-281, 288-315
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-167, 171-191, 194-203, 206-214, 217-220, 223, 243, 263, 275, 289, 300, 313, 325, 336, 346, 356, 364
src\gui\panels\lyra_panel.py                                           349    303    13%   60-64, 68-86, 98-99, 103-112, 124-132, 136-400, 407-420, 424-425, 429-449, 453-456, 460-464, 468-483, 491-493, 497-500, 504-507, 511-512, 516-521, 531-551, 557-560, 564-578, 582-599, 603-635, 643-656, 660-672, 676-687, 691-696
src\gui\panels\notifications_panel.py                                  247     46    81%   143-144, 148-150, 160-162, 176, 229, 235, 237, 239, 243, 301-302, 308-324, 342-343, 351-356, 364-366, 403-414
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-49, 56-108, 111-201, 205-216, 220-240, 244-250, 254-270, 274-327, 333-337, 341-353
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-76, 80-82, 85-93, 96-102, 105-115, 119-190
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-66, 69-72, 75-76, 79-84, 94-126, 131-138, 141-143
src\gui\panels\scarico_ore_panel.py                                    306    270    12%   42-44, 49-83, 94-101, 105-234, 238-253, 257-285, 289-291, 295-303, 307-328, 332-334, 338-356, 367-396, 400-405, 409-421, 425-434, 438-439, 443-451, 455-469, 473-492, 496-499, 503-524
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-160, 163-171, 174-177, 180-193, 196-201, 204-214, 218-226, 231-238, 241-272, 276-288, 292-314, 318-332, 336-343, 347-369, 373-375, 379-393, 397-399
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-78, 82-84, 88, 92-105, 109-117, 121-123, 127-132, 146-148, 154-210
src\gui\panels\settings\main_panel.py                                  105     80    24%   23-34, 37-99, 102-103, 107-109, 113-131, 134-137, 140, 145-147, 150-163, 166-182
src\gui\panels\settings\pages\diag_page.py                              32     21    34%   13-14, 17-36, 40-41, 44, 47
src\gui\panels\settings\pages\general_page.py                           43     34    21%   20-21, 24-64, 68-69, 73-74
src\gui\panels\settings\pages\lists_page.py                            319    268    16%   32-33, 36-62, 67-84, 87-104, 107-126, 129-148, 151-170, 173-192, 197-203, 206-207, 214, 224, 234-243, 246-254, 259-262, 265-272, 275-283, 286-302, 305-315, 318-324, 329-338, 341-355, 358-368, 371-377, 382-383, 386, 389-392, 395-400, 403-410, 414, 417, 420, 423, 426, 429, 432, 435, 438, 441, 444, 447, 452-457, 460-465
src\gui\panels\settings\pages\paths_page.py                            107     86    20%   26-27, 30-68, 71-90, 94-115, 132-133, 136, 139-141, 144-146, 149-151, 154-156, 159-161, 166-181, 184-189
src\gui\panels\settings\shared.py                                       16      9    44%   7-25, 30, 57, 78, 98-100
src\gui\panels\settings\tabs\backup_tab.py                             133    115    14%   31-32, 35-145, 148-155, 158-160, 163, 166-171, 174-175, 178-197, 200-224
src\gui\panels\settings\tabs\config_tab.py                              55     40    27%   25-27, 30-104, 111, 114-116, 119-121
src\gui\panels\settings\tabs\telegram_tab.py                           136    117    14%   28-29, 32-129, 132-137, 140-153, 156-165, 169-173, 181-191, 195-208
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-248, 252-265, 269-279, 283, 287, 291-302, 306-313, 317-324, 328-380, 384-497, 501-525
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-61, 69-109, 113-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-154, 158-174, 178-209, 212-218, 221-228, 232, 235-258, 262
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-128
src\gui\styles\widget_styles.py                                         35     35     0%   6-431
src\gui\toast.py                                                        45     45     0%   6-90
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-183, 187, 191-193, 202-210, 213-261, 266, 271-317
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-139
src\gui\widgets\audit\audit_filter_bar.py                               70      8    89%   89-95, 104-105
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   37, 45-46
src\gui\widgets\audit_log_widget.py                                    102     16    84%   119-129, 132, 135-136, 140, 168-170
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                                    486    452     7%   43-147, 151-168, 172-189, 198-327, 331-339, 343-359, 369-521, 525-534, 538-554, 563-572, 576, 580, 584-694, 698-712, 716-741, 745-749, 753-773, 777-787, 791-817, 822-847, 855-882, 890-912, 916-1021, 1025-1097
src\gui\widgets\bot_parameters.py                                      112     89    21%   39-43, 46-108, 118-125, 129, 145, 149-151, 155-164, 169, 173-175, 179-181, 191-198, 202, 206-207
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-167, 170-181, 184-192, 195-200, 203-221, 224-227, 231-239, 242-245, 248-251, 254-257, 260-263, 266-270, 273-284, 287-292
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-296, 305-330, 336-373, 378-389, 393-402, 406-409, 413-416, 420-430, 433-438, 441-446, 450-553
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-90, 94, 97-124, 127-134, 138, 141-157, 160-178, 182-194, 197-214, 217-233
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                                         330    292    12%   29-34, 45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 280-282, 285-306, 309-364, 367-370, 373-379, 382-414, 417-420, 423-425, 428, 432-449, 458-468, 472-512, 517-542
src\gui\widgets\footer_stats.py                                        400    400     0%   7-693
src\gui\widgets\info_widgets.py                                         89     74    17%   26-57, 60, 67-75, 80-104, 111-161, 164, 167
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        61     12    80%   52-54, 68-69, 75-78, 82-85
src\gui\widgets\notification_card.py                                   220     90    59%   113, 268-273, 300-314, 319-320, 327-337, 341, 359, 363-365, 379-410, 424-431, 435-439, 443-445, 449-450, 454-458, 463-464, 468-503, 507-511, 515-520
src\gui\widgets\notification_group_header.py                            47      9    81%   129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106      9    92%   236-237, 241-242, 258-259, 274, 278, 282
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-261, 265-306, 311-354, 359
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-322
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     85    15%   26-27, 30-107, 110-142, 146-148, 152-163, 169-211
src\gui\widgets\status_card.py                                          59     47    20%   19-84, 88-91, 100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42     35    17%   18-32, 42-59, 63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 165-170, 173-186, 191-198, 202, 205-215, 218-231, 234-239, 242-246, 257-273, 276, 279, 284-309
src\gui\widgets\toast.py                                               128     98    23%   55-75, 79-118, 122-145, 148-152, 156-158, 162-163, 166-178, 189-191, 201-227, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35     35     0%   1-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13     13     0%   5-35
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-54, 59-70, 75-90
src\utils\helpers.py                                                    97     65    33%   24-30, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 212-234, 243, 249-252
src\utils\log_humanizer.py                                              41     30    27%   12-26, 81-89, 94-111, 116-119
src\utils\parsing.py                                                    53     46    13%   13-33, 39-51, 56-66, 71-79, 84-97, 102-119
src\utils\printing.py                                                   83     68    18%   18-23, 28-39, 47-51, 62-141
src\utils\resource_manager.py                                           43     43     0%   6-82
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79     79     0%   6-141
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                20625  16378    21%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_notifications_panel_deep.py::TestNotificationsPanelDeep::test_audit_log_widget_refresh
1 failed in 12.31s

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
tests\unit\test_sprint_a_audit_backup.py:29: in test_audit_integrity_chain
    assert audit_mgr.verify_integrity() is True
E   assert False is True
E    +  where False = verify_integrity()
E    +    where verify_integrity = <src.core.audit.manager.AuditManager object at 0x000001931810C770>.verify_integrity
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.12.10-final-0 _______________

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
src\bots\__init__.py                                                    20      7    65%   99, 112, 126-130
src\bots\base\__init__.py                                                2      0   100%
src\bots\base\base_bot.py                                              241    160    34%   74, 80, 85, 90-92, 107, 119, 124-130, 134, 138, 142, 156-170, 174-219, 224-241, 245-247, 254-259, 263-273, 284-318, 322-347, 351-353, 358-360, 365-367, 371, 375-381, 392-404, 408-413, 425
src\bots\base\login_page.py                                             94     78    17%   34-37, 43-53, 57-77, 81-93, 97-103, 110-154
src\bots\base\wait_helpers.py                                          171    171     0%   14-478
src\bots\portale_fornitori\carico_ts\__init__.py                         2      0   100%
src\bots\portale_fornitori\carico_ts\bot.py                             48     31    35%   20, 25, 31, 52, 56, 60-72, 77-101
src\bots\portale_fornitori\carico_ts\locators.py                         6      0   100%
src\bots\portale_fornitori\carico_ts\pages\carico_ts_page.py            54     40    26%   28-30, 34-36, 42-49, 60-73, 84-108
src\bots\portale_fornitori\common\locators.py                           12      0   100%
src\bots\portale_fornitori\dettagli_oda\__init__.py                      2      0   100%
src\bots\portale_fornitori\dettagli_oda\bot.py                          81     59    27%   21, 26, 31, 38, 42, 51-54, 60-67, 71-92, 96-107, 118-136, 140-145
src\bots\portale_fornitori\dettagli_oda\locators.py                     19      0   100%
src\bots\portale_fornitori\dettagli_oda\pages\dettagli_oda_page.py     212    184    13%   38-41, 45, 49-55, 66-91, 102-115, 119-148, 152-162, 186-283, 287-305, 315-341, 345-354, 358-367, 371-384
src\bots\portale_fornitori\prenota_bp\__init__.py                        1      0   100%
src\bots\portale_fornitori\prenota_bp\bot.py                            86     70    19%   19, 26, 30, 42-51, 56-63, 67-93, 97-102, 106-131
src\bots\portale_fornitori\prenota_bp\locators.py                       33      0   100%
src\bots\portale_fornitori\prenota_bp\pages\prenota_bp_page.py         228    201    12%   27-30, 34, 38-42, 54-79, 90-95, 100-107, 111-141, 145-178, 182-190, 199-227, 231-238, 242-264, 268-280, 284-298, 302-320, 324-350, 354-358
src\bots\portale_fornitori\scarico_ts\__init__.py                        2      0   100%
src\bots\portale_fornitori\scarico_ts\bot.py                           225     49    78%   39, 44, 49, 60, 79-81, 92, 98, 108, 119-121, 155, 163-164, 171, 210, 216, 225-236, 245, 283, 290-291, 298, 304-307, 316, 322-324, 333, 342-343, 362-365, 381-384
src\bots\portale_fornitori\scarico_ts\locators.py                       10      0   100%
src\bots\portale_fornitori\scarico_ts\pages\scarico_ts_page.py         104     20    81%   43-44, 63-65, 89-91, 122-124, 134-135, 143-145, 154, 164-166
src\bots\portale_fornitori\scarico_ts\scarico_ts_bot.py                 59     14    76%   24, 29, 34, 41, 45, 59, 61-62, 67-68, 77, 81, 95-96
src\bots\portale_fornitori\timbrature\__init__.py                        2      0   100%
src\bots\portale_fornitori\timbrature\bot.py                            75     55    27%   21, 26, 31, 36, 39-43, 47-63, 69-113, 120-121
src\bots\portale_fornitori\timbrature\locators.py                       11      0   100%
src\bots\portale_fornitori\timbrature\pages\timbrature_page.py         163    141    13%   34-38, 41, 45-60, 67-84, 88-149, 153-207, 212-238, 242-253, 258-293
src\bots\portale_fornitori\timbrature\storage.py                       189    141    25%   90, 109-110, 117-149, 159-171, 181-189, 192-220, 227-266, 269-284, 289-322, 325-363, 367-384, 391-392
src\bots\safework\base.py                                               41     19    54%   21, 27-28, 44-45, 52-68, 72, 76
src\bots\safework\pdl\__init__.py                                        0      0   100%
src\bots\safework\pdl\bot.py                                           400    138    66%   26, 31, 36, 46, 64, 75-76, 86, 89-90, 97-156, 186-187, 199-200, 243, 252-254, 265-266, 272-275, 284, 295-297, 309-311, 318-323, 332, 346-348, 358-359, 364, 369-396, 403-405, 410, 422-425, 445-446, 449-450, 465-466, 474, 484-485, 492-494, 505-510, 516, 530-531, 552-554, 557-558
src\core\__init__.py                                                     2      0   100%
src\core\app_initializer.py                                             90     90     0%   5-158
src\core\app_updater.py                                                 46     37    20%   17-45, 50-55, 60-81, 85
src\core\audit\__init__.py                                               3      0   100%
src\core\audit\database.py                                              98     28    71%   59-61, 76-77, 115-118, 120-122, 124-128, 140-141, 149-150, 153-159
src\core\audit\integrity.py                                             15      0   100%
src\core\audit\manager.py                                              133     52    61%   45, 49, 57-61, 114-118, 122-138, 151, 165-168, 171-172, 181-184, 192-213
src\core\audit\models.py                                                 9      0   100%
src\core\audit\signals.py                                               24     10    58%   21-30
src\core\audit_manager.py                                                5      0   100%
src\core\auth_monitor.py                                                72     72     0%   6-132
src\core\backup_manager.py                                             137     34    75%   42, 48, 59-61, 68, 71, 85, 93, 95, 108-110, 115, 120-125, 174-187, 214, 220-222, 236-248
src\core\bug_reporter.py                                                60     60     0%   1-119
src\core\config_manager.py                                             241    149    38%   35, 87, 97-102, 113-119, 135-152, 160-174, 183-184, 203-204, 218-236, 250-251, 256-257, 269, 274-289, 294-307, 312-322, 331-358, 363-367, 379-381, 386-391, 400-419, 427-470
src\core\constants.py                                                   90      0   100%
src\core\contabilita_manager.py                                        106     56    47%   29, 34, 39, 48-60, 77-131, 140-147, 156-161, 170-177, 182, 187, 192, 197, 202, 207, 229
src\core\contabilita_queries.py                                         87     70    20%   19-30, 35-46, 51-74, 79-90, 95-106, 111-122
src\core\contabilita_search.py                                          91     14    85%   26-27, 50, 78-79, 109-110, 119, 122-123, 132-133, 151-152
src\core\contabilita_stats.py                                           59     38    36%   31-51, 56-80, 85-99
src\core\contabilita_worker.py                                         102     84    18%   23-28, 32-63, 67-77, 96-122, 126-147, 152-160, 170-178, 188-196, 199-207, 210-216
src\core\data_synchronizer.py                                          143    114    20%   19-23, 28-31, 38-55, 60-70, 76-102, 108-146, 150-151, 159-194, 198, 208, 219-232, 239-260
src\core\database.py                                                   220    140    36%   77-88, 95-125, 129-133, 136-139, 142, 148-167, 175-236, 241-245, 253-272, 277-279, 287-318, 326-369, 376-378, 386-401, 406-446, 453-501, 506-508, 513-519, 526-536, 541-558
src\core\employees.py                                                   89     73    18%   25-63, 67-69, 76-99, 104-120, 127-182
src\core\excel_importer.py                                               4      0   100%
src\core\importers\__init__.py                                          43     10    77%   32, 49, 61, 72, 76, 87, 98, 103-105
src\core\importers\attivita.py                                          64     48    25%   41-58, 62-76, 80-96, 100-114
src\core\importers\base.py                                              63     42    33%   14-15, 22-24, 34-36, 41-59, 64-80, 85-92
src\core\importers\certificati.py                                      119     95    20%   35-54, 59-63, 68-72, 77-93, 100-124, 129-140, 145-151, 156-185
src\core\importers\contabilita.py                                      140    116    17%   37-54, 65-101, 108-125, 130-183, 188-202, 207-231, 236-239
src\core\importers\giornaliere.py                                      189    157    17%   36-56, 66-84, 93-109, 115-134, 140-178, 182-197, 201-223, 227-279, 283-299
src\core\importers\scarico_ore.py                                      198    167    16%   11-12, 18-20, 45-85, 93-111, 115-135, 149-180, 184-248, 252-261, 278-282, 286-314
src\core\importers\storico_oda.py                                       85     65    24%   57-84, 89-95, 100-117, 122, 127-161, 166-180
src\core\license_updater.py                                            155    102    34%   75, 80, 85-101, 106-148, 153-195, 200-202, 207-213, 226, 234-235, 248-250, 267-271, 274, 279-287, 291-294
src\core\license_validator.py                                          183    146    20%   38-42, 49-58, 64-111, 117-133, 138-145, 159-183, 193-219, 230-231, 240-264, 269-287, 292-340, 345-348, 353-356
src\core\lyra_client.py                                                128    113    12%   21-37, 55-69, 73-76, 80-108, 112-143, 152-206, 215-253
src\core\lyra_sentinel.py                                               32     32     0%   6-53
src\core\notification_manager.py                                        97     56    42%   44, 52-59, 63-76, 80-84, 103-148, 153, 158, 162-169, 173-182, 186-189, 193-196
src\core\oda_manager.py                                                 17      6    65%   22, 31-36
src\core\report_history.py                                              67     44    34%   26-28, 36-41, 46-50, 61-85, 95-96, 114-134, 147-157
src\core\schemas.py                                                     78     25    68%   67-72, 77-88, 94, 100-102, 107-109
src\core\secrets_manager.py                                             96      8    92%   48-51, 124-126, 133-134
src\core\stats_manager.py                                               47     15    68%   40-45, 48, 61, 63, 71-79
src\core\telegram\__init__.py                                            2      0   100%
src\core\telegram\handlers\callbacks.py                                187    165    12%   14-31, 35-43, 47-48, 52-54, 58-95, 103-129, 137-145, 149-245, 249-252, 260-276, 280-283, 287-300, 304-322, 326-334, 338-347
src\core\telegram\handlers\commands.py                                  47     39    17%   13-33, 51-72, 80-83, 91-95
src\core\telegram\handlers\messages.py                                  98     84    14%   17-40, 45-52, 57-61, 66-84, 92-101, 109-119, 127-162
src\core\telegram\service.py                                           175    140    20%   38-48, 52-67, 71-78, 82, 86-98, 101, 105-127, 130-143, 147-157, 165-171, 180-190, 194-204, 207-218, 221-232, 235-245, 248-259, 262-274
src\core\telegram\ui\keyboards.py                                       98     52    47%   10, 26, 31-36, 41-47, 52-64, 69-77, 82-86, 91, 96-106, 111-128, 133-142, 147-156, 161, 171, 182-187, 192-197, 202-203, 214-221, 226-231, 236-244, 249-254, 259-263
src\core\telegram_bridge.py                                            342    342     0%   1-482
src\core\telegram_manager.py                                             2      0   100%
src\core\time_manager.py                                                19     14    26%   21-36, 49-55
src\core\timesheet_processor.py                                         99     77    22%   26-66, 71-81, 86-91, 96-106, 112-146, 151-159, 164-166
src\core\version.py                                                      4      0   100%
src\gui\__init__.py                                                      0      0   100%
src\gui\components\scarico_ore\__init__.py                               6      0   100%
src\gui\components\scarico_ore\cache.py                                108     55    49%   28-102, 105-120, 145, 153-156, 174-175, 182-183, 186-191
src\gui\components\scarico_ore\filters\header.py                        30     18    40%   22-25, 29-51
src\gui\components\scarico_ore\filters\popup_date.py                   187     43    77%   70, 74, 81-82, 108, 143, 151, 171-176, 186-211, 230-231, 237, 262-267
src\gui\components\scarico_ore\filters\popup_list.py                    91     79    13%   21-73, 76-82, 85-90, 93-98, 101, 104-105, 108-120, 123-128
src\gui\components\scarico_ore\model.py                                169     54    68%   84, 87-100, 127, 153, 161-165, 169, 185, 189, 197-210, 221-227, 238-265
src\gui\controllers\search_controller.py                               197     69    65%   59, 83-84, 89, 102, 115, 130, 140-141, 154-189, 202-236, 249-282, 296, 304-305
src\gui\controllers\service_controller.py                              211    142    33%   115, 133-160, 164-340, 352-355, 374-375, 394-395, 413-414, 420-427, 447-463
src\gui\design\colors.py                                                27      0   100%
src\gui\design\spacing.py                                               25      0   100%
src\gui\dialogs\__init__.py                                              0      0   100%
src\gui\dialogs\account_dialog.py                                       51      4    92%   82-84, 87
src\gui\dialogs\audit_detail_dialog.py                                  59     47    20%   24-28, 31-114, 117-119
src\gui\dialogs\bug_report_dialog.py                                   158    158     0%   1-349
src\gui\dialogs\command_palette.py                                     302    302     0%   1-512
src\gui\dialogs\confirmation_dialog.py                                  27     27     0%   1-72
src\gui\dialogs\quick_actions_config.py                                 81     81     0%   1-207
src\gui\dialogs\startup_dialog.py                                      244    244     0%   6-382
src\gui\formatters.py                                                  129     92    29%   12-27, 37-68, 73, 95-98, 102, 118-120, 126, 130, 134, 140, 144-147, 151-230
src\gui\layouts\responsive.py                                           64     10    84%   33-39, 73, 78, 96-97
src\gui\main_window\__init__.py                                          2      2     0%   1-3
src\gui\main_window\components\__init__.py                               0      0   100%
src\gui\main_window\components\menu_bar.py                              72     72     0%   1-329
src\gui\main_window\components\status_bar.py                           158    158     0%   1-278
src\gui\main_window\components\tool_bar.py                              25     25     0%   1-39
src\gui\main_window\components\tray_icon.py                             16     16     0%   1-36
src\gui\main_window\controllers\__init__.py                              0      0   100%
src\gui\main_window\controllers\app_event_handler.py                    30     30     0%   1-52
src\gui\main_window\controllers\signal_connector.py                     20     20     0%   1-40
src\gui\main_window\main.py                                            280    280     0%   1-445
src\gui\main_window\page_index.py                                       14     14     0%   1-18
src\gui\models\audit_model.py                                          128     23    82%   52, 97, 110-111, 121, 127, 129, 139-141, 160-161, 166-168, 176, 178, 180, 183-184, 187-189
src\gui\panels\__init__.py                                              21      0   100%
src\gui\panels\base.py                                                 196    142    28%   51-55, 59-72, 84-88, 92-94, 119-127, 131-175, 182, 186-197, 201, 205, 209, 217, 226, 230-235, 239-242, 246-248, 252-263, 267-270, 274-290, 294-298, 302-307, 317-320, 324-337, 341, 345-360, 367-370, 374-379, 383-386
src\gui\panels\carico_ts.py                                             90     70    22%   28-36, 39-43, 48-92, 96-99, 103-108, 112-120, 124-125, 129-183
src\gui\panels\contabilita_kpi_panel.py                                379    352     7%   41-50, 53-240, 250-291, 295-309, 313-331, 335, 339-449, 453-538, 541-609, 613-705, 708-773, 777-878
src\gui\panels\contabilita_panel.py                                    255    221    13%   38-45, 49-55, 59-180, 184-191, 195, 199, 223-239, 243-264, 269-293, 297-299, 303-306, 310-335, 339-357, 360-361, 364-368, 371-388, 391-393, 396-413, 417, 420-439
src\gui\panels\dashboard_panel.py                                      168    147    12%   25-80, 84, 88-95, 99-126, 130-132, 136-146, 150-165, 170-185, 190-208, 213-227, 232-241, 245-260, 264-292, 296-302
src\gui\panels\dettagli_oda.py                                         127    104    18%   26-34, 37-41, 45-89, 92-94, 98, 101-113, 116-126, 129-131, 135-141, 144-220
src\gui\panels\dipendenti\__init__.py                                    2      0   100%
src\gui\panels\dipendenti\main_panel.py                                 29     18    38%   20-21, 24-50, 55-62
src\gui\panels\dipendenti\pages\anagrafica_page.py                     530    485     8%   53-83, 86-206, 209-314, 317-322, 326-360, 364-377, 380-408, 411-455, 459-467, 471-488, 491-518, 521-533, 536-545, 549-580, 583-616, 621-626, 629-670, 673-675, 678-714, 718-740, 744-787, 795-881, 885-896, 900-922, 926-959
src\gui\panels\dipendenti\shared.py                                    150    134    11%   24-71, 80-159, 162-164, 167-169, 172-174, 177, 182-223, 228-276
src\gui\panels\dipendenti_manager_panel.py                             156    137    12%   27-69, 72, 83-95, 98-123, 126-157, 160-190, 194-223, 227-243, 247-266, 269-281, 288-315
src\gui\panels\help_panel.py                                           120     96    20%   32-35, 38-167, 171-191, 194-203, 206-214, 217-220, 223, 243, 263, 275, 289, 300, 313, 325, 336, 346, 356, 364
src\gui\panels\lyra_panel.py                                           349    303    13%   60-64, 68-86, 98-99, 103-112, 124-132, 136-400, 407-420, 424-425, 429-449, 453-456, 460-464, 468-483, 491-493, 497-500, 504-507, 511-512, 516-521, 531-551, 557-560, 564-578, 582-599, 603-635, 643-656, 660-672, 676-687, 691-696
src\gui\panels\notifications_panel.py                                  247     46    81%   143-144, 148-150, 160-162, 176, 229, 235, 237, 239, 243, 301-302, 308-324, 342-343, 351-356, 364-366, 403-414
src\gui\panels\pdl_db.py                                               202    181    10%   37-38, 41-49, 56-108, 111-201, 205-216, 220-240, 244-250, 254-270, 274-327, 333-337, 341-353
src\gui\panels\prenota_bp.py                                           104     86    17%   23-31, 34-37, 41-76, 80-82, 85-93, 96-102, 105-115, 119-190
src\gui\panels\ricerca_pdl.py                                           80     65    19%   29-36, 39-66, 69-72, 75-76, 79-84, 94-126, 131-138, 141-143
src\gui\panels\scarico_ore_panel.py                                    306    102    67%   42-44, 49-83, 244-253, 260-285, 303, 310-311, 327-328, 332-334, 338-356, 378-379, 389-390, 395-396, 400-405, 413-414, 429-431, 444, 455-469, 496-499, 506
src\gui\panels\scarico_pdl.py                                          223    191    14%   40-48, 51-55, 59-160, 163-171, 174-177, 180-193, 196-201, 204-214, 218-226, 231-238, 241-272, 276-288, 292-314, 318-332, 336-343, 347-369, 373-375, 379-393, 397-399
src\gui\panels\scarico_ts.py                                           121     99    18%   24-32, 35-39, 43-78, 82-84, 88, 92-105, 109-117, 121-123, 127-132, 146-148, 154-210
src\gui\panels\settings\main_panel.py                                  105     23    78%   103, 130-131, 145-147, 150-163, 166-182
src\gui\panels\settings\pages\diag_page.py                              32      0   100%
src\gui\panels\settings\pages\general_page.py                           43      0   100%
src\gui\panels\settings\pages\lists_page.py                            319    109    66%   214, 224, 234-243, 246-254, 261, 286-302, 305-315, 318-324, 329-338, 341-355, 358-368, 371-377, 395-400, 403-410, 414, 417, 420, 426, 429, 432, 435, 438, 441, 444, 447
src\gui\panels\settings\pages\paths_page.py                            107     19    82%   101, 132-133, 136, 139-141, 144-146, 149-151, 154-156, 159-161
src\gui\panels\settings\shared.py                                       16      0   100%
src\gui\panels\settings\tabs\backup_tab.py                             133     29    78%   150-152, 158-160, 171, 174-175, 182-184, 192-195, 200-224
src\gui\panels\settings\tabs\config_tab.py                              55      1    98%   111
src\gui\panels\settings\tabs\telegram_tab.py                           136     26    81%   132-137, 140-153, 156-165, 169-173, 205-206
src\gui\panels\storico_oda_panel.py                                    225    199    12%   41-42, 46-92, 99-160, 163-248, 252-265, 269-279, 283, 287, 291-302, 306-313, 317-324, 328-380, 384-497, 501-525
src\gui\panels\timbrature\__init__.py                                    2      0   100%
src\gui\panels\timbrature\components\detail_view.py                     63     54    14%   13-36, 39-61, 69-109, 113-131, 135-136
src\gui\panels\timbrature\components\settings_tab.py                    94     81    14%   26-31, 34-74, 78-99, 103-132, 135-142, 145-146, 151-153
src\gui\panels\timbrature\panel.py                                     148    124    16%   38-48, 51-83, 86-117, 120-154, 158-174, 178-209, 212-218, 221-228, 232, 235-258, 262
src\gui\panels\timbrature_bot.py                                       116     94    19%   26-35, 38-42, 46-55, 60-62, 66-67, 70-81, 85-94, 98-103, 108-195, 198-200
src\gui\panels\timbrature_db.py                                          2      0   100%
src\gui\styles\__init__.py                                               4      4     0%   6-45
src\gui\styles\constants.py                                              8      8     0%   9-156
src\gui\styles\theme_manager.py                                         70     70     0%   6-128
src\gui\styles\widget_styles.py                                         35     35     0%   6-431
src\gui\toast.py                                                        45      0   100%
src\gui\widgets\__init__.py                                             12      0   100%
src\gui\widgets\activity_feed.py                                       137    119    13%   29-183, 187, 191-193, 202-210, 213-261, 266, 271-317
src\gui\widgets\animated_progress_bar.py                                74     74     0%   7-139
src\gui\widgets\audit\audit_filter_bar.py                               70      8    89%   89-95, 104-105
src\gui\widgets\audit\audit_pagination_bar.py                           34      3    91%   37, 45-46
src\gui\widgets\audit_log_widget.py                                    102     16    84%   119-129, 132, 135-136, 140, 168-170
src\gui\widgets\automazioni_widget.py                                   54     54     0%   1-131
src\gui\widgets\autopilot_widget.py                                    486    452     7%   43-147, 151-168, 172-189, 198-327, 331-339, 343-359, 369-521, 525-534, 538-554, 563-572, 576, 580, 584-694, 698-712, 716-741, 745-749, 753-773, 777-787, 791-817, 822-847, 855-882, 890-912, 916-1021, 1025-1097
src\gui\widgets\bot_parameters.py                                      112     89    21%   39-43, 46-108, 118-125, 129, 145, 149-151, 155-164, 169, 173-175, 179-181, 191-198, 202, 206-207
src\gui\widgets\calendar_date_edit.py                                   16      0   100%
src\gui\widgets\contabilita\attivita_tab.py                            208    176    15%   52-54, 58-128, 131, 134-149, 153-167, 170-181, 184-192, 195-200, 203-221, 224-227, 231-239, 242-245, 248-251, 254-257, 260-263, 266-270, 273-284, 287-292
src\gui\widgets\contabilita\certificati_tab.py                         222    192    14%   57-59, 62-188, 192, 196-296, 305-330, 336-373, 378-389, 393-402, 406-409, 413-416, 420-430, 433-438, 441-446, 450-553
src\gui\widgets\contabilita\giornaliere_tab.py                         166    138    17%   44-47, 51-90, 94, 97-124, 127-134, 138, 141-157, 160-178, 182-194, 197-214, 217-233
src\gui\widgets\contabilita\helpers.py                                  33     26    21%   11-31, 34-39, 42-47
src\gui\widgets\contabilita\year_tab.py                                 69     56    19%   38-54, 57-95, 99, 103-124, 128-157, 161
src\gui\widgets\data_table.py                                          109     86    21%   46-50, 53-123, 127, 131-132, 135-160, 163-169, 173-181, 184-186, 190-207, 211, 215
src\gui\widgets\excel_table.py                                         330    292    12%   29-34, 45-58, 62-69, 73-90, 94-114, 117-118, 121-122, 126-137, 141-163, 167-189, 193-210, 214-234, 238-249, 252-257, 260-264, 267-271, 280-282, 285-306, 309-364, 367-370, 373-379, 382-414, 417-420, 423-425, 428, 432-449, 458-468, 472-512, 517-542
src\gui\widgets\footer_stats.py                                        400    400     0%   7-693
src\gui\widgets\info_widgets.py                                         89     74    17%   26-57, 60, 67-75, 80-104, 111-161, 164, 167
src\gui\widgets\message_bubble.py                                       53     46    13%   38-40, 43-123
src\gui\widgets\modern_button.py                                        61     12    80%   52-54, 68-69, 75-78, 82-85
src\gui\widgets\notification_card.py                                   220     90    59%   113, 268-273, 300-314, 319-320, 327-337, 341, 359, 363-365, 379-410, 424-431, 435-439, 443-445, 449-450, 454-458, 463-464, 468-503, 507-511, 515-520
src\gui\widgets\notification_group_header.py                            47      9    81%   129-132, 136-137, 141, 145-146
src\gui\widgets\notification_item.py                                    70     59    16%   20-23, 26-123, 127-129, 132
src\gui\widgets\notification_toolbar.py                                106      9    92%   236-237, 241-242, 258-259, 274, 278, 282
src\gui\widgets\priority_badge.py                                       46     34    26%   30-37, 41-78, 82-90, 94-97, 101, 105-107
src\gui\widgets\quick_actions.py                                        76     61    20%   22-30, 234-235, 238-261, 265-306, 311-354, 359
src\gui\widgets\security_dashboard.py                                  143    143     0%   1-237
src\gui\widgets\sidebar_button.py                                       41     41     0%   1-89
src\gui\widgets\sidebar_widget.py                                      183    183     0%   1-322
src\gui\widgets\simple_chart.py                                         64     64     0%   1-103
src\gui\widgets\sortable_table_item.py                                  45     37    18%   19-24, 28-61, 66-79, 83-96
src\gui\widgets\statistics_widget.py                                   100     24    76%   153-155, 178-209
src\gui\widgets\status_card.py                                          59     47    20%   19-84, 88-91, 100-116, 120, 124-125
src\gui\widgets\status_indicator.py                                     42      6    86%   63-68
src\gui\widgets\timeline_widget.py                                     191    155    19%   44-69, 72-79, 82-115, 118-131, 134-139, 142-151, 154-155, 158-160, 165-170, 173-186, 191-198, 202, 205-215, 218-231, 234-239, 242-246, 257-273, 276, 279, 284-309
src\gui\widgets\toast.py                                               128     34    73%   137-145, 148-152, 156-158, 162-163, 168-169, 175, 206-213, 221, 232, 237, 242, 247
src\gui\widgets\update_banner.py                                        35     35     0%   1-49
src\utils\__init__.py                                                    2      0   100%
src\utils\animation_helpers.py                                         100    100     0%   6-295
src\utils\date_utils.py                                                 69     69     0%   6-230
src\utils\document_generator.py                                         13     13     0%   5-35
src\utils\document_processor.py                                         66     50    24%   15-16, 25-34, 39-54, 59-70, 75-90
src\utils\helpers.py                                                    97     58    40%   24-30, 41-45, 59-81, 94-96, 101, 128-129, 134, 147-161, 175-177, 192-198, 213, 232, 243, 249-252
src\utils\log_humanizer.py                                              41     15    63%   12-26, 86, 110-111
src\utils\parsing.py                                                    53      4    92%   102-119
src\utils\printing.py                                                   83     14    83%   21-23, 37-39, 50-51, 113-116, 140-141
src\utils\resource_manager.py                                           43     10    77%   22-36, 55
src\utils\secure_logger.py                                              22     10    55%   45-52, 55-58
src\utils\security.py                                                   79      5    94%   43-44, 80-82
src\utils\system_telemetry.py                                           25     25     0%   6-70
src\utils\validators.py                                                 73     73     0%   5-208
--------------------------------------------------------------------------------------------------
TOTAL                                                                21116  14569    31%
Coverage HTML written to dir htmlcov
=========================== short test summary info ===========================
FAILED tests/unit/test_sprint_a_audit_backup.py::TestSprintAAuditBackup::test_audit_integrity_chain
1 failed in 5.22s

```
</details>

---
