"""Logica di reporting e UI Rich per il Robust Test Runner."""

from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .models import AIReport
from .utils import MAX_OUTPUT_CHARS

if TYPE_CHECKING:
    from pathlib import Path

    from rich.console import Console


def finish_ai(
    runner: Any, total_files: int, ai_report_file: Path, root_dir: Path, system_metadata: dict[str, Any]
) -> None:
    """Genera e stampa l'output JSON strutturato per l'IA.
    Args:
        runner: L'istanza del runner.
        total_files: Numero totale di file processati.
        ai_report_file: Percorso del file di report JSON.
        root_dir: Directory radice del progetto.
        system_metadata: Metadati dell'ambiente di sistema.
    """
    from collections import defaultdict

    duration = time.time() - runner.start_time
    seen: set[str] = set()
    unique_failures = []
    clusters = defaultdict(list)
    for fd in runner.failure_details:
        if fd.node_id not in seen:
            seen.add(fd.node_id)
            unique_failures.append(fd)
            clusters[fd.fingerprint].append(fd.node_id)
    report = AIReport(
        success=runner.total_failed == 0 and not unique_failures,
        total_passed=runner.total_passed,
        total_failed=runner.total_failed,
        duration=duration,
        strategy=runner.strategy,
        total_files=total_files,
        failures=[asdict(f) for f in unique_failures],
        failure_clusters=dict(clusters),
        file_results=[
            {
                "target": r.target,
                "success": r.success,
                "duration": round(r.duration, 3),
                "passed": r.passed,
                "failed": r.failed,
                "error_msg": (r.error_msg[:MAX_OUTPUT_CHARS] if r.error_msg else None),
            }
            for r in sorted(runner.file_results, key=lambda x: x.duration, reverse=True)
        ],
        system_metadata=system_metadata,
    )
    report_dict = asdict(report)
    ai_report_file.write_text(json.dumps(report_dict, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.stdout.write(json.dumps(report_dict, indent=2, ensure_ascii=False) + "\n")
    sys.stdout.flush()
    os_exit_code = 0 if report.success else 1
    os._exit(os_exit_code)


def finish_human(runner: Any, duration: float, with_cov: bool, root_dir: Path, console: Console) -> None:
    """Genera il report tabellare Rich per gli utenti umani.
    Args:
        runner: L'istanza del runner.
        duration: Durata totale in secondi.
        with_cov: Se True, tenta di generare report di coverage.
        root_dir: Directory radice del progetto.
        console: Console Rich per l'output.
    """
    console.print("\n")
    console.rule("[bold green]ESECUZIONE COMPLETATA[/bold green]")
    if runner.file_results:
        table = Table(title="Risultati per File", title_style="bold cyan", box=None)
        table.add_column("File di Test", style="dim", width=60)
        table.add_column("Status", justify="center", width=10)
        table.add_column("P", justify="right", width=4)
        table.add_column("F", justify="right", width=4)
        table.add_column("Tempo", justify="right", width=10)
        table.add_column("Dettaglio Errore", style="dim italic red", overflow="ellipsis")
        for r in sorted(runner.file_results, key=lambda x: x.duration, reverse=True):
            status = "[bold green]PASS[/bold green]" if r.success else "[bold red]FAIL[/bold red]"
            table.add_row(
                r.target,
                status,
                str(r.passed),
                str(r.failed),
                f"{r.duration:.2f}s",
                (r.error_msg or "").replace("\n", " "),
            )
        console.print(table)
    summary_text = Text.assemble(
        ("Totale: ", "bold"),
        (f"{runner.total_passed} passed", "green"),
        (", ", ""),
        (f"{runner.total_failed} failed", "red"),
        (f" in {duration:.2f}s", "bold"),
    )
    console.print(
        Panel(summary_text, expand=False, border_style="green" if runner.total_failed == 0 else "red")
    )
    if with_cov:
        _generate_coverage_reports(root_dir, console)
    if runner.failed_list:
        console.print(f"\n[bold red]Suite fallita con {len(runner.failed_list)} errori:[/bold red]")
        for f in runner.failed_list:
            console.print(f"  [red]•[/red] [bold white]{f['id']}:[/bold white] [dim]{f['error']}[/dim]")
    else:
        console.print("\n[bold green][OK] Suite completata con successo![/bold green]")


def _generate_coverage_reports(root_dir: Path, console: Console) -> None:
    """Helper interno per la generazione dei report coverage."""
    console.print("\n")
    console.rule("[bold cyan]REPORT COPERTURA[/bold cyan]")
    with console.status("[bold blue]Generazione report coverage...", spinner="bouncingBall"):
        with contextlib.suppress(Exception):
            subprocess.run([sys.executable, "-m", "coverage", "combine"], check=False, cwd=root_dir)
            subprocess.run([sys.executable, "-m", "coverage", "report", "-m"], check=False, cwd=root_dir)
            subprocess.run([sys.executable, "-m", "coverage", "html"], check=False, cwd=root_dir)
