"""
SyncroJob - Health Panel

Pannello completo per visualizzare health status, anomalie e analytics.
"""

from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.gui.widgets.modern_button import ModernButton


class HealthScoreBadge(QWidget):
    """Badge circolare grande con health score."""

    def __init__(self, parent=None, size: int = 120):
        super().__init__(parent)
        self._score = 100
        self._size = size
        self.setFixedSize(size, size)

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int):
        self._score = max(0, min(100, value))
        self.update()

    def _get_color(self) -> QColor:
        """Colore basato su score."""
        if self._score >= 80:
            return QColor("#22c55e")  # Verde
        elif self._score >= 60:
            return QColor("#eab308")  # Giallo
        elif self._score >= 40:
            return QColor("#f97316")  # Arancio
        else:
            return QColor("#ef4444")  # Rosso

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = self._size
        margin = 8

        # Background circle
        color = self._get_color()
        painter.setBrush(color.lighter(180))
        painter.setPen(QPen(color, 6))
        painter.drawEllipse(margin, margin, size - 2 * margin, size - 2 * margin)

        # Score text
        painter.setPen(color.darker(120))
        font = QFont()
        font.setPointSize(28)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, str(self._score))


class AnomalyCard(QFrame):
    """Card per visualizzare un'anomalia."""

    def __init__(self, anomaly, parent=None):
        super().__init__(parent)
        self._setup_ui(anomaly)

    def _setup_ui(self, anomaly):
        self.setStyleSheet(
            """
            QFrame {
                background-color: rgba(30, 41, 59, 0.8);
                border-radius: 8px;
                border-left: 4px solid %s;
                padding: 10px;
            }
            QLabel { color: #e2e8f0; }
        """
            % self._get_severity_color(anomaly.severity)
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        # Header
        header = QHBoxLayout()

        emoji = {"low": "ℹ️", "medium": "⚠️", "high": "🔴", "critical": "🚨"}.get(
            anomaly.severity, "📢"
        )
        title = QLabel(f"{emoji} {anomaly.message}")
        title.setStyleSheet("font-weight: bold; font-size: 13px;")
        title.setWordWrap(True)
        header.addWidget(title)

        severity_label = QLabel(anomaly.severity.upper())
        severity_label.setStyleSheet(
            f"color: {self._get_severity_color(anomaly.severity)}; font-size: 11px;"
        )
        header.addWidget(severity_label)

        layout.addLayout(header)

        # Suggestion
        if anomaly.suggestion:
            suggestion = QLabel(f"💡 {anomaly.suggestion}")
            suggestion.setStyleSheet(
                "color: #94a3b8; font-size: 11px; font-style: italic;"
            )
            suggestion.setWordWrap(True)
            layout.addWidget(suggestion)

    def _get_severity_color(self, severity: str) -> str:
        return {
            "low": "#3b82f6",
            "medium": "#eab308",
            "high": "#f97316",
            "critical": "#ef4444",
        }.get(severity, "#64748b")


class StatCard(QFrame):
    """Card per una statistica."""

    def __init__(
        self,
        title: str,
        value: str,
        icon: str = "",
        color: str = "#3b82f6",
        parent=None,
    ):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QFrame {
                background-color: rgba(30, 41, 59, 0.6);
                border-radius: 8px;
                border: 1px solid rgba(100, 116, 139, 0.3);
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        # Value
        value_label = QLabel(f"{icon} {value}" if icon else value)
        value_label.setStyleSheet(
            f"color: {color}; font-size: 24px; font-weight: bold;"
        )
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #94a3b8; font-size: 11px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)


class HealthPanel(QWidget):
    """
    Pannello completo per System Health.

    Mostra:
    - Health score grande
    - Statistiche bot runs
    - Lista anomalie rilevate
    - Pattern ricorrenti
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

        # Auto-refresh ogni 2 minuti
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.refresh)
        self._refresh_timer.start(2 * 60 * 1000)

        # Alert check scheduler ogni 30 minuti
        self._alert_timer = QTimer(self)
        self._alert_timer.timeout.connect(self._auto_check_alerts)
        self._alert_timer.start(30 * 60 * 1000)  # 30 minuti

        # Carica dati iniziali
        QTimer.singleShot(500, self.refresh)

    def _setup_ui(self):
        self.setObjectName("healthPanel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header = QHBoxLayout()

        title = QLabel("🏥 System Health")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #f1f5f9;")
        header.addWidget(title)

        header.addStretch()

        # Alert button
        self._alert_btn = ModernButton(
            "📢 Invia Alert", variant=ModernButton.Variant.SECONDARY
        )
        self._alert_btn.setToolTip("Invia alert Telegram per anomalie rilevate")
        self._alert_btn.clicked.connect(self._send_telegram_alert)
        header.addWidget(self._alert_btn)

        # Refresh button
        self._refresh_btn = ModernButton("🔄 Aggiorna")
        self._refresh_btn.clicked.connect(self.refresh)
        header.addWidget(self._refresh_btn)

        layout.addLayout(header)

        # Main content area
        content = QHBoxLayout()
        content.setSpacing(20)

        # Left: Score + Stats
        left_panel = QVBoxLayout()
        left_panel.setSpacing(15)

        # Score badge
        score_container = QFrame()
        score_container.setStyleSheet(
            """
            QFrame {
                background-color: rgba(30, 41, 59, 0.6);
                border-radius: 12px;
                border: 1px solid rgba(100, 116, 139, 0.3);
            }
        """
        )
        score_layout = QVBoxLayout(score_container)
        score_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._score_badge = HealthScoreBadge(size=140)
        score_layout.addWidget(
            self._score_badge, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self._score_label = QLabel("Health Score")
        self._score_label.setStyleSheet("color: #94a3b8; font-size: 14px;")
        self._score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addWidget(self._score_label)

        self._last_update = QLabel("Ultimo aggiornamento: --")
        self._last_update.setStyleSheet("color: #64748b; font-size: 10px;")
        self._last_update.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addWidget(self._last_update)

        left_panel.addWidget(score_container)

        # Stats grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(10)

        self._stat_runs_ok = StatCard("Bot Runs ✅", "0", color="#22c55e")
        self._stat_runs_fail = StatCard("Bot Runs ❌", "0", color="#ef4444")
        self._stat_error_rate = StatCard("Error Rate", "0%", color="#eab308")
        self._stat_anomalies = StatCard("Anomalie", "0", color="#f97316")

        stats_grid.addWidget(self._stat_runs_ok, 0, 0)
        stats_grid.addWidget(self._stat_runs_fail, 0, 1)
        stats_grid.addWidget(self._stat_error_rate, 1, 0)
        stats_grid.addWidget(self._stat_anomalies, 1, 1)

        left_panel.addLayout(stats_grid)
        left_panel.addStretch()

        content.addLayout(left_panel, stretch=1)

        # Right: Anomalies list
        right_panel = QVBoxLayout()
        right_panel.setSpacing(10)

        anomalies_title = QLabel("⚠️ Anomalie Rilevate")
        anomalies_title.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #f1f5f9;"
        )
        right_panel.addWidget(anomalies_title)

        # Scroll area per anomalie
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: rgba(30, 41, 59, 0.5);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(100, 116, 139, 0.5);
                border-radius: 4px;
            }
        """
        )

        self._anomalies_container = QWidget()
        self._anomalies_layout = QVBoxLayout(self._anomalies_container)
        self._anomalies_layout.setContentsMargins(0, 0, 0, 0)
        self._anomalies_layout.setSpacing(8)
        self._anomalies_layout.addStretch()

        scroll.setWidget(self._anomalies_container)
        right_panel.addWidget(scroll)

        content.addLayout(right_panel, stretch=2)

        layout.addLayout(content)

    def refresh(self):
        """Aggiorna dati dal sistema di analytics."""
        try:
            from src.core.logging.analytics import generate_analytics_report
            from src.core.logging.viewer import LogViewer

            # Report analytics
            report = generate_analytics_report(hours=24)

            # Health score
            self._score_badge.score = report.health_score

            # Stats dal viewer
            viewer = LogViewer()
            health = viewer.generate_health_report()

            bot_runs = health.get("bot_runs", {})
            success = bot_runs.get("successful", 0)
            failed = bot_runs.get("failed", 0)
            error_rate = health.get("error_rate_percent", 0)

            # Aggiorna stat cards
            self._stat_runs_ok.findChild(QLabel).setText(str(success))
            self._stat_runs_fail.findChild(QLabel).setText(str(failed))
            self._stat_error_rate.findChild(QLabel).setText(f"{error_rate:.1f}%")
            self._stat_anomalies.findChild(QLabel).setText(str(len(report.anomalies)))

            # Aggiorna timestamp
            self._last_update.setText(
                f"Ultimo aggiornamento: {datetime.now().strftime('%H:%M:%S')}"
            )

            # Aggiorna lista anomalie
            self._update_anomalies(report.anomalies)

        except Exception as e:
            # Fallback silenzioso
            self._last_update.setText(f"Errore: {str(e)[:30]}")

    def _update_anomalies(self, anomalies):
        """Aggiorna lista anomalie."""
        # Clear existing
        while self._anomalies_layout.count() > 1:  # Keep stretch
            item = self._anomalies_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not anomalies:
            no_anomalies = QLabel("✅ Nessuna anomalia rilevata")
            no_anomalies.setStyleSheet(
                "color: #22c55e; font-size: 14px; padding: 20px;"
            )
            no_anomalies.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._anomalies_layout.insertWidget(0, no_anomalies)
        else:
            for anomaly in anomalies:
                card = AnomalyCard(anomaly)
                self._anomalies_layout.insertWidget(
                    self._anomalies_layout.count() - 1, card
                )

    def _send_telegram_alert(self):
        """Invia alert Telegram manuale per anomalie correnti."""
        try:
            from src.core.logging.alert_manager import get_alert_manager
            from src.core.logging.analytics import generate_analytics_report

            report = generate_analytics_report(hours=24)

            if not report.anomalies:
                self._show_toast("ℹ️ Nessuna anomalia da segnalare", "info")
                return

            alert_manager = get_alert_manager()

            # Forza invio anche se sotto threshold
            for anomaly in report.anomalies:
                alert_manager.alert_on_critical(
                    anomaly
                ) if anomaly.severity == "critical" else None

            # Invia report summary
            summary = "🏥 <b>Health Report SyncroJob</b>\n\n"
            summary += f"<b>Score:</b> {report.health_score}%\n"
            summary += f"<b>Anomalie:</b> {len(report.anomalies)}\n\n"

            for a in report.anomalies[:5]:  # Max 5 anomalie
                emoji = {"low": "ℹ️", "medium": "⚠️", "high": "🔴", "critical": "🚨"}.get(
                    a.severity, "📢"
                )
                summary += f"{emoji} {a.message}\n"

            alert_manager.send_alert("Health Report", summary, "info")
            self._show_toast("✅ Alert inviato su Telegram", "success")

        except Exception as e:
            self._show_toast(f"❌ Errore invio alert: {str(e)[:50]}", "error")

    def _auto_check_alerts(self):
        """Check automatico anomalie e invio alert se necessario."""
        try:
            from src.core.logging.alert_manager import get_alert_manager

            alerts_sent = get_alert_manager().check_and_alert(hours=24)
            if alerts_sent > 0:
                self._last_update.setText(f"🔔 {alerts_sent} alert inviati")
        except Exception:
            pass  # Silenzioso in background

    def _show_toast(self, message: str, level: str = "info"):
        """Mostra toast notification."""
        try:
            from src.core.notification_manager import NotificationManager

            NotificationManager.instance().add(
                title="Health Panel", message=message, level=level
            )
        except Exception:
            pass
