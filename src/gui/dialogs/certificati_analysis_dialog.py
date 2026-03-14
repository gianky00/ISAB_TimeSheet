"""
SyncroJob - Certificati Analysis Dialog
Modulo specializzato per la visualizzazione e l'esportazione delle scadenze certificati.
"""

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtWidgets import (
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

from src.core import config_manager
from src.core.version import __app_name__, __version__
from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.gui.widgets.core_widgets import PrimaryButton


class ScadenzeAnalysisDialog(QDialog):
    """Finestra di analisi scadenze certificati - Design professionale."""

    def __init__(self, certificates_data: list[Any], parent=None):
        super().__init__(parent)
        self.certificates_data = certificates_data

        # Widget members
        self.header: QFrame
        self.stats_frame: QFrame
        self.content_widget: QWidget
        self.footer: QFrame

        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle(f"Analisi Scadenze Certificati - {__app_name__}")
        self.setMinimumSize(900, 650)
        self.setStyleSheet(
            f"""
            QDialog {{
                background-color: {COLORS["bg_light"]};
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # === HEADER ===
        header = self.header = QFrame()
        header.setStyleSheet(
            f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS["glass_dark"]}, stop:1 {COLORS["glass_deep"]});
                border: none;
            }}
            """
        )
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(30, 25, 30, 25)

        # Titolo e versione
        title_row = QHBoxLayout()
        title_label = QLabel("Analisi Scadenze Certificati")
        title_label.setStyleSheet(f"color: {COLORS['bg_white']}; font-size: 24px; font-weight: bold;")
        title_row.addWidget(title_label)
        title_row.addStretch()

        version_label = QLabel(f"{__app_name__} v{__version__}")
        version_label.setStyleSheet(f"color: {hex_to_rgba(COLORS['bg_white'], 0.7)}; font-size: 13px;")
        title_row.addWidget(version_label)
        header_layout.addLayout(title_row)

        # Data analisi
        date_label = QLabel(f"Generato il {datetime.now(UTC).astimezone().strftime('%d/%m/%Y alle %H:%M')}")
        date_label.setStyleSheet(
            f"color: {hex_to_rgba(COLORS['bg_white'], 0.6)}; font-size: 12px; margin-top: 5px;"
        )
        header_layout.addWidget(date_label)

        layout.addWidget(header)

        # === STATISTICHE ===
        stats_frame = self.stats_frame = QFrame()
        stats_frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {COLORS["bg_white"]};
                border-bottom: 1px solid {COLORS["border_light"]};
            }}
            """
        )
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(30, 20, 30, 20)
        stats_layout.setSpacing(40)

        # Calcola statistiche
        scaduti = [c for c in self.certificates_data if c["days"] is not None and c["days"] < 0]
        urgenti = [c for c in self.certificates_data if c["days"] is not None and 0 <= c["days"] <= 15]
        attenzione = [c for c in self.certificates_data if c["days"] is not None and 16 <= c["days"] <= 30]
        attivi = [c for c in self.certificates_data if c["days"] is not None and c["days"] > 30]
        non_disp = [c for c in self.certificates_data if c["days"] is None]

        stats_layout.addWidget(
            self._create_stat_card("Totale Monitorati", len(self.certificates_data), COLORS["info_blue"])
        )
        stats_layout.addWidget(self._create_stat_card("Scaduti", len(scaduti), COLORS["error_red"]))
        stats_layout.addWidget(
            self._create_stat_card("Urgenti (0-15gg)", len(urgenti), COLORS["warning_orange"])
        )
        stats_layout.addWidget(
            self._create_stat_card("Attenzione (16-30gg)", len(attenzione), COLORS["warning_yellow"])
        )
        stats_layout.addWidget(self._create_stat_card("Attivi (>30gg)", len(attivi), COLORS["success_dark"]))
        stats_layout.addStretch()

        layout.addWidget(stats_frame)

        # === CONTENUTO SCROLLABILE ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            f"""
            QScrollArea {{
                border: none;
                background-color: {COLORS["bg_light"]};
            }}
            """
        )

        content = self.content_widget = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 20, 30, 20)
        content_layout.setSpacing(20)

        # Sezioni per stato
        if scaduti:
            content_layout.addWidget(
                self._create_section("SCADUTI", scaduti, COLORS["error_red"], COLORS["bg_error_pastel"])
            )
        if urgenti:
            content_layout.addWidget(
                self._create_section(
                    "IN SCADENZA (0-15 giorni)",
                    urgenti,
                    COLORS["warning_orange"],
                    COLORS["bg_warning_pastel"],
                )
            )
        if attenzione:
            content_layout.addWidget(
                self._create_section(
                    "ATTENZIONE (16-30 giorni)",
                    attenzione,
                    COLORS["warning_yellow"],
                    COLORS["bg_attention_pastel"],
                )
            )
        if attivi:
            content_layout.addWidget(
                self._create_section(
                    "ATTIVI (oltre 30 giorni)", attivi, COLORS["success_dark"], COLORS["bg_success_pastel"]
                )
            )
        if non_disp:
            content_layout.addWidget(
                self._create_section("DATA NON DISPONIBILE", non_disp, COLORS["text_muted"], COLORS["bg_alt"])
            )

        if not self.certificates_data:
            empty_label = QLabel("Nessun certificato in monitoraggio.")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 16px; padding: 40px;")
            content_layout.addWidget(empty_label)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        # === FOOTER ===
        footer = self.footer = QFrame()
        footer.setStyleSheet(
            f"""
            QFrame {{
                background-color: {COLORS["bg_white"]};
                border-top: 1px solid {COLORS["border_light"]};
            }}
            """
        )
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(30, 15, 30, 15)

        footer_info = QLabel(f"Report generato da {__app_name__} v{__version__}")
        footer_info.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 11px;")
        footer_layout.addWidget(footer_info)
        footer_layout.addStretch()

        # Pulsante Invia Email
        email_btn = PrimaryButton("Invia Email")
        email_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {COLORS["success_dark"]};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 25px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {COLORS["success_green"]};
            }}
        """
        )
        email_btn.clicked.connect(self._send_email)
        footer_layout.addWidget(email_btn)

        footer_layout.addSpacing(10)

        close_btn = PrimaryButton("Chiudi")
        close_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {COLORS["primary_blue"]};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 30px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {COLORS["primary_dark"]};
            }}
            """
        )
        close_btn.clicked.connect(self.accept)
        footer_layout.addWidget(close_btn)

        layout.addWidget(footer)

    def _create_stat_card(self, title: str, value: int, color: str) -> QFrame:
        """Crea una card per le statistiche."""
        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 8px;
                padding: 10px;
            }}
            """
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 10, 15, 10)
        card_layout.setSpacing(5)

        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 500;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout.addWidget(value_label)
        card_layout.addWidget(title_label)

        return card

    def _create_section(self, title: str, items: list[Any], color: str, bg_color: str) -> QFrame:
        """Crea una sezione con elenco certificati."""
        section = QFrame()
        section.setStyleSheet(
            f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {color}40;
                border-radius: 8px;
            }}
            """
        )
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(20, 15, 20, 15)
        section_layout.setSpacing(10)

        # Header sezione
        header_layout = QHBoxLayout()
        title_label = QLabel(f"{title} ({len(items)})")
        title_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        section_layout.addLayout(header_layout)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"background-color: {color}30;")
        sep.setFixedHeight(1)
        section_layout.addWidget(sep)

        # Items
        for item in items:
            item_layout = QHBoxLayout()
            item_layout.setSpacing(15)

            # Matricola
            matricola_label = QLabel(item["matricola"])
            matricola_label.setStyleSheet(
                f"color: {color}; font-weight: 600; font-size: 13px; min-width: 120px;"
            )
            item_layout.addWidget(matricola_label)

            # Modello + Range (per manometri)
            modello_text = item["modello"]
            if "MANOMETRO DIGITALE" in modello_text.upper() and item.get("range"):
                modello_text += f" ({item['range']})"
            modello_label = QLabel(modello_text)
            modello_label.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 12px;")
            modello_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            item_layout.addWidget(modello_label)

            # Costruttore
            costruttore_label = QLabel(item["costruttore"])
            costruttore_label.setStyleSheet(
                f"color: {COLORS['text_muted']}; font-size: 12px; min-width: 100px;"
            )
            item_layout.addWidget(costruttore_label)

            # Scadenza
            if item["days"] is not None:
                if item["days"] < 0:
                    days_text = f"Scaduto da {abs(item['days'])} gg"
                else:
                    days_text = f"Scade tra {item['days']} gg"
            else:
                days_text = "N/D"
            days_label = QLabel(days_text)
            days_label.setStyleSheet(f"color: {color}; font-weight: 500; font-size: 12px; min-width: 130px;")
            days_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            item_layout.addWidget(days_label)

            section_layout.addLayout(item_layout)

        return section

    def _send_email(self):
        """Genera screenshot completo del report e apre il client email."""
        import subprocess
        import tempfile

        try:
            # Assicura che il layout sia aggiornato e calcolato prima del rendering
            self.header.adjustSize()
            self.stats_frame.adjustSize()
            self.content_widget.adjustSize()
            self.footer.adjustSize()

            # Calcola l'altezza totale del contenuto con margini di sicurezza
            header_height = self.header.height()
            stats_height = self.stats_frame.height()
            content_height = self.content_widget.height()
            footer_height = self.footer.height()

            total_height = header_height + stats_height + content_height + footer_height + 40

            # Limite di sicurezza per evitare allocazioni pixmap troppo grandi
            total_height = min(total_height, 15000)
            total_width = max(900, self.width())

            # Crea un pixmap per il report completo
            pixmap = QPixmap(total_width, total_height)
            pixmap.fill(QColor(COLORS["bg_light"]))

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Header
            self.header.render(painter, targetOffset=self.header.pos())

            # Stats
            self.stats_frame.render(
                painter,
                targetOffset=self.stats_frame.mapTo(self, self.stats_frame.rect().topLeft()),
            )

            # Content
            self.content_widget.render(
                painter,
                targetOffset=self.content_widget.mapTo(self, self.content_widget.rect().topLeft()),
            )

            painter.end()

            # Salva come PNG temporaneo
            temp_path = os.path.join(tempfile.gettempdir(), "syncrojob_scadenze_report.png")
            pixmap.save(temp_path, "PNG")

            # Tenta di usare la macro Excel se configurata
            excel_path = config_manager.load_config().get("certificati_campione_path", "")

            if excel_path and Path(excel_path).exists():
                ps_script = f"""
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$wb = $xl.Workbooks.Open("{excel_path.replace(chr(92), chr(92) + chr(92))}")
try {{
    $xl.Run("'" + $wb.Name + "'!InviaEmailConScreenshotDaPS", "{temp_path.replace(chr(92), chr(92) + chr(92))}")
}} catch {{
    Start-Process "{temp_path.replace(chr(92), chr(92) + chr(92))}"
}}
$wb.Close($false)
$xl.Quit()
"""
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".ps1", delete=False, encoding="utf-8"
                ) as tmp:
                    tmp.write(ps_script)
                    ps_path = tmp.name

                CREATE_NO_WINDOW = 0x08000000
                subprocess.Popen(
                    ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_path],
                    creationflags=CREATE_NO_WINDOW,
                )

                QMessageBox.information(
                    self,
                    "Email in preparazione",
                    "Lo screenshot del report è stato generato.\n\n"
                    f"Percorso: {temp_path}\n\n"
                    "Se configurata, la macro Excel invierà l'email automaticamente.",
                )
            else:
                # Se non c'è excel, apri solo lo screenshot
                os.startfile(temp_path)  # noqa: S606

        except Exception as e:
            QMessageBox.critical(self, "Errore invio email", f"Impossibile generare il report:\n{e}")
