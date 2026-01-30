import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QStyle,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class ColoredDotDelegate(QStyledItemDelegate):
    """Delegate personalizzato per colorare i pallini nella colonna SCAD. ISAB."""

    def paint(self, painter, option, index):
        """Disegna il pallino colorato con il numero di giorni."""
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
            painter.fillRect(option.rect, QColor("#f8f9fa"))

        try:
            parts = str(value).split()
            if len(parts) >= 2:
                days = int(parts[1])

                if days >= 10:
                    color = QColor("#198754")  # Verde
                elif days >= 0:
                    color = QColor("#fd7e14")  # Arancione
                else:
                    color = QColor("#dc3545")  # Rosso
                    days = 0

                center_x = option.rect.center().x() - 15
                center_y = option.rect.center().y()
                painter.setBrush(color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(center_x, center_y - 5, 10, 10)

                painter.setPen(QColor("#333333"))
                font = QFont()
                font.setPointSize(10)
                font.setBold(True)
                painter.setFont(font)
                text_rect = option.rect.adjusted(10, 0, 0, 0)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(days))
        except Exception as e:
            logger.error(f"Errore rendering pallino: {e}")
            super().paint(painter, option, index)

        painter.restore()


class InteractiveStatusCard(QFrame):
    """Card moderna con animazioni e ombreggiature."""

    clicked = pyqtSignal(str)

    def __init__(self, label, color, icon_path, description, filter_type, parent=None):
        super().__init__(parent)
        self.base_color = color
        self.filter_type = filter_type
        self.description = description
        self.setFixedHeight(85)  # Appiattita: ridotta da 110 a 85
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Testo tooltip più professionale
        tooltip_map = {
            "ok": "Dipendenti con ultimo accesso entro 20 giorni<br/><i>Clicca per visualizzare</i>",
            "warning": "Dipendenti con ultimo accesso tra 21 e 30 giorni<br/><i>Clicca per visualizzare</i>",
            "expired": "Dipendenti con ultimo accesso oltre 30 giorni<br/><i>Clicca per visualizzare</i>",
        }
        tooltip = f"<b>{label}</b><br/>{tooltip_map.get(filter_type, description)}"
        self.setToolTip(tooltip)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(12)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 35))
        self.setGraphicsEffect(self.shadow)

        self.setStyleSheet(
            f"""
            InteractiveStatusCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 white, stop:1 #fafbfc);
                border: 2px solid {color};
                border-radius: 10px;
            }}
            """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Emoji per contesto visivo
        emoji_map = {"ok": "✅", "warning": "⚠️", "expired": "🚫"}
        emoji_label = QLabel(emoji_map.get(filter_type, "📊"))
        emoji_label.setStyleSheet("font-size: 24px; border: none;")
        emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(emoji_label)

        self.val_text = QLabel("0")
        self.val_text.setStyleSheet(
            f"font-size: 30px; font-weight: 900; color: {color};"
        )
        self.val_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.val_text)

        layout.addLayout(left_layout)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #dee2e6; min-width: 2px;")
        layout.addWidget(line)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(3)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_title = QLabel(label.upper())
        lbl_title.setStyleSheet(
            "font-size: 14px; font-weight: 800; color: #495057; letter-spacing: 0.8px;"
        )

        lbl_desc = QLabel(description)
        lbl_desc.setStyleSheet(
            "font-size: 13px; color: #6c757d; font-weight: 600;"  # Aumentato a 13px e font-weight 600
        )
        lbl_desc.setWordWrap(False)  # Disabilita word wrap per evitare a capo
        lbl_desc.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        right_layout.addWidget(lbl_title)
        right_layout.addWidget(lbl_desc)

        layout.addLayout(right_layout)

    def enterEvent(self, event):
        self.shadow.setBlurRadius(15)
        self.shadow.setYOffset(4)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.shadow.setBlurRadius(10)
        self.shadow.setYOffset(2)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.filter_type)
        super().mousePressEvent(event)

    def setValue(self, val):
        self.val_text.setText(str(val))


def create_info_card(title):
    """Crea una card informativa con ombra e stile moderno."""
    card = QFrame()
    card_shadow = QGraphicsDropShadowEffect()
    card_shadow.setBlurRadius(12)
    card_shadow.setXOffset(0)
    card_shadow.setYOffset(2)
    card_shadow.setColor(QColor(0, 0, 0, 30))
    card.setGraphicsEffect(card_shadow)
    card.setStyleSheet(
        """
        QFrame {
            background-color: white;
            border-radius: 10px;
        }
    """
    )

    main_layout = QVBoxLayout(card)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)

    header = QLabel(title)
    header.setStyleSheet(
        """
        font-size: 14px;
        font-weight: bold;
        color: #5a5a5a;
        background-color: transparent;
        padding: 10px 12px 6px 12px;
        letter-spacing: 0.5px;
    """
    )
    main_layout.addWidget(header)

    content_widget = QWidget()
    content_widget.setStyleSheet("background-color: transparent;")
    content_layout = QVBoxLayout(content_widget)
    content_layout.setContentsMargins(12, 8, 12, 10)  # Ridotto per compattezza
    content_layout.setSpacing(8)  # Ridotto da 10 a 8

    main_layout.addWidget(content_widget)

    return card, content_layout


def create_field_row(label_text):
    """Crea una riga di campo con label e valore stilizzati."""
    container = QWidget()
    container.setStyleSheet("background-color: transparent;")
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 6)  # Ridotto da 8 a 6
    layout.setSpacing(3)  # Ridotto da 4 a 3

    label = QLabel(label_text.upper())
    label.setStyleSheet(
        """
        font-size: 13px;
        font-weight: 700;
        color: #7f8c8d;
        letter-spacing: 0.8px;
    """
    )

    value_label = QLabel("-")
    value_label.setStyleSheet(
        """
        font-size: 15px;
        color: #2c3e50;
        font-weight: 500;
        border-bottom: 1px solid #e0e0e0;
        padding-bottom: 4px;
    """
    )
    value_label.setWordWrap(True)
    value_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    layout.addWidget(label)
    layout.addWidget(value_label)

    # Restituisce il container (widget da aggiungere al layout) e la label del valore (da aggiornare)
    # Monkey-patching per compatibilità con il codice esistente che si aspetta 'value_label' come attributo?
    # No, nel codice originale:
    # widget = self._create_field_row(...)
    # self.detail_labels["ID Risorsa"] = widget
    # E poi in _update_detail:
    # widget = self.detail_labels[...]
    # value_lbl = widget.findChild(QLabel, "") ... no, come recuperava il valore?

    # Devo controllare come _update_detail usa questi widget.
    # Nel codice originale non ho letto _update_detail.
    # Leggo un attimo per essere sicuro.

    # Assegno un objectName alla value_label per ritrovarla
    value_label.setObjectName("value_label")

    return container
