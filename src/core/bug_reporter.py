import json
import logging
import os
import platform
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from src.core.config_manager import CONFIG_DIR, get_version

logger = logging.getLogger(__name__)


class BugReporter:
    """
    Gestisce la raccolta di log e informazioni di debug per la segnalazione di bug.
    Crea un pacchetto ZIP contenente:
    - Log applicativi (syncrojob.log, crash.log)
    - Log errori bot (screenshot/html recenti)
    - Info di sistema (OS, versione app, config parziale)
    """

    @staticmethod
    def collect_diagnostics() -> Tuple[Optional[Path], str]:
        """
        Raccoglie tutti i file diagnostici e crea un archivio ZIP.

        Returns:
            Tuple[Path, str]: (Percorso dello ZIP creato, Messaggio di stato)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"syncrojob_report_{timestamp}.zip"
            report_path = CONFIG_DIR / "reports" / report_name

            # Assicura che la directory reports esista
            report_path.parent.mkdir(parents=True, exist_ok=True)

            log_dir = CONFIG_DIR / "logs"
            if not log_dir.exists():
                return None, "Directory logs non trovata."

            with zipfile.ZipFile(report_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # 1. Aggiungi file di log principali
                for log_file in ["syncrojob.log", "crash.log"]:
                    f = log_dir / log_file
                    if f.exists():
                        zipf.write(f, arcname=f"logs/{log_file}")

                # 2. Aggiungi contenuto cartella errors (ultimi 5 errori x evitare gonfiare lo zip)
                error_dir = log_dir / "errors"
                if error_dir.exists():
                    files = sorted(
                        error_dir.glob("*"),
                        key=lambda x: x.stat().st_mtime,
                        reverse=True,
                    )
                    # Prendi gli ultimi 10 file (screenshot/html)
                    for f in files[:10]:
                        zipf.write(f, arcname=f"logs/errors/{f.name}")

                # 3. System Info Report
                sys_info = {
                    "app_version": get_version(),
                    "os": platform.system(),
                    "os_release": platform.release(),
                    "os_version": platform.version(),
                    "machine": platform.machine(),
                    "timestamp": datetime.now().isoformat(),
                    "python_version": platform.python_version(),
                    "processor": platform.processor(),
                    "env": {
                        k: v
                        for k, v in os.environ.items()
                        if "TOKEN" not in k and "KEY" not in k and "PASS" not in k
                    },  # Filter sensitive
                }

                # Try to get Memory Info
                try:
                    import psutil

                    mem = psutil.virtual_memory()
                    sys_info["memory"] = {
                        "total": f"{mem.total / (1024**3):.2f} GB",
                        "available": f"{mem.available / (1024**3):.2f} GB",
                        "percent": f"{mem.percent}%",
                    }
                except ImportError:
                    sys_info["memory"] = "psutil not installed"
                except Exception as e:
                    sys_info["memory_error"] = str(e)

                zipf.writestr("system_info.json", json.dumps(sys_info, indent=2))

            logger.info(f"Bug report creato: {report_path}")
            return report_path, "Report generato con successo."

        except Exception as e:
            logger.error("Errore durante la creazione del bug report", exc_info=True)
            return None, f"Errore creazione report: {e}"

    @staticmethod
    def cleanup_old_reports(max_reports: int = 5):
        """Mantiene solo gli ultimi N report per risparmiare spazio."""
        try:
            reports_dir = CONFIG_DIR / "reports"
            if not reports_dir.exists():
                return

            reports = sorted(
                reports_dir.glob("*.zip"), key=lambda x: x.stat().st_mtime, reverse=True
            )
            for r in reports[max_reports:]:
                try:
                    r.unlink()
                except Exception:
                    pass
        except Exception:
            pass
