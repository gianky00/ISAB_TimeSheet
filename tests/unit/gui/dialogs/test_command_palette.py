"""Unit tests for CommandPaletteDialog."""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from src.gui.controllers.command_registry import CommandNode
from src.gui.dialogs.command_palette import CommandPaletteDialog


@pytest.fixture
def root_nodes(mocker):
    """Fixture per nodi comando di test."""
    # Nodo con sottomenu
    sub_node = CommandNode(
        label="Sub Command", icon="activity", action=mocker.Mock(), description="A sub command"
    )
    menu_node = CommandNode(label="Main Menu", icon="menu", children=[sub_node])

    # Nodo con input mode
    input_node = CommandNode(
        label="Input Command",
        icon="edit",
        input_prompts=["Enter Value 1", "Enter Value 2"],
        on_input_complete=mocker.Mock(),
    )

    # Nodo semplice
    leaf_node = CommandNode(label="Direct Action", icon="play", action=mocker.Mock())

    return [menu_node, input_node, leaf_node]


class TestCommandPaletteDialog:
    """Test suite per CommandPaletteDialog."""

    def test_initialization(self, qtbot, root_nodes):
        """Verifica lbl'inizializzazione corretta."""
        dialog = CommandPaletteDialog(root_nodes=root_nodes)
        qtbot.addWidget(dialog)

        assert dialog.list_widget.count() == 3
        assert dialog.search_bar.placeholderText() == "Type a command..."

    def _get_item_label(self, list_widget, row):
        """Helper per estrarre la label da un item con widget custom."""
        item = list_widget.item(row)
        widget = list_widget.itemWidget(item)
        labels = widget.findChildren(QLabel)
        # La label principale è solitamente la prima o quella con font bold
        for lbl in labels:
            if lbl.font().bold():
                return lbl.text()
        return labels[0].text() if labels else ""

    def test_navigation_down(self, qtbot, root_nodes):
        """Verifica lbl'ingresso in un sottomenu."""
        dialog = CommandPaletteDialog(root_nodes=root_nodes)
        qtbot.addWidget(dialog)
        dialog.show()

        # Selezioniamo il primo nodo (Main Menu) e premiamo Invio
        dialog.list_widget.setCurrentRow(0)
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Return)

        # Ora la lista deve contenere solo il sub_node
        assert dialog.list_widget.count() == 1
        assert "Sub Command" in self._get_item_label(dialog.list_widget, 0)
        assert dialog.breadcrumb_lbl.isVisible()
        assert "Main Menu" in dialog.breadcrumb_lbl.text()

    def test_navigation_up_via_backspace(self, qtbot, root_nodes):
        """Verifica il ritorno al menu superiore via Backspace."""
        dialog = CommandPaletteDialog(root_nodes=root_nodes)
        qtbot.addWidget(dialog)
        dialog.show()

        # Entriamo nel menu
        dialog.list_widget.setCurrentRow(0)
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Return)
        assert dialog.list_widget.count() == 1

        # Premiamo Backspace nella search bar vuota
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Backspace)

        # Torniamo alla radice
        assert dialog.list_widget.count() == 3
        assert not dialog.breadcrumb_lbl.isVisible()

    def test_search_filtering_recursive(self, qtbot, root_nodes):
        """Verifica la ricerca globale ricorsiva."""
        dialog = CommandPaletteDialog(root_nodes=root_nodes)
        qtbot.addWidget(dialog)
        dialog.show()

        # Cerchiamo "Sub" (che è dentro un sottomenu)
        dialog.search_bar.setText("sub")
        # Il timer della ricerca è 300ms
        qtbot.wait(500)

        assert dialog.list_widget.count() == 1
        assert "Sub Command" in self._get_item_label(dialog.list_widget, 0)

    def test_input_mode_workflow(self, qtbot, root_nodes, mocker):
        """Verifica il workflow di inserimento parametri."""
        dialog = CommandPaletteDialog(root_nodes=root_nodes)
        qtbot.addWidget(dialog)
        dialog.show()

        # Mock hide_animated perché viene chiamato alla fine
        mock_hide = mocker.patch.object(dialog, "hide_animated")

        # Selezioniamo il nodo con input (indice 1)
        dialog.list_widget.setCurrentRow(1)
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Return)

        assert dialog._input_mode
        assert "Enter Value 1" in dialog.search_bar.placeholderText()

        # Primo input
        dialog.search_bar.setText("Valore 1")
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Return)

        assert "Enter Value 2" in dialog.search_bar.placeholderText()

        # Secondo input
        dialog.search_bar.setText("Valore 2")
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Return)

        # Verifica completamento
        callback = root_nodes[1].on_input_complete
        assert callback.called
        args, _ = callback.call_args
        assert args[0] == ["Valore 1", "Valore 2"]
        assert mock_hide.called

    def test_list_navigation_keys(self, qtbot, root_nodes):
        """Verifica la navigazione su/giù con le frecce."""
        dialog = CommandPaletteDialog(root_nodes=root_nodes)
        qtbot.addWidget(dialog)

        assert dialog.list_widget.currentRow() == 0

        # Freccia Giù
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Down)
        assert dialog.list_widget.currentRow() == 1

        # Freccia Su
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Up)
        assert dialog.list_widget.currentRow() == 0

    def test_esc_closes_or_navigates_up(self, qtbot, root_nodes, mocker):
        """Verifica che Esc torni su o chiuda la palette."""
        dialog = CommandPaletteDialog(root_nodes=root_nodes)
        qtbot.addWidget(dialog)
        dialog.show()
        mock_hide = mocker.patch.object(dialog, "hide_animated")

        # 1. Caso: radice -> deve chiudere
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Escape)
        assert mock_hide.called

        # 2. Caso: sottomenu -> deve tornare su
        mock_hide.reset_mock()
        dialog.list_widget.setCurrentRow(0)
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Return)
        assert dialog.breadcrumb_lbl.isVisible()

        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Escape)
        assert not dialog.breadcrumb_lbl.isVisible()
        assert not mock_hide.called

    def test_direct_action_execution(self, qtbot, root_nodes):
        """Verifica lbl'esecuzione immediata di una foglia."""
        dialog = CommandPaletteDialog(root_nodes=root_nodes)
        qtbot.addWidget(dialog)
        dialog.show()

        # Selezioniamo Direct Action (indice 2)
        dialog.list_widget.setCurrentRow(2)
        qtbot.keyClick(dialog.search_bar, Qt.Key.Key_Return)

        # L'azione viene chiamata tramite QTimer.singleShot(50)
        qtbot.wait(100)
        assert root_nodes[2].action.called
