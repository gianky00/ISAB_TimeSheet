"""
SyncroJob - Notification Manager
Gestore centralizzato delle notifiche applicative.
Fornisce un'interfaccia thread-safe per aggiungere, filtrare e gestire lo stato di lettura dei messaggi di sistema.
Supporta la persistenza su JSON e l'integrazione con la UI tramite segnali e toast.
"""

import json
import threading
import uuid
from collections.abc import Sequence
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any, Final, Optional

from PySide6.QtCore import QObject, Signal

from src.core.constants import FileNames
from src.core.paths import CONFIG_DIR


class NotificationManager(QObject):
    """
    Manager singleton per il sistema di notifiche.
    Gestisce il ciclo di vita dei messaggi (creazione, lettura, pin, eliminazione).
    Emette segnali per l'aggiornamento dinamico dell'interfaccia utente.
    """

    _instance: Optional["NotificationManager"] = None
    _lock = threading.RLock()

    # Segnali
    notification_added = Signal(dict)
    """Segnale emesso quando viene aggiunta una nuova notifica."""

    notifications_updated = Signal()
    """Segnale emesso a seguito di qualsiasi modifica alla lista delle notifiche."""

    unread_count_changed = Signal(int)
    """Segnale emesso quando cambia il numero di errori non letti."""

    request_toast = Signal(str, str, int)
    """Segnale emesso per richiedere la visualizzazione di un toast (msg, livello, ms)."""

    MAX_MESSAGE_LEN: Final[int] = 120
    TRUNCATE_SUFFIX_LEN: Final[int] = 3

    @classmethod
    def instance(cls) -> "NotificationManager":
        """
        Restituisce l'istanza singleton della classe, creandola se necessario (Thread-Safe).

        Returns:
          NotificationManager: L'istanza unica globale.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = NotificationManager()
        return cls._instance

    @classmethod
    def _reset_instance_for_testing(cls) -> None:
        """Resetta l'istanza singleton (Solo per testing)."""
        with cls._lock:
            cls._instance = None

    def __init__(self) -> None:
        """Inizializza il manager caricando le notifiche salvate su disco."""
        super().__init__()
        self.notifications_file = CONFIG_DIR / FileNames.NOTIFICATIONS
        if not hasattr(self, "_lock"):
            self._lock = threading.RLock()
        self.notifications: list[dict[str, Any]] = self._load_notifications()

    def _load_notifications(self) -> list[dict[str, Any]]:
        """Carica le notifiche dal file JSON applicando migrazioni di schema se necessario."""
        if not self.notifications_file.exists():
            return []
        with suppress(Exception), self.notifications_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            migrated_data = [self._migrate_notification(n) for n in data if isinstance(n, dict)]
            return sorted(migrated_data, key=lambda x: x.get("timestamp", ""), reverse=True)
        return []

    def _migrate_notification(self, notif: dict[str, Any]) -> dict[str, Any]:
        """Assicura che la notifica contenga tutti i campi richiesti dallo schema attuale."""
        defaults = {
            "category": "system",
            "priority": "low",
            "source": "Sistema",
            "pinned": False,
            "snoozed_until": None,
            "archived": False,
            "tags": [],
            "metadata": {},
            "actions": [],
            "related_id": None,
        }
        return defaults | notif

    def _save_notifications(self) -> None:
        """Persiste la lista corrente delle notifiche nel file JSON."""
        try:
            with self.notifications_file.open("w", encoding="utf-8") as f:
                json.dump(self.notifications, f, indent=4)
        except Exception as e:
            print(f"Errore salvataggio notifiche: {e}")

    def add_notification(
        self,
        title: str,
        message: str,
        level: str = "info",
        category: str = "system",
        priority: str = "low",
        source: str = "Sistema",
        tags: Sequence[str] | None = None,
        metadata: dict[str, Any] | None = None,
        actions: Sequence[dict[str, Any]] | None = None,
        related_id: str | None = None,
        show_toast: bool = False,
    ) -> None:
        """
        Crea e aggiunge una nuova notifica al sistema.

        Args:
          title: Titolo della notifica.
          message: Contenuto del messaggio.
          level: Severità (info, success, warning, error).
          category: Categoria logica del messaggio.
          priority: Priorità di visualizzazione.
          source: Modulo sorgente.
          tags: Etichette di ricerca.
          metadata: Dati strutturati extra.
          actions: Lista di azioni rapide (callback/link).
          related_id: ID di un oggetto correlato (es. ID OdA).
          show_toast: Se richiedere l'emissione immediata di un toast a schermo.
        """
        id_notif = str(uuid.uuid4())
        notif: dict[str, Any] = {
            "id": id_notif,
            "title": title,
            "message": message,
            "level": level,
            "category": category,
            "priority": priority,
            "source": source,
            "timestamp": datetime.now(UTC).isoformat(),
            "read": False,
            "archived": False,
            "pinned": False,
            "snoozed_until": None,
            "tags": list(tags) if tags is not None else [],
            "metadata": metadata or {},
            "actions": list(actions) if actions is not None else [],
            "related_id": related_id,
        }

        with self._lock:
            self.notifications.insert(0, notif)
            self._save_notifications()

        self.notification_added.emit(notif)
        self.notifications_updated.emit()
        self.unread_count_changed.emit(self.get_unread_count())

        if show_toast:
            duration_map = {"success": 2000, "warning": 10000, "error": 10000, "info": 3000}
            duration = duration_map.get(level, 3000)
            clean_msg = message.replace("<b>", "").replace("</b>", "").replace("<br>", " ")
            if len(clean_msg) > self.MAX_MESSAGE_LEN:
                cutoff = self.MAX_MESSAGE_LEN - self.TRUNCATE_SUFFIX_LEN
                clean_msg = clean_msg[:cutoff] + "..."
            self.request_toast.emit(f"{title}: {clean_msg}", level, duration)

    def get_notifications(self, filter_unread: bool = False) -> list[dict[str, Any]]:
        """
        Restituisce l'elenco delle notifiche in memoria.

        Args:
          filter_unread: Se True, restituisce solo i messaggi non letti.

        Returns:
          list: Lista di dizionari notifica.
        """
        if filter_unread:
            return [n for n in self.notifications if not n.get("read", False)]
        return self.notifications

    def get_unread_count(self) -> int:
        """
        Restituisce il conteggio degli errori (level=error) non ancora letti.

        Returns:
          int: Numero di errori pendenti.
        """
        return sum(1 for n in self.notifications if not n.get("read", False) and n.get("level") == "error")

    def mark_as_read(self, notification_id: str) -> None:
        """Segna un singolo messaggio come letto e aggiorna i contatori."""
        for n in self.notifications:
            if n["id"] == notification_id:
                if not n["read"]:
                    n["read"] = True
                    self._save_notifications()
                    self.notifications_updated.emit()
                    self.unread_count_changed.emit(self.get_unread_count())
                break

    def mark_all_as_read(self) -> None:
        """Segna indistintamente tutti i messaggi come letti."""
        changed = False
        for n in self.notifications:
            if not n["read"]:
                n["read"] = True
                changed = True
        if changed:
            self._save_notifications()
            self.notifications_updated.emit()
            self.unread_count_changed.emit(0)

    def update_notification(self, notification_id: str, updates: dict[str, Any]) -> None:
        """Aggiorna parzialmente i campi di una notifica identificata per ID."""
        with self._lock:
            for n in self.notifications:
                if n["id"] == notification_id:
                    n.update(updates)
                    self._save_notifications()
                    self.notifications_updated.emit()
                    if "read" in updates:
                        self.unread_count_changed.emit(self.get_unread_count())
                    break

    def pin_notification(self, notification_id: str, pinned: bool) -> None:
        """Fissa o sblocca una notifica nella parte alta della lista."""
        self.update_notification(notification_id, {"pinned": pinned})

    def delete_notification(self, notification_id: str) -> None:
        """Rimuove definitivamente una notifica dal sistema."""
        self.notifications = [n for n in self.notifications if n["id"] != notification_id]
        self._save_notifications()
        self.notifications_updated.emit()
        self.unread_count_changed.emit(self.get_unread_count())

    def clear_all(self) -> None:
        """Svuota l'intera cronologia delle notifiche."""
        self.notifications = []
        self._save_notifications()
        self.notifications_updated.emit()
        self.unread_count_changed.emit(0)
