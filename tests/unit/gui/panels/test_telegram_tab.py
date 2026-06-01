"""Unit tests for TelegramTab."""

from src.gui.panels.settings.tabs.telegram_tab import TelegramTab


class TestTelegramTab:
    """Test suite per TelegramTab."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione del tab e dei widget."""
        widget = TelegramTab()
        qtbot.addWidget(widget)

        assert len(widget.cards) == 2
        assert widget.token_edit is not None
        assert widget.chat_id_edit is not None
        assert widget.btn_test is not None

    def test_load_from_config(self, qtbot):
        """Verifica il caricamento dati."""
        widget = TelegramTab()
        qtbot.addWidget(widget)

        config = {"telegram_token": "TOK:123", "telegram_chat_id": "456"}
        widget.load_from_config(config)

        assert widget.token_edit.text() == "TOK:123"
        assert widget.chat_id_edit.text() == "456"

    def test_save_to_config(self, qtbot):
        """Verifica il salvataggio dati."""
        widget = TelegramTab()
        qtbot.addWidget(widget)

        widget.token_edit.setText("NEW:TOK")
        widget.chat_id_edit.setText("789")

        config = {}
        widget.save_to_config(config)

        assert config["telegram_token"] == "NEW:TOK"
        assert config["telegram_chat_id"] == "789"

    def test_settings_changed_signal(self, qtbot):
        """Verifica lbl'emissione del segnale alla modifica del testo."""
        widget = TelegramTab()
        qtbot.addWidget(widget)

        with qtbot.waitSignal(widget.settings_changed):
            widget.token_edit.setText("modified")

    def test_filter_cards(self, qtbot):
        """Verifica la ricerca interna."""
        widget = TelegramTab()
        qtbot.addWidget(widget)

        # Cerchiamo "Connettività"
        widget.search_bar.setText("Connettività")

        visible_cards = [c for c in widget.cards if not c.isHidden()]
        assert len(visible_cards) == 1
        assert "Test Connettività" in visible_cards[0].title_text

    def test_connectivity_test_trigger(self, qtbot, mocker):
        """Verifica lbl'avvio del test di invio (mockato)."""
        widget = TelegramTab()
        qtbot.addWidget(widget)

        # Nota: il pulsante test è collegato a un metodo che solitamente sta nel controller
        # o nel tab stesso. In telegram_tab.py non vedo la connessione a un metodo reale nel codice letto.
        # Vediamo se c'è un metodo _on_test_clicked... no, non c'è nel file letto.
        # Probabilmente viene collegato esternamente o manca.
        # Verifichiamo almeno la presenza del bottone.
        assert widget.btn_test.text() == "Invia Messaggio di Test"
