from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.telegram_manager import TelegramService


class TestTelegramDeepDive:
    @pytest.fixture
    def service(self):
        return TelegramService()

    @pytest.mark.asyncio
    async def test_all_nav_menus(self, service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()

        menus = ["menu_main", "nav_bots", "nav_db", "nav_lyra", "nav_utility", "nav_portale", "nav_safework"]
        for menu in menus:
            await service._handle_nav_actions(menu, mock_query)
            assert mock_query.edit_message_text.called

    @pytest.mark.asyncio
    async def test_db_actions_flow(self, service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()

        # Test year selection for strumentale
        with patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2023, 2024]):
            await service._handle_db_actions("db_select_year_strumentale", mock_query, "123")
            assert "Seleziona Anno" in mock_query.edit_message_text.call_args[0][0]

    @pytest.mark.asyncio
    async def test_bot_actions_menus(self, service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()

        # Test various bot menus
        bot_menus = ["menu_pdl", "menu_ts", "menu_oda_details", "menu_carico", "menu_timbrature"]
        for m in bot_menus:
            await service._handle_bot_actions(m, mock_query, "123", MagicMock(), MagicMock())
            assert mock_query.edit_message_text.called

    @pytest.mark.asyncio
    async def test_utility_actions_complex(self, service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()

        # Test settings and power menus
        await service._handle_utility_actions("menu_power", mock_query, "123")
        assert "Manutenzione" in mock_query.edit_message_text.call_args[0][0]

        with patch("src.core.config_manager.load_config", return_value={"fornitori": ["F1"]}):
            await service._handle_utility_actions("menu_settings", mock_query, "123")
            assert "Impostazioni" in mock_query.edit_message_text.call_args[0][0]
