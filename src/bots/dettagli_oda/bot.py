"""
Bot TS - Dettagli OdA Bot
Bot for Dettagli OdA using POM.
"""
from pathlib import Path
from typing import List, Dict, Any
import time

from src.bots.base import BaseBot
from src.bots.dettagli_oda.pages.dettagli_oda_page import DettagliOdAPage

class DettagliOdABot(BaseBot):
    
    @staticmethod
    def get_name() -> str:
        return "Dettagli OdA"
    
    @staticmethod
    def get_description() -> str:
        return "Scarica il dettaglio OdA"
    
    @staticmethod
    def get_columns() -> list:
        return [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Numero Contratto", "type": "combo", "options": []}
        ]
    
    @property
    def name(self) -> str:
        return "Dettagli OdA"
    
    @property
    def description(self) -> str:
        return "Scarica il dettaglio OdA"
    
    def __init__(self, data_a: str = "31.12.2025", fornitore: str = "KK10608 - COEMI S.R.L.", **kwargs):
        # Remove extra arguments passed by the factory that BaseBot doesn't accept
        kwargs.pop('data_da', None)
        super().__init__(**kwargs)
        self.data_a = data_a
        self.fornitore = fornitore

    def run(self, data: List[Dict[str, Any]]) -> bool:
        if isinstance(data, dict):
            rows = data.get('rows', [])
            self.data_a = data.get('data_a', self.data_a)
            self.fornitore = data.get('fornitore', self.fornitore)
        else:
            rows = data
            
        if not rows: return True
        
        self.log(f"Processamento {len(rows)} righe...")
        page = DettagliOdAPage(self.driver, self.log)
        
        if not page.navigate_to_dettagli(): return False
        if not page.setup_supplier(self.fornitore): return False
        
        download_dir = Path(self.download_path) if self.download_path else Path.home() / "Downloads"
        success = 0
        
        for i, row in enumerate(rows, 1):
            self._check_stop()
            oda = str(row.get('numero_oda', '')).strip()
            contract = str(row.get('numero_contratto', '')).strip()
            
            if not oda: continue
            
            self.log("-" * 40)
            self.log(f"Riga {i}: OdA={oda}, Contratto={contract}")

            if page.process_oda(oda, contract, self.data_a, download_dir):
                success += 1
            
            time.sleep(1)

        return success == len(rows)
