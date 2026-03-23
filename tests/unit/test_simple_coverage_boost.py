from src.gui.styles.constants import COLORS, FONT_SIZES, UI_SIZES
from src.utils.log_humanizer import SmartLogTranslator


class TestSimpleCoverage:
    def test_colors(self):
        """Verifica che i colori del Design System siano caricati."""
        assert "primary_blue" in COLORS
        assert "success_green" in COLORS
        assert COLORS["primary_blue"].startswith("#")

    def test_ui_sizes(self):
        """Verifica che le dimensioni UI del Design System siano caricate."""
        assert "spacing_md" in UI_SIZES
        assert isinstance(UI_SIZES["spacing_md"], int)

    def test_font_sizes(self):
        """Verifica che i font size siano caricate."""
        assert "md" in FONT_SIZES
        assert FONT_SIZES["md"] >= 10  # noqa: PLR2004


class TestLogHumanizer:
    def test_humanize_categories(self):
        """Verifica il rilevamento categorie deterministico V9.0."""
        # Download
        _, _, cat = SmartLogTranslator.humanize("scarico i dati")
        assert cat == "download"

        # Error
        _, _, cat = SmartLogTranslator.humanize("errore fatale")
        assert cat == "error"

        # Success
        _, _, cat = SmartLogTranslator.humanize("✅ missione compiuta")
        assert cat == "success"

        # Wait
        _, _, cat = SmartLogTranslator.humanize("⏳ attendi un attimo")
        assert cat == "wait"

    def test_humanize_cleaning_logic(self):
        """Verifica la pulizia del messaggio prima del mapping."""
        msg = "  MISSIONE COMPIUTA.  "
        human, _, _ = SmartLogTranslator.humanize(msg)
        assert "Missione" in human
        assert "completata" in human
