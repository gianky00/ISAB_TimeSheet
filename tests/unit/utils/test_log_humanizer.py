from datetime import UTC, datetime, timedelta

from src.utils.log_humanizer import SmartLogTranslator, friendly_time_delta


class TestLogHumanizer:
    def test_friendly_time_delta(self):
        now = datetime.now(UTC).astimezone()

        # Adesso
        assert friendly_time_delta(now - timedelta(seconds=10)) == "Adesso"

        # Minuti
        assert friendly_time_delta(now - timedelta(minutes=5)) == "5 min fa"

        # Ore
        assert friendly_time_delta(now - timedelta(hours=3)) == "3h fa"

        # Giorni
        past = now - timedelta(days=2)
        assert friendly_time_delta(past) == past.strftime("%d/%m")

    def test_smart_log_translator_humanize_fixed(self):
        # Messaggio mappato
        h, t, c = SmartLogTranslator.humanize("avvio automazione")
        assert h == "[AVVIO] Avvio automazione in corso..."
        assert t == "avvio automazione"
        assert c == "info"  # Per keyword "avvio" non c'è cat specifica, va in info

    def test_smart_log_translator_humanize_prefixed(self):
        # Messaggio con prefisso speciale
        msg = "[CLICK] Click su pulsante"
        h, _t, c = SmartLogTranslator.humanize(msg)
        assert h == msg
        assert c == "action"

    def test_smart_log_translator_categories(self):
        # Download
        assert SmartLogTranslator._detect_category("Sto scaricando i file") == "download"
        # Error
        assert SmartLogTranslator._detect_category("Errore critico rilevato") == "error"
        # Success
        assert SmartLogTranslator._detect_category("Operazione completata") == "success"
        # Search
        assert SmartLogTranslator._detect_category("Ricerca in corso") == "search"
        # Wait
        assert SmartLogTranslator._detect_category("In attesa del sito") == "wait"
        # Default category (info)
        assert SmartLogTranslator._detect_category("Qualcosa di generico") == "info"

    def test_smart_log_translator_humanize_raw(self):
        # Messaggio non mappato e senza prefisso
        msg = "Messaggio sconosciuto"
        h, t, _c = SmartLogTranslator.humanize(msg)
        assert h == msg
        assert t == msg
