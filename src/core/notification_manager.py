"""
SyncroJob - Notification Manager
Gestisce le notifiche dell'applicazione.
"""

import json
import uuid
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSignal

from src.core import config_manager


class NotificationManager(QObject):
    _instance = None

    # Segnali
    notification_added = pyqtSignal(dict)
    notifications_updated = pyqtSignal()
    unread_count_changed = pyqtSignal(int)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = NotificationManager()
        return cls._instance

    def __init__(self):
        super().__init__()
        self.notifications_file = config_manager.CONFIG_DIR / "notifications.json"
        self.notifications = self._load_notifications()

    def _load_notifications(self) -> list:
        """Carica le notifiche dal file JSON."""
        if not self.notifications_file.exists():
            return []
        try:
            with open(self.notifications_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ordina per timestamp (più recenti prima)
                return sorted(data, key=lambda x: x.get("timestamp", ""), reverse=True)
        except Exception as e:
            print(f"Errore caricamento notifiche: {e}")
            return []

    def _save_notifications(self):
        """Salva le notifiche su file."""
        try:
            with open(self.notifications_file, "w", encoding="utf-8") as f:
                json.dump(self.notifications, f, indent=4)
        except Exception as e:
            print(f"Errore salvataggio notifiche: {e}")

    def add_notification(self, title: str, message: str, level: str = "info"):
        """
        Aggiunge una nuova notifica.
        level: 'info', 'success', 'warning', 'error'
        """
        notification = {
            "id": str(uuid.uuid4()),
            "title": title,
            "message": message,
            "level": level,
            "timestamp": datetime.now().isoformat(),
            "read": False,
        }

        self.notifications.insert(0, notification)
        self._save_notifications()

        # Emetti segnali
        self.notification_added.emit(notification)
        self.notifications_updated.emit()
        self.unread_count_changed.emit(self.get_unread_count())

    def get_notifications(self, filter_unread: bool = False) -> list:
        """Restituisce la lista delle notifiche."""
        if filter_unread:
            return [n for n in self.notifications if not n.get("read", False)]
        return self.notifications

    def get_unread_count(self) -> int:
        """Restituisce il numero di notifiche non lette."""
        return sum(1 for n in self.notifications if not n.get("read", False))

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
