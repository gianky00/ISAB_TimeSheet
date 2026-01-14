import unittest
from unittest.mock import MagicMock, patch, ANY
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QPoint
from src.gui.controllers.search_controller import SearchController


class TestSearchControllerCoverage(unittest.TestCase):
    def setUp(self):
        self.mock_mw = MagicMock()
        self.mock_mw.global_search = MagicMock()
        self.mock_mw.global_search.mapToGlobal.return_value = QPoint(0, 0)
        self.mock_mw.global_search.height.return_value = 30
        
        # Patch QObject init
        with patch('PyQt6.QtCore.QObject.__init__'):
            self.controller = SearchController(self.mock_mw)

    @patch('src.gui.controllers.search_controller.QMenu')
    def test_perform_search_short_query(self, mock_menu):
        self.controller.perform_search("a")
        mock_menu.assert_not_called()

    @patch('src.gui.controllers.search_controller.QMenu')
    def test_perform_search_no_results(self, MockMenu):
        mock_menu_instance = MockMenu.return_value
        
        # Mock sub-searches to return 0
        self.controller._search_oda = MagicMock(return_value=0)
        self.controller._search_extended = MagicMock(return_value=0)
        self.controller._search_employees = MagicMock(return_value=0)
        self.controller._search_audit = MagicMock(return_value=0)
        
        self.controller.perform_search("nothing")
        
        # Check "No results" action added
        mock_menu_instance.addAction.assert_called_with("❌ Nessun risultato trovato")
        mock_menu_instance.exec.assert_called()

    @patch('src.core.contabilita_manager.ContabilitaManager')
    def test_search_oda_found(self, MockCM):
        MockCM.search_oda.return_value = [{'codice_oda': '123', 'descrizione': 'Test OdA'}]
        menu = MagicMock()
        
        count = self.controller._search_oda("123", menu)
        
        self.assertEqual(count, 1)
        menu.addAction.assert_any_call("📊 CONTABILITÀ STRUMENTALE (OdA):")

    @patch('src.core.contabilita_manager.ContabilitaManager')
    def test_search_oda_exception(self, MockCM):
        MockCM.search_oda.side_effect = Exception("Boom")
        menu = MagicMock()
        count = self.controller._search_oda("123", menu)
        self.assertEqual(count, 0)

    @patch('src.core.contabilita_manager.ContabilitaManager')
    def test_search_extended_found(self, MockCM):
        MockCM.search_extended.return_value = {
            "GIORNALIERE": [{'data': '2023', 'personale': 'P1', 'descrizione': 'D1'}],
            "CANTIERE": [{'data': '2023', 'personale': 'P2', 'commessa': 'C1'}],
            "CERTIFICATI": [{'matricola': 'M1', 'modello': 'Mod1', 'costruttore': 'Cost1'}]
        }
        menu = MagicMock()
        
        count = self.controller._search_extended("query", menu)
        
        self.assertEqual(count, 3)
        menu.addAction.assert_any_call("📂 GIORNALIERE:")
        menu.addAction.assert_any_call("🏗️ CANTIERE (Scarico Ore):")
        menu.addAction.assert_any_call("📜 CERTIFICATI:")

    @patch('src.bots.portale_fornitori.timbrature.storage.TimbratureStorage')
    def test_search_employees_found(self, MockStorage):
        MockStorage.return_value.search_employees.return_value = [{'cognome': 'Rossi', 'nome': 'Mario'}]
        menu = MagicMock()
        
        count = self.controller._search_employees("Rossi", menu)
        
        self.assertEqual(count, 1)
        menu.addAction.assert_any_call("👥 DIPENDENTI:")

    @patch('src.core.audit_manager.AuditManager')
    def test_search_audit_found(self, MockAudit):
        MockAudit.return_value.get_logs.return_value = [
            {'action': 'Login', 'entity': 'User'},
            {'action': 'Logout', 'entity': 'User'}
        ]
        menu = MagicMock()
        
        count = self.controller._search_audit("Login", menu)
        
        self.assertEqual(count, 1) # Only 1 matches "Login"
        menu.addAction.assert_any_call("🛡️ AUDIT LOG:")

    @patch('src.gui.controllers.search_controller.QMenu')
    def test_perform_search_integration(self, MockMenu):
        mock_menu = MockMenu.return_value
        
        # Use simple return values for sub-methods to verify orchestration
        self.controller._search_oda = MagicMock(return_value=1)
        self.controller._search_extended = MagicMock(return_value=0)
        self.controller._search_employees = MagicMock(return_value=0)
        self.controller._search_audit = MagicMock(return_value=0)
        
        self.controller.perform_search("test")
        
        self.controller._search_oda.assert_called()
        # "No results" should NOT be added
        self.assertFalse(any("Nessun risultato" in str(call) for call in mock_menu.addAction.mock_calls))
        mock_menu.exec.assert_called()
