"""
SyncroJob - SafeWork PDL Download Bot
Bot modulare per lo scarico e la stampa dei PDL.
"""

import logging
import time
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING, Any

import fitz
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from src.bots.safework.base import SafeworkBaseBot
from src.utils.printing import print_pdf

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


class SafeWorkPDLBot(SafeworkBaseBot):
    """Bot per lo scarico e la stampa automatizzata dei PDL."""

    def __init__(self, username, password, headless=False, timeout=30, download_path=""):
        super().__init__(username, password, headless, timeout, download_path)
        self.downloaded_files: list[str] = []
        self.missing_pdls: list[str] = []
        self.progress_callback: Callable[[int, bool], None] | None = None

    @staticmethod
    def get_name() -> str:
        return "Scarico PDL"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return [{"name": "Numero PDL", "type": "text"}]

    @property
    def name(self) -> str:
        return "scarico_pdl"

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Validazione specifica per SafeWork PDL."""
        self.log("🔍 Avvio validazione dati...")
        base_valid, base_msg = super().validate_data(data)
        if not base_valid:
            return False, base_msg

        rows = data.get("rows", []) if isinstance(data, dict) else data
        if not rows:
            return False, "Nessun dato da elaborare."

        found_pdl = False
        for _i, item in enumerate(rows):
            if item.get("pdl_number") or item.get("numero_pdl"):
                found_pdl = True
                break

        if not found_pdl:
            return False, "Nessun numero PDL trovato nei dati."

        return True, ""

    def set_progress_callback(self, callback):
        self.progress_callback = callback

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Ciclo principale di scarico PDL."""
        success_count = 0
        total = len(data)
        self.downloaded_files = []
        all_paths: list[str] = []

        for index, item in enumerate(data):
            try:
                self._check_stop()
                pdl_raw = item.get("pdl_number") or item.get("numero_pdl")
                if not pdl_raw:
                    continue

                pdl_num = self._sanitizza_pdl_number(pdl_raw)
                self.log(f"--- PDL {index + 1}/{total}: {pdl_num} ---")

                if self._esegui_ricerca_pdl(pdl_num):
                    path_p1 = self._scarica_parte_prima(pdl_num)
                    path_p2 = self._scarica_parte_seconda(pdl_num)

                    if (
                        path_p1
                        and path_p2
                        and self._unisci_e_stampa(pdl_num, path_p1, path_p2, item, all_paths)
                    ):
                        success_count += 1

                    self._safe_remove(path_p1)
                    self._safe_remove(path_p2)

                if self.progress_callback:
                    self.progress_callback(index, True)
            except Exception as e:
                self.log(f"❌ Errore PDL {pdl_raw}: {e}")

        return success_count == total

    def _sanitizza_pdl_number(self, pdl_raw: Any) -> str:
        num = str(pdl_raw).strip().upper().replace(" ", "")
        if num.isdigit() and len(num) == 6:
            suffix = "/S" if int(num) < 400000 else "/C"
            return f"{num}{suffix}"
        return num

    def _esegui_ricerca_pdl(self, pdl_num: str) -> bool:
        """Esegue ricerca PDL gestendo popup."""
        assert self.wait is not None
        try:
            campo = self.wait.until(EC.visibility_of_element_located((By.ID, "fldRicercaPdLVeloce")))
            campo.clear()
            campo.send_keys(pdl_num + Keys.ENTER)
            self._attendi_scomparsa_overlay()

            # Check se caricato
            self.wait.until(EC.presence_of_element_located((By.ID, "topIcon-acticonAnteprimaStampaMenu")))
            return True
        except Exception:
            self.log(f"⚠️ PDL {pdl_num} non caricato.")
            return False

    def _scarica_parte_prima(self, pdl_num: str) -> str | None:
        from src.bots.base.wait_helpers import poll_for_new_file

        ts = time.time()
        files_before = {str(f.resolve()) for f in Path(self.download_path).glob("*.pdf")}

        assert self.wait is not None
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "topIcon-acticonAnteprimaStampaMenu"))).click()
            self.wait.until(EC.element_to_be_clickable((By.ID, "appItaliano"))).click()

            f = poll_for_new_file(self.download_path, files_before, timeout=60)
            if f:
                dest = Path(self.download_path) / f"temp_p1_{int(ts)}.pdf"
                Path(f).rename(dest)
                self._clean_pdf(str(dest))
                return str(dest)
        except Exception:
            logger.debug("Impossibile scaricare la parte prima del PDL.")
        return None

    def _scarica_parte_seconda(self, pdl_num: str) -> str | None:
        from src.bots.base.wait_helpers import poll_for_new_file

        ts = time.time()
        files_before = {str(f.resolve()) for f in Path(self.download_path).glob("*.pdf")}

        assert self.driver is not None
        assert self.wait is not None
        try:
            # Espandi accordion
            with suppress(Exception):
                self.driver.find_element(By.ID, "lblTitoloParteSeconda").click()

            self.wait.until(EC.element_to_be_clickable((By.ID, "btnPrintPS"))).click()

            f = poll_for_new_file(self.download_path, files_before, timeout=90)
            if f:
                dest = Path(self.download_path) / f"temp_p2_{int(ts)}.pdf"
                Path(f).rename(dest)
                return str(dest)
        except Exception:
            logger.debug("Impossibile scaricare la parte seconda del PDL.")
        return None

    def _clean_pdf(self, path: str):
        try:
            doc = fitz.open(path)
            if doc.page_count >= 2:
                doc.delete_page(1)
                doc.save(path + ".tmp")
                doc.close()
                Path(path).unlink()
                Path(path + ".tmp").rename(path)
            else:
                doc.close()
        except Exception as e:
            logger.debug(f"Errore pulizia PDF: {e}")

    def _unisci_e_stampa(self, pdl_num, p1, p2, item, all_paths) -> bool:
        from src.utils.document_processor import DocumentProcessor

        nome = f"PDL_{pdl_num.replace('/', '-')}.pdf"
        out = Path(self.download_path) / nome
        if DocumentProcessor.merge_pdfs([p1, p2], str(out)):
            self.downloaded_files.append(str(out))
            if item.get("print_enabled") and item.get("printer_name"):
                print_pdf(str(out), item["printer_name"])
            return True
        return False

    def _safe_remove(self, path: str | None):
        if path and Path(path).exists():
            with suppress(Exception):
                Path(path).unlink()
