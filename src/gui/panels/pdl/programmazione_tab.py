"""
SyncroJob - PDL Programmazione Tab
Scheda per il monitoraggio della programmazione settimanale SafeWork.
"""

import base64
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from src.gui.widgets.core_widgets import (PrimaryButton, SecondaryButton, DangerButton, GhostButton, IconButton, SearchInput, StandardInput, StandardTextEdit, FilterComboBox, StandardCheckBox, StandardSpinBox, StandardTable, StandardListWidget, StandardTreeWidget, StandardGroupBox, StandardProgressBar)
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.bots import create_bot
from src.core import config_manager
from src.core.constants import Icons
from src.core.database.pdl_queries import PDLQueries
from src.gui.panels.base import BotWorker
from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.gui.widgets import MultiSelectFilter, TimelineWidget
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path

logger = logging.getLogger(__name__)


class ProgrammingStatusWidget(QWidget):
    """Widget elegante che mostra una barra di stato verde/arancione per TCL e TGO."""

    def __init__(
        self,
        tcl: bool,
        tgo: bool,
        connect_left: bool = False,
        connect_right: bool = False,
        is_today: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self.tcl = tcl
        self.tgo = tgo
        self.connect_left = connect_left
        self.connect_right = connect_right
        self.is_today = is_today
        # Espansione orizzontale completa per coprire l'intera cella (effetto colonna)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setMinimumHeight(16)
        self._setup_tooltip()

    def _get_icon_base64(self, icon_path: str) -> str:
        """Converte un'icona SVG in base64 per l'uso nel tooltip HTML."""
        try:
            path = Path(icon_path)
            if path.exists():
                with path.open("rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                    return f"data:image/svg+xml;base64,{encoded}"
        except Exception as e:
            logger.error(f"Errore caricamento icona base64: {e}")
        return ""

    def _setup_tooltip(self):
        """Crea un tooltip puramente grafico con solo le icone originali."""
        tcl_icon_path = get_asset_path(Icons.FLAG_TCL_ON if self.tcl else Icons.FLAG_TCL_OFF)
        tgo_icon_path = get_asset_path(Icons.FLAG_TGO_ON if self.tgo else Icons.FLAG_TGO_OFF)

        tcl_b64 = self._get_icon_base64(tcl_icon_path)
        tgo_b64 = self._get_icon_base64(tgo_icon_path)

        html = f"""
        <div style='padding: 5px; background-color: white;'>
            <img src='{tcl_b64}' width='32' height='18'>
            <img src='{tgo_b64}' width='32' height='18' style='margin-left: 5px;'>
        </div>
        """
        self.setToolTip(html)

    def paintEvent(self, event):
        """Disegna la barra di stato TCL/TGO nella cella con evidenziazione del giorno corrente."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = float(self.width())
        h = float(self.height())

        # 0. Evidenziazione Giorno Corrente (Background TOTALE della cella)
        if self.is_today:
            # Opacità marcata (~16%) per un effetto colonna pieno e professionale
            c = QColor(COLORS["primary_dark"])
            painter.fillRect(self.rect(), QColor(c.red(), c.green(), c.blue(), 40))

        # Configurazione Barra di Progresso
        bar_w = 80.0  # Larghezza fissa centrata
        bar_h = 10.0  # Altezza barra
        x = (w - bar_w) / 2.0
        y = (h - bar_h) / 2.0
        radius = 5.0

        # Percorso per bordi arrotondati selettivi (Gantt-style)
        path = QPainterPath()

        tl = 0.0 if self.connect_left else radius
        bl = 0.0 if self.connect_left else radius
        tr = 0.0 if self.connect_right else radius
        br = 0.0 if self.connect_right else radius

        # Disegno manuale del rettangolo centrato con angoli variabili
        path.moveTo(x + bar_w - tr, y)
        if tr > 0:
            path.arcTo(x + bar_w - 2 * tr, y, 2 * tr, 2 * tr, 90, -90)
        else:
            path.lineTo(x + bar_w, y)

        path.lineTo(x + bar_w, y + bar_h - br)
        if br > 0:
            path.arcTo(x + bar_w - 2 * br, y + bar_h - 2 * br, 2 * br, 2 * br, 0, -90)
        else:
            path.lineTo(x + bar_w, y + bar_h)

        path.lineTo(x + bl, y + bar_h)
        if bl > 0:
            path.arcTo(x, y + bar_h - 2 * bl, 2 * bl, 2 * bl, 270, -90)
        else:
            path.lineTo(x, y + bar_h)

        path.lineTo(x, y + tl)
        if tl > 0:
            path.arcTo(x, y, 2 * tl, 2 * tl, 180, -90)
        else:
            path.lineTo(x, y)
        path.closeSubpath()

        # 1. Tracciato di sfondo (Grigio visibile)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(COLORS["bg_hover"]))
        painter.drawPath(path)

        # 2. Colori
        green_color = QColor(COLORS["success_dark"])
        orange_color = QColor(COLORS["warning_orange"])

        # 3. Disegno contenuto
        if self.tcl and self.tgo:
            painter.setBrush(green_color)
            painter.drawPath(path)
        elif self.tcl:
            # Solo TCL - Arancione (Sinistra)
            tcl_rect = QRectF(x, y, bar_w / 2.0 + 2.0, bar_h)
            tcl_path = QPainterPath()
            tcl_path.addRoundedRect(tcl_rect, radius, radius)
            painter.setBrush(orange_color)
            painter.drawPath(tcl_path)
        elif self.tgo:
            # Solo TGO - Arancione (Destra)
            tgo_rect = QRectF(x + bar_w / 2.0 - 2.0, y, bar_w / 2.0 + 2.0, bar_h)
            tgo_path = QPainterPath()
            tgo_path.addRoundedRect(tgo_rect, radius, radius)
            painter.setBrush(orange_color)
            painter.drawPath(tgo_path)


class ProgrammazioneTab(QWidget):
    """Sottoscheda per il controllo della programmazione settimanale con vista PDL aggregata."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.worker: BotWorker | None = None
        self.last_results: list[dict[str, Any]] = []
        self.requesters: list[str] = []
        self.tables: list[QTableWidget] = []
        self._setup_ui()
        self._load_requesters()
        # Carica dati persistenti
        self._load_persisted_data()

    def _load_persisted_data(self):
        """Carica dati per la settimana selezionata."""
        try:
            start_date, end_date, _ = self._get_selected_week_range()
            self.last_results = PDLQueries.get_programming_results_by_week(start_date, end_date)

            if self.last_results:
                last_upd = self.last_results[0].get("ultimo_aggiornamento", "N/D")
                self._on_log(
                    f"ℹ️ Caricati {len(self.last_results)} risultati (Aggiornati al: {last_upd}) per la settimana {start_date} - {end_date}."
                )
            else:
                self._on_log(f"ℹ️ Nessun dato salvato per la settimana {start_date} - {end_date}.")

            self._update_table(self.last_results)
            self.btn_email.setEnabled(len(self.last_results) > 0)
        except Exception as e:
            logger.error(f"Errore caricamento dati: {e}")
            self._on_log(f"⚠️ Errore caricamento dati: {e}")

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # --- BARRA SUPERIORE MODERNA ---
        top_bar = QHBoxLayout()

        # Area Filtri
        filter_area = QVBoxLayout()

        # Info Settimana
        start_date, end_date = self._get_current_week_range()
        self.week_label = QLabel(
            f"<span style='color: {COLORS['text_muted']};'>Monitoraggio Settimana:</span> "
            f"<b style='color: {COLORS['text_dark']};'>{start_date} - {end_date}</b>"
        )
        self.week_label.setStyleSheet("font-size: 13px; margin-bottom: 5px;")
        filter_area.addWidget(self.week_label)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(20)

        # --- SEZIONE 1: IMPORTAZIONE (A sinistra) ---
        import_group = QWidget()
        import_layout = QHBoxLayout(import_group)
        import_layout.setContentsMargins(0, 0, 0, 0)
        import_layout.setSpacing(8)

        import_label = QLabel("IMPORTA:")
        import_label.setStyleSheet(f"color: {COLORS['success_dark']}; font-weight: bold; font-size: 11px;")
        import_layout.addWidget(import_label)

        # Selettore Settimana
        self.week_selector = FilterComboBox()
        self.week_selector.addItems(["Settimana Corrente", "Settimana Prossima"])
        self.week_selector.setFixedWidth(160)
        saved_week = config_manager.get_config_value("programming_selected_week", 0)
        self.week_selector.setCurrentIndex(saved_week)
        self.week_selector.currentIndexChanged.connect(self._on_week_changed)
        import_layout.addWidget(self.week_selector)

        # Filtro Richiedenti (Bot)
        self.req_filter = MultiSelectFilter("Richiedenti", "Seleziona Bot...")
        self.req_filter.setFixedWidth(220)
        saved_reqs = config_manager.get_config_value("selected_programming_requesters", [])
        self.req_filter.set_selected(saved_reqs)
        self.req_filter.changed.connect(self._on_requesters_changed)
        # Stile Hover per Importazione
        self.req_filter.setStyleSheet(
            f"""
            MultiSelectFilter QPushButton {{ border: 1px solid transparent; background: transparent; color: {COLORS["success_dark"]}; }}
            MultiSelectFilter QPushButton:hover {{ border: 1px solid {COLORS["success_dark"]}; background: {COLORS["bg_success_pastel"]}; border-radius: 6px; }}
        """
        )
        import_layout.addWidget(self.req_filter)

        controls_layout.addWidget(import_group)

        # Separatore verticale
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet(f"color: {COLORS['border_light']};")
        controls_layout.addWidget(line)

        # --- SEZIONE 2: VISUALIZZAZIONE (A destra) ---
        view_group = QWidget()
        view_layout = QHBoxLayout(view_group)
        view_layout.setContentsMargins(0, 0, 0, 0)
        view_layout.setSpacing(8)

        view_label = QLabel("FILTRA:")
        view_label.setStyleSheet(f"color: {COLORS['primary_blue']}; font-weight: bold; font-size: 11px;")
        view_layout.addWidget(view_label)

        # Filtro Visualizzazione (Locale)
        self.view_filter = MultiSelectFilter("Mostra", "Filtra Risultati...")
        self.view_filter.setFixedWidth(200)
        self.view_filter.changed.connect(self._apply_view_filter)
        # Stile Hover per Visualizzazione
        self.view_filter.setStyleSheet(
            f"""
            MultiSelectFilter QPushButton {{ border: 1px solid transparent; background: transparent; color: {COLORS["primary_blue"]}; }}
            MultiSelectFilter QPushButton:hover {{ border: 1px solid {COLORS["primary_blue"]}; background: {COLORS["bg_info_pastel"]}; border-radius: 6px; }}
        """
        )
        view_layout.addWidget(self.view_filter)

        # Selettore Giorno (Compattazione)
        self.day_selector = FilterComboBox()
        self.day_selector.addItems(
            [
                "Settimana Intera",
                "Oggi",
                "Lunedì",
                "Martedì",
                "Mercoledì",
                "Giovedì",
                "Venerdì",
                "Sabato",
                "Domenica",
            ]
        )
        self.day_selector.setFixedWidth(130)
        self.day_selector.currentTextChanged.connect(self._on_day_filter_changed)
        view_layout.addWidget(self.day_selector)

        # Selettore Raggruppamento
        self.group_selector = FilterComboBox()
        self.group_selector.addItems(["Tabella Unica", "Area", "Richiedente"])
        self.group_selector.setFixedWidth(140)
        saved_group = config_manager.get_config_value("programming_group_mode", "Tabella Unica")
        self.group_selector.setCurrentText(saved_group)
        self.group_selector.currentTextChanged.connect(self._on_group_mode_changed)
        view_layout.addWidget(self.group_selector)

        controls_layout.addWidget(view_group)
        controls_layout.addStretch()
        filter_area.addLayout(controls_layout)

        top_bar.addLayout(filter_area)

        top_bar.addStretch()

        # Azioni
        self.btn_run = ModernButton(
            "Esegui Controllo", variant=ModernButton.Variant.PRIMARY, icon=get_asset_path(Icons.PLAY)
        )
        self.btn_email = ModernButton(
            "Report Outlook", variant=ModernButton.Variant.GHOST, icon=get_asset_path(Icons.SEND)
        )
        self.btn_email.setEnabled(False)
        self.btn_run.clicked.connect(self._on_run_clicked)
        self.btn_email.clicked.connect(self._on_email_clicked)

        top_bar.addWidget(self.btn_email)
        top_bar.addWidget(self.btn_run)

        layout.addLayout(top_bar)

        # --- LOG (Dinamico) ---
        self.log_widget = TimelineWidget()
        self.log_widget.setFixedHeight(180)
        self.log_widget.setVisible(False)
        layout.addWidget(self.log_widget)

        # --- CONTENITORE TABELLE SCROLLABILE ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.tables_container = QWidget()
        self.tables_layout = QVBoxLayout(self.tables_container)
        self.tables_layout.setContentsMargins(0, 0, 0, 0)
        self.tables_layout.setSpacing(25)
        self.tables_layout.addStretch()

        self.scroll_area.setWidget(self.tables_container)
        layout.addWidget(self.scroll_area)

        # Calcolo date iniziale
        self._update_ui_dates()

    def _get_selected_week_range(self) -> tuple[str, str, datetime]:
        """Restituisce start_str, end_str e start_dt in base alla selezione."""
        today = datetime.now()
        current_weekday = today.weekday()
        start_current = today - timedelta(days=current_weekday)

        # 0 = Current, 1 = Next
        offset = self.week_selector.currentIndex() if hasattr(self, "week_selector") else 0

        start_target = start_current + timedelta(weeks=offset)
        end_target = start_target + timedelta(days=6)

        return start_target.strftime("%d/%m/%Y"), end_target.strftime("%d/%m/%Y"), start_target

    def _get_current_week_range(self) -> tuple[str, str]:
        # Mantenuto per compatibilità o uso interno iniziale
        s, e, _ = self._get_selected_week_range()
        return s, e

    def _update_ui_dates(self):
        """Aggiorna label e header di tutte le tabelle attive."""
        start_str, end_str, start_dt = self._get_selected_week_range()

        if hasattr(self, "week_label"):
            self.week_label.setText(
                f"<span style='color: {COLORS['text_muted']};'>Monitoraggio Settimana:</span> "
                f"<b style='color: {COLORS['text_dark']};'>{start_str} - {end_str}</b>"
            )

        d = [(start_dt + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
        headers = [
            "Richiedente",
            "Area",
            "Unità",
            "N° PDL",
            "Descrizione",
            f"LUN {d[0]}",
            f"MAR {d[1]}",
            f"MER {d[2]}",
            f"GIO {d[3]}",
            f"VEN {d[4]}",
            f"SAB {d[5]}",
            f"DOM {d[6]}",
        ]

        is_current_week = getattr(self, "week_selector", None) and self.week_selector.currentIndex() == 0
        current_weekday = datetime.now().weekday()

        for table in self.tables:
            table.setHorizontalHeaderLabels(headers)
            h_header = table.horizontalHeader()
            if h_header is not None:
                h_header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
            for i in range(5, 12):
                item = table.horizontalHeaderItem(i)
                if not item:
                    continue
                is_today = is_current_week and (i - 5 == current_weekday)
                if is_today:
                    # Header più scuro per abbinarsi alla colonna marcata
                    item.setBackground(QColor(COLORS["table_info_bg"]))
                    item.setForeground(QColor(COLORS["primary_dark"]))
                    item.setText(headers[i])
                    font = QFont()
                    font.setBold(True)
                    font.setPointSize(11)
                    item.setFont(font)
                else:
                    item.setBackground(QColor(COLORS["bg_light"]))
                    item.setForeground(QColor(COLORS["text_dark"]))
                    item.setText(headers[i])
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)

        # Ricarica sempre i dati dal DB per la settimana selezionata
        self._load_persisted_data()

    def _load_requesters(self):
        try:
            self.requesters = PDLQueries.get_unique_requesters()
            self.req_filter.set_items(self.requesters)
        except Exception as e:
            logger.error(f"Errore caricamento richiedenti: {e}")

    def _on_requesters_changed(self, selected: list[str]):
        """Salva i richiedenti selezionati nella configurazione."""
        config_manager.set_config_value("selected_programming_requesters", selected)

    def _on_week_changed(self, index: int):
        """Gestisce il cambio settimana salvando la preferenza e aggiornando i dati."""
        config_manager.set_config_value("programming_selected_week", index)
        self._update_ui_dates()

    def _apply_view_filter(self, selected_reqs: list[str] | None = None):
        """Nasconde o mostra le righe delle tabelle in base ai richiedenti selezionati."""
        if selected_reqs is None:
            selected_reqs = self.view_filter.selected

        # Se non c'è nulla di selezionato, mostriamo tutto (comportamento standard)
        show_all = not selected_reqs

        for table in self.tables:
            for row in range(table.rowCount()):
                req_item = table.item(row, 0)
                if req_item:
                    is_visible = show_all or req_item.text() in selected_reqs
                    table.setRowHidden(row, not is_visible)

            # Gestione righe espanse: se nascondo una riga padre, nascondo anche la figlia
            for row in range(table.rowCount()):
                if table.isRowHidden(row) and row + 1 < table.rowCount():
                    # Se la riga successiva è un'espansione, nascondila
                    widget = table.cellWidget(row + 1, 0)
                    from src.gui.widgets.pdl_timeline import PDLTimelineWidget

                    if isinstance(widget, PDLTimelineWidget):
                        table.setRowHidden(row + 1, True)

        self._refresh_tables_visibility()

    def _on_day_filter_changed(self, choice: str):
        """Nasconde le colonne e le righe non programmate per il giorno selezionato."""
        day_map = {
            "Lunedì": 0,
            "Martedì": 1,
            "Mercoledì": 2,
            "Giovedì": 3,
            "Venerdì": 4,
            "Sabato": 5,
            "Domenica": 6,
        }

        target_idx = -1
        if choice == "Oggi":
            target_idx = datetime.now().weekday()
        elif choice in day_map:
            target_idx = day_map[choice]

        for table in self.tables:
            # 1. Gestione Colonne
            for i in range(7):
                col_idx = 5 + i
                table.setColumnHidden(col_idx, target_idx != -1 and i != target_idx)

            # 2. Gestione Righe (Solo se un giorno è selezionato)
            for row in range(table.rowCount()):
                # Salta le righe di espansione (Timeline)
                widget_0 = table.cellWidget(row, 0)
                from src.gui.widgets.pdl_timeline import PDLTimelineWidget

                if isinstance(widget_0, PDLTimelineWidget):
                    continue

                if target_idx == -1:
                    # Ripristina visibilità righe (il filtro 'Mostra' verrà riapplicato dopo)
                    table.setRowHidden(row, False)
                else:
                    # Verifica se c'è programmazione in quel giorno
                    widget = table.cellWidget(row, 5 + target_idx)
                    is_programmed = False
                    if isinstance(widget, ProgrammingStatusWidget):
                        is_programmed = widget.tcl or widget.tgo

                    # Nascondi se non programmato
                    table.setRowHidden(row, not is_programmed)

        # 3. Riapplica sempre il filtro richiedenti e aggiorna visibilità gruppi
        if target_idx == -1:
            self._apply_view_filter()
        else:
            self._refresh_tables_visibility()

    def _refresh_tables_visibility(self):
        """Aggiorna la visibilità dei QGroupBox e l'altezza delle tabelle in base alle righe visibili."""
        # header_h = 45 # Header nascosti
        header_h = 25  # Margine headers

        for table in self.tables:
            visible_rows = 0
            total_height = header_h

            for row in range(table.rowCount()):
                if not table.isRowHidden(row):
                    visible_rows += 1
                    total_height += table.rowHeight(row)

            # Nascondi il GroupBox se non ci sono righe visibili
            group_box = table.parentWidget()
            if isinstance(group_box, QGroupBox):
                group_box.setVisible(visible_rows > 0)

            # Compatta l'altezza della tabella
            if visible_rows > 0:
                new_height = total_height + 20  # Padding extra
                table.setMinimumHeight(new_height)
                table.setMaximumHeight(new_height)
            else:
                table.setMinimumHeight(0)
                table.setMaximumHeight(0)

    def _on_log(self, message: str):
        """Aggiunge un messaggio alla console di log."""
        if hasattr(self, "log_widget"):
            self.log_widget.append(message)

    def _on_group_mode_changed(self, mode: str):
        config_manager.set_config_value("programming_group_mode", mode)
        if self.last_results:
            self._update_table(self.last_results)

    def _deselect_other_tables(self) -> None:
        """Deseleziona tutte le tabelle tranne quella che ha emesso il segnale per garantire selezione univoca."""
        sender_table = self.sender()
        for t in self.tables:
            if t is not sender_table:
                t.clearSelection()

    def _toggle_row_expansion(self, row: int, column: int):
        """Gestisce l'espansione/collasso della riga per mostrare la timeline."""
        sender_table = self.sender()
        if not isinstance(sender_table, QTableWidget):
            return

        # Ignora click sulle righe già espanse (Timeline)
        widget = sender_table.cellWidget(row, 0)
        from src.gui.widgets.pdl_timeline import PDLTimelineWidget

        if isinstance(widget, PDLTimelineWidget):
            return

        # Verifica se la riga successiva è già un'espansione di QUESTA riga
        # Usiamo un UserRole sulla riga successiva per tracciarlo?
        # Più semplice: controlliamo se la riga sotto è una TimelineWidget

        next_row = row + 1
        is_expanded = False
        if next_row < sender_table.rowCount():
            next_widget = sender_table.cellWidget(next_row, 0)
            if isinstance(next_widget, PDLTimelineWidget):
                is_expanded = True

        # Se espansa, chiudi
        if is_expanded:
            sender_table.removeRow(next_row)
            # Ripristina altezza riga originale (opzionale, già standard)
        else:
            # Apri espansione
            # 1. Recupera PDL
            pdl_item = sender_table.item(row, 3)
            if not pdl_item:
                return

            pdl_code = pdl_item.text()

            # 2. Inserisci riga sotto
            sender_table.insertRow(next_row)

            # 3. Recupera dati interveti
            try:
                interventions = PDLQueries.get_pdl_interventions(pdl_code)
            except Exception as e:
                logger.error(f"Errore recupero timeline PDL {pdl_code}: {e}")
                interventions = []

            # 4. Crea Widget Timeline
            timeline = PDLTimelineWidget(interventions)

            # 5. Imposta widget che spanna tutte le colonne
            # Nota: setCellWidget funziona su una cella. Dobbiamo fare span.
            sender_table.setSpan(next_row, 0, 1, sender_table.columnCount())
            sender_table.setCellWidget(next_row, 0, timeline)

            # 6. Adatta altezza riga al contenuto
            sender_table.setRowHeight(next_row, timeline.sizeHint().height())

            # Connetti resize event del widget per aggiornare altezza riga se cambia?
            # Per ora fix height

        self._refresh_tables_visibility()

    def _on_run_clicked(self):
        selected_reqs = self.req_filter.selected

        if not selected_reqs:
            ToastManager.instance().show("Seleziona almeno un richiedente.", "warning")
            return

        config = config_manager.load_config()
        safework_accounts = config.get("safework_accounts", [])
        account = None
        account_type = "Esecutore"
        if safework_accounts:
            account = next((a for a in safework_accounts if a.get("default")), safework_accounts[0])
            account_type = account.get("type", "Esecutore")

        if not account:
            ToastManager.instance().show("Credenziali SafeWork non configurate.", "error")
            return

        start_date, end_date, _ = self._get_selected_week_range()

        # Assicura che la cartella temp esista
        temp_dir = config_manager.CONFIG_DIR / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        bot = create_bot(
            "programmazione_pdl",
            username=account["username"],
            password=account["password"],
            account_type=account_type,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=str(temp_dir),
        )

        if not bot:
            return

        self.btn_run.setEnabled(False)
        self.btn_email.setEnabled(False)

        # Pulisci tabelle esistenti
        while self.tables_layout.count() > 1:
            item = self.tables_layout.takeAt(0)
            if item is not None and (widget := item.widget()):
                widget.deleteLater()
        self.tables.clear()

        self.log_widget.clear()
        self.log_widget.setVisible(True)
        self.log_widget.set_mood("running")

        self.worker = BotWorker(
            bot, [{"requesters": selected_reqs, "date_start": start_date, "date_end": end_date}]
        )
        self.worker.log_signal.connect(self._on_log)
        self.worker.finished_signal.connect(self._on_bot_finished)
        self.worker.start()
        ToastManager.instance().show("Avvio monitoraggio SafeWork...", "info")

    def _on_bot_finished(self, success: bool):
        self.btn_run.setEnabled(True)
        self.log_widget.set_mood("idle")
        if success and self.worker:
            self.log_widget.setVisible(False)
            self.last_results = getattr(self.worker.bot, "results", [])

            start_date, end_date, _ = self._get_selected_week_range()
            if self.last_results:
                PDLQueries.save_programming_results(self.last_results, start_date, end_date)
                self._on_log(f"✅ Dati salvati per la settimana {start_date} - {end_date}")
            else:
                # Carica i vecchi dati se i nuovi sono vuoti (opzionale, ma garantisce 'permanenza')
                self.last_results = PDLQueries.get_programming_results_by_week(start_date, end_date)
                self._on_log(
                    f"ℹ️ Nessun nuovo dato trovato. Mantengo dati precedenti per {start_date} - {end_date}"
                )

            self._update_table(self.last_results)
        else:
            ToastManager.instance().show("Errore durante il controllo SafeWork.", "error")

    def _update_table(self, results: list[dict[str, Any]]):
        """Crea e popola le tabelle in base alla modalità di raggruppamento selezionata."""
        # Pulisci layout esistente
        while self.tables_layout.count() > 1:
            item = self.tables_layout.takeAt(0)
            if item is not None and (widget := item.widget()):
                widget.deleteLater()

        self.tables.clear()
        if not results:
            # Pulisci anche il filtro se non ci sono dati
            self.view_filter.set_items([])
            return

        # Aggiorna gli elementi del filtro visualizzazione con i richiedenti presenti nei risultati
        available_reqs = sorted({r["richiedente"] for r in results})
        self.view_filter.set_items(available_reqs)

        group_mode = self.group_selector.currentText()
        row_h = 42

        # Raggruppamento dati
        grouped_data: dict[str, list[dict[str, Any]]] = {}
        if group_mode == "Tabella Unica":
            grouped_data = {"Programmazione Globale": results}
        elif group_mode == "Area":
            for r in results:
                area = r.get("area") or "Area Non Definita"
                if area not in grouped_data:
                    grouped_data[area] = []
                grouped_data[area].append(r)
        else:  # Richiedente
            for r in results:
                req = r.get("richiedente") or "Richiedente Ignoto"
                if req not in grouped_data:
                    grouped_data[req] = []
                grouped_data[req].append(r)

        # Creazione tabelle per ogni gruppo
        today_idx = datetime.now().weekday()

        for group_name, group_results in sorted(grouped_data.items()):
            group_box = StandardGroupBox(group_name)
            group_box.setStyleSheet(
                f"""
                QGroupBox {{
                    font-weight: bold; font-size: 14px; color: {COLORS["glass_dark"]};
                    border: 1px solid {COLORS["border_light"]}; border-radius: 10px;
                    margin-top: 20px; padding-top: 25px; background-color: {COLORS["bg_white"]};
                }}
                QGroupBox::title {{ subcontrol-origin: margin; subcontrol-position: top center; padding: 0 10px; }}
            """
            )
            group_layout = QVBoxLayout(group_box)

            table = StandardTable()
            table.setColumnCount(12)
            table.setAlternatingRowColors(True)
            table.setRowCount(len(group_results))
            # Disabilita editing per permettere click su riga
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

            # Connetti click (Doppio click per espandere, singolo per selezionare)
            table.cellDoubleClicked.connect(self._toggle_row_expansion)
            # Selezione esclusiva tra tabelle: click su una deseleziona le altre
            table.cellClicked.connect(self._deselect_other_tables)

            # Padding 0 e Margini 0 per permettere al widget di toccare i bordi cella
            # Stile minimale per integrarsi con il GroupBox
            table.setStyleSheet(f"QTableWidget {{ border: none; background-color: {COLORS['bg_white']}; }}")
            v_header = table.verticalHeader()
            if v_header is not None:
                v_header.setVisible(False)
                v_header.setDefaultSectionSize(row_h)  # Use standard row height

            h_header = table.horizontalHeader()
            if h_header is not None:
                h_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
                h_header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

                h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
                h_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
                h_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
                h_header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
                h_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
                for i in range(5, 12):
                    h_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
                    table.setColumnWidth(i, 85)

            # Popolamento Righe
            for row_idx, res in enumerate(group_results):
                table.setItem(row_idx, 0, QTableWidgetItem(res["richiedente"]))
                table.setItem(row_idx, 1, QTableWidgetItem(res.get("area", "")))
                table.setItem(row_idx, 2, QTableWidgetItem(res.get("unita", "")))

                # Cella PDL
                pdl_item = QTableWidgetItem(res["pdl"])
                pdl_item.setData(Qt.ItemDataRole.UserRole, res["pdl"])
                pdl_item.setToolTip("Clicca per vedere la cronologia interventi")
                table.setItem(row_idx, 3, pdl_item)

                table.setItem(row_idx, 4, QTableWidgetItem(res.get("descrizione", "")))

                prog_list = res["programmazione"]
                for i, prog in enumerate(prog_list):
                    is_full = prog["tcl"] and prog["tgo"]

                    conn_left = False
                    if i > 0 and is_full:
                        prev = prog_list[i - 1]
                        if prev["tcl"] and prev["tgo"]:
                            conn_left = True

                    conn_right = False
                    if i < len(prog_list) - 1 and is_full:
                        nxt = prog_list[i + 1]
                        if nxt["tcl"] and nxt["tgo"]:
                            conn_right = True

                    status_widget = ProgrammingStatusWidget(
                        prog["tcl"],
                        prog["tgo"],
                        connect_left=conn_left,
                        connect_right=conn_right,
                        is_today=(i == today_idx),
                    )
                    table.setCellWidget(row_idx, 5 + i, status_widget)

            self.tables.append(table)
            group_layout.addWidget(table)
            self.tables_layout.insertWidget(self.tables_layout.count() - 1, group_box)

        # Applica header dates
        self._update_ui_dates_internal()

        # Riapplica i filtri visualizzazione correnti e compatta
        self._apply_view_filter()
        self._on_day_filter_changed(self.day_selector.currentText())
        self._refresh_tables_visibility()

    def _update_ui_dates_internal(self):
        """Versione interna di update_ui_dates che non ricarica i dati per evitare loop."""
        _, _, start_dt = self._get_selected_week_range()
        d = [(start_dt + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
        headers = [
            "Richiedente",
            "Area",
            "Unità",
            "N° PDL",
            "Descrizione",
            f"LUN {d[0]}",
            f"MAR {d[1]}",
            f"MER {d[2]}",
            f"GIO {d[3]}",
            f"VEN {d[4]}",
            f"SAB {d[5]}",
            f"DOM {d[6]}",
        ]
        is_current_week = getattr(self, "week_selector", None) and self.week_selector.currentIndex() == 0
        current_weekday = datetime.now().weekday()

        for table in self.tables:
            table.setHorizontalHeaderLabels(headers)
            h_header = table.horizontalHeader()
            if h_header is not None:
                h_header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
            for i in range(5, 12):
                item = table.horizontalHeaderItem(i)
                if not item:
                    continue
                if is_current_week and (i - 5 == current_weekday):
                    item.setBackground(QColor(COLORS["table_info_bg"]))
                    item.setForeground(QColor(COLORS["primary_dark"]))
                    item.setText(headers[i])
                    f = QFont()
                    f.setBold(True)
                    f.setPointSize(11)
                    item.setFont(f)
                else:
                    item.setBackground(QColor(COLORS["bg_light"]))
                    item.setForeground(QColor(COLORS["text_dark"]))
                    item.setText(headers[i])
                    f = QFont()
                    f.setBold(True)
                    item.setFont(f)

    def _on_email_clicked(self):
        if not self.last_results:
            return
        try:
            import win32com.client

            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            start_date, end_date, start_dt = self._get_selected_week_range()

            # Calcolo numero settimana
            week_num = start_dt.isocalendar()[1]
            mail.Subject = f"Programmazione Settimanale - Settimana {week_num} ({start_date} - {end_date})"

            unique_reqs = {r["richiedente"] for r in self.last_results}
            recipients = []
            for r in unique_reqs:
                if r and len(r.split()) >= 2:
                    parts = r.split()
                    # Destinatari: rimuovi punti (fcaldarella invece di f.caldarella)
                    email_prefix = f"{parts[1][0].lower()}{parts[0].lower()}"
                    recipients.append(f"{email_prefix}@isab.com")

            from src.core.constants import Emails

            mail.To = "; ".join(recipients)
            mail.CC = Emails.PROG_CC

            # Check se siamo nella settimana corrente per evidenziazione oggi
            is_current_week = getattr(self, "week_selector", None) and self.week_selector.currentIndex() == 0
            today_idx = datetime.now().weekday() if is_current_week else -1

            # Template HTML Moderno e Professionale (Larghezza Dinamica)
            html = f"""
            <div style='font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif; color: {COLORS["text_dark"]}; padding: 20px; line-height: 1.5;'>
                <h2 style='color: {COLORS["primary_dark"]}; border-bottom: 2px solid {COLORS["border_light"]}; padding-bottom: 15px; font-size: 24px; margin-top: 0;'>
                    Programmazione Settimanale
                </h2>
                <p style='font-size: 16px; margin-bottom: 20px;'>
                    Periodo: <span style='color: {COLORS["primary_dark"]}; font-weight: bold;'>{{start_date}} - {{end_date}}</span>
                    <span style='color: {COLORS["text_muted"]}; margin-left: 10px;'>(Settimana {{week_num}})</span>
                </p>

                <table style='border-collapse: collapse; min-width: 600px; width: auto; font-size: 14px; box-shadow: 0 4px 6px {hex_to_rgba(COLORS["text_dark"], 0.05)}; border: 1px solid {COLORS["border_light"]};'>
                    <thead>
                        <tr style='background-color: {COLORS["bg_light"]}; color: {COLORS["text_dark"]}; text-align: center;'>
                            <th style='padding: 12px 15px; border: 1px solid {COLORS["border_light"]};'>Richiedente</th>
                            <th style='padding: 12px 15px; border: 1px solid {COLORS["border_light"]};'>Area</th>
                            <th style='padding: 12px 15px; border: 1px solid {COLORS["border_light"]};'>Unità</th>
                            <th style='padding: 12px 15px; border: 1px solid {COLORS["border_light"]}; text-align: center;'>PdL</th>
                            <th style='padding: 12px 15px; border: 1px solid {COLORS["border_light"]};'>Descrizione</th>
                            {{headers_html}}
                        </tr>
                    </thead>
                    <tbody>
            """

            day_names = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
            headers_html = ""
            for i, day in enumerate(day_names):
                style = f"padding: 12px 10px; border: 1px solid {COLORS['border_light']}; text-align: center; min-width: 65px;"
                if i == today_idx:
                    style += f" background-color: {COLORS['table_info_bg']}; color: {COLORS['primary_dark']}; font-weight: bold; border-bottom: 3px solid {COLORS['primary_dark']};"
                headers_html += f"<th style='{style}'>{day}</th>"

            html = html.format(
                start_date=start_date,
                end_date=end_date,
                week_num=week_num,
                headers_html=headers_html,
            )

            for res in self.last_results:
                html += "<tr>"
                html += f"<td style='padding: 12px 15px; border: 1px solid {COLORS['border_light']}; white-space: nowrap;'>{res['richiedente']}</td>"
                html += f"<td style='padding: 12px 15px; border: 1px solid {COLORS['border_light']}; color: {COLORS['text_muted']};'>{res.get('area', '')}</td>"
                html += f"<td style='padding: 12px 15px; border: 1px solid {COLORS['border_light']}; color: {COLORS['text_muted']};'>{res.get('unita', '')}</td>"
                html += f"<td style='padding: 12px; border: 1px solid {COLORS['border_light']}; text-align: center;'><b>{res['pdl']}</b></td>"
                html += f"<td style='padding: 12px 15px; border: 1px solid {COLORS['border_light']}; color: {COLORS['text_muted']};'>{res.get('descrizione', '')}</td>"

                for i, prog in enumerate(res["programmazione"]):
                    tcl_val = prog["tcl"]
                    tgo_val = prog["tgo"]

                    bg_color = COLORS["bg_white"]
                    if tcl_val or tgo_val:
                        bg_color = COLORS["bg_success_pastel"]  # Verde chiarissimo attività

                    if i == today_idx:
                        bg_color = COLORS["bg_info_pastel"]  # Azzurro oggi

                    tcl_style = f"color: {COLORS['success_dark'] if tcl_val else COLORS['error_red']}; font-weight: {'bold' if tcl_val else 'normal'};"
                    tgo_style = f"color: {COLORS['success_dark'] if tcl_val else COLORS['error_red']}; font-weight: {'bold' if tcl_val else 'normal'};"

                    html += f"<td align='center' style='padding: 10px; border: 1px solid {COLORS['border_light']}; background-color: {bg_color}; font-size: 13px;'>"
                    html += f"<span style='{tcl_style}'>TCL</span><br><span style='{tgo_style}'>TGO</span>"
                    html += "</td>"
                html += "</tr>"

            html += """
                    </tbody>
                </table>
            </div>
            """

            mail.HTMLBody = html + mail.HTMLBody
            mail.Display()
            ToastManager.instance().show("Bozza Outlook creata!", "success")
        except Exception as e:
            ToastManager.instance().show(f"Errore Outlook: {e}", "error")
