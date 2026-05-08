import os
import shlex
import subprocess
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


MAX_OUTPUT_LEN = 2000


def run_command(name: str, command: str) -> bool:
    console.print(f"\n[bold blue]🚀 Eseguendo {name}...[/bold blue]")
    try:
        # Split command for non-shell execution to improve security
        cmd_args = shlex.split(command)

        result = subprocess.run(
            cmd_args, check=False, shell=False, capture_output=True, text=True, encoding="utf-8"
        )
        if result.returncode == 0:
            console.print(f"[bold green]✅ {name} completato con successo.[/bold green]")
            if result.stdout:
                console.print(
                    result.stdout[:MAX_OUTPUT_LEN] + "..."
                    if len(result.stdout) > MAX_OUTPUT_LEN
                    else result.stdout
                )
            return True
        console.print(f"[bold red]❌ {name} ha rilevato problemi (Exit Code: {result.returncode})[/bold red]")
        console.print(
            result.stdout[:MAX_OUTPUT_LEN] + "..." if len(result.stdout) > MAX_OUTPUT_LEN else result.stdout
        )
        console.print(result.stderr)
        return False
    except Exception as e:
        console.print(f"[bold red]💥 Errore critico durante {name}: {e}[/bold red]")
        return False


def main() -> None:
    console.print(
        Panel(
            "[bold white]ISAB TimeSheet - Enterprise Quality Check[/bold white]",
            border_style="cyan",
            expand=True,
        )
    )

    venv_bin = os.path.join(os.getcwd(), ".venv", "Scripts")

    steps: list[tuple[str, str]] = [
        ("RUF Linter", f'"{os.path.join(venv_bin, "ruff.exe")}" check . --fix'),
        ("RUF Formatter", f'"{os.path.join(venv_bin, "ruff.exe")}" format .'),
        ("MYPY Type Check", f'"{os.path.join(venv_bin, "mypy.exe")}" .'),
        (
            "XENON Complexity",
            f'"{os.path.join(venv_bin, "xenon.exe")}" --max-absolute B --max-modules B --max-average A src',
        ),
        ("RADON CC Analysis", f'"{os.path.join(venv_bin, "radon.exe")}" cc src -a -s'),
        ("BANDIT Security", f'"{os.path.join(venv_bin, "bandit.exe")}" -r src'),
    ]

    table = Table(title="Report Qualità Finale")
    table.add_column("Tool", style="cyan")
    table.add_column("Stato", style="magenta")

    all_passed = True
    for name, cmd in steps:
        success = run_command(name, cmd)
        table.add_row(name, "✅ PASS" if success else "❌ FAIL")
        if not success:
            all_passed = False

    console.print("\n")
    console.print(table)

    if all_passed:
        console.print(
            "\n[bold green]🏆 ECCELLENZA RAGGIUNTA: Il codice rispetta tutti gli standard Enterprise.[/bold green]"
        )
    else:
        console.print(
            "\n[bold yellow]⚠️ ATTENZIONE: Alcuni controlli sono falliti. Revisiona il codice sopra.[/bold yellow]"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
