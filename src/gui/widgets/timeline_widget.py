"""
SyncroJob - Timeline Widgets
Widget per la visualizzazione cronologica dei log e dei report di missione.
"""

import re
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    QUrl,
)
from PyQt6.QtGui import (
    QColor,
    QDesktopServices,
    QPainter,
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

from src.utils.log_humanizer import SmartLogTranslator


class HorizontalLogItem(QWidget):
    """Widget per singolo elemento della timeline log orizzontale."""

    def __init__(self, human_msg, tech_msg, category, timestamp, parent=None):
        """
        Inizializza un elemento log con icona, messaggio umano e timestamp.
        Supporta screenshot integrati e pulsanti di correzione rapida (FixIt).
        """
        super().__init__(parent)
        self.setFixedSize(180, 150)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.setStyleSheet(
            """
            QWidget {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
        """
        )

        snapshot_path = None
        fixit_action = None

        if "[IMG:" in tech_msg:
            match = re.search(r"\[IMG:(.*?)\]", tech_msg)
            if match:
                snapshot_path = match.group(1)
                tech_msg = tech_msg.replace(match.group(0), "").strip()

        if "[FIXIT:" in tech_msg:
            match = re.search(r"\[FIXIT:(.*?)\]", tech_msg)
            if match:
                fixit_action = match.group(1)
                tech_msg = tech_msg.replace(match.group(0), "").strip()

        icons = {
            "start": "🚀",
            "login": "🔐",
            "search": "🔍",
            "download": "📥",
            "success": "✅",
            "error": "❌",
            "wait": "⏳",
            "info": "ℹ️",
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

        top_row = QHBoxLayout()
        top_row.setSpacing(5)

        lbl_icon = QLabel(icons.get(category, "•"))
        lbl_icon.setStyleSheet(f"font-size: 24px; color: {self.category_color};")
        top_row.addWidget(lbl_icon)

        lbl_time = QLabel(timestamp)
        lbl_time.setStyleSheet("color: #adb5bd; font-size: 12px; font-family: monospace;")
        top_row.addWidget(lbl_time)

        top_row.addStretch()
        layout.addLayout(top_row)

        self.lbl_human = QLabel(human_msg)
        self.lbl_human.setStyleSheet("font-weight: bold; font-size: 13px; color: #212529;")
        self.lbl_human.setWordWrap(True)
        self.lbl_human.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.lbl_human)

        layout.addStretch()

        action_layout = QHBoxLayout()
        action_layout.setSpacing(5)

        if snapshot_path:
            btn = QPushButton("📷")
            btn.setFixedSize(30, 24)
            btn.setToolTip("Apri Screenshot")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("background-color: #dc3545; color: white; border-radius: 4px; font-size: 12px;")
            btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(snapshot_path)))
            action_layout.addWidget(btn)

        if fixit_action == "ACCOUNT":
            btn = QPushButton("🔧")
            btn.setFixedSize(30, 24)
            btn.setToolTip("Configura Account")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("background-color: #ffc107; color: black; border-radius: 4px; font-size: 12px;")
            btn.clicked.connect(self._open_settings)
            action_layout.addWidget(btn)

        path_matches = re.findall(
            r'([a-zA-Z]:\[^ :<>|"\n]+|/(?:Users|home|tmp|var|usr|opt|app|data)/[^ :<>|"\n]+)',
            tech_msg,
        )
        seen = set()
        for path in path_matches:
            path = path.rstrip(".,';)]}").strip()
            if len(path) > 4 and "http" not in path and path not in seen:
                seen.add(path)
                btn = QPushButton("📂")
                btn.setFixedSize(30, 24)
                btn.setToolTip(f"Apri: {Path(path).name}")
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet(
                    "background-color: #17a2b8; color: white; border-radius: 4px; font-size: 12px;"
                )
                btn.clicked.connect(lambda c, p=path: QDesktopServices.openUrl(QUrl.fromLocalFile(p)))
                action_layout.addWidget(btn)

        action_layout.addStretch()
        if action_layout.count() > 1:
            layout.addLayout(action_layout)

    def set_count(self, count):
        """Aggiorna il contatore dei log consecutivi identici."""
        current_text = self.lbl_human.text()
        base = current_text.split(" (x")[0]
        self.lbl_human.setText(f"{base} (x{count})")

    def _open_settings(self):
        """Apre il pannello impostazioni per correggere problemi di configurazione."""
        parent = self.window()
        if hasattr(parent, "show_settings"):
            parent.show_settings()


class HorizontalTimelineContainer(QWidget):
    """Container interno che disegna la linea di connessione."""

    def __init__(self, parent=None):
        """Inizializza il layout orizzontale del container."""
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 5, 10, 5)
        self.main_layout.setSpacing(10)
        self.main_layout.addStretch()
        self.setMinimumHeight(160)

    def paintEvent(self, event):
        """Disegna una linea di connessione grigia tra gli elementi del log."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        line_y = 30
        pen = QPen(QColor("#dee2e6"))
        pen.setWidth(2)
        painter.setPen(pen)

        # Trova il primo e l'ultimo widget reali (escludendo lo stretch)
        widgets = []
        for i in range(self.main_layout.count()):
            w = self.main_layout.itemAt(i).widget()
            if w and not w.isHidden():
                widgets.append(w)

        if len(widgets) >= 2:
            first = widgets[0]
            last = widgets[-1]
            start_x = first.geometry().center().x()
            end_x = last.geometry().center().x()
            painter.drawLine(start_x, line_y, end_x, line_y)


class HorizontalTimelineWidget(QScrollArea):
    """Widget Timeline Orizzontale con animazioni."""

    def __init__(self, parent=None):
        """Inizializza l'area di scorrimento orizzontale."""
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFixedHeight(220)
        self.setStyleSheet("border: none; background-color: transparent;")

        self.container = HorizontalTimelineContainer()
        self.setWidget(self.container)
        self.last_category = None
        self.consecutive_count = 0

    def wheelEvent(self, event):
        """Abilita lo scorrimento orizzontale tramite rotellina verticale del mouse."""
        delta = event.angleDelta().y()
        if delta != 0:
            scrollbar = self.horizontalScrollBar()
            scrollbar.setValue(scrollbar.value() - delta)
        else:
            super().wheelEvent(event)

    def add_widget(self, widget: QWidget):
        """Aggiunge un widget alla timeline con un effetto di dissolvenza (fade-in)."""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)

        # Inserisce prima dello stretch finale
        idx = self.container.main_layout.count() - 1
        self.container.main_layout.insertWidget(max(0, idx), widget)

        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.start()

        QApplication.processEvents()
        self._smooth_scroll_to_end()
        self.container.update()

    def add_log(self, message: str):
        """Analizza un messaggio di log tecnico e lo aggiunge alla timeline."""
        human, tech, cat = SmartLogTranslator.humanize(message)
        timestamp = datetime.now().strftime("%H:%M")

        if cat == self.last_category and cat in ["download", "search"]:
            self.consecutive_count += 1
            # Cerca l'ultimo widget reale
            widgets = []
            for i in range(self.container.main_layout.count()):
                w = self.container.main_layout.itemAt(i).widget()
                if isinstance(w, HorizontalLogItem):
                    widgets.append(w)

            if widgets:
                widgets[-1].set_count(self.consecutive_count)
                return
        else:
            self.consecutive_count = 1
            self.last_category = cat

        item = HorizontalLogItem(human, tech, cat, timestamp)
        self.add_widget(item)

    def _smooth_scroll_to_end(self):
        """Scorre fluidamente verso l'ultimo elemento aggiunto."""
        sb = self.horizontalScrollBar()
        start_val = sb.value()
        end_val = sb.maximum()

        self.scroll_anim = QPropertyAnimation(sb, b"value")
        self.scroll_anim.setDuration(400)
        self.scroll_anim.setStartValue(start_val)
        self.scroll_anim.setEndValue(end_val)
        self.scroll_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.scroll_anim.start()

    def set_mood(self, mood: str):
        """Cambia lo stile visuale della timeline in base al mood (es. 'running', 'success', 'error')."""
        self.last_mood = mood
        # Implementazione futura per cambiare colori di sfondo o animazioni
        pass

    def clear(self):
        """Rimuove tutti gli elementi dalla timeline."""
        while self.container.main_layout.count():
            item = self.container.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Re-aggiunge lo stretch dopo la pulizia
        self.container.main_layout.addStretch()
        self.container.update()


class LogWidget(QWidget):
    """Widget per visualizzare i log (Horizontal Wrapper)."""

    def __init__(self, parent=None):
        """Inizializza il widget log."""
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Configura l'interfaccia con header e timeline."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        header_layout = QHBoxLayout()
        label = QLabel("📋 Timeline Attività")
        label.setStyleSheet("font-weight: bold; font-size: 13px;")
        header_layout.addWidget(label)
        header_layout.addStretch()

        clear_btn = QPushButton("🧹 Pulisci Log")
        clear_btn.setMaximumWidth(120)
        clear_btn.setStyleSheet(
            "QPushButton { background-color: #6c757d; color: white; border: none; border-radius: 4px; padding: 2px 8px; font-size: 11px; } QPushButton:hover { background-color: #5a6268; }"
        )
        clear_btn.clicked.connect(self.clear)
        header_layout.addWidget(clear_btn)
        layout.addLayout(header_layout)

        self.timeline = HorizontalTimelineWidget()
        layout.addWidget(self.timeline)

    def append(self, message: str):
        """Aggiunge un nuovo messaggio alla timeline."""
        self.timeline.add_log(message)

    def append_log(self, message: str):
        """Alias per append (compatibilità test)."""
        self.append(message)

    def clear(self):
        """Svuota la timeline."""
        self.timeline.clear()


class MissionReportCard(QFrame):
    """Card riepilogativa stile 'Mission Complete'."""

    def __init__(self, duration_str, status, parent=None):
        """
        Inizializza la card di report con durata ed esito.

        Args:
            duration_str: Stringa formattata del tempo impiegato.
            status: Boolean indicante il successo della missione.
        """
        super().__init__(parent)
        self.setFixedSize(260, 150)
        self.setStyleSheet(
            "QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8f9fa, stop:1 #e9ecef); border: 1px solid #dee2e6; border-radius: 8px; margin: 10px 5px; }"
        )

        layout = QVBoxLayout(self)
        title_text = "🎉 Missione Compiuta!" if status else "⚠️ Missione Terminata"
        title_color = "#198754" if status else "#dc3545"
        lbl_title = QLabel(title_text)
        lbl_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {title_color};")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        stats_layout = QHBoxLayout()
        self._add_stat(stats_layout, "⏱️ Tempo", duration_str)
        self._add_stat(stats_layout, "📊 Esito", "Successo" if status else "Errore")
        layout.addLayout(stats_layout)

    def _add_stat(self, layout, label, value):
        """Aggiunge una statistica individuale alla card."""
        container = QWidget()
        v_layout = QVBoxLayout(container)
        v_layout.setContentsMargins(0, 0, 0, 0)
        lbl_l = QLabel(label)
        lbl_l.setStyleSheet("font-size: 12px; color: #6c757d;")
        lbl_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_v = QLabel(value)
        lbl_v.setStyleSheet("font-size: 16px; font-weight: bold; color: #212529;")
        lbl_v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_layout.addWidget(lbl_l)
        v_layout.addWidget(lbl_v)
        layout.addWidget(container)
