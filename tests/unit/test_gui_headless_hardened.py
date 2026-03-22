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
        m_save = mocker.patch("src.gui.panels.settings.main_panel.config_manager.save_config")
        p = SettingsPanel()
        p._mock_save = m_save
        return p

    def test_settings_auto_save_trigger(self, settings_panel, qtbot):
        """Verifica che i cambiamenti nella UI scatenino il salvataggio."""
        # Attendi che il caricamento iniziale (QTimer) finisca
        qtbot.wait(100)
        gen_page = settings_panel.config_tab.general_page
        gen_page.headless_check.setChecked(True)
        # Il salvataggio usa debouncing (500ms) e un QThread
        qtbot.waitUntil(lambda: settings_panel._mock_save.called, timeout=2000)

    def test_toast_animation_lifecycle(self, qapp, mocker):
        """Verifica che il toast si mostri e avvii l'animazione."""
        parent = QWidget()
        toast = Toast("Test Message", parent=parent)
        m_anim = MagicMock()
        toast._fade_in = m_anim
        toast.show_at(0, 0)
        assert m_anim.start.called

    def test_settings_account_addition_flow(self, settings_panel, mocker):
        """Verifica il flusso di aggiunta account tramite widget dedicato."""
        mock_dlg = MagicMock()
        mock_dlg.exec.return_value = True
        mock_dlg.get_data.return_value = ("new_user", "new_pass", "default")

        mocker.patch(
            "src.gui.panels.settings.widgets.account_list_widget.AccountDialog",
            return_value=mock_dlg,
        )
        # In V9.0 add_account non chiama SecretsManager direttamente (lo fa il controller dopo il salvataggio o set_accounts)

        lists_page = settings_panel.config_tab.lists_page
        acc_widget = lists_page.account_section

        initial_count = acc_widget.list_widget.count()
        # Chiamata al metodo pubblico corretto V9.0
        acc_widget.add_account()

        assert acc_widget.list_widget.count() == initial_count + 1

        found = any(
            "new_user" in acc_widget.list_widget.item(i).text() for i in range(acc_widget.list_widget.count())
        )
        assert found

    def test_settings_tab_change_logic(self, settings_panel):
        """Verifica la navigazione tra i tab delle impostazioni."""
        assert settings_panel.tabs.currentIndex() == 0
        settings_panel.tabs.setCurrentIndex(1)
        assert settings_panel.tabs.currentIndex() == 1
        assert "ROI" in settings_panel.tabs.tabText(1)
