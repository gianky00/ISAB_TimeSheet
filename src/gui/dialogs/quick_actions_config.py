from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QTreeWidgetItemIterator,
    QVBoxLayout,
)

from src.core.config_manager import get_config_value, set_config_value
from src.gui.widgets.quick_actions import AVAILABLE_ACTIONS


class QuickActionsConfigDialog(QDialog):
    """Dialogo per configurare quali azioni rapide mostrare (ad Albero)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configura Azioni Rapide")
        self.setMinimumSize(500, 600)  # Increased size and flexible width
        self.setModal(True)
        self.setModal(True)

        # AGGRESSIVE LOCAL OVERRIDE to ensure Dark Mode doesn't leak
        self.setStyleSheet(
            """
            QDialog { background-color: #ffffff; color: #000000; }
            QLabel { color: #000000; background-color: transparent; }
            QCheckBox { color: #000000; background-color: transparent; }
        """
        )

        # Load current config
        self.current_selection = get_config_value("quick_actions", [])

        self._setup_ui()

    def _setup_ui(self):
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
            """
            QTreeWidget {
                background-color: #ffffff;
                color: #212529;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:hover {
                background-color: #f8f9fa;
            }
        """
        )
        layout.addWidget(self.tree)

        # Populate Tree
        self._populate_tree()
        self.tree.expandAll()  # Show all by default for visibility

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _populate_tree(self):
        """Costruisce l'albero basandosi sulla struttura 'path'."""

        # 1. Build a simplified node structure
        # nodes = { "root_name": { "child_name": { ... "leaves": [(key, text)] } } }

        # Helper to find or create a node item
        items_map = {}  # path_tuple -> QTreeWidgetItem

        def get_or_create_parent(path_tuple):
            if path_tuple in items_map:
                return items_map[path_tuple]

            # Create it
            if len(path_tuple) == 0:
                return self.tree.invisibleRootItem()

            parent_path = path_tuple[:-1]
            parent_item = get_or_create_parent(parent_path)

            name = path_tuple[-1]
            item = QTreeWidgetItem(parent_item)
            item.setText(0, name)
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsAutoTristate
            )
            item.setCheckState(
                0, Qt.CheckState.Unchecked
            )  # Start unchecked, will update if children checked

            # Style for Group Items
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
            leaf.setText(0, meta["text"])
            leaf.setData(0, Qt.ItemDataRole.UserRole, key)
            leaf.setFlags(leaf.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            if key in self.current_selection:
                leaf.setCheckState(0, Qt.CheckState.Checked)
            else:
                leaf.setCheckState(0, Qt.CheckState.Unchecked)

    def get_selected_actions(self):
        """Ritorna la lista delle chiavi selezionate (solo foglie)."""
        selected = []

        # Recursive check
        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            item = iterator.value()
            key = item.data(0, Qt.ItemDataRole.UserRole)
            if key:  # It's a leaf setup with a key
                if item.checkState(0) == Qt.CheckState.Checked:
                    selected.append(key)
            iterator += 1

        return selected

    def accept(self):
        """Salva la configurazione e chiude."""
        new_selection = self.get_selected_actions()
        set_config_value("quick_actions", new_selection)
        super().accept()
