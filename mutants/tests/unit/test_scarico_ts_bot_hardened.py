from unittest.mock import MagicMock

from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot


class TestScaricoTSBotHardened:
    def test_filename_generation_logic(self):
        """Testa la logica di costruzione del nome file (Pure Logic)."""
        # Simuliamo la logica di _download_excel senza istanziare il bot
        numero_oda = "12345"
        posizione_oda = "10"

        # Scenario 1: ODA + POS
        safe_oda = numero_oda
        safe_pos = posizione_oda
        name = f"TS_{safe_oda}-{safe_pos}.xlsx"
        assert name == "TS_12345-10.xlsx"

        # Scenario 2: Solo ODA
        posizione_oda = ""
        name = f"TS_{safe_oda}.xlsx"
        assert name == "TS_12345.xlsx"

    def test_validate_data_scenarios(self, mocker):
        """Verifica la validazione dati mockando l'istanza."""
        # Creiamo un mock dell'oggetto bot per evitare l'init reale
        bot = MagicMock(spec=ScaricaTSBot)
        bot.username = "u"
        bot.password = "p"
        bot.fornitore = "FornitoreTest"

        # Colleghiamo il metodo reale al mock per testarlo
        bot.validate_data = ScaricaTSBot.validate_data.__get__(bot, ScaricaTSBot)

        # Mock del metodo super().validate_data (BaseBot)
        mocker.patch(
            "src.bots.base.base_bot.BaseBot.validate_data", return_value=(True, "")
        )

        # 1. Successo
        valid, msg = bot.validate_data([{"numero_oda": "123"}])
        assert valid is True

        # 2. Fallimento fornitore
        bot.fornitore = ""
        valid, msg = bot.validate_data([{"numero_oda": "123"}])
        assert valid is False
        assert "Fornitore" in msg

    def test_setup_filters_mocked_driver(self, mocker):
        """Verifica la sequenza di interazione con il driver per i filtri."""
        bot = MagicMock(spec=ScaricaTSBot)
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        bot.long_wait = MagicMock()
        bot.fornitore = "TEST_FORN"
        bot.data_da = "01.01.2024"  # Obbligatorio per send_keys
        bot._check_stop = MagicMock()
        bot._attendi_scomparsa_overlay = MagicMock()

        # Colleghiamo il metodo reale
        bot._setup_filters = ScaricaTSBot._setup_filters.__get__(bot, ScaricaTSBot)

        # Mocking expected_conditions e ActionChains
        mocker.patch("src.bots.portale_fornitori.scarico_ts.bot.EC")
        m_actions = mocker.patch(
            "src.bots.portale_fornitori.scarico_ts.bot.ActionChains"
        )
        mocker.patch("time.sleep")

        # Mock elementi
        mock_arrow = MagicMock()
        mock_option = MagicMock()
        mock_date_field = MagicMock()

        # Configura i wait per restituire i mock degli elementi in sequenza
        bot.wait.until.side_effect = [mock_arrow, mock_date_field]
        bot.long_wait.until.return_value = mock_option

        res = bot._setup_filters()

        assert res is True
        # Verifica iniezione JavaScript per click opzione (scrolling + click)
        assert bot.driver.execute_script.call_count >= 2
        # Verifica inserimento data
        mock_date_field.send_keys.assert_called_with(bot.data_da)
        # Verifica ActionChains
        m_actions.assert_called_with(bot.driver)
        m_actions.return_value.move_to_element.assert_called_with(mock_arrow)
