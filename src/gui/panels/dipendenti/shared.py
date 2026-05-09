"""
SyncroJob - Employee Shared Components
Widget, delegate e componenti UI condivisi utilizzati nei pannelli della gestione personale.
"""

import logging
from typing import Any

from PySide6.QtCore import QEvent, QModelIndex, QPersistentModelIndex, Qt, Signal
from PySide6.QtGui import QColor, QEnterEvent, QFont, QMouseEvent, QPainter
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class ColoredDotDelegate(QStyledItemDelegate):
    """
    Delegate personalizzato per colorare i pallini nella colonna SCAD. ISAB.
    Visualizza un cerchio colorato (Verde, Arancio, Rosso) in base ai giorni rimanenti.
    """

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        """
        Disegna il pallino colorato con il numero di giorni.

        Args:
          painter: Oggetto per il disegno.
          option: Opzioni di visualizzazione.
          index: Indice del modello.
        """
        if index.column() != 0:  # Solo per la prima colonna
            super().paint(painter, option, index)
            return

        value = index.data(Qt.ItemDataRole.DisplayRole)
        if not value:
            super().paint(painter, option, index)
            return

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        elif index.row() % 2 == 1:
            painter.fillRect(option.rect, QColor(COLORS["bg_light"]))

        try:
            parts = str(value).split()
            if len(parts) >= 2:  # noqa: PLR2004
                days = int(parts[1])

                if days >= 10:  # noqa: PLR2004
                    color = QColor(COLORS["success_dark"])
                elif days >= 0:
                    color = QColor(COLORS["warning_orange"])
                else:
                    color = QColor(COLORS["error_red"])
                    days = 0

                center_x = option.rect.center().x() - 15
                center_y = option.rect.center().y()
                painter.setBrush(color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(center_x, center_y - 5, 10, 10)

                painter.setPen(QColor(COLORS["text_dark"]))
                font = QFont()
                font.setPointSize(10)
                font.setBold(True)
                painter.setFont(font)
                text_rect = option.rect.adjusted(10, 0, 0, 0)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(days))
        except Exception as e:
            logger.error(f"Errore rendering pallino: {e}")  # noqa: TRY400
            super().paint(painter, option, index)

        painter.restore()


class InteractiveStatusCard(QFrame):
    """
    Card moderna interattiva con animazioni e ombreggiature.
    Utilizzata per visualizzare i conteggi aggregati (es. Abilitati, In Scadenza, Scaduti).
    """

    clicked = Signal(str)

    def __init__(  # noqa: PLR0913
        self,
        label: str,
        color: str,
        icon_path: str,
        description: str,
        filter_type: str,
        parent: QWidget | None = None,
    ) -> None:
        """Inizializza la card di stato interattiva."""
        super().__init__(parent)
        self.base_color = color
        self.filter_type = filter_type
        self.description = description
        self.setFixedHeight(85)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._setup_style(label, color)
        self._init_layout(color, filter_type, label, description)

    def _setup_style(self, label: str, color: str) -> None:
        """Configura ombreggiatura e stile QSS."""
        # Tooltip professionale
        tooltip_map = {
            "ok": "Dipendenti con ultimo accesso entro 20 giorni<br/><i>Clicca per visualizzare</i>",
            "warning": "Dipendenti con ultimo accesso tra 21 e 30 giorni<br/><i>Clicca per visualizzare</i>",
            "expired": "Dipendenti con ultimo accesso oltre 30 giorni<br/><i>Clicca per visualizzare</i>",
        }
        self.setToolTip(f"<b>{label}</b><br/>{tooltip_map.get(self.filter_type, self.description)}")

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(12)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 35))
        self.setGraphicsEffect(self.shadow)

        self.setStyleSheet(f"""
            InteractiveStatusCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {COLORS["bg_white"]}, stop:1 {COLORS["bg_alt"]});
                border: 2px solid {color}; border-radius: 10px;
            }}
        """)

    def _init_layout(self, color: str, filter_type: str, label: str, description: str) -> None:
        """Inizializza i widget e il posizionamento degli elementi."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        # Parte Sinistra (Icona + Valore)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_map = {
            "ok": (Icons.CHECK_CIRCLE, color),
            "warning": (Icons.ALERT, color),
            "expired": (Icons.X_CIRCLE, color),
        }
        path, icon_color = icon_map.get(filter_type, (Icons.INFO, color))

        icon_label = QLabel()
        icon_label.setFixedSize(32, 32)
        pixmap = get_colored_icon(get_asset_path(path), icon_color).pixmap(32, 32)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(icon_label)

        self.val_text = QLabel("0")
        self.val_text.setStyleSheet(f"font-size: 30px; font-weight: 900; color: {color};")
        self.val_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.val_text)
        layout.addLayout(left_layout)

        # Separatore
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet(f"background-color: {COLORS['border_light']}; min-width: 2px;")
        layout.addWidget(line)

        # Parte Destra (Titolo + Descrizione)
        right_layout = QVBoxLayout()
        right_layout.setSpacing(3)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_title = QLabel(label.upper())
        lbl_title.setStyleSheet(
            f"font-size: 14px; font-weight: 800; color: {COLORS['text_dark']}; letter-spacing: 0.8px;"
        )

        lbl_desc = QLabel(description)
        lbl_desc.setStyleSheet(f"font-size: 13px; color: {COLORS['text_muted']}; font-weight: 600;")
        lbl_desc.setWordWrap(False)
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        right_layout.addWidget(lbl_title)
        right_layout.addWidget(lbl_desc)
        layout.addLayout(right_layout)

    def enterEvent(self, event: QEnterEvent) -> None:
        """Aumenta l'ombra all'ingresso del mouse."""
        self.shadow.setBlurRadius(15)
        self.shadow.setYOffset(4)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """Ripristina l'ombra all'uscita del mouse."""
        self.shadow.setBlurRadius(10)
        self.shadow.setYOffset(2)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Emette il segnale 'clicked' con il tipo di filtro."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.filter_type)
        super().mousePressEvent(event)

    def setValue(self, val: Any) -> None:
        """
        Aggiorna il valore numerico visualizzato sulla card.

        Args:
          val: Valore da visualizzare.
        """
        self.val_text.setText(str(val))


def create_info_card(title: str) -> tuple[QFrame, QVBoxLayout]:
    """
    Crea una card informativa con ombra e stile moderno.

    Args:
      title: Il titolo da visualizzare nell'header della card.

    Returns:
      tuple: (QFrame istanza card, QVBoxLayout layout del contenuto).
    """
    card = QFrame()
    card_shadow = QGraphicsDropShadowEffect()
    card_shadow.setBlurRadius(12)
    card_shadow.setXOffset(0)
    card_shadow.setYOffset(2)
    card_shadow.setColor(QColor(0, 0, 0, 30))
    card.setGraphicsEffect(card_shadow)
    card.setStyleSheet(
        f"""
    QFrame {{
      background-color: {COLORS["bg_white"]};
      border-radius: 10px;
    }}
  """
    )

    main_layout = QVBoxLayout(card)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)

    header = QLabel(title)
    header.setStyleSheet(
        f"""
    font-size: 14px;
    font-weight: bold;
    color: {COLORS["text_dark"]};
    background-color: transparent;
    padding: 10px 12px 6px 12px;
    letter-spacing: 0.5px;
  """
    )
    main_layout.addWidget(header)

    content_widget = QWidget()
    content_widget.setStyleSheet("background-color: transparent;")
    content_layout = QVBoxLayout(content_widget)
    content_layout.setContentsMargins(12, 8, 12, 10)
    content_layout.setSpacing(8)

    main_layout.addWidget(content_widget)

    return card, content_layout


def create_field_row(label_text: str) -> QWidget:
    """
    Crea una riga di campo con label e valore stilizzati (stile Material Design).

    Args:
      label_text: Il testo dell'etichetta del campo.

    Returns:
      QWidget: Il container della riga di campo.
    """
    container = QWidget()
    container.setStyleSheet("background-color: transparent;")
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 6)
    layout.setSpacing(3)

    label = QLabel(label_text.upper())
    label.setStyleSheet(
        f"""
    font-size: 13px;
    font-weight: 700;
    color: {COLORS["text_muted"]};
    letter-spacing: 0.8px;
  """
    )

    value_label = QLabel("-")
    value_label.setStyleSheet(
        f"""
    font-size: 15px;
    color: {COLORS["text_dark"]};
    font-weight: 500;
    border-bottom: 1px solid {COLORS["border_light"]};
    padding-bottom: 4px;
  """
    )
    value_label.setWordWrap(True)
    value_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    layout.addWidget(label)
    layout.addWidget(value_label)

    # Assegno un objectName alla value_label per ritrovarla
    value_label.setObjectName("value_label")

    return container
