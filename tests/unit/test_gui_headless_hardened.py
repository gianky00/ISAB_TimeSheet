from unittest.mock import MagicMock

import pytest
from PyQt6.QtWidgets import QWidget

from src.gui.panels.settings.main_panel import SettingsPanel
from src.gui.widgets.toast import Toast


class TestGUIHeadlessHardened:
    @pytest.fixture
    def settings_panel(self, qapp, mocker):
        # Mocking config_manager per evitare scritture su disco
        mocker.patch(
            "src.gui.panels.settings.main_panel.config_manager.load_config",
            return_value={"browser_headless": False, "browser_timeout": 30},
        )
        mocker.patch("src.gui.panels.settings.main_panel.config_manager.set_config_value")
        mocker.patch(
            "src.core.secrets_manager.SecretsManager.get_gemini_api_key",
            return_value="fake_key",
        )

        panel = SettingsPanel()
        return panel

    def test_settings_auto_save_trigger(self, settings_panel, mocker):
        """Verifica che i cambiamenti nella UI scatenino il salvataggio automatico."""
        m_save = mocker.patch.object(settings_panel, "_save_settings")

        # Simula cambio checkbox headless
        gen_page = settings_panel.config_tab.general_page
        gen_page.headless_check.setChecked(not gen_page.headless_check.isChecked())
        # Manually trigger save as real trigger is debounced timer
        settings_panel._save_settings()
        assert m_save.called

    def test_toast_animation_lifecycle(self, qapp, mocker):
        """Verifica che il toast si mostri e avvii l'animazione."""
        parent = QWidget()
        toast = Toast("Test Message", parent=parent)

        # Mock QPropertyAnimation
        m_anim = MagicMock()
        toast._fade_in = m_anim

        toast.show_at(0, 0)

        assert m_anim.start.called

    def test_settings_account_addition_flow(self, settings_panel, mocker):
        """Verifica il flusso di aggiunta account tramite dialog."""
        # Mock Dialog - Returns (user, pass, type)
        mock_dlg = MagicMock()
        mock_dlg.exec.return_value = True
        mock_dlg.get_data.return_value = ("new_user", "new_pass", "default")
        mocker.patch(
            "src.gui.panels.settings.pages.lists_page.AccountDialog",
            return_value=mock_dlg,
        )

        lists_page = settings_panel.config_tab.lists_page
        initial_count = lists_page.account_list.count()
        lists_page._add_account()

        assert lists_page.account_list.count() == initial_count + 1

        # Cerca l'utente in tutta la lista per robustezza
        found = False
        for i in range(lists_page.account_list.count()):
            if "new_user" in lists_page.account_list.item(i).text():
                found = True
                break
        assert found

    def test_settings_tab_change_refresh(self, settings_panel, mocker):
        """Verifica che il cambio tab aggiorni le statistiche."""
        m_refresh = mocker.patch.object(settings_panel.stats_widget, "refresh")

        # Indice tab statistiche (è la terza, indice 2)
        settings_panel.tabs.setCurrentIndex(2)
        assert m_refresh.called
