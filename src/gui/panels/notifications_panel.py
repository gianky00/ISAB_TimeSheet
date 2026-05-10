"""
SyncroJob - Notifications Panel
Pannello per la visualizzazione delle notifiche di sistema, Audit Log e Health Score.
Gestisce il filtraggio, la ricerca e il raggruppamento temporale dei messaggi.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import shiboken6
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.notification_manager import NotificationManager
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.panels.health_panel import HealthPanel
from src.gui.styles import COLORS
from src.gui.widgets.audit_log_widget import AuditLogWidget
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.notification_card import NotificationCard
from src.gui.widgets.notification_group_header import NotificationGroupHeader
from src.gui.widgets.notification_toolbar import NotificationToolbar
from src.utils.helpers import get_asset_path, get_colored_icon


@dataclass
class FilterState:
    """
    Gestione dello stato dei filtri per le notifiche.
    Mantiene le preferenze dell'utente su livelli, categorie e visibilità.
    """

    levels: list[str] = field(default_factory=lambda: ["all"])
    categories: list[str] = field(default_factory=list)
    priorities: list[str] = field(default_factory=list)
    date_range: tuple[datetime, datetime] | None = None
    show_read: bool = True
    show_unread: bool = True
    show_archived: bool = False
    search_query: str = ""
    sort_by: str = "date_desc"
    group_by: str = "time"


class NotificationsPanel(QWidget):
    """
    Pannello principale delle notifiche con architettura a schede (Tab).
    Include:
    - Notifiche: Feed interattivo dei messaggi di sistema.
    - Audit: Log dettagliato delle azioni utente e bot.
    - Health: Indicatori di salute e performance del sistema.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello notifiche e collega il manager globale.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.current_filter = "all"
        self.current_search = ""
        self.current_sort = "date_desc"
        self.manager = NotificationManager.instance()
        self._group_widgets: dict[str, dict[str, Any]] = {}
        self._cached_filter_result: list[dict[str, Any]] | None = None
        self._last_filter_state: tuple[str, str, str, int] | None = None
        self._refresh_timer = QTimer()
        self._refresh_timer.setSingleShot(True)
        self._refresh_timer.timeout.connect(self._do_refresh)

        # UI Elements
        self.tabs: AnimatedTabWidget
        self.notif_tab: QWidget
        self.toolbar: NotificationToolbar
        self.scroll_area: QScrollArea
        self.scroll_content: QWidget
        self.scroll_layout: QVBoxLayout
        self.audit_tab: AuditLogWidget
        self.health_tab: HealthPanel

        self._first_refresh_done = False
        self._setup_ui()
        self.manager.notifications_updated.connect(self._schedule_refresh)
        # Il refresh iniziale viene differito a showEvent per non bloccare lo startup

    def showEvent(self, event: Any) -> None:
        """Esegue il primo refresh solo quando il pannello diventa visibile."""
        super().showEvent(event)
        if not self._first_refresh_done:
            self._first_refresh_done = True
            QTimer.singleShot(50, self.refresh_notifications)

    def _setup_ui(self) -> None:
        """Configura il layout principale e inizializza i tab."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        self.tabs = AnimatedTabWidget()
        main_layout.addWidget(self.tabs)

        # Tab Notifiche
        self.notif_tab = QWidget()
        nl = QVBoxLayout(self.notif_tab)
        nl.setContentsMargins(0, 10, 0, 0)
        nl.setSpacing(10)

        self.toolbar = NotificationToolbar()
        self.toolbar.search_query_changed.connect(self._on_search_changed)
        self.toolbar.filter_changed.connect(self._on_filter_changed)
        self.toolbar.sort_changed.connect(self._on_sort_changed)
        nl.addWidget(self.toolbar)

        # Barra Azioni integrata meglio
        actions_card = QFrame()
        actions_card.setStyleSheet("background: transparent; border: none;")
        actions_layout = QHBoxLayout(actions_card)
        actions_layout.setContentsMargins(10, 0, 10, 0)

        actions_layout.addStretch()

        mark_read = ModernButton(
            "SEGNA TUTTI COME LETTI",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.CHECK_CIRCLE),
        )
        mark_read.clicked.connect(self.manager.mark_all_as_read)
        actions_layout.addWidget(mark_read)

        clear = ModernButton(
            "SVUOTA TUTTO",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),
        )
        clear.clicked.connect(self._clear_notifications)
        actions_layout.addWidget(clear)
        nl.addWidget(actions_card)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(12)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)
        nl.addWidget(self.scroll_area)

        self.tabs.addTab(
            self.notif_tab, get_colored_icon(get_asset_path(Icons.BELL), COLORS["text_muted"]), "Notifiche"
        )

        # Tab Audit
        self.audit_tab = AuditLogWidget()
        self.tabs.addTab(
            self.audit_tab, get_colored_icon(get_asset_path(Icons.SHIELD), COLORS["text_muted"]), "Audit"
        )

        # Tab Health
        self.health_tab = HealthPanel()
        self.tabs.addTab(
            self.health_tab, get_colored_icon(get_asset_path(Icons.HEART), COLORS["text_muted"]), "Health"
        )

        self.tabs.currentChanged.connect(self._on_tab_changed)

    def _on_tab_changed(self, index: int) -> None:
        """Aggiorna i dati del tab selezionato."""
        tab_text = self.tabs.tabText(index)
        if tab_text == "Audit":
            self.audit_tab.refresh()
        elif tab_text == "Health":
            self.health_tab.refresh()

    @Slot(str)
    def _on_search_changed(self, query: str) -> None:
        """Reagisce alla modifica del testo nella barra di ricerca."""
        self.current_search = query.lower()
        self._invalidate_cache()
        self._schedule_refresh()

    @Slot(str)
    def _on_filter_changed(self, filter_key: str) -> None:
        """Applica il filtro selezionato (es. Errori, Non letti)."""
        self.current_filter = filter_key
        self._invalidate_cache()
        self._schedule_refresh()

    @Slot(str)
    def _on_sort_changed(self, sort_key: str) -> None:
        """Cambia l'ordinamento della lista (Data, Priorita')."""
        self.current_sort = sort_key
        self._invalidate_cache()
        self._schedule_refresh()

    @Slot()
    def _schedule_refresh(self) -> None:
        """Pianifica un aggiornamento della UI con debounce."""
        if shiboken6.isValid(self):
            self._refresh_timer.stop()
            self._refresh_timer.start(50)

    def _invalidate_cache(self) -> None:
        """Invalida i risultati filtrati salvati in cache."""
        self._cached_filter_result = None
        self._last_filter_state = None

    @Slot()
    def _do_refresh(self) -> None:
        """Esegue l'aggiornamento effettivo della UI."""
        if shiboken6.isValid(self):
            self.refresh_notifications()

    def _clear_notifications(self) -> None:
        """Svuota tutte le notifiche previa conferma dell'utente."""
        if (
            QMessageBox.question(self, "Conferma", "Vuoi svuotare i messaggi?")
            == QMessageBox.StandardButton.Yes
        ):
            self.manager.clear_all()

    def refresh_notifications(self) -> None:
        """
        Ricarica la lista delle notifiche applicando filtri, ricerca e raggruppamento.
        Ottimizza il rendering utilizzando la cache del filtraggio.
        """
        if not shiboken6.isValid(self):
            return

        cache_key = (
            self.current_filter,
            self.current_search,
            self.current_sort,
            len(self.manager.notifications),
        )

        if self._last_filter_state == cache_key and self._cached_filter_result is not None:
            notifs = self._cached_filter_result
        else:
            notifs = self._get_filtered_sorted_notifications()
            self._cached_filter_result = notifs
            self._last_filter_state = cache_key

        self._update_toolbar_counts()
        self._clear_scroll_area()

        if not notifs:
            self._show_empty_state()
            return

        disable_animations = len(notifs) > 30
        grouped = self._group_notifications_by_time(notifs)
        self._render_groups(grouped, disable_animations)

    def _get_filtered_sorted_notifications(self) -> list[dict[str, Any]]:
        """Esegue il filtraggio e l'ordinamento logico dei dati."""
        if self.current_filter == "unread":
            notifs = self.manager.get_notifications(filter_unread=True)
        else:
            notifs = self.manager.get_notifications(filter_unread=False)

        if self.current_filter == "error":
            notifs = [n for n in notifs if n.get("level") == "error"]
        elif self.current_filter == "warning":
            notifs = [n for n in notifs if n.get("level") == "warning"]
        elif self.current_filter == "info":
            notifs = [n for n in notifs if n.get("level") == "info"]

        if self.current_search:
            notifs = [
                n
                for n in notifs
                if self.current_search in n.get("title", "").lower()
                or self.current_search in n.get("message", "").lower()
            ]

        return self._sort_notifications(notifs)

    def _render_groups(self, grouped: dict[str, dict[str, Any]], disable_animations: bool) -> None:
        """Crea i widget per i gruppiùtemporali e inserisce le card notifiche."""
        for group_key, group_data in grouped.items():
            if not group_data["notifications"]:
                continue

            header = NotificationGroupHeader(
                title=group_data["title"],
                group_key=group_key,
                count=len(group_data["notifications"]),
                icon=group_data["icon"],
            )
            header.toggled.connect(self._on_group_toggled)
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, header)

            group_container = QWidget()
            group_layout = QVBoxLayout(group_container)
            group_layout.setContentsMargins(0, 0, 0, 0)
            group_layout.setSpacing(8)

            for notif in group_data["notifications"]:
                card = NotificationCard(notif, disable_animations=disable_animations)
                card.card_deleted.connect(self._invalidate_and_refresh)
                group_layout.addWidget(card)

            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, group_container)
            self._group_widgets[group_key] = {"header": header, "container": group_container}

    def _clear_scroll_area(self) -> None:
        """Rimuove tutti i widget correnti dall'area scrollabile."""
        self._group_widgets.clear()
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item and (widget := item.widget()):
                widget.setParent(None)
                widget.deleteLater()

    @Slot()
    def _invalidate_and_refresh(self) -> None:
        """Invalida cache e pianifica refresh (callback per eliminazione singola card)."""
        self._invalidate_cache()
        self._schedule_refresh()

    def _sort_notifications(self, notifs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Ordina la lista in base alla strategiàselezionata."""
        if self.current_sort == "date_desc":
            return sorted(notifs, key=lambda n: n.get("timestamp", ""), reverse=True)
        if self.current_sort == "date_asc":
            return sorted(notifs, key=lambda n: n.get("timestamp", ""))
        if self.current_sort == "priority":
            priority_map = {"high": 3, "medium": 2, "low": 1}
            return sorted(notifs, key=lambda n: priority_map.get(n.get("priority", "low"), 1), reverse=True)
        if self.current_sort == "level":
            level_map = {"error": 4, "warning": 3, "success": 2, "info": 1}
            return sorted(notifs, key=lambda n: level_map.get(n.get("level", "info"), 1), reverse=True)
        return notifs

    def _group_notifications_by_time(self, notifs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        """Suddivide le notifiche in secchielli temporali (Oggi, Ieri, ecc.)."""
        now = datetime.now(UTC)
        groups: dict[str, dict[str, Any]] = {
            "pinned": {"title": "Fissate", "icon": "📌", "notifications": []},
            "today": {"title": "Oggi", "icon": "📅", "notifications": []},
            "yesterday": {"title": "Ieri", "icon": "📆", "notifications": []},
            "week": {"title": "Ultimi 7 giorni", "icon": "[FILE]", "notifications": []},
            "older": {"title": "Più vecchie", "icon": "🗂️", "notifications": []},
        }

        for notif in notifs:
            if notif.get("pinned", False):
                groups["pinned"]["notifications"].append(notif)
                continue
            try:
                ts = datetime.fromisoformat(notif.get("timestamp", ""))
                diff = now - ts
                if diff.days == 0:
                    groups["today"]["notifications"].append(notif)
                elif diff.days == 1:
                    groups["yesterday"]["notifications"].append(notif)
                elif diff.days <= 7:
                    groups["week"]["notifications"].append(notif)
                else:
                    groups["older"]["notifications"].append(notif)
            except Exception:
                groups["older"]["notifications"].append(notif)
        return groups

    @Slot(str, bool)
    def _on_group_toggled(self, group_key: str, is_expanded: bool) -> None:
        """Mostra o nasconde il container di un gruppo."""
        if group_key in self._group_widgets:
            self._group_widgets[group_key]["container"].setVisible(is_expanded)

    def _update_toolbar_counts(self) -> None:
        """Aggiorna i contatori numerici sulle chip dei filtri."""
        all_notifs = self.manager.notifications
        counts = {"all": len(all_notifs), "unread": 0, "error": 0, "warning": 0, "info": 0}
        for n in all_notifs:
            if not n.get("read", False):
                counts["unread"] += 1
            level = n.get("level", "info")
            if level in counts:
                counts[level] += 1
        self.toolbar.update_filter_counts(counts)

    def _show_empty_state(self) -> None:
        """Visualizza un widget informativo quando non ci sono notifiche per il filtro corrente."""
        empty_widget = QWidget()
        empty_layout = QVBoxLayout(empty_widget)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.setSpacing(16)

        if self.current_filter == "all":
            icon_text, title, subtitle = "📭", "Nessuna notifica", "Le tue notifiche appariranno qui"
        elif self.current_filter == "unread":
            icon_text, title, subtitle = "✅", "Tutto a posto!", "Nessuna notifica da leggere"
        elif self.current_filter == "error":
            icon_text, title, subtitle = "🎉", "Sistema funzionante!", "Nessun errore registrato"
        else:
            icon_text, title, subtitle = (
                "📭",
                "Nessuna notifica",
                f"Nessuna notifica di tipo {self.current_filter}",
            )

        icon_lbl = QLabel(icon_text)
        icon_lbl.setStyleSheet("font-size: 64px; border: none;")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(
            f"font-size: 20px; font-weight: bold; color: {COLORS['text_dark']}; border: none;"
        )
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(title_lbl)

        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setStyleSheet(f"font-size: 14px; color: {COLORS['text_muted']}; border: none;")
        subtitle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(subtitle_lbl)

        empty_widget.setStyleSheet("background: transparent;")
        self.scroll_layout.insertWidget(0, empty_widget)
