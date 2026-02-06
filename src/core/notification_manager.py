"""
SyncroJob - Notification Manager
Gestisce le notifiche dell'applicazione.
"""

import json
import threading
import uuid
from contextlib import suppress
from datetime import datetime
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal

from src.core import config_manager


class NotificationManager(QObject):
    _instance = None
    _lock = threading.RLock()  # Thread-safety lock

    # Segnali
    notification_added = pyqtSignal(dict)
    notifications_updated = pyqtSignal()
    unread_count_changed = pyqtSignal(int)
    request_toast = pyqtSignal(str, str, int)  # messaggio, tipo, durata

    @classmethod
    def instance(cls):
        if cls._instance is None:
            # Double-checked locking pattern is not strictly needed here given GIL and simple init,
            # but we use lock for instance safety if accessed concurrently during startup
            with cls._lock:
                if cls._instance is None:
                    cls._instance = NotificationManager()
        return cls._instance

    def __init__(self):
        super().__init__()
        self.notifications_file = config_manager.CONFIG_DIR / "notifications.json"

        # Ensure we have a lock instance even if manually instantiated (though shouldn't be)
        if not hasattr(self, "_lock"):
            self._lock = threading.RLock()

        self.notifications = self._load_notifications()

    def _load_notifications(self) -> list:
        """Carica le notifiche dal file JSON con migrazione automatica."""
        if not self.notifications_file.exists():
            return []
        with suppress(Exception):
            with self.notifications_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                # Applica migrazione per retrocompatibilità
                data = [self._migrate_notification(n) for n in data]
                # Ordina per timestamp (più recenti prima)
                return sorted(data, key=lambda x: x.get("timestamp", ""), reverse=True)
        return []

    def _migrate_notification(self, notif: dict) -> dict:
        """Migra notifica vecchia al nuovo schema con valori default."""
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
        # Merge: existing fields override defaults
        return defaults | notif

    def _save_notifications(self):
        """Salva le notifiche su file."""
        try:
            with open(self.notifications_file, "w", encoding="utf-8") as f:
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
        tags: Optional[list] = None,
        metadata: Optional[dict] = None,
        actions: Optional[list] = None,
        related_id: Optional[str] = None,
        show_toast: bool = False,
    ):
        """
        Aggiunge una nuova notifica con schema esteso.
        """
        id_notif = str(uuid.uuid4())
        notif = {
            "id": id_notif,
            "title": title,
            "message": message,
            "level": level,
            "category": category,
            "priority": priority,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "read": False,
            "archived": False,
            "pinned": False,
            "snoozed_until": None,
            "tags": tags or [],
            "metadata": metadata or {},
            "actions": actions or [],
            "related_id": related_id,
        }

        with self._lock:
            self.notifications.insert(0, notif)
            self._save_notifications()

        # Emissione segnali (fuori dal lock per evitare deadlock con Qt loop)
        self.notification_added.emit(notif)
        self.notifications_updated.emit()
        self.unread_count_changed.emit(self.get_unread_count())

        # Se richiesto, richiede la visualizzazione del toast tramite segnale
        if show_toast:
            # Determinazione durata basata sul livello (Enterprise standards)
            duration_map = {
                "success": 2000,
                "warning": 10000,
                "error": 10000,
                "info": 3000,
            }
            duration = duration_map.get(level, 3000)

            # Puliamo il messaggio per il toast (niente HTML pesante)
            clean_msg = (
                message.replace("<b>", "").replace("</b>", "").replace("<br>", " ")
            )
            if len(clean_msg) > 120:
                clean_msg = clean_msg[:117] + "..."

            self.request_toast.emit(f"{title}: {clean_msg}", level, duration)

    def get_notifications(self, filter_unread: bool = False) -> list:
        """Restituisce la lista delle notifiche."""
        if filter_unread:
            return [n for n in self.notifications if not n.get("read", False)]
        return self.notifications

    def get_unread_count(self) -> int:
        """Restituisce il numero di notifiche di errore non lette."""
        return sum(
            1
            for n in self.notifications
            if not n.get("read", False) and n.get("level") == "error"
        )

    def mark_as_read(self, notification_id: str):
        """Segna una notifica come letta."""
        for n in self.notifications:
            if n["id"] == notification_id:
                if not n["read"]:
                    n["read"] = True
                    self._save_notifications()
                    self.notifications_updated.emit()
                    self.unread_count_changed.emit(self.get_unread_count())
                break

    def mark_all_as_read(self):
        """Segna tutte le notifiche come lette."""
        changed = False
        for n in self.notifications:
            if not n["read"]:
                n["read"] = True
                changed = True

        if changed:
            self._save_notifications()
            self.notifications_updated.emit()
            self.unread_count_changed.emit(0)

    def delete_notification(self, notification_id: str):
        """Elimina una notifica."""
        self.notifications = [
            n for n in self.notifications if n["id"] != notification_id
        ]
        self._save_notifications()
        self.notifications_updated.emit()
        self.unread_count_changed.emit(self.get_unread_count())

    def clear_all(self):
        """Elimina tutte le notifiche."""
        self.notifications = []
        self._save_notifications()
        self.notifications_updated.emit()
        self.unread_count_changed.emit(0)
