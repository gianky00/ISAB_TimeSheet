"""
Selenium Wait Helper Utilities
===============================
Centralizza pattern di wait comuni per eliminare time.sleep() hardcoded.

Questo modulo fornisce polling utilities per operazioni asincrone (es. download).

Autore: Refactoring Sprint 2026-01
"""

import logging
import time
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


# ============================================================================
# FILE POLLING UTILITIES
# ============================================================================


def poll_for_file(
    directory: Path | str,
    pattern: str = "*",
    timeout: int = 60,
    poll_interval: float = 0.5,
    min_age: Optional[float] = None,
    exclude_patterns: Optional[List[str]] = None,
) -> Optional[str]:
    """
    Attende che un file appaia in una directory usando polling.
    Approccio PERMISSIVO: ritorna il file più recente che soddisfa i criteri.

    Args:
        directory: Directory da monitorare.
        pattern: Glob pattern (es: "*.xlsx").
        timeout: Timeout massimo in secondi.
        poll_interval: Intervallo tra polling in secondi.
        min_age: Timestamp minimo del file (unix timestamp). Se None, accetta qualsiasi file.
        exclude_patterns: Pattern da escludere (es: [".crdownload", ".tmp"]).

    Returns:
        Path assoluto del file più recente, o None se timeout.
    """
    directory = Path(directory)
    if not directory.exists():
        logger.error(f"Directory does not exist: {directory}")
        return None

    exclude_patterns = exclude_patterns or []
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Check se ci sono download in corso (crdownload, tmp, part)
        in_progress = any(
            directory.glob(f"*{ext}") for ext in [".crdownload", ".tmp", ".part"]
        )

        if in_progress:
            time.sleep(poll_interval)
            continue

        # Trova tutti i file matching
        files = list(directory.glob(pattern))

        # Filtra per esclusioni
        files = [
            f
            for f in files
            if f.is_file()
            and not any(f.suffix == ext or ext in f.name for ext in exclude_patterns)
        ]

        # Filtra per età minima se specificata
        if min_age is not None:
            files = [f for f in files if f.stat().st_mtime > min_age]

        if files:
            # Ritorna il più recente
            latest = max(files, key=lambda f: f.stat().st_mtime)
            logger.debug(f"Found file: {latest.name}")
            return str(latest.absolute())

        time.sleep(poll_interval)

    logger.warning(f"Timeout polling for file in {directory} with pattern {pattern}")
    return None
