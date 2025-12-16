"""
Bot TS - Carico Timesheet
Bot per l'upload dei timesheet sul portale ISAB.
"""
from typing import Dict, Any, List
from ..base import BaseBot, BotStatus


class CaricoTSBot(BaseBot):
    """
    Bot per l'upload dei Timesheet sul portale ISAB.
    
    Funzionalità:
    - Login al portale ISAB
    - Navigazione alla sezione Timesheet
    - Upload file timesheet per commessa/mese/anno
    """
    
    @property
    def name(self) -> str:
        return "Carico TS"
    
    @property
    def description(self) -> str:
        return "Upload automatico dei Timesheet sul portale ISAB"
    
    @staticmethod
    def get_name() -> str:
        return "Carico TS"
    
    @staticmethod
    def get_description() -> str:
        return "Upload automatico dei Timesheet sul portale ISAB"
    
    @staticmethod
    def get_icon() -> str:
        return "📤"
    
    @staticmethod
    def get_columns() -> list:
        """Restituisce la configurazione delle colonne per la tabella dati."""
        return [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"},
            {"name": "Codice Fiscale", "type": "text"},
            {"name": "Ingresso", "type": "text"},
            {"name": "Uscita", "type": "text"},
            {"name": "Tipo Prestazione", "type": "text"},
            {"name": "C", "type": "text"},
            {"name": "M", "type": "text"},
            {"name": "Str D", "type": "text"},
            {"name": "Str N", "type": "text"},
            {"name": "Str F D", "type": "text"},
            {"name": "Str F N", "type": "text"},
            {"name": "Sq", "type": "text"},
            {"name": "Nota D", "type": "text"},
            {"name": "Nota S", "type": "text"},
            {"name": "F S", "type": "text"},
            {"name": "G T", "type": "text"}
        ]
    
    @staticmethod
    def get_config_key() -> str:
        return "last_carico_ts_data"
    
    def run(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue l'upload dei timesheet.
        
        Args:
            data: Lista di dict con i dati delle righe
        
        Returns:
            True se completato con successo
        """
        rows = data if isinstance(data, list) else data.get("rows", [])
        
        if not rows:
            self.log("[AVVISO] Nessun dato da processare")
            return True
        
        self.log(f"[INFO] Trovate {len(rows)} righe da processare")
        
        # TODO: Implementare la logica di upload
        self.log("[INFO] Funzionalità Carico TS in fase di sviluppo...")
        
        return True


class CaricoTSBotFactory:
    """Factory per creare istanze di CaricoTSBot."""
    
    @staticmethod
    def create(**kwargs) -> CaricoTSBot:
        return CaricoTSBot(**kwargs)
