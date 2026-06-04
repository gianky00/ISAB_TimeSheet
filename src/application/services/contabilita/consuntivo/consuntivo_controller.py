"""SyncroJob - Consuntivo Controller.

Logica di business per la gestione, generazione e scansione dei consuntivi.
Agnostico rispetto alla GUI.
"""

import logging
import os

from src.application.services import config_manager
from src.application.services.preventivi_manager import PreventiviGeneratorManager

logger = logging.getLogger(__name__)


class ConsuntivoController:
    """Controller per l'orchestrazione delle attività sui Consuntivi.

    Inizializza il controller per i consuntivi.
    """

    def __init__(self) -> None:
        self.base_network = r"\\192.168.11.251\Database_Tecnico_SMI\Contabilità strumentale"

    def get_dynamic_path(self, year: str) -> str:
        """Restituisce il percorso di rete calcolato per l'anno specificato."""
        return os.path.join(self.base_network, year, "CONSUNTIVI", year)

    def get_next_progressive(self, year: str) -> str:
        """Calcola il prossimo numero progressivo per l'anno dato."""
        path = self.get_dynamic_path(year)
        try:
            manager = PreventiviGeneratorManager("")
            return manager.get_next_progressive(path)
        except Exception:
            logger.exception("Errore calcolo progressivo")
            return "001"

    def get_config_options(self) -> dict[str, list[str]]:
        """Recupera le opzioni di configurazione per i menu a tendina."""
        config = config_manager.load_config()
        return {
            "tcl": config.get("preventivi_tcl", []),
            "stati": config.get("preventivi_stati", []),
            "tipologie": ["MISURA", "SQUADRA", "CHIAMATA", "FORNITURA", "PREVENTIVO"],
            "economie": ["SQUADRA GIORNALIERA", "SQUADRA SETTIMANALE", "CONSTATAZIONE PURA"],
        }

    def get_master_path(self) -> str:
        """Restituisce il percorso del file master configurato."""
        return str(config_manager.load_config().get("master_preventivi_path", ""))
