from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
    QTimer,
    pyqtSignal,
)
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QDialog,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.gui.controllers.command_registry import CommandNode
from src.utils.helpers import get_asset_path, get_colored_icon


class CommandPaletteDialog(QDialog):
    """
    Dialogo 'Quick Open' stile VSCode V2 (Interactive CLI).
    - Frameless, Overlay
    - Gerarchico (Root -> Submenu -> Action)
    - Breadcrumb Navigation
    """

    # Segnale emesso quando il dialogo è completamente chiuso
    closed = pyqtSignal()

    def __init__(self, parent=None, root_nodes=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Dimensioni target
        self.target_width = 700
        self.target_height = 500
        self.setFixedSize(self.target_width, self.target_height)

        # Stato Navigazione
        self.root_nodes = root_nodes or []
        self.current_nodes = self.root_nodes  # Lista corrente visualizzata
        self.navigation_stack = []  # Stack di (Label, Nodes) per tornare indietro
        self.breadcrumb_path = []  # Lista stringhe breadcrumb

        self._setup_ui()
        self._populate_list(self.current_nodes)

        # Animazione Proprietà
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.is_closing = False

    def _setup_ui(self):
        # Container Principale
        self.container = QWidget(self)
        self.container.setGeometry(
            10, 10, self.target_width - 20, self.target_height - 20
        )

        # Colors
        bg_color = "#1e1e1e"
        input_bg = "#3c3c3c"
        text_color = "#cccccc"
        border_color = "#454545"

        self.container.setObjectName("MainContainer")
        self.container.setStyleSheet(
            f"""
            QWidget#MainContainer {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 6px;
                color: {text_color};
            }}
            QLabel {{ border: none; background: transparent; }}
        """
        )

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Breadcrumb Area (NEW) ---
        self.breadcrumb_lbl = QLabel(">")
        self.breadcrumb_lbl.setStyleSheet(
            "color: #007fd4; font-weight: bold; padding: 5px 10px; font-family: 'Consolas', monospace;"
        )
        self.breadcrumb_lbl.setVisible(False)
        layout.addWidget(self.breadcrumb_lbl)

        # --- Search Bar Area ---
        search_container = QWidget()
        search_container.setStyleSheet(
            f"""
            background-color: {input_bg};
            border-top-left-radius: 6px; # Se Breadcrumb visibile, questo cambia
            border-top-right-radius: 6px;
            padding: 5px;
            border-bottom: 1px solid {border_color};
        """
        )
        search_layout = QVBoxLayout(search_container)
        search_layout.setContentsMargins(8, 0, 8, 5)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("> Type to search...")
        self.search_bar.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: #3c3c3c;
                color: {text_color};
                border: 1px solid transparent;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                padding: 4px;
            }}
            QLineEdit:focus {{
                border: 1px solid #007fd4;
                background-color: #252526;
            }}
        """
        )
        self.search_bar.textChanged.connect(self._filter_list)
        self.search_bar.installEventFilter(self)

        search_layout.addWidget(self.search_bar)
        layout.addWidget(search_container)

        # --- List Widget ---
        self.list_widget = QListWidget()
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.list_widget.setStyleSheet(
            f"""
            QListWidget {{
                background-color: {bg_color};
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                padding: 0px;
                border: none;
                color: {text_color};
            }}
            QListWidget::item:selected {{
                background-color: #04395e;
                color: #ffffff;
            }}
            QListWidget::item:hover {{
                background-color: #2a2d2e;
            }}
             /* Scrollbar Styling */
            QScrollBar:vertical {{
                border: none;
                background: {bg_color};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #424242;
                min-height: 20px;
                border-radius: 5px;
                margin: 2px;
            }}
        """
        )
        self.list_widget.itemActivated.connect(self._execute_selected)
        self.list_widget.clicked.connect(self._execute_selected)
        layout.addWidget(self.list_widget)

    def show_animated(self):
        """Mostra il dialogo con reset dello stato."""
        if not self.parent():
            return

        # Debounce
        self._can_close_via_shortcut = False
        QTimer.singleShot(400, lambda: setattr(self, "_can_close_via_shortcut", True))

        # Reset Navigazione
        self.navigation_stack.clear()
        self.breadcrumb_path.clear()
        self.current_nodes = self.root_nodes
        self._populate_list(self.current_nodes)
        self._update_breadcrumb_ui()
        self.search_bar.setText("")
        self.search_bar.setFocus()

        parent_geo = self.parent().geometry()
        x = parent_geo.x() + (parent_geo.width() - self.width()) // 2
        start_y = parent_geo.y() + 30

        self.setGeometry(x, start_y, self.width(), 0)
        self.show()
        self.raise_()

        self.anim.setStartValue(QRect(x, start_y, self.width(), 0))
        self.anim.setEndValue(QRect(x, start_y, self.width(), self.target_height))
        self.anim.start()

    def hide_animated(self):
        if self.is_closing:
            return
        self.is_closing = True

        geo = self.geometry()
        self.anim.setStartValue(geo)
        self.anim.setEndValue(QRect(geo.x(), geo.y(), geo.width(), 0))
        self.anim.finished.connect(self._finish_close)
        self.anim.start()

    def _finish_close(self):
        self.hide()
        self.is_closing = False
        try:
            self.anim.finished.disconnect(self._finish_close)
        except:
            pass
        self.closed.emit()

    def eventFilter(self, obj, event):
        if obj == self.search_bar and event.type() == event.Type.KeyPress:
            key = event.key()
            if key == Qt.Key.Key_Down:
                idx = self.list_widget.currentRow()
                if idx < self.list_widget.count() - 1:
                    self.list_widget.setCurrentRow(idx + 1)
                return True
            elif key == Qt.Key.Key_Up:
                idx = self.list_widget.currentRow()
                if idx > 0:
                    self.list_widget.setCurrentRow(idx - 1)
                return True
            elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
                self._execute_selected()
                return True
            elif key == Qt.Key.Key_Backspace:
                if not self.search_bar.text():  # Se input vuoto, torna indietro
                    self._navigate_up()
                    return True
            elif key == Qt.Key.Key_Escape:
                if self.navigation_stack and not self.search_bar.text():
                    self._navigate_up()  # Esc torna su di un livello
                else:
                    self.hide_animated()  # O chiude se siamo alla root
                return True
            elif (
                key == Qt.Key.Key_K
                and event.modifiers() == Qt.KeyboardModifier.ControlModifier
            ):
                if not event.isAutoRepeat() and getattr(
                    self, "_can_close_via_shortcut", True
                ):
                    self.hide_animated()
                return True

        return super().eventFilter(obj, event)

    def _navigate_down(self, node: CommandNode):
        """Entra in un sottomenu."""
        children = node.get_children()
        if not children:
            return

        # Push stato corrente nello stack
        self.navigation_stack.append(
            (self.current_nodes, self.list_widget.currentRow())
        )
        self.breadcrumb_path.append(node.label)

        # Aggiorna stato
        self.current_nodes = children
        self._populate_list(self.current_nodes)
        self._update_breadcrumb_ui()
        self.search_bar.setText("")  # Reset ricerca

    def _navigate_up(self):
        """Torna al livello superiore."""
        if not self.navigation_stack:
            return

        prev_nodes, prev_row = self.navigation_stack.pop()
        if self.breadcrumb_path:
            self.breadcrumb_path.pop()

        self.current_nodes = prev_nodes
        self._populate_list(self.current_nodes)
        self._update_breadcrumb_ui()
        self.list_widget.setCurrentRow(prev_row)
        self.search_bar.setText("")

    def _update_breadcrumb_ui(self):
        if not self.breadcrumb_path:
            self.breadcrumb_lbl.setVisible(False)
            self.search_bar.setPlaceholderText("> Type to search...")
        else:
            self.breadcrumb_lbl.setVisible(True)
            path_str = " > ".join(self.breadcrumb_path)
            self.breadcrumb_lbl.setText(f"> {path_str}")
            self.search_bar.setPlaceholderText(
                f"Search inside {self.breadcrumb_path[-1]}..."
            )

    def _populate_list(self, nodes: list[CommandNode]):
        self.list_widget.clear()
        for node in nodes:
            self._add_item(node)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _add_item(self, node: CommandNode):
        item = QListWidgetItem(self.list_widget)
        item.setSizeHint(QSize(0, 50))

        widget = QWidget()
        widget.setStyleSheet("background: transparent; border: none;")
        h = QHBoxLayout(widget)
        h.setContentsMargins(10, 5, 10, 5)
        h.setSpacing(15)

        # Icon
        icon_lbl = QLabel()
        icon_lbl.setFixedSize(20, 20)
        pm = get_colored_icon(get_asset_path(node.icon), "#cccccc").pixmap(20, 20)
        icon_lbl.setPixmap(pm)
        h.addWidget(icon_lbl)

        # Text
        v = QVBoxLayout()
        v.setSpacing(2)
        v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        lbl = QLabel(node.label)
        lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #e1e1e1;")
        v.addWidget(lbl)

        if node.description:
            desc = QLabel(node.description)
            desc.setStyleSheet("font-size: 12px; color: #858585;")
            v.addWidget(desc)
        h.addLayout(v)
        h.addStretch()

        # Is Menu Indicator OR Shortcut
        if not node.is_leaf:
            # Arrow Icon for menus
            arrow = QLabel("▶")  # Placeholder per icona arrow
            arrow.setStyleSheet("color: #858585; font-size: 10px;")
            h.addWidget(arrow)
        elif node.shortcut:
            sc = QLabel(node.shortcut)
            sc.setStyleSheet("color: #858585; font-family: monospace;")
            h.addWidget(sc)

        item.setData(Qt.ItemDataRole.UserRole, node)
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

    def _filter_list(self, text):
        search = text.lower()
        self.list_widget.clear()
        # Filtra solo i nodi correnti
        filtered = [
            n
            for n in self.current_nodes
            if search in n.label.lower() or search in n.description.lower()
        ]
        for n in filtered:
            self._add_item(n)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _execute_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        node: CommandNode = item.data(Qt.ItemDataRole.UserRole)

        if node.is_leaf:
            # Esegui Azione
            if node.close_on_execute:
                self.hide()
            QTimer.singleShot(50, lambda: node.action() if node.action else None)
        else:
            # Naviga Sottomenu
            self._navigate_down(node)
