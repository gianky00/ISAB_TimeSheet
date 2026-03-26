import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QObject, QThread, pyqtSignal

from src.utils.parsing import parse_currency


class CacheWorker(QThread):
    """
    ⚡ BOLT OPTIMIZATION: Background worker for heavy cache operations.
    Handles file I/O (JSON) and data processing.
    Now builds a PRE-FORMATTED display cache for max speed.
    """

    finished = pyqtSignal(
        object, object, object, object, object
    )  # display_data, search_index, float_totals, style_cache, date_keys
    progress = pyqtSignal(str)

    def __init__(
        self,
        cache_path: Path,
        data_source: list[tuple[Any, ...]] | Callable[[], list[tuple[Any, ...]]] | None = None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        # Use .json extension if not already present, for clarity
        if cache_path.suffix != ".json":
            self.cache_path = cache_path.with_suffix(".json")
        else:
            self.cache_path = cache_path
        self.data_source = data_source

    def run(self) -> None:
        """Esegue l'operazione di caricamento o generazione della cache in background."""
        if self.data_source:
            self.progress.emit("Recupero dati...")

            # Se data_source è una funzione, la eseguiamo nel thread di background
            if callable(self.data_source):
                try:
                    data = self.data_source()
                except Exception as e:
                    print(f"Error fetching data from source: {e}")
                    self.finished.emit([], [], [], [], [])
                    return
            else:
                data = self.data_source

            if not data:
                self.finished.emit([], [], [], [], [])
                return

            self.progress.emit("Elaborazione dati...")
            (
                display_data,
                search_index,
                float_totals,
                style_cache,
                date_keys,
            ) = self._build_caches(data)
            self.progress.emit("Salvataggio cache...")
            self._save_cache(display_data, search_index, float_totals, style_cache, date_keys)
            self.finished.emit(display_data, search_index, float_totals, style_cache, date_keys)
        else:
            if not self.cache_path.exists():
                self.finished.emit([], [], [], [], [])
                return

            try:
                self.progress.emit("Caricamento cache...")
                # FIX B403: Use JSON instead of pickle for security
                with self.cache_path.open("r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, list) and len(loaded) == 5:  # noqa: PLR2004
                        d, s, t, st, dk = loaded
                        self.finished.emit(d, s, t, st, dk)
                    else:
                        # Fallback for old cache format or invalid data
                        self.finished.emit([], [], [], [], [])

            except Exception as e:
                print(f"Error loading cache: {e}")
                self.finished.emit([], [], [], [], [])

    def _build_caches(
        self, data: list[tuple[Any, ...]]
    ) -> tuple[list[list[str]], list[str], list[float], list[dict[str, Any] | None], list[str]]:
        display_data: list[list[str]] = []
        search_index: list[str] = []
        float_totals: list[float] = []
        style_cache: list[dict[str, Any] | None] = []
        date_keys: list[str] = []

        for row in data:
            date_str = self._format_date_for_display(row[0])
            disp_row, search_parts = self._process_row_fields(row, date_str)

            display_data.append(disp_row)
            search_index.append(" ".join(search_parts).lower())
            float_totals.append(self._parse_row_total(row[7]))
            style_cache.append(self._parse_row_style(row))
            date_keys.append(str(row[0]) if row[0] else "")

        return display_data, search_index, float_totals, style_cache, date_keys

    def _format_date_for_display(self, val: Any) -> str:
        if not val:
            return ""
        s_val = str(val)
        if "-" not in s_val:
            return s_val

        try:
            if len(s_val) >= 10 and s_val[4] == s_val[7] == "-":  # noqa: PLR2004
                return f"{s_val[8:10]}/{s_val[5:7]}/{s_val[0:4]}"
            parts = s_val.split(" ")[0].split("-")
            return f"{parts[2]}/{parts[1]}/{parts[0]}" if len(parts) == 3 else s_val  # noqa: PLR2004
        except Exception:
            return s_val

    def _process_row_fields(self, row: tuple[Any, ...], date_str: str) -> tuple[list[str], list[str]]:
        disp_row = [date_str]
        search_parts = [date_str]
        for i in range(1, 11):
            val = row[i]
            d_val = "" if val is None else str(val)
            disp_row.append(d_val)
            if d_val:
                search_parts.append(d_val)
        return disp_row, search_parts

    def _parse_row_total(self, val: Any) -> float:
        try:
            if isinstance(val, (int, float)):
                return float(val)
            return parse_currency(val)
        except Exception:
            return 0.0

    def _parse_row_style(self, row: tuple[Any, ...]) -> dict[str, Any] | None:
        if len(row) <= 11 or not row[11]:  # noqa: PLR2004
            return None
        try:
            return json.loads(row[11])  # type: ignore[no-any-return]
        except Exception:
            return None

    def _save_cache(
        self,
        data: list[list[str]],
        search: list[str],
        totals: list[float],
        style_cache: list[dict[str, Any] | None],
        date_keys: list[str],
    ) -> None:
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            # FIX B403: Use JSON instead of pickle for security
            with self.cache_path.open("w", encoding="utf-8") as f:
                json.dump((data, search, totals, style_cache, date_keys), f)
        except Exception as e:
            print(f"Error saving cache: {e}")
