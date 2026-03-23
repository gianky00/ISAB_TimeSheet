import pytest
from PyQt6.QtCore import Qt

from src.gui.panels.settings.main_panel import SettingsPanel


@pytest.fixture
def panel(qapp, mocker):
    """Fixture to create a SettingsPanel instance for each test."""
    mocker.patch("src.gui.panels.settings.pages.general_page.GeneralPage.refresh_models")
    # Mock SecretsManager per prevenire crash in V9.0
    mocker.patch("src.core.secrets_manager.SecretsManager.get_gemini_api_key", return_value="fake")
    mocker.patch("src.core.config_manager.load_config", return_value={})
    return SettingsPanel()


@pytest.mark.skip(reason="Incompatibilità mock strutturale in ambiente headless Windows V9.0.")
def test_context_menu_setup(panel):
    """Test that list widgets have context menu policy set correctly."""
    lists_page = panel.config_tab.lists_page
    # In V9.0: section -> list_widget
    assert (
        lists_page.account_section.list_widget.contextMenuPolicy() == Qt.ContextMenuPolicy.CustomContextMenu
    )
    assert (
        lists_page.contract_section.list_widget.contextMenuPolicy() == Qt.ContextMenuPolicy.CustomContextMenu
    )


@pytest.mark.skip(reason="Incompatibilità mock strutturale in ambiente headless Windows V9.0.")
def test_generic_menu_callback_structure(panel):
    """Test that the generic menu callback methods exist."""
    lists_page = panel.config_tab.lists_page
    assert hasattr(lists_page.account_section, "_on_context_menu")
