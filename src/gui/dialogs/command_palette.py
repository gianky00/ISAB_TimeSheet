"""
SyncroJob - Command Palette Dialog
Dialogo 'Quick Open' interattivo ispirato a VSCode per l'accesso rapido a comandi e funzioni.
Supporta navigazione gerarchica, ricerca globale ricorsiva e modalità di input interattivo.
"""

from contextlib import suppress
from typing import TYPE_CHECKING, cast

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import QColor, QKeyEvent
from PySide6.QtWidgets import (
    QDialog,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.gui.controllers.command_registry import CommandNode
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    SearchInput,
    StandardListWidget,
)
from src.utils.helpers import get_asset_path, get_colored_icon

if TYPE_CHECKING:
    from collections.abc import Callable


class CommandPaletteDialog(QDialog):
    """
    Dialogo 'Quick Open' in sovraimpressione.
    Permette di navigare nell'albero dei comandi (Root -> Submenu -> Action)
    o di cercare globalmente qualsiasi funzione registrata nel sistema.
    """

    closed = Signal()
    """Segnale emesso quando il dialogo completa l'animazione di chiusura."""

    def __init__(self, parent: QWidget | None = None, root_nodes: list[CommandNode] | None = None) -> None:
        """
        Inizializza la command palette.

        Args:
          parent: Widget genitore per il posizionamento.
          root_nodes: Lista dei nodi comando radice.
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.target_width = 700
        self.target_height = 500
        self.setFixedSize(self.target_width, self.target_height)

        # Stato Navigazione
        self.root_nodes = root_nodes or []
        self.current_nodes = self.root_nodes
        self.navigation_stack: list[tuple[list[CommandNode], int]] = []
        self.breadcrumb_path: list[str] = []

        # Input Mode State
        self._input_mode = False
        self._input_prompts: list[str] = []
        self._input_callback: Callable[[list[str]], None] | None = None
        self._input_answers: list[str] = []
        self._input_index = 0

        self._setup_ui()
        self._populate_list(self.current_nodes)

        # Animazione
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.is_closing = False
        self._can_close_via_shortcut = True

    def _setup_ui(self) -> None:
        """Configura l'interfaccia scura e moderna con ombre e bordi arrotondati."""
        self.container = QWidget(self)
        self.container.setGeometry(10, 10, self.target_width - 20, self.target_height - 20)

        bg_color = COLORS["glass_dark"]
        text_color = COLORS["bg_white"]
        accent_color = COLORS["primary_blue"]

        self.container.setObjectName("MainContainer")
        self.container.setStyleSheet(
            f"QWidget#MainContainer {{ background-color: {bg_color}; border: 1px solid {COLORS['glass_border']}; border-radius: 16px; color: {text_color}; }} QLabel {{ border: none; background: transparent; }}"
        )

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(20)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Breadcrumb
        self.breadcrumb_lbl = QLabel(">")
        self.breadcrumb_lbl.setStyleSheet(
            f"color: {accent_color}; font-weight: 600; padding: 12px 20px 4px 20px; font-size: 13px; font-family: 'Segoe UI', sans-serif;"
        )
        self.breadcrumb_lbl.setVisible(False)
        layout.addWidget(self.breadcrumb_lbl)

        # Search Bar
        search_container = QWidget()
        search_container.setStyleSheet("background: transparent; border: none;")
        search_layout = QVBoxLayout(search_container)
        search_layout.setContentsMargins(15, 15, 15, 15)

        self.search_bar = SearchInput()
        self.search_bar.setPlaceholderText("Type a command...")
        self.search_bar.setStyleSheet(
            f"QLineEdit {{ background-color: transparent; color: {text_color}; border: none; border-bottom: 2px solid {COLORS['glass_border']}; font-size: 20px; padding: 8px 4px; }} QLineEdit:focus {{ border-bottom: 2px solid {accent_color}; }}"
        )
        self.search_bar.textChanged.connect(self._filter_list)
        self.search_bar.installEventFilter(self)

        search_layout.addWidget(self.search_bar)
        layout.addWidget(search_container)

        # List Widget
        self.list_widget = StandardListWidget()
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.list_widget.setStyleSheet(
            f"QListWidget {{ background-color: {bg_color}; border: none; outline: none; }} QListWidget::item {{ color: {text_color}; }} QListWidget::item:selected {{ background-color: {COLORS['primary_dark']}; color: #ffffff; }} QListWidget::item:hover {{ background-color: {COLORS['glass_deep']}; }}"
        )
        self.list_widget.itemActivated.connect(self._execute_selected)
        self.list_widget.clicked.connect(self._execute_selected)
        layout.addWidget(self.list_widget)

    def show_animated(self) -> None:
        """Visualizza la palette con un'animazione a tendina dall'alto."""
        parent = self.parent()
        if not parent or not hasattr(parent, "geometry"):
            return

        # Debounce per evitare chiusure accidentali con Ctrl+K
        self._can_close_via_shortcut = False
        QTimer.singleShot(400, lambda: setattr(self, "_can_close_via_shortcut", True))

        # Reset Stato
        self.navigation_stack.clear()
        self.breadcrumb_path.clear()
        self.current_nodes = self.root_nodes
        self._populate_list(self.current_nodes)
        self._update_breadcrumb_ui()
        self.search_bar.setText("")
        self.search_bar.setFocus()

        parent_geo = parent.geometry()
        x = parent_geo.x() + (parent_geo.width() - self.width()) // 2
        start_y = parent_geo.y() + 30

        self.setGeometry(x, start_y, self.width(), 0)
        self.show()
        self.raise_()
        self.activateWindow()

        self.anim.setStartValue(QRect(x, start_y, self.width(), 0))
        self.anim.setEndValue(QRect(x, start_y, self.width(), self.target_height))
        self.anim.start()

    def hide_animated(self) -> None:
        """Chiude la palette con un'animazione a scomparsa verso l'alto."""
        if self.is_closing:
            return
        self.is_closing = True

        geo = self.geometry()
        self.anim.setStartValue(geo)
        self.anim.setEndValue(QRect(geo.x(), geo.y(), geo.width(), 0))
        self.anim.finished.connect(self._finish_close)
        self.anim.start()

    def _finish_close(self) -> None:
        """Completa la chiusura nascondendo il widget e resettando i flag."""
        self.hide()
        self.is_closing = False
        with suppress(Exception):
            self.anim.finished.disconnect(self._finish_close)
        self.closed.emit()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Gestisce la navigazione da tastiera (frecce, invio, esc) intercettando gli eventi della search bar."""
        if obj == self.search_bar and event.type() == QEvent.Type.KeyPress:
            key_event = cast("QKeyEvent", event)
            if self._input_mode:
                return self._handle_input_mode_key(key_event)
            return self._handle_standard_key(key_event)
        return super().eventFilter(obj, event)

    def _handle_input_mode_key(self, event: QKeyEvent) -> bool:
        """Gestisce i tasti speciali durante la modalità di inserimento parametri."""
        key = event.key()
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._submit_input_step()
            return True
        if key == Qt.Key.Key_Escape:
            self._cancel_input_mode()
            return True
        return False

    def _handle_standard_key(self, event: QKeyEvent) -> bool:
        """Gestisce i tasti durante la navigazione standard dei menu."""
        key = event.key()

        # 1. Navigazione Lista (Frecce)
        if key in (Qt.Key.Key_Up, Qt.Key.Key_Down):
            return self._handle_list_navigation(key)

        # 2. Esecuzione (Invio)
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._execute_selected()
            return True

        # 3. Navigazione Back / Chiusura (Esc, Backspace)
        if key in (Qt.Key.Key_Escape, Qt.Key.Key_Backspace):
            return self._handle_back_navigation(key)

        # 4. Shortcut Globale (Ctrl+K)
        if key == Qt.Key.Key_K and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if not event.isAutoRepeat() and getattr(self, "_can_close_via_shortcut", True):
                self.hide_animated()
            return True

        return False

    def _handle_list_navigation(self, key: int) -> bool:
        """Sposta la selezione nella lista dei comandi."""
        idx = self.list_widget.currentRow()
        if key == Qt.Key.Key_Down and idx < self.list_widget.count() - 1:
            self.list_widget.setCurrentRow(idx + 1)
            return True
        if key == Qt.Key.Key_Up and idx > 0:
            self.list_widget.setCurrentRow(idx - 1)
            return True
        return False

    def _handle_back_navigation(self, key: int) -> bool:
        """Gestisce il ritorno al menu precedente o la chiusura."""
        search_empty = not self.search_bar.text()

        if key == Qt.Key.Key_Backspace and search_empty:
            self._navigate_up()
            return True

        if key == Qt.Key.Key_Escape:
            if self.navigation_stack and search_empty:
                self._navigate_up()
            else:
                self.hide_animated()
            return True
        return False

    def _start_input_mode(self, node: CommandNode) -> None:
        """Avvia la procedura di richiesta parametri per un comando specifico."""
        self._input_mode = True
        self._input_prompts = node.input_prompts
        self._input_callback = node.on_input_complete
        self._input_answers = []
        self._input_index = 0

        self.list_widget.setVisible(False)
        self.breadcrumb_lbl.setVisible(True)
        self.breadcrumb_lbl.setText(f"> {node.label}")
        self._show_next_prompt()

    def _show_next_prompt(self) -> None:
        """Visualizza la richiesta per il parametro successivo."""
        if self._input_index < len(self._input_prompts):
            prompt = self._input_prompts[self._input_index]
            self.search_bar.setText("")
            self.search_bar.setPlaceholderText(f"{prompt} (Invio per confermare, Esc per annullare)")
            self.search_bar.setFocus()
        else:
            self._finish_input_mode()

    def _submit_input_step(self) -> None:
        """Raccoglie la risposta corrente e passa alla successiva."""
        val = self.search_bar.text().strip()
        if not val:
            return
        self._input_answers.append(val)
        self._input_index += 1
        self._show_next_prompt()

    def _finish_input_mode(self) -> None:
        """Esegue la callback finale con tutte le risposte raccolte e chiude la palette."""
        if self._input_callback:
            with suppress(Exception):
                self._input_callback(self._input_answers)
        self.hide_animated()

    def _cancel_input_mode(self) -> None:
        """Abbandona l'inserimento parametri e torna alla navigazione menu."""
        self._input_mode = False
        self.list_widget.setVisible(True)
        self.search_bar.setText("")
        self._update_breadcrumb_ui()
        self.search_bar.setFocus()

    def _navigate_down(self, node: CommandNode) -> None:
        """Entra in un sottomenu aggiornando la lista e i breadcrumb."""
        children = node.get_children()
        if not children:
            return
        self.navigation_stack.append((self.current_nodes, self.list_widget.currentRow()))
        self.breadcrumb_path.append(node.label)
        self.current_nodes = children
        self._populate_list(self.current_nodes)
        self._update_breadcrumb_ui()
        self.search_bar.setText("")

    def _navigate_up(self) -> None:
        """Torna al livello gerarchico superiore ripristinando lo stato precedente."""
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

    def _update_breadcrumb_ui(self) -> None:
        """Aggiorna la label dei breadcrumb per riflettere la posizione attuale nei menu."""
        if not self.breadcrumb_path:
            self.breadcrumb_lbl.setVisible(False)
            self.search_bar.setPlaceholderText("> Cerca...")
        else:
            self.breadcrumb_lbl.setVisible(True)
            path_str = " > ".join(self.breadcrumb_path)
            self.breadcrumb_lbl.setText(f"> {path_str}")
            self.search_bar.setPlaceholderText(f"Cerca dentro {self.breadcrumb_path[-1]}...")

    def _populate_list(self, nodes: list[CommandNode]) -> None:
        """Riempie la QListWidget con i nodi forniti."""
        self.list_widget.clear()
        for node in nodes:
            self._add_item(node)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _add_item(self, node: CommandNode) -> None:
        """Crea e aggiunge un elemento personalizzato (icona + testo + shortcut) alla lista."""
        item = QListWidgetItem(self.list_widget)
        item.setSizeHint(QSize(0, 50))
        widget = QWidget()
        widget.setStyleSheet("background: transparent; border: none;")
        h = QHBoxLayout(widget)
        h.setContentsMargins(10, 5, 10, 5)
        h.setSpacing(15)

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(20, 20)
        pm = get_colored_icon(get_asset_path(node.icon), COLORS["text_light"]).pixmap(20, 20)
        icon_lbl.setPixmap(pm)
        h.addWidget(icon_lbl)

        v = QVBoxLayout()
        v.setSpacing(2)
        lbl = QLabel(node.label)
        lbl.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['bg_white']};")
        v.addWidget(lbl)
        if node.description:
            desc = QLabel(node.description)
            desc.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']};")
            v.addWidget(desc)
        h.addLayout(v)
        h.addStretch()

        if not node.is_leaf:
            arrow = QLabel("  ")
            arrow.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
            h.addWidget(arrow)
        elif node.shortcut:
            sc = QLabel(node.shortcut)
            sc.setStyleSheet(f"color: {COLORS['text_muted']}; font-family: monospace;")
            h.addWidget(sc)

        item.setData(Qt.ItemDataRole.UserRole, node)
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

    def _filter_list(self, text: str) -> None:
        """Filtra i comandi in base alla ricerca, eseguendo un match ricorsivo se necessario."""
        if self._input_mode:
            return
        search = text.lower().strip()
        self.list_widget.clear()
        if not search:
            self._update_breadcrumb_ui()
            self._populate_list(self.current_nodes)
            return
        self.breadcrumb_lbl.setVisible(False)
        results: list[CommandNode] = []
        self._collect_all_nodes(self.root_nodes, search, results)
        for n in results:
            self._add_item(n)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _collect_all_nodes(self, nodes: list[CommandNode], search: str, results: list[CommandNode]) -> None:
        """Attraversa ricorsivamente l'albero dei comandi per trovare corrispondenze."""
        for node in nodes:
            match = (search in node.label.lower()) or (
                node.description and search in node.description.lower()
            )
            if match:
                results.append(node)
            children = node.get_children()
            if children:
                self._collect_all_nodes(children, search, results)

    def _execute_selected(self) -> None:
        """Esegue l'azione del nodo selezionato o entra nel sottomenu."""
        item = self.list_widget.currentItem()
        if not item:
            return
        node: CommandNode = item.data(Qt.ItemDataRole.UserRole)
        if node.input_prompts:
            self._start_input_mode(node)
            return
        if node.is_leaf:
            if node.close_on_execute:
                self.hide_animated()
            QTimer.singleShot(50, lambda: node.action() if node.action else None)
        else:
            self._navigate_down(node)
