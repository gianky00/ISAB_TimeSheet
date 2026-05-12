"""
SyncroJob - Certificati Analysis Dialog
Modulo specializzato per la visualizzazione e l'esportazione delle scadenze certificati.
"""

import os
import tempfile
from datetime import UTC, datetime
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

from src.core.constants import UbicazioneStrumenti
from src.core.version import __app_name__, __version__
from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.gui.widgets.core_widgets import PrimaryButton

# Soglie giorni per scadenze
THRESHOLD_URGENT = 15
THRESHOLD_ATTENTION = 30


class ScadenzeAnalysisDialog(QDialog):
    """Finestra di analisi scadenze certificati - Design professionale."""

    def __init__(
        self,
        certificates_data: list[Any],
        show_excluded: bool = False,
        parent: QWidget | None = None,
        tree_widget: Any | None = None,
        engine: Any | None = None,
    ) -> None:
        super().__init__(parent)

        # Filtriamo gli strumenti ASSENTI immediatamente (Richiesta Utente)
        self.certificates_data = [
            c for c in certificates_data
            if UbicazioneStrumenti.ASSENTE.value not in str(c.get("ubicazione", "")).upper()
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
        """Genera e invia il report via Outlook con screenshot degli stati critici e PDF allegato."""
        try:
            # 1. Importazione win32com
            try:
                import win32com.client
            except ImportError as err:
                raise ImportError("Libreria 'pywin32' non trovata. Contattare l'amministratore.") from err

            # 2. Cattura immagini dei widget (Scaduti, In Scadenza, N/D)
            image_paths = self._capture_widgets_as_images()
            if not image_paths:
                self._raise_no_images()

            # 3. Inizializzazione Outlook
            try:
                outlook = win32com.client.Dispatch("Outlook.Application")
            except Exception as err:
                raise RuntimeError("Impossibile connettersi a Outlook. Assicurarsi che sia installato e configurato.") from err

            # Calcolo urgenza per oggetto e CTA
            scaduti_count = self._count_by_condition(lambda d: d is not None and d < 0)
            nd_count = self._count_by_condition(lambda d: d is None)

            prefix = "[URGENTE] " if scaduti_count > 0 else ""

            # Costruzione dettagli oggetto
            details = []
            if scaduti_count > 0:
                details.append(f"{scaduti_count} Scaduti")
            if nd_count > 0:
                details.append(f"{nd_count} N/D")

            details_str = f" ({', '.join(details)})" if details else ""

            mail = outlook.CreateItem(0)
            mail.To = "andrea.litrico@coemi.it"
            mail.CC = "ciro.scaravelli@coemi.it"
            mail.Subject = f"{prefix}AUDIT CERTIFICATI STRUMENTALI ISAB SUD - {datetime.now().strftime('%d/%m/%Y')}{details_str}"

            # Imposta priorità alta se urgente (Importance: 2 = High, 1 = Normal, 0 = Low)
            if scaduti_count > 0:
                mail.Importance = 2

            # 4. Generazione PDF da allegare (Sempre Storico, No ASSENTI)
            pdf_path = self._generate_audit_pdf()

            # 5. Costruzione HTML Body con immagini embedded
            cta_html = ""
            if scaduti_count > 0:
                cta_html = f"<p style='color: #b91c1c; font-weight: bold; font-size: 16px; margin-top: 20px;'>⚠️ Si prega di provvedere alla programmazione delle tarature per gli strumenti scaduti ({scaduti_count}).</p>"

            last_update = datetime.now().strftime("%d/%m/%Y alle %H:%M")
            disclaimer_html = f"""
                <div style='margin-top: 40px; padding: 15px; background-color: #f8fafc; border-left: 4px solid #cbd5e1; color: #64748b; font-size: 12px;'>
                    <p style='margin: 0;'><b>Disclaimer Sistema</b></p>
                    <p style='margin: 5px 0 0 0;'>Questa è un'email generata dal sistema Autopilot di SyncroJob v{__version__}. L'ultimo aggiornamento del database è avvenuto il {last_update}.</p>
                </div>
            """
            html_body = f"""
                <html>
                <body style='font-family: Segoe UI, Arial, sans-serif;'>
                    <h2 style='color: #1e3a8a;'>Monitoraggio Scadenze Certificati - Stabilimento ISAB SUD</h2>
                    <p>Per un’analisi approfondita, consultare il PDF allegato contenente il tracciato storico delle verifiche periodiche.</p>
                    <p>Vengono evidenziate di seguito le principali anomalie e le scadenze che richiedono attenzione immediata:</p>
                    {cta_html}
            """

            # Alleghiamo le immagini e creiamo i tag IMG con CID
            for i, path in enumerate(image_paths):
                attachment = mail.Attachments.Add(path)
                cid = f"img_part_{i}"
                attachment.PropertyAccessor.SetProperty(
                    "http://schemas.microsoft.com/mapi/proptag/0x3712001E", cid
                )
                html_body += f"<div style='margin-bottom:15px; border: 1px solid #eee;'><img src='cid:{cid}' style='max-width:100%;'></div>"

            # Alleghiamo il PDF se generato correttamente
            if pdf_path and os.path.exists(pdf_path):
                mail.Attachments.Add(pdf_path)

            # Aggiungiamo il disclaimer e chiudiamo l'HTML
            html_body += f"""
                    {disclaimer_html}
                </body>
                </html>
            """

            mail.HTMLBody = html_body
            mail.Display()

            QMessageBox.information(
                self,
                "Email generata",
                "La bozza Outlook è stata creata con successo includendo il report PDF.",
            )

        except Exception as e:
            QMessageBox.critical(self, "Errore invio email", f"Impossibile generare il report:\n{e}")

    def _generate_audit_pdf(self) -> str | None:
        """Genera un file PDF temporaneo con lo storico ed escludendo gli ASSENTI e gli ATTIVI."""
        if not self.tree_widget or not self.engine:
            return None

        from src.gui.widgets.contabilita.certificati.pdf_exporter import CertificatiPdfExporter

        # 1. Nascondi temporaneamente gli ASSENTI e gli ATTIVI nel TreeWidget
        # Salviamo lo stato di visibilità corrente per ripristinarlo
        visibility_map = {}
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if not item:
                continue

            visibility_map[i] = not item.isHidden()

            # Verifica se è ASSENTE o ATTIVO (> 30gg)
            is_absent = False
            is_active = False
            if item.childCount() > 0:
                child = item.child(0)
                if child:
                    child_loc = child.text(self.tree_widget.IDX_UBICAZIONE).upper()
                    is_absent = UbicazioneStrumenti.ASSENTE.value in child_loc

                    # Verifica se è ATTIVO (oltre THRESHOLD_ATTENTION)
                    scadenza_str = child.text(self.tree_widget.IDX_SCADENZA)
                    days, _ = self.engine.calculate_days_and_status(scadenza_str)
                    if days is not None and days > THRESHOLD_ATTENTION:
                        is_active = True

            if is_absent or is_active:
                item.setHidden(True)

        # 2. Genera PDF
        temp_pdf = os.path.join(
            tempfile.gettempdir(),
            f"Audit Certificati Strumentali ISAB SUD del {datetime.now().strftime('%d_%m_%Y')}.pdf"
        )

        exporter = CertificatiPdfExporter(
            self.tree_widget,
            show_excluded=self.show_excluded,
            include_history=True, # Richiesto sempre lo storico
            print_exclusions=self.engine._print_exclusions
        )

        success, _ = exporter.export(temp_pdf)

        # 3. Ripristina visibilità originale
        for i, was_visible in visibility_map.items():
            t_item = self.tree_widget.topLevelItem(i)
            if t_item:
                t_item.setHidden(not was_visible)

        return temp_pdf if success else None

    def _generate_email_table_html(self) -> str:
        """Genera la tabella HTML per il corpo dell'email."""
        rows = ""
        # Ordiniamo per urgenza per l'email
        sorted_data = sorted(
            self.certificates_data, key=lambda x: x["days"] if x["days"] is not None else 9999
        )

        for item in sorted_data:
            days = item["days"]
            # Includiamo solo Scaduti, In Scadenza e N/D
            if days is not None and days > THRESHOLD_ATTENTION:
                continue

            if days is None:
                status_color = COLORS["text_light"]
                status_text = "N/D"
            elif days < 0:
                status_color = COLORS["error_red"]
                status_text = f"SCADUTO ({abs(days)}gg fa)"
            elif days <= THRESHOLD_URGENT:
                status_color = COLORS["warning_orange"]
                status_text = f"SCADENZA ({days}gg)"
            else:
                status_color = COLORS["warning_yellow"]
                status_text = f"ATTENZIONE ({days}gg)"

            rows += f"""
                <tr>
                    <td style="border: 1px solid #ddd; padding: 6px;">{item.get('id_strumento', 'N/D')}</td>
                    <td style="border: 1px solid #ddd; padding: 6px;">{item.get('modello', 'N/D')}</td>
                    <td style="border: 1px solid #ddd; padding: 6px;">{item.get('matricola', 'N/D')}</td>
                    <td style="border: 1px solid #ddd; padding: 6px; color: {status_color}; font-weight: bold;">{status_text}</td>
                </tr>
            """

        return f"""
            <table style="border-collapse: collapse; width: 100%; font-family: Segoe UI, Arial, sans-serif; font-size: 12px; margin-top: 20px;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">ID COEMI</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">MODELLO</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">MATRICOLA</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">STATO</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        """

    def _raise_no_images(self) -> None:
        """Lancia eccezione per mancanza immagini."""
        msg = "Nessuna immagine generata."
        raise ValueError(msg)

    def _capture_widgets_as_images(self) -> list[str]:
        """Cattura solo gli screenshot delle sezioni critiche (Scaduti, In Scadenza, N/D)."""
        widgets: list[QWidget] = []

        layout = self.content_widget.layout()
        if layout:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and (w := item.widget()):
                    # Cerchiamo i widget che contengono i titoli richiesti
                    # Nota: In _create_section il titolo viene impostato in un QLabel
                    text = ""
                    title_label = w.findChild(QLabel)
                    if title_label:
                        text = title_label.text().upper()

                    if "SCADUTI" in text or "IN SCADENZA" in text or "DATA NON DISPONIBILE" in text:
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
