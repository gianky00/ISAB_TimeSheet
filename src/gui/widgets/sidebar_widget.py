from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.widgets.sidebar_button import SidebarButton
from src.utils.helpers import get_asset_path


class SidebarChildButton(SidebarButton):
    """Pulsante figlio indentato per i sottomenu."""

    def _update_style(self):
        super()._update_style()
        if not self._collapsed:
            # Sovrascriviamo per aggiungere indentazione extra
            current_style = self.styleSheet()
            new_style = current_style.replace(
                "padding: 12px 15px;", "padding: 10px 10px 10px 35px;"
            )
            self.setStyleSheet(new_style)


class SidebarGroup(QWidget):
    """Gruppo espandibile per la sidebar."""

    def __init__(self, title, icon_path, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.header_btn = SidebarButton(title, icon_path)
        # Indicatore freccia (verrà gestito dinamicamente se necessario)
        self.layout.addWidget(self.header_btn)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(2)

        self.content_area.setVisible(False)  # Default chiuso
        self.layout.addWidget(self.content_area)

        self.header_btn.clicked.connect(self.toggle_group)
        self.children_btns = []
        self._was_expanded = False  # Memorizza stato apertura prima del collasso

    def add_child(self, btn: SidebarButton):
        self.content_layout.addWidget(btn)
        self.children_btns.append(btn)

    def toggle_group(self):
        is_visible = self.content_area.isVisible()
        self.content_area.setVisible(not is_visible)
        # Aggiorna anche lo stato memorizzato
        self._was_expanded = not is_visible

    def set_collapsed(self, collapsed):
        self.header_btn.set_collapsed(collapsed)
        for btn in self.children_btns:
            btn.set_collapsed(collapsed)

        if collapsed:
            # Salva lo stato corrente prima di collassare
            self._was_expanded = self.content_area.isVisible()
            self.content_area.setVisible(False)
        else:
            # Ripristina lo stato salvato quando si espande
            self.content_area.setVisible(self._was_expanded)

    def set_active_index(self, index, group_indices):
        """Gestisce lo stato attivo del gruppo e dei figli."""
        is_child_active = index in group_indices
        self.header_btn.setChecked(is_child_active)

        if is_child_active and not self.header_btn._collapsed:
            self.content_area.setVisible(True)

        for btn, idx in zip(self.children_btns, group_indices, strict=False):
            btn.setChecked(idx == index)


class SidebarWidget(QFrame):
    """Widget della sidebar per la navigazione principale, collassabile."""

    navigation_requested = pyqtSignal(int)
    automation_tab_requested = pyqtSignal(int)  # 0: Fornitori, 1: Safework
    notifications_tab_requested = pyqtSignal(int)  # 0: Notifiche, 1: Audit

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebarFrame")
        self._is_collapsed = True  # Partenza collassata
        self.setMouseTracking(True)  # Importante per hover

        # Larghezze
        self.expanded_width = 220
        self.collapsed_width = 70

        self.setFixedWidth(self.collapsed_width)  # Start collapsed
        self.setStyleSheet(
            """
            QFrame#sidebarFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1E293B, stop:1 #0F172A); /* Dark Navy Blue Theme */
                border-right: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
            }
            QLabel { color: white; background: transparent; }
        """
        )

        self._setup_ui()

        # Stato iniziale visuale
        self._update_ui_state()

    def enterEvent(self, event):
        """Espande la sidebar al passaggio del mouse."""
        if self._is_collapsed:
            self._set_collapsed(False)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Collassa la sidebar all'uscita del mouse."""
        if not self._is_collapsed:
            self._set_collapsed(True)
        super().leaveEvent(event)

    def _set_collapsed(self, collapsed):
        """Imposta lo stato ed esegue l'animazione/update."""
        self._is_collapsed = collapsed
        target_width = self.collapsed_width if collapsed else self.expanded_width
        self.setFixedWidth(target_width)
        self._update_ui_state()

    def _update_ui_state(self):
        """Aggiorna visibilità elementi in base allo stato."""
        self.logo_label.setVisible(not self._is_collapsed)
        self.separator.setVisible(not self._is_collapsed)

        # Aggiorna pulsanti
        for btn in [
            self.btn_home,
            self.btn_lyra,
            self.btn_help,
            self.btn_settings,
        ]:
            btn.set_collapsed(self._is_collapsed)

        # Aggiorna Gruppi
        self.group_db.set_collapsed(self._is_collapsed)
        self.group_automazioni.set_collapsed(self._is_collapsed)
        self.group_notifiche.set_collapsed(self._is_collapsed)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 20, 5, 20)
        layout.setSpacing(8)

        # Header con Logo (Toggle rimosso)
        header_container = QFrame()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(15, 0, 0, 0)  # Padding sinistro per logo
        header_layout.setSpacing(10)

        self.logo_label = QLabel("SyncroJob")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setStyleSheet(
            "font-size: 20px; font-weight: 900; letter-spacing: 1px; color: #ffffff; border: none;"
        )

        header_layout.addWidget(self.logo_label)
        header_layout.addStretch()

        layout.addWidget(header_container)

        # Separatore
        self.separator = QFrame()
        self.separator.setObjectName("sidebarSeparator")
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setStyleSheet("color: rgba(255,255,255,0.3);")
        layout.addWidget(self.separator)

        layout.addSpacing(15)

        # --- MENU ITEMS ---

        # 0: Home
        self.btn_home = SidebarButton("Home", get_asset_path(Icons.HOME))
        self.btn_home.clicked.connect(lambda: self._handle_click(0))
        layout.addWidget(self.btn_home)

        # -- GRUPPO AUTOMAZIONI (Livello 1) --
        self.group_automazioni = SidebarGroup("Automazioni", get_asset_path(Icons.CPU))
        layout.addWidget(self.group_automazioni)

        # Figlio: Portale Fornitori
        self.btn_fornitori = SidebarChildButton(
            "Portale Fornitori", get_asset_path(Icons.GLOBE)
        )
        self.btn_fornitori.clicked.connect(lambda: self._handle_automazione_click(0))
        self.group_automazioni.add_child(self.btn_fornitori)

        # Figlio: SafeWork
        self.btn_safework = SidebarChildButton("SafeWork", get_asset_path(Icons.SHIELD))
        self.btn_safework.clicked.connect(lambda: self._handle_automazione_click(1))
        self.group_automazioni.add_child(self.btn_safework)

        # -- GRUPPO DATABASE (Livello 1) --
        self.group_db = SidebarGroup("Database", get_asset_path(Icons.DATABASE))
        layout.addWidget(self.group_db)

        # 3: Timbrature (Clock)
        self.btn_timbrature = SidebarChildButton(
            "Timbrature", get_asset_path(Icons.CLOCK)
        )
        self.btn_timbrature.clicked.connect(lambda: self._handle_child_click(3))
        self.group_db.add_child(self.btn_timbrature)

        # 4: Strumentale (Folder)
        self.btn_strumentale = SidebarChildButton(
            "Strumentale", get_asset_path(Icons.FOLDER)
        )
        self.btn_strumentale.clicked.connect(lambda: self._handle_child_click(4))
        self.group_db.add_child(self.btn_strumentale)

        # 5: DataEase (Cloud Download)
        self.btn_dataease = SidebarChildButton(
            "DataEase", get_asset_path(Icons.DOWNLOAD)
        )
        self.btn_dataease.clicked.connect(lambda: self._handle_child_click(5))
        self.group_db.add_child(self.btn_dataease)

        # 6: PDL (ex Anagrafiche)
        self.btn_pdl = SidebarChildButton("PDL", get_asset_path(Icons.PDL))
        self.btn_pdl.clicked.connect(lambda: self._handle_child_click(6))
        self.group_db.add_child(self.btn_pdl)

        # 11: Dipendenti (Users)
        self.btn_dipendenti = SidebarChildButton(
            "Dipendenti", get_asset_path(Icons.DIPENDENTI)
        )
        self.btn_dipendenti.clicked.connect(lambda: self._handle_child_click(11))
        self.group_db.add_child(self.btn_dipendenti)

        # 10: Storico OdA
        self.btn_storico_oda = SidebarChildButton(
            "Storico OdA", get_asset_path(Icons.FILE_TEXT)
        )
        self.btn_storico_oda.clicked.connect(lambda: self._handle_child_click(10))
        self.group_db.add_child(self.btn_storico_oda)

        layout.addStretch()

        # 2: Lyra AI
        self.btn_lyra = SidebarButton("Lyra AI", get_asset_path(Icons.SPARKLES))
        self.btn_lyra.clicked.connect(lambda: self._handle_click(2))
        layout.addWidget(self.btn_lyra)

        # -- GRUPPO NOTIFICHE (Livello 1) --
        self.group_notifiche = SidebarGroup("Notifiche", get_asset_path(Icons.BELL))
        layout.addWidget(self.group_notifiche)

        # Figlio: Audit
        self.btn_audit = SidebarChildButton("Audit", get_asset_path(Icons.SHIELD))
        self.btn_audit.clicked.connect(lambda: self._handle_notifications_click(1))
        self.group_notifiche.add_child(self.btn_audit)

        # 8: Guida
        self.btn_help = SidebarButton("Guida", get_asset_path(Icons.HELP))
        self.btn_help.clicked.connect(lambda: self._handle_click(8))
        layout.addWidget(self.btn_help)

        layout.addSpacing(10)

        # 7: Impostazioni
        self.btn_settings = SidebarButton(
            "Impostazioni", get_asset_path(Icons.SETTINGS)
        )
        self.btn_settings.clicked.connect(lambda: self._handle_click(7))
        layout.addWidget(self.btn_settings)

    def _handle_click(self, index):
        """Gestisce il click sui pulsanti standard."""
        self.navigation_requested.emit(index)

    def _handle_child_click(self, index):
        """Gestisce il click sui figli diretti (Database)."""
        self.navigation_requested.emit(index)

    def _handle_automazione_click(self, tab_index):
        """Gestisce il click sui figli di Automazione (indice pagina 1 fissa)."""
        self.navigation_requested.emit(1)  # Vai a Pagina Automazioni
        self.automation_tab_requested.emit(tab_index)  # Cambia tab interno

    def _handle_notifications_click(self, tab_index):
        """Gestisce il click sui figli di Notifiche (indice pagina 9 fissa)."""
        self.navigation_requested.emit(9)  # Vai a Pagina Notifiche
        self.notifications_tab_requested.emit(
            tab_index
        )  # Cambia tab interno (0: Notifiche, 1: Audit)

    def set_active_button(self, index: int):
        """Aggiorna lo stato checked dei pulsanti."""

        # Mappa diretta per pulsanti semplici
        buttons_map = {
            0: self.btn_home,
            2: self.btn_lyra,
            7: self.btn_settings,
            8: self.btn_help,
        }

        # Reset pulsanti semplici
        for idx, btn in buttons_map.items():
            btn.setChecked(idx == index)

        # Gestione Gruppo Database (Indici 3, 4, 5, 6, 10, 11)
        db_indices = [3, 4, 5, 6, 10, 11]
        self.group_db.set_active_index(index, db_indices)

        # Gestione Gruppo Notifiche (Indice 9)
        if index == 9:
            self.group_notifiche.set_active_index(9, [999])  # Illumina header
            self.group_notifiche.header_btn.setChecked(True)
        else:
            self.group_notifiche.header_btn.setChecked(False)
            self.btn_audit.setChecked(False)

        # Gestione Gruppo Automazioni (Indice 1)
        # Qui è più complesso perché dipende dal tab interno, non solo dalla pagina.
        # Per ora illuminiamo l'header se siamo a pagina 1.
        if index == 1:
            self.group_automazioni.set_active_index(
                1, [999, 999]
            )  # Hack: illumina header
            self.group_automazioni.header_btn.setChecked(True)
        else:
            self.group_automazioni.header_btn.setChecked(False)
            self.btn_fornitori.setChecked(False)
            self.btn_safework.setChecked(False)
