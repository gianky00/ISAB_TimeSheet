"""
SyncroJob - Sidebar Widget (Premium Spectacular V8.6)
Navigazione magnetica estesa a 3 livelli per l'intera applicazione.
Tutti i pannelli con tab interni sono ora accessibili direttamente dalla Sidebar.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence

from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRect,
    Qt,
    QTimer,
    pyqtProperty,  # type: ignore[attr-defined]
    pyqtSignal,
)
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


class SidebarSubGroup(QWidget):
    """Sottogruppo di secondo livello (es. Portale Fornitori sotto Automazioni)."""

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.header_btn = SidebarChildButton(title, "")
        self.header_btn.setCheckable(True)
        self.main_layout.addWidget(self.header_btn)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(1)
        self.content_area.setVisible(False)
        self.main_layout.addWidget(self.content_area)

        self.header_btn.clicked.connect(self.toggle_group)
        self.children_btns: list[SidebarButton] = []

    def toggle_group(self) -> None:
        is_visible = self.content_area.isVisible()
        self.content_area.setVisible(not is_visible)

    def add_child(self, btn: SidebarButton) -> None:
        # Indentazione aggiuntiva per il terzo livello (55px)
        if not btn._collapsed:
            current_style = btn.styleSheet()
            new_style = current_style.replace("padding: 12px 15px;", "padding: 8px 10px 8px 55px;")
            # Assicura che la dimensione del font sia leggermente più piccola per il 3° livello
            new_style = new_style.replace("font-size: 13px;", "font-size: 12px;")
            btn.setStyleSheet(new_style)
        self.content_layout.addWidget(btn)
        self.children_btns.append(btn)

    def set_collapsed(self, collapsed: bool) -> None:
        self.header_btn.set_collapsed(collapsed)
        for btn in self.children_btns:
            btn.set_collapsed(collapsed)
            if collapsed:
                btn.setVisible(btn.isChecked())
            else:
                btn.setVisible(True)
        if collapsed:
            has_active = any(b.isChecked() for b in self.children_btns)
            self.content_area.setVisible(has_active)


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
        self.children_elements: list[QWidget] = []
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

    def add_child(self, widget: QWidget) -> None:
        self.content_layout.addWidget(widget)
        self.children_elements.append(widget)

    def set_collapsed(self, collapsed: bool) -> None:
        self.header_btn.set_collapsed(collapsed)
        self.arrow_label.setVisible(not collapsed)

        has_active_child = False
        for elem in self.children_elements:
            if hasattr(elem, "set_collapsed"):
                elem.set_collapsed(collapsed)

            if (isinstance(elem, SidebarButton) and elem.isChecked()) or (
                isinstance(elem, SidebarSubGroup)
                and (elem.header_btn.isChecked() or any(b.isChecked() for b in elem.children_btns))
            ):
                has_active_child = True

            if collapsed:
                if isinstance(elem, SidebarButton):
                    elem.setVisible(elem.isChecked())
                elif isinstance(elem, SidebarSubGroup):
                    elem.setVisible(
                        elem.header_btn.isChecked() or any(b.isChecked() for b in elem.children_btns)
                    )
            else:
                elem.setVisible(True)

        if collapsed:
            self.content_area.setVisible(has_active_child)
        else:
            self.content_area.setVisible(self._was_expanded)
        self._set_arrow_icon(self.content_area.isVisible() and not collapsed)

    def set_active_index(self, index: int, group_indices: Sequence[int]) -> None:
        is_child_active = index in group_indices
        self.header_btn.setChecked(is_child_active)

        if is_child_active:
            self.content_area.setVisible(True)
            if not self.header_btn._collapsed:
                self._was_expanded = True
        self._set_arrow_icon(self.content_area.isVisible() and not self.header_btn._collapsed)


class SidebarWidget(QFrame):
    """
    Sidebar Enterprise con navigazione profonda a 3 livelli.
    """

    navigation_requested = pyqtSignal(int, int, int)  # (page_idx, sub_idx, bot_idx)
    palette_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebarContainer")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
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
        self.setMinimumHeight(90)
        self.setMaximumHeight(90)
        self.setMouseTracking(True)

        self._setup_ui()
        self.bg_frame.setStyleSheet(self._get_glass_style(collapsed=True))
        self._update_ui_state()
        QTimer.singleShot(500, self._update_track_instant)

    def get_sidebar_width(self) -> int:
        return self.minimumWidth()

    def set_sidebar_width(self, w: int) -> None:
        self.setMinimumWidth(w)
        self.setMaximumWidth(w)

    sidebar_width = pyqtProperty(int, fget=get_sidebar_width, fset=set_sidebar_width)

    def _get_glass_style(self, collapsed: bool = False) -> str:
        if collapsed:
            return """
                QFrame#sidebarFrame { background-color: transparent; border: none; }
                QScrollArea { border: none; background: transparent; }
                QScrollArea > QWidget > QWidget { background: transparent; }
                QWidget#scrollContent { background: transparent; }
            """
        gradient = """qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 #0f172a, stop: 0.4 #172554, stop: 0.8 #081121, stop: 1 #1e1b4b
        )"""
        return f"""
            QFrame#sidebarFrame {{ background: {gradient}; border-right: 1px solid rgba(255, 255, 255, 0.05); border-radius: 18px; }}
            QScrollArea {{ border: none; background: transparent; }}
            QScrollArea > QWidget > QWidget {{ background: transparent; }}
            QWidget#scrollContent {{ background: transparent; }}
            QScrollBar:vertical {{ border: none; background: transparent; width: 4px; }}
            QScrollBar::handle:vertical {{ background: {hex_to_rgba(COLORS["bg_white"], 0.15)}; border-radius: 2px; }}
            QScrollBar::handle:vertical:hover {{ background: {hex_to_rgba(COLORS["bg_white"], 0.25)}; }}
        """

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.bg_frame = QFrame(self)
        self.bg_frame.setObjectName("sidebarFrame")
        main_layout.addWidget(self.bg_frame)

        layout = QVBoxLayout(self.bg_frame)
        layout.setContentsMargins(0, 7, 0, 20)
        layout.setSpacing(0)

        # Header
        self.header_container = QWidget()
        h_layout = QHBoxLayout(self.header_container)
        h_layout.setContentsMargins(14, 0, 14, 15)
        h_layout.setSpacing(12)

        self.logo_badge = QLabel()
        self.logo_badge.setFixedSize(46, 46)
        self.logo_badge.setStyleSheet(
            "background-color: white; border-radius: 23px; border: 2px solid black;"
        )
        self.logo_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        from PyQt6.QtGui import QIcon

        pix = QIcon(get_asset_path("assets/app.ico")).pixmap(64, 64)
        if not pix.isNull():
            self.logo_badge.setPixmap(
                pix.scaled(
                    30,
                    30,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        h_layout.addWidget(self.logo_badge)

        self.logo_label = QLabel("SyncroJob")
        self.logo_label.setStyleSheet("font-size: 18px; font-weight: 900; color: white;")
        self.logo_opacity = QGraphicsOpacityEffect(self.logo_label)
        self.logo_label.setGraphicsEffect(self.logo_opacity)
        h_layout.addWidget(self.logo_label)
        layout.addWidget(self.header_container)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")
        self.menu_layout = QVBoxLayout(self.scroll_content)
        self.menu_layout.setContentsMargins(5, 0, 5, 0)
        self.menu_layout.setSpacing(6)

        # Pulsanti Principali
        self.btn_palette = SidebarButton("Apri Palette", get_asset_path(Icons.COMMAND_PALETTE))
        self.btn_home = SidebarButton("Home", get_asset_path(Icons.HOME))
        self.group_automazioni = SidebarGroup("Automazioni", get_asset_path(Icons.CPU))
        self.group_db = SidebarGroup("Database", get_asset_path(Icons.DATABASE))
        self.group_contabilita = SidebarGroup("Contabilità", get_asset_path(Icons.BAR_CHART))

        self.main_btns = [
            self.btn_palette,
            self.btn_home,
            self.group_automazioni,
            self.group_db,
            self.group_contabilita,
        ]
        for btn in self.main_btns:
            self.menu_layout.addWidget(btn)
            if isinstance(btn, SidebarGroup):
                btn.expanded.connect(self._on_group_expanded)

        # --- LIVELLO 3: AUTOMAZIONI ---
        self.sub_fornitori = SidebarSubGroup("Portale Fornitori")
        bots_fornitori = [
            ("Dettagli OdA", 0),
            ("Scarico TS", 1),
            ("Timbrature", 2),
            ("Prenota BP", 3),
            ("Carico TS", 4),
        ]
        for name, idx in bots_fornitori:
            b = SidebarChildButton(name, "")
            b.clicked.connect(lambda _, s=idx: self.navigation_requested.emit(1, 0, s))
            self.sub_fornitori.add_child(b)

        self.sub_safework = SidebarSubGroup("SafeWork")
        bots_safework = [("Scarico PDL", 0), ("Ricerca PDL", 1)]
        for name, idx in bots_safework:
            b = SidebarChildButton(name, "")
            b.clicked.connect(lambda _, s=idx: self.navigation_requested.emit(1, 1, s))
            self.sub_safework.add_child(b)

        self.group_automazioni.add_child(self.sub_fornitori)
        self.group_automazioni.add_child(self.sub_safework)

        # --- LIVELLO 3: DATABASE ---
        self.btn_timbrature = SidebarChildButton("Timbrature", get_asset_path(Icons.CLOCK))
        self.btn_dataease = SidebarChildButton("DataEase", get_asset_path(Icons.DOWNLOAD))
        self.btn_pdl = SidebarChildButton("PDL", get_asset_path(Icons.PDL))
        self.btn_storico_oda = SidebarChildButton("Storico OdA", get_asset_path(Icons.FILE_TEXT))

        self.sub_dipendenti = SidebarSubGroup("Dipendenti")
        for name, idx in (("Monitoraggio", 0), ("Configurazione", 1)):
            b = SidebarChildButton(name, "")
            b.clicked.connect(lambda _, s=idx: self.navigation_requested.emit(11, s, -1))
            self.sub_dipendenti.add_child(b)

        for db_elem in (
            self.btn_timbrature,
            self.btn_dataease,
            self.btn_pdl,
            self.sub_dipendenti,
            self.btn_storico_oda,
        ):
            self.group_db.add_child(db_elem)

        # --- LIVELLO 3: CONTABILITÀ ---
        self.sub_strumentale = SidebarSubGroup("Strumentale")
        strumentale_tabs = [
            ("Preventivi", 0),
            ("Giornaliere", 1),
            ("Attività Programmate", 2),
            ("Certificati Campione", 3),
            ("Analisi KPI", 4),
        ]
        for s_name, s_idx in strumentale_tabs:
            s_btn = SidebarChildButton(s_name, "")
            s_btn.clicked.connect(lambda _, s=s_idx: self.navigation_requested.emit(4, s, -1))
            self.sub_strumentale.add_child(s_btn)

        self.sub_consuntivo = SidebarSubGroup("Consuntivo")
        consuntivo_tabs = [("Crea Nuovo", 0), ("Modifica Esistente", 1), ("Impostazioni", 2)]
        for c_name, c_idx in consuntivo_tabs:
            c_btn = SidebarChildButton(c_name, "")
            c_btn.clicked.connect(lambda _, s=c_idx: self.navigation_requested.emit(12, s, -1))
            self.sub_consuntivo.add_child(c_btn)

        self.group_contabilita.add_child(self.sub_strumentale)
        self.group_contabilita.add_child(self.sub_consuntivo)

        self.menu_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Footer
        self.footer = QWidget()
        f_layout = QVBoxLayout(self.footer)
        f_layout.setContentsMargins(5, 10, 5, 0)
        f_layout.setSpacing(6)
        self.btn_lyra = SidebarButton("Lyra AI", get_asset_path(Icons.SPARKLES))
        self.group_notifiche = SidebarGroup("Monitoraggio", get_asset_path(Icons.ACTIVITY))
        self.btn_help = SidebarButton("Guida", get_asset_path(Icons.HELP))
        self.btn_settings = SidebarButton("Impostazioni", get_asset_path(Icons.SETTINGS))
        self.footer_btns = [self.btn_lyra, self.group_notifiche, self.btn_help, self.btn_settings]
        for f_btn in self.footer_btns:
            f_layout.addWidget(f_btn)
            if isinstance(f_btn, SidebarGroup):
                f_btn.expanded.connect(self._on_group_expanded)

        # --- LIVELLO 3: MONITORAGGIO ---
        notif_tabs = [("Notifiche", 0), ("Audit", 1), ("Health", 2)]
        self.notif_child_btns = []
        for n_name, n_idx in notif_tabs:
            n_btn = SidebarChildButton(n_name, "")
            n_btn.clicked.connect(lambda _, s=n_idx: self.navigation_requested.emit(9, s, -1))
            self.group_notifiche.add_child(n_btn)
            self.notif_child_btns.append(n_btn)

        layout.addWidget(self.footer)
        if self._is_collapsed:
            self.scroll_area.setVisible(False)
            self.footer.setVisible(False)

        self.active_track = QWidget(self)
        self.active_track.setFixedWidth(5)
        self.active_track.setStyleSheet(f"background: {COLORS['teal_accent']}; border-radius: 2px;")
        self.active_track.raise_()
        self._track_anim.setTargetObject(self.active_track)
        self._setup_connections()

    def _setup_connections(self) -> None:
        self.btn_palette.clicked.connect(self.palette_requested.emit)
        self.btn_home.clicked.connect(lambda: self.navigation_requested.emit(0, -1, -1))
        self.btn_timbrature.clicked.connect(lambda: self.navigation_requested.emit(3, -1, -1))
        self.btn_dataease.clicked.connect(lambda: self.navigation_requested.emit(5, -1, -1))
        self.btn_pdl.clicked.connect(lambda: self.navigation_requested.emit(6, -1, -1))
        self.btn_storico_oda.clicked.connect(lambda: self.navigation_requested.emit(10, -1, -1))
        self.btn_lyra.clicked.connect(lambda: self.navigation_requested.emit(2, -1, -1))
        self.btn_help.clicked.connect(lambda: self.navigation_requested.emit(8, -1, -1))
        self.btn_settings.clicked.connect(lambda: self.navigation_requested.emit(7, -1, -1))

    def _on_group_expanded(self, group: SidebarGroup) -> None:
        for g in (
            self.group_automazioni,
            self.group_db,
            self.group_contabilita,
            self.group_notifiche,
        ):
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
        all_child_widgets = []
        for g in (
            self.group_automazioni,
            self.group_db,
            self.group_contabilita,
            self.group_notifiche,
        ):
            for elem in g.children_elements:
                if isinstance(elem, SidebarButton):
                    all_child_widgets.append(elem)
                elif isinstance(elem, SidebarSubGroup):
                    all_child_widgets.append(elem.header_btn)
                    all_child_widgets.extend(elem.children_btns)

        for btn in all_child_widgets:
            if btn.isChecked() and btn.isVisible():
                self._animate_track(btn)
                return

        potential_targets: list[SidebarButton] = []
        for b in self.main_btns + self.footer_btns:
            if isinstance(b, SidebarGroup):
                potential_targets.append(b.header_btn)
            elif isinstance(b, SidebarButton):
                potential_targets.append(b)
        for t_btn in potential_targets:
            if t_btn.isChecked() and t_btn.isVisible():
                self._animate_track(t_btn)
                return
        self.active_track.hide()

    def _update_track_instant(self) -> None:
        self._update_track()

    def set_active_button(
        self, index: int, sub_index: int | None = None, bot_index: int | None = None
    ) -> None:
        btns = {
            0: self.btn_home,
            2: self.btn_lyra,
            7: self.btn_settings,
            8: self.btn_help,
            3: self.btn_timbrature,
            5: self.btn_dataease,
            6: self.btn_pdl,
            10: self.btn_storico_oda,
        }
        for i, b in btns.items():
            b.setChecked(i == index)

        self.group_db.set_active_index(index, (3, 5, 6, 11, 10))
        self.group_contabilita.set_active_index(index, (4, 12))
        self.group_notifiche.set_active_index(index, (9,))
        self.group_automazioni.set_active_index(index, (1,))

        # Sincronizzazione Livello 3
        if index == 1:
            self.sub_fornitori.header_btn.setChecked(sub_index == 0)
            self.sub_safework.header_btn.setChecked(sub_index == 1)
            for i, b in enumerate(self.sub_fornitori.children_btns):
                b.setChecked(sub_index == 0 and i == bot_index)
            for i, b in enumerate(self.sub_safework.children_btns):
                b.setChecked(sub_index == 1 and i == bot_index)
            if not self._is_collapsed:
                if sub_index == 0:
                    self.sub_fornitori.content_area.setVisible(True)
                elif sub_index == 1:
                    self.sub_safework.content_area.setVisible(True)

        elif index == 11:
            self.sub_dipendenti.header_btn.setChecked(True)
            for i, b in enumerate(self.sub_dipendenti.children_btns):
                b.setChecked(i == sub_index)
            if not self._is_collapsed:
                self.sub_dipendenti.content_area.setVisible(True)

        elif index == 4:
            self.sub_strumentale.header_btn.setChecked(True)
            for i, b in enumerate(self.sub_strumentale.children_btns):
                b.setChecked(i == sub_index)
            if not self._is_collapsed:
                self.sub_strumentale.content_area.setVisible(True)

        elif index == 12:
            self.sub_consuntivo.header_btn.setChecked(True)
            for i, b in enumerate(self.sub_consuntivo.children_btns):
                b.setChecked(i == sub_index)
            if not self._is_collapsed:
                self.sub_consuntivo.content_area.setVisible(True)

        elif index == 9:
            for i, b in enumerate(self.notif_child_btns):
                b.setChecked(i == sub_index)

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
        self.scroll_area.setVisible(not c)
        self.footer.setVisible(not c)
        if c:
            self.active_track.hide()
            self.setMinimumHeight(90)
            self.setMaximumHeight(90)
            self.bg_frame.setStyleSheet(self._get_glass_style(collapsed=True))
        else:
            p = self.parentWidget()
            ph = p.height() if p else 800
            self.setMinimumHeight(ph - 20)
            self.setMaximumHeight(ph - 20)
            self.bg_frame.setStyleSheet(self._get_glass_style(collapsed=False))
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
        for g in (
            self.group_db,
            self.group_automazioni,
            self.group_contabilita,
            self.group_notifiche,
        ):
            g.set_collapsed(self._is_collapsed)

    def _handle_notifications_click(self, tab_index: int) -> None:
        self.navigation_requested.emit(9, tab_index, -1)
