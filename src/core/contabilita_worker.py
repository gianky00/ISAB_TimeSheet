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
        # Inizializza DB se necessario
        ContabilitaManager.init_db()

        self.progress_signal.emit("⏳ Analisi carico di lavoro...")

        # Scan workload for Global ETA
        sheets, files = ContabilitaManager.scan_workload(
            self.file_path, self.giornaliere_path
        )

        # Attività Programmate counts as 1 task if configured
        attivita_task = (
            1 if self.attivita_path and os.path.exists(self.attivita_path) else 0
        )

        # Certificati Campione counts as 1 task if configured
        certificati_task = (
            1 if self.certificati_path and os.path.exists(self.certificati_path) else 0
        )

        total_ops = sheets + files + attivita_task + certificati_task
        if total_ops == 0:
            total_ops = 1

        self.start_time = time.time()

        def global_progress(processed_in_phase, phase_offset, phase_name):
            nonlocal total_ops
            current_total = phase_offset + processed_in_phase
            if current_total > total_ops:
                total_ops = current_total  # Dynamic adjustment

            elapsed = time.time() - self.start_time

            if current_total > 0 and elapsed > 0:
                rate = current_total / elapsed
                remaining = total_ops - current_total
                eta_seconds = remaining / rate if rate > 0 else 0

                m, s = divmod(int(eta_seconds), 60)
                percent = int((current_total / total_ops) * 100)
                if percent > 99:
                    percent = 99  # Cap until actually finished

                self.progress_signal.emit(
                    f"⏳ Importazione: {percent}% completato ({current_total}/{total_ops}) • Tempo stimato: {m}m {s}s"
                )

        total_added = 0
        total_removed = 0
        messages = []
        overall_success = False

        # 1. Import Contabilità (Dati)
        if self.file_path and os.path.exists(self.file_path):
            def dati_cb(c, t):
                return global_progress(c, 0, "Contabilità")

            success, msg, added, removed = ContabilitaManager.import_data_from_excel(
                self.file_path, progress_callback=dati_cb
            )
            total_added += added
            total_removed += removed
            if success:
                messages.append(f"Contabilità: OK (+{added}/-{removed})")
                overall_success = True
            else:
                messages.append(f"Err Contabilità: {msg}")
        else:
            messages.append("Contabilità: File non trovato o non configurato.")

        # 2. Import Giornaliere (se configurato)
        if self.giornaliere_path:
            def giorn_cb(c, t):
                return global_progress(c, sheets, "Giornaliere")

            g_success, g_msg, g_added, g_removed = (
                ContabilitaManager.import_giornaliere(
                    self.giornaliere_path, progress_callback=giorn_cb
                )
            )
            total_added += g_added
            total_removed += g_removed
            if g_success:
                messages.append(f"Giornaliere: OK (+{g_added}/-{g_removed})")
                overall_success = True
            else:
                messages.append(f"Err Giornaliere: {g_msg}")

        # 3. Import Attività Programmate (se configurato)
        if self.attivita_path:
            def att_cb(c, t):
                return global_progress(c, sheets + files, "Attività Programmate")

            att_success, att_msg, att_added, att_removed = (
                ContabilitaManager.import_attivita_programmate(self.attivita_path)
            )
            att_cb(1, 1)
            total_added += att_added
            total_removed += att_removed
            if att_success:
                messages.append("Att. Prog: OK")
                overall_success = True
            else:
                messages.append(
                    f"Err Att. Prog: {att_success}"
                )  # Fix: success contains message if False

        # 4. Import Certificati Campione (se configurato)
        if self.certificati_path:
            def cert_cb(c, t):
                return global_progress(c, sheets + files + attivita_task, "Certificati Campione")

            cert_success, cert_msg, cert_added, cert_removed = (
                ContabilitaManager.import_certificati_campione(self.certificati_path)
            )
            cert_cb(1, 1)
            total_added += cert_added
            total_removed += cert_removed
            if cert_success:
                messages.append("Certificati: OK")
                overall_success = True
            else:
                messages.append(f"Err Certificati: {cert_msg}")

        total_duration = time.time() - self.start_time
        final_msg = " | ".join(messages)
        self.finished_signal.emit(
            overall_success, final_msg, total_added, total_removed, total_duration
        )
