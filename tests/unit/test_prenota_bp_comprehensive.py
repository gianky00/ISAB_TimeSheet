import unittest
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from src.bots.portale_fornitori.prenota_bp.bot import PrenotaBPBot
from src.bots.portale_fornitori.prenota_bp.locators import PrenotaBPLocators
from src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page import PrenotaBPPage


class TestPrenotaBPBotComprehensive(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.bot = PrenotaBPBot(username="test_user", password="test_pass")
        self.bot.driver = self.mock_driver
        self.bot._log_callback = MagicMock()

    def test_init_and_properties(self):
        """Verifica l'inizializzazione e le proprietà di base."""
        self.assertEqual(self.bot.name, "Prenota BP")
        self.assertEqual(self.bot.username, "test_user")
        self.assertTrue(len(self.bot.fornitore) > 0)
        self.assertIn("Prenotazione Badge Provvisori", self.bot.description)

        cols = self.bot.get_columns()
        self.assertEqual(len(cols), 2)
        self.assertEqual(cols[0]["name"], "numero_bp")

    def test_get_row_value_normalization(self):
        """Verifica che l'estrazione dei valori dalle righe sia robusta."""
        row = {"numero_bp": "123", "Note di Ritiro": "Test Note"}
        self.assertEqual(self.bot._get_row_value(row, "Numero BP"), "123")
        self.assertEqual(self.bot._get_row_value(row, "note_di_ritiro"), "Test Note")
        self.assertEqual(self.bot._get_row_value(row, "Inesistente"), "")

    @patch("src.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_run_success(self, mock_page_class):
        """Test di esecuzione completata con successo."""
        mock_page = mock_page_class.return_value
        data = {"rows": [{"Numero BP": "BP001", "Note di Ritiro": "Nota 1"}]}

        result = self.bot.run(data)

        self.assertTrue(result)
        mock_page.navigate_to_gestione_bp.assert_called_once()
        mock_page.filtra_buoni_prelievo.assert_called_once()
        mock_page.apri_dettagli_bp.assert_called_once()
        mock_page.gestisci_creazione_richiesta.assert_called_with("Nota 1")
        self.assertEqual(len(self.bot.results), 1)
        self.assertEqual(self.bot.results[0]["STATO"], "OK")

    @patch("src.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_run_stop_requested(self, mock_page_class):
        """Verifica che il bot si fermi se richiesto dall'utente."""
        self.bot._stop_requested = True
        data = {"rows": [{"Numero BP": "BP001"}]}

        result = self.bot.run(data)

        self.assertTrue(result)
        mock_page_class.return_value.navigate_to_gestione_bp.assert_called_once()
        mock_page_class.return_value.filtra_buoni_prelievo.assert_not_called()


class TestPrenotaBPPageComprehensive(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_log = MagicMock()

        # Patch WebDriverWait in __init__
        with patch(
            "src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page.WebDriverWait"
        ) as mock_wait_class:
            self.mock_wait = MagicMock()
            self.mock_short_wait = MagicMock()
            # self.wait, self.short_wait
            mock_wait_class.side_effect = [self.mock_wait, self.mock_short_wait]
            self.page = PrenotaBPPage(self.mock_driver, self.mock_log)

    @patch("src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page.EC")
    def test_wait_and_click_retry_logic(self, mock_ec):
        """Verifica la logica di retry di wait_and_click."""
        with patch(
            "src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page.WebDriverWait"
        ) as mock_local_wait_class:
            mock_local_wait = MagicMock()
            mock_local_wait_class.return_value = mock_local_wait

            mock_el = MagicMock()
            # Primo tentativo fallisce (TimeoutException), secondo ha successo
            mock_local_wait.until.side_effect = [TimeoutException(), mock_el]

            # overlay (short_wait)
            self.mock_short_wait.until.return_value = True

            locator = (By.ID, "test-id")
            result = self.page.wait_and_click(locator)

            self.assertEqual(result, mock_el)
            self.assertEqual(mock_local_wait.until.call_count, 2)
            mock_el.click.assert_called_once()

    @patch("src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page.EC")
    def test_wait_and_click_js_fallback(self, mock_ec):
        """Verifica il fallback JS se il click standard fallisce."""
        with patch(
            "src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page.WebDriverWait"
        ) as mock_local_wait_class:
            mock_local_wait = MagicMock()
            mock_local_wait_class.return_value = mock_local_wait
            mock_el = MagicMock()
            mock_local_wait.until.return_value = mock_el
            mock_el.click.side_effect = Exception("Element not clickable")

            self.mock_short_wait.until.return_value = True

            locator = (By.ID, "test-id")
            self.page.wait_and_click(locator)

            self.mock_driver.execute_script.assert_any_call("arguments[0].click();", mock_el)

    @patch("src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page.EC")
    def test_navigate_to_gestione_bp_expansion(self, mock_ec):
        """Verifica l'espansione del menu se il sottomenu non è subito visibile."""
        self.mock_driver.find_elements.return_value = []

        # Sequenza short_wait.until (per _wait_for_overlay)
        # 1. Inizio navigate_to_gestione_bp
        # 2. In visibility_of_element_located per SUBMENU -> Fallisce
        # 3. In wait_and_click (MENU_BUONO_PRELIEVO)
        # 4. In fine navigate_to_gestione_bp
        self.mock_short_wait.until.side_effect = [True, TimeoutException(), True, True, True]

        mock_submenu = MagicMock()
        # self.wait.until calls:
        # 1. element_to_be_clickable SUBMENU_GESTIONE_BP
        # 2. presence_of_element_located FILTER_FORNITORE
        self.mock_wait.until.side_effect = [mock_submenu, True]

        with patch.object(self.page, "wait_and_click") as mock_wc:
            self.page.navigate_to_gestione_bp()
            mock_wc.assert_called_with(PrenotaBPLocators.MENU_BUONO_PRELIEVO)

        self.mock_driver.execute_script.assert_any_call("arguments[0].click();", mock_submenu)

    @patch("src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page.EC")
    @patch("selenium.webdriver.common.action_chains.ActionChains")
    def test_filtra_buoni_prelievo_vendor_selection(self, mock_action_class, mock_ec):
        """Verifica la selezione del fornitore tramite freccia e lista."""
        mock_arrow = MagicMock()
        mock_option = MagicMock()
        mock_input = MagicMock()

        # short_wait per _wait_for_overlay
        self.mock_short_wait.until.return_value = True

        # self.wait.until calls:
        # 1. FILTER_FORNITORE_ARROW (element_to_be_clickable)
        # 2. FILTER_NUMERO_BP (visibility_of_element_located in wait_and_fill)
        # 3. FILTER_DATA_DA (visibility_of_element_located in wait_and_fill)
        # 4. FILTER_DATA_A (visibility_of_element_located in wait_and_fill)
        self.mock_wait.until.side_effect = [mock_arrow, mock_input, mock_input, mock_input]

        with patch(
            "src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page.WebDriverWait"
        ) as mock_local_wait_class:
            mock_local_wait = MagicMock()
            mock_local_wait_class.return_value = mock_local_wait

            # mock_local_wait calls (new WebDriverWait(driver, 10) for option and wait_time/2 for click):
            # 1. option (presence_of_element_located)
            # 2. BT_CERCA (visibility_of_element_located in wait_and_click)
            mock_local_wait.until.side_effect = [mock_option, MagicMock()]

            self.page.filtra_buoni_prelievo(
                fornitore="VENDOR", numero_bp="123", data_da="01/01", data_a="02/01"
            )

        mock_action_class.return_value.move_to_element.assert_called_with(mock_arrow)
        self.mock_driver.execute_script.assert_any_call("arguments[0].click();", mock_option)
        self.assertEqual(mock_input.clear.call_count, 3)

    @patch("src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page.EC")
    def test_gestisci_creazione_richiesta_select_all(self, mock_ec):
        """Test del flusso di creazione richiesta con selezione 'Tutti i materiali'."""
        mock_row = MagicMock()
        mock_row.find_element.return_value = MagicMock()
        self.mock_driver.find_elements.side_effect = [[mock_row]]  # data_rows

        self.mock_wait.until.return_value = True
        self.mock_short_wait.until.return_value = True

        with patch.object(self.page, "wait_and_click") as mock_wc:
            with patch.object(self.page, "wait_and_fill") as mock_wf:
                self.page.gestisci_creazione_richiesta("Test Note")

                mock_wc.assert_any_call(PrenotaBPLocators.HEADER_CHECKBOX_SELECT_ALL)
                mock_wc.assert_any_call(PrenotaBPLocators.BT_CREA_RICHIESTA)
                mock_wc.assert_any_call(PrenotaBPLocators.BT_SALVA)

    @patch("src.bots.portale_fornitori.prenota_bp.pages.prenota_bp_page.EC")
    def test_gestisci_creazione_richiesta_partial_selection(self, mock_ec):
        """Test della selezione puntuale se solo alcuni materiali sono disponibili."""
        mock_row_ok = MagicMock()
        mock_row_err = MagicMock()
        mock_row_err.find_element.side_effect = Exception("Not available")

        mock_checker_ok = MagicMock()
        mock_checker_err = MagicMock()

        # In _analizza_disponibilita e _esegui_selezione
        self.mock_driver.find_elements.side_effect = [
            [mock_row_ok, mock_row_err],  # data_rows
            [mock_checker_ok, mock_checker_err],  # checkers
        ]

        self.mock_wait.until.return_value = True
        self.mock_short_wait.until.return_value = True

        with patch.object(self.page, "wait_and_click"):
            with patch.object(self.page, "wait_and_fill"):
                self.page.gestisci_creazione_richiesta("Partial Note")

        # Verifica scroll e click standard tramite _click_safe
        self.mock_driver.execute_script.assert_any_call(
            "arguments[0].scrollIntoView({block: 'center'});", mock_checker_ok
        )
        mock_checker_ok.click.assert_called_once()

        # Non deve aver toccato il secondo checker
        mock_checker_err.click.assert_not_called()


if __name__ == "__main__":
    unittest.main()
