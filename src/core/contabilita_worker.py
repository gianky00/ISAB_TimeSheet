import os
import time

from PyQt6.QtCore import QThread, pyqtSignal

from src.core.contabilita_manager import ContabilitaManager


class ContabilitaWorker(QThread):
    """Worker per l'importazione in background della contabilità."""

    finished_signal = pyqtSignal(bool, str, int, int, float)
    progress_signal = pyqtSignal(str)

    def __init__(
        self,
        file_path: str,
        giornaliere_path: str = "",
        attivita_path: str = "",
        certificati_path: str = "",
    ):
        super().__init__()
        self.file_path = file_path
        self.giornaliere_path = giornaliere_path
        self.attivita_path = attivita_path
        self.certificati_path = certificati_path
        self.start_time = 0

    def run(self):
        """Esegue il workflow di importazione completo in background."""
        try:
            ContabilitaManager.init_db()
            total_ops = self._calculate_total_ops()
            self.start_time = time.time()

            # Stato interno accumulato
            state = {
                "added": 0,
                "removed": 0,
                "messages": [],
                "success": False,
                "total_ops": total_ops,
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

    def _calculate_total_ops(self) -> int:
        """Calcola il numero totale di operazioni per la barra di progresso."""
        self.progress_signal.emit("⏳ Analisi carico di lavoro...")
        sheets, files = ContabilitaManager.scan_workload(
            self.file_path, self.giornaliere_path
        )

        attivita = 1 if self.attivita_path and os.path.exists(self.attivita_path) else 0
        certificati = (
            1 if self.certificati_path and os.path.exists(self.certificati_path) else 0
        )

        total = sheets + files + attivita + certificati
        return total if total > 0 else 1

    def _emit_progress(self, processed, offset, state):
        """Calcola ed emette il progresso globale con ETA."""
        current = offset + processed
        if current > state["total_ops"]:
            state["total_ops"] = current

        elapsed = time.time() - self.start_time
        if current > 0 and elapsed > 0:
            rate = current / elapsed
            eta = (state["total_ops"] - current) / rate
            m, s = divmod(int(eta), 60)
            percent = min(99, int((current / state["total_ops"]) * 100))
            self.progress_signal.emit(
                f"⏳ Importazione: {percent}% completato ({current}/{state['total_ops']}) • ETA: {m}m {s}s"
            )

    def _phase_import_contabilita(self, state):
        if not self.file_path or not os.path.exists(self.file_path):
            state["messages"].append("Contabilità: File non trovato.")
            return

        success, msg, added, removed = ContabilitaManager.import_data_from_excel(
            self.file_path,
            progress_callback=lambda c, t: self._emit_progress(c, 0, state),
        )
        self._update_state(
            state,
            success,
            added,
            removed,
            f"Contabilità: OK (+{added}/-{removed})",
            f"Err Contabilità: {msg}",
        )

    def _phase_import_giornaliere(self, state):
        if not self.giornaliere_path:
            return

        # Offset: numero di fogli caricati nella prima fase
        # Nota: per semplicità usiamo un offset approssimativo o passiamo il numero reale
        sheets, _ = ContabilitaManager.scan_workload(self.file_path, "")

        success, msg, added, removed = ContabilitaManager.import_giornaliere(
            self.giornaliere_path,
            progress_callback=lambda c, t: self._emit_progress(c, sheets, state),
        )
        self._update_state(
            state,
            success,
            added,
            removed,
            f"Giornaliere: OK (+{added}/-{removed})",
            f"Err Giornaliere: {msg}",
        )

    def _phase_import_attivita(self, state):
        if not self.attivita_path:
            return

        success, msg, added, removed = ContabilitaManager.import_attivita_programmate(
            self.attivita_path
        )
        # Offset manuale per l'attivita (fine delle giornaliere)
        sheets, files = ContabilitaManager.scan_workload(
            self.file_path, self.giornaliere_path
        )
        self._emit_progress(1, sheets + files, state)

        self._update_state(
            state, success, added, removed, "Att. Prog: OK", f"Err Att. Prog: {msg}"
        )

    def _phase_import_certificati(self, state):
        if not self.certificati_path:
            return

        success, msg, added, removed = ContabilitaManager.import_certificati_campione(
            self.certificati_path
        )
        # Offset per certificati
        sheets, files = ContabilitaManager.scan_workload(
            self.file_path, self.giornaliere_path
        )
        att_task = 1 if self.attivita_path and os.path.exists(self.attivita_path) else 0
        self._emit_progress(1, sheets + files + att_task, state)

        self._update_state(
            state, success, added, removed, "Certificati: OK", f"Err Certificati: {msg}"
        )

    def _update_state(self, state, success, added, removed, ok_msg, err_msg):
        state["added"] += added
        state["removed"] += removed
        if success:
            state["messages"].append(ok_msg)
            state["success"] = True
        else:
            state["messages"].append(err_msg)
