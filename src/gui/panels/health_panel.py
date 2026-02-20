"""
SyncroJob - Health Panel
Dashboard avanzata per il monitoraggio della salute del sistema (Observability).
Visualizza punteggi di affidabilità (Health Score), statistiche di esecuzione dei bot nelle ultime 24 ore
e un elenco dettagliato di anomalie rilevate, con integrazione diretta per gli alert Telegram.
"""

from contextlib import suppress
from datetime import datetime
from typing import Any

from PyQt6.QtCore import QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.gui.widgets.modern_button import ModernButton


class HealthScoreBadge(QWidget):
    """
    Widget circolare (Gauge) che rappresenta visivamente l'Health Score.
    Cambia colore (verde, giallo, arancio, rosso) in base al punteggio percentuale.
    """

    def __init__(self, parent: QWidget | None = None, size: int = 160) -> None:
        """
        Inizializza il badge del punteggio salute.

        Args:
            parent: Widget genitore.
            size: Diametro del widget in pixel.
        """
        super().__init__(parent)
        self._score = 100
        self._size = size
        self.setFixedSize(size, size)

    @property
    def score(self) -> int:
        """Restituisce il punteggio attuale (0-100)."""
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        """Imposta il punteggio e richiede il ridisegno del widget."""
        self._score = max(0, min(100, value))
        self.update()

    def _get_color(self) -> QColor:
        """Determina il colore dell'arco in base alla soglia di punteggio."""
        if self._score >= 80:
            return QColor("#28a745")
        if self._score >= 60:
            return QColor("#ffc107")
        if self._score >= 40:
            return QColor("#fd7e14")
        return QColor("#dc3545")

    def _get_status_text(self) -> str:
        """Restituisce la label testuale associata al punteggio."""
        if self._score >= 80:
            return "OTTIMO"
        if self._score >= 60:
            return "DISCRETO"
        if self._score >= 40:
            return "ATTENZIONE"
        return "CRITICO"

    def paintEvent(self, event) -> None:
        """Esegue il rendering personalizzato dell'arco di progresso tramite QPainter."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        margin, arc_width = 15, 12
        rect = QRectF(margin, margin, self._size - 2 * margin, self._size - 2 * margin)

        painter.setPen(QPen(QColor("#e9ecef"), arc_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawEllipse(rect)

        painter.setPen(QPen(self._get_color(), arc_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawArc(rect, 90 * 16, -int(360 * 16 * self._score / 100))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(rect.adjusted(18, 18, -18, -18))

        painter.setPen(QColor("#343a40"))
        painter.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(self._score))


class StatCard(QFrame):
    """Card informativa minimalista per visualizzare singole metriche (es. Bot Run, Error Rate)."""

    def __init__(self, title: str, value: str = "0", icon: str = "", color: str = "#007bff", parent: QWidget | None = None) -> None:
        """
        Inizializza la card statistica.

        Args:
            title: Etichetta della metrica.
            value: Valore visualizzato.
            icon: Emoji o carattere icona.
            color: Colore primario della card (bordo e testo).
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._value_label: QLabel | None = None
        self._color = color
        self._setup_ui(title, value, icon, color)

    def _setup_ui(self, title: str, value: str, icon: str, color: str) -> None:
        """Configura lo stile CSS e il layout interno della card."""
        self.setStyleSheet(f"QFrame {{ background-color: #ffffff; border-radius: 12px; border: 1px solid #dee2e6; border-left: 4px solid {color}; }}")
        self.setMinimumSize(140, 95)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout = QVBoxLayout(self)

        header = QHBoxLayout()
        if icon:
            lbl_icon = QLabel(icon)
            lbl_icon.setStyleSheet("font-size: 18px; border: none;")
            header.addWidget(lbl_icon)
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #6c757d; font-size: 12px; font-weight: 500; border: none;")
        header.addWidget(lbl_title)
        header.addStretch()
        layout.addLayout(header)

        self._value_label = QLabel(value)
        self._value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold; border: none;")
        layout.addWidget(self._value_label)

    def set_value(self, value: str) -> None:
        """Aggiorna dinamicamente il testo del valore nella card."""
        if self._value_label:
            self._value_label.setText(value)


class AnomalyCard(QFrame):
    """Widget per la visualizzazione di un'anomalia specifica rilevata dal sistema di monitoraggio."""

    def __init__(self, anomaly, parent: QWidget | None = None) -> None:
        """
        Inizializza la card anomalia.

        Args:
            anomaly: Oggetto anomalia (deve avere message, severity e suggestion).
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._setup_ui(anomaly)

    def _setup_ui(self, anomaly) -> None:
        """Configura il layout e i colori in base alla gravità dell'anomalia."""
        color, bg = self._get_severity_color(anomaly.severity), self._get_bg_color(anomaly.severity)
        self.setStyleSheet(f"QFrame {{ background-color: {bg}; border-radius: 10px; border: 1px solid {color}40; border-left: 5px solid {color}; }}")
        layout = QVBoxLayout(self)

        header = QHBoxLayout()
        emoji = {"low": "ℹ️", "medium": "⚠️", "high": "🔴", "critical": "🚨"}.get(anomaly.severity, "📢")
        lbl_title = QLabel(f"{emoji}  {anomaly.message}")
        lbl_title.setStyleSheet("color: #343a40; font-weight: 600; font-size: 14px;")
        lbl_title.setWordWrap(True)
        header.addWidget(lbl_title, stretch=1)

        lbl_sev = QLabel(anomaly.severity.upper())
        lbl_sev.setStyleSheet(f"color: {color}; background-color: {color}20; padding: 4px 10px; border-radius: 6px; font-size: 10px; font-weight: bold;")
        header.addWidget(lbl_sev)
        layout.addLayout(header)

        if anomaly.suggestion:
            lbl_sug = QLabel(f"💡 {anomaly.suggestion}")
            lbl_sug.setStyleSheet("color: #495057; font-size: 12px; padding-left: 24px;")
            lbl_sug.setWordWrap(True)
            layout.addWidget(lbl_sug)

    def _get_severity_color(self, severity: str) -> str:
        """Mappa la gravità a un colore HEX enterprise."""
        return {"low": "#007bff", "medium": "#ffc107", "high": "#fd7e14", "critical": "#dc3545"}.get(severity, "#6c757d")

    def _get_bg_color(self, severity: str) -> str:
        """Mappa la gravità a un colore di sfondo leggero."""
        return {"low": "#e7f1ff", "medium": "#fff8e1", "high": "#fff3e0", "critical": "#ffebee"}.get(severity, "#f8f9fa")


class HealthPanel(QWidget):
    """
    Pannello principale Health & Observability.
    Integra timer di auto-refresh per mantenere i dati sempre aggiornati.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza l'interfaccia e avvia gli scheduler di monitoraggio."""
        super().__init__(parent)
        self._setup_ui()
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.refresh)
        self._refresh_timer.start(120000)
        self._alert_timer = QTimer(self)
        self._alert_timer.timeout.connect(self._auto_check_alerts)
        self._alert_timer.start(1800000)
        QTimer.singleShot(500, self.refresh)

    def _setup_ui(self) -> None:
        """Costruisce il layout a due colonne: statistiche a sinistra, anomalie a destra."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        header = QHBoxLayout()
        title = QLabel("📊 System Health")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #343a40; border: none;")
        header.addWidget(title)
        header.addStretch()

        self._alert_btn = ModernButton("📢 Invia Alert", variant=ModernButton.Variant.SECONDARY)
        self._alert_btn.clicked.connect(self._send_telegram_alert)
        header.addWidget(self._alert_btn)
        self._refresh_btn = ModernButton("🔄 Aggiorna")
        self._refresh_btn.clicked.connect(self.refresh)
        header.addWidget(self._refresh_btn)
        layout.addLayout(header)

        content = QHBoxLayout()
        content.setSpacing(24)
        left_panel = QVBoxLayout()
        left_panel.setSpacing(20)
        score_card = QFrame()
        score_card.setStyleSheet("QFrame { background-color: #ffffff; border-radius: 16px; border: 1px solid #dee2e6; }")
        score_layout = QVBoxLayout(score_card)
        self._score_badge = HealthScoreBadge(size=160)
        score_layout.addWidget(self._score_badge, alignment=Qt.AlignmentFlag.AlignCenter)
        self._status_label = QLabel("OTTIMO")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addWidget(self._status_label)
        self._last_update = QLabel("Ultimo aggiornamento: --")
        self._last_update.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addWidget(self._last_update)
        left_panel.addWidget(score_card)

        stats_grid = QGridLayout()
        stats_grid.setSpacing(12)
        self._stat_runs_ok = StatCard("Bot Successo", color="#28a745", icon="✅")
        self._stat_runs_fail = StatCard("Bot Falliti", color="#dc3545", icon="❌")
        self._stat_error_rate = StatCard("Error Rate", color="#ffc107", icon="📉")
        self._stat_anomalies = StatCard("Anomalie", color="#fd7e14", icon="⚠️")
        stats_grid.addWidget(self._stat_runs_ok, 0, 0)
        stats_grid.addWidget(self._stat_runs_fail, 0, 1)
        stats_grid.addWidget(self._stat_error_rate, 1, 0)
        stats_grid.addWidget(self._stat_anomalies, 1, 1)
        left_panel.addLayout(stats_grid)
        left_panel.addStretch()
        content.addLayout(left_panel, stretch=1)

        right_panel = QVBoxLayout()
        right_panel.setSpacing(16)
        anom_header = QHBoxLayout()
        anom_header.addWidget(QLabel("⚠️ Anomalie Rilevate"))
        self._anomaly_count_label = QLabel("0 problemi")
        anom_header.addStretch()
        anom_header.addWidget(self._anomaly_count_label)
        right_panel.addLayout(anom_header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self._anomalies_container = QWidget()
        self._anomalies_layout = QVBoxLayout(self._anomalies_container)
        self._anomalies_layout.addStretch()
        scroll.setWidget(self._anomalies_container)
        right_panel.addWidget(scroll)
        content.addLayout(right_panel, stretch=2)
        layout.addLayout(content)

    def refresh(self) -> None:
        """Interroga i motori di analytics e il LogViewer per aggiornare tutte le card e lo score."""
        try:
            from src.core.logging.analytics import generate_analytics_report
            from src.core.logging.viewer import LogViewer
            report = generate_analytics_report(hours=24)
            self._score_badge.score = report.health_score
            self._status_label.setText(self._score_badge._get_status_text())

            health = LogViewer().generate_health_report()
            self._stat_runs_ok.set_value(str(health.get("bot_runs", {}).get("successful", 0)))
            self._stat_runs_fail.set_value(str(health.get("bot_runs", {}).get("failed", 0)))
            self._stat_error_rate.set_value(f"{health.get('error_rate_percent', 0):.1f}%")
            self._stat_anomalies.set_value(str(len(report.anomalies)))
            self._last_update.setText(f"Ultimo aggiornamento: {datetime.now().strftime('%H:%M:%S')}")
            self._update_anomalies(report.anomalies)
        except Exception as e:
            self._last_update.setText(f"Errore: {str(e)[:30]}")

    def _update_anomalies(self, anomalies: list[Any]) -> None:
        """Rigenera dinamicamente la lista delle card anomalia nella colonna di destra."""
        while self._anomalies_layout.count() > 1:
            if (item := self._anomalies_layout.takeAt(0)) and (w := item.widget()):
                w.deleteLater()
        self._anomaly_count_label.setText(f"{len(anomalies)} problema{'i' if len(anomalies) != 1 else ''}")
        if not anomalies:
            empty = QFrame()
            empty.setStyleSheet("QFrame { background: #e8f5e9; border-radius: 12px; border: 1px dashed #81c784; }")
            el = QVBoxLayout(empty)
            el.addWidget(QLabel("✨"), alignment=Qt.AlignmentFlag.AlignCenter)
            el.addWidget(QLabel("Nessuna anomalia"), alignment=Qt.AlignmentFlag.AlignCenter)
            self._anomalies_layout.insertWidget(0, empty)
        else:
            for a in anomalies:
                self._anomalies_layout.insertWidget(self._anomalies_layout.count() - 1, AnomalyCard(a))

    def _send_telegram_alert(self) -> None:
        """Compone e invia un report di salute testuale al canale Telegram configurato."""
        try:
            from src.core.logging.alert_manager import get_alert_manager
            from src.core.logging.analytics import generate_analytics_report
            report = generate_analytics_report(hours=24)
            if not report.anomalies:
                self._show_toast("ℹ️ Nessuna anomalia da segnalare", "info")
                return

            am = get_alert_manager()
            summary = f"🏥 <b>Health Report</b>\nScore: {report.health_score}%\nAnomalie: {len(report.anomalies)}\n\n"
            for a in report.anomalies[:5]:
                summary += f"• {a.message}\n"
            am.send_alert("Health Report", summary, "info")
            self._show_toast("✅ Alert inviato su Telegram", "success")
        except Exception as e:
            self._show_toast(f"❌ Errore invio: {str(e)[:50]}", "error")

    def _auto_check_alerts(self) -> None:
        """Esegue un controllo periodico e invia notifiche automatiche se vengono rilevate anomalie critiche."""
        with suppress(Exception):
            from src.core.logging.alert_manager import get_alert_manager
            if (sent := get_alert_manager().check_and_alert(hours=24)) > 0:
                self._last_update.setText(f"🔔 {sent} alert inviati")

    def _show_toast(self, message: str, level: str = "info") -> None:
        """Inoltra una notifica interna al NotificationManager."""
        with suppress(Exception):
            from src.core.notification_manager import NotificationManager
            NotificationManager.instance().add_notification(title="Health Panel", message=message, level=level)
