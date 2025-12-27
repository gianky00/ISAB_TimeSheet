"""
Bot TS - Carico TS Bot
Bot for Carico TS using POM.
"""
from typing import List, Dict, Any
from src.bots.base import BaseBot
from src.bots.carico_ts.pages.carico_ts_page import CaricoTSPage
from src.bots import register_bot

@register_bot('carico_ts')
class CaricoTSBot(BaseBot):
    
    FORNITORE = "KK10608 - COEMI S.R.L."
    
    METADATA = {
        "name": "Carico TS",
        "description": "Carica i timesheet sul portale ISAB",
        "icon": "📤",
        "columns": [
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
        ],
        "config_key": "last_carico_ts_data"
    }

    @property
    def name(self) -> str: return self.METADATA["name"]
    
    @property
    def description(self) -> str: return self.METADATA["description"]

    @property
    def columns(self) -> list: return self.METADATA["columns"]

    def run(self, data: List[Dict[str, Any]]) -> bool:
        rows = data if isinstance(data, list) else data.get('rows', [])
        if not rows: return True
        
        # Original logic: process ONLY the first row
        row = rows[0]
        oda = str(row.get('numero_oda', '')).strip()
        
        self.log(f"Avvio Carico TS per OdA: {oda}")
        
        page = CaricoTSPage(self.driver, self.log)
        
        if not page.navigate(): return False
        if not page.select_supplier(self.FORNITORE): return False
        
        if page.process_oda(oda):
            self.log("OdA estratta. Bot terminato (come da logica originale).")
            return True

        return False
