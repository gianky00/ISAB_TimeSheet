"""
SyncroJob - Audit Table Model
Modello per la visualizzazione tabellare dell'Audit Log di sistema.
Gestisce la formattazione, i colori e le icone degli eventi di audit.
"""

import json
from datetime import datetime
from typing import Any, ClassVar

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor, QFont, QIcon

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon


class AuditTableModel(QAbstractTableModel):
    """
    Modello dati avanzato per la tabella Audit V2.
    Fornisce decorazioni visuali (icone di stato, colori di sfondo per errori)
    e formattazione dei metadati (durata, timestamp).
    """

    COLUMNS: ClassVar[list[str]] = [
        "",
        "Data/Ora",
        "Durata",
        "Modulo",
        "Categoria",
        "Azione",
        "Codice/Entità",
        "Dettagli",
    ]

    def __init__(self, logs: list[dict[str, Any]] | None = None) -> None:
        """
        Inizializza il modello audit.

        Args:
            logs: Lista iniziale di dizionari log.
        """
        super().__init__()
        self._logs = logs or []
        # Pre-load icons
        self._icons: dict[str, QIcon] = {
            "high": get_colored_icon(get_asset_path(Icons.STATUS_DOT_RED), COLORS["error_red"]),
            "medium": get_colored_icon(get_asset_path(Icons.STATUS_DOT_ORANGE), COLORS["warning_orange"]),
            "low": get_colored_icon(get_asset_path(Icons.STATUS_DOT_GREEN), COLORS["success_dark"]),
            "success": get_colored_icon(get_asset_path(Icons.STATUS_DOT_GREEN), COLORS["success_dark"]),
            "error": get_colored_icon(get_asset_path(Icons.STATUS_DOT_RED), COLORS["error_red"]),
        }

    def update_data(self, logs: list[dict[str, Any]]) -> None:
        """
        Aggiorna l'intero set di dati del modello.

        Args:
            logs: Nuova lista di log da visualizzare.
        """
        self.beginResetModel()
        self._logs = logs
        self.endResetModel()

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        """Restituisce il numero di log presenti."""
        return len(self._logs)

    def columnCount(self, parent: QModelIndex | None = None) -> int:
        """Restituisce il numero di colonne definite."""
        return len(self.COLUMNS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Fornisce i dati per la cella specificata in base al ruolo richiesto.
        Gestisce testo, icone, font e colori.
        """
        if not index.isValid():
            return None

        log = self._logs[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            return self._get_display_data(log, col)

        if role == Qt.ItemDataRole.DecorationRole:
            return self._get_decoration_data(log, col)

        if role == Qt.ItemDataRole.BackgroundRole:
            return self._get_background_data(log)

        if role == Qt.ItemDataRole.ForegroundRole:
            return self._get_foreground_data(log, col)

        if role == Qt.ItemDataRole.FontRole:
            return self._get_font_data(log, col)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return self._get_alignment_data(col)

        return None

    def _get_display_data(self, log: dict[str, Any], col: int) -> str | None:
        """Restituisce il testo da mostrare per ogni colonna."""
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
        return None

    def _get_decoration_data(self, log: dict[str, Any], col: int) -> QIcon | None:
        """Restituisce l'icona (pallino colorato) per la colonna di stato."""
        if col != 0:
            return None

        status = str(log.get("status", "success")).lower()
        if status == "success":
            return self._icons["success"]
        if status == "error":
            return self._icons["error"]

        severity = str(log.get("severity", "low")).lower()
        return self._icons.get(severity, self._icons["low"])

    def _get_background_data(self, log: dict[str, Any]) -> QColor | None:
        """Restituisce un colore di sfondo tenue per evidenziare errori o warning."""
        status = str(log.get("status", "success")).lower()
        if status == "error":
            return QColor(COLORS["table_error_bg"])

        severity = str(log.get("severity", "low")).lower()
        if severity == "medium":
            return QColor(COLORS["table_warning_bg"])
        return None

    def _get_foreground_data(self, log: dict[str, Any], col: int) -> QColor | None:
        """Evidenzia in rosso i codici errore e in arancione le operazioni lente."""
        if col == 6 and log.get("error_code"):  # Error Code Red
            return QColor(COLORS["error_red"])
        if col == 2 and (log.get("duration_ms", 0) or 0) > 5000:  # Slow ops
            return QColor(COLORS["warning_orange"])
        return None

    def _get_font_data(self, log: dict[str, Any], col: int) -> QFont | None:
        """Applica il grassetto alle azioni e ai codici errore."""
        if col == 5:  # Action Bold
            f = QFont()
            f.setBold(True)
            return f
        if col == 6 and log.get("error_code"):  # Error Code Bold
            f = QFont()
            f.setBold(True)
            return f
        return None

    def _get_alignment_data(self, col: int) -> Qt.AlignmentFlag:
        """Restituisce l'allineamento ottimale per ogni colonna."""
        if col in (0, 2):
            return Qt.AlignmentFlag.AlignCenter
        return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        """Restituisce il nome della colonna per l'header orizzontale."""
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.COLUMNS[section]
        return None

    def _format_timestamp(self, ts: Any) -> str:
        """Formatta il timestamp ISO in formato leggibile GG/MM HH:MM:SS."""
        try:
            dt = datetime.fromisoformat(str(ts))
            return dt.strftime("%d/%m %H:%M:%S")
        except Exception:
            return str(ts)

    def _format_duration(self, ms: Any) -> str:
        """Formatta i millisecondi in secondi se superano il secondo."""
        if not ms:
            return "-"
        f_ms = float(ms)
        if f_ms < 1000:
            return f"{f_ms:.0f}ms"
        return f"{f_ms / 1000.0:.1f}s"

    def _extract_message(self, log: dict[str, Any]) -> str:
        """Estrae il messaggio più significativo dai parametri JSON del log."""
        p_str = log.get("params", "{}")
        try:
            p = json.loads(p_str) if isinstance(p_str, str) else p_str
            if "error_details" in p:
                return str(p["error_details"])
            if "dettagli" in p:
                return str(p["dettagli"])
            if "messaggio" in p:
                return str(p["messaggio"])
            return str(p_str)[:50]
        except Exception:
            return str(p_str)

    def get_log_at(self, row: int) -> dict[str, Any] | None:
        """
        Restituisce i dati completi del log alla riga specificata.

        Args:
            row: Indice della riga.

        Returns:
            dict | None: Il dizionario del log o None.
        """
        if 0 <= row < len(self._logs):
            return self._logs[row]
        return None
