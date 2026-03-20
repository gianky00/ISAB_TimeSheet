"""
SyncroJob - Certificati Engine
Motore di business per il calcolo delle scadenze, ricerca file e gestione esclusioni.
"""

import json
import os
from datetime import UTC, datetime
from pathlib import Path

from src.core import config_manager
from src.core.config_manager import CONFIG_DIR
from src.core.constants import Icons


class CertificatiEngine:
    """Motore logico per la gestione dei certificati campione."""

    EXCLUSIONS_FILE: Path = CONFIG_DIR / "data" / "certificati_exclusions.json"

    def __init__(self):
        self._exclusions: set[str] = set()
        self._print_exclusions: set[str] = set()
        self.load_exclusions()

    def load_exclusions(self) -> set[str]:
        """Carica le matricole escluse dal monitoraggio e dalla stampa."""
        try:
            if self.EXCLUSIONS_FILE.exists():
                with self.EXCLUSIONS_FILE.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._exclusions = {str(x).strip() for x in data.get("excluded_matricole", [])}
                    self._print_exclusions = {
                        str(x).strip() for x in data.get("print_excluded_matricole", [])
                    }
        except Exception:
            self._exclusions = set()
            self._print_exclusions = set()
        return self._exclusions

    def save_exclusions(
        self, exclusions: set[str] | None = None, print_exclusions: set[str] | None = None
    ) -> bool:
        """Salva le matricole escluse su disco."""
        try:
            if exclusions is not None:
                self._exclusions = exclusions
            if print_exclusions is not None:
                self._print_exclusions = print_exclusions

            self.EXCLUSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with self.EXCLUSIONS_FILE.open("w", encoding="utf-8") as f:
                json.dump(
                    {
                        "excluded_matricole": list(self._exclusions),
                        "print_excluded_matricole": list(self._print_exclusions),
                    },
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
            return True
        except Exception:
            return False

    @staticmethod
    def calculate_days_and_status(scadenza_str: str) -> tuple[int | None, str]:
        """
        Calcola i giorni alla scadenza e determina l'icona di stato.
        Returns: (giorni_alla_scadenza, icona_pallino)
        """
        if not scadenza_str:
            return None, Icons.STATUS_DOT_GRAY

        if "GUASTO" in scadenza_str.upper():
            return -9999, Icons.STATUS_DOT_RED

        try:
            scadenza_date = datetime.strptime(scadenza_str, "%d/%m/%Y").replace(tzinfo=UTC)
            today = datetime.now(UTC)
            delta = scadenza_date - today
            days = delta.days

            if days < 0:
                return days, Icons.STATUS_DOT_RED
            if 0 <= days <= 15:
                return days, Icons.STATUS_DOT_ORANGE
            if 16 <= days <= 30:
                return days, Icons.STATUS_DOT_YELLOW

            return days, Icons.STATUS_DOT_GREEN
        except Exception:
            return None, Icons.STATUS_DOT_GRAY

    @staticmethod
    def format_days_text_short(days: int | None) -> str:
        """Ritorna una rappresentazione testuale breve dello stato scadenze."""
        if days == -9999:
            return "❌ STRUMENTO GUASTO"
        if days is None:
            return "N/D"
        if days < 0:
            return f"🔴 Scaduto ({abs(days)}gg fa)"
        if 0 <= days <= 15:
            return f"🟠 Scade tra {days}gg"
        if 16 <= days <= 30:
            return f"🟡 Scade tra {days}gg"
        return f"✅ Attivo ({days}gg rim.)"

    @staticmethod
    def format_errore_max(val: float | str | None) -> str:
        """Formatta il valore decimale di errore in percentuale localizzata (es. 0.0005 -> 0,05%)."""
        if val is None or val == "":
            return ""
        try:
            f_val = float(val)
            # Moltiplichiamo per 100 per avere la percentuale
            perc = f_val * 100
            # Formattiamo con virgola come separatore decimale, rimuovendo ,00 se superfluo
            res = f"{perc:.4f}".rstrip(".0").replace(".", ",")
            return f"{res}%" if res else "0%"
        except (ValueError, TypeError):
            return str(val)

    @staticmethod
    def find_certificate_path(cert_number: str) -> str | None:
        """Cerca il file PDF del certificato nel server in modo ricorsivo."""
        cert_root = config_manager.load_config().get("certificati_root_path", "")
        if not cert_root or not Path(cert_root).exists():
            return None

        search_patterns = [
            f"{cert_number}.pdf",
            f"{cert_number}.PDF",
            f"CERTIFICATO {cert_number}.pdf",
            f"certificato {cert_number}.pdf",
        ]

        for root, _, files in os.walk(cert_root):
            for file in files:
                # Match esatto o parziale intelligente
                is_match = any(file.lower() == p.lower() for p in search_patterns)
                is_partial = cert_number.lower() in file.lower() and file.lower().endswith(".pdf")
                if is_match or is_partial:
                    return str(os.path.join(root, file))
        return None

    @staticmethod
    def parse_parent_label(text: str) -> dict[str, str]:
        """Estrae i metadati dalla stringa del nodo padre del TreeWidget."""
        parts = text.split("  •  ")
        return {
            "matricola": parts[0].strip() if parts else "",
            "costruttore": parts[1].strip() if len(parts) > 1 else "N/D",
            "modello": parts[2].strip() if len(parts) > 2 else "N/D",
            "range": parts[3].strip() if len(parts) > 3 and "Digital" in parts[2] else "",
        }
