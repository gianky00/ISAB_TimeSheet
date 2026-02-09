import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar

from src.core.config_manager import CONFIG_DIR

logger = logging.getLogger(__name__)


class SyncTracker:
    """
    Gestisce la persistenza dello stato di sincronizzazione (Ultimo aggiornamento, Diff).
    Salva i dati in un file JSON per persistenza tra riavvii.
    """

    STATE_FILE: ClassVar[Path] = CONFIG_DIR / "data" / "sync_state.json"
    _cache: ClassVar[dict[str, Any]] = {}
    _loaded = False

    @classmethod
    def _load(cls) -> None:
        """Carica lo stato dal file JSON."""
        if cls._loaded:
            return

        if cls.STATE_FILE.exists():
            try:
                cls._cache = json.loads(cls.STATE_FILE.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Errore caricamento sync state: {e}")
                cls._cache = {}
        else:
            cls._cache, cls._loaded = {}, True
            return

        cls._loaded = True

    @classmethod
    def _save(cls) -> None:
        """Salva lo stato su file JSON."""
        try:
            cls.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            cls.STATE_FILE.write_text(json.dumps(cls._cache, indent=4), encoding="utf-8")
        except Exception as e:
            logger.error(f"Errore salvataggio sync state: {e}")

    @classmethod
    def update_status(cls, module: str, added: int, removed: int, duration: float = 0.0) -> None:
        """
        Aggiorna lo stato di sincronizzazione per un modulo.

        Args:
            module: Chiave identificativa (es. 'pdl', 'dipendenti', 'storico_oda')
            added: Numero righe aggiunte/aggiornate
            removed: Numero righe rimosse
            duration: Tempo impiegato in secondi
        """
        cls._load()

        timestamp_str = datetime.now().strftime("%d/%m/%Y %H:%M")

        cls._cache[module] = {
            "timestamp": timestamp_str,
            "added": added,
            "removed": removed,
            "duration": duration,
            "last_ts": time.time(),  # Timestamp numerico per ordinamento/confronto
        }

        cls._save()

    @classmethod
    def get_status(cls, module: str) -> dict[str, Any]:
        """Restituisce lo stato salvato per il modulo, o un dict vuoto se assente."""
        cls._load()
        return cls._cache.get(module, {})  # type: ignore[no-any-return]

    @classmethod
    def get_formatted_status(cls, module: str) -> str:
        """
        Restituisce una stringa formattata per la UI.
        Es: "30/01/2026 14:00 +1 -5 (Tempo: 2.5s)"
        """
        data = cls.get_status(module)
        if not data:
            return "Mai sincronizzato"

        timestamp = data.get("timestamp", "N/A")
        added = data.get("added", 0)
        removed = data.get("removed", 0)
        duration = data.get("duration", 0.0)

        added_str = f"<font color='green'><b>+{added}</b></font>"
        removed_str = f"<font color='red'><b>-{removed}</b></font>"

        if duration < 60:
            time_str = f"{duration:.1f}s"
        else:
            m, s = divmod(int(duration), 60)
            time_str = f"{m}m {s}s"

        return f"{timestamp} {added_str} {removed_str} (Tempo: {time_str})"
