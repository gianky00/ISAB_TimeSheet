from datetime import UTC, datetime, timedelta

from src.infrastructure.utils.log_humanizer import SmartLogTranslator, friendly_time_delta


class TestLogHumanizer:
    def test_friendly_time_delta(self):
        now = datetime.now(UTC).astimezone()

        # Adesso
        assert friendly_time_delta(now - timedelta(seconds=10)) == "Adesso"

        # Minuti fa
        assert friendly_time_delta(now - timedelta(minutes=5)) == "5 min fa"

        # Ore fa
        assert friendly_time_delta(now - timedelta(hours=2)) == "2h fa"

        # Giorni fa (formato DD/MM)
        past = now - timedelta(days=2)
        assert friendly_time_delta(past) == past.strftime("%d/%m")

    def test_smart_translator_humanize_fixed(self):
        # Mappatura fissa
        human, _tech, cat = SmartLogTranslator.humanize("avvio automazione")
        assert "[AVVIO]" in human
        assert cat == "info"  # default if no other keyword match

    def test_smart_translator_humanize_prefixed(self):
        # Messaggio già con prefisso
        msg = "✅ Operazione conclusa"
        human, _tech, cat = SmartLogTranslator.humanize(msg)
        assert human == msg
        assert cat == "success"

    def test_smart_translator_categories(self):
        # Error
        _, _, cat = SmartLogTranslator.humanize("Errore nel sistema")
        assert cat == "error"

        # Search
        _, _, cat = SmartLogTranslator.humanize("Ricerca dipendente")
        assert cat == "search"

        # Action
        _, _, cat = SmartLogTranslator.humanize("Click su pulsante")
        assert cat == "action"

        # Wait
        _, _, cat = SmartLogTranslator.humanize("In attesa di risposta")
        assert cat == "wait"

        # Download
        _, _, cat = SmartLogTranslator.humanize("Scarico file excel")
        assert cat == "download"

    def test_smart_translator_unknown(self):
        msg = "Messaggio generico casuale"
        human, _tech, cat = SmartLogTranslator.humanize(msg)
        assert human == msg
        assert cat == "info"
