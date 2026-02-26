"""
SyncroJob - Sidebar Widget (Next-Gen)
Menu laterale con Glassmorphism, Indicatore Verticale Fluido e telemetria integrata.
Gestisce la navigazione principale dell'applicazione con estetica premium.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRect,
    Qt,
    QTimer,
    pyqtSignal,
)
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.sidebar_button import SidebarButton
from src.utils.helpers import get_asset_path


class SidebarChildButton(SidebarButton):
    """Pulsante figlio con indentazione e stile Glass specifico per i sottomenu."""

    def _update_style(self) -> None:
        """Applica lo stile base aggiungendo indentazione se la sidebar è espansa."""
        super()._update_style()
        if not self._collapsed:
            current_style = self.styleSheet()
            new_style = current_style.replace("padding: 12px 15px;", "padding: 10px 10px 10px 35px;")
            self.setStyleSheet(new_style)


class SidebarGroup(QWidget):
    """
    Gruppo espandibile con segnale di espansione per Accordion logic.
    Gestisce la visibilità selettiva dei pulsanti figli in modalità compatta.
    """

    expanded = pyqtSignal(object)
    """Segnale emesso quando il gruppo viene aperto manualmente."""

    def __init__(self, title: str, icon_path: str, parent: QWidget | None = None) -> None:
        """
        Inizializza un gruppo della sidebar.

        Args:
            title: Titolo del gruppo.
            icon_path: Icona principale.
            parent: Widget genitore.
        """
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
        self._was_expanded = False  # Inizializzato per evitare AttributeError

    def _set_arrow_icon(self, expanded: bool) -> None:
        """Aggiorna l'icona della freccia (Chevron) in base allo stato."""
        from src.utils.helpers import get_colored_icon

        icon_enum = Icons.CHEVRON_DOWN if expanded else Icons.CHEVRON_RIGHT
        icon = get_colored_icon(get_asset_path(icon_enum), "#FFFFFF")
        self.arrow_label.setPixmap(icon.pixmap(12, 12))

    def toggle_group(self) -> None:
        """Inverte lo stato di visibilità della sezione contenuti."""
        is_opening = not self.content_area.isVisible()
        self.content_area.setVisible(is_opening)
        self._set_arrow_icon(is_opening)
        if is_opening:
            self._was_expanded = True
            self.expanded.emit(self)
        else:
            self._was_expanded = False

    def collapse(self) -> None:
        """Chiude forzatamente il gruppo nascondendo i contenuti."""
        self.content_area.setVisible(False)
        self._was_expanded = False
        self._set_arrow_icon(False)

    def add_child(self, btn: SidebarButton) -> None:
        """
        Aggiunge un pulsante figlio alla lista interna.

        Args:
            btn: Istanza SidebarButton da aggiungere.
        """
        self.content_layout.addWidget(btn)
        self.children_btns.append(btn)

    def set_collapsed(self, collapsed: bool) -> None:
        """
        Gestisce la transizione visiva del gruppo tra modalità compatta ed espansa.

        Args:
            collapsed: True se la sidebar è contratta.
        """
        self.header_btn.set_collapsed(collapsed)
        self.arrow_label.setVisible(not collapsed)

        has_active_child = False
        for btn in self.children_btns:
            btn.set_collapsed(collapsed)
            if btn.isChecked():
                has_active_child = True

            # In modalità compatta, mostriamo solo il figlio attivo
            if collapsed:
                btn.setVisible(btn.isChecked())
            else:
                btn.setVisible(True)

        if collapsed:
            # Mostra l'area contenuto SOLO se ha un figlio attivo
            self.content_area.setVisible(has_active_child)
        else:
            self.content_area.setVisible(self._was_expanded)

        self._set_arrow_icon(self.content_area.isVisible() and not collapsed)

    def set_active_index(self, index: int, group_indices: Sequence[int]) -> None:
        """
        Attiva i pulsanti interni se l'indice corrisponde a uno di quelli del gruppo.

        Args:
            index: Indice della pagina attiva.
            group_indices: Lista di indici appartenenti a questo gruppo.
        """
        is_child_active = index in group_indices
        self.header_btn.setChecked(is_child_active)

        # Aggiorna lo stato dei figli
        for btn, idx in zip(self.children_btns, group_indices, strict=False):
            is_this_checked = idx == index
            btn.setChecked(is_this_checked)
            # Se siamo collassati, aggiorniamo subito la visibilità
            if self.header_btn._collapsed:
                btn.setVisible(is_this_checked)

        if is_child_active:
            self.content_area.setVisible(True)
            if not self.header_btn._collapsed:
                self._was_expanded = True

        self._set_arrow_icon(self.content_area.isVisible() and not self.header_btn._collapsed)


class SidebarWidget(QFrame):
    """
    Sidebar Enterprise con Glassmorphism e Indicatore Verticale Fluido.
    Gestisce il menu di navigazione principale con supporto per l'espansione al passaggio del mouse.
    """

    navigation_requested = pyqtSignal(int)
    """Segnale emesso per richiedere il cambio della pagina principale."""

    automation_tab_requested = pyqtSignal(int)
    """Segnale emesso per switchare i tab interni dei bot (Fornitori/SafeWork)."""

    notifications_tab_requested = pyqtSignal(int)
    """Segnale emesso per switchare i tab interni del monitoraggio."""

    palette_requested = pyqtSignal()
    """Segnale per aprire la Command Palette."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza la sidebar.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.setObjectName("sidebarFrame")
        self._is_collapsed = True
        self.expanded_width = 230
        self.collapsed_width = 75
        self.setMouseTracking(True)
        self.setFixedWidth(self.collapsed_width)

        self.setStyleSheet(self._get_glass_style())
        self._setup_ui()

        # --- INDICATORE VERTICALE PREMIUM (The Track) ---
        self.active_track = QWidget(self)
        self.active_track.setFixedWidth(5)
        self.active_track.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4DB6AC, stop:0.5 #009688, stop:1 #00796B);
            border-radius: 2px;
        """)

        # Effetto Glow per la linea
        track_glow = QGraphicsDropShadowEffect(self.active_track)
        track_glow.setBlurRadius(15)
        track_glow.setColor(QColor(0, 150, 136, 150))
        track_glow.setOffset(0, 0)
        self.active_track.setGraphicsEffect(track_glow)

        self.active_track.raise_()
        self._track_anim = QPropertyAnimation(self.active_track, b"geometry")
        self._track_anim.setDuration(450)
        self._track_anim.setEasingCurve(QEasingCurve.Type.OutQuint)

        self._update_ui_state()
        QTimer.singleShot(500, self._update_track_instant)

    def _get_glass_style(self) -> str:
        """Restituisce lo stile QSS avanzato per il look Glassmorphism."""
        return """
            QFrame#sidebarFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a2639, stop:1 #0d1421);
                border-right: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 15px;
            }
            QScrollArea { border: none; background: transparent; }
            QWidget#scrollContent { background: transparent; }

            /* Nascondi Scrollbar Orizzontale */
            QScrollBar:horizontal { height: 0px; }

            /* Scrollbar Verticale Sottile */
            QScrollBar:vertical {
                border: none; background: transparent; width: 4px; margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.1); border-radius: 2px; min-height: 30px;
            }
            QScrollBar::handle:vertical:hover { background: rgba(255, 255, 255, 0.2); }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """

    def _setup_ui(self) -> None:
        """Costruisce la gerarchia interna degli elementi (Header, Menu, Footer)."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(0)

        # Header
        self.header_container = QWidget()
        h_layout = QHBoxLayout(self.header_container)
        h_layout.setContentsMargins(12, 5, 10, 15)
        h_layout.setSpacing(12)

        # --- LOGO BADGE (Radiant Halo) ---
        self.logo_badge = QFrame()
        self.logo_badge.setFixedSize(42, 42)
        self.logo_badge.setStyleSheet("""
            background: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 21px;
        """)
        badge_layout = QVBoxLayout(self.logo_badge)
        badge_layout.setContentsMargins(0, 0, 0, 0)
        badge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Effetto Glow per il Badge (Bianco più deciso)
        logo_glow = QGraphicsDropShadowEffect(self.logo_badge)
        logo_glow.setBlurRadius(15)
        logo_glow.setColor(QColor(255, 255, 255, 80))
        logo_glow.setOffset(0, 0)
        self.logo_badge.setGraphicsEffect(logo_glow)

        self.logo_icon = QLabel()
        pix = QPixmap(get_asset_path("assets/app.ico"))
        if not pix.isNull():
            self.logo_icon.setPixmap(
                pix.scaled(
                    28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                )
            )

        badge_layout.addWidget(self.logo_icon)
        h_layout.addWidget(self.logo_badge)

        self.logo_label = QLabel("SyncroJob")
        self.logo_label.setStyleSheet("font-size: 18px; font-weight: 900; color: white; letter-spacing: 0.5px;")
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
        self.btn_palette.clicked.connect(self.palette_requested.emit)
        self.menu_layout.addWidget(self.btn_palette)

        self.btn_home = SidebarButton("Home", get_asset_path(Icons.HOME))
        self.btn_home.clicked.connect(lambda: self.navigation_requested.emit(0))
        self.menu_layout.addWidget(self.btn_home)

        self.group_automazioni = SidebarGroup("Automazioni", get_asset_path(Icons.CPU))
        self.group_automazioni.expanded.connect(self._on_group_expanded)
        self.menu_layout.addWidget(self.group_automazioni)

        self.btn_fornitori = SidebarChildButton("Portale Fornitori", get_asset_path(Icons.GLOBE))
        self.btn_fornitori.clicked.connect(lambda: self._handle_automazione_click(0))
        self.group_automazioni.add_child(self.btn_fornitori)

        self.btn_safework = SidebarChildButton("SafeWork", get_asset_path(Icons.SHIELD))
        self.btn_safework.clicked.connect(lambda: self._handle_automazione_click(1))
        self.group_automazioni.add_child(self.btn_safework)

        self.group_db = SidebarGroup("Database", get_asset_path(Icons.DATABASE))
        self.group_db.expanded.connect(self._on_group_expanded)
        self.menu_layout.addWidget(self.group_db)

        # Sotto-pulsanti DB
        self.btn_timbrature = SidebarChildButton("Timbrature", get_asset_path(Icons.CLOCK))
        self.btn_timbrature.clicked.connect(lambda: self.navigation_requested.emit(3))
        self.group_db.add_child(self.btn_timbrature)

        self.btn_strumentale = SidebarChildButton("Strumentale", get_asset_path(Icons.FOLDER))
        self.btn_strumentale.clicked.connect(lambda: self.navigation_requested.emit(4))
        self.group_db.add_child(self.btn_strumentale)

        self.btn_dataease = SidebarChildButton("DataEase", get_asset_path(Icons.DOWNLOAD))
        self.btn_dataease.clicked.connect(lambda: self.navigation_requested.emit(5))
        self.group_db.add_child(self.btn_dataease)

        self.btn_pdl = SidebarChildButton("PDL", get_asset_path(Icons.PDL))
        self.btn_pdl.clicked.connect(lambda: self.navigation_requested.emit(6))
        self.group_db.add_child(self.btn_pdl)

        self.btn_dipendenti = SidebarChildButton("Dipendenti", get_asset_path(Icons.DIPENDENTI))
        self.btn_dipendenti.clicked.connect(lambda: self.navigation_requested.emit(11))
        self.group_db.add_child(self.btn_dipendenti)

        self.btn_storico_oda = SidebarChildButton("Storico OdA", get_asset_path(Icons.FILE_TEXT))
        self.btn_storico_oda.clicked.connect(lambda: self.navigation_requested.emit(10))
        self.group_db.add_child(self.btn_storico_oda)

        self.btn_lyra = SidebarButton("Lyra AI", get_asset_path(Icons.SPARKLES))
        self.btn_lyra.clicked.connect(lambda: self.navigation_requested.emit(2))
        self.menu_layout.addWidget(self.btn_lyra)

        self.group_notifiche = SidebarGroup("Monitoraggio", get_asset_path(Icons.ACTIVITY))
        self.group_notifiche.expanded.connect(self._on_group_expanded)
        self.menu_layout.addWidget(self.group_notifiche)

        self.btn_notifiche = SidebarChildButton("Notifiche", get_asset_path(Icons.BELL))
        self.btn_notifiche.clicked.connect(lambda: self._handle_notifications_click(0))
        self.group_notifiche.add_child(self.btn_notifiche)

        self.btn_audit = SidebarChildButton("Audit", get_asset_path(Icons.SHIELD))
        self.btn_audit.clicked.connect(lambda: self._handle_notifications_click(1))
        self.group_notifiche.add_child(self.btn_audit)

        self.btn_health = SidebarChildButton("Health", get_asset_path(Icons.ACTIVITY))
        self.btn_health.clicked.connect(lambda: self._handle_notifications_click(2))
        self.group_notifiche.add_child(self.btn_health)

        self.menu_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Footer Fisso (Sotto la scroll area)
        self.footer = QWidget()
        f_layout = QVBoxLayout(self.footer)
        f_layout.setContentsMargins(5, 10, 5, 0)
        self.btn_help = SidebarButton("Guida", get_asset_path(Icons.HELP))
        self.btn_help.clicked.connect(lambda: self.navigation_requested.emit(8))
        self.btn_settings = SidebarButton("Impostazioni", get_asset_path(Icons.SETTINGS))
        self.btn_settings.clicked.connect(lambda: self.navigation_requested.emit(7))
        f_layout.addWidget(self.btn_help)
        f_layout.addWidget(self.btn_settings)
        layout.addWidget(self.footer)

    def _on_group_expanded(self, group: SidebarGroup) -> None:
        """Logica Accordion: chiude tutti i gruppi tranne quello appena espanso."""
        for g in (self.group_automazioni, self.group_db, self.group_notifiche):
            if g != group:
                g.collapse()
        QTimer.singleShot(100, self._update_track)

    def _animate_track(self, target_widget: QWidget) -> None:
        """
        Avvia l'animazione della linea magnetica verso il pulsante target.

        Args:
            target_widget: Il widget su cui posizionare l'indicatore.
        """
        if not target_widget or not target_widget.isVisible():
            return
        pos = target_widget.mapTo(self, QPoint(0, 0))
        target_rect = QRect(2, pos.y() + 8, 5, target_widget.height() - 16)
        self.active_track.show()
        self._track_anim.stop()
        self._track_anim.setEndValue(target_rect)
        self._track_anim.start()

    def _update_track(self) -> None:
        """Cerca il pulsante attualmente selezionato e aggiorna la traccia."""
        all_btns = [
            self.btn_home,
            self.btn_lyra,
            self.btn_help,
            self.btn_settings,
            self.btn_fornitori,
            self.btn_safework,
            self.btn_timbrature,
            self.btn_strumentale,
            self.btn_dataease,
            self.btn_pdl,
            self.btn_dipendenti,
            self.btn_storico_oda,
            self.btn_notifiche,
            self.btn_audit,
            self.btn_health,
        ]
        for btn in all_btns:
            if btn.isChecked() and btn.isVisible():
                self._animate_track(btn)
                return
        self.active_track.hide()

    def _update_track_instant(self) -> None:
        """Aggiorna istantaneamente la posizione della traccia senza animazioni."""
        self._update_track()

    def set_active_button(self, index: int, sub_index: int | None = None) -> None:
        """
        Sincronizza lo stato dei pulsanti della sidebar con la pagina attiva della MainWindow.

        Args:
            index: Indice della pagina principale.
            sub_index: Indice della sottoscheda (opzionale).
        """
        btns = {0: self.btn_home, 2: self.btn_lyra, 7: self.btn_settings, 8: self.btn_help}
        for i, b in btns.items():
            b.setChecked(i == index)
        self.group_db.set_active_index(index, (3, 4, 5, 6, 11, 10))
        self.group_notifiche.set_active_index(index, (9,))  # Notifiche usa 9 come indice base
        if index == 9:
            self.btn_notifiche.setChecked(sub_index == 0)
            self.btn_audit.setChecked(sub_index == 1)
            self.btn_health.setChecked(sub_index == 2)
        self.group_automazioni.set_active_index(index, (1,))
        if index == 1:
            self.btn_fornitori.setChecked(sub_index == 0)
            self.btn_safework.setChecked(sub_index == 1)
        QTimer.singleShot(150, self._update_track)

    def enterEvent(self, e) -> None:
        """Espande la sidebar all'ingresso del mouse."""
        self._set_collapsed(False)
        super().enterEvent(e)

    def leaveEvent(self, e) -> None:
        """Contrae la sidebar all'uscita del mouse."""
        self._set_collapsed(True)
        super().leaveEvent(e)

    def _set_collapsed(self, c: bool) -> None:
        """Imposta lo stato di contrazione e aggiorna il layout."""
        self._is_collapsed = c
        self.setFixedWidth(self.collapsed_width if c else self.expanded_width)
        self._update_ui_state()
        QTimer.singleShot(150, self._update_track)

    def _update_ui_state(self) -> None:
        """Sincronizza la visibilità degli elementi testuali e delle icone badge."""
        self.logo_label.setVisible(not self._is_collapsed)
        for b in (self.btn_home, self.btn_lyra, self.btn_help, self.btn_settings, self.btn_palette):
            b.set_collapsed(self._is_collapsed)
        for g in (self.group_db, self.group_automazioni, self.group_notifiche):
            g.set_collapsed(self._is_collapsed)

    def _handle_automazione_click(self, tab_index: int) -> None:
        """Inoltra la navigazione ai tab dei bot."""
        self.navigation_requested.emit(1)
        self.automation_tab_requested.emit(tab_index)

    def _handle_notifications_click(self, tab_index: int) -> None:
        """Inoltra la navigazione ai tab del monitoraggio."""
        self.navigation_requested.emit(9)
        self.notifications_tab_requested.emit(tab_index)
