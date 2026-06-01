"""Unit tests for ConfigTab."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from src.gui.panels.settings.tabs.config_tab import ConfigTab, SettingCard


class MockPage(QWidget):
    """Pagina mock che include segnali e metodi attesi."""

    settings_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_from_config = MagicMock()
        self.save_to_config = MagicMock()
        # Mock per ListsPage sections
        self.account_section = QWidget()
        self.sw_account_section = QWidget()
        self.fornitori_section = QWidget()
        self.contract_section = QWidget()
        self.reparti_section = QWidget()
        self.cantieri_section = QWidget()


@pytest.fixture
def mock_pages(mocker):
    """Mock delle pagine interne per isolare ConfigTab."""
    mocker.patch("src.gui.panels.settings.tabs.config_tab.GeneralPage", return_value=MockPage())
    mocker.patch("src.gui.panels.settings.tabs.config_tab.ListsPage", return_value=MockPage())
    mocker.patch("src.gui.panels.settings.tabs.config_tab.PathsPage", return_value=MockPage())
    mocker.patch("src.gui.panels.settings.tabs.config_tab.DiagPage", return_value=MockPage())


class TestConfigTab:
    """Test suite per ConfigTab."""

    def test_initialization(self, qtbot, mock_pages):
        """Verifica lbl'inizializzazione del tab e delle card."""
        widget = ConfigTab()
        qtbot.addWidget(widget)

        assert len(widget.cards) == 7
        assert widget.search_bar is not None

    def test_filter_cards(self, qtbot, mock_pages):
        """Verifica il filtraggio delle card tramite ricerca."""
        widget = ConfigTab()
        qtbot.addWidget(widget)

        # Cerchiamo "SafeWork"
        widget.search_bar.setText("SafeWork")

        visible_cards = [c for c in widget.cards if not c.isHidden()]
        assert len(visible_cards) < 7
        assert any("SafeWork" in c.title_text for c in visible_cards)

    def test_load_save_delegation(self, qtbot, mock_pages):
        """Verifica che load/save deleghi alle pagine."""
        widget = ConfigTab()
        qtbot.addWidget(widget)

        config = {"test": 1}

        # Load
        widget.load_from_config(config)
        for page in widget.pages:
            assert page.load_from_config.called

        # Save
        widget.save_to_config(config)
        for page in widget.pages:
            assert page.save_to_config.called

    def test_settings_changed_signal_propagation(self, qtbot, mock_pages):
        """Verifica che il segnale delle pagine risalga al tab."""
        widget = ConfigTab()
        qtbot.addWidget(widget)

        with qtbot.waitSignal(widget.settings_changed):
            widget.general_page.settings_changed.emit()


class TestSettingCard:
    """Test suite per SettingCard."""

    def test_card_init(self, qtbot):
        content = QWidget()
        card = SettingCard("Title", "Subtitle", "activity", content)
        qtbot.addWidget(card)

        assert card.title_text == "Title"
        assert card.subtitle_text == "Subtitle"

        from PySide6.QtWidgets import QLabel

        labels = card.findChildren(QLabel)
        assert any("Title" in lbl.text() for lbl in labels)
