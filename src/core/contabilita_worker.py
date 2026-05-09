import time
from pathlib import Path
from typing import Any

from PySide6.QtCore import QThread, Signal

from src.core.contabilita_manager import ContabilitaManager


class ContabilitaWorker(QThread):
    """Worker per l'importazione in background della contabilità."""

    finished_signal = Signal(bool, str, int, int, float)
    progress_signal = Signal(str)

    def __init__(
        self,
        file_path: str,
        giornaliere_path: str = "",
        attivita_path: str = "",
        certificati_path: str = "",
    ) -> None:
        super().__init__()
        self.file_path = file_path
        self.giornaliere_path = giornaliere_path
        self.attivita_path = attivita_path
        self.certificati_path = certificati_path
        self.start_time: float = 0.0

    def run(self) -> None:
        """Esegue il workflow di importazione completo in background."""
        try:
            ContabilitaManager.init_db()
            ops_info = self._calculate_total_ops()
            total_ops = ops_info["total"]
            self.start_time = time.time()

            # Stato interno accumulato
            state = {
                "added": 0,
                "removed": 0,
                "messages": [],
                "success": False,
                "total_ops": total_ops,
                "estimates": ops_info,  # Salva stima iniziale e breakdown
            }

            # Esecuzione fasi
            self._phase_import_contabilita(state)
            self._phase_import_giornaliere(state)
            self._phase_import_attivita(state)
            self._phase_import_certificati(state)

            duration = time.time() - self.start_time
            self.finished_signal.emit(
                state["success"],
                " | ".join(state["messages"]),
                state["added"],
                state["removed"],
                duration,
            )
        except Exception as e:
            self.finished_signal.emit(False, f"Errore critico: {e}", 0, 0, 0.0)

    def _calculate_total_ops(self) -> dict[str, Any]:
        """Calcola il totale operazioni e ritorna il dettaglio per stime accurate."""
        self.progress_signal.emit("[ATTESA] Analisi carico di lavoro...")
        sheets, files = ContabilitaManager.scan_workload(self.file_path, self.giornaliere_path)

        attivita = 1 if self.attivita_path and Path(self.attivita_path).exists() else 0
        certificati = 1 if self.certificati_path and Path(self.certificati_path).exists() else 0

        total = sheets + files + attivita + certificati
        if total == 0:
            total = 1

        return {
            "total": total,
            "est_sheets": sheets,
            "est_files": files,
            "est_attivita": attivita,
            "est_certificati": certificati,
        }

    def _update_progress_dynamic(
        self, current_in_phase: int, total_in_phase: int, state: Any, phase_key: str
    ) -> None:
        """
        Aggiorna il totale operazioni se il numero effettivo differisce dalla stima.

        Args:
          current_in_phase: Numero elemento corrente (1-based)
          total_in_phase: Totale elementi reali nella fase
          state: Stato del worker
          phase_key: Chiave della stima nel dizionario state (es. 'est_sheets')
        """
        # Se  la prima volta che riceviamo il totale reale per questa fase
        if not state.get(f"{phase_key}_adjusted", False):
            est = state["estimates"].get(phase_key, 0)
            diff = total_in_phase - est

            if diff != 0:
                state["total_ops"] += diff
                # Aggiorna anche la stima per evitare ricalcoli
                state["estimates"][phase_key] = total_in_phase

            state[f"{phase_key}_adjusted"] = True

        # Calcola offset basato sulle fasi precedenti
        # Ordine: Contabilita -> Giornaliere -> Attivita -> Certificati
        offset = 0
        est = state["estimates"]

        if phase_key == "est_files":  # Giornaliere
            offset += est["est_sheets"]
        elif phase_key == "est_attivita":
            offset += est["est_sheets"] + est["est_files"]
        elif phase_key == "est_certificati":
            offset += est["est_sheets"] + est["est_files"] + est["est_attivita"]

        current_global = offset + current_in_phase

        # Emissione
        self._emit_simple_progress(current_global, state)

    def _emit_simple_progress(self, current: int, state: Any) -> None:
        """Emette il segnale di progresso calcolato."""
        elapsed = time.time() - self.start_time
        total = state["total_ops"]

        # Clamp current to total (per evitare >100% temporaneo)
        if current > total:
            # Se siamo oltre, espandiamo il totale
            total = current
            state["total_ops"] = current

        if total > 0:
            percent = int((current / total) * 100)
            percent = min(99, percent)
        else:
            percent = 0

        # Stima ETA
        rate = current / elapsed if elapsed > 0 else 0
        remaining_ops = total - current
        eta_s = remaining_ops / rate if rate > 0 else 0
        m, s = divmod(int(eta_s), 60)

        self.progress_signal.emit(
            f"[ATTESA] Importazione: {percent}% completato ({current}/{total})   ETA: {m}m {s}s"
        )

    def _phase_import_contabilita(self, state: Any) -> None:
        if not self.file_path or not Path(self.file_path).exists():
            return

        success, msg, added, removed = ContabilitaManager.import_data_from_excel(
            self.file_path,
            progress_callback=lambda c, t: self._update_progress_dynamic(c, t, state, "est_sheets"),
        )
        self._update_state(
            state,
            success,
            added,
            removed,
            f"Contabilità: OK (+{added}/-{removed})",
            f"Err Contabilità: {msg}",
        )

    def _phase_import_giornaliere(self, state: Any) -> None:
        if not self.giornaliere_path:
            return

        # Nota: Import giornaliere scansiona internamente i file, ma noi passiamo callback
        success, msg, added, removed = ContabilitaManager.import_giornaliere(
            self.giornaliere_path,
            progress_callback=lambda c, t: self._update_progress_dynamic(c, t, state, "est_files"),
        )
        self._update_state(
            state,
            success,
            added,
            removed,
            f"Giornaliere: OK (+{added}/-{removed})",
            f"Err Giornaliere: {msg}",
        )

    def _phase_import_attivita(self, state: Any) -> None:
        if not self.attivita_path:
            return

        success, msg, added, removed = ContabilitaManager.import_attivita_programmate(self.attivita_path)

        # Aggiorna progresso (1 step)
        self._update_progress_dynamic(1, 1, state, "est_attivita")

        self._update_state(state, success, added, removed, "Att. Prog: OK", f"Err Att. Prog: {msg}")

    def _phase_import_certificati(self, state: Any) -> None:
        if not self.certificati_path:
            return

        success, msg, added, removed = ContabilitaManager.import_certificati_campione(self.certificati_path)

        # Aggiorna progresso (1 step)
        self._update_progress_dynamic(1, 1, state, "est_certificati")

        self._update_state(state, success, added, removed, "Certificati: OK", f"Err Certificati: {msg}")

    def _update_state(
        self, state: Any, success: bool, added: int, removed: int, ok_msg: str, err_msg: str
    ) -> None:
        state["added"] += added
        state["removed"] += removed
        if success:
            state["messages"].append(ok_msg)
            state["success"] = True
        else:
            state["messages"].append(err_msg)
