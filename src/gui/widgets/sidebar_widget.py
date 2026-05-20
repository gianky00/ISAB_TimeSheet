"""
SyncroJob - Sidebar Widget (Refactored V8.8 - Performance Optimized V4)
Navigazione magnetica professionale a 3 livelli.
Risolti bug di sovrapposizione e artefatti grafici. Massima fluidità garantita.
"""

from __future__ import annotations

from PySide6.QtCore import Property, QEvent, Qt, QTimer, Signal
from PySide6.QtGui import QEnterEvent, QIcon
from PySide6.QtWidgets import (
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

    navigation_requested = Signal(int, int, int)  # (page, sub, bot)
    palette_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il componente sidebar.

        Args:
          parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self._initialize_constants()
        self._initialize_ui_elements()
        self._setup_ui()
        self._finalize_init()

    def _initialize_constants(self) -> None:
        """Inizializza le costanti di configurazione."""
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

    def _initialize_ui_elements(self) -> None:
        """Dichiara tutti i membri UI per evitare violazioni di tipo."""
        # UI Elements
        self.bg_frame = QFrame()
        self.content_layout = QVBoxLayout()
        self.h_container = QWidget()
        self.h_lay = QHBoxLayout()
        self.logo_badge = QLabel()
        self.logo_label = QLabel()
        self.logo_opacity = QGraphicsOpacityEffect()
        self.scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.menu_layout = QVBoxLayout()
        self.active_track = QWidget()
        self.footer = QWidget()

        # Menu Elements
        self.btn_palette = SidebarButton("", "")
        self.btn_home = SidebarButton("", "")
        self.group_automazioni = SidebarGroup("", "")
        self.group_db = SidebarGroup("", "")
        self.group_contabilita = SidebarGroup("", "")
        self.group_notifiche = SidebarGroup("", "")
        self.btn_timbrature = SidebarChildButton("", "")
        self.btn_dataease = SidebarChildButton("", "")
        self.btn_pdl = SidebarChildButton("", "")
        self.btn_storico_oda = SidebarChildButton("", "")
        self.sub_dipendenti = SidebarSubGroup("")
        self.sub_strumentale = SidebarSubGroup("")
        self.sub_consuntivo = SidebarSubGroup("")
        self.sub_fornitori = SidebarSubGroup("")
        self.sub_safework = SidebarSubGroup("")
        self.btn_help = SidebarButton("", "")
        self.btn_changelog = SidebarButton("", "")
        self.btn_settings = SidebarButton("", "")
        self.main_btns: tuple[QWidget, ...] = ()
        self.footer_btns: tuple[QWidget, ...] = ()
        self.notif_child_btns: list[SidebarChildButton] = []

    def _finalize_init(self) -> None:
        """Operazioni finali dopo il setup UI."""
        self.bg_frame.setStyleSheet(self._get_glass_style())
        self.bg_frame.setProperty("state", "collapsed")
        self._update_ui_state()
        QTimer.singleShot(500, self._update_track)

    def get_sidebar_width(self) -> int:
        """Restituisce la larghezza corrente della sidebar."""
        return self.minimumWidth()

    def set_sidebar_width(self, w: int) -> None:
        """Imposta la larghezza della sidebar (usato dalle animazioni)."""
        self.setMinimumWidth(w)
        self.setMaximumWidth(w)

    sidebar_width = Property(int, fget=get_sidebar_width, fset=set_sidebar_width)

    def _get_glass_style(self) -> str:
        """Genera lo stile QSS pulito ed efficiente."""
        gradient = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0f172a, stop:1 #1e1b4b)"
        sb_handle = hex_to_rgba(COLORS["bg_white"], 0.15)

        return f"""
      QFrame#sidebarFrame {{
        background: {gradient};
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 18px;
      }}
      QFrame#sidebarFrame[state="collapsed"] {{
        background: transparent;
        border: none;
      }}
      QScrollArea {{ border: none; background: transparent; }}
      QWidget#scrollContent {{ background: transparent; }}
      QScrollBar:vertical {{ border: none; background: transparent; width: 4px; }}
      QScrollBar::handle:vertical {{ background: {sb_handle}; border-radius: 2px; }}
    """

    def _setup_ui(self) -> None:
        """Inizializza l'interfaccia grafica e la struttura dei menu."""
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0, 0, 0, 0)
        self.bg_frame = QFrame(self)
        self.bg_frame.setObjectName("sidebarFrame")
        main_lay.addWidget(self.bg_frame)

        # Layout principale del frame di sfondo
        self.content_layout = QVBoxLayout(self.bg_frame)
        self.content_layout.setContentsMargins(0, 7, 0, 20)
        self.content_layout.setSpacing(0)

        self._setup_header()
        self._setup_scroll_area()
        self._setup_footer()

        self.active_track = QWidget(self)
        track_width = 5
        self.active_track.setFixedWidth(track_width)
        self.active_track.setStyleSheet(f"background: {COLORS['teal_accent']}; border-radius: 2px;")
        self.active_track.hide()

        # Stato iniziale visibilit
        self.scroll_area.setVisible(not self._is_collapsed)
        self.footer.setVisible(not self._is_collapsed)

        self._setup_connections()

    def _setup_header(self) -> None:
        """Inizializza l'header con il logo."""
        self.h_container = QWidget()
        self.h_lay = QHBoxLayout(self.h_container)
        self.h_lay.setContentsMargins(0, 18, 0, 15)
        self.h_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h_lay.setSpacing(10)

        self.logo_badge = QLabel()
        badge_size = 46
        self.logo_badge.setFixedSize(badge_size, badge_size)
        self.logo_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_badge.setStyleSheet("background: white; border-radius: 23px; border: 1px solid #e2e8f0;")
        icon_size = 64
        pix = QIcon(get_asset_path("assets/app.ico")).pixmap(icon_size, icon_size)
        if not pix.isNull():
            scaled_size = 30
            self.logo_badge.setPixmap(
                pix.scaled(
                    scaled_size,
                    scaled_size,
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

        self.logo_opacity.setOpacity(0.0 if self._is_collapsed else 1.0)
        self.content_layout.addWidget(self.h_container)

    def _setup_scroll_area(self) -> None:
        """Inizializza l'area a scorrimento con i menu."""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")
        self.menu_layout = QVBoxLayout(self.scroll_content)
        self.menu_layout.setContentsMargins(5, 0, 5, 0)
        self.menu_layout.setSpacing(6)

        # Main groups
        self.btn_palette = SidebarButton("Apri Palette", get_asset_path(Icons.COMMAND_PALETTE))
        self.btn_home = SidebarButton("Home", get_asset_path(Icons.HOME))
        self.group_automazioni = SidebarGroup("Automazioni", get_asset_path(Icons.CPU))
        self.group_db = SidebarGroup("Database", get_asset_path(Icons.DATABASE))
        self.group_contabilita = SidebarGroup("Contabilità", get_asset_path(Icons.BAR_CHART))

        self.main_btns = (
            self.btn_palette,
            self.btn_home,
            self.group_automazioni,
            self.group_db,
            self.group_contabilita,
        )
        for main_btn in self.main_btns:
            self.menu_layout.addWidget(main_btn)
            if isinstance(main_btn, SidebarGroup):
                main_btn.expanded.connect(self._on_group_expanded)

        self._setup_automations_menu()
        self._setup_database_menu()
        self._setup_accounting_menu()

        self.menu_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)
        self.content_layout.addWidget(self.scroll_area)

    def _setup_automations_menu(self) -> None:
        """Configura il sottomenu delle automazioni."""
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

    def _setup_database_menu(self) -> None:
        """Configura il sottomenu dei database."""
        self.btn_timbrature = SidebarChildButton("Timbrature", get_asset_path(Icons.CLOCK))
        self.btn_dataease = SidebarChildButton("DataEase", get_asset_path(Icons.DOWNLOAD))
        self.btn_pdl = SidebarChildButton("PDL", get_asset_path(Icons.PDL))
        self.btn_storico_oda = SidebarChildButton("Storico OdA", get_asset_path(Icons.FILE_TEXT))
        self.sub_dipendenti = SidebarSubGroup("Dipendenti")
        for n, i in (("Monitoraggio", 0), ("Configurazione", 1)):
            btn = SidebarChildButton(n, "")
            btn.clicked.connect(lambda _, s=i: self.navigation_requested.emit(11, s, -1))
            self.sub_dipendenti.add_child(btn)

        for db_btn in (
            self.btn_timbrature,
            self.btn_dataease,
            self.btn_pdl,
            self.sub_dipendenti,
            self.btn_storico_oda,
        ):
            self.group_db.add_child(db_btn)

    def _setup_accounting_menu(self) -> None:
        """Configura il sottomenu della contabilità."""
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

    def _setup_footer(self) -> None:
        """Inizializza il footer della sidebar."""
        self.footer = QWidget()
        f_lay = QVBoxLayout(self.footer)
        f_lay.setContentsMargins(5, 10, 5, 0)
        f_lay.setSpacing(6)
        self.group_notifiche = SidebarGroup("Monitoraggio", get_asset_path(Icons.ACTIVITY))
        self.btn_help = SidebarButton("Guida", get_asset_path(Icons.HELP))
        self.btn_changelog = SidebarButton("Novità", get_asset_path(Icons.LIST))
        self.btn_settings = SidebarButton("Impostazioni", get_asset_path(Icons.SETTINGS))

        self.footer_btns = (self.group_notifiche, self.btn_help, self.btn_changelog, self.btn_settings)
        for footer_btn in self.footer_btns:
            f_lay.addWidget(footer_btn)
            if isinstance(footer_btn, SidebarGroup):
                footer_btn.expanded.connect(self._on_group_expanded)

        self.notif_child_btns = []
        for n, i in (("Notifiche", 0), ("Audit", 1), ("Health", 2)):
            btn = SidebarChildButton(n, "")
            btn.clicked.connect(lambda _, s=i: self.navigation_requested.emit(9, s, -1))
            self.group_notifiche.add_child(btn)
            self.notif_child_btns.append(btn)

        self.content_layout.addWidget(self.footer)

    def _setup_connections(self) -> None:
        """Configura i collegamenti dei segnali."""
        self.btn_palette.clicked.connect(lambda: self.palette_requested.emit())
        self.btn_home.clicked.connect(lambda: self.navigation_requested.emit(0, -1, -1))
        self.btn_timbrature.clicked.connect(lambda: self.navigation_requested.emit(3, -1, -1))
        self.btn_dataease.clicked.connect(lambda: self.navigation_requested.emit(5, -1, -1))
        self.btn_pdl.clicked.connect(lambda: self.navigation_requested.emit(6, -1, -1))
        self.btn_storico_oda.clicked.connect(lambda: self.navigation_requested.emit(10, -1, -1))
        self.btn_help.clicked.connect(lambda: self.navigation_requested.emit(8, -1, -1))
        self.btn_changelog.clicked.connect(lambda: self.navigation_requested.emit(13, -1, -1))
        self.btn_settings.clicked.connect(lambda: self.navigation_requested.emit(7, -1, -1))

    def _on_group_expanded(self, group: SidebarGroup) -> None:
        """Accordion logic."""
        for g in (self.group_automazioni, self.group_db, self.group_contabilita, self.group_notifiche):
            if g != group:
                g.collapse()
        QTimer.singleShot(100, self._update_track)

    def _update_track(self) -> None:
        """Sposta il track magnetico in modo sicuro."""
        if self._is_collapsed:
            self.active_track.hide()
            return

        targets = self._get_all_nav_buttons()

        for t in targets:
            if t.isChecked() and t.isVisible():
                self.anim_manager.move_track(self.active_track, t)
                return
        self.active_track.hide()

    def _get_all_nav_buttons(self) -> list[SidebarButton | SidebarChildButton]:
        """Raccoglie tutti i pulsanti di navigazione per il track."""
        targets: list[SidebarButton | SidebarChildButton] = []

        # Pulsanti dei gruppi
        for g in (self.group_automazioni, self.group_db, self.group_contabilita, self.group_notifiche):
            for e in g.children_elements:
                if isinstance(e, SidebarButton):
                    targets.append(e)
                elif isinstance(e, SidebarSubGroup):
                    targets.append(e.header_btn)
                    targets.extend(e.children_btns)

        # Pulsanti principali e footer
        for b in (*self.main_btns, *self.footer_btns):
            if isinstance(b, SidebarButton):
                targets.append(b)
            elif isinstance(b, SidebarGroup):
                targets.append(b.header_btn)

        return targets

    def set_active_button(self, index: int, sub: int | None = None, bot: int | None = None) -> None:
        """Evidenzia il pulsante attivo."""
        from src.gui.main_window.page_index import PageIndex

        btns = {
            PageIndex.DASHBOARD: self.btn_home,
            PageIndex.SETTINGS: self.btn_settings,
            PageIndex.HELP: self.btn_help,
            PageIndex.CHANGELOG: self.btn_changelog,
            PageIndex.TIMBRATURE: self.btn_timbrature,
            PageIndex.DATAEASE: self.btn_dataease,
            PageIndex.PDL_DB: self.btn_pdl,
            PageIndex.STORICO_ODA: self.btn_storico_oda,
        }
        for i, b in btns.items():
            b.setChecked(i == index)

        for g, indices in (
            (
                self.group_db,
                (
                    PageIndex.TIMBRATURE,
                    PageIndex.DATAEASE,
                    PageIndex.PDL_DB,
                    PageIndex.DIPENDENTI,
                    PageIndex.STORICO_ODA,
                ),
            ),
            (self.group_contabilita, (PageIndex.STRUMENTALE, PageIndex.CONSUNTIVO)),
            (self.group_notifiche, (PageIndex.NOTIFICATIONS,)),
            (self.group_automazioni, (PageIndex.AUTOMAZIONI,)),
        ):
            g.set_active_index(index, indices)

        self._set_sub_button_active(index, sub, bot)
        QTimer.singleShot(150, self._update_track)

    def _set_sub_button_active(self, index: int, sub: int | None, bot: int | None) -> None:
        """Gestisce l'evidenziazione dei pulsanti di terzo livello."""
        from src.gui.main_window.page_index import PageIndex

        # Mappatura dei gruppi con i relativi pulsanti
        mapping = {
            PageIndex.AUTOMAZIONI: self._handle_active_automazioni,
            PageIndex.DIPENDENTI: self._handle_active_dipendenti,
            PageIndex.STRUMENTALE: self._handle_active_strumentale,
            PageIndex.CONSUNTIVO: self._handle_active_consuntivo,
            PageIndex.NOTIFICATIONS: self._handle_active_notifications,
        }

        if handler := mapping.get(PageIndex(index)):
            handler(sub, bot)

    def _handle_active_automazioni(self, sub: int | None, bot: int | None) -> None:
        """Evidenzia sottomenu automazioni."""
        self.sub_fornitori.header_btn.setChecked(sub == 0)
        self.sub_safework.header_btn.setChecked(sub == 1)
        for i, b in enumerate(self.sub_fornitori.children_btns):
            b.setChecked(sub == 0 and i == bot)
        for i, b in enumerate(self.sub_safework.children_btns):
            b.setChecked(sub == 1 and i == bot)

    def _handle_active_dipendenti(self, sub: int | None, _: int | None) -> None:
        """Evidenzia sottomenu dipendenti."""
        self.sub_dipendenti.header_btn.setChecked(True)
        for i, b in enumerate(self.sub_dipendenti.children_btns):
            b.setChecked(i == sub)

    def _handle_active_strumentale(self, sub: int | None, _: int | None) -> None:
        """Evidenzia sottomenu strumentale."""
        self.sub_strumentale.header_btn.setChecked(True)
        for i, b in enumerate(self.sub_strumentale.children_btns):
            b.setChecked(i == sub)

    def _handle_active_consuntivo(self, sub: int | None, _: int | None) -> None:
        """Evidenzia sottomenu consuntivo."""
        self.sub_consuntivo.header_btn.setChecked(True)
        for i, b in enumerate(self.sub_consuntivo.children_btns):
            b.setChecked(i == sub)

    def _handle_active_notifications(self, sub: int | None, _: int | None) -> None:
        """Evidenzia sottomenu notifiche."""
        for i, b in enumerate(self.notif_child_btns):
            b.setChecked(i == sub)

    def enterEvent(self, event: QEnterEvent) -> None:
        """Gestisce l'evento di entrata del mouse (espansione)."""
        self._set_collapsed(False)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """Gestisce l'evento di uscita del mouse (collasso)."""
        if getattr(self, "_drag_in_progress", False):
            super().leaveEvent(event)
            return
        self._set_collapsed(True)
        super().leaveEvent(event)

    def _set_collapsed(self, c: bool) -> None:
        """Gestisce espansione e contrazione senza rompere il layout."""
        if self._is_collapsed == c:
            return
        self._is_collapsed = c

        # Nascondiamo il track durante il movimento per evitare artefatti (gui2.png)
        self.active_track.hide()

        # Animazioni
        self.anim_manager.animate_width(self.collapsed_width if c else self.expanded_width)
        self.anim_manager.animate_content(self.logo_opacity, 0.0 if c else 1.0)
        self.logo_label.setVisible(not c)

        if not c:
            # ESPANSIONE
            self._handle_expansion()
        else:
            # COLLASSO
            self._handle_collapse()

        # Refresh stile per lo sfondo (OBBLIGATORIO per QSS property)
        if style := self.bg_frame.style():
            style.unpolish(self.bg_frame)
            style.polish(self.bg_frame)

        for b in self.main_btns + self.footer_btns:
            if hasattr(b, "set_collapsed"):
                b.set_collapsed(c)
            if isinstance(b, SidebarGroup):
                b.header_btn.set_collapsed(c)

        if not c:
            QTimer.singleShot(50, self._update_ui_state)
        else:
            self._update_ui_state()

        # Riposizionamento track a fine corsa
        QTimer.singleShot(250, self._update_track)

    def _handle_expansion(self) -> None:
        """Logica specifica per l'espansione della sidebar."""
        self.scroll_area.show()
        self.footer.show()
        expanded_margin_left = 14
        expanded_margin_top = 18
        expanded_margin_right = 14
        expanded_margin_bottom = 15
        self.h_lay.setContentsMargins(
            expanded_margin_left, expanded_margin_top, expanded_margin_right, expanded_margin_bottom
        )
        self.h_lay.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        p = self.parentWidget()
        ph = p.height() if p else 800
        height_offset = 20
        self.setMinimumHeight(ph - height_offset)
        self.setMaximumHeight(ph - height_offset)
        self.bg_frame.setProperty("state", "expanded")

    def _handle_collapse(self) -> None:
        """Logica specifica per il collasso della sidebar."""
        collapsed_margin_top = 8
        collapsed_margin_bottom = 15
        self.h_lay.setContentsMargins(0, collapsed_margin_top, 0, collapsed_margin_bottom)
        self.h_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bg_frame.setProperty("state", "collapsed")

        # Nascondiamo SUBITO le aree pesanti per evitare l'overlap (GUI.png)
        self.scroll_area.hide()
        self.footer.hide()
        collapsed_height = 100
        self.setMinimumHeight(collapsed_height)
        self.setMaximumHeight(collapsed_height)

    def _update_ui_state(self) -> None:
        """Sincronizza lo stato dei gruppi."""
        for g in (self.group_db, self.group_automazioni, self.group_contabilita, self.group_notifiche):
            g.set_collapsed(self._is_collapsed)
