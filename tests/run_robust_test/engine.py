"""Engine di orchestrazione test per il Robust Test Runner."""

from __future__ import annotations

import re
import subprocess
import sys
import time

from .models import FailureDetail, TestResult
from .utils import (
    ROOT_DIR,
    _build_env,
    _extract_traceback_block,
    _generate_fingerprint,
    _parse_pytest_summary,
)


def _worker_task(  # noqa: PLR0913
    target: str,
    timeout: int,
    mark: str | None = None,
    with_cov: bool = False,
    ai_mode: bool = False,
    is_retry: bool = False,
) -> TestResult:
    """Esegue un singolo target di test in un subprocess.

    Args:
        target: Percorso del test o NodeID.
        timeout: Limite di tempo in secondi.
        mark: Eventuale marker pytest per filtrare.
        with_cov: Se True, abilita la coverage.
        ai_mode: Se True, ottimizza per l'IA.
        is_retry: Se True, appende il flag --last-failed.

    Returns:
        TestResult: Il risultato dell'esecuzione.
    """
    worker_id = f"{__import__('os').getpid()}_{int(time.time() * 1000)}"
    cmd = _build_pytest_cmd(target, ai_mode, with_cov, mark, is_retry)

    start = time.time()
    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,
            timeout=timeout,
            check=False,
            env=_build_env(worker_id, with_cov),
            encoding="utf-8",
            errors="replace",
        )
        duration = time.time() - start
        output = res.stdout + res.stderr
        passed, failed = _parse_pytest_summary(output)
        success = res.returncode == 0 and "INTERNALERROR" not in output

        error_msg = _get_error_msg(success, output, res.returncode)
        return TestResult(target, success, duration, passed, failed, error_msg, output)
    except subprocess.TimeoutExpired:
        return TestResult(target, False, time.time() - start, 0, 0, "TIMEOUT", "Execution timed out")
    except Exception as e:
        return TestResult(target, False, 0, 0, 0, str(e), str(e))


def _build_pytest_cmd(
    target: str, ai_mode: bool, with_cov: bool, mark: str | None, is_retry: bool = False
) -> list[str]:
    """Costruisce il comando pytest."""
    tb_style = "long" if ai_mode else "short"
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        target,
        "--no-header",
        "-q",
        f"--tb={tb_style}",
        "-p",
        "no:sugar",
        "-p",
        "no:cacheprovider",
    ]
    if mark:
        cmd.extend(["-m", mark])
    if is_retry:
        cmd.extend(["--last-failed", "--last-failed-no-failures", "all"])
    if not with_cov:
        cmd.extend(["-p", "no:cov", "-o", "addopts="])
    else:
        cmd.extend(["--cov=src", "--cov-append"])
    return cmd


def _get_error_msg(success: bool, output: str, returncode: int) -> str | None:
    """Estrae il messaggio d'errore principale dall'output."""
    if success:
        return None
    for line in reversed(output.splitlines()):
        if any(x in line for x in ("E ", "Error:", "FAILED", "ImportError", "INTERNALERROR")):
            return line.strip()
    return f"Exit code {returncode}"


def _classify_error(error_text: str, full_output: str, node_id: str) -> tuple[str, str, str]:
    """Classifica un errore in tipo, messaggio e categoria semantica.

    Args:
        error_text: Riassunto dell'errore.
        full_output: Output completo del test.
        node_id: Identificatore del test.

    Returns:
        tuple: (Tipo Errore, Messaggio, Categoria)
    """
    error_text = error_text.strip()

    # 1. Priorita' alta
    res = _check_critical_errors(error_text, full_output)
    if res:
        return res

    # 2. Mappatura standard
    for err, cat in {
        "TimeoutError": "timeout",
        "TIMEOUT": "timeout",
        "TypeError": "runtime",
        "ValueError": "runtime",
        "AttributeError": "runtime",
    }.items():
        if err in error_text:
            if err == "TIMEOUT":
                return "TimeoutError", error_text, cat
            return err.replace("Error", "") + "Error", error_text, cat

    # 3. Fallback Regex
    type_match = re.match(r"(\w+Error|\w+Exception):\s*(.*)", error_text)
    if type_match:
        return type_match.group(1), type_match.group(2), "runtime"

    return "UnknownError", error_text or "No error details captured", "runtime"


def _check_critical_errors(error_text: str, full_output: str) -> tuple[str, str, str] | None:
    """Helper per errori critici (complessita' scomposizione)."""
    if "ImportError" in error_text or "ModuleNotFoundError" in error_text:
        return "ImportError", error_text, "import_error"
    if "AssertionError" in error_text or "assert " in error_text.lower():
        return "AssertionError", error_text, "assertion"
    if any(x in full_output.lower() for x in ("segfault", "access violation", "fatal")):
        return "NativeCrash", error_text, "crash"
    return None


def _extract_failures(output: str, target: str) -> list[FailureDetail]:
    """Estrae dettagli strutturati dei fallimenti dall'output pytest.

    Args:
        output: Lo stdout+stderr dei test.
        target: Il file o target analizzato.

    Returns:
        list: Lista di oggetti FailureDetail.
    """
    failures = []
    lines = output.splitlines()
    for line in lines:
        failed_match = re.match(r"FAILED\s+([\S]+::\S+)\s*-?\s*(.*)", line)
        if failed_match:
            failures.append(
                _create_failure_detail(failed_match.group(1), failed_match.group(2), lines, output)
            )
            continue
        if line.strip().startswith("E ") and re.match(r"E\s+\w+Error|E\s+\w+Exception", line.strip()):
            failures.append(_create_failure_detail(target, line.strip()[2:], lines, output))
    return failures


def _create_failure_detail(
    node_id: str, error_summary: str, lines: list[str], full_output: str
) -> FailureDetail:
    """Helper per la creazione di un FailureDetail."""
    error_type, error_message, category = _classify_error(error_summary, full_output, node_id)
    return FailureDetail(
        node_id=node_id,
        file=node_id.split("::")[0],
        test_name=node_id.split("::")[-1] if "::" in node_id else node_id,
        error_type=error_type,
        error_message=error_message,
        traceback=_extract_traceback_block(lines, node_id),
        category=category,
        fingerprint=_generate_fingerprint(error_type, error_message),
        repro_cmd=f"python -m pytest {node_id} -vv --tb=long",
    )
