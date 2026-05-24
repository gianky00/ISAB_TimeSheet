"""Utility di sistema e parsing per il Robust Test Runner."""

from __future__ import annotations

import datetime
import hashlib
import multiprocessing
import os
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from rich.console import Console

# --- CONFIGURAZIONE GLOBALE ---
DEFAULT_TIMEOUT: Final[int] = 120
SEQUENZIALE_THRESHOLD: Final[int] = 5
MAX_OUTPUT_CHARS: Final[int] = 2000  # Limite output per file nel report IA
MAX_WORKERS: Final[int] = max(1, multiprocessing.cpu_count() - 1)

# Risoluzione dinamica della ROOT_DIR (3 salti indietro da qui)
ROOT_DIR: Final[Path] = Path(__file__).parent.parent.parent.resolve()

# Aggiunta obbligatoria al sys.path per permettere ai test di importare 'src'
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# File di stato
AI_REPORT_FILE: Final[Path] = Path(__file__).parent / ".test_results.json"
STATE_FILE: Final[Path] = Path(__file__).parent / ".test_passed_state.json"


def _build_env(worker_id: str | None = None, with_cov: bool = False) -> dict[str, str]:
    """Costruisce l'environment per i subprocess dei test."""
    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    if worker_id:
        temp_config_dir = Path(tempfile.gettempdir()) / f"syncrojob_test_{worker_id}"
        temp_config_dir.mkdir(parents=True, exist_ok=True)
        env["SYNCROJOB_CONFIG_DIR"] = str(temp_config_dir)
        if with_cov:
            env["COVERAGE_FILE"] = f".coverage.worker.{worker_id}"
    elif "SYNCROJOB_CONFIG_DIR" not in env:
        base_temp = Path(tempfile.gettempdir()) / "syncrojob_global_test_env"
        env["SYNCROJOB_CONFIG_DIR"] = str(base_temp)
    return env


def _get_system_metadata(max_workers: int) -> dict[str, Any]:
    """Raccoglie informazioni sull'ambiente di sistema."""
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "python_version": sys.version.split()[0],
        "cpu_count": multiprocessing.cpu_count(),
        "workers_used": max_workers,
        "root_dir": str(ROOT_DIR),
        "timestamp": datetime.datetime.now().isoformat(),
    }


def _parse_pytest_summary(output: str) -> tuple[int, int]:
    """Estrae (passed, failed) dalla riga di summary di pytest."""
    passed = 0
    failed = 0
    for line in reversed(output.splitlines()):
        if "passed" in line or "failed" in line or "error" in line:
            p_match = re.search(r"(\d+)\s+passed", line)
            f_matches = re.findall(r"(\d+)\s+(?:failed|error)", line)
            if p_match:
                passed = int(p_match.group(1))
            for fm in f_matches:
                failed += int(fm)
            if p_match or f_matches:
                break
    return passed, failed


def _generate_fingerprint(error_type: str, error_message: str) -> str:
    """Genera un hash unico dell'errore per raggruppare fallimenti simili."""
    # Normalizziamo il messaggio rimuovendo timestamp o indirizzi di memoria
    clean_msg = re.sub(r"0x[0-9a-fA-F]+", "0xADDR", error_message)
    clean_msg = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", "TS", clean_msg)
    raw = f"{error_type}:{clean_msg}".encode()
    return hashlib.sha256(raw).hexdigest()


def _extract_traceback_block(lines: list[str], node_id: str) -> str:
    """Estrae il blocco di traceback rilevante per un test specifico."""
    in_block = False
    tb_lines: list[str] = []
    test_name = node_id.split("::")[-1] if "::" in node_id else node_id
    for line in lines:
        if test_name in line and (re.match(r"^[_= ]{5,}", line) or "FAILED" in line):
            in_block = True
            tb_lines = [line]
            continue
        if in_block:
            tb_lines.append(line)
            if re.match(r"^[=]{10,}", line) and len(tb_lines) > 2:
                break
    return "\n".join(tb_lines[-50:]) if tb_lines else ""


def _collect_tests_inprocess(console: Console, mark: str | None = None) -> list[str]:
    """Discovery dei test in-process via pytest --collect-only -q."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests",
        "--collect-only",
        "-q",
        "-o",
        "addopts=",
        "-p",
        "no:sugar",
        "-p",
        "no:cacheprovider",
    ]
    if mark:
        cmd.extend(["-m", mark])

    env = _build_env()
    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,
            timeout=60,
            env=env,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired:
        console.print("[bold red][!] Timeout nella discovery dei test (60s)[/bold red]")
        return []

    node_ids = []
    for line in res.stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("=", "no tests", "ERROR")):
            continue
        if "::" in stripped:
            node_ids.append(stripped)
    return node_ids
