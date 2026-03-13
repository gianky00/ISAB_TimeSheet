"""
SyncroJob - Sidebar Widget (Refactored V8.7)
Navigazione magnetica enterprise a 3 livelli.
Modularizzato per una manutenibilità superiore.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import Qt, QTimer, pyqtProperty, pyqtSignal  # type: ignore[attr-defined]
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

from .sidebar.animations import SidebarAnimationManager
from .sidebar.components import SidebarChildButton, SidebarGroup, SidebarSubGroup


class SidebarWidget(QFrame):
    """
    Orchestratore della Sidebar con navigazione profonda e track magnetico.
    Gestisce l'espansione automatica all'hover e la gerarchia dei menu a 3 livelli.
    """

    navigation_requested = pyqtSignal(int, int, int)  # (page, sub, bot)
    palette_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il componente sidebar.

        Args:
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.setObjectName("sidebarContainer")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._is_collapsed = True
        self._drag_in_progress = False
        self.expanded_width = 245
        self.collapsed_width = 75

        self.anim_manager = SidebarAnimationManager(self)

        self.setMinimumWidth(self.collapsed_width)
        self.setMaximumWidth(self.collapsed_width)
        self.setMinimumHeight(100)
        self.setMaximumHeight(100)
        self.setMouseTracking(True)

        self._setup_ui()
        self.bg_frame.setStyleSheet(self._get_glass_style(collapsed=True))
        self._update_ui_state()
        QTimer.singleShot(500, self._update_track)

    def get_sidebar_width(self) -> int:
        """Restituisce la larghezza corrente della sidebar."""
        return self.minimumWidth()

    def set_sidebar_width(self, w: int) -> None:
        """Imposta la larghezza della sidebar (usato dalle animazioni)."""
        self.setMinimumWidth(w)
        self.setMaximumWidth(w)

    sidebar_width = pyqtProperty(int, fget=get_sidebar_width, fset=set_sidebar_width)

    def _get_glass_style(self, collapsed: bool = False) -> str:
        """Genera lo stile QSS per l'effetto glass della sidebar."""
        if collapsed:
            return "QFrame#sidebarFrame { background: transparent; border: none; }"
        gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f172a, stop:0.4 #172554, stop:0.8 #081121, stop:1 #1e1b4b)"
        return f"""
            QFrame#sidebarFrame {{ background: {gradient}; border-right: 1px solid rgba(255, 255, 255, 0.05); border-radius: 18px; }}
            QScrollArea {{ border: none; background: transparent; }}
            QWidget#scrollContent {{ background: transparent; }}
            QScrollBar:vertical {{ border: none; background: transparent; width: 4px; }}
            QScrollBar::handle:vertical {{ background: {hex_to_rgba(COLORS["bg_white"], 0.15)}; border-radius: 2px; }}
        """

    def _setup_ui(self) -> None:
        """Inizializza l'interfaccia grafica e la struttura dei menu."""
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0, 0, 0, 0)
        self.bg_frame = QFrame(self)
        self.bg_frame.setObjectName("sidebarFrame")
        main_lay.addWidget(self.bg_frame)

        layout = QVBoxLayout(self.bg_frame)
        layout.setContentsMargins(0, 7, 0, 20)
        layout.setSpacing(0)

        # Header
        self.h_container = QWidget()
        self.h_lay = QHBoxLayout(self.h_container)
        # Default state: Collapsed
        self.h_lay.setContentsMargins(0, 8, 0, 15)
        self.h_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h_lay.setSpacing(10)

        self.logo_badge = QLabel()
        self.logo_badge.setFixedSize(46, 46)
        self.logo_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_badge.setStyleSheet("background: white; border-radius: 23px; border: 2px solid black;")

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
        self.h_lay.addWidget(self.logo_badge)

        self.logo_label = QLabel("SyncroJob")
        self.logo_label.setStyleSheet("font-size: 18px; font-weight: 900; color: white;")
        self.logo_opacity = QGraphicsOpacityEffect(self.logo_label)
        self.logo_label.setGraphicsEffect(self.logo_opacity)
        self.h_lay.addWidget(self.logo_label)

        # Gestione visibilità iniziale
        self.logo_label.setVisible(not self._is_collapsed)
        self.logo_opacity.setOpacity(0.0 if self._is_collapsed else 1.0)

        layout.addWidget(self.h_container)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")
        self.menu_layout = QVBoxLayout(self.scroll_content)
        self.menu_layout.setContentsMargins(5, 0, 5, 0)
        self.menu_layout.setSpacing(6)

        # Level 1
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
        for b in self.main_btns:
            self.menu_layout.addWidget(b)
            if isinstance(b, SidebarGroup):
                b.expanded.connect(self._on_group_expanded)

        # --- LEVEL 3: AUTOMATIONS ---
        self.sub_fornitori = SidebarSubGroup("Portale Fornitori")
        for n, i in (
            ("Dettagli OdA", 0),
            ("Scarico TS", 1),
            ("Timbrature", 2),
            ("Prenota BP", 3),
            ("Carico TS", 4),
        ):
            btn = SidebarChildButton(n, "")
            btn.clicked.connect(lambda _, s=i: self.navigation_requested.emit(1, 0, s))
            self.sub_fornitori.add_child(btn)

        self.sub_safework = SidebarSubGroup("SafeWork")
        for n, i in (("Scarico PDL", 0), ("Ricerca PDL", 1)):
            btn = SidebarChildButton(n, "")
            btn.clicked.connect(lambda _, s=i: self.navigation_requested.emit(1, 1, s))
            self.sub_safework.add_child(btn)

        self.group_automazioni.add_child(self.sub_fornitori)
        self.group_automazioni.add_child(self.sub_safework)

        # --- LEVEL 3: DATABASE ---
        self.btn_timbrature = SidebarChildButton("Timbrature", get_asset_path(Icons.CLOCK))
        self.btn_dataease = SidebarChildButton("DataEase", get_asset_path(Icons.DOWNLOAD))
        self.btn_pdl = SidebarChildButton("PDL", get_asset_path(Icons.PDL))
        self.btn_storico_oda = SidebarChildButton("Storico OdA", get_asset_path(Icons.FILE_TEXT))
        self.sub_dipendenti = SidebarSubGroup("Dipendenti")
        for n, i in (("Monitoraggio", 0), ("Configurazione", 1)):
            btn = SidebarChildButton(n, "")
            btn.clicked.connect(lambda _, s=i: self.navigation_requested.emit(11, s, -1))
            self.sub_dipendenti.add_child(btn)

        for b in (
            self.btn_timbrature,
            self.btn_dataease,
            self.btn_pdl,
            self.sub_dipendenti,
            self.btn_storico_oda,
        ):
            self.group_db.add_child(b)

        # --- LEVEL 3: CONTABILITA ---
        self.sub_strumentale = SidebarSubGroup("Strumentale")
        for n, i in (
            ("Preventivi", 0),
            ("Giornaliere", 1),
            ("Attività Programmate", 2),
            ("Certificati", 3),
            ("KPI", 4),
        ):
            btn = SidebarChildButton(n, "")
            btn.clicked.connect(lambda _, s=i: self.navigation_requested.emit(4, s, -1))
            self.sub_strumentale.add_child(btn)

        self.sub_consuntivo = SidebarSubGroup("Consuntivo")
        for n, i in (("Crea Nuovo", 0), ("Modifica Esistente", 1), ("Impostazioni", 2)):
            btn = SidebarChildButton(n, "")
            btn.clicked.connect(lambda _, s=i: self.navigation_requested.emit(12, s, -1))
            self.sub_consuntivo.add_child(btn)

        self.group_contabilita.add_child(self.sub_strumentale)
        self.group_contabilita.add_child(self.sub_consuntivo)

        self.menu_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Footer
        self.footer = QWidget()
        f_lay = QVBoxLayout(self.footer)
        f_lay.setContentsMargins(5, 10, 5, 0)
        f_lay.setSpacing(6)
        self.group_notifiche = SidebarGroup("Monitoraggio", get_asset_path(Icons.ACTIVITY))
        self.btn_help = SidebarButton("Guida", get_asset_path(Icons.HELP))
        self.btn_settings = SidebarButton("Impostazioni", get_asset_path(Icons.SETTINGS))

        self.footer_btns = [self.group_notifiche, self.btn_help, self.btn_settings]
        for b in self.footer_btns:
            f_lay.addWidget(b)
            if isinstance(b, SidebarGroup):
                b.expanded.connect(self._on_group_expanded)

        self.notif_child_btns = []
        for n, i in (("Notifiche", 0), ("Audit", 1), ("Health", 2)):
            btn = SidebarChildButton(n, "")
            btn.clicked.connect(lambda _, s=i: self.navigation_requested.emit(9, s, -1))
            self.group_notifiche.add_child(btn)
            self.notif_child_btns.append(btn)

        layout.addWidget(self.footer)
        self.active_track = QWidget(self)
        self.active_track.setFixedWidth(5)
        self.active_track.setStyleSheet(f"background: {COLORS['teal_accent']}; border-radius: 2px;")

        # Nascondi elementi se parte collassata
        if self._is_collapsed:
            self.scroll_area.setVisible(False)
            self.footer.setVisible(False)

        self._setup_connections()

    def _setup_connections(self) -> None:
        """Configura i collegamenti dei segnali per i pulsanti principali."""
        self.btn_palette.clicked.connect(self.palette_requested.emit)
        self.btn_home.clicked.connect(lambda: self.navigation_requested.emit(0, -1, -1))
        self.btn_timbrature.clicked.connect(lambda: self.navigation_requested.emit(3, -1, -1))
        self.btn_dataease.clicked.connect(lambda: self.navigation_requested.emit(5, -1, -1))
        self.btn_pdl.clicked.connect(lambda: self.navigation_requested.emit(6, -1, -1))
        self.btn_storico_oda.clicked.connect(lambda: self.navigation_requested.emit(10, -1, -1))
        self.btn_help.clicked.connect(lambda: self.navigation_requested.emit(8, -1, -1))
        self.btn_settings.clicked.connect(lambda: self.navigation_requested.emit(7, -1, -1))

    def _on_group_expanded(self, group: SidebarGroup) -> None:
        """
        Gestisce l'espansione di un gruppo, assicurando che gli altri siano chiusi (Accordion logic).

        Args:
            group: Il gruppo che è stato espanso.
        """
        for g in (
            self.group_automazioni,
            self.group_db,
            self.group_contabilita,
            self.group_notifiche,
        ):
            if g != group:
                g.collapse()
        QTimer.singleShot(100, self._update_track)

    def _update_track(self) -> None:
        """Aggiorna la posizione del track magnetico basandosi sul pulsante attivo."""
        targets = []
        for g in (
            self.group_automazioni,
            self.group_db,
            self.group_contabilita,
            self.group_notifiche,
        ):
            for e in g.children_elements:
                if isinstance(e, SidebarButton):
                    targets.append(e)
                elif isinstance(e, SidebarSubGroup):
                    targets.append(e.header_btn)
                    targets.extend(e.children_btns)

        for b in (*self.main_btns, *self.footer_btns):
            if isinstance(b, SidebarButton):
                targets.append(b)
            elif isinstance(b, SidebarGroup):
                targets.append(b.header_btn)

        for t in targets:
            if t.isChecked() and t.isVisible():
                self.anim_manager.move_track(self.active_track, t)
                return
        self.active_track.hide()

    def set_active_button(self, index: int, sub: int | None = None, bot: int | None = None) -> None:
        """
        Imposta visivamente il pulsante attivo nella sidebar.

        Args:
            index: Indice della pagina principale.
            sub: Indice del sottomenu opzionale.
            bot: Indice del bot specifico opzionale.
        """
        btns = {
            0: self.btn_home,
            7: self.btn_settings,
            8: self.btn_help,
            3: self.btn_timbrature,
            5: self.btn_dataease,
            6: self.btn_pdl,
            10: self.btn_storico_oda,
        }
        for i, b in btns.items():
            b.setChecked(i == index)

        for g, indices in (
            (self.group_db, (3, 5, 6, 11, 10)),
            (self.group_contabilita, (4, 12)),
            (self.group_notifiche, (9,)),
            (self.group_automazioni, (1,)),
        ):
            g.set_active_index(index, indices)

        if index == 1:
            self.sub_fornitori.header_btn.setChecked(sub == 0)
            self.sub_safework.header_btn.setChecked(sub == 1)
            for i, b in enumerate(self.sub_fornitori.children_btns):
                b.setChecked(sub == 0 and i == bot)
            for i, b in enumerate(self.sub_safework.children_btns):
                b.setChecked(sub == 1 and i == bot)
        elif index == 11:
            self.sub_dipendenti.header_btn.setChecked(True)
            for i, b in enumerate(self.sub_dipendenti.children_btns):
                b.setChecked(i == sub)
        elif index == 4:
            self.sub_strumentale.header_btn.setChecked(True)
            for i, b in enumerate(self.sub_strumentale.children_btns):
                b.setChecked(i == sub)
        elif index == 12:
            self.sub_consuntivo.header_btn.setChecked(True)
            for i, b in enumerate(self.sub_consuntivo.children_btns):
                b.setChecked(i == sub)
        elif index == 9:
            for i, b in enumerate(self.notif_child_btns):
                b.setChecked(i == sub)

        QTimer.singleShot(150, self._update_track)

    def enterEvent(self, e: Any) -> None:
        """Espande la sidebar all'ingresso del mouse."""
        self._set_collapsed(False)
        super().enterEvent(e)

    def leaveEvent(self, e: Any) -> None:
        """Contrae la sidebar all'uscita del mouse."""
        if getattr(self, "_drag_in_progress", False):
            super().leaveEvent(e)
            return
        self._set_collapsed(True)
        super().leaveEvent(e)

    def _set_collapsed(self, c: bool) -> None:
        """Configura lo stato di espansione/contrazione della sidebar."""
        if self._is_collapsed == c:
            return
        self._is_collapsed = c
        self.anim_manager.animate_width(self.collapsed_width if c else self.expanded_width)
        self.logo_opacity.setOpacity(0.0 if c else 1.0)
        self.logo_label.setVisible(not c)
        self.scroll_area.setVisible(not c)
        self.footer.setVisible(not c)

        # Aggiorna allineamento header
        if c:
            self.h_lay.setContentsMargins(0, 8, 0, 15)
            self.h_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.h_lay.setContentsMargins(14, 8, 14, 15)
            self.h_lay.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        if c:
            self.active_track.hide()
            self.setMinimumHeight(100)
            self.setMaximumHeight(100)
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
        """Sincronizza lo stato dei gruppi figli con quello della sidebar."""
        for g in (
            self.group_db,
            self.group_automazioni,
            self.group_contabilita,
            self.group_notifiche,
        ):
            g.set_collapsed(self._is_collapsed)
