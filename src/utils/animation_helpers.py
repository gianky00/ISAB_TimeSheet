"""SyncroJob - Helper per Animazioni PySide6.

Funzioni centralizzate per creare e gestire animazioni UI.
"""

from collections.abc import Callable
from contextlib import suppress

from PySide6.QtCore import (
    QAbstractAnimation,
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QTimer,
)
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
    QLayout,
    QWidget,
)

from src.gui.styles.constants import ANIMATION_TIMINGS


def create_opacity_effect(widget: QWidget) -> QGraphicsOpacityEffect:
    """Crea e applica un effetto di opacit  a un widget.

    Args:
      widget: Il widget a cui applicare l'effetto

    Returns:
      L'effetto di opacit  creato
    """
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    return effect


def create_fade_animation(
    effect: QGraphicsOpacityEffect,
    start: float = 0.0,
    end: float = 1.0,
    duration: int = ANIMATION_TIMINGS["fade_normal"],
    easing: QEasingCurve.Type = QEasingCurve.Type.InOutQuad,
) -> QPropertyAnimation:
    """Crea un'animazione di fade (opacit ).

    Args:
      effect: L'effetto di opacit  da animare
      start: Valore iniziale (0.0 - 1.0)
      end: Valore finale (0.0 - 1.0)
      duration: Durata in millisecondi
      easing: Curva di easing

    Returns:
      L'animazione creata (non avviata)
    """
    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(start)
    anim.setEndValue(end)
    anim.setEasingCurve(easing)
    return anim


def create_pulse_animation(
    effect: QGraphicsOpacityEffect,
    min_opacity: float = 0.6,
    max_opacity: float = 1.0,
    duration: int = ANIMATION_TIMINGS["pulse_slow"],
    loop: bool = True,
) -> QPropertyAnimation:
    """Crea un'animazione di pulsazione (fade in/out continuo).

    Args:
      effect: L'effetto di opacit  da animare
      min_opacity: Opacit  minima
      max_opacity: Opacit  massima
      duration: Durata di un ciclo completo
      loop: Se True, loop infinito

    Returns:
      L'animazione creata (non avviata)
    """
    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(min_opacity)
    anim.setEndValue(max_opacity)
    anim.setEasingCurve(QEasingCurve.Type.InOutSine)
    if loop:
        anim.setLoopCount(-1)
    return anim


def create_position_animation(
    widget: QWidget,
    start_pos: tuple[int, int],
    end_pos: tuple[int, int],
    duration: int = ANIMATION_TIMINGS["fade_normal"],
    easing: QEasingCurve.Type = QEasingCurve.Type.OutCubic,
) -> QPropertyAnimation:
    """Crea un'animazione di posizione.

    Args:
      widget: Il widget da animare
      start_pos: Posizione iniziale (x, y)
      end_pos: Posizione finale (x, y)
      duration: Durata in millisecondi
      easing: Curva di easing

    Returns:
      L'animazione creata (non avviata)
    """
    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duration)
    anim.setStartValue(QPoint(*start_pos))
    anim.setEndValue(QPoint(*end_pos))
    anim.setEasingCurve(easing)
    return anim


def cleanup_animation_safely(anim: QAbstractAnimation | None) -> None:
    """Ferma e pulisce un'animazione in modo sicuro.

    Args:
      anim: L'animazione da pulire (pu  essere None)
    """
    if anim is None:
        return

    with suppress(RuntimeError, AttributeError):
        if anim.state() == QAbstractAnimation.State.Running:
            anim.stop()
        anim.deleteLater()


def cleanup_effect_safely(widget: QWidget | None, effect: QGraphicsOpacityEffect | None) -> None:
    """Rimuove e pulisce un effetto grafico in modo sicuro.

    Args:
      widget: Il widget con l'effetto
      effect: L'effetto da pulire
    """
    with suppress(RuntimeError, AttributeError):
        if widget:
            widget.setGraphicsEffect(None)  # type: ignore[arg-type]
        if effect:
            effect.deleteLater()


def clear_layout_safely(layout: QLayout, process_events: bool = True) -> None:
    """Pulisce un layout rimuovendo tutti i widget in modo sicuro.

    Chiama cleanup() sui widget che lo supportano prima di eliminarli.

    Args:
      layout: Il layout da pulire
      process_events: Se True, forza il processing degli eventi Qt
    """
    widgets_to_delete = []

    while layout.count() > 0:
        item = layout.takeAt(0)
        if item is None:
            continue

        widget = item.widget()
        if widget:
            # Chiama cleanup se disponibile
            if hasattr(widget, "cleanup") and callable(widget.cleanup):
                with suppress(RuntimeError):
                    widget.cleanup()
            widgets_to_delete.append(widget)

        # Gestisci anche layout annidati
        nested_layout = item.layout()
        if nested_layout:
            clear_layout_safely(nested_layout, process_events=False)

    # Elimina tutti i widget
    for widget in widgets_to_delete:
        with suppress(RuntimeError):
            widget.deleteLater()

    # Forza processing eventi per pulizia immediata
    if process_events:
        QApplication.processEvents()


def stop_layout_animations(layout: QLayout) -> None:
    """Ferma ricorsivamente tutte le animazioni nei widget di un layout.

    Args:
      layout: Il layout da processare
    """
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if not item:
            continue

        widget = item.widget()
        if widget:
            # Stop pulse animation
            if hasattr(widget, "pulse_anim") and widget.pulse_anim:
                with suppress(RuntimeError):
                    widget.pulse_anim.stop()

            # Stop timers
            if hasattr(widget, "timer") and widget.timer:
                with suppress(RuntimeError):
                    widget.timer.stop()

        # Processa layout annidati
        nested_layout = item.layout()
        if nested_layout:
            stop_layout_animations(nested_layout)


def create_animation_timer(
    parent: QWidget,
    callback: Callable[[], None],
    interval: int = ANIMATION_TIMINGS["fps_60"],
    single_shot: bool = False,
) -> QTimer:
    """Crea un timer per animazioni.

    Args:
      parent: Il widget parent
      callback: La funzione da chiamare
      interval: Intervallo in millisecondi
      single_shot: Se True, esegue una sola volta

    Returns:
      Il timer creato (non avviata)
    """
    timer = QTimer(parent)
    timer.timeout.connect(callback)
    timer.setSingleShot(single_shot)
    if not single_shot:
        timer.setInterval(interval)
    return timer


def delayed_call(callback: Callable[[], None], delay: int = 100, parent: QWidget | None = None) -> None:
    """Esegue una funzione dopo un ritardo.

    Args:
      callback: La funzione da chiamare
      delay: Ritardo in millisecondi
      parent: Parent opzionale per il timer
    """
    # In PySide6 QTimer.singleShot(msec, slot)  la firma standard.
    # L'uso di un parent  gestito internamente se il timer  creato come istanza,
    # ma il metodo statico accetta solo 2 o 3 argomenti (msec, timerType, slot).
    QTimer.singleShot(delay, callback)


def staggered_fade_in(
    widgets: list[QWidget],
    delay_between: int = 50,
    fade_duration: int = ANIMATION_TIMINGS["fade_normal"],
) -> list[QPropertyAnimation]:
    """Crea animazioni di fade-in sfalsate per una lista di widget.

    Args:
      widgets: Lista di widget da animare
      delay_between: Ritardo tra ogni animazione
      fade_duration: Durata di ogni fade

    Returns:
      Lista delle animazioni create
    """
    animations = []

    for i, widget in enumerate(widgets):
        effect = create_opacity_effect(widget)
        effect.setOpacity(0)

        anim = create_fade_animation(effect, 0.0, 1.0, fade_duration)
        animations.append(anim)

        # Avvia con ritardo
        QTimer.singleShot(i * delay_between, anim.start)

    return animations
