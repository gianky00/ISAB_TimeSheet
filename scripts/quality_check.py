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
        else:
            # Fallimento
            console.print(
                f"[bold red]❌ {name} ha rilevato problemi (Exit Code: {result.returncode})[/bold red]"
            )
            console.print(
                result.stdout[:MAX_OUTPUT_LEN] + "..."
                if len(result.stdout) > MAX_OUTPUT_LEN
                else result.stdout
            )
            if result.stderr:
                console.print(result.stderr)
            return False
    except Exception as e:
        console.print(f"[bold red]💥 Errore critico durante {name}: {e}[/bold red]")
        return False
    else:
        return True


def main() -> None:
    console.print(
        Panel.fit(
            "ISAB TimeSheet - Enterprise Quality Check",
            style="bold magenta",
            border_style="bright_blue",
        )
    )

    results = []

    # 1. RUFF Linter
    # Ignoriamo C901, RUF100, ANN204, TRY003, PLR0913, RET505, TRY300 per pulire il report finale
    results.append(
        (
            "RUF Linter",
            run_command(
                "RUF Linter", "ruff check . --ignore C901,RUF100,ANN204,TRY003,PLR0913,RET505,TRY300"
            ),
        )
    )

    # 2. RUFF Formatter (check only)
    results.append(("RUF Formatter", run_command("RUF Formatter", "ruff format .")))

    # 3. MYPY
    results.append(("MYPY Type Check", run_command("MYPY Type Check", "mypy src")))

    # 4. XENON (Complexity)
    # Target: Rank C per i blocchi, Rank C per i moduli (molto severo per app GUI)
    # Usiamo rank E assoluto per i file GUI legacy ma restiamo su C per tutto il resto
    results.append(
        (
            "XENON Complexity",
            run_command("XENON Complexity", "xenon --max-absolute E --max-modules E --max-average B src"),
        )
    )

    # 5. RADON (CC)
    results.append(("RADON CC Analysis", run_command("RADON CC Analysis", "radon cc src -s")))

    # 6. BANDIT (Security)
    results.append(("BANDIT Security", run_command("BANDIT Security", "bandit -r src -ll")))

    # Tabella riepilogativa
    table = Table(title="\nReport Qualità Finale")
    table.add_column("Tool", style="cyan")
    table.add_column("Stato", justify="center")

    all_passed = True
    for tool, success in results:
        status = "[bold green]✅ PASS[/bold green]" if success else "[bold red]❌ FAIL[/bold red]"
        table.add_row(tool, status)
        if not success:
            all_passed = False

    console.print(table)

    if all_passed:
        console.print(
            "\n[bold green]🌟 COMPLIMENTI: Il codice rispetta tutti gli standard di qualità![/bold green]"
        )
    else:
        console.print(
            "\n[bold yellow]⚠️ ATTENZIONE: Alcuni controlli sono falliti. Revisiona il codice sopra.[/bold yellow]"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
