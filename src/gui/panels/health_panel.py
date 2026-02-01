"""
SyncroJob - Health Panel

Pannello completo per visualizzare health status, anomalie e analytics.
Design con tema chiaro coerente con il resto dell'applicazione.
"""

from datetime import datetime

from PyQt6.QtCore import Qt, QTimer, QRectF
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
    """Badge circolare con arco progressivo - tema chiaro."""

    def __init__(self, parent=None, size: int = 160):
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
        if self._score >= 80:
            return QColor("#28a745")  # Verde
        elif self._score >= 60:
            return QColor("#ffc107")  # Giallo
        elif self._score >= 40:
            return QColor("#fd7e14")  # Arancio
        else:
            return QColor("#dc3545")  # Rosso

    def _get_status_text(self) -> str:
        if self._score >= 80:
            return "OTTIMO"
        elif self._score >= 60:
            return "DISCRETO"
        elif self._score >= 40:
            return "ATTENZIONE"
        else:
            return "CRITICO"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = self._size
        margin = 15
        arc_width = 12

        color = self._get_color()
        rect = QRectF(margin, margin, size - 2 * margin, size - 2 * margin)

        # Background track (grigio chiaro)
        track_color = QColor("#e9ecef")
        painter.setPen(QPen(track_color, arc_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(rect)

        # Progress arc
        painter.setPen(QPen(color, arc_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        span_angle = int(360 * 16 * self._score / 100)
        painter.drawArc(rect, 90 * 16, -span_angle)

        # Center circle (bianco)
        inner_rect = rect.adjusted(18, 18, -18, -18)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(inner_rect)

        # Score number (testo scuro)
        painter.setPen(QColor("#343a40"))
        font = QFont("Segoe UI", 36, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(self._score))


class StatCard(QFrame):
    """Card statistica con design chiaro."""

    def __init__(
        self,
        title: str,
        value: str = "0",
        icon: str = "",
        color: str = "#007bff",
        parent=None,
    ):
        super().__init__(parent)
        self._value_label = None
        self._color = color
        self._setup_ui(title, value, icon, color)

    def _setup_ui(self, title: str, value: str, icon: str, color: str):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #dee2e6;
                border-left: 4px solid {color};
            }}
            QFrame:hover {{
                border: 1px solid {color};
                border-left: 4px solid {color};
                background-color: #f8f9fa;
            }}
        """)
        self.setMinimumSize(140, 95)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        # Icon + Title row
        header = QHBoxLayout()
        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 18px; border: none;")
            header.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #6c757d; font-size: 12px; font-weight: 500; border: none;")
        header.addWidget(title_label)
        header.addStretch()
        layout.addLayout(header)

        # Value
        self._value_label = QLabel(value)
        self._value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold; border: none;")
        layout.addWidget(self._value_label)

    def set_value(self, value: str):
        if self._value_label:
            self._value_label.setText(value)


class AnomalyCard(QFrame):
    """Card anomalia con design chiaro e leggibile."""

    def __init__(self, anomaly, parent=None):
        super().__init__(parent)
        self._setup_ui(anomaly)

    def _setup_ui(self, anomaly):
        border_color = self._get_severity_color(anomaly.severity)
        bg_color = self._get_bg_color(anomaly.severity)
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 10px;
                border: 1px solid {border_color}40;
                border-left: 5px solid {border_color};
            }}
            QLabel {{ background: transparent; border: none; }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Header row
        header = QHBoxLayout()

        emoji = {"low": "ℹ️", "medium": "⚠️", "high": "🔴", "critical": "🚨"}.get(
            anomaly.severity, "📢"
        )
        
        title = QLabel(f"{emoji}  {anomaly.message}")
        title.setStyleSheet("color: #343a40; font-weight: 600; font-size: 14px;")
        title.setWordWrap(True)
        header.addWidget(title, stretch=1)

        severity_badge = QLabel(anomaly.severity.upper())
        severity_badge.setStyleSheet(f"""
            QLabel {{
                color: {border_color};
                background-color: {border_color}20;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 10px;
                font-weight: bold;
            }}
        """)
        header.addWidget(severity_badge)

        layout.addLayout(header)

        # Suggestion
        if anomaly.suggestion:
            suggestion = QLabel(f"💡 {anomaly.suggestion}")
            suggestion.setStyleSheet(
                "color: #495057; font-size: 12px; padding-left: 24px;"
            )
            suggestion.setWordWrap(True)
            layout.addWidget(suggestion)

    def _get_severity_color(self, severity: str) -> str:
        return {
            "low": "#007bff",
            "medium": "#ffc107",
            "high": "#fd7e14",
            "critical": "#dc3545",
        }.get(severity, "#6c757d")

    def _get_bg_color(self, severity: str) -> str:
        return {
            "low": "#e7f1ff",
            "medium": "#fff8e1",
            "high": "#fff3e0",
            "critical": "#ffebee",
        }.get(severity, "#f8f9fa")


class HealthPanel(QWidget):
    """Pannello Health con design chiaro coerente con l'app."""

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
        self._alert_timer.start(30 * 60 * 1000)

        # Carica dati iniziali
        QTimer.singleShot(500, self.refresh)

    def _setup_ui(self):
        self.setObjectName("healthPanel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # ═══════════════════════════════════════════
        # HEADER
        # ═══════════════════════════════════════════
        header = QHBoxLayout()

        title = QLabel("📊 System Health")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #343a40;
            border: none;
        """)
        header.addWidget(title)

        header.addStretch()

        # Buttons
        self._alert_btn = ModernButton(
            "📢 Invia Alert", variant=ModernButton.Variant.SECONDARY
        )
        self._alert_btn.setToolTip("Invia alert Telegram per anomalie rilevate")
        self._alert_btn.clicked.connect(self._send_telegram_alert)
        header.addWidget(self._alert_btn)

        self._refresh_btn = ModernButton("🔄 Aggiorna")
        self._refresh_btn.clicked.connect(self.refresh)
        header.addWidget(self._refresh_btn)

        layout.addLayout(header)

        # ═══════════════════════════════════════════
        # MAIN CONTENT: 2 columns
        # ═══════════════════════════════════════════
        content = QHBoxLayout()
        content.setSpacing(24)

        # ───────────────────────────────────────
        # LEFT COLUMN: Score + Stats
        # ───────────────────────────────────────
        left_panel = QVBoxLayout()
        left_panel.setSpacing(20)

        # Score Card Container
        score_card = QFrame()
        score_card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 16px;
                border: 1px solid #dee2e6;
            }
        """)
        score_layout = QVBoxLayout(score_card)
        score_layout.setContentsMargins(24, 24, 24, 24)
        score_layout.setSpacing(12)

        # Badge
        self._score_badge = HealthScoreBadge(size=160)
        score_layout.addWidget(
            self._score_badge, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Status label
        self._status_label = QLabel("OTTIMO")
        self._status_label.setStyleSheet("""
            color: #28a745;
            font-size: 16px;
            font-weight: bold;
            letter-spacing: 2px;
            border: none;
        """)
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addWidget(self._status_label)

        # Ultimo aggiornamento
        self._last_update = QLabel("Ultimo aggiornamento: --")
        self._last_update.setStyleSheet("color: #6c757d; font-size: 11px; border: none;")
        self._last_update.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addWidget(self._last_update)

        left_panel.addWidget(score_card)

        # Stats title
        stats_title = QLabel("📈 Statistiche Ultime 24h")
        stats_title.setStyleSheet("color: #495057; font-size: 14px; font-weight: 600; border: none;")
        left_panel.addWidget(stats_title)

        # Stats Grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(12)

        self._stat_runs_ok = StatCard("Bot Successo", "0", "✅", "#28a745")
        self._stat_runs_fail = StatCard("Bot Falliti", "0", "❌", "#dc3545")
        self._stat_error_rate = StatCard("Error Rate", "0%", "📉", "#ffc107")
        self._stat_anomalies = StatCard("Anomalie", "0", "⚠️", "#fd7e14")

        stats_grid.addWidget(self._stat_runs_ok, 0, 0)
        stats_grid.addWidget(self._stat_runs_fail, 0, 1)
        stats_grid.addWidget(self._stat_error_rate, 1, 0)
        stats_grid.addWidget(self._stat_anomalies, 1, 1)

        left_panel.addLayout(stats_grid)
        left_panel.addStretch()

        content.addLayout(left_panel, stretch=1)

        # ───────────────────────────────────────
        # RIGHT COLUMN: Anomalies
        # ───────────────────────────────────────
        right_panel = QVBoxLayout()
        right_panel.setSpacing(16)

        anomalies_header = QHBoxLayout()
        anomalies_title = QLabel("⚠️ Anomalie Rilevate")
        anomalies_title.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #343a40; border: none;"
        )
        anomalies_header.addWidget(anomalies_title)
        anomalies_header.addStretch()
        
        self._anomaly_count_label = QLabel("0 problemi")
        self._anomaly_count_label.setStyleSheet("color: #6c757d; font-size: 12px; border: none;")
        anomalies_header.addWidget(self._anomaly_count_label)
        
        right_panel.addLayout(anomalies_header)

        # Scroll area per anomalie
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f1f3f4;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #c4c9cc;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a8adb0;
            }
        """)

        self._anomalies_container = QWidget()
        self._anomalies_layout = QVBoxLayout(self._anomalies_container)
        self._anomalies_layout.setContentsMargins(0, 0, 8, 0)
        self._anomalies_layout.setSpacing(12)
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

            report = generate_analytics_report(hours=24)

            # Health score
            self._score_badge.score = report.health_score
            
            # Status label update
            status_text = self._score_badge._get_status_text()
            status_color = self._score_badge._get_color().name()
            self._status_label.setText(status_text)
            self._status_label.setStyleSheet(f"""
                color: {status_color};
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 2px;
                border: none;
            """)

            # Stats dal viewer
            viewer = LogViewer()
            health = viewer.generate_health_report()

            bot_runs = health.get("bot_runs", {})
            success = bot_runs.get("successful", 0)
            failed = bot_runs.get("failed", 0)
            error_rate = health.get("error_rate_percent", 0)

            # Aggiorna stat cards
            self._stat_runs_ok.set_value(str(success))
            self._stat_runs_fail.set_value(str(failed))
            self._stat_error_rate.set_value(f"{error_rate:.1f}%")
            self._stat_anomalies.set_value(str(len(report.anomalies)))

            # Aggiorna timestamp
            self._last_update.setText(
                f"Ultimo aggiornamento: {datetime.now().strftime('%H:%M:%S')}"
            )

            # Aggiorna lista anomalie
            self._update_anomalies(report.anomalies)

        except Exception as e:
            self._last_update.setText(f"Errore: {str(e)[:30]}")

    def _update_anomalies(self, anomalies):
        """Aggiorna lista anomalie."""
        # Clear existing
        while self._anomalies_layout.count() > 1:
            item = self._anomalies_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Update count
        count = len(anomalies)
        self._anomaly_count_label.setText(f"{count} problema{'i' if count != 1 else ''}")

        if not anomalies:
            # Empty state card
            empty_card = QFrame()
            empty_card.setStyleSheet("""
                QFrame {
                    background-color: #e8f5e9;
                    border-radius: 12px;
                    border: 1px dashed #81c784;
                }
            """)
            empty_layout = QVBoxLayout(empty_card)
            empty_layout.setContentsMargins(24, 32, 24, 32)
            
            emoji = QLabel("✨")
            emoji.setStyleSheet("font-size: 48px; border: none;")
            emoji.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.addWidget(emoji)
            
            text = QLabel("Nessuna anomalia rilevata")
            text.setStyleSheet("color: #2e7d32; font-size: 16px; font-weight: 600; border: none;")
            text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.addWidget(text)
            
            subtext = QLabel("Il sistema funziona correttamente")
            subtext.setStyleSheet("color: #558b2f; font-size: 12px; border: none;")
            subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.addWidget(subtext)
            
            self._anomalies_layout.insertWidget(0, empty_card)
        else:
            for anomaly in anomalies:
                card = AnomalyCard(anomaly)
                self._anomalies_layout.insertWidget(
                    self._anomalies_layout.count() - 1, card
                )

    def _send_telegram_alert(self):
        """Invia alert Telegram manuale."""
        try:
            from src.core.logging.alert_manager import get_alert_manager
            from src.core.logging.analytics import generate_analytics_report

            report = generate_analytics_report(hours=24)

            if not report.anomalies:
                self._show_toast("ℹ️ Nessuna anomalia da segnalare", "info")
                return

            alert_manager = get_alert_manager()

            for anomaly in report.anomalies:
                if anomaly.severity == "critical":
                    alert_manager.alert_on_critical(anomaly)

            summary = "🏥 <b>Health Report SyncroJob</b>\n\n"
            summary += f"<b>Score:</b> {report.health_score}%\n"
            summary += f"<b>Anomalie:</b> {len(report.anomalies)}\n\n"

            for a in report.anomalies[:5]:
                emoji = {"low": "ℹ️", "medium": "⚠️", "high": "🔴", "critical": "🚨"}.get(
                    a.severity, "📢"
                )
                summary += f"{emoji} {a.message}\n"

            alert_manager.send_alert("Health Report", summary, "info")
            self._show_toast("✅ Alert inviato su Telegram", "success")

        except Exception as e:
            self._show_toast(f"❌ Errore invio alert: {str(e)[:50]}", "error")

    def _auto_check_alerts(self):
        """Check automatico anomalie."""
        try:
            from src.core.logging.alert_manager import get_alert_manager

            alerts_sent = get_alert_manager().check_and_alert(hours=24)
            if alerts_sent > 0:
                self._last_update.setText(f"🔔 {alerts_sent} alert inviati")
        except Exception:
            pass

    def _show_toast(self, message: str, level: str = "info"):
        """Mostra toast notification."""
        try:
            from src.core.notification_manager import NotificationManager

            NotificationManager.instance().add(
                title="Health Panel", message=message, level=level
            )
        except Exception:
            pass
