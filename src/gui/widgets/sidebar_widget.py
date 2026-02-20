"""
SyncroJob - Sidebar Widget
Gestione del menu di navigazione laterale con icone, sottomenu espandibili e indicatori di stato.
Supporta modalità collassata/espansa e integrazione con il sistema di notifiche.
"""

from __future__ import annotations

from typing import Any, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.widgets.sidebar_button import SidebarButton
from src.utils.helpers import get_asset_path


class SidebarChildButton(SidebarButton):
    """Pulsante figlio indentato per i sottomenu della sidebar."""

    def _update_style(self) -> None:
        """Applica lo stile base e aggiunge indentazione se la sidebar è espansa."""
        super()._update_style()
        if not self._collapsed:
            current_style = self.styleSheet()
            new_style = current_style.replace(
                "padding: 12px 15px;", "padding: 10px 10px 10px 35px;"
            )
            self.setStyleSheet(new_style)


class SidebarGroup(QWidget):
    """
    Gruppo espandibile per la sidebar.
    Contiene un pulsante header e un'area di contenuto per i pulsanti figli.
    """

    def __init__(self, title: str, icon_path: str, parent: QWidget | None = None) -> None:
        """
        Inizializza il gruppo della sidebar.

        Args:
            title: Titolo del gruppo.
            icon_path: Percorso dell'icona del gruppo.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Container per header (pulsante + freccia)
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 10, 0)
        header_layout.setSpacing(0)

        self.header_btn = SidebarButton(title, icon_path)
        header_layout.addWidget(self.header_btn, stretch=1)

        # Freccia indicatore
        self.arrow_label = QLabel()
        self.arrow_label.setFixedSize(16, 16)
        self.arrow_label.setStyleSheet("background: transparent;")
        self._set_arrow_icon(expanded=False)
        header_layout.addWidget(self.arrow_label)

        self.main_layout.addWidget(header_container)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(2)

        self.content_area.setVisible(False)  # Default chiuso
        self.main_layout.addWidget(self.content_area)

        self.header_btn.clicked.connect(self.toggle_group)
        self.children_btns: list[SidebarButton] = []
        self._was_expanded = False

    def _set_arrow_icon(self, expanded: bool) -> None:
        """Imposta l'icona della freccia (giù o destra)."""
        from src.utils.helpers import get_colored_icon

        icon_enum = Icons.CHEVRON_DOWN if expanded else Icons.CHEVRON_RIGHT
        icon = get_colored_icon(get_asset_path(icon_enum), "#FFFFFF")
        self.arrow_label.setPixmap(icon.pixmap(14, 14))

    def _update_arrow(self) -> None:
        """Aggiorna l'orientamento della freccia basandosi sulla visibilità del contenuto."""
        self._set_arrow_icon(self.content_area.isVisible())

    def add_child(self, btn: SidebarButton) -> None:
        """Aggiunge un pulsante figlio al gruppo."""
        self.content_layout.addWidget(btn)
        self.children_btns.append(btn)

    def toggle_group(self) -> None:
        """Inverte lo stato di espansione del gruppo."""
        is_visible = self.content_area.isVisible()
        self.content_area.setVisible(not is_visible)
        self._was_expanded = not is_visible
        self._update_arrow()

    def set_collapsed(self, collapsed: bool) -> None:
        """Configura lo stato collassato del gruppo e dei suoi figli."""
        self.header_btn.set_collapsed(collapsed)
        self.arrow_label.setVisible(not collapsed)
        for btn in self.children_btns:
            btn.set_collapsed(collapsed)

        if collapsed:
            self._was_expanded = self.content_area.isVisible()
            self.content_area.setVisible(False)
        else:
            self.content_area.setVisible(self._was_expanded)
        self._update_arrow()

    def set_active_index(self, index: int, group_indices: list[int]) -> None:
        """Gestisce lo stato attivo del gruppo e seleziona il figlio corrispondente."""
        is_child_active = index in group_indices
        self.header_btn.setChecked(is_child_active)

        if is_child_active and not self.header_btn._collapsed:
            self.content_area.setVisible(True)
            self._update_arrow()

        for btn, idx in zip(self.children_btns, group_indices, strict=False):
            btn.setChecked(idx == index)


class SidebarWidget(QFrame):
    """Widget della sidebar principale con supporto per sottomenu e stati animati."""

    navigation_requested = pyqtSignal(int)
    automation_tab_requested = pyqtSignal(int)
    notifications_tab_requested = pyqtSignal(int)
    palette_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza la sidebar e configura lo stato iniziale collassato."""
        super().__init__(parent)
        self.setObjectName("sidebarFrame")
        self._is_collapsed = True
        self.setMouseTracking(True)

        self.expanded_width = 220
        self.collapsed_width = 70

        self.setFixedWidth(self.collapsed_width)
        self.setStyleSheet(
            """
            QFrame#sidebarFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1E293B, stop:1 #0F172A);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
            }
            QLabel { color: white; background: transparent; }
        """
        )

        self._setup_ui()
        self._update_ui_state()

    def enterEvent(self, event: Any) -> None:
        """Espande automaticamente la sidebar quando il mouse entra nell'area."""
        if self._is_collapsed:
            self._set_collapsed(False)
        super().enterEvent(event)

    def leaveEvent(self, event: Any) -> None:
        """Collassa automaticamente la sidebar quando il mouse esce dall'area."""
        if not self._is_collapsed:
            self._set_collapsed(True)
        super().leaveEvent(event)

    def _set_collapsed(self, collapsed: bool) -> None:
        """Cambia lo stato di espansione e aggiorna la larghezza del widget."""
        self._is_collapsed = collapsed
        target_width = self.collapsed_width if collapsed else self.expanded_width
        self.setFixedWidth(target_width)
        self._update_ui_state()

    def _update_ui_state(self) -> None:
        """Aggiorna la visibilità di tutti i componenti interni in base allo stato collassato."""
        self.logo_icon.setVisible(not self._is_collapsed)
        self.logo_label.setVisible(not self._is_collapsed)
        self.separator.setVisible(not self._is_collapsed)

        if hasattr(self, "sep_1"):
            self.sep_1.setVisible(not self._is_collapsed)
        if hasattr(self, "sep_2"):
            self.sep_2.setVisible(not self._is_collapsed)

        for btn in (
            self.btn_home,
            self.btn_lyra,
            self.btn_help,
            self.btn_settings,
            self.btn_palette,
        ):
            btn.set_collapsed(self._is_collapsed)

        self.group_db.set_collapsed(self._is_collapsed)
        self.group_automazioni.set_collapsed(self._is_collapsed)
        self.group_notifiche.set_collapsed(self._is_collapsed)

    def _create_elegant_separator(self) -> QFrame:
        """Crea un divisore visivo con gradiente per separare le sezioni."""
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent,
                    stop:0.2 rgba(255, 255, 255, 0.15),
                    stop:0.5 rgba(255, 255, 255, 0.25),
                    stop:0.8 rgba(255, 255, 255, 0.15),
                    stop:1 transparent
                );
                margin: 8px 15px;
                border: none;
            }
        """
        )
        return sep

    def _setup_ui(self) -> None:
        """Costruisce la gerarchia dei widget della sidebar."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 20, 5, 20)
        layout.setSpacing(8)

        # Header con Logo
        header_container = QFrame()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(10, 0, 0, 0)
        header_layout.setSpacing(8)

        from PyQt6.QtGui import QPixmap

        self.logo_icon = QLabel()
        logo_pixmap = QPixmap(get_asset_path("assets/app.ico"))
        if not logo_pixmap.isNull():
            self.logo_icon.setPixmap(
                logo_pixmap.scaled(
                    28,
                    28,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        self.logo_icon.setFixedSize(28, 28)
        header_layout.addWidget(self.logo_icon)

        self.logo_label = QLabel("SyncroJob")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setStyleSheet(
            "font-size: 20px; font-weight: 900; letter-spacing: 1px; color: #ffffff; border: none;"
        )
        header_layout.addWidget(self.logo_label)
        header_layout.addStretch()
        layout.addWidget(header_container)

        self.separator = QFrame()
        self.separator.setObjectName("sidebarSeparator")
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setStyleSheet("color: rgba(255,255,255,0.3);")
        layout.addWidget(self.separator)

        layout.addSpacing(10)

        # Pulsante Apri Palette
        self.btn_palette = SidebarButton("Apri Palette", get_asset_path(Icons.COMMAND_PALETTE))
        self.btn_palette.setToolTip("Apri Command Palette (Ctrl+K)")
        self.btn_palette.clicked.connect(self.palette_requested.emit)
        layout.addWidget(self.btn_palette)

        layout.addSpacing(10)

        # 0: Home
        self.btn_home = SidebarButton("Home", get_asset_path(Icons.HOME))
        self.btn_home.clicked.connect(lambda: self.navigation_requested.emit(0))
        layout.addWidget(self.btn_home)

        # -- GRUPPO AUTOMAZIONI --
        self.group_automazioni = SidebarGroup("Automazioni", get_asset_path(Icons.CPU))
        layout.addWidget(self.group_automazioni)

        self.btn_fornitori = SidebarChildButton("Portale Fornitori", get_asset_path(Icons.GLOBE))
        self.btn_fornitori.clicked.connect(lambda: self._handle_automazione_click(0))
        self.group_automazioni.add_child(self.btn_fornitori)

        self.btn_safework = SidebarChildButton("SafeWork", get_asset_path(Icons.SHIELD))
        self.btn_safework.clicked.connect(lambda: self._handle_automazione_click(1))
        self.group_automazioni.add_child(self.btn_safework)

        self.sep_1 = self._create_elegant_separator()
        layout.addWidget(self.sep_1)

        # -- GRUPPO DATABASE --
        self.group_db = SidebarGroup("Database", get_asset_path(Icons.DATABASE))
        layout.addWidget(self.group_db)

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

        layout.addStretch()

        self.sep_2 = self._create_elegant_separator()
        layout.addWidget(self.sep_2)

        # 2: Lyra AI
        self.btn_lyra = SidebarButton("Lyra AI", get_asset_path(Icons.SPARKLES))
        self.btn_lyra.clicked.connect(lambda: self.navigation_requested.emit(2))
        layout.addWidget(self.btn_lyra)

        # -- GRUPPO MONITORAGGIO --
        self.group_notifiche = SidebarGroup("Monitoraggio", get_asset_path(Icons.ACTIVITY))
        layout.addWidget(self.group_notifiche)

        self.btn_notifiche = SidebarChildButton("Notifiche", get_asset_path(Icons.BELL))
        self.btn_notifiche.clicked.connect(lambda: self._handle_notifications_click(0))
        self.group_notifiche.add_child(self.btn_notifiche)

        self.btn_audit = SidebarChildButton("Audit", get_asset_path(Icons.SHIELD))
        self.btn_audit.clicked.connect(lambda: self._handle_notifications_click(1))
        self.group_notifiche.add_child(self.btn_audit)

        self.btn_health = SidebarChildButton("Health", get_asset_path(Icons.ACTIVITY))
        self.btn_health.clicked.connect(lambda: self._handle_notifications_click(2))
        self.group_notifiche.add_child(self.btn_health)

        self.btn_help = SidebarButton("Guida", get_asset_path(Icons.HELP))
        self.btn_help.clicked.connect(lambda: self.navigation_requested.emit(8))
        layout.addWidget(self.btn_help)

        layout.addSpacing(10)

        self.btn_settings = SidebarButton("Impostazioni", get_asset_path(Icons.SETTINGS))
        self.btn_settings.clicked.connect(lambda: self.navigation_requested.emit(7))
        layout.addWidget(self.btn_settings)

    def _handle_automazione_click(self, tab_index: int) -> None:
        """Naviga alla pagina automazioni e seleziona il tab interno."""
        self.navigation_requested.emit(1)
        self.automation_tab_requested.emit(tab_index)

    def _handle_notifications_click(self, tab_index: int) -> None:
        """Naviga alla pagina monitoraggio e seleziona il tab interno."""
        self.navigation_requested.emit(9)
        self.notifications_tab_requested.emit(tab_index)

    def set_active_button(self, index: int, sub_index: Optional[int] = None) -> None:
        """Aggiorna lo stato visivo (checked) dei pulsanti basandosi sulla pagina attiva."""
        buttons_map = {
            0: self.btn_home,
            2: self.btn_lyra,
            7: self.btn_settings,
            8: self.btn_help,
        }

        for idx, btn in buttons_map.items():
            btn.setChecked(idx == index)

        self.group_db.set_active_index(index, [3, 4, 5, 6, 11, 10])

        if index == 9:
            self.group_notifiche.header_btn.setChecked(True)
            self.btn_notifiche.setChecked(sub_index == 0)
            self.btn_audit.setChecked(sub_index == 1)
            self.btn_health.setChecked(sub_index == 2)
        else:
            self.group_notifiche.header_btn.setChecked(False)
            self.btn_notifiche.setChecked(False)
            self.btn_audit.setChecked(False)
            self.btn_health.setChecked(False)

        if index == 1:
            self.group_automazioni.header_btn.setChecked(True)
            self.btn_fornitori.setChecked(sub_index == 0)
            self.btn_safework.setChecked(sub_index == 1)
        else:
            self.group_automazioni.header_btn.setChecked(False)
            self.btn_fornitori.setChecked(False)
            self.btn_safework.setChecked(False)
