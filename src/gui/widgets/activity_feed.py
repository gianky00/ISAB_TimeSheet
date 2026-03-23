from datetime import datetime
from typing import Any

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon
from src.utils.log_humanizer import friendly_time_delta

# Stile forzato per i tooltip in Light Mode
TOOLTIP_CSS = """
QToolTip {
    background-color: #FFFFFF;
    color: #212121;
    border: 1px solid #BBBBBB;
    border-radius: 6px;
    padding: 8px 12px;
}
"""


class ActivityItem(QFrame):
    """
    Rappresenta una singola voce nella timeline orizzontale (Compact) con animazioni moderne.
    """

    opacity_effect: QGraphicsOpacityEffect | None
    fade_in_animation: QPropertyAnimation | None

    def __init__(self, log_entry: dict[str, Any], parent: QWidget | None = None, animate: bool = True):  # noqa: ANN204, PLR0915
        super().__init__(parent)
        self.log_entry = log_entry
        self.setFrameShape(QFrame.Shape.NoFrame)

        # Determina il colore in base allo status
        status = log_entry.get("status", "success").lower()
        if status == "error":
            self.border_color = COLORS["error_red"]
            self.bg_gradient = f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})"
        elif status == "warning":
            self.border_color = COLORS["warning_yellow"]
            self.bg_gradient = f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})"
        else:
            self.border_color = COLORS["success_dark"]
            self.bg_gradient = f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})"

        self.setStyleSheet(
            f"""
            {TOOLTIP_CSS}
            ActivityItem {{
                background: {self.bg_gradient};
                border-radius: 12px;
                border-left: 4px solid {self.border_color};
                border-top: 1px solid {COLORS["border_light"]};
                border-right: 1px solid {COLORS["border_light"]};
                border-bottom: 1px solid {COLORS["border_light"]};
            }}
            ActivityItem:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS["bg_hover"]}, stop:1 {COLORS["bg_white"]});
                border-left: 4px solid {self.border_color};
                border-top: 1px solid {COLORS["border_medium"]};
                border-right: 1px solid {COLORS["border_medium"]};
                border-bottom: 1px solid {COLORS["border_medium"]};
            }}
        """
        )
        self.setFixedWidth(300)  # Leggermente più largo

        # Ombra moderna (box-shadow simulato con QGraphicsDropShadowEffect)
        # Non possiamo usare direttamente box-shadow in Qt, ma possiamo simularlo
        # con l'effetto opacity

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        # 1. Badge Stato con Icona (Stile Moderno)
        status = log_entry.get("status", "success").lower()
        if status == "error":
            icon_color = "white"
            badge_bg = COLORS["error_red"]
            icon_path = Icons.ALERT_CIRCLE
        elif status == "warning":
            icon_color = "black"
            badge_bg = COLORS["warning_yellow"]
            icon_path = Icons.ALERT_TRIANGLE
        else:
            icon_color = "white"
            badge_bg = COLORS["success_dark"]
            icon_path = Icons.CHECK_CIRCLE

        # Badge container
        badge = QLabel()
        badge.setFixedSize(32, 32)
        badge.setPixmap(get_colored_icon(get_asset_path(icon_path), icon_color).pixmap(20, 20))
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"""
            QLabel {{
                background-color: {badge_bg};
                border-radius: 16px;
                border: none;
                padding: 6px;
            }}
        """
        )
        layout.addWidget(badge)

        # 2. Contenuto Testuale (Action + Time)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)

        # Action (Full Specific Text)
        action_text = log_entry.get("action", "Azione")
        entity = log_entry.get("entity", "")

        full_text = f"{action_text} - {entity}" if entity and entity != "-" else action_text

        action_lbl = QLabel(full_text)
        action_lbl.setStyleSheet(
            f"""
            QLabel {{
                font-weight: 600;
                font-size: 14px;
                color: {COLORS["text_dark"]};
                border: none;
                background: transparent;
            }}
        """
        )
        action_lbl.setWordWrap(True)
        text_layout.addWidget(action_lbl)

        # Tooltip sull'intero widget per coerenza
        self.setToolTip(full_text)

        # Time con icona
        ts_str = log_entry.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts_str)
            time_str = f"🕐 {friendly_time_delta(ts)}"
        except ValueError:
            time_str = "🕐 --"

        time_lbl = QLabel(time_str)
        time_lbl.setStyleSheet(
            f"""
            QLabel {{
                font-size: 12px;
                color: {COLORS["text_muted"]};
                border: none;
                background: transparent;
                font-weight: 500;
            }}
        """
        )
        text_layout.addWidget(time_lbl)

        layout.addLayout(text_layout)

        # Animazione fade-in (solo se richiesta)
        if animate:
            self.opacity_effect = QGraphicsOpacityEffect(self)
            # DEBUG: Disabling effect to check painter error

            self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
            self.fade_in_animation.setDuration(600)
            self.fade_in_animation.setStartValue(0.0)
            self.fade_in_animation.setEndValue(1.0)
            self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

            # Rimuovi l'effect dopo l'animazione per evitare problemi con hover
            self.fade_in_animation.finished.connect(self._remove_opacity_effect)
        else:
            self.opacity_effect = None
            self.fade_in_animation = None

    def _remove_opacity_effect(self):  # noqa: ANN202
        """Rimuove l'effetto opacity dopo l'animazione per evitare interferenze."""
        self.setGraphicsEffect(None)

    def showEvent(self, event):  # noqa: ANN001, ANN201
        """Avvia l'animazione quando il widget viene mostrato."""
        super().showEvent(event)
        if self.opacity_effect is not None and self.fade_in_animation is not None:
            self.fade_in_animation.start()


class ActivityFeed(QWidget):
    """
    Widget che mostra una timeline orizzontale delle ultime attività.
    """

    def __init__(self, parent=None):  # noqa: ANN001, ANN204
        super().__init__(parent)
        self.setFixedHeight(90)  # Aumentato per le card più alte
        self._refreshing = False  # Flag per evitare refresh multipli
        self._setup_ui()

        # Connetti al segnale dell'AuditManager per aggiornamenti in tempo reale
        from src.core.audit_manager import AuditManager  # noqa: PLC0415

        AuditManager.instance().signals.log_added.connect(self._on_new_log_added)

    def _setup_ui(self):  # noqa: ANN202
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Scroll Area Orizzontale con scrollbar moderna
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet(
            f"""
            QScrollArea {{
                background: transparent;
                border: none;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: {COLORS["bg_light"]};
                height: 8px;
                border-radius: 4px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {COLORS["border_medium"]};
                border-radius: 4px;
                min-width: 40px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {COLORS["border_dark"]};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
                width: 0px;
            }}
        """
        )
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.feed_widget = QWidget()
        self.feed_layout = QHBoxLayout(self.feed_widget)  # Horizontal!
        self.feed_layout.setContentsMargins(0, 0, 0, 5)  # Padding for scrollbar
        self.feed_layout.setSpacing(10)
        self.feed_layout.addStretch()  # Align items to right (latest first?) or left? Let's align left.

        self.scroll_area.setWidget(self.feed_widget)
        layout.addWidget(self.scroll_area)

        # Caricamento differito per non bloccare lo splash screen
        QTimer.singleShot(800, self.refresh_feed)

    def _on_new_log_added(self, log_entry: dict[str, Any]):  # noqa: ANN202
        """Chiamato quando viene aggiunto un nuovo log all'AuditManager."""
        # Refresh della feed per mostrare il nuovo log
        self.refresh_feed()

    def refresh_feed(self):  # noqa: ANN201
        """Ricarica i log dall'AuditManager."""
        # Evita refresh multipli simultanei
        if self._refreshing:
            return

        self._refreshing = True
        try:
            # Pulisci: remove all but stretch (last item)
            while self.feed_layout.count() > 1:
                layout_item = self.feed_layout.takeAt(0)
                if layout_item:
                    widget = layout_item.widget()
                    if widget is not None:
                        if isinstance(widget, ActivityItem) and widget.fade_in_animation is not None:
                            widget.fade_in_animation.stop()
                        if widget.graphicsEffect():
                            widget.setGraphicsEffect(None)
                        widget.deleteLater()

            # Limit to 10 latest
            from src.core.audit_manager import AuditManager  # noqa: PLC0415

            logs = AuditManager.instance().get_logs(limit=10)

            if not logs:
                empty_lbl = QLabel("✨ Nessuna attività recente")
                empty_lbl.setStyleSheet(
                    f"""
                    QLabel {{
                        color: {COLORS["text_muted"]};
                        font-size: 13px;
                        font-weight: 500;
                        font-style: italic;
                        padding: 10px 20px;
                        background-color: {COLORS["bg_light"]};
                        border-radius: 8px;
                        border: 1px dashed {COLORS["border_light"]};
                    }}
                """
                )
                self.feed_layout.insertWidget(0, empty_lbl)
                return

            for log in logs:
                activity = ActivityItem(log, animate=False)
                # Insert at beginning (left)
                self.feed_layout.insertWidget(self.feed_layout.count() - 1, activity)
        finally:
            self._refreshing = False
