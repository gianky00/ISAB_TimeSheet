"""
Layout responsivi che si adattano alle dimensioni finestra.
"""

from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QHBoxLayout, QLayout, QVBoxLayout, QWidget


class ResponsiveContainer(QWidget):
    """Container che cambia layout in base alla larghezza."""

    BREAKPOINT_MOBILE = 600
    BREAKPOINT_TABLET = 900

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza il container responsivo."""
        super().__init__(parent)
        self._widgets: list[QWidget] = []
        self._current_mode: str | None = None
        self._main_layout: QVBoxLayout
        self._setup_layouts()

    def _setup_layouts(self) -> None:
        """Configura il layout di base del container."""
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

    def addWidget(self, widget: QWidget) -> None:
        """Aggiunge un widget alla lista interna e aggiorna la visualizzazione."""
        self._widgets.append(widget)
        self._rebuild_layout()

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        """Gestisce il cambio di dimensioni della finestra aggiornando il layout se necessario."""
        if event is not None:
            super().resizeEvent(event)
            width = event.size().width()

            new_mode = self._get_mode(width)
            if new_mode != self._current_mode:
                self._current_mode = new_mode
                self._rebuild_layout()

    def _get_mode(self, width: int) -> str:
        """Determina la modalità di visualizzazione (mobile, tablet, desktop) in base alla larghezza."""
        if width < self.BREAKPOINT_MOBILE:
            return "mobile"
        if width < self.BREAKPOINT_TABLET:
            return "tablet"
        return "desktop"

    def _rebuild_layout(self) -> None:
        """Pulisce e ricostruisce il layout in base alla modalità corrente."""
        self._clear_layout()
        self._build_layout_by_mode()

    def _clear_layout(self, layout: QLayout | None = None) -> None:
        """Rimuove ricorsivamente tutti gli elementi dal layout senza distruggere i widget."""
        if layout is None:
            layout = self._main_layout

        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue
            child_layout = item.layout()
            if child_layout is not None:
                self._clear_layout(child_layout)
                child_layout.deleteLater()
            child_widget = item.widget()
            if child_widget is not None:
                # Disaccoppia il widget dal layout ma non distruggerlo
                child_widget.setParent(None)
                child_widget.setParent(self)

    def _build_layout_by_mode(self) -> None:
        """Sceglie il metodo di costruzione del layout basandosi sul modo corrente."""
        # Se non ci sono widget, non fare nulla
        if not self._widgets:
            return

        if self._current_mode == "mobile":
            self._add_widgets_stacked()
        elif self._current_mode == "tablet":
            self._add_widgets_grid(cols=3)
        else:
            self._add_widgets_grid(cols=6)

    def _add_widgets_stacked(self) -> None:
        """Disposizione verticale (1 colonna)."""
        for widget in self._widgets:
            self._main_layout.addWidget(widget)
            widget.show()

    def _add_widgets_grid(self, cols: int) -> None:
        """Disposizione a griglia con numero di colonne specificato."""
        current_row = QHBoxLayout()
        for i, widget in enumerate(self._widgets):
            current_row.addWidget(widget)
            widget.show()

            if (i + 1) % cols == 0:
                self._main_layout.addLayout(current_row)
                current_row = QHBoxLayout()

        if current_row.count() > 0:
            self._main_layout.addLayout(current_row)
        else:
            current_row.deleteLater()
