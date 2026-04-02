# mypy: disable-error-code="no-untyped-call"
"""
SyncroJob - Playwright SafeWork PDL Download Bot
Versione Playwright del bot per lo scarico e la stampa dei PDL.
"""

import time
from contextlib import suppress
from pathlib import Path
from typing import Any, ClassVar, Final

import fitz
from playwright.sync_api import TimeoutError

from src.bots.base.base_bot import StepStatus
from src.bots.safework.playwright_base import PlaywrightSafeworkBaseBot
from src.utils.document_processor import DocumentProcessor
from src.utils.printing import print_pdf

# Costanti per soglie e limiti
MAX_PDL_DIGITS: Final[int] = 6
PDL_THRESHOLD_NORTH_SOUTH: Final[int] = 400000


class PlaywrightSafeWorkPDLBot(PlaywrightSafeworkBaseBot):
    """Bot per lo scarico e la stampa automatizzata dei PDL usando Playwright."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login SafeWork"),
        ("search", "Ricerca PdL"),
        ("download_p1", "Scarico Parte Prima"),
        ("download_p2", "Scarico Parte Seconda"),
        ("merge", "Unione e Stampa"),
        ("session", "Chiusura Sessione"),
    ]

    def __init__(  # noqa: PLR0913
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = 30,
        download_path: str = "",
        account_type: str = "Esecutore",
    ) -> None:
        super().__init__(username, password, headless, timeout, download_path, account_type=account_type)
        self.downloaded_files: list[str] = []

    @property
    def name(self) -> str:
        return "Scarico PDL (PW)"

    @property
    def description(self) -> str:
        return "Scarica e stampa Permessi di Lavoro da SafeWork (Playwright)"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return [{"name": "numero_pdl", "label": "Numero PDL", "type": "text"}]

    def run(self, data: list[dict[str, Any]]) -> bool:
        self.update_step("login", StepStatus.COMPLETED)

        success_count = 0
        total = len(data)
        self.downloaded_files = []
        all_pdl_paths: list[str] = []

        self.log(f"🚀 Inizio elaborazione (PW) di {total} PDL...")

        for index, item in enumerate(data):
            pdl_raw = "N/A"
            try:
                self._check_stop()
                val = item.get("numero_pdl")
                pdl_raw = str(val) if val else ""
                if not pdl_raw:
                    continue

                pdl_num = self._sanitizza_pdl_number(pdl_raw)
                self.log(f"📋 PDL {index + 1}/{total}: {pdl_num}")

                self.update_step("search", StepStatus.RUNNING)
                if self._esegui_ricerca_pdl(pdl_num):
                    self.update_step("search", StepStatus.COMPLETED)

                    self.update_step("download_p1", StepStatus.RUNNING)
                    path_p1 = self._scarica_parte_prima(pdl_num)

                    path_p2 = None
                    if path_p1:
                        self.update_step("download_p1", StepStatus.COMPLETED)
                        self.update_step("download_p2", StepStatus.RUNNING)
                        path_p2 = self._scarica_parte_seconda(pdl_num)

                    if path_p1 and path_p2:
                        self.update_step("download_p2", StepStatus.COMPLETED)
                        self.update_step("merge", StepStatus.RUNNING)
                        if self._unisci_e_stampa(pdl_num, path_p1, path_p2, item, all_pdl_paths):
                            self.update_step("merge", StepStatus.COMPLETED)
                            success_count += 1
                        else:
                            self.update_step("merge", StepStatus.ERROR)
                    else:
                        if not path_p1:
                            self.update_step("download_p1", StepStatus.ERROR)
                        if not path_p2:
                            self.update_step("download_p2", StepStatus.ERROR)

                    self._safe_remove(path_p1)
                    self._safe_remove(path_p2)
                else:
                    self.update_step("search", StepStatus.ERROR)

                callback = getattr(self, "_progress_callback", None)
                if callback:
                    callback(index, True, "")
            except Exception as e:
                self.log(f"❌ Errore PDL {pdl_raw}: {e}")
                callback = getattr(self, "_progress_callback", None)
                if callback:
                    callback(index, False, str(e))

        self.update_step("session", StepStatus.RUNNING)
        self._handle_session_merge(data, all_pdl_paths)
        self.update_step("session", StepStatus.COMPLETED)

        return success_count == total

    def _sanitizza_pdl_number(self, pdl_raw: str) -> str:
        num = pdl_raw.strip().upper().replace(" ", "")
        if num.isdigit() and len(num) == MAX_PDL_DIGITS:
            suffix = "/S" if int(num) < PDL_THRESHOLD_NORTH_SOUTH else "/C"
            return f"{num}{suffix}"
        return num

    def _esegui_ricerca_pdl(self, pdl_num: str) -> bool:
        if not self.page:
            return False
        try:
            self._attendi_scomparsa_overlay()

            # Ricerca veloce
            self.page.fill("#txtRicercaVelocePdL", pdl_num)
            self.page.press("#txtRicercaVelocePdL", "Enter")

            if self._gestisci_ricerca_estesa():
                return False

            self._attendi_scomparsa_overlay()

            # Verifica caricamento
            self.page.wait_for_selector("#topIcon-acticonAnteprimaStampaMenu", state="visible", timeout=30000)
            return True
        except Exception as e:
            self.log(f"❌ Errore ricerca PDL {pdl_num}: {e}")
            return False

    def _gestisci_ricerca_estesa(self) -> bool:
        if not self.page:
            return False
        try:
            # Popup "estenderla?"
            popup_xpath = "//p[contains(text(), 'estenderla')]"
            if self.page.is_visible(f"xpath={popup_xpath}", timeout=5000):
                self.log("🖱️ Estensione ricerca...")
                self.page.click("span[idtxt='E421C594']")  # 'Si' button
                self._attendi_scomparsa_overlay()

                # Verifica se ancora nulla
                if self.page.is_visible("xpath=//div[contains(text(), 'nessun dato trovato')]", timeout=5000):
                    return True
            return False
        except Exception:
            return False

    def _scarica_parte_prima(self, pdl_num: str) -> str | None:
        if not self.page:
            return None
        try:
            self.page.click("#topIcon-acticonAnteprimaStampaMenu")

            with self.page.expect_download(timeout=60000) as download_info:
                self.page.click("#appItaliano")

            download = download_info.value
            dest = Path(self.download_path) / f"temp_p1_{int(time.time())}.pdf"
            download.save_as(str(dest))
            self._clean_pdf(str(dest))
            return str(dest)
        except Exception as e:
            self.log(f"❌ Errore scarico Parte Prima: {e}")
            return None

    def _scarica_parte_seconda(self, pdl_num: str) -> str | None:
        if not self.page:
            return None
        try:
            # Espandi Parte Seconda
            if not self.page.is_visible("#lblPAFoglio"):
                self.page.click("#lblTitoloParteSeconda")
                self.page.wait_for_selector("#lblPAFoglio", state="visible", timeout=10000)

            with self.page.expect_download(timeout=90000) as download_info:
                self.page.click("#btnPrintPS")
                # Gestione eventuale popup 'Stampa Tutte'
                with suppress(TimeoutError):
                    self.page.click("#rbStampaTutte", timeout=3000)
                    self.page.click("#btnAnteprima")

            download = download_info.value
            dest = Path(self.download_path) / f"temp_p2_{int(time.time())}.pdf"
            download.save_as(str(dest))
            return str(dest)
        except Exception as e:
            self.log(f"❌ Errore scarico Parte Seconda: {e}")
            return None

    def _clean_pdf(self, path: str) -> None:
        try:
            doc = fitz.open(path)
            if doc.page_count >= 2:  # noqa: PLR2004
                doc.delete_page(1)
                doc.save(path + ".tmp")
                doc.close()
                Path(path).unlink()
                Path(path + ".tmp").rename(path)
            else:
                doc.close()
        except Exception:
            pass

    def _unisci_e_stampa(
        self, pdl_num: str, p1: str, p2: str, item: dict[str, Any], all_paths: list[str]
    ) -> bool:
        nome = f"PDL_{pdl_num.replace('/', '-')}.pdf"
        output_dir = item.get("output_dir") or self.download_path
        out = Path(output_dir) / nome
        if DocumentProcessor.merge_pdfs([p1, p2], str(out)):
            self.downloaded_files.append(str(out))
            all_paths.append(str(out))
            if item.get("print_enabled") and item.get("printer_name"):
                print_pdf(str(out), item["printer_name"])
            return True
        return False

    def _handle_session_merge(self, data: list[dict[str, Any]], all_paths: list[str]) -> None:
        if any(i.get("merge_all_session") for i in data) and all_paths:
            try:
                ts = time.strftime("%d-%m-%Y_%H-%M")
                path_merge = Path(self.download_path) / f"PDL_SESSIONE_{ts}.pdf"
                if DocumentProcessor.merge_pdfs(all_paths, str(path_merge)):
                    self.log(f"✅ PDF Unico Sessione creato: {path_merge.name}")
                    self.downloaded_files.append(str(path_merge))
            except Exception:
                pass

    def _safe_remove(self, path: str | None) -> None:
        if path and Path(path).exists():
            with suppress(Exception):
                Path(path).unlink()
