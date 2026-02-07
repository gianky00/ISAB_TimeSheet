"""
Decorators per logging automatico.
"""

import functools
import time
from collections.abc import Callable

from .context import generate_span_id, get_context, with_context
from .logger import get_logger
from .metrics import get_tracker


def measure_time(
    func: Callable | None = None,
    *,
    threshold_ms: float | None = None,
    logger_name: str | None = None,
):
    """
    Decorator per misurare tempo esecuzione e loggarlo automaticamente.

    Usage:
        @measure_time
        def my_function():
            ...

        @measure_time(threshold_ms=1000)
        def slow_function():
            # Alert se > 1sec
            ...

        @measure_time(logger_name="custom.logger")
        def other_function():
            ...

    Args:
        func: Funzione da decorare (auto-fornito quando usato senza parentesi)
        threshold_ms: Threshold in millisecondi. Se specificato e superato,
                     logga WARNING invece di DEBUG
        logger_name: Nome logger custom (default: nome modulo funzione)
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Determina logger
            if logger_name:
                logger = get_logger(logger_name)
            elif args and hasattr(args[0], "logger"):
                # Se è un metodo di classe con attributo logger
                logger = args[0].logger
            else:
                # Usa nome modulo funzione
                logger = get_logger(f"{f.__module__}.{f.__qualname__}")

            # Genera span_id per questa operazione
            span_id = generate_span_id()

            # Misura tempo
            start = time.perf_counter()

            # Esegui con context
            with with_context(span_id=span_id, function=f.__name__):
                try:
                    result = f(*args, **kwargs)
                    duration_ms = (time.perf_counter() - start) * 1000

                    # Track metrica
                    operation_name = f"{f.__module__}.{f.__qualname__}"
                    tracker = get_tracker()
                    tracker.track(
                        operation_name,
                        duration_ms,
                        metadata=get_context().to_dict(),
                    )

                    # Determina livello log
                    if threshold_ms and duration_ms > threshold_ms:
                        level = "WARNING"
                        threshold_exceeded = True
                    else:
                        level = "DEBUG"
                        threshold_exceeded = False

                    # Log performance
                    logger.log(
                        level,
                        f"Function {f.__name__} completed",
                        extra={
                            "duration_ms": round(duration_ms, 2),
                            "threshold_ms": threshold_ms,
                            "threshold_exceeded": threshold_exceeded,
                        },
                    )

                    return result

                except Exception as e:
                    duration_ms = (time.perf_counter() - start) * 1000

                    # Log exception con timing
                    logger.exception(
                        f"Function {f.__name__} failed after {duration_ms:.2f}ms",
                        exc=e,
                        extra={
                            "duration_ms": round(duration_ms, 2),
                            "threshold_ms": threshold_ms,
                        },
                    )
                    raise

        return wrapper

    # Support both @measure_time and @measure_time(threshold_ms=X)
    if func is None:
        return decorator
    return decorator(func)


def log_entry_exit(
    func: Callable | None = None,
    *,
    logger_name: str | None = None,
    log_args: bool = False,
    log_result: bool = False,
):
    """
    Decorator per loggare ingresso e uscita da funzione.

    Usage:
        @log_entry_exit
        def my_function(arg1, arg2):
            ...

        @log_entry_exit(log_args=True, log_result=True)
        def detailed_function(x, y):
            return x + y

    Args:
        func: Funzione da decorare
        logger_name: Nome logger custom
        log_args: Se True, logga gli argomenti della funzione
        log_result: Se True, logga il risultato della funzione
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Determina logger
            if logger_name:
                logger = get_logger(logger_name)
            else:
                logger = get_logger(f"{f.__module__}.{f.__qualname__}")

            # Log entry
            entry_msg = f"Entering {f.__name__}"
            if log_args:
                logger.debug(entry_msg, extra={"args": args, "kwargs": kwargs})
            else:
                logger.debug(entry_msg)

            try:
                result = f(*args, **kwargs)

                # Log exit
                exit_msg = f"Exiting {f.__name__}"
                if log_result:
                    logger.debug(exit_msg, extra={"result": result})
                else:
                    logger.debug(exit_msg)

                return result

            except Exception as e:
                logger.error(f"Exception in {f.__name__}: {e}")
                raise

        return wrapper

    # Support both @log_entry_exit and @log_entry_exit(log_args=True)
    if func is None:
        return decorator
    return decorator(func)
