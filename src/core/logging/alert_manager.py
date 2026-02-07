"""
SyncroJob - Alert Manager

Gestisce invio automatico alert su Telegram per anomalie e eventi critici.
"""

import threading
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal

from .analytics import Anomaly, get_anomalies


@dataclass
class AlertConfig:
    """Configurazione soglie per alerting."""

    # Abilita/disabilita alerts
    enabled: bool = True

    # Soglie per alerting automatico
    error_rate_threshold: float = 10.0  # %
    failure_rate_threshold: float = 20.0  # %
    slow_operation_ms: int = 30000  # 30s

    # Cooldown tra alert dello stesso tipo (minuti)
    cooldown_minutes: int = 30

    # Livelli minimi per alert
    min_severity: Literal["low", "medium", "high", "critical"] = "high"


class AlertManager:
    """
    Gestisce invio automatico alert su Telegram per anomalie.

    Features:
    - Invio alert su anomalie critiche
    - Cooldown per evitare spam
    - Configurazione soglie
    - Integrazione con TelegramService
    """

    _instance = None

    @classmethod
    def instance(cls):
        """Singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self, config: AlertConfig | None = None):
        self.config = config or AlertConfig()
        self._last_alerts: dict[str, datetime] = {}
        self._telegram_service = None
        self._lock = threading.Lock()

    @property
    def telegram(self):
        """Lazy load TelegramService."""
        if self._telegram_service is None:
            with suppress(ImportError):
                from src.core.telegram import TelegramService

                self._telegram_service = TelegramService()
        return self._telegram_service

    def configure(
        self,
        enabled: bool | None = None,
        error_rate_threshold: float | None = None,
        failure_rate_threshold: float | None = None,
        slow_operation_ms: int | None = None,
        cooldown_minutes: int | None = None,
        min_severity: Literal["low", "medium", "high", "critical"] | None = None,
    ):
        """Aggiorna configurazione alert."""
        if enabled is not None:
            self.config.enabled = enabled
        if error_rate_threshold is not None:
            self.config.error_rate_threshold = error_rate_threshold
        if failure_rate_threshold is not None:
            self.config.failure_rate_threshold = failure_rate_threshold
        if slow_operation_ms is not None:
            self.config.slow_operation_ms = slow_operation_ms
        if cooldown_minutes is not None:
            self.config.cooldown_minutes = cooldown_minutes
        if min_severity is not None:
            self.config.min_severity = min_severity

    def _should_alert(self, anomaly: Anomaly) -> bool:
        """Verifica se un'anomalia deve generare alert."""
        if not self.config.enabled:
            return False

        # Check severity minimo
        severity_order = ["low", "medium", "high", "critical"]
        if severity_order.index(anomaly.severity) < severity_order.index(self.config.min_severity):
            return False

        # Check cooldown
        alert_key = f"{anomaly.type}:{anomaly.message[:50]}"
        with self._lock:
            last_alert = self._last_alerts.get(alert_key)
            if last_alert:
                cooldown = timedelta(minutes=self.config.cooldown_minutes)
                if datetime.now() - last_alert < cooldown:
                    return False

        return True

    def _record_alert(self, anomaly: Anomaly):
        """Registra che un alert è stato inviato."""
        alert_key = f"{anomaly.type}:{anomaly.message[:50]}"
        with self._lock:
            self._last_alerts[alert_key] = datetime.now()

    def _format_alert_message(self, anomaly: Anomaly) -> str:
        """Formatta messaggio alert per Telegram."""
        emoji = {"low": "ℹ️", "medium": "⚠️", "high": "🔴", "critical": "🚨"}.get(anomaly.severity, "📢")

        type_names = {
            "error_spike": "Error Rate Spike",
            "slow_operation": "Operazione Lenta",
            "high_failure_rate": "Fallimenti Bot",
            "unusual_pattern": "Pattern Anomalo",
        }

        lines = [
            f"{emoji} <b>ALERT SyncroJob</b>",
            "",
            f"<b>Tipo:</b> {type_names.get(anomaly.type, anomaly.type)}",
            f"<b>Severità:</b> {anomaly.severity.upper()}",
            f"<b>Messaggio:</b> {anomaly.message}",
        ]

        if anomaly.suggestion:
            lines.extend(("", f"💡 <i>{anomaly.suggestion}</i>"))

        # Aggiungi dettagli rilevanti
        if anomaly.details:
            lines.extend(("", "<b>Dettagli:</b>"))
            for key, value in list(anomaly.details.items())[:3]:
                lines.append(f"• {key}: {value}")

        lines.extend(("", f"<code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>"))

        return "\n".join(lines)

    def send_alert(
        self,
        title: str,
        message: str,
        level: Literal["info", "warning", "error", "critical"] = "info",
    ) -> bool:
        """
        Invia alert manuale via Telegram.

        Args:
            title: Titolo alert
            message: Messaggio
            level: Livello alert

        Returns:
            True se inviato con successo
        """
        if not self.telegram:
            return False

        emoji = {"info": "ℹ️", "warning": "⚠️", "error": "🔴", "critical": "🚨"}.get(level, "📢")

        formatted = f"{emoji} <b>{title}</b>\n\n{message}"

        try:
            self.telegram.send_message_sync(formatted)
            return True
        except Exception:
            return False

    def check_and_alert(self, hours: int = 24) -> int:
        """
        Controlla anomalie e invia alert se necessario.

        Args:
            hours: Ore di lookback per analisi

        Returns:
            Numero di alert inviati
        """
        if not self.config.enabled:
            return 0

        if not self.telegram:
            return 0

        anomalies = get_anomalies(hours)
        alerts_sent = 0

        for anomaly in anomalies:
            if self._should_alert(anomaly):
                message = self._format_alert_message(anomaly)
                with suppress(Exception):
                    self.telegram.send_message_sync(message)
                    self._record_alert(anomaly)
                    alerts_sent += 1

        return alerts_sent

    def alert_on_critical(self, anomaly: Anomaly) -> bool:
        """
        Invia alert immediato per anomalia critica (bypass config).

        Args:
            anomaly: Anomalia da segnalare

        Returns:
            True se alert inviato
        """
        if not self.telegram:
            return False

        if anomaly.severity != "critical":
            return False

        message = self._format_alert_message(anomaly)
        with suppress(Exception):
            self.telegram.send_message_sync(message)
            self._record_alert(anomaly)
            return True
        return False


# Singleton helper
def get_alert_manager() -> AlertManager:
    """Restituisce istanza singleton AlertManager."""
    return AlertManager.instance()
