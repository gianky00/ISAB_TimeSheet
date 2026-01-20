from datetime import datetime

from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtGui import QColor, QFont

from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon


class AuditTableModel(QAbstractTableModel):
    """
    Modello dati avanzato per la tabella Audit V2.
    """

    COLUMNS = [
        "",
        "Data/Ora",
        "Durata",
        "Modulo",
        "Categoria",
        "Azione",
        "Codice/Entità",
        "Dettagli",
    ]

    def __init__(self, logs=None):
        super().__init__()
        self._logs = logs or []
        # Pre-load icons
        self._icons = {
            "high": get_colored_icon(get_asset_path(Icons.STATUS_DOT_RED), "#dc3545"),
            "medium": get_colored_icon(
                get_asset_path(Icons.STATUS_DOT_ORANGE), "#fd7e14"
            ),
            "low": get_colored_icon(get_asset_path(Icons.STATUS_DOT_GREEN), "#198754"),
            "success": get_colored_icon(
                get_asset_path(Icons.STATUS_DOT_GREEN), "#198754"
            ),
            "error": get_colored_icon(get_asset_path(Icons.STATUS_DOT_RED), "#dc3545"),
        }

    def update_data(self, logs):
        self.beginResetModel()
        self._logs = logs
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self._logs)

    def columnCount(self, parent=None):
        return len(self.COLUMNS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        log = self._logs[index.row()]
        col = index.column()
        status = str(log.get("status", "success")).lower()
        severity = str(log.get("severity", "low")).lower()

        # --- TESTO ---
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return ""
            if col == 1:
                return self._format_timestamp(log.get("timestamp"))
            if col == 2:
                return self._format_duration(log.get("duration_ms", 0))
            if col == 3:
                return str(log.get("module", "-") or "-")
            if col == 4:
                return str(log.get("category", "-"))
            if col == 5:
                return str(log.get("action", "-"))
            if col == 6:
                # Priorità a error_code se c'è, altrimenti entity
                err = log.get("error_code")
                return str(err) if err else str(log.get("entity", "-"))
            if col == 7:
                return self._extract_message(log)

        # --- ICONE ---
        if role == Qt.ItemDataRole.DecorationRole and col == 0:
            if status == "success":
                return self._icons["success"]
            if status == "error":
                return self._icons["error"]
            return self._icons.get(severity, self._icons["low"])

        # --- STILI ---
        if role == Qt.ItemDataRole.BackgroundRole:
            if status == "error":
                return QColor("#fff5f5")  # Red tint
            if severity == "medium":
                return QColor("#fff9f0")  # Orange tint

        if role == Qt.ItemDataRole.ForegroundRole:
            if col == 6 and log.get("error_code"):  # Error Code Red
                return QColor("#dc3545")
            if col == 2 and (log.get("duration_ms", 0) or 0) > 5000:  # Slow ops
                return QColor("#fd7e14")

        if role == Qt.ItemDataRole.FontRole:
            if col == 5:  # Action Bold
                f = QFont()
                f.setBold(True)
                return f
            if col == 6 and log.get("error_code"):  # Error Code Bold
                f = QFont()
                f.setBold(True)
                return f

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col in [0, 2]:
                return Qt.AlignmentFlag.AlignCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        return None

    def headerData(self, section, orientation, role):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return self.COLUMNS[section]
        return None

    def _format_timestamp(self, ts):
        try:
            # Formato completo con secondi per debug
            dt = datetime.fromisoformat(ts)
            return dt.strftime("%d/%m %H:%M:%S")
        except Exception:
            return str(ts)

    def _format_duration(self, ms):
        if not ms:
            return "-"
        if ms < 1000:
            return f"{ms}ms"
        return f"{ms/1000:.1f}s"

    def _extract_message(self, log):
        # Cerca il messaggio più utile nel JSON params
        import json

        p_str = log.get("params", "{}")
        try:
            p = json.loads(p_str) if isinstance(p_str, str) else p_str
            if "error_details" in p:
                return p["error_details"]
            if "dettagli" in p:
                return p["dettagli"]
            if "messaggio" in p:
                return p["messaggio"]
            # Fallback: primi 50 caratteri del json
            return str(p_str)[:50]
        except Exception:
            return str(p_str)

    def get_log_at(self, row):
        if 0 <= row < len(self._logs):
            return self._logs[row]
        return None
