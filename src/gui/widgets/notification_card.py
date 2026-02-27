"""
NotificationCard - Modern notification card widget con design migliorato.
Supporta gradient backgrounds, animations, rich content e inline actions.
"""

from datetime import datetime
from typing import Any, ClassVar

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QContextMenuEvent, QMouseEvent, QShowEvent
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.notification_manager import NotificationManager
from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.priority_badge import PriorityBadge
from src.utils.helpers import get_asset_path, get_colored_icon


class NotificationCard(QFrame):
    """
    Widget moderno per la visualizzazione di una singola notifica.

    Features:
    - Border 4px colorato basato su level
    - Gradient background per notifiche unread
    - Icon badge 32px circolare
    - Animazioni: fade-in, hover scale
    - Support per pin, priority badge, action buttons
    """

    # Signals
    card_clicked = pyqtSignal(str)  # notification_id
    card_deleted = pyqtSignal(str)  # notification_id
    pin_toggled = pyqtSignal(str, bool)  # notification_id, pinned
    action_triggered = pyqtSignal(str, str)  # notification_id, action_key

    # Level styles (colors, gradients, icons)
    LEVEL_STYLES: ClassVar[dict[str, dict[str, Any]]] = {
        "error": {
            "accent": COLORS["error_red"],
            "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})",
            "icon": Icons.X_CIRCLE,
            "icon_color": COLORS["error_red"],
            "badge_bg": "#FFEBEE",
        },
        "warning": {
            "accent": COLORS["warning_orange"],
            "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})",
            "icon": Icons.ALERT_TRIANGLE,
            "icon_color": COLORS["warning_orange"],
            "badge_bg": "#FFF3E0",
        },
        "success": {
            "accent": COLORS["success_dark"],
            "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})",
            "icon": Icons.CHECK_CIRCLE,
            "icon_color": COLORS["success_dark"],
            "badge_bg": "#E8F5E9",
        },
        "info": {
            "accent": COLORS["primary_blue"],
            "gradient": f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_white']}, stop:1 {COLORS['bg_white']})",
            "icon": Icons.INFO,
            "icon_color": COLORS["primary_blue"],
            "badge_bg": "#E3F2FD",
        },
    }

    def __init__(
        self,
        notification: dict[str, Any],
        parent: QWidget | None = None,
        disable_animations: bool = False,
    ) -> None:
        super().__init__(parent)
        self.notification = notification
        self.manager = NotificationManager.instance()
        self._disable_animations = disable_animations

        # Widget members (Strict Typing - Option D)
        self.pin_btn: QPushButton
        self.title_lbl: QLabel
        self.time_lbl: QLabel
        self.del_btn: QPushButton
        self.message_widget: QLabel | QTextBrowser
        self.opacity_effect: QGraphicsOpacityEffect
        self.fade_in_animation: QPropertyAnimation

        self._setup_ui()
        if not disable_animations:
            self._setup_animations()

    def _setup_ui(self) -> None:
        """Setup del layout e componenti della card."""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Get notification properties
        level = self.notification.get("level", "info").lower()
        is_read = self.notification.get("read", False)
        is_pinned = self.notification.get("pinned", False)

        # Get style for level
        style = self.LEVEL_STYLES.get(level, self.LEVEL_STYLES["info"])
        accent_color = style["accent"]
        gradient = style["gradient"]

        # Background: gradient for unread, white for read
        bg = gradient if not is_read else COLORS["bg_white"]

        # Stylesheet con border 4px e hover effect
        self.setStyleSheet(
            f"""
            NotificationCard {{
                background: {bg};
                border-radius: 12px;
                border-left: 4px solid {accent_color};
                border-top: 1px solid {COLORS['border_light']};
                border-right: 1px solid {COLORS['border_light']};
                border-bottom: 1px solid {COLORS['border_light']};
            }}
            NotificationCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['bg_hover']}, stop:1 {COLORS['bg_white']});
                border-left: 4px solid {accent_color};
                border-top: 1px solid {COLORS['border_medium']};
                border-right: 1px solid {COLORS['border_medium']};
                border-bottom: 1px solid {COLORS['border_medium']};
            }}
            QToolTip {{
                background-color: {COLORS['bg_white']};
                color: {COLORS['text_dark']};
                border: 1px solid {COLORS['border_dark']};
                border-radius: 4px;
                padding: 5px;
            }}
        """
        )

        # Main layout (optimized spacing)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 10, 12, 10)  # Reduced from 16,12
        main_layout.setSpacing(6)  # Reduced from 8

        # === HEADER ===
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        # Pin button (using text emoji instead of icon)
        self.pin_btn = QPushButton()
        pin_text = "📌" if is_pinned else "📍"
        self.pin_btn.setText(pin_text)
        self.pin_btn.setFixedSize(24, 24)
        self.pin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pin_btn.setToolTip("Fissa notifica" if not is_pinned else "Rimuovi pin")
        self.pin_btn.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {COLORS['text_muted']};
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: {COLORS['text_dark']};
                background: {COLORS['bg_hover']};
                border-radius: 4px;
            }}
        """
        )
        self.pin_btn.clicked.connect(self._toggle_pin)
        header_layout.addWidget(self.pin_btn)

        badge = QLabel()
        badge.setFixedSize(36, 36)
        icon_path = style["icon"]
        icon_color = style["icon_color"]
        badge_bg = style["badge_bg"]
        badge.setPixmap(get_colored_icon(get_asset_path(icon_path), icon_color).pixmap(20, 22))
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"""
            QLabel {{
                background-color: {badge_bg};
                border-radius: 18px;
                border: 1px solid {accent_color}30;
            }}
        """
        )
        header_layout.addWidget(badge)

        # Title
        title = self.notification.get("title", "Notifica")
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet(
            f"""
            QLabel {{
                font-weight: 600;
                font-size: 14px;
                color: {COLORS['text_dark']};
                border: none;
                background: transparent;
            }}
        """
        )
        self.title_lbl.setWordWrap(False)
        header_layout.addWidget(self.title_lbl, 1)  # Stretch

        # Timestamp
        try:
            raw_ts = self.notification.get("timestamp")
            if isinstance(raw_ts, str):
                ts = datetime.fromisoformat(raw_ts)
                time_str = self._format_time(ts)
            else:
                time_str = ""
        except Exception:
            time_str = ""

        self.time_lbl = QLabel(time_str)
        self.time_lbl.setStyleSheet(
            f"""
            QLabel {{
                color: {COLORS['text_muted']};
                font-size: 12px;
                font-weight: 500;
                border: none;
                background: transparent;
            }}
        """
        )
        header_layout.addWidget(self.time_lbl)

        # Delete button
        self.del_btn = QPushButton()
        self.del_btn.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), COLORS["text_muted"]))
        self.del_btn.setIconSize(QSize(14, 14))
        self.del_btn.setFixedSize(24, 24)
        self.del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.del_btn.setToolTip("Elimina")
        self.del_btn.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {COLORS['text_light']};
            }}
            QPushButton:hover {{
                color: {COLORS['error_red']};
                background: {hex_to_rgba(COLORS['error_red'], 0.1)};
                border-radius: 4px;
            }}
        """
        )
        self.del_btn.clicked.connect(self._delete)
        header_layout.addWidget(self.del_btn)

        main_layout.addLayout(header_layout)

        # === BODY === (with markdown support, optimized)
        message = str(self.notification.get("message", ""))

        # Check for HTML tags to force RichText mode
        has_html = "<" in message and ">" in message
        has_markdown = any(char in message for char in ("*", "`", "[", "]", "\n"))

        if has_html or has_markdown or len(message) > 200:
            # Use QTextBrowser for rich content or long text
            html_message = self._markdown_to_html(message) if not has_html else message
            browser = QTextBrowser()
            browser.setHtml(html_message)
            browser.setOpenExternalLinks(True)
            browser.setFrameShape(QFrame.Shape.NoFrame)
            browser.setMaximumHeight(150)
            self.message_widget = browser
        else:
            # Use lightweight QLabel for simple short text
            lbl = QLabel(message)
            lbl.setWordWrap(True)
            lbl.setTextFormat(Qt.TextFormat.PlainText)
            lbl.setMaximumHeight(100)
            self.message_widget = lbl

        self.message_widget.setStyleSheet(
            f"""
            QTextBrowser, QLabel {{
                color: {COLORS['text_dark']};
                font-size: 13px;
                border: none;
                background: transparent;
            }}
        """
        )
        main_layout.addWidget(self.message_widget)

        # === FOOTER === (tags, priority badge, action buttons)
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(8)

        # Category tag (if present)
        category = self.notification.get("category", "system")
        if category and category != "system":
            category_label = QLabel(f"🏷️ {category.capitalize()}")
            category_label.setStyleSheet(
                f"""
                QLabel {{
                    background-color: {COLORS['table_info_bg']};
                    color: {COLORS['primary_dark']};
                    border-radius: 12px;
                    padding: 4px 10px;
                    font-size: 11px;
                    font-weight: 600;
                    border: none;
                }}
            """
            )
            footer_layout.addWidget(category_label)

        # Priority badge (if not low)
        priority = self.notification.get("priority", "low")
        if priority != "low":
            priority_badge = PriorityBadge(priority)
            footer_layout.addWidget(priority_badge)

        footer_layout.addStretch()

        # Action buttons (if present)
        actions = self.notification.get("actions", [])
        for action in actions:
            btn = ModernButton(
                text=action.get("label", ""),
                variant=action.get("variant", ModernButton.Variant.GHOST),
                size=ModernButton.Size.SMALL,
            )
            btn.setFixedHeight(32)
            btn.setMinimumWidth(80)
            # Store action key in button property for retrieval
            btn.setProperty("action_key", action.get("key", ""))
            btn.clicked.connect(lambda checked, a=action: self._on_action_clicked(a))
            footer_layout.addWidget(btn)

        # Only add footer if it has content
        if footer_layout.count() > 1 or actions:  # >1 because of stretch
            main_layout.addLayout(footer_layout)

    def _setup_animations(self) -> None:
        """Setup fade-in animation."""
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(400)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Remove effect after animation to avoid hover issues
        self.fade_in_animation.finished.connect(self._remove_opacity_effect)

    def _remove_opacity_effect(self) -> None:
        """Rimuove opacity effect dopo animazione."""
        self.setGraphicsEffect(None)

    def showEvent(self, event: QShowEvent | None) -> None:
        """Avvia animazione quando widget mostrato."""
        super().showEvent(event)
        if not self._disable_animations and hasattr(self, "fade_in_animation"):
            self.fade_in_animation.start()

    def _markdown_to_html(self, text: str) -> str:
        """
        Convert simple markdown to HTML (optimized).

        Supports:
        - **bold** → <b>bold</b>
        - *italic* → <i>italic</i>
        - `code` → <code style='background:{COLORS["bg_alt"]};padding:2px 4px;border-radius:3px'>code</code>
        - [link](url) → <a href='url'>link</a>
        - Newlines → <br>
        """
        # Fast path: if no markdown syntax, return as-is with just <br> for newlines
        if not any(char in text for char in ("*", "`", "[", "]", "(", ")")) and "\n" not in text:
            return text

        import re

        html = text

        # Bold: **text** → <b>text</b>
        if "**" in html:
            html = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html)

        # Italic: *text* → <i>text</i>
        if "*" in html:
            html = re.sub(r"\*(.+?)\*", r"<i>\1</i>", html)

        # Inline code: `code` → <code>code</code>
        if "`" in html:
            html = re.sub(
                r"`(.+?)`",
                r"<code style='background:"
                + COLORS["bg_alt"]
                + ";padding:2px 4px;border-radius:3px;font-family:monospace'>\\1</code>",
                html,
            )

        # Links: [text](url) → <a href='url'>text</a>
        if "[" in html and "]" in html:
            html = re.sub(r"\[(.+?)\]\((.+?)\)", r"<a href='\2'>\1</a>", html)

        # Newlines → <br>
        if "\n" in html:
            html = html.replace("\n", "<br>")

        return html

    def _format_time(self, dt: datetime) -> str:
        """Format timestamp in friendly format."""
        now = datetime.now()
        diff = now - dt

        if diff.days == 0:
            # Today
            hours = diff.seconds // 3600
            if hours == 0:
                minutes = diff.seconds // 60
                if minutes == 0:
                    return "Adesso"
                return f"{minutes}m fa"
            return f"{hours}h fa"
        if diff.days == 1:
            return "Ieri"
        if diff.days < 7:
            return f"{diff.days} giorni fa"
        return dt.strftime("%d/%m/%Y")

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """Mark as read when clicked."""
        if not self.notification.get("read", False):
            self.manager.mark_as_read(self.notification["id"])
            # Emit signal
            self.card_clicked.emit(self.notification["id"])
        if event:
            super().mousePressEvent(event)

    def _on_action_clicked(self, action: dict[str, Any]) -> None:
        """Handle action button click."""
        action_key = action.get("key", "")
        if action_key:
            self.action_triggered.emit(self.notification["id"], action_key)

    def _delete(self) -> None:
        """Delete notification."""
        self.manager.delete_notification(self.notification["id"])
        self.card_deleted.emit(self.notification["id"])

    def _toggle_pin(self) -> None:
        """Toggle pin status."""
        current_pinned = self.notification.get("pinned", False)
        new_pinned = not current_pinned
        # Update via manager
        if hasattr(self.manager, "pin_notification"):
            self.manager.pin_notification(self.notification["id"], new_pinned)
        self.pin_toggled.emit(self.notification["id"], new_pinned)

    def contextMenuEvent(self, event: QContextMenuEvent | None) -> None:
        """Show context menu on right-click (lazy creation)."""
        if event is None:
            return
        # Create menu on-demand for better performance
        menu = self._create_context_menu()
        menu.exec(event.globalPos())

    def _create_context_menu(self) -> QMenu:
        """Create context menu (called on-demand)."""
        menu = QMenu(self)

        # Mark as read/unread
        is_read = self.notification.get("read", False)
        mark_text = "Segna come non letta" if is_read else "Segna come letta"
        mark_action = QAction(mark_text, self)
        if is_read:
            if hasattr(self.manager, "update_notification"):
                mark_action.triggered.connect(
                    lambda: self.manager.update_notification(self.notification["id"], {"read": False})
                )
        else:
            mark_action.triggered.connect(lambda: self.manager.mark_as_read(self.notification["id"]))
        menu.addAction(mark_action)

        # Pin/Unpin
        is_pinned = self.notification.get("pinned", False)
        pin_text = "Rimuovi pin" if is_pinned else "Fissa"
        pin_action = QAction(pin_text, self)
        if hasattr(self.manager, "pin_notification"):
            pin_action.triggered.connect(
                lambda: self.manager.pin_notification(self.notification["id"], not is_pinned)
            )
        menu.addAction(pin_action)

        menu.addSeparator()

        # Copy text
        copy_text_action = QAction("Copia testo", self)
        copy_text_action.triggered.connect(self._copy_text)
        menu.addAction(copy_text_action)

        # Delete
        delete_action = QAction("Elimina", self)
        delete_action.triggered.connect(self._delete)
        menu.addAction(delete_action)

        return menu

    def _copy_link(self) -> None:
        """Copy related link to clipboard."""
        from PyQt6.QtGui import QGuiApplication

        related_id = self.notification.get("related_id", "")
        link = f"syncrojob://audit/{related_id}"  # Custom URL scheme
        clipboard = QGuiApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(link)

    def _copy_text(self) -> None:
        """Copy notification text to clipboard."""
        from PyQt6.QtGui import QGuiApplication

        title = self.notification.get("title", "")
        message = self.notification.get("message", "")
        text = f"{title}\n\n{message}"
        clipboard = QGuiApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(text)
