"""
SyncroJob - Sidebar Widget (Premium Spectacular V8)
Perfezionamento Track: Navigazione magnetica estesa alle sottoschede.
Prioritizza la selezione specifica dei figli per un feedback visivo millimetrico.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence

from PyQt6.QtCore import (  # type: ignore[attr-defined]
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRect,
    Qt,
    QTimer,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import QPixmap
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
from src.gui.styles.palette_helpers import hex_to_rgba
from src.gui.widgets.sidebar_button import SidebarButton
from src.utils.helpers import get_asset_path


class SidebarChildButton(SidebarButton):
    """Pulsante figlio con stile Glass specifico e indentazione."""

    def _update_style(self) -> None:
        super()._update_style()
        if not self._collapsed:
            current_style = self.styleSheet()
            new_style = current_style.replace("padding: 12px 15px;", "padding: 10px 10px 10px 35px;")
            self.setStyleSheet(new_style)


class SidebarGroup(QWidget):
    """Gruppo espandibile con Accordion logic per sottomenu."""

    expanded = pyqtSignal(object)

    def __init__(self, title: str, icon_path: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 10, 0)
        header_layout.setSpacing(0)

        self.header_btn = SidebarButton(title, icon_path)
        header_layout.addWidget(self.header_btn, stretch=1)

        self.arrow_label = QLabel()
        self.arrow_label.setFixedSize(16, 16)
        self._set_arrow_icon(expanded=False)
        header_layout.addWidget(self.arrow_label)

        self.main_layout.addWidget(header_container)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(2)
        self.content_area.setVisible(False)
        self.main_layout.addWidget(self.content_area)

        self.header_btn.clicked.connect(self.toggle_group)
        self.children_btns: list[SidebarButton] = []
        self._was_expanded = False

    def _set_arrow_icon(self, expanded: bool) -> None:
        from src.utils.helpers import get_colored_icon

        icon_enum = Icons.CHEVRON_DOWN if expanded else Icons.CHEVRON_RIGHT
        icon = get_colored_icon(get_asset_path(icon_enum), COLORS["bg_white"])
        self.arrow_label.setPixmap(icon.pixmap(12, 12))

    def toggle_group(self) -> None:
        is_opening = not self.content_area.isVisible()
        self.content_area.setVisible(is_opening)
        self._set_arrow_icon(is_opening)
        if is_opening:
            self._was_expanded = True
            self.expanded.emit(self)
        else:
            self._was_expanded = False

    def collapse(self) -> None:
        self.content_area.setVisible(False)
        self._was_expanded = False
        self._set_arrow_icon(False)

    def add_child(self, btn: SidebarButton) -> None:
        self.content_layout.addWidget(btn)
        self.children_btns.append(btn)

    def set_collapsed(self, collapsed: bool) -> None:
        self.header_btn.set_collapsed(collapsed)
        self.arrow_label.setVisible(not collapsed)
        has_active_child = False
        for btn in self.children_btns:
            btn.set_collapsed(collapsed)
            if btn.isChecked():
                has_active_child = True
            if collapsed:
                btn.setVisible(btn.isChecked())
            else:
                btn.setVisible(True)
        if collapsed:
            self.content_area.setVisible(has_active_child)
        else:
            self.content_area.setVisible(self._was_expanded)
        self._set_arrow_icon(self.content_area.isVisible() and not collapsed)

    def set_active_index(self, index: int, group_indices: Sequence[int]) -> None:
        is_child_active = index in group_indices
        self.header_btn.setChecked(is_child_active)
        for btn, idx in zip(self.children_btns, group_indices, strict=False):
            is_this_checked = idx == index
            btn.setChecked(is_this_checked)
            if self.header_btn._collapsed:
                btn.setVisible(is_this_checked)
        if is_child_active:
            self.content_area.setVisible(True)
            if not self.header_btn._collapsed:
                self._was_expanded = True
        self._set_arrow_icon(self.content_area.isVisible() and not self.header_btn._collapsed)


class SidebarWidget(QFrame):
    """
    Sidebar Enterprise con animazioni Ultra-Smooth e Design d'Elite.
    """

    navigation_requested = pyqtSignal(int)
    automation_tab_requested = pyqtSignal(int)
    notifications_tab_requested = pyqtSignal(int)
    palette_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebarFrame")
        self._is_collapsed = True
        self.expanded_width = 245
        self.collapsed_width = 75

        self._width_anim = QPropertyAnimation(self, b"sidebar_width")
        self._width_anim.setDuration(300)
        self._width_anim.setEasingCurve(QEasingCurve.Type.OutQuart)

        self._track_anim = QPropertyAnimation(None, b"geometry")
        self._track_anim.setDuration(400)
        self._track_anim.setEasingCurve(QEasingCurve.Type.OutQuint)

        self.setMinimumWidth(self.collapsed_width)
        self.setMaximumWidth(self.collapsed_width)
        self.setMinimumHeight(102)
        self.setMaximumHeight(102) # Altezza fissa iniziale (solo logo)
        self.setMouseTracking(True)
        self.setStyleSheet(self._get_glass_style(collapsed=True))

        self._setup_ui()
        self._update_ui_state()
        QTimer.singleShot(500, self._update_track_instant)

    @pyqtProperty(int)
    def sidebar_width(self) -> int:
        return self.minimumWidth()

    @sidebar_width.setter  # type: ignore[no-redef]
    def sidebar_width(self, w: int) -> None:
        self.setMinimumWidth(w)
        self.setMaximumWidth(w)

    def _get_glass_style(self, collapsed: bool = False) -> str:
        if collapsed:
            return """
                QFrame#sidebarFrame {
                    background: transparent;
                    border: none;
                }
                QScrollArea { border: none; background: transparent; }
                QScrollArea > QWidget > QWidget { background: transparent; }
                QWidget#scrollContent { background: transparent; }
            """
        return f"""
            QFrame#sidebarFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS["glass_dark"]}, stop:1 {COLORS["glass_deep"]});
                border-right: 1px solid {COLORS["glass_border"]};
                border-radius: 15px;
            }}
            QScrollArea {{ border: none; background: transparent; }}
            QScrollArea > QWidget > QWidget {{ background: transparent; }}
            QWidget#scrollContent {{ background: transparent; }}
            QScrollBar:vertical {{ border: none; background: transparent; width: 4px; }}
            QScrollBar::handle:vertical {{ background: {hex_to_rgba(COLORS["bg_white"], 0.1)}; border-radius: 2px; }}
        """

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(0)

        # Header
        self.header_container = QWidget()
        h_layout = QHBoxLayout(self.header_container)
        h_layout.setContentsMargins(12, 5, 10, 15)
        h_layout.setSpacing(12)

        self.logo_badge = QFrame()
        self.logo_badge.setFixedSize(42, 42)
        self.logo_badge.setStyleSheet("background: white; border-radius: 21px;")
        logo_layout = QVBoxLayout(self.logo_badge)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_icon = QLabel()
        pix = QPixmap(get_asset_path("assets/app.ico"))
        if not pix.isNull():
            self.logo_icon.setPixmap(
                pix.scaled(
                    28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                )
            )
        logo_layout.addWidget(self.logo_icon)
        h_layout.addWidget(self.logo_badge)

        self.logo_label = QLabel("SyncroJob")
        self.logo_label.setStyleSheet("font-size: 18px; font-weight: 900; color: white;")
        self.logo_opacity = QGraphicsOpacityEffect(self.logo_label)
        self.logo_label.setGraphicsEffect(self.logo_opacity)
        h_layout.addWidget(self.logo_label)
        layout.addWidget(self.header_container)

        # Menu Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_content = QWidget()
        self.menu_layout = QVBoxLayout(self.scroll_content)
        self.menu_layout.setContentsMargins(5, 0, 5, 0)
        self.menu_layout.setSpacing(6)

        # Pulsanti
        self.btn_palette = SidebarButton("Apri Palette", get_asset_path(Icons.COMMAND_PALETTE))
        self.btn_home = SidebarButton("Home", get_asset_path(Icons.HOME))
        self.group_automazioni = SidebarGroup("Automazioni", get_asset_path(Icons.CPU))
        self.group_db = SidebarGroup("Database", get_asset_path(Icons.DATABASE))
        self.btn_lyra = SidebarButton("Lyra AI", get_asset_path(Icons.SPARKLES))
        self.group_notifiche = SidebarGroup("Monitoraggio", get_asset_path(Icons.ACTIVITY))

        self.main_btns: list[SidebarButton | SidebarGroup] = [
            self.btn_palette,
            self.btn_home,
            self.group_automazioni,
            self.group_db,
            self.btn_lyra,
            self.group_notifiche,
        ]
        for btn in self.main_btns:
            self.menu_layout.addWidget(btn)
            if isinstance(btn, SidebarGroup):
                btn.expanded.connect(self._on_group_expanded)

        # Sotto-pulsanti
        self.btn_fornitori = SidebarChildButton("Portale Fornitori", get_asset_path(Icons.GLOBE))
        self.btn_safework = SidebarChildButton("SafeWork", get_asset_path(Icons.SHIELD))
        self.group_automazioni.add_child(self.btn_fornitori)
        self.group_automazioni.add_child(self.btn_safework)

        self.btn_timbrature = SidebarChildButton("Timbrature", get_asset_path(Icons.CLOCK))
        self.btn_strumentale = SidebarChildButton("Strumentale", get_asset_path(Icons.FOLDER))
        self.btn_dataease = SidebarChildButton("DataEase", get_asset_path(Icons.DOWNLOAD))
        self.btn_pdl = SidebarChildButton("PDL", get_asset_path(Icons.PDL))
        self.btn_dipendenti = SidebarChildButton("Dipendenti", get_asset_path(Icons.DIPENDENTI))
        self.btn_storico_oda = SidebarChildButton("Storico OdA", get_asset_path(Icons.FILE_TEXT))
        self.db_child_btns: list[SidebarChildButton] = [
            self.btn_timbrature,
            self.btn_strumentale,
            self.btn_dataease,
            self.btn_pdl,
            self.btn_dipendenti,
            self.btn_storico_oda,
        ]
        for b in self.db_child_btns:
            self.group_db.add_child(b)

        self.btn_notifiche = SidebarChildButton("Notifiche", get_asset_path(Icons.BELL))
        self.btn_audit = SidebarChildButton("Audit", get_asset_path(Icons.SHIELD))
        self.btn_health = SidebarChildButton("Health", get_asset_path(Icons.ACTIVITY))
        self.notif_child_btns: list[SidebarChildButton] = [
            self.btn_notifiche,
            self.btn_audit,
            self.btn_health,
        ]
        for b in self.notif_child_btns:
            self.group_notifiche.add_child(b)

        self.menu_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Footer
        self.footer = QWidget()
        f_layout = QVBoxLayout(self.footer)
        f_layout.setContentsMargins(5, 10, 5, 0)
        self.btn_help = SidebarButton("Guida", get_asset_path(Icons.HELP))
        self.btn_settings = SidebarButton("Impostazioni", get_asset_path(Icons.SETTINGS))
        self.footer_btns: list[SidebarButton] = [self.btn_help, self.btn_settings]
        for footer_btn in self.footer_btns:
            f_layout.addWidget(footer_btn)
        layout.addWidget(self.footer)

        # Nascondi elementi se parte collassata
        if self._is_collapsed:
            self.scroll_area.setVisible(False)
            self.footer.setVisible(False)

        # Indicatore
        self.active_track = QWidget(self)
        self.active_track.setFixedWidth(5)
        self.active_track.setStyleSheet(f"background: {COLORS['teal_accent']}; border-radius: 2px;")
        self.active_track.raise_()
        self._track_anim.setTargetObject(self.active_track)

        self._setup_connections()

    def _setup_connections(self) -> None:
        self.btn_palette.clicked.connect(self.palette_requested.emit)
        self.btn_home.clicked.connect(lambda: self.navigation_requested.emit(0))
        self.btn_fornitori.clicked.connect(lambda: self._handle_automazione_click(0))
        self.btn_safework.clicked.connect(lambda: self._handle_automazione_click(1))
        self.btn_timbrature.clicked.connect(lambda: self.navigation_requested.emit(3))
        self.btn_strumentale.clicked.connect(lambda: self.navigation_requested.emit(4))
        self.btn_dataease.clicked.connect(lambda: self.navigation_requested.emit(5))
        self.btn_pdl.clicked.connect(lambda: self.navigation_requested.emit(6))
        self.btn_dipendenti.clicked.connect(lambda: self.navigation_requested.emit(11))
        self.btn_storico_oda.clicked.connect(lambda: self.navigation_requested.emit(10))
        self.btn_lyra.clicked.connect(lambda: self.navigation_requested.emit(2))
        self.btn_notifiche.clicked.connect(lambda: self._handle_notifications_click(0))
        self.btn_audit.clicked.connect(lambda: self._handle_notifications_click(1))
        self.btn_health.clicked.connect(lambda: self._handle_notifications_click(2))
        self.btn_help.clicked.connect(lambda: self.navigation_requested.emit(8))
        self.btn_settings.clicked.connect(lambda: self.navigation_requested.emit(7))

    def _on_group_expanded(self, group: SidebarGroup) -> None:
        for g in (self.group_automazioni, self.group_db, self.group_notifiche):
            if g != group:
                g.collapse()
        QTimer.singleShot(100, self._update_track)

    def _animate_track(self, target_widget: QWidget) -> None:
        if not target_widget or not target_widget.isVisible():
            return
        pos = target_widget.mapTo(self, QPoint(0, 0))
        target_rect = QRect(2, pos.y() + 8, 5, target_widget.height() - 16)
        self.active_track.show()
        self._track_anim.stop()
        self._track_anim.setEndValue(target_rect)
        self._track_anim.start()

    def _update_track(self) -> None:
        """Cerca il pulsante attivo dando priorità alle sottoschede."""
        # 1. Priorità: Sottoschede (Child Buttons)
        # Includiamo esplicitamente anche i figli di automazioni
        automazioni_children = [self.btn_fornitori, self.btn_safework]
        all_children = automazioni_children + self.db_child_btns + self.notif_child_btns

        for btn in all_children:
            if btn.isChecked() and btn.isVisible():
                self._animate_track(btn)
                return

        # 2. Pulsanti Principali o Header dei Gruppi
        potential_targets: list[SidebarButton] = []
        for b in self.main_btns:
            if isinstance(b, SidebarGroup):
                potential_targets.append(b.header_btn)
            elif isinstance(b, SidebarButton):
                potential_targets.append(b)

        for t_btn in potential_targets + self.footer_btns:
            if t_btn.isChecked() and t_btn.isVisible():
                self._animate_track(t_btn)
                return

        self.active_track.hide()

    def _update_track_instant(self) -> None:
        self._update_track()

    def set_active_button(self, index: int, sub_index: int | None = None) -> None:
        btns = {0: self.btn_home, 2: self.btn_lyra, 7: self.btn_settings, 8: self.btn_help}
        for i, b in btns.items():
            b.setChecked(i == index)
        self.group_db.set_active_index(index, (3, 4, 5, 6, 11, 10))
        self.group_notifiche.set_active_index(index, (9,))
        if index == 9:
            self.btn_notifiche.setChecked(sub_index == 0)
            self.btn_audit.setChecked(sub_index == 1)
            self.btn_health.setChecked(sub_index == 2)
        self.group_automazioni.set_active_index(index, (1,))
        if index == 1:
            self.btn_fornitori.setChecked(sub_index == 0)
            self.btn_safework.setChecked(sub_index == 1)
        QTimer.singleShot(150, self._update_track)

    def enterEvent(self, e: Any) -> None:
        self._set_collapsed(False)
        super().enterEvent(e)

    def leaveEvent(self, e: Any) -> None:
        self._set_collapsed(True)
        super().leaveEvent(e)

    def _set_collapsed(self, c: bool) -> None:
        if self._is_collapsed == c:
            return
        self._is_collapsed = c

        self._width_anim.stop()
        self._width_anim.setEndValue(self.collapsed_width if c else self.expanded_width)
        self._width_anim.start()

        self.logo_opacity.setOpacity(0.0 if c else 1.0)
        self.logo_label.setVisible(not c)

        # Mostra/nascondi le intere aree per un effetto "solo logo"
        self.scroll_area.setVisible(not c)
        self.footer.setVisible(not c)

        if c:
            self.active_track.hide()
            self.setMinimumHeight(102)
            self.setMaximumHeight(102)
            self.setStyleSheet(self._get_glass_style(collapsed=True))
        else:
            parent = self.parentWidget()
            parent_height = parent.height() if parent else 800
            self.setMinimumHeight(parent_height - 20)
            self.setMaximumHeight(parent_height - 20)
            self.setStyleSheet(self._get_glass_style(collapsed=False))

        for b in self.main_btns + self.footer_btns:
            if hasattr(b, "set_collapsed"):
                b.set_collapsed(c)
            if isinstance(b, SidebarGroup):
                b.header_btn.set_collapsed(c)

        if not c:
            QTimer.singleShot(100, self._update_ui_state)
        else:
            self._update_ui_state()
        QTimer.singleShot(150, self._update_track)

    def _update_ui_state(self) -> None:
        for g in (self.group_db, self.group_automazioni, self.group_notifiche):
            g.set_collapsed(self._is_collapsed)

    def _handle_automazione_click(self, tab_index: int) -> None:
        self.navigation_requested.emit(1)
        self.automation_tab_requested.emit(tab_index)

    def _handle_notifications_click(self, tab_index: int) -> None:
        self.navigation_requested.emit(9)
        self.notifications_tab_requested.emit(tab_index)
