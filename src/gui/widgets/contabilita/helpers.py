from datetime import UTC, datetime
from typing import Any

from PyQt6.QtWidgets import QTreeWidgetItem


class SortableTreeWidgetItem(QTreeWidgetItem):
    """Custom QTreeWidgetItem che implementa l'ordinamento numerico e per data."""

    def __lt__(self, other: Any) -> bool:  # noqa: ANN401
        tw = self.treeWidget()
        if tw is None or not isinstance(other, QTreeWidgetItem):
            return super().__lt__(other)

        column = tw.sortColumn()
        t1, t2 = self.text(column).strip(), other.text(column).strip()

        # 1. Date
        if "/" in t1 and "/" in t2 and len(t1) <= 10:  # noqa: PLR2004
            res = self._compare_dates(t1, t2)
            if res is not None:
                return res

        # 2. Percentage
        if "%" in t1 and "%" in t2:
            res = self._compare_numeric(t1.replace("%", ""), t2.replace("%", ""))
            if res is not None:
                return res

        # 3. Numeric
        res = self._compare_numeric(t1, t2)
        if res is not None:
            return res

        return t1.lower() < t2.lower()

    def _compare_dates(self, t1: str, t2: str) -> bool | None:
        for fmt in ("%d/%m/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(t1, fmt).replace(tzinfo=UTC) < datetime.strptime(t2, fmt).replace(
                    tzinfo=UTC
                )
            except ValueError:
                continue
        return None

    def _compare_numeric(self, t1: str, t2: str) -> bool | None:
        if not t1 or not t2:
            return None
        try:
            return float(t1.replace(",", ".")) < float(t2.replace(",", "."))
        except ValueError:
            return None
