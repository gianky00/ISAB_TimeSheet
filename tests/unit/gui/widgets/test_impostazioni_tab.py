"""Unit tests for ImpostazioniTab."""

import pytest
from PySide6.QtCore import Qt

from src.gui.widgets.contabilita.consuntivo.impostazioni_tab import ImpostazioniTab


@pytest.fixture
def mock_config(mocker):
    """Fixture per mockare config_manager."""
    config_data = {"preventivi_tcl": ["TCL1", "TCL2"], "preventivi_stati": ["Stato1"]}
    mocker.patch("src.core.config_manager.get_config_value", side_effect=lambda k, d: config_data.get(k, d))
    mocker.patch("src.core.config_manager.set_config_value")
    return config_data


class TestImpostazioniTab:
    """Test suite per ImpostazioniTab."""

    def test_initialization(self, qtbot, mock_config):
        """Verifica lbl'inizializzazione del tab e il caricamento liste."""
        widget = ImpostazioniTab()
        qtbot.addWidget(widget)

        # tcl_editor è un QFrame che contiene la lista
        from PySide6.QtWidgets import QListWidget

        lists = widget.findChildren(QListWidget)

        # Ci sono 2 editor di liste
        assert len(lists) == 2
        # Verifichiamo il contenuto di uno (TCL)
        found_tcl = False
        for lbl in lists:
            if "TCL1" in [lbl.item(i).text() for i in range(lbl.count())]:
                found_tcl = True
                break
        assert found_tcl

    def test_add_item(self, qtbot, mock_config, mocker):
        """Verifica lbl'aggiunta di un elemento via dialogo."""
        widget = ImpostazioniTab()
        qtbot.addWidget(widget)

        # Mock StandardInputDialog
        mock_input = mocker.patch("src.gui.dialogs.standard_input_dialog.StandardInputDialog.get_input")
        mock_input.return_value = ("Nuovo Tecnico", True)

        # Mock salvataggio
        mock_set = mocker.patch("src.core.config_manager.set_config_value")

        # Trova il bottone "Aggiungi" del primo editor
        from src.gui.widgets.core_widgets import SecondaryButton

        add_btns = [b for b in widget.findChildren(SecondaryButton) if b.text() == "Aggiungi"]

        qtbot.mouseClick(add_btns[0], Qt.MouseButton.LeftButton)

        assert mock_set.called
        assert "Nuovo Tecnico" in mock_set.call_args[0][1]

    def test_remove_item(self, qtbot, mock_config, mocker):
        """Verifica la rimozione di un elemento selezionato."""
        widget = ImpostazioniTab()
        qtbot.addWidget(widget)

        # Trova la prima lista e seleziona un item
        from PySide6.QtWidgets import QListWidget

        lst = widget.findChildren(QListWidget)[0]
        lst.setCurrentRow(0)

        # Mock salvataggio
        mock_set = mocker.patch("src.core.config_manager.set_config_value")

        # Trova bottone "Rimuovi"
        from src.gui.widgets.core_widgets import SecondaryButton

        rem_btns = [b for b in widget.findChildren(SecondaryButton) if b.text() == "Rimuovi"]

        qtbot.mouseClick(rem_btns[0], Qt.MouseButton.LeftButton)

        assert mock_set.called
        # Dovrebbe essere rimasta solo una riga se ne avevamo 2
        assert len(mock_set.call_args[0][1]) == 1
