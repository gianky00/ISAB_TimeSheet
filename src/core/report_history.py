"""
Gestione storico dei report email per calcolo trend e confronti.

Salva snapshot di ogni report inviato e permette il confronto con il precedente.
"""

import json
import logging
from datetime import UTC, datetime
from typing import Any

from src.core.config_manager import CONFIG_DIR
from src.core.constants import FileNames

logger = logging.getLogger(__name__)


class ReportHistory:
    """Gestisce lo storico dei report email per il calcolo dei trend."""

    HISTORY_FILE = CONFIG_DIR / "data" / FileNames.REPORT_HISTORY
    MAX_HISTORY_ENTRIES = 30  # Mantieni ultimi 30 report

    @classmethod
    def _ensure_file(cls) -> None:
        """Assicura che il file e la directory esistano."""
        cls.HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not cls.HISTORY_FILE.exists():
            cls.HISTORY_FILE.write_text(
                json.dumps({"last_report": None, "history": []}, indent=2),
                encoding="utf-8",
            )

    @classmethod
    def _load_data(cls) -> dict[str, Any]:
        """Carica i dati dallo storico."""
        cls._ensure_file()
        try:
            data: dict[str, Any] = json.loads(cls.HISTORY_FILE.read_text(encoding="utf-8"))
            return data  # noqa: TRY300
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.warning(f"Errore caricamento storico report: {e}")
            return {"last_report": None, "history": []}

    @classmethod
    def _save_data(cls, data: dict[str, Any]) -> None:
        """Salva i dati nello storico."""
        cls._ensure_file()
        try:
            cls.HISTORY_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            logger.error(f"Errore salvataggio storico report: {e}")  # noqa: TRY400

    @classmethod
    def save_report(cls, warning_list: list[dict[str, Any]], expired_list: list[dict[str, Any]]) -> None:
        """
        Salva snapshot del report corrente.

        Args:
            warning_list: Lista dipendenti in scadenza (21-30 gg)
            expired_list: Lista dipendenti scaduti (>30 gg)
        """
        data = cls._load_data()

        # Estrai ID dipendenti per confronto successivo
        warning_ids = [str(d.get("id", d.get("badge", ""))) for d in warning_list]
        expired_ids = [str(d.get("id", d.get("badge", ""))) for d in expired_list]

        new_report = {
            "date": datetime.now(UTC).isoformat(),
            "warning_count": len(warning_list),
            "expired_count": len(expired_list),
            "warning_ids": warning_ids,
            "expired_ids": expired_ids,
        }

        # Sposta il report corrente nello storico
        if data.get("last_report"):
            data["history"].insert(0, data["last_report"])
            # Mantieni solo gli ultimi N report
            data["history"] = data["history"][: cls.MAX_HISTORY_ENTRIES]

        # Aggiorna last_report
        data["last_report"] = new_report

        cls._save_data(data)
        logger.info(f"Report salvato: {len(warning_list)} warning, {len(expired_list)} expired")

    @classmethod
    def get_last_report(cls) -> dict[str, Any] | None:
        """
        Recupera l'ultimo report salvato.

        Returns:
            Dict con i dati dell'ultimo report, o None se non esiste.
        """
        return cls._load_data().get("last_report")

    @classmethod
    def calculate_trend(cls, current_warning: int, current_expired: int) -> dict[str, Any] | None:
        """
        Calcola la differenza con il report precedente.

        Args:
            current_warning: Numero attuale di dipendenti in scadenza
            current_expired: Numero attuale di dipendenti scaduti

        Returns:
            Dict con:
                - warning_diff: Differenza warning (+2, -1, ecc.)
                - expired_diff: Differenza scaduti
                - last_date: Data ultimo report formattata
            None se non esiste un report precedente.
        """
        last_report = cls.get_last_report()
        if not last_report:
            return None

        try:
            last_date = datetime.fromisoformat(last_report["date"])
            last_date_str = last_date.strftime("%d/%m/%Y")

            warning_diff = current_warning - last_report.get("warning_count", 0)
            expired_diff = current_expired - last_report.get("expired_count", 0)

            return {
                "warning_diff": warning_diff,
                "expired_diff": expired_diff,
                "last_date": last_date_str,
                "last_warning_count": last_report.get("warning_count", 0),
                "last_expired_count": last_report.get("expired_count", 0),
            }
        except Exception as e:
            logger.error(f"Errore calcolo trend: {e}")  # noqa: TRY400
            return None

    @classmethod
    def get_history(cls, limit: int = 10) -> list[dict[str, Any]]:
        """
        Recupera lo storico degli ultimi N report.

        Args:
            limit: Numero massimo di report da recuperare

        Returns:
            Lista di report storici ordinati per data (dal più recente)
        """
        data = cls._load_data()
        history: list[dict[str, Any]] = []

        # Aggiungi last_report se esiste
        if data.get("last_report"):
            history.append(data["last_report"])

        # Aggiungi lo storico
        history.extend(data.get("history", []))

        return history[:limit]
