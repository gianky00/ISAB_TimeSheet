"""
SyncroJob - Ultra Smooth Animated Stacked Widget
Gestisce transizioni tra widget usando snapshot e cross-fade per performance massime.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    Signal,
)
from PySide6.QtWidgets import QGraphicsOpacityEffect, QLabel, QStackedWidget, QWidget

if TYPE_CHECKING:
    from PySide6.QtGui import QResizeEvent


class SlidingStackedWidget(QStackedWidget):
    """
    StackedWidget ad alte prestazioni che anima istantanee (snapshot) dei widget
    per garantire 60 FPS anche con contenuti pesanti.
    """

    animation_finished = Signal()
    """Segnale emesso al termine della transizione animata."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza lo stack animato.

        Args:
          parent: Widget genitore.
        """
        super().__init__(parent)
        self._animation_duration = 350
        self._easing_curve = QEasingCurve.Type.OutCubic
        self._animation_group = QParallelAnimationGroup(self)
        self._animation_group.finished.connect(self._on_animation_finished)

        self._is_animating = False
        self._current_index = 0
        self._next_index = 0

        # Overlay per snapshot
        self.fade_label_old = QLabel(self)
        self.fade_label_new = QLabel(self)
        self.fade_label_old.hide()
        self.fade_label_new.hide()

    def slide_to_index(self, index: int) -> None:  # noqa: PLR0915
        """
        Esegue l'animazione di transizione premium verso l'indice specificato.
        Utilizza snapshot QPixmap per mantenere la fluidit  indipendentemente dal carico dei widget.

        Args:
          index: L'indice del widget verso cui navigare.
        """
        if self._is_animating or index == self.currentIndex() or index < 0 or index >= self.count():
            self.setCurrentIndex(index)
            return

        self._is_animating = True
        self._current_index = self.currentIndex()
        self._next_index = index

        # 1. Cattura Snapshot (Cruciale per performance)
        old_widget = self.widget(self._current_index)
        next_widget = self.widget(self._next_index)

        if not old_widget or not next_widget:
            self.setCurrentIndex(index)
            self._is_animating = False
            return

        # Prepariamo il prossimo widget (deve essere renderizzato ma non visibile)
        next_widget.setGeometry(0, 0, self.width(), self.height())

        pix_old = old_widget.grab()
        pix_new = next_widget.grab()

        self.fade_label_old.setPixmap(pix_old)
        self.fade_label_new.setPixmap(pix_new)
        self.fade_label_old.setGeometry(0, 0, self.width(), self.height())

        # Direzione
        forward = index > self._current_index
        offset = self.width() if forward else -self.width()
        self.fade_label_new.setGeometry(offset, 0, self.width(), self.height())

        # Effetti opacit
        eff_old = QGraphicsOpacityEffect(self.fade_label_old)
        eff_new = QGraphicsOpacityEffect(self.fade_label_new)
        self.fade_label_old.setGraphicsEffect(eff_old)
        self.fade_label_new.setGraphicsEffect(eff_new)

        self.fade_label_old.show()
        self.fade_label_new.show()
        old_widget.hide()  # Nasconde il reale per non interferire

        # 2. Configura animazioni
        self._animation_group.clear()

        # Slide & Fade Out
        anim_out_pos = QPropertyAnimation(self.fade_label_old, b"pos")
        anim_out_pos.setDuration(self._animation_duration)
        anim_out_pos.setStartValue(QPoint(0, 0))
        anim_out_pos.setEndValue(QPoint(-int(offset / 2), 0))
        anim_out_pos.setEasingCurve(self._easing_curve)

        anim_out_fade = QPropertyAnimation(eff_old, b"opacity")
        anim_out_fade.setDuration(self._animation_duration)
        anim_out_fade.setStartValue(1.0)
        anim_out_fade.setEndValue(0.0)

        # Slide & Fade In
        anim_in_pos = QPropertyAnimation(self.fade_label_new, b"pos")
        anim_in_pos.setDuration(self._animation_duration)
        anim_in_pos.setStartValue(QPoint(offset, 0))
        anim_in_pos.setEndValue(QPoint(0, 0))
        anim_in_pos.setEasingCurve(self._easing_curve)

        anim_in_fade = QPropertyAnimation(eff_new, b"opacity")
        anim_in_fade.setDuration(self._animation_duration)
        anim_in_fade.setStartValue(0.0)
        anim_in_fade.setEndValue(1.0)

        self._animation_group.addAnimation(anim_out_pos)
        self._animation_group.addAnimation(anim_out_fade)
        self._animation_group.addAnimation(anim_in_pos)
        self._animation_group.addAnimation(anim_in_fade)

        self._animation_group.start()

    def _on_animation_finished(self) -> None:
        """Cleanup al termine dell'animazione: scambia i widget reali e nasconde gli snapshot."""
        self.setCurrentIndex(self._next_index)
        w = self.widget(self._next_index)
        if w:
            w.show()
        self.fade_label_old.hide()
        self.fade_label_new.hide()
        self._is_animating = False
        self.animation_finished.emit()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Sincronizza le dimensioni degli snapshot con il widget principale."""
        super().resizeEvent(event)
        size = event.size()
        self.fade_label_old.resize(size)
        self.fade_label_new.resize(size)
