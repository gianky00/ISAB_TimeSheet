"""SyncroJob - GUI Panels Module.

Facade per retrocompatibilit .
"""

from src.gui.controllers.bot_worker import BotWorker
from src.gui.panels.base import BaseBotPanel
from src.gui.panels.carico_ts import CaricoTSPanel
from src.gui.panels.consuntivo_panel import ConsuntivoPanel
from src.gui.panels.contabilita_kpi import ContabilitaKPIPanel
from src.gui.panels.contabilita_panel import ContabilitaPanel
from src.gui.panels.dashboard_panel import DashboardPanel
from src.gui.panels.dettagli_oda import DettagliOdAPanel
from src.gui.panels.dipendenti import DipendentiPanel
from src.gui.panels.help_panel import HelpPanel
from src.gui.panels.notifications_panel import NotificationsPanel
from src.gui.panels.pdl import PDLDBPanel
from src.gui.panels.prenota_bp import PrenotaBPPanel
from src.gui.panels.ricerca_pdl import RicercaPDLPanel
from src.gui.panels.scarico_ore_panel import ScaricoOrePanel
from src.gui.panels.scarico_pdl import ScaricoPDLPanel
from src.gui.panels.scarico_ts import ScaricaTSPanel
from src.gui.panels.settings.main_panel import SettingsPanel
from src.gui.panels.storico_oda import StoricoOdaPanel
from src.gui.panels.timbrature_bot import TimbratureBotPanel
from src.gui.panels.timbrature_db import TimbratureDBPanel

__all__ = [
    "BaseBotPanel",
    "BotWorker",
    "CaricoTSPanel",
    "ConsuntivoPanel",
    "ContabilitaKPIPanel",
    "ContabilitaPanel",
    "DashboardPanel",
    "DettagliOdAPanel",
    "DipendentiPanel",
    "HelpPanel",
    "NotificationsPanel",
    "PDLDBPanel",
    "PrenotaBPPanel",
    "RicercaPDLPanel",
    "ScaricaTSPanel",
    "ScaricoOrePanel",
    "ScaricoPDLPanel",
    "SettingsPanel",
    "StoricoOdaPanel",
    "TimbratureBotPanel",
    "TimbratureDBPanel",
]
