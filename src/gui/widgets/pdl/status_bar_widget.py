"""
SyncroJob - PDL Programming Status Widget
Widget elegante che mostra una barra di stato verde/arancione per TCL e TGO nelle celle Gantt.
"""

from __future__ import annotations

import base64
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath
from PySide6.QtWidgets import QSizePolicy, QWidget

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path

if TYPE_CHECKING:
    from PySide6.QtGui import QPaintEvent

logger = logging.getLogger(__name__)


class ProgrammingStatusWidget(QWidget):
    """Widget elegante che mostra una barra di stato verde/arancione per TCL e TGO."""

    def __init__(  # noqa: PLR0913
        self,
        tcl: bool,
        tgo: bool,
        connect_left: bool = False,
        connect_right: bool = False,
        is_today: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.tcl = tcl
        self.tgo = tgo
        self.connect_left = connect_left
        self.connect_right = connect_right
        self.is_today = is_today
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setMinimumHeight(16)
        self._setup_tooltip()

    def _get_icon_base64(self, icon_path: str) -> str:
        """Converte un'icona SVG in base64 per l'uso nel tooltip HTML."""
        try:
            path = Path(icon_path)
            if path.exists():
                encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
                return f"data:image/svg+xml;base64,{encoded}"
        except Exception:
            logger.exception("Errore caricamento icona base64")
        return ""

    def _setup_tooltip(self) -> None:
        """Crea un tooltip grafico con le icone di stato."""
        tcl_icon_path = get_asset_path(Icons.FLAG_TCL_ON if self.tcl else Icons.FLAG_TCL_OFF)
        tgo_icon_path = get_asset_path(Icons.FLAG_TGO_ON if self.tgo else Icons.FLAG_TGO_OFF)

        tcl_b64 = self._get_icon_base64(tcl_icon_path)
        tgo_b64 = self._get_icon_base64(tgo_icon_path)

        html = f"""
    <div style='padding: 5px; background-color: white;'>
      <img src='{tcl_b64}' width='32' height='18'>
      <img src='{tgo_b64}' width='32' height='18' style='margin-left: 5px;'>
    </div>
    """
        self.setToolTip(html)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna la barra di stato TCL/TGO nella cella."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._draw_today_highlight(painter)

        bar_w, bar_h = 80.0, 10.0
        w, h = float(self.width()), float(self.height())
        x, y = (w - bar_w) / 2.0, (h - bar_h) / 2.0
        radius = 5.0

        bar_rect = QRectF(x, y, bar_w, bar_h)
        path = self._create_bar_path(x, y, bar_w, bar_h, radius)

        # Disegna lo sfondo (vuoto/default)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(COLORS["bg_hover"]))
        painter.drawPath(path)

        # Disegna gli indicatori attivi
        self._draw_status_indicators(painter, path, bar_rect, radius)

    def _draw_today_highlight(self, painter: QPainter) -> None:
        """Disegna un'evidenziazione se la cella rappresenta il giorno corrente."""
        if self.is_today:
            c = QColor(COLORS["primary_dark"])
            highlight_opacity = 40
            painter.fillRect(self.rect(), QColor(c.red(), c.green(), c.blue(), highlight_opacity))

    def _create_bar_path(self, x: float, y: float, w: float, h: float, r: float) -> QPainterPath:
        """Crea il tracciato della barra gestendo le connessioni laterali."""
        path = QPainterPath()
        tl = 0.0 if self.connect_left else r
        bl = 0.0 if self.connect_left else r
        tr = 0.0 if self.connect_right else r
        if tr > 0:
            path.arcTo(x + w - 2 * tr, y, 2 * tr, 2 * tr, 90, -90)
        else:
            path.lineTo(x + w, y)

        # Bottom-right
        br = 0.0 if self.connect_right else r
        path.lineTo(x + w, y + h - br)
        if br > 0:
            path.arcTo(x + w - 2 * br, y + h - 2 * br, 2 * br, 2 * br, 0, -90)
        else:
            path.lineTo(x + w, y + h)

        # Bottom-left
        path.lineTo(x + bl, y + h)
        if bl > 0:
            path.arcTo(x, y + h - 2 * bl, 2 * bl, 2 * bl, 270, -90)
        else:
            path.lineTo(x, y + h)

        # Top-left
        path.lineTo(x, y + tl)
        if tl > 0:
            path.arcTo(x, y, 2 * tl, 2 * tl, 180, -90)
        else:
            path.lineTo(x, y)
        path.closeSubpath()
        return path

    def _draw_status_indicators(
        self, painter: QPainter, path: QPainterPath, rect: QRectF, r: float
    ) -> None:
        """Disegna i colori verde o arancione in base allo stato TCL/TGO."""
        green_color = QColor(COLORS["success_dark"])
        orange_color = QColor(COLORS["warning_orange"])
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

        if self.tcl and self.tgo:
            painter.setBrush(green_color)
            painter.drawPath(path)
        elif self.tcl:
            overlap = 2.0
            tcl_rect = QRectF(x, y, w / 2.0 + overlap, h)
            tcl_path = QPainterPath()
            tcl_path.addRoundedRect(tcl_rect, r, r)
            painter.setBrush(orange_color)
            painter.drawPath(tcl_path)
        elif self.tgo:
            overlap = 2.0
            tgo_rect = QRectF(x + w / 2.0 - overlap, y, w / 2.0 + overlap, h)
            tgo_path = QPainterPath()
            tgo_path.addRoundedRect(tgo_rect, r, r)
            painter.setBrush(orange_color)
            painter.drawPath(tgo_path)
