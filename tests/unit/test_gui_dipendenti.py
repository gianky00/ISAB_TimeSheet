import pytest
from PyQt6.QtWidgets import QApplication
from src.gui.panels.dipendenti_manager_panel import DipendentiManagerPanel

# Fixture per l'app Qt (necessaria per i widget)
@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    yield app

def test_dipendenti_panel_creation(qapp):
    """Verifica che il pannello Dipendenti si crei senza errori."""
    panel = DipendentiManagerPanel()
    assert panel is not None
    assert panel.objectName() == "DipendentiManagerPanel"
    
    # Verifica presenza widget chiave
    assert panel.table is not None
    assert panel.search_bar is not None
    assert panel.btn_add is not None
    
    # Verifica colonne tabella
    assert panel.table.columnCount() == 6
