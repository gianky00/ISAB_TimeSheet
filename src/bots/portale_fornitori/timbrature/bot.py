"""
Bot TS - Timbrature Bot
Bot for accessing Timbrature section using Page Object Model.
"""
import os
from pathlib import Path
from typing import Dict, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.bots.base import BaseBot
from src.bots.portale_fornitori.timbrature.pages.timbrature_page import TimbraturePage
from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage
import time

class TimbratureBot(BaseBot):
    """
    Bot for downloading and archiving Timbrature data.
    """

    @property
    def name(self) -> str:
        return "Timbrature"

    @property
    def description(self) -> str:
        return "Scarica e archivia le timbrature dal portale ISAB"

    @staticmethod
    def get_name() -> str:
        return "Timbrature"

    @staticmethod
    def get_description() -> str:
        return "Scarica e archivia le timbrature dal portale ISAB"

    def __init__(self, data_da: str = "", data_a: str = "", fornitore: str = "", **kwargs):
        super().__init__(**kwargs)
        self.data_da = data_da
        self.data_a = data_a
        self.fornitore = fornitore
        self.storage = TimbratureStorage()

    def run(self, data: Dict[str, Any]) -> bool:
        """
        Executes the Timbrature workflow: Navigate -> Filter -> Download -> Import.
        """
        if isinstance(data, dict):
            self.data_da = data.get('data_da', self.data_da)
            self.data_a = data.get('data_a', self.data_a)
            self.fornitore = data.get('fornitore', self.fornitore)

        self.log(f"🚀 Inizio recupero timbrature per {self.fornitore} ({self.data_da} - {self.data_a})...")

        page = TimbraturePage(self.driver, self.log)

        # 1. Navigation
        if not page.navigate_to_timbrature():
            self.log("❌ Non riesco a raggiungere la sezione Timbrature.")
            return False

        # 2. Filter & Download
        if not page.set_filters(self.fornitore, self.data_da, self.data_a):
            self.log("❌ Filtri non applicati correttamente.")
            return False

        excel_path = page.download_excel()

        # 3. Process File
        if excel_path:
            self.log("✅ Report scaricato! Sto analizzando i dati...")
            try:
                self.storage.import_excel(excel_path, self.log)
                self.log("💾 Dati salvati nel database con successo.")
            except Exception as e:
                self.log(f"❌ Errore durante il salvataggio: {e}")
            finally:
                # Cleanup
                if os.path.exists(excel_path):
                    try:
                        os.remove(excel_path)
                        # self.log("🗑️ File Excel eliminato.")
                    except Exception as e:
                        pass
        else:
            self.log("⚠️ Non ho trovato dati o il download non è partito.")

        self.log("✨ Procedura conclusa.")
        return True

    @staticmethod
    def import_to_db_static(excel_path: str, db_path: Path, log_callback=None):
        """
        Static method for manual import (GUI).
        """
        storage = TimbratureStorage(db_path)
        return storage.import_excel(excel_path, log_callback)

    def execute(self, data: Any) -> bool:
        """Executes full workflow with login/logout."""
        try:
            if not self._safe_login_with_retry():
                return False

            result = self.run(data)
            self._logout()
            return result
        except Exception as e:
            self.log(f"Errore critico: {e}")
            return False
        finally:
            self.cleanup()
