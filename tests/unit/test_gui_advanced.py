from src.gui.widgets.info_widgets import KPIBigCard


class TestGUIAdvanced:
    def test_info_label_callback(self, qtbot):
        """Test: Verifica che l'icona info mostri il contenuto corretto."""

        def test_callback():
            return "Info Dettagliata Test"

        card = KPIBigCard("Test", "Valore")
        card.set_info_callback(test_callback)

        assert card._get_info_content() == "Info Dettagliata Test"
