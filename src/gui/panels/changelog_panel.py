"""
SyncroJob - Changelog Panel (Next-Gen)
Pannello Premium per la visualizzazione dinamica e strutturata delle note di rilascio e novità.
"""

import json
import logging
import platform
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QGuiApplication
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.version import __version__
from src.gui.styles import COLORS, SCROLL_AREA_TRANSPARENT, card_style
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class ReleaseCard(QFrame):
    """
    Card grafica associata ad un singolo rilascio di versione.
    Supporta micro-interazioni di sollevamento 3D/bagliore al passaggio del mouse e copia negli appunti.
    """

    def __init__(
        self,
        release: dict[str, Any],
        is_latest: bool,
        is_next: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        self.release = release
        self.is_latest = is_latest
        self.is_next = is_next
        self.border_color = (
            COLORS["warning_orange"]
            if is_next
            else (COLORS["teal_accent"] if is_latest else COLORS["primary_blue"])
        )
        self.notes_rows: list[tuple[QWidget, str]] = []  # Memorizza tuple (widget_riga, categoria_stile)
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout e gli elementi grafici interni della card."""
        self.setStyleSheet(card_style(self.border_color))

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(12)

        self._setup_header(card_layout)

        # Separatore sottile
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"background-color: {COLORS['border_light']};")
        card_layout.addWidget(separator)

        self._setup_notes(card_layout)

    def _setup_header(self, card_layout: QVBoxLayout) -> None:
        """Configura l'header della card con versione, data e pulsante copia."""
        card_header_layout = QHBoxLayout()
        card_header_layout.setSpacing(10)

        # Badge Versione
        version = self.release.get("version", "N/D")
        version_text = f" Versione v{version} " if not self.is_next else f" In Arrivo v{version} [NEXT] "
        version_badge = QLabel(version_text)
        version_badge.setStyleSheet(f"""
            background-color: {self.border_color};
            color: {COLORS['bg_white']};
            border-radius: 6px;
            font-size: 13px;
            font-weight: 800;
            padding: 4px 8px;
        """)
        card_header_layout.addWidget(version_badge)

        # Data Rilascio
        if not self.is_next:
            date_raw = self.release.get("date", "N/D")
            # Conversione data formato da YYYY-MM-DD a GG/MM/AAAA
            if len(date_raw) == 10 and date_raw[4] == "-" and date_raw[7] == "-":
                parts = date_raw.split("-")
                date = f"{parts[2]}/{parts[1]}/{parts[0]}"
            else:
                date = date_raw
            date_lbl = QLabel(f"Rilasciato il:  {date}")
            date_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px; font-weight: 500;")
            card_header_layout.addWidget(date_lbl)

        card_header_layout.addStretch()

        # Pulsante Copia (Clipboard Integration)
        if not self.is_next:
            self.copy_btn = QPushButton()
            self.copy_btn.setFixedSize(28, 28)
            self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.copy_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: 1px solid {COLORS['border_light']};
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['glass_border']};
                    border-color: {self.border_color};
                }}
            """)
            self.copy_btn.setIcon(get_colored_icon(get_asset_path(Icons.COPY), COLORS["text_secondary"]))
            self.copy_btn.setToolTip("Copia note negli appunti")
            self.copy_btn.clicked.connect(self._copy_to_clipboard)
            card_header_layout.addWidget(self.copy_btn)

        card_layout.addLayout(card_header_layout)

    def _setup_notes(self, card_layout: QVBoxLayout) -> None:
        """Configura l'elenco delle note e le aggiunge al layout."""
        notes_container = QWidget()
        notes_container.setStyleSheet("background: transparent; border: none;")
        notes_layout = QVBoxLayout(notes_container)
        notes_layout.setContentsMargins(5, 5, 5, 5)
        notes_layout.setSpacing(10)

        notes = self.release.get("notes", [])
        for note in notes:
            note_row = QWidget()
            note_row.setStyleSheet("background: transparent; border: none;")
            note_row_layout = QHBoxLayout(note_row)
            note_row_layout.setContentsMargins(0, 0, 0, 0)
            note_row_layout.setSpacing(8)

            category_label, category_style_type = self._parse_note_category(note)
            clean_text = self._clean_note_text(note)

            # Pillola Categoria
            pill = self._create_pill(category_label, category_style_type)
            note_row_layout.addWidget(pill)

            # Testo
            note_text_lbl = QLabel(clean_text)
            note_text_lbl.setWordWrap(True)
            note_text_lbl.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px; line-height: 1.4;")
            note_row_layout.addWidget(note_text_lbl, 1)

            notes_layout.addWidget(note_row)
            self.notes_rows.append((note_row, category_style_type))

        card_layout.addWidget(notes_container)

    def _parse_note_category(self, note: str) -> tuple[str, str]:
        """Esegue il parsing della nota e restituisce l'etichetta e lo stile della categoria."""
        lower_note = note.lower()
        categories = {
            "feat": ("FEATURE", "success"),
            "fix": ("BUGFIX", "danger"),
            "refactor": ("REFACTOR", "purple"),
            "perf": ("PERF", "warning"),
            "docs": ("DOCS", "info"),
            "chore": ("CHORE", "secondary"),
        }
        for prefix, result in categories.items():
            if lower_note.startswith((f"{prefix}:", f"{prefix}(", f"{prefix} ")):
                return result
        return "UPDATE", "info"

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
            "secondary": f"background-color: {COLORS['bg_light']}; color: {COLORS['text_secondary']}; border: 1px solid {COLORS['border_dark']}; border-radius: 4px; font-size: 10px; font-weight: 800;"
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
        QTimer.singleShot(1500, lambda: self.copy_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.COPY), COLORS["text_secondary"])
        ))

    def filter_notes(self, category_filter: str) -> bool:
        """Filtra le note interne e restituisce True se la card contiene almeno una nota visibile."""
        if category_filter == "all":
            for note_widget, _ in self.notes_rows:
                note_widget.show()
            self.show()
            return True

        visible_count = 0
        for note_widget, category in self.notes_rows:
            if category == category_filter:
                note_widget.show()
                visible_count += 1
            else:
                note_widget.hide()

        if visible_count > 0:
            self.show()
            return True

        self.hide()
        return False

    def enterEvent(self, event: Any) -> None:
        """Applica l'effetto 3D di sollevamento e bagliore neon al passaggio del mouse."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(self.border_color))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        super().enterEvent(event)

    def leaveEvent(self, event: Any) -> None:
        """Rimuove l'effetto di sollevamento e bagliore neon all'uscita del mouse."""
        self.setGraphicsEffect(None)  # type: ignore[arg-type]
        super().leaveEvent(event)


class ChangelogPanel(QWidget):
    """
    Pannello Novità & Note di Rilascio.
    Rendering dinamico ed estetico del changelog strutturato con timeline DevOps e filtri sticky.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.release_rows: list[tuple[QWidget, ReleaseCard]] = []
        self.active_filter = "all"
        self._setup_ui()
        self._load_changelog()

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
        layout.addWidget(self.filter_container)

        # Configurazione Stile Tooltip Light Premium
        self.setStyleSheet(f"""
            QToolTip {{
                background-color: {COLORS['bg_white']};
                color: {COLORS['text_dark']};
                border: 1px solid {COLORS['border_light']};
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
        self.scroll_layout.setSpacing(25)

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

        bg_active, text_active = active_styles.get(cat_type, (COLORS["bg_info_pastel"], COLORS["primary_blue"]))

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
                    background-color: {COLORS['bg_white']};
                    color: {COLORS['text_dark']};
                    border: 1px solid {COLORS['border_light']};
                    border-radius: 12px;
                    padding: 4px 14px;
                    font-size: 11px;
                    font-weight: 700;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['bg_light']};
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

    def _apply_filter(self) -> None:
        """Applica il filtro attivo a tutte le card di rilascio."""
        for row_widget, card in self.release_rows:
            has_visible_notes = card.filter_notes(self.active_filter)
            if has_visible_notes:
                row_widget.show()
            else:
                row_widget.hide()

    def _get_git_commit_sha(self) -> str:
        """Recupera lo short commit SHA attuale dal repository Git locale."""
        try:
            from admin.release import ROOT_DIR, find_git_executable
            git_bin = find_git_executable()
            res = subprocess.run(
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
            return sha if sha else "dev"

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
        platform_str = self._get_platform_info()
        sha_str = self._get_git_commit_sha()
        update_str = self._get_last_update_date()

        def add_column(title: str, value: str, icon_path: str, color: str) -> None:
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

        # Aggiungiamo le colonne
        add_column("VERSIONE UTENTE", f"v{version_str}", Icons.CPU, COLORS["teal_accent"])
        add_column("PIATTAFORMA", platform_str, Icons.GLOBE, COLORS["primary_blue"])
        add_column("COMMIT SHA", sha_str, Icons.ACTIVITY, COLORS["teal_accent"])
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
        row_layout.setSpacing(20)

        # 1. Indicatore Timeline (Linea + LED)
        timeline_widget = QWidget()
        timeline_widget.setFixedWidth(40)
        timeline_widget.setStyleSheet("background: transparent; border: none;")
        timeline_layout = QVBoxLayout(timeline_widget)
        timeline_layout.setContentsMargins(0, 0, 0, 0)
        timeline_layout.setSpacing(0)
        timeline_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Linea Superiore
        top_line = QFrame()
        top_line.setFixedWidth(2)
        if is_first:
            top_line.setStyleSheet("background: transparent;")
        else:
            top_line.setStyleSheet(f"background-color: {COLORS['border_light']};")
        timeline_layout.addWidget(top_line, 1)

        # LED circolare
        led = QFrame()
        led.setFixedSize(14, 14)
        led_color = (
            COLORS["warning_orange"]
            if is_next
            else (COLORS["teal_accent"] if is_latest else COLORS["primary_blue"])
        )
        led.setStyleSheet(f"""
            background-color: {led_color};
            border: 2px solid {COLORS['bg_white']};
            border-radius: 7px;
        """)
        timeline_layout.addWidget(led, 0, Qt.AlignmentFlag.AlignCenter)

        # Linea Inferiore
        bottom_line = QFrame()
        bottom_line.setFixedWidth(2)
        if is_last:
            bottom_line.setStyleSheet("background: transparent;")
        else:
            bottom_line.setStyleSheet(f"background-color: {COLORS['border_light']};")
        timeline_layout.addWidget(bottom_line, 1)

        row_layout.addWidget(timeline_widget)

        # 2. Card di rilascio
        card = ReleaseCard(release, is_latest, is_next)
        row_layout.addWidget(card, 1)

        self.scroll_layout.addWidget(row_widget)
        self.release_rows.append((row_widget, card))

    def _load_changelog(self) -> None:
        """Carica il file changelog.json ed esegue il rendering delle card di versione con la timeline."""
        changelog_path = Path(__file__).resolve().parent.parent.parent / "core" / "changelog.json"

        changelog_data = []
        if changelog_path.exists():
            try:
                changelog_data = json.loads(changelog_path.read_text(encoding="utf-8"))
            except Exception:
                logger.exception("Impossibile decodificare il file changelog.json")

        # Fallback se il file è vuoto o non esiste
        if not changelog_data:
            changelog_data = [
                {
                    "version": __version__,
                    "date": "2026-05-20",
                    "notes": ["Release iniziale della versione corrente. Changelog in fase di indicizzazione."]
                }
            ]

        # Svuota i layout per sicurezza
        self._clear_layout(self.diag_outer_layout)
        self._clear_layout(self.scroll_layout)
        self.release_rows.clear()

        # 1. Aggiungiamo la scheda diagnostica premium nel contenitore fisso in cima
        diagnostics = self._create_diagnostics_card()
        self.diag_outer_layout.addWidget(diagnostics)

        # 2. Rendering delle release reali dal file JSON
        total_real = len(changelog_data)

        # Troviamo l'indice della prima release stabile reale (non in arrivo/roadmap)
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

        for i, release in enumerate(changelog_data):
            if isinstance(release, dict):
                is_next = (
                    release.get("is_next", False)
                    or "roadmap" in str(release.get("date", "")).lower()
                    or "arrivo" in str(release.get("date", "")).lower()
                )
                is_latest_real = (i == first_stable_index)
                is_first_real = (i == 0)
                is_last_real = (i == total_real - 1)

                self._add_release_row(
                    release,
                    is_latest=is_latest_real,
                    is_next=is_next,
                    is_first=is_first_real,
                    is_last=is_last_real,
                )

        # Spazio elastico in fondo
        self.scroll_layout.addStretch()
