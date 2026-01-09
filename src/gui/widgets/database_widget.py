from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QTabWidget, QWidget


class DatabaseWidget(QTabWidget):
    """Pannello raggruppato per i Database con caricamento pigro."""

    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window

        for i in range(3):
            self.addTab(QWidget(), f"Tab {i}")

        self.setTabText(0, "Timbrature Isab")
        self.setTabText(1, "Strumentale")
        self.setTabText(2, "DataEase")

        self._init_states = [False, False, False]
        self.currentChanged.connect(self._on_tab_changed)
        QTimer.singleShot(0, lambda: self._on_tab_changed(0))

    def _on_tab_changed(self, index):
        if self._init_states[index]:
            return

        if index == 0:
            from src.gui.panels import TimbratureDBPanel

            panel = TimbratureDBPanel()
            self.mw.timbrature_db_panel = panel
        elif index == 1:
            from src.gui.contabilita_panel import ContabilitaPanel

            panel = ContabilitaPanel()
            self.mw.contabilita_panel = panel
        elif index == 2:
            from src.gui.scarico_ore_panel import ScaricoOrePanel

            panel = ScaricoOrePanel()
            self.mw.scarico_ore_panel = panel

        old_text = self.tabText(index)
        self.blockSignals(True)
        try:
            self.removeTab(index)
            self.insertTab(index, panel, old_text)
            self.setCurrentIndex(index)
        finally:
            self.blockSignals(False)
        
        self._init_states[index] = True
