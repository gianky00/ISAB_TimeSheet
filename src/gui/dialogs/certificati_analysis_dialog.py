# mypy: disable-error-code="no-untyped-def, no-untyped-call, unused-ignore, arg-type"
"""
SyncroJob - Certificati Analysis Dialog
Modulo specializzato per la visualizzazione e l'esportazione delle scadenze certificati.
"""

import os
import subprocess
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

from src.core.version import __app_name__, __version__
from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.gui.widgets.core_widgets import PrimaryButton

# Soglie giorni per scadenze
THRESHOLD_URGENT = 15
THRESHOLD_ATTENTION = 30


class ScadenzeAnalysisDialog(QDialog):
    """Finestra di analisi scadenze certificati - Design professionale."""

    def __init__(self, certificates_data: list[Any], show_excluded: bool = False, parent=None):  # noqa: ANN001, ANN204
        super().__init__(parent)
        self.certificates_data = certificates_data
        self.show_excluded = show_excluded

        # Widget members
        self.header: QFrame
        self.stats_frame: QFrame
        self.content_widget: QWidget
        self.footer: QFrame

        self._setup_ui()

    def _setup_ui(self):  # noqa: ANN202
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

        add_h("ID-COEMI", 80)
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

        add_l(item.get("id_coemi", ""), COLORS["text_dark"], "600", 13, 80)
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
        """Genera e invia il report via Outlook."""
        try:
            image_paths = self._capture_widgets_as_images()
            if not image_paths:
                self._raise_no_images()

            self._execute_outlook_powershell(image_paths)

            QMessageBox.information(
                self,
                "Email in preparazione",
                "Il report  stato suddiviso in sezioni ed inserito in una nuova email Outlook.",
            )

        except Exception as e:
            QMessageBox.critical(self, "Errore invio email", f"Impossibile generare il report:\n{e}")

    def _raise_no_images(self) -> None:
        """Lancia eccezione per mancanza immagini."""
        msg = "Nessuna immagine generata."
        raise ValueError(msg)

    def _capture_widgets_as_images(self) -> list[str]:
        """Cattura tutti i componenti visuali come immagini PNG temporanee."""
        widgets = [self.header, self.stats_frame]

        layout = self.content_widget.layout()
        if layout:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and (w := item.widget()):
                    widgets.append(w)

        widgets.append(self.footer)

        paths = []
        temp_dir = tempfile.gettempdir()
        for i, w in enumerate(widgets):
            w.adjustSize()
            px = w.grab()
            if not px.isNull():
                p = os.path.join(temp_dir, f"syncro_report_part_{i}.png")
                if px.save(p, "PNG"):
                    paths.append(p)
        return paths

    def _execute_outlook_powershell(self, images: list[str]) -> None:
        """Esegue lo script PowerShell per generare l'email con immagini embedded."""
        img_list = "@('" + "','".join(p.replace("\\", "\\\\") for p in images) + "')"

        ps = f"""
    $images = {img_list}
    try {{
      $o = New-Object -ComObject Outlook.Application
      $m = $o.CreateItem(0)
      $m.Subject = "Report Analisi Scadenze Certificati - $(Get-Date -Format 'dd/MM/yyyy')"
      $html = "<html><body><h3>Report Scadenze Certificati Campione</h3>"
      $idx = 0
      foreach ($img in $images) {{
        $att = $m.Attachments.Add($img)
        $att.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001E", "img_$idx")
        $html += "<div style='margin-bottom:10px;'><img src='cid:img_$idx' style='max-width:100%;'></div>"
        $idx++
      }}
      $html += "<p style='font-size:10px;color:#666;'>Generato da SyncroJob v{__version__}</p></body></html>"
      $m.HTMLBody = $html
      $m.Display()
    }} catch {{ Start-Process "explorer.exe" (Split-Path $images[0]) }}
    """

        with tempfile.NamedTemporaryFile(mode="w", suffix=".ps1", delete=False, encoding="utf-8") as f:
            f.write(ps)
            ps_path = f.name

        subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_path], creationflags=0x08000000
        )
