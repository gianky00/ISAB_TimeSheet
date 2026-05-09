"""
SyncroJob - Log Viewer & Query Utility
Fornisce strumenti avanzati per l'interrogazione, l'analisi e la ricostruzione dei log JSON dell'applicazione.
Include un Query Builder fluido e utility per generare report sulla salute del sistema.
"""

import json
import operator
from collections import defaultdict
from collections.abc import Callable  # noqa: TC003
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

from .config import get_config

if TYPE_CHECKING:
    from .config import LoggingConfig


class LogQuery:
    """
    Query builder per file di log in formato JSON.
    Permette di concatenare filtri per livello, messaggio, contesto, trace_id e range temporale.
    """

    def __init__(self, log_file: Path) -> None:
        """
        Inizializza il query builder su un file specifico.

        Args:
          log_file: Percorso del file .json o .log da interrogare.
        """
        self.log_file = log_file
        self.filters: list[Callable[[dict[str, Any]], bool]] = []
        self._limit: int | None = None
        self._offset: int = 0

    def level(self, *levels: str) -> "LogQuery":
        """
        Filtra le entry in base ai livelli specificati (es. INFO, ERROR).

        Args:
          *levels: Uno o piu' livelli di log desiderati.

        Returns:
          LogQuery: L'istanza corrente per concatenazione.
        """
        self.filters.append(lambda entry: entry.get("level") in levels)
        return self

    def contains_message(self, text: str, case_sensitive: bool = False) -> "LogQuery":
        """
        Filtra i log il cui messaggio contiene la stringa specificata.

        Args:
          text: Sottostringa da cercare.
          case_sensitive: Se distinguere tra maiuscole e minuscole.

        Returns:
          LogQuery: L'istanza corrente.
        """

        def filter_fn(entry: dict[str, Any]) -> bool:
            """Filtra per contenuto del messaggio."""
            message = str(entry.get("message", ""))
            if not case_sensitive:
                return text.lower() in message.lower()
            return text in message

        self.filters.append(filter_fn)
        return self

    def context_match(self, **kwargs: object) -> "LogQuery":
        """
        Filtra in base ai campi contenuti nell'oggetto 'context' del log JSON.

        Args:
          **kwargs: Coppie chiave=valore da matchare nel contesto.

        Returns:
          LogQuery: L'istanza corrente.
        """

        def filter_fn(entry: dict[str, Any]) -> bool:
            """Filtra per corrispondenza dei campiu'nel contesto."""
            context = entry.get("context", {})
            return all(context.get(key) == value for key, value in kwargs.items())

        self.filters.append(filter_fn)
        return self

    def trace_id(self, trace_id: str) -> "LogQuery":
        """Filtra i log appartenenti a una specifica transazione (trace_id)."""
        return self.context_match(trace_id=trace_id)

    def bot_type(self, bot_type: str) -> "LogQuery":
        """Filtra i log generati da un particolare tipo di bot."""
        return self.context_match(bot_type=bot_type)

    def time_range(self, start: datetime | None = None, end: datetime | None = None) -> "LogQuery":
        """
        Filtra i log all'interno di una finestra temporale.

        Args:
          start: Data/ora iniziale (inclusa).
          end: Data/ora finale (inclusa).

        Returns:
          LogQuery: L'istanza corrente.
        """

        def filter_fn(entry: dict[str, Any]) -> bool:
            """Filtra per finestra temporale."""
            timestamp_str = str(entry.get("timestamp", ""))
            try:
                # Supporta sia formati con 'Z' che senza
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", ""))

                # Se il timestamp  naive, assumiamo UTC per coerenza con i log JSON
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=UTC)
            except Exception:
                return False
            if start:
                # Assicura che start sia aware per il confronto
                start_aware = start if start.tzinfo else start.replace(tzinfo=UTC)
                if timestamp < start_aware:
                    return False
            if end:
                # Assicura che end sia aware per il confronto
                end_aware = end if end.tzinfo else end.replace(tzinfo=UTC)
                if timestamp > end_aware:
                    return False
            return True

        self.filters.append(filter_fn)
        return self

    def has_exception(self) -> "LogQuery":
        """Filtra solo le entry che contengono una traccia di eccezione."""
        self.filters.append(lambda entry: "exception" in entry)
        return self

    def limit(self, count: int) -> "LogQuery":
        """Limita il numero massimo di risultati restituiti."""
        self._limit = count
        return self

    def offset(self, count: int) -> "LogQuery":
        """Salta i primi N risultati (paginazione)."""
        self._offset = count
        return self

    def execute(self) -> list[dict[str, Any]]:
        """
        Esegue la query leggendo il file riga per riga e applicando i filtri.

        Returns:
          list: Lista di dizionari log che soddisfano tutti i criteri.
        """
        if not self.log_file.exists():
            return []
        results: list[dict[str, Any]] = []
        skipped = 0
        with suppress(Exception), self.log_file.open("r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                if all(filter_fn(entry) for filter_fn in self.filters):
                    if skipped < self._offset:
                        skipped += 1
                        continue
                    results.append(entry)
                    if self._limit and len(results) >= self._limit:
                        break
        return results

    def count(self) -> int:
        """
        Conta il numero totale di log che matchano la query senza caricarli in memoria.

        Returns:
          int: Numero di occorrenze.
        """
        if not self.log_file.exists():
            return 0
        count = 0
        with suppress(Exception), self.log_file.open("r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                if all(filter_fn(entry) for filter_fn in self.filters):
                    count += 1
        return count


class LogViewer:
    """
    Interfaccia ad alto livello per l'analisi dei log applicativi.
    Fornisce metodi aggregati per statistiche, analisi errori e monitoraggio performance.
    """

    DEFAULT_LIMIT: Final[int] = 10
    HEALTH_PERIOD_HOURS: Final[int] = 24

    def __init__(self, config: "LoggingConfig | None" = None) -> None:
        """Inizializza il viewer con la configurazione di logging corrente."""
        self.config = config or get_config()

    def query(self, log_type: str = "application") -> LogQuery:
        """
        Crea un nuovo query builder per il tipo di log specificato.

        Args:
          log_type: "application" per i log generali, "errors" per i soli errori.

        Returns:
          LogQuery: Istanza del builder configurata sul file corretto.
        """
        if log_type == "application":
            log_file = self.config.json_log_file
        elif log_type == "errors":
            log_file = self.config.errors_log_file
        else:
            err_msg = f"Unknown log_type: {log_type}"
            raise ValueError(err_msg)
        return LogQuery(log_file)

    def get_level_stats(self) -> dict[str, int]:
        """Restituisce la distribuzione dei log per livello (DEBUG, INFO, ecc.)."""
        stats: dict[str, int] = defaultdict(int)
        results = self.query().execute()
        for entry in results:
            stats[str(entry.get("level", "UNKNOWN"))] += 1
        return stats.copy()

    def get_error_summary(self, limit: int = DEFAULT_LIMIT) -> list[dict[str, Any]]:
        """Analizza i log di errore e raggruppa i messaggia'piu' frequenti."""
        error_messages: dict[str, int] = defaultdict(int)
        error_details: dict[str, dict[str, Any]] = {}
        results = self.query("errors").execute()
        for entry in results:
            message = str(entry.get("message", ""))
            error_messages[message] += 1
            if message not in error_details:
                error_details[message] = {
                    "message": message,
                    "first_seen": entry.get("timestamp"),
                    "exception_type": (entry.get("exception", {}).get("type", "unknown")),
                    "count": 0,
                }
            error_details[message]["count"] = error_messages[message]

        sorted_errors = sorted(error_details.values(), key=operator.itemgetter("count"), reverse=True)
        return sorted_errors[:limit]

    def get_slow_operations(
        self, threshold_ms: float = 5000, limit: int = DEFAULT_LIMIT
    ) -> list[dict[str, Any]]:
        """Identifica le funzioni la cui esecuzione ha superato la soglia di millisecondi specificata."""
        slow_ops = []
        results = self.query().execute()
        for entry in results:
            duration = entry.get("data", {}).get("duration_ms")
            if duration and duration > threshold_ms:
                slow_ops.append(
                    {
                        "timestamp": entry.get("timestamp"),
                        "operation": entry.get("context", {}).get("function", "unknown"),
                        "duration_ms": duration,
                        "message": entry.get("message"),
                        "trace_id": entry.get("context", {}).get("trace_id"),
                    }
                )
        slow_ops.sort(key=operator.itemgetter("duration_ms"), reverse=True)
        return slow_ops[:limit]

    def reconstruct_trace(self, trace_id: str) -> list[dict[str, Any]]:
        """Ricostruisce la sequenza cronologica di tutti i log appartenenti a un singolo trace_id."""
        results = self.query().trace_id(trace_id).execute()
        results.sort(key=lambda x: str(x.get("timestamp", "")))
        return results

    def get_bot_runs_summary(
        self, bot_type: str | None = None, hours: int = HEALTH_PERIOD_HOURS
    ) -> list[dict[str, Any]]:
        """Genera un riepilogo delle esecuzioni bot nelle ultime ore, raggruppate per trace_id."""
        end = datetime.now(UTC)
        start = end - timedelta(hours=hours)
        query = self.query().time_range(start, end)
        if bot_type:
            query = query.bot_type(bot_type)
        results = query.execute()

        traces: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for entry in results:
            trace_id = entry.get("context", {}).get("trace_id")
            if trace_id:
                traces[trace_id].append(entry)

        summaries = []
        for trace_id, entries in traces.items():
            entries.sort(key=lambda x: str(x.get("timestamp", "")))
            try:
                start_time = datetime.fromisoformat(str(entries[0].get("timestamp", "")).replace("Z", ""))
                end_time = datetime.fromisoformat(str(entries[-1].get("timestamp", "")).replace("Z", ""))
                duration_sec = (end_time - start_time).total_seconds()
            except Exception:
                duration_sec = 0.0
            has_error = any(e.get("level") == "ERROR" for e in entries)
            summaries.append(
                {
                    "trace_id": trace_id,
                    "bot_type": entries[0].get("context", {}).get("bot_type", "unknown"),
                    "start_time": entries[0].get("timestamp"),
                    "end_time": entries[-1].get("timestamp"),
                    "duration_sec": round(duration_sec, 2),
                    "entry_count": len(entries),
                    "success": not has_error,
                    "context": entries[0].get("context", {}),
                }
            )
        summaries.sort(key=operator.itemgetter("start_time"), reverse=True)
        return summaries

    def generate_health_report(self, hours: int = HEALTH_PERIOD_HOURS) -> dict[str, Any]:
        """Esegue un'analisi completa dei log recenti per determinare il punteggio di salute (Health Score) del sistema."""
        end = datetime.now(UTC)
        start = end - timedelta(hours=hours)
        results = self.query().time_range(start, end).execute()

        level_stats: dict[str, int] = defaultdict(int)
        for entry in results:
            level_stats[str(entry.get("level", "UNKNOWN"))] += 1

        total = len(results)
        errors = level_stats.get("ERROR", 0) + level_stats.get("CRITICAL", 0)
        error_rate = (errors / total * 100) if total > 0 else 0.0

        bot_runs = self.get_bot_runs_summary(hours=hours)
        successful_runs = sum(1 for run in bot_runs if run["success"])
        failed_runs = sum(1 for run in bot_runs if not run["success"])

        return {
            "timestamp": datetime.now(UTC).isoformat() + "Z",
            "period_hours": hours,
            "total_events": total,
            "level_distribution": level_stats.copy(),
            "error_rate_percent": round(error_rate, 2),
            "bot_runs": {
                "total": len(bot_runs),
                "successful": successful_runs,
                "failed": failed_runs,
                "success_rate_percent": (
                    round(successful_runs / len(bot_runs) * 100, 2) if bot_runs else 0.0
                ),
            },
            "top_errors": self.get_error_summary(limit=5),
            "slow_operations": self.get_slow_operations(limit=5),
        }


def query_logs(log_type: str = "application") -> LogQuery:
    """Helper per creare una query sui log senza istanziare LogViewer manualmente."""
    return LogViewer().query(log_type)


def view_trace(trace_id: str) -> list[dict[str, Any]]:
    """Helper per ricostruire rapidamente un trace specifico."""
    return LogViewer().reconstruct_trace(trace_id)


def health_report(hours: int = LogViewer.HEALTH_PERIOD_HOURS) -> dict[str, Any]:
    """Helper per generare un report di salute rapido."""
    return LogViewer().generate_health_report(hours=hours)
