"""
SyncroJob - Certificati Engine
Motore di business per il calcolo delle scadenze, ricerca file e gestione esclusioni.
"""

import json
import os
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Final, TypedDict

from src.core import config_manager
from src.core.constants import Icons, StatoCertificatoLabel, UbicazioneStrumenti
from src.core.paths import DB_DIR


class CertificatiStats(TypedDict):
    """Statistiche aggregate dei certificati."""

    attivi: int
    in_scadenza: int
    scaduti: int
    senza_data: int
    guasti: int
    ufficio_stru: int
    ufficio_cc: int
    officina: int
    sede: int
    tecnico: int
    assenti: int
    totale: int
    prossime_tarature: dict[str, int]
    picco_imminente: dict[str, Any]


class CertificatiEngine:
    """Motore logico per la gestione dei certificati campione."""

    # Costanti per il calcolo delle scadenze
    WARNING_THRESHOLD: Final[int] = 15
    EXPIRING_THRESHOLD: Final[int] = 30
    FAULTY_MARKER: Final[int] = -9999

    # Indici colonne dati certificati
    IDX_CERTIFICATO: Final[int] = 1
    IDX_MATRICOLA: Final[int] = 4
    IDX_EMISSIONE: Final[int] = 7
    IDX_SCADENZA: Final[int] = 8
    IDX_UBICAZIONE: Final[int] = 10

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
            return f"❌ {StatoCertificatoLabel.GUASTO}"
        if days is None:
            return StatoCertificatoLabel.SENZA_SCADENZA
        if days < 0:
            return f"❌ {StatoCertificatoLabel.SCADUTO} ({abs(days)}gg fa)"
        if days <= cls.WARNING_THRESHOLD:
            return f"[ARANCIONE] {StatoCertificatoLabel.IN_SCADENZA} ({days}gg)"
        if days <= cls.EXPIRING_THRESHOLD:
            return f"[GIALLO] {StatoCertificatoLabel.IN_SCADENZA} ({days}gg)"
        return f"✅ {StatoCertificatoLabel.ATTIVO} ({days}gg rim.)"

    @classmethod
    def get_statistics(cls, data: list[Any]) -> dict[str, Any]:
        """Calcola le statistiche aggregate per un set di dati certificati."""
        stats: dict[str, Any] = {
            "attivi": 0,
            "in_scadenza": 0,
            "scaduti": 0,
            "senza_data": 0,
            "guasti": 0,
            "ufficio_stru": 0,
            "ufficio_cc": 0,
            "officina": 0,
            "sede": 0,
            "tecnico": 0,
            "assenti": 0,
            "totale": 0,
            "prossime_tarature": {"30": 0, "60": 0, "90": 0, "oltre": 0},
            "picco_imminente": {},
        }
        expiration_map: dict[datetime, int] = {}

        for r in data:
            stats["totale"] += 1
            scadenza_str = str(r[cls.IDX_SCADENZA]) if len(r) > cls.IDX_SCADENZA else ""
            days, _ = cls.calculate_days_and_status(scadenza_str)

            cls._process_status_stats(stats, days, scadenza_str, expiration_map)
            cls._process_location_stats(stats, r)

        cls._analyze_bottlenecks(stats, expiration_map)
        return stats

    @classmethod
    def _process_status_stats(
        cls, stats: dict[str, Any], days: int | None, scadenza_str: str, expiration_map: dict[datetime, int]
    ) -> None:
        """Aggiorna i conteggia'di stato e mappa le scadenze temporali."""
        if days == cls.FAULTY_MARKER:
            stats["guasti"] += 1
        elif days is None:
            stats["senza_data"] += 1
        elif days < 0:
            stats["scaduti"] += 1
        elif days <= cls.EXPIRING_THRESHOLD:
            stats["in_scadenza"] += 1
        else:
            stats["attivi"] += 1

        if days is not None and days >= 0:
            cls._update_timer_buckets(stats, days)
            with suppress(Exception):
                dt = datetime.strptime(scadenza_str, "%d/%m/%Y").replace(
                    hour=0, minute=0, second=0, microsecond=0, tzinfo=UTC
                )
                expiration_map[dt] = expiration_map.get(dt, 0) + 1

    @classmethod
    def _update_timer_buckets(cls, stats: dict[str, Any], days: int) -> None:
        """Incrementa i bucket temporali per le tarature future."""
        limit_30, limit_60, limit_90 = 30, 60, 90
        if days <= limit_30:
            stats["prossime_tarature"]["30"] += 1
        elif days <= limit_60:
            stats["prossime_tarature"]["60"] += 1
        elif days <= limit_90:
            stats["prossime_tarature"]["90"] += 1
        else:
            stats["prossime_tarature"]["oltre"] += 1

    @classmethod
    def _process_location_stats(cls, stats: dict[str, Any], record: Any) -> None:
        """Aggiorna i conteggia'basati sull'ubicazione fisica degli strumenti."""
        ubicazione = str(record[cls.IDX_UBICAZIONE]).upper() if len(record) > cls.IDX_UBICAZIONE else ""
        if UbicazioneStrumenti.UFFICIO_STRU.value in ubicazione:
            stats["ufficio_stru"] += 1
        elif UbicazioneStrumenti.UFFICIO_CC.value in ubicazione:
            stats["ufficio_cc"] += 1
        elif UbicazioneStrumenti.OFFICINA.value in ubicazione:
            stats["officina"] += 1
        elif UbicazioneStrumenti.SEDE.value in ubicazione:
            stats["sede"] += 1
        elif "TECNICO" in ubicazione:
            stats["tecnico"] += 1
        elif UbicazioneStrumenti.ASSENTE.value in ubicazione:
            stats["assenti"] += 1

    @classmethod
    def _analyze_bottlenecks(cls, stats: dict[str, Any], expiration_map: dict[datetime, int]) -> None:
        """Identifica picchi di scadenze in finestre mobili di 5 giorni."""
        if not expiration_map:
            return

        sorted_dates = sorted(expiration_map.keys())
        max_count = 0
        best_window: tuple[datetime | None, datetime | None] = (None, None)
        window_size_days = 5

        for i, start_date in enumerate(sorted_dates):
            current_count = 0
            end_window = start_date + timedelta(days=window_size_days)
            for j in range(i, len(sorted_dates)):
                if sorted_dates[j] <= end_window:
                    current_count += expiration_map[sorted_dates[j]]
                else:
                    break

            if current_count > max_count:
                max_count = current_count
                best_window = (start_date, end_window)

        if max_count > 0 and best_window[0] and best_window[1]:
            stats["picco_imminente"] = {
                "count": max_count,
                "inizio": best_window[0].strftime("%d/%m"),
                "fine": best_window[1].strftime("%d/%m/%Y"),
            }

    @staticmethod
    def format_errore_max(val: float | str | None) -> str:
        """Formatta il valore decimale di errore in percentuale localizzata."""
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
        parts = text.split("    ")
        idx_mat, idx_cos, idx_mod, idx_range = 0, 1, 2, 3
        return {
            "matricola": parts[idx_mat].strip() if len(parts) > idx_mat else "",
            "costruttore": parts[idx_cos].strip() if len(parts) > idx_cos else "N/D",
            "modello": parts[idx_mod].strip() if len(parts) > idx_mod else "N/D",
            "range": parts[idx_range].strip()
            if len(parts) > idx_range and "Digital" in parts[idx_mod]
            else "",
        }
