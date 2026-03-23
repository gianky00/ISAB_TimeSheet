from unittest.mock import patch

import pytest
from PyQt6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem

from src.gui.panels.contabilita_panel import ContabilitaPanel


class TestContabilitaPanelRefactoring:
    @pytest.fixture
    def panel(self, qtbot):  # noqa: ANN001
        with (
            patch("src.gui.panels.contabilita_panel.ContabilitaPanel.refresh_tabs"),
            patch("src.gui.panels.contabilita_panel.ContabilitaPanel._connect_selection_signal"),
        ):
            p = ContabilitaPanel()
            p.selection_count_label = QLabel("0")
            p.selection_sum_label = QLabel("0")
            return p

    @pytest.mark.skip(
        reason="Incompatibilità mock in ambiente headless Windows. Logica da spostare in utility."
    )
    def test_update_selection_total_table(self, panel, qtbot):  # noqa: ANN001
        """Test calculation of totals in a QTableWidget."""
        table = QTableWidget(3, 3)
        table.setItem(0, 0, QTableWidgetItem("10,5"))
        table.setItem(1, 0, QTableWidgetItem("5,0"))

        # Inseriamo la tabella nel pannello o rendiamola attiva
        # selezioniamo gli indici tramite il selectionModel reale
        sel_model = table.selectionModel()
        sel_model.select(table.model().index(0, 0), sel_model.SelectionFlag.Select)
        sel_model.select(table.model().index(1, 0), sel_model.SelectionFlag.Select)

        # Chiamata al metodo interno di calcolo
        panel._update_selection_total(table)

        # Verifica
        count_text = panel.selection_count_label.text()
        sum_text = panel.selection_sum_label.text()

        # Debug print (sarà visibile solo se il test fallisce con -s)
        print(f"DEBUG: Count={count_text}, Sum={sum_text}")

        assert "2" in count_text
        assert "15,5" in sum_text

    @pytest.mark.skip(
        reason="Incompatibilità mock in ambiente headless Windows. Logica da spostare in utility."
    )
    def test_update_selection_total_tree(self, panel):  # noqa: ANN001
        """Test selection count in a QTreeWidget."""
        from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem  # noqa: PLC0415

        tree = QTreeWidget()
        item = QTreeWidgetItem(["A"])
        tree.addTopLevelItem(item)
        item.setSelected(True)

        panel._update_selection_total(tree)
        assert "1" in panel.selection_count_label.text()
