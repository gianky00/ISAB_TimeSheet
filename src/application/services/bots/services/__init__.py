"""Inizializzazione del pacchetto services."""

from src.application.services.bots.services.base_service import BaseBotService
from src.application.services.bots.services.prenota_bp_service import PrenotaBPService
from src.application.services.bots.services.scarico_pdl_service import ScaricoPDLService
from src.application.services.bots.services.scarico_ts_service import ScaricoTSService

__all__ = [
    "BaseBotService",
    "PrenotaBPService",
    "ScaricoPDLService",
    "ScaricoTSService",
]
