"""Inizializzazione del pacchetto footer."""

from .business_info import FooterLeftWidget
from .components import ClickableLabel, FooterItemWidget, StartupConsole, StatsCard
from .manager import FooterStatsManager
from .status_bar import FooterRightWidget
from .telemetry import BootTelemetryWidget

__all__ = [
    "BootTelemetryWidget",
    "ClickableLabel",
    "FooterItemWidget",
    "FooterLeftWidget",
    "FooterRightWidget",
    "FooterStatsManager",
    "StartupConsole",
    "StatsCard",
]
