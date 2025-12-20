"""
Bot TS - Scarico TS Bot
Bot for downloading timesheets using Page Object Model.
"""
from pathlib import Path
from typing import List, Dict, Any
import time

from src.bots.base import BaseBot
from src.bots.scarico_ts.pages.scarico_ts_page import ScaricoTSPage

class ScaricaTSBot(BaseBot):
    """
    Bot for automatic timesheet download.
    """
    
    # Default supplier
    FORNITORE = "KK10608 - COEMI S.R.L."
    
    @staticmethod
    def get_name() -> str:
        return "Scarico TS"
    
    @staticmethod
    def get_description() -> str:
        return "Scarica i timesheet dal portale ISAB"
    
    @staticmethod
    def get_columns() -> list:
        return [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"}
        ]
    
    @property
    def name(self) -> str:
        return "Scarico TS"
    
    @property
    def description(self) -> str:
        return "Scarica i timesheet dal portale ISAB"
    
    def __init__(self, data_da: str = "01.01.2025", **kwargs):
        super().__init__(**kwargs)
        self.data_da = data_da
    
    def run(self, data: List[Dict[str, Any]]) -> bool:
        """
        Executes the download workflow.
        """
        if isinstance(data, dict):
            rows = data.get('rows', [])
            self.data_da = data.get('data_da', self.data_da)
        else:
            rows = data
        
        if not rows:
            self.log("Nessun dato da processare")
            return True
        
        self.log(f"Processamento {len(rows)} righe...")
        self.log(f"Data inizio: {self.data_da}")
        
        page = ScaricoTSPage(self.driver, self.log)
        
        # 1. Navigation
        if not page.navigate_to_timesheet():
            return False
        
        # 2. Setup Filters
        if not page.setup_filters(self.FORNITORE, self.data_da):
            return False
        
        # 3. Process Rows
        success_count = 0
        download_dir = Path(self.download_path) if self.download_path else Path.home() / "Downloads"
        
        for i, row in enumerate(rows, 1):
            self._check_stop()
            
            numero_oda = str(row.get('numero_oda', '')).strip()
            posizione_oda = str(row.get('posizione_oda', '')).strip()
            
            if not numero_oda:
                self.log(f"Riga {i}: Numero OdA mancante, saltata")
                continue
            
            self.log("-" * 40)
            self.log(f"Riga {i}/{len(rows)}: OdA='{numero_oda}', Pos='{posizione_oda}'")
            
            if page.search_and_download(numero_oda, posizione_oda, download_dir):
                success_count += 1
            
            time.sleep(1)
        
        self.log("-" * 40)
        self.log(f"Completato: {success_count}/{len(rows)} download riusciti")
        
        # Logout is handled by execute() in BaseBot or orchestrator
        return success_count == len(rows)
