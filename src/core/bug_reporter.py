# ruff: noqa: TRY300, PLR2004
"""
SyncroJob - Enhanced Bug Reporter

Raccoglie diagnostica completa per segnalazioni bug, integrando:
- Log strutturati (app.json, app.log, errors.json)
- Analytics report (anomalie, health score)
- Audit trail (ultime azioni)
- Info sistema
"""

import json
import logging
import os
import platform
import zipfile
from contextlib import suppress
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from src.core.audit import AuditManager
from src.core.logging import generate_analytics_report, view_trace
from src.core.paths import CONFIG_DIR, get_version

logger = logging.getLogger(__name__)


class BugReporter:
    """
    Gestisce la raccolta di log e informazioni di debug per la segnalazione di bug.

    Crea un pacchetto ZIP contenente:
    - Log strutturati (app.json, app.log, errors.json, performance.jsonl)
    - Log errori bot (screenshot/html recenti)
    - Analytics report (anomalie, pattern, health score)
    - Audit trail (ultime 50 azioni)
    - Info di sistema (OS, versione app, memoria)
    """

    @staticmethod
    def collect_diagnostics(
        include_structured_logs: bool = True,
        include_analytics: bool = True,
        include_audit: bool = True,
        trace_id: str | None = None,
        hours: int = 24,
        **kwargs: Any,
    ) -> tuple[Path | None, str, list[str]]:
        """
        Raccoglie tutti i file diagnostici e crea un archivio ZIP.

        Args:
          include_structured_logs: Includi log strutturati
          include_analytics: Includi report analytics (anomalie, health)
          include_audit: Includi audit trail recente
          trace_id: Trace ID specifico per debug mirato (opzionale)
          hours: Ore di log da includere

        Returns:
          Tuple[Path, str, List[str]]: (Path ZIP, messaggio, lista file inclusi)
        """
        # Supporto retrocompatibilità
        if "include_enterprise_logs" in kwargs:
            include_structured_logs = kwargs["include_enterprise_logs"]

        included_files: list[str] = []

        try:
            timestamp = datetime.now(UTC).astimezone().strftime("%Y%m%d_%H%M%S")
            report_name = f"syncrojob_report_{timestamp}.zip"
            report_path = CONFIG_DIR / "reports" / report_name

            # Assicura che la directory reports esista
            report_path.parent.mkdir(parents=True, exist_ok=True)

            log_dir = CONFIG_DIR / "logs"

            with zipfile.ZipFile(report_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # 1. Structured Logs
                if include_structured_logs and log_dir.exists():
                    included_files.extend(BugReporter._add_structured_logs(zipf, log_dir))

                # 2. Bot Errors (screenshot/html)
                error_dir = log_dir / "errors"
                if error_dir.exists():
                    included_files.extend(BugReporter._add_bot_errors(zipf, error_dir))

                # 3. Analytics Report
                if include_analytics:
                    analytics_files = BugReporter._add_analytics_report(zipf, hours)
                    included_files.extend(analytics_files)

                # 4. Audit Trail
                if include_audit:
                    audit_files = BugReporter._add_audit_trail(zipf)
                    included_files.extend(audit_files)

                # 5. Trace Timeline (se specificato)
                if trace_id:
                    trace_files = BugReporter._add_trace_timeline(zipf, trace_id)
                    included_files.extend(trace_files)

                # 6. System Info
                sys_info = BugReporter._collect_system_info()
                zipf.writestr("system_info.json", json.dumps(sys_info, indent=2))
                included_files.append("system_info.json")

            logger.info(f"Bug report creato: {report_path} ({len(included_files)} file)")
            return report_path, "Report generato con successo.", included_files

        except Exception as e:
            logger.error("Errore durante la creazione del bug report", exc_info=True)
            return None, f"Errore creazione report: {e}", []

    @staticmethod
    def _add_structured_logs(zipf: zipfile.ZipFile, log_dir: Path) -> list[str]:
        """Aggiunge log strutturati allo ZIP."""
        added = []

        # Log strutturati in application/
        app_dir = log_dir / "application"
        if app_dir.exists():
            for log_file in ("app.json", "app.log"):
                f = app_dir / log_file
                if f.exists():
                    zipf.write(f, arcname=f"logs/application/{log_file}")
                    added.append(f"logs/application/{log_file}")

        # Errors JSON
        errors_json = log_dir / "errors" / "errors.json"
        if errors_json.exists():
            zipf.write(errors_json, arcname="logs/errors/errors.json")
            added.append("logs/errors/errors.json")

        # Performance metrics
        metrics_dir = log_dir / "metrics"
        if metrics_dir.exists():
            perf_file = metrics_dir / "performance.jsonl"
            if perf_file.exists():
                zipf.write(perf_file, arcname="logs/metrics/performance.jsonl")
                added.append("logs/metrics/performance.jsonl")

        # Startup log
        startup_log = log_dir / "startup.log"
        if startup_log.exists():
            zipf.write(startup_log, arcname="logs/startup.log")
            added.append("logs/startup.log")

        return added

    @staticmethod
    def _add_bot_errors(zipf: zipfile.ZipFile, error_dir: Path) -> list[str]:
        """Aggiunge ultimi errori bot (screenshot/html)."""
        added = []
        files = sorted(
            [f for f in error_dir.glob("*") if f.is_file() and f.suffix != ".json"],
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )
        # Prendi gli ultimi 10 file
        for f in files[:10]:
            zipf.write(f, arcname=f"logs/errors/{f.name}")
            added.append(f"logs/errors/{f.name}")
        return added

    @staticmethod
    def _add_analytics_report(zipf: zipfile.ZipFile, hours: int) -> list[str]:
        """Aggiunge report analytics con anomalie e health score."""
        try:
            report = generate_analytics_report(hours=hours)

            # Converti dataclass in dict
            report_dict = {
                "generated_at": datetime.now(UTC).isoformat(),
                "hours_analyzed": hours,
                "health_score": report.health_score,
                "anomalies": [asdict(a) for a in report.anomalies],
                "patterns": [asdict(p) for p in report.patterns],
            }

            zipf.writestr(
                "analytics_report.json",
                json.dumps(report_dict, indent=2, default=str),
            )
            return ["analytics_report.json"]

        except Exception as e:
            logger.warning(f"Impossibile generare analytics report: {e}")
            return []

    @staticmethod
    def _add_audit_trail(zipf: zipfile.ZipFile, limit: int = 50) -> list[str]:
        """Aggiunge audit trail recente."""
        try:
            manager = AuditManager.instance()
            actions = manager.get_logs(limit=limit)

            audit_data = {
                "generated_at": datetime.now(UTC).isoformat(),
                "total_actions": len(actions),
                "actions": actions,
            }

            zipf.writestr(
                "audit_trail.json",
                json.dumps(audit_data, indent=2, default=str),
            )
            return ["audit_trail.json"]

        except Exception as e:
            logger.warning(f"Impossibile generare audit trail: {e}")
            return []

    @staticmethod
    def _add_trace_timeline(zipf: zipfile.ZipFile, trace_id: str) -> list[str]:
        """Aggiunge timeline di un trace specifico."""
        try:
            timeline = view_trace(trace_id)

            if not timeline:
                return []

            trace_data = {
                "trace_id": trace_id,
                "generated_at": datetime.now(UTC).isoformat(),
                "events_count": len(timeline),
                "events": timeline,
            }

            zipf.writestr(
                f"trace_{trace_id[:8]}.json",
                json.dumps(trace_data, indent=2, default=str),
            )
            return [f"trace_{trace_id[:8]}.json"]

        except Exception as e:
            logger.warning(f"Impossibile generare trace timeline: {e}")
            return []

    @staticmethod
    def _collect_system_info() -> dict[str, Any]:
        """Raccoglie informazioni di sistema."""
        sys_info: dict[str, Any] = {
            "app_version": get_version(),
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "timestamp": datetime.now(UTC).astimezone().isoformat(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
        }

        # Filtra variabili ambiente sensibili
        safe_env = {
            k: v
            for k, v in os.environ.items()
            if not any(
                s in k.upper() for s in ("TOKEN", "KEY", "PASS", "SECRET", "API", "AUTH", "CREDENTIAL")
            )
        }
        sys_info["env_filtered"] = safe_env

        # Memory Info
        try:
            if PSUTIL_AVAILABLE:
                mem = psutil.virtual_memory()
                sys_info["memory"] = {
                    "total": f"{mem.total / (1024**3):.2f} GB",
                    "available": f"{mem.available / (1024**3):.2f} GB",
                    "percent": f"{mem.percent}%",
                }

                # CPU Info
                sys_info["cpu"] = {
                    "cores_physical": psutil.cpu_count(logical=False),
                    "cores_logical": psutil.cpu_count(logical=True),
                    "usage_percent": psutil.cpu_percent(interval=0.1),
                }

                # Disk Info
                disk = psutil.disk_usage("/")
                sys_info["disk"] = {
                    "total": f"{disk.total / (1024**3):.2f} GB",
                    "free": f"{disk.free / (1024**3):.2f} GB",
                    "percent": f"{disk.percent}%",
                }
        except ImportError:
            sys_info["memory"] = "psutil not installed"
        except Exception as e:
            sys_info["system_info_error"] = str(e)

        return sys_info

    @staticmethod
    def cleanup_old_reports(max_reports: int = 5) -> None:
        """Mantiene solo gli ultimi N report per risparmiare spazio."""
        with suppress(Exception):
            reports_dir = CONFIG_DIR / "reports"
            if not reports_dir.exists():
                return

            reports = sorted(
                reports_dir.glob("*.zip"),
                key=lambda x: x.stat().st_mtime,
                reverse=True,
            )
            for r in reports[max_reports:]:
                with suppress(Exception):
                    r.unlink()

    @staticmethod
    def get_estimated_size(
        include_structured_logs: bool = True,
        include_analytics: bool = True,
        include_audit: bool = True,
    ) -> str:
        """Stima dimensione del report ZIP."""
        size_kb = 50  # Base (system_info)

        log_dir = CONFIG_DIR / "logs"

        if include_structured_logs and log_dir.exists():
            app_dir = log_dir / "application"
            if app_dir.exists():
                for f in app_dir.glob("*"):
                    size_kb += f.stat().st_size // 1024

        if include_analytics:
            size_kb += 10  # Analytics JSON

        if include_audit:
            size_kb += 20  # Audit JSON

        if size_kb < 1024:
            return f"~{size_kb} KB"
        return f"~{size_kb / 1024:.1f} MB"
