"""SyncroJob - Changelog Panel (Next-Gen).

Pannello Premium per la visualizzazione dinamica e strutturata delle note di rilascio e novità.
"""

import contextlib
import hashlib
import json
import logging
import platform
import subprocess  # nosec B404
from datetime import datetime
from pathlib import Path
from typing import Any

from PySide6.QtCore import QEasingCurve, QEvent, QPoint, QPropertyAnimation, Qt, QThread, QTimer, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QEnterEvent,
    QGuiApplication,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
)
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.config_manager import set_config_value
from src.core.constants import Icons
from src.core.version import __version__
from src.gui.styles import COLORS, SCROLL_AREA_TRANSPARENT
from src.gui.styles.widget_styles import CARD_STYLE
from src.gui.workers.changelog_worker import ChangelogWorker
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class DiagnosticsWorker(QThread):
    """Worker in background per caricare lo SHA di Git e i dati hardware in modo asincrono."""

    finished = Signal(str, str)  # Invia (sha, platform)

    def run(self) -> None:
        """Esegue il recupero dei dati diagnostici in background."""
        # 1. Recupero Git Commit SHA
        sha = "dev"
        try:
            from admin.release import ROOT_DIR, find_git_executable

            git_bin = find_git_executable()
            res = subprocess.run(  # nosec B603
                [git_bin, "rev-parse", "--short", "HEAD"],
                cwd=ROOT_DIR,
                capture_output=True,
                text=True,
                check=False,
            )
            sha_stripped = res.stdout.strip()
            if sha_stripped:
                sha = sha_stripped
        except Exception:
            logger.debug("Impossibile caricare lo SHA di Git")

        # 2. Platform info
        plat = "Windows (x64)"
        try:
            os_name = platform.system()
            arch = platform.machine()
            plat = f"{os_name} ({arch})"
        except Exception:
            logger.debug("Impossibile ottenere informazioni di piattaforma")

        self.finished.emit(sha, plat)


class TimelineNode(QWidget):
    """Nodo della timeline verticale per le card dei rilasci."""

    def __init__(
        self,
        color: str,
        is_latest: bool,
        is_first: bool = False,
        is_last: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setFixedWidth(40)
        self.color = QColor(color)
        self.is_latest = is_latest
        self.is_first = is_first
        self.is_last = is_last
        self.is_hovered = False

    def set_hovered(self, state: bool) -> None:
        """Imposta lo stato di hover."""
        self.is_hovered = state
        self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna il nodo e la timeline."""
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            w = self.width()
            h = self.height()
            cx = w / 2.0

            # Disegno del nodo (allineato all'header della card calcolando il padding esterno)
            node_y = 44

            # Linea verticale (Timeline)
            pen_line = QPen(QColor(COLORS["border_light"]), 2)
            painter.setPen(pen_line)
            start_y = 0 if not self.is_first else node_y
            end_y = h if not self.is_last else node_y
            painter.drawLine(int(cx), start_y, int(cx), end_y)

            if self.is_latest or self.is_hovered:
                glow_radius = 12 if self.is_hovered else 8
                glow_color = QColor(self.color)
                glow_color.setAlpha(100 if self.is_hovered else 60)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(glow_color))
                painter.drawEllipse(QPoint(int(cx), node_y), glow_radius, glow_radius)

            node_radius = 5 if (self.is_latest or self.is_hovered) else 4
            painter.setPen(QPen(self.color, 2))
            painter.setBrush(QBrush(QColor(COLORS["bg_white"])))
            painter.drawEllipse(QPoint(int(cx), node_y), node_radius, node_radius)
        finally:
            painter.end()


class ReleaseCard(QWidget):
    """Card grafica associata ad un singolo rilascio di versione.

    Supporta layout a timeline, micro-interazioni, e statistiche dinamiche.
    """

    def __init__(  # noqa: PLR0913
        self,
        release: dict[str, Any],
        is_latest: bool,
        is_next: bool = False,
        is_first: bool = False,
        is_last: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.release = release
        self.is_latest = is_latest
        self.is_next = is_next
        self.is_first = is_first
        self.is_last = is_last
        self.border_color = (
            COLORS["warning_orange"]
            if is_next
            else (COLORS["teal_accent"] if is_latest else COLORS["primary_blue"])
        )
        self.notes_rows: list[tuple[QWidget, str]] = []
        self._anim: QPropertyAnimation | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Timeline Node
        self.timeline_node = TimelineNode(self.border_color, self.is_latest, self.is_first, self.is_last)
        main_layout.addWidget(self.timeline_node)

        # 2. Card Content Wrapper per spaziatura
        card_wrapper = QWidget()
        wrapper_layout = QVBoxLayout(card_wrapper)
        wrapper_layout.setContentsMargins(15, 12, 0, 12)

        self.card_frame = QFrame()
        self.card_frame.setStyleSheet(CARD_STYLE)

        # Effetto Glassmorphism/Hover iniziale
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QColor(0, 0, 0, 20))
        self.shadow.setOffset(0, 4)
        self.card_frame.setGraphicsEffect(self.shadow)

        card_layout = QVBoxLayout(self.card_frame)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(12)

        self._setup_header(card_layout)

        self.separator = QFrame()
        self.separator.setFixedHeight(1)
        self.separator.setStyleSheet(f"background-color: {COLORS['border_light']};")
        card_layout.addWidget(self.separator)

        self._setup_notes(card_layout)

        wrapper_layout.addWidget(self.card_frame)
        main_layout.addWidget(card_wrapper)

        self.is_expanded = False
        self.notes_container.setMaximumHeight(0)
        self.notes_container.hide()
        self.separator.hide()

    def _count_stats(self) -> dict[str, int]:
        stats = {"NEW": 0, "FIX": 0, "UPDATE": 0}
        for note_data in self.release.get("notes", []):
            note = note_data.get("message", "").lower() if isinstance(note_data, dict) else note_data.lower()

            if note.startswith("feat"):
                stats["NEW"] += 1
            elif note.startswith("fix"):
                stats["FIX"] += 1
            else:
                stats["UPDATE"] += 1
        return stats

    def _setup_header(self, card_layout: QVBoxLayout) -> None:
        card_header_layout = QHBoxLayout()
        card_header_layout.setSpacing(10)
        # Badge Versione - Rimossa la stroke per un look più moderno e flat
        version = self.release.get("version", "N/D")
        version_text = f"  v{version}  " if not self.is_next else f"  In Arrivo v{version} [NEXT]  "
        version_badge = QLabel(version_text)

        if self.is_latest or self.is_next:
            bg_css = f"background-color: {self.border_color}; color: {COLORS['bg_white']}; border: none;"
        else:
            bg_css = f"background-color: {COLORS['bg_white']}; color: {self.border_color}; border: none; font-size: 15px;"

        version_badge.setStyleSheet(f"""
            {bg_css}
            border-radius: 6px;
            font-size: 14px;
            font-weight: 900;
            padding: 4px 6px;
        """)
        card_header_layout.addWidget(version_badge)

        # Smart Header: Statistiche
        stats = self._count_stats()
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(6)

        if stats["NEW"] > 0:
            lbl = QLabel(f"🚀 {stats['NEW']} Feature")
            lbl.setStyleSheet(
                f"color: {COLORS['success_dark']}; font-size: 11px; font-weight: 800; background: {COLORS['bg_success_pastel']}; padding: 4px 8px; border-radius: 6px;"
            )
            stats_layout.addWidget(lbl)
        if stats["FIX"] > 0:
            lbl = QLabel(f"🐛 {stats['FIX']} Fix")
            lbl.setStyleSheet(
                f"color: {COLORS['error_red']}; font-size: 11px; font-weight: 800; background: {COLORS['bg_error_pastel']}; padding: 4px 8px; border-radius: 6px;"
            )
            stats_layout.addWidget(lbl)
        if stats["UPDATE"] > 0:
            lbl = QLabel(f"🔄 {stats['UPDATE']} Update")
            lbl.setStyleSheet(
                f"color: {COLORS['primary_blue']}; font-size: 11px; font-weight: 800; background: {COLORS['bg_info_pastel']}; padding: 4px 8px; border-radius: 6px;"
            )
            stats_layout.addWidget(lbl)

        card_header_layout.addLayout(stats_layout)

        card_header_layout.addStretch()

        # Data Rilascio spostata a destra
        if not self.is_next:
            date_raw = self.release.get("date", "N/D")
            if len(date_raw) == 10 and date_raw[4] == "-" and date_raw[7] == "-":
                parts = date_raw.split("-")
                date = f"{parts[2]}/{parts[1]}/{parts[0]}"
            else:
                date = date_raw
            date_lbl = QLabel(f"{date}")
            date_lbl.setStyleSheet(
                f"color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 600; letter-spacing: 1px;"
            )
            card_header_layout.addWidget(date_lbl)

        # Pulsante Copia
        if not self.is_next:
            self.copy_btn = QPushButton()
            self.copy_btn.setFixedSize(28, 28)
            self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.copy_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: 1px solid {COLORS["border_light"]};
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS["glass_border"]};
                    border-color: {self.border_color};
                }}
            """)
            self.copy_btn.setIcon(get_colored_icon(get_asset_path(Icons.COPY), COLORS["text_secondary"]))
            self.copy_btn.setToolTip("Copia note negli appunti")
            self.copy_btn.clicked.connect(self._copy_to_clipboard)
            card_header_layout.addWidget(self.copy_btn)

        card_layout.addLayout(card_header_layout)

    def _setup_notes(self, card_layout: QVBoxLayout) -> None:
        self.notes_container = QWidget()
        self.notes_container.setStyleSheet("background: transparent; border: none;")
        notes_layout = QVBoxLayout(self.notes_container)
        notes_layout.setContentsMargins(5, 5, 5, 5)
        notes_layout.setSpacing(12)

        notes = self.release.get("notes", [])
        for note_data in notes:
            if isinstance(note_data, dict):
                note = note_data.get("message", "")
                sha = note_data.get("sha", "")
                if not sha:
                    sha = hashlib.sha256(note.encode("utf-8")).hexdigest()[:7]
            else:
                note = note_data
                sha = hashlib.sha256(note.encode("utf-8")).hexdigest()[:7]

            note_row = QWidget()
            note_row.setStyleSheet("background: transparent; border: none;")
            note_row_layout = QHBoxLayout(note_row)
            note_row_layout.setContentsMargins(0, 0, 0, 0)
            note_row_layout.setSpacing(10)

            category_label, category_style_type = self._parse_note_category(note)
            clean_text = self._clean_note_text(note)

            # Design del Commit SHA migliorato
            sha_lbl = QLabel(f" 🔀 {sha} ")
            sha_lbl.setStyleSheet(f"""
                color: {COLORS["text_secondary"]};
                background-color: {COLORS["bg_light"]};
                font-family: Consolas, monospace;
                font-size: 11px;
                font-weight: bold;
                padding: 3px 6px;
                border-radius: 10px;
                border: 1px solid {COLORS["border_light"]};
            """)
            sha_lbl.setFixedHeight(22)
            note_row_layout.addWidget(sha_lbl)

            # Pillola Categoria
            pill = self._create_pill(category_label, category_style_type)
            note_row_layout.addWidget(pill)

            # Testo
            note_text_lbl = QLabel(clean_text)
            note_text_lbl.setWordWrap(True)
            note_text_lbl.setStyleSheet(
                f"color: {COLORS['text_dark']}; font-size: 13px; line-height: 1.5; font-weight: 500;"
            )
            note_row_layout.addWidget(note_text_lbl, 1)

            notes_layout.addWidget(note_row)
            self.notes_rows.append((note_row, category_style_type))

        card_layout.addWidget(self.notes_container)

    def enterEvent(self, event: QEnterEvent) -> None:
        """Gestisce l'evento di entrata del mouse."""
        self.timeline_node.set_hovered(True)
        self.shadow.setBlurRadius(20)
        self.shadow.setOffset(0, 6)
        self.shadow.setColor(QColor(self.border_color).darker(150))
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """Gestisce l'evento di uscita del mouse."""
        self.timeline_node.set_hovered(False)
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(0, 4)
        self.shadow.setColor(QColor(0, 0, 0, 20))
        self.card_frame.setStyleSheet(CARD_STYLE)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Gestisce il click del mouse per espandere."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._toggle_expansion()
        super().mousePressEvent(event)

    def _toggle_expansion(self) -> None:
        self.is_expanded = not self.is_expanded

        if self._anim:
            self._anim.stop()

        self._anim = QPropertyAnimation(self.notes_container, b"maximumHeight")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        if self.is_expanded:
            self.notes_container.show()
            self.separator.show()
            # Calcola l'altezza necessaria
            self.notes_container.adjustSize()
            target_h = self.notes_container.sizeHint().height()

            self._anim.setStartValue(0)
            self._anim.setEndValue(target_h + 20)  # Un po' di margine
        else:
            current_h = self.notes_container.height()
            self._anim.setStartValue(current_h)
            self._anim.setEndValue(0)
            self._anim.finished.connect(self._on_collapse_finished)
            self.separator.hide()

        self._anim.start()

    def _on_collapse_finished(self) -> None:
        if not self.is_expanded:
            self.notes_container.hide()
            with contextlib.suppress(Exception):
                if self._anim:
                    self._anim.finished.disconnect(self._on_collapse_finished)

    def _parse_note_category(self, note: str) -> tuple[str, str]:
        """Esegue il parsing della nota e restituisce l'etichetta e lo stile della categoria."""
        lower_note = note.lower()
        categories = {
            "feat": ("🚀 FEATURE", "success"),
            "fix": ("🐛 BUGFIX", "danger"),
            "refactor": ("♻️ REFACTOR", "purple"),
            "perf": ("⚡ PERF", "warning"),
            "docs": ("📝 DOCS", "info"),
            "chore": ("🔧 CHORE", "secondary"),
        }
        for prefix, result in categories.items():
            if lower_note.startswith((f"{prefix}:", f"{prefix}(", f"{prefix} ")):
                return result
        return "✨ UPDATE", "info"

    def _clean_note_text(self, note: str) -> str:
        """Rimuove i prefissi convenzionali a scopo di visualizzazione UI."""
        if ":" in note:
            parts = note.split(":", 1)
            if len(parts[0]) < 15:
                return parts[1].strip()
        return note

    def _create_pill(self, text: str, style_type: str) -> QLabel:
        """Crea un'etichetta pillola colorata associata alla categoria."""
        pill = QLabel(f" {text} ")
        pill.setContentsMargins(6, 2, 6, 2)
        pill.setFixedHeight(20)
        pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
        styles = {
            "success": f"background-color: {COLORS['bg_success_pastel']}; color: {COLORS['success_dark']}; border: 1px solid {COLORS['success_green']}; border-radius: 4px; font-size: 10px; font-weight: 800;",
            "danger": f"background-color: {COLORS['bg_error_pastel']}; color: {COLORS['error_red']}; border: 1px solid {COLORS['error_red']}; border-radius: 4px; font-size: 10px; font-weight: 800;",
            "purple": f"background-color: {COLORS['bg_info_pastel']}; color: {COLORS['purple']}; border: 1px solid {COLORS['purple']}; border-radius: 4px; font-size: 10px; font-weight: 800;",
            "warning": f"background-color: {COLORS['bg_warning_pastel']}; color: {COLORS['warning_orange']}; border: 1px solid {COLORS['warning_light']}; border-radius: 4px; font-size: 10px; font-weight: 800;",
            "info": f"background-color: {COLORS['bg_info_pastel']}; color: {COLORS['info_blue']}; border: 1px solid {COLORS['info_blue']}; border-radius: 4px; font-size: 10px; font-weight: 800;",
            "secondary": f"background-color: {COLORS['bg_light']}; color: {COLORS['text_secondary']}; border: 1px solid {COLORS['border_dark']}; border-radius: 4px; font-size: 10px; font-weight: 800;",
        }
        pill.setStyleSheet(styles.get(style_type, styles["info"]))
        return pill

    def _copy_to_clipboard(self) -> None:
        """Copia le note di rilascio in formato Markdown negli appunti."""
        version = self.release.get("version", "N/D")
        date = self.release.get("date", "N/D")
        notes = self.release.get("notes", [])

        md_text = f"## SyncroJob v{version} ({date})\n"
        for note in notes:
            md_text += f"- {note}\n"

        QGuiApplication.clipboard().setText(md_text)

        # Feedback visivo sul bottone
        self.copy_btn.setIcon(get_colored_icon(get_asset_path(Icons.ACTIVITY), COLORS["success_green"]))
        QTimer.singleShot(
            1500,
            lambda: self.copy_btn.setIcon(
                get_colored_icon(get_asset_path(Icons.COPY), COLORS["text_secondary"])
            ),
        )

    def filter_notes(self, category_filter: str, search_text: str = "") -> bool:
        """Filtra le note interne e restituisce True se la card contiene almeno una nota visibile.

        Args:
          category_filter: Categoria per filtrare le note.
          search_text: Testo per la ricerca nelle note.

        Returns:
          bool: True se la card è visibile dopo il filtro.
        """
        visible_count = 0
        for note_widget, category in self.notes_rows:
            # Estrarre il testo della nota dall'etichetta del testo
            note_layout = note_widget.layout()
            note_text = ""
            if note_layout and note_layout.count() >= 2:
                item = note_layout.itemAt(1)
                if item is not None:
                    text_widget = item.widget()
                    if isinstance(text_widget, QLabel):
                        note_text = text_widget.text().lower()

            category_match = category_filter in ("all", category)
            text_match = not search_text or search_text in note_text

            if category_match and text_match:
                note_widget.show()
                visible_count += 1
            else:
                note_widget.hide()

        if visible_count > 0:
            self.show()
            return True

        self.hide()
        return False


class ChangelogPanel(QWidget):
    """Pannello Novità & Note di Rilascio.

    Rendering dinamico ed estetico del changelog strutturato con timeline DevOps e filtri sticky.

    Inizializza la classe.
    """

    _changelog_cache: list[dict[str, Any]] | None = None

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.release_rows: list[tuple[QWidget, ReleaseCard]] = []
        self.active_filter = "all"
        self.search_text = ""
        self.search_bar: QLineEdit | None = None
        self.sha_lbl: QLabel | None = None
        self.platform_lbl: QLabel | None = None
        self._setup_ui()
        self._load_changelog()

        # Avvio Diagnostics Worker in Background
        self.worker = DiagnosticsWorker(self)
        self.worker.finished.connect(self._on_diagnostics_loaded)
        self.worker.start()

    def _on_diagnostics_loaded(self, sha: str, plat: str) -> None:
        """Aggiorna le label diagnostiche una volta caricati i dati in background."""
        if self.sha_lbl:
            self.sha_lbl.setText(sha)
        if self.platform_lbl:
            self.platform_lbl.setText(plat)

    def _setup_search_bar(self, layout: QHBoxLayout) -> None:
        """Configura la barra di ricerca premium e la aggiunge al layout dei filtri."""
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cerca nelle note...")
        self.search_bar.setFixedWidth(200)
        self.search_bar.setFixedHeight(24)
        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS["bg_white"]};
                color: {COLORS["text_dark"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 12px;
                padding: 2px 10px 2px 26px;
                font-size: 11px;
                font-weight: 600;
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS["primary_blue"]};
            }}
        """)

        # Icona lente di ingrandimento
        search_icon = QLabel(self.search_bar)
        search_icon.setPixmap(
            get_colored_icon(get_asset_path(Icons.SEARCH), COLORS["text_secondary"]).pixmap(12, 12)
        )
        search_icon.setStyleSheet("background: transparent; border: none;")
        search_icon.setGeometry(8, 6, 12, 12)

        self.search_bar.textChanged.connect(self._on_search_changed)
        layout.addWidget(self.search_bar)

    def _setup_ui(self) -> None:
        """Configura il layout del portale Changelog con area diagnostica e scorrimento."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Contenitore Diagnostica Fisso (Sticky)
        self.diagnostics_container = QWidget()
        self.diagnostics_container.setStyleSheet("background: transparent; border: none;")
        self.diag_outer_layout = QVBoxLayout(self.diagnostics_container)
        self.diag_outer_layout.setContentsMargins(40, 30, 40, 10)
        layout.addWidget(self.diagnostics_container)

        # 2. Contenitore Barra dei Filtri Fisso (Sticky)
        self.filter_container = QWidget()
        self.filter_container.setStyleSheet("background: transparent; border: none;")
        filter_outer_layout = QHBoxLayout(self.filter_container)
        filter_outer_layout.setContentsMargins(40, 5, 40, 15)
        filter_outer_layout.setSpacing(10)

        # Label "Filtra per:"
        filter_lbl = QLabel("Filtra per:")
        filter_lbl.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 11px; font-weight: 800; "
            "text-transform: uppercase; letter-spacing: 0.5px;"
        )
        filter_outer_layout.addWidget(filter_lbl)

        # Pulsanti Filtro Pillola
        self.filter_buttons: dict[str, QPushButton] = {}
        filters = [
            ("Tutte", "all"),
            ("Nuove Feature", "success"),
            ("Bugfix", "danger"),
            ("Refactor", "purple"),
            ("Prestazioni", "warning"),
        ]

        for label, cat_type in filters:
            btn = QPushButton(label)
            btn.setCheckable(True)
            if cat_type == "all":
                btn.setChecked(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            self._style_filter_button(btn, cat_type, btn.isChecked())
            btn.clicked.connect(lambda _, c=cat_type, b=btn: self._on_filter_changed(c, b))
            filter_outer_layout.addWidget(btn)
            self.filter_buttons[cat_type] = btn

        filter_outer_layout.addStretch()
        self._setup_search_bar(filter_outer_layout)
        layout.addWidget(self.filter_container)

        # Configurazione Stile Tooltip Light Premium
        self.setStyleSheet(f"""
            QToolTip {{
                background-color: {COLORS["bg_white"]};
                color: {COLORS["text_dark"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)

        # 3. Area di scorrimento trasparente per le Card di rilascio
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(SCROLL_AREA_TRANSPARENT)

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(40, 15, 40, 30)
        self.scroll_layout.setSpacing(0)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

    def _style_filter_button(self, btn: QPushButton, cat_type: str, active: bool) -> None:
        """Applica lo stile pillola premium chiaro al pulsante di filtro in base allo stato."""
        active_styles = {
            "all": (COLORS["bg_info_pastel"], COLORS["primary_blue"]),
            "success": (COLORS["bg_success_pastel"], COLORS["success_dark"]),
            "danger": (COLORS["bg_error_pastel"], COLORS["error_red"]),
            "purple": ("#f5f3ff", COLORS["purple"]),
            "warning": (COLORS["bg_warning_pastel"], COLORS["warning_orange"]),
        }

        bg_active, text_active = active_styles.get(
            cat_type, (COLORS["bg_info_pastel"], COLORS["primary_blue"])
        )

        if active:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_active};
                    color: {text_active};
                    border: 1px solid {text_active};
                    border-radius: 12px;
                    padding: 4px 14px;
                    font-size: 11px;
                    font-weight: 800;
                }}
            """)

        else:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS["bg_white"]};
                    color: {COLORS["text_dark"]};
                    border: 1px solid {COLORS["border_light"]};
                    border-radius: 12px;
                    padding: 4px 14px;
                    font-size: 11px;
                    font-weight: 700;
                }}
                QPushButton:hover {{
                    background-color: {COLORS["bg_light"]};
                    border-color: {text_active};
                    color: {text_active};
                }}
            """)

    def _on_filter_changed(self, category: str, clicked_btn: QPushButton) -> None:
        """Gestisce il cambio di filtro per categoria e aggiorna lo stile delle pillole."""
        self.active_filter = category

        for cat_type, btn in self.filter_buttons.items():
            if btn != clicked_btn:
                btn.setChecked(False)
            self._style_filter_button(btn, cat_type, btn.isChecked())

        self._apply_filter()

    def _on_search_changed(self, text: str) -> None:
        """Gestisce il cambio del testo di ricerca in tempo reale."""
        self.search_text = text.lower().strip()
        self._apply_filter()

    def _apply_filter(self) -> None:
        """Applica il filtro attivo e di ricerca a tutte le card di rilascio."""
        for row_widget, card in self.release_rows:
            has_visible_notes = card.filter_notes(self.active_filter, self.search_text)
            if has_visible_notes:
                row_widget.show()
            else:
                row_widget.hide()

    def _get_git_commit_sha(self) -> str:
        """Recupera lo short commit SHA attuale dal repository Git locale."""
        try:
            from admin.release import ROOT_DIR, find_git_executable

            git_bin = find_git_executable()
            res = subprocess.run(  # nosec B603
                [git_bin, "rev-parse", "--short", "HEAD"],
                cwd=ROOT_DIR,
                capture_output=True,
                text=True,
                check=False,
            )
            sha = res.stdout.strip()
        except Exception:
            return "dev"
        else:
            return sha or "dev"

    def _get_platform_info(self) -> str:
        """Restituisce informazioni sulla piattaforma hardware/OS."""
        try:
            os_name = platform.system()
            arch = platform.machine()
        except Exception:
            return "Windows (x64)"
        else:
            return f"{os_name} ({arch})"

    def _format_date(self, date_str: str) -> str:
        """Converte una data da YYYY-MM-DD a GG/MM/AAAA."""
        if len(date_str) == 10 and date_str[4] == "-" and date_str[7] == "-":
            parts = date_str.split("-")
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
        return date_str

    def _get_last_update_date(self) -> str:
        """Restituisce la data dell'ultimo aggiornamento disponibile in formato GG/MM/AAAA."""
        import contextlib

        changelog_path = Path(__file__).resolve().parent.parent.parent / "core" / "changelog.json"

        if changelog_path.exists():
            with contextlib.suppress(Exception):
                changelog_data = json.loads(changelog_path.read_text(encoding="utf-8"))
                if changelog_data and isinstance(changelog_data, list):
                    first_entry = changelog_data[0]
                    if isinstance(first_entry, dict) and "date" in first_entry:
                        return self._format_date(str(first_entry["date"]))

        return datetime.now().strftime("%d/%m/%Y")

    def _create_diagnostics_card(self) -> QFrame:
        """Crea una scheda diagnostica premium orizzontale in stile Enterprise."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS["glass_dark"]};
                border: 1px solid {COLORS["glass_border"]};
                border-radius: 14px;
            }}
        """)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(30)

        # Dati diagnostici
        version_str = __version__
        update_str = self._get_last_update_date()

        def add_column(title: str, value: str, icon_path: str, color: str) -> QLabel:
            col_widget = QWidget()
            col_widget.setStyleSheet("background: transparent; border: none;")
            col_layout = QVBoxLayout(col_widget)
            col_layout.setContentsMargins(0, 0, 0, 0)
            col_layout.setSpacing(4)

            title_lbl = QLabel(title)
            title_lbl.setStyleSheet(
                f"color: {COLORS['text_secondary']}; font-size: 10px; font-weight: 800; "
                "text-transform: uppercase; letter-spacing: 0.5px;"
            )

            val_container = QWidget()
            val_container.setStyleSheet("background: transparent; border: none;")
            val_layout = QHBoxLayout(val_container)
            val_layout.setContentsMargins(0, 0, 0, 0)
            val_layout.setSpacing(6)

            icon_lbl = QLabel()
            icon_lbl.setPixmap(get_colored_icon(get_asset_path(icon_path), color).pixmap(14, 14))
            val_layout.addWidget(icon_lbl)

            val_lbl = QLabel(value)
            val_lbl.setStyleSheet(f"color: {COLORS['bg_white']}; font-size: 13px; font-weight: 700;")
            val_layout.addWidget(val_lbl)
            val_layout.addStretch()

            col_layout.addWidget(title_lbl)
            col_layout.addWidget(val_container)
            layout.addWidget(col_widget, 1)
            return val_lbl

        # Aggiungiamo le colonne
        add_column("VERSIONE UTENTE", f"v{version_str}", Icons.CPU, COLORS["teal_accent"])
        self.platform_lbl = add_column("PIATTAFORMA", "Caricamento...", Icons.GLOBE, COLORS["primary_blue"])
        self.sha_lbl = add_column("COMMIT SHA", "Caricamento...", Icons.ACTIVITY, COLORS["teal_accent"])
        add_column("AGGIORNATO IL", update_str, Icons.CALENDAR, COLORS["teal_accent"])

        return card

    def _clear_layout(self, layout: QVBoxLayout) -> None:
        """Svuota ricorsivamente tutti i widget da un layout Qt."""
        while layout.count():
            child = layout.takeAt(0)
            if child is not None:
                widget = child.widget()
                if widget is not None:
                    widget.deleteLater()

    def _add_release_row(
        self,
        release: dict[str, Any],
        is_latest: bool,
        is_next: bool,
        is_first: bool,
        is_last: bool,
    ) -> None:
        """Crea e aggiunge una riga di rilascio contenente l'indicatore timeline a sinistra e la card a destra."""
        row_widget = QWidget()
        row_widget.setStyleSheet("background: transparent; border: none;")
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(0)

        # 2. Card di rilascio (Contiene già il nodo della timeline integrato)
        card = ReleaseCard(release, is_latest, is_next, is_first, is_last)
        row_layout.addWidget(card)

        self.scroll_layout.addWidget(row_widget)
        self.release_rows.append((row_widget, card))

    def _read_changelog_from_disk(self) -> list[dict[str, Any]]:
        """Legge il file changelog.json da disco e applica un fallback in caso di errori."""
        changelog_path = Path(__file__).resolve().parent.parent.parent / "core" / "changelog.json"
        changelog_data: list[dict[str, Any]] = []
        if changelog_path.exists():
            try:
                data = json.loads(changelog_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    changelog_data = data
            except Exception:
                logger.exception("Impossibile decodificare il file changelog.json")

        # Fallback se il file è vuoto o non esiste
        if not changelog_data:
            changelog_data = [
                {
                    "version": __version__,
                    "date": "2026-05-20",
                    "notes": [
                        "Release iniziale della versione corrente. Changelog in fase di indicizzazione."
                    ],
                }
            ]
        return changelog_data

    def _load_changelog(self) -> None:
        """Avvia il caricamento asincrono del changelog."""
        if ChangelogPanel._changelog_cache is not None:
            self._on_changelog_ready(ChangelogPanel._changelog_cache)
            return

        self._changelog_worker = ChangelogWorker()
        self._changelog_worker.finished_signal.connect(self._on_changelog_ready)
        self._changelog_worker.start()

    def _on_changelog_ready(self, changelog_data: list[dict[str, Any]]) -> None:
        """Popola la UI con i dati del changelog caricati asincronamente."""
        ChangelogPanel._changelog_cache = changelog_data

        # Svuota i layout per sicurezza
        self._clear_layout(self.diag_outer_layout)
        self._clear_layout(self.scroll_layout)
        self.release_rows.clear()

        # 1. Aggiungiamo la scheda diagnostica premium nel contenitore fisso in cima
        diagnostics = self._create_diagnostics_card()
        self.diag_outer_layout.addWidget(diagnostics)

        # 2. Rendering delle release reali
        total_real = len(changelog_data)

        # Troviamo l'indice della prima release stabile reale
        first_stable_index = -1
        for idx, release in enumerate(changelog_data):
            if isinstance(release, dict):
                is_next = (
                    release.get("is_next", False)
                    or "roadmap" in str(release.get("date", "")).lower()
                    or "arrivo" in str(release.get("date", "")).lower()
                )
                if not is_next:
                    first_stable_index = idx
                    break

        # Impostiamo la versione corrente vista (Asincrono per non bloccare con fsync)
        if first_stable_index != -1 and first_stable_index < total_real:
            latest_version = changelog_data[first_stable_index].get("version")
            if latest_version:
                # Differiamo il salvataggio per massimizzare la fluidità immediata
                QTimer.singleShot(
                    1000, lambda v=latest_version: set_config_value("changelog_last_viewed_version", str(v))
                )

        for i, release in enumerate(changelog_data):
            if isinstance(release, dict):
                is_next = (
                    release.get("is_next", False)
                    or "roadmap" in str(release.get("date", "")).lower()
                    or "arrivo" in str(release.get("date", "")).lower()
                )
                is_latest_real = i == first_stable_index
                is_first_real = i == 0
                is_last_real = i == total_real - 1

                self._add_release_row(
                    release,
                    is_latest=is_latest_real,
                    is_next=is_next,
                    is_first=is_first_real,
                    is_last=is_last_real,
                )

        self.scroll_layout.addStretch()
