"""
Bot per la prenotazione automatica dei Badge Provvisori (BP) sul Portale Fornitori ISAB.
"""

from datetime import UTC, datetime
from typing import Any, ClassVar

from src.bots.base.base_bot import StepStatus
from src.bots.base.selenium_base_bot import SeleniumBaseBot
from src.bots.base.selenium_bot_config import SeleniumBotConfig
from src.core.constants import Business
from src.core.logging import get_logger

from .pages.prenota_bp_page import PrenotaBPPage

logger = get_logger(__name__)


class PrenotaBPBot(SeleniumBaseBot):
    """Bot per la prenotazione massiva di Badge Provvisori (BP) sul Portale Fornitori."""

    STEPS: ClassVar[list[tuple[str, str]]] = [
        ("login", "Login Portale ISAB"),
        ("nav", "Navigazione Gestione BP"),
        ("filter", "Filtraggio Buoni"),
        ("details", "Apertura Dettagli"),
        ("reserve", "Prenotazione BP"),
        ("cleanup", "Chiusura Sessione"),
    ]

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        """Definisce le colonne richieste per l'input dei dati (Numero BP, Note)."""
        return [
            {"name": "numero_bp", "label": "Numero BP", "type": "text"},
            {"name": "note_ritiro", "label": "Note di Ritiro", "type": "text"},
        ]

    @property
    def name(self) -> str:
        """Restituisce l'ID del bot."""
        return "Prenota BP"

    @property
    def description(self) -> str:
        """Restituisce la descrizione del bot."""
        return "Prenotazione Badge Provvisori sul portale ISAB"

    def __init__(  # noqa: PLR0913
        self,
        username: str | None = None,
        password: str | None = None,
        config: SeleniumBotConfig | None = None,
        data_da: str | None = None,
        data_a: str | None = None,
        fornitore: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Inizializza il bot Prenota BP."""
        super().__init__(username, password, config)
        current_year = datetime.now(UTC).astimezone().year
        self.data_da = data_da or kwargs.get("data_da") or f"01.01.{current_year}"
        self.data_a = data_a or kwargs.get("data_a") or f"31.12.{current_year}"
        self.fornitore = fornitore or kwargs.get("fornitore") or Business.DEFAULT_SUPPLIER
        self.results: list[dict[str, Any]] = []

    def _get_row_value(self, row: dict[str, Any], target_key: str) -> str:
        """Estrae un valore dalla riga in modo robusto (ignora case, spazi e underscore)."""

        def normalize(s: Any) -> str:
            return str(s).strip().lower().replace(" ", "").replace("_", "")

        target_norm = normalize(target_key)
        for k, v in row.items():
            if normalize(k) == target_norm:
                return str(v).strip()
        return ""

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Verifica la presenza dei dati necessari (numero_bp)."""
        base_ok, base_msg = super().validate_data(data)
        if not base_ok:
            return False, base_msg

        rows = data.get("rows", []) if isinstance(data, dict) else data
        if not rows:
            return False, "Nessun dato fornito."

        for i, row in enumerate(rows):
            if not self._get_row_value(row, "numero_bp"):
                return False, f"Numero BP mancante alla riga {i + 1}"

        return True, ""

    def run(self, data: list[dict[str, Any]]) -> bool:
        """Esegue il workflow di prenotazione BP."""
        self.update_step("login", StepStatus.COMPLETED)

        if not self.driver:
            self.log("❌ Driver non inizializzato")
            return False

        try:
            self.update_step("nav", StepStatus.RUNNING)
            page = PrenotaBPPage(self.driver, self.log)
            try:
                page.navigate_to_gestione_bp()
            except Exception as e:
                self.log(f"❌ Impossibile raggiungere la sezione Gestione BP: {e}")
                self.update_step("nav", StepStatus.ERROR)
                return False
            self.update_step("nav", StepStatus.COMPLETED)

            # 2. Ciclo di prenotazione per ogni riga
            success_count = 0
            for i, row in enumerate(data):
                self._check_stop()
                try:
                    if self._process_single_bp(page, row, i):
                        success_count += 1
                except Exception as e:
                    self.log(f"❌ Errore riga {i + 1}: {e}")
                    if callback := getattr(self, "_progress_callback", None):
                        callback(i, False, str(e))

            self.update_step("cleanup", StepStatus.RUNNING)
            self.log(f"ℹ️ Fine: {success_count}/{len(data)} BP processati.")
            self.update_step("cleanup", StepStatus.COMPLETED)
            return success_count == len(data)

        except Exception as e:
            self.log(f"❌ Errore fatale Prenota BP: {e}")
            logger.exception("PrenotaBP Critical Error")
            return False

    def _process_single_bp(self, page: PrenotaBPPage, row: dict[str, Any], index: int) -> bool:
        """Gestisce la prenotazione di un singolo BP."""
        num_bp = self._get_row_value(row, "numero_bp")
        note = self._get_row_value(row, "note_ritiro") or "Ritiro c/o Portineria"

        self.log(f"🔄 Elaborazione BP: {num_bp}...")

        # 1. Filtro
        self.update_step("filter", StepStatus.RUNNING)
        try:
            page.filtra_buoni_prelievo(self.fornitore, num_bp, self.data_da, self.data_a)
        except Exception as e:
            self.log(f"⚠️ Buono {num_bp} non trovato o errore filtro: {e}")
            self.update_step("filter", StepStatus.ERROR)
            return False
        self.update_step("filter", StepStatus.COMPLETED)

        # 2. Apertura Dettaglio
        self.update_step("details", StepStatus.RUNNING)
        try:
            page.apri_dettagli_bp()
        except Exception as e:
            self.log(f"⚠️ Impossibile aprire dettaglio per {num_bp}: {e}")
            self.update_step("details", StepStatus.ERROR)
            return False
        self.update_step("details", StepStatus.COMPLETED)

        # 3. Prenotazione
        self.update_step("reserve", StepStatus.RUNNING)
        try:
            page.gestisci_creazione_richiesta(note)
            success, msg = True, "Prenotazione creata con successo."
        except Exception as e:
            success, msg = False, str(e)

        if success:
            self.log(f"✅ BP {num_bp} prenotato con successo.")
            self.update_step("reserve", StepStatus.COMPLETED)
        else:
            self.log(f"❌ Errore prenotazione {num_bp}: {msg}")
            self.update_step("reserve", StepStatus.ERROR)

        # Notifica progresso
        if callback := getattr(self, "_progress_callback", None):
            callback(index, success, msg)

        return success
