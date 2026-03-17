"""
SyncroJob - Sidebar Components
Raccolta di widget per la gerarchia della Sidebar (Gruppi, Sottogruppi e Bot).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.sidebar_button import SidebarButton
from src.utils.helpers import get_asset_path


class SidebarChildButton(SidebarButton):
    """Pulsante figlio con stile Glass specifico e indentazione."""

    def set_collapsed(self, collapsed: bool, animated: bool = False) -> None:
        """Sovrascrive set_collapsed per mantenere l'indentazione specifica dei figli."""
        super().set_collapsed(collapsed, animated)
        if not collapsed:
            # Ripristiniamo l'indentazione specifica per il secondo livello
            # Questo sovrascrive il padding standard del SidebarButton
            current_style = self.styleSheet()
            new_style = current_style.replace("padding: 12px 15px;", "padding: 10px 10px 10px 35px;")
            self.setStyleSheet(new_style)


class SidebarSubGroup(QWidget):
    """Sottogruppo di secondo livello (es. Portale Fornitori sotto Automazioni)."""

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        """
        Inizializza il sottogruppo della sidebar.

        Args:
            title: Titolo del sottogruppo.
            parent: Widget genitore opzionale.
        """
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
        """Alterna la visibilità del contenuto del sottogruppo."""
        is_visible = self.content_area.isVisible()
        self.content_area.setVisible(not is_visible)

    def add_child(self, btn: SidebarButton) -> None:
        """
        Aggiunge un pulsante figlio al sottogruppo.

        Args:
            btn: Il pulsante da aggiungere.
        """
        # Indentazione aggiuntiva per il terzo livello (55px)
        if not btn._collapsed:
            current_style = btn.styleSheet()
            new_style = current_style.replace("padding: 12px 15px;", "padding: 8px 10px 8px 55px;")
            new_style = new_style.replace("font-size: 13px;", "font-size: 12px;")
            btn.setStyleSheet(new_style)
        self.content_layout.addWidget(btn)
        self.children_btns.append(btn)

    def set_collapsed(self, collapsed: bool) -> None:
        """
        Imposta lo stato di contrazione del sottogruppo.

        Args:
            collapsed: True per contrarre, False per espandere.
        """
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
        """
        Inizializza il gruppo principale della sidebar.

        Args:
            title: Titolo del gruppo.
            icon_path: Percorso dell'icona del gruppo.
            parent: Widget genitore opzionale.
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
        self.children_elements: list[QWidget] = []
        self._was_expanded = False

    def _set_arrow_icon(self, expanded: bool) -> None:
        """Imposta l'icona della freccia (espansa/contratta)."""
        from src.utils.helpers import get_colored_icon

        icon_enum = Icons.CHEVRON_DOWN if expanded else Icons.CHEVRON_RIGHT
        icon = get_colored_icon(get_asset_path(icon_enum), COLORS["bg_white"])
        self.arrow_label.setPixmap(icon.pixmap(12, 12))

    def toggle_group(self) -> None:
        """Alterna lo stato di apertura del gruppo principale."""
        is_opening = not self.content_area.isVisible()
        self.content_area.setVisible(is_opening)
        self._set_arrow_icon(is_opening)
        if is_opening:
            self._was_expanded = True
            self.expanded.emit(self)
        else:
            self._was_expanded = False

    def collapse(self) -> None:
        """Chiude forzatamente il gruppo."""
        self.content_area.setVisible(False)
        self._was_expanded = False
        self._set_arrow_icon(False)

    def add_child(self, widget: QWidget) -> None:
        """
        Aggiunge un elemento figlio (pulsante o sottogruppo).

        Args:
            widget: Il widget da aggiungere.
        """
        self.content_layout.addWidget(widget)
        self.children_elements.append(widget)

    def set_collapsed(self, collapsed: bool) -> None:
        """
        Imposta lo stato di contrazione del gruppo.

        Args:
            collapsed: True per contrarre, False per espandere.
        """
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
        """
        Imposta il pulsante attivo all'interno del gruppo.

        Args:
            index: Indice della pagina corrente.
            group_indices: Elenco degli indici appartenenti a questo gruppo.
        """
        is_child_active = index in group_indices
        self.header_btn.setChecked(is_child_active)
        if is_child_active:
            self.content_area.setVisible(True)
            if not self.header_btn._collapsed:
                self._was_expanded = True
        self._set_arrow_icon(self.content_area.isVisible() and not self.header_btn._collapsed)
