from src.infrastructure.utils.log_humanizer import SmartLogTranslator


class TestLogHumanizerBoost:
    """Test suite per SmartLogTranslator V9.0 deterministico."""

    def test_humanize_fixed_mapping(self):
        """Verifica la traduzione di messaggi comuni."""
        msg = "avvio automazione"
        human, tech, _cat = SmartLogTranslator.humanize(msg)
        assert human == "[AVVIO] Avvio automazione in corso..."
        assert tech == msg

    def test_humanize_preserve_icons(self):
        """Verifica che i messaggi con icone non vengano alterati."""
        msg = "[OK] Operazione conclusa"
        human, _tech, cat = SmartLogTranslator.humanize(msg)
        assert human == msg
        assert cat == "success"

    def test_detect_category_wait(self):
        """Verifica rilevamento categoria attesa con keyword V9.0."""
        # 'attendi' è presente, 'attendo' no.
        assert SmartLogTranslator._detect_category("Attendi un attimo") == "wait"
        assert SmartLogTranslator._detect_category("caricamento in corso") == "wait"
        assert SmartLogTranslator._detect_category("[ATTESA] Polling") == "wait"

    def test_detect_category_error(self):
        """Verifica rilevamento categoria errore."""
        assert SmartLogTranslator._detect_category("Errore di connessione") == "error"
        assert SmartLogTranslator._detect_category("Login fallito") == "error"
        assert SmartLogTranslator._detect_category("[ERRORE] Eccezione") == "error"

    def test_detect_category_success(self):
        """Verifica rilevamento categoria successo."""
        assert SmartLogTranslator._detect_category("Completato con successo") == "success"
        assert SmartLogTranslator._detect_category("[OK] Fatto") == "success"
        assert SmartLogTranslator._detect_category("[INFO] Ottimo") == "success"

    def test_detect_category_action(self):
        """Verifica rilevamento categoria azione utente/bot."""
        assert SmartLogTranslator._detect_category("Click sul pulsante") == "action"
        assert SmartLogTranslator._detect_category("[CLICK] Seleziono") == "action"

    def test_detect_category_search(self):
        """Verifica rilevamento categoria ricerca."""
        assert SmartLogTranslator._detect_category("Ricerca documenti") == "search"
        assert SmartLogTranslator._detect_category("[CERCA] Analisi") == "search"

    def test_detect_category_download(self):
        """Verifica rilevamento categoria download."""
        assert SmartLogTranslator._detect_category("Scaricamento file") == "download"
        assert SmartLogTranslator._detect_category("[DOWNLOAD] Download") == "download"

    def test_fallback_info(self):
        """Verifica fallback su info per messaggi neutri."""
        assert SmartLogTranslator._detect_category("Messaggio informativo generico") == "info"

    def test_humanize_cleaning(self):
        """Verifica pulizia spazi e punti nei messaggi per il mapping."""
        msg = "  MISSIONE COMPIUTA.  "
        human, _, _ = SmartLogTranslator.humanize(msg)
        assert human == "[INFO] Missione completata con successo!"
