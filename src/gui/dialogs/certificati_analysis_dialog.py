"""SyncroJob - Certificati Analysis Dialog.

Modulo specializzato per la visualizzazione e l'esportazione delle scadenze certificati.
"""

import os
import tempfile
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.application.services.constants import UbicazioneStrumenti
from src.application.services.logging import get_logger
from src.application.services.version import __app_name__, __version__
from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.gui.widgets.core_widgets import PrimaryButton
from src.gui.workers.outlook_worker import OutlookEmailWorker

logger = get_logger(__name__)

# Soglie giorni per scadenze
THRESHOLD_URGENT = 15
THRESHOLD_ATTENTION = 30


class ScadenzeAnalysisDialog(QDialog):
    """Finestra di analisi scadenze certificati - Design professionale.

    Inizializza la classe.
    """

    def __init__(
        self,
        certificates_data: list[Any],
        show_excluded: bool = False,
        parent: QWidget | None = None,
        tree_widget: Any | None = None,
        engine: Any | None = None,
    ) -> None:
        super().__init__(parent)

        # Filtriamo gli strumenti ASSENTI immediatamente e i guasti/controlli/dismessi
        self.certificates_data = [
            c
            for c in certificates_data
            if UbicazioneStrumenti.ASSENTE.value not in str(c.get("ubicazione", "")).upper()
            and c.get("days") not in (-9999, -8888, -7777)
        ]

        self.show_excluded = show_excluded
        self.tree_widget = tree_widget
        self.engine = engine

        # Widget members
        self.header: QFrame
        self.stats_frame: QFrame
        self.content_widget: QWidget
        self.footer: QFrame

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Inizializzazione principale dell'interfaccia."""
        self.setWindowTitle(f"Analisi Scadenze Certificati - {__app_name__}")
        self.setMinimumSize(950, 650)
        self.setStyleSheet(f"QDialog {{ background-color: {COLORS['bg_light']}; }}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Componenti principali
        layout.addWidget(self._build_header())
        layout.addWidget(self._build_stats_frame())
        layout.addWidget(self._build_scroll_area())
        layout.addWidget(self._build_footer())

    def _build_header(self) -> QFrame:
        """Costruisce la sezione header con titolo e data."""
        self.header = QFrame()
        self.header.setStyleSheet(
            f"QFrame {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLORS['glass_dark']}, stop:1 {COLORS['glass_deep']}); border: none; }}"
        )
        layout = QVBoxLayout(self.header)
        layout.setContentsMargins(30, 25, 30, 25)

        title_row = QHBoxLayout()
        title_label = QLabel("Analisi Scadenze Certificati")
        title_label.setStyleSheet(f"color: {COLORS['bg_white']}; font-size: 24px; font-weight: bold;")
        title_row.addWidget(title_label)
        title_row.addStretch()

        v_label = QLabel(f"{__app_name__} v{__version__}")
        v_label.setStyleSheet(f"color: {hex_to_rgba(COLORS['bg_white'], 0.7)}; font-size: 13px;")
        title_row.addWidget(v_label)
        layout.addLayout(title_row)

        d_str = datetime.now(UTC).astimezone().strftime("%d/%m/%Y alle %H:%M")
        date_label = QLabel(f"Generato il {d_str}")
        date_label.setStyleSheet(
            f"color: {hex_to_rgba(COLORS['bg_white'], 0.6)}; font-size: 12px; margin-top: 5px;"
        )
        layout.addWidget(date_label)

        return self.header

    def _build_stats_frame(self) -> QFrame:
        """Costruisce il frame delle statistiche riepilogative."""
        self.stats_frame = QFrame()
        self.stats_frame.setStyleSheet(
            f"QFrame {{ background-color: {COLORS['bg_white']}; border-bottom: 1px solid {COLORS['border_light']}; }}"
        )
        layout = QHBoxLayout(self.stats_frame)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(40)

        # Calcoli
        stats = self._calculate_metrics()

        layout.addWidget(self._create_stat_card("Totale Monitorati", stats["total"], COLORS["info_blue"]))
        layout.addWidget(self._create_stat_card("Scaduti", stats["scaduti"], COLORS["error_red"]))
        layout.addWidget(
            self._create_stat_card(
                f"Urgenti (0-{THRESHOLD_URGENT}gg)", stats["urgenti"], COLORS["warning_orange"]
            )
        )
        layout.addWidget(
            self._create_stat_card(
                f"Attenzione ({THRESHOLD_URGENT + 1}-{THRESHOLD_ATTENTION}gg)",
                stats["attenzione"],
                COLORS["warning_yellow"],
            )
        )
        layout.addWidget(
            self._create_stat_card(
                f"Attivi (>{THRESHOLD_ATTENTION}gg)", stats["attivi"], COLORS["success_dark"]
            )
        )
        layout.addStretch()

        return self.stats_frame

    def _calculate_metrics(self) -> dict[str, int]:
        """Esegue il conteggio dei certificati per categoria."""
        data = self.certificates_data
        return {
            "total": len(data),
            "scaduti": self._count_by_condition(lambda d: d is not None and d < 0),
            "urgenti": self._count_by_condition(lambda d: d is not None and 0 <= d <= THRESHOLD_URGENT),
            "attenzione": self._count_by_condition(
                lambda d: d is not None and THRESHOLD_URGENT < d <= THRESHOLD_ATTENTION
            ),
            "attivi": self._count_by_condition(lambda d: d is not None and d > THRESHOLD_ATTENTION),
        }

    def _count_by_condition(self, condition: Any) -> int:
        """Helper per contare elementi che soddisfano una condizione sui giorni."""
        return len([c for c in self.certificates_data if condition(c["days"])])

    def _build_scroll_area(self) -> QScrollArea:
        """Costruisce l'area di contenuto scrollabile."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {COLORS['bg_light']}; }}")

        self.content_widget = QWidget()
        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        self._add_sections_to_layout(layout)

        if not self.certificates_data:
            empty = QLabel("Nessun certificato in monitoraggio.")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 16px; padding: 40px;")
            layout.addWidget(empty)

        layout.addStretch()
        scroll.setWidget(self.content_widget)
        return scroll

    def _add_sections_to_layout(self, layout: QVBoxLayout) -> None:
        """Aggiunge le sezioni filtrate per stato al layout."""
        for title, condition, color, bg in self._get_section_configs():
            items = [c for c in self.certificates_data if condition(c["days"])]
            if items:
                layout.addWidget(self._create_section(title, items, color, bg))

    def _get_section_configs(self) -> list[tuple[str, Any, str, str]]:
        """Ritorna la configurazione delle sezioni (Titolo, Condizione, Colore, BG)."""
        return [
            ("SCADUTI", lambda d: d is not None and d < 0, COLORS["error_red"], COLORS["bg_error_pastel"]),
            (
                f"IN SCADENZA (0-{THRESHOLD_URGENT} giorni)",
                lambda d: d is not None and 0 <= d <= THRESHOLD_URGENT,
                COLORS["warning_orange"],
                COLORS["bg_warning_pastel"],
            ),
            (
                f"ATTENZIONE ({THRESHOLD_URGENT + 1}-{THRESHOLD_ATTENTION} giorni)",
                lambda d: d is not None and THRESHOLD_URGENT < d <= THRESHOLD_ATTENTION,
                COLORS["warning_yellow"],
                COLORS["bg_attention_pastel"],
            ),
            (
                f"ATTIVI (oltre {THRESHOLD_ATTENTION} giorni)",
                lambda d: d is not None and d > THRESHOLD_ATTENTION,
                COLORS["success_dark"],
                COLORS["bg_success_pastel"],
            ),
            ("DATA NON DISPONIBILE", lambda d: d is None, COLORS["text_muted"], COLORS["bg_alt"]),
        ]

    def _build_footer(self) -> QFrame:
        """Costruisce la sezione footer con i pulsanti di azione."""
        self.footer = QFrame()
        self.footer.setStyleSheet(
            f"QFrame {{ background-color: {COLORS['bg_white']}; border-top: 1px solid {COLORS['border_light']}; }}"
        )
        layout = QHBoxLayout(self.footer)
        layout.setContentsMargins(30, 15, 30, 15)

        info = QLabel(f"Report generato da {__app_name__} v{__version__}")
        info.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 11px;")
        layout.addWidget(info)
        layout.addStretch()

        # Email Button
        email_btn = PrimaryButton("Invia Email")
        email_btn.setStyleSheet(self._get_btn_style(COLORS["success_dark"], COLORS["success_green"]))
        email_btn.clicked.connect(self._send_email)
        layout.addWidget(email_btn)

        layout.addSpacing(10)

        # Close Button
        close_btn = PrimaryButton("Chiudi")
        close_btn.setStyleSheet(self._get_btn_style(COLORS["primary_blue"], COLORS["primary_dark"]))
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        return self.footer

    def _get_btn_style(self, main_color: str, hover_color: str) -> str:
        """Ritorna lo stile CSS per i pulsanti del footer."""
        return f"""
      QPushButton {{ background-color: {main_color}; color: white; border: none; border-radius: 6px; padding: 10px 25px; font-weight: 600; font-size: 14px; }}
      QPushButton:hover {{ background-color: {hover_color}; }}
    """

    def _create_stat_card(self, title: str, value: int, color: str) -> QFrame:
        """Crea una card per le statistiche."""
        card = QFrame()
        card.setStyleSheet(
            f"QFrame {{ background-color: {COLORS['bg_white']}; border: 1px solid {COLORS['border_light']}; border-radius: 8px; padding: 10px; }}"
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)

        val_lbl = QLabel(str(value))
        val_lbl.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tit_lbl = QLabel(title)
        tit_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 500;")
        tit_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(val_lbl)
        layout.addWidget(tit_lbl)
        return card

    def _create_section(self, title: str, items: list[Any], color: str, bg_color: str) -> QFrame:
        """Crea una sezione con elenco certificati."""
        section = QFrame()
        section.setStyleSheet(f"QFrame {{ background-color: {bg_color}; border: none; border-radius: 8px; }}")
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)

        # Header
        h_layout = QHBoxLayout()
        t_label = QLabel(f"{title} ({len(items)})")
        t_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
        h_layout.addWidget(t_label)
        h_layout.addStretch()
        layout.addLayout(h_layout)

        # Separator
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background-color: {color}30;")
        layout.addWidget(sep)

        # Columns
        layout.addLayout(self._build_section_columns_header())

        # Rows
        for item in items:
            layout.addLayout(self._build_item_row(item, color))

        return section

    def _build_section_columns_header(self) -> QHBoxLayout:
        """Crea l'intestazione delle colonne per una sezione."""
        layout = QHBoxLayout()
        layout.setSpacing(15)

        def add_h(
            txt: str,
            min_w: int | None = None,
            policy: QSizePolicy.Policy | None = None,
            align: Qt.AlignmentFlag | None = None,
        ) -> None:
            lbl = QLabel(txt)
            lbl.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px; font-weight: bold;")
            if min_w:
                lbl.setFixedWidth(min_w)
            if policy:
                lbl.setSizePolicy(policy, QSizePolicy.Policy.Preferred)
            if align:
                lbl.setAlignment(align)
            layout.addWidget(lbl)

        add_h("ID COEMI", 80)
        add_h("COSTRUTTORE", 100)
        add_h("MODELLO / TIPO", policy=QSizePolicy.Policy.Expanding)
        add_h("MATRICOLA", 110)
        add_h("STATO SCADENZA", 130, align=Qt.AlignmentFlag.AlignRight)
        return layout

    def _build_item_row(self, item: dict[str, Any], color: str) -> QHBoxLayout:
        """Costruisce una riga di dati per un certificato."""
        layout = QHBoxLayout()
        layout.setSpacing(15)

        def add_l(  # noqa: PLR0913
            txt: Any,
            color_v: str,
            weight: str = "normal",
            size: int = 12,
            min_w: int | None = None,
            policy: QSizePolicy.Policy | None = None,
            align: Qt.AlignmentFlag | None = None,
        ) -> None:
            lbl = QLabel(str(txt))
            lbl.setStyleSheet(f"color: {color_v}; font-size: {size}px; font-weight: {weight};")
            if min_w:
                lbl.setFixedWidth(min_w)
            if policy:
                lbl.setSizePolicy(policy, QSizePolicy.Policy.Preferred)
            if align:
                lbl.setAlignment(align)
            layout.addWidget(lbl)

        add_l(item.get("id_strumento", ""), COLORS["text_dark"], "600", 13, 80)
        add_l(item["costruttore"], COLORS["text_muted"], min_w=100)

        mod_text = item["modello"]
        if "MANOMETRO DIGITALE" in mod_text.upper() and item.get("range"):
            mod_text += f" ({item['range']})"
        add_l(mod_text, COLORS["text_dark"], policy=QSizePolicy.Policy.Expanding)

        add_l(item["matricola"], COLORS["text_dark"], "600", 13, 110)

        days = item["days"]
        if days is not None:
            txt = f"Scaduto da {abs(days)} gg" if days < 0 else f"Scade tra {days} gg"
        else:
            txt = "N/D"
        add_l(txt, color, "bold", 13, 130, align=Qt.AlignmentFlag.AlignRight)

        return layout

    def _send_email(self) -> None:
        """Genera e invia il report via Outlook asincronamente."""
        try:
            # 1. Cattura immagini e PDF (DEVE stare nel Main Thread)
            image_paths = self._capture_widgets_as_images()
            if not image_paths:
                self._raise_no_images()

            pdf_path = self._generate_audit_pdf()

            # 2. Definiamo la logica pesante di Outlook da eseguire nel Worker
            def outlook_task() -> None:
                import win32com.client  # nosec B403

                outlook = win32com.client.Dispatch("Outlook.Application")
                scaduti_count = self._count_by_condition(lambda d: d is not None and d < 0)
                nd_count = self._count_by_condition(lambda d: d is None)

                mail = outlook.CreateItem(0)
                mail.To = "laboratoriostrumenti@coemi.it"
                mail.CC = "ciro.scaravelli@coemi.it"
                mail.Subject = self._build_email_subject(scaduti_count, nd_count)

                if scaduti_count > 0:
                    mail.Importance = 2  # High

                html_body = self._build_email_body(scaduti_count)

                for i, path in enumerate(image_paths):
                    attachment = mail.Attachments.Add(path)
                    cid = f"img_{i}"
                    attachment.PropertyAccessor.SetProperty(
                        "http://schemas.microsoft.com/mapi/proptag/0x3712001E", cid
                    )
                    html_body += f"<div style='margin-bottom: 20px;'><img src='cid:{cid}' style='max-width: 100%; border: 1px solid #e2e8f0; border-radius: 8px;'></div>"

                html_body += self._build_email_disclaimer()
                html_body += "</body></html>"
                mail.HTMLBody = html_body

                if pdf_path and Path(pdf_path).exists():
                    mail.Attachments.Add(str(pdf_path))

                mail.Display()

            # 3. Avvio Worker
            self._email_worker = OutlookEmailWorker(outlook_task)
            self._email_worker.finished_signal.connect(
                lambda ok, msg: self._cleanup_temp_images(image_paths)
                if ok
                else QMessageBox.critical(self, "Errore", msg)
            )
            self._email_worker.start()

        except Exception as e:
            logger.exception("Inizializzazione invio email fallita")
            QMessageBox.critical(self, "Errore", str(e))

    def _build_email_disclaimer(self) -> str:
        """Costruisce il disclaimer di sistema per il fondo pagina."""
        last_update = datetime.now().strftime("%d/%m/%Y alle %H:%M")
        return f"""
            <div style='margin-top: 40px; padding: 15px; background-color: #f8fafc; border-left: 4px solid #cbd5e1; color: #64748b; font-size: 12px;'>
                <p style='margin: 0;'><b>Disclaimer Sistema</b></p>
                <p style='margin: 5px 0 0 0;'>Questa è un'email generata dal sistema Autopilot di SyncroJob v{__version__}. L'ultimo aggiornamento del database è avvenuto il {last_update}.</p>
            </div>
        """

    def _build_email_subject(self, scaduti: int, nd: int) -> str:
        """Costruisce l'oggetto dell'email basandosi sull'urgenza."""
        prefix = "[URGENTE] " if scaduti > 0 else ""
        details = []
        if scaduti > 0:
            details.append(f"{scaduti} Scaduti")
        if nd > 0:
            details.append(f"{nd} N/D")

        details_str = f" ({', '.join(details)})" if details else ""
        date_str = datetime.now().strftime("%d/%m/%Y")
        return f"{prefix}AUDIT CERTIFICATI STRUMENTALI ISAB SUD - {date_str}{details_str}"

    def _build_email_body(self, scaduti_count: int) -> str:
        """Costruisce la parte iniziale dell'HTML body."""
        cta_html = ""
        if scaduti_count > 0:
            cta_html = f"<p style='color: #b91c1c; font-weight: bold; font-size: 16px; margin-top: 20px;'>⚠️ Si prega di provvedere alla programmazione delle tarature per gli strumenti scaduti ({scaduti_count}).</p>"

        return f"""
            <html>
            <body style='font-family: Segoe UI, Arial, sans-serif;'>
                <h2 style='color: #1e3a8a;'>Monitoraggio Scadenze Certificati - Stabilimento ISAB SUD</h2>
                <p>Per un’analisi approfondita, consultare il PDF allegato contenente il tracciato storico delle verifiche periodiche.</p>
                <p>Vengono evidenziate di seguito le principali anomalie e le scadenze che richiedono attenzione immediata:</p>
                {cta_html}
        """

    def _generate_audit_pdf(self) -> str | None:  # noqa: C901
        """Genera un file PDF temporaneo con lo storico ed escludendo gli ASSENTI e gli ATTIVI."""
        if not self.tree_widget or not self.engine:
            return None

        from src.gui.widgets.contabilita.certificati.pdf_exporter import CertificatiPdfExporter

        # 1. Nascondi temporaneamente gli ASSENTI e gli ATTIVI
        visibility_map = {}
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if not item:
                continue
            visibility_map[i] = not item.isHidden()
            is_absent = False
            is_active = False
            is_special = False
            if item.childCount() > 0:
                child = item.child(0)
                if child:
                    child_loc = child.text(self.tree_widget.IDX_UBICAZIONE).upper()
                    is_absent = UbicazioneStrumenti.ASSENTE.value in child_loc
                    scadenza_str = child.text(self.tree_widget.IDX_SCADENZA)
                    days, _ = self.engine.calculate_days_and_status(scadenza_str)
                    if days is not None and days > THRESHOLD_ATTENTION:
                        is_active = True
                    user_data = item.data(0, Qt.ItemDataRole.UserRole)
                    if user_data and user_data.get("days") in (-9999, -8888, -7777):
                        is_special = True
            if is_absent or is_active or is_special:
                item.setHidden(True)

        # 2. Genera PDF
        temp_pdf = os.path.join(
            tempfile.gettempdir(),
            f"Audit Certificati Strumentali ISAB SUD del {datetime.now().strftime('%d_%m_%Y')}.pdf",
        )
        exporter = CertificatiPdfExporter(
            self.tree_widget,
            show_excluded=self.show_excluded,
            include_history=True,
            print_exclusions=self.engine._print_exclusions,
        )
        success, _ = exporter.export(temp_pdf)

        # 3. Ripristina visibilità
        for i, was_visible in visibility_map.items():
            t_item = self.tree_widget.topLevelItem(i)
            if t_item:
                t_item.setHidden(not was_visible)
        return temp_pdf if success else None

    def _raise_no_images(self) -> None:
        """Lancia eccezione per mancanza immagini."""
        msg = "Nessuna immagine generata."
        raise ValueError(msg)

    def _cleanup_temp_images(self, paths: list[str]) -> None:
        """Rimuove i file temporanei delle immagini."""
        for p in paths:
            with suppress(Exception):
                Path(p).unlink()

    def _capture_widgets_as_images(self) -> list[str]:
        """Cattura solo gli screenshot delle sezioni critiche."""
        widgets: list[QWidget] = []
        layout = self.content_widget.layout()
        if layout:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and (w := item.widget()):
                    title_label = w.findChild(QLabel)
                    if title_label:
                        text = title_label.text().upper()
                        if any(x in text for x in ("SCADUTI", "IN SCADENZA", "DATA NON DISPONIBILE")):
                            widgets.append(w)
        paths = []
        temp_dir = tempfile.gettempdir()
        for i, w in enumerate(widgets):
            w.adjustSize()
            px = w.grab()
            if not px.isNull():
                p = os.path.join(temp_dir, f"syncro_audit_part_{i}.png")
                if px.save(p, "PNG"):
                    paths.append(p)
        return paths
