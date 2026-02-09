from unittest.mock import patch

from src.utils.log_humanizer import SmartLogTranslator


class TestLogHumanizerCoverage:
    """Test suite per src/utils/log_humanizer.py"""

    def test_humanize_start(self):
        human, tech, cat = SmartLogTranslator.humanize("Avvio sistema")
        assert cat == "start"
        assert human in SmartLogTranslator.TEMPLATES["start"]
        assert tech == "Avvio sistema"

    def test_humanize_login(self):
        human, _tech, cat = SmartLogTranslator.humanize("Tentativo di accesso")
        assert cat == "login"
        assert human in SmartLogTranslator.TEMPLATES["login"]

    def test_humanize_search(self):
        human, _tech, cat = SmartLogTranslator.humanize("Ricerca dati in corso")
        assert cat == "search"
        assert human in SmartLogTranslator.TEMPLATES["search"]

    def test_humanize_download(self):
        human, _tech, cat = SmartLogTranslator.humanize("Scarico file excel")
        assert cat == "download"
        assert human in SmartLogTranslator.TEMPLATES["download"]

    def test_humanize_success(self):
        human, _tech, cat = SmartLogTranslator.humanize("Operazione completata")
        assert cat == "success"
        assert human in SmartLogTranslator.TEMPLATES["success"]

        # Test con carattere speciale
        _, _, cat2 = SmartLogTranslator.humanize("Risultato ✓")
        assert cat2 == "success"

    def test_humanize_error(self):
        human, _tech, cat = SmartLogTranslator.humanize("Errore imprevisto")
        assert cat == "error"
        assert human in SmartLogTranslator.TEMPLATES["error"]

        # Test con carattere speciale
        _, _, cat2 = SmartLogTranslator.humanize("Fallito ✗")
        assert cat2 == "error"

    def test_humanize_wait(self):
        human, _tech, cat = SmartLogTranslator.humanize("In attesa del server")
        assert cat == "wait"
        assert human in SmartLogTranslator.TEMPLATES["wait"]

    def test_humanize_fallback(self):
        """Test messaggio che non rientra in nessuna categoria specifica."""
        msg = "Messaggio generico qualunque"
        human, tech, cat = SmartLogTranslator.humanize(msg)
        assert cat == "info"
        assert human == msg
        assert tech == msg

    def test_rich_tags_injection_account(self):
        """Test aggiunta tag [FIXIT:ACCOUNT] su errori credenziali."""
        # Caso login + errore
        _, tech, cat = SmartLogTranslator.humanize("Errore login credenziali")
        assert cat == "error"
        assert "[FIXIT:ACCOUNT]" in tech

        # Solo credenziali
        _, tech, cat = SmartLogTranslator.humanize("credenziali errate")
        assert "[FIXIT:ACCOUNT]" in tech

    @patch("random.choice")
    def test_humanize_deterministic(self, mock_choice):
        """Verifica che venga effettivamente chiamato random.choice con i template corretti."""
        mock_choice.return_value = "Messaggio Mockato"
        human, _, _ = SmartLogTranslator.humanize("start")
        assert human == "Messaggio Mockato"
        mock_choice.assert_called_once_with(SmartLogTranslator.TEMPLATES["start"])
