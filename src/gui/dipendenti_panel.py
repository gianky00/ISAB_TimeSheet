"""
SyncroJob - Pannello Dipendenti
Visualizzazione e gestione dell'anagrafica dipendenti.
"""

import csv
import logging
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
        self.setFixedSize(180, 110)  # Dimensioni fisse - ridotto a 180px
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Tooltip informativo
        tooltip = f"<b>{label}</b><br/>{description} nello stabilimento ISAB<br/><i>Clicca per filtrare</i>"
        self.setToolTip(tooltip)

        # Effetto Ombra
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(self.shadow)

        self.setStyleSheet(
            f"""
            InteractiveStatusCard {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 12px;
            }}
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(12)

        # Icona e Testo
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        lbl_title = QLabel(label.upper())
        lbl_title.setStyleSheet(
            "font-size: 12px; font-weight: 800; color: #9e9e9e; letter-spacing: 1px;"
        )

        self.val_text = QLabel("0")
        self.val_text.setStyleSheet(
            f"font-size: 36px; font-weight: 900; color: {color};"
        )

        # Descrizione sotto il numero
        lbl_desc = QLabel(description)
        lbl_desc.setStyleSheet("font-size: 11px; color: #6c757d; font-weight: 600;")
        lbl_desc.setWordWrap(True)

        info_layout.addWidget(lbl_title)
        info_layout.addWidget(self.val_text)
        info_layout.addWidget(lbl_desc)

        # Indicatore laterale colorato
        self.accent = QFrame()
        self.accent.setFixedWidth(5)
        self.accent.setStyleSheet(f"background-color: {color}; border-radius: 2px;")

        layout.addWidget(self.accent)
        layout.addLayout(info_layout)
        layout.addStretch()

    def enterEvent(self, event):
        # Animazione ombra al passaggio del mouse - senza spostare la card
        self.shadow.setBlurRadius(20)
        self.shadow.setYOffset(6)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Ritorna all'ombra normale
        self.shadow.setBlurRadius(15)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(0, 0, 0, 40))
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Gestisce il click sulla card."""
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
            "ID\nBADGE",
            "DATA\nASSUNZIONE",
        ]

        # Mapping completo per il Dettaglio
        self.full_headers = [
            "ID Risorsa",
            "Cognome",
            "Nome",
            "Data Nascita",
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
        filter_layout.setSpacing(1)  # Spacing ridotto tra gli elementi

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca per nome, cognome o badge...")
        self.search_input.textChanged.connect(lambda: self.search_timer.start(500))
        filter_layout.addWidget(self.search_input)

        refresh_btn = QPushButton("Aggiorna")
        refresh_btn.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), "#000000"))
        refresh_btn.setIconSize(QSize(24, 24))  # Icona ingrandita
        refresh_btn.setToolTip("Aggiorna l'elenco dei dipendenti dal database")
        refresh_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(refresh_btn)

        import_btn = QPushButton("Importa CSV")
        import_btn.setIcon(get_colored_icon(get_asset_path(Icons.UPLOAD), "#000000"))
        import_btn.setIconSize(QSize(24, 24))  # Icona ingrandita
        import_btn.setToolTip(
            "Importa anagrafica dipendenti da file CSV (separatore: punto e virgola)"
        )
        import_btn.clicked.connect(self._on_import_clicked)
        filter_layout.addWidget(import_btn)

        main_layout.addLayout(filter_layout)

        # 2. Area Contenuti (Tabella | Medio: Contatori | Destra: Scheda)
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(
            10
        )  # Spacing ridotto per avvicinare card alla tabella

        # --- TABELLA (A SINISTRA) - STATICA CON COLONNE FISSE ---
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

        # Aggiungi delegate per colorare i pallini
        self.table.setItemDelegateForColumn(0, ColoredDotDelegate(self.table))

        # Larghezze fisse per ogni colonna (in px) - calcolate sui dati reali
        # Ordine: SCAD.ISAB | ID RISORSA | Cognome | Nome | ID BADGE | DATA ASSUNZIONE
        # Cognomi più lunghi: "BELLUCCI PRESTIGIACOMO" (22 char)
        # Nomi più lunghi: "MOHAMED NASER", "ADEL IBRAHIM" (12-13 char)
        self.column_widths = [70, 90, 200, 160, 90, 135]  # Nome aumentato a 160px

        # Imposta tutte le colonne come Fixed (non ridimensionabili)
        for col_idx in range(len(self.column_widths)):
            header.setSectionResizeMode(col_idx, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(col_idx, self.column_widths[col_idx])

        # Calcola larghezza totale tabella: somma colonne + scrollbar + bordi
        total_width = sum(self.column_widths) + 20  # 20px per scrollbar e margini
        self.table.setFixedWidth(total_width)

        self.content_layout.addWidget(self.table)

        # --- AREA MEDIA (CONTATORI ORIZZONTALI IN ALTO) - STATICA ---
        self.middle_container = QWidget()
        self.middle_container.setFixedWidth(
            600
        )  # Larghezza fissa con margine per bordi: 3 card × 180px + 2 spacing × 12px + margini
        middle_layout = QVBoxLayout(self.middle_container)
        middle_layout.setContentsMargins(
            10, 20, 10, 0
        )  # Margine superiore aumentato da 10 a 20
        middle_layout.setSpacing(0)

        # Container orizzontale per le card
        self.summary_container = QWidget()
        summary_h_layout = QHBoxLayout(self.summary_container)
        summary_h_layout.setContentsMargins(0, 0, 0, 0)
        summary_h_layout.setSpacing(12)  # Spacing ridotto tra le card

        self.card_ok = InteractiveStatusCard(
            "Operativi",
            "#198754",
            Icons.CHECK_CIRCLE,
            "Ultimo accesso entro 20 giorni",
            "ok",
        )
        self.card_warning = InteractiveStatusCard(
            "In Scadenza",
            "#fd7e14",
            Icons.ALERT_TRIANGLE,
            "Nessun accesso da 21-30 giorni",
            "warning",
        )
        self.card_expired = InteractiveStatusCard(
            "Scaduti",
            "#dc3545",
            Icons.X_CIRCLE,
            "Oltre 30 giorni senza accesso",
            "expired",
        )

        # Connetti i segnali delle card
        self.card_ok.clicked.connect(self._on_card_filter)
        self.card_warning.clicked.connect(self._on_card_filter)
        self.card_expired.clicked.connect(self._on_card_filter)

        summary_h_layout.addWidget(self.card_ok)
        summary_h_layout.addWidget(self.card_warning)
        summary_h_layout.addWidget(self.card_expired)

        middle_layout.addWidget(self.summary_container)
        middle_layout.addStretch(1)  # Spinge tutto verso l'alto

        self.content_layout.addWidget(self.middle_container)

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

        self.content_layout.addWidget(right_container)

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
        query = """
            SELECT data FROM timbrature
            WHERE UPPER(cognome) = UPPER(?) AND UPPER(nome) = UPPER(?)
            ORDER BY data DESC LIMIT 1
        """
        try:
            res = db_manager.execute_query(
                db_manager.DB_TIMBRATURE, query, (cognome, nome)
            )
            if not res:
                return "Mai effettuato", "-", "#6c757d"  # Grigio

            last_date_str = res[0][0]
            # Formato data in timbrature è solitamente 'YYYY-MM-DD'
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
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
        """Aggiorna il pannello dettaglio quando si seleziona una riga."""
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return

        row_idx = indexes[0].row()
        if row_idx < len(self._raw_full_data):
            data = self._raw_full_data[row_idx]
            cognome = ""
            nome = ""

            for i, h in enumerate(self.full_headers):
                val = str(data[i]) if data[i] is not None else ""
                if val.lower() == "nan":
                    val = ""

                if h == "Cognome":
                    cognome = val
                if h == "Nome":
                    nome = val

                # Formattazione speciale per l'ultima colonna (Importato il)
                if h == "Importato il":
                    val = self._format_db_date(val)

                # Aggiorna il valore nel container (usa value_label)
                if h in self.detail_labels:
                    self.detail_labels[h].value_label.setText(val)

            # Recupero e visualizzazione Ultimo Accesso ISAB
            if cognome and nome:
                access_info, _, color = self._get_last_isab_access(cognome, nome)
                self.last_access_label.setText(access_info)
                self.last_access_label.setStyleSheet(
                    f"color: {color}; font-weight: bold; font-size: 14px; padding: 5px 0;"
                )
            else:
                self.last_access_label.setText("-")
                self.last_access_label.setStyleSheet(
                    "color: #6c757d; font-weight: bold; font-size: 13px; padding: 5px 0;"
                )

    def _inactivation_formatter(self, value):
        """Formatta la colonna SCAD. ISAB con pallino e numero."""
        if value is None or value == "":
            return ""

        try:
            days = int(value)
            # Determina il colore basato sui giorni rimanenti
            # days = 30 - giorni_trascorsi
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

        # Update Counters logic
        from src.core.auth_monitor import check_expiring_isab_authorizations

        try:
            expiring = check_expiring_isab_authorizations()
            scaduti = len([d for d in expiring if d["stato"] == "SCADUTA"])
            in_scadenza = len([d for d in expiring if d["stato"] == "IN SCADENZA"])

            # Query per gli operativi (chi ha accesso <= 20gg)
            query_ok = "SELECT COUNT(*) FROM (SELECT MAX(data) as d FROM timbrature GROUP BY cognome, nome) WHERE (julianday('now') - julianday(d)) <= 20"
            res_ok = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_ok)
            operativi = res_ok[0][0] if res_ok else 0

            self.card_ok.setValue(operativi)
            self.card_warning.setValue(in_scadenza)
            self.card_expired.setValue(scaduti)
        except Exception as e:
            logger.error(f"Errore aggiornamento contatori ISAB: {e}")

        query = """
            SELECT id_risorsa, cognome, nome, data_nascita, badge, data_assunzione, created_at
            FROM dipendenti WHERE 1=1
        """
        params = []

        if search_text:
            query += " AND (cognome LIKE ? OR nome LIKE ? OR badge LIKE ?)"
            p = f"%{search_text}%"
            params.extend([p, p, p])

        query += " ORDER BY cognome ASC, nome ASC"

        # Update Headers Alignment
        self.table.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )

        try:
            full_rows = db_manager.execute_query(
                db_manager.DB_DIPENDENTI, query, tuple(params)
            )

            # Dizionario per accesso rapido all'ultimo accesso
            # Recuperiamo tutti gli ultimi accessi ISAB in una volta
            query_timb = "SELECT MAX(data), cognome, nome FROM timbrature GROUP BY UPPER(cognome), UPPER(nome)"
            last_access_map = {}
            accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)
            today = datetime.now()
            for d_str, cog, nom in accessi:
                if d_str:
                    try:
                        d_dt = datetime.strptime(d_str, "%Y-%m-%d")
                        diff = (today - d_dt).days
                        last_access_map[
                            (cog.upper().strip(), nom.upper().strip())
                        ] = diff
                    except Exception:
                        pass

            # Preparazione dati per tabella master (subset di colonne)
            master_rows = []
            filtered_full_rows = []

            for r in full_rows:
                cog_key = (str(r[1]).upper().strip(), str(r[2]).upper().strip())
                diff_days = last_access_map.get(cog_key)

                inactivation_val = None
                if diff_days is not None:
                    inactivation_val = 30 - diff_days

                # Applica il filtro se attivo
                if self.current_filter:
                    if diff_days is None:
                        continue  # Salta chi non ha mai fatto accesso

                    if self.current_filter == "ok" and diff_days > 20:
                        continue
                    elif self.current_filter == "warning" and (
                        diff_days <= 20 or diff_days > 30
                    ):
                        continue
                    elif self.current_filter == "expired" and diff_days <= 30:
                        continue

                # inattivazione(new), id(0), cognome(1), nome(2), badge(4), assunzione(5)
                master_rows.append([inactivation_val, r[0], r[1], r[2], r[4], r[5]])
                filtered_full_rows.append(r)

            # Aggiorna il buffer dei dati completi con i dati filtrati
            self._raw_full_data = filtered_full_rows

            self.model.update_data(master_rows)
            self.model.set_column_formatter(0, self._inactivation_formatter)
            self.model.set_column_alignment(0, Qt.AlignmentFlag.AlignCenter)

        except Exception as e:
            logger.error(f"Errore caricamento dipendenti: {e}")

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
                        (id_risorsa, cognome, nome, data_nascita, badge, data_assunzione)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """
                    db_manager.execute_query(
                        db_manager.DB_DIPENDENTI,
                        query,
                        (
                            row.get("id_risorsa"),
                            row.get("Cognome"),
                            row.get("Nome"),
                            row.get("Data_nascita"),
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
