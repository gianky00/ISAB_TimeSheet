from contextlib import suppress
from typing import Any, Dict, List, Optional, Set

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMenu,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


class DateFilterPopupWidget(QWidget):
    """Widget filtro gerarchico per date (Anno -> Mese -> Giorno)."""

    def __init__(
        self, values: List[str], selected_values: Optional[List[str]] = None
    ) -> None:
        super().__init__()
        self.values = values
        self.applied = False
        self.raw_dates: Set[str] = set()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        btn_layout = QHBoxLayout()
        btn_all = QPushButton("Tutti")
        btn_none = QPushButton("Nessuno")
        btn_ok = QPushButton("OK")
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

    def _build_tree(
        self, values: List[str], selected_values: Optional[List[str]]
    ) -> None:
        self.raw_dates = set(values)
        structure: Dict[str, Dict[str, List[str]]] = self._group_dates_by_hierarchy(
            values
        )

        is_all_selected = selected_values is None
        selected_set = set(selected_values) if selected_values else set()

        for y in sorted(structure.keys(), reverse=True):
            y_item = self._create_year_item(
                y, structure[y], selected_set, is_all_selected
            )
            self.model.appendRow(y_item)

    def _group_dates_by_hierarchy(
        self, values: List[str]
    ) -> Dict[str, Dict[str, List[str]]]:
        structure: Dict[str, Dict[str, List[str]]] = {}
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
        months_map: Dict[str, List[str]],
        selected_set: Set[str],
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
        days: List[str],
        selected_set: Set[str],
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

            state = (
                Qt.CheckState.Checked
                if (is_all or date_str in selected_set)
                else Qt.CheckState.Unchecked
            )
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
        self.model.blockSignals(True)
        root = self.model.invisibleRootItem()
        if root:
            self._set_children_state(root, Qt.CheckState.Checked)
        self.model.blockSignals(False)
        self.model.layoutChanged.emit()

    def select_none(self) -> None:
        self.model.blockSignals(True)
        root = self.model.invisibleRootItem()
        if root:
            self._set_children_state(root, Qt.CheckState.Unchecked)
        self.model.blockSignals(False)
        self.model.layoutChanged.emit()

    def apply_filter(self) -> None:
        self.applied = True
        self._close_menu()

    def get_selected_values(self) -> Optional[List[str]]:
        selected: List[str] = []
        root = self.model.invisibleRootItem()
        if not root:
            return None

        all_checked = True

        stack = [root.child(i) for i in range(root.rowCount())]
        while stack:
            # Type assertion per mypy
            item: QStandardItem = stack.pop()  # type: ignore[assignment]
            if item.rowCount() > 0:
                if item.checkState() != Qt.CheckState.Checked:
                    all_checked = False
                stack.extend([item.child(i) for i in range(item.rowCount())])
            else:
                if item.checkState() == Qt.CheckState.Checked:
                    # Rimuoviamo il cast Any se data ritorna Any correttamente
                    val = item.data(Qt.ItemDataRole.UserRole)
                    selected.append(str(val))
                else:
                    all_checked = False

        if all_checked:
            return None
        return selected

    def _close_menu(self) -> None:
        parent: Any = self.parent()
        while parent:
            if isinstance(parent, QMenu):
                parent.close()
                break
            parent = parent.parent()
