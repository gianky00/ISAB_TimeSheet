"""
SyncroJob - Sync Tracker
Modulo per il monitoraggio e la persistenza dello stato di sincronizzazione dei database.
Traccia timestamp, numero di record aggiunti/rimossi e tempi di esecuzione per ogni operazione di importazione dati.
Permette di visualizzare nella UI lo stato dell'ultimo aggiornamento (es. PDL, Dipendenti, OdA).
"""

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
    Gestore dello stato di sincronizzazione globale.
    Utilizza un file JSON per mantenere la persistenza tra i riavvii dell'applicazione.
    Fornisce metodi statici per aggiornare e recuperare i metadati delle operazioni di sync.
    """

    STATE_FILE: ClassVar[Path] = CONFIG_DIR / "data" / "sync_state.json"
    """Percorso del file JSON contenente lo stato di sincronizzazione."""

    _cache: ClassVar[dict[str, Any]] = {}
    """Cache interna per evitare letture ridondanti da disco."""

    _loaded = False
    """Flag per indicare se lo stato è già stato caricato in memoria."""

    @classmethod
    def _load(cls) -> None:
        """Carica lo stato dal file JSON se non già presente nella cache interna."""
        if cls._loaded: return
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
        """Sincronizza lo stato in cache con il file JSON su disco."""
        try:
            cls.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            cls.STATE_FILE.write_text(json.dumps(cls._cache, indent=4), encoding="utf-8")
        except Exception as e:
            logger.error(f"Errore salvataggio sync state: {e}")

    @classmethod
    def update_status(cls, module: str, added: int, removed: int, duration: float = 0.0) -> None:
        """
        Registra l'avvenuta sincronizzazione di un modulo specifico.

        Args:
            module: Identificativo del modulo (es. 'pdl', 'dipendenti', 'storico_oda').
            added: Numero di record inseriti o aggiornati durante l'operazione.
            removed: Numero di record eliminati (non più presenti nella sorgente).
            duration: Tempo totale impiegato per la sincronizzazione (secondi).
        """
        cls._load()
        timestamp_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        cls._cache[module] = {
            "timestamp": timestamp_str, "added": added, "removed": removed,
            "duration": duration, "last_ts": time.time(),
        }
        cls._save()

    @classmethod
    def get_status(cls, module: str) -> dict[str, Any]:
        """
        Recupera i dati dell'ultima sincronizzazione per un determinato modulo.

        Args:
            module: Nome del modulo da interrogare.

        Returns:
            dict: Dizionario con timestamp, record aggiunti, rimossi e durata.
        """
        cls._load()
        return cls._cache.get(module, {})

    @classmethod
    def get_formatted_status(cls, module: str) -> str:
        """
        Restituisce una rappresentazione testuale formattata in HTML per la UI.
        Esempio: "30/01/2026 14:00 +1 -5 (Tempo: 2.5s)"

        Args:
            module: Nome del modulo.

        Returns:
            str: Stringa formattata pronta per essere visualizzata in un QLabel.
        """
        data = cls.get_status(module)
        if not data: return "Mai sincronizzato"

        timestamp = data.get("timestamp", "N/A")
        added, removed = data.get("added", 0), data.get("removed", 0)
        duration = data.get("duration", 0.0)

        added_str = f"<font color='green'><b>+{added}</b></font>"
        removed_str = f"<font color='red'><b>-{removed}</b></font>"
        time_str = f"{duration:.1f}s" if duration < 60 else f"{int(duration // 60)}m {int(duration % 60)}s"

        return f"{timestamp} {added_str} {removed_str} (Tempo: {time_str})"
