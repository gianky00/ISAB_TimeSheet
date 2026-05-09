"""
SyncroJob - Animated Tab Widget (Premium Stylized)
Componente universale con animazioni di lusso, gradienti e glow effect.
Fornisce una navigazione tra schede fluida con indicatore di selezione dinamico.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect, QTimer, Signal
from PySide6.QtGui import QColor, QResizeEvent, QShowEvent
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QTabBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.gui.components.animated_stack import SlidingStackedWidget
from src.gui.styles import COLORS


class AnimatedTabWidget(QWidget):
    """
    Sostituto d' lite di QTabWidget con transizioni Snapshot-Fade
    e indicatore di selezione con effetto 'Illumination'.

    Supporta il posizionamento dei tab (North/South) e garantisce performance a 60 FPS
    grazie alla tecnica di snapshot rendering durante le transizioni.
    """

    currentChanged = Signal(int)  # noqa: N815
    """Segnale emesso quando il tab attivo cambia."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza the widget dei tab animati.

        Args:
          parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # Header superiore: TabBar + Controlli opzionali
        self.header_widget = QWidget()
        self.header_widget.setMinimumHeight(55)  # Leggermente più alto per il glow
        # Track di fondo (La linea sottile grigiàche segna il percorso)
        self.header_widget.setStyleSheet("border-bottom: 1px solid rgba(0, 0, 0, 0.05); background: white;")

        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(10, 0, 10, 0)
        self.header_layout.setSpacing(15)

        # Tab Bar personalizzata
        self.tab_bar = QTabBar()
        self.tab_bar.setDrawBase(False)
        self.tab_bar.setExpanding(False)
        self.tab_bar.setDocumentMode(True)
        self.tab_bar.setStyleSheet(self._get_default_style())
        self.tab_bar.currentChanged.connect(self._on_tab_bar_changed)

        self.header_layout.addWidget(self.tab_bar)
        self.header_layout.addStretch()

        # --- INDICATORE PREMIUM (Gradients & Glow) ---
        self.indicator = QWidget(self.header_widget)
        self.indicator.setFixedHeight(4)  # Un pò più spessa per mostrare il gradiente

        # Design con gradiente lineare
        self.indicator.setStyleSheet(f"""
      background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS["primary_blue"]}, stop:0.5 {COLORS["teal_accent"]}, stop:1 {COLORS["primary_dark"]});
      border-radius: 2px;
    """)

        # Effetto Glow (Bagliore)
        glow = QGraphicsDropShadowEffect(self.indicator)
        glow.setBlurRadius(10)
        c = QColor(COLORS["teal_accent"])
        glow.setColor(QColor(c.red(), c.green(), c.blue(), 120))
        glow.setOffset(0, 1)
        self.indicator.setGraphicsEffect(glow)

        self.indicator.raise_()
        self._indicator_anim = QPropertyAnimation(self.indicator, b"geometry")
        self._indicator_anim.setDuration(400)  # Un pò più lenta per eleganza
        self._indicator_anim.setEasingCurve(QEasingCurve.Type.OutQuint)  # Il top della fluidit

        # Stack animato
        self.stack = SlidingStackedWidget()
        self.stack.animation_finished.connect(lambda: self.setEnabled(True))

        # Default Position: North
        self._tab_position = QTabWidget.TabPosition.North
        self._layout.addWidget(self.header_widget)
        self._layout.addWidget(self.stack)

        QTimer.singleShot(100, self._update_indicator_instant)

    def showEvent(self, event: QShowEvent) -> None:
        """Forza l'aggiornamento dello stile quando il widget viene mostrato."""
        super().showEvent(event)
        self._update_indicator_instant()

        # Riapplica lo stile locale per evitare override da ThemeManager globale
        if self._tab_position == QTabWidget.TabPosition.South:
            self.tab_bar.setStyleSheet(self._get_south_style())
        else:
            self.tab_bar.setStyleSheet(self._get_default_style())

    def setTabPosition(self, position: QTabWidget.TabPosition) -> None:
        """
        Imposta la posizione della barra dei tab.

        Args:
          position: Posizione desiderata (North o South).
        """
        if position == self._tab_position:
            return
        self._tab_position = position
        self._layout.removeWidget(self.header_widget)
        self._layout.removeWidget(self.stack)

        if position == QTabWidget.TabPosition.South:
            self._layout.addWidget(self.stack)
            self._layout.addWidget(self.header_widget)
            self.header_widget.setStyleSheet("border-top: 1px solid rgba(0, 0, 0, 0.05); background: white;")
            self.tab_bar.setStyleSheet(self._get_south_style())
        else:
            self._layout.addWidget(self.header_widget)
            self._layout.addWidget(self.stack)
            self.header_widget.setStyleSheet(
                "border-bottom: 1px solid rgba(0, 0, 0, 0.05); background: white;"
            )
            self.tab_bar.setStyleSheet(self._get_default_style())

        QTimer.singleShot(10, self._update_indicator_instant)

    def addTab(self, widget: QWidget, *args: Any) -> int:
        """
        Aggiunge un nuovo tab.

        Args:
          widget: Il widget da visualizzare nella scheda.
          *args: Argomenti per QTabBar.addTab (es. icona e testo).

        Returns:
          int: L'indice del tab aggiunto.
        """
        index = self.tab_bar.addTab(*args)
        self.stack.addWidget(widget)
        return index

    def removeTab(self, index: int) -> None:
        """
        Rimuove un tab e il relativo widget dallo stack.

        Args:
          index: Indice del tab da rimuovere.
        """
        if 0 <= index < self.tab_bar.count():
            self.tab_bar.removeTab(index)
            w = self.stack.widget(index)
            if w:
                self.stack.removeWidget(w)
                w.deleteLater()
            self._update_indicator_instant()

    def clear(self) -> None:
        """Svuota tutti i tab e i relativi widget resettando l'interfaccia."""
        while self.tab_bar.count() > 0:
            self.tab_bar.removeTab(0)
        while self.stack.count() > 0:
            w = self.stack.widget(0)
            if w:
                self.stack.removeWidget(w)
                w.deleteLater()
        self.indicator.hide()

    def _on_tab_bar_changed(self, index: int) -> None:
        """
        Gestisce internamente il cambio di tab nella barra.

        Args:
          index: Nuovo indice selezionato.
        """
        self._animate_indicator(index)
        if index != self.stack.currentIndex():
            self.setEnabled(False)
            self.stack.slide_to_index(index)
            if not self.stack._is_animating:
                self.setEnabled(True)
            self.currentChanged.emit(index)

    def _animate_indicator(self, index: int) -> None:
        """
        Avvia l'animazione dell'indicatore verso il tab specificato.

        Args:
          index: Indice di destinazione.
        """
        rect = self.tab_bar.tabRect(index)
        if rect.isValid():
            global_pos = self.tab_bar.mapTo(self.header_widget, rect.topLeft())
            y_pos = self.header_widget.height() - self.indicator.height()
            if self._tab_position == QTabWidget.TabPosition.South:
                y_pos = 0

            # Effetto "Elastic": la linea  leggermente più stretta del tab per eleganza
            target_rect = QRect(global_pos.x() + 15, y_pos, rect.width() - 30, self.indicator.height())

            self.indicator.show()
            self._indicator_anim.stop()
            self._indicator_anim.setEndValue(target_rect)
            self._indicator_anim.start()

    def _update_indicator_instant(self) -> None:
        """Aggiorna istantaneamente la posizione della linea senza animazioni."""
        idx = self.tab_bar.currentIndex()
        if idx < 0:
            self.indicator.hide()
            return

        rect = self.tab_bar.tabRect(idx)
        if rect.isValid():
            self.indicator.show()
            global_pos = self.tab_bar.mapTo(self.header_widget, rect.topLeft())
            y_pos = self.header_widget.height() - self.indicator.height()
            if self._tab_position == QTabWidget.TabPosition.South:
                y_pos = 0
            self.indicator.setGeometry(global_pos.x() + 15, y_pos, rect.width() - 30, self.indicator.height())
        else:
            self.indicator.hide()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Assicura che l'indicatore sia allineato dopo il ridimensionamento."""
        super().resizeEvent(event)
        self._update_indicator_instant()

    def currentIndex(self) -> int:
        """Restituisce l'indice del tab corrente."""
        return self.tab_bar.currentIndex()

    def currentWidget(self) -> QWidget | None:
        """Restituisce il widget associato al tab corrente."""
        return self.stack.currentWidget()

    def setCurrentIndex(self, index: int) -> None:
        """
        Imposta programmaticamente il tab corrente.

        Args:
          index: Indice da attivare.
        """
        self.tab_bar.setCurrentIndex(index)
        self.stack.setCurrentIndex(index)
        self._update_indicator_instant()

    def count(self) -> int:
        """Restituisce il numero totale di tab."""
        return self.tab_bar.count()

    def tabText(self, index: int) -> str:
        """Restituisce il testo del tab all'indice specificato."""
        return self.tab_bar.tabText(index)

    def widget(self, index: int) -> QWidget | None:
        """Restituisce il widget all'indice specificato."""
        return self.stack.widget(index)

    def tabBar(self) -> QTabBar:
        """Restituisce l'istanza della QTabBar interna."""
        return self.tab_bar

    def _get_default_style(self) -> str:
        """Restituisce lo stile QSS per la barra dei tab in posizione North."""
        return f"""
      QTabBar::tab {{
        background: transparent; color: {COLORS["text_muted"]}; padding: 12px 24px;
        font-weight: 600; font-size: 13px; border: none;
      }}
      QTabBar::tab:selected {{ color: {COLORS["primary_dark"]}; }}
      QTabBar::tab:hover:!selected {{ color: {COLORS["text_dark"]}; background: rgba({QColor(COLORS["teal_accent"]).red()}, {QColor(COLORS["teal_accent"]).green()}, {QColor(COLORS["teal_accent"]).blue()}, 0.04); border-radius: 4px; }}
    """

    def _get_south_style(self) -> str:
        """Restituisce lo stile QSS per la barra dei tab in posizione South."""
        return f"""
      QTabBar::tab {{
        background: transparent; color: {COLORS["text_muted"]}; padding: 10px 18px;
        font-weight: 600; font-size: 12px; border: none;
      }}
      QTabBar::tab:selected {{ color: {COLORS["primary_dark"]}; }}
    """
