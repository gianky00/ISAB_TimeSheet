from PyQt6.QtCore import QModelIndex, Qt

from src.gui.design.colors import DARK, LIGHT, get_palette
from src.gui.design.spacing import BorderRadius, Shadow, Spacing
from src.gui.formatters import FastTableModel
from src.utils.log_humanizer import SmartLogTranslator


class TestDesignSystem:
    def test_colors(self):
        assert LIGHT.primary == "#009688"
        assert DARK.primary == "#4DB6AC"
        assert get_palette("light") == LIGHT
        assert get_palette("dark") == DARK
        assert get_palette("invalid") == LIGHT

    def test_spacing(self):
        assert Spacing.BASE == 4
        assert Spacing.md == 16
        assert BorderRadius.full == 9999
        assert "rgba" in Shadow.md


class TestLogHumanizer:
    def test_humanize_categories(self):
        # Start
        h, t, c = SmartLogTranslator.humanize("Avvio bot")
        assert c == "start"
        assert h in SmartLogTranslator.TEMPLATES["start"]

        # Login
        _, _, c = SmartLogTranslator.humanize("Effettuo login")
        assert c == "login"

        # Search
        _, _, c = SmartLogTranslator.humanize("Cerca OdA")
        assert c == "search"

        # Download
        _, _, c = SmartLogTranslator.humanize("Scarico file")
        assert c == "download"

        # Success
        _, _, c = SmartLogTranslator.humanize("Completato con successo")
        assert c == "success"

        # Error
        h, t, c = SmartLogTranslator.humanize("Errore fatale")
        assert c == "error"

        # Wait
        _, _, c = SmartLogTranslator.humanize("In attesa...")
        assert c == "wait"

    def test_fixit_tag_injection(self):
        h, t, c = SmartLogTranslator.humanize("login fallito per credenziali errate")
        assert "[FIXIT:ACCOUNT]" in t


class TestFastTableModelExtended:
    def test_model_edge_cases(self):
        model = FastTableModel(data=[[None]], headers=["Col1"])
        assert model.data(model.index(0, 0)) == ""

        # Invalid index
        assert model.data(QModelIndex()) is None

        # Unhandled role
        assert model.data(model.index(0, 0), role=Qt.ItemDataRole.ToolTipRole) is None

        # Vertical header
        assert (
            model.headerData(0, Qt.Orientation.Vertical, Qt.ItemDataRole.DisplayRole)
            is None
        )
