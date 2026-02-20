"""
SyncroJob - Timeline Widgets
Widget per la visualizzazione cronologica orizzontale dei log e dei report di missione.
Fornisce una vista a 'nodi' per monitorare l'avanzamento delle attività del bot.
"""

import re
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import (
    QPropertyAnimation,
    QUrl,
)
from PyQt6.QtGui import (
    QColor,
    QDesktopServices,
    QPainter,
    QPaintEvent,
    QPen,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon
from src.utils.log_humanizer import SmartLogTranslator


class HorizontalLogItem(QWidget):
    """
    Rappresenta un singolo elemento di log all'interno della timeline orizzontale.
    Include l'icona della categoria, il timestamp e il messaggio tradotto.
    """

    def __init__(
        self, human_msg: str, tech_msg: str, category: str, timestamp: str, parent: QWidget | None = None
    ) -> None:
        """
        Inizializza un elemento di log orizzontale.

        Args:
            human_msg: Messaggio leggibile per l'utente.
            tech_msg: Messaggio tecnico dettagliato.
            category: Categoria del log (es. login, download, error).
            timestamp: Orario del log.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.setFixedSize(180, 150)
        self.setStyleSheet(
            "QWidget { background-color: white; border: 1px solid #dee2e6; border-radius: 8px; } QLabel { background-color: transparent; border: none; }"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Header con Icona e Tempo
        header = self._setup_header(category, timestamp)
        layout.addLayout(header)

        # Messaggio Human
        self.lbl_human = QLabel(human_msg)
        self.lbl_human.setWordWrap(True)
        self.lbl_human.setStyleSheet("font-weight: bold; color: #212529; font-size: 13px;")
        layout.addWidget(self.lbl_human)

        # Azioni rapide (Screenshot, ecc.)
        self._setup_actions(layout, tech_msg, None, None)

        layout.addStretch()

    def _setup_header(self, category: str, timestamp: str) -> QHBoxLayout:
        """Configura l'header dell'item con icona e orario."""
        icons = {
            "start": Icons.ACTIVITY,
            "login": Icons.USER,
            "search": Icons.SEARCH,
            "download": Icons.DOWNLOAD,
            "success": Icons.CHECK_CIRCLE,
            "error": Icons.ALERT,
            "wait": Icons.CLOCK,
            "info": Icons.HELP,
        }
        colors = {
            "start": "#0d6efd",
            "login": "#6f42c1",
            "search": "#fd7e14",
            "download": "#0dcaf0",
            "success": "#198754",
            "error": "#dc3545",
            "wait": "#ffc107",
            "info": "#6c757d",
        }
        self.category_color = colors.get(category, "#6c757d")

        row = QHBoxLayout()
        row.setSpacing(5)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(
            get_colored_icon(get_asset_path(icons.get(category, Icons.HELP)), "#000000").pixmap(24, 24)
        )
        row.addWidget(icon_lbl)
        time_lbl = QLabel(timestamp)
        time_lbl.setStyleSheet("color: #adb5bd; font-size: 12px; font-family: monospace;")
        row.addWidget(time_lbl)
        row.addStretch()
        return row

    def _setup_actions(
        self, layout: QVBoxLayout, tech_msg: str, snap_path: str | None, fixit_act: str | None
    ) -> None:
        """Aggiunge pulsanti di azione in base al contenuto del log."""
        action_row = QHBoxLayout()
        action_row.setSpacing(5)
        if snap_path:
            btn = self._create_btn(Icons.EYE, "#dc3545", "Apri Screenshot")
            btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(snap_path)))
            action_row.addWidget(btn)
        if fixit_act == "ACCOUNT":
            btn = self._create_btn(Icons.SETTINGS, "#ffc107", "Configura Account", "black")
            btn.clicked.connect(self._open_settings)
            action_row.addWidget(btn)
        self._add_path_btns(action_row, tech_msg)
        action_row.addStretch()
        if action_row.count() > 1:
            layout.addLayout(action_row)

    def _create_btn(self, icon: str, bg: str, tip: str, fg: str = "white") -> QPushButton:
        """Helper per la creazione di mini-pulsanti di azione."""
        btn = QPushButton()
        btn.setIcon(get_colored_icon(get_asset_path(icon), "#000000"))
        btn.setFixedSize(30, 24)
        btn.setToolTip(tip)
        btn.setStyleSheet(f"background-color: {bg}; color: {fg}; border-radius: 4px;")
        return btn

    def _add_path_btns(self, layout: QHBoxLayout, msg: str) -> None:
        """Analizza il messaggio tecnico per trovare percorsi file e aggiungere pulsanti 'Apri'."""
        matches = re.findall(
            r'([a-zA-Z]:\[^ :<>|"\n]+|/(?:Users|home|tmp|var|usr|opt|app|data)/[^ :<>|"\n]+)',
            msg,
        )
        for p in set(matches):
            p = p.rstrip(".,';)]}").strip()
            if len(p) > 4 and "http" not in p:
                btn = self._create_btn(Icons.FOLDER_OPEN, "#17a2b8", f"Apri: {Path(p).name}")
                btn.clicked.connect(lambda c, path=p: QDesktopServices.openUrl(QUrl.fromLocalFile(path)))
                layout.addWidget(btn)

    def set_count(self, count: int) -> None:
        """Aggiorna il contatore di ripetizioni per log identici (es. download x5)."""
        base = self.lbl_human.text().split(" (x")[0]
        self.lbl_human.setText(f"{base} (x{count})")

    def _open_settings(self) -> None:
        """Naviga alla pagina impostazioni della MainWindow."""
        win = self.window()
        if win and hasattr(win, "show_settings"):
            win.show_settings()


class HorizontalTimelineContainer(QWidget):
    """
    Contenitore interno per la timeline che gestisce il disegno della linea di collegamento.
    """
    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza il contenitore con layout orizzontale."""
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 5, 10, 5)
        self.main_layout.setSpacing(10)
        self.main_layout.addStretch()
        self.setMinimumHeight(160)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna la linea grigia di fondo che unisce i nodi."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor("#dee2e6"))
        pen.setWidth(2)
        painter.setPen(pen)
        widgets = []
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item and (w := item.widget()) and not w.isHidden():
                widgets.append(w)
        if len(widgets) >= 2:
            start_x = widgets[0].geometry().center().x()
            end_x = widgets[-1].geometry().center().x()
            painter.drawLine(start_x, 30, end_x, 30)


class HorizontalTimelineWidget(QScrollArea):
    """
    Widget scrollabile che ospita la timeline orizzontale dei log.
    Fornisce metodi per aggiungere log dinamici con animazioni di dissolvenza.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza la scroll area per la timeline."""
        super().__init__(parent)
        self.setFixedHeight(220)
        self.setStyleSheet("border: none; background-color: transparent;")
        self.container = HorizontalTimelineContainer()
        self.setWidget(self.container)
        self.last_category: str | None = None
        self.consecutive_count = 0

    def set_mood(self, _mood: str) -> None:
        """Metodo placeholder per il cambio mood visivo."""

    def add_widget(self, widget: QWidget) -> None:
        """Aggiunge un widget alla timeline con animazione di opacità."""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        idx = self.container.main_layout.count() - 1
        self.container.main_layout.insertWidget(max(0, idx), widget)
        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()
        QApplication.processEvents()
        self._scroll_to_end()

    def add_log(self, message: str) -> None:
        """
        Traduce un messaggio tecnico e lo aggiunge come nodo alla timeline.
        Raggruppa log consecutivi della stessa categoria (es. download).
        """
        human, tech, cat = SmartLogTranslator.humanize(message)
        if cat == self.last_category and cat in ("download", "search"):
            self.consecutive_count += 1
            items = []
            for i in range(self.container.main_layout.count()):
                item = self.container.main_layout.itemAt(i)
                if item and (w := item.widget()) and isinstance(w, HorizontalLogItem):
                    items.append(w)
            if items:
                last_item = items[-1]
                last_item.set_count(self.consecutive_count)
                return
        self.consecutive_count = 1
        self.last_category = cat
        self.add_widget(HorizontalLogItem(human, tech, cat, datetime.now().strftime("%H:%M")))

    def _scroll_to_end(self) -> None:
        """Esegue lo scroll fluido verso l'ultimo elemento aggiunto."""
        sb = self.horizontalScrollBar()
        if sb:
            self.scroll_anim = QPropertyAnimation(sb, b"value")
            self.scroll_anim.setDuration(400)
            self.scroll_anim.setStartValue(sb.value())
            self.scroll_anim.setEndValue(sb.maximum())
            self.scroll_anim.start()

    def clear(self) -> None:
        """Rimuove tutti gli elementi dalla timeline e resetta il layout."""
        while self.container.main_layout.count():
            item = self.container.main_layout.takeAt(0)
            if item and (w := item.widget()):
                w.deleteLater()
        self.container.main_layout.addStretch()


class TimelineWidget(QWidget):
    """
    Contenitore principale per la timeline dei log con header e pulsante di pulizia.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza l'interfaccia della timeline."""
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        header = QHBoxLayout()
        header.addWidget(QLabel("<b>Timeline Attività</b>"))
        header.addStretch()
        btn = ModernButton(
            "Pulisci Log",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),
        )
        btn.clicked.connect(self.clear)
        header.addWidget(btn)
        layout.addLayout(header)
        self.timeline = HorizontalTimelineWidget()
        layout.addWidget(self.timeline)

    def append(self, message: str) -> None:
        """Aggiunge un messaggio alla timeline interna."""
        self.timeline.add_log(message)

    def clear(self) -> None:
        """Svuota la timeline interna."""
        self.timeline.clear()


class MissionReportCard(QFrame):
    """
    Card di riepilogo visualizzata al termine di una sessione bot.
    """
    def __init__(self, duration_str: str, status: bool, parent: QWidget | None = None) -> None:
        """
        Inizializza la card di report missione.

        Args:
            duration_str: Testo della durata.
            status: Successo o errore.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.setFixedSize(260, 150)
        self.setStyleSheet(
            "QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8f9fa, stop:1 #e9ecef); border: 1px solid #dee2e6; border-radius: 8px; margin: 10px 5px; }"
        )
        layout = QVBoxLayout(self)
        title = "Missione Compiuta!" if status else "Missione Terminata"
        lbl_title = QLabel(f"<b>{title}</b>")
        lbl_title.setStyleSheet(f"color: {'#198754' if status else '#dc3545'}; font-size: 16px;")
        layout.addWidget(lbl_title)
        layout.addWidget(QLabel(f"Durata: {duration_str}"))
