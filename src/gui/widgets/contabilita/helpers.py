from datetime import datetime

from PyQt6.QtWidgets import QTreeWidgetItem


class SortableTreeWidgetItem(QTreeWidgetItem):
    """Custom QTreeWidgetItem che implementa l'ordinamento numerico e per data."""

    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        text1 = self.text(column).strip()
        text2 = other.text(column).strip()

        # Date Sorting
        if "/" in text1 and "/" in text2 and len(text1) <= 10:
            try:
                for fmt in ("%d/%m/%Y", "%Y/%m/%d"):
                    try:
                        dt1 = datetime.strptime(text1, fmt)
                        dt2 = datetime.strptime(text2, fmt)
                        return dt1 < dt2
                    except ValueError:
                        continue
            except Exception:
                pass

        # Percentage Sorting
        if "%" in text1 and "%" in text2:
            try:
                v1 = float(text1.replace("%", "").replace(",", ".").strip())
                v2 = float(text2.replace("%", "").replace(",", ".").strip())
                return v1 < v2
            except Exception:
                pass

        # Numeric Sorting
        if text1 and text2:
            try:
                v1 = float(text1.replace(",", "."))
                v2 = float(text2.replace(",", "."))
                return v1 < v2
            except Exception:
                pass

        return text1.lower() < text2.lower()
