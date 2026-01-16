"""
SyncroJob - Timbrature Bot
Bot for accessing Timbrature section using Page Object Model.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from src.bots.base import BaseBot
from src.bots.portale_fornitori.timbrature.pages.timbrature_page import TimbraturePage
from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage


class TimbratureBot(BaseBot):
    """Bot per lo scarico e l'archiviazione automatica delle timbrature dal Portale Fornitori."""

    @property
    def name(self) -> str:
        """Restituisce il nome del bot."""
        return "Timbrature"

    @property
    def description(self) -> str:
        """Restituisce una descrizione delle funzionalità del bot."""
        return "Scarica e archivia le timbrature dal portale ISAB"

    @staticmethod
    def get_name() -> str:
        """Metodo statico che restituisce il nome del bot."""
        return "Timbrature"

    @staticmethod
    def get_description() -> str:
        """Metodo statico che restituisce la descrizione del bot."""
        return "Scarica e archivia le timbrature dal portale ISAB"

    def __init__(self, data_da: str = "", data_a: str = "", fornitore: str = "", **kwargs):
        super().__init__(**kwargs)
        self.data_da = data_da
        self.data_a = data_a
        self.fornitore = fornitore
        self.storage = TimbratureStorage()

    def validate_data(self, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Validazione specifica per Timbrature."""
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            return False, base_msg

        if not self.fornitore:
            if isinstance(data, dict) and not data.get("fornitore"):
                return False, "Fornitore non specificato."
            elif not isinstance(data, dict):
                return False, "Fornitore non specificato."

        if not self.data_da:
            if isinstance(data, dict) and data.get("data_da"):
                self.data_da = data.get("data_da")
            else:
                return False, "Data Inizio non specificata."

        return True, ""

    def run(self, data: Union[List[Dict[str, Any]], Dict[str, Any]]) -> bool:
        """
        Executes the Timbrature workflow: Navigate -> Filter -> Download -> Import.
        """
        if isinstance(data, dict):
            self.data_da = data.get("data_da", self.data_da)
            self.data_a = data.get("data_a", self.data_a)
            self.fornitore = data.get("fornitore", self.fornitore)

        self.log(f"🚀 Inizio recupero timbrature per {self.fornitore} ({self.data_da} - {self.data_a})...")

        if not self.driver:
            return False
        assert self.driver

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
                    except Exception:
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
