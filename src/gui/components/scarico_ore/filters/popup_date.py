from contextlib import suppress
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMenu,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from src.gui.widgets.core_widgets import (
    PrimaryButton,
)


class DateFilterPopupWidget(QWidget):
    """Widget filtro gerarchico per date (Anno -> Mese -> Giorno)."""

    def __init__(self, values: list[str], selected_values: list[str] | None = None) -> None:
        super().__init__()
        self.values = values
        self.applied = False
        self.raw_dates: set[str] = set()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        btn_layout = QHBoxLayout()
        btn_all = PrimaryButton("Tutti")
        btn_none = PrimaryButton("Nessuno")
        btn_ok = PrimaryButton("OK")
        for btn in (btn_all, btn_none, btn_ok):
            btn.setStyleSheet("font-size: 11px; padding: 2px;")

        btn_all.clicked.connect(self.select_all)
        btn_none.clicked.connect(self.select_none)
        btn_ok.clicked.connect(self.apply_filter)

        btn_layout.addWidget(btn_all)
        btn_layout.addWidget(btn_none)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.model = QStandardItemModel()
        self.tree.setModel(self.model)
        self.tree.setFixedHeight(300)
        self.tree.setMinimumWidth(250)

        self.model.itemChanged.connect(self._on_item_changed)

        layout.addWidget(self.tree)
        self._build_tree(values, selected_values)

    def _build_tree(self, values: list[str], selected_values: list[str] | None) -> None:
        self.raw_dates = set(values)
        structure: dict[str, dict[str, list[str]]] = self._group_dates_by_hierarchy(values)

        is_all_selected = selected_values is None
        selected_set = set(selected_values) if selected_values else set()

        for y in sorted(structure.keys(), reverse=True):
            y_item = self._create_year_item(y, structure[y], selected_set, is_all_selected)
            self.model.appendRow(y_item)

    def _group_dates_by_hierarchy(self, values: list[str]) -> dict[str, dict[str, list[str]]]:
        structure: dict[str, dict[str, list[str]]] = {}
        for v in values:
            if not v:
                continue
            with suppress(Exception):
                parts = v.split("/")
                if len(parts) == 3:
                    _, m, y = parts
                    if y not in structure:
                        structure[y] = {}
                    if m not in structure[y]:
                        structure[y][m] = []
                    structure[y][m].append(v)
        return structure

    def _create_year_item(
        self,
        year: str,
        months_map: dict[str, list[str]],
        selected_set: set[str],
        is_all: bool,
    ) -> QStandardItem:
        y_item = QStandardItem(year)
        y_item.setCheckable(True)
        y_item.setEditable(False)

        checked_months = 0
        for m in sorted(months_map.keys()):
            m_item = self._create_month_item(m, months_map[m], selected_set, is_all)
            y_item.appendRow(m_item)
            if m_item.checkState() == Qt.CheckState.Checked:
                checked_months += 1

        if checked_months == len(months_map):
            y_item.setCheckState(Qt.CheckState.Checked)
        elif checked_months > 0 or self._has_any_child_checked(y_item):
            y_item.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            y_item.setCheckState(Qt.CheckState.Unchecked)

        return y_item

    def _create_month_item(
        self,
        month_code: str,
        days: list[str],
        selected_set: set[str],
        is_all: bool,
    ) -> QStandardItem:
        m_name = self._get_month_name(month_code)
        m_item = QStandardItem(f"{m_name} ({month_code})")
        m_item.setCheckable(True)
        m_item.setEditable(False)

        checked_days = 0
        for date_str in sorted(days):
            day_part = date_str.split("/")[0]
            d_item = QStandardItem(day_part)
            d_item.setCheckable(True)
            d_item.setEditable(False)
            d_item.setData(date_str, Qt.ItemDataRole.UserRole)

            state = Qt.CheckState.Checked if (is_all or date_str in selected_set) else Qt.CheckState.Unchecked
            d_item.setCheckState(state)
            if state == Qt.CheckState.Checked:
                checked_days += 1
            m_item.appendRow(d_item)

        if checked_days == len(days):
            m_item.setCheckState(Qt.CheckState.Checked)
        elif checked_days > 0:
            m_item.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            m_item.setCheckState(Qt.CheckState.Unchecked)
        return m_item

    def _has_any_child_checked(self, item: QStandardItem) -> bool:
        for r in range(item.rowCount()):
            child = item.child(r)
            if child and child.checkState() != Qt.CheckState.Unchecked:
                return True
        return False

    def _get_month_name(self, m_str: str) -> str:
        return {
            "01": "Gennaio",
            "02": "Febbraio",
            "03": "Marzo",
            "04": "Aprile",
            "05": "Maggio",
            "06": "Giugno",
            "07": "Luglio",
            "08": "Agosto",
            "09": "Settembre",
            "10": "Ottobre",
            "11": "Novembre",
            "12": "Dicembre",
        }.get(m_str, m_str)

    def _on_item_changed(self, item: QStandardItem) -> None:
        self.model.blockSignals(True)
        state = item.checkState()
        if state != Qt.CheckState.PartiallyChecked:
            self._set_children_state(item, state)
        self._update_parent_state(item)
        self.model.blockSignals(False)

    def _set_children_state(self, item: QStandardItem, state: Qt.CheckState) -> None:
        for i in range(item.rowCount()):
            child = item.child(i)
            if child:
                child.setCheckState(state)
                self._set_children_state(child, state)

    def _update_parent_state(self, item: QStandardItem) -> None:
        parent = item.parent()
        if not parent:
            return

        checked = 0
        partial = 0
        count = parent.rowCount()

        for i in range(count):
            child = parent.child(i)
            if not child:
                continue
            s = child.checkState()
            if s == Qt.CheckState.Checked:
                checked += 1
            elif s == Qt.CheckState.PartiallyChecked:
                partial += 1

        if checked == count:
            parent.setCheckState(Qt.CheckState.Checked)
        elif checked > 0 or partial > 0:
            parent.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            parent.setCheckState(Qt.CheckState.Unchecked)

        self._update_parent_state(parent)

    def select_all(self) -> None:
        """Seleziona tutti gli elementi nel widget ad albero."""
        self.model.blockSignals(True)
        root = self.model.invisibleRootItem()
        if root:
            self._set_children_state(root, Qt.CheckState.Checked)
        self.model.blockSignals(False)
        self.model.layoutChanged.emit()

    def select_none(self) -> None:
        """Deseleziona tutti gli elementi nel widget ad albero."""
        self.model.blockSignals(True)
        root = self.model.invisibleRootItem()
        if root:
            self._set_children_state(root, Qt.CheckState.Unchecked)
        self.model.blockSignals(False)
        self.model.layoutChanged.emit()

    def apply_filter(self) -> None:
        """Applica il filtro corrente e chiude il menu di popup."""
        self.applied = True
        self._close_menu()

    def get_selected_values(self) -> list[str] | None:
        """
        Recupera la lista dei valori di data selezionati.

        Returns:
          list[str] | None: Lista delle stringhe di data selezionate o None se tutte sono selezionate.
        """
        root = self.model.invisibleRootItem()
        if not root:
            return None

        selected: list[str] = []
        all_checked_info = {"all_checked": True}

        self._collect_selected_leaves(root, selected, all_checked_info)

        if all_checked_info["all_checked"]:
            return None
        return selected

    def _collect_selected_leaves(
        self, item: QStandardItem, selected: list[str], state: dict[str, bool]
    ) -> None:
        """Helper ricorsivo per raccogliere le foglie selezionate e verificare lo stato globale."""
        for i in range(item.rowCount()):
            child = item.child(i)
            if not child:
                continue

            if child.rowCount() > 0:
                # Nodo intermedio (es: Anno, Mese)
                if child.checkState() != Qt.CheckState.Checked:
                    state["all_checked"] = False
                self._collect_selected_leaves(child, selected, state)
            # Nodo foglia (Giorno)
            elif child.checkState() == Qt.CheckState.Checked:
                val = child.data(Qt.ItemDataRole.UserRole)
                selected.append(str(val))
            else:
                state["all_checked"] = False

    def _close_menu(self) -> None:
        parent: Any = self.parent()
        while parent:
            if isinstance(parent, QMenu):
                parent.close()
                break
            parent = parent.parent()
