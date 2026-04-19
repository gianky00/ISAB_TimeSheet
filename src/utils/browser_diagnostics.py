"""
SyncroJob - Browser Diagnostics
Strumenti per diagnosticare e risolvere problemi di avvio dei bot Playwright.
"""

import json
import logging
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

from src.core import config_manager
from src.utils.helpers import cleanup_bot_processes

logger = logging.getLogger("BrowserDiagnostics")


def run_browser_diagnostic(user_data_dir: Path | str) -> dict[str, Any]:
    """
    Esegue una suite completa di test diagnostici sull'ambiente del browser.
    """
    user_data_path = Path(user_data_dir)
    report: dict[str, Any] = {
        "timestamp": datetime.now(UTC).astimezone().isoformat(),
        "os": sys.platform,
        "user_data_dir": str(user_data_path),
        "checks": {},
        "overall_status": "PASS",
    }

    # 1. Verifica Permessi Filesystem
    report["checks"]["filesystem"] = _check_filesystem(user_data_path)

    # 2. Verifica Processi Bloccanti
    report["checks"]["processes"] = _check_processes(user_data_path)

    # 3. Test di Avvio "Bare" (Senza Profilo Persistente)
    report["checks"]["playwright_launch"] = _test_bare_launch()

    # Determina stato finale
    for check in report["checks"].values():
        if check.get("status") == "FAIL":
            report["overall_status"] = "FAIL"
            break

    # Salva il report
    _save_report(report)
    return report


def _check_filesystem(path: Path) -> dict[str, Any]:
    """Verifica accesso e permessi sulla cartella del profilo."""
    result: dict[str, Any] = {"status": "PASS", "details": []}

    if not path.exists():
        try:
            path.mkdir(parents=True, exist_ok=True)
            result["details"].append(f"Directory {path.name} creata.")
        except Exception as e:
            result["status"] = "FAIL"
            result["details"].append(f"Impossibile creare directory: {e}")
            return result

    # Test scrittura
    test_file = path / ".write_test"
    try:
        test_file.write_text("test", encoding="utf-8")
        test_file.unlink()
        result["details"].append("Permessi di scrittura OK.")
    except Exception as e:
        result["status"] = "FAIL"
        result["details"].append(f"Errore scrittura: {e}")

    # Check file di lock
    lock_files = ["SingletonLock", "Lock", "DevToolsActivePort"]
    for lock in lock_files:
        lp = path / lock
        if lp.exists():
            result["details"].append(f"Rilevato file di lock: {lock}")

    return result


def _check_processes(path: Path) -> dict[str, Any]:
    """Rileva processi che potrebbero bloccare la directory."""
    import psutil  # noqa: PLC0415

    result: dict[str, Any] = {"status": "PASS", "details": []}
    blocking_procs = []

    for proc in psutil.process_iter(["name", "cmdline"]):
        try:
            if proc.info["name"] in ("chrome.exe", "msedge.exe", "chromium"):
                cmdline = " ".join(proc.info["cmdline"] or [])
                if str(path).lower() in cmdline.lower():
                    blocking_procs.append(f"{proc.info['name']} (PID: {proc.pid})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if blocking_procs:
        result["status"] = "WARNING"
        result["details"].append(f"Processi bloccanti rilevati: {', '.join(blocking_procs)}")

    return result


def _test_bare_launch() -> dict[str, Any]:
    """Tenta un avvio barebone di Playwright per escludere problemi ai binari."""
    result: dict[str, Any] = {"status": "PASS", "details": []}
    try:
        with sync_playwright() as p:
            # Avvio rapido senza profilo persistente
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("about:blank", timeout=5000)
            browser.close()
            result["details"].append("Avvio barebone Playwright riuscito.")
    except Exception as e:
        result["status"] = "FAIL"
        result["details"].append(f"Fallimento avvio barebone Playwright: {e}")

    return result


def _save_report(report: dict[str, Any]) -> None:
    """Salva il report in logs/browser_debug.json."""
    try:
        log_dir = config_manager.CONFIG_DIR / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        report_path = log_dir / "browser_debug.json"
        with report_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
        logger.info(f"Report diagnostico salvato in: {report_path}")
    except Exception:
        logger.exception("Errore salvataggio report")


def emergency_profile_reset(user_data_dir: Path) -> bool:
    """
    Rinomina la cartella del profilo attuale per forzare Playwright a crearne una nuova.
    """
    if not user_data_dir.exists():
        return False

    try:
        # Assicura cleanup processi prima del reset
        cleanup_bot_processes()

        ts = datetime.now(UTC).astimezone().strftime("%Y%m%d_%H%M%S")
        new_name = user_data_dir.parent / f"{user_data_dir.name}_corrupted_{ts}"

        shutil.move(str(user_data_dir), str(new_name))
        logger.warning(f"Profilo corrotto isolato in: {new_name.name}")
    except Exception:
        logger.exception("Impossibile resettare il profilo")
        return False
    else:
        return True
