"""SyncroJob - Sync Tracker.

Modulo per il monitoraggio e la persistenza dello stato di sincronizzazione dei database.
Traccia timestamp, numero di record aggiunti/rimossi e tempi di esecuzione per ogni operazione di importazione dati.
Permette di visualizzare nella UI lo stato dell'ultimo aggiornamento (es. PDL, Dipendenti, OdA).
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, Final

from src.core.constants import FileNames
from src.core.paths import DB_DIR

logger = logging.getLogger(__name__)


class SyncTracker:
    """Gestore dello stato di sincronizzazione globale.

    Utilizza un file JSON per mantenere la persistenza tra i riavvii dell'applicazione.
    Fornisce metodi statici per aggiornare e recuperare i metadati delle operazioni di sync.
    """

    STATE_FILE: Final[Path] = DB_DIR / FileNames.SYNC_STATE
    SECONDS_IN_MINUTE: Final[int] = 60

    _cache: ClassVar[dict[str, Any]] = {}
    """Cache interna per evitare letture ridondanti da disco."""

    _loaded: ClassVar[bool] = False
    """Flag per indicare se lo stato  già stato caricato in memoria."""

    @classmethod
    def _load(cls) -> None:
        """Carica lo stato dal file JSON se non già presente nella cache interna."""
        if cls._loaded:
            return
        if cls.STATE_FILE.exists():
            try:
                cls._cache = json.loads(cls.STATE_FILE.read_text(encoding="utf-8"))
            except Exception:
                logger.exception("Errore caricamento sync state")
                cls._cache = {}
        else:
            cls._cache, cls._loaded = {}, True
            return
        cls._loaded = True

    @classmethod
    def _save(cls) -> None:
        """Sincronizza lo stato in cache con il file JSON su disco."""
        try:
            cls.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            cls.STATE_FILE.write_text(json.dumps(cls._cache, indent=4), encoding="utf-8")
        except Exception:
            logger.exception("Errore salvataggio sync state")

    @classmethod
    def update_status(cls, module: str, added: int, removed: int, duration: float = 0.0) -> None:
        """Registra l'avvenuta sincronizzazione con successo di un modulo specifico.

        Args:
          module: Identificativo del modulo (es. 'pdl', 'dipendenti', 'storico_oda').
          added: Numero di record inseriti o aggiornati durante l'operazione.
          removed: Numero di record eliminati (non più presenti nella sorgente).
          duration: Tempo totale impiegato per la sincronizzazione (secondi).
        """
        cls._load()
        now = time.time()
        timestamp_str = datetime.fromtimestamp(now).astimezone().strftime("%d/%m/%Y %H:%M")
        cls._cache[module] = {
            "timestamp": timestamp_str,
            "added": added,
            "removed": removed,
            "duration": duration,
            "last_ts": now,
            "last_attempt_success": True,
            "last_attempt_ts": now,
            "last_error": "",
        }
        cls._save()

    @classmethod
    def mark_start(cls, module: str) -> None:
        """Segnala l'inizio di un tentativo di sincronizzazione."""
        cls._load()
        if module not in cls._cache:
            cls._cache[module] = {
                "timestamp": "Mai",
                "added": 0,
                "removed": 0,
                "duration": 0,
                "last_ts": 0,
            }
        cls._cache[module]["last_attempt_success"] = None
        cls._cache[module]["last_attempt_ts"] = time.time()
        cls._save()

    @classmethod
    def mark_failure(cls, module: str, error: str = "") -> None:
        """Registra il fallimento dell'ultimo tentativo di sincronizzazione."""
        cls._load()
        if module not in cls._cache:
            cls._cache[module] = {
                "timestamp": "Mai",
                "added": 0,
                "removed": 0,
                "duration": 0,
                "last_ts": 0,
            }
        cls._cache[module]["last_attempt_success"] = False
        cls._cache[module]["last_attempt_ts"] = time.time()
        cls._cache[module]["last_error"] = error
        cls._save()

    @classmethod
    def get_status(cls, module: str) -> dict[str, Any]:
        """Recupera i dati dell'ultima sincronizzazione per un determinato modulo.

        Args:
          module: Nome del modulo da interrogare.

        Returns:
          dict: Dizionario con timestamp, record aggiunti, rimossi e durata.
        """
        cls._load()
        result: dict[str, Any] = cls._cache.get(module, {})
        return result

    @classmethod
    def get_formatted_status(cls, module: str) -> str:
        """Restituisce una rappresentazione testuale formattata in HTML per la UI.

        Esempio: "30/01/2026 14:00 +1 -5 (Tempo: 2.5s)".

        Args:
          module: Nome del modulo.

        Returns:
          str: Stringa formattata pronta per essere visualizzata in un QLabel.
        """
        data = cls.get_status(module)
        if not data:
            return "Mai sincronizzato"

        timestamp = data.get("timestamp", "N/A")
        added, removed = data.get("added", 0), data.get("removed", 0)
        duration = data.get("duration", 0.0)

        added_str = f"<font color='green'><b>+{added}</b></font>"
        removed_str = f"<font color='red'><b>-{removed}</b></font>"

        if duration < cls.SECONDS_IN_MINUTE:
            time_str = f"{duration:.1f}s"
        else:
            time_str = f"{int(duration // cls.SECONDS_IN_MINUTE)}m {int(duration % cls.SECONDS_IN_MINUTE)}s"

        return f"{timestamp} {added_str} {removed_str} (Tempo: {time_str})"
