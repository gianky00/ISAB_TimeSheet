"""
SyncroJob - Pannello Dipendenti
Visualizzazione e gestione dell'anagrafica dipendenti.
"""

import csv
import logging
from contextlib import suppress
from datetime import datetime

from PyQt6.QtCore import (
    QSize,
    Qt,
    QTimer,
    pyqtSignal,
)
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.database import db_manager
from src.gui.formatters import FastTableModel
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class ColoredDotDelegate(QStyledItemDelegate):
    """Delegate personalizzato per colorare i pallini nella colonna SCAD. ISAB."""

    def paint(self, painter, option, index):
        """Disegna il pallino colorato con il numero di giorni."""
        if index.column() != 0:  # Solo per la prima colonna
            super().paint(painter, option, index)
            return

        value = index.data(Qt.ItemDataRole.DisplayRole)
        if not value:
            super().paint(painter, option, index)
            return

        # Configura il painter
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Sfondo alternato se necessario
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        elif index.row() % 2 == 1:
            painter.fillRect(option.rect, QColor("#f8f9fa"))

        try:
            # Estrai il valore numerico
            parts = str(value).split()
            if len(parts) >= 2:
                days = int(parts[1])

                # Determina il colore
                if days >= 10:
                    color = QColor("#198754")  # Verde
                elif days >= 0:
                    color = QColor("#fd7e14")  # Arancione
                else:
                    color = QColor("#dc3545")  # Rosso
                    days = 0

                # Disegna il pallino
                center_x = option.rect.center().x() - 15
                center_y = option.rect.center().y()
                painter.setBrush(color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(center_x, center_y - 5, 10, 10)

                # Disegna il numero
                painter.setPen(QColor("#333333"))
                font = QFont()
                font.setPointSize(10)
                font.setBold(True)
                painter.setFont(font)
                text_rect = option.rect.adjusted(10, 0, 0, 0)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(days))
        except Exception as e:
            logger.error(f"Errore rendering pallino: {e}")
            super().paint(painter, option, index)

        painter.restore()


class InteractiveStatusCard(QFrame):
    """Card moderna con animazioni e ombreggiature."""

    clicked = pyqtSignal(str)  # Emette il tipo di filtro ("ok", "warning", "expired")

    def __init__(self, label, color, icon_path, description, filter_type, parent=None):
        super().__init__(parent)
        self.base_color = color
        self.filter_type = filter_type
        self.description = description
        # Nuovo Layout: Largo e Basso
        self.setFixedSize(240, 75)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Tooltip informativo
        tooltip = f"<b>{label}</b><br/>{description} nello stabilimento ISAB<br/><i>Clicca per filtrare</i>"
        self.setToolTip(tooltip)

        # Effetto Ombra
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(self.shadow)

        self.setStyleSheet(
            f"""
            InteractiveStatusCard {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 8px;
            }}
            """
        )

        # Layout Orizzontale Compatto
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Sinistra: Icona/Colore + Numero
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.val_text = QLabel("0")
        self.val_text.setStyleSheet(
            f"font-size: 28px; font-weight: 900; color: {color};"
        )
        self.val_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.val_text)

        layout.addLayout(left_layout)

        # Separatore leggero
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #eee;")
        layout.addWidget(line)

        # Destra: Titolo + Descrizione
        right_layout = QVBoxLayout()
        right_layout.setSpacing(2)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_title = QLabel(label.upper())
        lbl_title.setStyleSheet(
            "font-size: 11px; font-weight: 800; color: #555; letter-spacing: 0.5px;"
        )

        lbl_desc = QLabel(description)
        lbl_desc.setStyleSheet("font-size: 10px; color: #777; font-weight: 500;")
        lbl_desc.setWordWrap(True)
        lbl_desc.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        right_layout.addWidget(lbl_title)
        right_layout.addWidget(lbl_desc)

        layout.addLayout(right_layout)

    def enterEvent(self, event):
        self.shadow.setBlurRadius(15)
        self.shadow.setYOffset(4)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.shadow.setBlurRadius(10)
        self.shadow.setYOffset(2)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.filter_type)
        super().mousePressEvent(event)

    def setValue(self, val):
        self.val_text.setText(str(val))


class DipendentiPanel(QWidget):
    """Pannello per la visualizzazione e l'importazione dell'anagrafica dipendenti."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Colonne della Tabella (Vista Master)
        self.master_headers = [
            "SCAD.\nISAB",
            "ID\nRISORSA",
            "Cognome",
            "Nome",
            "CODICE FISCALE",
            "ID\nBADGE",
            "DATA\nASSUNZIONE",
        ]

        # Mapping completo per il Dettaglio
        self.full_headers = [
            "ID Risorsa",
            "Cognome",
            "Nome",
            "Data Nascita",
            "Codice Fiscale",
            "Badge",
            "Data Assunzione",
            "Importato il",
        ]

        self.model = FastTableModel([], self.master_headers)
        self._raw_full_data = []  # Buffer per i dati completi
        self.current_filter = (
            None  # Traccia il filtro attivo ("ok", "warning", "expired", None)
        )

        # Timer per ricerca ritardata (Debounce)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._setup_ui()
        QTimer.singleShot(50, self.refresh_data)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Filtri e Azioni (Top)
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(5)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca per nome, cognome, CF o badge...")
        self.search_input.textChanged.connect(lambda: self.search_timer.start(500))
        filter_layout.addWidget(self.search_input)

        refresh_btn = QPushButton("Aggiorna")
        refresh_btn.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), "#000000"))
        refresh_btn.setIconSize(QSize(24, 24))
        refresh_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(refresh_btn)

        import_btn = QPushButton("Importa CSV")
        import_btn.setIcon(get_colored_icon(get_asset_path(Icons.UPLOAD), "#000000"))
        import_btn.setIconSize(QSize(24, 24))
        import_btn.clicked.connect(self._on_import_clicked)
        filter_layout.addWidget(import_btn)

        main_layout.addLayout(filter_layout)

        # 1.5 Cards Container (Between Search and Table)
        self.cards_container = QWidget()
        cards_layout = QHBoxLayout(self.cards_container)
        cards_layout.setContentsMargins(5, 5, 5, 5)
        cards_layout.setSpacing(15)
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.card_ok = InteractiveStatusCard(
            "Operativi", "#198754", Icons.CHECK_CIRCLE, "Ultimo accesso <= 20gg", "ok"
        )
        self.card_warning = InteractiveStatusCard(
            "In Scadenza",
            "#fd7e14",
            Icons.ALERT_TRIANGLE,
            "Accesso 21-30gg fa",
            "warning",
        )
        self.card_expired = InteractiveStatusCard(
            "Scaduti", "#dc3545", Icons.X_CIRCLE, "Accesso > 30gg fa", "expired"
        )

        self.card_ok.clicked.connect(self._on_card_filter)
        self.card_warning.clicked.connect(self._on_card_filter)
        self.card_expired.clicked.connect(self._on_card_filter)

        cards_layout.addWidget(self.card_ok)
        cards_layout.addWidget(self.card_warning)
        cards_layout.addWidget(self.card_expired)
        cards_layout.addStretch()  # Push cards to left

        main_layout.addWidget(self.cards_container)

        # 2. Area Contenuti (Tabella | Destra: Scheda)
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        # --- TABELLA (A SINISTRA) ---
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        header = self.table.horizontalHeader()
        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)

        self.table.setItemDelegateForColumn(0, ColoredDotDelegate(self.table))

        self.column_widths = [70, 90, 180, 140, 150, 90, 135]
        for col_idx in range(len(self.column_widths)):
            header.setSectionResizeMode(col_idx, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(col_idx, self.column_widths[col_idx])

        total_width = sum(self.column_widths) + 20
        self.table.setFixedWidth(total_width)
        self.content_layout.addWidget(self.table)

        # --- PANNELLO DESTRA (SCHEDA DIPENDENTE VERTICALE) ---

        right_container = QWidget()
        right_container.setFixedWidth(360)
        right_container.setStyleSheet(
            """
            QWidget {
                background-color: #f8f9fa;
            }
        """
        )
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(12)

        # Header Card con gradiente
        header_card = QFrame()
        header_card.setFixedHeight(80)
        header_shadow = QGraphicsDropShadowEffect()
        header_shadow.setBlurRadius(20)
        header_shadow.setXOffset(0)
        header_shadow.setYOffset(3)
        header_shadow.setColor(QColor(0, 0, 0, 60))
        header_card.setGraphicsEffect(header_shadow)
        header_card.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2196F3, stop:1 #1976D2);
                border-radius: 12px;
            }
        """
        )
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel("📋 SCHEDA DIPENDENTE")
        title_label.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            color: white;
            letter-spacing: 1px;
        """
        )

        subtitle_label = QLabel("Dettagli anagrafica e accessi")
        subtitle_label.setStyleSheet(
            """
            font-size: 14px;
            color: rgba(255, 255, 255, 0.90);
            margin-top: 2px;
        """
        )

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        right_layout.addWidget(header_card)

        # Scroll Area per contenuti
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """
        )

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        # Card Informazioni Personali
        personal_card, personal_layout = self._create_info_card("👤 Dati Personali")

        self.detail_labels = {}

        # Riga 1: ID Risorsa | Data Nascita
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)
        id_widget = self._create_field_row("ID Risorsa")
        nascita_widget = self._create_field_row("Data Nascita")
        self.detail_labels["ID Risorsa"] = id_widget
        self.detail_labels["Data Nascita"] = nascita_widget
        row1_layout.addWidget(id_widget)
        row1_layout.addWidget(nascita_widget)
        personal_layout.addLayout(row1_layout)

        # Riga 2: Cognome | Nome
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(10)
        cognome_widget = self._create_field_row("Cognome")
        nome_widget = self._create_field_row("Nome")
        self.detail_labels["Cognome"] = cognome_widget
        self.detail_labels["Nome"] = nome_widget
        row2_layout.addWidget(cognome_widget)
        row2_layout.addWidget(nome_widget)
        personal_layout.addLayout(row2_layout)

        # Riga 3: Codice Fiscale
        cf_widget = self._create_field_row("Codice Fiscale")
        self.detail_labels["Codice Fiscale"] = cf_widget
        personal_layout.addWidget(cf_widget)

        scroll_layout.addWidget(personal_card)

        # Card Badge e Assunzione
        work_card, work_layout = self._create_info_card("💼 Informazioni Lavorative")

        # Riga 1: Badge | Data Assunzione
        row3_layout = QHBoxLayout()
        row3_layout.setSpacing(10)
        badge_widget = self._create_field_row("Badge")
        assunzione_widget = self._create_field_row("Data Assunzione")
        self.detail_labels["Badge"] = badge_widget
        self.detail_labels["Data Assunzione"] = assunzione_widget
        row3_layout.addWidget(badge_widget)
        row3_layout.addWidget(assunzione_widget)
        work_layout.addLayout(row3_layout)

        # Campo singolo: Importato il
        importato_widget = self._create_field_row("Importato il")
        self.detail_labels["Importato il"] = importato_widget
        work_layout.addWidget(importato_widget)

        scroll_layout.addWidget(work_card)

        # Card Ultimo Accesso ISAB (Evidenziata)
        access_card = QFrame()
        access_shadow = QGraphicsDropShadowEffect()
        access_shadow.setBlurRadius(15)
        access_shadow.setXOffset(0)
        access_shadow.setYOffset(3)
        access_shadow.setColor(QColor(0, 0, 0, 50))
        access_card.setGraphicsEffect(access_shadow)
        access_card.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 10px;
                border-left: 4px solid #2196F3;
            }
        """
        )
        access_layout = QVBoxLayout(access_card)
        access_layout.setContentsMargins(18, 15, 18, 15)
        access_layout.setSpacing(10)

        access_title = QLabel("🏭 ULTIMO ACCESSO ISAB")
        access_title.setStyleSheet(
            """
            font-size: 13px;
            font-weight: bold;
            color: #2196F3;
            letter-spacing: 0.5px;
        """
        )

        self.last_access_label = QLabel("-")
        self.last_access_label.setWordWrap(True)
        self.last_access_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.last_access_label.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            padding: 5px 0;
        """
        )

        access_layout.addWidget(access_title)
        access_layout.addWidget(self.last_access_label)
        scroll_layout.addWidget(access_card)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        right_layout.addWidget(scroll)

        # Add components to content layout
        self.content_layout.addWidget(right_container)
        self.content_layout.addStretch()  # Push Table and Scheda to the left

        main_layout.addLayout(self.content_layout)

    def _create_info_card(self, title):
        """Crea una card informativa con ombra e stile moderno.
        Restituisce (card, content_layout) dove content_layout è il layout per i contenuti.
        """
        card = QFrame()
        card_shadow = QGraphicsDropShadowEffect()
        card_shadow.setBlurRadius(12)
        card_shadow.setXOffset(0)
        card_shadow.setYOffset(2)
        card_shadow.setColor(QColor(0, 0, 0, 30))
        card.setGraphicsEffect(card_shadow)
        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """
        )

        # Layout principale della card
        main_layout = QVBoxLayout(card)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header della card
        header = QLabel(title)
        header.setStyleSheet(
            """
            font-size: 15px;
            font-weight: bold;
            color: #5a5a5a;
            background-color: transparent;
            padding: 12px 15px 8px 15px;
            letter-spacing: 0.5px;
        """
        )
        main_layout.addWidget(header)

        # Container per il contenuto
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 12, 15, 12)
        content_layout.setSpacing(10)

        main_layout.addWidget(content_widget)

        return card, content_layout

    def _create_field_row(self, label_text):
        """Crea una riga di campo con label e valore stilizzati."""
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 8)
        layout.setSpacing(4)

        # Label
        label = QLabel(label_text.upper())
        label.setStyleSheet(
            """
            font-size: 13px;
            font-weight: 700;
            color: #888;
            letter-spacing: 0.5px;
        """
        )

        # Valore
        value = QLabel("-")
        value.setWordWrap(True)
        value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        value.setStyleSheet(
            """
            font-size: 17px;
            font-weight: 600;
            color: #2c3e50;
            padding: 3px 0;
        """
        )

        layout.addWidget(label)
        layout.addWidget(value)

        # Salviamo il riferimento al widget valore per poterlo aggiornare
        container.value_label = value

        return container

    def _create_summary_card(self, label, color):
        """Crea una card VERTICALE compatta (per essere disposta in riga)."""
        card = QFrame()
        card.setFixedSize(120, 60)
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: white;
                border: 1px solid #dee2e6;
                border-top: 4px solid {color};
                border-radius: 6px;
            }}
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

        lbl_text = QLabel(label)
        lbl_text.setStyleSheet("font-size: 10px; color: #6c757d; font-weight: bold;")
        lbl_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        val_text = QLabel("0")
        val_text.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")
        val_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl_text)
        layout.addWidget(val_text)

        setattr(self, f"val_{label.lower().replace(' ', '_')}", val_text)
        return card

    def _format_db_date(self, date_str: str) -> str:
        """Converte la data ISO del DB in formato GG/MM/AAAA HH:MM:SS."""
        if not date_str or date_str == "None":
            return "-"
        try:
            # SQLite CURRENT_TIMESTAMP è 'YYYY-MM-DD HH:MM:SS'
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            return date_str

    def _get_last_isab_access(self, cognome: str, nome: str) -> tuple[str, str, str]:
        """
        Recupera l'ultimo accesso ISAB e calcola lo stato abilitazione.
        Ritorna: (data_formattata, giorni_trascorsi, colore_hex)
        """
        # Normalizziamo input in modo aggressivo
        norm_cognome = self._normalize_name(cognome)
        norm_nome = self._normalize_name(nome)

        # Usiamo una ricerca flessibile per gestire sdoppiamenti nel DB
        query = """
            SELECT data FROM timbrature
            WHERE UPPER(REPLACE(REPLACE(TRIM(cognome), '  ', ' '), '  ', ' ')) = ? 
              AND UPPER(REPLACE(REPLACE(TRIM(nome), '  ', ' '), '  ', ' ')) = ?
            ORDER BY data DESC LIMIT 1
        """
        try:
            res = db_manager.execute_query(
                db_manager.DB_TIMBRATURE, query, (norm_cognome, norm_nome)
            )
            if not res:
                return "Mai effettuato", "-", "#6c757d"  # Grigio

            last_date_str = str(res[0][0])
            date_part = last_date_str.split(" ")[0]

            last_date = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                try:
                    last_date = datetime.strptime(date_part, fmt)
                    break
                except ValueError:
                    continue

            if not last_date:
                return "Errore data", "-", "#6c757d"

            today = datetime.now()
            delta = (today - last_date).days

            formatted_date = last_date.strftime("%d/%m/%Y")

            if delta <= 20:
                return (
                    f"{formatted_date} ({delta} gg fa)",
                    str(delta),
                    "#198754",
                )  # Verde
            elif delta <= 30:
                return (
                    f"{formatted_date} ({delta} gg fa)",
                    str(delta),
                    "#fd7e14",
                )  # Arancione
            else:
                return (
                    f"{formatted_date} (SCADUTA - {delta} gg fa)",
                    str(delta),
                    "#dc3545",
                )  # Rosso

        except Exception as e:
            logger.error(f"Errore recupero ultimo accesso ISAB: {e}")
            return "Errore", "-", "#6c757d"

    def _on_card_filter(self, filter_type):
        """Gestisce il filtro quando si clicca su una card."""
        # Se clicco sulla stessa card, rimuovo il filtro
        if self.current_filter == filter_type:
            self.current_filter = None
            ToastManager.instance().show(
                "Filtro rimosso - Visualizzazione completa ripristinata",
                "info",
                duration=2000,
            )
        else:
            self.current_filter = filter_type
            filter_names = {
                "ok": "Operativi (≤20 giorni)",
                "warning": "In Scadenza (21-30 giorni)",
                "expired": "Scaduti (>30 giorni)",
            }
            ToastManager.instance().show(
                f"Filtro attivo: {filter_names.get(filter_type)}", "info", duration=2000
            )

        # Aggiorna l'aspetto delle card per indicare quale è attiva
        for card in [self.card_ok, self.card_warning, self.card_expired]:
            if card.filter_type == self.current_filter:
                card.setStyleSheet(
                    f"""
                    InteractiveStatusCard {{
                        background-color: #f0f0f0;
                        border: 3px solid {card.base_color};
                        border-radius: 12px;
                    }}
                """
                )
            else:
                card.setStyleSheet(
                    f"""
                    InteractiveStatusCard {{
                        background-color: white;
                        border: 2px solid {card.base_color};
                        border-radius: 12px;
                    }}
                """
                )

        # Ricarica i dati con il filtro applicato
        self.refresh_data()

    def _on_selection_changed(self, selected, _deselected):
        """Aggiorna il pannello dettaglio prendendo i dati direttamente dal modello (sincronizzato con sorting)."""
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return

        row_idx = indexes[0].row()
        # Recuperiamo la riga completa dal modello (contiene anche i campi extra oltre i 7 visibili)
        row_data = self.model._data[row_idx]

        # Mappatura indici basata sulla struttura creata in _process_employee_rows:
        # 0:scad, 1:id_ris, 2:disp_cog, 3:nome, 4:cf, 5:badge, 6:assunz, 7:nascita, 8:created, 9:real_cog
        mapping = {
            "ID Risorsa": 1,
            "Cognome": 9,  # Usiamo il cognome reale senza icone
            "Nome": 3,
            "Data Nascita": 7,
            "Codice Fiscale": 4,
            "Badge": 5,
            "Data Assunzione": 6,
            "Importato il": 8,
        }

        cognome = str(row_data[9])
        nome = str(row_data[3])

        for h in self.full_headers:
            idx = mapping.get(h)
            val = (
                str(row_data[idx])
                if idx is not None and row_data[idx] is not None
                else ""
            )

            if val.lower() in ["nan", "none"]:
                val = ""

            # Formattazione speciale per l'ultima colonna (Importato il)
            if h == "Importato il":
                val = self._format_db_date(val)

            # Aggiorna il valore nel container
            if h in self.detail_labels:
                self.detail_labels[h].value_label.setText(val)

        # Recupero e visualizzazione Ultimo Accesso ISAB (usando la logica robusta di match)
        access_info, _, color = self._get_last_isab_access(cognome, nome)
        self.last_access_label.setText(access_info)
        self.last_access_label.setStyleSheet(
            f"color: {color}; font-weight: bold; font-size: 14px; padding: 5px 0;"
        )

    def _inactivation_formatter(self, value):
        """Formatta la colonna SCAD. ISAB con pallino e numero."""
        if value is None or value == "":
            return ""

        try:
            days = int(value)
            # Determina il colore basato sui giorni rimanenti
            # Se giorni_trascorsi <= 20 -> days >= 10 (VERDE)
            # Se 21 <= giorni_trascorsi <= 30 -> 0 <= days < 10 (ARANCIO)
            # Se giorni_trascorsi > 30 -> days < 0 (ROSSO)

            dot = "●"
            if days >= 10:
                pass  # Verde
            elif days >= 0:
                pass  # Arancio
            else:
                days = 0  # Mostriamo 0 per gli scaduti come da immagine

            return f"{dot} {days}"
        except Exception:
            return str(value)

    def refresh_data(self):
        """Aggiorna i dati della tabella Dipendenti."""
        search_text = self.search_input.text().lower()

        query = """
            SELECT id_risorsa, cognome, nome, data_nascita, badge, data_assunzione, created_at, codice_fiscale
            FROM dipendenti WHERE 1=1
        """
        params = []

        if search_text:
            query += " AND (cognome LIKE ? OR nome LIKE ? OR badge LIKE ? OR codice_fiscale LIKE ?)"
            p = f"%{search_text}%"
            params.extend([p, p, p, p])

        query += " ORDER BY cognome ASC, nome ASC"

        # Update Headers Alignment
        self.table.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )

        try:
            full_rows = db_manager.execute_query(
                db_manager.DB_DIPENDENTI, query, tuple(params)
            )

            master_rows = self._process_employee_rows(full_rows)

            self.model.update_data(master_rows)
            self.model.set_column_formatter(0, self._inactivation_formatter)
            self.model.set_column_alignment(0, Qt.AlignmentFlag.AlignCenter)

        except Exception as e:
            logger.error(f"Errore caricamento dipendenti: {e}")

    def _normalize_name(self, text: str) -> str:
        """Rimuove spazi multipli interni e spazi esterni, tutto maiuscolo."""
        if not text:
            return ""
        # Rimuove spazi esterni e converte in maiuscolo
        text = str(text).strip().upper()
        # Rimpiazza spazi multipli interni con spazio singolo
        import re

        return re.sub(r"\s+", " ", text)

    def _build_timbrature_maps(self, accessi):
        """Costruisce le mappe per lookup accessi (Xenon Refactor)."""
        today = datetime.now()
        last_by_cf = {}
        last_by_name = {}

        def normalize(t):
            return re.sub(r"\s+", " ", str(t).strip().upper())

        for cog, nom, cf, d_str in accessi:
            if d_str:
                norm_key = (normalize(cog), normalize(nom))
                norm_cf = cf.strip().upper() if cf and cf.strip() else None

                with suppress(Exception):
                    date_part = str(d_str).split(" ")[0]
                    d_dt = None
                    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                        try:
                            d_dt = datetime.strptime(date_part, fmt)
                            break
                        except ValueError:
                            continue

                    if d_dt:
                        diff = (today - d_dt).days
                        if norm_cf:
                            if norm_cf not in last_by_cf or diff < last_by_cf[norm_cf]:
                                last_by_cf[norm_cf] = diff
                        if (
                            norm_key not in last_by_name
                            or diff < last_by_name[norm_key]
                        ):
                            last_by_name[norm_key] = diff
        return last_by_cf, last_by_name, normalize

    def _compute_employee_status(self, r, last_by_cf, last_by_name, normalize):
        """Calcola lo stato di un singolo dipendente."""
        cf_val = str(r[7]).strip().upper() if r[7] else ""
        cog_val = normalize(r[1])
        nom_val = normalize(r[2])

        diff_days = None
        cf_warning = False

        if cf_val:
            diff_days = last_by_cf.get(cf_val)
        if diff_days is None:
            diff_days = last_by_name.get((cog_val, nom_val))
            if diff_days is not None and not cf_val:
                cf_warning = True

        return diff_days, cf_warning, cog_val, nom_val, cf_val

    def _process_employee_rows(self, full_rows):
        """Elabora le righe dipendenti calcolando scadenza e preparando i dati completi per il modello."""
        # Recuperiamo tutte le timbrature per processarle con normalizzazione
        query_timb = "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
        accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)
        today = datetime.now()

        import re

        def normalize(t):
            return re.sub(r"\s+", " ", str(t).strip().upper())

        # Mappe per l'ultimo accesso
        last_by_cf = {}
        last_by_name = {}

        for cog, nom, cf, d_str in accessi:
            if d_str:
                norm_key = (normalize(cog), normalize(nom))
                norm_cf = cf.strip().upper() if cf and cf.strip() else None

                with suppress(Exception):
                    date_part = str(d_str).split(" ")[0]
                    d_dt = None
                    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                        try:
                            d_dt = datetime.strptime(date_part, fmt)
                            break
                        except ValueError:
                            continue

                    if d_dt:
                        diff = (today - d_dt).days
                        if norm_cf:
                            if norm_cf not in last_by_cf or diff < last_by_cf[norm_cf]:
                                last_by_cf[norm_cf] = diff
                        if (
                            norm_key not in last_by_name
                            or diff < last_by_name[norm_key]
                        ):
                            last_by_name[norm_key] = diff

        master_rows = []

        # Counters
        count_ok = 0
        count_warning = 0
        count_expired = 0

        for r in full_rows:
            # Source fields from DB (id_risorsa, cognome, nome, data_nascita, badge, data_assunzione, created_at, codice_fiscale)
            cf_val = str(r[7]).strip().upper() if r[7] else ""
            cog_val = normalize(r[1])
            nom_val = normalize(r[2])

            diff_days = None
            cf_warning = False

            if cf_val:
                diff_days = last_by_cf.get(cf_val)
            if diff_days is None:
                diff_days = last_by_name.get((cog_val, nom_val))
                if diff_days is not None and not cf_val:
                    cf_warning = True

            # --- Aggiorna Contatori (TOTALE) ---
            if diff_days is not None:
                # <= 20: Operativi
                # 21-30: In Scadenza
                # > 30: Scaduti
                if diff_days <= 20:
                    count_ok += 1
                elif diff_days <= 30:
                    count_warning += 1
                else:
                    count_expired += 1
            # -----------------------------------

            inactivation_val = None
            if diff_days is not None:
                inactivation_val = 30 - diff_days

            # Filtro Visualizzazione
            if self.current_filter:
                if diff_days is None:
                    continue
                if self.current_filter == "ok" and diff_days > 20:
                    continue
                elif self.current_filter == "warning" and (
                    diff_days <= 20 or diff_days > 30
                ):
                    continue
                elif self.current_filter == "expired" and diff_days <= 30:
                    continue

            display_cognome = r[1]
            if cf_warning:
                display_cognome = f"⚠️ {r[1]}"

            # Costruiamo la riga "Mega" che contiene colonne visibili (0-6) e dati extra (7-9)
            # 0:scad, 1:id_ris, 2:disp_cog, 3:nome, 4:cf, 5:badge, 6:assunz | 7:nascita, 8:created, 9:real_cog
            master_rows.append(
                [
                    inactivation_val,  # 0
                    r[0],  # 1 (id_risorsa)
                    display_cognome,  # 2
                    r[2],  # 3 (nome)
                    r[7],  # 4 (codice_fiscale)
                    r[4],  # 5 (badge)
                    r[5],  # 6 (data_assunzione)
                    r[3],  # 7 (data_nascita)
                    r[6],  # 8 (created_at)
                    r[1],  # 9 (cognome pulito)
                ]
            )

        # Aggiorna UI Cards
        self.card_ok.setValue(count_ok)
        self.card_warning.setValue(count_warning)
        self.card_expired.setValue(count_expired)

        return master_rows

    def _on_import_clicked(self):
        """Gestisce l'importazione del file CSV."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona Anagrafica Dipendenti",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if not file_path:
            return

        try:
            with open(file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f, delimiter=";")

                imported_count = 0
                for row in reader:
                    query = """
                        INSERT OR REPLACE INTO dipendenti
                        (id_risorsa, cognome, nome, data_nascita, codice_fiscale, badge, data_assunzione)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                    db_manager.execute_query(
                        db_manager.DB_DIPENDENTI,
                        query,
                        (
                            row.get("id_risorsa"),
                            row.get("Cognome"),
                            row.get("Nome"),
                            row.get("Data_nascita"),
                            row.get("Codice_fiscale", ""),
                            row.get("Badge"),
                            row.get("Data_assunzione"),
                        ),
                    )
                    imported_count += 1

            ToastManager.instance().show(
                f"Importazione completata: {imported_count} dipendenti.", "success"
            )
            self.refresh_data()
        except Exception as e:
            logger.error(f"Errore durante l'importazione CSV: {e}")
            QMessageBox.critical(
                self, "Errore Importazione", f"Impossibile importare il file:\n{e}"
            )
