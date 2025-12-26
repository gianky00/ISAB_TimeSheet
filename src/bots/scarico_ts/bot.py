"""
Bot TS - Scarico TS Bot
Bot per il download automatico dei timesheet dal portale ISAB.
"""
from pathlib import Path
from typing import List, Dict, Any

from src.bots.base import BaseBot, BotStatus
from src.bots.scarico_ts.pages.scarico_ts_page import ScaricoTSPage
from src.core import config_manager
from src.bots import register_bot

@register_bot('scarico_ts')
class ScaricaTSBot(BaseBot):
    """
    Bot per lo scarico automatico dei timesheet.
    """
    
    METADATA = {
        "name": "Scarico TS",
        "description": "Scarica i timesheet dal portale ISAB",
        "icon": "📥",
        "columns": [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"}
        ],
        "config_key": "last_ts_data"
    }

    @property
    def name(self) -> str:
        return self.METADATA["name"]
    
    @property
    def description(self) -> str:
        return self.METADATA["description"]
    
    def __init__(self, data_da: str = "01.01.2025", fornitore: str = "", elabora_ts: bool = False, **kwargs):
        """
        Inizializza il bot.
        """
        super().__init__(**kwargs)
        self.data_da = data_da
        self.fornitore = fornitore
        self.elabora_ts = elabora_ts
        self.page = None
    
    def run(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue il download dei timesheet utilizzando il Page Object Model.
        """
        # Estrai i dati
        if isinstance(data, dict):
            rows = data.get('rows', [])
            self.data_da = data.get('data_da', self.data_da)
            if data.get('fornitore'):
                self.fornitore = data.get('fornitore')
        else:
            rows = data
        
        if not rows:
            self.log("ℹ️ Nessun dato da processare.")
            return True
        
        self.log(f"🚀 Inizio scarico TS per {len(rows)} OdA (Fornitore: {self.fornitore})...")
        
        # Initialize Page Object
        self.page = ScaricoTSPage(self.driver, self.log)

        try:
            # 1. Naviga a Report -> Timesheet
            if not self.page.navigate_to_timesheet():
                return False
            
            # 2. Imposta filtri (Fornitore e Data)
            if not self.page.setup_filters(self.fornitore, self.data_da):
                return False
            
            # 3. Processa ogni riga
            success_count = 0

            # Usa directory download di sistema (o quella configurata come dest_dir nel bot)
            # Se self.download_path è settato (dal pannello), usiamolo come destinazione.
            download_dir = Path(self.download_path) if self.download_path else Path.home() / "Downloads"
            if not download_dir.exists():
                download_dir.mkdir(parents=True, exist_ok=True)

            for i, row in enumerate(rows, 1):
                self._check_stop()
                
                numero_oda = str(row.get('numero_oda', '')).strip()
                posizione_oda = str(row.get('posizione_oda', '')).strip()
                
                if not numero_oda:
                    self.log(f"Riga {i}: Numero OdA mancante, saltata")
                    continue
                
                self.log(f"➡️ Processing OdA {numero_oda} ({i}/{len(rows)})...")
                
                if self.page.search_and_download(numero_oda, posizione_oda, download_dir):
                    success_count += 1
            
            self.log(f"✨ Operazione completata. {success_count}/{len(rows)} file scaricati.")
            
            self._logout()
            return success_count == len(rows)
            
        except Exception as e:
            self.log(f"❌ Errore imprevisto: {e}")
            return False

    def execute(self, data: List[Dict[str, Any]]) -> bool:
        """
        Esegue il workflow completo: login -> download -> logout -> chiusura.
        """
        self._stop_requested = False
        
        try:
            if not self._safe_login_with_retry():
                self.status = BotStatus.ERROR
                return False
            
            self.status = BotStatus.RUNNING
            result = self.run(data)
            
            self.status = BotStatus.COMPLETED if result else BotStatus.ERROR
            return result
            
        except InterruptedError:
            self.log("Bot interrotto")
            self.status = BotStatus.STOPPED
            return False
        except Exception as e:
            self.log(f"✗ Errore esecuzione: {e}")
            self.status = BotStatus.ERROR
            return False
        finally:
            self.cleanup()
