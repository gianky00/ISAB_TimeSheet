from src.utils.log_humanizer import SmartLogTranslator


class TestLogHumanizerBoost:
    """Test suite estesa per SmartLogTranslator."""

    def test_humanize_start_category(self):
        """Verifica che messaggi di avvio vengano categorizzati correttamente."""
        msg = "Avvio del sistema in corso..."
        human, tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "start"
        assert human in SmartLogTranslator.TEMPLATES["start"]
        assert tech == msg

    def test_humanize_login_category(self):
        """Verifica categorizzazione login."""
        msg = "Esecuzione login utente"
        human, _tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "login"
        assert human in SmartLogTranslator.TEMPLATES["login"]

    def test_humanize_search_category(self):
        """Verifica categorizzazione ricerca."""
        msg = "Analizzo i dati ricevuti"
        human, _tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "search"
        assert human in SmartLogTranslator.TEMPLATES["search"]

    def test_humanize_download_category(self):
        """Verifica categorizzazione download."""
        msg = "Export completato e file salvato"
        # Nota: 'salvat' attiva download, ma 'completat' attiva success.
        # L'ordine degli if nel codice originale determina la priorità.
        # 'scaric'/'salvat' viene prima di 'successo'/'completat'?
        # Controllando il codice: 'download' è prima di 'success' nell'if-elif chain?
        # No, guardando il codice:
        # 1. start
        # 2. login
        # 3. search
        # 4. download (scaric, salvat, export)
        # 5. success (successo, completat)
        # Quindi "Export completato e file salvato" -> ha "export" e "salvat" -> entra in download.
        human, _tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "download"
        assert human in SmartLogTranslator.TEMPLATES["download"]

    def test_humanize_success_category(self):
        """Verifica categorizzazione successo."""
        msg = "Operazione completata con successo"
        # Qui non ci sono keyword di download, quindi dovrebbe andare su success
        human, _tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "success"
        assert human in SmartLogTranslator.TEMPLATES["success"]

    def test_humanize_error_category(self):
        """Verifica categorizzazione errore."""
        msg = "Eccezione non gestita durante il processo"  # 'exception' -> error
        human, _tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "error"
        assert human in SmartLogTranslator.TEMPLATES["error"]

    def test_humanize_wait_category(self):
        """Verifica categorizzazione attesa."""
        msg = "In attesa del caricamento pagina..."
        human, _tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "wait"
        assert human in SmartLogTranslator.TEMPLATES["wait"]

    def test_fallback_unknown_category(self):
        """Verifica fallback per messaggi non riconosciuti."""
        msg = "Messaggio neutro senza keyword particolari"
        human, tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "info"
        assert human == msg  # Human message is same as original
        assert tech == msg

    def test_rich_tags_injection_login_error(self):
        """Verifica l'injection del tag [FIXIT:ACCOUNT] per errori di login."""
        # Deve essere categoria error E contenere "login"
        msg = "Errore durante il login al portale"
        _human, tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "error"
        assert "[FIXIT:ACCOUNT]" in tech

    def test_rich_tags_injection_credentials(self):
        """Verifica l'injection del tag [FIXIT:ACCOUNT] se presente 'credenziali'."""
        msg = "Credenziali non valide"
        # 'credenziali' non è mappato a una categoria specifica nell'if-elif principale
        # quindi cat sarà 'info' (a meno che non ci siano altre keyword).
        _human, tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "info"
        assert "[FIXIT:ACCOUNT]" in tech
