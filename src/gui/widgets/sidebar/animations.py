"""
SyncroJob - Sidebar Animation Manager
Gestisce le transizioni fluide e il movimento magnetico del track.
"""

from PyQt6.QtCore import QEasingCurve, QObject, QPoint, QPropertyAnimation, QRect
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget


class SidebarAnimationManager(QObject):
    """Orchestratore delle animazioni per la Sidebar Widget."""

    def __init__(self, sidebar: QWidget):
        super().__init__(sidebar)
        self.sidebar = sidebar

        # Animazione Larghezza Sidebar
        self.width_anim = QPropertyAnimation(sidebar, b"sidebar_width")
        self.width_anim.setDuration(250)
        self.width_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Animazione Opacità Contenuto
        self.content_anim = QPropertyAnimation(None, b"opacity")
        self.content_anim.setDuration(200)
        self.content_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Animazione Track Magnetico
        self.track_anim = QPropertyAnimation(None, b"geometry")
        self.track_anim.setDuration(350)
        self.track_anim.setEasingCurve(QEasingCurve.Type.OutQuint)

    def animate_width(self, target_width: int):
        """Esegue l'animazione di espansione/collasso."""
        self.width_anim.stop()
        self.width_anim.setEndValue(target_width)
        self.width_anim.start()

    def animate_content(self, effect: QGraphicsOpacityEffect, target_opacity: float):
        """Esegue l'animazione di dissolvenza per i contenuti della sidebar."""
        self.content_anim.stop()
        self.content_anim.setTargetObject(effect)
        self.content_anim.setEndValue(target_opacity)
        self.content_anim.start()

    def move_track(self, track_widget: QWidget, target_widget: QWidget):
        """Sposta l'indicatore magnetico verso il widget target."""
        if not target_widget or not target_widget.isVisible():
            return

        pos = target_widget.mapTo(self.sidebar, QPoint(0, 0))
        target_rect = QRect(2, pos.y() + 8, 5, target_widget.height() - 16)

        track_widget.show()
        self.track_anim.stop()
        self.track_anim.setTargetObject(track_widget)
        self.track_anim.setEndValue(target_rect)
        self.track_anim.start()
