import pytest

from src.gui.panels.settings.pages.general_page import GeneralPage


class TestGeneralPage:
    @pytest.fixture
    def page(self, qtbot):
        p = GeneralPage()
        qtbot.addWidget(p)
        return p

    def test_initial_state(self, page):
        """Verifica lo stato iniziale dei widget."""
        assert not page.headless_check.isChecked()
        assert page.timeout_spin.value() == 300

    def test_load_from_config(self, page):
        """Verifica il caricamento dei valori dalla configurazione."""
        config = {
            "browser_headless": True,
            "browser_timeout": 45,
        }
        page.load_from_config(config)

        assert page.headless_check.isChecked()
        assert page.timeout_spin.value() == 45

    def test_save_to_config(self, page):
        """Verifica il salvataggio dei valori nel dizionario di configurazione."""
        page.headless_check.setChecked(True)
        page.timeout_spin.setValue(60)

        config = {}
        page.save_to_config(config)

        assert config["browser_headless"] is True
        assert config["browser_timeout"] == 60

    def test_settings_changed_signal(self, page, qtbot):
        """Verifica che i widget emettano il segnale settings_changed."""
        with qtbot.waitSignal(page.settings_changed):
            page.headless_check.setChecked(not page.headless_check.isChecked())

        with qtbot.waitSignal(page.settings_changed):
            page.timeout_spin.setValue(page.timeout_spin.value() + 1)
