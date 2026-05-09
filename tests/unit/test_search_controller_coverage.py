import unittest
from unittest.mock import MagicMock, patch

from PySide6.QtCore import QPoint

from src.gui.controllers.search_controller import SearchController


class TestSearchControllerCoverage(unittest.TestCase):
    def setUp(self):
        self.mock_mw = MagicMock()
        self.mock_mw.global_search = MagicMock()
        self.mock_mw.global_search.mapToGlobal.return_value = QPoint(0, 0)
        self.mock_mw.global_search.height.return_value = 30

        self.controller = SearchController(self.mock_mw)

    def test_perform_search_short_query(self):
        self.controller.perform_search("a")
        # should not trigger search timer
        self.assertEqual(self.controller._last_query, "")

    @patch("src.gui.controllers.search_controller.QMenu")
    def test_perform_search_no_results(self, MockMenu):  # noqa: N803
        mock_menu_instance = MockMenu.return_value

        # Mock all sub-searches to return 0
        self.controller._add_oda_matches = MagicMock(return_value=0)
        self.controller._add_storico_oda_matches = MagicMock(return_value=0)
        self.controller._add_extended_matches = MagicMock(return_value=0)
        self.controller._add_employees_matches = MagicMock(return_value=0)
        self.controller._add_attivita_matches = MagicMock(return_value=0)
        self.controller._add_pdl_matches = MagicMock(return_value=0)
        self.controller._add_audit_matches = MagicMock(return_value=0)

        self.controller._show_results_menu({})

        # Check "No results" action added
        mock_menu_instance.addAction.assert_called_with("Nessun risultato trovato")
        mock_menu_instance.exec.assert_called()

    def test_add_oda_matches(self):
        menu = MagicMock()
        count = self.controller._add_oda_matches([{"codice_oda": "123", "descrizione": "Test OdA"}], menu)
        self.assertEqual(count, 1)
        menu.addAction.assert_any_call("CONTABILITÀ STRUMENTALE (OdA):")

    def test_add_extended_matches(self):
        ext_results = {
            "GIORNALIERE": [{"data": "2023", "personale": "P1", "descrizione": "D1"}],
            "CANTIERE": [{"data": "2023", "personale": "P2", "commessa": "C1"}],
            "CERTIFICATI": [{"matricola": "M1", "modello": "Mod1", "costruttore": "Cost1"}],
        }
        menu = MagicMock()
        count = self.controller._add_extended_matches(ext_results, menu)

        self.assertEqual(count, 3)
        menu.addAction.assert_any_call("GIORNALIERE:")
        menu.addAction.assert_any_call("CANTIERE (Scarico Ore):")
        menu.addAction.assert_any_call("CERTIFICATI:")

    def test_add_employees_matches(self):
        menu = MagicMock()
        count = self.controller._add_employees_matches([{"cognome": "Rossi", "nome": "Mario"}], menu)
        self.assertEqual(count, 1)
        menu.addAction.assert_any_call("DIPENDENTI:")

    def test_add_audit_matches(self):
        menu = MagicMock()
        count = self.controller._add_audit_matches([{"action": "Login", "entity": "User"}], menu)
        self.assertEqual(count, 1)
        menu.addAction.assert_any_call("AUDIT LOG:")

    @patch("src.gui.controllers.search_controller.QMenu")
    def test_perform_search_integration(self, MockMenu):  # noqa: N803
        mock_menu = MockMenu.return_value

        # Use simple return values for sub-methods to verify orchestration
        self.controller._add_oda_matches = MagicMock(return_value=1)
        self.controller._add_extended_matches = MagicMock(return_value=0)
        self.controller._add_employees_matches = MagicMock(return_value=0)
        self.controller._add_audit_matches = MagicMock(return_value=0)
        self.controller._add_storico_oda_matches = MagicMock(return_value=0)
        self.controller._add_attivita_matches = MagicMock(return_value=0)
        self.controller._add_pdl_matches = MagicMock(return_value=0)

        self.controller._show_results_menu({"oda": [{"codice_oda": "1", "descrizione": ""}]})

        self.controller._add_oda_matches.assert_called()
        # "No results" should NOT be added
        self.assertFalse(any("Nessun risultato" in str(call) for call in mock_menu.addAction.mock_calls))
        mock_menu.exec.assert_called()
