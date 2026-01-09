from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QTabWidget, QWidget

from src.gui.panels import (
    CaricoTSPanel,
    DettagliOdAPanel,
    ScaricaTSPanel,
    TimbratureBotPanel,
    ScaricoPDLPanel,
)


class AutomazioniWidget(QTabWidget):
    """Pannello raggruppato per i Bot con caricamento pigro dei sub-pannelli."""

    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window
        self.setTabPosition(QTabWidget.TabPosition.North)

        # Placeholders per i tab
        self.tab_fornitori = QTabWidget()
        for i in range(4):  # Dettagli, Scarico, Timbrature, Carico
            self.tab_fornitori.addTab(QWidget(), f"Tab {i}")

        self.tab_safework = QTabWidget()
        self.tab_safework.addTab(QWidget(), "🛡️ Scarico PDL")

        self.addTab(self.tab_fornitori, "Portale Fornitori")
        self.addTab(self.tab_safework, "SafeWork")

        # Nomi tab
        self.tab_fornitori.setTabText(0, "📋 Dettagli OdA")
        self.tab_fornitori.setTabText(1, "📥 Scarico TS")
        self.tab_fornitori.setTabText(2, "⏱️ Timbrature")
        self.tab_fornitori.setTabText(3, "📤 Carico TS")

        # Stato inizializzazione
        self._init_states = {
            "dettagli": False,
            "scarico": False,
            "timbrature": False,
            "carico": False,
            "pdl": False,
        }

        # Connessione segnali
        self.tab_fornitori.currentChanged.connect(self._on_fornitori_tab_changed)
        self.tab_safework.currentChanged.connect(self._on_safework_tab_changed)

        # Carica il primo tab
        QTimer.singleShot(0, lambda: self._on_fornitori_tab_changed(0))

    def _on_fornitori_tab_changed(self, index):
        mapping = {
            0: ("dettagli", DettagliOdAPanel, "dettagli_panel"),
            1: ("scarico", ScaricaTSPanel, "scarico_panel"),
            2: ("timbrature", TimbratureBotPanel, "timbrature_bot_panel"),
            3: ("carico", CaricoTSPanel, "carico_panel"),
        }

        if index in mapping:
            key, cls, attr = mapping[index]
            if not self._init_states[key]:
                panel = cls()
                setattr(self.mw, attr, panel)
                self.tab_fornitori.removeWidget(self.tab_fornitori.widget(index))
                self.tab_fornitori.insertTab(
                    index, panel, self.tab_fornitori.tabText(index)
                )
                self.tab_fornitori.setCurrentIndex(index)
                self._init_states[key] = True

                # Registra nel bot controller
                if hasattr(self.mw, "bot_controller"):
                    self.mw.bot_controller.register_panels([panel])

    def _on_safework_tab_changed(self, index):
        if index == 0 and not self._init_states["pdl"]:
            panel = ScaricoPDLPanel()
            self.mw.pdl_panel = panel
            self.tab_safework.removeWidget(self.tab_safework.widget(0))
            self.tab_safework.insertTab(0, panel, "🛡️ Scarico PDL")
            self._init_states["pdl"] = True
            if hasattr(self.mw, "bot_controller"):
                self.mw.bot_controller.register_panels([panel])
