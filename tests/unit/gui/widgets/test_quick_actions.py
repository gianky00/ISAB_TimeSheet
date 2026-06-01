"""Unit tests for QuickActions widget."""

import pytest
from PySide6.QtCore import QPoint, Qt

from src.gui.widgets.quick_actions import ActionChip, QuickActions


@pytest.fixture
def mock_config(mocker):
    """Mock della configurazione azioni rapide."""
    return mocker.patch(
        "src.gui.widgets.quick_actions.get_config_value", return_value=["nav_scarico_ts", "pf_timbrature"]
    )


class TestQuickActions:
    """Test suite per QuickActions."""

    def test_initialization(self, qtbot, mock_config):
        """Verifica lbl'inizializzazione e il caricamento iniziale."""
        widget = QuickActions()
        qtbot.addWidget(widget)

        chips = widget.findChildren(ActionChip)
        assert len(chips) >= 2

    def test_refresh_actions_custom(self, qtbot, mock_config):
        """Verifica il ricaricamento con chiavi diverse."""
        widget = QuickActions()
        qtbot.addWidget(widget)

        # Cambiamo il mock per il secondo refresh
        mock_config.return_value = ["nav_carico_ts"]
        widget.refresh_actions()

        # Verifichiamo che tra i chip ce ne sia uno con il nuovo testo (usando partial match)
        chips = widget.findChildren(ActionChip)
        texts = [c.text().strip() for c in chips]
        assert any("Carico TS" in t for t in texts)

    def test_action_clicked_signal(self, qtbot, mock_config):
        """Verifica lbl'emissione del segnale al click su un chip."""
        widget = QuickActions()
        qtbot.addWidget(widget)

        chip = widget.findChild(ActionChip)
        assert chip is not None

        with qtbot.waitSignal(widget.action_clicked) as blocker:
            qtbot.mouseClick(chip, Qt.MouseButton.LeftButton)

        assert blocker.args[0] in ["nav_scarico_ts", "pf_timbrature"]

    def test_context_menu_trigger_mocked(self, qtbot, mocker):
        """Verifica lbl'apertura del menu contestuale senza bloccare."""
        widget = QuickActions()
        qtbot.addWidget(widget)

        mock_menu = mocker.patch("src.gui.widgets.quick_actions.QMenu")
        mock_instance = mock_menu.return_value

        widget._show_context_menu(QPoint(10, 10))

        assert mock_menu.called
        assert mock_instance.exec.called


class TestActionChip:
    """Test suite per ActionChip."""

    def test_chip_init(self, qtbot):
        chip = ActionChip("Test", "activity", "#ff0000")
        qtbot.addWidget(chip)
        assert "Test" in chip.text()
        assert chip.icon() is not None
        assert chip.height() == 38
