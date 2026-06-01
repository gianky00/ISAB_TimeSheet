from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QStackedWidget, QWidget

from src.core.contabilita.consuntivo.consuntivo_controller import ConsuntivoController
from src.core.contabilita.scarico_ore.controller import ScaricoOreController
from src.core.dipendenti.anagrafica_controller import AnagraficaController
from src.core.oda.oda_controller import ODAController

# Importiamo i Controller del Core che ci aspettiamo di trovare
from src.core.pdl.pdl_controller import PDLController

# Importiamo il controller principale che funge da DI Container
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.main_window.page_index import PageIndex

# Importiamo le Viste (GUI) per verificare lbl'iniezione
from src.gui.panels.pdl.pdl_panel import PDLDBPanel
from src.gui.panels.storico_oda.oda_panel import StoricoOdaPanel


@pytest.fixture
def mock_main_window(qtbot):
    """Crea un finto MainWindow basato su QWidget per soddisfare PyQt C++ binding."""
    mock_mw = QWidget()
    # Mocking dei componenti interni
    mock_mw.stacked_widget = QStackedWidget()
    # Inizializza lo stack con QWidget per matchare PageIndex
    for _ in range(len(PageIndex)):
        mock_mw.stacked_widget.addWidget(QWidget())

    mock_mw.footer_left = MagicMock()
    mock_mw.status_bar_component = MagicMock()
    mock_mw.sidebar = MagicMock()
    mock_mw._current_page_index = 0
    return mock_mw


def test_navigation_controller_dependency_injection(mock_main_window):
    """Test architetturale: Verifica che il NavigationController agisca correttamente come
    Dependency Injection Container (IoC).
    """
    # 1. Instanziazione del Container
    nav_controller = NavigationController(mock_main_window)

    # 2. Verifica che i Controller del CORE siano stati istanziati come Singleton di contesto
    assert isinstance(nav_controller.pdl_controller, PDLController)
    assert isinstance(nav_controller.oda_controller, ODAController)
    assert isinstance(nav_controller.anagrafica_controller, AnagraficaController)
    assert isinstance(nav_controller.scarico_ore_controller, ScaricoOreController)
    assert isinstance(nav_controller.consuntivo_controller, ConsuntivoController)

    # 3. Verifica lbl'Iniezione (Inversion of Control) all'interno di una Vista
    # Testiamo la creazione differita (Lazy Loading) del pannello PDL (Indice 6)
    pdl_panel = nav_controller.get_panel(6)

    assert isinstance(pdl_panel, PDLDBPanel), "Il costruttore deve restituire il pannello corretto"
    assert hasattr(pdl_panel, "controller"), "Il pannello deve possedere lbl'attributo controller"

    # VERIFICA CRITICA: Il controller all'interno della vista DEVE ESSERE ESATTAMENTE
    # la stessa istanza posseduta dal NavigationController (Singleton injection).
    assert pdl_panel.controller is nav_controller.pdl_controller, (
        "Violazione DIP: Il pannello ha istanziato un nuovo controller invece di usare quello iniettato!"
    )

    # 4. Verifica Iniezione per Storico OdA (Indice 10)
    oda_panel = nav_controller.get_panel(10)
    assert isinstance(oda_panel, StoricoOdaPanel)
    assert oda_panel.controller is nav_controller.oda_controller, (
        "Violazione DIP: StoricoOdaPanel non usa il controller iniettato!"
    )
