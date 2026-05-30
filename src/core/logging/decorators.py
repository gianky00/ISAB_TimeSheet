"""Decorators per il logging automatico e il monitoraggio delle performance.

Fornisce strumenti per misurare i tempi di esecuzione e tracciare l'ingresso/uscita dalle funzioni.
"""

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar, cast, overload

from .context import generate_span_id, get_context, with_context
from .logger import get_logger
from .metrics import get_tracker

F = TypeVar("F", bound=Callable[..., Any])


@overload
def measure_time[F: Callable[..., Any]](
    func: F,
    *,
    threshold_ms: float | None = None,
    logger_name: str | None = None,
) -> F: ...


@overload
def measure_time(
    func: None = None,
    *,
    threshold_ms: float | None = None,
    logger_name: str | None = None,
) -> Callable[[F], F]: ...
def measure_time[F: Callable[..., Any]](
    func: F | None = None,
    *,
    threshold_ms: float | None = None,
    logger_name: str | None = None,
) -> F | Callable[[F], F]:
    """Decorator per misurare tempo esecuzione e loggarlo automaticamente.

    Invia le metriche al tracker globale e genera span_id per il contesto.

    Args:
      func: Funzione da decorare.
      threshold_ms: Soglia in ms oltre la quale loggare un WARNING.
      logger_name: Nome del logger da utilizzare.

    Returns:
      La funzione decorata o il decoratore stesso.
    """

    def decorator(f: F) -> F:
        """Decoratore effettivo che avvolge la funzione per la misurazione del tempo."""

        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper interno per la misurazione del tempo."""
            if logger_name:
                logger = get_logger(logger_name)
            elif args and hasattr(args[0], "logger"):
                logger = args[0].logger
            else:
                logger = get_logger(f"{f.__module__}.{f.__qualname__}")

            span_id = generate_span_id()
            start = time.perf_counter()

            with with_context(span_id=span_id, function=f.__name__):
                try:
                    result = f(*args, **kwargs)
                    duration_ms = (time.perf_counter() - start) * 1000

                    operation_name = f"{f.__module__}.{f.__qualname__}"
                    tracker = get_tracker()
                    tracker.track(
                        operation_name,
                        duration_ms,
                        metadata=get_context().to_dict(),
                    )

                    if threshold_ms and duration_ms > threshold_ms:
                        level = "WARNING"
                        threshold_exceeded = True
                    else:
                        level = "DEBUG"
                        threshold_exceeded = False

                    logger.log(
                        level,
                        f"Function {f.__name__} completed",
                        extra={
                            "duration_ms": round(duration_ms, 2),
                            "threshold_ms": threshold_ms,
                            "threshold_exceeded": threshold_exceeded,
                        },
                    )

                    return result  # noqa: TRY300

                except Exception as e:
                    duration_ms = (time.perf_counter() - start) * 1000
                    logger.exception(
                        f"Function {f.__name__} failed after {duration_ms:.2f}ms",
                        exc=e,
                        extra={
                            "duration_ms": round(duration_ms, 2),
                            "threshold_ms": threshold_ms,
                        },
                    )
                    raise

        return cast("F", wrapper)

    if func is None:
        return cast("Callable[[F], F]", decorator)
    return decorator(func)


@overload
def log_entry_exit[F: Callable[..., Any]](
    func: F,
    *,
    logger_name: str | None = None,
    log_args: bool = False,
    log_result: bool = False,
) -> F: ...


@overload
def log_entry_exit(
    func: None = None,
    *,
    logger_name: str | None = None,
    log_args: bool = False,
    log_result: bool = False,
) -> Callable[[F], F]: ...


def log_entry_exit[F: Callable[..., Any]](
    func: F | None = None,
    *,
    logger_name: str | None = None,
    log_args: bool = False,
    log_result: bool = False,
) -> F | Callable[[F], F]:
    """Decorator per loggare l'ingresso e l'uscita da una funzione.

    Utile per il tracciamento del flusso di esecuzione nel debug.

    Args:
      func: Funzione da decorare.
      logger_name: Nome del logger.
      log_args: Se loggare gli argomenti passati.
      log_result: Se loggare il valore restituito.

    Returns:
      La funzione decorata o il decoratore stesso.
    """

    def decorator(f: F) -> F:
        """Decoratore effettivo che avvolge la funzione per il log entry/exit."""

        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper interno per loggare entry/exit."""
            if logger_name:
                logger = get_logger(logger_name)
            else:
                logger = get_logger(f"{f.__module__}.{f.__qualname__}")

            entry_msg = f"Entering {f.__name__}"
            if log_args:
                logger.debug(entry_msg, extra={"args": args, "kwargs": kwargs})
            else:
                logger.debug(entry_msg)

            try:
                result = f(*args, **kwargs)
                exit_msg = f"Exiting {f.__name__}"
                if log_result:
                    logger.debug(exit_msg, extra={"result": result})
                else:
                    logger.debug(exit_msg)
                return result  # noqa: TRY300

            except Exception:
                logger.exception(f"Exception in {f.__name__}")
                raise

        return cast("F", wrapper)

    if func is None:
        return cast("Callable[[F], F]", decorator)
    return decorator(func)
