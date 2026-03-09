import pytest
from src.utils.log_humanizer import SmartLogTranslator

class TestLogHumanizerBoost:
    """Test suite per SmartLogTranslator V9.0 deterministico."""

    def test_humanize_fixed_mapping(self):
        """Verifica la traduzione di messaggi comuni."""
        msg = "avvio automazione"
        human, tech, cat = SmartLogTranslator.humanize(msg)
        assert human == "🚀 Avvio automazione in corso..."
        assert tech == msg

    def test_humanize_preserve_icons(self):
        """Verifica che i messaggi con icone non vengano alterati."""
        msg = "✅ Operazione conclusa"
        human, tech, cat = SmartLogTranslator.humanize(msg)
        assert human == msg
        assert cat == "success"

    def test_detect_category_wait(self):
        """Verifica rilevamento categoria attesa con keyword V9.0."""
        # 'attendi' è presente, 'attendo' no.
        assert SmartLogTranslator._detect_category("Attendi un attimo") == "wait"
        assert SmartLogTranslator._detect_category("caricamento in corso") == "wait"
        assert SmartLogTranslator._detect_category("⏳ Polling") == "wait"

    def test_detect_category_error(self):
        """Verifica rilevamento categoria errore."""
        assert SmartLogTranslator._detect_category("Errore di connessione") == "error"
        assert SmartLogTranslator._detect_category("Login fallito") == "error"
        assert SmartLogTranslator._detect_category("❌ Eccezione") == "error"

    def test_detect_category_success(self):
        """Verifica rilevamento categoria successo."""
        assert SmartLogTranslator._detect_category("Completato con successo") == "success"
        assert SmartLogTranslator._detect_category("✅ Fatto") == "success"
        assert SmartLogTranslator._detect_category("✨ Ottimo") == "success"

    def test_detect_category_action(self):
        """Verifica rilevamento categoria azione utente/bot."""
        assert SmartLogTranslator._detect_category("Click sul pulsante") == "action"
        assert SmartLogTranslator._detect_category("🖱️ Seleziono") == "action"

    def test_detect_category_search(self):
        """Verifica rilevamento categoria ricerca."""
        assert SmartLogTranslator._detect_category("Ricerca documenti") == "search"
        assert SmartLogTranslator._detect_category("🔍 Analisi") == "search"

    def test_detect_category_download(self):
        """Verifica rilevamento categoria download."""
        assert SmartLogTranslator._detect_category("Scaricamento file") == "download"
        assert SmartLogTranslator._detect_category("⬇️ Download") == "download"

    def test_fallback_info(self):
        """Verifica fallback su info per messaggi neutri."""
        assert SmartLogTranslator._detect_category("Messaggio informativo generico") == "info"

    def test_humanize_cleaning(self):
        """Verifica pulizia spazi e punti nei messaggi per il mapping."""
        msg = "  MISSIONE COMPIUTA.  "
        human, _, _ = SmartLogTranslator.humanize(msg)
        assert human == "✨ Missione completata con successo!"
