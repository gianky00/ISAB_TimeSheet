import json
import operator
import os
from collections import defaultdict
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, ClassVar

from src.gui.widgets.core_widgets import PrimaryButton, SecondaryButton, SearchInput, FilterComboBox, StandardTable, DangerButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QBrush, QColor, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.config_manager import CONFIG_DIR
from src.core.constants import Icons
from src.core.contabilita_manager import ContabilitaManager
from src.core.version import __app_name__, __version__
from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.gui.widgets.contabilita.helpers import SortableTreeWidgetItem
from src.utils.helpers import get_asset_path


class ScadenzeAnalysisDialog(QDialog):
    """Finestra di analisi scadenze certificati - Design professionale."""

    def __init__(self, certificates_data: list[Any], parent=None):
        super().__init__(parent)
        self.certificates_data = certificates_data

        # Widget members (Strict Typing - Option D)
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
                background-color: {COLORS['bg_light']};
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
                    stop:0 {COLORS['glass_dark']}, stop:1 {COLORS['glass_deep']});
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
        date_label = QLabel(f"Generato il {datetime.now().strftime('%d/%m/%Y alle %H:%M')}")
        date_label.setStyleSheet(f"color: {hex_to_rgba(COLORS['bg_white'], 0.6)}; font-size: 12px; margin-top: 5px;")
        header_layout.addWidget(date_label)

        layout.addWidget(header)

        # === STATISTICHE ===
        stats_frame = self.stats_frame = QFrame()
        stats_frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {COLORS['bg_white']};
                border-bottom: 1px solid {COLORS['border_light']};
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
        stats_layout.addWidget(self._create_stat_card("Urgenti (0-15gg)", len(urgenti), COLORS["warning_orange"]))
        stats_layout.addWidget(self._create_stat_card("Attenzione (16-30gg)", len(attenzione), COLORS["warning_yellow"]))
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
                background-color: {COLORS['bg_light']};
            }}
            """
        )

        content = self.content_widget = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 20, 30, 20)
        content_layout.setSpacing(20)

        # Sezioni per stato
        if scaduti:
            content_layout.addWidget(self._create_section("SCADUTI", scaduti, COLORS["error_red"], COLORS["bg_error_pastel"]))
        if urgenti:
            content_layout.addWidget(
                self._create_section("IN SCADENZA (0-15 giorni)", urgenti, COLORS["warning_orange"], COLORS["bg_warning_pastel"])
            )
        if attenzione:
            content_layout.addWidget(
                self._create_section("ATTENZIONE (16-30 giorni)", attenzione, COLORS["warning_yellow"], COLORS["bg_attention_pastel"])
            )
        if attivi:
            content_layout.addWidget(
                self._create_section("ATTIVI (oltre 30 giorni)", attivi, COLORS["success_dark"], COLORS["bg_success_pastel"])
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
                background-color: {COLORS['bg_white']};
                border-top: 1px solid {COLORS['border_light']};
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
                background-color: {COLORS['success_dark']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 25px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['success_green']};
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
                background-color: {COLORS['primary_blue']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 30px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_dark']};
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
                background-color: {COLORS['bg_white']};
                border: 1px solid {COLORS['border_light']};
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
            costruttore_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px; min-width: 100px;")
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

            # Limite di sicurezza per evitare allocazioni pixmap troppo grandi (es. report infiniti)
            total_height = min(total_height, 15000)
            total_width = max(900, self.width())

            # Crea un pixmap per il report completo
            pixmap = QPixmap(total_width, total_height)
            pixmap.fill(QColor(COLORS["bg_light"]))

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Renderizza ogni sezione
            y_offset = 0

            # Header
            self.header.render(painter, targetOffset=self.header.pos())
            y_offset += header_height

            # Stats
            self.stats_frame.render(
                painter,
                targetOffset=self.stats_frame.mapTo(self, self.stats_frame.rect().topLeft()),
            )
            y_offset += stats_height

            # Content (renderizza il widget interno dello scroll, non lo scroll)
            self.content_widget.render(
                painter,
                targetOffset=self.content_widget.mapTo(self, self.content_widget.rect().topLeft()),
            )

            painter.end()

            # Salva come PNG temporaneo
            temp_path = os.path.join(tempfile.gettempdir(), "syncrojob_scadenze_report.png")
            pixmap.save(temp_path, "PNG")

            # Tenta di usare la macro Excel se configurata, altrimenti apre file manager
            excel_path = config_manager.load_config().get("certificati_campione_path", "")

            if excel_path and Path(excel_path).exists():
                # Prova ad eseguire la macro Excel per inviare email
                try:
                    ps_script = f"""
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$wb = $xl.Workbooks.Open("{excel_path.replace(chr(92), chr(92) + chr(92))}")
try {{
    $xl.Run("'" + $wb.Name + "'!InviaEmailConScreenshotDaPS", "{temp_path.replace(chr(92), chr(92) + chr(92))}")
}} catch {{
    # Se la macro non esiste, apri solo il file
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
                        f"Lo screenshot del report è stato generato.\n\n"
                        f"Percorso: {temp_path}\n\n"
                        "Se configurata, la macro Excel invierà l'email automaticamente.",
                    )
                except Exception:
                    # Fallback: apri il file
                    os.startfile(temp_path)  # noqa: S606
                    QMessageBox.information(
                        self,
                        "Screenshot salvato",
                        f"Lo screenshot è stato salvato in:\n{temp_path}\n\n"
                        "Puoi allegarlo manualmente alla tua email.",
                    )
            else:
                # Apri il file direttamente
                os.startfile(temp_path)  # noqa: S606
                QMessageBox.information(
                    self,
                    "Screenshot salvato",
                    f"Lo screenshot è stato salvato in:\n{temp_path}\n\n"
                    "Puoi allegarlo manualmente alla tua email.",
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Errore",
                f"Impossibile generare lo screenshot:\n{e}",
            )


class CertificatiCampioneTab(QWidget):
    """Tab per Certificati Campione (Tree View)."""

    # File per memorizzare le esclusioni
    EXCLUSIONS_FILE: ClassVar[Path] = CONFIG_DIR / "data" / "certificati_exclusions.json"

    # Stile per elementi esclusi
    EXCLUDED_STYLE: ClassVar[str] = f"""
        color: {COLORS['text_light']};
        text-decoration: line-through;
    """

    HEADERS: ClassVar[list[str]] = [
        "Modello /\nTipo",
        "Costruttore",
        "Matricola",
        "Range\nStrumento",
        "Errore\nmax %",
        "Certificato\nTaratura",
        "Scadenza\nCertificato",
        "Emissione\nCertificato",
        "ID-COEMI",
        "Stato\nCertificato",
    ]
    (
        IDX_MODELLO,
        IDX_COSTRUTTORE,
        IDX_MATRICOLA,
        IDX_RANGE,
        IDX_ERRORE,
        IDX_CERTIFICATO,
        IDX_SCADENZA,
        IDX_EMISSIONE,
        IDX_ID,
        IDX_STATO,
    ) = range(10)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Widget members (Strict Typing - Option D)
        self.tree: QTreeWidget
        self.show_excluded_check: QCheckBox
        self.excluded_count_label: QLabel
        self.btn_analyze: QPushButton

        self._exclusions: set[str] = set()  # Set di matricole escluse
        self._show_excluded = False  # Flag per mostrare/nascondere esclusi
        self._load_exclusions()
        self._setup_ui()
        self._load_data()

    def _load_exclusions(self):
        """Carica le esclusioni dal file JSON."""
        with suppress(Exception):
            if self.EXCLUSIONS_FILE.exists():
                with self.EXCLUSIONS_FILE.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._exclusions = set(data.get("excluded_matricole", []))

    def _save_exclusions(self):
        """Salva le esclusioni nel file JSON."""
        with suppress(Exception):
            # Assicura che la directory esista
            self.EXCLUSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with self.EXCLUSIONS_FILE.open("w", encoding="utf-8") as f:
                json.dump(
                    {"excluded_matricole": list(self._exclusions)},
                    f,
                    indent=2,
                    ensure_ascii=False,
                )

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        # Tree widget configuration
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(self.HEADERS)
        self.tree.setWordWrap(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setAnimated(True)  # Animazione per expand/collapse

        # Header configuration con larghezza dinamica per evitare troncamenti
        h = self.tree.header()
        if h is None:
            raise RuntimeError("Tree header is None")
        # Imposta tutte le colonne a ResizeToContents per adattarsi al contenuto
        for col in range(10):
            h.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        # L'ultima colonna (Stato) può anche espandersi
        h.setStretchLastSection(True)

        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)

        # Stile personalizzato per il tree
        self.tree.setStyleSheet(
            f"""
            QTreeWidget {{
                border: 1px solid {COLORS['border_light']};
                border-radius: 8px;
                background-color: {COLORS['bg_white']};
                outline: none;
            }}
            QTreeWidget::item {{
                padding: 8px 4px;
                border-bottom: 1px solid {COLORS['bg_alt']};
            }}
            QTreeWidget::item:hover {{
                background-color: {COLORS['bg_light']};
            }}
            QTreeWidget::item:selected {{
                background-color: {COLORS['bg_info_pastel']};
                color: {COLORS['primary_dark']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_light']};
                padding: 10px 8px;
                border: none;
                border-bottom: 2px solid {COLORS['border_light']};
                border-right: 1px solid {COLORS['border_light']};
                font-weight: bold;
                color: {COLORS['text_muted']};
            }}
        """
        )

        # Toolbar con pulsanti migliorati
        toolbar = QHBoxLayout()

        # Gruppo espansione
        btn_expand = PrimaryButton("Espandi Tutto")
        btn_expand.setIcon(QIcon(get_asset_path(Icons.FOLDER_OPEN)))
        btn_expand.clicked.connect(self.tree.expandAll)
        btn_expand.setStyleSheet(
            f"""
            QPushButton {{
                padding: 8px 16px;
                background-color: {COLORS['bg_alt']};
                border: 1px solid {COLORS['border_medium']};
                border-radius: 6px;
                font-weight: 500;
                color: {COLORS['text_dark']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_hover']};
            }}
        """
        )

        btn_collapse = PrimaryButton("Comprimi Tutto")
        btn_collapse.setIcon(QIcon(get_asset_path(Icons.FOLDER)))
        btn_collapse.clicked.connect(self.tree.collapseAll)
        btn_collapse.setStyleSheet(
            f"""
            QPushButton {{
                padding: 8px 16px;
                background-color: {COLORS['bg_alt']};
                border: 1px solid {COLORS['border_medium']};
                border-radius: 6px;
                font-weight: 500;
                color: {COLORS['text_dark']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_hover']};
            }}
        """
        )

        toolbar.addWidget(btn_expand)
        toolbar.addWidget(btn_collapse)
        toolbar.addSpacing(20)

        # Checkbox per mostrare esclusi
        self.show_excluded_check = QCheckBox("Mostra esclusi")
        self.show_excluded_check.setChecked(False)
        self.show_excluded_check.setStyleSheet(
            f"""
            QCheckBox {{
                padding: 8px 12px;
                font-weight: 500;
                color: {COLORS['text_muted']};
            }}
            QCheckBox:hover {{
                color: {COLORS['text_dark']};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
            QCheckBox::indicator:unchecked {{
                border: 2px solid {COLORS['border_medium']};
                border-radius: 4px;
                background: {COLORS['bg_white']};
            }}
            QCheckBox::indicator:checked {{
                border: 2px solid {COLORS['primary_blue']};
                border-radius: 4px;
                background: {COLORS['primary_blue']};
            }}
        """
        )
        self.show_excluded_check.stateChanged.connect(self._on_show_excluded_changed)
        toolbar.addWidget(self.show_excluded_check)

        # Label conteggio esclusi
        self.excluded_count_label = QLabel("")
        self.excluded_count_label.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 12px; padding: 0 8px;")
        toolbar.addWidget(self.excluded_count_label)

        toolbar.addStretch()

        # Pulsante analisi con stile migliorato
        self.btn_analyze = PrimaryButton("Analizza Scadenze")
        self.btn_analyze.setIcon(QIcon(get_asset_path(Icons.BAR_CHART)))
        self.btn_analyze.clicked.connect(self._run_analysis)
        self.btn_analyze.setStyleSheet(
            f"""
            QPushButton {{
                padding: 8px 20px;
                background-color: {COLORS['primary_blue']};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_dark']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['primary_dark']};
            }}
        """
        )
        toolbar.addWidget(self.btn_analyze)

        layout.addLayout(toolbar)
        layout.addWidget(self.tree)

    def _on_show_excluded_changed(self, state):
        """Gestisce il cambio di stato della checkbox 'Mostra esclusi'."""
        self._show_excluded = state == Qt.CheckState.Checked.value
        self._apply_exclusion_visibility()

    def _apply_exclusion_visibility(self):
        """Applica la visibilità agli elementi in base allo stato di esclusione."""
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if parent is None:
                raise RuntimeError(f"Tree topLevelItem({i}) is None")
            matricola = self._extract_matricola_from_parent(parent)
            is_excluded = matricola in self._exclusions

            # Nascondi o mostra in base al flag
            if is_excluded and not self._show_excluded:
                parent.setHidden(True)
            else:
                parent.setHidden(False)

    def _extract_matricola_from_parent(self, parent_item) -> str:
        """Estrae la matricola dal testo del nodo padre."""
        # Il formato è: "matricola  •  costruttore  •  modello  •  days_text"
        if parts := str(parent_item.text(0)).split("  •  "):
            return parts[0].strip()
        return ""

    def _update_excluded_count_label(self):
        """Aggiorna la label con il conteggio degli esclusi."""
        count = len(self._exclusions)
        if count > 0:
            self.excluded_count_label.setText(f"({count} esclusi)")
        else:
            self.excluded_count_label.setText("")

    def refresh_data(self):
        """Ricarica i certificati dal database."""
        self._load_data()

    def _load_data(self):
        """Esegue la query e popola l'albero dei certificati raggruppati per matricola con logica intelligente."""
        data = ContabilitaManager.get_certificati_campione_data()
        self.tree.clear()
        self.tree.setSortingEnabled(False)

        # Step 1: Raggruppa per matricola
        matricola_groups = defaultdict(list)
        for r in data:
            matricola = r[self.IDX_MATRICOLA] or "N/D"
            matricola_groups[matricola].append(r)

        # Step 2: Crea una lista di gruppi con metadati per ordinamento
        groups_with_priority = []

        for matricola, certificates in matricola_groups.items():
            # Ordina per data di emissione (più recente in alto)
            def parse_date(cert):
                date_str = cert[self.IDX_EMISSIONE] or ""
                try:
                    if "/" in date_str:
                        return datetime.strptime(date_str, "%d/%m/%Y").replace(tzinfo=UTC)
                    return datetime.min.replace(tzinfo=UTC)
                except Exception:
                    return datetime.min.replace(tzinfo=UTC)

            certificates_sorted = sorted(certificates, key=parse_date, reverse=True)

            # Step 3: Determina lo stato del certificato più recente (PRIMO della lista)
            latest_cert = certificates_sorted[0]
            modello = latest_cert[self.IDX_MODELLO] or "N/D"
            costruttore = latest_cert[self.IDX_COSTRUTTORE] or "N/D"
            range_strumento = latest_cert[self.IDX_RANGE] or ""

            # Calcola giorni alla scadenza per il certificato più recente
            days_to_expiry, status_dot_icon = self._calculate_days_and_status(latest_cert[self.IDX_SCADENZA])

            # Aggiungi alla lista con priorità per ordinamento
            # Priorità: scaduti (negativo) < prossimi alla scadenza (0-15) < medi (16-30) < attivi (>30)
            priority = days_to_expiry if days_to_expiry is not None else 9999
            groups_with_priority.append(
                {
                    "matricola": matricola,
                    "costruttore": costruttore,
                    "modello": modello,
                    "range_strumento": range_strumento,
                    "certificates": certificates_sorted,
                    "days_to_expiry": days_to_expiry,
                    "status_dot_icon": status_dot_icon,
                    "priority": priority,
                }
            )

        # Step 4: Ordina i gruppi per priorità (scaduti prima)
        groups_with_priority.sort(key=operator.itemgetter("priority"))

        # Step 5: Crea i nodi padre e figli
        for group in groups_with_priority:
            matricola = group["matricola"]
            costruttore = group["costruttore"]
            modello = group["modello"]
            range_strumento = group["range_strumento"]
            certificates_sorted = group["certificates"]
            days_to_expiry = group["days_to_expiry"]
            status_dot_icon = group["status_dot_icon"]

            # Verifica se è escluso
            is_excluded = matricola in self._exclusions

            # Costruisci label padre con icone separator e info giorni
            # Punto 4: Mostra giorni anche quando compresso
            days_text = self._format_days_text_short(days_to_expiry)

            # Per MANOMETRO DIGITALE, aggiungi il range strumento prima dello stato
            is_manometro_digitale = "MANOMETRO DIGITALE" in modello.upper()
            range_part = f"  •  {range_strumento}" if is_manometro_digitale and range_strumento else ""

            # Aggiungi indicatore [ESCLUSO] se necessario
            excluded_marker = "  [ESCLUSO]" if is_excluded else ""
            parent_label = (
                f"{matricola}  •  {costruttore}  •  {modello}{range_part}  •  {days_text}{excluded_marker}"
            )
            parent_item = SortableTreeWidgetItem(self.tree, [parent_label])
            parent_item.setFirstColumnSpanned(True)

            # Pallino di stato sul padre (visibile anche quando compresso)
            # Se escluso, usa pallino grigio
            if is_excluded:
                parent_item.setIcon(0, QIcon(get_asset_path(Icons.STATUS_DOT_GRAY)))
            else:
                parent_item.setIcon(0, QIcon(get_asset_path(status_dot_icon)))

            # Punto 6: Grassetto solo se espanso (inizialmente no)
            # Salviamo lo stato per gestirlo dinamicamente
            parent_item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                {"days": days_to_expiry, "matricola": matricola},
            )

            # Styling per elementi esclusi
            if is_excluded:
                font = parent_item.font(0)
                font.setStrikeOut(True)
                parent_item.setFont(0, font)
                parent_item.setForeground(0, QBrush(QColor(COLORS["text_light"])))

            # Step 6: Aggiungi i certificati come figli
            for idx, cert in enumerate(certificates_sorted):
                row_item = SortableTreeWidgetItem(
                    parent_item, [str(x) if x is not None else "" for x in cert]
                )

                # LOGICA INTELLIGENTE:
                # - Il PRIMO certificato (idx == 0) è quello "attivo" con stato reale
                # - TUTTI gli altri (idx > 0) sono STORICO senza alert
                is_current = idx == 0

                if is_current:
                    # Certificato corrente: mostra stato reale con pallino
                    self._apply_current_certificate_styling(row_item, cert, days_to_expiry, status_dot_icon)
                else:
                    # Certificato storico: sempre grigio, nessun alert
                    self._apply_historical_certificate_styling(row_item, cert)

        self.tree.setSortingEnabled(False)  # Disabilita sorting per mantenere ordine
        # IMPORTANTE: Comprimi tutto di default (punto 5)
        self.tree.collapseAll()

        self._apply_exclusion_visibility()
        self._update_excluded_count_label()

        # Connetti segnale per gestire grassetto dinamico (solo se non già connesso)
        with suppress(TypeError):
            self.tree.itemExpanded.disconnect(self._on_item_expanded)
            self.tree.itemCollapsed.disconnect(self._on_item_collapsed)
        self.tree.itemExpanded.connect(self._on_item_expanded)
        self.tree.itemCollapsed.connect(self._on_item_collapsed)

    def _calculate_days_and_status(self, scadenza_str):
        """
        Calcola i giorni alla scadenza e ritorna il pallino di stato appropriato.

        Returns:
            tuple: (giorni_alla_scadenza, icona_pallino)
        """
        with suppress(Exception):
            if not scadenza_str:
                return None, Icons.STATUS_DOT_GRAY

            scadenza_date = datetime.strptime(scadenza_str, "%d/%m/%Y").replace(tzinfo=UTC)
            today = datetime.now(UTC)
            delta = scadenza_date - today
            days = delta.days

            # Determina il pallino basato sui giorni
            if days < 0:
                # Scaduto
                return days, Icons.STATUS_DOT_RED
            if 0 <= days <= 15:
                # Scadenza entro 15 giorni
                return days, Icons.STATUS_DOT_ORANGE
            if 16 <= days <= 30:
                # Scadenza tra 16-30 giorni
                return days, Icons.STATUS_DOT_YELLOW
            # Attivo oltre 30 giorni
            return days, Icons.STATUS_DOT_GREEN

        return None, Icons.STATUS_DOT_GRAY

    def _apply_current_certificate_styling(self, item, cert, days_to_expiry, status_dot_icon):
        """Applica styling al certificato CORRENTE (più recente) con stato reale."""
        # Colori e stati basati sui giorni alla scadenza
        if days_to_expiry is None:
            status_text = "N/D"
            bg_color = QColor(COLORS["bg_alt"])
            text_color = QColor(COLORS["text_muted"])
        elif days_to_expiry < 0:
            # ROSSO SCURO per scaduti
            status_text = f"Scaduto da {abs(days_to_expiry)} giorni"
            bg_color = QColor(COLORS["bg_error_pastel"])
            text_color = QColor(COLORS["error_red"])
        elif 0 <= days_to_expiry <= 15:
            # ARANCIONE SCURO per urgenza massima (0-15 giorni)
            status_text = f"Scade tra {days_to_expiry} giorni"
            bg_color = QColor(COLORS["bg_warning_pastel"])
            text_color = QColor(COLORS["warning_orange"])
        elif 16 <= days_to_expiry <= 30:
            # GIALLO CHIARO/BRILLANTE per attenzione (16-30 giorni)
            status_text = f"Scade tra {days_to_expiry} giorni"
            bg_color = QColor(COLORS["bg_attention_pastel"])
            text_color = QColor(COLORS["warning_yellow"])
        else:
            # VERDE per attivi (>30 giorni)
            status_text = f"Attivo ({days_to_expiry} giorni rimanenti)"
            bg_color = QColor(COLORS["bg_success_pastel"])
            text_color = QColor(COLORS["success_dark"])

        # Applica background
        for col in range(self.tree.columnCount()):
            item.setBackground(col, QBrush(bg_color))

        # Applica pallino e testo stato
        item.setIcon(self.IDX_STATO, QIcon(get_asset_path(status_dot_icon)))
        item.setText(self.IDX_STATO, status_text)
        item.setForeground(self.IDX_STATO, QBrush(text_color))

        # Punto 6: Font bold per certificato corrente (più recente)
        font = item.font(self.IDX_STATO)
        font.setBold(True)
        item.setFont(self.IDX_STATO, font)

    def _apply_historical_certificate_styling(self, item, cert):
        """Applica styling ai certificati STORICI (nessun alert)."""
        # Background grigio molto chiaro
        bg_color = QColor(COLORS["bg_alt"])
        for col in range(self.tree.columnCount()):
            item.setBackground(col, QBrush(bg_color))

        # Pallino grigio e testo STORICO
        item.setIcon(self.IDX_STATO, QIcon(get_asset_path(Icons.STATUS_DOT_GRAY)))
        item.setText(self.IDX_STATO, "STORICO")
        item.setForeground(self.IDX_STATO, QBrush(QColor(COLORS["text_light"])))

        # Tooltip informativo
        tooltip = "Certificato storico - Esiste un certificato più recente per questa matricola"
        item.setToolTip(self.IDX_STATO, tooltip)

    def _format_days_text_short(self, days):
        """Formatta il testo dei giorni in versione breve per il nodo padre."""
        if days is None:
            return "N/D"
        if days < 0:
            return f"🔴 Scaduto ({abs(days)}gg fa)"  # Rosso scuro
        if 0 <= days <= 15:
            return f"🟠 Scade tra {days}gg"  # Arancione scuro (urgente)
        if 16 <= days <= 30:
            return f"🟡 Scade tra {days}gg"  # Giallo chiaro (attenzione)
        return f"✅ Attivo ({days}gg rim.)"  # Verde

    def _on_item_expanded(self, item):
        """Gestisce l'evento di espansione: applica grassetto."""
        if item.parent() is None:  # Solo per nodi padre
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)

    def _on_item_collapsed(self, item):
        """Gestisce l'evento di compressione: rimuove grassetto."""
        if item.parent() is None:  # Solo per nodi padre
            font = item.font(0)
            font.setBold(False)
            item.setFont(0, font)

    def filter_data(self, text):
        """Filtra l'albero dei certificati in base al testo di ricerca."""
        query = text.lower()
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if parent is None:
                raise RuntimeError(f"Tree topLevelItem({i}) is None")
            parent_visible = False
            for j in range(parent.childCount()):
                child = parent.child(j)
                if child is None:
                    raise RuntimeError(f"Parent child({j}) is None")
                match = any(query in child.text(c).lower() for c in range(self.tree.columnCount()))
                child.setHidden(not match)
                if match:
                    parent_visible = True
            parent.setHidden(not parent_visible)

    def _show_context_menu(self, pos):
        item = self.tree.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)

        # Determina se è un nodo padre o figlio
        is_parent = item.parent() is None

        if is_parent:
            # Context menu per nodo PADRE (matricola)
            matricola = self._extract_matricola_from_parent(item)
            is_excluded = matricola in self._exclusions

            if is_excluded:
                # Opzione: Includi nel monitoraggio
                include_action = QAction("✅ Includi nel monitoraggio", self)
                include_action.triggered.connect(lambda: self._include_matricola(matricola))
                menu.addAction(include_action)
            else:
                # Opzione: Escludi dal monitoraggio
                exclude_action = QAction("🚫 Escludi dal monitoraggio", self)
                exclude_action.triggered.connect(lambda: self._exclude_matricola(matricola))
                menu.addAction(exclude_action)

            menu.addSeparator()

            # Espandi/Comprimi
            if item.isExpanded():
                collapse_action = QAction("Comprimi", self)
                collapse_action.triggered.connect(lambda: self.tree.collapseItem(item))
                menu.addAction(collapse_action)
            else:
                expand_action = QAction("Espandi", self)
                expand_action.triggered.connect(lambda: self.tree.expandItem(item))
                menu.addAction(expand_action)

        else:
            # Context menu per nodo FIGLIO (certificato)
            # Azione: Apri Certificato
            cert_number = item.text(self.IDX_CERTIFICATO)
            if cert_number:
                open_action = QAction("📄 Apri Certificato", self)
                open_action.triggered.connect(lambda: self._open_certificate(cert_number))
                menu.addAction(open_action)
                menu.addSeparator()

            # Azione: Analizza con Lyra
            lyra_action = QAction("🔍 Analizza con Lyra", self)
            lyra_action.triggered.connect(lambda: self._analyze_item(item))
            menu.addAction(lyra_action)

            menu.addSeparator()

            # Opzione esclusione anche dal figlio (usa la matricola del padre)
            parent_item = item.parent()
            if parent_item:
                matricola = self._extract_matricola_from_parent(parent_item)
                is_excluded = matricola in self._exclusions

                if is_excluded:
                    include_action = QAction("✅ Includi strumento nel monitoraggio", self)
                    include_action.triggered.connect(lambda: self._include_matricola(matricola))
                    menu.addAction(include_action)
                else:
                    exclude_action = QAction("🚫 Escludi strumento dal monitoraggio", self)
                    exclude_action.triggered.connect(lambda: self._exclude_matricola(matricola))
                    menu.addAction(exclude_action)

        if viewport := self.tree.viewport():
            menu.exec(viewport.mapToGlobal(pos))

    def _exclude_matricola(self, matricola: str):
        """Rimuove una matricola dal monitoraggio."""
        self._exclusions.add(matricola)
        self._save_exclusions()
        self._load_data()  # Ricarica per aggiornare lo styling

    def _include_matricola(self, matricola: str):
        """Include una matricola nel monitoraggio (rimuove esclusione)."""
        self._exclusions.discard(matricola)
        self._save_exclusions()
        self._load_data()  # Ricarica per aggiornare lo styling

    def _open_certificate(self, cert_number: str):
        """Apre il file PDF del certificato cercandolo ricorsivamente nella root configurata."""
        cert_root = config_manager.load_config().get("certificati_root_path", "")

        if not cert_root or not Path(cert_root).exists():
            QMessageBox.warning(
                self,
                "Percorso non configurato",
                "Configura il percorso root dei certificati nelle impostazioni.\n"
                "Chiave: certificati_root_path",
            )
            return

        # Cerca il file PDF ricorsivamente
        # Il certificato "016-25" potrebbe essere in "2025/016-25.pdf" o simile
        search_patterns = [
            f"{cert_number}.pdf",
            f"{cert_number}.PDF",
            f"CERTIFICATO {cert_number}.pdf",
            f"certificato {cert_number}.pdf",
        ]

        found_path = None
        for root, _, files in os.walk(cert_root):
            for file in files:
                if any(file.lower() == pattern.lower() for pattern in search_patterns):
                    found_path = os.path.join(root, file)
                    break
                # Match parziale: il file contiene il numero certificato
                if cert_number.lower() in file.lower() and file.lower().endswith(".pdf"):
                    found_path = os.path.join(root, file)
                    break
            if found_path:
                break

        if found_path:
            os.startfile(found_path)  # noqa: S606
        else:
            QMessageBox.warning(
                self,
                "Certificato non trovato",
                f"Impossibile trovare il certificato '{cert_number}' in:\n{cert_root}",
            )

    def _analyze_item(self, item):
        from src.gui.main_window import MainWindow

        mw = self.window()
        if isinstance(mw, MainWindow):
            text = " | ".join([f"{self.HEADERS[c]}: {item.text(c)}" for c in range(self.tree.columnCount())])
            mw.analyze_with_lyra(f"Certificato: {text}")

    def _run_analysis(self):
        """Apre la finestra di analisi scadenze con tutti i certificati monitorati."""
        # Raccogli i dati dai nodi padre del tree (solo quelli NON esclusi)
        certificates_data = []

        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if parent is None:
                raise RuntimeError(f"Tree topLevelItem({i}) is None")
            matricola = self._extract_matricola_from_parent(parent)

            # Salta gli esclusi
            if matricola in self._exclusions:
                continue

            # Estrai i dati dal UserRole
            user_data = parent.data(0, Qt.ItemDataRole.UserRole)
            days = user_data.get("days") if user_data else None

            # Estrai altri dati dal testo del nodo padre
            parts = parent.text(0).split("  •  ")

            costruttore = parts[1].strip() if len(parts) > 1 else "N/D"
            modello = parts[2].strip() if len(parts) > 2 else "N/D"

            # Controlla se c'è il range (per manometri digitali)
            range_strumento = ""
            if "MANOMETRO DIGITALE" in modello.upper() and len(parts) > 4:
                range_strumento = parts[3].strip()

            certificates_data.append(
                {
                    "matricola": matricola,
                    "costruttore": costruttore,
                    "modello": modello,
                    "range": range_strumento,
                    "days": days,
                }
            )

        # Ordina per giorni (scaduti prima)
        certificates_data.sort(key=lambda x: x["days"] if x["days"] is not None else 9999)

        # Apri la finestra di analisi
        dialog = ScadenzeAnalysisDialog(certificates_data, self)
        dialog.exec()
