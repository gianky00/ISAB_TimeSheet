"""
SyncroJob - PDL Programming Status Widget
Widget elegante che mostra una barra di stato verde/arancione per TCL e TGO nelle celle Gantt.
"""

import base64
import logging
from pathlib import Path

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QSizePolicy, QWidget

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path

logger = logging.getLogger(__name__)


class ProgrammingStatusWidget(QWidget):
    """Widget elegante che mostra una barra di stato verde/arancione per TCL e TGO."""

    def __init__(  # noqa: ANN204, PLR0913
        self,
        tcl: bool,
        tgo: bool,
        connect_left: bool = False,
        connect_right: bool = False,
        is_today: bool = False,
        parent=None,  # noqa: ANN001
    ):
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
                with path.open("rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                    return f"data:image/svg+xml;base64,{encoded}"
        except Exception as e:
            logger.error(f"Errore caricamento icona base64: {e}")  # noqa: TRY400
        return ""

    def _setup_tooltip(self):  # noqa: ANN202
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

    def paintEvent(self, event):  # noqa: ANN001, ANN201, PLR0915
        """Disegna la barra di stato TCL/TGO nella cella."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = float(self.width()), float(self.height())

        if self.is_today:
            c = QColor(COLORS["primary_dark"])
            painter.fillRect(self.rect(), QColor(c.red(), c.green(), c.blue(), 40))

        bar_w, bar_h = 80.0, 10.0
        x, y = (w - bar_w) / 2.0, (h - bar_h) / 2.0
        radius = 5.0

        path = QPainterPath()
        tl = 0.0 if self.connect_left else radius
        bl = 0.0 if self.connect_left else radius
        tr = 0.0 if self.connect_right else radius
        br = 0.0 if self.connect_right else radius

        path.moveTo(x + bar_w - tr, y)
        if tr > 0:
            path.arcTo(x + bar_w - 2 * tr, y, 2 * tr, 2 * tr, 90, -90)
        else:
            path.lineTo(x + bar_w, y)

        path.lineTo(x + bar_w, y + bar_h - br)
        if br > 0:
            path.arcTo(x + bar_w - 2 * br, y + bar_h - 2 * br, 2 * br, 2 * br, 0, -90)
        else:
            path.lineTo(x + bar_w, y + bar_h)

        path.lineTo(x + bl, y + bar_h)
        if bl > 0:
            path.arcTo(x, y + bar_h - 2 * bl, 2 * bl, 2 * bl, 270, -90)
        else:
            path.lineTo(x, y + bar_h)

        path.lineTo(x, y + tl)
        if tl > 0:
            path.arcTo(x, y, 2 * tl, 2 * tl, 180, -90)
        else:
            path.lineTo(x, y)
        path.closeSubpath()

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(COLORS["bg_hover"]))
        painter.drawPath(path)

        green_color, orange_color = QColor(COLORS["success_dark"]), QColor(COLORS["warning_orange"])

        if self.tcl and self.tgo:
            painter.setBrush(green_color)
            painter.drawPath(path)
        elif self.tcl:
            tcl_rect = QRectF(x, y, bar_w / 2.0 + 2.0, bar_h)
            tcl_path = QPainterPath()
            tcl_path.addRoundedRect(tcl_rect, radius, radius)
            painter.setBrush(orange_color)
            painter.drawPath(tcl_path)
        elif self.tgo:
            tgo_rect = QRectF(x + bar_w / 2.0 - 2.0, y, bar_w / 2.0 + 2.0, bar_h)
            tgo_path = QPainterPath()
            tgo_path.addRoundedRect(tgo_rect, radius, radius)
            painter.setBrush(orange_color)
            painter.drawPath(tgo_path)
