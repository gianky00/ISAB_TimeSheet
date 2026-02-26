from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QTreeWidgetItemIterator,
    QVBoxLayout,
    QWidget,
)

from src.core.config_manager import get_config_value, set_config_value
from src.gui.design.colors import get_palette
from src.gui.styles import COLORS
from src.gui.widgets.quick_actions import AVAILABLE_ACTIONS


class QuickActionsConfigDialog(QDialog):
    """Dialogo per configurare quali azioni rapide mostrare (ad Albero)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Configura Azioni Rapide")
        self.setFixedSize(450, 500)  # Dimensioni più compatte e fisse
        self.setModal(True)

        palette = get_palette()

        # AGGRESSIVE LOCAL OVERRIDE to ensure Dark Mode doesn't leak
        self.setStyleSheet(
            f"""
            QDialog {{
                background-color: {palette.background};
                color: {palette.on_background};
            }}
            QLabel {{
                color: {palette.on_background};
                background-color: transparent;
            }}
            QCheckBox {{
                color: {palette.on_background};
                background-color: transparent;
            }}
            QPushButton {{
                background-color: {palette.primary};
                color: {palette.on_primary};
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {palette.primary_variant};
            }}
            QPushButton:pressed {{
                background-color: {palette.primary_variant};
            }}
        """
        )

        # Load current config
        self.current_selection: list[str] = get_config_value("quick_actions", [])

        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        lbl = QLabel("Seleziona le voci da mostrare nelle Azioni Rapide:")
        lbl.setWordWrap(True)
        layout.addWidget(lbl)

        # TREE WIDGET
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(20)
        # Forced Style to ensure Light Theme inside Dialog
        self.tree.setStyleSheet(
            f"""
            QTreeWidget {{
                background-color: {palette.surface};
                color: {palette.on_background};
                border: 1px solid {palette.border};
                border-radius: 4px;
            }}
            QTreeWidget::item {{
                padding: 4px;
            }}
            QTreeWidget::item:hover {{
                background-color: {COLORS["bg_light"]};
            }}
        """
        )
        layout.addWidget(self.tree)

        # Populate Tree
        self._populate_tree()
        # NON espandere di default - l'utente espande manualmente

        # Buttons (Salva e Annulla)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        # Traduci i pulsanti in italiano
        ok_btn = buttons.button(QDialogButtonBox.StandardButton.Ok)
        if ok_btn is not None:
            ok_btn.setText("Salva")
            ok_btn.setMinimumHeight(36)

        cancel_btn = buttons.button(QDialogButtonBox.StandardButton.Cancel)
        if cancel_btn is not None:
            cancel_btn.setText("Annulla")
            cancel_btn.setMinimumHeight(36)
            cancel_btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {COLORS["text_muted"]};
                    color: {COLORS["bg_white"]};
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: 600;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    opacity: 0.8;
                }}
            """
            )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _populate_tree(self) -> None:
        """Costruisce l'albero basandosi sulla struttura 'path'."""

        # 1. Build a simplified node structure
        # nodes = { "root_name": { "child_name": { ... "leaves": [(key, text)] } } }

        # Helper to find or create a node item
        items_map: dict[tuple[str, ...], QTreeWidgetItem] = {}  # path_tuple -> QTreeWidgetItem

        def get_or_create_parent(path_tuple: tuple[str, ...]) -> QTreeWidgetItem:
            if path_tuple in items_map:
                return items_map[path_tuple]

            # Create it
            if not path_tuple:
                root = self.tree.invisibleRootItem()
                if root is None:
                    # Should not happen
                    raise RuntimeError("Invisible root item is None")
                return root

            parent_path = path_tuple[:-1]
            parent_item = get_or_create_parent(parent_path)

            name = path_tuple[-1]
            item = QTreeWidgetItem(parent_item)
            item.setText(0, name)
            # Nodi padre: NON selezionabili dall'utente (solo le foglie)
            # Rimuovere ItemIsUserCheckable per renderli non cliccabili
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)

            # Style for Group Items (bold, dark gray)
            item.setForeground(0, Qt.GlobalColor.darkGray)
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)

            items_map[path_tuple] = item
            return item

        # 2. Add leaves
        for key, meta in AVAILABLE_ACTIONS.items():
            path_list = meta.get("path", [])
            path_tuple = tuple(path_list)

            parent_item = get_or_create_parent(path_tuple)

            leaf = QTreeWidgetItem(parent_item)
            leaf.setText(0, str(meta["text"]))
            leaf.setData(0, Qt.ItemDataRole.UserRole, key)
            leaf.setFlags(leaf.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            if key in self.current_selection:
                leaf.setCheckState(0, Qt.CheckState.Checked)
            else:
                leaf.setCheckState(0, Qt.CheckState.Unchecked)

    def get_selected_actions(self) -> list[str]:
        """Ritorna la lista delle chiavi selezionate (solo foglie)."""
        selected: list[str] = []

        # Recursive check
        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            item = iterator.value()
            if item is not None:
                key = item.data(0, Qt.ItemDataRole.UserRole)
                if key and item.checkState(0) == Qt.CheckState.Checked:
                    selected.append(str(key))
            iterator += 1

        return selected

    def accept(self) -> None:
        """Salva la configurazione e chiude."""
        new_selection = self.get_selected_actions()
        set_config_value("quick_actions", new_selection)
        super().accept()
