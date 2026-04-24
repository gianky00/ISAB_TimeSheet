"""
SyncroJob - Certificati Engine
Motore di business per il calcolo delle scadenze, ricerca file e gestione esclusioni.
"""

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Final

from src.core import config_manager
from src.core.constants import Icons, StatoCertificatoLabel, UbicazioneStrumenti
from src.core.paths import DB_DIR


class CertificatiEngine:
    """Motore logico per la gestione dei certificati campione."""

    # Costanti per il calcolo delle scadenze
    WARNING_THRESHOLD: Final[int] = 15
    EXPIRING_THRESHOLD: Final[int] = 30
    FAULTY_MARKER: Final[int] = -9999

    @property
    def exclusions_file(self) -> Path:
        """Restituisce il percorso dinamico del file delle esclusioni."""
        return DB_DIR / "certificati_exclusions.json"

    def __init__(self) -> None:
        self._exclusions: set[str] = set()
        self._print_exclusions: set[str] = set()
        self.load_exclusions()

    def load_exclusions(self) -> set[str]:
        """Carica le matricole escluse dal monitoraggio e dalla stampa."""
        try:
            if self.exclusions_file.exists():
                with self.exclusions_file.open("r", encoding="utf-8") as f:
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

            self.exclusions_file.parent.mkdir(parents=True, exist_ok=True)
            with self.exclusions_file.open("w", encoding="utf-8") as f:
                json.dump(
                    {
                        "excluded_matricole": list(self._exclusions),
                        "print_excluded_matricole": list(self._print_exclusions),
                    },
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
        except Exception:
            return False
        else:
            return True

    @classmethod
    def calculate_days_and_status(cls, scadenza_str: str) -> tuple[int | None, str]:
        """
        Calcola i giorni alla scadenza e determina l'icona di stato.
        Returns: (giorni_alla_scadenza, icona_pallino)
        """
        if not scadenza_str:
            return None, Icons.STATUS_DOT_GRAY

        if "GUASTO" in scadenza_str.upper():
            return cls.FAULTY_MARKER, Icons.STATUS_DOT_RED

        try:
            scadenza_date = datetime.strptime(scadenza_str, "%d/%m/%Y").replace(tzinfo=UTC)
            today = datetime.now(UTC)
            delta = scadenza_date - today
            days = delta.days

            return days, cls._get_status_icon(days)
        except Exception:
            return None, Icons.STATUS_DOT_GRAY

    @classmethod
    def _get_status_icon(cls, days: int) -> str:
        """Determina l'icona basandosi sui giorni rimasti."""
        if days < 0:
            return Icons.STATUS_DOT_RED
        if days <= cls.WARNING_THRESHOLD:
            return Icons.STATUS_DOT_ORANGE
        if days <= cls.EXPIRING_THRESHOLD:
            return Icons.STATUS_DOT_YELLOW
        return Icons.STATUS_DOT_GREEN

    @classmethod
    def format_days_text_short(cls, days: int | None) -> str:
        """Ritorna una rappresentazione testuale breve dello stato scadenze."""
        if days == cls.FAULTY_MARKER:
            return f"[ERRORE] {StatoCertificatoLabel.GUASTO}"
        if days is None:
            return StatoCertificatoLabel.SENZA_SCADENZA
        if days < 0:
            return f"[ROSSO] {StatoCertificatoLabel.SCADUTO} ({abs(days)}gg fa)"
        if days <= cls.WARNING_THRESHOLD:
            return f"[ARANCIONE] {StatoCertificatoLabel.IN_SCADENZA} ({days}gg)"
        if days <= cls.EXPIRING_THRESHOLD:
            return f"[GIALLO] {StatoCertificatoLabel.IN_SCADENZA} ({days}gg)"
        return f"[OK] {StatoCertificatoLabel.ATTIVO} ({days}gg rim.)"

    @classmethod
    def get_statistics(cls, data: list[Any]) -> dict[str, int]:
        """
        Calcola le statistiche aggregate per un set di dati certificati.
        Args:
            data: Lista di tuple/record (formato ContabilitaQueries)
        """
        stats = {
            "attivi": 0,
            "in_scadenza": 0,
            "scaduti": 0,
            "senza_data": 0,
            "guasti": 0,
            "ufficio_stru": 0,
            "ufficio_cc": 0,
            "officina": 0,
            "tecnico": 0,
            "assenti": 0,
            "totale": 0,
        }

        for r in data:
            stats["totale"] += 1
            # Indice scadenza: 8, Ubicazione: 10
            scadenza_str = str(r[8]) if len(r) > 8 else ""
            days, _ = cls.calculate_days_and_status(scadenza_str)

            if days == cls.FAULTY_MARKER:
                stats["guasti"] += 1
            elif days is None:
                stats["senza_data"] += 1
            elif days < 0:
                stats["scaduti"] += 1
            elif 0 <= days <= cls.EXPIRING_THRESHOLD:
                stats["in_scadenza"] += 1
            else:
                stats["attivi"] += 1

            ubicazione = str(r[10]).upper() if len(r) > 10 else ""
            if UbicazioneStrumenti.UFFICIO_STRU.value in ubicazione:
                stats["ufficio_stru"] += 1
            elif UbicazioneStrumenti.UFFICIO_CC.value in ubicazione:
                stats["ufficio_cc"] += 1
            elif UbicazioneStrumenti.OFFICINA.value in ubicazione:
                stats["officina"] += 1
            elif UbicazioneStrumenti.TECNICO.value in ubicazione:
                stats["tecnico"] += 1
            elif UbicazioneStrumenti.ASSENTE.value in ubicazione:
                stats["assenti"] += 1

        return stats

    @staticmethod
    def format_errore_max(val: float | str | None) -> str:
        """Formatta il valore decimale di errore in percentuale localizzata (es. 0.0005 -> 0,05%)."""
        if val is None or val == "":
            return ""
        try:
            f_val = float(val)
            perc = f_val * 100
            res = f"{perc:.4f}".rstrip(".0").replace(".", ",")
        except (ValueError, TypeError):
            return str(val)
        else:
            return f"{res}%" if res else "0%"

    @staticmethod
    def find_certificate_path(cert_number: str) -> str | None:
        """Cerca il file PDF del certificato nel server in modo ricorsivo."""
        cert_root = config_manager.get_config_value("certificati_root_path", "")
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
            "modello": parts[2].strip() if len(parts) > 2 else "N/D",  # noqa: PLR2004
            "range": parts[3].strip() if len(parts) > 3 and "Digital" in parts[2] else "",  # noqa: PLR2004
        }
