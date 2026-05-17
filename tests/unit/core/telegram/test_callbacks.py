from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.telegram.handlers.callbacks import handle_button


class TestTelegramCallbacks:
    @pytest.fixture
    def service(self):
        s = MagicMock()
        s.connected_chat_id = "123"
        s.user_states = {}
        s.pdl_settings = {}
        s._check_auth = AsyncMock(return_value=True)
        return s

    @pytest.fixture
    def update(self):
        u = MagicMock()
        u.effective_chat.id = 123
        u.effective_user.id = 123
        u.callback_query = AsyncMock()
        u.callback_query.data = ""
        u.callback_query.message = MagicMock()
        return u

    @pytest.mark.asyncio
    async def test_handle_button_nav_main(self, service, update):
        update.callback_query.data = "menu_main"
        await handle_button(service, update, MagicMock())
        assert "Command Center" in update.callback_query.edit_message_text.call_args[0][0]

    @pytest.mark.asyncio
    async def test_handle_button_db_select_year(self, service, update):
        update.callback_query.data = "db_select_year_strumentale"
        with patch(
            "src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2024]
        ):
            await handle_button(service, update, MagicMock())
            assert "Seleziona Anno" in update.callback_query.edit_message_text.call_args[0][0]

    @pytest.mark.asyncio
    async def test_handle_button_bot_menu_ts(self, service, update):
        update.callback_query.data = "menu_ts"
        await handle_button(service, update, MagicMock())
        assert "Portale TS" in update.callback_query.edit_message_text.call_args[0][0]

    @pytest.mark.asyncio
    async def test_handle_button_direct_run(self, service, update):
        update.callback_query.data = "run_ts"
        await handle_button(service, update, MagicMock())
        assert service.command_received.emit.called
        assert service.command_received.emit.call_args[0][0] == "run_ts"

    @pytest.mark.asyncio
    async def test_handle_button_input_pdl(self, service, update):
        update.callback_query.data = "input_pdl"
        await handle_button(service, update, MagicMock())
        assert service.user_states[123] == "WAITING_PDL"
        assert "[INPUT]" in update.callback_query.edit_message_text.call_args[0][0]

    @pytest.mark.asyncio
    async def test_handle_button_utility_status(self, service, update):
        update.callback_query.data = "status"
        await handle_button(service, update, MagicMock())
        assert service.status_requested.emit.called

    @pytest.mark.asyncio
    async def test_handle_button_wrong_user(self, service, update):
        update.effective_user.id = 999
        update.callback_query.data = "menu_main"
        await handle_button(service, update, MagicMock())
        assert not update.callback_query.edit_message_text.called

    @pytest.mark.asyncio
    async def test_handle_button_toggle_merge_all_pdl(self, service, update):
        update.callback_query.data = "toggle_merge_all_pdl"
        await handle_button(service, update, MagicMock())
        # Toggles from False to True
        assert service.pdl_settings[123]["merge_all"] is True

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "nav_data,expected_text",
        [
            ("nav_bots", "Seleziona Piattaforma"),
            ("nav_db", "Seleziona Database"),
            ("nav_lyra", "Lyra AI Assistant"),
            ("nav_utility", "Utility & Stato"),
            ("nav_portale", "Portale Fornitori"),
            ("nav_safework", "SafeWork"),
        ],
    )
    async def test_handle_button_nav_menus(self, service, update, nav_data, expected_text):
        update.callback_query.data = nav_data
        await handle_button(service, update, MagicMock())
        assert expected_text in update.callback_query.edit_message_text.call_args[0][0]

    @pytest.mark.asyncio
    async def test_handle_button_db_info(self, service, update):
        update.callback_query.data = "db_info_pdl"
        await handle_button(service, update, MagicMock())
        assert service.user_states[123] == "WAITING_DB_QUERY_PDL"
        assert "DB Pdl" in update.callback_query.edit_message_text.call_args[0][0]

    @pytest.mark.asyncio
    async def test_handle_button_utility_screenshot(self, service, update):
        update.callback_query.data = "screenshot"
        await handle_button(service, update, MagicMock())
        assert "Screenshot:" in update.callback_query.edit_message_text.call_args[0][0]

    @pytest.mark.asyncio
    async def test_handle_button_snap_app(self, service, update):
        update.callback_query.data = "snap_app"
        await handle_button(service, update, MagicMock())
        assert service.screenshot_requested.emit.called
        assert service.screenshot_requested.emit.call_args[0][0] == "app"
