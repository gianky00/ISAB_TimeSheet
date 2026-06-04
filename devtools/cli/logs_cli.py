#!/usr/bin/env python3
"""SyncroJob - Log Analysis CLI Tool.

Strumento command-line per l'analisi e l'esportazione dei log strutturati.
Consente di eseguire query filtrate, ricostruire trace e visualizzare report di salute.

Usage:
    python devtools/cli/logs_cli.py query --level ERROR --bot scarico_ts --limit 20
    python devtools/cli/logs_cli.py trace <trace_id>
    python devtools/cli/logs_cli.py health --hours 24
    python devtools/cli/logs_cli.py export --format csv --output report.csv
"""

import argparse
import csv
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

# Aggiungi il path del progetto per gli import
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.application.services.logging import health_report, query_logs, view_trace  # noqa: E402


def format_timestamp(ts: str) -> str:
    """Formatta un timestamp ISO in un formato leggibile dall'utente.

    Args:
        ts: Stringa del timestamp in formato ISO.

    Returns:
        str: Timestamp formattato come YYYY-MM-DD HH:MM:SS.
    """
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts


def print_log_entry(entry: dict[str, Any], verbose: bool = False) -> None:
    """Stampa una singola entry di log formattata con colori ANSI per il terminale.

    Args:
        entry: Dizionario dei dati del log.
        verbose: Se True, stampa anche il contesto esteso e i metadati.
    """
    ts = format_timestamp(entry.get("timestamp", ""))
    level = entry.get("level", "INFO")
    message = entry.get("message", "")

    # Colori ANSI per livelli
    colors = {
        "DEBUG": "\033[90m",  # Grigio
        "INFO": "\033[32m",  # Verde
        "WARNING": "\033[33m",  # Giallo
        "ERROR": "\033[31m",  # Rosso
        "CRITICAL": "\033[35m",  # Magenta
    }
    reset = "\033[0m"
    color = colors.get(level, "")

    print(f"{ts} {color}[{level:8}]{reset} {message}")

    if verbose:
        context = entry.get("context", {})
        if context:
            print(f"           Context: {json.dumps(context, ensure_ascii=False)}")
        data = entry.get("data", {})
        if data:
            print(f"           Data: {json.dumps(data, ensure_ascii=False)}")
        if entry.get("exception"):
            print(f"           Exception: {entry['exception'].get('type', 'Unknown')}")


def cmd_query(args: argparse.Namespace) -> None:
    """Esegue una query sui log utilizzando i filtri forniti tramite argomenti CLI.

    Args:
        args: Argomenti parsati da argparse.
    """
    query = query_logs()

    if args.level:
        levels = [lvl.upper() for lvl in args.level]
        query = query.level(*levels)

    if args.bot:
        query = query.bot_type(args.bot)

    if args.message:
        query = query.contains_message(args.message, case_sensitive=False)

    if args.hours:
        start = datetime.now(UTC) - timedelta(hours=args.hours)
        query = query.time_range(start=start, end=datetime.now(UTC))

    if args.limit:
        query = query.limit(args.limit)

    results = query.execute()

    if not results:
        print("Nessun log trovato con i filtri specificati.")
        return

    print(f"\n📋 Trovati {len(results)} log entries:\n")
    print("-" * 80)

    for entry in results:
        print_log_entry(entry, verbose=args.verbose)

    print("-" * 80)


def cmd_trace(args: argparse.Namespace) -> None:
    """Ricostruisce e visualizza la timeline di eventi associata a un trace_id specifico.

    Args:
        args: Argomenti parsati (deve contenere trace_id).
    """
    trace_id = args.trace_id

    print(f"\n🔍 Ricostruzione timeline per trace: {trace_id}\n")
    print("=" * 80)

    timeline = view_trace(trace_id)

    if not timeline:
        print(f"Nessun evento trovato per trace_id: {trace_id}")
        return

    print(f"Trovati {len(timeline)} eventi:\n")

    for i, entry in enumerate(timeline, 1):
        ts = format_timestamp(entry.get("timestamp", ""))
        level = entry.get("level", "INFO")
        message = entry.get("message", "")
        span = entry.get("context", {}).get("span_id", "")

        span_info = f" [{span}]" if span else ""
        print(f"{i:3}. {ts} [{level}]{span_info} {message}")

        # Mostra duration se presente
        data = entry.get("data", {})
        if "duration_ms" in data:
            print(f"     ⏱️  Duration: {data['duration_ms']}ms")

        # Mostra exception se presente
        if entry.get("exception"):
            exc_type = entry["exception"].get("type", "Exception")
            print(f"     ❌ Exception: {exc_type}")

    print("=" * 80)


def cmd_health(args: argparse.Namespace) -> None:
    """Genera e visualizza un report di salute del sistema basato sugli ultimi eventi di log.

    Args:
        args: Argomenti parsati (opzionale: hours).
    """
    hours = args.hours or 24

    print(f"\n🏥 Health Report (ultime {hours}h)\n")
    print("=" * 60)

    report = health_report(hours=hours)

    # Stats generali
    print("\n📊 Statistiche Generali:")
    print(f"   Total Events:     {report.get('total_events', 0):,}")
    print(f"   Error Rate:       {report.get('error_rate_percent', 0):.2f}%")

    # Distribuzione livelli
    levels = report.get("level_distribution", {})
    if levels:
        print("\n📈 Distribuzione per Livello:")
        for level, count in levels.items():
            bar = "█" * min(int(count / 10), 40)
            print(f"   {level:10} {count:6} {bar}")

    # Bot runs
    bot_runs = report.get("bot_runs", {})
    if bot_runs:
        print("\n🤖 Bot Runs:")
        print(f"   Total:            {bot_runs.get('total', 0)}")
        print(f"   Successful:       {bot_runs.get('successful', 0)}")
        print(f"   Failed:           {bot_runs.get('failed', 0)}")
        print(f"   Success Rate:     {bot_runs.get('success_rate_percent', 0):.1f}%")

    # Top errors
    top_errors = report.get("top_errors", [])
    if top_errors:
        print("\n❌ Top Errors:")
        for i, err in enumerate(top_errors[:5], 1):
            msg = err.get("message", "Unknown")[:50]
            count = err.get("count", 0)
            print(f"   {i}. ({count}x) {msg}")

    # Slow operations
    slow_ops = report.get("slow_operations", [])
    if slow_ops:
        print("\n🐌 Operazioni Lente:")
        for i, op in enumerate(slow_ops[:5], 1):
            name = op.get("operation", "unknown")
            duration = op.get("duration_ms", 0)
            print(f"   {i}. {name}: {duration:,}ms")

    print("\n" + "=" * 60)


def cmd_export(args: argparse.Namespace) -> None:
    """Esporta i log filtrati in formato JSON o CSV su file.

    Args:
        args: Argomenti parsati (format, output, filters).
    """
    print(f"\n📤 Esportazione log in formato {args.format}...")

    query = query_logs()

    if args.hours:
        start = datetime.now(UTC) - timedelta(hours=args.hours)
        query = query.time_range(start=start, end=datetime.now(UTC))

    if args.level:
        levels = [lvl.upper() for lvl in args.level]
        query = query.level(*levels)

    results = query.execute()

    if not results:
        print("Nessun log da esportare.")
        return

    output_path = Path(args.output)

    if args.format == "json":
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    elif args.format == "csv" and results:
        # Estrai colonne da primo record
        fieldnames = ["timestamp", "level", "message", "trace_id", "bot_type"]

        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()

            for entry in results:
                row = {
                    "timestamp": entry.get("timestamp", ""),
                    "level": entry.get("level", ""),
                    "message": entry.get("message", ""),
                    "trace_id": entry.get("context", {}).get("trace_id", ""),
                    "bot_type": entry.get("context", {}).get("bot_type", ""),
                }
                writer.writerow(row)

    print(f"✅ Esportati {len(results)} log entries in: {output_path}")


def main() -> None:
    """Entry point principale per il tool CLI dei log."""
    parser = argparse.ArgumentParser(
        prog="logs_cli",
        description="SyncroJob - Log Analysis CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  %(prog)s query --level ERROR WARNING --limit 20
  %(prog)s query --bot scarico_ts --hours 24
  %(prog)s trace trace_abc123def456
  %(prog)s health --hours 48
  %(prog)s export --format csv --output errors.csv --level ERROR
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Query command
    query_parser = subparsers.add_parser("query", help="Query log con filtri")
    query_parser.add_argument(
        "--level",
        "-l",
        nargs="+",
        help="Filtra per livello (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    query_parser.add_argument("--bot", "-b", help="Filtra per bot type (es. scarico_ts, carico_ts)")
    query_parser.add_argument("--message", "-m", help="Cerca nel messaggio (case-insensitive)")
    query_parser.add_argument("--hours", "-H", type=int, default=24, help="Filtra ultime N ore (default: 24)")
    query_parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=50,
        help="Numero massimo risultati (default: 50)",
    )
    query_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Mostra dettagli extra (context, data)",
    )
    query_parser.set_defaults(func=cmd_query)

    # Trace command
    trace_parser = subparsers.add_parser("trace", help="Ricostruisci timeline trace")
    trace_parser.add_argument("trace_id", help="ID del trace da ricostruire")
    trace_parser.set_defaults(func=cmd_trace)

    # Health command
    health_parser = subparsers.add_parser("health", help="Report salute sistema")
    health_parser.add_argument(
        "--hours",
        "-H",
        type=int,
        default=24,
        help="Periodo analisi in ore (default: 24)",
    )
    health_parser.set_defaults(func=cmd_health)

    # Export command
    export_parser = subparsers.add_parser("export", help="Esporta log")
    export_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv"],
        default="json",
        help="Formato output (default: json)",
    )
    export_parser.add_argument("--output", "-o", required=True, help="File di output")
    export_parser.add_argument("--hours", "-H", type=int, help="Filtra ultime N ore")
    export_parser.add_argument("--level", "-l", nargs="+", help="Filtra per livello")
    export_parser.set_defaults(func=cmd_export)

    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
