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
        return "Scarica dettaglio OdA (o lista generale se OdA vuoto)"
    
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
        return "Scarica dettaglio OdA (o lista generale se OdA vuoto)"
    
    def __init__(self, data_da: str = "01.01.2024", data_a: str = "31.12.2025", fornitore: str = "KK10608 - COEMI S.R.L.", **kwargs):
        super().__init__(**kwargs)
        self.data_da = data_da
        self.data_a = data_a
        self.fornitore = fornitore

    def run(self, data: List[Dict[str, Any]]) -> bool:
        if isinstance(data, dict):
            rows = data.get('rows', [])
            self.data_da = data.get('data_da', self.data_da)
            self.data_a = data.get('data_a', self.data_a)
            self.fornitore = data.get('fornitore', self.fornitore)
        else:
            rows = data
            
        if not rows: return True
        
        self.log(f"🚀 Avvio scarico dettagli per {len(rows)} OdA...")
        page = DettagliOdAPage(self.driver, self.log)
        
        # Define source (System Downloads) and destination (Configured Path)
        source_dir = Path.home() / "Downloads"
        dest_dir = Path(self.download_path) if self.download_path else source_dir

        success = 0
        
        for i, row in enumerate(rows, 1):
            self._check_stop()
            oda = str(row.get('numero_oda', '')).strip()
            contract = str(row.get('numero_contratto', '')).strip()
            
            # Note: ODA can be empty for General List export
            
            # self.log("-" * 40)
            # self.log(f"Riga {i}: OdA={oda}, Contratto={contract}")

            # Navigate and Setup for each row as required by the workflow (resetting tabs)
            # Pass (i==1) to let the page know if it's the first row
            if not page.navigate_to_dettagli(is_first_row=(i==1)):
                self.log("❌ Problema nella navigazione.")
                continue
            if not page.setup_supplier(self.fornitore):
                self.log("❌ Fornitore non selezionabile.")
                continue

            if page.process_oda(oda, contract, self.data_da, self.data_a, source_dir, dest_dir):
                success += 1
            
            time.sleep(1)

        page.logout()
        self.log("✨ Procedura conclusa.")
        return success == len(rows)
