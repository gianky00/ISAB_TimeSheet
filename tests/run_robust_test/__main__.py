"""Entry point principale per il Robust Test Runner modulare."""

from __future__ import annotations

import argparse
import contextlib
import multiprocessing
import subprocess
import sys

from rich.console import Console
from rich.panel import Panel

from .runner import UltraRunner
from .utils import ROOT_DIR, SEQUENZIALE_THRESHOLD, STATE_FILE

console = Console()


def _parse_args() -> argparse.Namespace:
    """Configura e analizza gli argomenti della riga di comando."""
    parser = argparse.ArgumentParser(
        description=(
            "Ultra Test Runner V5.2 (The Apex Runner)\n"
            "========================================\n"
            "Sistema ibrido per l'orchestrazione dei test.\n"
            "Usa PARALLELO mode (tutti i core) per >5 target.\n"
            "Usa SEQUENZIALE mode (live debug) per <=5 target.\n\n"
            "Workflow Consigliati:\n"
            "  [Fix Iterativo IA] : python -m tests.run_robust_test --ai --resume --max-fail 1\n"
            "  [Analisi Finale]   : python -m tests.run_robust_test --cov\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("targets", nargs="*", help="File, cartelle o NodeID da testare.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Forza la pulizia dei file di coverage e cancella lo stato del --resume.",
    )
    parser.add_argument(
        "--timeout", type=int, default=120, help="Timeout rigido per ogni singolo worker (default: 120s)."
    )
    parser.add_argument("-m", "--mark", help="Passato a pytest: esegue solo i test con un marker specifico.")
    parser.add_argument(
        "--cov",
        action="store_true",
        help="Esegue la suite generando il report di copertura HTML/Terminal.\n[!] MUTUALMENTE ESCLUSIVO con --ai.",
    )
    parser.add_argument(
        "--retry", type=int, default=0, help="Numero di esecuzioni aggiuntive in caso di fallimento."
    )
    parser.add_argument(
        "--ai",
        action="store_true",
        help="Modalita' headless ottimizzata per IA.\n[!] MUTUALMENTE ESCLUSIVO con --cov.",
    )
    parser.add_argument(
        "--resume", action="store_true", help="Legge lo stato dei test superati in precedenza e li salta."
    )
    parser.add_argument(
        "-x", "--exitfirst", action="store_true", help="Arresta l'intero runner al primo fallimento."
    )
    parser.add_argument("--max-fail", type=int, default=0, help="Stop dopo N fallimenti.")
    parser.add_argument(
        "-t", "--test", action="store_true", help="Scorciatoia IA: equivale a --ai --resume --max-fail 1."
    )
    args = parser.parse_args()
    if args.test:
        args.ai = True
        args.resume = True
        if args.max_fail == 0:
            args.max_fail = 1
    return args


def _enable_windows_ansi() -> None:
    """Abilita il supporto ANSI su Windows legacy."""
    if sys.platform == "win32":
        import ctypes

        with contextlib.suppress(Exception):
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def _handle_reset() -> None:
    """Esegue la pulizia dei file di stato e copertura."""
    with contextlib.suppress(Exception):
        subprocess.run([sys.executable, "-m", "coverage", "erase"], check=False, cwd=ROOT_DIR)
    with contextlib.suppress(FileNotFoundError):
        STATE_FILE.unlink()


def main() -> None:
    """Funzione principale per gestire la CLI e avviare il runner."""
    multiprocessing.freeze_support()
    args = _parse_args()

    if not args.ai:
        _enable_windows_ansi()
    else:
        console.quiet = True

    if args.ai and args.cov:
        err_console = Console(stderr=True)
        err_console.print(
            Panel(
                "[bold red][ERROR] I flag --ai e --cov sono mutualmente esclusivi.[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    if args.reset:
        _handle_reset()

    runner = UltraRunner(console=console, ai_mode=args.ai)
    runner.load_state(args.resume)

    try:
        if args.targets and len(args.targets) <= SEQUENZIALE_THRESHOLD:
            runner.run_sequenziale(args.targets, args)
        else:
            runner.run_parallelo(args)
    except KeyboardInterrupt:
        if not args.ai:
            console.print(
                "\n[bold orange3][!] Runner interrotto dall'utente. Uscita pulita...[/bold orange3]"
            )
        sys.exit(130)


if __name__ == "__main__":
    main()
