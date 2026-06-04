from telegram import InlineKeyboardMarkup

from src.api.telegram.ui.keyboards import TelegramUI


class TestTelegramUI:
    def test_get_main_keyboard(self):
        kb = TelegramUI.get_main_keyboard()
        assert isinstance(kb, InlineKeyboardMarkup)
        assert len(kb.inline_keyboard) == 2

    def test_get_back_keyboard(self):
        kb = TelegramUI.get_back_keyboard("test_cb")
        assert kb.inline_keyboard[0][0].callback_data == "test_cb"

    def test_get_db_year_selection(self):
        years = [2024, 2023, 2022, 2021]
        kb = TelegramUI.get_db_year_selection(years)
        # COLS_PER_ROW = 3, so 2 rows of years + 1 back row
        assert len(kb.inline_keyboard) == 3
        assert kb.inline_keyboard[0][0].text == "2024"

    def test_get_pdl_menu(self):
        kb_on = TelegramUI.get_pdl_menu(True)
        assert "✅" in kb_on.inline_keyboard[2][0].text

        kb_off = TelegramUI.get_pdl_menu(False)
        assert "❌" in kb_off.inline_keyboard[2][0].text

    def test_get_printer_selection_menu(self):
        printers = ["P1", "P2"]
        kb = TelegramUI.get_printer_selection_menu(printers, "back")
        assert len(kb.inline_keyboard) == 3  # 2 printers + 1 back
        assert "P1" in kb.inline_keyboard[0][0].text

    def test_get_confirm_merge_menu(self):
        kb = TelegramUI.get_confirm_merge_menu(noprint=True)
        assert "_noprint" in kb.inline_keyboard[0][0].callback_data

        kb_p = TelegramUI.get_confirm_merge_menu(noprint=False)
        assert "_print" in kb_p.inline_keyboard[0][0].callback_data

    def test_get_settings_menu(self):
        fornitori = ["F1", "F2"]
        kb = TelegramUI.get_settings_menu(fornitori)
        assert "F1" in kb.inline_keyboard[0][0].text
        assert "Autopilot" in kb.inline_keyboard[2][0].text
