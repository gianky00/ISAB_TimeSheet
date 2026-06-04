"""Logica di orchestrazione principale per il Robust Test Runner."""

from __future__ import annotations

import contextlib
import json
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool
from typing import TYPE_CHECKING, Any

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from .engine import _extract_failures, _worker_task
from .reporting import finish_ai, finish_human
from .utils import (
    AI_REPORT_FILE,
    MAX_WORKERS,
    ROOT_DIR,
    STATE_FILE,
    _collect_tests_inprocess,
    _get_system_metadata,
)

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


class UltraRunner:
    """Orchestratore per l'esecuzione robusta e parallela dei test."""

    def __init__(self, console: Console, ai_mode: bool = False) -> None:
        """Inizializza il runner.

        Args:
            console: L'oggetto console di Rich per l'output.
            ai_mode: Se True, abilita l'output strutturato per l'IA.
        """
        self.console = console
        self.ai_mode = ai_mode
        self.failed_list: list[dict[str, str | None]] = []
        self.failure_details: list[Any] = []
        self.file_results: list[Any] = []
        self.total_passed = 0
        self.total_failed = 0
        self.start_time = 0.0
        self.strategy = "PARALLELO"
        self.passed_targets: set[str] = set()
        self._exit_code = 0

    def load_state(self, resume: bool) -> None:
        """Carica lo stato dei test passati dal file persistente.

        Args:
            resume: Se True, tenta di caricare lo stato precedente.
        """
        if resume and STATE_FILE.exists():
            try:
                data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
                self.passed_targets = set(data.get("passed", []))
                if not self.ai_mode:
                    self.console.print(
                        f"  [dim][RESUME] Caricati {len(self.passed_targets)} test passati.[/dim]"
                    )
            except Exception:
                self.passed_targets = set()
        else:
            self.passed_targets = set()
            with contextlib.suppress(FileNotFoundError):
                STATE_FILE.unlink()

    def save_state(self) -> None:
        """Salva lo stato corrente dei test passati su disco."""
        if self.passed_targets:
            STATE_FILE.write_text(
                json.dumps({"passed": list(self.passed_targets)}, indent=2), encoding="utf-8"
            )

    def run_sequenziale(self, targets: list[str], args: argparse.Namespace) -> None:
        """Esegue i test in modalità sequenziale (uno ad uno).

        Args:
            targets: Lista di target (file/cartelle) da testare.
            args: Gli argomenti della riga di comando.
        """
        self.strategy = "SEQUENZIALE"
        if not self.ai_mode:
            self.console.rule("[bold magenta]MODALITÀ SEQUENZIALE[/bold magenta]")
            self.console.print(f"Esecuzione mirata di [bold cyan]{len(targets)}[/bold cyan] target\n")

        targets = [t for t in targets if t not in self.passed_targets]
        if not targets:
            self._handle_no_tests(0)
            return

        self.start_time = time.time()
        for target in targets:
            self._execute_with_retry(target, args)
            if self._should_stop_early(args):
                break

        self._finalize(len(targets), args.cov, 1)

    def run_parallelo(self, args: argparse.Namespace) -> None:
        """Esegue l'intera suite in modalità parallela con recupero isolato.

        Args:
            args: Gli argomenti della riga di comando.
        """
        self.strategy = "PARALLELO"
        if not self.ai_mode:
            self.console.rule("[bold cyan]MODALITÀ PARALLELA[/bold cyan]")

        node_ids = self._discover_tests(args.mark)
        if not node_ids:
            return

        files_map = self._map_nodes_to_files(node_ids)
        queue = sorted(files_map.keys(), key=lambda x: len(files_map[x]), reverse=True)
        queue = [f for f in queue if f not in self.passed_targets]

        if not queue:
            self._handle_no_tests(MAX_WORKERS)
            return

        self.start_time = time.time()
        isolation_queue: list[str] = []

        # Fase 1: Esecuzione Parallela
        self._execute_parallel_phase(queue, isolation_queue, args)

        # Fase 2: Isolamento (Riesecuzione sequenziale dei falliti)
        if isolation_queue:
            self._execute_isolation_phase(isolation_queue, files_map, args)

        self._finalize(len(queue), args.cov, MAX_WORKERS)

    def _discover_tests(self, mark: str | None) -> list[str]:
        """Esegue la discovery dei test con feedback visivo."""
        with self.console.status("[bold green]Discovery dei test...", spinner="bouncingBar") as status:
            node_ids = _collect_tests_inprocess(self.console, mark=mark)
            if not node_ids:
                status.stop()
                if not self.ai_mode:
                    self.console.print("[bold red]x Nessun test trovato![/bold red]")
                if self.ai_mode:
                    finish_ai(self, 0, AI_REPORT_FILE, ROOT_DIR, _get_system_metadata(MAX_WORKERS))
            return node_ids

    def _map_nodes_to_files(self, node_ids: list[str]) -> dict[str, list[str]]:
        """Mappa i NodeID di pytest ai rispettivi file sorgente."""
        files_map = defaultdict(list)
        for nid in node_ids:
            files_map[nid.split("::")[0]].append(nid)
        return files_map

    def _execute_with_retry(self, target: str, args: argparse.Namespace) -> None:
        """Esegue un target con la logica di retry configurata."""
        max_attempts = 1 + args.retry
        for attempt in range(max_attempts):
            res = _worker_task(target, args.timeout, args.mark, args.cov, self.ai_mode, attempt > 0)
            if res.success:
                self.file_results.append(res)
                self.passed_targets.add(target)
                self.save_state()
                self.total_passed += res.passed
                return
            if attempt == max_attempts - 1:
                self.file_results.append(res)
                self.total_failed += res.failed or 1
                if res.full_output:
                    self.failure_details.extend(_extract_failures(res.full_output, target))

    def _execute_parallel_phase(
        self, queue: list[str], isolation_queue: list[str], args: argparse.Namespace
    ) -> None:
        """Gestisce il pool di processi per l'esecuzione parallela."""
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            MofNCompleteColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=self.console,
            disable=self.ai_mode,
        )

        with progress:
            task_id = progress.add_task("[cyan]Esecuzione...", total=len(queue))
            try:
                with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    futures = {
                        executor.submit(_worker_task, f, args.timeout, args.mark, args.cov, self.ai_mode): f
                        for f in queue
                    }
                    for future in as_completed(futures):
                        target = futures[future]
                        try:
                            res = future.result()
                            self.file_results.append(res)
                            if not res.success:
                                isolation_queue.append(target)
                                if self.ai_mode and res.full_output:
                                    self.failure_details.extend(_extract_failures(res.full_output, target))
                            else:
                                self.passed_targets.add(target)
                                self.save_state()
                                self.total_passed += res.passed
                                self.total_failed += res.failed
                            progress.advance(task_id)

                            if self._should_stop_early(args, isolation_queue):
                                executor.shutdown(wait=False, cancel_futures=True)
                                break
                        except Exception:
                            isolation_queue.append(target)
                            progress.advance(task_id)
            except (BrokenProcessPool, KeyboardInterrupt):
                if not self.ai_mode:
                    self.console.print("\n[bold orange3][!] Runner interrotto.[/bold orange3]")
                sys.exit(130)

    def _execute_isolation_phase(
        self, isolation_queue: list[str], files_map: dict[str, list[str]], args: argparse.Namespace
    ) -> None:
        """Riesegue sequenzialmente i file falliti in parallelo."""
        if self.ai_mode:
            for target in isolation_queue:
                if self._should_stop_early(args):
                    break
                self._isolate_target(target, files_map[target], args)
            return

        self.console.print("\n")
        total_iso = len(isolation_queue)
        self.console.rule(f"[bold yellow]FASE ISOLAMENTO ({total_iso} file)[/bold yellow]")

        iso_progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold yellow][{task.fields[idx]}/{task.fields[total_field]}][/bold yellow]"),
            TextColumn("[bold white]Analisi:[/bold white] {task.description}"),
            BarColumn(bar_width=30, style="yellow"),
            TimeElapsedColumn(),
            console=self.console,
        )

        with iso_progress:
            task_iso = iso_progress.add_task("", total=total_iso, idx=0, total_field=total_iso)
            for idx, target in enumerate(isolation_queue, 1):
                if self._should_stop_early(args):
                    break
                iso_progress.update(task_iso, description=target, idx=idx)
                if self._isolate_target(target, files_map[target], args):
                    self.passed_targets.add(target)
                    self.save_state()
                iso_progress.advance(task_iso)

    def _isolate_target(self, target: str, nodes: list[str], args: argparse.Namespace) -> bool:
        """Analizza un singolo file in isolamento. Ritorna True se tutti i nodi passano."""
        target_success = True
        for node in nodes:
            max_attempts = 1 + args.retry
            node_passed = False
            res = None
            for attempt in range(max_attempts):
                res = _worker_task(node, args.timeout + 30, args.mark, args.cov, self.ai_mode, attempt > 0)
                if res and res.success:
                    self.total_passed += res.passed
                    self.file_results.append(res)
                    node_passed = True
                    break

            if not node_passed:
                target_success = False
                if res is not None:
                    self.total_passed += res.passed
                    self.total_failed += res.failed or 1
                    self.failed_list.append({"id": node, "error": res.error_msg})
                    self.file_results.append(res)
                    if self.ai_mode and res.full_output:
                        self.failure_details.extend(_extract_failures(res.full_output, node))
                else:
                    self.total_failed += 1

            if self._should_stop_early(args):
                break
        return target_success

    def _should_stop_early(self, args: argparse.Namespace, isolation_queue: list[str] | None = None) -> bool:
        """Determina se l'esecuzione deve essere interrotta (Fail-Fast)."""
        current_fails = self.total_failed
        if isolation_queue is not None:
            current_fails += len(isolation_queue)

        if args.exitfirst and current_fails > 0:
            return True
        return bool(args.max_fail > 0 and current_fails >= args.max_fail)

    def _handle_no_tests(self, workers: int) -> None:
        """Gestisce il caso in cui non ci siano test da eseguire."""
        if not self.ai_mode:
            self.console.print("[bold green]Tutti i test già passati.[/bold green]")
        if self.ai_mode:
            finish_ai(self, 0, AI_REPORT_FILE, ROOT_DIR, _get_system_metadata(workers))

    def _finalize(self, total_files: int, with_cov: bool, workers: int) -> None:
        """Conclude l'esecuzione e genera il report finale."""
        if self.ai_mode:
            finish_ai(self, total_files, AI_REPORT_FILE, ROOT_DIR, _get_system_metadata(workers))
        else:
            finish_human(self, time.time() - self.start_time, with_cov, ROOT_DIR, self.console)
            sys.exit(1 if self.total_failed > 0 else 0)
