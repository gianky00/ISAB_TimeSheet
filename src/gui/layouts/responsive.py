"""
Layout responsivi che si adattano alle dimensioni finestra.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QSize

class ResponsiveContainer(QWidget):
    """Container che cambia layout in base alla larghezza."""

    BREAKPOINT_MOBILE = 600
    BREAKPOINT_TABLET = 900

    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgets = []
        self._current_mode = None
        self._setup_layouts()

    def _setup_layouts(self):
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

    def addWidget(self, widget: QWidget):
        self._widgets.append(widget)
        self._rebuild_layout()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = event.size().width()

        new_mode = self._get_mode(width)
        if new_mode != self._current_mode:
            self._current_mode = new_mode
            self._rebuild_layout()

    def _get_mode(self, width: int) -> str:
        if width < self.BREAKPOINT_MOBILE:
            return "mobile"
        elif width < self.BREAKPOINT_TABLET:
            return "tablet"
        return "desktop"

    def _rebuild_layout(self):
        # Clear layout
        while self._main_layout.count():
            item = self._main_layout.takeAt(0)
            if item.layout():
                # We need to reparent items inside nested layouts or just clear the pointers
                # Since we added widgets to nested layouts, taking the layout item doesn't automatically unparent widgets
                # But here we keep reference in self._widgets
                pass

        # To reuse widgets, we must ensure they are not deleted.
        # QVBoxLayout.takeAt removes from layout but doesn't delete widget if it has a parent.
        # But we need to explicitly hide/show or just re-add.

        if self._current_mode == "mobile":
            # Stack verticale
            for widget in self._widgets:
                self._main_layout.addWidget(widget)
                widget.show()
        elif self._current_mode == "tablet":
            # 2 colonne
            row = QHBoxLayout()
            for i, widget in enumerate(self._widgets):
                row.addWidget(widget)
                widget.show()
                if (i + 1) % 2 == 0:
                    self._main_layout.addLayout(row)
                    row = QHBoxLayout()
            if row.count():
                self._main_layout.addLayout(row)
        else:
            # 3+ colonne (Desktop)
            row = QHBoxLayout()
            for i, widget in enumerate(self._widgets):
                row.addWidget(widget)
                widget.show()
                if (i + 1) % 3 == 0:
                    self._main_layout.addLayout(row)
                    row = QHBoxLayout()
            if row.count():
                self._main_layout.addLayout(row)
