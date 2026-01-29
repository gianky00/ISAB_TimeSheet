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
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
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

        # Input Mode State
        self._input_mode = False
        self._input_prompts = []
        self._input_callback = None
        self._input_answers = []
        self._input_index = 0

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
        self.container.setGeometry(10, 10, self.target_width - 20, self.target_height - 20)

        # Colors - Modern Dark Theme
        bg_color = "rgba(32, 33, 36, 0.98)"  # Deep unified background
        text_color = "#e8eaed"
        accent_color = "#8ab4f8"  # Google Blue-ish / VSCode Blue

        self.container.setObjectName("MainContainer")
        self.container.setStyleSheet(
            f"""
            QWidget#MainContainer {{
                background-color: {bg_color};
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                color: {text_color};
            }}
            QLabel {{ border: none; background: transparent; }}
        """
        )

        # Shadow (Subtler, deeper)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(20)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Breadcrumb ---
        self.breadcrumb_lbl = QLabel(">")
        self.breadcrumb_lbl.setStyleSheet(
            f"color: {accent_color}; font-weight: 600; padding: 12px 20px 4px 20px; font-size: 13px; font-family: 'Segoe UI', sans-serif;"
        )
        self.breadcrumb_lbl.setVisible(False)
        layout.addWidget(self.breadcrumb_lbl)

        # --- Search Bar Area ---
        search_container = QWidget()
        search_container.setStyleSheet("background: transparent; border: none;")
        search_layout = QVBoxLayout(search_container)
        search_layout.setContentsMargins(15, 15, 15, 15)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Type a command...")
        self.search_bar.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: transparent;
                color: {text_color};
                border: none;
                border-bottom: 2px solid rgba(255, 255, 255, 0.1);
                font-family: 'Segoe UI', sans-serif;
                font-size: 20px;
                padding: 8px 4px;
                selection-background-color: {accent_color};
            }}
            QLineEdit:focus {{
                border-bottom: 2px solid {accent_color};
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
        except Exception:
            pass
        self.closed.emit()

    def eventFilter(self, obj, event):
        if obj == self.search_bar and event.type() == event.Type.KeyPress:
            if self._input_mode:
                return self._handle_input_mode_key(event)
            return self._handle_standard_key(event)

        return super().eventFilter(obj, event)

    def _handle_input_mode_key(self, event):
        key = event.key()
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self._submit_input_step()
            return True
        elif key == Qt.Key.Key_Escape:
            self._cancel_input_mode()
            return True
        return False

    def _handle_standard_key(self, event):
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
            if not self.search_bar.text():
                self._navigate_up()
                return True

        elif key == Qt.Key.Key_Escape:
            if self.navigation_stack and not self.search_bar.text():
                self._navigate_up()
            else:
                self.hide_animated()
            return True

        elif key == Qt.Key.Key_K and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if not event.isAutoRepeat() and getattr(self, "_can_close_via_shortcut", True):
                self.hide_animated()
            return True

        return False

    def _start_input_mode(self, node: CommandNode):
        """Avvia la modalità input per il nodo selezionato."""
        self._input_mode = True
        self._input_prompts = node.input_prompts
        self._input_callback = node.on_input_complete
        self._input_answers = []
        self._input_index = 0

        self.list_widget.setVisible(False)
        self.breadcrumb_lbl.setVisible(True)
        self.breadcrumb_lbl.setText(f"> {node.label}")  # Show Context
        self._show_next_prompt()

    def _show_next_prompt(self):
        if self._input_index < len(self._input_prompts):
            prompt = self._input_prompts[self._input_index]
            self.search_bar.setText("")
            self.search_bar.setPlaceholderText(f"{prompt} (Invio per confermare, Esc per annullare)")
            self.search_bar.setFocus()
        else:
            # Finished
            self._finish_input_mode()

    def _submit_input_step(self):
        val = self.search_bar.text().strip()
        if not val:
            return  # Block empty? Or allow empty? Let's block empty for now.

        self._input_answers.append(val)
        self._input_index += 1
        self._show_next_prompt()

    def _finish_input_mode(self):
        if self._input_callback:
            try:
                self._input_callback(self._input_answers)
            except Exception as e:
                print(f"Error in input callback: {e}")

        self.hide_animated()

    def _cancel_input_mode(self):
        """Esce dalla modalità input e torna alla lista."""
        self._input_mode = False
        self.list_widget.setVisible(True)
        self.search_bar.setText("")
        self._update_breadcrumb_ui()
        self.search_bar.setFocus()

    def _navigate_down(self, node: CommandNode):
        """Entra in un sottomenu."""
        children = node.get_children()
        if not children:
            return

        # Push stato corrente nello stack
        self.navigation_stack.append((self.current_nodes, self.list_widget.currentRow()))
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
            self.search_bar.setPlaceholderText("> Cerca...")
        else:
            self.breadcrumb_lbl.setVisible(True)
            path_str = " > ".join(self.breadcrumb_path)
            self.breadcrumb_lbl.setText(f"> {path_str}")
            self.search_bar.setPlaceholderText(f"Cerca dentro {self.breadcrumb_path[-1]}...")

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
        try:
            if self._input_mode:
                return

            search = text.lower().strip()
            print(f"DEBUG PALETTE: Searching for '{search}'...")

            self.list_widget.clear()

            # Se vuoto, mostra la vista corrente (navigazione gerarchica)
            if not search:
                # Restore UI state
                self._update_breadcrumb_ui()
                self._populate_list(self.current_nodes)
                return

            # Hide breadcrumb in flat search mode
            self.breadcrumb_lbl.setVisible(False)

            # Se c'è testo, cerca ricorsivamente in TUTTO l'albero (vista piatta)
            results = []
            self._collect_all_nodes(self.root_nodes, search, results)
            print(f"DEBUG PALETTE: Found {len(results)} matches for '{search}'")

            for n in results:
                self._add_item(n)

            if self.list_widget.count() > 0:
                self.list_widget.setCurrentRow(0)
            else:
                # Optional: Show "No results" item?
                pass
        except Exception as e:
            print(f"ERROR in _filter_list: {e}")
            import traceback

            traceback.print_exc()

    def _collect_all_nodes(self, nodes, search, results):
        """Raccoglie ricorsivamente tutti i nodi che matchano la ricerca."""
        for node in nodes:
            # Check match su label o description
            match = (search in node.label.lower()) or (
                node.description and search in node.description.lower()
            )

            # Se è una foglia (azione) ed è un match, aggiungi
            # Se è un menu (folder), aggiungi SOLO se matcha il nome del menu
            # Ma vogliamo cercare anche DENTRO i menu

            if match:
                results.append(node)

            # Ricorsione sui figli (se ci sono)
            children = node.get_children()
            if children:
                self._collect_all_nodes(children, search, results)

    def _execute_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        node: CommandNode = item.data(Qt.ItemDataRole.UserRole)

        # Check Input Mode
        if node.input_prompts:
            self._start_input_mode(node)
            return

        if node.is_leaf:
            # Esegui Azione
            if node.close_on_execute:
                self.hide()
            QTimer.singleShot(50, lambda: node.action() if node.action else None)
        else:
            # Naviga Sottomenu
            self._navigate_down(node)
