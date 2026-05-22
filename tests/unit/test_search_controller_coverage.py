import unittest
from typing import Any
from unittest.mock import MagicMock, patch

import PySide6.QtWidgets

# Salviamo il riferimento originario di QMenu
orig_qmenu = PySide6.QtWidgets.QMenu


# Definiamo la classe fittizia pure-Python per sostituire QMenu
class MockQMenu:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._actions: list[Any] = []
        self.exec: Any = MagicMock()

    def setParent(self, parent: PySide6.QtWidgets.QWidget) -> None:  # noqa: N802
        pass

    def setStyleSheet(self, style: str) -> None:  # noqa: N802
        pass

    def addAction(self, text: str) -> MagicMock:  # noqa: N802
        action = MagicMock()
        action.text.return_value = text
        self._actions.append(action)
        return action

    def addSeparator(self) -> None:  # noqa: N802
        pass

    def actions(self) -> list[Any]:
        return self._actions


# Sostituiamo QMenu con la versione fittizia prima di importare il modulo sotto test
PySide6.QtWidgets.QMenu = MockQMenu  # type: ignore

from src.gui.components.search.results_menu import SearchResultsMenu  # noqa: E402
from src.gui.controllers.search_controller import SearchController  # noqa: E402


class TestSearchControllerCoverage(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_mw = MagicMock()
        self.mock_mw.global_search = MagicMock()
        self.mock_mw.global_search.mapToGlobal.return_value = MagicMock()
        self.mock_mw.global_search.height.return_value = 30

        self.controller = SearchController(self.mock_mw)

    def test_perform_search_short_query(self) -> None:
        self.controller.perform_search("a")
        # should not trigger search timer
        self.assertEqual(self.controller._last_query, "")

    @patch("src.gui.controllers.search_controller.SearchResultsMenu")
    def test_show_results_menu_delegation(self, mock_menu_class: MagicMock) -> None:
        mock_menu_instance = mock_menu_class.return_value

        self.controller._last_query = "test_query"
        self.controller._show_results_menu({"oda": []})

        # Il codice reale passa parent=self.mw (cioè self.mock_mw nei test)
        mock_menu_class.assert_called_once_with(self.mock_mw, "test_query", parent=self.mock_mw)
        mock_menu_instance.build_and_exec.assert_called_once_with({"oda": []}, self.mock_mw.global_search)


class TestSearchResultsMenuCoverage(unittest.TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        # Ripristiniamo la classe base originaria per non influenzare altri test
        PySide6.QtWidgets.QMenu = orig_qmenu  # type: ignore

    def setUp(self) -> None:
        self.mock_mw = MagicMock()
        self.mock_search_widget = MagicMock()
        self.mock_search_widget.mapToGlobal.return_value = MagicMock()
        self.mock_search_widget.height.return_value = 30

        # Istanziamo il menu (usa MockQMenu internamente come classe base)
        self.menu = SearchResultsMenu(self.mock_mw, "query_di_prova", parent=None)

    def test_results_menu_no_results(self) -> None:
        self.menu.build_and_exec({}, self.mock_search_widget)

        # Verifica che sia stata aggiunta l'azione "Nessun risultato trovato"
        actions = self.menu.actions()
        self.assertTrue(any(a.text() == "Nessun risultato trovato" for a in actions))
        self.menu.exec.assert_called_once()  # type: ignore[attr-defined]

    def test_add_oda_matches(self) -> None:
        results = {"oda": [{"codice_oda": "123", "descrizione": "Test OdA"}]}
        self.menu.build_and_exec(results, self.mock_search_widget)

        actions = self.menu.actions()
        self.assertTrue(any("CONTABILITÀ STRUMENTALE (OdA):" in a.text() for a in actions))
        self.assertTrue(any("OdA 123 - Test OdA..." in a.text() for a in actions))
        self.menu.exec.assert_called_once()  # type: ignore[attr-defined]

    def test_add_extended_matches(self) -> None:
        results = {
            "extended": {
                "GIORNALIERE": [{"data": "2023", "personale": "P1", "descrizione": "D1"}],
                "CANTIERE": [{"data": "2023", "personale": "P2", "commessa": "C1"}],
                "CERTIFICATI": [{"matricola": "M1", "modello": "Mod1", "costruttore": "Cost1"}],
            }
        }
        self.menu.build_and_exec(results, self.mock_search_widget)

        actions = self.menu.actions()
        self.assertTrue(any("GIORNALIERE:" in a.text() for a in actions))
        self.assertTrue(any("CANTIERE (Scarico Ore):" in a.text() for a in actions))
        self.assertTrue(any("CERTIFICATI:" in a.text() for a in actions))
        self.menu.exec.assert_called_once()  # type: ignore[attr-defined]

    def test_add_employees_matches(self) -> None:
        results = {"employees": [{"cognome": "Rossi", "nome": "Mario"}]}
        self.menu.build_and_exec(results, self.mock_search_widget)

        actions = self.menu.actions()
        self.assertTrue(any("DIPENDENTI:" in a.text() for a in actions))
        self.assertTrue(any("Rossi Mario" in a.text() for a in actions))
        self.menu.exec.assert_called_once()  # type: ignore[attr-defined]

    def test_add_audit_matches(self) -> None:
        results = {"audit": [{"action": "Login", "entity": "User"}]}
        self.menu.build_and_exec(results, self.mock_search_widget)

        actions = self.menu.actions()
        self.assertTrue(any("AUDIT LOG:" in a.text() for a in actions))
        self.assertTrue(any("Login - User" in a.text() for a in actions))
        self.menu.exec.assert_called_once()  # type: ignore[attr-defined]
