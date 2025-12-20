"""
Bot TS - Carico TS Bot
Bot for Carico TS using POM.
"""
from typing import List, Dict, Any
from src.bots.base import BaseBot
from src.bots.carico_ts.pages.carico_ts_page import CaricoTSPage

class CaricoTSBot(BaseBot):
    
    FORNITORE = "KK10608 - COEMI S.R.L."
    
    @staticmethod
    def get_name() -> str:
        return "Carico TS"
    
    @staticmethod
    def get_description() -> str:
        return "Caricamento automatico timesheet"
    
    @staticmethod
    def get_columns() -> list:
        # Full list from original code
        return [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Codice Fiscale", "type": "text"},
            {"name": "Cognome", "type": "text"},
            {"name": "Nome", "type": "text"},
            {"name": "Mese", "type": "text"},
            {"name": "Anno", "type": "text"},
            {"name": "G 1", "type": "text"}, {"name": "G 2", "type": "text"}, {"name": "G 3", "type": "text"},
            {"name": "G 4", "type": "text"}, {"name": "G 5", "type": "text"}, {"name": "G 6", "type": "text"},
            {"name": "G 7", "type": "text"}, {"name": "G 8", "type": "text"}, {"name": "G 9", "type": "text"},
            {"name": "G T", "type": "text"}
        ]

    @property
    def name(self) -> str: return "Carico TS"
    
    @property
    def description(self) -> str: return "Caricamento automatico timesheet"

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
