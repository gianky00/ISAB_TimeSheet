"""
SyncroJob - Health Panel
Dashboard avanzata per il monitoraggio della salute del sistema (Observability).
Visualizza punteggi di affidabilità (Health Score), statistiche di esecuzione dei bot nelle ultime 24 ore
e un elenco dettagliato di anomalie rilevate, con integrazione diretta per gli alert Telegram.
"""

from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from PyQt6.QtCore import QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPainter, QPaintEvent, QPen
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets import ModernButton, ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon


class HealthScoreBadge(QWidget):
    """
    Widget circolare (Gauge) Premium per l'Health Score.
    Implementa gradienti dinamici e ombre interne per un look Next-Gen.
    """

    def __init__(self, parent: QWidget | None = None, size: int = 180) -> None:
        super().__init__(parent)
        self._score = 100
        self._size = size
        self.setFixedSize(size, size)

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        self._score = max(0, min(100, value))
        self.update()

    def _get_gradient(self) -> QColor:
        if self._score >= 80:  # noqa: PLR2004
            return QColor(COLORS["success_green"])
        if self._score >= 60:  # noqa: PLR2004
            return QColor(COLORS["warning_yellow"])
        if self._score >= 40:  # noqa: PLR2004
            return QColor(COLORS["warning_orange"])
        return QColor(COLORS["error_red"])

    def _get_status_text(self) -> str:
        if self._score >= 80:  # noqa: PLR2004
            return "SISTEMA OTTIMO"
        if self._score >= 60:  # noqa: PLR2004
            return "SISTEMA STABILE"
        if self._score >= 40:  # noqa: PLR2004
            return "ATTENZIONE RICHIESTA"
        return "STATO CRITICO"

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Esegue il rendering del badge circolare."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = self.rect().center()
        radius = (self._size // 2) - 10
        arc_width = 14

        # 1. Background Circle (Track)
        bg_pen = QPen(QColor(COLORS["bg_hover"]), arc_width)
        bg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawEllipse(center, radius, radius)

        # 2. Progress Arc with Gradient
        color = self._get_gradient()
        grad_pen = QPen(color, arc_width)
        grad_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(grad_pen)

        rect = QRectF(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
        start_angle = 90 * 16
        span_angle = -int(360 * 16 * (self._score / 100))
        painter.drawArc(rect, start_angle, span_angle)

        # 3. Inner Shadow/Circle
        inner_radius = radius - 15
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 255, 255, 200))
        painter.drawEllipse(center, inner_radius, inner_radius)

        # 4. Score Text
        painter.setPen(QColor(COLORS["text_dark"]))
        font = QFont("Segoe UI", 38, QFont.Weight.Black)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, str(self._score))


class StatCard(ModernCard):
    """Card statistica Premium con elevazione e icone colorate."""

    def __init__(
        self,
        title: str,
        value: str = "0",
        icon_key: str = Icons.ACTIVITY,
        color: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent, elevation=10)
        self._color = color or COLORS["info_blue"]
        self.setMinimumSize(160, 100)
        self._setup_content(title, value, icon_key, self._color)

    def _setup_content(self, title: str, value: str, icon_key: str, color: str) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # Icon Container
        self.icon_box = QWidget()
        self.icon_box.setFixedSize(42, 42)
        self.icon_box.setStyleSheet(f"background: {color}15; border-radius: 10px;")
        ib_layout = QVBoxLayout(self.icon_box)
        ib_layout.setContentsMargins(0, 0, 0, 0)
        ib_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(get_colored_icon(get_asset_path(icon_key), color).pixmap(22, 22))
        ib_layout.addWidget(icon_lbl)
        layout.addWidget(self.icon_box)

        # Text Column
        text_v = QVBoxLayout()
        text_v.setSpacing(2)

        self.title_lbl = QLabel(title.upper())
        self.title_lbl.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 10px; font-weight: 800; letter-spacing: 0.5px;"
        )

        self.val_lbl = QLabel(value)
        self.val_lbl.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 22px; font-weight: 900;")

        text_v.addWidget(self.title_lbl)
        text_v.addWidget(self.val_lbl)
        layout.addLayout(text_v)
        layout.addStretch()

    def set_value(self, value: str) -> None:
        """Aggiorna il valore visualizzato nella card."""
        self.val_lbl.setText(value)


class AnomalyCard(ModernCard):
    """Card anomalia con design a lista orizzontale e badge di severità."""

    def __init__(self, anomaly, parent: QWidget | None = None) -> None:  # noqa: ANN001
        super().__init__(parent, elevation=6)
        self._setup_content(anomaly)

    def _setup_content(self, anomaly) -> None:  # noqa: ANN001
        color = self._get_severity_color(anomaly.severity)
        self.setObjectName("anomalyCard")
        self.setStyleSheet(f"QFrame#anomalyCard {{ border-left: 4px solid {color}; }}")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)

        # Icon Status
        icon_lbl = QLabel()
        emoji = {
            "low": Icons.INFO,
            "medium": Icons.ALERT_TRIANGLE,
            "high": Icons.X_CIRCLE,
            "critical": Icons.ACTIVITY,
        }.get(anomaly.severity, Icons.BELL)
        icon_lbl.setPixmap(get_colored_icon(get_asset_path(emoji), color).pixmap(24, 24))
        layout.addWidget(icon_lbl)

        # Message Content
        text_v = QVBoxLayout()
        text_v.setSpacing(2)

        msg_lbl = QLabel(anomaly.message)
        msg_lbl.setStyleSheet(f"color: {COLORS['text_dark']}; font-weight: 700; font-size: 13px;")
        msg_lbl.setWordWrap(True)
        text_v.addWidget(msg_lbl)

        if anomaly.suggestion:
            sug_lbl = QLabel(anomaly.suggestion)
            sug_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
            text_v.addWidget(sug_lbl)

        layout.addLayout(text_v, stretch=1)

        # Severity Badge
        sev_badge = QLabel(anomaly.severity.upper())
        sev_badge.setStyleSheet(f"""
            background-color: {color};
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 9px;
            font-weight: 900;
        """)
        layout.addWidget(sev_badge)

    def _get_severity_color(self, severity: str) -> str:
        return {
            "low": COLORS["info_blue"],
            "medium": COLORS["warning_yellow"],
            "high": COLORS["warning_orange"],
            "critical": COLORS["error_red"],
        }.get(severity, COLORS["text_muted"])


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

    def _setup_ui(self) -> None:  # noqa: PLR0915
        """Costruisce il layout a due colonne: statistiche a sinistra, anomalie a destra."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(25)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 10)

        title_v = QVBoxLayout()
        title_v.setSpacing(2)
        title = QLabel("System Health")
        title.setStyleSheet(f"font-size: 28px; font-weight: 900; color: {COLORS['text_dark']}; border: none;")
        subtitle = QLabel("Monitoraggio in tempo reale e diagnostica di sistema")
        subtitle.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px; font-weight: 500;")
        title_v.addWidget(title)
        title_v.addWidget(subtitle)
        header.addLayout(title_v)
        header.addStretch()

        self._alert_btn = ModernButton(
            "INVIA ALERT", variant=ModernButton.Variant.GHOST, icon=get_asset_path(Icons.SEND)
        )
        self._alert_btn.clicked.connect(self._send_telegram_alert)
        header.addWidget(self._alert_btn)

        self._refresh_btn = ModernButton(
            "AGGIORNA", variant=ModernButton.Variant.PRIMARY, icon=get_asset_path(Icons.REFRESH)
        )
        self._refresh_btn.clicked.connect(self.refresh)
        header.addWidget(self._refresh_btn)
        layout.addLayout(header)

        content = QHBoxLayout()
        content.setSpacing(30)

        left_panel = QVBoxLayout()
        left_panel.setSpacing(25)

        # 1. Main Gauge Card
        score_card = ModernCard(elevation=15)
        score_card.setStyleSheet(f"QFrame {{ background-color: {COLORS['bg_white']}; border-radius: 20px; }}")
        score_layout = QVBoxLayout(score_card)
        score_layout.setContentsMargins(20, 30, 20, 30)
        score_layout.setSpacing(15)

        self._score_badge = HealthScoreBadge(size=180)
        score_layout.addWidget(self._score_badge, alignment=Qt.AlignmentFlag.AlignCenter)

        self._status_label = QLabel("OTTIMO")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-weight: 900; font-size: 14px; letter-spacing: 1px;"
        )
        score_layout.addWidget(self._status_label)

        self._last_update = QLabel("Ultimo aggiornamento: --")
        self._last_update.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._last_update.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        score_layout.addWidget(self._last_update)
        left_panel.addWidget(score_card)

        # 2. Mini Stats Grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        self._stat_runs_ok = StatCard(
            "Bot Successo", color=COLORS["success_green"], icon_key=Icons.CHECK_CIRCLE
        )
        self._stat_runs_fail = StatCard("Bot Falliti", color=COLORS["error_red"], icon_key=Icons.X_CIRCLE)
        self._stat_error_rate = StatCard(
            "Error Rate", color=COLORS["warning_yellow"], icon_key=Icons.BAR_CHART
        )
        self._stat_anomalies = StatCard(
            "Anomalie", color=COLORS["warning_orange"], icon_key=Icons.ALERT_TRIANGLE
        )

        stats_grid.addWidget(self._stat_runs_ok, 0, 0)
        stats_grid.addWidget(self._stat_runs_fail, 0, 1)
        stats_grid.addWidget(self._stat_error_rate, 1, 0)
        stats_grid.addWidget(self._stat_anomalies, 1, 1)
        left_panel.addLayout(stats_grid)
        left_panel.addStretch()
        content.addLayout(left_panel, stretch=1)

        # 3. Anomalies Panel (Right)
        right_panel = QVBoxLayout()
        right_panel.setSpacing(15)

        anom_header = QHBoxLayout()
        anom_title = QLabel("Anomalie Rilevate")
        anom_title.setStyleSheet(f"font-size: 16px; font-weight: 800; color: {COLORS['text_dark']};")
        anom_header.addWidget(anom_title)

        self._anomaly_count_label = QLabel("0 problemi")
        self._anomaly_count_label.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-weight: 600; font-size: 13px;"
        )
        anom_header.addStretch()
        anom_header.addWidget(self._anomaly_count_label)
        right_panel.addLayout(anom_header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")

        self._anomalies_container = QWidget()
        self._anomalies_container.setStyleSheet("background: transparent;")
        self._anomalies_layout = QVBoxLayout(self._anomalies_container)
        self._anomalies_layout.setContentsMargins(5, 5, 15, 5)
        self._anomalies_layout.setSpacing(12)
        self._anomalies_layout.addStretch()

        scroll.setWidget(self._anomalies_container)
        right_panel.addWidget(scroll)

        content.addLayout(right_panel, stretch=2)
        layout.addLayout(content)

    def refresh(self) -> None:
        """Interroga i motori di analytics e il LogViewer per aggiornare tutte le card e lo score."""
        try:
            from src.core.logging.analytics import generate_analytics_report  # noqa: PLC0415
            from src.core.logging.viewer import LogViewer  # noqa: PLC0415

            report = generate_analytics_report(hours=24)
            self._score_badge.score = report.health_score
            self._status_label.setText(self._score_badge._get_status_text())

            health = LogViewer().generate_health_report()
            self._stat_runs_ok.set_value(str(health.get("bot_runs", {}).get("successful", 0)))
            self._stat_runs_fail.set_value(str(health.get("bot_runs", {}).get("failed", 0)))
            self._stat_error_rate.set_value(f"{health.get('error_rate_percent', 0):.1f}%")
            self._stat_anomalies.set_value(str(len(report.anomalies)))
            self._last_update.setText(
                f"Ultimo aggiornamento: {datetime.now(UTC).astimezone().strftime('%H:%M:%S')}"
            )
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
            empty.setStyleSheet(
                f"QFrame {{ background: {COLORS['bg_success_pastel']}; border-radius: 12px; border: 1px dashed {COLORS['success_green']}; }}"
            )
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
            from src.core.logging.alert_manager import get_alert_manager  # noqa: PLC0415
            from src.core.logging.analytics import generate_analytics_report  # noqa: PLC0415

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
            from src.core.logging.alert_manager import get_alert_manager  # noqa: PLC0415

            if (sent := get_alert_manager().check_and_alert(hours=24)) > 0:
                self._last_update.setText(f"🔔 {sent} alert inviati")

    def _show_toast(self, message: str, level: str = "info") -> None:
        """Inoltra una notifica interna al NotificationManager."""
        with suppress(Exception):
            from src.core.notification_manager import NotificationManager  # noqa: PLC0415

            NotificationManager.instance().add_notification(
                title="Health Panel", message=message, level=level
            )
