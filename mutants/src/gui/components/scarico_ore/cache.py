import json
import pickle

from PyQt6.QtCore import QThread, pyqtSignal

from src.utils.parsing import parse_currency


class CacheWorker(QThread):
    """
    ⚡ BOLT OPTIMIZATION: Background worker for heavy cache operations.
    Handles file I/O (pickle) and data processing.
    Now builds a PRE-FORMATTED display cache for max speed.
    """

    finished = pyqtSignal(
        object, object, object, object, object
    )  # display_data, search_index, float_totals, style_cache, date_keys
    progress = pyqtSignal(str)

    def __init__(self, cache_path, data_source=None):
        super().__init__()
        self.cache_path = cache_path
        self.data_source = data_source  # If provided, we build cache from this data.

    def run(self):
        """Esegue l'operazione di caricamento o generazione della cache in background."""
        if self.data_source:
            self.progress.emit("Elaborazione dati...")
            (
                display_data,
                search_index,
                float_totals,
                style_cache,
                date_keys,
            ) = self._build_caches(self.data_source)
            self.progress.emit("Salvataggio cache...")
            self._save_cache(
                display_data, search_index, float_totals, style_cache, date_keys
            )
            self.finished.emit(
                display_data, search_index, float_totals, style_cache, date_keys
            )
        else:
            if not self.cache_path.exists():
                self.finished.emit([], [], [], [], [])
                return

            try:
                self.progress.emit("Caricamento cache...")
                with open(self.cache_path, "rb") as f:
                    loaded = pickle.load(f)  # nosec B301
                    if len(loaded) == 3:
                        raw_data = loaded[0]
                        (
                            display_data,
                            search_index,
                            float_totals,
                            style_cache,
                            date_keys,
                        ) = (
                            self._build_caches(raw_data)
                            if raw_data and not isinstance(raw_data[0][0], str)
                            else (raw_data, [], [], [], [])
                        )
                    elif len(loaded) == 5:
                        d, s, t, st, dk = loaded
                        (
                            display_data,
                            search_index,
                            float_totals,
                            style_cache,
                            date_keys,
                        ) = (
                            d,
                            s,
                            t,
                            st,
                            dk,
                        )
                    elif len(loaded) == 4:
                        d, _, _, _ = loaded
                        (
                            display_data,
                            search_index,
                            float_totals,
                            style_cache,
                            date_keys,
                        ) = (
                            self._build_caches(d)
                            if d and not isinstance(d[0][0], str)
                            else (d, [], [], [], [])
                        )
                    else:
                        (
                            display_data,
                            search_index,
                            float_totals,
                            style_cache,
                            date_keys,
                        ) = ([], [], [], [], [])

                self.finished.emit(
                    display_data, search_index, float_totals, style_cache, date_keys
                )
            except Exception as e:
                print(f"Error loading cache: {e}")
                self.finished.emit([], [], [], [], [])

    def _build_style_cache_only(self, data):
        style_cache = []
        append_style = style_cache.append

        for row in data:
            if len(row) > 11:
                style_json = row[11]
                if style_json:
                    try:
                        append_style(json.loads(style_json))
                    except Exception:
                        append_style(None)
                else:
                    append_style(None)
            else:
                append_style(None)
        return style_cache

    def _build_caches(self, data):
        display_data, search_index, float_totals, style_cache, date_keys = (
            [],
            [],
            [],
            [],
            [],
        )

        for row in data:
            date_str = self._format_date_for_display(row[0])
            disp_row, search_parts = self._process_row_fields(row, date_str)

            display_data.append(disp_row)
            search_index.append(" ".join(search_parts).lower())
            float_totals.append(self._parse_row_total(row[7]))
            style_cache.append(self._parse_row_style(row))
            date_keys.append(str(row[0]) if row[0] else "")

        return display_data, search_index, float_totals, style_cache, date_keys

    def _format_date_for_display(self, val) -> str:
        if not val:
            return ""
        s_val = str(val)
        if "-" not in s_val:
            return s_val

        try:
            if len(s_val) >= 10 and s_val[4] == s_val[7] == "-":
                return f"{s_val[8:10]}/{s_val[5:7]}/{s_val[0:4]}"
            parts = s_val.split(" ")[0].split("-")
            return f"{parts[2]}/{parts[1]}/{parts[0]}" if len(parts) == 3 else s_val
        except Exception:
            return s_val

    def _process_row_fields(self, row, date_str) -> tuple[list[str], list[str]]:
        disp_row = [date_str]
        search_parts = [date_str]
        for i in range(1, 11):
            val = row[i]
            d_val = "" if val is None else str(val)
            disp_row.append(d_val)
            if d_val:
                search_parts.append(d_val)
        return disp_row, search_parts

    def _parse_row_total(self, val) -> float:
        try:
            if isinstance(val, (int, float)):
                return float(val)
            return parse_currency(val)
        except Exception:
            return 0.0

    def _parse_row_style(self, row):
        if len(row) <= 11 or not row[11]:
            return None
        try:
            return json.loads(row[11])
        except Exception:
            return None

    def _save_cache(self, data, search, totals, style_cache, date_keys):
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, "wb") as f:
                pickle.dump((data, search, totals, style_cache, date_keys), f)  # nosec B403
        except Exception as e:
            print(f"Error saving cache: {e}")
