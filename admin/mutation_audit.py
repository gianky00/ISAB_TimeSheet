"""
🧬 Mutation Audit Tool for SyncroJob
Esegue test di mutazione (Mutation Testing) utilizzando 'mutatest'.
Consente un'analisi incrementale ("poco a poco") per identificare falle nella copertura dei test.
"""

import argparse
import contextlib
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Configurazione Percorsi
ROOT_DIR = Path(__file__).parent.parent.resolve()
SRC_DIR = ROOT_DIR / "src"
REPORTS_DIR = ROOT_DIR / "reports" / "mutation"


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"


def print_banner():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║        🧬 SyncroJob Mutation Audit Tool (Mutatest)           ║")
    print("║        ☢️  Incremental Quality & Resilience Check             ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")


def get_mutatest_path():
    """Trova il percorso dell'eseguibile mutatest."""
    candidates = [
        Path(r"C:\Users\gianc\AppData\Roaming\Python\Python312\Scripts\mutatest.exe"),
        Path(sys.executable).parent / "Scripts" / "mutatest.exe",
        Path(sys.executable).parent / "mutatest.exe",
    ]

    for c in candidates:
        if c.exists():
            return str(c)
    return "mutatest"  # Fallback al PATH


def check_mutatest():
    """Verifica se mutatest è installato."""
    mutatest_path = get_mutatest_path()
    try:
        # Usiamo -h invece di --version perché mutatest non supporta --version
        subprocess.run([mutatest_path, "-h"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.RED}[ERRORE] 'mutatest' non trovato.{Colors.END}")
        return False


def get_subpackages():
    """Ritorna la lista dei subpackage in src/."""
    return [
        p.name
        for p in SRC_DIR.iterdir()
        if p.is_dir() and ((p / "__init__.py").exists() or p.name in ["core", "utils", "gui", "bots"])
    ]


def run_mutation(target: str, trials: int, mode: str):
    """Esegue mutatest su un target specifico."""
    target_path = SRC_DIR / target
    mutatest_path = get_mutatest_path()

    print(f"\n{Colors.BLUE}[AUDIT] 🔬 Analisi modulo: {target}{Colors.END}")

    # Costruzione comando
    # -s: source, -t: test command, -n: trials, --mode: f(ast), r(andom), search
    cmd = [
        mutatest_path,
        "-s",
        str(target_path),
        "-t",
        "pytest",
        "-n",
        str(trials),
        "--mode",
        mode,
    ]

    print(f"  -> Comando: {' '.join(cmd)}")

    start_time = time.time()
    # Usiamo shell=False per sicurezza, passando la lista
    process = subprocess.run(cmd, capture_output=True, text=True)
    duration = time.time() - start_time

    return {
        "target": target,
        "stdout": process.stdout,
        "stderr": process.stderr,
        "duration": duration,
        "success": process.returncode == 0,
    }


def parse_results(output: str):
    """Parsing dell'output di mutatest per estrarre le statistiche e i dettagli."""
    stats = {"killed": 0, "survived": 0, "incompetent": 0, "timeout": 0}
    details = []

    for line in output.splitlines():
        if "Killed mutants:" in line:
            with contextlib.suppress(ValueError, IndexError):
                stats["killed"] = int(line.split(":")[-1].strip())
        elif "Survived mutants:" in line:
            with contextlib.suppress(ValueError, IndexError):
                stats["survived"] = int(line.split(":")[-1].strip())
        elif "Incompetent mutants:" in line:
            with contextlib.suppress(ValueError, IndexError):
                stats["incompetent"] = int(line.split(":")[-1].strip())
        elif "Timeout mutants:" in line:
            with contextlib.suppress(ValueError, IndexError):
                stats["timeout"] = int(line.split(":")[-1].strip())

        # Estrazione dettagli sopravvissuti
        if "SURVIVED:" in line:
            details.append(line.replace("SURVIVED:", "").strip())

    return stats, details


def generate_final_report(results: list):
    """Genera un report markdown dettagliato."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"mutation_audit_{timestamp}.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 🧬 Mutation Audit Report\n\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## 📊 Statistiche Generali\n\n")
        f.write("| Modulo | Stato | Killed 🟢 | Survived 🔴 | Incompetent 🟡 | Timeout ⏱️ | Durata |\n")
        f.write("| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n")

        total_killed = 0
        total_survived = 0

        for res in results:
            s, _ = parse_results(res["stdout"])
            status = "✅ OK" if s["survived"] == 0 else "⚠️ WEAK"
            f.write(
                f"| {res['target']} | {status} | {s['killed']} | {s['survived']} | "
                f"{s['incompetent']} | {s['timeout']} | {res['duration']:.1f}s |\n"
            )
            total_killed += s["killed"]
            total_survived += s["survived"]

        total = total_killed + total_survived
        score = (total_killed / total * 100) if total > 0 else 0

        f.write(f"\n**Mutation Score Totale: {score:.2f}%**\n\n")

        f.write("## 🔍 Dettagli e Migliorie Suggerite\n\n")
        for res in results:
            s, details = parse_results(res["stdout"])
            if s["survived"] > 0:
                f.write(f"### 🚩 Modulo `{res['target']}`\n")
                f.write(f"- **Problema:** {s['survived']} mutanti sono sopravvissuti.\n")
                f.write("- **Locazioni critiche:**\n")
                f.writelines(f"  - `{d}`\n" for d in details[:10])  # Limitiamo i primi 10 per leggibilità
                if len(details) > 10:
                    f.write(f"  - ... e altri {len(details) - 10} mutanti.\n")

                f.write(
                    "\n- **Miglioria Suggerita:** I mutanti sopra elencati indicano codice che può "
                    "essere modificato senza fallimenti nei test. \n"
                )
                f.write("  1. Verifica se il codice mutato è effettivamente necessario (dead code?).\n")
                f.write(
                    "  2. Aggiungi test specifici che asseriscano il comportamento corretto "
                    "per quelle righe/operazioni.\n\n"
                )

                f.write("<details><summary>Visualizza Log Completo</summary>\n\n")
                f.write("```text\n")
                f.write(res["stdout"])
                f.write("\n```\n\n</details>\n\n")

    return report_path


def main():
    parser = argparse.ArgumentParser(description="SyncroJob Mutation Audit Tool")
    parser.add_argument("--target", help="Modulo specifico da analizzare (es: core, bots, gui)")
    parser.add_argument("--trials", type=int, default=20, help="Numero di mutazioni per modulo (default: 20)")
    parser.add_argument(
        "--mode",
        choices=["f", "r", "s"],
        default="f",
        help="Modalità: f(ast), r(random), search",
    )
    parser.add_argument("--all", action="store_true", help="Analizza tutti i moduli in src/")

    args = parser.parse_args()

    print_banner()

    if not check_mutatest():
        sys.exit(1)

    targets = []
    if args.target:
        targets = [args.target]
    elif args.all:
        targets = get_subpackages()
    else:
        print(
            f"{Colors.YELLOW}Utilizzo: python admin/mutation_audit.py --target <modulo> o --all{Colors.END}"
        )
        print(f"Moduli disponibili: {', '.join(get_subpackages())}")
        sys.exit(0)

    results = []
    for t in targets:
        res = run_mutation(t, args.trials, args.mode)
        results.append(res)

        s, _ = parse_results(res["stdout"])
        color = Colors.GREEN if s["survived"] == 0 else Colors.YELLOW
        print(
            f"  -> {color}Killed: {s['killed']}, Survived: {s['survived']}{Colors.END} "
            f"(Durata: {res['duration']:.1f}s)"
        )

    report_path = generate_final_report(results)
    print(f"\n{Colors.CYAN}✅ Audit terminato con successo!{Colors.END}")
    print(f"📄 Report generato: {Colors.BOLD}{report_path}{Colors.END}")


if __name__ == "__main__":
    main()
