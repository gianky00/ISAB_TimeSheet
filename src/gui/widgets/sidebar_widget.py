"""
SyncroJob - Sidebar Widget
Gestione del menu di navigazione laterale con icone e indicatori di stato.
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.widgets.sidebar_button import SidebarButton


class SidebarWidget(QWidget):
    """
    Barra laterale di navigazione principale dell'applicazione.
    Contiene i pulsanti per passare tra le varie sezioni (Dashboard, Automazioni, Impostazioni, ecc.).
    """

    page_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        """
        Inizializza la sidebar e crea i pulsanti di navigazione.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.setFixedWidth(70)
        self.buttons = []
        self._setup_ui()

    def _setup_ui(self):
        """Configura il layout e i componenti visivi della sidebar."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 10, 5, 10)
        self.main_layout.setSpacing(10)

        # Pulsanti Superiori
        self.btn_dashboard = self.add_button(Icons.HOME, "Dashboard", 0)
        self.btn_automazioni = self.add_button(Icons.ACTIVITY, "Automazioni", 1)
        self.btn_dati = self.add_button(Icons.DATABASE, "Dati", 2)
        self.btn_dipendenti = self.add_button(Icons.USERS, "Dipendenti", 3)
        self.btn_lyra = self.add_button(Icons.ACTIVITY, "Analisi Lyra", 4)

        self.main_layout.addStretch()

        # Pulsanti Inferiori
        self.btn_settings = self.add_button(Icons.SETTINGS, "Impostazioni", 7)
        self.btn_help = self.add_button(Icons.HELP, "Aiuto", 8)

    def add_button(self, icon_path: str, tooltip: str, page_index: int) -> SidebarButton:
        """
        Aggiunge un pulsante alla sidebar.

        Args:
            icon_path: Percorso dell'icona SVG.
            tooltip: Testo descrittivo del pulsante.
            page_index: Indice della pagina nel QStackedWidget principale.

        Returns:
            SidebarButton: L'istanza del pulsante creato.
        """
        btn = SidebarButton(icon_path, tooltip, self)
        btn.clicked.connect(lambda: self._on_button_clicked(page_index))
        self.main_layout.addWidget(btn)
        self.buttons.append((btn, page_index))
        return btn

    def _on_button_clicked(self, index: int):
        """Gestisce il click del pulsante aggiornando lo stato visivo e emettendo il segnale."""
        self.page_changed.emit(index)
        self.set_active_page(index)

    def set_active_page(self, index: int):
        """
        Aggiorna l'evidenziazione visiva del pulsante attivo.

        Args:
            index: Indice della pagina da attivare.
        """
        for btn, page_idx in self.buttons:
            btn.set_active(page_idx == index)
