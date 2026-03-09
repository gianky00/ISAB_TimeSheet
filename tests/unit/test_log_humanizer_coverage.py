import pytest
from src.utils.log_humanizer import SmartLogTranslator

class TestLogHumanizerCoverage:
    def test_humanize_start(self):
        """Verifica la mappatura del messaggio di avvio."""
        msg = "avvio automazione"
        human, _, cat = SmartLogTranslator.humanize(msg)
        assert human == "🚀 Avvio automazione in corso..."
        assert cat == "info"

    def test_humanize_login(self):
        """Verifica la mappatura dell'inserimento credenziali."""
        msg = "inserimento credenziali"
        human, _, cat = SmartLogTranslator.humanize(msg)
        assert human == "🔐 Inserimento credenziali..."
        assert cat == "info"

    def test_humanize_search(self):
        """Verifica la mappatura del messaggio di ricerca."""
        msg = "mi metto alla ricerca"
        human, _, cat = SmartLogTranslator.humanize(msg)
        assert human == "🔍 Ricerca in corso..."
        assert cat == "search"

    def test_humanize_download(self):
        """Verifica la mappatura del messaggio di scarico."""
        msg = "scarico i file"
        human, _, cat = SmartLogTranslator.humanize(msg)
        assert human == "⬇️ Scarico file in corso..."
        assert cat == "download"

    def test_humanize_success(self):
        """Verifica la mappatura del successo."""
        msg = "missione compiuta"
        human, _, cat = SmartLogTranslator.humanize(msg)
        assert human == "✨ Missione completata con successo!"
        assert cat == "success"

    def test_humanize_error(self):
        """Verifica la mappatura dell'errore."""
        msg = "errore critico"
        human, _, cat = SmartLogTranslator.humanize(msg)
        assert human == "❌ Errore critico rilevato!"
        assert cat == "error"

    def test_detect_category_error_variants(self):
        """Verifica varianti di keyword per categoria errore."""
        assert SmartLogTranslator._detect_category("Fallimento critico") == "error"
        assert SmartLogTranslator._detect_category("Eccezione timeout") == "error"
        assert SmartLogTranslator._detect_category("❌ Portale offline") == "error"

    def test_detect_category_success_variants(self):
        """Verifica varianti di keyword per categoria successo."""
        assert SmartLogTranslator._detect_category("Operazione completata") == "success"
        assert SmartLogTranslator._detect_category("✅ Dati inviati") == "success"
        assert SmartLogTranslator._detect_category("✨ Risultato ottimo") == "success"

    def test_humanize_preserve_custom_icons(self):
        """Verifica che icone non standard vengano preservate."""
        msg = "ℹ️ Nota di sistema"
        human, _, _ = SmartLogTranslator.humanize(msg)
        assert human == msg
